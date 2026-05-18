# ChessMentor

Real-time chess coaching via screen capture, Stockfish analysis, and Claude AI.

## Features

- **Screen capture** — monitors a region of your screen every N seconds
- **Board recognition** — Claude vision API extracts the position from the screenshot
- **Engine analysis** — Stockfish evaluates each position at configurable depth
- **Adaptive coaching** — Claude gives contextual coaching after blunders, mistakes, or every 5 moves
- **Persistent profile** — lessons learned, opening tendencies, strengths/weaknesses, and coach notes survive across sessions
- **Match history** — post-game summaries stored locally

## Installation

```bash
pip install -r requirements.txt
# Install Stockfish: https://stockfishchess.org/download/
# On Debian/Ubuntu: sudo apt install stockfish
# On macOS: brew install stockfish
```

## Setup

```bash
export ANTHROPIC_API_KEY=your_key_here
export STOCKFISH_PATH=/usr/bin/stockfish   # if not on PATH
```

## Usage

```bash
# Start a coaching session (prompts for screen region)
python main.py

# Pass region directly: left,top,width,height in pixels
python main.py --region 100,200,800,800

# One-shot debug capture (saves to /tmp/chess_capture.png)
python main.py --region 100,200,800,800 --debug-capture

# Profile management
python main.py --set-name "Alice"
python main.py --set-rating 1400
python main.py --profile
python main.py --history
```

## Configuration (environment variables)

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Required |
| `STOCKFISH_PATH` | `stockfish` | Path to Stockfish binary |
| `CAPTURE_INTERVAL` | `5` | Seconds between screenshots |
| `ENGINE_DEPTH` | `18` | Stockfish search depth |
| `ENGINE_TOP_MOVES` | `3` | Number of top moves shown to coach |
| `COACHING_THRESHOLD` | `100` | Centipawn loss to trigger coaching |
| `CLAUDE_MODEL` | `claude-opus-4-7` | Claude model for vision + coaching |

## Data storage

All data is stored in `~/.chessMentor/`:
- `profile.json` — player profile (openings, lessons, strengths, weaknesses, coach notes)
- `history.json` — match summaries

## How it works

1. Every `CAPTURE_INTERVAL` seconds, a screenshot of the configured region is taken.
2. The image is sent to Claude's vision API to extract the FEN position.
3. Stockfish analyses the position and finds the top moves.
4. If the position changed and a significant evaluation swing occurred (or every 5 moves), Claude acts as a coach — explaining what happened, what should have been played, and linking it to the player's known patterns.
5. Claude emits a structured `PROFILE_UPDATE` that the system parses to persistently update the player profile.
6. On session end (Ctrl+C), a post-game summary is requested and stored.
