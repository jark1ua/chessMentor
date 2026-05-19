"""
Persistent user profile — stores chess identity, lessons learned, opening
repertoire tendencies, recurring habits, and match history summaries.
"""
import json
from datetime import datetime
from typing import Any
from config import PROFILE_FILE, HISTORY_FILE, CONVERSATION_FILE, ensure_data_dir

_DEFAULT_PROFILE = {
    "username": "",
    "rating_estimate": None,
    "preferred_color": "both",
    # openings the user tends to play, keyed by color
    "openings": {"white": [], "black": []},
    # recurring good habits observed
    "strengths": [],
    # recurring mistakes / weaknesses
    "weaknesses": [],
    # lessons explicitly given by the coach
    "lessons": [],
    # free-form notes the coach adds over time
    "coach_notes": [],
    "created_at": "",
    "updated_at": "",
    "total_games_analyzed": 0,
}


def load_profile() -> dict:
    ensure_data_dir()
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE) as f:
            data = json.load(f)
        # forward-compat: fill missing keys
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
    # keep last 100 notes
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
    profile["openings"][color] = lst[-20:]  # keep last 20


# ---------------------------------------------------------------------------
# Match history — lightweight append-only log
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


def load_conversation() -> list:
    """Load the persisted coaching conversation from disk."""
    ensure_data_dir()
    if CONVERSATION_FILE.exists():
        try:
            with open(CONVERSATION_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_conversation(messages: list) -> None:
    """Persist the coaching conversation to disk."""
    ensure_data_dir()
    with open(CONVERSATION_FILE, "w") as f:
        json.dump(messages, f)


def profile_summary_text(profile: dict) -> str:
    """Return a compact text block suitable for an LLM system prompt."""
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
