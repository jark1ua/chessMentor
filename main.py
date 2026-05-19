"""
ChessMentor — real-time chess coaching via screen capture + engine + LLM.

Usage
-----
  python main.py                         # start coaching session (interactive region select)
  python main.py --chat                  # pre-match chat / opening prep before region select
  python main.py --review [FILE.pgn]     # review last saved PGN (or a specific file)
  python main.py --puzzles               # tactical puzzles from your weakness profile
  python main.py --dashboard             # launch web stats dashboard (localhost:5555)
  python main.py --profile               # view / edit player profile
  python main.py --history               # show match history summaries
  python main.py --set-name NAME         # set username
  python main.py --set-rating N          # set estimated rating
  python main.py --region L,T,W,H        # screen region (skip interactive select)
  python main.py --clock-region L,T,W,H  # extra region for OCR clock reading
  python main.py --debug-capture         # capture one screenshot and exit
"""
import sys
import time
import argparse
import signal
from pathlib import Path
from typing import Optional, List

import chess

from config import (
    CAPTURE_INTERVAL, COACHING_THRESHOLD, ANTHROPIC_API_KEY,
    ENGINE_PROVIDER, VISION_PROVIDER, LLM_PROVIDER, LLM_FALLBACK_CHAIN,
    STOCKFISH_PATH, ENGINE_TOP_MOVES,
    OPENAI_API_KEY, OPENAI_VISION_MODEL, OPENAI_LLM_MODEL,
    GEMINI_API_KEY, GEMINI_VISION_MODEL,
    OLLAMA_BASE_URL, OLLAMA_MODEL,
    CLAUDE_MODEL, CV_MODEL_PATH,
    OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_SITE_URL, OPENROUTER_APP_NAME,
    DEEPSEEK_API_KEY, DEEPSEEK_MODEL,
    DASHBOARD_PORT, PGN_SAVE_DIR,
)
from capture import select_region_interactively, capture, image_to_base64, save_debug_image
import board_analyzer
import engine as engine_module
from coach import CoachSession
from profile import (
    load_profile, save_profile, append_match_summary,
    load_history, profile_summary_text,
    record_session_accuracy, get_adaptive_threshold,
)
from providers.engine import get_engine
from providers.vision import get_vision_provider
from providers.llm import get_llm_provider
from providers.depth import depth_rationale
from opening import detect_opening
from pgn_export import GameRecorder
from clock import read_clock, is_time_pressure

try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
    def info(msg):      console.print(f"[cyan]{msg}[/cyan]")
    def warn(msg):      console.print(f"[yellow]{msg}[/yellow]")
    def coach_msg(msg): console.print(Panel(msg, title="[bold green]ChessMentor[/bold green]", expand=False))
    def err(msg):       console.print(f"[bold red]{msg}[/bold red]")
    def debug(msg):     console.print(f"[dim]{msg}[/dim]")
    def ask(prompt):    return console.input(f"[bold cyan]{prompt}[/bold cyan] ")
except ImportError:
    def info(msg):      print(f"[INFO] {msg}")
    def warn(msg):      print(f"[WARN] {msg}")
    def coach_msg(msg): print(f"\n=== ChessMentor ===\n{msg}\n==================\n")
    def err(msg):       print(f"[ERROR] {msg}")
    def debug(msg):     print(f"[DEBUG] {msg}")
    def ask(prompt):
        print(prompt, end=" ", flush=True)
        return input()


# ---------------------------------------------------------------------------
# Provider initialisation
# ---------------------------------------------------------------------------

def build_config(profile: dict) -> dict:
    return {
        "engine_provider":       ENGINE_PROVIDER,
        "stockfish_path":        STOCKFISH_PATH,
        "engine_top_moves":      ENGINE_TOP_MOVES,
        "vision_provider":       VISION_PROVIDER,
        "llm_provider":          LLM_PROVIDER,
        "anthropic_api_key":     ANTHROPIC_API_KEY,
        "claude_model":          CLAUDE_MODEL,
        "openai_api_key":        OPENAI_API_KEY,
        "openai_vision_model":   OPENAI_VISION_MODEL,
        "openai_llm_model":      OPENAI_LLM_MODEL,
        "gemini_api_key":        GEMINI_API_KEY,
        "gemini_vision_model":   GEMINI_VISION_MODEL,
        "ollama_base_url":       OLLAMA_BASE_URL,
        "ollama_model":          OLLAMA_MODEL,
        "cv_model_path":         CV_MODEL_PATH,
        "openrouter_api_key":    OPENROUTER_API_KEY,
        "openrouter_model":      OPENROUTER_MODEL,
        "openrouter_site_url":   OPENROUTER_SITE_URL,
        "openrouter_app_name":   OPENROUTER_APP_NAME,
        "deepseek_api_key":      DEEPSEEK_API_KEY,
        "deepseek_model":        DEEPSEEK_MODEL,
        "llm_fallback_chain":    LLM_FALLBACK_CHAIN,
    }


