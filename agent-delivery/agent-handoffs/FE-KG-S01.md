# FE-KG-S01 · 科技知识图谱前端模块基座（分析/指标/算法/服务四页壳）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 派单默认强度；未用 YAGNI 跳过 D8/D9/D10、可观测埋点与架构铁律（四页仅页壳，未涉调用链/Nebula）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载。 |

## 问题清单

- 无阻塞问题。

## 修改内容

**仓 1：`repos/lumen-ui-science-pc`（本任务全部代码产物）**

- 基座（commit `d1c3132`）：`src/api/knowledgeGraph.ts`（4 端点 defineApi + contractPending）、`src/types/knowledgeGraph.ts`、`src/mock/modules/knowledgeGraph.ts` + `knowledgeGraphSeed.ts`（种子冻结自 demo `tech-knowledge-graph`，`@ts-nocheck` 防漂移）、`src/mock/register.ts` 注册、`src/views/knowledge-graph/kgL6.ts`（L6 序列 400–454 映射）、`components/KgL6SectionTitle.vue`、`useKnowledgeGraphTrack.ts`（可观测埋点）、`src/router/menu.ts` 四页路由接线（graph-analysis/indicators/algorithms/service）、`src/styles/demo-knowledge-graph.css`。
- 头部统一（本次，孔东走查反馈）：四页重构为 `PageTabFrame` + `#header` 插槽，新增 `components/KgPageHeader.vue`（对齐政策跟踪 `pol-track-page-header` 布局语义：h2 20px 标题行 + 副标题 + actions）、`components/KgKpiCard.vue`（PolicyStatCard 同构变体：ⓘ 挂点 + 大数字/单位/趋势 + MockBadge 右上）、`components/kgPageHeader.css`（`kg-track-page-stats-row--cols-4` KPI 栅格，含 992/576 响应式降列）。
- 各页头部内容：分析页 4 KPI（种子 `knowledgeGraphKPIs` 含趋势）；指标页 3 告警（demo 冻结文案）+ 4 KPI（demo 冻结值）；算法页标题+副标题（demo 无 KPI，三算法 Radio → 三页签承载）；服务页 4 KPI（`serviceKpis` 种子，D9 `metricId` 挂点）。
- 自检 `kg.selfcheck.mjs` 新增第 7 组断言：四页必须 PageTabFrame + KgPageHeader + #header。

**仓 2：`gkx-orchestration`（本 handoff + task-registry 状态推进）**

## 测试结果

- `node src/views/knowledge-graph/kg.selfcheck.mjs` ✅ 9 组断言全绿
- `pnpm type-check` ✅
- `pnpm build` ✅（43s）
- 浏览器目检（本地 dev 5199）：四页头部与政策全景页对照同构（标题行 → KPI 栅格 → 页签），截图已附会话记录。

## 遗留风险

- Java REST `/kg/v1/*` 契约未冻结（contractPending），`USE_MOCK=true` 双轨运行；后端联调对齐后切 `USE_MOCK=false`（空壳显式报错不挡页）。
- 服务页 4 KPI 的 `metric_id` 沿用 demo 种子 `M_KG_SVC_*` 系；registry 正名对齐 `M_SCIUI_KGSVC_*` 系待指标注册表确认（不阻塞联调）。
- 四页正文均为占位（a-empty + L6 叶清单），整页复刻由 FE-KG-01A/02A/03A/04A 批次填充。

## CI/CD（必填）

- 分支：`dev`
- commit：`d1c3132`（基座）+ `0020aff`（AGENTS 孔东限定）+ 本次头部统一 commit（见 git log）
- pipeline URL / ID：CI 由 push 自动触发（lumen-ui-science-pc dev 管线）
- 部署 namespace / 镜像 tag：K8s dev（CI 产物）
- K8s rollout：待 CI（push 后自动）
- dev 测试 URL / 命令与结果：`/graph/graph-analysis`、`/graph/graph-indicators`、`/graph/graph-algorithms`、`/graph/graph-service`（本地 dev 目检通过；K8s dev 上线后走查）

## 可观测性（建议）

- OTEL_SERVICE_NAME：前端 `observability.ts` 链路（`useKnowledgeGraphTrack` 4 页 page-mounted + algo-switch 埋点已埋）
- traceId（dev 抽样）：N/A（mock 双轨，无真实 REST 调用）
- Tempo / Loki：无（前端埋点，等 BE 接通后联动）

## 涉及文件

- `repos/lumen-ui-science-pc/src/api/knowledgeGraph.ts`
- `repos/lumen-ui-science-pc/src/types/knowledgeGraph.ts`
- `repos/lumen-ui-science-pc/src/mock/modules/knowledgeGraph.ts`、`knowledgeGraphSeed.ts`、`register.ts`
- `repos/lumen-ui-science-pc/src/views/knowledge-graph/**`（四页 index.vue + components/* + kgL6.ts + useKnowledgeGraphTrack.ts + kg.selfcheck.mjs）
- `repos/lumen-ui-science-pc/src/router/menu.ts`
- `repos/lumen-ui-science-pc/src/styles/demo-knowledge-graph.css`
- `gkx-orchestration/agent-delivery/agent-handoffs/FE-KG-S01.md`（本文件）
