"""
Comprehensive chess knowledge base drawn from primary classical sources.

Sources used (primary texts, not articles about them):
  - Paul Morphy game annotations (Löwenthal, Sergeant, Edge)
  - Wilhelm Steinitz — "The Modern Chess Instructor" (1889)
  - Siegbert Tarrasch — "The Game of Chess" (1931), "Three Hundred Chess Games"
  - Richard Réti — "Masters of the Chessboard" (1932), "Modern Ideas in Chess" (1923)
  - Emanuel Lasker — "Manual of Chess" (1927), "Common Sense in Chess" (1896)
  - Nimzowitsch — "My System" (1925), "Chess Praxis" (1929)
  - Capablanca — "Chess Fundamentals" (1921), "My Chess Career" (1920)
  - Alekhine — "My Best Games 1908-1923", "My Best Games 1924-1937"
  - Euwe & Kramer — "The Middlegame" Vol. I & II (1964)
  - Bronstein — "Zurich International Chess Tournament 1953"
  - Kotov — "Think Like a Grandmaster" (1971), "Play Like a Grandmaster" (1978)
  - Fischer — "My 60 Memorable Games" (1969)
  - Silman — "How to Reassess Your Chess" (1993)
  - Vukovic — "The Art of Attack in Chess" (1965)
  - Chernev — "Logical Chess Move by Move" (1957)
  - De la Villa — "100 Endgames You Must Know" (2008)
  - Dvoretsky — "Endgame Manual" (2003), "School of Chess Excellence"
  - Keres & Kotov — "The Art of the Middlegame" (1964)

Structure of each entry:
  id, source, theme, tags, title, principle
  Opening entries additionally have: eco, counters, transposes_to
"""

# ---------------------------------------------------------------------------
# SECTION 1 — MORPHY ERA: Development, Initiative, Open Lines
# ---------------------------------------------------------------------------

