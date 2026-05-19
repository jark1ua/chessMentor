# ChessMentor

Real-time chess coaching via screen capture, engine analysis, and LLM coaching — with a persistent player profile that grows smarter every session.

---

## How It Works — Full Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  Every CAPTURE_INTERVAL seconds (default: 5s)                       │
│                                                                     │
│  1. SCREENSHOT ──► screen region captured with mss/Pillow           │
│          │                                                          │
│          ▼                                                          │
│  2. BOARD DETECTION                                                 │
│     ├─ CV provider (default):  OpenCV contour detection             │
│     │    └─ perspective warp ──► 64 squares ──► heuristic classify  │
│     │    └─ optional CNN (TorchScript model) for higher accuracy    │
│     └─ LLM vision (claude/openai/gemini): send image, get FEN back  │
│          │                                                          │
│          ▼  (chess.Board + which colour is at bottom)               │
│  3. POSITION CHANGED?  ── no ──► sleep, repeat                      │
│          │ yes                                                      │
│          ▼                                                          │
│  4. ENGINE ANALYSIS                                                 │
│     ├─ Lichess cloud eval API (free, depth 20+, instant)            │
│     └─ Local Stockfish fallback (adaptive depth by rating+phase)    │
│          │                                                          │
│          ▼  (score_cp, mate_in, top_moves[], source)                │
│  5. EVAL DELTA — centipawns lost since last position                │
│     ├─ > 200 cp  → blunder   ──► trigger coaching                  │
│     ├─ > 80 cp   → mistake   ──► trigger coaching                  │
│     ├─ > 30 cp   → inaccuracy──► trigger coaching                  │
│     └─ every 5 moves         ──► periodic check-in                 │
│          │                                                          │
│          ▼                                                          │
│  6. PRINCIPLE RETRIEVAL                                             │
│     knowledge/retrieval.py scans the board for features:           │
│     passed pawns, open files, isolated pawns, doubled pawns,       │
│     bishop vs knight, two bishops, uncastled king, material imbal. │
│     ──► scores 100+ principles from 17 classic sources             │
│     ──► injects top-3 most relevant + novel into the system prompt  │
│          │                                                          │
│          ▼                                                          │
│  7. LLM COACHING CALL                                               │
│     System prompt:  player profile + injected principles (CACHED)  │
│     Conversation:   full history loaded from disk (~30 exchanges)   │
│     Tool use:       model calls update_player_profile() structured  │
│                     function — no regex parsing                     │
│     ──► coaching_text returned to terminal                          │
│     ──► tool_input dict written to profile immediately              │
│          │                                                          │
│          ▼                                                          │
│  8. PERSIST                                                         │
│     ~/.chessMentor/profile.json      ← lessons, weaknesses, etc.   │
│     ~/.chessMentor/conversation.json ← full message history        │
└─────────────────────────────────────────────────────────────────────┘

On Ctrl+C:
  ──► post-game summary requested from coach
  ──► result + summary written to history.json
  ──► engine closed cleanly
