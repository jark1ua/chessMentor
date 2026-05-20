import os
import json
from pathlib import Path

# Apply persisted UI settings to os.environ BEFORE we read any env vars below.
# This lets settings saved via the web control panel override env-var defaults.
try:
    from settings import apply_settings_to_env
    apply_settings_to_env()
except Exception:
    pass

DATA_DIR = Path.home() / ".chessMentor"
PROFILE_FILE = DATA_DIR / "profile.json"
HISTORY_FILE = DATA_DIR / "history.json"
CONVERSATION_FILE = DATA_DIR / "conversation.json"

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

# Provider selection
ENGINE_PROVIDER = os.environ.get("ENGINE_PROVIDER", "auto")   # auto|lichess|local
VISION_PROVIDER = os.environ.get("VISION_PROVIDER", "claude") # cv|claude|openai|gemini
# Path to a TorchScript chess piece classifier model for the CV vision provider.
# Leave empty to use the heuristic (no model required).
CV_MODEL_PATH   = os.environ.get("CV_MODEL_PATH", "")
LLM_PROVIDER    = os.environ.get("LLM_PROVIDER", "claude")
# LLM_PROVIDER options: claude | openai | openrouter | deepseek | ollama | fallback
# When fallback: comma-separated chain tried in order
LLM_FALLBACK_CHAIN = os.environ.get("LLM_FALLBACK_CHAIN", "openrouter,claude")

# Additional API keys
OPENAI_API_KEY      = os.environ.get("OPENAI_API_KEY", "")
GEMINI_API_KEY      = os.environ.get("GEMINI_API_KEY", "")
OPENROUTER_API_KEY  = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL    = os.environ.get("OPENROUTER_MODEL", "deepseek/deepseek-chat")
OPENROUTER_SITE_URL = os.environ.get("OPENROUTER_SITE_URL", "")
OPENROUTER_APP_NAME = os.environ.get("OPENROUTER_APP_NAME", "ChessMentor")
DEEPSEEK_API_KEY    = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL      = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

# Ollama settings
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.environ.get("OLLAMA_MODEL", "llama3")

# Provider-specific model overrides
OPENAI_VISION_MODEL = os.environ.get("OPENAI_VISION_MODEL", "gpt-4o")
OPENAI_LLM_MODEL    = os.environ.get("OPENAI_LLM_MODEL", "gpt-4o")
GEMINI_VISION_MODEL = os.environ.get("GEMINI_VISION_MODEL", "gemini-1.5-flash")


# Dashboard
DASHBOARD_PORT = int(os.environ.get("DASHBOARD_PORT", "5555"))

# Directory where annotated PGN files are saved (default: ~/.chessMentor/pgns/)
PGN_SAVE_DIR = Path(os.environ.get("PGN_SAVE_DIR", str(DATA_DIR / "pgns")))


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