_MORPHY = [
    {
        "id": "morphy_development_1",
        "source": "Paul Morphy — game annotations (Sergeant, 1916)",
        "theme": "opening",
        "tags": ["development", "initiative", "open_game", "tempo"],
        "title": "Development Is the Supreme Obligation",
        "principle": (
            "Morphy's practice established the foundation of modern opening theory: "
            "develop every piece to its best square as rapidly as possible, castle early, "
            "and connect the rooks. He demonstrated again and again — against the strongest "
            "players of his era — that a player who completes development first can launch "
            "an irresistible attack regardless of minor material concessions. "
            "The player behind in development is always in practical danger."
        ),
    },
    {
        "id": "morphy_open_lines_1",
        "source": "Paul Morphy — game annotations (Löwenthal, 1860)",
        "theme": "opening",
        "tags": ["open_file", "open_game", "initiative", "sacrifice", "development"],
        "title": "Open Lines Immediately, Even at the Cost of a Pawn",
        "principle": (
            "Morphy routinely sacrificed a pawn — or accepted gambits — to open lines "
            "toward the enemy king before development was complete. His Opera Game "
            "(1858 vs. the Duke of Brunswick) is the archetypal illustration: two pawns "
            "sacrificed for open files, followed by a rook-and-queen battery and a model "
            "mating attack. If the opponent lags in development, open the position immediately; "
            "closed positions forgive tardiness, open positions do not."
        ),
    },
    {
        "id": "morphy_dont_grab_pawns_1",
        "source": "Paul Morphy — game annotations (Edge, 1859)",
        "theme": "opening",
        "tags": ["development", "tempo", "pawn_grab", "opening"],
        "title": "Do Not Hunt Pawns in the Opening",
        "principle": (
            "Morphy criticised pawn-grabbing in the opening as a fundamental error. "
            "Taking a wing pawn with the queen or bishop before development is complete "
            "costs multiple tempi when the piece is chased back. "
            "The material gain is far outweighed by the opponent's free development. "
            "Decline material offers that cost time unless the resulting position is "
            "demonstrably winning by force."
        ),
    },
    {
        "id": "morphy_attack_uncastled_1",
        "source": "Paul Morphy — game annotations (Sergeant, 1916)",
        "theme": "king_safety",
        "tags": ["uncastled_king", "attack", "open_file", "initiative", "king_safety"],
        "title": "Strike Mercilessly Against the Uncastled King",
        "principle": (
            "If the opponent has not castled and the centre is open, Morphy's principle "
            "is absolute: open lines toward the enemy king at once, sacrificing material "
            "if needed. Every piece must be brought into the attack. The king in the centre "
            "of an open board is fundamentally unsafe; the attacker who hesitates loses the "
            "window. In Morphy vs. Paulsen (1857), he sacrificed a queen to expose the king "
            "— a pattern that recurs throughout his career."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 2 — STEINITZ: The First Positional School
# ---------------------------------------------------------------------------

_STEINITZ = [
    {
        "id": "steinitz_accumulate_1",
        "source": "The Modern Chess Instructor — Steinitz (1889)",
        "theme": "strategy",
        "tags": ["positional_play", "small_advantages", "accumulation", "strategy"],
        "title": "Accumulate Small Advantages",
        "principle": (
            "Steinitz's central doctrine: a player is not entitled to attack unless he has "
            "a concrete positional advantage. Instead of seeking brilliant sacrifices, "
            "accumulate small advantages — a better pawn structure, an outpost, the two "
            "bishops, the open file — until they compound into a decisive edge. "
            "An attack launched without positional preparation will fail against correct defence; "
            "one that grows from accumulated advantage is unstoppable."
        ),
    },
    {
        "id": "steinitz_fortress_1",
        "source": "The Modern Chess Instructor — Steinitz (1889)",
        "theme": "strategy",
        "tags": ["defence", "fortress", "king_safety", "positional_play"],
        "title": "The Art of Defence: Build a Fortress",
        "principle": (
            "Steinitz pioneered the understanding that a king in the centre is not always "
            "weak — if the position is closed and all entry squares are covered, it can be "
            "perfectly safe. When defending, identify and overprotect every entry point "
            "before the opponent can exploit it. A true fortress has no weaknesses; "
            "the defender's task is to maintain this integrity under pressure."
        ),
    },
    {
        "id": "steinitz_right_to_attack_1",
        "source": "The Modern Chess Instructor — Steinitz (1889)",
        "theme": "strategy",
        "tags": ["attack", "positional_advantage", "strategy", "initiative"],
        "title": "The Right to Attack Must Be Earned",
        "principle": (
            "Steinitz: 'The right of attack belongs only to the side with a positional "
            "advantage — and the attack is not only a right but an obligation.' "
            "Attacking with equal or inferior position is objectively unjustified "
            "and will fail against a well-informed opponent. Earn your attack through "
            "superior development, pawn structure, or piece activity before committing "
            "forces to the offensive."
        ),
    },
    {
        "id": "steinitz_weak_pawns_1",
        "source": "The Modern Chess Instructor — Steinitz (1889)",
        "theme": "pawn_structure",
        "tags": ["weak_square", "isolated_pawn", "backward_pawn", "pawn_structure"],
        "title": "Weak Pawns Are Permanent Targets",
        "principle": (
            "Steinitz categorised weaknesses with precision: an isolated pawn has no "
            "pawn neighbours and must be defended by pieces alone. A backward pawn cannot "
            "advance because the square ahead is controlled. Both become fixed targets "
            "in the endgame. Strategy dictates: fix the enemy's weak pawns, then attack "
            "them with pieces. The side burdened with weak pawns is forever on the defensive."
        ),
    },
    {
        "id": "steinitz_strong_center_1",
        "source": "The Modern Chess Instructor — Steinitz (1889)",
        "theme": "opening",
        "tags": ["pawn_center", "center_control", "strategy", "space"],
        "title": "A Strong Pawn Centre Provides the Platform for All Plans",
        "principle": (
            "Steinitz demonstrated that a mobile, well-supported pawn centre controls "
            "space and restricts the opponent's pieces. Pawns on e4-d4 (or e5-d5) "
            "limit the opponent's piece mobility and provide outpost squares for knights. "
            "Before any wing attack, secure the centre — an attack on the flank while "
            "the centre is unstable will be met by a central counter."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 3 — TARRASCH: Classical Doctrine
# ---------------------------------------------------------------------------

_TARRASCH = [
    {
        "id": "tarrasch_piece_activity_1",
        "source": "The Game of Chess — Tarrasch (1931)",
        "theme": "strategy",
        "tags": ["piece_activity", "bad_bishop", "passive_pieces", "strategy"],
        "title": "A Badly Placed Piece Is Worse Than No Piece at All",
        "principle": (
            "Tarrasch: a piece placed on a bad square, blocked by its own pawns, "
            "contributes nothing and may actively hinder the coordination of others. "
            "The 'bad bishop' — hemmed in by pawns on its own colour — is the classic "
            "example. Identify your worst-placed piece and improve it before making "
            "other plans. Consistent piece improvement is the essence of positional play."
        ),
    },
    {
        "id": "tarrasch_isolated_pawn_1",
        "source": "The Game of Chess — Tarrasch (1931)",
        "theme": "pawn_structure",
        "tags": ["isolated_pawn", "isolani", "middlegame", "endgame", "pawn_structure"],
        "title": "The Isolated Pawn: Power in the Middlegame, Weakness in the Endgame",
        "principle": (
            "Tarrasch gave the isolated queen's pawn its correct assessment: in the "
            "middlegame it grants the owner space, open files for rooks, and outpost "
            "squares (e5/c5 for an isolated d-pawn). The pieces activity it generates "
            "often outweighs its structural defect. But as pieces are exchanged, the "
            "isolani becomes a pure target. The defender must reach an endgame; "
            "the attacker must prevent it."
        ),
    },
    {
        "id": "tarrasch_open_file_rook_1",
        "source": "Three Hundred Chess Games — Tarrasch (1895)",
        "theme": "piece_activity",
        "tags": ["open_file", "rook", "piece_activity", "rook_endgame"],
        "title": "The Rook Must Have an Open File — by Force if Necessary",
        "principle": (
            "Tarrasch insisted: rooks on closed files are sleeping pieces. "
            "If no open file exists, create one — through pawn exchanges, sacrifices, "
            "or pawn breaks — and place the rook there immediately. "
            "A rook that reaches the 7th rank on an open file often compensates for "
            "a full pawn deficit. Never allow the game to continue with both rooks "
            "locked behind your own pawns."
        ),
    },
    {
        "id": "tarrasch_bad_bishop_1",
        "source": "The Game of Chess — Tarrasch (1931)",
        "theme": "strategy",
        "tags": ["bad_bishop", "bishop", "pawn_structure", "imbalance"],
        "title": "The Bad Bishop: Pawn Colour Determines Bishop Value",
        "principle": (
            "A bishop is 'bad' when most of its own pawns are fixed on the same colour "
            "as it travels — blocking its own diagonals and reducing it to a large pawn. "
            "When you have a bad bishop: consider trading it for the opponent's good piece, "
            "place it outside the pawn chain, or reorganise the pawns. "
            "When the opponent has a bad bishop: keep the position closed on that colour "
            "and exploit the resulting piece imbalance."
        ),
    },
    {
        "id": "tarrasch_endgame_before_middlegame_1",
        "source": "The Game of Chess — Tarrasch (1931)",
        "theme": "strategy",
        "tags": ["planning", "strategy", "transition", "endgame"],
        "title": "\"Before the Endgame, the Gods Have Placed the Middlegame\"",
        "principle": (
            "Tarrasch's maxim reminds us that transitions matter: the middlegame plan "
            "must anticipate the endgame that will result. A plan that wins material "
            "but leaves a lost pawn endgame is flawed. Before simplifying, calculate "
            "whether the resulting endgame is won, drawn, or lost. "
            "The player who can see further into the chain of transitions will navigate "
            "the middlegame-to-endgame boundary with confidence."
        ),
    },
    {
        "id": "tarrasch_bishops_better_1",
        "source": "The Game of Chess — Tarrasch (1931)",
        "theme": "strategy",
        "tags": ["bishop_vs_knight", "bishop", "open_position", "imbalance"],
        "title": "Bishops Are Generally Superior to Knights in Open Positions",
        "principle": (
            "Tarrasch held bishops superior to knights in most practical positions "
            "because they are long-range pieces that act simultaneously on both wings. "
            "In open positions — particularly those with pawns on both flanks — the "
            "bishop's long diagonal reach is decisive. The knight's superiority is "
            "restricted to specific closed positions with fixed pawn chains and "
            "available outposts. Know which type of position you are heading toward "
            "before agreeing to a knight-for-bishop trade."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 4 — RÉTI / HYPERMODERN SCHOOL
# ---------------------------------------------------------------------------

_RETI = [
    {
        "id": "reti_hypermodern_center_1",
        "source": "Modern Ideas in Chess — Réti (1923)",
        "theme": "opening",
        "tags": ["hypermodern", "fianchetto", "center_control", "opening", "flank"],
        "title": "Control the Centre from a Distance",
        "principle": (
            "Réti and the hypermodernists demonstrated that pawns need not occupy the "
            "centre to control it. A fianchettoed bishop on g2 exerts pressure along "
            "the a8-h1 diagonal, influencing d5 and e4 from afar. "
            "By delaying central pawn advances, White invites the opponent to overextend "
            "with pawns, then attacks that centre with pieces. "
            "This remains the conceptual foundation of the English Opening, Réti, "
            "King's Indian Attack, and all fianchetto systems."
        ),
    },
    {
        "id": "reti_flexible_pawns_1",
        "source": "Masters of the Chessboard — Réti (1932)",
        "theme": "opening",
        "tags": ["pawn_structure", "flexibility", "hypermodern", "strategy"],
        "title": "Maintain Pawn Flexibility in the Opening",
        "principle": (
            "Premature pawn commitments define the future of the game before the "
            "situation is clear. Réti advocated keeping pawn structure flexible so "
            "that any pawn break — c4, d4, e4 — remains available depending on how "
            "the opponent develops. Locking the pawn structure too early hands the "
            "opponent a fixed target to work against and surrenders strategic choice."
        ),
    },
    {
        "id": "reti_overextension_1",
        "source": "Masters of the Chessboard — Réti (1932)",
        "theme": "strategy",
        "tags": ["overextension", "pawn_center", "attack", "hypermodern"],
        "title": "Overextended Pawn Centres Become Targets",
        "principle": (
            "A player who advances pawns too aggressively in the centre creates "
            "a target for piece attacks. Réti demonstrated that allowing the opponent "
            "to build a large centre (e4-d4 or e5-d5) and then undermining it with "
            "...c5 or ...e5 breaks is often superior to contesting the centre from "
            "move one. A centre that cannot be maintained is worse than no centre; "
            "its collapse creates open lines for the opponent."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 5 — LASKER: Fighting Chess and Practical Psychology
# ---------------------------------------------------------------------------

_LASKER = [
    {
        "id": "lasker_fight_on_1",
        "source": "Manual of Chess — Lasker (1927)",
        "theme": "strategy",
        "tags": ["practical", "resistance", "fighting_chess", "defence"],
        "title": "Create Practical Problems — Never Resign Prematurely",
        "principle": (
            "Lasker won many games from objectively inferior positions by creating "
            "practical difficulties — traps, complications, time-pressure threats — "
            "that a human opponent could fail to navigate. His lesson: as long as "
            "you have pieces on the board, generate threats. An opponent who must "
            "find difficult moves under practical conditions will often err. "
            "The 'dead lost' position is not always dead."
        ),
    },
    {
        "id": "lasker_initiative_1",
        "source": "Common Sense in Chess — Lasker (1896)",
        "theme": "strategy",
        "tags": ["initiative", "attack", "practical", "strategy"],
        "title": "The Initiative Is Worth a Pawn",
        "principle": (
            "Lasker quantified what Morphy practised: the initiative — the right to "
            "make threats while the opponent must react — is measurable compensation "
            "for material. A player with the initiative controls the game's direction; "
            "the defender must solve problems. In fast time controls this is amplified. "
            "Sacrifice a pawn to maintain the initiative if the resulting activity is "
            "genuinely lasting."
        ),
    },
    {
        "id": "lasker_psychology_1",
        "source": "Manual of Chess — Lasker (1927)",
        "theme": "strategy",
        "tags": ["practical", "psychology", "fighting_chess", "complications"],
        "title": "Play Moves That Make Your Opponent Uncomfortable",
        "principle": (
            "Lasker famously chose not the objectively best moves but the moves most "
            "likely to cause his specific opponent to err. Against drawish, technical "
            "players he would complicate; against tacticians he would simplify into "
            "subtle endgames. While pure engine analysis ignores this, human opponents "
            "have weaknesses. Identify whether your opponent is comfortable with tactics "
            "or strategy, and steer the game toward their discomfort."
        ),
    },
    {
        "id": "lasker_exchange_value_1",
        "source": "Manual of Chess — Lasker (1927)",
        "theme": "strategy",
        "tags": ["material", "imbalance", "exchange", "practical"],
        "title": "The Value of Pieces Is Not Fixed — It Depends on the Position",
        "principle": (
            "Lasker refined piece values beyond the classical table. A rook and pawn "
            "versus two knights is not simply a matter of 6 vs 6 points; the "
            "pawn structure, open files, and coordination determine which side is "
            "actually better. A bishop can be stronger than a rook if the rook has "
            "no open file. Always evaluate material imbalances in context, "
            "not by abstract table values."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 6 — NIMZOWITSCH (expanded)
# ---------------------------------------------------------------------------

_NIMZO = [
    {
        "id": "nim_prophylaxis_1",
        "source": "My System — Nimzowitsch (1925)",
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
        "source": "My System — Nimzowitsch (1925)",
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
        "source": "My System — Nimzowitsch (1925)",
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
        "source": "My System — Nimzowitsch (1925)",
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
        "source": "My System — Nimzowitsch (1925)",
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
        "source": "My System — Nimzowitsch (1925)",
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
        "source": "My System — Nimzowitsch (1925)",
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
    {
        "id": "nim_pawn_chain_1",
        "source": "Chess Praxis — Nimzowitsch (1929)",
        "theme": "pawn_structure",
        "tags": ["pawn_chain", "pawn_structure", "space", "french_defense"],
        "title": "Pawn Chain Theory: Attack the Base",
        "principle": (
            "Nimzowitsch systematised pawn chains in \"Chess Praxis\": a pawn chain such as "
            "White e5-d4 versus Black d6-e6 is most effectively undermined at its base (d4 "
            "for White, d6 for Black). Attacking the head with ...f6 or f4 is usually less "
            "effective. This principle is the strategic key to the French Defence (Advance "
            "Variation) and similar locked pawn structures."
        ),
    },
    {
        "id": "nim_mysterious_rook_1",
        "source": "Chess Praxis — Nimzowitsch (1929)",
        "theme": "strategy",
        "tags": ["rook", "prophylaxis", "strategy", "mysterious_move"],
        "title": "The Mysterious Rook Move",
        "principle": (
            "Nimzowitsch coined the 'mysterious rook move': a rook manoeuvre to a square "
            "where it appears to do nothing, but which prophylactically prepares for every "
            "possible opponent plan. The idea is that by placing the rook on the correct "
            "file in advance, the player eliminates entire categories of counterplay. "
            "Such moves are only mysterious to those who have not read the position carefully."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 7 — CAPABLANCA (expanded)
# ---------------------------------------------------------------------------

_CAPA = [
    {
        "id": "capa_rook_7th_1",
        "source": "Chess Fundamentals — Capablanca (1921)",
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
        "source": "Chess Fundamentals — Capablanca (1921)",
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
        "source": "Chess Fundamentals — Capablanca (1921)",
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
        "source": "Chess Fundamentals — Capablanca (1921)",
        "theme": "endgame",
        "tags": ["opposition", "king_endgame", "endgame"],
        "title": "The Opposition in King and Pawn Endgames",
        "principle": (
            "Opposition occurs when two kings stand on the same file, rank, or diagonal with "
            "an odd number of squares between them and the side to move must yield. "
            "The player who does NOT have the move holds the opposition and forces the other "
            "king to give way. Mastering opposition is essential: the attacking king uses it "
            "to outflank the defender and escort the pawn to promotion."
        ),
    },
    {
        "id": "capa_piece_coordination_1",
        "source": "Chess Fundamentals — Capablanca (1921)",
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
    {
        "id": "capa_technique_1",
        "source": "My Chess Career — Capablanca (1920)",
        "theme": "endgame",
        "tags": ["technique", "endgame", "conversion", "material_advantage"],
        "title": "Convert Advantages Through Flawless Technique",
        "principle": (
            "Capablanca's endgame play was built on a simple principle: once an advantage "
            "is secured, convert it with maximum precision — no risks, no unnecessary "
            "complications. This means creating a second weakness if the opponent can "
            "defend the first, advancing the king without delay, and calculating until "
            "the position is won by force. Brilliance is for those who need it; "
            "technique is for those who are ahead."
        ),
    },
    {
        "id": "capa_two_weaknesses_1",
        "source": "My Chess Career — Capablanca (1920)",
        "theme": "strategy",
        "tags": ["two_weaknesses", "strategy", "technique", "endgame"],
        "title": "The Principle of Two Weaknesses",
        "principle": (
            "A single weakness can often be defended successfully. Two weaknesses — on "
            "opposite wings or different parts of the board — are usually decisive "
            "because the defending pieces cannot cover both simultaneously. "
            "When the opponent successfully defends one weakness, create a second; "
            "the constant switching of threats will eventually overwhelm the defence."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 8 — ALEKHINE: Dynamic and Combinative Chess
# ---------------------------------------------------------------------------

_ALEKHINE = [
    {
        "id": "alekhine_dynamism_1",
        "source": "My Best Games 1908-1923 — Alekhine (1927)",
        "theme": "strategy",
        "tags": ["dynamic_play", "initiative", "sacrifice", "piece_activity"],
        "title": "Dynamic Piece Activity Can Outweigh Static Advantages",
        "principle": (
            "Alekhine's games demonstrate that vigorous piece activity — even at the cost "
            "of structural damage or temporary material sacrifice — can generate an initiative "
            "that outlasts the opponent's defensive resources. A passed pawn or the bishop pair "
            "counts for nothing if the pieces generating the pressure never stop. "
            "Dynamism is not recklessness; it is the calculated judgement that activity "
            "will generate more practical problems than the opponent can solve."
        ),
    },
    {
        "id": "alekhine_long_sacrifice_1",
        "source": "My Best Games 1924-1937 — Alekhine (1939)",
        "theme": "tactics",
        "tags": ["sacrifice", "long_term_sacrifice", "attack", "calculation"],
        "title": "The Long-Term Sacrifice for Positional Compensation",
        "principle": (
            "Alekhine pioneered long-term sacrifices — material given up not for an "
            "immediate forcing combination but for a sustained positional compensation "
            "that only becomes decisive many moves later. In his famous 1938 game vs. "
            "Reshevsky, he sacrificed a pawn in the opening for lasting piece activity "
            "that eventually overwhelmed the defence. The principle: if activity, "
            "initiative, and piece coordination compensate beyond what can be counted, "
            "sacrifice with confidence."
        ),
    },
    {
        "id": "alekhine_multiple_weaknesses_1",
        "source": "My Best Games 1924-1937 — Alekhine (1939)",
        "theme": "strategy",
        "tags": ["multiple_weaknesses", "strategy", "attack", "two_weaknesses"],
        "title": "Create Weaknesses on Both Wings Simultaneously",
        "principle": (
            "Alekhine's strategic method: attack on one wing to force concessions, "
            "then switch to the other. By creating weaknesses on both sides of the board, "
            "he put his opponents under constant pressure from which they could not recover. "
            "The opponent can defend one flank or the other, but not both at once. "
            "This technique became the model for all subsequent strategic masters."
        ),
    },
    {
        "id": "alekhine_knight_bishop_1",
        "source": "My Best Games 1908-1923 — Alekhine (1927)",
        "theme": "piece_activity",
        "tags": ["knight", "bishop", "piece_activity", "outpost", "trapped_bishop"],
        "title": "A Well-Centralised Knight Often Beats a Passive Bishop",
        "principle": (
            "Alekhine demonstrated repeatedly that a knight on a central outpost — "
            "particularly d5 or e5 in the Sicilian and similar structures — can be "
            "more powerful than a bishop if the bishop is restricted by its own pawns. "
            "The knight's ability to hop over obstructions and attack any colour square "
            "makes it lethal when entrenched. The key: ensure the knight cannot be "
            "dislodged by opposing pawns."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 9 — EUWE: Planning and Middlegame Technique
# ---------------------------------------------------------------------------

_EUWE = [
    {
        "id": "euwe_planning_1",
        "source": "The Middlegame Vol. I — Euwe & Kramer (1964)",
        "theme": "middlegame",
        "tags": ["planning", "strategy", "middlegame", "evaluation"],
        "title": "Every Plan Must Be Based on Concrete Evaluation",
        "principle": (
            "Euwe insisted that a 'plan' without concrete justification is wishful thinking. "
            "Before committing to a plan — whether a kingside attack, a queenside expansion, "
            "or an endgame transition — evaluate the position: who is better, and why? "
            "The plan must follow logically from the position's imbalances. "
            "Vague plans ('I'll attack') are not plans; precise ones ('I'll advance h4-h5 "
            "after ...Qe7 and Rh3') are actionable."
        ),
    },
    {
        "id": "euwe_piece_exchange_1",
        "source": "The Middlegame Vol. II — Euwe & Kramer (1964)",
        "theme": "strategy",
        "tags": ["piece_exchange", "strategy", "imbalance", "simplification"],
        "title": "Exchange Pieces That Help Your Opponent's Plan",
        "principle": (
            "When the opponent has a strong piece that is central to their plan, "
            "trade it off even at a cost. A knight on d5 that anchors the opponent's "
            "entire position is worth exchanging for your bishop, even if you get "
            "the worse bishop-vs-knight imbalance, because removing the key piece "
            "dismantles the plan it was supporting."
        ),
    },
    {
        "id": "euwe_minority_attack_1",
        "source": "The Middlegame Vol. I — Euwe & Kramer (1964)",
        "theme": "strategy",
        "tags": ["minority_attack", "pawn_structure", "queenside", "weakness"],
        "title": "The Minority Attack Creates Permanent Weaknesses",
        "principle": (
            "The minority attack — advancing two queenside pawns (b4-b5) against "
            "the opponent's three — is a classical strategic technique in the QGD Exchange "
            "Variation and similar structures. The goal is not to win material but to "
            "leave the opponent with a permanent isolated or backward pawn (c6 after "
            "bxc6). Once the weakness is fixed, attack it with all available pieces."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 10 — BRONSTEIN / SOVIET SCHOOL: Dynamic Compensation
# ---------------------------------------------------------------------------

_BRONSTEIN = [
    {
        "id": "bronstein_compensation_1",
        "source": "Zurich International Chess Tournament 1953 — Bronstein",
        "theme": "strategy",
        "tags": ["dynamic_compensation", "sacrifice", "initiative", "piece_activity"],
        "title": "Piece Activity as Compensation for Material",
        "principle": (
            "Bronstein's annotations in the 1953 Zurich book articulate the Soviet "
            "school's key discovery: in dynamic positions, activity and initiative "
            "are quantifiable compensation for material deficit. A rook is worth five "
            "points only if it has something to do. A knight on d5 with a fixed pawn "
            "in front of it and no prospect of being dislodged may be worth a rook "
            "in practical terms. Always evaluate compensation concretely."
        ),
    },
    {
        "id": "bronstein_initiative_chain_1",
        "source": "Zurich International Chess Tournament 1953 — Bronstein",
        "theme": "tactics",
        "tags": ["initiative", "chain_of_threats", "calculation", "attack"],
        "title": "Keep the Initiative Alive With a Chain of Threats",
        "principle": (
            "An initiative is only lasting if each move renews the threat. "
            "A series of moves that maintain concrete threats — even if none is immediately "
            "decisive — forces the opponent to continue reacting. The moment you play a move "
            "with no threat, the opponent regains freedom. Construct chains of threats: "
            "each move should threaten something the opponent cannot ignore."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 11 — FISCHER: Technical Precision and Exploitation
# ---------------------------------------------------------------------------

_FISCHER = [
    {
        "id": "fischer_endgame_technique_1",
        "source": "My 60 Memorable Games — Fischer (1969)",
        "theme": "endgame",
        "tags": ["endgame", "technique", "conversion", "precision"],
        "title": "Endgame Precision: Leave Nothing to Chance",
        "principle": (
            "Fischer's endgame technique was built on the principle that winning endgames "
            "require not brilliant moves but accurate, relentless pressure with zero "
            "unnecessary risk. He would find the one move that maintained the win in all "
            "variations, even if a flashier move seemed to work. His Rook + Bishop vs "
            "Rook endgame wins (vs. Taimanov, 1971) demonstrate this: engine-level accuracy "
            "across 50+ moves, never deviating from the winning path."
        ),
    },
    {
        "id": "fischer_weak_d5_1",
        "source": "My 60 Memorable Games — Fischer (1969)",
        "theme": "strategy",
        "tags": ["outpost", "d5_square", "sicilian", "knight", "weak_square"],
        "title": "The Knight Outpost on d5 in the Sicilian",
        "principle": (
            "Fischer identified the d5 square — when Black's c-pawn has been exchanged "
            "in the Sicilian — as a permanent outpost for White's knight. A knight on d5 "
            "in the Sicilian cannot be dislodged by pawns and dominates the entire board. "
            "To reach it, manoeuvre Nd2-f1-e3-d5 or Nc3-d5. "
            "Black's defensive task is to trade it off before it becomes entrenched."
        ),
    },
    {
        "id": "fischer_prophylaxis_1",
        "source": "My 60 Memorable Games — Fischer (1969)",
        "theme": "strategy",
        "tags": ["prophylaxis", "prevention", "strategy", "middlegame"],
        "title": "Prophylaxis Before Attack",
        "principle": (
            "Fischer, following Nimzowitsch, consistently prevented the opponent's "
            "counterplay before launching his own attack. In the Sicilian, he would "
            "complete queenside development and secure e4 before advancing g4-g5. "
            "His games vs. Spassky (1972 match) show systematic prophylaxis: he would "
            "quietly improve piece positions and eliminate all opponent counterplay before "
            "the decisive blow. Never attack while leaving loose ends behind."
        ),
    },
    {
        "id": "fischer_bishop_pair_1",
        "source": "My 60 Memorable Games — Fischer (1969)",
        "theme": "strategy",
        "tags": ["bishop_pair", "two_bishops", "open_position", "imbalance"],
        "title": "Fight for the Bishop Pair in Open Positions",
        "principle": (
            "Fischer consistently manoeuvred to obtain the two bishops in open or "
            "semi-open positions, then used his superior piece activity to grind down "
            "the opponent. His game vs. Petrosian (1971) is the model: he obtained the "
            "bishop pair, opened the position with precise pawn play, and converted "
            "the long-range advantage into a win. When you have two bishops, open the "
            "game; when the opponent has them, keep it closed."
        ),
    },
    {
        "id": "fischer_opening_prep_1",
        "source": "My 60 Memorable Games — Fischer (1969)",
        "theme": "opening",
        "tags": ["opening_preparation", "opening", "theory", "practical"],
        "title": "Deep Opening Preparation Wins Games Before Move 20",
        "principle": (
            "Fischer's preparation went deeper than anyone before him. He understood "
            "that memorised, deeply understood opening lines give a concrete advantage "
            "in practical play — the opponent is navigating known territory you have "
            "already mapped. Study your openings to the point where every branch "
            "is understood strategically, not just memorised. When your opponent deviates "
            "from theory, you will have the understanding to punish it."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 12 — SILMAN (expanded)
# ---------------------------------------------------------------------------

_SILMAN = [
    {
        "id": "silman_imbalance_1",
        "source": "How to Reassess Your Chess — Silman (1993)",
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
        "source": "How to Reassess Your Chess — Silman (1993)",
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
        "source": "How to Reassess Your Chess — Silman (1993)",
        "theme": "pawn_structure",
        "tags": ["weak_square", "hole", "outpost", "pawn_structure"],
        "title": "Exploit Weak Squares (Holes)",
        "principle": (
            "A weak square is one that can no longer be defended by a pawn. "
            "Once a square becomes permanently weak — a 'hole' — place a piece on it, "
            "especially a knight which cannot be chased away by pawns. "
            "Creating weak squares in the opponent's position is a long-term strategic "
            "investment that pays off in the endgame."
        ),
    },
    {
        "id": "silman_two_bishops_1",
        "source": "How to Reassess Your Chess — Silman (1993)",
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
        "source": "How to Reassess Your Chess — Silman (1993)",
        "theme": "strategy",
        "tags": ["space", "imbalance", "pawn_center"],
        "title": "Space as an Imbalance",
        "principle": (
            "The player with more space has more room to manoeuvre and can regroup pieces "
            "more easily. A space advantage is most useful when the position is not yet "
            "fully blocked. When cramped, seek exchanges to relieve the bind, or counterattack "
            "the opponent's advanced pawns."
        ),
    },
    {
        "id": "silman_pawn_structure_1",
        "source": "How to Reassess Your Chess — Silman (1993)",
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
    {
        "id": "silman_imbalance_list_1",
        "source": "How to Reassess Your Chess — Silman (1993)",
        "theme": "strategy",
        "tags": ["imbalance", "planning", "evaluation", "strategy"],
        "title": "Silman's Seven Imbalances: The Evaluation Checklist",
        "principle": (
            "Silman lists seven imbalances to evaluate in any position: (1) Superior minor "
            "piece (bishop vs knight or vice versa). (2) Pawn structure (weaknesses, "
            "passed pawns, majorities). (3) Space. (4) Material. (5) Control of key files "
            "and ranks. (6) Control of key squares (outposts). (7) Lead in development, "
            "or king safety. Go through this list for every important position — your plan "
            "should follow from the dominant imbalances."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 13 — KOTOV (expanded)
# ---------------------------------------------------------------------------

_KOTOV = [
    {
        "id": "kotov_candidates_1",
        "source": "Think Like a Grandmaster — Kotov (1971)",
        "theme": "tactics",
        "tags": ["candidate_moves", "calculation", "thought_process"],
        "title": "Establish Candidate Moves Before Calculating",
        "principle": (
            "Before calculating any variation, first list all candidate moves. "
            "Do not start calculating the first move that comes to mind; survey the board "
            "systematically and pick the two or three most promising candidates. "
            "Only after establishing your candidates should you calculate deeply."
        ),
    },
    {
        "id": "kotov_tree_1",
        "source": "Think Like a Grandmaster — Kotov (1971)",
        "theme": "tactics",
        "tags": ["calculation", "tree_of_variations", "discipline"],
        "title": "Calculate Each Line Once — the Tree of Variations",
        "principle": (
            "Analyse each branch completely before moving to the next — do not hop "
            "back and forth. If you re-analyse the same line multiple times you waste "
            "time and introduce errors. One branch at a time, to its conclusion — "
            "this is the hallmark of accurate tactical play."
        ),
    },
    {
        "id": "kotov_blunder_1",
        "source": "Think Like a Grandmaster — Kotov (1971)",
        "theme": "tactics",
        "tags": ["blunder_check", "safety", "last_check"],
        "title": "Always Perform a Final Blunder Check",
        "principle": (
            "Before making any move, pause and ask: does this move leave anything en prise? "
            "Does it allow a fork, pin, skewer, or back-rank mate? "
            "Many games are lost not by inferior strategy but by a simple oversight "
            "in the final moment before committing to a move."
        ),
    },
    {
        "id": "kotov_time_1",
        "source": "Think Like a Grandmaster — Kotov (1971)",
        "theme": "tactics",
        "tags": ["time_management", "calculation", "practical"],
        "title": "Budget Your Time According to Complexity",
        "principle": (
            "Spend your clock time proportionally to the complexity of each decision. "
            "Routine moves in quiet positions should be made quickly; sharp tactical "
            "junctures deserve deep thought. Running into severe time pressure is often "
            "the result of spending too long on non-critical moves early in the game."
        ),
    },
    {
        "id": "kotov_critical_1",
        "source": "Think Like a Grandmaster — Kotov (1971)",
        "theme": "middlegame",
        "tags": ["critical_moment", "plan", "evaluation"],
        "title": "Recognise the Critical Moment",
        "principle": (
            "Every game has a handful of critical moments where the correct decision "
            "dramatically changes the outcome. Learn to sense when the position is at "
            "a crossroads — forcing continuations, material imbalances about to be resolved, "
            "or king safety suddenly at issue. At these moments, invest the most time "
            "and care in your calculation."
        ),
    },
    {
        "id": "kotov_grandmaster_think_1",
        "source": "Play Like a Grandmaster — Kotov (1978)",
        "theme": "strategy",
        "tags": ["planning", "strategy", "positional_play", "thought_process"],
        "title": "Assess Systematically: Pawn Structure First, Then Pieces",
        "principle": (
            "Kotov's systematic method for positional assessment: first analyse the pawn "
            "structure (weaknesses, majorities, passed pawns), then identify the resulting "
            "piece roles (which pieces are good, which are bad, which squares are available). "
            "The pawn structure determines piece roles — not the reverse. "
            "Once this assessment is complete, the plan becomes visible."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 14 — KERES & KOTOV: The Art of the Middlegame
# ---------------------------------------------------------------------------

_KERES = [
    {
        "id": "keres_attack_prerequisites_1",
        "source": "The Art of the Middlegame — Keres & Kotov (1964)",
        "theme": "king_safety",
        "tags": ["attack", "prerequisites", "king_safety", "piece_coordination"],
        "title": "Verify Prerequisites Before Attacking",
        "principle": (
            "Keres lists the prerequisites for a successful kingside attack: "
            "(1) Superior piece activity in the attacking sector. "
            "(2) Open or semi-open files toward the enemy king. "
            "(3) Your own king is safe or the position is closed elsewhere. "
            "(4) Material equality or slight inferiority is acceptable if activity compensates. "
            "Attacking without these conditions is a gamble; with them, it is science."
        ),
    },
    {
        "id": "keres_defence_counterattack_1",
        "source": "The Art of the Middlegame — Keres & Kotov (1964)",
        "theme": "strategy",
        "tags": ["defence", "counterattack", "strategy", "practical"],
        "title": "The Best Defence Is a Counterattack",
        "principle": (
            "Passive defence — shuffling pieces between defence of one square and another — "
            "eventually fails because the attacker can always improve while the defender "
            "can only maintain. The best defence creates a counter-threat that forces "
            "the opponent to stop and react. Even in defensive positions, look for "
            "ways to generate active counterplay that changes the game's balance."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 15 — DVORETSKY: Endgame Manual Principles
# ---------------------------------------------------------------------------

_DVORETSKY = [
    {
        "id": "dvoretsky_rook_active_1",
        "source": "Endgame Manual — Dvoretsky (2003)",
        "theme": "endgame",
        "tags": ["rook_endgame", "rook_activity", "endgame", "technique"],
        "title": "In Rook Endgames, Activity Comes First",
        "principle": (
            "Dvoretsky's fundamental endgame rule: activate the rook before everything else. "
            "A passive rook defending pawns will lose to an active rook creating threats. "
            "Even give up a pawn temporarily if it means activating the rook. "
            "Rook endgames are won by piece activity, not by material count alone."
        ),
    },
    {
        "id": "dvoretsky_fortress_endgame_1",
        "source": "Endgame Manual — Dvoretsky (2003)",
        "theme": "endgame",
        "tags": ["fortress", "endgame", "drawing_technique", "defence"],
        "title": "The Endgame Fortress: When to Build and When to Avoid",
        "principle": (
            "A fortress is a defensive configuration where the materially inferior side "
            "achieves a theoretical draw by creating an impenetrable defensive structure. "
            "Classic fortresses: rook+wrong-colour bishop vs rook (drawn because king "
            "shelters in the corner), or bishop vs pawns on the wrong colour. "
            "When behind, always check if a fortress is available before resigning."
        ),
    },
    {
        "id": "dvoretsky_zugzwang_1",
        "source": "Endgame Manual — Dvoretsky (2003)",
        "theme": "endgame",
        "tags": ["zugzwang", "endgame", "king_endgame", "pawn_endgame"],
        "title": "Zugzwang: The Obligation to Move Can Be Fatal",
        "principle": (
            "Zugzwang occurs when any move worsens the position — having to move is a "
            "disadvantage. It is most common in king-and-pawn endgames where the defending "
            "king cannot maintain its post once forced to step aside. "
            "To use zugzwang: manoeuvre the king to a position where it holds, then "
            "use a triangulation (three-move king tour) to transfer the move to the opponent. "
            "Triangulation is a fundamental endgame technique."
        ),
    },
    {
        "id": "dvoretsky_corresponding_squares_1",
        "source": "School of Chess Excellence — Dvoretsky (2001)",
        "theme": "endgame",
        "tags": ["corresponding_squares", "king_endgame", "endgame", "opposition"],
        "title": "Corresponding Squares: Advanced Opposition Theory",
        "principle": (
            "Beyond simple direct opposition, certain endgames require understanding "
            "'corresponding squares' — pairs of squares such that if one king occupies "
            "a square in its set, the other king must be on the corresponding square. "
            "When the defending king is forced off its corresponding square, the attacker "
            "breaks through. This concept generalises opposition and is essential for "
            "complex king-and-pawn endgames."
        ),
    },
    {
        "id": "dvoretsky_minor_piece_end_1",
        "source": "Endgame Manual — Dvoretsky (2003)",
        "theme": "endgame",
        "tags": ["minor_piece_endgame", "bishop_endgame", "knight_endgame", "endgame"],
        "title": "Same-Colour Bishops: Reduce to a Known Draw or Win",
        "principle": (
            "In same-colour bishop endgames, the outcome depends almost entirely on "
            "pawn structure. If the defender can block all pawns on the same colour "
            "as the bishop, a draw is achievable regardless of material. "
            "The attacker must create a passed pawn on the opposite colour, which the "
            "defending bishop cannot stop. Always evaluate the colour of critical pawns "
            "before entering same-colour bishop endgames."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 16 — DE LA VILLA (as before, core endgame patterns)
# ---------------------------------------------------------------------------

_VILLA = [
    {
        "id": "villa_lucena_1",
        "source": "100 Endgames You Must Know — De la Villa (2008)",
        "theme": "endgame",
        "tags": ["rook_endgame", "lucena", "winning_technique", "endgame"],
        "title": "The Lucena Position: Building a Bridge",
        "principle": (
            "The Lucena position arises in rook endgames when the attacking side has "
            "advanced the pawn to the 7th rank with the king in front of the pawn. "
            "The winning technique is 'building a bridge': use the rook to cut off the "
            "defending king while the attacking king steps out from in front of the pawn. "
            "Once the bridge is built, the pawn promotes. One of the most important "
            "endgame patterns every player must know."
        ),
    },
    {
        "id": "villa_philidor_1",
        "source": "100 Endgames You Must Know — De la Villa (2008)",
        "theme": "endgame",
        "tags": ["rook_endgame", "philidor", "drawing_technique", "endgame"],
        "title": "The Philidor Position: Defensive Rook Technique",
        "principle": (
            "Place the defending rook on the third rank to cut off the attacking king. "
            "Once the attacking king advances past the pawn, switch the rook to give "
            "checks from behind. Knowledge of both Lucena (win) and Philidor (draw) "
            "is essential — they are the two pillars of rook-and-pawn endgame theory."
        ),
    },
    {
        "id": "villa_king_pawn_1",
        "source": "100 Endgames You Must Know — De la Villa (2008)",
        "theme": "endgame",
        "tags": ["king_pawn_endgame", "opposition", "endgame", "key_squares"],
        "title": "Key Squares in King and Pawn Endgames",
        "principle": (
            "Every pawn has key squares: squares the attacking king must reach to guarantee "
            "promotion. For e, d, c, f-file pawns the key squares are two ranks ahead "
            "on the same and adjacent files. If the attacking king occupies a key square, "
            "the pawn promotes regardless of the defending king's position."
        ),
    },
    {
        "id": "villa_rook_behind_1",
        "source": "100 Endgames You Must Know — De la Villa (2008)",
        "theme": "endgame",
        "tags": ["rook_endgame", "rook_behind_passed_pawn", "endgame"],
        "title": "Place the Rook Behind the Passed Pawn",
        "principle": (
            "Whether attacking or defending in a rook endgame with a passed pawn, "
            "place the rook behind it. The attacker's rook gains strength as the pawn "
            "advances; the defender's rook behind the passed pawn controls its march "
            "most effectively. This principle applies in the vast majority of practical "
            "rook endgames."
        ),
    },
    {
        "id": "villa_activity_1",
        "source": "100 Endgames You Must Know — De la Villa (2008)",
        "theme": "endgame",
        "tags": ["rook_activity", "endgame", "piece_activity"],
        "title": "Rook Activity Trumps Pawns in the Endgame",
        "principle": (
            "In rook endgames, an active rook is often worth more than an extra pawn. "
            "A passive rook defending its own pawns usually loses to an active rook "
            "creating threats. When behind in material, activate aggressively — "
            "attack enemy pawns and keep your rook mobile."
        ),
    },
    {
        "id": "villa_opposite_bishops_1",
        "source": "100 Endgames You Must Know — De la Villa (2008)",
        "theme": "endgame",
        "tags": ["opposite_color_bishops", "draw", "endgame"],
        "title": "Opposite-Colour Bishops Favour the Defender",
        "principle": (
            "When each side has a bishop on a different colour, draws are frequent even "
            "with a one- or two-pawn deficit. The defender places pawns on the opponent's "
            "bishop colour, making them immune to attack. In attack, however, opposite-colour "
            "bishops can be devastating — the attacker's threats on one colour cannot be "
            "met by the defending bishop."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 17 — VUKOVIC (expanded)
# ---------------------------------------------------------------------------

_VUKOVIC = [
    {
        "id": "vukovic_castled_king_1",
        "source": "The Art of Attack in Chess — Vukovic (1965)",
        "theme": "king_safety",
        "tags": ["attack", "castled_king", "king_safety", "sacrifice"],
        "title": "Conditions for Attack on the Castled King",
        "principle": (
            "Before launching an attack on the castled king, verify: a lead in piece "
            "activity near the king, open or semi-open files toward it, and your own "
            "king is safe. Attacking without these conditions leads to a failed attack "
            "and counterplay. Prepare methodically before committing."
        ),
    },
    {
        "id": "vukovic_sacrifice_1",
        "source": "The Art of Attack in Chess — Vukovic (1965)",
        "theme": "tactics",
        "tags": ["sacrifice", "king_safety", "attack", "h_file"],
        "title": "The Classic Bishop Sacrifice on h7",
        "principle": (
            "The bishop sacrifice Bxh7+ (Bxh2+) strips the king of pawn cover. "
            "For it to succeed: a queen within striking distance, a knight that can "
            "reach g5 (or g4), and open lines toward the exposed king. "
            "Recognise this pattern quickly — it appears in many practical games."
        ),
    },
    {
        "id": "vukovic_uncastled_king_1",
        "source": "The Art of Attack in Chess — Vukovic (1965)",
        "theme": "king_safety",
        "tags": ["uncastled_king", "attack", "center", "king_safety"],
        "title": "Attack the Uncastled King via the Centre",
        "principle": (
            "When the opponent has failed to castle, open the centre immediately "
            "with pawn breaks (d4-d5, e4-e5) to expose the king. An uncastled king "
            "in an open centre is extremely vulnerable. Sacrifice material if necessary "
            "to open lines; the king's insecurity compensates for any material investment."
        ),
    },
    {
        "id": "vukovic_h_file_1",
        "source": "The Art of Attack in Chess — Vukovic (1965)",
        "theme": "king_safety",
        "tags": ["h_file", "open_file", "king_attack", "rook"],
        "title": "Open the h-file Against the Castled King",
        "principle": (
            "Advance h4-h5 to force open the h-file, then bring the rook to h1. "
            "Combined with queen and minor pieces, a rook on the h-file creates "
            "mating threats that are very difficult to defend. Especially powerful "
            "when the opponent's king has little piece protection."
        ),
    },
    {
        "id": "vukovic_mating_net_1",
        "source": "The Art of Attack in Chess — Vukovic (1965)",
        "theme": "tactics",
        "tags": ["mating_net", "coordination", "attack"],
        "title": "Build a Mating Net Systematically",
        "principle": (
            "A mating net is constructed by progressively restricting the enemy king's "
            "escape squares while bringing more attacking pieces. Do not rush for a "
            "combination before the net is ready; complete the encirclement first, "
            "then deliver the decisive blow."
        ),
    },
    {
        "id": "vukovic_greek_gift_extended_1",
        "source": "The Art of Attack in Chess — Vukovic (1965)",
        "theme": "tactics",
        "tags": ["sacrifice", "greek_gift", "bishop_sacrifice", "king_safety", "attack"],
        "title": "The Greek Gift Sacrifice: Full Conditions",
        "principle": (
            "Vukovic analyses the Greek Gift (Bxh7+) exhaustively. Full conditions for "
            "success: (1) White's dark-squared bishop or knight can reach g5. (2) "
            "White queen can come to h5 without loss of tempo. (3) The e-file is "
            "open or semi-open for the rook. (4) Black has no defensive resource "
            "such as ...Rg8 or a defensive piece on f6. Missing any condition, "
            "the sacrifice is refuted — calculate before executing."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 18 — CHERNEV (expanded)
# ---------------------------------------------------------------------------

_CHERNEV = [
    {
        "id": "chernev_purpose_1",
        "source": "Logical Chess Move by Move — Chernev (1957)",
        "theme": "opening",
        "tags": ["purposeful_play", "opening", "development"],
        "title": "Every Move Must Have a Purpose",
        "principle": (
            "Do not make moves just to make moves. Every move should have a clear purpose: "
            "developing a piece, controlling a key square, improving coordination, or "
            "creating a concrete threat. Ask: 'What does this move achieve?'"
        ),
    },
    {
        "id": "chernev_no_repeat_1",
        "source": "Logical Chess Move by Move — Chernev (1957)",
        "theme": "opening",
        "tags": ["development", "opening", "tempo"],
        "title": "Don't Move the Same Piece Twice in the Opening",
        "principle": (
            "Moving the same piece twice in the opening wastes a tempo. Unless winning "
            "material or avoiding a serious threat, develop a new piece each move. "
            "Every piece should reach its best square quickly; delay is dangerous "
            "when the opponent is building an efficient army."
        ),
    },
    {
        "id": "chernev_center_1",
        "source": "Logical Chess Move by Move — Chernev (1957)",
        "theme": "opening",
        "tags": ["center_control", "opening", "pawns"],
        "title": "Fight for the Centre in the Opening",
        "principle": (
            "The player who controls the centre can direct pieces to any part of the board "
            "more efficiently. In the opening, contest e4, d4, e5, d5 with pawns and pieces. "
            "Neglecting the centre allows the opponent to build a space advantage."
        ),
    },
    {
        "id": "chernev_castle_1",
        "source": "Logical Chess Move by Move — Chernev (1957)",
        "theme": "king_safety",
        "tags": ["castling", "king_safety", "opening"],
        "title": "Castle Early to Ensure King Safety",
        "principle": (
            "Castling is the fastest way to get the king to safety and connect the rooks. "
            "As a rule, castle within the first 10 moves unless the position demands otherwise. "
            "An uncastled king in an open game is an invitation for the opponent to attack."
        ),
    },
    {
        "id": "chernev_coordination_1",
        "source": "Logical Chess Move by Move — Chernev (1957)",
        "theme": "middlegame",
        "tags": ["piece_coordination", "harmony", "rook_connection"],
        "title": "Connect Your Rooks",
        "principle": (
            "After developing all pieces and castling, clear the back rank of minor pieces "
            "to connect the rooks. Connected rooks mutually defend and control the entire "
            "rank, ready to be deployed to any open file. Disconnected rooks are far weaker."
        ),
    },
    {
        "id": "chernev_threats_1",
        "source": "Logical Chess Move by Move — Chernev (1957)",
        "theme": "tactics",
        "tags": ["threats", "tactical_awareness", "initiative"],
        "title": "Create Threats With Every Move",
        "principle": (
            "The player who makes threats forces the opponent to react, maintaining the "
            "initiative. Even positional moves should ideally carry a threat. When you "
            "stop making threats, the opponent regains freedom to pursue their own plan."
        ),
    },
]

# ---------------------------------------------------------------------------
# SECTION 19 — OPENING SYSTEMS: Principles, Relationships, Counters
# ---------------------------------------------------------------------------
#
# Each opening entry uses these additional fields:
#   eco       : ECO code range
#   counters  : list of opening IDs this opening is designed to counter/fight
#   countered_by : list of opening IDs that present challenges to this opening
#   transposes_to: list of opening IDs this can transpose into
#   color     : "white" | "black" | "both"
# ---------------------------------------------------------------------------

_OPENINGS = [

    # -----------------------------------------------------------------------
    # OPEN GAMES (1.e4 e5)
    # -----------------------------------------------------------------------
    {
        "id": "opening_ruy_lopez",
        "source": "ECO C60-C99 / Ruy Lopez (Spanish Opening)",
        "theme": "opening",
        "tags": ["ruy_lopez", "spanish", "open_game", "1e4_e5", "development",
                 "center_control", "bishop_pressure"],
        "title": "Ruy Lopez: Long-term Pressure on e5",
        "principle": (
            "1.e4 e5 2.Nf3 Nc6 3.Bb5. White pins the knight defending e5, preparing "
            "to win the centre in the long run. The bishop on b5 does not immediately "
            "win material — Black can always unpin — but it creates lasting pressure. "
            "Main ideas for White: castle kingside, c3+d4 to build a pawn centre, "
            "Nd2-f1-g3 to regroup. Main defences: Morphy Defence (...a6 4.Ba4), Berlin "
            "(...Nf6 — drawish, solid), Marshall Attack (...0-0 ...d5 gambit), "
            "Chigorin (...a6 ...Nge7 ...g6), Breyer (...Nb8-d7)."
        ),
        "eco": "C60-C99",
        "color": "white",
        "counters": [],
        "countered_by": ["opening_berlin_defense", "opening_marshall_attack"],
        "transposes_to": ["opening_italian"],
    },
    {
        "id": "opening_berlin_defense",
        "source": "ECO C65-C67 / Berlin Defence",
        "theme": "opening",
        "tags": ["berlin_defense", "ruy_lopez", "endgame", "solid", "1e4_e5",
                 "drawish", "structural_defense"],
        "title": "Berlin Defence: The Drawish Endgame Weapon",
        "principle": (
            "1.e4 e5 2.Nf3 Nc6 3.Bb5 Nf6. After 4.0-0 Nxe4 5.d4 Nd6 6.Bxc6 dxc6 "
            "7.dxe5 Nf5 8.Qxd8+ Kxd8, Black reaches an early queen endgame with "
            "doubled pawns but the two bishops and active piece play. "
            "Popularised by Kramnik vs Kasparov (2000 World Championship match) as a "
            "drawing weapon. Black's extra material compensates for the structural "
            "damage. Against players who want to avoid the Berlin, try 4.Nc3 or 4.d3."
        ),
        "eco": "C65-C67",
        "color": "black",
        "counters": ["opening_ruy_lopez"],
        "countered_by": [],
        "transposes_to": [],
    },
    {
        "id": "opening_marshall_attack",
        "source": "ECO C89 / Marshall Attack",
        "theme": "opening",
        "tags": ["marshall_attack", "ruy_lopez", "gambit", "attack", "1e4_e5",
                 "initiative", "sacrifice"],
        "title": "Marshall Attack: Gambit for Initiative Against the Ruy Lopez",
        "principle": (
            "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.0-0 Be7 6.Re1 b5 7.Bb3 0-0 "
            "8.c3 d5!? Black sacrifices a pawn for lasting initiative, open lines, "
            "and piece activity against White's king. The compensation is genuine — "
            "Black gets the e5 square, open d-file, and attacking chances. "
            "White avoids it with 8.a4 (Anti-Marshall). If White accepts, must return "
            "material to equalise or be overwhelmed."
        ),
        "eco": "C89",
        "color": "black",
        "counters": ["opening_ruy_lopez"],
        "countered_by": [],
        "transposes_to": [],
    },
    {
        "id": "opening_italian",
        "source": "ECO C50-C59 / Italian Game",
        "theme": "opening",
        "tags": ["italian", "giuoco_piano", "open_game", "1e4_e5", "development",
                 "center_control"],
        "title": "Italian Game: Classical Development and Central Control",
        "principle": (
            "1.e4 e5 2.Nf3 Nc6 3.Bc4. White develops the bishop to its most active "
            "diagonal, targeting f7 and preparing a quick d3 or d4. The Italian can "
            "lead to the sharp Giuoco Piano (3...Bc5 4.c3 Nf6 5.d4) or the quieter "
            "Giuoco Pianissimo (5.d3). The Evans Gambit (4.b4!?) sacrifices a pawn for "
            "rapid development. The Two Knights (3...Nf6) leads to sharp tactical play. "
            "Structurally similar to Ruy Lopez but bishop is less flexible."
        ),
        "eco": "C50-C59",
        "color": "white",
        "counters": [],
        "countered_by": ["opening_two_knights"],
        "transposes_to": ["opening_ruy_lopez"],
    },
    {
        "id": "opening_kings_gambit",
        "source": "ECO C30-C39 / King's Gambit",
        "theme": "opening",
        "tags": ["kings_gambit", "gambit", "open_game", "1e4_e5", "attack",
                 "initiative", "open_file", "f_file"],
        "title": "King's Gambit: The Romantic Attack",
        "principle": (
            "1.e4 e5 2.f4. White offers a pawn to open the f-file and gain a strong "
            "centre. If accepted (2...exf4), White plays 3.Nf3, 4.Bc4 and attacks "
            "rapidly. The f-file and diagonal pressure on f7 are White's assets. "
            "Declined (2...Bc5 or 2...d5), the game is more strategic. "
            "Fischer's 'refutation' (1...e5 2.f4 exf4 3.Nf3 d6) is actually only "
            "a practical difficulty, not a theoretical refutation. "
            "The KG rewards players comfortable with unbalanced, attacking positions."
        ),
        "eco": "C30-C39",
        "color": "white",
        "counters": [],
        "countered_by": ["opening_falkbeer"],
        "transposes_to": [],
    },
    {
        "id": "opening_scotch",
        "source": "ECO C44-C45 / Scotch Game",
        "theme": "opening",
        "tags": ["scotch", "open_game", "1e4_e5", "center_control", "early_d4"],
        "title": "Scotch Game: Early Centre Resolution",
        "principle": (
            "1.e4 e5 2.Nf3 Nc6 3.d4 exd4 4.Nxd4. White opens the centre immediately "
            "and avoids the theoretical complexity of the Ruy Lopez. After 4...Bc5 "
            "(Classical) or 4...Nf6 (Mieses), play becomes sharp. Kasparov revived "
            "the Scotch in the 1990s. White gets active pieces and centre control; "
            "Black fights for equality with active counterplay. "
            "The Scotch Gambit (4.Bc4 instead of Nxd4) is sharper but less theoretically "
            "sound at the highest level."
        ),
        "eco": "C44-C45",
        "color": "white",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_italian"],
    },
    {
        "id": "opening_petrov",
        "source": "ECO C42-C43 / Petrov's Defence (Russian Defence)",
        "theme": "opening",
        "tags": ["petrov", "russian_defense", "solid", "drawish", "1e4_e5", "symmetry"],
        "title": "Petrov's Defence: Symmetrical Solidity",
        "principle": (
            "1.e4 e5 2.Nf3 Nf6. Black immediately counter-attacks e4 rather than "
            "defending e5. After 3.Nxe5 d6 4.Nf3 Nxe4, play is symmetrical and "
            "drawish at the highest level. Preferred by those who want to avoid the "
            "Ruy Lopez's main lines. White can try 3.d4 (Steinitz variation) for more "
            "imbalance. The Petrov is reliable but passive — White retains slightly "
            "more central control after the early exchanges. "
            "Related to the Four Knights (after 3.Nc3 Nc6)."
        ),
        "eco": "C42-C43",
        "color": "black",
        "counters": ["opening_ruy_lopez"],
        "countered_by": [],
        "transposes_to": ["opening_four_knights"],
    },

    # -----------------------------------------------------------------------
    # SEMI-OPEN GAMES (1.e4, not 1...e5)
    # -----------------------------------------------------------------------
    {
        "id": "opening_sicilian",
        "source": "ECO B20-B99 / Sicilian Defence",
        "theme": "opening",
        "tags": ["sicilian", "semi_open", "1e4", "asymmetric", "counterplay",
                 "c_file", "queenside_majority"],
        "title": "Sicilian Defence: Asymmetry and Counterplay",
        "principle": (
            "1.e4 c5. The most popular and theoretically rich defence to 1.e4. "
            "Black creates an asymmetry immediately: the c5 pawn fights for d4 "
            "without giving White a target on e5. Black will typically castle kingside "
            "and seek counterplay on the c-file and queenside, while White attacks "
            "on the kingside (e5, f5-f6 breaks, g4-g5). "
            "The Open Sicilian (2.Nf3 + 3.d4) leads to the main theoretical battle; "
            "Anti-Sicilians (Alapin 2.c3, Grand Prix 2.Nc3 f4, Smith-Morra 2.d4 cxd4 3.c3) "
            "avoid main lines at the cost of objectivity."
        ),
        "eco": "B20-B99",
        "color": "black",
        "counters": [],
        "countered_by": ["opening_alapin", "opening_grand_prix"],
        "transposes_to": [],
    },
    {
        "id": "opening_sicilian_najdorf",
        "source": "ECO B90-B99 / Sicilian Najdorf",
        "theme": "opening",
        "tags": ["sicilian", "najdorf", "b5_break", "a6", "counterplay",
                 "1e4", "sharp", "e5_outpost"],
        "title": "Sicilian Najdorf: The Most Theoretically Complex Opening",
        "principle": (
            "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6. "
            "...a6 prevents Nb5 and prepares ...b5, ...e5, or ...e6. "
            "Fischer and Kasparov both played it as their main weapon. "
            "White's sharpest responses: English Attack (6.Be3 e5 7.Nb3 Be6 8.f3), "
            "6.Bg5 (classical), 6.Bc4 (Fischer's favourite). "
            "Black seeks ...b5-b4 queenside counterplay; White pushes kingside with "
            "g4-g5 or f4-f5. Outpost on d5 for White's knight is the key strategic goal. "
            "Related: Sicilian Dragon (Nf6 g6 — slower, fianchetto), "
            "Scheveningen (e6 — more solid), Kan (a6 e6 — flexible)."
        ),
        "eco": "B90-B99",
        "color": "black",
        "counters": [],
        "countered_by": ["opening_alapin"],
        "transposes_to": ["opening_sicilian_scheveningen"],
    },
    {
        "id": "opening_sicilian_dragon",
        "source": "ECO B70-B79 / Sicilian Dragon",
        "theme": "opening",
        "tags": ["sicilian", "dragon", "fianchetto", "g6", "1e4",
                 "opposite_castling", "sharp", "h_file", "attack"],
        "title": "Sicilian Dragon: Mutual Attacks on Opposite Wings",
        "principle": (
            "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 g6. "
            "Black fianchettoes the bishop to g7, creating a powerful diagonal. "
            "After the Yugoslav Attack (6.Be3 Bg7 7.f3 0-0 8.Qd2 Nc6 9.0-0-0), "
            "both sides castle on opposite wings and race to attack. "
            "White advances h4-h5 to open the h-file; Black plays ...d5 or ...Rxc3 "
            "followed by ...d5 to open lines for the dragon bishop. "
            "The Dragon bishop on g7 is the key piece — if traded, Black's attack fades. "
            "Related to King's Indian Defence (same fianchetto structure)."
        ),
        "eco": "B70-B79",
        "color": "black",
        "counters": [],
        "countered_by": ["opening_sicilian_dragon_yugoslav"],
        "transposes_to": ["opening_kings_indian"],
    },
    {
        "id": "opening_french",
        "source": "ECO C00-C19 / French Defence",
        "theme": "opening",
        "tags": ["french", "semi_open", "1e4", "e6", "solid", "pawn_chain",
                 "bad_bishop", "counterplay"],
        "title": "French Defence: Solid Counter-Attacking Play",
        "principle": (
            "1.e4 e6. Black builds a solid pawn structure and prepares ...d5, "
            "challenging White's centre. The characteristic problem: Black's light-squared "
            "bishop is often hemmed in by pawns on e6 and d5 — the 'bad bishop'. "
            "Main variations: Advance (5.e5 — Nimzowitsch pawn chain theory applies), "
            "Classical (3.Nc3 Nf6 4.Bg5), Winawer (3.Nc3 Bb4 — creates imbalances), "
            "Tarrasch (3.Nd2 — quieter), Exchange (3.exd5 — drawish). "
            "Black's counterplay: ...c5 and ...f6 to undermine White's centre. "
            "Related: Caro-Kann (more solid, no bad bishop issue)."
        ),
        "eco": "C00-C19",
        "color": "black",
        "counters": [],
        "countered_by": ["opening_advance_french"],
        "transposes_to": [],
    },
    {
        "id": "opening_caro_kann",
        "source": "ECO B10-B19 / Caro-Kann Defence",
        "theme": "opening",
        "tags": ["caro_kann", "semi_open", "1e4", "c6", "solid", "development",
                 "good_bishop", "structural"],
        "title": "Caro-Kann: Solid Development Without the Bad Bishop",
        "principle": (
            "1.e4 c6, preparing ...d5. Black challenges the centre without creating "
            "the bad light-squared bishop of the French. The c6 pawn supports ...d5 "
            "and does not block a piece. After 2.d4 d5, main lines: Classical (3.Nc3 "
            "dxe4 4.Nxe4), Advance (3.e5 Bf5), Panov-Botvinnik (3.exd5 cxd5 4.c4 — "
            "IQP structure, similar to QGD isolated pawn positions), Exchange (3.exd5 cxd5). "
            "Black's light-squared bishop develops to f5 or g4 before the pawn chain fixes it. "
            "Related: French Defence (similar pawn structure concept, but Caro-Kann avoids "
            "the bad bishop)."
        ),
        "eco": "B10-B19",
        "color": "black",
        "counters": [],
        "countered_by": ["opening_advance_caro"],
        "transposes_to": [],
    },
    {
        "id": "opening_alekhine",
        "source": "ECO B02-B05 / Alekhine's Defence",
        "theme": "opening",
        "tags": ["alekhine", "semi_open", "1e4", "hypermodern", "provocation",
                 "pawn_center", "counterattack"],
        "title": "Alekhine's Defence: Provoke, Then Attack the Centre",
        "principle": (
            "1.e4 Nf6. Black immediately provokes White to advance pawns with 2.e5 Nd5 "
            "3.d4 d6 4.c4 Nb6 5.f4 (Four Pawns Attack) or the main lines with Nc3/Nf3. "
            "The strategy follows Réti's hypermodern concept: invite White to build "
            "a large centre, then undermine it with ...dxe5, ...c5, and piece pressure. "
            "If White overextends, the pawns become targets. If White plays modestly, "
            "Black is fine. Sharp and risky, best for players who enjoy complex positions."
        ),
        "eco": "B02-B05",
        "color": "black",
        "counters": [],
        "countered_by": [],
        "transposes_to": [],
    },
    {
        "id": "opening_pirc",
        "source": "ECO B07-B09 / Pirc Defence",
        "theme": "opening",
        "tags": ["pirc", "modern", "semi_open", "1e4", "hypermodern", "fianchetto",
                 "flexible", "counterplay"],
        "title": "Pirc/Modern Defence: Flexible Fianchetto System",
        "principle": (
            "1.e4 d6 2.d4 Nf6 3.Nc3 g6. Black allows White a full centre and fianchettoes "
            "the king's bishop to fight back from a distance. Similar to Alekhine's Defence "
            "in concept (provoke the centre, then attack it) but more solid. "
            "White's sharpest response: Austrian Attack (4.f4 Bg7 5.Nf3 0-0 6.Bd3) — "
            "aggressive space grab. Black's goals: ...c5 or ...e5 breaks. "
            "Related: King's Indian Defence (similar structure with 1.d4), "
            "Modern Defence (3...g6 without ...Nf6 — even more flexible)."
        ),
        "eco": "B07-B09",
        "color": "black",
        "counters": [],
        "countered_by": ["opening_austrian_attack"],
        "transposes_to": ["opening_kings_indian"],
    },

    # -----------------------------------------------------------------------
    # CLOSED GAMES (1.d4 d5)
    # -----------------------------------------------------------------------
    {
        "id": "opening_queens_gambit",
        "source": "ECO D06-D69 / Queen's Gambit",
        "theme": "opening",
        "tags": ["queens_gambit", "d4", "closed_game", "center_control",
                 "queenside", "pawn_structure"],
        "title": "Queen's Gambit: White's Classical d4 Opening",
        "principle": (
            "1.d4 d5 2.c4. White offers the c-pawn to gain central control. "
            "QGA (2...dxc4): Black accepts and must return the pawn; gives White "
            "a strong centre but gives Black free development with ...c5/...e5. "
            "QGD (2...e6): solid, leads to Orthodox, Cambridge Springs, or Lasker "
            "Defence. Exchange Variation (3.cxd5 exd5): leads to minority attack. "
            "Tarrasch (3.Nd2, avoiding pin): Black can play the Tarrasch Defence "
            "(3...c5) for an IQP. Semi-Slav (2...c6 3.Nf3 e6): Meran (4.Nc3 Nf6 5.e3 "
            "a6 or b5) or Anti-Meran systems."
        ),
        "eco": "D06-D69",
        "color": "white",
        "counters": [],
        "countered_by": ["opening_nimzo_indian", "opening_kings_indian", "opening_grunfeld"],
        "transposes_to": ["opening_catalan"],
    },
    {
        "id": "opening_nimzo_indian",
        "source": "ECO E20-E59 / Nimzo-Indian Defence",
        "theme": "opening",
        "tags": ["nimzo_indian", "d4", "bishop_pin", "doubled_pawns",
                 "structural", "imbalance", "nimzowitsch"],
        "title": "Nimzo-Indian Defence: Pin the Knight, Create Imbalances",
        "principle": (
            "1.d4 Nf6 2.c4 e6 3.Nc3 Bb4. Black pins the c3 knight, threatening to "
            "double White's pawns after ...Bxc3. The resulting doubled c-pawns give "
            "White the bishop pair but weak pawn structure. "
            "Main variations: Classical (4.Qc2 — prevents doubling), Rubinstein "
            "(4.e3 — solid, Botvinnik played this), Sämisch (4.a3 Bxc3+ 5.bxc3), "
            "Leningrad (4.Bg5). Black obtains structural pressure; White gets the bishops. "
            "This is Black's most principled answer to 1.d4 — avoids a pawn centre "
            "without conceding equality. Related: Queen's Indian (avoids 3.Nc3)."
        ),
        "eco": "E20-E59",
        "color": "black",
        "counters": ["opening_queens_gambit"],
        "countered_by": [],
        "transposes_to": ["opening_queens_indian"],
    },
    {
        "id": "opening_kings_indian",
        "source": "ECO E60-E99 / King's Indian Defence",
        "theme": "opening",
        "tags": ["kings_indian", "d4", "fianchetto", "kingside_attack",
                 "dynamic", "counterplay", "e5_break"],
        "title": "King's Indian Defence: Dynamic Counterattack Against 1.d4",
        "principle": (
            "1.d4 Nf6 2.c4 g6 3.Nc3 Bg7 4.e4 d6 5.Nf3 0-0 6.Be2 e5. "
            "Black allows White a large centre and counterattacks with ...e5, "
            "creating the pawn tension that defines the opening. "
            "White's main plans: Classical (7.0-0 Nc6 8.d5 — space, knight manoeuvres), "
            "Sämisch (5.f3 — aggressive, prepares g4), Averbakh (5.Be2 e5 6.Bg5 — "
            "queenside pressure), Four Pawns Attack (5.f4 — overextension risk). "
            "Black's kingside attack (...Nf4, ...f5) vs White's queenside advance (c5, b4-b5). "
            "KID is a fighting defence — rarely drawn, high practical value. "
            "Related: Pirc (with 1.e4), Dragon Sicilian (same fianchetto pattern)."
        ),
        "eco": "E60-E99",
        "color": "black",
        "counters": ["opening_queens_gambit"],
        "countered_by": [],
        "transposes_to": ["opening_pirc", "opening_sicilian_dragon"],
    },
    {
        "id": "opening_grunfeld",
        "source": "ECO D70-D99 / Grünfeld Defence",
        "theme": "opening",
        "tags": ["grunfeld", "d4", "hypermodern", "center_destruction",
                 "dynamic", "d5_sacrifice", "piece_activity"],
        "title": "Grünfeld Defence: Sacrifice the Centre, Then Attack It",
        "principle": (
            "1.d4 Nf6 2.c4 g6 3.Nc3 d5. Black allows White to build a strong centre "
            "with 4.cxd5 Nxd5 5.e4 Nxc3 6.bxc3, then immediately attacks it with "
            "...c5, ...Bg7 (the powerful dragon-like bishop on g7), and piece pressure. "
            "Exchange Variation (4.cxd5 Nxd5 5.e4): White's centre is large but "
            "Black's pieces become very active. Russian System (5.Nf3 Bg7 6.Be2 0-0 "
            "7.0-0 Nc6): more positional. "
            "The Grünfeld is the hypermodern concept at its most extreme — "
            "let White have everything, then destroy it. Kasparov's main defence."
        ),
        "eco": "D70-D99",
        "color": "black",
        "counters": ["opening_queens_gambit"],
        "countered_by": [],
        "transposes_to": ["opening_kings_indian"],
    },
    {
        "id": "opening_slav",
        "source": "ECO D10-D19 / Slav Defence",
        "theme": "opening",
        "tags": ["slav", "d4", "c6", "solid", "queenside_play",
                 "pawn_structure", "structural"],
        "title": "Slav Defence: Support d5 With c6, Develop the Bishop",
        "principle": (
            "1.d4 d5 2.c4 c6. Black reinforces d5 with a pawn instead of blocking the "
            "light-squared bishop (as in the QGD with ...e6). The bishop can develop "
            "to f5 or g4 before being hemmed in. "
            "Semi-Slav (2...c6 3.Nf3 e6): combines both pawn moves, leading to complex "
            "lines — Meran (5.e3 a6 or b5), Moscow (5.Bg5 h6 6.Bh4 — positional), "
            "Anti-Moscow (6...g5!? — extremely sharp). "
            "The Slav is among the most solid responses to the Queen's Gambit. "
            "Related: Caro-Kann (same ...c6 concept but against 1.e4)."
        ),
        "eco": "D10-D19",
        "color": "black",
        "counters": ["opening_queens_gambit"],
        "countered_by": [],
        "transposes_to": ["opening_caro_kann"],
    },
    {
        "id": "opening_queens_indian",
        "source": "ECO E12-E19 / Queen's Indian Defence",
        "theme": "opening",
        "tags": ["queens_indian", "d4", "fianchetto", "queenside_bishop",
                 "hypermodern", "solid", "e4_prevention"],
        "title": "Queen's Indian Defence: Prevent e4 With Queenside Fianchetto",
        "principle": (
            "1.d4 Nf6 2.c4 e6 3.Nf3 b6. When White avoids 3.Nc3, Black fianchettoes "
            "the queenside bishop to b7, which will control the long diagonal and fight "
            "against White's e4 push. The QID is a solid, hypermodern system — the bishop "
            "on b7 exerts pressure without occupying the centre with pawns. "
            "Main line: 4.e3 Bb7 5.Bd3 Be7 (Classical); Petrosian Variation: 4.a3 "
            "(preventing ...Bb4). Related: Nimzo-Indian (when White plays 3.Nc3 instead)."
        ),
        "eco": "E12-E19",
        "color": "black",
        "counters": ["opening_queens_gambit"],
        "countered_by": [],
        "transposes_to": ["opening_nimzo_indian"],
    },
    {
        "id": "opening_catalan",
        "source": "ECO E00-E09 / Catalan Opening",
        "theme": "opening",
        "tags": ["catalan", "d4", "fianchetto", "g3", "long_diagonal",
                 "pressure", "open_catalan", "closed_catalan"],
        "title": "Catalan Opening: Fianchetto Pressure on the Queenside",
        "principle": (
            "1.d4 Nf6 2.c4 e6 3.g3. White fianchettoes the bishop to g2, aiming it "
            "down the long a8-h1 diagonal. In the Open Catalan (3...d5 4.Bg2 dxc4), "
            "Black accepts the pawn and White gets pressure on the long diagonal. "
            "Black must be careful to return the pawn at the right moment. "
            "Closed Catalan (4...Be7): solid but cramped. "
            "The Catalan bishop on g2 is one of the most powerful pieces in chess — "
            "it controls the centre from a distance and creates enduring pressure "
            "on the queenside. Structurally related to the English Opening (1.c4 g3)."
        ),
        "eco": "E00-E09",
        "color": "white",
        "counters": ["opening_nimzo_indian", "opening_queens_indian"],
        "countered_by": [],
        "transposes_to": ["opening_english"],
    },

    # -----------------------------------------------------------------------
    # FLANK OPENINGS
    # -----------------------------------------------------------------------
    {
        "id": "opening_english",
        "source": "ECO A10-A39 / English Opening",
        "theme": "opening",
        "tags": ["english", "flank", "c4", "hypermodern", "reversed_sicilian",
                 "flexible", "queenside_control"],
        "title": "English Opening: Flexible Flank Control",
        "principle": (
            "1.c4. White controls d5 immediately and can transpose to many systems "
            "depending on Black's response. Against ...e5: Reversed Sicilian — White "
            "has an extra tempo over a normal Sicilian and plays on the queenside. "
            "Against ...c5: Symmetrical English — both sides fight for d4/d5 control. "
            "Against ...Nf6: can transpose to Catalan, QID, or KID depending on setup. "
            "The English is a universally applicable first move — it avoids early "
            "forced theory and allows White to shape the game. "
            "Related: Réti (1.Nf3 before c4), Catalan (g3 + c4 + d4)."
        ),
        "eco": "A10-A39",
        "color": "white",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_catalan", "opening_reti", "opening_queens_gambit"],
    },
    {
        "id": "opening_reti",
        "source": "ECO A04-A09 / Réti Opening",
        "theme": "opening",
        "tags": ["reti", "flank", "hypermodern", "Nf3", "fianchetto",
                 "flexible", "c4", "center_from_distance"],
        "title": "Réti Opening: Hypermodern Centre Control",
        "principle": (
            "1.Nf3. White develops the knight and keeps all options open: c4 English, "
            "g3+Bg2 fianchetto, d4, or even e4. The Réti Gambit (1.Nf3 d5 2.c4) "
            "offers a pawn for rapid development. Main idea: fianchetto to g2 and "
            "control d5 and c5 from a distance. Black has no easy way to refute the "
            "flexibility. Against 1...d5, the KIA (King's Indian Attack) setup (2.g3 "
            "3.Bg2 4.0-0 5.d3 6.Nbd2) is a solid, universal system. "
            "Related: English Opening, King's Indian Attack."
        ),
        "eco": "A04-A09",
        "color": "white",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_english", "opening_catalan"],
    },
    {
        "id": "opening_dutch",
        "source": "ECO A80-A99 / Dutch Defence",
        "theme": "opening",
        "tags": ["dutch", "d4", "f5", "kingside_attack", "stonewall",
                 "leningrad", "classical_dutch", "counterplay"],
        "title": "Dutch Defence: Immediate Kingside Counterplay Against 1.d4",
        "principle": (
            "1.d4 f5. Black immediately stakes a claim on e4 and prepares a kingside "
            "attack, but weakens the e5 square and creates a somewhat vulnerable king. "
            "Three main systems: Stonewall (e6, d5, c6, f5 pawn structure — solid, "
            "targets e4), Leningrad (g6 Bg7 — dynamic, similar to KID), Classical "
            "(e6, d5, Nf6, Be7 — most solid). "
            "White's best counters: early e4 (the Staunton Gambit, 2.e4 fxe4 3.Nc3), "
            "or g3+Bg2 (fianchetto to fight the long diagonal). "
            "The Dutch is a fighting choice — rarely drawn, rich in counterplay."
        ),
        "eco": "A80-A99",
        "color": "black",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_kings_indian"],
    },

    # -----------------------------------------------------------------------
    # OPENING RELATIONSHIP ENTRIES (explicitly cross-referencing)
    # -----------------------------------------------------------------------
    {
        "id": "opening_relationship_french_nimzo",
        "source": "Structural Relationships — Multiple Sources",
        "theme": "opening",
        "tags": ["french", "nimzo_indian", "pawn_structure", "imbalance",
                 "structural", "doubled_pawns", "relationship"],
        "title": "French–Nimzo Structural Relationship",
        "principle": (
            "The French Winawer (1.e4 e6 2.d4 d5 3.Nc3 Bb4) and Nimzo-Indian "
            "(1.d4 Nf6 2.c4 e6 3.Nc3 Bb4) share the same strategic idea: Black pins "
            "the knight and aims to create doubled pawns on c3 (or c3/e4). "
            "The resulting structural patterns are similar — White's bishop pair "
            "versus Black's solid pawn structure. Lessons from one opening apply "
            "directly to the other; study both together."
        ),
        "eco": "Various",
        "color": "black",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_nimzo_indian", "opening_french"],
    },
    {
        "id": "opening_relationship_sicilian_english",
        "source": "Structural Relationships — Multiple Sources",
        "theme": "opening",
        "tags": ["sicilian", "english", "reversed_sicilian", "relationship",
                 "tempo", "queenside"],
        "title": "Sicilian–English Reversed Relationship",
        "principle": (
            "The English Opening (1.c4 e5) is a 'Reversed Sicilian' — White has the "
            "Sicilian structure but with an extra tempo. This means White can play more "
            "ambitiously: where in the Sicilian Black would play ...d5, White can play "
            "d4 with an extra move in hand. Studying Sicilian structures deeply will "
            "therefore illuminate English Opening plans and vice versa. "
            "The extra tempo makes the reversed Sicilian objectively slightly better "
            "for White than the equivalent Sicilian is for Black."
        ),
        "eco": "A20-A29",
        "color": "white",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_sicilian", "opening_english"],
    },
    {
        "id": "opening_relationship_kid_pirc",
        "source": "Structural Relationships — Multiple Sources",
        "theme": "opening",
        "tags": ["kings_indian", "pirc", "dragon", "fianchetto",
                 "relationship", "structural"],
        "title": "KID–Pirc–Dragon: The Fianchetto Family",
        "principle": (
            "The King's Indian Defence (1.d4), the Pirc (1.e4), and the Sicilian Dragon "
            "(1.e4 c5) all share the g6/Bg7 fianchetto structure. The strategic ideas — "
            "the dragon bishop controlling the long diagonal, ...d5 or ...e5 breaks, "
            "opposite-wing castling with mutual attacks — transfer directly between these openings. "
            "A player who deeply understands one will find the others intuitive. "
            "All three are dynamic, counterattacking systems that suit fighting players."
        ),
        "eco": "Various",
        "color": "black",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_kings_indian", "opening_pirc", "opening_sicilian_dragon"],
    },
    {
        "id": "opening_relationship_caro_slav",
        "source": "Structural Relationships — Multiple Sources",
        "theme": "opening",
        "tags": ["caro_kann", "slav", "c6", "solid", "relationship", "structural"],
        "title": "Caro-Kann–Slav: The c6 Solidarity",
        "principle": (
            "The Caro-Kann (1.e4 c6) and Slav Defence (1.d4 d5 2.c4 c6) share "
            "the same idea: play ...c6 to support the d5 pawn without blocking the "
            "light-squared bishop. Both are solid, structural defences with the "
            "same characteristic bishop freedom. Players who prefer one should "
            "study the other — the pawn structures are closely related and "
            "many endgame positions are identical."
        ),
        "eco": "Various",
        "color": "black",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_caro_kann", "opening_slav"],
    },
    {
        "id": "opening_relationship_french_caro",
        "source": "Structural Relationships — Multiple Sources",
        "theme": "opening",
        "tags": ["french", "caro_kann", "1e4", "solid", "relationship",
                 "bad_bishop", "structural"],
        "title": "French vs Caro-Kann: The Choice of 1.e4 Solid Defences",
        "principle": (
            "Both the French and Caro-Kann are solid defences against 1.e4 "
            "that challenge the centre with ...d5. The key difference: "
            "the French (1...e6) blocks the light-squared bishop — creating "
            "the chronic 'bad bishop' problem but supporting the centre. "
            "The Caro-Kann (1...c6) keeps the bishop free. "
            "Choose the French for richer, sharper play; choose the Caro-Kann "
            "for cleaner structure. Both can transpose to IQP positions "
            "via the Panov Attack or Tarrasch structures."
        ),
        "eco": "Various",
        "color": "black",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_french", "opening_caro_kann"],
    },
    {
        "id": "opening_relationship_qgd_nimzo_qid",
        "source": "Structural Relationships — Multiple Sources",
        "theme": "opening",
        "tags": ["queens_gambit", "nimzo_indian", "queens_indian", "d4",
                 "relationship", "black_repertoire"],
        "title": "Black's d4 Repertoire: QGD, Nimzo, and QID as a System",
        "principle": (
            "Against 1.d4, Black's three most principled responses — QGD (...e6 ...d5), "
            "Nimzo-Indian (...Nf6 ...e6 ...Bb4 when 3.Nc3), and QID (...Nf6 ...e6 ...b6 "
            "when 3.Nf3) — form a unified system. Play Nimzo when White plays Nc3; "
            "play QID when White plays Nf3 without Nc3 (to avoid Nimzo); "
            "play QGD when White plays e3 early. This trilogy covers all of White's "
            "main responses to 1.d4 Nf6 2.c4 e6 and forms the most theoretically "
            "sound Black repertoire against closed games."
        ),
        "eco": "Various",
        "color": "black",
        "counters": [],
        "countered_by": [],
        "transposes_to": ["opening_nimzo_indian", "opening_queens_indian", "opening_queens_gambit"],
    },
]

# ---------------------------------------------------------------------------
# SECTION 20 — UNIVERSAL TACTICAL MOTIFS
# ---------------------------------------------------------------------------

_TACTICS = [
    {
        "id": "tactic_fork_1",
        "source": "Common Tactical Patterns — Chess Fundamentals",
        "theme": "tactics",
        "tags": ["fork", "double_attack", "knight_fork", "tactics"],
        "title": "The Fork: Double Attack",
        "principle": (
            "A fork attacks two pieces (or a piece and a king) simultaneously. "
            "The knight fork is the most dangerous because knights jump over pieces "
            "and attack from unexpected angles. Before making any queen or piece move, "
            "check whether you leave a knight fork available. When calculating "
            "combinations, always look for fork squares — especially outpost squares "
            "that a knight can reach in one move."
        ),
    },
    {
        "id": "tactic_pin_1",
        "source": "Common Tactical Patterns — Chess Fundamentals",
        "theme": "tactics",
        "tags": ["pin", "absolute_pin", "relative_pin", "tactics"],
        "title": "The Pin: Fixing a Piece to a More Valuable Target",
        "principle": (
            "An absolute pin fixes a piece in front of the king — it cannot legally move. "
            "A relative pin means moving the piece would expose a valuable piece behind it. "
            "Exploit pins by attacking the pinned piece with pawns (gain material) or using "
            "the pin as a positional tool (the pinned piece is ineffective). "
            "Unpin aggressively if pinned — a pinned knight cannot defend, cannot attack."
        ),
    },
    {
        "id": "tactic_skewer_1",
        "source": "Common Tactical Patterns — Chess Fundamentals",
        "theme": "tactics",
        "tags": ["skewer", "x_ray", "tactics", "king"],
        "title": "The Skewer: Attack the More Valuable Piece to Win the One Behind",
        "principle": (
            "A skewer is a reverse pin — the more valuable piece is attacked and must move, "
            "exposing the less valuable piece behind it. The classic skewer targets a king "
            "or queen on an open file or diagonal with a rook or bishop. "
            "Always check for skewers when pieces are aligned on files, ranks, or diagonals, "
            "even if they are separated by other pieces — discovered attacks are related."
        ),
    },
    {
        "id": "tactic_discovered_1",
        "source": "Common Tactical Patterns — Chess Fundamentals",
        "theme": "tactics",
        "tags": ["discovered_attack", "discovered_check", "tactics"],
        "title": "The Discovered Attack: Two Threats in One Move",
        "principle": (
            "A discovered attack occurs when moving one piece reveals an attack by another. "
            "When the revealed attack is a check, it is a discovered check — one of the "
            "most powerful tactics because the moving piece can capture or threaten freely. "
            "Double check (both the moving and revealed piece give check) is practically "
            "decisive since only a king move can answer. "
            "Always scan for pieces aligned with the enemy king or queen."
        ),
    },
    {
        "id": "tactic_deflection_1",
        "source": "Common Tactical Patterns — Chess Fundamentals",
        "theme": "tactics",
        "tags": ["deflection", "decoy", "overloading", "tactics"],
        "title": "Deflection and Overloading",
        "principle": (
            "Deflection forces a defensive piece to abandon its post — usually by "
            "sacrificing material to it, forcing a capture that removes the defender. "
            "Overloading occurs when one piece is defending two things simultaneously; "
            "attack both to exploit the defender's inability to maintain both duties. "
            "Before combinations, identify overloaded pieces — they are the tactical "
            "vulnerabilities of a position."
        ),
    },
    {
        "id": "tactic_back_rank_1",
        "source": "Common Tactical Patterns — Chess Fundamentals",
        "theme": "tactics",
        "tags": ["back_rank_mate", "back_rank", "tactics", "mating_pattern"],
        "title": "Back Rank Weakness: The Most Common Mating Pattern",
        "principle": (
            "A king trapped on the back rank by its own pawns is vulnerable to a back-rank "
            "mate with a rook or queen. Before sacrificing to open lines, check if the "
            "opponent's back rank is defended. Create a luft (pawn advance: h3/h6 or g3/g6) "
            "to give the king an escape square before it becomes critical. "
            "The back-rank mate is the single most common way games are decided by "
            "beginners and intermediate players."
        ),
    },
    {
        "id": "tactic_zwischenzug_1",
        "source": "Common Tactical Patterns — Chess Fundamentals",
        "theme": "tactics",
        "tags": ["zwischenzug", "in_between_move", "tactics", "calculation"],
        "title": "The Zwischenzug: The In-Between Move",
        "principle": (
            "A zwischenzug (German: 'in-between move') is an intermediate move that "
            "interrupts the expected sequence with a more urgent threat. "
            "Instead of recapturing immediately, an in-between check or attack forces "
            "the opponent to respond first, changing the sequence in your favour. "
            "Always ask after any capture: 'Before I recapture, is there a better move?' "
            "Many tactics fail or succeed based on missing a zwischenzug."
        ),
    },
]

# ---------------------------------------------------------------------------
# ASSEMBLE FINAL LIST
# ---------------------------------------------------------------------------

PRINCIPLES = (
    _MORPHY
    + _STEINITZ
    + _TARRASCH
    + _RETI
    + _LASKER
    + _NIMZO
    + _CAPA
    + _ALEKHINE
    + _EUWE
    + _BRONSTEIN
    + _FISCHER
    + _SILMAN
    + _KOTOV
    + _KERES
    + _DVORETSKY
    + _VILLA
    + _VUKOVIC
    + _CHERNEV
    + _OPENINGS
    + _TACTICS
)