```

---

## Adaptive Engine Depth

Depth is computed per-position from the player's estimated rating and the game phase — never a fixed value:

| Rating       | Middlegame | Opening | Endgame |
|-------------|-----------|---------|---------|
| < 800        | 3          | 3       | 5       |
| 800–1199     | 5          | 4       | 7       |
| 1200–1499    | 8          | 7       | 10      |
| 1500–1799    | 10         | 9       | 12      |
| 1800–2199    | 13         | 12      | 15      |
| 2200+        | 15         | 14      | 15      |

The Lichess cloud eval API returns depth 20+ instantly for most positions — local Stockfish only activates for positions not in the cloud cache.

---

## Knowledge Base

`knowledge/principles.py` contains 100+ structured principles drawn from **primary sources**:

| Source | Key themes |
|--------|-----------|
| Paul Morphy (Sergeant/Löwenthal annotations) | Development, open lines, attacking uncastled king |
| Steinitz — *The Modern Chess Instructor* (1889) | Accumulate small advantages, right to attack |
| Tarrasch — *The Game of Chess* (1931) | Bad bishop, isolated pawn duality, open files |
| Réti — *Modern Ideas in Chess* (1923) | Hypermodern centre control, pawn flexibility |
| Lasker — *Manual of Chess* (1927) | Initiative value, practical problems, fight on |
| Nimzowitsch — *My System* + *Chess Praxis* | Prophylaxis, blockade, restraint, outposts |
| Capablanca — *Chess Fundamentals* (1921) | Two weaknesses, technique, king activation |
| Alekhine — *My Best Games* Vol. 1–2 | Dynamic compensation, long-term sacrifice |
| Euwe & Kramer — *The Middlegame* Vol. 1–2 | Planning, minority attack, piece exchange |
| Bronstein — *Zurich 1953* | Initiative chains, activity as material |
| Fischer — *My 60 Memorable Games* | d5 outpost, prophylaxis, bishop pair technique |
| Silman — *How to Reassess Your Chess* | Seven imbalances checklist |
| Kotov — *Think/Play Like a Grandmaster* | Candidate moves, tree of variations |
| Keres & Kotov — *Art of the Middlegame* | Attack prerequisites, best defence = counterattack |
| Dvoretsky — *Endgame Manual* | Fortress, zugzwang, corresponding squares |
| De la Villa — *100 Endgames You Must Know* | Lucena, Philidor, rook activity |
| Vukovic — *The Art of Attack in Chess* | Greek gift, h-file attack, mating nets |
| Chernev — *Logical Chess Move by Move* | Purposeful play, connect rooks, create threats |

Plus: all major opening systems with ECO codes, counter-relationships, and transpositions.

The retrieval engine detects 8 board features (passed pawns, open files, isolated/doubled pawns, bishop-vs-knight, two bishops, uncastled king, material imbalance) and scores principles by theme+tag overlap and novelty against the player's seen lessons.

---

## Persistent Player Profile

Stored at `~/.chessMentor/profile.json`:

```json
{
  "username": "Alice",
  "rating_estimate": 1350,
  "preferred_color": "both",
  "openings": {
    "white": ["Italian Game", "King's Gambit"],
    "black": ["Sicilian Najdorf", "French Defence"]
  },
  "strengths": ["consistent king safety", "active rook placement"],
  "weaknesses": ["missing back-rank threats", "poor endgame king activation"],
  "lessons": [
    "Always check for zwischenzug before recapturing",
    "The Lucena position: build a bridge to promote"
  ],
  "coach_notes": [
    {"ts": "2025-05-19T14:32:00", "note": "Tends to push kingside pawns too early"}
  ],
  "total_games_analyzed": 12
}
```

Profile updates arrive via **structured tool calls** (not text parsing) — the LLM calls `update_player_profile(lessons=[...], weaknesses=[...])` and the arguments are directly written to disk. The conversation history (`~/.chessMentor/conversation.json`) persists across sessions so the coach remembers everything discussed.

---

## Installation

```bash
git clone https://github.com/jark1ua/chessMentor
cd chessMentor
pip install -r requirements.txt

# Stockfish (for local engine fallback)
# Ubuntu/Debian:
sudo apt install stockfish
# macOS:
brew install stockfish
# Windows: download from https://stockfishchess.org/download/
```

---

## Quick Start

```bash
# Minimum — Claude vision + Claude coaching
export ANTHROPIC_API_KEY=sk-ant-...
python main.py

# Recommended — CV board detection (no vision tokens) + DeepSeek coaching (near-free)
export VISION_PROVIDER=cv
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-...
python main.py

# OpenRouter (200+ models, many free)
export LLM_PROVIDER=openrouter
export OPENROUTER_API_KEY=sk-or-...
export OPENROUTER_MODEL=deepseek/deepseek-chat   # or meta-llama/llama-3.3-70b-instruct
python main.py

# Fully local (no API costs, no internet after first run)
export VISION_PROVIDER=cv
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.1
python main.py

# Fallback chain: try OpenRouter first, fall back to Claude if it fails
export LLM_PROVIDER=fallback
export LLM_FALLBACK_CHAIN=openrouter,claude
export OPENROUTER_API_KEY=sk-or-...
export ANTHROPIC_API_KEY=sk-ant-...
python main.py

# Pass screen region directly (left,top,width,height in pixels)
python main.py --region 100,200,800,800

