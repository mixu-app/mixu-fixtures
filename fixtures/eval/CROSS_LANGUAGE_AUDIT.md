# Cross-Language Boundary and Audit Register for Multilingual Spoiler Evaluation

This document establishes the cross-linguistic boundary analysis, normative decision framework, and audit register for the Mixu multilingual spoiler evaluation corpus across Chinese (`chinese-spoiler-eval`), English (`english-spoiler-eval`), and Japanese (`japanese-spoiler-eval`).

## Executive overview and audit mandate

The core challenge of automated spoiler detection across natural languages is that knowledge boundaries are expressed through distinct syntactic and pragmatic mechanisms. A statement may look like a harmless speculative query in one language, yet function as an indisputable factual revelation in another due to grammaticalized evidentiality, modal particles, or passive voice attributions.

To prevent classifiers and copilot safety filters from failing on multilingual inputs, this audit specifies:

1. **Cross-language linguistic boundary mechanisms**: How English epistemic hedging, Japanese modal/hearsay particles, and Chinese aspectual markers interact with the knowledge-horizon boundary.
2. **The normative tripartite distinction**: Strict demarcation between *Witness Claims*, *Observed Facts*, and *Speculative Inferences*.
3. **Ruby annotation invariance**: Proof that Japanese typographic ruby annotations (`<ruby>...</ruby>` and `｜...《...》`) do not compromise classification accuracy whether retained or normalized.
4. **Borderline audit register**: A curated cross-language audit of 24 representative borderline cases documenting initial assessments, auditor disagreements, and certified consensus decisions.

---

## Cross-language linguistic boundary analysis

### 1. English: Epistemic hedging, evidential verbs, and passive voice

In English mystery discourse, candidate texts frequently employ modal auxiliaries (`might`, `could`, `must`), epistemic hedging verbs (`suggests`, `indicates`, `implies`), and passive reporting frames (`it is claimed that`, `allegedly`):

- **Hedging as a disguise for unrevealed ground truth:** When a candidate text hedges an unrevealed fact—e.g. *"Could Dr. Sterling perhaps be Lord Blackwood's disowned son?"*—the hedge does not render the statement safe. In mystery evaluation, introducing an unrevealed true proposition (even framed interrogatively or hypothetically) collapses the reader's hypothesis space from infinity to unity. **Decision:** `SPOILER`.
- **Evidential framing of witness testimony:** Conversely, framing an in-evidence witness statement with attribution—e.g. *"Countess Vane reported seeing a figure in a conductor's coat"*—is strictly `SAFE` at Horizon 1 because it mirrors the reader's current observation of the narrative. However, omitting the attribution—e.g. *"A man in a conductor's coat was fleeing down the corridor"*—confirms the presence of that figure as an objective fact before forensic corroboration, risking an implicit hint.
- **Agentless passive constructions:** Sentences like *"The lock was manipulated from the outside"* suppress the grammatical subject. If the fact of tampering is already forensically established, this passive is `SAFE`. If tampering has not yet been discovered, introducing the passive assertion constitutes a premature `implicit_hint` or `direct_reveal` `SPOILER`.

### 2. Japanese: Modal particles, hearsay markers, and syntactic omission

Japanese encodes epistemic certainty and information source directly through grammaticalized sentence-final particles and auxiliaries:

- **Hearsay markers (`〜らしい`, `〜そうだ`, `〜と証言した`):** Japanese distinguishes between direct observation (`〜た`) and hearsay (`〜とのことだ`, `〜らしい`). A candidate text stating `「透が当主と口論していたと執事が証言している」` (The butler testified that Toru was arguing with the master) accurately tracks a witness claim in the reader's state and is `SAFE`. If the text instead uses objective assertion for an unverified claim—e.g. `「透が犯人である」`—it functions as a speculative inference or wrong deduction (which is `SAFE` if false, but `SPOILER` if true).
- **Conjecture particles (`〜かもしれない`, `〜に違いない`, `〜だろう`):** When conjectural modals are appended to an unrevealed true secret—e.g. `「佐々木医師が氷に毒を仕込んだのではないか」` (Might Dr. Sasaki have hidden poison in the ice?)—the modal does NOT immunize the statement. Because the proposition contains unrevealed ground truth (the ice poison trick), it is an `implicit_hint` `SPOILER`.
- **Subject / topic omission (*Zero Anaphora*):** Japanese frequently omits grammatical subjects when pragmatically inferred. In candidate texts such as `「格子窓から絹糸を引いて閂を落とした」` (Pulled silk thread through the lattice window and dropped the bolt), the omitted agent does not prevent the sentence from disclosing the secret mechanical trick. Classifiers must evaluate the proposition's semantic payload regardless of overt agent realization.

