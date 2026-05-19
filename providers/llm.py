"""
LLM provider abstraction for chess coaching conversations.

Backends:
  - ClaudeLLM  : Anthropic Claude — tool use + prompt caching
  - OpenAILLM  : OpenAI GPT — function calling
  - OllamaLLM  : local Ollama — JSON text fallback (no native tool use)

Every provider exposes two methods:
  chat(system, messages)               -> str          (plain, no tools)
  chat_with_tools(system, messages, tools) -> (str, dict|None)
      Returns (coaching_text, tool_input_dict_or_None).
      tool_input_dict is the parsed arguments from the first tool call,
      or None if no tool call was made.
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
# Factory
# ---------------------------------------------------------------------------

def get_llm_provider(config: dict) -> LLMProvider:
    provider = config.get("llm_provider", "claude")

    if provider == "openai":
        return OpenAILLM(
            api_key=config.get("openai_api_key", ""),
            model=config.get("openai_llm_model", "gpt-4o"),
        )
    elif provider == "ollama":
        return OllamaLLM(
            base_url=config.get("ollama_base_url", "http://localhost:11434"),
            model=config.get("ollama_model", "llama3"),
        )
    else:  # "claude"
        return ClaudeLLM(
            api_key=config.get("anthropic_api_key", ""),
            model=config.get("claude_model", "claude-opus-4-7"),
        )
