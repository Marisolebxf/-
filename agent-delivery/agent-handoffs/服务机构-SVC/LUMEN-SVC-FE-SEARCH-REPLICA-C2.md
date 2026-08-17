# LUMEN-SVC-FE-SEARCH-REPLICA-C2 · 服务机构查询完整复刻 ElementSearchWorkbench

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：门户/工作区其它页、E1 金路径伪绿、React merge 进 Vue。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权「不必再问」；lock 24h。本单完工转 **integration**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照 Demo 一次闭合；未用「轻量表格/半成品壳」跳过 workbench / RecentSearchPanel / 结果卡密度 / D9。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 headroom MCP；对照 Demo + 外网验收 URL，禁止 compress 代替对照。 |

## 范围与实现

`lumen-ui-topic` `/service-center/search` 按 Demo `ServiceOrgSearchPage.tsx` 完整复刻：

1. **三段 ElementSearchWorkbench**：`query` / `recent` / `content`；CSS 对齐 `theme.css`（`.element-search-workbench`、`.search-content-surface`、workbench 内 Hero）。
2. **独立 RecentSearchPanel**（`hideRecentHistory` 关掉 Hub 内嵌最近检索）。
3. **未搜推荐**标题「技术力领先机构」；结果卡密度：tags、城市/成立/领域、专利专家案例标准、技术力分+D9、行级 `ServiceOrgBasketButton` + 加入分析集合。
4. **OrgProfileDrawer** + URL `?org=`（query 同步）。
5. **高级筛选**整页 `FilterPanel`（`viewState` editing/result）+ 面包屑。
6. 只调 Java `/svc/topic/v1/service/**`（D12）。

### 硬对照闭合表

| # | 项 | 结果 |
|---|---|---|
| 1 | ElementSearchWorkbench 三段 + CSS | ✅ |
| 2 | RecentSearchPanel 独立 | ✅ |
| 3 | 推荐卡/结果卡密度 + BasketButton + 分析集合 | ✅ |
| 4 | OrgProfileDrawer + `?org=` | ✅ |
| 5 | FilterPanel page + 面包屑 | ✅ |
| 6 | 外网验收 | ⏳ push 后等部署再验 http://111.198.38.90:50892/service-center/search |

## 视觉验收 V1–V7

| # | 项 | 结果 |
|---|---|---|
| V1 | 页底 `var(--sci-bg-page)` / `#D8E7FC` | ✅ `.svc-org-search-page` |
| V2 | 检索 Hub Hero 与企业/产业同皮肤 | ✅ workbench + `.svc-org-search-page` 选择器 |
| V3 | 卡片内部标题+摘要横向；操作不漂 | ✅ `search-content-card` + flex 左文右分 |
| V4 | 一个节点一套 layout；不叠 result-card 网格 | ✅ 无 `industry-search-result-card` |
| V5 | `min-width: 0` 仅在 flex 子项截断处 | ✅ `.svc-org-search-card-main` / title button |
| V6 | 推荐/结果空态诚实；有数则横卡结构 | ✅ Empty + 2 列 flex 卡 |
| V7 | 推荐/结果 article class 不叠 result-card | ✅ selfcheck 断言 |

## 偏离说明（as-built）

| 项 | Demo | As-built | 理由 |
|---|---|---|---|
| 栈 | Arco React | Arco Vue | 禁止 React merge；语义+布局对齐 |
| 推荐数据 | 本地 Mock 按 techScore 排序 | Java `seed=recommend` | D12；空则诚实空，不伪造 |
| ReviewOnly 演示脚注 | Demo ReviewOnly | TraceInfoIcon / ReviewMetricBadges | 本仓评审层门控 |

## 产物清单

| 产物 | 路径 |
|---|---|
| 查询页 | `src/views/service-center/ServiceOrgSearchPage.vue` · `serviceOrgSearch.css` |
| BasketButton | `src/views/service-center/ServiceOrgBasketButton.vue`（抽屉复用） |
| workbench 组件 | `ElementSearchWorkbench` / `RecentSearchPanel` / `SearchContentSurface` |
| 主题 CSS | `src/assets/search-workspace.css` |
| FilterPanel viewState | `src/components/filter/FilterPanel.vue` |
| selfcheck | `src/utils/serviceOrgSearchModel.selfcheck.mjs` |
| 本 handoff | `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-SEARCH-REPLICA-C2.md` |

## 验收证据

| 项 | 结果 |
|---|---|
| selfcheck | ✅ `node src/utils/serviceOrgSearchModel.selfcheck.mjs` |
| type-check | ✅ `npm run type-check` |
| D12 | ✅ 仅 `/svc/topic/v1/**` |
| 外网视觉 | ⏳ 部署后人工验 |

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | 前端 → Java REST | ✅ |
| 3 | Nebula | ✅ 本单不画图谱 |
| 4 | 可观测 | ✅ request `X-Trace-Id` |
| 5 | CI/CD | ✅ push `origin/dev` |
| 6 | demo 不 merge lumen | ✅ Vue 重写 |
| 9 | D8 Design | ✅ |
| 10 | D9 | ✅ `M_SVC_ORG_TECH_SCORE` ReviewMetricBadges |
| D12 | 禁 demo-* | ✅ |

## CI/CD

- 分支：`lumen-ui-topic` `dev`
- commit：见 push 后 sha（`[agent:frontend-agent]`）
- pipeline：push → frontend:build → deploy ns=`dev`
- 验收 URL：http://111.198.38.90:50892/service-center/search
- **不**宣称 E1 / e2e 绿

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 2.5 |
| cost_warn | green |

## 遗留风险

- 外网部署有 2–5 min 滞后；推荐接口空时仅诚实空，不回落 Demo Mock。
- 高级筛选最近检索恢复不还原 DSL 条件（与现仓 Industry 行为一致；Demo 可还原）——若监管要求可再开叶。
