# SPDX-License-Identifier: Apache-2.0
"""Evaluation data for src_midnight_train (35 samples, val split)."""

SOURCE_ID = "src_midnight_train"
SPLIT = "val"

H1_SUMMARY = "风雪迫停快车，3号包厢客商何老板遇袭昏迷且证券被盗，门闩从内反锁形成密室，车窗结霜完好，茶杯中残留强效安眠药。"
H2_SUMMARY = "老郑在门框上方通风百叶窗缝隙提取到极细尼龙钓鱼线，茶水间垃圾桶发现安眠药包装，乘客白先生称案发前见制服人员走过。"
H3_SUMMARY = "老郑在机车煤水舱起获藏有证券的手套，并查获严峰更衣柜内的假指套与线轴；严峰右手食指残缺的通缉巨盗'铁指老齐'身份大白，认罪伏法。"


def get_midnight_train_samples() -> list[dict]:
    raw = [
        # --- Horizon 1 (16 samples) ---
        # direct_reveal
        (
            "eval_zh_151",
            1,
            H1_SUMMARY,
            "盗窃证券并伪造反锁密室的是列车长严峰。",
            "direct_reveal",
            "SPOILER",
            "在第1阶段直接指认列车长严峰为真凶，严重剧透。",
        ),
        (
            "eval_zh_152",
            1,
            H1_SUMMARY,
            "反锁的门闩是用极细的尼龙线穿过通风格栅从门外拉动插上的。",
            "direct_reveal",
            "SPOILER",
            "提前揭示第2阶段才发现的钓鱼线反锁密室手法。",
        ),
        (
            "eval_zh_153",
            1,
            H1_SUMMARY,
            "失窃的无记名证券被凶手藏在了车头蒸汽机车的煤水舱铁箱里。",
            "direct_reveal",
            "SPOILER",
            "直接泄露第3阶段搜查起赃地点。",
        ),
        (
            "eval_zh_154",
            1,
            H1_SUMMARY,
            "被害人何老板是在3号包厢内饮用含有安眠成分的洋甘菊茶后陷入昏睡的。",
            "direct_reveal",
            "SAFE",
            "第1阶段现场调查已确认的受害与中毒事实，安全。",
        ),
        (
            "eval_zh_155",
            1,
            H1_SUMMARY,
            "案发时列车因雪崩障碍被迫临时停靠在深山雪原轨道上。",
            "direct_reveal",
            "SAFE",
            "第1阶段故事环境背景陈述，安全。",
        ),
        # implicit_hint
        (
            "eval_zh_156",
            1,
            H1_SUMMARY,
            "留意列车长严峰戴手套的方式，他似乎总在掩饰右手手指的异常。",
            "implicit_hint",
            "SPOILER",
            "提前引导读者注意假指套特征，属于隐性剧透通缉犯身份。",
        ),
        (
            "eval_zh_157",
            1,
            H1_SUMMARY,
            "门上方的百叶通风口距离门闩很近，可能存在从外部伸入细物操作的空间。",
            "implicit_hint",
            "SPOILER",
            "在第1阶段精准提示通风格栅的作案可能，越过第2阶段物证发现。",
        ),
        (
            "eval_zh_158",
            1,
            H1_SUMMARY,
            "车窗外侧结霜完好，表明凶手极大概率没有翻窗逃至车外雪地。",
            "implicit_hint",
            "SAFE",
            "根据第1阶段公开的车窗结霜痕迹进行顺向逻辑排查，安全。",
        ),
        (
            "eval_zh_159",
            1,
            H1_SUMMARY,
            "茶水是由随车列车员送入的，需要核对送茶的具体时间与经手人员。",
            "implicit_hint",
            "SAFE",
            "基于已知供水流程的常规侦查思路，安全。",
        ),
        # alias_identity
        (
            "eval_zh_160",
            1,
            H1_SUMMARY,
            "这位列车长严峰其实就是数年前在平原多省作案的通缉巨盗'铁指老齐'。",
            "alias_identity",
            "SPOILER",
            "直接将列车长与通缉犯'铁指老齐'进行身份绑定，属于重大剧透。",
        ),
        (
            "eval_zh_161",
            1,
            H1_SUMMARY,
            "严峰是这列快车的现任列车长，具备全列车厢的巡视通行权限。",
            "alias_identity",
            "SAFE",
            "陈述严峰公开的列车职务与权限，安全。",
        ),
        # wrong_inference
        (
            "eval_zh_162",
            1,
            H1_SUMMARY,
            "戴眼镜的学者白先生形迹可疑，肯定是他为了抢夺研究资金在茶里下了安眠药。",
            "wrong_inference",
            "SAFE",
            "对乘客白先生的错误怀疑（红鲱鱼），安全。",
        ),
        (
            "eval_zh_163",
            1,
            H1_SUMMARY,
            "何老板自己为了骗取商业保险自导自演了昏迷，证券还在他自己的贴身衣物里。",
            "wrong_inference",
            "SAFE",
            "针对受害者的错误骗保假说，安全。",
        ),
        # benign_explanation
        (
            "eval_zh_164",
            1,
            H1_SUMMARY,
            "车厢内的黄铜横插闩只有从内侧平行推移才能滑入闭锁咬合卡槽。",
            "benign_explanation",
            "SAFE",
            "对包厢门闩物理构造的客观解释，安全。",
        ),
        # paraphrase
        (
            "eval_zh_165",
            1,
            H1_SUMMARY,
            "那位掌握全车钥匙的长官利用细韧透明丝线牵引门闩构筑了铜墙铁壁般的假象，巨款已被转移到锅炉煤堆深处。",
            "paraphrase",
            "SPOILER",
            "文学化转述严峰使用钓鱼线机关与煤水舱藏赃的真相，构成剧透。",
        ),
        (
            "eval_zh_166",
            1,
            H1_SUMMARY,
            "门顶百叶缝隙穿过的无形引线，正是将门栓悄然送入锁扣的真正无形之手。",
            "paraphrase",
            "SPOILER",
            "转述钓鱼线密室机关手法，越过第2阶段发现。",
        ),
        # --- Horizon 2 (11 samples) ---
        # direct_reveal
        (
            "eval_zh_167",
            2,
            H2_SUMMARY,
            "严峰右手的假指套里隐藏着他作为通缉犯'铁指老齐'的断指特征。",
            "direct_reveal",
            "SPOILER",
            "直接泄露第3阶段才搜查揭穿的假指套物证。",
        ),
        (
            "eval_zh_168",
            2,
            H2_SUMMARY,
            "证券就藏在车头机车底部的煤水舱黑铁工具箱里。",
            "direct_reveal",
            "SPOILER",
            "直接透露起赃的具体位置，破坏搜查悬念。",
        ),
        (
            "eval_zh_169",
            2,
            H2_SUMMARY,
            "百叶窗缝隙中提取到的透明细线被证实为高强度聚乙烯钓鱼线。",
            "direct_reveal",
            "SAFE",
            "第2阶段警方现场取证公布的物证事实，安全。",
        ),
        (
            "eval_zh_170",
            2,
            H2_SUMMARY,
            "茶水间垃圾桶里清理出了微量安眠药粉末的蜡纸包装残片。",
            "direct_reveal",
            "SAFE",
            "第2阶段搜查公开的已知物证，安全。",
        ),
        # implicit_hint
        (
            "eval_zh_171",
            2,
            H2_SUMMARY,
            "快车上唯一的业余钓鱼爱好者正是喜欢在停运期间钓鱼的严峰车长。",
            "implicit_hint",
            "SPOILER",
            "利用爱好特征提前锁定严峰，越过第3阶段更衣柜线轴物证。",
        ),
        (
            "eval_zh_172",
            2,
            H2_SUMMARY,
            "白先生看到的制服人员体态特征，应当与车上所有当班员工进行交叉比对。",
            "implicit_hint",
            "SAFE",
            "根据第2阶段白先生证词进行的合理侦查排查建议，安全。",
        ),
        # alias_identity
        (
            "eval_zh_173",
            2,
            H2_SUMMARY,
            "警方通缉令上的'铁指老齐'正是当班列车长严峰。",
            "alias_identity",
            "SPOILER",
            "在第2阶段直接曝光严峰与老齐的同一身份，严重剧透。",
        ),
        (
            "eval_zh_174",
            2,
            H2_SUMMARY,
            "白先生是北方大学的地理学者，此行前往边陲考察雪原气候。",
            "alias_identity",
            "SAFE",
            "介绍乘客白先生的身份背景，安全。",
        ),
        # wrong_inference
        (
            "eval_zh_175",
            2,
            H2_SUMMARY,
            "肯定是乘务员小孙在茶水间冲泡茶叶时被收买下了药，他是唯一的下毒者。",
            "wrong_inference",
            "SAFE",
            "针对小孙的错误猜测，安全。",
        ),
        # benign_explanation
        (
            "eval_zh_176",
            2,
            H2_SUMMARY,
            "高强度尼龙钓鱼线具有极高的抗拉强度，且直径纤细，容易穿过狭窄通风叶片。",
            "benign_explanation",
            "SAFE",
            "对提取物证特性的科普说明，安全。",
        ),
        # paraphrase
        (
            "eval_zh_177",
            2,
            H2_SUMMARY,
            "那份失落的财富正静静躺在机车熊熊炉膛后方的幽暗煤仓中，等待风雪停歇后被取走。",
            "paraphrase",
            "SPOILER",
            "转述煤水舱藏匿巨额证券的事实，构成剧透。",
        ),
        # --- Horizon 3 (8 samples) ---
        # direct_reveal
        (
            "eval_zh_178",
            3,
            H3_SUMMARY,
            "乘警老郑在煤水舱起获证券手套并缴获假指套，严峰彻底认罪伏法。",
            "direct_reveal",
            "SAFE",
            "第3阶段官方搜查起赃与审讯终局事实，公开安全。",
        ),
        (
            "eval_zh_179",
            3,
            H3_SUMMARY,
            "严峰承认利用通风格栅钓鱼线反锁包厢，全案告破。",
            "direct_reveal",
            "SAFE",
            "结案口供与事实全盘总结，安全。",
        ),
        # implicit_hint
        (
            "eval_zh_180",
            3,
            H3_SUMMARY,
            "严峰利用风雪停车造成的混乱与列车长巡查便利实施了精密作案。",
            "implicit_hint",
            "SAFE",
            "结案后对作案环境与手法的逻辑评述，安全。",
        ),
        # alias_identity
        (
            "eval_zh_181",
            3,
            H3_SUMMARY,
            "列车长严峰已被证实就是数省通缉的惯窃巨盗'铁指老齐'。",
            "alias_identity",
            "SAFE",
            "官方结案确认的逃犯身份合一事实，安全。",
        ),
        (
            "eval_zh_182",
            3,
            H3_SUMMARY,
            "右手食指第一节缺损正是识别'铁指老齐'的决定性生理特征。",
            "alias_identity",
            "SAFE",
            "官方验伤公布的身份确认特征，安全。",
        ),
        # wrong_inference
        (
            "eval_zh_183",
            3,
            H3_SUMMARY,
            "或许严峰只是替车上更有权势的旅客保管赃物，并没有真正参与谋划。",
            "wrong_inference",
            "SAFE",
            "结案后的读者主观发散，不剧透未知事实，安全。",
        ),
        # benign_explanation
        (
            "eval_zh_184",
            3,
            H3_SUMMARY,
            "蒸汽机车煤水舱位于车头紧后方，用于储备机车燃烧所需的硬煤与冷却用水。",
            "benign_explanation",
            "SAFE",
            "对机车结构的常规机械工程解释，安全。",
        ),
        # paraphrase
        (
            "eval_zh_185",
            3,
            H3_SUMMARY,
            "隐姓埋名的断指大盗在煤灰阴暗处藏匿的财宝终被起获，雪原飞车上的密室魔术彻底落幕。",
            "paraphrase",
            "SAFE",
            "终局阶段对全案事实的文学化陈述，属于已知事实的安全总结。",
        ),
    ]

    samples = []
    for item in raw:
        s_id, h_ord, state_sum, cand_text, cat, label, rationale = item
        samples.append(
            {
                "id": s_id,
                "source_text_id": SOURCE_ID,
                "horizon_ordinal": h_ord,
                "reading_state_summary": state_sum,
                "candidate_text": cand_text,
                "category": cat,
                "label": label,
                "rationale": rationale,
                "split": SPLIT,
            }
        )
    return samples
