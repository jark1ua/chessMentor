"""
LLM provider abstraction for chess coaching conversations.

Backends
--------
  ClaudeLLM      Anthropic Claude — tool use + prompt caching
  OpenAILLM      OpenAI GPT — function calling
  OpenRouterLLM  openrouter.ai — single key, 200+ models, OpenAI-compatible
                 Recommended free/cheap models:
                   deepseek/deepseek-chat          (DeepSeek-V3, near-free)
                   deepseek/deepseek-r1            (reasoning, very cheap)
                   meta-llama/llama-3.3-70b-instruct (free tier available)
                   mistralai/mistral-7b-instruct   (free tier)
                   google/gemini-flash-1.5         (cheap)
  DeepSeekLLM    DeepSeek direct API — OpenAI-compatible, extremely low cost
  OllamaLLM      local Ollama — JSON text fallback (no native tool use)
  FallbackLLM    Tries providers in order; moves to the next on any error.
                 Use this to maximise uptime and manage costs automatically.

Every provider exposes two methods:
  chat(system, messages)                   -> str
  chat_with_tools(system, messages, tools) -> (str, dict|None)
      coaching_text : prose reply
      tool_input    : parsed tool-call arguments dict, or None
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any


class LLMProvider(ABC):

    @abstractmethod
    def chat(self, system: str, messages: List[Dict]) -> str:
        """Plain chat — no tool use."""

    @abstractmethod
    def chat_with_tools(
        self,
        system: str,
        messages: List[Dict],
        tools: List[Dict],
    ) -> Tuple[str, Optional[Dict]]:
        """
        Chat with tool use support.

        Returns:
            (coaching_text, tool_input)
            coaching_text : the model's prose reply
            tool_input    : dict of tool arguments if the model called a tool,
                            else None
        """


# ---------------------------------------------------------------------------
# Claude
# ---------------------------------------------------------------------------

class ClaudeLLM(LLMProvider):
    """
    Anthropic Claude backend.

    Features:
    - Prompt caching via cache_control on the system prompt — the large
      system prompt (profile + principles) is cached for ~5 minutes,
      saving input tokens on repeated calls within a session.
    - Native tool use: profile updates arrive as structured tool_use blocks,
      not fragile text parsing.
    """

    def __init__(self, api_key: str, model: str):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self._api_key)
        return self._client

    def _anthropic_tools(self, tools: List[Dict]) -> List[Dict]:
        """Convert generic tool dicts to Anthropic's expected format."""
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "input_schema": t["input_schema"],
            }
            for t in tools
        ]

    def chat(self, system: str, messages: List[Dict]) -> str:
        client = self._get_client()
        response = client.messages.create(
            model=self._model,
            max_tokens=512,
            # Cache the large system prompt
            system=[
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
        )
        return response.content[0].text.strip()

    def chat_with_tools(
        self,
        system: str,
        messages: List[Dict],
        tools: List[Dict],
    ) -> Tuple[str, Optional[Dict]]:
        client = self._get_client()
        response = client.messages.create(
            model=self._model,
            max_tokens=600,
            system=[
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
            tools=self._anthropic_tools(tools),
            # Require the model to call the tool — eliminates forgetting
            tool_choice={"type": "auto"},
        )

        coaching_text = ""
        tool_input: Optional[Dict] = None

        for block in response.content:
            if block.type == "text":
                coaching_text = block.text.strip()
            elif block.type == "tool_use":
                tool_input = block.input  # already a dict

        return coaching_text, tool_input


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------

class OpenAILLM(LLMProvider):
    """OpenAI GPT backend with function calling."""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            import openai
            self._client = openai.OpenAI(api_key=self._api_key)
        return self._client

    def _openai_functions(self, tools: List[Dict]) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t["input_schema"],
                },
            }
            for t in tools
        ]

    def chat(self, system: str, messages: List[Dict]) -> str:
        client = self._get_client()
        oai_msgs = [{"role": "system", "content": system}] + messages
        response = client.chat.completions.create(
            model=self._model,
            max_tokens=512,
            messages=oai_msgs,
        )
        return response.choices[0].message.content.strip()

    def chat_with_tools(
        self,
        system: str,
        messages: List[Dict],
        tools: List[Dict],
    ) -> Tuple[str, Optional[Dict]]:
        client = self._get_client()
        oai_msgs = [{"role": "system", "content": system}] + messages
        response = client.chat.completions.create(
            model=self._model,
            max_tokens=600,
            messages=oai_msgs,
            tools=self._openai_functions(tools),
            tool_choice="auto",
        )

        msg = response.choices[0].message
        coaching_text = (msg.content or "").strip()
        tool_input: Optional[Dict] = None

        if msg.tool_calls:
            try:
                tool_input = json.loads(msg.tool_calls[0].function.arguments)
            except (json.JSONDecodeError, IndexError):
                tool_input = None

        return coaching_text, tool_input


