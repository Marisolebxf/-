# POL-L2-DS11-PLAN-ARCH · 政策分析评价推荐方案架构

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| lock_until | `2026-11-03T11:15:34.640Z` |
| 说明 | 2026-11-03 两轮均为四角色同意。待 human:淮政玮 签收。不标 done |

## Ponytail

ponytail: off

定义任务，不缩文档。未用 YAGNI 跳过调用链、缺项表读法，以及与推演键、布局推荐、可视化二级、解读二级的分界。

## 范围

政策分析评价 · 二级「推荐方案报告交互展示」。只覆盖 SRS 序号 227–231，用户故事 `US-DS-POL-05`。

| 序号 | 叶子 | 流程 |
|---|---|---|
| 227 | 多方案对比展示 | `jobs` 读 `gapfill_policy_eval_scheme` 的方案对照行 |
| 228 | 方案参数自定义模拟 | 同一条 `jobs` 按方案和参数档读参数模拟行。请求内不重算 |
| 229 | 实施路径与风险辅助 | 同一条 `jobs` 读路径与风险行。`metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015` |
| 230 | 互动意见收集与专家参与 | `shells` 读意见行。请求不插入 |
| 231 | 方案报告导出与归档 | `shells` 从方案行和意见行生成导出。不灌文件 |

浏览器只打 `/display/v1/policy/**`。五叶都不进 `gkxlumen-topic-async-service`，不调用 `polan.text.simulate`。

## 产物路径

`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-PLAN-ARCH.md`

## 与相邻叶子的边界

本叶不写 219–226。`evaluation/counts` 留给短板条数和机遇条数。同一条 `jobs` 上的焦点、效能、摘要、趋势、分区、解读，以及同一条 `shells` 上的模板、多媒体、分析报告份数，由可视化与解读两个二级定义。实现时按种类分发。

`M_POLICY_SIMULATE` 与 `ads.policy_simulate` 留在推演键。`M_POLICY_LAYOUT_REC_COUNT` 留在布局推荐键。序号 241 不顶替 229。`report/jobs` 不是 231。

## 未做事项

- 未写 OpenAPI 字段表、请求体、响应体、枚举。留给 `POL-L2-DS11-PLAN-API`
- 未新造 `metric_id`，未改 D4，未改模型注册表，未把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开
- 未改 `FE-POL-02A`，未新建前端单，未重开 GDF
- 浏览器未改打 `/topic/v1/policy`。未把 `E-E7-POLICY-M1-L06` 写成展示路径
- 未改说明书、调研分册，未改 WBS 里的四单拆分
- 未执行灌数。执行单是 `POL-L2-DS11-PLAN-GAPFILL-L01`，依赖本架构和 `POL-L2-DS11-PLAN-DATA`

## 偏离

原登记说明写「方案对比、参数模拟、实施路径 501；意见收集与方案归档是交互壳，并入 501」。说明书第 11.2 节把这五叶改成一张缺项表。本稿按第 11 节的可实现标准写：接口读 `gapfill_policy_eval_scheme`，不用 501 充当功能，也不在接口里直接返回 mock。

算法中台效果推演页和 `polan.text.simulate.run` 只产出省级力度情景，`metric_id` 是 `M_POLICY_SIMULATE`。注册表虽把 `M_POLICY_DS_11_POLICY_EVAL_015` 列在同一模型下，函数并不写路径与风险。本叶不迁移这套计算。

## 验收证据

架构稿与本 handoff 已落盘。2026-11-03 两轮四角色同意。待 human:淮政玮 签收。定义单，无业务 PR。不标 done。

| 序号 | 链路 | 结论 |
|---|---|---|
| 227 | element 读方案对照行。少于两行则对比空 | 符合。没有方案生成函数 |
| 228 | 按方案和参数档读参数模拟行。对不上则空 | 符合。不挂 `M_POLICY_SIMULATE`，请求内不重算 |
| 229 | 读路径与风险行，沿用已有 `M_POLICY_DS_11_POLICY_EVAL_015` | 符合。不读图，不改 D4 |
| 230 | 读意见行。请求不插入 | 符合。没有采集服务 |
| 231 | 从方案行和意见行生成导出 | 符合。不灌文件，不是研报 Job |

要灌的 mock 在架构稿第 9 节。一张表、四种种类。不灌导出文件、推演情景和当场提交的新意见。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本叶不写算法。五叶没有可迁的方案函数。mock 行由 Python 灌进缺项表，Java 只读 |
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`。display 委托 element，不直连 Python |
| 图谱 | ✅ 229 不读图，不写 nGQL |
| 可观测 | ✅ 沿既有展示链 trace，不新设计观测点 |
| CI/CD | ✅ 定义文档，未 force |
| D12 | ✅ 不调用 demo 服务，不把 demo 页面写成对外入口 |
| D9 | ✅ 不新造 metric_id，不改 D4。229 沿用已有指标号 |
| D14 | ✅ 导出从行生成。本叶不写对象存储 |
| D18 | ✅ 做不到的只建 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`，接口只读 |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POL-L2-DS11-PLAN-ARCH-SEQ` |
| 图 diff | 227–229 走 `evaluation/jobs`，230–231 走 `evaluation/shells`，都由 element 读同一张 gapfill 表。禁止边：进入异步管道、调用 `polan.text.simulate`、接口直接返回 mock、用 501 充当五叶、改挂推演或布局推荐 |
| 会签态 | 图源无 frontmatter，记 `draft`。2026-11-03 四角色同意。待 human:淮政玮 签收 |
| 说明 | 图在架构稿第 2 节，图下有四列表 |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 8000、architect 80/20、B 档 `$3/$15` 回填：`8000×0.80×3/1e6 + 8000×0.20×15/1e6 = 0.043`，记 `0.04`。

## 修改内容

- 新增 `sdd/l2/POL-L2-DS11-PLAN-ARCH.md`
- 新增本 handoff
