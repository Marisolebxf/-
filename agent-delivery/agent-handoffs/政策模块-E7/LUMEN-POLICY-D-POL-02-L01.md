# LUMEN-POLICY-D-POL-02-L01 · 政策专题 D · /policy/overview 时序工作区结果板

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-FE-D-总派单.md`](./LUMEN-POLICY-FE-D-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §2  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> 前序：[`LUMEN-POLICY-D-WAITVIEW-L01.md`](./LUMEN-POLICY-D-WAITVIEW-L01.md) `d6e13bd` · [`LUMEN-POLICY-D-POL-01-L01.md`](./LUMEN-POLICY-D-POL-01-L01.md) `67628df0` · [`LUMEN-POLICY-C-TASK-L01.md`](./LUMEN-POLICY-C-TASK-L01.md) `6b91104` · [`LUMEN-POLICY-C-METRICS-L01.md`](./LUMEN-POLICY-C-METRICS-L01.md) `7d4b164`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。未回滚产业链 `KEEP_ANALYSIS_QUERY`。未改 `/policy/analysis`、`/policy/recommendation` 结果板。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `IndustryMetricCard` / `IndustryResultReportEntry` / `SystemReportReader` / `buildIndustryAnalysisReportDocument` / `@/review` / `analysisTaskResult`；未贴 JSX；未 new 地图；未复制第二套任务队列；未做政策文档 Tab、未让查询页入篮。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 结果板只消费 Java `GET /topicAsync/topic/v1/analysis/tasks/{id}/result`；KPI 缺字段才读 `GET /policy/topic/v1/policy/metrics`。切条件不自动 create；succeeded 不自动跳结果。工厂 ODS→GDF→DWD→ADS 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

US-E7-POL-02，金路径 #3 结果段。路由仅 `/policy/overview`（`analysisKey=policy_timeseries`）：

1. 把 WAITVIEW `policy-analysis-result-placeholder`（仅 overview）换成时序结果板：冻结配置条、KPI×4、关联表、密度趋势、效力层级、支持强度趋势、关键节点时间轴、洞察。
2. 数据只来自 Java `GET /topicAsync/topic/v1/analysis/tasks/{id}/result`；KPI 缺值时才补 `policyMetrics` 读面，不把全局 headline 伪装成本任务切片。空/缺字段诚实空 + 评审角标。
3. 统计数字旁 ⓘ：`IndustryMetricCard` → `@/review` `ReviewMetricBadges` / `MetricSpecCard`，只读 catalog/readiness 镜像；禁止手写 D1–D4。QPOL-02 / QPOL-07 挂 ⚠️，不改绿。
4. 配置区 / 过程壳 / 记录 Tab 保持 POL-01 + WAITVIEW；本叶未拆。
5. I2-12：切条件不自动 create；点「查看结果」才进本叶结果；当天成功打开 wait_view；「重新分析」`force=true`；Job failed 停过程壳，不当空态。

## 偏离说明

- 现网 Job snapshot 多为 harness `{result.results[]}`，密度/支持强度/节点常为空：结果板结构在、字段诚实空，禁止 Demo fixture 填 2024/2026 窗口期文案。
- KPI 若 result 无 headline，才读 metrics；评审态提示非本任务切片。
- 未改 `/policy/analysis`、`/policy/recommendation` 结果占位（POL-03/04）。
- 未改 vite / package.json / `.gitignore`。未回滚 `KEEP_ANALYSIS_QUERY`。

## 产物清单

- 代码：`lumen-ui-topic` `ed592164dbb8eb0e97bdfffbf459c9b388e02c0e` → `origin/dev`
- 本文 handoff

## 菜单路径（本叶改）

| 侧栏 | path | 页 |
|------|------|----|
| 政策时序分析 | `/policy/overview` | 配置 + 过程壳 + **时序结果板** + 报告阅读 |
| 区域政策对比 | `/policy/analysis` | 配置 + 过程壳 + 结果占位（未改） |
| 深圳政策现状分析 | `/policy/recommendation` | 配置 + 过程壳 + 结果占位（未改） |

## Java 调用

| 动作 | 方法 | 路径 |
|------|------|------|
| 查看结果 | `analysisTaskResult` GET | `/topicAsync/topic/v1/analysis/tasks/{id}/result` |
| KPI 补读（仅缺 headline） | `policyMetrics` GET | `/policy/topic/v1/policy/metrics` |
| 重新分析 | `analysisTaskCreate` POST | `/topicAsync/topic/v1/analysis/tasks`（`force=true`） |
| poll / 记录 | 沿用 WAITVIEW | GET `{id}` / POST list |

未调 `#106` asset、未调 demo-*、未直打 Python。

## 验收证据

