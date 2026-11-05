ponytail: off

# POL-L2-DS12-SIM-DATA · 政策效果推演科技政策推演数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 登记表已有认领。本单不改认领字段 |
| lock_until | `2026-11-06T14:52:42.447Z` |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链和空表返回空。

## 范围

政策效果推演。用户故事 `US-DS-POL-06`。数据落点写在 `sdd/l2/POL-L2-DS12-SIM-DATA.md`。上游是 `POL-L2-DS12-SIM-ARCH` 第 5、7、9 节（2026-11-05 已改第 7、9 节）。235、236 的读法沿 `POL-L2-DS12-EST-ARCH` §5.4、§5.5，列在本单。灌数单名 `POL-L2-DS12-SIM-GAPFILL-L01`，与 EST §9 一致。本单不改这两叶已经写明的行内容。

| 序号 | 叶子 | 落点 |
|---|---|---|
| 235 | 多维度效果评估 | 库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_result`，多维评估行 |
| 236 | 利益攸关方参与评估 | 库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_stakeholder`，参与意见行 |
| 237 | 政策文本智能解析 | 库 `gkxlumenx_ads`，表 `policy_text_parse`。只读已有列。不建 gapfill，不灌 |
| 238 | 政策重点可视化展示 | 同一张结果表的重点行 |
| 239 | 政策影响范围分析 | 同一张结果表的影响范围行 |
| 240 | 政策关联分析 | 无表 |
| 241 | 政策实施路径预测 | 同一张结果表的路径环节行 |
| 242 | 政策解读报告生成 | 同一张结果表的解读段落行。内容只在正文列 |

232–234 的列不在本单。那张表是 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`，归 `POL-L2-DS12-EST-DATA`。

## 表与粒度

两张缺项表，不合并，不加第三张。本单只定列，不建库，不灌数。

结果表 `row_kind` 五个值：多维评估、重点、影响范围、路径环节、解读段落。

多维评估一行一个维度：经济、社会、环境、创新，外加得分和一句说明。`policy_id` 空。`gap_item` 为 `235 多维度效果评估`。`metric_id` 留空。无行则雷达空。

重点一行一个重点项：政策、组别（政策目标、支持领域、实施路径、资金安排）、标题、一句明细。`gap_item` 为 `238 政策重点可视化展示`。`metric_id` 留空。政策对不上则该区空。

影响范围一行一个影响对象：政策、类别（受益对象、影响区域、影响行业）、名称、一句说明、时间变化、区域维度原文。`gap_item` 为 `239 政策影响范围分析`。`metric_id` 留空。区域原文不是文件路径。无行则该区空。

路径环节一行一个环节：政策、五环节之一、时间安排、责任主体、一句说明。同一政策同一环节一行。`gap_item` 为 `241 政策实施路径预测`。`metric_id` 留空。无行则该区空。

解读段落一行一个段落：政策、四段之一、正文。正文只在 `body_text`。不设文件路径。`gap_item` 为 `242 政策解读报告生成`。`metric_id` 留空。无行则报告区空。

意见表只有 `row_kind=参与意见`。一行一条：主体（决策者、评估者、利益攸关方）、渠道（在线问卷、意见征集、专家评审）、意见正文、时间。`gap_item` 为 `236 利益攸关方参与评估`。`metric_id` 留空。请求不插入。无行则列表空。汇总是读取时的行数，不另设列。

每行带 `metric_id`、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`，以及 `is_mock=1`。六种业务行的 `metric_id` 都留空。不设 `fill_model`。查询不插入。列清单不是可执行 SQL。

237 按 `policy_id` 读已有 `title`、`summary`、`auto_tags`、`structured_elements`。返回的要素去掉 `clauses` 与 `clause_meta`。行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。无行则报告空。

240 不设列。D4 保持 mock。不写 ODS、DWD、ADS、供应方库。空态是空，不返回 501。

## 灌数单

