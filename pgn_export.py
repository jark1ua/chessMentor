"""
PGN game recorder with embedded coach annotations.

Usage
-----
recorder = GameRecorder("Alice", "white")
# each time a new board position is detected:
recorder.record_position(board, coach_comment="Nice development!")
recorder.set_result("1-0")
pgn_str = recorder.export_pgn()
recorder.save("/tmp/my_game.pgn")
"""
from __future__ import annotations

import io
from datetime import datetime
from typing import Optional

import chess
import chess.pgn


class GameRecorder:
    """Records a chess game progressively, adding coach comments as PGN annotations."""

    def __init__(self, player_username: str = "Player", player_color: str = "white"):
        self.game = chess.pgn.Game()
        self.game.headers["Event"] = "ChessMentor Session"
        self.game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
        self.game.headers["White"] = player_username if player_color == "white" else "Opponent"
        self.game.headers["Black"] = player_username if player_color == "black" else "Opponent"
        self.game.headers["Result"] = "*"
        self._node: chess.pgn.GameNode = self.game
        self._prev_board: Optional[chess.Board] = None
        self.move_count = 0

    def record_position(self, board: chess.Board, coach_comment: Optional[str] = None) -> bool:
        """
        Detect the move played since the last call and record it.
        Returns True if a move was recorded, False if position unchanged or
        no single legal move explains the change.
        """
        if self._prev_board is None:
            self._prev_board = board.copy()
            if coach_comment:
                self.game.comment = coach_comment
            return False

        if board.board_fen() == self._prev_board.board_fen():
            return False

        move = _detect_move(self._prev_board, board)
        if move is None:
            self._prev_board = board.copy()
            return False

        self._node = self._node.add_variation(move)
        if coach_comment:
            self._node.comment = coach_comment
        self._prev_board = board.copy()
        self.move_count += 1
        return True

    def set_result(self, result: str) -> None:
        valid = {"1-0", "0-1", "1/2-1/2", "*"}
        r = result.strip() if result.strip() in valid else "*"
        self.game.headers["Result"] = r
        # Walk to the last node and set result comment
        node = self._node
        while node.variations:
            node = node.variations[0]

    def export_pgn(self) -> str:
        buf = io.StringIO()
        exporter = chess.pgn.FileExporter(buf)
        self.game.accept(exporter)
        return buf.getvalue()

    def save(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.export_pgn())


def _detect_move(prev: chess.Board, curr: chess.Board) -> Optional[chess.Move]:
    """Return the legal move on *prev* that produces *curr*'s piece layout, or None."""
    target_fen = curr.board_fen()
    for move in prev.legal_moves:
        candidate = prev.copy()
        candidate.push(move)
        if candidate.board_fen() == target_fen:
            return move
    return None
