#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the synthetic English and Japanese spoiler decision evaluation sets.

Outputs:
- `fixtures/eval/english-spoiler-eval/eval-set.json` (68 samples, train/val/test)
- `fixtures/eval/japanese-spoiler-eval/eval-set.json` (68 samples, train/val/test)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.eval_data_en_blackwood import get_blackwood_samples
from tools.eval_data_en_clock import get_hollow_clock_samples
from tools.eval_data_en_silver import get_silver_express_samples
from tools.eval_data_ja_mist import get_mist_pavilion_samples
from tools.eval_data_ja_snow import get_snow_hotspring_samples
from tools.eval_data_ja_temple import get_clock_temple_samples

EN_DIR = ROOT / "fixtures" / "eval" / "english-spoiler-eval"
JA_DIR = ROOT / "fixtures" / "eval" / "japanese-spoiler-eval"

EN_SOURCE_TEXTS = [
    {
        "id": "src_blackwood_manor",
        "title": "The Cipher of Blackwood Manor",
        "description": "Lord Blackwood is poisoned by curare inside his locked study; the safe will is replaced by a coded parchment, pointing to an unacknowledged heir.",
        "split": "train",
        "total_horizons": 3,
    },
    {
        "id": "src_silver_express",
        "title": "The Vanishing Emerald of the Silver Express",
        "description": "A blizzard halts an express train across the moors; Lady Catherine's emerald necklace vanishes from a locked sleeper compartment in an insurance conspiracy.",
        "split": "val",
        "total_horizons": 3,
    },
    {
        "id": "src_hollow_clock",
        "title": "The Riddle of the Hollow Clock",
        "description": "An antiquarian falls to his death from St. Jude's bell tower; the escapement mechanism was corroded with acid and jammed by an ivory chess piece.",
        "split": "test",
        "total_horizons": 3,
    },
]

JA_SOURCE_TEXTS = [
    {
        "id": "src_mist_pavilion",
        "title": "霧幻館の双重密室",
        "description": "孤島の洋館の茶室で旧華族の一条当主が毒殺される。急須に毒はなく茶碗のみ陽性、格子窓の糸痕と溶けた毒氷による二重密室殺人。",
        "split": "train",
        "total_horizons": 3,
    },
    {
        "id": "src_snow_hotspring",
        "title": "白雪楼の消えた短刀",
        "description": "雪崩で孤立した温泉宿の離れから家宝の短刀が忽然と消失する。深雪に足跡なき密室と、女将と画商が共謀した狂言保険金詐欺。",
        "split": "val",
        "total_horizons": 3,
    },
    {
        "id": "src_clock_temple",
        "title": "時鐘寺の傀儡鐘楼",
        "description": "古刹の鐘楼で大鐘が落下し住職が圧死する。自動撞木の歯車に仕組まれた岩塩融解時限装置と、托鉢僧の潜入監察活動。",
        "split": "test",
        "total_horizons": 3,
    },
]


def generate_english() -> None:
    samples = []
    samples.extend(get_blackwood_samples())
    samples.extend(get_silver_express_samples())
    samples.extend(get_hollow_clock_samples())

    eval_set = {
        "$schema": "../../schema/eval-set.schema.json",
        "name": "english-spoiler-eval",
        "version": "1.0.0",
        "description": "A held-out evaluation set for spoiler decisions on English synthetic mystery micro-narratives.",
        "content_basis": "SYNTHETIC_ORIGINAL",
        "rights_note": "Dedicated to the public domain under CC0-1.0. 100% synthetic text authored for Mixu.",
        "source_texts": EN_SOURCE_TEXTS,
        "samples": samples,
    }

    EN_DIR.mkdir(parents=True, exist_ok=True)
    out_file = EN_DIR / "eval-set.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(eval_set, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Generated {len(samples)} English samples to {out_file}")


def generate_japanese() -> None:
    samples = []
    samples.extend(get_mist_pavilion_samples())
    samples.extend(get_snow_hotspring_samples())
    samples.extend(get_clock_temple_samples())

    eval_set = {
        "$schema": "../../schema/eval-set.schema.json",
        "name": "japanese-spoiler-eval",
        "version": "1.0.0",
        "description": "A held-out evaluation set for spoiler decisions on Japanese synthetic mystery micro-narratives.",
        "content_basis": "SYNTHETIC_ORIGINAL",
        "rights_note": "Dedicated to the public domain under CC0-1.0. 100% synthetic text authored for Mixu.",
        "source_texts": JA_SOURCE_TEXTS,
        "samples": samples,
    }

    JA_DIR.mkdir(parents=True, exist_ok=True)
    out_file = JA_DIR / "eval-set.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(eval_set, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Generated {len(samples)} Japanese samples to {out_file}")


def main() -> None:
    generate_english()
    generate_japanese()


if __name__ == "__main__":
    main()
