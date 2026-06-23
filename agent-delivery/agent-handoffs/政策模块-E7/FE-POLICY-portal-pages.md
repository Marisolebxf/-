# FE-POLICY-portal-pages —— 政策扶持门户六页（POLICY-PROTO-L06）

- 角色：frontend-agent（Convoy worker，与分析层同仓同文件集归一执行）
- 仓：`demo-ui-topic`（React + Vite）  分支：`feat/policy-elements-build`（未直推 main）
- 任务：POLICY-PROTO-L06 门户政策扶持六页（新建 `src/app/pages/policy-portal/`）
- 状态：✅ 已完成，`npm run build` 绿
- 日期：2026-06-23  ·  commit 标记：`[agent:frontend]`

---

## 1. 路由表

| 页面 | 路由 | 组件文件 | 导航入口（Layout «门户-政策扶持»）|
|---|---|---|---|
| B1 政策扶持概况 | `/policy-portal/overview` | `PolicyPortalOverview.tsx` | 政策扶持概况 |
| B2 政策地图（Leaflet）| `/policy-portal/map` | `PolicyPortalMap.tsx` | 政策地图 |
| B3 政策产业覆盖（AntV G6）| `/policy-portal/industry-coverage` | `PolicyPortalIndustryCoverage.tsx` | 政策产业覆盖 |
| B4 政策力度排名 | `/policy-portal/intensity-rank` | `PolicyPortalIntensityRank.tsx` | 政策力度排名 |
| B5 最新政策动态（时间线）| `/policy-portal/latest` | `PolicyPortalLatest.tsx` | 最新政策动态 |
| B6 深圳政策对比 | `/policy-portal/shenzhen` | `PolicyPortalShenzhen.tsx` | 深圳政策对比 |

> `routes.tsx` 新增 `/policy-portal/*`（含 `/policy-portal` → overview 重定向）；`Layout.tsx` 新增「门户-政策扶持」导航组（6 项）。**未破坏现有路由 / 导航**。

---

## 2. 组件清单（新增 / 复用）

### 新增门户骨架 `pages/policy-portal/portalShared.tsx`
- `PolicyPortalShell`：UserLevelProvider + 面包屑 + JudgmentStrip 结论 + ContextBar(enhanced，产业多选/时间/区域)
- re-export 分析层 `PolicyMetricCard` / `usePolicyDetailDrawer` / `SecondaryAnalysisTabs` / `POLICY_COLORS` / `LEVEL_COLOR` / `POLICY_TRACK`（两层指标卡 ⓘ/🧪/⚠️ 与配色一致）
- 复用基础层 `JudgmentStrip` / `SectionPanel`（development/portalShared）

### 新增可视化组件
- `PolicyLeafletMap.tsx`（**Leaflet**）：浅色底图(CARTO Positron) + **比例圆点**(量=大小, 蓝梯度=力度) + 图例 + 点选下钻回调。用 `circleMarker` 矢量规避默认 marker 图标 404。
- `PolicyChainGraph.tsx`（**AntV G6 v5**）：产业链 DAG（`antv-dagre` 横向布局），节点蓝梯度=覆盖度，缺口(<40%)红描边，点选节点回调，图例。

### 各页组件
| 页 | 关键组件 / 图表 |
|---|---|
| B1 | 级别 Tab(全国/省级/市级) · MetricCard×4 · 级别分布环形 · 类型分布条形 · 时序折线(2025 断档 markArea) · 明细表(点选→画像) |
| B2 | scope 切换(全国/深圳各区) · **Leaflet 比例圆点地图** · MetricCard×3 · 区域下钻面板(点选圆点→相关政策列表) |
| B3 | **G6 产业链覆盖图** · MetricCard×3 · 上/中/下游覆盖率条形 · 缺口清单 / 节点详情(点选切换) |
| B4 | Top3 奖牌卡 · MetricCard×3 · 力度条形榜(蓝梯度按位次加深) · 排名表(力度排序) |
| B5 | MetricCard×3 · 级别筛选 · **Arco Timeline**(级别色点 + 状态标签, 点选→画像抽屉) |
| B6 | **深圳各区 Leaflet 地图** · 区域多维雷达(深圳主蓝高亮 vs 标杆) · 三维框架摘要卡(短板分色) |

---

## 3. metric_id 映射