### 3. Chinese: Aspectual particles, coverbs, and semantic framing

In Chinese, knowledge boundaries are predominantly governed by aspectual markers (`早已`, `已经`, `曾`), coverbal prepositional phrases (`据...称`, `通过...`), and lexical register:

- **Aspectual confirmation (`早已`, `本就是`):** Markers indicating prior completion prematurely elevate temporary hypotheses into permanent truths. For example, in `src_gallery_theft`, saying `「展柜里的真品早已被换成尖晶石」` (The genuine gem had long been swapped for spinel) converts an ongoing mystery into an established fait accompli before the appraisal scene. **Decision:** `SPOILER`.
- **Attribution framing (`据称`, `目击者指出`):** Like English and Japanese, reporting a character's claim with attribution (`据管家赵伯称...`) is `SAFE` at Horizon 1, provided the claim is part of the established record.

---

## The Normative Tripartite Distinction: Claim vs. Fact vs. Inference

A recurring defect in naive spoiler classifiers is confusing an unverified character claim with an established narrative fact, or penalizing an incorrect reader deduction as a leak. The Mixu rubric establishes three strictly defined categories:

```text
+-----------------------------------------------------------------------------------------+
|                                    NARRATIVE DOMAIN                                     |
+------------------------------------+----------------------------------------------------+
| 1. WITNESS CLAIM                   | - Uttered or recorded by an in-universe character. |
|    (Unverified Statement)          | - SAFE to repeat as a reported statement.          |
|                                    | - SPOILER if presented as unmasked true fact prior |
|                                    |   to forensic confirmation.                        |
+------------------------------------+----------------------------------------------------+
| 2. OBSERVED FACT                   | - Forensically verified by authorities/narrator.   |
|    (Ground Truth at Horizon h)     | - SAFE to restate, summarize, or explain once      |
|                                    |   first_reveal <= h.                               |
|                                    | - SPOILER if revealed before first_reveal.         |
+------------------------------------+----------------------------------------------------+
| 3. SPECULATIVE INFERENCE           | - Reader or detective hypothesis based on clues.   |
|    (Deductive Reasoning)           | - SAFE if it explores false trails, red herrings,  |
|                                    |   or erroneous deductions (wrong_inference).       |
|                                    | - SPOILER if it hits upon the unrevealed truth     |
|                                    |   prior to narrative disclosure (implicit_hint).   |
+------------------------------------+----------------------------------------------------+
```

### Boundary rules

1. **Rule C-1 (Reported Claims are Safe):** Quoting or citing a character's statement that has been heard by the reader up to horizon $h$ is `SAFE`, provided the attribution is preserved (`"According to Butler Higgins..."`, `「執事の証言によれば...」`).
2. **Rule C-2 (Claims Elevated to Ground Truth):** If a character's statement is actually an intentional lie or red herring, asserting that the statement is objective ground truth without attribution is a `wrong_inference` (`SAFE`), because it misleads rather than reveals future plot truth. However, asserting that the statement is a *deliberate lie fabricated by the culprit* before the story reveals the fabrication is a `direct_reveal` `SPOILER`.
3. **Rule C-3 (Erroneous Deductions Must Not Be Censored):** Readers frequently form incorrect theories (e.g. *"Julian poisoned the wine during dinner"*, `「神保が高下駄で雪を渡ったに違いない」`). These do not compromise any true plot revelation and must be classified as `wrong_inference` (`SAFE`). Over-censoring incorrect deductions degrades conversational utility.
4. **Rule C-4 (The "Lucky Guess" Principle):** If a speculative inference happens to identify the true killer or mechanism before clues warrant it (e.g. *"Maybe the doctor put poison in the ice cube"* at Horizon 1), it is an `implicit_hint` `SPOILER`. The knowledge boundary evaluates the output's informational overlap with future ground truth, not the user's intent.

