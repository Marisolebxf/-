# POL-L2-DS11-VIZ-GAPFILL-L02-FE · Tab1 七可视化块真轨接线 · handoff

> [agent:frontend-agent] · 2026-11-12 · 仓 `lumen-ui-science-pc`（dev，未 commit 未 push，产物停本地工作区等 fe-manual-confirm-push 人工确认）
> 强度：ponytail full
> 监管：human:淮政玮（主会话代认领 in_progress；本会话未碰 task-registry MCP）

## 1. 范围与实现（对照接线说明书 §2 七块）

端点契约（DATA 单 §8.1 拍板 ③）：`GET /display/v1/policy/evaluation/viz?block=<key>` → `R.ok({records})`，行 = 七张 `gapfill_policy_eval_viz_*` 表列经 element DAO camel 形。七 fetch 全部落 `src/api/policyEvaluationViz.ts`，`defineApi` + `optional:true`（404/501 降级不登出）。

| # | 块 | 组件 | 接线改动 | 数值坑修复 |
|---|---|---|---|---|
| 1 | 评估指标体系卡 | `analysis/index.vue` 内联 | `fetchPolicyEvalVizMetric` → `assemblePolicyEvalVizMetricItems`；列表与雷达同读这批（indicator=label、value=score、weight） | — |
| 2 | 三联画像 | `PortraitTrio.vue` | `fetchPolicyEvalVizPortrait` → `assemblePolicyEvalVizPortraitItems`（tags 顿号拆、`detail_metrics_text` 按「；」分对、「、」拆 label/value、`detail_highlights_text` 按「；」分条） | — |
| 3 | 地理分布 | `GeographicMapPanel.vue` | `fetchPolicyEvalVizGeo` → `assemblePolicyEvalVizGeoRegions`（name/value/coord/policies）；保留挂载后 resize 兜底 | — |
| 4 | 分地区落实率 | `ImplementationByRegion.vue` | `fetchPolicyEvalVizRegionImpl` → `assemblePolicyEvalVizImplRows`；**0 值行分支**：`rate=0` 渲染 `0%` 文案 + 进度条轨道可见（模板 #rate 槽补分支） | ✔ FIX-A |
| 5 | 话题热力 | `TopicHeatmapWithSentiment.vue` 热力部 | `fetchPolicyEvalVizTopicHeat` → `assemblePolicyEvalTopicHeat`（topics[]/months[]/values 矩阵；缺格 null 不补 0，null 格不进系列） | ✔ FIX-B：visualMap 50–100 写死 → 行值域 `floor(min)/ceil(max)` 派生（max≤min 时 +10 兜底） |
| 6 | 情感分布 | 同组件情感部 | `fetchPolicyEvalVizTopicSentiment` → `assemblePolicyEvalSentiment`（scope_kind=总体→环形 pick() 防护；分话题→堆叠柱；闭集外行丢弃） | ✔ FIX-C：`pieOption` 补 undefined 防护（无总体行 → null → 空态，不喂 undefined 给 pie data） |
| 7 | 产业气泡 | `analysis/index.vue` bubbleOption | `fetchPolicyEvalVizBubble` → `assemblePolicyEvalBubble`（四元组 + categories 行去重） | ✔ FIX-D：轴范围 60–100 写死 → `xRange/yRange` 行值域派生；**行<2 不画**（`bubbles.length < 2` 分支） |

双轨语义：`USE_MOCK=true` 七块种子直出不动（冻结 demo 视觉，组件内 `if (USE_MOCK) return props/seed` 三段式保留）；`USE_MOCK=false` 有行渲染 / 无行保留 FIX-03 诚实空态文案（「无读面出处…」）；接口失败**本块置空不清其它块**（七个独立 `.catch(() => { xRows.value = [] })`，自检断言逐点核对）。

## 2. 数值坑修复清单（任务契约四项全修）

1. **FIX-A**（`ImplementationByRegion.vue`）：0 值率行不再被吞，`percent=0` 显式渲染 `0%` 且进度条轨道可见。
2. **FIX-B**（`TopicHeatmapWithSentiment.vue` 热力）：visualMap min/max 从行值派生；原写死 50–100 会把 <50 行值压成同色。
3. **FIX-C**（同组件情感）：`pieOption` 对 `effectiveSentiment` 判空 + 三分类 `pick(v, fallback)` 数值防护。
4. **FIX-D**（`index.vue` 气泡）：X/Y 轴 min/max 从行值派生（`assemblePolicyEvalBubble` 返回 `xRange/yRange`）；单值域退化 max=min+10；行 <2 整卡空态不画。

## 3. 新增文件

- `src/api/policyEvalVizRows.ts` — 七行形状（camel 主 + snake 兜底）+ 组装纯函数 + `policyEvalVizRowsOf<T>` 信封解包 + `policyEvalVizMetaOf` 行级血缘（is_mock/pending_ref/gap_item）。**零 import**：node 直测友好（`--experimental-strip-types`），组件经 `policyEvaluationViz.ts` re-export 消费。
- `src/views/policy/analysis/VizRowLineageBadges.vue` — D9 角标三件套：ⓘ（source_table/gap_item 卡）、🧪（行 is_mock=1）、⚠️（pending_ref，如 metric 块 QPOL-02）。经 `useReviewStore().reviewMode` 自闸门控；MockBadge 停用文案未新增（仅保留既有挂载）。
- `src/views/policy/analysis/POL-L2-DS11-VIZ-GAPFILL-L02-FE.test.mjs` — 专用自检（见 §5）。

