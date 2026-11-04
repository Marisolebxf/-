# POL-L2-DS12-SIM-ARCH · 政策效果推演 · 科技政策推演 · 后台实现架构设计

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 长任务总控已授权，无人值守按叶推进 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off`（定义任务，不缩文档） |

## 范围
- 任务：`POL-L2-DS12-SIM-ARCH`（task_type=definition；WBS-05-23-L2-09A）
- 日期：2026-11-04
- SRS 序号 237–242（level5「科技政策推演」六叶），用户故事 `US-DS-POL-06`
- 产物：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-SIM-ARCH.md`
- 上游只引用不改写：SRS 政策效果推演.md、说明书第 2/11 节、`sdd/调用链与边界.md`、`sdd/契约输入清单.md`、`sdd/指标与501.md` §3、`survey/DS-12.md`、EST-ARCH §0 分组裁定

## 修改内容

1. 新增 `sdd/l2/POL-L2-DS12-SIM-ARCH.md`：237–242 六叶实现架构与整体流程。
2. 注册表状态推进：claimed → in_progress。不标 done（definition 单，待会签）。

## 关键裁定（详见分册）

1. **资源不变**：推演页唯一资源 `POST /display/v1/policy/simulation/jobs`，237–242 在其上按种类分发；不新开 URL、不进异步管道、不加 Job 键（`PolicyAnalysisTypes` / `JOB_SUB_TYPES` 均不动）。
2. **237 读已有解析表**：`ads.policy_text_parse` 解析行（title/summary/auto_tags/structured_elements），排除条款行；请求不调用 `polan.text.parse.run`（run() 清空整表会连带清条款行，评价 226 同款先例）。中台读面 `/v1/policy/text/parse` 与 demo 签留原地，展示不直连（D12）。
3. **238/239/241/242 读缺项表**：`gapfill_policy_sim_result` 四种行（重点、影响范围、路径环节、解读段落），枚举以需规原文四/三/五/四组为界；图表渲染在前端，服务端只返回行。灌数归 `POL-L2-DS12-SIM-GAPFILL-L01`，字段归 `POL-L2-DS12-SIM-DATA`；灌数单 DoD 的「文本解析」一行不灌（已有表收窄，评价 READ-ARCH 同款先例）。
4. **239 跟随推演上下文**：推演键 `M_POLICY_SIMULATE` 只挂 232–234（EST 裁定）；真推演接通后影响范围改随真结果，资源与种类不变。
5. **240 不设资源**：跨项索引，页面消费第 7 项政策子图；`M_POLICY_DEEP_171_1` / `M_POLICY_LAYOUT_REC_COUNT` 布局推荐键不进本二级。
6. **metric_id 纪律**：237 行仍是 `M_POLICY_TEXT_PARSE`；其余缺项行 `metric_id` 留空。不新造、不改 D4。

## 测试结果

- 文档叶。无业务仓测试。
- 自检：六叶各有「现在就能照着做」的链路（分册 §8 表），无「以后再选算法」表述；无接口直返 mock；三档判定与调研/指标分册一致（0 统计读面，501 10 行归属 EST+SIM 两半区，跨项索引 240 + 布局推荐）。

## 遗留风险

- 会签未完成：架构、算法、数据、产品四角色未签。签收只由 `human:淮政玮` 做。会签前 `指标与501.md` / 说明书 / 契约输入清单里 237–242 仍写 501，本叶不改写它们。
- `POL-L2-DS12-SIM-DATA` 需把 237 的取列口径与条款行判别写法落成字段；若数据侧裁定条款行判别不可靠，回退方案是 237 降级为只读 summary 列（评价 226 同款），报告区只显摘要。
- 灌数单 DoD 写有「文本解析」灌数项，与本裁定冲突处已在本叶 §9 写明收窄；data-agent 开工前需按本叶执行。

## CI/CD（必填）

- 分支：编排仓本地工作区，未 commit、未 push
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：文档叶，无

## 可观测性（建议）

- 无代码改动，无新埋点。trace 沿既有展示链（display → element 带 traceId），分册不新设计观测点。

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-SIM-ARCH.md`（新增）
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-SIM-ARCH.md`（本 handoff，新增）
- 注册表 `POL-L2-DS12-SIM-ARCH` 状态（claimed → in_progress，MCP 操作）

## 架构合规自检（公约 §2 逐条）

| 铁律 | 自检 |
|---|---|
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/**`；display → element 只读 / async 管道不新增 |
| 算法只在 Python | ✅ 不迁任何 `polan.*` 进 Java；run() 不进请求路径 |
| 图谱 Nebula | ✅ 240 只消费子图，Java 不写 nGQL，不建查图任务 |
| 可观测 | ✅ 沿既有链，无新埋点 |
| D12 demo 隔离 | ✅ 中台读面留原地，lumen 链零 demo 运行时依赖 |
| D16/D18 mock 表 | ✅ 只用 `gkxlumenx_gapfill.gapfill_policy_sim_result`；237 不灌缺项行、读已有 ADS；接口只读表，禁止直返 mock |
| D9 指标 | ✅ 不新造 metric_id、不改 D4；237 仍 `M_POLICY_TEXT_PARSE`，其余留空 |
| 分键 | ✅ 布局推荐两键不进 237–242；推演键只挂 232–234 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~60k |
| model_used | glm-5.3-flash |
| actual_cost | <0.1 |
| cost_warn | green |
