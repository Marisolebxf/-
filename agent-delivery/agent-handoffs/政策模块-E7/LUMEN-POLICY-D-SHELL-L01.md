# LUMEN-POLICY-D-SHELL-L01 · 侧栏壳 + api/policy + 产业篮政策分析分组

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-FE-D-总派单.md`](./LUMEN-POLICY-FE-D-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §2  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。`FE-CHAIN-ANALYSIS-RESUME-L01` 不挡本叶；未回滚产业链 `KEEP_ANALYSIS_QUERY` / `demo_state` / Pinia 袋 / 记录 Tab。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 SearchHub / AnalysisPageHeader / compareBasket / `@/review` / 已有 `/topicAsync` 任务封装；未贴 JSX；未 new 地图；未做 POL-01c 完整检索、未做三项工作区。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 前端走图上已有实线：`lumen-ui-topic` → `gkxlumen-platform-gateway` `/policy/**` → `gkxlumen-topic-policy`。分析任务声明走已有 `/topicAsync/topic/v1/analysis/tasks`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

1. **侧栏政策菜单可点**（对照 demo Layout 政策分组 + 本仓企业/产业皮肤）：政策扶持 / 政策查询 / 政策时序分析 / 区域政策对比 / 深圳政策现状分析 / 维护管理。均进 `DefaultLayout`。
2. **`src/api/policy` 薄封装**只调 Java：`/policy/topic/v1/policy/{health,search,docs/{id},graph,metrics,indicators}`。分析任务 re-export 已有 `analysisTask*` → `/topicAsync/topic/v1/analysis/tasks`（本叶不 create、不实现工作区）。
3. **对比篮产业 Tab「政策分析」分组**：时序 / 区域对比 / 深圳三维；仅产业对象；无政策文档 Tab。查询页不入篮、不发起分析。

本叶不算查询完成页（POL-01c 另叶）。`/policy/search` 为空壳：SearchHub 皮肤 + Java search + 无数诚实空。

## 偏离说明

- 查询页仅 keyword/smart 把 `q`/`keyword` 打 Java search；高级筛选字段库与智能解析留给 POL-01c。
- 门户四 Tab / 三项工作区 / 维护业务均为 `PolicyShellPlaceholder`（可点进布局）。
- Java Job 规范键 `policy_regional` / `policy_shenzhen` 写在 registry `javaType`；篮分发 URL 仍用 demo `analysis_type`（`policy_region_compare` / `policy_sz_3d`），工作区叶再映射。
- 未改 vite / package.json / `.gitignore`。未回滚产业链过程态。

## 产物清单

- 代码：`lumen-ui-topic` `f96f2a66fffcd77cedded1bec993ed0469a32250` → `origin/dev`
- 本文 handoff

## 菜单路径

| 侧栏 | path | routeName | 页 |
|------|------|-----------|----|
| 政策扶持 | `/policy-portal` → `/policy-portal/overview` | `policy-portal` / `policy-portal-overview` | 壳 |
| 政策查询 | `/policy/search` | `policy-search` | SearchHub 空壳 |
| 政策时序分析 | `/policy/overview` | `policy-overview` | 壳 |
| 区域政策对比 | `/policy/analysis` | `policy-analysis` | 壳 |
| 深圳政策现状分析 | `/policy/recommendation` | `policy-recommendation` | 壳 |
| 维护管理 | `/policy/maintenance` | `policy-maintenance` | 壳 |

## api/policy 方法列表

| 方法 | HTTP | 路径 |
|------|------|------|
| `policyHealth` | GET | `/policy/topic/v1/policy/health` |
| `policySearch` | GET | `/policy/topic/v1/policy/search` |
| `policyDocs` | GET | `/policy/topic/v1/policy/docs/{id}` |
| `policyGraph` | GET | `/policy/topic/v1/policy/graph` |
| `policyMetrics` | GET | `/policy/topic/v1/policy/metrics` |
| `policyIndicators` | GET | `/policy/topic/v1/policy/indicators` |
| `analysisTaskCreate` / `List` / `Detail` / `Result` | 声明 | `/topicAsync/topic/v1/analysis/tasks`（已有封装，本叶不跑工作区） |

## 产业篮入口

系统对比篮 → **产业 Tab** → 发起分析 → 分组 **「政策分析」**：政策时序分析 / 区域政策对比 / 深圳政策现状分析。仅 `elementKey=industry`。无政策文档 Tab。

## 验收证据

- `node src/router/menu.selfcheck.mjs`：`svc-shell ok` + `policy-shell ok`（含 KEEP_ANALYSIS_QUERY / demo_state / 不入篮 / 无 demo-* 路径）
- `npx vue-tsc --noEmit`：通过
- USE_MOCK=true：`registerApiMock` 诚实空包（`items=[]` / `item=null` / `fabricated=false`）
- USE_MOCK=false：页内无 `MOCK_`、无 `@/mock/**` 填数

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ 侧栏六入口 + 查询 SearchHub Hero + 产业篮政策分组；一节点一套 layout |
| R2 交互 | ✅ 查询：未搜 / 加载 / 失败 / 诚实空 / 有结果；篮：选产业后出现政策三项并分发到配置壳 |
| R3 样式 | ✅ `--sci-bg-page` / `#D8E7FC`；SearchHub 与企业查询同皮肤 |
| R4 评审 | ✅ 只从 `@/review`：`POLICY-SEARCH-SHELL-TRACE` / `POLICY-SHELL-ENTRY-TRACE`；沿用 `ENT-COMPARE-F08-INDUSTRY-BASKET-TRACE` |
| R5 Mock | ✅ 开：`src/mock/register.ts`；关：Java 实包，无数诚实空 |

### 检索皮肤 V1–V7

本叶 **不是** POL-01c 完成查询页。`/policy/search` 为空壳，下列为壳页自检（完整 V 由 POL-01c 收口）：

| # | 结果 |
|---|------|
| V1 | ✅ 页底 `var(--sci-bg-page)` / `#D8E7FC` |
| V2 | ✅ SearchHub `enterprise-search-hero` 与企业查询同皮肤 |
| V3 | ✅ 结果卡标题+摘要横向书写（`policy-search-result`，操作未做，查询不入篮） |
| V4 | ✅ 未叠 `industry-search-result-card` |
| V5 | ✅ 内容列 `min-width: 0` + `flex: 1` |
| V6 | ✅ 无数 `a-empty`；有数才出卡 |
| V7 | ✅ 结果 `article` 不含 `industry-search-result-card` |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端无 NLP |
| 前端→Java→Python `/internal/*` | ✅ 只调 `/policy/topic/v1/policy/**` 与 `/topicAsync` |
| 图谱 Nebula | ✅ 本叶不 new 地图、不直连 nGQL |
| 可观测 | ✅ 复用 `request.ts` `X-Trace-Id` |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ Vue 重写 |
| D8 / D10 | ✅ token + Arco；交互走兄弟页 |
| D9 8 件套 | ✅ 本叶无数统计数字；未自造 ⓘ（评审只 TraceInfoIcon） |
| D12 lumen 不调 demo **服务** | ✅ 无 `demo-*` URL；数仓共用 `demo_gkxlumenx_*` 是总控 §0 #6 |

## 测试结果

- 菜单自检通过；vue-tsc 通过。
- 本机未起 K8s 现网页点；联调确认：C 门面路径已就绪，前端只声明 Java 路径。

## 遗留风险

- POL-01c 需补智能解析 / 高级筛选 / 卡片操作（仍禁止入篮）。
- 三项工作区叶需把篮分发 query 接到 async `policy_*` types。
- K8s `helm:chart` / `deploy:topic-policy` 仍可能挡现网 search；空库诚实空。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`f96f2a66fffcd77cedded1bec993ed0469a32250`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署：随仓既有 CI；本叶不改 helm
- dev URL：`http://10.50.69.111:30892`（发布后点侧栏政策）

## 可观测性

- 复用前端 `request.ts` `X-Trace-Id` / `traceparent`
- Tempo / Loki：随平台；本叶未抽样

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/router/menu.ts` | 政策分组 + 六入口 |
| `src/perms/matrix.ts` | 政策 perm L0/L2/L4 |
| `src/layouts/DefaultLayout.vue` | `IconFile` 政策图标；**未改** KEEP_ANALYSIS_QUERY |
| `src/api/policy/*` | 薄封装 |
| `src/config/policyAnalysisRegistry.ts` | 篮分发三项 |
| `src/config/policySearchConfig.ts` | SearchHub 皮肤契约 |
| `src/views/policy/PolicySearchPage.vue` | 查询空壳 |
| `src/views/policy/PolicyShellPlaceholder.vue` | 其余入口壳 |
| `src/components/enterprise/compare/IndustryCompareBasketPanel.vue` | 政策分析分组 |
| `src/api/enterprise/types/analysisTask.ts` | `PolicyAnalysisType` 四键 |
| `src/mock/policy/policyApi.ts` + `register.ts` | 诚实空 mock |
| `src/router/menu.selfcheck.mjs` | 政策壳断言 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 165000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.10 |
| cost_warn | green |
