"""
Post-match position review: walks through a saved annotated PGN,
queries Lichess cloud eval for key positions, and prompts the player
to find the best move.
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional

import chess
import chess.pgn
import requests

_CLOUD_URL = "https://lichess.org/api/cloud-eval"


def _cloud_eval(fen: str) -> Optional[dict]:
    try:
        r = requests.get(_CLOUD_URL, params={"fen": fen, "multiPv": 3}, timeout=8)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def _top_san(prev_board: chess.Board, cloud: Optional[dict]) -> Optional[str]:
    """Extract the engine's top move as SAN from a cloud-eval response."""
    if not cloud:
        return None
    pvs = cloud.get("pvs", [])
    if not pvs:
        return None
    uci = pvs[0].get("moves", "").split()
    if not uci:
        return None
    try:
        return prev_board.san(chess.Move.from_uci(uci[0]))
    except Exception:
        return None


def _show_fn():
    """Return (show, prompt_fn) using rich if available, else plain print."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        def show(msg, title=""):
            console.print(Panel(msg, title=f"[bold blue]{title}[/bold blue]", expand=False))
        def ask(msg):
            return console.input(f"[cyan]{msg}[/cyan] ").strip()
    except ImportError:
        def show(msg, title=""):
            print(f"\n--- {title} ---\n{msg}\n")
        def ask(msg):
            print(msg, end=" ", flush=True)
            return input().strip()
    return show, ask


def review_game(pgn_path: str, max_positions: int = 12) -> None:
    """
    Interactively review key positions from *pgn_path*.

    Key positions are those that have a coach comment embedded in the PGN.
    For each, the Lichess cloud is queried and the player is asked to find
    the best continuation.
    """
    show, ask = _show_fn()

    pgn_file = Path(pgn_path)
    if not pgn_file.exists():
        show(f"File not found: {pgn_path}", "Error")
        return

    with open(pgn_file, encoding="utf-8") as f:
        game = chess.pgn.read_game(f)

    if game is None:
        show("No game found in PGN file.", "Error")
        return

    headers = game.headers
    show(
        f"Event : {headers.get('Event', '?')}\n"
        f"White : {headers.get('White', '?')}  vs  "
        f"Black : {headers.get('Black', '?')}\n"
        f"Result: {headers.get('Result', '*')}",
        "Post-Game Review",
    )

    board = game.board()
    node  = game
    reviewed = 0

    while node.variations and reviewed < max_positions:
        next_node = node.variations[0]
        move = next_node.move

        # Only pause on annotated positions
        if next_node.comment:
            fen   = board.fen()
            cloud = _cloud_eval(fen)
            top   = _top_san(board, cloud)

            move_label = (
                f"{board.fullmove_number}{'.' if board.turn == chess.WHITE else '...'}"
                f"{board.san(move)}"
            )
            detail = (
                f"After {move_label}\n"
                f"Coach note: {next_node.comment}"
            )
            if top:
                detail += f"\n(Engine best: {top})"
            show(detail, f"Key Position {reviewed + 1}")

            guess = ask("Your move here? (Enter to skip):")
            if guess:
                try:
                    g_move = board.parse_san(guess)
                    g_san  = board.san(g_move)
                    if top and g_san == top:
                        show(f"✓ {g_san} — that's the engine's top choice!", "Correct!")
                    else:
                        resp = f"You chose {g_san}."
                        if top:
                            resp += f" Engine preferred {top}."
                        show(resp, "Analysis")
                except (chess.IllegalMoveError, chess.InvalidMoveError, ValueError):
                    show("Could not parse that move notation.", "Note")

            reviewed += 1

        board.push(move)
        node = next_node

    show(
        f"{reviewed} key position(s) reviewed.\n"
        "Open the PGN in Lichess, ChessBase, or any GUI for deeper study.",
        "Review Complete",
    )
