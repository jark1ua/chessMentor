"""
OCR-based clock reading.

Optional dependency: pytesseract + Tesseract binary.
All functions degrade gracefully if unavailable — callers receive None.
"""
from __future__ import annotations
from typing import Optional

try:
    import pytesseract
    _TESS_AVAILABLE = True
except ImportError:
    _TESS_AVAILABLE = False


def read_clock(image) -> Optional[str]:
    """
    Extract time text (e.g. '5:23') from a PIL Image of the clock region.
    Returns a string like 'M:SS' / 'MM:SS', or None.
    """
    if not _TESS_AVAILABLE:
        return None
    try:
        text = pytesseract.image_to_string(
            image,
            config="--psm 7 -c tessedit_char_whitelist=0123456789:",
        ).strip()
        if ":" in text and 3 <= len(text) <= 5:
            return text
        return None
    except Exception:
        return None


def parse_seconds(time_str: str) -> Optional[int]:
    """Convert 'M:SS' or 'MM:SS' to total seconds."""
    try:
        parts = time_str.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        return None
    except (ValueError, IndexError):
        return None


def is_time_pressure(time_str: str, threshold_seconds: int = 120) -> bool:
    """Return True if remaining time is below threshold_seconds."""
    seconds = parse_seconds(time_str)
    if seconds is None:
        return False
    return seconds < threshold_seconds
