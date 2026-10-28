# LUMEN-CHAIN-UI-WALKTHROUGH-L01 · 产业链分析模块页面 demo 布局对齐与人走查整改

> 格式参考 `templates/handoff-template.md`。Demo 真源：`repos/demo-ui-topic/src/app/pages/industry-center/`（诊断 `IndustryDiagnosisPage.tsx`、区域 `IndustryRegionalPage.tsx`）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 2026-10-28 孔东走查登记；本单分多批 push，见下方 commit。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | demo 五维（布局/交互/样式/评审/Mock 门控）；`USE_MOCK=false` 不伪造排名/叶子/地图分数；地图坐标用 `regionalCompareMapPoints` 演示行政中心并注明。未用 YAGNI 跳过 D8/D9/D10、评审自闸。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 对照 demo TSX 与 lumen Vue DOM；未挂 Headroom。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | — |
| 会签态 | — |

## 范围与实现

### 批 A · commit `2b8630c`（已 push）

- 关键环节 / 瓶颈堵点：双栏 + 底部 `IndustryAnalysisResultReportPanel`；`parseKeyLinkDetail` / `parseBottleneckNodeDetail`；`industryReplicaFix.selfcheck` 断言。

### 批 B · 本 handoff 对应 commit（待填 hash）

1. **产业周期**：配置区业务态缩短冻结提示；QC06 / 周期旅程 / 联网检索说明包进 `IndustryReviewOnly`；`IndustryCycleResultBoard` 业务态空文案与 demo 一致。
2. **区域产业指数 / 竞争力结果**（`IndustryRegionalResultBoard.vue`）：
   - 指数区：四 KPI、柱/雷达、排名表、叶子贡献表、优劣势（扩展 `parseRegionalBoard`：`indexRows` / `leafRows` / `kpiSummary` / `gisItems`）。
   - 竞争力区：标题 **「综合竞争力计算与横向排名」** + 四 KPI（对齐 demo `buildCompetitivenessResult.summaryMetrics`）；柱状/三维热力/GIS 地图/排名明细/优劣势/版本边界。
   - `RegionalCompareMap.vue` + `regionalCompareMapPoints.ts`（分数来自 Java，经纬度演示坐标）；`IndustryRegionalPage` 传 `region-codes`。
3. **结果区 rhythm**（`industryDiagnosis.css`）：`.diagnosis-result { gap: 16px }`、直接子级标题 margin 归零（对齐 demo）；区域图表/地图去掉叠 margin；去掉 KPI 区多余 `mt-4`。
4. **排名明细表**：选中行 `diagnosis-rank-row--selected`（浅蓝底 `#e8f3ff`，仅首列 inset 主色条）；未选中时第 1 名 `diagnosis-rank-row--leader`；点击行时不再与第 1 名双高亮。
5. **自检**：`industryReplicaFix.selfcheck.mjs`（竞争力标题、compSummaryCards 等）；`regionalCompareMapPoints.selfcheck.mjs`（新增）。

### 未闭合（后续走查）

- 周期结果区 demo 级报告密度与其它诊断类型附录 D/E 全量扫描。
- 产业链其余工作台（深圳、查询、全景专业版等）五维清单。
- `objectSummary` 未选产业文案、叶子表无 `leaf_contributions` 时空态联调。
- CI / K8s dev 目视验收（本批 push 后）。

## 偏离说明

- 报告「生成」仍为骨架（批 A）；区域 GIS 无后端坐标时用前端演示点 + Alert 说明。
- `.env.development` 本地联调改动 **未纳入 commit**（网关/Mock 开关属本机配置）。

## 产物清单

- 代码：`repos/lumen-ui-topic` `origin/dev` — `2b8630c` + **`e87b4df`**
- handoff：`gkx-orchestration` **`cd6877e0`** + 本文件

## 测试结果

- `node src/views/industry-center/industryReplicaFix.selfcheck.mjs` — 绿（2026-10-28）
- `node src/utils/regionalCompareMapPoints.selfcheck.mjs` — 绿（2026-10-28）
- CI：待本批 push 后 GitLab dev Pipeline

## 遗留风险

- GetResult 缺 `sections.*.items` 时对应图表/表诚实空态；需 Java 实包对照联调。
- 地图演示坐标与真实行政区划边界不一致（产品已知，非 GIS 终态）。

## CI/CD（必填）

| 项 | 值 |
|----|-----|
| 分支 | `lumen-ui-topic` / `gkx-orchestration` → `origin/dev` |
| commit（批 A） | `2b8630cbbb612eb9301f098518f467c24168aa39` |
| commit（批 B） | `e87b4df`（lumen-ui-topic）；编排仓 handoff 同批 |
| pipeline URL / ID | 待 GitLab |
| K8s rollout | 待 CI |
| dev 测试 | 区域 `/industry-center/regional` 指数/竞争力结果；诊断周期配置/结果业务态 |

## 可观测性

- 沿用既有 analysis / topic 请求链；本批无新增 `observability.ts` 埋点。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1–7 调用链 / Nebula / CI / demo 隔离 | ✅ |
| 8 诚实空 / 无 fixture 填数 | ✅ |
| 9 D9 评审挂点 / metric 入口 | ✅ |
| 10 D10 双栏、表格联动、Arco 表 | ✅ |
| 11 D12 不打 demo 服务 | ✅ |

## 涉及文件（批 B）

- `src/components/industry-center/IndustryRegionalResultBoard.vue`
- `src/components/industry-center/IndustryCycleResultBoard.vue`
- `src/components/industry-center/RegionalCompareMap.vue`（新）
- `src/utils/industryChainTask.ts`
- `src/utils/regionalCompareMapPoints.ts`（新）
- `src/utils/regionalCompareMapPoints.selfcheck.mjs`（新）
- `src/views/industry-center/IndustryDiagnosisPage.vue`
- `src/views/industry-center/IndustryRegionalPage.vue`
- `src/views/industry-center/industryDiagnosis.css`
- `src/views/industry-center/industryReplicaFix.selfcheck.mjs`

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 145000（批 A+B 走查+区域结果+样式修正估计，任务未全量完工） |
| model_used | composer（Cursor Agent） |
| actual_cost | 待账单核对 |
| cost_warn | green |
