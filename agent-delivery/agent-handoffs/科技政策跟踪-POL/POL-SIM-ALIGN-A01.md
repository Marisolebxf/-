# POL-SIM-ALIGN-A01 · DS-12 按现行读口重写

- 日期：2026-11-10
- 监管：`human:淮政玮`
- 执行：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 状态：说明书已改。四角色会签仍未完成。未改任务注册表，未 commit，未 push。

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 本单派令禁止调用 `task-claim` / `task-update-status` / `task-create`，也禁止改 `task-registry.yaml`。注册表状态未动。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `off` |
| 说明 | 定义任务。总控与用户都要求不缩文档。未用 YAGNI 删掉 DS-12 的需规首句、会签表或第 11 节。 |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | 无。本单不改图 |
| 图 diff | 无 |
| 会签态 | 说明书第 9 节仍是架构、算法、数据、产品四行「未签」。本 handoff 不把会签标成已完成 |

## 范围

只改 `sdd/科技政策跟踪-系统详细设计说明书.md` 的 DS-12，以及与序号 232–242 直接矛盾的句子。未改 `POL-SIM-ALIGN-长任务总控.md`。未改业务代码。未新造 `metric_id`。D4 仍写 mock。原型卡片上的增减幅和分数没有写进契约。§5.3 页头写死的 86.5 等数字原样保留，并写明它们不是 DS-12 的契约数字。

依据是《产品实现规程》§4.1：会签未完成可以起草，不标 done。

## 改了哪些叶

232–242 全部重写了读口。需规首句保留。

| 序号 | 原型块名（jsx 卡片） | 现行 Java | 表 | 原文列（回执样本列在前） |
|---|---|---|---|---|
| 232 | 未出台政策仿真模拟：政策参数配置、仿真模拟结果、多次模拟对比 | `POST /display/v1/policy/simulation/jobs`，`kind=未出台仿真` | `gkxlumenx_gapfill.gapfill_policy_sim_forecast`，`row_kind=未出台仿真` | `econ_text`；同叶还有 `social_text`、`innovation_text`、`explain_text`、`yearly_trend` |
| 233 | 新出台政策效果预测：政策摘要（引用解析）、短中长期效果、时间变化趋势、产业发展影响、空间分布特征 | 同上，`kind=新出台预测` | 同上，`row_kind=新出台预测` | `short_effect_text`；同叶还有 `long_effect_text`、`growth_text`、`industry_text`、`tech_effect_text`、`time_trend_text`、`space_feature_text`、`similar_basis_text` |
| 234 | 区域经济发展空间模拟：三维地图 · 省域热力 + 城市柱高、热力图 · 指标矩阵、模拟参数、模拟结果预测 | 同上，`kind=区域空间` | 同上，`row_kind=区域空间` | `gdp_text`；同叶还有 `industry_change_text`、`employment_text`；地图原文是 `spatial_items` |
| 235 | 多维度效果评估：四维雷达图、分项柱状图、按维度名分卡 | 同上，`kind=多维评估` | `gapfill_policy_sim_result`，`row_kind=多维评估` | `score_text`。`score_value` 是数字 |
| 236 | 利益攸关方参与评估：评估活动识别、信息反馈与互动、意见征集 / 在线问卷、专家评审 | 同上，`kind=利益攸关方` | `gapfill_policy_sim_stakeholder`，`row_kind=参与意见` | `opinion_text` |
| 237 | 政策文本智能解析：卡片标题为政策标题；字段为政策关键词、核心内容、战略意图、支持对象、申报条件、支持力度 | 同上，`kind=文本解析` | 不建缺项表。读 `gkxlumenx_ads.policy_text_parse` | `summary`。要素在 `structured_elements`，SELECT 为 `title, summary, auto_tags, structured_elements` |
| 238 | 政策重点可视化展示：政策重点导图、政策重点（柱图）、节点详细说明 | 同上，`kind=重点可视化` → `row_kind=重点` | `gapfill_policy_sim_result` | `detail_text` |
| 239 | 政策影响范围分析：受益对象、覆盖面、覆盖面（分区域）、影响区域（柱图辅视 · 渗透指数）、影响行业、空间分布、时间变化 | 同上，`kind=影响范围` | 同上，`row_kind=影响范围` | `impact_text`；同叶还有 `time_change_text`、`region_text` |
| 240 | 政策关联分析：政策关联网络图、协同效应与体系位置 | 无读口。未知 `kind` 返回空 `records` | 不建表 | 无 |
| 241 | 政策实施路径预测：历史评估图、政策实施流程图 | 同上，`kind=路径预测` → `row_kind=路径环节` | `gapfill_policy_sim_result` | `stage_text`；时间安排原文是 `schedule_text` |
| 242 | 政策解读报告生成：章节自定义、报告预览卡 | 同上，`kind=解读报告` → `row_kind=解读段落` | 同上 | `body_text` |

`M_POLICY_SIMULATE` 只保留在 232–234。235、236、238、239、241、242 的 `metric_id` 按建表和 SELECT 为空。237 行上既有 `M_POLICY_TEXT_PARSE`，本读口 SELECT 不取该列。240 不读 `M_POLICY_RELATION_DEGREE`。

232 另记现行分支：预测表无命中行时，`PolicySimulationService` 调用 `POST /internal/policy/simulation/fallback`。`polan.sim_fallback.fallback_unpublished` 不写库。这与「接口只读表」并列存在于代码里，会签未收成已签收读法。

## 列名从哪段代码核对

未凭记忆填列名。核对过的位置：

