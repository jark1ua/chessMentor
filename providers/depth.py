"""
Adaptive Stockfish depth computation based on player profile and board state.
"""
import chess
from typing import Optional


def _material_count(board: chess.Board) -> int:
    """Return total material on the board in centipawn units (approximate)."""
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }
    total = 0
    for piece_type, value in piece_values.items():
        total += len(board.pieces(piece_type, chess.WHITE)) * value
        total += len(board.pieces(piece_type, chess.BLACK)) * value
    return total


def _game_phase(board: chess.Board) -> str:
    """Return 'opening', 'middlegame', or 'endgame'."""
    material = _material_count(board)
    if board.fullmove_number <= 12 and material >= 50:
        return "opening"
    if material < 26:
        return "endgame"
    return "middlegame"


def adaptive_depth(profile: dict, board: chess.Board) -> int:
    """Compute adaptive Stockfish search depth based on player profile and position."""
    rating: Optional[int] = profile.get("rating_estimate")

    # Rating-based base depth
    if rating is None or rating < 800:
        base = 3
    elif rating < 1200:
        base = 5
    elif rating < 1500:
        base = 8
    elif rating < 1800:
        base = 10
    elif rating < 2200:
        base = 13
    else:
        base = 15

    # Game phase modifier
    phase = _game_phase(board)
    if phase == "opening":
        modifier = -1
    elif phase == "endgame":
        modifier = 2
    else:
        modifier = 0

    depth = base + modifier
    return max(3, min(15, depth))


def depth_rationale(profile: dict, board: chess.Board) -> str:
    """Return a human-readable explanation of the chosen depth."""
    rating: Optional[int] = profile.get("rating_estimate")
    rating_str = str(rating) if rating is not None else "unknown"

    if rating is None or rating < 800:
        base = 3
        rating_band = "unknown/<800"
    elif rating < 1200:
        base = 5
        rating_band = "800-1199"
    elif rating < 1500:
        base = 8
        rating_band = "1200-1499"
    elif rating < 1800:
        base = 10
        rating_band = "1500-1799"
    elif rating < 2200:
        base = 13
        rating_band = "1800-2199"
    else:
        base = 15
        rating_band = "2200+"

    phase = _game_phase(board)
    if phase == "opening":
        modifier = -1
        phase_note = "opening (-1)"
    elif phase == "endgame":
        modifier = 2
        phase_note = "endgame (+2)"
    else:
        modifier = 0
        phase_note = "middlegame (+0)"

    final = max(3, min(15, base + modifier))
    return (
        f"Depth {final}: rating {rating_str} (band {rating_band} -> base {base}), "
        f"phase {phase_note}, capped to [{3}, {15}]"
    )
