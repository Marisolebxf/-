ponytail: off

# POL-L2-DS11-PLAN-DATA · 政策分析评价推荐方案报告交互展示数据落点

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 登记表已有认领。本单不改认领字段 |
| lock_until | `2026-11-03T17:08:46.514Z` |
| 说明 | 定义单。只写数据落点。列级定义只定粒度和必要列。不建库，不灌数，不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过 D9、D16 行级列、调用链和空表返回空。

## 范围

政策分析评价 · 二级「推荐方案报告交互展示」。SRS 序号 227–231，用户故事 `US-DS-POL-05`。上游是 `POL-L2-DS11-PLAN-ARCH` 第 9 节。数据落点写在 `sdd/l2/POL-L2-DS11-PLAN-DATA.md`。对照同目录解读分册，不改那份文件。

| 序号 | 叶子 | 落点 |
|---|---|---|
| 227 | 多方案对比展示 | `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 的方案对照行 |
| 228 | 方案参数自定义模拟 | 同一张表的参数模拟行。按方案和参数档拣 |
| 229 | 实施路径与风险辅助 | 同一张表的路径与风险行。`metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015` |
| 230 | 互动意见收集与专家参与 | 同一张表的互动意见行 |
| 231 | 方案报告导出与归档 | 不另建行。导出从方案对照行和互动意见行生成 |

## 表与粒度

只一张表 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。本单只定列，不建库，不灌数。四种 `row_kind`：方案对照、参数模拟、路径与风险、互动意见。231 不占种类。

方案对照一行一个方案：名称、一句说明、对照维度和数值、优劣结论、实施建议。`gap_item` 为 `227 多方案对比展示`。`metric_id` 留空。少于两行则对比空，不补方案。

参数模拟一行挂一档：参数档、评估结果、一句趋势、一条归档说明。`gap_item` 为 `228 方案参数自定义模拟`。`metric_id` 留空。对不上方案和参数档则预览空。采纳不插入。

路径与风险一行一个节点，风险写在同一行，同一方案按 `sort_no` 排序。`gap_item` 为 `229 实施路径与风险辅助`。`metric_id` 固定 `M_POLICY_DS_11_POLICY_EVAL_015`。D4 保持 mock。无行则路径空。

互动意见一行一条：主体、分类（评价、评论、建议）、正文、时间。`gap_item` 为 `230 互动意见收集与专家参与`。`metric_id` 留空。未选方案则列表空。请求不插入。

每行带 `metric_id`、`gap_item`、`fill_method=manual`、`gapfill_batch_id`、`generated_at`，以及 `is_mock=1`。不设 `fill_model`。查询不插入。列清单不是可执行 SQL。

231 读取方案对照行的名称、说明、优劣结论、实施建议、对照值，以及挂在这些方案上的互动意见行。不读参数模拟行和路径行来拼导出。不灌文件，不写对象存储。

本二级不读已有 ADS。`ads.policy_simulate` 不复制进本表。不写 ODS、DWD、ADS、供应方库。D4 保持 mock。

## 灌数单

只点名，本单不认领，不执行。

| 灌数单 | 点名内容 |
|---|---|
| `POL-L2-DS11-PLAN-GAPFILL-L01` | 按本单第 2 节建 `gapfill_policy_eval_scheme`，灌四种行。231 不灌文件。依赖本单。当前 `backlog` |

该单 DoD 已指向这一张表。本分册把专家意见条目收成互动意见行。本单不改那张任务的注册字段。查询请求不调用这张灌数单。

## 不重开 GDF

不重开 GDF。不写 nGQL。不加 ODS、DWD、ADS 表。不新造 `metric_id`。不把 D4 从 mock 改绿。

## 偏离

无实现偏离。五叶只加架构第 9 节这一张缺项表。已有推演表留在推演键，不进入本表。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-PLAN-DATA.md`（本 handoff）

未改代码仓，未改 `task-registry.yaml` 手稿，未 commit，未 push。未改说明书、WBS、`指标与501.md`、解读分册、架构稿。未认领 `POL-L2-DS11-PLAN-GAPFILL-L01`。未建库，未灌数。

## 验收证据

- 227–231 的库表与架构第 9 节一致：只一张 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`，四种类。
- 路径行 `metric_id` 为已有 `M_POLICY_DS_11_POLICY_EVAL_015`，其余三种留空。`fill_method=manual`。D16 列写明。D4 保持 mock。
- 231 不另建表、不灌文件。导出从方案对照行和互动意见行生成。
- 推演情景不进本表。灌数单只出现在点名表。本单没有建库、没有插入。
- 定义任务，未跑业务 CI，未部署。待会签。不标 done，不标 ready_to_sign。

## 架构合规自检

- ✅ 调用链：`gkxlumen-element` 只读这张表。展示不直连库，不直连 Python。
- ✅ Java 不写算法，不按弹性公式现算，不插入意见。
- ✅ 不写 nGQL。路径行不读政策子图。
- ✅ D9：不新造 `metric_id`，不改 D4。无行不造数。
- ✅ D14：不写 PDF、Word、Excel，不新建桶，不写对象键。
- ✅ D16：只在 `gkxlumenx_gapfill`。行上带 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。不写 ODS、DWD、ADS、供应方库。
- ✅ D18：mock 先落这张表，再被查询。查询不直接返回 mock。231 的文件从当次读到的行生成。
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
| diagram_id | `POL-L2-DS11-PLAN-ARCH-SEQ` |
| 图 diff | 本数据叶不改图、不加边。读路径沿用架构第 9 节 |
| 会签态 | `draft`。源文件无 frontmatter，沿架构稿记 draft。不自填绿 |
| 说明 | 数据落点不替代该图。本单待会签 |

## 问题清单

- `POL-L2-DS11-PLAN-GAPFILL-L01` 仍是 backlog。表尚未建。查询在表出现之前返回空。本单不认领它。
- 架构稿文件头仍写待 `human:淮政玮` 签收。本单按第 9 节定列，不改那份稿，不把它标成 done。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS11-PLAN-DATA.md`
- 新增本 handoff

## 测试结果

- 只读核对架构第 9 节与解读数据分册的壳表边界。未跑业务测试，未建库，未灌数。

## 遗留风险

- 灌数单未执行。空表时五叶都返回空。这是当前正确行为。
- 架构稿若在签收时改第 9 节的种类或表名，本分册要跟着改。本单不预先改架构。

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

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-DATA.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-PLAN-DATA.md`