# ---------------------------------------------------------------------------
# Ollama
# ---------------------------------------------------------------------------

class OllamaLLM(LLMProvider):
    """
    Local Ollama backend.

    Tool use is emulated: the system prompt is extended with an instruction
    to output a JSON block, which is then extracted by the caller as a
    fallback.  Most local models don't support structured tool calls reliably.
    """

    _TOOL_INSTRUCTION = (
        "\n\nAfter your coaching reply, output a JSON block on a single line "
        "starting with PROFILE_JSON: containing any of: lessons, weaknesses, "
        "strengths, opening {color, name}, coach_note. "
        "Example: PROFILE_JSON: {\"lessons\":[\"Always castle before move 10\"]}"
    )

    def __init__(self, base_url: str, model: str):
        self._base_url = base_url.rstrip("/")
        self._model = model

    def _post(self, messages: List[Dict]) -> str:
        import requests
        resp = requests.post(
            f"{self._base_url}/api/chat",
            json={"model": self._model, "messages": messages, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"].strip()

    def chat(self, system: str, messages: List[Dict]) -> str:
        ollama_messages = [{"role": "system", "content": system}] + messages
        return self._post(ollama_messages)

    def chat_with_tools(
        self,
        system: str,
        messages: List[Dict],
        tools: List[Dict],
    ) -> Tuple[str, Optional[Dict]]:
        augmented_system = system + self._TOOL_INSTRUCTION
        ollama_messages = [{"role": "system", "content": augmented_system}] + messages
        reply = self._post(ollama_messages)

        # Extract JSON from PROFILE_JSON: prefix
        tool_input: Optional[Dict] = None
        coaching_text = reply
        marker = "PROFILE_JSON:"
        if marker in reply:
            parts = reply.split(marker, 1)
            coaching_text = parts[0].strip()
            json_str = parts[1].strip().split("\n")[0]
            try:
                tool_input = json.loads(json_str)
            except json.JSONDecodeError:
                tool_input = None

        return coaching_text, tool_input


# ---------------------------------------------------------------------------
# OpenRouter — single API key, 200+ models, OpenAI-compatible wire format
# ---------------------------------------------------------------------------

class OpenRouterLLM(OpenAILLM):
    """
    openrouter.ai backend.

    Uses the OpenAI SDK pointed at https://openrouter.ai/api/v1.
    Model names follow the provider/model-slug convention, e.g.:
      deepseek/deepseek-chat
      deepseek/deepseek-r1
      meta-llama/llama-3.3-70b-instruct
      mistralai/mistral-7b-instruct
      google/gemini-flash-1.5
      anthropic/claude-opus-4-7
      openai/gpt-4o

    Free models (no cost): check https://openrouter.ai/models?q=free
    Tool use: supported for all models that declare it in their capabilities.
    """

    OPENROUTER_BASE = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str, model: str, site_url: str = "", app_name: str = "ChessMentor"):
        super().__init__(api_key=api_key, model=model)
        self._site_url = site_url
        self._app_name = app_name

    def _get_client(self):
        if self._client is None:
            import openai
            self._client = openai.OpenAI(
                api_key=self._api_key,
                base_url=self.OPENROUTER_BASE,
                default_headers={
                    "HTTP-Referer": self._site_url,
                    "X-Title": self._app_name,
                },
            )
        return self._client


# ---------------------------------------------------------------------------
# DeepSeek — direct API, OpenAI-compatible, extremely low cost
# ---------------------------------------------------------------------------

class DeepSeekLLM(OpenAILLM):
    """
    DeepSeek direct API (api.deepseek.com).

    Models:
      deepseek-chat    DeepSeek-V3 — general purpose, very cheap
      deepseek-reasoner  DeepSeek-R1 — chain-of-thought reasoning

    Pricing as of 2025: ~$0.014 / 1M input tokens (cache hit), ~$0.28 output.
    Effectively free for light coaching use.
    """

    DEEPSEEK_BASE = "https://api.deepseek.com/v1"

    def _get_client(self):
        if self._client is None:
            import openai
            self._client = openai.OpenAI(
                api_key=self._api_key,
                base_url=self.DEEPSEEK_BASE,
            )
        return self._client


# ---------------------------------------------------------------------------
# FallbackLLM — try providers in order, advance on any exception
# ---------------------------------------------------------------------------

class FallbackLLM(LLMProvider):
    """
    Wraps an ordered list of providers.  On any exception from the primary,
    logs a warning and tries the next.  Useful for:
      - Cost management (cheap model first, expensive as backup)
      - Uptime (API outage resilience)
      - Free tier exhaustion (OpenRouter free → DeepSeek → Claude)

    Example config:
      LLM_PROVIDER=fallback
      LLM_FALLBACK_CHAIN=openrouter,deepseek,claude
    """

    def __init__(self, providers: List[LLMProvider]):
        if not providers:
            raise ValueError("FallbackLLM requires at least one provider")
        self._providers = providers

    def _try(self, method_name: str, *args, **kwargs):
        last_exc: Optional[Exception] = None
        for p in self._providers:
            try:
                return getattr(p, method_name)(*args, **kwargs)
            except Exception as exc:
                import warnings
                warnings.warn(
                    f"[FallbackLLM] {type(p).__name__} failed ({exc}), trying next provider"
                )
                last_exc = exc
        raise RuntimeError(
            f"All LLM providers failed. Last error: {last_exc}"
        ) from last_exc

    def chat(self, system: str, messages: List[Dict]) -> str:
        return self._try("chat", system, messages)

    def chat_with_tools(
        self, system: str, messages: List[Dict], tools: List[Dict]
    ) -> Tuple[str, Optional[Dict]]:
        return self._try("chat_with_tools", system, messages, tools)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def _build_single(name: str, config: dict) -> LLMProvider:
    """Build one named provider from config."""
    name = name.strip().lower()
    if name == "openai":
        return OpenAILLM(
            api_key=config.get("openai_api_key", ""),
            model=config.get("openai_llm_model", "gpt-4o"),
        )
    elif name == "openrouter":
        return OpenRouterLLM(
            api_key=config.get("openrouter_api_key", ""),
            model=config.get("openrouter_model", "deepseek/deepseek-chat"),
            site_url=config.get("openrouter_site_url", ""),
            app_name=config.get("openrouter_app_name", "ChessMentor"),
        )
    elif name == "deepseek":
        return DeepSeekLLM(
            api_key=config.get("deepseek_api_key", ""),
            model=config.get("deepseek_model", "deepseek-chat"),
        )
    elif name == "ollama":
        return OllamaLLM(
            base_url=config.get("ollama_base_url", "http://localhost:11434"),
            model=config.get("ollama_model", "llama3"),
        )
    else:  # "claude" or default
        return ClaudeLLM(
            api_key=config.get("anthropic_api_key", ""),
            model=config.get("claude_model", "claude-opus-4-7"),
        )


def get_llm_provider(config: dict) -> LLMProvider:
    """
    Factory returning the appropriate LLM provider.

    LLM_PROVIDER accepts:
      claude | openai | openrouter | deepseek | ollama
      fallback  — uses LLM_FALLBACK_CHAIN (comma-separated list of the above)

    Examples:
      LLM_PROVIDER=openrouter
      OPENROUTER_API_KEY=sk-or-...
      OPENROUTER_MODEL=deepseek/deepseek-chat

      LLM_PROVIDER=fallback
      LLM_FALLBACK_CHAIN=openrouter,deepseek,claude
    """
    provider = config.get("llm_provider", "claude").strip().lower()

    if provider == "fallback":
        chain_str = config.get("llm_fallback_chain", "claude")
        chain_names = [n.strip() for n in chain_str.split(",") if n.strip()]
        providers = [_build_single(n, config) for n in chain_names]
        return FallbackLLM(providers)

    return _build_single(provider, config)
