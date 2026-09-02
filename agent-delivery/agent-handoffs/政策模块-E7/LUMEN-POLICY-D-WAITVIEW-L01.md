# LUMEN-POLICY-D-WAITVIEW-L01 · 政策专题 D · wait_view 过程壳（复用 SystemTaskLayer）

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-FE-D-总派单.md`](./LUMEN-POLICY-FE-D-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §2  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> 前序：[`LUMEN-POLICY-D-POL-01-L01.md`](./LUMEN-POLICY-D-POL-01-L01.md) `67628df0` · [`LUMEN-POLICY-C-TASK-L01.md`](./LUMEN-POLICY-C-TASK-L01.md) `6b91104`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。未回滚产业链 `KEEP_ANALYSIS_QUERY` / `demo_state` / Pinia 袋。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `IndustryAnalysisProcessShell` + `SystemTaskFloat` + `analysisTaskCreate/Detail/List`；未复制第二套任务队列；未贴 JSX；未 new 地图；未做完整时序/区域/深圳结果可视化（POL-02/03/04）；未做政策文档 Tab、未让查询页入篮。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 过程壳只调 Java：`POST/GET /topicAsync/topic/v1/analysis/tasks`（及 list/`{id}`）；succeeded `page_mode_hint=process_succeeded_wait_view` + `viewed=false`，点「查看结果」才进结果入口。工厂 ODS→GDF→DWD→ADS 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

US-E7-POL-06，金路径 #3 的过程 / wait_view 段。三路由共用 `PolicyAnalysisConfigPage`：

1. **开始分析**成功后 `view=processing` 进入过程壳（running / failed / succeeded wait_view）。
2. **poll** `GET /topicAsync/topic/v1/analysis/tasks/{id}`（及 list）；只调 Java。
3. **succeeded 停留 wait_view**，禁止自动跳结果；点「查看结果」才进结果占位（完整 W1–W3 结果板留给 POL-02/03/04）。
4. **Job failed 可见失败**（过程壳 error alert + 记录 Tab 红标），不得当空态。
5. **复用** `IndustryAnalysisProcessShell` + 全局 `SystemTaskFloat`；记录 Tab 接 `policy_timeseries` / `policy_regional` / `policy_shenzhen`（及 `policy_focus` 若 list 返回）。
6. **I2-12**：切条件不自动 create；同用户同条件一条在跑则打开过程；当天成功打开 wait_view；「重新分析」`force=true`。
7. 点查看才本地 `viewed`；GetResult 不改 Java `viewed`。

## 过程壳如何复用 SystemTaskLayer

- 页内过程 UI 复用本仓 **`IndustryAnalysisProcessShell`**（与企业/产业 wait_view 同壳：步骤 + 失败红 + succeeded 停页 +「查看分析结果」）。
- 全局任务浮层复用 **`SystemTaskFloat`**（`data-system-task-layer`）：running 探测 + list；recent 增加政策 types；点击走 `buildAnalysisTaskRoute` → 对应 `/policy/*?view=processing`（未 viewed 的 success 不跳 result）。
- 未新建任务表 / 队列 / 第二套浮层。

## succeeded 是否停 wait_view

是。`shouldStayOnPolicyProcessPage`：running / failed 停过程壳；success + `page_mode_hint=process_succeeded_wait_view` + 本地未点查看 → 停 `processing`。`viewResult` 才 `view=result` 并 `markLocalResultViewed`。

## 记录 Tab 是否接政策 type

是。`analysisTaskList` 后过滤 `isPolicyAnalysisType`，当前页 javaType + `policy_focus`。失败行红标可「查看过程」，不可当空表。

## 偏离说明

- 结果板本叶诚实占位（`policy-analysis-result-placeholder`），完整可视化留给 POL-02/03/04。
- `policy_focus` 无独立路由，浮层/记录落到 `/policy/overview`。
- 未改 vite / package.json / `.gitignore`。未回滚 `KEEP_ANALYSIS_QUERY`。

## 产物清单

- 代码：`lumen-ui-topic` `d6e13bd7438d8dee1d048410a24f3d0abbf78e5e` → `origin/dev`
- 本文 handoff

## 菜单路径（本叶改）

| 侧栏 | path | 页 |
|------|------|----|
| 政策时序分析 | `/policy/overview` | 配置 + 过程壳 + 记录 + 结果占位 |
| 区域政策对比 | `/policy/analysis` | 同上 |
| 深圳政策现状分析 | `/policy/recommendation` | 同上 |

## Java 调用

| 动作 | 方法 | 路径 |
|------|------|------|
| 开始 / 重新分析 | `analysisTaskCreate` POST | `/topicAsync/topic/v1/analysis/tasks`（`force=true` 仅重新分析） |
| poll 详情 | `analysisTaskDetail` GET | `/topicAsync/topic/v1/analysis/tasks/{id}` |
| 记录 / 门控 | `analysisTaskList` POST | `/topicAsync/topic/v1/analysis/tasks` list |
| 查看结果指针 | `analysisTaskResult` GET | `.../tasks/{id}/result`（不改 viewed；本叶不渲染结果板） |

## 验收证据

- `node src/router/menu.selfcheck.mjs`：`svc-shell ok` + `policy-shell ok`
- `node src/views/policy/policyConfig.selfcheck.mjs`：`policyConfig.selfcheck ok`
- `node src/views/policy/policyWaitView.selfcheck.mjs`：`policyWaitView.selfcheck ok`
- `npx vue-tsc --noEmit`：通过
- USE_MOCK=false：页内无 `MOCK_`、无 `@/mock/**` 填数

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ 三路由共用：配置区 + 过程壳 + 记录 Tab + 结果入口占位；一节点一套 layout |
| R2 交互 | ✅ 空 / 加载 / 失败 / wait_view / 条件脏 / 重新分析；切条件不 create |
| R3 样式 | ✅ `--sci-bg-page` / `#D8E7FC`；复用 `industry-diagnosis` 过程壳皮肤 |
| R4 评审 | ✅ 只从 `@/review`：原 CONFIG/SCOPE Trace + `E7-POL-WAITVIEW-PROCESS-TRACE` / `E7-POL-WAITVIEW-RESULT-PLACEHOLDER` |
| R5 Mock | ✅ 开：既有 `registerApiMock` + `analysisTaskStore`；关：Java 实包，无数诚实空 |

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
| W1 | ✅ **过程壳必有**（`IndustryAnalysisProcessShell`）。配置区继承 POL-01；记录 Tab 已接政策 type。结果板留给 POL-02/03/04 |
| W2 | N/A 本叶无关系图 |
| W3 | N/A 本叶无报告阅读器 |
| W4 | ✅ 切条件不自动 create；条件栏「开始分析」；同指纹 inflight 复用过程；当天成功打开 wait_view；「重新分析」`force=true` |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端无 NLP |
| 前端→Java→Python `/internal/*` | ✅ 只调 `/topicAsync/topic/v1/analysis/tasks` 与既有 `/policy/topic/v1/policy/**` |
| 图谱 Nebula | ✅ 不 new 地图、不直连 nGQL |
| 可观测 | ✅ 复用 `request.ts` `X-Trace-Id` |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ Vue 重写，未贴 JSX |
| D8 / D10 | ✅ token + Arco；过程壳对照产业/SVC |
| D9 8 件套 | ✅ 未自造 ⓘ；配置页既有 MetricSpecCard 保留 |
| D12 lumen 不调 demo **服务** | ✅ 无 `demo-*` URL；数仓共用 `demo_gkxlumenx_*` 是总控 §0 #6 |
| I2-12 | ✅ 见 W4 |

## 测试结果

- 菜单 / policyConfig / policyWaitView 自检、vue-tsc 通过。
- 联调确认：过程壳只打 Java 契约路径；create 用规范键；poll GET `{id}`；succeeded 不自动跳结果。

## 遗留风险

- POL-02/03/04 需把本叶 `view=result` 占位换成完整结果板（W1 结果 / W2 / W3）。
- 现网 Job 空结果仍签发 snapshot 时，结果入口诚实空，由结果叶按角标渲染。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`d6e13bd7438d8dee1d048410a24f3d0abbf78e5e`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署：随仓既有 CI；本叶不改 helm
- dev URL：`http://192.168.88.50:30892`（发布后：三项分析「开始分析」→ 过程壳）

## 可观测性

- 复用前端 `request.ts` `X-Trace-Id` / `traceparent`
- Tempo / Loki：随平台；本叶未抽样

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/composables/usePolicyAnalysisJob.ts` | 新增：poll / wait_view / force / 记录 |
| `src/views/policy/PolicyAnalysisConfigPage.vue` | 配置成功进过程壳；记录 Tab；结果占位；重新分析 |
| `src/composables/analysisTaskRoutes.ts` | 政策 type 浮层路由；未 viewed → processing |
| `src/components/system/SystemTaskFloat.vue` | recent 接政策 types |
| `src/config/policyAnalysisRegistry.ts` | 阶段文案 + javaType 路由 |
| `src/views/policy/policyWaitView.selfcheck.mjs` | wait_view / failed / force 自检 |
| `src/router/menu.selfcheck.mjs` | 过程壳 / force 断言 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 165000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.12 |
| cost_warn | green |
