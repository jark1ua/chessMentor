"""
Vision provider abstraction for chess board position extraction from images.

Backends:
  - ClaudeVision: uses Anthropic Claude (original logic)
  - OpenAIVision: uses OpenAI GPT-4o
  - GeminiVision: uses Google Gemini

Factory: get_vision_provider(config) -> VisionProvider
"""
import re
import json
import base64
from abc import ABC, abstractmethod
from typing import Optional, Tuple

import chess

_VISION_PROMPT = """\
You are a chess position recognizer. The user has provided a screenshot that
may contain a chess board.

Your task:
1. Identify whether a chess board is visible in the image.
2. If yes, determine the position of all pieces and return the FEN string for
   that position (piece placement only — you may omit castling/en-passant/clocks
   if you cannot reliably determine them, but include the active color if you
   can tell whose turn it is).
3. Also identify the player color at the bottom of the board (white or black).
4. If no board is visible or the position is unclear, respond with: NO_BOARD

Respond ONLY in this JSON format (no markdown, no explanation):
{"fen": "<FEN or NO_BOARD>", "bottom_color": "<white|black|unknown>"}
"""


def _parse_vision_response(raw: str) -> Tuple[Optional[chess.Board], str]:
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        return None, "unknown"
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return None, "unknown"

    fen = data.get("fen", "NO_BOARD")
    bottom_color = data.get("bottom_color", "unknown")

    if fen == "NO_BOARD" or not fen:
        return None, bottom_color

    try:
        parts = fen.split()
        if len(parts) == 1:
            fen = fen + " w - - 0 1"
        board = chess.Board(fen)
        return board, bottom_color
    except ValueError:
        return None, bottom_color


class VisionProvider(ABC):
    @abstractmethod
    def extract_position(self, image_b64: str) -> Tuple[Optional[chess.Board], str]:
        """
        Returns (board, bottom_color) or (None, 'unknown') if no board found.
        bottom_color is 'white', 'black', or 'unknown'.
        """


class ClaudeVision(VisionProvider):
    def __init__(self, api_key: str, model: str):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self._api_key)
        return self._client

    def extract_position(self, image_b64: str) -> Tuple[Optional[chess.Board], str]:
        client = self._get_client()
        response = client.messages.create(
            model=self._model,
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": _VISION_PROMPT},
                    ],
                }
            ],
        )
        raw = response.content[0].text.strip()
        return _parse_vision_response(raw)


class OpenAIVision(VisionProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            import openai
            self._client = openai.OpenAI(api_key=self._api_key)
        return self._client

    def extract_position(self, image_b64: str) -> Tuple[Optional[chess.Board], str]:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self._model,
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}",
                            },
                        },
                        {"type": "text", "text": _VISION_PROMPT},
                    ],
                }
            ],
        )
        raw = response.choices[0].message.content.strip()
        return _parse_vision_response(raw)


class GeminiVision(VisionProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            import google.generativeai as genai
            genai.configure(api_key=self._api_key)
            self._client = genai.GenerativeModel(self._model)
        return self._client

    def extract_position(self, image_b64: str) -> Tuple[Optional[chess.Board], str]:
        import google.generativeai as genai
        client = self._get_client()
        image_data = base64.b64decode(image_b64)
        blob = {"mime_type": "image/png", "data": image_data}
        response = client.generate_content([_VISION_PROMPT, blob])
        raw = response.text.strip()
        return _parse_vision_response(raw)


def get_vision_provider(config: dict) -> VisionProvider:
    """
    Factory returning the appropriate vision provider.

    config["vision_provider"] = "claude" | "openai" | "gemini"
    """
    provider = config.get("vision_provider", "claude")

    if provider == "openai":
        return OpenAIVision(
            api_key=config.get("openai_api_key", ""),
            model=config.get("openai_vision_model", "gpt-4o"),
        )
    elif provider == "gemini":
        return GeminiVision(
            api_key=config.get("gemini_api_key", ""),
            model=config.get("gemini_vision_model", "gemini-1.5-flash"),
        )
    else:  # "claude"
        return ClaudeVision(
            api_key=config.get("anthropic_api_key", ""),
            model=config.get("claude_model", "claude-opus-4-7"),
        )
