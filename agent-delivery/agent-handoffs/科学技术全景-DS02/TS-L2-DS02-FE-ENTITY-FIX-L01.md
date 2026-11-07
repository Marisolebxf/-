# TS-L2-DS02-FE-ENTITY-FIX-L01 · 全景 live 实体区/列表消费 graph.listRecords

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | task_type = bugfix，P1；registry 状态由 coordinator 推进，本叶不动 task-registry |

## Ponytail（coding 任务必填）

ponytail: full

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单一致。只加 `listRecords→GraphEntityRow` 映射与接线，实体类型筛选改 Arco `a-select`；未新造组件库/依赖。D8 Arco 优先已落实；未以 YAGNI 跳过 listRecords 真源 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 小 diff 前端 bugfix，未用 |

## 范围与实现

**问题清单**

- ENTITY-API as-built：`relations` 只有技术点间 `tech_rel`，实体在 `listRecords`。live 实体区仍走 `entityRowsFor(nodes, relations)`，后端有实体页面也不显示。
- 列表视图 live 用 `techPointListRecords` 从画布技术点推导，不消费 `graph.listRecords`（人/机构/论文/专利）。
- 实体类型筛选仍是原生 `<select>`，违反仓规 Arco 优先。

**修改内容**

1. `liveGraph.ts` 新增 `entityRowsFromListRecords`：过滤四类实体，映射 `typeLabel` / `typeKey` / `influence` / `id→graphNodeId`。
2. `buildLiveAnalysisContext` 在传入 `listRecords`（含空数组）时只消费该名单，不再从 nodes+relations 推实体。
3. `panorama/index.vue`：`liveAnalysis` 传 `graphResult.listRecords`；`liveListRecords` 改为 `filterLiveListRecords(graph.listRecords)`。
4. `GraphAnalysisPanel.vue`：实体类型筛选改为 Arco `a-select`（时间/排序仍原生，本叶最小 diff）。
5. `entityRanking.ts`：补 `人/人员 → person` 因子键与色板，避免 listRecords 类型标签漂色。
6. `GraphListRecord` 类型补可选 `influence`。
7. `liveGraph.selfcheck.mjs`：覆盖 listRecords 映射、优先于 nodes+relations、未选点空名单、页面接线与 a-select 锚点。

## 偏离说明

- 无。未改接口契约；未动 mock 轨种子路径。
- 列表视图在未选技术点时 `listRecords=[]`，列表为空（与 ENTITY-ARCH「未选点实体区空」一致）；不再用技术点名单顶替。

## 产物清单

| 仓 | commit | 说明 |
|----|--------|------|
| lumen-ui-science-pc | `b67de13d60afd4d87a5272d039c66aa4a177f08f` | `fix(panorama): live 实体区/列表消费 graph.listRecords [agent:frontend-agent]` |
| gkx-orchestration | （本 handoff 提交 SHA 见下方 CI/CD） | 仅本 handoff 文件 |

涉及文件（lumen-ui-science-pc）：

- `src/lib/graph/liveGraph.ts`
- `src/lib/graph/liveGraph.selfcheck.mjs`
- `src/lib/graph/entityRanking.ts`
- `src/types/panorama.ts`
- `src/views/situation/panorama/index.vue`
- `src/views/situation/panorama/components/GraphAnalysisPanel.vue`
- `src/views/situation/panorama/styles/demo-panorama.css`

## 验收证据

**测试结果**

| 命令 | 结果 |
|------|------|
| `node src/lib/graph/liveGraph.selfcheck.mjs` | 退出码 0，`liveGraph.selfcheck ok` |
| `pnpm type-check` | 退出码 0（`vue-tsc --build`） |
| `pnpm build` | 退出码 0（type-check + vite build 绿） |

用户本会话明确「放行，推」：自检绿后已 `git push origin/dev`（非 force）。未改他会话残留的 `vite.config.ts`。

## CI/CD（必填）

- 分支：`dev`（lumen-ui-science-pc / gkx-orchestration）
- 前端 commit：`b67de13d60afd4d87a5272d039c66aa4a177f08f`
- pipeline：push 后由 GitLab CI 触发（本叶提交时未等流水线结束）
- K8s rollout：前端仓 push → 既有 CI/CD 自动部署链
- registry：本叶 **不** 改状态；请 coordinator 据本 handoff 推进

## 遗留风险

- 关联强度：`listRecords` 无 `relationStrength`/`weight`（API 已说明），live Top5 按关联强度排序时分数多为 0；影响力排序仍可用 `influence`。
- 实体中文名依赖后端 `name_zh`；空名时页面可能显示编号（已知演示用例脚注，非本叶范围）。
- 页面端到端（选点后 Top5=61）待 QA 在 dev 复测。

## 架构合规自检（D1–D18）

| 条 | 结论 |
|----|------|
| D1 算法只在 Python | ✅ 前端只映射展示，不计算影响力 |
| D2 调用链 | ✅ 仍只打 Java `/display/**` |
| D3 NebulaGraph | N/A 前端不接图 |
| D4 可观测 | ✅ 未改埋点路径 |
| D5 CI/CD | ✅ push `origin/dev` |
| D6 demo 只读 | ✅ 未 merge demo |
| D7 共享聚合核心 | ✅ 前端只调 Java |
| D8 Design/Arco | ✅ 实体类型筛选改 `a-select` |
| D9 数据血缘 | ✅ 未新造 metric；既有 ⓘ / MockBadge 保留 |
| D10 交互 | ✅ 筛选语义不变，仅控件换 Arco |
| D12 demo/lumen 隔离 | ✅ 无 demo 服务依赖 |
| D14 / D16 / D17 / D18 | N/A 或 ✅ 无写死 fixture 填实体 |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~80k（估） |
| model_used | Composer（Cursor agent） |
| actual_cost | ~$1.5（估） |
| cost_warn | false |