- `lumen-svc-platform` `gkxlumen-display` … `PolicySimulationController`：对外只有 `POST /v1/policy/simulation/jobs`。注释写明 240 不在这条资源上。
- 同模块 `PolicySimulationService`：`kind` 闭集、条件、`未出台仿真` 空列表才调 `simulationFallback`。
- 同模块 `RemoteElementClient.policySimulation`：`GET /v1/element/policy/simulation`。
- 同模块 `RemotePolicySyncClient.simulationFallback`：`POST /internal/policy/simulation/fallback`。
- `gkxlumen-element` … `PolicySimulationReadController`：`FORECAST_COLUMNS`、`RESULT_COLUMNS`、`STAKEHOLDER_COLUMNS`、`PARSE_SQL`，以及 `rowKind`（重点可视化→重点，路径预测→路径环节，解读报告→解读段落）。排序闭集：经济/社会/环境/创新，政策目标/支持领域/实施路径/资金安排，政策发布/申报受理/评审评估/资金拨付/效果评估，政策背景/主要内容/预期效果/实施建议。
- `lumen-algo-py/scripts/mysql/gapfill_policy_sim_forecast.sql` 建表列，含 `target_industry`、`econ_text`、`spatial_items`。
- `lumen-algo-py/scripts/mysql/gapfill_policy_sim_result.sql` 两张表的建表列：结果表 `score_text`、`detail_text`、`impact_text`、`time_change_text`、`region_text`、`stage_text`、`schedule_text`、`body_text`；意见表 `opinion_text`。结果表 INSERT 无「文本解析」行。
- `vendor/entan-py/polan/mockgen/simulation.py` `write_simulation` 的样本列：232 `econ_text`，233 `short_effect_text`，234 `gdp_text`，235 `score_text`，236 `opinion_text`，237 与 240 的 `written` 为 0、样本为空，238 `detail_text`，239 `impact_text`，241 `stage_text`，242 `body_text`。文件头写明 237 不另建表、240 不灌，232–234 只用已有 `M_POLICY_SIMULATE`。
- `vendor/entan-py/polan/mockgen/btn.py` 的 `simulation` 元组：237「不另建表」，240「不建表」。
- 原型块名：`demo-ui-science` `estimate/EstimateWorkbench.jsx`、`interpret/InterpretWorkbench.jsx` 的 `pp-l6-section-title` 与 `Card` `title`。
- 真轨差表：`lumen-ui-science-pc` `src/views/policy/simulation/estimate/EstimateWorkbench.vue`、`interpret/InterpretWorkbench.vue`、`simulationLive.mjs` 的 `simulationJobBody`（未出台仿真不提交 `target_industry`；政策关联直接返回 null）。

## 说明书里一并改过的矛盾句

这些句子原先把 11 叶写成整页一个 `M_POLICY_SIMULATE` Job、把 237 算进缺项结果表、或把 240 写成已经在读子图：

- §1 范围：232–242 无行是空 `records`。
- §2 表头：DS-12 拆解列改为现行读口。
- §3：`simulation/jobs` 不走异步链；237 读解析表，其余有读口的叶读 gapfill。
- §4 推演行。
- §5 的 11-09 汇总：推演改为读缺项表 9、读已有 ADS 1、跨项索引 0。240 不计入六列。11-03 原判表未改。
- §5.1 推演行：237 改到「读已有 ADS」。
- §5.3 末句：`M_POLICY_SIMULATE` 只挂 232–234。页头 86.5 那张表的数字未改。
- §6：`simulation/jobs` 注明 240 不在此路径。
- §9 会签四行仍是未签。
- §11.2：预估、结果、意见、解析、关联拆开。文本解析不再写成要灌进 `gapfill_policy_sim_result`。

## 与原型仍对不上的叶

对照 2026-11-10 展示仓真轨（`USE_MOCK=false`）。D01 若随后改布局，读口列名仍以说明书 DS-12 为准。

- 232：三张卡的标题在。结果是正文，不是原型分数。多次对比是页面当次保存。目标产业控件不进请求。
- 233：五张原型卡收成「政策摘要」「效果与分布」，趋势、产业、空间没有按原型单独成图。
- 234：四张卡标题在。GDP、产业结构、就业率展示的是正文。
- 235：雷达图和柱图在。原型维度卡里的分项指标没有列。
- 236：「评估活动识别」真轨为空。意见正文能列出。页内提交不入库。
- 237：原型上的关键词、核心内容、战略意图、支持对象、申报条件、支持力度没有单独列。
- 238：「政策重点（柱图）」没有数值列。
- 239：受益对象、覆盖面、分区域柱图、渗透指数、影响行业、空间分布、时间变化没有按原型分卡。
- 240：整叶无读口。原型两张卡只在 Mock。
- 241：「历史评估图」没有列。流程图用 `stage_text`。
- 242：「章节自定义」和导出格式没有列。接口不返回文件。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 调用链 | 展示读口是前端 → display → element。232 空表分支会再调 Python `/internal/policy/simulation/fallback`，已写入 DS-12，会签未收 |
| 算法在 Python | 未改 Java / Python 业务代码 |
| D4 | 仍是 mock |
| D18 | 主路径是读表。232 的 fallback 不写库、直接返回句子，与「接口只读表」不一致，未签收 |
| 不新造 metric_id | 遵守 |
| 会签 | 第 9 节四行仍为未签 |

## 开放项

- 未调用任务注册表，本单状态未推进。
- 未提交。编排仓改动停在工作区：说明书与本 handoff。
- U01 重写合规演示用例时，期望行来自库内能演的列，不把原型分数写成期望。

## cost

未回填注册表（本单禁止改注册表、禁止提交）。本单为定义改稿，无业务仓 CI。