def initialise_providers(profile: dict):
    """Create and register all provider instances; print which are active."""
    cfg = build_config(profile)

    engine_provider = get_engine(profile, cfg)
    vision_provider = get_vision_provider(cfg)
    llm_provider    = get_llm_provider(cfg)

    board_analyzer.set_provider(vision_provider)
    engine_module.set_provider(engine_provider, profile)

    info(
        f"Active providers — engine: {ENGINE_PROVIDER} "
        f"| vision: {VISION_PROVIDER} | llm: {LLM_PROVIDER}"
    )
    return llm_provider


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def cmd_show_profile():
    print("\n" + profile_summary_text(load_profile()) + "\n")


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


def _latest_pgn() -> Optional[str]:
    """Return path to the most recently saved PGN, or None."""
    pgn_dir = Path(PGN_SAVE_DIR)
    if not pgn_dir.exists():
        return None
    pgns = sorted(pgn_dir.glob("*.pgn"))
    return str(pgns[-1]) if pgns else None


# ---------------------------------------------------------------------------
# Pre-match chat loop
# ---------------------------------------------------------------------------

def run_pre_match_chat(profile: dict, coach_session: CoachSession) -> str:
    """
    Interactive chat before (or instead of) a match.

    Returns one of:
      'start'   — player is ready to begin a match
      'puzzles' — player wants puzzle training
      'quit'    — player wants to exit
    """
    is_new = profile.get("total_games_analyzed", 0) == 0

    if is_new:
        opener = (
            f"Welcome, {profile.get('username', 'there')}! I'm your ChessMentor. "
            "Since this is your first session, let's start by having you play a game — "
            "just play naturally and I'll observe and coach in real time.\n\n"
            "Or if you'd like to discuss openings or strategy first, just ask!\n\n"
            "Type **start** when you're ready to begin, or chat with me first."
        )
    else:
        weaknesses = profile.get("weaknesses", [])
        last_lesson = (profile.get("lessons") or [""])[-1]
        opener = f"Welcome back, {profile.get('username', 'there')}!"
        if weaknesses:
            opener += f" We've noted weakness in: {', '.join(weaknesses[:3])}."
        if last_lesson:
            opener += f"\n\nLast lesson: *{last_lesson}*"
        opener += (
            "\n\nType **start** to begin your match, **puzzles** for tactical training, "
            "or ask me anything."
        )

    coach_msg(opener)

    while True:
        try:
            user_input = ask("You:").strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"

        if not user_input:
            continue

        lower = user_input.lower()
        if lower in ("start", "play", "begin", "go", "ready"):
            coach_msg("Let's go! Select your board region and the coaching begins.")
            return "start"
        if lower == "puzzles":
            return "puzzles"
        if lower in ("quit", "exit", "q"):
            return "quit"

        # Pass to the LLM coach
        try:
            reply = coach_session.chat(user_input)
            coach_msg(reply)
        except Exception as exc:
            warn(f"Chat error: {exc}")


# ---------------------------------------------------------------------------
# Main session loop
# ---------------------------------------------------------------------------

