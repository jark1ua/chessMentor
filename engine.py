"""
Stockfish integration via python-chess.
"""
from typing import Optional, List, Dict, Any
import chess
import chess.engine
from config import STOCKFISH_PATH, ENGINE_DEPTH, ENGINE_TOP_MOVES

_engine: Optional[chess.engine.SimpleEngine] = None


def get_engine() -> chess.engine.SimpleEngine:
    global _engine
    if _engine is None:
        _engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    return _engine


def close_engine():
    global _engine
    if _engine is not None:
        _engine.quit()
        _engine = None


def analyse(board: chess.Board) -> Dict[str, Any]:
    """
    Return a dict with:
      - score_cp: centipawn score from white's perspective (None if mate)
      - mate_in: move number if forced mate, else None
      - top_moves: list of {"move": uci, "san": san, "score_cp": int}
      - best_move: SAN string of the top move
    """
    engine = get_engine()

    info = engine.analyse(
        board,
        chess.engine.Limit(depth=ENGINE_DEPTH),
        multipv=ENGINE_TOP_MOVES,
    )

    result: Dict[str, Any] = {
        "score_cp": None,
        "mate_in": None,
        "top_moves": [],
        "best_move": None,
    }

    for i, pv_info in enumerate(info):
        score = pv_info["score"].white()
        cp = score.score()          # None if mate
        mate = score.mate()         # None if not forced mate

        if i == 0:
            result["score_cp"] = cp
            result["mate_in"] = mate
            if pv_info.get("pv"):
                best_uci = pv_info["pv"][0]
                result["best_move"] = board.san(best_uci)

        if pv_info.get("pv"):
            move = pv_info["pv"][0]
            san = board.san(move)
            entry: Dict[str, Any] = {"move": move.uci(), "san": san}
            if cp is not None:
                entry["score_cp"] = cp
            elif mate is not None:
                entry["score_cp"] = 100000 * (1 if mate > 0 else -1)
            result["top_moves"].append(entry)

    return result


def eval_delta(prev_cp: Optional[int], curr_cp: Optional[int], player_is_white: bool) -> int:
    """
    Returns how many centipawns the current player *lost* since the previous
    evaluation.  Positive = the player made a mistake, negative = improvement.
    Handles None (mate scores) by substituting ±9999.
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
