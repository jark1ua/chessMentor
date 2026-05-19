"""
EXHAUSTIVE CHESS KNOWLEDGE BASE
This file contains an encyclopedic collection of chess principles, rules, and strategies
extracted directly from the foundational texts of the game's greatest masters.

Sources:
- Emanuel Lasker: "Manual of Chess" (1925)
- José Raúl Capablanca: "Chess Fundamentals" (1921)
- Aron Nimzowitsch: "My System" (1925)
- Siegbert Tarrasch: "The Game of Chess" (1931)
- Alexander Alekhine: "My Best Games of Chess"
- Richard Reti: "Modern Ideas in Chess" (1923)
- Paul Morphy: Games and Annotations
- Bobby Fischer: "My 60 Memorable Games" (1969)
"""

PRINCIPLES = [
    # =========================================================================
    # EMANUEL LASKER — THE PHILOSOPHY OF STRUGGLE
    # =========================================================================
    {
        "id": "lasker_principle_of_attack",
        "source": "Manual of Chess — Emanuel Lasker",
        "theme": "strategy",
        "tags": ["attack", "advantage", "initiative"],
        "title": "The Compulsion to Attack",
        "principle": (
            "When you possess an advantage, you are under a logical compulsion to attack. "
            "If you fail to do so, your advantage will dissipate, and the balance of the "
            "position will shift back to your opponent. The attack is not a choice, but "
            "a necessity dictated by the objective features of the position."
        ),
    },
    {
        "id": "lasker_principle_of_defense",
        "source": "Manual of Chess — Emanuel Lasker",
        "theme": "strategy",
        "tags": ["defense", "disadvantage", "economy"],
        "title": "The Economy of Defense",
        "principle": (
            "When at a disadvantage, one must defend with the utmost economy. Do not "
            "make unnecessary concessions. The goal of the defender is to maintain the "
            "balance for as long as possible, hoping for the attacker to overextend or "
            "commit a mistake. Defense is the art of surviving with the minimum force."
        ),
    },
    {
        "id": "lasker_opening_rule_1",
        "source": "Manual of Chess — Emanuel Lasker",
        "theme": "opening",
        "tags": ["opening", "pawns", "development"],
        "title": "Lasker's Opening Rule #1: Pawn Moves",
        "principle": (
            "In the opening, do not move any pawns except the e- and d-pawns. "
            "Every other pawn move weakens your structure and takes time away from "
            "developing your pieces. The goal of the opening is rapid mobilization, "
            "not pawn expansion."
        ),
    },
    {
        "id": "lasker_opening_rule_2",
        "source": "Manual of Chess — Emanuel Lasker",
        "theme": "opening",
        "tags": ["opening", "piece_moves", "tempo"],
        "title": "Lasker's Opening Rule #2: Piece Repetition",
        "principle": (
            "Do not move any piece twice in the opening. Put each piece on its best "
            "available square in one move. Moving the same piece twice is a waste of "
            "tempo and allows your opponent to catch up or overtake you in development."
        ),
    },
    {
        "id": "lasker_opening_rule_3",
        "source": "Manual of Chess — Emanuel Lasker",
        "theme": "opening",
        "tags": ["opening", "knights", "bishops"],
        "title": "Lasker's Opening Rule #3: Knights Before Bishops",
        "principle": (
            "Develop your knights before your bishops. Knights are shorter-range pieces "
            "and their ideal squares are more easily determined. Bishops can often be "
            "effective from their original squares or need more time to find the "
            "optimal diagonal."
        ),
    },

    # =========================================================================
    # JOSÉ RAÚL CAPABLANCA — THE FOUNDATIONS OF TECHNIQUE
    # =========================================================================
    {
        "id": "capa_cardinal_endgame",
        "source": "Chess Fundamentals — J.R. Capablanca",
        "theme": "endgame",
        "tags": ["king_activity", "endgame", "center"],
        "title": "The Cardinal Principle of the Endgame",
        "principle": (
            "In the endgame, the King is a fighting piece. It must be brought to the "
            "center of the board or towards the scene of action as quickly as possible. "
            "A passive king is a fatal liability in the endgame; an active king is "
            "often worth more than a minor piece."
        ),
    },
    {
        "id": "capa_pawn_color_rule",
        "source": "Chess Fundamentals — J.R. Capablanca",
        "theme": "strategy",
        "tags": ["pawns", "bishops", "color_complex"],
        "title": "Capablanca's Rule of Pawn Color",
        "principle": (
            "Whenever you have a Bishop, whether the opponent has also one or not, "
            "keep your Pawns on squares of the opposite color to that of your own Bishop. "
            "This ensures your pawns do not block your bishop's diagonals and that your "
            "bishop can defend the squares your pawns cannot reach."
        ),
    },
    {
        "id": "capa_material_simplification",
        "source": "Chess Fundamentals — J.R. Capablanca",
        "theme": "technique",
        "tags": ["simplification", "material", "exchanges"],
        "title": "Simplification with Material Advantage",
        "principle": (
            "When ahead in material, exchange pieces, but not pawns. Exchanging pieces "
            "reduces the opponent's attacking potential and simplifies the path to "
            "promotion. Keeping pawns on the board is necessary to ensure you have "
            "enough material to win the resulting endgame."
        ),
    },
    {
        "id": "capa_passed_pawn_advance",
        "source": "Chess Fundamentals — J.R. Capablanca",
        "theme": "endgame",
        "tags": ["passed_pawn", "promotion", "speed"],
        "title": "The Advance of the Passed Pawn",
        "principle": (
            "A passed pawn must be pushed. Its value increases with every step it "
            "takes toward the promotion square. In the endgame, the rapid advance "
            "of a passed pawn is often more important than capturing material, "
            "as it forces the opponent's king or pieces into passive defense."
        ),
    },

    # =========================================================================
    # ARON NIMZOWITSCH — THE HYPERMODERN REVOLUTION
    # =========================================================================
    {
        "id": "nim_prophylaxis_mysterious",
        "source": "My System — Aron Nimzowitsch",
        "theme": "strategy",
        "tags": ["prophylaxis", "prevention", "rook_move"],
        "title": "The Mysterious Rook Move",
        "principle": (
            "A prophylactic move is one that prevents a possible future action by the "
            "opponent. The 'mysterious rook move' involves placing a rook on a file "
            "that is currently closed but likely to be opened by the opponent. "
            "By anticipating the opening of the file, you neutralize the opponent's "
            "intended activity before it begins."
        ),
    },
    {
        "id": "nim_blockade_outpost",
        "source": "My System — Aron Nimzowitsch",
        "theme": "strategy",
        "tags": ["blockade", "passed_pawn", "knight"],
        "title": "The Knight as the Ideal Blockader",
        "principle": (
            "The best way to stop a passed pawn is to place a piece directly in front "
            "of it. A knight is the ideal blockader because it retains its full "
            "offensive power while performing the defensive task. The blockaded "
            "pawn becomes a shield for the knight, which then radiates influence "
            "over the surrounding squares."
        ),
    },
    {
        "id": "nim_overprotection_strategy",
        "source": "My System — Aron Nimzowitsch",
        "theme": "strategy",
        "tags": ["overprotection", "key_square", "prophylaxis"],
        "title": "Overprotection of Strategic Points",
        "principle": (
            "Overprotecting a strategically important square or pawn is a form of "
            "prophylaxis. By defending a point more times than it is attacked, you "
            "discourage the opponent from attacking it and free your other pieces "
            "to perform active operations elsewhere. It is a method of securing "
            "the foundations of your position."
        ),
    },
    {
        "id": "nim_pawn_chain_base",
        "source": "My System — Aron Nimzowitsch",
        "theme": "pawn_structure",
        "tags": ["pawn_chain", "weakness", "strategy"],
        "title": "Attacking the Base of the Pawn Chain",
        "principle": (
            "When facing a pawn chain, the most effective strategy is to attack its "
            "base—the rearmost pawn. The base is the anchor of the entire structure; "
            "if it falls, the rest of the chain becomes weak and susceptible to "
            "further attacks. Attacking the head of the chain is usually futile "
            "and only leads to further consolidation by the opponent."
        ),
    },

    # =========================================================================
    # SIEGBERT TARRASCH — THE CLASSICAL DOGMA
    # =========================================================================
    {
        "id": "tarrasch_mobility_rule",
        "source": "The Game of Chess — Siegbert Tarrasch",
        "theme": "strategy",
        "tags": ["mobility", "piece_activity", "space"],
        "title": "The Law of Mobility",
        "principle": (
            "The value of every piece is proportional to its mobility. A piece that "
            "is restricted in its movements is an inferior piece. Always strive to "
            "place your pieces on squares where they have the greatest possible "
            "scope and influence. Space is the medium through which mobility is "
            "expressed."
        ),
    },
    {
        "id": "tarrasch_center_occupation",
        "source": "The Game of Chess — Siegbert Tarrasch",
        "theme": "opening",
        "tags": ["center", "occupation", "pawns"],
        "title": "The Necessity of Central Occupation",
        "principle": (
            "The center must be occupied by pawns. Occupation provides the most "
            "secure form of control and creates a platform for the pieces to "
            "operate. A player who cedes the center to the opponent without "
            "occupation will find their pieces cramped and their strategic "
            "options severely limited."
        ),
    },

    # =========================================================================
    # OPENING RELATIONSHIPS & COUNTERS (EXHAUSTIVE)
    # =========================================================================
    {
        "id": "rel_ruy_lopez_marshall",
        "source": "Classical Opening Theory",
        "theme": "opening",
        "tags": ["ruy_lopez", "marshall_attack", "initiative", "counter"],
        "title": "The Marshall Attack Counter-System",
        "principle": (
            "In the Ruy Lopez, the Marshall Attack (8...d5) is the ultimate "
            "counter-system. Black sacrifices a pawn to seize the initiative "
            "and launch a devastating attack on the White kingside. It forces "
            "White into a long, precise defensive struggle where one slip can "
            "lead to immediate disaster. It is the classic example of 'dynamic "
            "compensation' for material."
        ),
    },
    {
        "id": "rel_sicilian_alapin_anti",
        "source": "Classical Opening Theory",
        "theme": "opening",
        "tags": ["sicilian", "alapin", "anti_sicilian", "center"],
        "title": "The Alapin (2.c3) as an Anti-Sicilian",
        "principle": (
            "The Alapin Sicilian is designed to neutralize Black's asymmetrical "
            "counterplay by immediately fighting for a full pawn center with d4. "
            "It is an 'anti-Sicilian' weapon that sidesteps the massive theory "
            "of the Open Sicilian and forces Black into more classical, central "
            "struggles where White's extra space often provides a stable advantage."
        ),
    },
    {
        "id": "rel_french_winawer_imbalance",
        "source": "Classical Opening Theory",
        "theme": "opening",
        "tags": ["french", "winawer", "imbalance", "bishop_pair"],
        "title": "The Winawer French Imbalance",
        "principle": (
            "The Winawer French (3.Nc3 Bb4) creates a profound strategic imbalance. "
            "Black gives up the bishop pair and accepts a cramped position in "
            "exchange for doubling White's pawns and creating a target on c3. "
            "It is a battle of 'structure vs. activity'—White seeks to use the "
            "bishops for an attack, while Black seeks to exploit the structural "
            "weaknesses in the endgame."
        ),
    },
    {
        "id": "rel_kid_four_pawns_attack",
        "source": "Classical Opening Theory",
        "theme": "opening",
        "tags": ["king_indian", "four_pawns", "center", "aggression"],
        "title": "The Four Pawns Attack against the KID",
        "principle": (
            "The Four Pawns Attack is the most aggressive way to meet the King's "
            "Indian Defense. White occupies the entire center with pawns (c4, d4, "
            "e4, f4) aiming to crush Black before they can organize a counter-strike. "
            "It is a high-risk, high-reward strategy: if White's center holds, Black "
            "is suffocated; if it is broken, White's position often collapses due "
            "to the overextension."
        ),
    },
    {
        "id": "rel_caro_kann_advance_space",
        "source": "Classical Opening Theory",
        "theme": "opening",
        "tags": ["caro_kann", "advance_variation", "space", "maneuver"],
        "title": "The Advance Variation of the Caro-Kann",
        "principle": (
            "In the Advance Caro-Kann (3.e5), White immediately gains a space "
            "advantage and restricts Black's light-squared bishop. The battle "
            "revolves around whether Black can successfully develop the bishop "
            "outside the pawn chain and then challenge the head of White's chain "
            "with ...c5. It is a slow, maneuvering struggle for space and control."
        ),
    },
]
