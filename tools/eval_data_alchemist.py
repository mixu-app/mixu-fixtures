# SPDX-License-Identifier: Apache-2.0
"""Evaluation data for src_alchemist_chamber (35 samples, test split)."""

SOURCE_ID = "src_alchemist_chamber"
SPLIT = "test"

H1_SUMMARY = "封闭石室内演示炼金术时突起白烟浓雾，待烟散尽学者冯泊舟凭空消失，仅剩天鹅绒长袍与硫磺粉；石室独门外锁，铁栅窗完好无损。"
H2_SUMMARY = "徐峰在壁炉烟道内发现新鲜的人工滑降刮痕，书架暗处查出机械配重滑轮；韩会长证实冯泊舟近期面临三笔高额破产催债。"
H3_SUMMARY = "徐峰直捣古堡地窖暗室，当场抓获洗脱假胡须伪装的'哑巴锅炉工'冯泊舟；假死逃债真相大白，苏青退还科研款，全案告破。"


def get_alchemist_samples() -> list[dict]:
    raw = [
        # --- Horizon 1 (16 samples) ---
        # direct_reveal
        (
            "eval_zh_186",
            1,
            H1_SUMMARY,
            "冯泊舟根本没有死亡或消失，他只是顺着壁炉烟道暗槽逃到了古堡地窖。",
            "direct_reveal",
            "SPOILER",
            "在第1阶段直接揭穿整起密室消失案的核心逃生路线与假死真相，严重剧透。",
        ),
        (
            "eval_zh_187",
            1,
            H1_SUMMARY,
            "地窖里那个不说话的哑巴锅炉工其实就是冯泊舟假扮的。",
            "direct_reveal",
            "SPOILER",
            "直接泄露终局第3阶段才揭晓的锅炉工易容伪装身份。",
        ),
        (
            "eval_zh_188",
            1,
            H1_SUMMARY,
            "冯泊舟自导自演凭空蒸发是为了躲避即将到期的三张巨额破产借据。",
            "direct_reveal",
            "SPOILER",
            "泄露第2阶段才公布的破产催收与逃债作案动机。",
        ),
        (
            "eval_zh_189",
            1,
            H1_SUMMARY,
            "白烟散去后石室中央留下了冯泊舟平时穿着的天鹅绒长袍与刺鼻的硫磺粉末。",
            "direct_reveal",
            "SAFE",
            "第1阶段现场第一目击公开的客观物质遗留，安全。",
        ),
        (
            "eval_zh_190",
            1,
            H1_SUMMARY,
            "演示石室唯一的厚木门在演示期间被赞助人韩会长从外部挂锁锁闭。",
            "direct_reveal",
            "SAFE",
            "第1阶段公开的密室锁闭状态说明，安全。",
        ),
        # implicit_hint
        (
            "eval_zh_191",
            1,
            H1_SUMMARY,
            "壁炉内的烟灰如果很厚，往往可以作为天然缓冲物掩盖攀爬或坠落的声响。",
            "implicit_hint",
            "SPOILER",
            "精准暗示壁炉烟道这一第2阶段才发现的逃生出口，越过当前搜查进度。",
        ),
        (
            "eval_zh_192",
            1,
            H1_SUMMARY,
            "演示所用的磷光闪光药剂配方需要化学专业人员提供，助手苏青具备调配能力。",
            "implicit_hint",
            "SPOILER",
            "提前暗示侄女苏青在药剂上的共谋协助，属于隐性剧透。",
        ),
        (
            "eval_zh_193",
            1,
            H1_SUMMARY,
            "石室四周的铁栅窗镶嵌牢固，成人的头颅骨骼无法穿过栅栏间隙。",
            "implicit_hint",
            "SAFE",
            "根据第1阶段公开的铁栅窗构造进行的常规物理排除，安全。",
        ),
        (
            "eval_zh_194",
            1,
            H1_SUMMARY,
            "白烟突发说明现场发生了剧烈的发烟化学反应，应注意反应物来源。",
            "implicit_hint",
            "SAFE",
            "对现场发烟现象的常理技术分析，安全。",
        ),
        # alias_identity
        (
            "eval_zh_195",
            1,
            H1_SUMMARY,
            "古堡底层的哑巴锅炉工就是学者冯泊舟本人。",
            "alias_identity",
            "SPOILER",
            "直接将地窖锅炉工与冯泊舟进行身份合并，提前曝光终局大反转。",
        ),
        (
            "eval_zh_196",
            1,
            H1_SUMMARY,
            "冯泊舟是这处山间古堡的主人，多年潜心研究矿物炼金与化学提纯。",
            "alias_identity",
            "SAFE",
            "陈述冯泊舟的公开学者身份与背景，安全。",
        ),
        # wrong_inference
        (
            "eval_zh_197",
            1,
            H1_SUMMARY,
            "冯泊舟一定是掌握了真正的古代炼金奥秘，将肉身升华为高能气体融入了以太之中。",
            "wrong_inference",
            "SAFE",
            "符合表象怪力乱神的读者错误空想，无真实事实泄露，安全。",
        ),
        (
            "eval_zh_198",
            1,
            H1_SUMMARY,
            "门外的韩会长肯定在挂锁时暗中在锁眼里灌注了腐蚀酸，把冯泊舟化成了血水。",
            "wrong_inference",
            "SAFE",
            "针对韩会长的荒诞错误指控（红鲱鱼），安全。",
        ),
        # benign_explanation
        (
            "eval_zh_199",
            1,
            H1_SUMMARY,
            "硫磺粉末燃烧会产生大量具有刺激性气味的二氧化硫气体，并伴有淡蓝色火焰与浓烟。",
            "benign_explanation",
            "SAFE",
            "对现场残留硫磺粉理化性质的科学普及，安全。",
        ),
        # paraphrase
        (
            "eval_zh_200",
            1,
            H1_SUMMARY,
            "那位所谓的隐士学者借着闪光烟雾掩护从烟囱夹壁滑入地下，化身为浑身煤灰的哑仆以此赖掉千万账目。",
            "paraphrase",
            "SPOILER",
            "文学化转述烟道滑降、地窖哑仆伪装及逃债动机，构成实质剧透。",
        ),
        (
            "eval_zh_201",
            1,
            H1_SUMMARY,
            "壁炉后方沉重的石砖其实暗藏着连接钢缆的机械平衡块，只需轻踩踏板便会开启暗门。",
            "paraphrase",
            "SPOILER",
            "提前揭穿第2阶段才发现的配重机关工作原理。",
        ),
        # --- Horizon 2 (11 samples) ---
        # direct_reveal
        (
            "eval_zh_202",
            2,
            H2_SUMMARY,
            "冯泊舟此刻正藏在古堡地下煤仓附近，剃掉了络腮胡装作聋哑工人。",
            "direct_reveal",
            "SPOILER",
            "直接指出第3阶段搜查才能揭露的藏匿地点与外貌改变特征。",
        ),
        (
            "eval_zh_203",
            2,
            H2_SUMMARY,
            "真正的赞助款项已经被苏青转移到了山下钱庄的私密户头。",
            "direct_reveal",
            "SPOILER",
            "泄露第3阶段结案时苏青交代并交出的赃款去向。",
        ),
        (
            "eval_zh_204",
            2,
            H2_SUMMARY,
            "徐峰勘查证实壁炉烟道内留有近期人体顺绳索滑降擦蹭出的清晰刮痕。",
            "direct_reveal",
            "SAFE",
            "第2阶段现场勘验公布的官方物证发现，安全。",
        ),
        (
            "eval_zh_205",
            2,
            H2_SUMMARY,
            "韩会长承认冯泊舟近期收到三张破产催告函，面临巨额财务清偿危机。",
            "direct_reveal",
            "SAFE",
            "第2阶段当事人证词披露的已知债务背景，安全。",
        ),
        # implicit_hint
        (
            "eval_zh_206",
            2,
            H2_SUMMARY,
            "古堡地窖最近新来的那个从不开口说话的运煤伙计，体型与冯泊舟颇为相似。",
            "implicit_hint",
            "SPOILER",
            "在第2阶段直接引导关注地窖哑巴锅炉工，越过自然线索发现过程。",
        ),
        (
            "eval_zh_207",
            2,
            H2_SUMMARY,
            "配重滑轮系统需要定期上油保养，唐师傅作为古堡机械师应能指出其走向。",
            "implicit_hint",
            "SAFE",
            "结合第2阶段发现的滑轮机关邀请机械师协助侦查，属于合乎逻辑的推进，安全。",
        ),
        # alias_identity
        (
            "eval_zh_208",
            2,
            H2_SUMMARY,
            "地下锅炉房里的聋哑工人就是逃债假死的冯泊舟。",
            "alias_identity",
            "SPOILER",
            "在第2阶段强行合并锅炉工与冯泊舟的身份，构成严重剧透。",
        ),
        (
            "eval_zh_209",
            2,
            H2_SUMMARY,
            "唐师傅是受聘维护古堡升降索道与钟表管道的老机械工匠。",
            "alias_identity",
            "SAFE",
            "介绍唐师傅的职业与工作范围，安全。",
        ),
        # wrong_inference
        (
            "eval_zh_210",
            2,
            H2_SUMMARY,
            "滑轮既然是唐师傅装的，肯定是唐师傅协助韩会长把冯泊舟吊出烟囱杀人灭口了。",
            "wrong_inference",
            "SAFE",
            "基于滑轮产生的错误阴谋论假说，安全。",
        ),
        # benign_explanation
        (
            "eval_zh_211",
            2,
            H2_SUMMARY,
            "机械配重滑轮通过平衡重锤能够显著降低垂直提升或下放重物所需的拉力。",
            "benign_explanation",
            "SAFE",
            "对配重滑轮力学常识的科普说明，安全。",
        ),
        # paraphrase
        (
            "eval_zh_212",
            2,
            H2_SUMMARY,
            "那位尊贵的主人脱下锦衣华服，正满脸油污地守在地底炉膛旁等待风波平息。",
            "paraphrase",
            "SPOILER",
            "文学化转述冯泊舟在地底假扮煤工的隐匿现状，构成剧透。",
        ),
        # --- Horizon 3 (8 samples) ---
        # direct_reveal
        (
            "eval_zh_213",
            3,
            H3_SUMMARY,
            "徐峰在地窖暗室抓获卸除伪装的冯泊舟，证实密室消失系借机关假死逃债，全案告破。",
            "direct_reveal",
            "SAFE",
            "第3阶段官方侦破终局事实，全盘公开安全。",
        ),
        (
            "eval_zh_214",
            3,
            H3_SUMMARY,
            "苏青认错并交出了私下藏匿的科研赞助公款。",
            "direct_reveal",
            "SAFE",
            "官方结案事实复述，安全。",
        ),
        # implicit_hint
        (
            "eval_zh_215",
            3,
            H3_SUMMARY,
            "这起所谓的密室超自然奇观本质上是利用了古堡旧有烟道与机械工程的物理诈术。",
            "implicit_hint",
            "SAFE",
            "结案后对诡计物理本质的总结评价，安全。",
        ),
        # alias_identity
        (
            "eval_zh_216",
            3,
            H3_SUMMARY,
            "地窖里的'哑巴锅炉工'确系冯泊舟剃须涂灰后的伪装身份，两者为同一个人。",
            "alias_identity",
            "SAFE",
            "官方结案定性的同一性身份，安全。",
        ),
        (
            "eval_zh_217",
            3,
            H3_SUMMARY,
            "苏青是冯泊舟的亲侄女兼实验助手，已对共谋伪造烟雾供认不讳。",
            "alias_identity",
            "SAFE",
            "结案审讯公开的亲属与共犯关系，安全。",
        ),
        # wrong_inference
        (
            "eval_zh_218",
            3,
            H3_SUMMARY,
            "地窖里抓到的可能只是替身，真正的炼金大师也许早就飞升远去了。",
            "wrong_inference",
            "SAFE",
            "结案后的荒谬调侃，安全。",
        ),
        # benign_explanation
        (
            "eval_zh_219",
            3,
            H3_SUMMARY,
            "假死欺诈触犯合同诈骗与妨害司法相关法规，涉案人员已被依法移交司法机关。",
            "benign_explanation",
            "SAFE",
            "对结案后续司法处置的程序性说明，安全。",
        ),
        # paraphrase
        (
            "eval_zh_220",
            3,
            H3_SUMMARY,
            "伴随浓烟消散的幻术终被机械钢缆拖回人间，褪去假须的大师在幽暗地窖现出了逃债者的凡胎真形。",
            "paraphrase",
            "SAFE",
            "第3阶段侦破后对全剧案情的文学化抒情总结，属已知安全总结。",
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