class Session:
    def __init__(
        self,
        region,
        profile: dict,
        llm_provider,
        clock_region=None,
    ):
        self.region = region
        self.profile = profile
        self.coach_session = CoachSession(profile, llm_provider=llm_provider, debug=True)
        self.clock_region = clock_region

        # Use adaptive threshold based on rating + accuracy history
        self.coaching_threshold = get_adaptive_threshold(profile, base=COACHING_THRESHOLD)
        info(f"Adaptive coaching threshold: {self.coaching_threshold} cp")

        self.prev_fen:    Optional[str]          = None
        self.prev_cp:     Optional[int]          = None
        self.prev_board:  Optional[chess.Board]  = None
        self.player_color: str                   = "white"
        self.running:      bool                  = True
        self.move_count:   int                   = 0
        self.uci_moves:    List[str]             = []
        self.cp_losses:    List[float]           = []

        # PGN recorder
        self.recorder = GameRecorder(
            player_username=profile.get("username", "Player"),
            player_color="white",  # updated on first position
        )
        self._current_opening: Optional[str] = None

    def stop(self, *_):
        self.running = False

    def run(self):
        info(f"Capturing every {CAPTURE_INTERVAL}s — Ctrl+C to stop.")
        signal.signal(signal.SIGINT,  self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        while self.running:
            try:
                self._tick()
            except Exception as exc:
                warn(f"Tick error: {exc}")
            time.sleep(CAPTURE_INTERVAL)

        self._wrap_up()

    def _tick(self):
        img     = capture(self.region)
        img_b64 = image_to_base64(img)

        board, bottom_color = board_analyzer.extract_position(img_b64)
        if board is None:
            info("No board detected in screenshot.")
            return

        if bottom_color in ("white", "black"):
            if self.player_color != bottom_color:
                self.player_color = bottom_color
                self.recorder = GameRecorder(
                    player_username=self.profile.get("username", "Player"),
                    player_color=bottom_color,
                )

        fen = board.fen()
        if fen == self.prev_fen:
            return  # position unchanged

        engine_result = engine_module.analyse(board)
        curr_cp = engine_result.get("score_cp")

        try:
            rationale = depth_rationale(self.profile, board)
            debug(f"Engine depth: {rationale}")
        except Exception:
            pass

        info(f"Position changed — eval: {engine_module.score_label(curr_cp, engine_result.get('mate_in'))}")

        # Detect the move played
        last_move_san = self._detect_last_move(self.prev_board, board)
        if last_move_san and self.prev_board is not None:
            for move in self.prev_board.legal_moves:
                cand = self.prev_board.copy()
                cand.push(move)
                if cand.board_fen() == board.board_fen():
                    self.uci_moves.append(move.uci())
                    break

        # Real-time opening detection
        opening = detect_opening(self.uci_moves)
        if opening and opening[1] != self._current_opening:
            self._current_opening = opening[1]
            info(f"Opening: {opening[0]} — {opening[1]}")

        # Clock OCR (optional)
        short_coaching = False
        if self.clock_region is not None:
            try:
                clock_img = capture(self.clock_region)
                time_str = read_clock(clock_img)
                if time_str and is_time_pressure(time_str):
                    short_coaching = True
                    debug(f"Time pressure detected ({time_str}) — shortening coaching messages.")
            except Exception:
                pass

        delta = None
        if self.prev_cp is not None and self.prev_board is not None:
            player_just_moved_white = (self.prev_board.turn == chess.WHITE)
            delta = engine_module.eval_delta(self.prev_cp, curr_cp, player_just_moved_white)
            if delta is not None:
                self.cp_losses.append(abs(delta))

        self.prev_fen   = fen
        self.prev_cp    = curr_cp
        self.prev_board = board
        self.move_count += 1

        should_coach = (
            delta is None
            or abs(delta) >= self.coaching_threshold
            or self.move_count % 5 == 0
        )

        if should_coach:
            try:
                msg = self.coach_session.coach(
                    board, engine_result, last_move_san, delta, self.player_color
                )
                if short_coaching:
                    # Truncate to first 2 sentences under time pressure
                    sentences = msg.replace("! ", "!|").replace(". ", ".|").split("|")
                    msg = " ".join(sentences[:2]).strip()
                coach_msg(msg)
                # Record position with coach annotation in PGN
                self.recorder.record_position(board, coach_comment=msg)
            except Exception as exc:
                warn(f"Coach error: {exc}")
        else:
            # Still record the position (no annotation)
            self.recorder.record_position(board)

    @staticmethod
    def _detect_last_move(
        prev: Optional[chess.Board], curr: chess.Board
    ) -> Optional[str]:
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
        result = ask("Game result? (1-0 / 0-1 / 1/2-1/2 / unknown):").strip() or "unknown"

        # Save annotated PGN
        try:
            pgn_dir = Path(PGN_SAVE_DIR)
            pgn_dir.mkdir(parents=True, exist_ok=True)
            ts = time.strftime("%Y%m%d_%H%M%S")
            pgn_path = pgn_dir / f"game_{ts}.pgn"
            self.recorder.set_result(result)
            self.recorder.save(str(pgn_path))
            info(f"Annotated PGN saved to: {pgn_path}")
        except Exception as exc:
            warn(f"Could not save PGN: {exc}")
            pgn_path = None

        # Record opening in profile
        if self._current_opening:
            from profile import record_opening
            record_opening(self.profile, self.player_color, self._current_opening)

        # Record session accuracy for adaptive threshold
        if self.cp_losses:
            avg_loss = sum(self.cp_losses) / len(self.cp_losses)
            record_session_accuracy(self.profile, avg_loss)
            info(f"Session avg centipawn loss: {avg_loss:.0f}")

        # LLM post-game summary
        try:
            summary_text = self.coach_session.end_game_summary(result)
            coach_msg(summary_text)
            append_match_summary({
                "result":          result,
                "summary":         summary_text,
                "moves_analyzed":  self.move_count,
                "opening":         self._current_opening,
                "pgn":             str(pgn_path) if pgn_path else None,
            })
        except Exception as exc:
            warn(f"Summary error: {exc}")

        engine_module.close_engine()
        info("Profile saved. Goodbye!")

        # Offer to review the game
        if pgn_path and pgn_path.exists():
            do_review = ask("Review key positions now? (y/N):").strip().lower()
            if do_review == "y":
                from review import review_game
                review_game(str(pgn_path))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="ChessMentor — real-time chess coaching")
    parser.add_argument("--profile",       action="store_true", help="Show player profile")
    parser.add_argument("--history",       action="store_true", help="Show match history")
    parser.add_argument("--set-name",      metavar="NAME",      help="Set username")
    parser.add_argument("--set-rating",    metavar="N", type=int, help="Set estimated rating")
    parser.add_argument("--region",        metavar="L,T,W,H",   help="Screen region (left,top,width,height)")
    parser.add_argument("--clock-region",  metavar="L,T,W,H",   help="Clock region for OCR time pressure detection")
    parser.add_argument("--chat",          action="store_true", help="Pre-match chat / opening prep")
    parser.add_argument("--review",        metavar="FILE",      nargs="?", const="__latest__",
                        help="Review last saved PGN (or specify a file)")
    parser.add_argument("--puzzles",       action="store_true", help="Tactical puzzles from your weakness profile")
    parser.add_argument("--dashboard",     action="store_true", help="Launch web stats dashboard")
    parser.add_argument("--dashboard-port", metavar="PORT", type=int, default=DASHBOARD_PORT,
                        help=f"Dashboard port (default: {DASHBOARD_PORT})")
    parser.add_argument("--debug-capture", action="store_true", help="Capture one screenshot and exit")
    args = parser.parse_args()

    # --- Simple info commands (no provider init needed) ---
    if args.profile:   cmd_show_profile(); return
    if args.history:   cmd_show_history(); return
    if args.set_name:  cmd_set_name(args.set_name); return
    if args.set_rating: cmd_set_rating(args.set_rating); return

    if args.dashboard:
        from dashboard import run_dashboard
        run_dashboard(port=args.dashboard_port)
        return

    if args.review is not None:
        pgn_file = _latest_pgn() if args.review == "__latest__" else args.review
        if not pgn_file:
            err("No PGN file found. Play a game first.")
            sys.exit(1)
        from review import review_game
        review_game(pgn_file)
        return

    # --- LLM required from here ---
    if not ANTHROPIC_API_KEY and LLM_PROVIDER == "claude":
        err("ANTHROPIC_API_KEY is not set. Export it before running ChessMentor.")
        sys.exit(1)

    profile = load_profile()
    if not profile["username"]:
        profile["username"] = ask("Your name (for the profile):").strip() or "Player"
        save_profile(profile)

    llm_provider = initialise_providers(profile)

    if args.puzzles:
        from puzzles import run_puzzle_session
        run_puzzle_session(profile)
        return

    # --- Pre-match chat (always offered, or forced with --chat) ---
    coach_session_for_chat = CoachSession(profile, llm_provider=llm_provider)

    if args.chat:
        decision = run_pre_match_chat(profile, coach_session_for_chat)
        if decision == "quit":
            return
        if decision == "puzzles":
            from puzzles import run_puzzle_session
            run_puzzle_session(profile)
            return
        # decision == 'start': fall through to match setup
    else:
        # Brief prompt — skip full chat but offer it
        is_new = profile.get("total_games_analyzed", 0) == 0
        if is_new:
            info("New profile detected. Tip: use --chat for an opening prep session first.")

    # --- Region selection ---
    if args.region:
        parts  = [int(x) for x in args.region.split(",")]
        region = tuple(parts[:4])
    else:
        region = select_region_interactively()

    clock_region = None
    if args.clock_region:
        parts        = [int(x) for x in args.clock_region.split(",")]
        clock_region = tuple(parts[:4])

    if args.debug_capture:
        img = capture(region)
        save_debug_image(img)
        info("Saved capture to /tmp/chess_capture.png")
        return

    session = Session(region, profile, llm_provider, clock_region=clock_region)
    session.run()


if __name__ == "__main__":
    main()