## 4. 工程验证（实跑证据）

| 门 | 结果 |
|---|---|
| `pnpm type-check`（vue-tsc --build） | **exit 0，0 error** |
| `node --experimental-strip-types src/views/policy/analysis/POL-L2-DS11-VIZ-GAPFILL-L02-FE.test.mjs` | **22 组断言全绿 ✓**（九节：七块行→渲染映射、0 值行、缺格 null、值域派生、退化轴、行<2 不画、空行→空态、失败隔离七置空点、信封解包、API 层契约七 fetch/block 闭集/行形状真源、USE_MOCK 三段式分支保留） |
| `node --experimental-strip-types src/views/policy/analysis/FE-POL-02A.test.mjs`（回归） | **35 组断言全绿 ✓** |
| `node --experimental-strip-types src/views/policy/simulation/simulationLive.test.mjs`（回归） | **通过 ✓** |
| `pnpm build` | **exit 0，✓ built in 3m 32s**（仅 chunk>500kB 既有警告，非本任务引入） |

## 5. 顺带修复（dev HEAD 既有破损，挡 type-check 门，已最小修复）

`f740bc5`（上一个会话，234 live）在 `EstimateWorkbench.vue` 引用了 `similarPolicyItems` / `termKpiItems`，但漏在 `simulationLive.mjs` 里加导出 → dev HEAD type-check 本来就红（非本任务改动面）。因 DoD 要求 type-check 0 error，按消费处形状（`{name,match,effect}` / `{term,gdp,industry,innovation}`，解析不出→[]→空态）补两个最小导出（`flatMap` 纯净收窄，vue-tsc 无 null 联合）。语义与组件既有空态文案（「暂无相似政策」「暂无短中长期效果」）一致，无行为变更。

## 6. 架构合规自检（公约 §2 逐条）

| 铁律 | 结论 |
|---|---|
| D8 前端栈（Arco/ECharts/既有依赖） | ✅ 只用仓内已有 Arco + VChart（`@/config/echarts` 按需注册），零新依赖、零配置文件改动 |
| D9 数据血缘 | ✅ 七块数字/图表旁 ⓘ+🧪+⚠️（`VizRowLineageBadges`，reviewMode 自闸）；无 metric_id 的块不错挂异义指标（接线说明书 §4.3）；MockBadge 无新增文案 |
| 双轨 / 禁 fixture | ✅ USE_MOCK=true 种子冻结不动；false 下无行即空态，未造数；失败本块置空不清其它块（自检第 8 节断言） |
| D12 demo/lumen 隔离 | ✅ 只在本 lumen 仓作业，未读改 demo 仓、未引 demo 服务 |
| 调用链 | ✅ 仅前端 → Java REST `/display/v1/policy/evaluation/viz`，未越层直连 Python |
| 诚实性 | ✅ 空态文案保留 FIX-03 原文；缺格 null 不补 0；0 值行合法渲染；无伪闭合 |
| git 纪律 | ✅ 未 commit / 未 push（fe-manual-confirm-push 闸门）；未碰 .gitignore/package.json/vite.config |

## 7. 文件清单（git status as-is）

修改（8）：
- `src/api/policyEvaluationViz.ts`（+111：七 fetch + vizGet + block 闭集 + re-export policyEvalVizRows）
- `src/views/policy/analysis/index.vue`（块1/块7 接线 + FIX-D + VizRowLineageBadges；import 三处去重）
- `src/views/policy/analysis/PortraitTrio.vue`（块2 接线）
- `src/views/policy/analysis/GeographicMapPanel.vue`（块3 接线）
- `src/views/policy/analysis/ImplementationByRegion.vue`（块4 接线 + FIX-A）
- `src/views/policy/analysis/TopicHeatmapWithSentiment.vue`（块5/6 接线 + FIX-B/C）
- `src/views/policy/analysis/FE-POL-02A.test.mjs`（6a 节断言对齐 L02 as-built）
- `src/views/policy/simulation/simulationLive.mjs`（顺带修复 §5：+35 两导出）

新增（4）：
- `src/api/policyEvalVizRows.ts`
- `src/views/policy/analysis/VizRowLineageBadges.vue`
- `src/views/policy/analysis/POL-L2-DS11-VIZ-GAPFILL-L02-FE.test.mjs`
- （本 handoff，编排仓侧）

## 8. 遗留问题

1. **推送待人工确认**：改动停本地工作区，按 `fe-manual-confirm-push` 等用户明确说「推」后由主会话执行 commit+push（commit 需带 `[agent:frontend-agent]`）。
2. **API 分册缺口**（接线说明书 §4.1）：`/viz` 端点需补进 `POL-L2-DS11-VIZ-API.md`，归 BE 单交付时一并补，非本任务范围。
3. **信封兜底双保险**：FE 侧 `policyEvalVizRowsOf` 同时认 `records`/`items`，若 BE 最终只发其一也兼容；不需要 BE 再改。
4. `pnpm build` 的 chunk>500kB 警告为仓内既有状态，未处理（不在任务范围）。
