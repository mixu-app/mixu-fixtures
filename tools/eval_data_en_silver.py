# SPDX-License-Identifier: Apache-2.0
"""Evaluation data for src_silver_express (20 samples, val split)."""

SOURCE_ID = "src_silver_express"
SPLIT = "val"

H1_SUMMARY = (
    "The Silver Express is halted by a blizzard in the Pennine moors; Lady Catherine's emerald necklace disappeared "
    "from her locked sleeping compartment; the door chain was unfastened; Countess Vane claims she saw a tall figure "
    "in a railway conductor's overcoat running toward the rear carriage."
)

H2_SUMMARY = (
    "A conductor's heavy wool overcoat stained with green velvet lint is discovered inside the carriage linen hamper; "
    "courier Pierre is detained after duplicate carriage master keys are found in his luggage; Countess Vane's presence "
    "in the dining saloon ten minutes after the alarm is supported by the chef."
)

H3_SUMMARY = (
    "Pierre and Countess Vane are exposed as co-conspirators in an insurance swindle; the man in the conductor's "
    "overcoat was Vane's estranged brother; the genuine emeralds were concealed inside Countess Vane's hollow perfume "
    "atomizer prior to the staged outcry."
)


def get_silver_express_samples() -> list[dict]:
    raw = [
        # --- Horizon 1 (9 samples) ---
        (
            "eval_en_029",
            1,
            H1_SUMMARY,
            "Countess Vane and courier Pierre conspired together to stage a bogus theft for an insurance payout.",
            "direct_reveal",
            "SPOILER",
            "Reveals the criminal conspiracy between Vane and Pierre ahead of Horizon 3.",
        ),
        (
            "eval_en_030",
            1,
            H1_SUMMARY,
            "The emerald necklace was hidden inside Countess Vane's hollow scent bottle before anyone raised the alarm.",
            "direct_reveal",
            "SPOILER",
            "Discloses the secret hiding place of the stolen jewels ahead of Horizon 3.",
        ),
        (
            "eval_en_031",
            1,
            H1_SUMMARY,
            "Lady Catherine reported that her emerald necklace was missing from her private sleeper compartment.",
            "direct_reveal",
            "SAFE",
            "States the basic theft report established at the start of Horizon 1.",
        ),
        (
            "eval_en_032",
            1,
            H1_SUMMARY,
            "Countess Vane claimed to have seen an individual in a conductor's overcoat dashing down the corridor.",
            "direct_reveal",
            "SAFE",
            "Accurately reports Countess Vane's witness statement given at Horizon 1.",
        ),
        (
            "eval_en_033",
            1,
            H1_SUMMARY,
            "Notice that Countess Vane was fully attired with fresh perfume applied despite the midnight hour.",
            "implicit_hint",
            "SPOILER",
            "Focuses attention on Countess Vane's suspicious preparedness and perfume bottle prior to forensic clues.",
        ),
        (
            "eval_en_034",
            1,
            H1_SUMMARY,
            "The unfastened security chain suggests the compartment door was either opened from the inside or bypassed with a tool.",
            "implicit_hint",
            "SAFE",
            "Valid physical deduction based on the condition of the door lock at Horizon 1.",
        ),
        (
            "eval_en_035",
            1,
            H1_SUMMARY,
            "The shadowy figure fleeing in the conductor's overcoat is Countess Vane's fugitive brother, Roger Vane.",
            "alias_identity",
            "SPOILER",
            "Prematurely unmasks the identity of the person seen in the corridor ahead of Horizon 3.",
        ),
        (
            "eval_en_036",
            1,
            H1_SUMMARY,
            "An outside tramp must have boarded the train while stalled in the snowdrift and snatched the jewels through the vestibule.",
            "wrong_inference",
            "SAFE",
            "Safe erroneous speculation that introduces a false outside intruder without leaking true plot facts.",
        ),
        (
            "eval_en_037",
            1,
            H1_SUMMARY,
            "First-class sleeping compartments on the Pennine route feature heavy mahogany doors secured by brass slide chains.",
            "benign_explanation",
            "SAFE",
            "Descriptive architectural and vehicular context of the train compartment.",
        ),
        # --- Horizon 2 (7 samples) ---
        (
            "eval_en_038",
            2,
            H2_SUMMARY,
            "The conductor coat discovered in the hamper was worn by Countess Vane's brother to manufacture an alibi.",
            "direct_reveal",
            "SPOILER",
            "Discloses the true wearer of the uniform and the decoy plan ahead of Horizon 3.",
        ),
        (
            "eval_en_039",
            2,
            H2_SUMMARY,
            "Searchers found a conductor's heavy wool overcoat bearing green velvet lint inside the service linen hamper.",
            "direct_reveal",
            "SAFE",
            "Direct statement of the physical item recovered during the official carriage search at Horizon 2.",
        ),
        (
            "eval_en_040",
            2,
            H2_SUMMARY,
            "The green velvet lint on the recovered coat matches the lining of Lady Catherine's jewel case.",
            "implicit_hint",
            "SAFE",
            "Forensic correlation established during the Horizon 2 inspection.",
        ),
        (
            "eval_en_041",
            2,
            H2_SUMMARY,
            "The conductor seen by Vane was an accomplice brought aboard under a false passenger manifest.",
            "implicit_hint",
            "SPOILER",
            "Discloses the accomplice conspiracy ahead of the official resolution in Horizon 3.",
        ),
        (
            "eval_en_042",
            2,
            H2_SUMMARY,
            "Courier Pierre acted alone, using duplicate keys to loot the compartment before shedding the uniform in the hamper.",
            "wrong_inference",
            "SAFE",
            "Classic red-herring hypothesis targeting the prime suspect; leaks none of Vane's complicity.",
        ),
        (
            "eval_en_043",
            2,
            H2_SUMMARY,
            "Master skeleton keys designed for railway carriages rely on notched ward blades that bypass standard tumbler stops.",
            "benign_explanation",
            "SAFE",
            "General technical locksmith explanation describing how railway skeleton keys function.",
        ),
        (
            "eval_en_044",
            2,
            H2_SUMMARY,
            "The courier in custody was carrying duplicate brass blanks, while a discarded railway uniform was retrieved from the laundry bin.",
            "paraphrase",
            "SAFE",
            "Accurate paraphrase of the public investigative findings established at Horizon 2.",
        ),
        # --- Horizon 3 (4 samples) ---
        (
            "eval_en_045",
            3,
            H3_SUMMARY,
            "Pierre and Countess Vane orchestrated the entire theft as an insurance fraud scheme with her brother acting as a decoy.",
            "direct_reveal",
            "SAFE",
            "At Horizon 3 all conspirators, roles, and motives are officially unmasked.",
        ),
        (
            "eval_en_046",
            3,
            H3_SUMMARY,
            "The genuine emerald necklace was retrieved from inside Countess Vane's hollow silver perfume atomizer.",
            "direct_reveal",
            "SAFE",
            "The recovery location of the physical evidence is fully revealed at Horizon 3.",
        ),
        (
            "eval_en_047",
            3,
            H3_SUMMARY,
            "The fleeing conductor spotted in the blizzard was in truth Roger Vane acting in concert with his sister.",
            "alias_identity",
            "SAFE",
            "Canonical identity resolution confirmed at Horizon 3.",
        ),
        (
            "eval_en_048",
            3,
            H3_SUMMARY,
            "The noblewoman and the courier engineered a phantom robbery to pocket the underwriter's indemnification funds.",
            "paraphrase",
            "SAFE",
            "Rephrases the established case resolution at Horizon 3.",
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
