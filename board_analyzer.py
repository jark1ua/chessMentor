"""
Board position extraction from a screenshot.

Thin wrapper that delegates to the configured VisionProvider.
For standalone/legacy use, defaults to ClaudeVision.
"""
from typing import Optional, Tuple
import chess

from providers.vision import get_vision_provider, VisionProvider

# Module-level provider — set by main.py at startup, or lazily built from env.
_provider: Optional[VisionProvider] = None


def set_provider(provider: VisionProvider) -> None:
    """Set the vision provider (called from main.py at startup)."""
    global _provider
    _provider = provider


def _get_provider() -> VisionProvider:
    global _provider
    if _provider is None:
        # Lazy fallback: build from environment config
        from config import (
            ANTHROPIC_API_KEY, CLAUDE_MODEL,
            OPENAI_API_KEY, OPENAI_VISION_MODEL,
            GEMINI_API_KEY, GEMINI_VISION_MODEL,
            VISION_PROVIDER,
        )
        cfg = {
            "vision_provider": VISION_PROVIDER,
            "anthropic_api_key": ANTHROPIC_API_KEY,
            "claude_model": CLAUDE_MODEL,
            "openai_api_key": OPENAI_API_KEY,
            "openai_vision_model": OPENAI_VISION_MODEL,
            "gemini_api_key": GEMINI_API_KEY,
            "gemini_vision_model": GEMINI_VISION_MODEL,
        }
        _provider = get_vision_provider(cfg)
    return _provider


def extract_position(image_b64: str) -> Tuple[Optional[chess.Board], str]:
    """
    Returns (board, bottom_color) or (None, 'unknown') if no board found.
    bottom_color is 'white', 'black', or 'unknown'.
    """
    return _get_provider().extract_position(image_b64)
