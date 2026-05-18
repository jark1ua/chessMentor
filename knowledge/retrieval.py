"""
Retrieval logic for chess knowledge base principles.

Functions:
  get_relevant_principles(board, profile, n) -> list[dict]
  format_principles_for_prompt(principles) -> str
"""
from typing import List, Set
import chess

from knowledge.principles import PRINCIPLES


# ---------------------------------------------------------------------------
# Board feature detection
# ---------------------------------------------------------------------------

def _material_points(board: chess.Board) -> int:
    """Total material (pawns=1, N/B=3, R=5, Q=9) for both sides."""
    values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
               chess.ROOK: 5, chess.QUEEN: 9}
    total = 0
    for pt, v in values.items():
        total += (len(board.pieces(pt, chess.WHITE)) + len(board.pieces(pt, chess.BLACK))) * v
    return total


def _detect_game_phase(board: chess.Board) -> str:
    material = _material_points(board)
    if board.fullmove_number <= 12 and material >= 50:
        return "opening"
    if material < 26:
        return "endgame"
    return "middlegame"


def _has_passed_pawn(board: chess.Board) -> bool:
    for color in (chess.WHITE, chess.BLACK):
        for sq in board.pieces(chess.PAWN, color):
            file = chess.square_file(sq)
            rank = chess.square_rank(sq)
            opp_color = not color
            passed = True
            if color == chess.WHITE:
                ahead = range(rank + 1, 8)
            else:
                ahead = range(rank - 1, -1, -1)
            for r in ahead:
                for f in [file - 1, file, file + 1]:
                    if 0 <= f <= 7:
                        s = chess.square(f, r)
                        if board.piece_at(s) and board.piece_at(s).piece_type == chess.PAWN \
                                and board.piece_at(s).color == opp_color:
                            passed = False
                            break
                if not passed:
                    break
            if passed:
                return True
    return False


def _has_open_file(board: chess.Board) -> bool:
    for f in range(8):
        white_pawns = any(
            board.piece_at(chess.square(f, r)) and
            board.piece_at(chess.square(f, r)).piece_type == chess.PAWN and
            board.piece_at(chess.square(f, r)).color == chess.WHITE
            for r in range(8)
        )
        black_pawns = any(
            board.piece_at(chess.square(f, r)) and
            board.piece_at(chess.square(f, r)).piece_type == chess.PAWN and
            board.piece_at(chess.square(f, r)).color == chess.BLACK
            for r in range(8)
        )
        if not white_pawns and not black_pawns:
            return True
    return False


def _has_bishop_vs_knight(board: chess.Board) -> bool:
    w_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
    w_knights = len(board.pieces(chess.KNIGHT, chess.WHITE))
    b_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))
    b_knights = len(board.pieces(chess.KNIGHT, chess.BLACK))
    return (w_bishops > 0 and b_knights > 0 and b_bishops == 0) or \
           (b_bishops > 0 and w_knights > 0 and w_bishops == 0)


def _has_two_bishops(board: chess.Board) -> bool:
    return len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2 or \
           len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2


def _king_uncastled(board: chess.Board) -> bool:
    """Return True if either king appears to not have castled (simple heuristic: still on e-file)."""
    wk = board.king(chess.WHITE)
    bk = board.king(chess.BLACK)
    return (wk is not None and chess.square_file(wk) == 4 and chess.square_rank(wk) == 0) or \
           (bk is not None and chess.square_file(bk) == 4 and chess.square_rank(bk) == 7)


def _detect_position_tags(board: chess.Board, phase: str) -> Set[str]:
    """Return a set of tag strings describing features present in the position."""
    tags: Set[str] = {phase}

    if _has_passed_pawn(board):
        tags.add("passed_pawn")
        tags.add("promotion")
    if _has_open_file(board):
        tags.add("open_file")
        tags.add("rook")
    if _has_bishop_vs_knight(board):
        tags.add("bishop_vs_knight")
        tags.add("imbalance")
    if _has_two_bishops(board):
        tags.add("two_bishops")
        tags.add("bishop_pair")
    if _king_uncastled(board):
        tags.add("uncastled_king")
        tags.add("king_safety")
        tags.add("castling")

    material = _material_points(board)
    if material < 40:
        tags.add("endgame")
        tags.add("king_activity")
        tags.add("rook_endgame")

    # Always relevant tactical awareness
    tags.add("candidate_moves")
    tags.add("blunder_check")

    return tags


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _score_principle(principle: dict, position_tags: Set[str], phase: str,
                     seen_ids: Set[str]) -> int:
    """Return a relevance score (higher = more relevant)."""
    score = 0

    # Theme match
    if principle["theme"] == phase:
        score += 10
    elif principle["theme"] in ("tactics", "strategy"):
        score += 3

    # Tag overlap
    p_tags = set(principle.get("tags", []))
    overlap = len(p_tags & position_tags)
    score += overlap * 5

    # Novelty bonus
    if principle["id"] not in seen_ids:
        score += 8

    return score


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_relevant_principles(board: chess.Board, profile: dict, n: int = 3) -> List[dict]:
    """
    Return the top-n most relevant principles for the current board and player profile.

    1. Detects game phase and position features.
    2. Scores each principle by theme/tag overlap and novelty.
    3. Returns top n principles.
    """
    phase = _detect_game_phase(board)
    position_tags = _detect_position_tags(board, phase)

    lessons = profile.get("lessons", [])
    seen_ids: Set[str] = set()
    # Treat lesson text substrings as a rough proxy for seen principles
    for p in PRINCIPLES:
        if any(p["id"] in lesson for lesson in lessons):
            seen_ids.add(p["id"])

    scored = [
        (p, _score_principle(p, position_tags, phase, seen_ids))
        for p in PRINCIPLES
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in scored[:n]]


def format_principles_for_prompt(principles: List[dict]) -> str:
    """Format a list of principles as a readable block for injection into a system prompt."""
    if not principles:
        return ""
    lines = ["--- Relevant Chess Principles ---"]
    for p in principles:
        lines.append(f"\n[{p['source']}] {p['title']}")
        lines.append(p["principle"])
    lines.append("--- End of Principles ---")
    return "\n".join(lines)
