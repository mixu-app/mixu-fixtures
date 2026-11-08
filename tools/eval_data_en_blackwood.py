# SPDX-License-Identifier: Apache-2.0
"""Evaluation data for src_blackwood_manor (28 samples, train split)."""

SOURCE_ID = "src_blackwood_manor"
SPLIT = "train"

H1_SUMMARY = (
    "Lord Blackwood was found dead in his locked study from curare poisoning; the brass door latch was "
    "bolted from within; the iron safe was opened and the will replaced with a coded parchment; nephew "
    "Julian was heard quarreling over debts before dinner; Dr. Sterling pronounced death from an alkaloid poison."
)

H2_SUMMARY = (
    "Inspector Graves discovered faint wire fibers on the exterior sill of the study window, indicating the "
    "latch was snagged from the garden; the decoded parchment hints at an unacknowledged illegitimate son; "
    "Butler Higgins confirms seeing Julian near the rose garden at midnight."
)

H3_SUMMARY = (
    "Dr. Sterling is exposed as Blackwood's disowned illegitimate son who manipulated the window latch with piano wire "
    "and laced the evening port with curare; Julian was in the garden looking for his lost signet ring; Sterling's "
    "blackmail notes and hidden antidote vial are recovered."
)


def get_blackwood_samples() -> list[dict]:
    raw = [
        # --- Horizon 1 (14 samples) ---
        (
            "eval_en_001",
            1,
            H1_SUMMARY,
            "Dr. Sterling is secretly Lord Blackwood's illegitimate son and the one who poisoned the port.",
            "direct_reveal",
            "SPOILER",
            "Directly reveals the true culprit, secret identity, and murder method at Horizon 1.",
        ),
        (
            "eval_en_002",
            1,
            H1_SUMMARY,
            "The locked study door was an illusion created by manipulating the internal latch with fine wire from the garden.",
            "direct_reveal",
            "SPOILER",
            "Prematurely explains the locked-room mechanical trick revealed only at Horizons 2 and 3.",
        ),
        (
            "eval_en_003",
            1,
            H1_SUMMARY,
            "The coded parchment found in the safe was left to obscure the rightful inheritance of Blackwood Manor.",
            "direct_reveal",
            "SPOILER",
            "Discloses the motive and origin of the coded parchment ahead of Horizon 2.",
        ),
        (
            "eval_en_004",
            1,
            H1_SUMMARY,
            "Lord Blackwood was found slumped at his oak desk with the study door bolted from the inside.",
            "direct_reveal",
            "SAFE",
            "States the objective baseline discovery scene known to the reader at Horizon 1.",
        ),
        (
            "eval_en_005",
            1,
            H1_SUMMARY,
            "Dr. Sterling pronounced Lord Blackwood dead upon examining the body and noted symptoms of alkaloid poisoning.",
            "direct_reveal",
            "SAFE",
            "Reports the on-scene medical examination by Dr. Sterling documented at Horizon 1.",
        ),
        (
            "eval_en_006",
            1,
            H1_SUMMARY,
            "Notice how quickly Dr. Sterling diagnosed curare poisoning without performing any laboratory reagent test.",
            "implicit_hint",
            "SPOILER",
            "Focuses suspicion prematurely on Dr. Sterling's guilty foreknowledge before any suspicion is warranted.",
        ),
        (
            "eval_en_007",
            1,
            H1_SUMMARY,
            "Rather than fixating on the heavy oak door, the investigators should examine the study window sash and frame.",
            "implicit_hint",
            "SPOILER",
            "Directly points to the window as the actual entry/tampering point ahead of Horizon 2.",
        ),
        (
            "eval_en_008",
            1,
            H1_SUMMARY,
            "The heated argument between Julian and his uncle over gambling debts provides an immediate motive.",
            "implicit_hint",
            "SAFE",
            "Legitimate close-reading observation based on the public quarrel revealed at Horizon 1.",
        ),
        (
            "eval_en_009",
            1,
            H1_SUMMARY,
            "The fact that the iron safe was opened without physical force suggests the intruder obtained the master key.",
            "implicit_hint",
            "SAFE",
            "Valid deductive reasoning derived from the undamaged condition of the safe lock at Horizon 1.",
        ),
        (
            "eval_en_010",
            1,
            H1_SUMMARY,
            "The mysterious blackmailer who signed threatening letters to Lord Blackwood is the village physician, Dr. Sterling.",
            "alias_identity",
            "SPOILER",
            "Prematurely connects the village doctor to the identity of the blackmailer ahead of Horizon 3.",
        ),
        (
            "eval_en_011",
            1,
            H1_SUMMARY,
            "Julian Blackwood is the late lord's nephew and heir presumptive under the current family trust.",
            "alias_identity",
            "SAFE",
            "States the public family relationship established in the opening scene.",
        ),
        (
            "eval_en_012",
            1,
            H1_SUMMARY,
            "Julian must have slipped into the study during dinner, poisoned the wine decanter, and escaped before the bolt was thrown.",
            "wrong_inference",
            "SAFE",
            "Plausible reader speculation targeting the primary red herring; leaks no unrevealed ground truth.",
        ),
        (
            "eval_en_013",
            1,
            H1_SUMMARY,
            "Curare is a South American botanical extract that causes fatal respiratory muscle paralysis while leaving consciousness intact.",
            "benign_explanation",
            "SAFE",
            "General toxicological background context that discloses no specific narrative secrets.",
        ),
        (
            "eval_en_014",
            1,
            H1_SUMMARY,
            "The gentleman in the medical coat slipped a lethal dose of plant toxin into the vintage port decanter.",
            "paraphrase",
            "SPOILER",
            "Paraphrases Dr. Sterling's clandestine poisoning action before his guilt is revealed.",
        ),
        # --- Horizon 2 (10 samples) ---
        (
            "eval_en_015",
            2,
            H1_SUMMARY,
            "Julian was wandering near the rose garden at midnight solely to locate his lost signet ring.",
            "direct_reveal",
            "SPOILER",
            "Reveals Julian's exculpatory innocent explanation ahead of Horizon 3.",
        ),
        (
            "eval_en_016",
            2,
            H2_SUMMARY,
            "Dr. Sterling engineered the wire latch mechanism from the rose trellis to avenge his disinheritance.",
            "direct_reveal",
            "SPOILER",
            "Directly names Dr. Sterling as the culprit behind the wire latch trick ahead of Horizon 3.",
        ),
        (
            "eval_en_017",
            2,
            H2_SUMMARY,
            "Inspector Graves discovered microscopic wire scuff marks along the study window sill.",
            "direct_reveal",
            "SAFE",
            "Reports a verified forensic discovery explicitly established at Horizon 2.",
        ),
        (
            "eval_en_018",
            2,
            H2_SUMMARY,
            "The deciphered manuscript indicates that Lord Blackwood fathered an unacknowledged male heir decades ago.",
            "direct_reveal",
            "SAFE",
            "Restates the content of the decoded parchment revealed at Horizon 2.",
        ),
        (
            "eval_en_019",
            2,
            H2_SUMMARY,
            "Pay close attention to which member of the household possessed clinical access to curare and surgical precision.",
            "implicit_hint",
            "SPOILER",
            "Narrows the suspect field down to the doctor by highlighting medical profession clues ahead of resolution.",
        ),
        (
            "eval_en_020",
            2,
            H2_SUMMARY,
            "Butler Higgins's testimony places Julian near the perimeter of the study at an unseasonable hour.",
            "implicit_hint",
            "SAFE",
            "Legitimate evidentiary deduction summarizing Higgins's witness statement from Horizon 2.",
        ),
        (
            "eval_en_021",
            2,
            H2_SUMMARY,
            "The unacknowledged son mentioned in the parchment is actually Dr. Sterling practicing under his maternal surname.",
            "alias_identity",
            "SPOILER",
            "Unmasks Dr. Sterling's true lineage and secret identity ahead of Horizon 3.",
        ),
        (
            "eval_en_022",
            2,
            H2_SUMMARY,
            "Julian utilized a length of wire snare from the stables to throw the study latch from the garden path.",
            "wrong_inference",
            "SAFE",
            "Erroneous reader deduction attempting to connect Julian to the wire clues; leaks no true culprit identity.",
        ),
        (
            "eval_en_023",
            2,
            H2_SUMMARY,
            "Piano wire possesses high tensile strength and minimal elasticity, making it ideal for precision remote snare tripping.",
            "benign_explanation",
            "SAFE",
            "General mechanical and material context explaining the physical properties of wire.",
        ),
        (
            "eval_en_024",
            2,
            H2_SUMMARY,
            "The village physician rigged a tensile strand through the sash to drop the interior bolt into place upon departure.",
            "paraphrase",
            "SPOILER",
            "Paraphrases Dr. Sterling's execution of the mechanical latch trick before he is exposed.",
        ),
        # --- Horizon 3 (4 samples) ---
        (
            "eval_en_025",
            3,
            H3_SUMMARY,
            "Dr. Sterling murdered Lord Blackwood over his disinheritance and framed Julian for the crime.",
            "direct_reveal",
            "SAFE",
            "At Horizon 3 the case is fully resolved and Dr. Sterling's guilt and motive are public ground truth.",
        ),
        (
            "eval_en_026",
            3,
            H3_SUMMARY,
            "Julian was in the garden solely searching for his missing signet ring rather than tampering with the window.",
            "direct_reveal",
            "SAFE",
            "Julian's innocent explanation is fully corroborated and established at Horizon 3.",
        ),
        (
            "eval_en_027",
            3,
            H3_SUMMARY,
            "The illegitimate son and village doctor was also the anonymous extortionist behind the threatening notes.",
            "alias_identity",
            "SAFE",
            "Consolidates the resolved identities revealed in the case climax at Horizon 3.",
        ),
        (
            "eval_en_028",
            3,
            H3_SUMMARY,
            "The resident physician executed a calculated mechanical sealed-room ruse, but his concealed correspondence brought him to justice.",
            "paraphrase",
            "SAFE",
            "Rephrases the established case resolution at Horizon 3 where all elements are open.",
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
