# LUMEN-SVC-FE-ENTRY-VISUAL-C1 · 产业服务链 ENTRY 视觉复刻

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：WORKSPACE-VISUAL-C1、E1 金路径伪绿、React merge 进 Vue。

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
| 说明 | 与派单 `/goal` 一致。未用「轻量/空壳」跳过 D8/D9/D10、SearchHub 布局、画像四段、门户图表骨架；对照 Demo class + IndustrySearchPage。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 对齐 demo service-portal/* + ServiceOrgSearchPage + OrgProfileDrawer；禁止 compress 代替对照。 |

## 范围与实现

`lumen-ui-topic` 纠正 ENTRY 视觉降级：查询页接 SearchHub + FilterPanel + flex 结果卡；门户五 Tab 子导航同构 + SectionPanel 骨架；画像抽屉四段结构化。只调 Java `/svc/topic/v1/service/**` 与 `/svc/topic/v1/service-portal/**`（D12）。

### 查询页 `/service-center/search`

- `SearchHub` 三模式 smart|org|advanced（URL mode 映射 keyword↔org）
- `FilterPanel` 高级筛选字段库
- 结果/推荐：`svc-org-search-card` **flex 横卡**（对齐 Demo `search-content-card`；**禁止**叠 `industry-search-result-card`）
- 对比篮 `service_org`、分析集合 sessionStorage、最近检索 localStorage
- `OrgProfileDrawer`：基本信息 / 领域覆盖条 / 技术力五维 / 近三年记录；缺段诚实空

### 门户五 Tab

- `ServicePortalShell`：`global-workbench-tabs` 子导航 + `--sci-bg-page`
- Overview：KPI 卡 + 趋势/类型饼/规模柱（有数据 VChart；无数据骨架诚实空）
- Industry：环节卡骨架 + 类型表 + 热力骨架
- Region：全球⇄全国 + Leaflet 壳 + 榜单图骨架
- Capability：Top 榜表 + 入篮/画像入口（无 JSON dump）
- Shenzhen：Demo 五块（100–104）骨架；有分段则图表，无数诚实空

## 视觉验收 V1–V7

| # | 项 | 结果 |
|---|---|---|
| V1 | 页底 `var(--sci-bg-page)` / `#D8E7FC` | ✅ 查询页 + 门户 shell |
| V2 | 检索 Hub Hero 与本仓企业/产业查询同皮肤 | ✅ 复用 `SearchHub` |
| V3 | 卡片内部标题+摘要横向；操作不漂 | ✅ `svc-org-search-card` flex 左文右分 |
| V4 | 一个节点一套 layout；不叠 result-card 网格 | ✅ 仅用 `svc-org-search-card`，无 `industry-search-result-card` |
| V5 | `min-width: 0` 仅在 flex 子项截断处 | ✅ `.svc-org-search-card-main` / title button |
| V6 | 推荐/结果空态诚实；有数则横卡结构 | ✅ 空 Empty；有数 2 列 flex 卡 |
| V7 | 推荐/结果 article class 不叠 result-card | ✅ selfcheck 断言 class 不含 result-card |

## 偏离说明（as-built）

| 项 | Demo | As-built | 理由 |
|---|---|---|---|
| 栈 | Arco React | Arco Vue | 禁止 React merge；语义+布局对齐 |
| RecommendationSection | 企业 ElementRecord | 同构 flex 卡 | 组件契约绑企业；布局对齐 Demo/Industry |
| SearchScaffold | Demo ElementSearchWorkbench | SearchHub+自建内容区 | 与 IndustrySearchPage 兄弟一致 |
| 门户假数据图 | Demo 演示聚合 | 门面有数才画图 | 诚实空，不造假折线/热力 |
| Leaflet 点位 | Demo 区域气泡 | UnifiedLeafletMap 壳 | 无 region 分段时不伪造业务气泡 |

## 产物清单

| 产物 | 路径 |
|---|---|
| 查询配置/模型 | `src/config/serviceOrgSearchConfig.ts` · `src/utils/serviceOrgSearchModel.ts` |
| 查询页+CSS | `src/views/service-center/ServiceOrgSearchPage.vue` · `serviceOrgSearch.css` |
| 画像抽屉 | `src/views/service-center/OrgProfileDrawer.vue` · `serviceOrgDrawer.css` |
| 门户五 Tab | `src/views/service-portal/*` |
| selfcheck | `src/utils/serviceOrgSearchModel.selfcheck.mjs` |
| 本 handoff | `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-ENTRY-VISUAL-C1.md` |

## 验收证据

| 项 | 结果 |
|---|---|
| selfcheck | ✅ `node src/utils/serviceOrgSearchModel.selfcheck.mjs` |
| type-check | ✅ `npm run type-check` |
| D12 | ✅ 仅 `/svc/topic/v1/**` |
| 无 JSON dump UI | ✅ 门户已移除 `<pre>` debug |
| 无裸 a-table 查询壳 | ✅ 查询页为卡片 |

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | 前端 → Java REST | ✅ `/svc/topic/v1/**` |
| 3 | Nebula | ✅ 本单不画图谱 |
| 4 | 可观测 | ✅ request `X-Trace-Id` |
| 5 | CI/CD | ✅ push `origin/dev` |
| 6 | demo 不 merge lumen | ✅ Vue 重写 |
| 7–8 | 共享聚合 / ADS·Mock | ✅ |
| 9 | D8 Design | ✅ 页底/主色/32px |
| 10 | D9 | ✅ KPI/技术力分 ReviewMetricBadges |
| D12 | 禁 demo-* | ✅ |

## CI/CD

- 分支：`lumen-ui-topic` `dev`
- commit：见 push 后 sha（本机提交含 `[agent:frontend-agent]`）
- pipeline：push → frontend:build → deploy ns=`dev`
- **不**宣称 E1 / e2e:chain-gold 绿

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 220000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 1.19 |
| cost_warn | green |

口径：`source: session_estimate`；80/20 × Sonnet 4.5 价表（$3/$15 per 1M）：`220000×0.8×3/1e6 + 220000×0.2×15/1e6 = 1.188`。

## 联调确认

**联调通过 / 联调确认**：视觉 C1 结构对齐 Demo（SearchHub 三模式、flex 卡、画像四段、门户五 Tab 骨架+图表区）；Java 契约仍走 `/svc/topic/v1/**`；空数据诚实空不造假 KPI。集群真数据待 facade/ADS 回填。本 agent **不**标 `done`（feature → `integration`）。

## 遗留风险 / 开放项

1. **WORKSPACE-VISUAL-C1**（下一叶）：分析/生态/招引工作区视觉。
2. 门户 `region_map` / `shenzhen` / 热力矩阵正式分段待 Python 回填。
3. 技术力分 Q-SVCCHAIN-01 正式口径待甲方确认。
