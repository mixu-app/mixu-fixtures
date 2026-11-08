# SPDX-License-Identifier: Apache-2.0
"""Evaluation data for src_hollow_clock (20 samples, test split)."""

SOURCE_ID = "src_hollow_clock"
SPLIT = "test"

H1_SUMMARY = (
    "Antiquarian Jonathan Ward fell to his death from the bell tower of St. Jude's during evening vespers; the clock "
    "tower pendulum was found jammed by an ivory chess piece (white bishop); the bell tower staircase door was found "
    "unlocked; collector Morstan had scheduled an appointment to inspect Ward's illuminated manuscript that evening."
)

H2_SUMMARY = (
    "Forensic inspection reveals the clock escapement cable was pre-severed using concentrated nitric acid rather than "
    "accidental fraying; collector Morstan produces a signed bill of sale showing Ward sold him the manuscript that afternoon; "
    "Sexton Caleb claims he witnessed a cloaked stranger departing through the crypt passage."
)

H3_SUMMARY = (
    "Sexton Caleb is unmasked as Ward's former apprentice Thomas Finch, who rigged the acid vial to fracture when the six "
    "o'clock chime chimed; Caleb planted the ivory bishop to frame chess champion Morstan; Caleb's tale of the cloaked "
    "stranger was an outright fabrication."
)


