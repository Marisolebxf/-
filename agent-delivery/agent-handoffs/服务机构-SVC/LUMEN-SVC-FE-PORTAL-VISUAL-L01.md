# LUMEN-SVC-FE-PORTAL-VISUAL-L01 · 门户五 Tab 视觉复刻（范围清单 + 五维）

> 日期：2026-08-18  
> Task：`LUMEN-SVC-FE-PORTAL-VISUAL-L01`  
> 总控 / 派单：`DEMO-SVC-ABCD-长任务总控.md` · `DEMO-SVC-FE-D-视觉复刻补单.md` · `DEMO-SVC-FE-D-总派单.md`  
> 对照：`templates/fe-replica-visual-dod.md` · `demo-ui-topic/src/app/pages/service-portal/*`  
> 上游有数叶：`LUMEN-SVC-FE-PORTAL-FULL-L01`（金路径绿 ≠ 本叶完成）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff 对齐 Demo 区块；未用 YAGNI 跳过 D8/D9/D10/评审/`USE_MOCK`；不贴 JSX；不 new 地图 |

## /goal 五 Tab 区块清单（对照 demo service-portal/*）

| Tab | 路由 | Demo 区块 | 本叶完成度 |
|-----|------|-----------|------------|
| 1 全球概况 | `/service-portal/overview` | 壳(面包屑/标题/五 Tab/产业级联/JudgmentStrip) · ReviewOnly 口径条 · KPI×3 · 历年趋势 · 类型环+规模四档 | ✅ |
| 2 产业分布 | `/service-portal/industry-distribution` | 口径条 · 六环节卡(序号/进度条/下钻) · KPI×3 · 领域×环节热力 | ✅ 结构齐；热力无矩阵诚实空 |
| 3 区域分布 | `/service-portal/region-map` | actions 全球⇄全国 · 口径条 · KPI×3 · 地图+排行(1.6fr/1fr) · others 注 | ✅；无 lat/lng 不伪造气泡 |
| 4 技术能力 | `/service-portal/capability-rank` | 口径条 · Top 表(彩色排名/标题摘要/得分条/画像+入篮) | ✅ |
| 5 深圳介绍 | `/service-portal/shenzhen` | KPI×3 · 趋势+类型 · 领域环节 · 十区地图+排行 · 重点机构卡墙+详情抽屉 | ✅；领域段无门面诚实空 |

## 复刻五维验收（R1–R5）

| # | 项 | 结果 |
|---|-----|------|
| R1 布局 | 五 Tab Demo 区块均有结构；一节点一套 layout | ✅ |
| R2 交互 | loading / 失败 Message / 空骨架 / 产业级联脏刷新 / Tab 切带 industry / 环节下钻 / 入篮 / 抽屉 URL `org` | ✅ |
| R3 样式 | `--sci-bg-page` 页底、KPI/环节/关键墙 token、JudgmentStrip、与兄弟门户同皮肤 | ✅ |
| R4 评审 | 只挂 `@/review`（`TraceInfoIcon` / `ReviewMetricBadges`）+ `IndustryReviewOnly` 口径条；关评审零泄漏口径条 | ✅ mount：`SVC-PT-OVERVIEW` / `SVC-PT-INDUSTRY` / `SVC-PT-REGION` / `SVC-PT-CAPABILITY` / `SVC-PT-SHENZHEN` 及分区 F01–F05 |
| R5 Mock | 开：`registerApiMock('svcPortalOverview'|…)`；关：只渲染 Java 实包，禁止 fixture 填数 | ✅ |

## 检索皮肤（V1–V7）

门户非查询 Hub；**不适用整页 Hero**。适用处：

| # | 项 | 结果 |
|---|-----|------|
| V1 | 页底 `var(--sci-bg-page)` / `#D8E7FC` | ✅ |
| V2 | Hub Hero | N/A（非检索 Hub） |
| V3 | 卡片/列表内部横向书写 | ✅ 能力榜 org-name / 重点机构卡 |
| V4 | 一节点一套 layout | ✅ 未叠 result-card 网格 |
| V5 | `min-width: 0` 防塌 | ✅ KPI/标题/卡片 |
| V6 | 空态诚实 / 有数同行 | ✅ |
| V7 | 无错误叠 class | ✅ |

工作区 W1–W3：本叶非分析工作区 → N/A。

## 偏离说明

- 领域×环节热力、深圳领域环节：门面无矩阵 → **诚实空骨架**（不本地造数）
- 区域/十区地图：门面无 lat/lng → `UnifiedLeafletMap` `presetLayers=false` 仅底图壳 + 提示，不伪造气泡
- `region_map.global` 与 `china` 同城池（上游 ADS）— FE 如实渲染

## 产物清单

| 产物 | 路径 |
|------|------|
| CSS | `repos/lumen-ui-topic/src/views/service-portal/servicePortal.css` |
| 壳 | `ServicePortalShell.vue`（JudgmentStrip） |
| 五页 | `ServicePortalOverview/IndustryDistribution/RegionMap/CapabilityRank/Shenzhen.vue` |
| 抽屉 | `KeyOrgDetailDrawer.vue` |
| 地图门控 | `components/map/UnifiedLeafletMap.vue`（`presetLayers`） |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-PORTAL-VISUAL-L01.md` |

## 验收证据

- [x] `node src/views/service-portal/servicePortalIndustry.selfcheck.mjs` → ok
- [x] 本叶 portal 文件 vue-tsc 无新增报错
- [x] commit + push `origin/dev`（见 CI 段）
- [ ] 外网截图人审（非下一叶闸门；联调闸门认 handoff+本清单）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 调用链 | 前端→Java→`/internal/*` | ✅ 只调 `/svc/topic/v1/service-portal/**` + `profile/get` |
| 可观测 | request / TraceInfoIcon | ✅ |
| D8 | Design / Arco | ✅ |
| D9 | 角标 / Q-SVC-010 | ✅ ReviewMetricBadges；不自造 ⓘ |
| D10 | 交互 | ✅ |
| D12 | 不调 demo-* | ✅ |
| 复刻五维 | R1–R5 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~11 万 |
| actual_cost | 估 <$5 |
| cost_warn | false |

## CI/CD

- 分支：`dev`
- commit：`404a607`
- pipeline：push 后 GitLab `lumen-ui-topic` tracking `origin/dev`
- 部署：跟踪 `origin/dev` → K8s

## 联调确认

联调通过：门户五 Tab 视觉区块按 Demo 清单铺齐；数据仍只消费 Java overview/ranking/profile；`USE_MOCK=false` 诚实空或实包。下一叶可开 `LUMEN-SVC-FE-ANALYSIS-VISUAL-L01`（依赖本叶 integration）。
