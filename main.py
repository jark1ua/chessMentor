"""
ChessMentor — real-time chess coaching via screen capture + Stockfish + Claude.

Usage:
    python main.py                    # start a coaching session
    python main.py --profile          # view / edit your player profile
    python main.py --history          # show match history summaries
    python main.py --set-name NAME    # set your username
    python main.py --set-rating N     # set estimated rating
"""
import sys
import time
import argparse
import signal
from typing import Optional

import chess

from config import CAPTURE_INTERVAL, COACHING_THRESHOLD, ANTHROPIC_API_KEY
from capture import select_region_interactively, capture, image_to_base64, save_debug_image
from board_analyzer import extract_position
from engine import analyse, eval_delta, score_label, close_engine
from coach import CoachSession
from profile import (
    load_profile, save_profile, append_match_summary,
    load_history, profile_summary_text
)

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    console = Console()
    def info(msg): console.print(f"[cyan]{msg}[/cyan]")
    def warn(msg): console.print(f"[yellow]{msg}[/yellow]")
    def coach_msg(msg): console.print(Panel(msg, title="[bold green]ChessMentor[/bold green]", expand=False))
    def err(msg): console.print(f"[bold red]{msg}[/bold red]")
except ImportError:
    def info(msg): print(f"[INFO] {msg}")
    def warn(msg): print(f"[WARN] {msg}")
    def coach_msg(msg): print(f"\n=== ChessMentor ===\n{msg}\n==================\n")
    def err(msg): print(f"[ERROR] {msg}")


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def cmd_show_profile():
    profile = load_profile()
    print("\n" + profile_summary_text(profile) + "\n")


def cmd_show_history():
    history = load_history()
    if not history:
        print("No match history yet.")
        return
    for i, entry in enumerate(history[-20:], 1):
        print(f"\n--- Match {i} [{entry.get('ts', '')[:10]}] ---")
        print(entry.get("summary", "(no summary)"))


def cmd_set_name(name: str):
    profile = load_profile()
    profile["username"] = name
    save_profile(profile)
    print(f"Username set to: {name}")


def cmd_set_rating(rating: int):
    profile = load_profile()
    profile["rating_estimate"] = rating
    save_profile(profile)
    print(f"Rating estimate set to: {rating}")


# ---------------------------------------------------------------------------
# Main session loop
# ---------------------------------------------------------------------------

class Session:
    def __init__(self, region, profile):
        self.region = region
        self.profile = profile
        self.coach_session = CoachSession(profile)
        self.prev_fen: Optional[str] = None
        self.prev_cp: Optional[int] = None
        self.prev_board: Optional[chess.Board] = None
        self.player_color: str = "white"
        self.running = True
        self.move_count = 0

    def stop(self, *_):
        self.running = False

    def run(self):
        info(f"Starting capture every {CAPTURE_INTERVAL}s.  Press Ctrl+C to stop.")
        info(f"Coaching threshold: {COACHING_THRESHOLD} centipawns")

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        while self.running:
            try:
                self._tick()
            except Exception as exc:
                warn(f"Tick error: {exc}")
            time.sleep(CAPTURE_INTERVAL)

        # end-of-session cleanup
        self._wrap_up()

    def _tick(self):
        img = capture(self.region)
        img_b64 = image_to_base64(img)

        board, bottom_color = extract_position(img_b64)
        if board is None:
            info("No board detected in screenshot.")
            return

        if bottom_color in ("white", "black"):
            self.player_color = bottom_color

        fen = board.fen()
        if fen == self.prev_fen:
            return  # position unchanged

        info(f"Position changed  eval: {self._eval_str(board)}")

        engine_result = analyse(board)
        curr_cp = engine_result.get("score_cp")

        # figure out last move by diffing boards
        last_move_san = self._detect_last_move(self.prev_board, board)

        delta = None
        if self.prev_cp is not None and self.prev_board is not None:
            # determine whose move it was (prev board's turn)
            player_just_moved_white = (self.prev_board.turn == chess.WHITE)
            delta = eval_delta(self.prev_cp, curr_cp, player_just_moved_white)

        self.prev_fen = fen
        self.prev_cp = curr_cp
        self.prev_board = board
        self.move_count += 1

        should_coach = (
            delta is None  # first move
            or abs(delta) >= COACHING_THRESHOLD
            or self.move_count % 5 == 0  # periodic check-in every 5 moves
        )

        if should_coach:
            try:
                msg = self.coach_session.coach(
                    board, engine_result, last_move_san, delta, self.player_color
                )
                coach_msg(msg)
            except Exception as exc:
                warn(f"Coach error: {exc}")

    def _eval_str(self, board: chess.Board) -> str:
        try:
            r = analyse(board)
            return score_label(r.get("score_cp"), r.get("mate_in"))
        except Exception:
            return "?"

    @staticmethod
    def _detect_last_move(prev: Optional[chess.Board], curr: chess.Board) -> Optional[str]:
        """Try to identify the last move by comparing positions."""
        if prev is None:
            return None
        try:
            for move in prev.legal_moves:
                candidate = prev.copy()
                candidate.push(move)
                if candidate.board_fen() == curr.board_fen():
                    return prev.san(move)
        except Exception:
            pass
        return None

    def _wrap_up(self):
        info("Session ending — requesting post-game summary...")
        result = input("Game result? (1-0 / 0-1 / 1/2-1/2 / unknown): ").strip() or "unknown"
        try:
            summary_text = self.coach_session.end_game_summary(result)
            coach_msg(summary_text)
            append_match_summary({"result": result, "summary": summary_text,
                                   "moves_analyzed": self.move_count})
        except Exception as exc:
            warn(f"Summary error: {exc}")
        close_engine()
        info("Profile saved.  Goodbye!")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="ChessMentor — real-time chess coaching")
    parser.add_argument("--profile", action="store_true", help="Show player profile")
    parser.add_argument("--history", action="store_true", help="Show match history")
    parser.add_argument("--set-name", metavar="NAME", help="Set username")
    parser.add_argument("--set-rating", metavar="N", type=int, help="Set estimated rating")
    parser.add_argument("--region", metavar="L,T,W,H", help="Screen region (left,top,width,height)")
    parser.add_argument("--debug-capture", action="store_true", help="Capture one screenshot and exit")
    args = parser.parse_args()

    if args.profile:
        cmd_show_profile(); return
    if args.history:
        cmd_show_history(); return
    if args.set_name:
        cmd_set_name(args.set_name); return
    if args.set_rating:
        cmd_set_rating(args.set_rating); return

    if not ANTHROPIC_API_KEY:
        err("ANTHROPIC_API_KEY is not set.  Export it before running ChessMentor.")
        sys.exit(1)

    profile = load_profile()
    if not profile["username"]:
        profile["username"] = input("Your name (for the profile): ").strip() or "Player"
        save_profile(profile)

    # region
    if args.region:
        parts = [int(x) for x in args.region.split(",")]
        region = tuple(parts[:4])
    else:
        region = select_region_interactively()

    if args.debug_capture:
        img = capture(region)
        save_debug_image(img)
        info(f"Saved capture to /tmp/chess_capture.png")
        return

    session = Session(region, profile)
    session.run()


if __name__ == "__main__":
    main()
