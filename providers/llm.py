"""
LLM provider abstraction for chess coaching conversations.

Backends:
  - ClaudeLLM: uses Anthropic Claude
  - OpenAILLM: uses OpenAI GPT
  - OllamaLLM: calls local Ollama server

Factory: get_llm_provider(config) -> LLMProvider
"""
from abc import ABC, abstractmethod
from typing import List, Dict


class LLMProvider(ABC):
    @abstractmethod
    def chat(self, system: str, messages: List[Dict]) -> str:
        """
        Send a conversation to the LLM.

        Args:
            system: System prompt string.
            messages: List of {"role": "user"|"assistant", "content": str} dicts.

        Returns:
            The model's reply as a plain string.
        """


class ClaudeLLM(LLMProvider):
    def __init__(self, api_key: str, model: str):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self._api_key)
        return self._client

    def chat(self, system: str, messages: List[Dict]) -> str:
        client = self._get_client()
        response = client.messages.create(
            model=self._model,
            max_tokens=512,
            system=system,
            messages=messages,
        )
        return response.content[0].text.strip()


class OpenAILLM(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            import openai
            self._client = openai.OpenAI(api_key=self._api_key)
        return self._client

    def chat(self, system: str, messages: List[Dict]) -> str:
        client = self._get_client()
        openai_messages = [{"role": "system", "content": system}] + messages
        response = client.chat.completions.create(
            model=self._model,
            max_tokens=512,
            messages=openai_messages,
        )
        return response.choices[0].message.content.strip()


class OllamaLLM(LLMProvider):
    def __init__(self, base_url: str, model: str):
        self._base_url = base_url.rstrip("/")
        self._model = model

    def chat(self, system: str, messages: List[Dict]) -> str:
        import requests
        ollama_messages = [{"role": "system", "content": system}] + messages
        resp = requests.post(
            f"{self._base_url}/api/chat",
            json={"model": self._model, "messages": ollama_messages, "stream": False},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"].strip()


def get_llm_provider(config: dict) -> LLMProvider:
    """
    Factory returning the appropriate LLM provider.

    config["llm_provider"] = "claude" | "openai" | "ollama"
    """
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