# Debug: capture one screenshot and save it for inspection
python main.py --region 100,200,800,800 --debug-capture
```

---

## Profile Management

```bash
python main.py --set-name "Alice"
python main.py --set-rating 1350
python main.py --profile        # display full profile
python main.py --history        # show last 20 match summaries
```

---

## Configuration Reference

All settings are environment variables:

### Core
| Variable | Default | Description |
|---|---|---|
| `CAPTURE_INTERVAL` | `5` | Seconds between screenshots |
| `COACHING_THRESHOLD` | `100` | Centipawn loss to trigger coaching |

### Vision (board detection)
| Variable | Default | Options |
|---|---|---|
| `VISION_PROVIDER` | `claude` | `cv` · `claude` · `openai` · `gemini` |
| `CV_MODEL_PATH` | *(empty)* | Path to TorchScript piece classifier (optional; heuristic used if unset) |
| `OPENAI_VISION_MODEL` | `gpt-4o` | Any OpenAI vision model |
| `GEMINI_VISION_MODEL` | `gemini-1.5-flash` | Any Gemini vision model |

### Engine
| Variable | Default | Options |
|---|---|---|
| `ENGINE_PROVIDER` | `auto` | `auto` (Lichess→local) · `lichess` · `local` |
| `STOCKFISH_PATH` | `stockfish` | Path to binary |
| `ENGINE_TOP_MOVES` | `3` | Top moves shown to coach |

### LLM (coaching)
| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `claude` | `claude` · `openai` · `openrouter` · `deepseek` · `ollama` · `fallback` |
| `LLM_FALLBACK_CHAIN` | `openrouter,claude` | Comma-separated chain for `fallback` mode |
| `CLAUDE_MODEL` | `claude-opus-4-7` | Anthropic model ID |
| `ANTHROPIC_API_KEY` | | |
| `OPENAI_API_KEY` | | |
| `OPENAI_LLM_MODEL` | `gpt-4o` | |
| `OPENROUTER_API_KEY` | | Get at openrouter.ai |
| `OPENROUTER_MODEL` | `deepseek/deepseek-chat` | Any model slug from openrouter.ai/models |
| `DEEPSEEK_API_KEY` | | Get at platform.deepseek.com |
| `DEEPSEEK_MODEL` | `deepseek-chat` | `deepseek-chat` or `deepseek-reasoner` |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | |
| `OLLAMA_MODEL` | `llama3` | Any model pulled in Ollama |

---

## Cost Guide

| Setup | Vision cost | Coaching cost | Notes |
|---|---|---|---|
| `VISION_PROVIDER=cv` + DeepSeek | **$0** | ~$0.001/game | Recommended default |
| `VISION_PROVIDER=cv` + OpenRouter free model | **$0** | **$0** | Llama-3.3-70B free tier |
| `VISION_PROVIDER=cv` + Ollama | **$0** | **$0** | Fully local, no internet |
| `VISION_PROVIDER=claude` + Claude | ~$0.01/move | ~$0.01/call | Most accurate vision |
| Fallback chain | **$0**→paid | **$0**→paid | Automatic cost control |

---

## Data Files

```
~/.chessMentor/
  profile.json       ← player identity, lessons, weaknesses, strengths, openings
  conversation.json  ← full coaching conversation history (last 60 messages)
  history.json       ← post-game summaries
```

---

## Ideas and Planned Improvements

Things not yet built that would meaningfully improve the system:

1. **Opening book identification** — use python-chess's ECO lookup or a polyglot book to name the opening being played in real time and record it automatically, rather than relying on the LLM to recognise it.

2. **PGN export** — detect and record moves during the session and export an annotated PGN with coach comments embedded as `{...}` annotations. Reviewable in any chess GUI after the game.

3. **Tactical puzzle recommendation** — after each game, query Lichess's puzzle API filtered by the tactical themes (pin, back-rank, Greek gift) that appeared in this player's weaknesses, and present 3 puzzles to solve.

4. **Voice coaching** — pipe coaching text through `pyttsx3` or `espeak` so you hear the coach without looking away from the board.

5. **Auto-detect chess website windows** — instead of manually entering pixel coordinates, detect an open chess.com or lichess browser window using accessibility APIs (`pygetwindow`, `Wnck`) and automatically set the region.

6. **Visual overlay** — draw the evaluation bar and best-move arrow as a transparent overlay on the chess window using `tkinter` or `pygame`, so the analysis is visible in-game.

7. **Time control awareness** — detect time remaining (OCR on the clock region) and shorten coaching messages automatically when the player is under 2 minutes.

8. **Endgame tablebase integration** — for positions with 6 or fewer pieces, query the Lichess tablebase API for the exact WDL result and DTZ, so the coach can state definitively "this is a drawn rook ending" rather than relying on engine evaluation.

9. **Blunder threshold auto-calibration** — adapt `COACHING_THRESHOLD` to each player's average accuracy across their session history, so a 600-rated player isn't coached on every 80cp inaccuracy and a 1800-rated player isn't let off for 100cp losses.

10. **Web dashboard** — a small Flask server (`python main.py --serve`) showing profile stats, match history graph, lesson library, and opening frequency chart in the browser.
