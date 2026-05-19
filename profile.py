"""
Persistent user profile — stores chess identity, lessons learned, opening
repertoire tendencies, recurring habits, and match history summaries.

Adaptive coaching threshold
---------------------------
get_adaptive_threshold(profile) returns a centipawn value used to decide
whether to coach on a given move.  It accounts for the player's estimated
rating and recent per-session average centipawn loss history.
"""
import json
from datetime import datetime
from typing import Any
from config import PROFILE_FILE, HISTORY_FILE, CONVERSATION_FILE, ensure_data_dir

_DEFAULT_PROFILE = {
    "username": "",
    "rating_estimate": None,
    "preferred_color": "both",
    "openings": {"white": [], "black": []},
    "strengths": [],
    "weaknesses": [],
    "lessons": [],
    "coach_notes": [],
    "created_at": "",
    "updated_at": "",
    "total_games_analyzed": 0,
    # List of avg centipawn-loss values, one per session (most recent last).
    "accuracy_history": [],
}


def load_profile() -> dict:
    ensure_data_dir()
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE) as f:
            data = json.load(f)
        for k, v in _DEFAULT_PROFILE.items():
            data.setdefault(k, v)
        return data
    profile = dict(_DEFAULT_PROFILE)
    profile["created_at"] = datetime.utcnow().isoformat()
    return profile


def save_profile(profile: dict):
    ensure_data_dir()
    profile["updated_at"] = datetime.utcnow().isoformat()
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=2)


def append_lesson(profile: dict, lesson: str):
    if lesson not in profile["lessons"]:
        profile["lessons"].append(lesson)


def append_coach_note(profile: dict, note: str):
    entry = {"ts": datetime.utcnow().isoformat(), "note": note}
    profile["coach_notes"].append(entry)
    profile["coach_notes"] = profile["coach_notes"][-100:]


def add_weakness(profile: dict, weakness: str):
    if weakness not in profile["weaknesses"]:
        profile["weaknesses"].append(weakness)


def add_strength(profile: dict, strength: str):
    if strength not in profile["strengths"]:
        profile["strengths"].append(strength)


def record_opening(profile: dict, color: str, opening_name: str):
    lst = profile["openings"].get(color, [])
    if opening_name not in lst:
        lst.append(opening_name)
    profile["openings"][color] = lst[-20:]


def record_session_accuracy(profile: dict, avg_cp_loss: float) -> None:
    """Append this session's average centipawn loss and keep last 20."""
    hist = profile.setdefault("accuracy_history", [])
    hist.append(round(avg_cp_loss, 1))
    profile["accuracy_history"] = hist[-20:]


def get_adaptive_threshold(profile: dict, base: int = 100) -> int:
    """
    Return a coaching centipawn threshold adapted to the player's level.

    Logic
    -----
    - Rating adjustment: lower-rated players get a higher threshold so they
      aren't coached on every small imprecision.
      +60 cp at 600, 0 at 1800, capped at -20 for 2000+.
    - Accuracy adjustment: if the player's recent average cp-loss is high
      (many blunders), raise the threshold slightly so coaching fires on
      genuinely significant mistakes, not constant noise.
    """
    rating = profile.get("rating_estimate") or 1000
    rating_adj = max(-20, (1800 - int(rating)) / 20)

    hist = profile.get("accuracy_history", [])
    if hist:
        recent_avg = sum(hist[-5:]) / len(hist[-5:])
        # If average loss > 150 cp, raise threshold slightly to avoid spam
        accuracy_adj = max(0, (recent_avg - 150) / 5)
    else:
        accuracy_adj = 0

    threshold = int(base + rating_adj + accuracy_adj)
    return max(40, min(250, threshold))


# ---------------------------------------------------------------------------
# Match history
# ---------------------------------------------------------------------------

def load_history() -> list:
    ensure_data_dir()
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []


def append_match_summary(summary: dict):
    history = load_history()
    summary["ts"] = datetime.utcnow().isoformat()
    history.append(summary)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


# ---------------------------------------------------------------------------
# Conversation persistence
# ---------------------------------------------------------------------------

def load_conversation() -> list:
    """Load the full persisted coaching conversation from disk."""
    ensure_data_dir()
    if CONVERSATION_FILE.exists():
        try:
            with open(CONVERSATION_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_conversation(messages: list) -> None:
    """Persist the coaching conversation to disk (full history, no trim)."""
    ensure_data_dir()
    with open(CONVERSATION_FILE, "w") as f:
        json.dump(messages, f)


# ---------------------------------------------------------------------------
# Profile summary for LLM system prompt
# ---------------------------------------------------------------------------

def profile_summary_text(profile: dict) -> str:
    lines = [
        f"Player: {profile['username'] or 'Unknown'}",
        f"Estimated rating: {profile['rating_estimate'] or 'Unknown'}",
        f"Preferred color: {profile['preferred_color']}",
        f"Games analyzed: {profile['total_games_analyzed']}",
    ]
    if profile["openings"]["white"]:
        lines.append("White openings: " + ", ".join(profile["openings"]["white"]))
    if profile["openings"]["black"]:
        lines.append("Black openings: " + ", ".join(profile["openings"]["black"]))
    if profile["strengths"]:
        lines.append("Strengths: " + "; ".join(profile["strengths"]))
    if profile["weaknesses"]:
        lines.append("Weaknesses: " + "; ".join(profile["weaknesses"]))
    if profile["lessons"]:
        lines.append("Past lessons:\n" + "\n".join(f"  - {l}" for l in profile["lessons"][-10:]))
    if profile["coach_notes"]:
        recent = profile["coach_notes"][-5:]
        notes_text = "\n".join(f"  [{n['ts'][:10]}] {n['note']}" for n in recent)
        lines.append("Recent coach notes:\n" + notes_text)
    return "\n".join(lines)
