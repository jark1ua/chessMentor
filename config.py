import os
import json
from pathlib import Path

DATA_DIR = Path.home() / ".chessMentor"
PROFILE_FILE = DATA_DIR / "profile.json"
HISTORY_FILE = DATA_DIR / "history.json"

# Stockfish path — override via STOCKFISH_PATH env var
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "stockfish")

# Anthropic API key
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# How often to capture a screenshot (seconds)
CAPTURE_INTERVAL = float(os.environ.get("CAPTURE_INTERVAL", "5"))

# Stockfish analysis depth
ENGINE_DEPTH = int(os.environ.get("ENGINE_DEPTH", "18"))

# How many engine top moves to include in coaching context
ENGINE_TOP_MOVES = int(os.environ.get("ENGINE_TOP_MOVES", "3"))

# Centipawn threshold: only coach when eval shifts by this much
COACHING_THRESHOLD = int(os.environ.get("COACHING_THRESHOLD", "100"))

# Anthropic model
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-7")


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
