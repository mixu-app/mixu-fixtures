# mixu-fixtures

谜序（Mixu）的**剧透回归语料**：公开、可复现、版权干净。每个 fixture 是一篇原创或
公有领域的微型悬疑文本，加上它在各个"揭示序号"上**必须可见 / 必须不可见**的标注。

这个仓库存在的理由只有一个：让"没有剧透"变成可以失败的测试，而不是一句承诺。

## 为什么必须单独一个仓库

- 客户端要跑剧透回归测试，但它不能引用私有语料或用户书籍。
- 抽取管线的效果评估需要同一份基准；语料必须两边可见、可审计。
- 版权必须干净：只用**原创合成文本**、公有领域文本或明确授权的文本，并记录依据。

## 结构与规则

```text
schema/fixture.schema.json     # fixture 格式（本仓库自有，引用 graph schema 版本号）
fixtures/synthetic/<id>/       # 每个 fixture 一个目录
  story.md                     # 故事正文（原创或公有领域）
  fixture.json                 # 实体、名称、声称、身份合并、状态变更、horizon 标注
  PROVENANCE.md                # 来源、作者、CC0-1.0 声明与版权干净边界证明
tools/validate_fixtures.py     # 校验标注自洽（不需要网络）
```

校验会拒绝**自相矛盾**的 fixture：如果某个标识符在 horizon 2 被列为"必须不可见"，
但它的揭示序号是 1，说明这份标注本身是错的，测试会假装通过。

```sh
just check     # markdownlint + fixture 标注校验
just validate
```

## 版权红线

- 只允许 `SYNTHETIC_ORIGINAL` / `PUBLIC_DOMAIN` / `EXPLICITLY_LICENSED`，
  并在 `rights_note` 里写清依据。
- 不允许提交真实出版书籍的正文、EPUB、插图、地图或在其上抽取的图数据。
- 不允许把个人阅读笔记、账号信息当作语料。

## 现有语料

| Fixture | 场景 | 证明什么 | 来源与权利 |
|---|---|---|---|
| [`locked-stair`](fixtures/synthetic/locked-stair/fixture.json) | 延迟身份揭示 | 第 2 个 horizon 之前，"灰大衣的人"与"石田先生"必须是两个实体；第 3 个 horizon 才允许合并 | [PROVENANCE.md](fixtures/synthetic/locked-stair/PROVENANCE.md) |
| [`silent-courier`](fixtures/synthetic/silent-courier/fixture.json) | 延迟身份揭示 | 第 3 个 horizon 之前，"无声信使"与"万斯医生"必须独立；第 4 个 horizon 才允许确认合并并推翻不在场证明 | [PROVENANCE.md](fixtures/synthetic/silent-courier/PROVENANCE.md) |
| [`false-witness`](fixtures/synthetic/false-witness/fixture.json) | 对抗性追溯修正 | 第 3 个 horizon 之前禁止泄露"钟表匠"的真实姓名；第 4 个 horizon 之前不可信证词必须保持 CLAIMED 状态，证据与认罪后才允许 CONTRADICTED 与 RETRACTED 追溯修正 | [PROVENANCE.md](fixtures/synthetic/false-witness/PROVENANCE.md) |
| [`chinese-spoiler-eval`](fixtures/eval/chinese-spoiler-eval/eval-set.json) | 剧透判定评测集 | 220 条中文微型悬疑样本，覆盖直接透露、隐性提示、身份别名、错误推论、良性解释与同义转述，严格按文本隔离 train/val/test | [PROVENANCE.md](fixtures/eval/chinese-spoiler-eval/PROVENANCE.md) |

## English

Public, rights-cleared spoiler regression corpus. Each fixture pairs an original
or public-domain mini-mystery with per-horizon "must be visible" /
"must not be visible" annotations, so a projection leak fails a test instead of
shipping.

## 许可证

| 范围 | 许可 |
|---|---|
| `fixtures/**` 故事文本与标注 | [CC0-1.0](LICENSE) |
| `tools/`、`schema/`、CI | [Apache-2.0](LICENSES/Apache-2.0.txt) |

语料刻意进入公有领域：任何实现方（包括商业实现）都必须能自由读取、引用和修改它，
否则它没法当共享回归基准。若某个 fixture 的 `content_basis` 是
`EXPLICITLY_LICENSED`，以该 fixture 的 `rights_note` 为准。
