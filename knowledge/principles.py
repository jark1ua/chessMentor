"""
Structured chess knowledge base drawn from classic instructional books.

Each principle is a dict with:
  id, source, theme, tags, title, principle
"""

PRINCIPLES = [
    # -------------------------------------------------------------------------
    # Nimzowitsch — "My System"
    # -------------------------------------------------------------------------
    {
        "id": "nim_prophylaxis_1",
        "source": "My System — Nimzowitsch",
        "theme": "strategy",
        "tags": ["prophylaxis", "prevention", "opponent_plan"],
        "title": "Prophylaxis: Prevent Before You Create",
        "principle": (
            "Before executing your own plan, ask: what is my opponent threatening? "
            "Prophylaxis means neutralising the enemy's intentions before they materialise. "
            "A player who constantly prevents the opponent's plans while advancing their own "
            "will rarely be surprised. This habit of thinking prophylactically is what separates "
            "strategic masters from tactical opportunists."
        ),
    },
    {
        "id": "nim_blockade_1",
        "source": "My System — Nimzowitsch",
        "theme": "pawn_structure",
        "tags": ["blockade", "passed_pawn", "knight", "outpost"],
        "title": "The Blockade of Passed Pawns",
        "principle": (
            "A passed pawn's power lies in its potential to queen; the best way to neutralise it "
            "is to place a piece — ideally a knight — directly in front of it. "
            "The blockader paralyses the pawn and turns it from an asset into a liability. "
            "Knights are the ideal blockaders because they lose no mobility sitting in front of a pawn, "
            "whereas bishops and rooks are more powerful on open diagonals and files respectively."
        ),
    },
    {
        "id": "nim_outpost_1",
        "source": "My System — Nimzowitsch",
        "theme": "piece_activity",
        "tags": ["outpost", "knight", "weak_square", "piece_activity"],
        "title": "Establishing an Outpost",
        "principle": (
            "An outpost is a square in or near the opponent's position that cannot be attacked "
            "by an enemy pawn. A knight planted on such a square becomes enormously powerful. "
            "To create an outpost, provoke or trade away the pawn that guards that square, "
            "then occupy it with your knight. The resulting piece will dominate the game."
        ),
    },
    {
        "id": "nim_passed_pawn_1",
        "source": "My System — Nimzowitsch",
        "theme": "endgame",
        "tags": ["passed_pawn", "endgame", "promotion"],
        "title": "The Passed Pawn Must Advance",
        "principle": (
            "A passed pawn is a potential queen — its strength increases the closer it gets to "
            "the promotion square. Do not be content to simply have a passed pawn; push it "
            "at every safe opportunity. The opponent must commit forces to stopping it, "
            "which creates weaknesses elsewhere. In the endgame, a protected passed pawn "
            "supported by the king is often a decisive advantage."
        ),
    },
    {
        "id": "nim_overprotection_1",
        "source": "My System — Nimzowitsch",
        "theme": "strategy",
        "tags": ["overprotection", "key_square", "prophylaxis"],
        "title": "Overprotect Your Key Points",
        "principle": (
            "Overprotection means defending an important pawn or square with more pieces than "
            "strictly necessary. This ensures that if one defender is exchanged, others remain. "
            "Key points are usually strong central pawns, outpost squares, or pieces that anchor "
            "your position. By overprotecting them you deprive the opponent of tactical tricks "
            "based on undermining these points."
        ),
    },
    {
        "id": "nim_restraint_1",
        "source": "My System — Nimzowitsch",
        "theme": "strategy",
        "tags": ["restraint", "space", "pawn_chain"],
        "title": "Restraint of the Pawn Chain",
        "principle": (
            "When the opponent has a pawn chain, attack its base — the rearmost pawn — rather "
            "than its head. Restraining the chain means preventing the pawns from advancing "
            "and suffocating the pieces behind them. Combine restraint with piece pressure "
            "against the base; once the base falls, the whole chain collapses."
        ),
    },
    {
        "id": "nim_rook_file_1",
        "source": "My System — Nimzowitsch",
        "theme": "piece_activity",
        "tags": ["open_file", "rook", "piece_activity"],
        "title": "Rooks Belong on Open Files",
        "principle": (
            "A rook's power is maximised on an open or semi-open file where it controls the "
            "entire column. Seize open files immediately and contest them if the opponent tries "
            "the same. A rook penetrating to the 7th rank attacks the enemy pawns and confines "
            "the king. Always look to double rooks on an open file or establish one on the 7th."
        ),
    },

    # -------------------------------------------------------------------------
    # Capablanca — "Chess Fundamentals"
    # -------------------------------------------------------------------------
    {
        "id": "capa_rook_7th_1",
        "source": "Chess Fundamentals — Capablanca",
        "theme": "piece_activity",
        "tags": ["rook", "seventh_rank", "endgame", "piece_activity"],
        "title": "The Rook on the Seventh Rank",
        "principle": (
            "A rook on the seventh rank is extremely powerful in the endgame: it attacks the "
            "opponent's unadvanced pawns and cuts off the enemy king from the action. "
            "If you can establish a rook on the 7th (or 2nd for Black), do so as soon as possible. "
            "Two rooks on the seventh rank together are often decisive regardless of material balance."
        ),
    },
    {
        "id": "capa_king_endgame_1",
        "source": "Chess Fundamentals — Capablanca",
        "theme": "endgame",
        "tags": ["king_activity", "endgame", "king"],
        "title": "Activate the King in the Endgame",
        "principle": (
            "In the endgame the king is a fighting piece and must be brought to the centre "
            "as quickly as possible. A passive king is one of the most common reasons for losing "
            "a drawn or even winning endgame. March the king toward the key pawns and squares; "
            "it should lead from the front, not hide on the back rank."
        ),
    },
    {
        "id": "capa_simplification_1",
        "source": "Chess Fundamentals — Capablanca",
        "theme": "endgame",
        "tags": ["simplification", "technique", "material_advantage"],
        "title": "Simplify When You Are Ahead in Material",
        "principle": (
            "When you have a material advantage, exchange pieces — not pawns. "
            "Reducing piece count converts a material edge into a technically won endgame "
            "while reducing the opponent's counterplay opportunities. Avoid unnecessary "
            "complications when ahead; let simplicity do the work for you."
        ),
    },
    {
        "id": "capa_opposition_1",
        "source": "Chess Fundamentals — Capablanca",
        "theme": "endgame",
        "tags": ["opposition", "king_endgame", "endgame"],
        "title": "The Opposition in King and Pawn Endgames",
        "principle": (
            "Opposition occurs when two kings stand on the same file, rank, or diagonal with "
            "an odd number of squares between them. The player who does NOT have the move "
            "holds the opposition and forces the other king to give way. "
            "Mastering opposition is essential in king-and-pawn endings: the attacking king "
            "uses it to outflank the defender and escort the pawn to promotion."
        ),
    },
    {
        "id": "capa_pawn_endings_1",
        "source": "Chess Fundamentals — Capablanca",
        "theme": "endgame",
        "tags": ["pawn_structure", "endgame", "passed_pawn"],
        "title": "Pawn Structure Determines Endgame Plans",
        "principle": (
            "The pawn structure in the endgame dictates the winning plan. Identify your "
            "candidate passed pawn or potential passed pawn, and direct your king toward "
            "supporting it. Meanwhile, prevent the opponent from creating their own passed pawn. "
            "Study the pawn majority and understand which side it favours."
        ),
    },
    {
        "id": "capa_piece_coordination_1",
        "source": "Chess Fundamentals — Capablanca",
        "theme": "middlegame",
        "tags": ["piece_coordination", "harmony", "strategy"],
        "title": "Coordinate Your Pieces",
        "principle": (
            "Pieces working in harmony are far more powerful than the same pieces working "
            "independently. Before calculating tactics, ask whether all your pieces are "
            "contributing to a unified plan. Inactive pieces should be repositioned so that "
            "every unit participates in the campaign."
        ),
    },

    # -------------------------------------------------------------------------
    # Silman — "How to Reassess Your Chess"
    # -------------------------------------------------------------------------
    {
        "id": "silman_imbalance_1",
        "source": "How to Reassess Your Chess — Silman",
        "theme": "strategy",
        "tags": ["imbalance", "bishop_vs_knight", "strategy"],
        "title": "Identify and Exploit Imbalances",
        "principle": (
            "Every position contains imbalances — differences between the two sides: "
            "material, pawn structure, piece activity, space, king safety, etc. "
            "Your plan should be built around exploiting YOUR imbalances and neutralising "
            "the opponent's. Do not blindly follow general rules; instead, ask what is "
            "unique about this specific position."
        ),
    },
    {
        "id": "silman_bishop_knight_1",
        "source": "How to Reassess Your Chess — Silman",
        "theme": "strategy",
        "tags": ["bishop_vs_knight", "imbalance", "pawn_structure"],
        "title": "Bishop vs Knight: Choose Based on Pawn Structure",
        "principle": (
            "Bishops excel in open positions with pawns on both sides of the board and long "
            "diagonal control. Knights are superior in closed positions, where their jumping "
            "ability and the availability of outposts make them dominant. "
            "When you have a bishop, try to open the position; when you have a knight, "
            "keep it closed and find it an outpost."
        ),
    },
    {
        "id": "silman_weak_squares_1",
        "source": "How to Reassess Your Chess — Silman",
        "theme": "pawn_structure",
        "tags": ["weak_square", "hole", "outpost", "pawn_structure"],
        "title": "Exploit Weak Squares (Holes)",
        "principle": (
            "A weak square is one that can no longer be defended by a pawn. "
            "Once a square becomes permanently weak — a 'hole' — place a piece on it, "
            "especially a knight which cannot be chased away. "
            "Creating weak squares in the opponent's position is a long-term strategic "
            "investment that pays off in the endgame."
        ),
    },
    {
        "id": "silman_two_bishops_1",
        "source": "How to Reassess Your Chess — Silman",
        "theme": "piece_activity",
        "tags": ["two_bishops", "bishop_pair", "imbalance", "open_position"],
        "title": "The Power of the Bishop Pair",
        "principle": (
            "Two bishops together control both colours and dominate open positions. "
            "The bishop pair is a long-term advantage — fight to keep it and to open "
            "the position when you possess it. If your opponent has two bishops, look "
            "to close the position with pawns and trade one bishop off to reduce its scope."
        ),
    },
    {
        "id": "silman_space_1",
        "source": "How to Reassess Your Chess — Silman",
        "theme": "strategy",
        "tags": ["space", "imbalance", "pawn_center"],
        "title": "Space as an Imbalance",
        "principle": (
            "The player with more space has more room to manoeuvre and can regroup pieces "
            "more easily. A space advantage is most useful when the position is not yet "
            "fully blocked — keep some tension so your pieces can exploit the extra room. "
            "When cramped, seek exchanges to relieve the bind, or counterattack the "
            "opponent's advanced pawns."
        ),
    },
    {
        "id": "silman_pawn_structure_1",
        "source": "How to Reassess Your Chess — Silman",
        "theme": "pawn_structure",
        "tags": ["pawn_structure", "isolated_pawn", "doubled_pawn", "weakness"],
        "title": "Understand Your Pawn Structure",
        "principle": (
            "Pawn structure determines the long-term character of the position. "
            "Isolated pawns lack pawn defenders and become targets; doubled pawns "
            "are immobile and may create open files for the opponent. "
            "Always assess whether your pawn moves create lasting weaknesses. "
            "A pawn cannot move backward — every pawn advance is a permanent commitment."
        ),
    },

    # -------------------------------------------------------------------------
    # Kotov — "Think Like a Grandmaster"
    # -------------------------------------------------------------------------
    {
        "id": "kotov_candidates_1",
        "source": "Think Like a Grandmaster — Kotov",
        "theme": "tactics",
        "tags": ["candidate_moves", "calculation", "thought_process"],
        "title": "Establish Candidate Moves Before Calculating",
        "principle": (
            "Before calculating any variation, first list all candidate moves — the moves "
            "worth considering. Do not start calculating the first move that comes to mind; "
            "survey the board systematically and then pick the two or three most promising "
            "candidates. Only after establishing your candidates should you calculate deeply."
        ),
    },
    {
        "id": "kotov_tree_1",
        "source": "Think Like a Grandmaster — Kotov",
        "theme": "tactics",
        "tags": ["calculation", "tree_of_variations", "discipline"],
        "title": "Calculate Each Line Once — the Tree of Variations",
        "principle": (
            "When calculating, imagine a tree of variations. Analyse each branch completely "
            "before moving to the next — do not hop back and forth. If you re-analyse the "
            "same line multiple times you waste time and introduce errors. "
            "Discipline in calculation — one branch at a time, to its conclusion — is the "
            "hallmark of accurate tactical play."
        ),
    },
    {
        "id": "kotov_blunder_1",
        "source": "Think Like a Grandmaster — Kotov",
        "theme": "tactics",
        "tags": ["blunder_check", "safety", "last_check"],
        "title": "Always Perform a Final Blunder Check",
        "principle": (
            "Before making any move, pause and ask: does this move leave anything en prise? "
            "Does it allow a fork, pin, skewer, or back-rank mate? "
            "Time pressure is no excuse for skipping this check. "
            "Many games are lost not by inferior strategy but by a simple oversight in the "
            "final moment before committing to a move."
        ),
    },
    {
        "id": "kotov_time_1",
        "source": "Think Like a Grandmaster — Kotov",
        "theme": "tactics",
        "tags": ["time_management", "calculation", "practical"],
        "title": "Budget Your Time According to Complexity",
        "principle": (
            "Spend your clock time proportionally to the complexity and criticality of "
            "each decision. Routine moves in quiet positions should be made quickly; "
            "sharp tactical junctures deserve deep thought. "
            "Running into severe time pressure is often the result of spending too long on "
            "non-critical moves early in the game."
        ),
    },
    {
        "id": "kotov_critical_1",
        "source": "Think Like a Grandmaster — Kotov",
        "theme": "middlegame",
        "tags": ["critical_moment", "plan", "evaluation"],
        "title": "Recognise the Critical Moment",
        "principle": (
            "Every game has a handful of critical moments where the correct decision "
            "dramatically changes the outcome. Learn to sense when the position is at "
            "a crossroads — usually when there are forcing continuations, material "
            "imbalances about to be resolved, or king safety is suddenly at issue. "
            "At these moments, invest the most time and care in your calculation."
        ),
    },

    # -------------------------------------------------------------------------
    # De la Villa — "100 Endgames You Must Know"
    # -------------------------------------------------------------------------
    {
        "id": "villa_lucena_1",
        "source": "100 Endgames You Must Know — De la Villa",
        "theme": "endgame",
        "tags": ["rook_endgame", "lucena", "winning_technique", "endgame"],
        "title": "The Lucena Position: Building a Bridge",
        "principle": (
            "The Lucena position arises in rook endgames when the attacking side has "
            "advanced the pawn to the 7th rank with the king in front of the pawn. "
            "The winning technique is 'building a bridge': use the rook to cut off the "
            "defending king while the attacking king steps out from in front of the pawn. "
            "Once the bridge is built, the pawn promotes. This is one of the most important "
            "endgame patterns every player must know."
        ),
    },
    {
        "id": "villa_philidor_1",
        "source": "100 Endgames You Must Know — De la Villa",
        "theme": "endgame",
        "tags": ["rook_endgame", "philidor", "drawing_technique", "endgame"],
        "title": "The Philidor Position: Defensive Rook Technique",
        "principle": (
            "The Philidor position is the key drawing technique in rook-vs-rook-and-pawn "
            "endgames. Place the defending rook on the third rank (the '6th-rank defence') "
            "to cut off the attacking king. Once the attacking king advances past the pawn, "
            "switch the rook to give checks from behind. "
            "Knowledge of both Lucena (win) and Philidor (draw) is essential for rook endgames."
        ),
    },
    {
        "id": "villa_king_pawn_1",
        "source": "100 Endgames You Must Know — De la Villa",
        "theme": "endgame",
        "tags": ["king_pawn_endgame", "opposition", "endgame", "key_squares"],
        "title": "Key Squares in King and Pawn Endgames",
        "principle": (
            "Every pawn has key squares: squares the attacking king must reach to guarantee "
            "promotion. For a pawn on the e, d, c, or f files the key squares are two ranks "
            "ahead of the pawn on the same and adjacent files. "
            "If the attacking king occupies a key square, the pawn always promotes regardless "
            "of the position of the defending king. Centralise your king toward these squares."
        ),
    },
    {
        "id": "villa_rook_behind_1",
        "source": "100 Endgames You Must Know — De la Villa",
        "theme": "endgame",
        "tags": ["rook_endgame", "rook_behind_passed_pawn", "endgame"],
        "title": "Place the Rook Behind the Passed Pawn",
        "principle": (
            "Whether you are the attacker or defender in a rook endgame involving a passed pawn, "
            "place the rook behind the pawn rather than in front of or beside it. "
            "The attacker's rook behind the pawn gains strength as the pawn advances. "
            "The defender's rook behind the passed pawn controls its march most effectively. "
            "This principle applies in the vast majority of practical rook endgames."
        ),
    },
    {
        "id": "villa_activity_1",
        "source": "100 Endgames You Must Know — De la Villa",
        "theme": "endgame",
        "tags": ["rook_activity", "endgame", "piece_activity"],
        "title": "Rook Activity Trumps Pawns in the Endgame",
        "principle": (
            "In rook endgames, an active rook is often worth more than an extra pawn. "
            "A passive rook defending its own pawns usually loses to an active rook that "
            "creates threats. When behind in material, activate your rook aggressively — "
            "create threats, attack enemy pawns, and keep your rook mobile rather than "
            "tying it to passive defence."
        ),
    },
    {
        "id": "villa_opposite_bishops_1",
        "source": "100 Endgames You Must Know — De la Villa",
        "theme": "endgame",
        "tags": ["opposite_color_bishops", "draw", "endgame"],
        "title": "Opposite-Colour Bishops Favour the Defender",
        "principle": (
            "When each side has a bishop on a different colour, the game frequently ends in a "
            "draw even with a material deficit of one or two pawns, because the bishops "
            "cannot oppose each other. The defender places pawns on the colour of the "
            "opponent's bishop, making them immune to attack. "
            "In attack, however, opposite-colour bishops can be devastating because the "
            "attacker's threats cannot be parried by the defending bishop."
        ),
    },

    # -------------------------------------------------------------------------
    # Vukovic — "The Art of Attack in Chess"
    # -------------------------------------------------------------------------
    {
        "id": "vukovic_castled_king_1",
        "source": "The Art of Attack in Chess — Vukovic",
        "theme": "king_safety",
        "tags": ["attack", "castled_king", "king_safety", "sacrifice"],
        "title": "Conditions for Attack on the Castled King",
        "principle": (
            "Before launching an attack on the castled king, verify that you have: "
            "a lead in piece activity near the king, open or semi-open files toward the enemy "
            "king, and that your own king is safe. Attacking without these conditions often "
            "leads to a failed attack and counterplay for the opponent. "
            "Prepare the attack methodically before committing."
        ),
    },
    {
        "id": "vukovic_sacrifice_1",
        "source": "The Art of Attack in Chess — Vukovic",
        "theme": "tactics",
        "tags": ["sacrifice", "king_safety", "attack", "h_file"],
        "title": "The Classic Bishop Sacrifice on h7",
        "principle": (
            "The bishop sacrifice Bxh7+ (or Bxh2+) is one of the most important attacking "
            "themes: the bishop is sacrificed to strip the king of its pawn cover. "
            "For it to succeed you typically need: a queen within striking distance, "
            "a knight that can reach g5 (or g4), and open lines toward the exposed king. "
            "Recognise this pattern quickly — it appears in many practical games."
        ),
    },
    {
        "id": "vukovic_uncastled_king_1",
        "source": "The Art of Attack in Chess — Vukovic",
        "theme": "king_safety",
        "tags": ["uncastled_king", "attack", "center", "king_safety"],
        "title": "Attack the Uncastled King via the Centre",
        "principle": (
            "When the opponent has failed to castle, open the centre immediately with "
            "pawn breaks — e.g. d4-d5, e4-e5 — to expose the king to attack on the "
            "central files. An uncastled king in an open centre is extremely vulnerable. "
            "Sacrifice material if necessary to open lines; the king's insecurity will "
            "compensate for any material investment."
        ),
    },
    {
        "id": "vukovic_h_file_1",
        "source": "The Art of Attack in Chess — Vukovic",
        "theme": "king_safety",
        "tags": ["h_file", "open_file", "king_attack", "rook"],
        "title": "Open the h-file Against the Castled King",
        "principle": (
            "The h-file is a natural target when attacking the castled king. Advance the "
            "h-pawn (h4-h5) to force open the h-file, then bring the rook to h1 (or h8). "
            "Combined with queen and minor pieces, a rook on the h-file creates mating threats "
            "that are very difficult to defend. This plan is especially powerful when the "
            "opponent's king has little piece protection."
        ),
    },
    {
        "id": "vukovic_mating_net_1",
        "source": "The Art of Attack in Chess — Vukovic",
        "theme": "tactics",
        "tags": ["mating_net", "coordination", "attack"],
        "title": "Build a Mating Net Systematically",
        "principle": (
            "A mating net is constructed by progressively restricting the enemy king's "
            "escape squares while bringing more attacking pieces into the area. "
            "Do not rush for a flashy combination before the net is ready; "
            "complete the encirclement first, then deliver the decisive blow. "
            "Check whether all escape squares are covered before each step."
        ),
    },

    # -------------------------------------------------------------------------
    # Chernev — "Logical Chess Move by Move"
    # -------------------------------------------------------------------------
    {
        "id": "chernev_purpose_1",
        "source": "Logical Chess Move by Move — Chernev",
        "theme": "opening",
        "tags": ["purposeful_play", "opening", "development"],
        "title": "Every Move Must Have a Purpose",
        "principle": (
            "Do not make moves just to make moves. Every move should have a clear purpose: "
            "developing a piece, controlling a key square, improving coordination, or "
            "creating a concrete threat. Aimless moves waste time and allow the opponent "
            "to seize the initiative. Before moving, ask: 'What does this move achieve?'"
        ),
    },
    {
        "id": "chernev_no_repeat_1",
        "source": "Logical Chess Move by Move — Chernev",
        "theme": "opening",
        "tags": ["development", "opening", "tempo"],
        "title": "Don't Move the Same Piece Twice in the Opening",
        "principle": (
            "Moving the same piece twice in the opening wastes a tempo and gives the opponent "
            "time to develop. Unless there is a concrete reason — such as winning material or "
            "avoiding a serious threat — develop a new piece each move. "
            "Every piece should be developed to its best square quickly; delay is dangerous "
            "when the opponent is building an efficient army."
        ),
    },
    {
        "id": "chernev_center_1",
        "source": "Logical Chess Move by Move — Chernev",
        "theme": "opening",
        "tags": ["center_control", "opening", "pawns"],
        "title": "Fight for the Centre in the Opening",
        "principle": (
            "The player who controls the centre can direct pieces to any part of the board "
            "more efficiently. In the opening, occupy or contest the central squares e4, d4, "
            "e5, d5 with pawns and pieces. Neglecting the centre allows the opponent to "
            "build a space advantage that will make the middlegame cramped and difficult."
        ),
    },
    {
        "id": "chernev_castle_1",
        "source": "Logical Chess Move by Move — Chernev",
        "theme": "king_safety",
        "tags": ["castling", "king_safety", "opening"],
        "title": "Castle Early to Ensure King Safety",
        "principle": (
            "Castling is the fastest way to get the king to safety and connect the rooks. "
            "Delay castling only when there is a concrete plan that justifies keeping the "
            "king in the centre. As a rule, castle within the first 10 moves unless the "
            "position demands otherwise. An uncastled king in an open game is an invitation "
            "for the opponent to open lines and attack."
        ),
    },
    {
        "id": "chernev_coordination_1",
        "source": "Logical Chess Move by Move — Chernev",
        "theme": "middlegame",
        "tags": ["piece_coordination", "harmony", "rook_connection"],
        "title": "Connect Your Rooks",
        "principle": (
            "After developing all pieces and castling, your next priority is connecting the "
            "rooks by clearing the back rank of all minor pieces. Connected rooks mutually "
            "defend each other and control the entire rank, ready to be deployed to any "
            "open file. Disconnected rooks are far weaker and cannot support each other."
        ),
    },
    {
        "id": "chernev_threats_1",
        "source": "Logical Chess Move by Move — Chernev",
        "theme": "tactics",
        "tags": ["threats", "tactical_awareness", "initiative"],
        "title": "Create Threats With Every Move",
        "principle": (
            "The player who makes threats forces the opponent to react, maintaining the "
            "initiative. Even positional moves should ideally carry a threat — against a "
            "pawn, a piece, or a key square. When you stop making threats, the opponent "
            "regains freedom to pursue their own plan. Ask after every candidate move: "
            "'What does this threaten?'"
        ),
    },
]