只点名，本单不认领，不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS12-SIM-GAPFILL-L01` | 按本单第 2 节、第 8 节建两张缺项表。灌 235、236、238、239、241、242。不灌文本解析。不灌 240。不灌文件。依赖本单。当前 `backlog` |

该单 DoD 仍写「灌入文本解析」。本分册按 SIM-ARCH 第 9 节收窄：不写 `gkxlumenx_ads.policy_text_parse`，不把文本解析行写入 gapfill。本单不改那张任务的注册字段。查询请求不调用这张灌数单。

## 不重开 GDF

不重开 GDF。不写 nGQL。不加 ODS、DWD、ADS 表。不新造 `metric_id`。不把 D4 从 mock 改绿。

## 偏离

列覆盖架构和 EST §5.4、§5.5 已写的行内容。有两处相对架构稿字面的落地差，都不改 235、236 的行内容：

- 架构 §9 点名的行级列是 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。本分册沿同目录方案数据分册，两张表各加 `is_mock`，每行 1。D4 仍是 mock。
- 架构 §1.4 写「`structured_elements` 不含 `clauses` 键的行」，并写明判别写法由本单定。条款批次把 `clauses` 更新进同一条解析行。本分册定为：读该行的标题、摘要、标签和其余要素，返回时去掉 `clauses` 与 `clause_meta`，不因该键整行丢弃。

不灌文本解析。不写预测表的列。两张 gapfill 表不合并，不加第三张。240 无表。242 的内容列只有正文。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-SIM-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-SIM-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml` 手稿，未 commit，未 push。未改架构稿、调研分册、`指标与501.md`、说明书、WBS。未认领 `POL-L2-DS12-SIM-GAPFILL-L01`。未建库，未灌数。

## 验收证据

- 结果表覆盖 235、238、239、241、242。意见表只覆盖 236。库与表分开写，都在 `gkxlumenx_gapfill`。
- 237 只读 `gkxlumenx_ads.policy_text_parse`。本单不建它的 gapfill 表，不灌解析行。
- 240 无表。242 内容在 `body_text`，无文件路径列。
- 六种业务行 `metric_id` 留空。`fill_method=manual`。D16 列写明。D4 保持 mock。空态是空，不是 501。
- 预测表 `gapfill_policy_sim_forecast` 的列不在本分册。
- 灌数单只出现在点名表。本单没有建库、没有插入。
- 定义任务，未跑业务 CI，未部署。待会签。不标 done，不标 ready_to_sign。

## 架构合规自检

- ✅ 调用链：`gkxlumen-element` 只读。展示不直连库，不直连 Python。
- ✅ Java 不写算法，不现算得分，不插入意见，不调用 `polan.text.parse.run`。
- ✅ 不写 nGQL。240 不建查图任务。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造数。空态不返回 501。
- ✅ D14：242 不写 PDF、Word，不新建桶，不写对象键，不写文件路径。
- ✅ D16：缺项行只在 `gkxlumenx_gapfill`。行上带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。不写 ODS、DWD、ADS、供应方库。237 对已有 ADS 只读。
- ✅ D18：mock 先落缺项表，再被查询。查询不直接返回 mock。237 读已落库解析行。
- ✅ 不重开 GDF。

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS12-SIM-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用 SIM-ARCH 第 9 节。235、236 的读法沿 EST-ARCH，本单不改那张图 |
| 会签态 | `draft`。源文件无 frontmatter，沿架构稿记 draft。不自填绿 |
| 说明 | 数据落点不替代该图。本单待会签 |

## 问题清单

- `POL-L2-DS12-SIM-GAPFILL-L01` 仍是 backlog。DoD 仍写灌文本解析。执行时按本分册不灌。本单不认领它，不改注册字段。
- 两份架构稿仍待会签。本单按 2026-11-05 的第 7、9 节和 EST §5.4、§5.5 定列，不改那两份稿，不把它们标成 done。
- 237 的判别相对「整行不含 `clauses` 才读取」有落地差，已写在数据分册第 9 节和本 handoff 的偏离节。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS12-SIM-DATA.md`
- 新增本 handoff

## 测试结果

- 只读核对 SIM-ARCH 第 7、9 节，EST-ARCH §5.4、§5.5、§9，以及 DS11 数据分册的章节。未跑业务测试，未建库，未灌数。

## 遗留风险

- 灌数单未执行。空表时 235、236、238、239、241、242 都返回空。这是当前正确行为。
- 架构稿若在会签时改表名、种类或 235、236 的行内容，本分册要跟着改。本单不预先改架构。
- 若会签要求 237 整行丢弃带 `clauses` 的解析行，第 9 节的判别要改回整行过滤。

## CI/CD

- 分支：未提交
- commit：无
- pipeline URL / ID：无。定义任务，`cicd: skip`
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未部署。未建库，未灌数

## 可观测性

- OTEL_SERVICE_NAME：本叶不新设计观测点。trace 沿既有展示链
- traceId（dev 抽样）：无。未发请求
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-SIM-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-SIM-DATA.md`
