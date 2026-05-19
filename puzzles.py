"""
Lichess puzzle integration: fetch puzzles matched to the player's tactical weaknesses.

Uses GET https://lichess.org/api/puzzle/next (public, no auth required).
"""
from __future__ import annotations
from typing import List, Optional

import requests

# Map weakness keywords → Lichess puzzle theme slugs
_WEAKNESS_THEMES: List[tuple] = [
    ("pin",             ["pin"]),
    ("fork",            ["fork"]),
    ("back rank",       ["backRankMate"]),
    ("back-rank",       ["backRankMate"]),
    ("skewer",          ["skewer"]),
    ("discovered",      ["discoveredAttack"]),
    ("double check",    ["doubleCheck"]),
    ("endgame",         ["endgame"]),
    ("pawn endgame",    ["pawnEndgame"]),
    ("rook endgame",    ["rookEndgame"]),
    ("king safety",     ["kingsideAttack", "attackingF2F7"]),
    ("hanging",         ["hangingPiece"]),
    ("sacrifice",       ["sacrifice"]),
    ("promotion",       ["promotion"]),
    ("mate",            ["mateIn1", "mateIn2"]),
    ("mating",          ["mateIn1", "mateIn2"]),
    ("trapped",         ["trappedPiece"]),
    ("intermezzo",      ["intermezzo"]),
    ("zwischenzug",     ["intermezzo"]),
    ("tactics",         ["fork", "pin", "skewer"]),
    ("greek gift",      ["sacrifice"]),
]

_LICHESS_PUZZLE_URL = "https://lichess.org/api/puzzle/next"
_DEFAULT_THEMES = ["fork", "pin", "skewer"]


def _weaknesses_to_themes(weaknesses: List[str]) -> List[str]:
    seen: set = set()
    result: List[str] = []
    for w in weaknesses:
        w_lower = w.lower()
        for keyword, themes in _WEAKNESS_THEMES:
            if keyword in w_lower:
                for t in themes:
                    if t not in seen:
                        seen.add(t)
                        result.append(t)
    return result if result else _DEFAULT_THEMES


def _fetch_one(theme: Optional[str] = None) -> Optional[dict]:
    params: dict = {}
    if theme:
        params["themes"] = theme
    try:
        resp = requests.get(_LICHESS_PUZZLE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def fetch_puzzles_for_player(profile: dict, count: int = 3) -> List[dict]:
    """Fetch *count* puzzles targeted at the player's weaknesses."""
    themes = _weaknesses_to_themes(profile.get("weaknesses", []))
    puzzles: List[dict] = []
    for i in range(count):
        theme = themes[i % len(themes)]
        p = _fetch_one(theme)
        if p:
            puzzles.append(p)
    return puzzles


def format_puzzle(puzzle: dict, number: int = 1) -> str:
    """Return a terminal-friendly description of one Lichess puzzle."""
    try:
        data  = puzzle.get("puzzle", {})
        game  = puzzle.get("game",   {})
        fen   = game.get("fen", "(no FEN)")
        themes = data.get("themes", [])
        rating = data.get("rating", "?")
        pid    = data.get("id", "")
        lines = [
            f"Puzzle {number}  |  Rating: {rating}  |  Themes: {', '.join(themes)}",
            f"FEN: {fen}",
        ]
        if pid:
            lines.append(f"Solve online: https://lichess.org/training/{pid}")
        return "\n".join(lines)
    except Exception:
        return f"Puzzle {number}: (could not parse response)"


def run_puzzle_session(profile: dict) -> None:
    """Fetch and display 3 puzzles in the terminal."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        def show(msg, title=""):
            console.print(Panel(msg, title=f"[bold yellow]{title}[/bold yellow]", expand=False))
    except ImportError:
        def show(msg, title=""):
            print(f"\n=== {title} ===\n{msg}\n{'=' * 40}")

    weaknesses = profile.get("weaknesses", [])
    intro = (
        f"Targeting your weaknesses: {', '.join(weaknesses[:5])}"
        if weaknesses else
        "Fetching general tactical puzzles."
    )
    show(intro, "Tactical Training")

    puzzles = fetch_puzzles_for_player(profile, count=3)
    if not puzzles:
        show("Could not reach Lichess. Check your internet connection.", "Error")
        return

    for i, p in enumerate(puzzles, 1):
        show(format_puzzle(p, i), f"Puzzle {i} of {len(puzzles)}")

    show(
        "Open each FEN in lichess.org/analysis or any chess GUI to solve.\n"
        "Use the Lichess link to get the interactive solver and solution.",
        "How to solve"
    )