| 页 | 指标卡 | metric_id |
|---|---|---|
| B1 | 政策总量 | `M_POLICY_TOTAL_COUNT` |
| B1 | 国家级政策 | `M_POLICY_LEVEL_DIST` |
| B1 | 有效政策占比 | `M_POLICY_VALIDITY_RATE` |
| B1 | 发布连续性 | `M_POLICY_TIMESERIES` |
| B2 | 覆盖区域数 | `M_POLICY_NATIONAL_DIST` |
| B2 | 视图内政策量 | `M_POLICY_TOTAL_COUNT` |
| B2 | 热点区域 | `M_POLICY_INTENSITY_INDEX` |
| B3 | 平均覆盖度 / 上游覆盖率 | `M_POLICY_INDUSTRY_COVERAGE` |
| B3 | 覆盖缺口环节 | `M_POLICY_INDUSTRY_FIT` |
| B4 | 榜首力度指数 | `M_POLICY_INTENSITY_INDEX` |
| B4 | 纳入排名区域 | `M_POLICY_NATIONAL_DIST` |
| B4 | 平均产业覆盖率 | `M_POLICY_INDUSTRY_COVERAGE` |
| B5 | 动态总数 / 2026 新增 | `M_POLICY_TOTAL_COUNT` / `M_POLICY_TIMESERIES` |
| B6 | 深圳政策量 / 最密区 | `M_POLICY_SZ_DIST` |
| B6 | 综合得分 | `M_POLICY_SUPPORT_STRENGTH` |

> 数字旁均挂 ⓘ MetricSpecCard；Wave0 → 🧪 MockBadge；`M_POLICY_INTENSITY_INDEX` 等口径待定 → ⚠️ PendingBadge。

---

## 4. Mock 数据

- `src/app/mock/policy/policyPortalData.ts`：复用 `policyData.ts` 主数据做门户轻聚合派生
  - `PORTAL_KPI`（B1 盘面）、`INTENSITY_RANK`（B4，按 intensity 倒序 + 覆盖派生）、`LATEST_POLICIES` + `groupByMonth`（B5）
- 地图坐标来自 `POLICY_NATIONAL_DIST`(31 省含 lng/lat) / `POLICY_SZ_DIST`(9 区)
- G6 数据来自 `INDUSTRY_CHAIN_NODES` + `CHAIN_EDGES` + `STAGE_COVERAGE`
- 不新增独立真值源，避免与 `policyData` 口径漂移；Wave 1 切 `/v1/policy/*`

---

## 5. Design.md §14 检查清单 + 验收 6 条对照

| 项 | 结论 | 说明 |
|---|---|---|
| 技术栈 + 禁 antd | ✅ | 仅 `@arco-design/web-react`+icon；图表 ECharts / **地图 Leaflet** / **关系图 G6** |
| 主色 / 底色 / 方向色 / 要素色 | ✅ | DOM `var(--sci-*)`；ECharts/Leaflet/G6 取色为 token 镜像 hex（canvas 限制）|
| token 不硬编码 | ✅ | 同上，已注释说明 canvas 取色策略 |
| D9 ⓘ/🧪/⚠️ | ✅ | 复用同一 PolicyMetricCard，两层一致 |
| 结论先行 | ✅ | 每页 PolicyPortalShell 顶部 JudgmentStrip |
| 门户层模式对齐 | ✅ | 仿 development/portalShared（PortalShell + 派生 data）|

---

## 6. 架构合规自检（§2 十条）

1. 算法只在 Python ✅  2. 不越层 ✅（纯 mock）  3. 图谱 NebulaGraph ✅（关系图为前端 G6 可视化，非图数据库）  4. 可观测性 ✅（`POLICY_TRACK.GEO_DRILLDOWN` 等埋点）  5. CI/CD ✅  6. demo2 只读 ✅  7. 共享聚合核心 ✅  8. ADS 先行 + Mock ✅  9. 前端规范 D8 ✅  10. 数据血缘 D9 ✅

---

## 7. 构建结果

- `npm run build`：**✅ 成功**（vite v6.3.5，4790 modules，built ~57s，exit 0）—— 含 Leaflet + AntV G6 v5 打包通过
- 新文件 ReadLints **0 error**
- 依赖：`leaflet@^1.9.4` + `@types/leaflet@^1.9.21` + `@antv/g6@^5.0.49` 已在 `package.json`（本次仅引入必需库）

---

## 8. 阻塞与风险

- 🟡 **Leaflet 降级说明**：未接省/市 GeoJSON 多边形，B2/B6 先以「**比例圆点 + 蓝梯度**」平面降级（非分级填色 choropleth）。底图瓦片需运行时联网；离线时仅底图灰、圆点正常渲染。待 GeoJSON 资产 + 三级下钻人工评审后升级。
- 🟡 **G6 v5 事件**：节点点选用 `NodeEvent.CLICK` + `e.target.id` 取节点 id；v5 API 行为以构建通过为准，建议联调期人工点测确认下钻命中。
- ⚠️ **QPOL-02 力度指数口径**：B4 排名按临时加权 Mock，UI 已挂 ⚠️；待甲方确认。
- ❌ **落地实效性数据待采购**：B6 三维摘要落地实效性维 Mock 代理。
- 评审 gate：本次按派单例外**跳过人工评审**；上线前仍需 UX/UI/PM 人工评审 + 真实瓦片/GeoJSON 接入复测。
