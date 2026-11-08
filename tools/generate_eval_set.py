#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the synthetic Chinese spoiler decision evaluation set.

Outputs `fixtures/eval/chinese-spoiler-eval/eval-set.json` with 220 samples
partitioned strictly across train/val/test splits by `source_text_id`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.eval_data_alchemist import get_alchemist_samples
from tools.eval_data_clocktower import get_clocktower_samples
from tools.eval_data_gallery import get_gallery_samples
from tools.eval_data_manor import get_manor_samples
from tools.eval_data_train import get_midnight_train_samples

OUTPUT_DIR = ROOT / "fixtures" / "eval" / "chinese-spoiler-eval"
OUTPUT_FILE = OUTPUT_DIR / "eval-set.json"

SOURCE_TEXTS = [
    {
        "id": "src_manor_poison",
        "title": "海雾庄园晚宴案",
        "description": "老庄主楚成远七十大寿晚宴后在密闭吸烟室饮茶中毒身亡，涉及糖罐剧毒、遗嘱信托篡改与医生赌债。",
        "split": "train",
        "total_horizons": 4,
    },
    {
        "id": "src_gallery_theft",
        "title": "月影画廊失窃案",
        "description": "珍宝展展柜玻璃完好而'海之眼'蓝宝石胸针失窃，涉及假宝石调包、易容黑纱女士与内部骗保阴谋。",
        "split": "train",
        "total_horizons": 3,
    },
    {
        "id": "src_clocktower_fall",
        "title": "旧钟楼暗影坠亡案",
        "description": "暴雨夜市政钟楼设计师顾明自顶层齿轮平台坠亡，涉及预割麻绳、特种润滑油与孪生兄弟身份替换。",
        "split": "train",
        "total_horizons": 3,
    },
    {
        "id": "src_midnight_train",
        "title": "午夜雪原快车案",
        "description": "暴风雪迫停的快车包厢内客商被麻醉且证券被盗，涉及钓鱼线暗锁密室、列车长假指套伪装与巨盗潜伏。",
        "split": "val",
        "total_horizons": 3,
    },
    {
        "id": "src_alchemist_chamber",
        "title": "秘境炼金密室案",
        "description": "封闭石室内炼金演示突发白烟与长袍遗留，学者凭空蒸发，涉及烟道配重逃生机关、易容地窖杂工与假死逃债。",
        "split": "test",
        "total_horizons": 3,
    },
]


def generate() -> None:
    samples = []
    samples.extend(get_manor_samples())
    samples.extend(get_gallery_samples())
    samples.extend(get_clocktower_samples())
    samples.extend(get_midnight_train_samples())
    samples.extend(get_alchemist_samples())

    eval_set = {
        "$schema": "../../schema/eval-set.schema.json",
        "name": "chinese-spoiler-eval",
        "version": "1.0.0",
        "description": "A held-out evaluation set for spoiler decisions on Chinese synthetic mystery micro-narratives.",
        "content_basis": "SYNTHETIC_ORIGINAL",
        "rights_note": "Dedicated to the public domain under CC0-1.0. 100% synthetic text authored for Mixu.",
        "source_texts": SOURCE_TEXTS,
        "samples": samples,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(eval_set, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Generated {len(samples)} samples to {OUTPUT_FILE}")


if __name__ == "__main__":
    generate()
