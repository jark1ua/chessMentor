"""
Engine provider abstraction.

Backends:
  - LocalStockfish: uses python-chess + stockfish binary with adaptive depth
  - LichessCloud: calls the Lichess cloud eval API, falls back to local

Factory: get_engine(profile, config) -> engine provider instance
"""
import time
import threading
from typing import Optional, Dict, Any, List

import chess
import chess.engine
import requests

from providers.depth import adaptive_depth

# Shared result dict shape:
# {
#   "score_cp": int | None,
#   "mate_in": int | None,
#   "top_moves": [{"san": str, "score_cp": int}],
#   "best_move": str | None,
#   "source": "lichess" | "local",
# }


class LocalStockfish:
    """Stockfish engine using python-chess, with adaptive depth from user profile."""

    def __init__(self, stockfish_path: str, top_moves: int = 3):
        self._path = stockfish_path
        self._top_moves = top_moves
        self._engine: Optional[chess.engine.SimpleEngine] = None
        self._lock = threading.Lock()

    def _get_engine(self) -> chess.engine.SimpleEngine:
        with self._lock:
            if self._engine is None:
                self._engine = chess.engine.SimpleEngine.popen_uci(self._path)
            return self._engine

    def analyse(self, board: chess.Board, profile: dict) -> Dict[str, Any]:
        depth = adaptive_depth(profile, board)
        engine = self._get_engine()

        info = engine.analyse(
            board,
            chess.engine.Limit(depth=depth),
            multipv=self._top_moves,
        )

        result: Dict[str, Any] = {
            "score_cp": None,
            "mate_in": None,
            "top_moves": [],
            "best_move": None,
            "source": "local",
        }

        for i, pv_info in enumerate(info):
            score = pv_info["score"].white()
            cp = score.score()
            mate = score.mate()

            if i == 0:
                result["score_cp"] = cp
                result["mate_in"] = mate
                if pv_info.get("pv"):
                    result["best_move"] = board.san(pv_info["pv"][0])

            if pv_info.get("pv"):
                move = pv_info["pv"][0]
                san = board.san(move)
                entry: Dict[str, Any] = {"san": san}
                if cp is not None:
                    entry["score_cp"] = cp
                elif mate is not None:
                    entry["score_cp"] = 100000 * (1 if mate > 0 else -1)
                result["top_moves"].append(entry)

        return result

    def close(self):
        with self._lock:
            if self._engine is not None:
                try:
                    self._engine.quit()
                except Exception:
                    pass
                self._engine = None


class LichessCloud:
    """Lichess cloud evaluation API. Falls back to LocalStockfish on cache miss."""

    _ENDPOINT = "https://lichess.org/api/cloud-eval"
    _MIN_INTERVAL = 1.0  # seconds between requests (rate limit)

    def __init__(self, fallback: LocalStockfish, multi_pv: int = 3):
        self._fallback = fallback
        self._multi_pv = multi_pv
        self._last_request: float = 0.0
        self._lock = threading.Lock()

    def _throttle(self):
        with self._lock:
            now = time.time()
            wait = self._MIN_INTERVAL - (now - self._last_request)
            if wait > 0:
                time.sleep(wait)
            self._last_request = time.time()

    def analyse(self, board: chess.Board, profile: dict) -> Dict[str, Any]:
        self._throttle()
        fen = board.fen()
        try:
            resp = requests.get(
                self._ENDPOINT,
                params={"fen": fen, "multiPv": self._multi_pv},
                timeout=5,
            )
            if resp.status_code == 404:
                # Position not in cache — fall back to local
                result = self._fallback.analyse(board, profile)
                return result
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException:
            return self._fallback.analyse(board, profile)

        pvs: List[dict] = data.get("pvs", [])
        result: Dict[str, Any] = {
            "score_cp": None,
            "mate_in": None,
            "top_moves": [],
            "best_move": None,
            "source": "lichess",
        }

        for i, pv in enumerate(pvs):
            cp = pv.get("cp")
            mate = pv.get("mate")
            moves_uci = pv.get("moves", "").split()

            if i == 0:
                result["score_cp"] = cp
                result["mate_in"] = mate
                if moves_uci:
                    try:
                        move = chess.Move.from_uci(moves_uci[0])
                        result["best_move"] = board.san(move)
                    except Exception:
                        result["best_move"] = moves_uci[0]

            if moves_uci:
                try:
                    move = chess.Move.from_uci(moves_uci[0])
                    san = board.san(move)
                except Exception:
                    san = moves_uci[0]
                entry: Dict[str, Any] = {"san": san}
                if cp is not None:
                    entry["score_cp"] = cp
                elif mate is not None:
                    entry["score_cp"] = 100000 * (1 if mate > 0 else -1)
                result["top_moves"].append(entry)

        return result

    def close(self):
        self._fallback.close()


def get_engine(profile: dict, config: dict):
    """
    Factory returning the appropriate engine provider.

    config["engine_provider"] = "lichess" | "local" | "auto"
    """
    stockfish_path = config.get("stockfish_path", "stockfish")
    top_moves = config.get("engine_top_moves", 3)
    provider = config.get("engine_provider", "auto")

    local = LocalStockfish(stockfish_path, top_moves)

    if provider == "local":
        return local
    elif provider == "lichess":
        return LichessCloud(local, multi_pv=top_moves)
    else:  # "auto" — try lichess, fall back to local
        return LichessCloud(local, multi_pv=top_moves)
