"""
Persistent runtime settings, editable via the web control panel.

Settings are stored in ~/.chessMentor/settings.json as a simple key→value map
where keys match the environment variable names used by config.py.

apply_settings_to_env() must be called BEFORE config.py is imported (or while
its module-level reads happen) so that the env-var defaults inside config.py
pick up the saved values.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any, Dict

SETTINGS_FILE = Path.home() / ".chessMentor" / "settings.json"

# Allow-list of keys exposable via the web UI (keeps secrets / typos out of env)
SETTINGS_KEYS = {
    # LLM provider selection
    "LLM_PROVIDER", "LLM_FALLBACK_CHAIN", "CLAUDE_MODEL",
    # API keys
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY",
    "DEEPSEEK_API_KEY", "GEMINI_API_KEY",
    # Model overrides
    "OPENAI_LLM_MODEL", "OPENAI_VISION_MODEL",
    "OPENROUTER_MODEL", "OPENROUTER_SITE_URL", "OPENROUTER_APP_NAME",
    "DEEPSEEK_MODEL", "GEMINI_VISION_MODEL",
    "OLLAMA_BASE_URL", "OLLAMA_MODEL",
    # Vision / engine providers
    "VISION_PROVIDER", "CV_MODEL_PATH",
    "ENGINE_PROVIDER", "STOCKFISH_PATH", "ENGINE_TOP_MOVES",
    # Behaviour knobs
    "CAPTURE_INTERVAL", "COACHING_THRESHOLD",
    # Misc
    "DASHBOARD_PORT", "PGN_SAVE_DIR",
}

# Keys that should never be echoed back to the client in plaintext
SENSITIVE_KEYS = {
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY",
    "OPENROUTER_API_KEY", "DEEPSEEK_API_KEY", "GEMINI_API_KEY",
}


def load_settings() -> Dict[str, str]:
    if not SETTINGS_FILE.exists():
        return {}
    try:
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_settings(updates: Dict[str, Any]) -> Dict[str, str]:
    """
    Merge *updates* into the persisted settings.
    Empty / None values delete the corresponding key.
    """
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    current = load_settings()
    for k, v in updates.items():
        if k not in SETTINGS_KEYS:
            continue
        if v is None or v == "":
            current.pop(k, None)
        else:
            current[k] = str(v)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(current, f, indent=2)
    apply_settings_to_env()
    return current


def apply_settings_to_env() -> None:
    """Push saved settings into os.environ so config.py picks them up."""
    for k, v in load_settings().items():
        if k in SETTINGS_KEYS and v not in (None, ""):
            os.environ[k] = str(v)


def public_settings() -> Dict[str, Any]:
    """Settings safe for the web UI — sensitive values are masked."""
    s = load_settings()
    out = {k: s.get(k, "") for k in sorted(SETTINGS_KEYS)}
    for k in SENSITIVE_KEYS:
        if out.get(k):
            out[k] = "***SET***"
    return out


def get_setting(key: str, default: str = "") -> str:
    """Read one persisted setting (does NOT consult os.environ)."""
    return load_settings().get(key, default)
