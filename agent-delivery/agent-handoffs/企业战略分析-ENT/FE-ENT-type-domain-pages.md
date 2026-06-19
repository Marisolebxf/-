# Handoff · WP3d 修偏离：E-21/E-22 改回独立页面 + 独立路由 + 侧边栏入口

| 属性 | 内容 |
|------|------|
| 任务 | WP3d（修偏离）|
| 角色 | frontend-agent |
| 仓 / 分支 | `topic_demo` · `feat/ent-elements-build`（未 push）|
| 关联验收 | E-21（P1 重点企业类型分析）、E-22（P2 重点企业领域分布分析）|
| 真源 | `ENT-IA.md` §2.2/§3.2/§1、`ENT-functional-design-v2.md` §9.2/§9.3 |

---

## 1. 修正了哪项偏离

- **偏离来源**：上一波 WP3c 把 **E-21 重点企业类型分析** 与 **E-22 重点企业领域分布分析** 并入了 `EnterpriseOverview` 的「结构洞察」`analysis-tabs`（`EnterpriseOverview.tsx` 旧注释自称「当前分支未单设独立路由，按 FDS v2 §4.2 并入承载」）。
- **为何属偏离**：权威 IA `ENT-IA.md` §2.2/§3.2 明确 P1=`/enterprise/type-distribution`（E-21）、P2=`/enterprise/domain-distribution`（E-22）是**独立页面 + 独立路由（标"新增"）**；IA §1 仅授权 `.3.3+.3.4`、`.3.6+.3.7` 两对做"页面合并 Tab 承载"，`.3.1/.3.2`（E-21/E-22）**不在授权合并之列**，必须独立可验收。FDS v2 §14.1 亦把「P1 类型分析独立页」「P2 领域分布独立页」列为 P0-1/P0-2 待建。
- **本 WP 修正**：把 E-21/E-22 拆为两个独立页面 + 独立路由 + 侧边栏入口；`EnterpriseOverview` 仅保留 P0 概览级摘要 + 下钻入口（去重）。

---

## 2. P1/P2 落点与路由

| # | 验收点 | 页面文件（新增） | 路由（新增） | 侧边栏入口（新增） |
|---|--------|-----------------|-------------|-------------------|
| P1 | E-21 | `src/app/pages/enterprise/EnterpriseTypeDistribution.tsx` | `/enterprise/type-distribution` | 企业分析 → 「重点企业类型分析」 |
| P2 | E-22 | `src/app/pages/enterprise/EnterpriseDomainDistribution.tsx` | `/enterprise/domain-distribution` | 企业分析 → 「重点企业领域分布分析」 |

### P1（E-21）实现要点（IA §4 骨架：ContextBar·SearchableCascadeFilter·MapPanel·ChartPanel·DataTable）
- `AnalysisShell` 包壳（ContextBar / 角色上下文 S1/S2 / 结论先行 JudgmentStrip）。
- **SearchableCascadeFilter**：产业级联（Arco `Cascader`）+ 企业类型多选（Arco `Checkbox.Group`）+ 重置/确认 + 已选摘要。
- **国/省/市三级下钻**：Arco `Radio.Group`（国/省/市）触发 `GEO_DRILLDOWN` 埋点；MapPanel 为 Wave 0 占位区块（指标条形 + 🧪 MockBadge，**未引新依赖**，Wave 1 接 Leaflet）。
- 二级 **analysis-tabs**（数量/占比/集聚指数）切换地图指标视图。
- 类型结构 ECharts（饼）+ 区域×类型堆叠柱 + 区域清单 **DataTable**（Arco `Table`：数量/上市占比/高企占比/集聚指数，可排序，导出）。
- 统计数字配 **MetricSpecCard(ⓘ)** + **MockBadge(🧪)**；导出 `RoleLevelGate allow={['S1','S2']}`。
- 复用 P0 已实现的类型分布逻辑：`getKeyEnterpriseScaleStats`（类型 × 国/省/市三级派生）。
- 带参：读 `?region=` 自动下钻到省级；读 `enterprise_code` 高亮（`DeepAnalysisEntryBanner`）。

### P2（E-22）实现要点（IA §4 骨架：FilterBar·ChartPanel·DataTable·DetailDrawer）
- `AnalysisShell` 包壳，结论先行。
- **FilterBar**：企业多选（Arco `Select` multiple，1~N 家）+「从对比篮带入」（`useCompareBasket`）。
- 选企业 → 解析业务/产品/技术标签（`domainTags`）映射产业领域 → 覆盖广度 / 深度 / 多元化指数（MetricCard×3，metric_id 齐全）。
- 领域分布饼 + 领域覆盖深度条形 ECharts；企业×领域标签映射区（点企业名 → **统一画像抽屉** `useEnterpriseProfileDrawer` / `ElementProfile`，DR-04）；领域清单 **DataTable**。
- **未选企业 → Empty 态**（Arco `Empty`，NF-07）；导出 `RoleLevelGate`。

---

## 3. 对 EnterpriseOverview 的减法改动（避免功能重复）