- `node src/views/policy/policyTimeseries.selfcheck.mjs`：`policyTimeseries.selfcheck ok`
- `node src/views/policy/policyWaitView.selfcheck.mjs`：`policyWaitView.selfcheck ok`
- `node src/router/menu.selfcheck.mjs`：`svc-shell ok` + `policy-shell ok`
- `npx vue-tsc --noEmit`：通过
- USE_MOCK=false：页内无 `MOCK_`、无 `@/mock/**` 填数；mock 开时 snapshot 形状=Java 包络（`res-{taskId}` + `honesty.empty`）

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ overview 结果：冻结条 + KPI×4 + 关联表 + 密度/层级 + 支持强度 + 关键节点 + 洞察；一节点一套 layout |
| R2 交互 | ✅ 空 / 加载 / 失败（过程壳）/ wait_view / 点查看才进结果 / 条件脏不 create / 重新分析 force / 行点选时间轴 |
| R3 样式 | ✅ `--sci-bg-page` / `#D8E7FC`；复用 `industry-diagnosis` 结果皮肤 + `--sci-primary` |
| R4 评审 | ✅ 只从 `@/review`：`E7-POL-F01-RESULT-BOARD` / `DYNAMIC-DB` / `INSIGHT-TRACE` + MetricSpecCard / PendingBadge；关评审零泄漏 |
| R5 Mock | ✅ 开：`registerApiMock` + `analysisTaskStore` Java 形状空包；关：只渲染 Java 实包 |

### 检索皮肤 V1–V7

本叶 **无检索页**（查询已由 POL-01c 交付）。下列 **N/A**：

| # | 结果 |
|---|------|
| V1 | N/A 本叶无检索 Hub；工作区页底仍用 `--sci-bg-page` / `#d8e7fc` |
| V2 | N/A 无检索 Hero |
| V3 | N/A 无检索结果卡 |
| V4 | N/A 未叠检索卡 class |
| V5 | N/A 无检索内容列 |
| V6 | N/A 检索空态属 POL-01c |
| V7 | N/A 无 `industry-search-result-card` |

### 工作区 W1–W4

| # | 结果 |
|---|------|
| W1 | ✅ **结果板必过**（密度/支持强度/关键节点）。配置区/过程壳/记录 Tab 继承 POL-01 + WAITVIEW |
| W2 | N/A Demo `/policy/overview` 无关系图，本页未用 G6/ECharts 冒充关系图 |
| W3 | ✅ Demo 有报告入口：挂已有 `SystemReportReader`（`PolicyTimeseriesReportHost`），未新造阅读器 |
| W4 | ✅ 切条件不自动 create；条件栏「开始分析」；同指纹 inflight 复用过程；当天成功打开 wait_view；点「查看结果」才进本叶；「重新分析」`force=true` |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端无 NLP |
| 前端→Java→Python `/internal/*` | ✅ 结果只调 Java GET `.../tasks/{id}/result`（及 metrics 读面） |
| 图谱 Nebula | ✅ 不 new 地图、不直连 nGQL；W2 N/A |
| 可观测 | ✅ 复用 `request.ts` `X-Trace-Id` |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ Vue 重写，未贴 JSX |
| D8 / D10 | ✅ token + Arco；对照 Demo 时序结果 + 本仓产业结果板 |
| D9 8 件套 | ✅ ⓘ 只读 catalog/readiness；QPOL ⚠️ 不改绿 |
| D12 lumen 不调 demo **服务** | ✅ 无 `demo-*` URL |
| I2-12 | ✅ 见 W4 |

## 测试结果

- 时序 / wait_view / menu 自检、vue-tsc 通过。
- 联调确认：overview 结果板只打 Java result；切条件不 create；succeeded 不自动跳结果。

## 遗留风险

- 现网 Job 空 snapshot 时图表/节点诚实空，需 Python/Java 结果包补 `density_trend` / `support_trend` / `key_nodes` 后才有线。
- POL-03/04 仍是结果占位。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`ed592164dbb8eb0e97bdfffbf459c9b388e02c0e`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署：随仓既有 CI；本叶不改 helm
- dev URL：`http://10.50.69.111:30892`（发布后：`/policy/overview` 开始分析 → wait_view → 查看结果 → 时序结果板）

## 可观测性

- 复用前端 `request.ts` `X-Trace-Id` / `traceparent`
- Tempo / Loki：随平台；本叶未抽样

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/utils/policyTimeseriesResult.ts` | 新增：解析 Java result 实包 |
| `src/components/policy/PolicyTimeseriesResultBoard.vue` | 新增：时序结果板 |
| `src/components/policy/PolicyTimeseriesReportHost.vue` | 新增：挂 `SystemReportReader` |
| `src/composables/usePolicyAnalysisJob.ts` | `resultPayload` + GET result；`view=report` |
| `src/views/policy/PolicyAnalysisConfigPage.vue` | overview 换结果板；analysis/recommendation 仍占位 |
| `src/mock/enterprise/analysisTaskStore.ts` | 政策 success 签发 `res-{taskId}` Java 形状空包 |
| `src/views/policy/policyTimeseries.selfcheck.mjs` | 新增自检 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 110000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.05 |
| cost_warn | green |
