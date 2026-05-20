"""
Shared runtime state for the web control panel.

This singleton bridges the capture/coach background thread with the Flask
web server: the thread pushes position / eval / coach updates here, the
server reads them for /api/state polling.
"""
from __future__ import annotations
import threading
import time
from collections import deque
from typing import Any, Optional, Dict


class AppState:
    """Thread-safe runtime state shared between capture loop and web UI."""

    def __init__(self):
        self._lock                              = threading.RLock()
        self.running:        bool               = False
        self.fen:            Optional[str]      = None
        self.eval_cp:        Optional[int]      = None
        self.eval_mate:      Optional[int]      = None
        self.eval_source:    str                = ""
        self.opening:        Optional[str]      = None
        self.opening_eco:    Optional[str]      = None
        self.player_color:   str                = "white"
        self.last_coach_msg: str                = ""
        self.move_count:     int                = 0
        self.thread:         Optional[threading.Thread] = None
        self.session                            = None  # live Session, if any
        self.pending_result: Optional[str]      = None  # set by /api/session/stop
        self.events:         deque              = deque(maxlen=100)

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def add_event(self, kind: str, message: str, data: Optional[Dict] = None) -> None:
        with self._lock:
            self.events.append({
                "ts":      time.time(),
                "kind":    kind,
                "message": message,
                "data":    data or {},
            })

    def update_position(
        self,
        fen: str,
        eval_cp: Optional[int],
        eval_mate: Optional[int],
        source: str,
        opening: Optional[str],
        opening_eco: Optional[str],
        color: str,
        last_msg: str,
        move_count: int,
    ) -> None:
        with self._lock:
            self.fen          = fen
            self.eval_cp      = eval_cp
            self.eval_mate    = eval_mate
            self.eval_source  = source
            self.opening      = opening
            self.opening_eco  = opening_eco
            self.player_color = color
            if last_msg:
                self.last_coach_msg = last_msg
            self.move_count   = move_count

    def set_running(self, running: bool) -> None:
        with self._lock:
            self.running = running

    def reset_session(self) -> None:
        with self._lock:
            self.fen = None
            self.eval_cp = None
            self.eval_mate = None
            self.opening = None
            self.opening_eco = None
            self.last_coach_msg = ""
            self.move_count = 0
            self.pending_result = None
            self.session = None
            self.thread = None

    # ------------------------------------------------------------------
    # Read-only
    # ------------------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "running":         self.running,
                "fen":             self.fen,
                "eval_cp":         self.eval_cp,
                "eval_mate":       self.eval_mate,
                "eval_source":     self.eval_source,
                "opening":         self.opening,
                "opening_eco":     self.opening_eco,
                "player_color":    self.player_color,
                "last_coach_msg":  self.last_coach_msg,
                "move_count":      self.move_count,
                "events":          list(self.events)[-30:],
            }


# Module-level singleton
STATE = AppState()


# ---------------------------------------------------------------------------
# Session orchestration helpers (used by the web server)
# ---------------------------------------------------------------------------

def start_session_thread(region, clock_region=None) -> tuple[bool, str]:
    """
    Spawn a Session in a background thread.
    Returns (ok, message).
    """
    if STATE.running:
        return False, "A session is already running."

    from profile import load_profile
    from main import Session, initialise_providers

    profile = load_profile()
    llm     = initialise_providers(profile)

    session = Session(
        region=region,
        profile=profile,
        llm_provider=llm,
        clock_region=clock_region,
        app_state=STATE,
    )
    STATE.session = session
    STATE.set_running(True)
    STATE.add_event("system", "Session started.")

    t = threading.Thread(target=session.run, daemon=True)
    STATE.thread = t
    t.start()
    return True, "Session started."


def stop_session_thread(result: str = "unknown") -> tuple[bool, str]:
    if not STATE.running or STATE.session is None:
        return False, "No session is running."
    STATE.pending_result = result
    STATE.session.stop()
    STATE.set_running(False)
    STATE.add_event("system", f"Session stopping (result: {result}).")
    return True, "Session stopped."