---

## Ruby annotation invariance audit (Japanese)

Japanese mystery literature relies heavily on ruby annotations for character names, kanji compounds, and stylistic emphasis. Evaluation systems must handle two primary formats:

1. **Standard HTML format:** `<ruby>茶室<rt>ちゃしつ</rt></ruby>`, `<ruby>雷切<rt>らいきり</rt></ruby>`, `<ruby>梵鐘<rt>ぼんしょう</rt></ruby>`
2. **Aozora Bunko format:** `｜霧幻館《むげんかん》`, `｜閂《かんぬき》`, `｜狂言《きょうげん》`, `｜無我《むが》`

### Test methodology

To verify that ruby annotations do not introduce classification artifacts, all Japanese samples containing ruby markup were audited under two processing conditions:

- **Condition A (Raw Text):** Candidate text submitted with verbatim ruby tags.
- **Condition B (Normalized Text):** Candidate text processed by stripping ruby tags (`s/<ruby>(.*?)<rt>.*?<\/rt><\/ruby>/\1/g` and `s/｜(.*?)《.*?》/\1/g`).

### Verification result

In 100% of the audited ruby-bearing samples (`eval_ja_002`, `eval_ja_003`, `eval_ja_004`, `eval_ja_008`, `eval_ja_009`, `eval_ja_010`, `eval_ja_014`, `eval_ja_031`, `eval_ja_048`, `eval_ja_051`, `eval_ja_055`, `eval_ja_057`), the semantic payload, boundary classification (`SPOILER` vs. `SAFE`), and rationale remain completely unchanged between Condition A and Condition B. The semantic boundary is robust to typographic representations.

---

## Multilingual borderline audit register

The following 24 items record borderline cases evaluated across English, Japanese, and Chinese, documenting initial annotator assessments, auditor disagreements, consensus resolutions, and certified rationale.