- 移除「结构洞察 → 企业类型分布分析」子页中的 **MetricCard×4（类型计数）+ 区域分布 provinceOption 重复图 + Q010/Q012 详情注记**；改为**概览级单图（类型饼）+ 一行摘要 + 「查看完整类型分析 → P1」入口按钮**（Arco Button，`navigate('/enterprise/type-distribution')`）。
- 移除「结构洞察 → 领域分布分析」子页中的 **MetricCard×3（覆盖领域/广度/多元化）+ Q013 详情注记**；改为**概览级单图（领域饼）+ 一行摘要 + 「查看完整领域分布 → P2」入口按钮**。
- `drillProvince`（全国分布点击省份）由"切内部 Tab"改为 **`navigate('/enterprise/type-distribution?region=<省>')`** 带参跳 P1，保留 `GEO_DRILLDOWN` 埋点。
- 「决策链下钻入口」：类型按钮改为跳 P1，新增「重点企业领域分布 → P2」按钮。
- **保留** 该文件 design:check 硬断言：Arco Button、`global-workbench-tabs`、`analysis-tabs` + `setPanoramaSubTab`、无私有/卡片 Tab、无 `cursor-pointer` —— 全部仍通过（结构洞察 analysis-tabs 与企业全景子页保留）。

---

## 4. 改动文件树

```
topic_demo/
├─ src/app/pages/enterprise/
│  ├─ EnterpriseTypeDistribution.tsx     (新增 · P1 / E-21)
│  ├─ EnterpriseDomainDistribution.tsx   (新增 · P2 / E-22)
│  └─ EnterpriseOverview.tsx             (改 · 移除并入详情→概览摘要+下钻入口)
├─ src/app/mock/enterprise/
│  ├─ analysisDistribution.ts            (新增 · 类型/领域分布派生 Mock)
│  └─ metricSeed.ts                      (改 · 新增 5 个 metric 8 件套:
│                                          M_ENT_TYPE_RATIO / M_ENT_CLUSTER_INDEX /
│                                          M_ENT_DOMAIN_BREADTH / _DEPTH / _DIVERSITY)
├─ src/app/routes.tsx                    (改 · 新增 type-distribution / domain-distribution 路由 + import)
└─ src/app/components/Layout.tsx         (改 · 企业分析菜单新增两入口)
```

> 仅新增/修改上述代码文件；未改 `package.json`/`vite.config.ts`/`.gitignore`/tailwind 配置；未引入新依赖（地图为占位区块）。

---

## 5. DoD 验收证据

| 项 | 结果 |
|----|------|
| `npm run design:check` | ✅ `Design contract checks passed`（exit 0）|
| `npm run build` | ✅ `built in 33.22s`（exit 0）|
| ReadLints（全部改动文件） | ✅ 0 错误 |
| 技术栈口径 | ✅ Arco（Button/Select/Cascader/Checkbox/Radio/Table/Empty/Tooltip）+ ECharts（复用 `EChart.tsx`）+ design-tokens 变量；无 recharts；统一画像复用 `ElementProfile`/`useEnterpriseProfileDrawer` |
| D9 血缘 | ✅ 统计数字旁 ⓘ MetricSpecCard；Mock 配 🧪 MockBadge；新增 metric 含 8 件套 |
| 埋点 | ✅ `GEO_DRILLDOWN`/`ENT_FILTER_APPLY`/`REPORT_EXPORT`，统一注入 `user_level` |

---

## 6. 与 IA §2.2/§3.2 对照

| IA 条目 | 要求 | 本 WP 落地 | 状态 |
|---------|------|-----------|------|
| §2.2 P1 | E-21 路由 `/enterprise/type-distribution`，组件 ContextBar·SearchableCascadeFilter·MapPanel·ChartPanel·DataTable | 全部落地（MapPanel 为 Wave 0 占位）| ✅ |
| §2.2 P2 | E-22 路由 `/enterprise/domain-distribution`，组件 FilterBar·ChartPanel·DataTable·DetailDrawer | 全部落地（DetailDrawer = 统一画像抽屉）| ✅ |
| §3.2 | type/domain-distribution **新增**路由；overview **拆分** | 已新增两路由；overview 拆分为 P0 概览 + 下钻入口 | ✅ |
| §1.58 | `P0 -.下钻.-> P1` | overview 下钻入口按钮 + drillProvince 带参跳 P1 | ✅ |

---

## 7. 遗留项

- **MapPanel 三级下钻**：当前为指标占位区块（🧪），Wave 1 接 Leaflet GIS（IA §9.2 / FDS §14 Wave 1）。
- **业务口径待甲方（🟡）**：Q010 企业类型判定、Q012 区划精度（P1）；Q013 领域广度/深度公式（P2）—— 已在 UI 加 ⚠ 提示与 metric `pending_ref`，登记于 `客户决策清单跟踪表.md`，上线前需甲方确认升 🟢。
- 国/省层级区域数据为 Mock 放大占位，市级（深圳区县）为 `ENTERPRISE_LIST` 明细派生；三方源到位后由数据工厂替换。
