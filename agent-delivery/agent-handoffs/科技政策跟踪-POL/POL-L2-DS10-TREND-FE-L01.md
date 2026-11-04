# POL-L2-DS10-TREND-FE-L01 · 科创政策全景 · 政策动向跟踪前端接线真实接口（SRS 203–206 四叶）

- 任务：`POL-L2-DS10-TREND-FE-L01`
- 日期：2026-11-04
- 监管：`human:淮政玮`（派单已授权完工即推，覆盖仓级人工验收闸门）
- 认领：`agent:frontend-agent`
- 强度：ponytail full
- 代码仓：`lumen-ui-science-pc` @ `origin/dev` commit **f4ea400**（5 文件，+941/−95；净树 = 60f9b66 + 本任务增量）
- 伴单：后端 ②号 `POL-L2-DS10-TREND-IMPL-JAVA` 已就绪（`/display/v1/policy/panorama/ingest|stats|jobs`）

## 1. 交付范围

政策动向跟踪四叶（203 入库列表 / 204 订阅复用 / 205 趋势与异步任务 / 206 重点领域主题分布）从契约占位与 mock 单轨切到真实接口双轨；`USE_MOCK=true` 完整保留 demo 冻结种子视觉（种子文件零改动、禁 Math.random 不变）。改动 5 文件：

| 文件 | 改动 |
|---|---|
| `src/api/policy.ts` | 新增 `panoramaIngest()`（GET `/ingest?limit=`）与 `panoramaStats()`（GET `/stats?kind=all`）；203 详情复用既有 `{id}/detail`，jobs 复用既有 `panoramaJobs`（POST `/jobs`），零新增传输封装 |
| `src/views/policy/panorama/trendLive.ts`（新增） | 后端响应 → 视图模型的纯函数层：`mapIngestRows`/`mapTimeseries`/`mapNationalRows`/`mapThemeRows`/`trendJobBodyOf`/`mapHotspotRows`/`mapImpactRows`/`mapReportRows`/`recordsOf`；空输入一律收敛为空数组（诚实空态的基础） |
| `components/TrendTab.vue` | 双轨改造：USE_MOCK=false 拉取 ingest + stats（kind=all）填最新入库表、地域分布条形图、时序折线图、主题分布卡网格；`runHotspot`（热点识别）按钮点击才触发 POST jobs，单飞 loading 禁重复提交；读失败不清已返回块 |
| `components/KeyFieldAnalysisPanel.vue` | 双轨改造：「深度分析报告」与新增「影响评估」按 domain 调 POST jobs（kind=深度分析报告/政策影响评估），`reportBusyFor`/`impactBusyFor` 单飞守卫；无行诚实空态，不前端拼报告 |
| `panorama/FE-POL-TREND-LIVE.test.mjs`（新增） | 最小自检（node `--experimental-strip-types` 直跑全绿）：纯函数单测、端点路径锚点、禁项扫描、MockBadge 保留、I2-12 规则断言 |

204 订阅叶：**只验复用不重接**——SUB-FE-L01 已接 `/subscriptions` 四方法，本任务零改动。

## 2. 接线明细（DoD 对账）

| 叶 | 接口 | 触发 | 行为 |
|---|---|---|---|
| 203 入库 | `GET /display/v1/policy/panorama/ingest?limit=20` | 挂载/切到动向 Tab | 无行 → 空列表（a-empty），不造行；行点击复用全景 `{id}/detail` 弹层 |
| 204 订阅 | `GET /subscriptions`（SUB-FE-L01 已接） | — | 零改动，只验复用 |
| 205 时序/地域 | `GET /stats?kind=all` | 挂载/切 Tab | timeseries 填折线（M_POLICY_TIMESERIES）、national 填条形（M_POLICY_NATIONAL_DIST）；某块空 → 图空不造 0；单块读失败不清其它块（后端块级隔离 + 前端 try/catch 逐块） |
| 205 异步任务 | `POST /jobs`（kind=热点识别/政策影响评估/深度分析报告） | **仅用户点击**（runHotspot/影响评估/深度分析报告按钮） | 切条件不自动起任务；单飞守卫禁重复提交；失败局部提示不清已显示块 |
| 206 主题分布 | `GET /stats` 响应 `theme_dist` 维度 | 同 205 一次拉取 | 无 metric_id：不挂 ⓘ 不造 D9 角标；无行 → 卡网格空态 |

## 3. 空态诚实（DoD）

- 入库/主题分布/热点/影响/报告：无行即空态（a-empty 或空网格），不造 0、不前端拼报告文本
- 时序/地域：records 空 → 图显空（无假 0 序列）
- 读失败：逐块 try/catch，失败块保持上次数据或空态，绝不清空已返回的其它块
- jobs 失败：Message.error 局部反馈，不污染页面数据