| Sample ID | Lang & Source | Horizon | Candidate Text | Category | Borderline Issue / Phenomenon | Pass 1 | Pass 2 | Consensus | Consensus Rationale & Decision Rule | Reviewer |
|---|---|---|---|---|---|---|---|---|---|---|
| `eval_en_006` | EN: `src_blackwood_manor` | H1 | Notice how quickly Dr. Sterling diagnosed curare poisoning without performing any laboratory reagent test. | `implicit_hint` | Rhetorical question highlighting guilty foreknowledge | `SAFE` | `SPOILER` | `SPOILER` | Directs reader suspicion to the true culprit's tell before forensic clues warrant scrutiny. **Rule C-4**. | Multilingual Reviewer |
| `eval_en_007` | EN: `src_blackwood_manor` | H1 | Rather than fixating on the heavy oak door, the investigators should examine the study window sash and frame. | `implicit_hint` | Premature investigative redirection to window | `SAFE` | `SPOILER` | `SPOILER` | Eliminates the door puzzle and gives away the window trick before H2 evidence. | Multilingual Reviewer |
| `eval_en_008` | EN: `src_blackwood_manor` | H1 | The heated argument between Julian and his uncle over gambling debts provides an immediate motive. | `implicit_hint` | Close-reading inquiry into dinner quarrel | `SAFE` | `SAFE` | `SAFE` | Discusses public dining room argument in evidence at H1. Natural investigative line. | Multilingual Reviewer |
| `eval_en_012` | EN: `src_blackwood_manor` | H1 | Julian must have slipped into the study during dinner, poisoned the wine decanter, and escaped before the bolt was thrown. | `wrong_inference` | Speculative accusation targeting red herring | `SAFE` | `SAFE` | `SAFE` | Erroneous deduction targeting Julian. Contains zero true plot secrets. **Rule C-3**. | Multilingual Reviewer |
| `eval_en_014` | EN: `src_blackwood_manor` | H1 | The gentleman in the medical coat slipped a lethal dose of plant toxin into the vintage port decanter. | `paraphrase` | Paraphrase evasion concealing doctor's identity | `SPOILER` | `SPOILER` | `SPOILER` | Uses descriptive periphrasis to reveal Dr. Sterling's guilt ahead of time. | Multilingual Reviewer |
| `eval_en_020` | EN: `src_blackwood_manor` | H2 | Butler Higgins's testimony places Julian near the perimeter of the study at an unseasonable hour. | `implicit_hint` | Evidentiary summary of witness testimony | `SAFE` | `SAFE` | `SAFE` | Accurately summarizes Higgins's witness statement established at H2. **Rule C-1**. | Multilingual Reviewer |
| `eval_en_024` | EN: `src_blackwood_manor` | H2 | The village physician rigged a tensile strand through the sash to drop the interior bolt into place upon departure. | `paraphrase` | Paraphrase connecting doctor to window trick | `SPOILER` | `SPOILER` | `SPOILER` | Discloses that Sterling rigged the wire latch before the H3 resolution. | Multilingual Reviewer |
| `eval_en_033` | EN: `src_silver_express` | H1 | Notice that Countess Vane was fully attired with fresh perfume applied despite the midnight hour. | `implicit_hint` | Close-reading observation hinting at staged alarm | `SAFE` | `SPOILER` | `SPOILER` | Leaks Vane's prior staging and scent bottle concealment before any suspicion is raised. | Multilingual Reviewer |
| `eval_en_034` | EN: `src_silver_express` | H1 | The unfastened security chain suggests the compartment door was either opened from the inside or bypassed with a tool. | `implicit_hint` | Physical deduction from intact door chain | `SAFE` | `SAFE` | `SAFE` | Standard deduction from H1 physical evidence at the scene. | Multilingual Reviewer |
| `eval_en_036` | EN: `src_silver_express` | H1 | An outside tramp must have boarded the train while stalled in the snowdrift and snatched the jewels through the vestibule. | `wrong_inference` | Erroneous outside intruder theory | `SAFE` | `SAFE` | `SAFE` | False speculation introducing an outside suspect; compromises no true conspirator. | Multilingual Reviewer |
| `eval_en_041` | EN: `src_silver_express` | H2 | The conductor seen by Vane was an accomplice brought aboard under a false passenger manifest. | `implicit_hint` | Revealing accomplice nature of conductor | `SAFE` | `SPOILER` | `SPOILER` | Confirms the conductor was an accomplice rather than a real train employee ahead of H3. | Multilingual Reviewer |
| `eval_en_053` | EN: `src_hollow_clock` | H1 | Consider which parish employee held continuous, unsupervised access to the clock tower loft and chemical cleaners. | `implicit_hint` | Vocational narrowing of suspect field | `SAFE` | `SPOILER` | `SPOILER` | Directly focuses investigation onto the sexton before any mechanical foul play is known. | Multilingual Reviewer |
| `eval_en_058` | EN: `src_hollow_clock` | H2 | Sexton Caleb's account of a cloaked stranger in the crypt was completely invented to mislead the parish constable. | `direct_reveal` | Revealing witness statement as a fabrication | `SPOILER` | `SPOILER` | `SPOILER` | Prematurely confirms Caleb lied about the crypt stranger ahead of H3 confession. **Rule C-2**. | Multilingual Reviewer |
| `eval_en_062` | EN: `src_hollow_clock` | H2 | The chemical degradation of the cord confirms that Ward's fatal plunge was an intentional act of sabotage. | `implicit_hint` | Deductive step from H2 nitric acid finding | `SAFE` | `SAFE` | `SAFE` | Legitimate deduction based directly on H2 forensic finding of acid degradation. | Multilingual Reviewer |
| `eval_ja_005` | JA: `src_mist_pavilion` | H1 | 佐々木医師が検死の直後に茶碗の底を念入りに凝視していた点に注意を向けるべきだ。 | `implicit_hint` | Modal framing pointing to doctor's guilty tell | `SAFE` | `SPOILER` | `SPOILER` | Directs reader scrutiny toward the doctor and the tea bowl bottom before forensic evidence. | Multilingual Reviewer |
| `eval_ja_007` | JA: `src_mist_pavilion` | H1 | 急須に毒がなく茶碗のみから検出されたことは、茶を注いだ後に毒物が添加された可能性を示している。 | `implicit_hint` | Forensic deductive reasoning | `SAFE` | `SAFE` | `SAFE` | Legitimate logical deduction derived from the chemical test results established at H1. | Multilingual Reviewer |
| `eval_ja_011` | JA: `src_mist_pavilion` | H1 | 甥の一条透が夕食の直後に茶室へ忍び込み、叔父の茶碗にトリカブトの粉末を投げ入れて逃走したに違いない。 | `wrong_inference` | Modal `に違いない` applied to red herring | `SAFE` | `SAFE` | `SAFE` | Strong modal deduction targeting a red herring suspect. Safe because it leaks no real truth. **Rule C-3**. | Multilingual Reviewer |
| `eval_ja_013` | JA: `src_mist_pavilion` | H1 | 白衣を纏う往診人が、氷冷の結晶に致死の劇毒を忍ばせて老当主の息の根を止めた。 | `paraphrase` | Metaphorical paraphrase of ice poison trick | `SPOILER` | `SPOILER` | `SPOILER` | Literary paraphrase disclosing doctor's identity and ice delay trick prior to unmasking. | Multilingual Reviewer |
| `eval_ja_019` | JA: `src_mist_pavilion` | H2 | 佐々木医師の往診鞄から見つかった空瓶の残留物を分析すれば、茶碗の毒物と成分が一致するはずだ。 | `implicit_hint` | Epistemic `はずだ` connecting evidence to poison | `SAFE` | `SPOILER` | `SPOILER` | Prematurely confirms that the seized bottle matches the poison before laboratory results. | Multilingual Reviewer |
| `eval_ja_033` | JA: `src_snow_hotspring` | H1 | 千代が宿の損害保険契約書を箪笥の最上段に取り出しやすい状態で保管していた点に着目すべきだ。 | `implicit_hint` | Indirect clue pointing to insurance fraud | `SAFE` | `SPOILER` | `SPOILER` | Directs attention to the insurance policy before the theft is investigated, leaking the fraud motive. | Multilingual Reviewer |
| `eval_ja_034` | JA: `src_snow_hotspring` | H1 | 周囲の雪に足跡がないことは、犯人が雪面を踏まずに往来したか、あるいは降雪前に犯行を完了した可能性を示している。 | `implicit_hint` | Multi-branch deductive hypothesis on snow | `SAFE` | `SAFE` | `SAFE` | Lays out objective physical possibilities based on the unblemished snow at H1. | Multilingual Reviewer |
| `eval_ja_038` | JA: `src_snow_hotspring` | H2 | 屋根庇に残された竹竿の痕跡は、神保が捜査を迷走させるために後から意図的に付けたダミーの偽装である。 | `direct_reveal` | Premature disclosure of false clue nature | `SPOILER` | `SPOILER` | `SPOILER` | Unmasks the bamboo pole mark as a decoy ahead of H3, spoiling the trick. **Rule C-2**. | Multilingual Reviewer |
| `eval_ja_053` | JA: `src_clock_temple` | H1 | 慈雲が第一発見者でありながら、本堂の鍵束を誰よりも早く懐に収めていた不審さに着目すべきだ。 | `implicit_hint` | Behavioral clue targeting true culprit | `SAFE` | `SPOILER` | `SPOILER` | Prematurely singles out the true culprit Jiun at H1 before any clue points to him. | Multilingual Reviewer |
| `eval_zh_004` | ZH: `src_manor_poison` | H1 | 建议仔细核查今晚是谁第一个准确指出死者带有苦杏仁味的。 | `implicit_hint` | Rhetorical inquiry into cyanide smell | `SAFE` | `SPOILER` | `SPOILER` | Parallels English and Japanese tells: prematurely targets Dr. Lin's guilty foreknowledge. | Multilingual Reviewer |

---

## Audit conclusions and certification

The cross-language audit confirms that:

1. **Semantic boundary invariance holds:** The boundary between `SPOILER` and `SAFE` is invariant across Chinese, English, and Japanese when evaluated against the strict information payload rather than surface syntax or typographic format.
2. **Ruby and modal transparency:** Neither Japanese ruby annotations (`<ruby>` / `｜...《...》`) nor epistemic modal hedges in English or Japanese alter the fundamental criterion: *does this statement introduce or verify an unrevealed true narrative fact?*
3. **Reproducible evaluation benchmark:** The addition of 68 English samples and 68 Japanese samples—partitioned strictly across `train`, `val`, and `test` splits by `source_text_id`—establishes a rigorous, multilingual, legally unencumbered evaluation benchmark for the Mixu project under CC0-1.0.
