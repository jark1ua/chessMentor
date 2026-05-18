"""
Stockfish / engine integration.

Thin wrapper that delegates to the configured engine provider.
Also re-exports eval_delta and score_label for backward compatibility.
"""
from typing import Optional, Dict, Any

import chess

from providers.engine import get_engine, LocalStockfish, LichessCloud

# Module-level provider — set by main.py at startup, or lazily built from env.
_provider = None
_profile: dict = {}


def set_provider(provider, profile: dict) -> None:
    """Set the engine provider and profile (called from main.py at startup)."""
    global _provider, _profile
    _provider = provider
    _profile = profile


def _get_provider():
    global _provider
    if _provider is None:
        from config import STOCKFISH_PATH, ENGINE_TOP_MOVES, ENGINE_PROVIDER
        cfg = {
            "stockfish_path": STOCKFISH_PATH,
            "engine_top_moves": ENGINE_TOP_MOVES,
            "engine_provider": ENGINE_PROVIDER,
        }
        _provider = get_engine(_profile, cfg)
    return _provider


def analyse(board: chess.Board) -> Dict[str, Any]:
    """Analyse the board and return the standard result dict."""
    return _get_provider().analyse(board, _profile)


def close_engine():
    """Shut down the engine cleanly."""
    global _provider
    if _provider is not None:
        try:
            _provider.close()
        except Exception:
            pass
        _provider = None


def eval_delta(prev_cp: Optional[int], curr_cp: Optional[int],
               player_is_white: bool) -> int:
    """
    Centipawns lost by the current player since the previous evaluation.
    Positive = mistake, negative = improvement.
    """
    if prev_cp is None:
        prev_cp = 9999
    if curr_cp is None:
        curr_cp = 9999

    if player_is_white:
        return prev_cp - curr_cp
    else:
        return curr_cp - prev_cp


def score_label(cp: Optional[int], mate: Optional[int]) -> str:
    if mate is not None:
        return f"Mate in {abs(mate)}" if mate > 0 else f"Mate in {abs(mate)} (for Black)"
    if cp is None:
        return "unknown"
    pawns = cp / 100.0
    sign = "+" if pawns >= 0 else ""
    return f"{sign}{pawns:.2f}"