## 4. 指标角标（DoD）

- `M_POLICY_TIMESERIES`、`M_POLICY_NATIONAL_DIST` 的 ⓘ（MetricSpecHint）与 MockBadge（USE_MOCK 时）完整保留，读数镜像仍走只读 seed（禁手写状态）
- 主题分布 `theme_dist` 无 metric_id：**不补造** ⓘ/角标（自检断言主题块无 metric_id 注入）

## 5. 工程验证

| 项 | 命令 | 结果 |
|---|---|---|
| 自检 | `node --experimental-strip-types src/views/policy/panorama/FE-POL-TREND-LIVE.test.mjs` | ✅ 全绿（纯函数/端点/禁项/角标/I2-12） |
| 类型 | 本任务 5 文件 vue-tsc | ✅ 0 错（`src/views/policy/analysis/index.vue` 的 88 错为**另一会话在飞改动**，非本单范围，未提交） |
| CI | 流水线 **3685**（f4ea400） | ✅ **success**（build/package/scan/deploy 4 job 全绿） https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/3685 |

自检覆盖：trendLive 纯函数（空输入→空数组、行映射、job body 构造）、API 端点路径与方法锚点（GET ingest / GET stats?kind=all / POST jobs）、禁项扫描（`/topic/v1/policy`、裸 `/v1/policy`、`/topicAsync`、`/internal` 全仓零命中）、MockBadge/MetricSpecHint 保留断言、I2-12（切条件不自动起任务：无 watch 直连 createJob；点击触发才查）。

## 6. 过程事件：多会话在飞改动卷入与修复

首次提交 9bde495 误把另一会话（POL-L2-DS11-READ-WIRING-L01）在 `src/api/policy.ts` 的在飞改动（PolicyEvaluation* 类型引用 + evaluation 3 端点）一并提交，而其依赖的 `types/policy.ts` 同块改动未提交 → 流水线 3683/3684 红（TS2305/TS2304）。经 5240c84、372c570、f4ea400 三次 fix 将提交树摘净为「60f9b66 + 仅本任务增量」；DS11 的 api 改动已恢复为工作区未提交态归还该会话（工作区 diff +69 行待其随配套 types 一并提交）。流水线 3685 终绿。教训已随 commit message 记录：**git add 共享文件前必先 `git diff` 卷入检查**。

## 7. 架构合规自检

- ✅ 调用链：浏览器只打 `/display/v1/policy/panorama/**`（ingest/stats/jobs/subscriptions），无越层、无 `/internal`、无直连 Python
- ✅ 禁项：`/topic/v1/policy`、裸 `/v1/policy`、`/topicAsync/**` 全仓零命中（自检断言）
- ✅ D12：未引入任何 `demo-*` 依赖；未 merge demo 代码
- ✅ D8/D10：布局与交互骨架不动（TrendTab 既有卡片结构），仅数据源与按钮触发逻辑；控件仍为 Arco（a-empty/a-card/a-button）
- ✅ D9：ⓘ/MockBadge 保留；主题分布不造 metric_id；就绪度仍读只读镜像
- ✅ I2-12：切条件不自动起任务；点击触发才查；单飞禁重复提交
- ✅ 未改 Java/后端；mock 种子文件内容零改动
- ✅ commit `[agent:frontend-agent]`；push `origin/dev` 无 force（9bde495 → 5240c84 → 372c570 → f4ea400）

## 8. 产物清单

- `lumen-ui-science-pc` @ dev：**f4ea400**（净增量 5 文件：`src/api/policy.ts`、`src/views/policy/panorama/trendLive.ts`、`components/TrendTab.vue`、`components/KeyFieldAnalysisPanel.vue`、`panorama/FE-POL-TREND-LIVE.test.mjs`）
- CI：流水线 3685 success（含 deploy:k8s 已滚动到 dev）
- 本 handoff（gkx-orchestration）

## 9. cost

| 项 | 值 |
|---|---|
| actual_tokens | ~260k（含读码/契约核对/双轨实现/三轮 CI 修复/自检/handoff） |
| model_used | glm-5.3（Cursor agent） |
| actual_cost | ~$1.8（低于 $10 告警线） |
| cost_warn | false |

ponytail: full —— 纯函数层 trendLive.ts 单文件不拆目录（仅 TrendTab 一处消费，第二处出现再提升）；API 层只加 2 个一行函数复用既有 panoramaGet 封装；jobs 复用既有 panoramaJobs 不另造传输；ImplementationTracker.vue 经核对无接线点未动；自检 node 直跑零框架。