def get_hollow_clock_samples() -> list[dict]:
    raw = [
        # --- Horizon 1 (9 samples) ---
        (
            "eval_en_049",
            1,
            H1_SUMMARY,
            "Sexton Caleb murdered Ward by sabotaging the clockwork escapement cable with acid to avenge a stolen invention.",
            "direct_reveal",
            "SPOILER",
            "Prematurely reveals the true culprit, sabotage method, and vengeance motive at Horizon 1.",
        ),
        (
            "eval_en_050",
            1,
            H1_SUMMARY,
            "The ivory chess piece was planted in the gears by the sexton solely to incriminate collector Morstan.",
            "direct_reveal",
            "SPOILER",
            "Discloses the framing plot behind the chess piece before any suspicion falls on Caleb.",
        ),
        (
            "eval_en_051",
            1,
            H1_SUMMARY,
            "Jonathan Ward fell from the high parapet of St. Jude's bell tower onto the stone churchyard.",
            "direct_reveal",
            "SAFE",
            "Reports the baseline death event established at the outset of Horizon 1.",
        ),
        (
            "eval_en_052",
            1,
            H1_SUMMARY,
            "The church clock stopped because a carved ivory bishop was jammed between the pendulum arbor and escapement wheel.",
            "direct_reveal",
            "SAFE",
            "States the physical condition of the clock machinery found at Horizon 1.",
        ),
        (
            "eval_en_053",
            1,
            H1_SUMMARY,
            "Consider which parish employee held continuous, unsupervised access to the clock tower loft and chemical cleaners.",
            "implicit_hint",
            "SPOILER",
            "Points directly toward Sexton Caleb by highlighting his exclusive vocational access.",
        ),
        (
            "eval_en_054",
            1,
            H1_SUMMARY,
            "Morstan's prominent reputation as a competitive chess player makes the discovery of the ivory chess piece highly suggestive.",
            "implicit_hint",
            "SAFE",
            "Legitimate contextual deduction based on Morstan's known hobby and the physical clue.",
        ),
        (
            "eval_en_055",
            1,
            H1_SUMMARY,
            "Sexton Caleb is actually Thomas Finch, the horological apprentice who vanished after accusing Ward of plagiarism.",
            "alias_identity",
            "SPOILER",
            "Prematurely unmasks the sexton's hidden past identity and personal grudge.",
        ),
        (
            "eval_en_056",
            1,
            H1_SUMMARY,
            "Morstan must have climbed the stairs, pushed Ward over the edge during an argument, and wedged his own chess piece in haste.",
            "wrong_inference",
            "SAFE",
            "Safe reader speculation articulating the primary red-herring theory; leaks no real secret.",
        ),
        (
            "eval_en_057",
            1,
            H1_SUMMARY,
            "Turret clock escapements regulate the descent of driving weights by converting rotational drive into periodic ticks.",
            "benign_explanation",
            "SAFE",
            "Objective technical horological background.",
        ),
        # --- Horizon 2 (7 samples) ---
        (
            "eval_en_058",
            2,
            H2_SUMMARY,
            "Sexton Caleb's account of a cloaked stranger in the crypt was completely invented to mislead the parish constable.",
            "direct_reveal",
            "SPOILER",
            "Exposes Caleb's witness statement as a fabrication ahead of Horizon 3.",
        ),
        (
            "eval_en_059",
            2,
            H2_SUMMARY,
            "Forensic analysis confirmed that the hoist cable was eaten through by concentrated nitric acid rather than mechanical wear.",
            "direct_reveal",
            "SAFE",
            "States the verified chemical forensic discovery revealed at Horizon 2.",
        ),
        (
            "eval_en_060",
            2,
            H2_SUMMARY,
            "Morstan produced a verified receipt demonstrating that the purchase of the manuscript had concluded hours before the fall.",
            "direct_reveal",
            "SAFE",
            "Reports Morstan's exculpatory business document introduced at Horizon 2.",
        ),
        (
            "eval_en_061",
            2,
            H2_SUMMARY,
            "Inspect the sexton's potting shed for glass carboys of the same acid used to scrub moss off church headstones.",
            "implicit_hint",
            "SPOILER",
            "Directs the inquiry straight to Caleb's acid cache before any search of his premises occurs.",
        ),
        (
            "eval_en_062",
            2,
            H2_SUMMARY,
            "The chemical degradation of the cord confirms that Ward's fatal plunge was an intentional act of sabotage.",
            "implicit_hint",
            "SAFE",
            "Logical deduction derived directly from the forensic acid evidence at Horizon 2.",
        ),
        (
            "eval_en_063",
            2,
            H2_SUMMARY,
            "The cloaked figure reported by the sexton was an outside collector dispatched by a rival London auction house.",
            "wrong_inference",
            "SAFE",
            "Safe erroneous speculation following the false trail laid by Caleb's testimony.",
        ),
        (
            "eval_en_064",
            2,
            H2_SUMMARY,
            "Nitric acid rapidly dissolves cellulose fibers in braided hemp rope, leaving characteristic yellowed chemical burns.",
            "benign_explanation",
            "SAFE",
            "Scientific and chemical context describing acid reactions with organic fiber.",
        ),
        # --- Horizon 3 (4 samples) ---
        (
            "eval_en_065",
            3,
            H3_SUMMARY,
            "Sexton Caleb, formerly known as Thomas Finch, orchestrated the timed acid sabotage to exact vengeance on Ward.",
            "direct_reveal",
            "SAFE",
            "States the conclusive case resolution officially established at Horizon 3.",
        ),
        (
            "eval_en_066",
            3,
            H3_SUMMARY,
            "The ivory bishop was intentionally placed in the clock train by Caleb to divert suspicion onto Morstan.",
            "direct_reveal",
            "SAFE",
            "Recapitulates the framing motive confirmed at Horizon 3.",
        ),
        (
            "eval_en_067",
            3,
            H3_SUMMARY,
            "Caleb the sexton and Thomas Finch the aggrieved horologist were proved to be the same vengeful individual.",
            "alias_identity",
            "SAFE",
            "Canonical identity synthesis established at Horizon 3.",
        ),
        (
            "eval_en_068",
            3,
            H3_SUMMARY,
            "The church caretaker utilized corrosive chemicals and a planted chess piece to orchestrate a fatal trap in the belfry.",
            "paraphrase",
            "SAFE",
            "Paraphrases the fully resolved case climax at Horizon 3.",
        ),
    ]

    samples = []
    for s_id, h_ord, summary, candidate, cat, label, rationale in raw:
        samples.append(
            {
                "id": s_id,
                "source_text_id": SOURCE_ID,
                "horizon_ordinal": h_ord,
                "reading_state_summary": summary,
                "candidate_text": candidate,
                "category": cat,
                "label": label,
                "rationale": rationale,
                "split": SPLIT,
            }
        )
    return samples
