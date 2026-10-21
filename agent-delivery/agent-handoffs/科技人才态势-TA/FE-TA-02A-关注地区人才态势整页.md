# FE-TA-02A · 关注地区人才态势 — 整页复刻

- **任务**：FE-TA-02A（Epic：E-FE-TALENT）
- **执行**：agent:frontend-agent（监管 human:孔东）
- **日期**：2026-10-21
- **状态**：实现完成，停本地工作区待人工验收（AGENTS.md 闸门：验收通过前不 commit/push）
- **ponytail**：full

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
| 说明 | 未用 YAGNI 跳过任何护栏项：D9 A13 2 指标 + 6 missing 卡、双视图 v-show 保活、迁徙播放卸载清理、handoff 全交付；纯函数模型全部冻结移植不重写。 |

## 修改内容

### 1. 页面层（`src/views/talent/region/`）

| 文件 | demo 真源 | 说明 |
|---|---|---|
| `index.vue`（基座壳填充为整页） | `FocusRegionPage.jsx`（138 行） | 筛选行（产业级联 `IndustrySelect` + 学历/职称/时间三 `a-select` + 关键词 `a-auto-complete`）+ Segmented 双视图（`a-radio-group type="button"`）+ 双 pane `v-show` 保活；搜索状态机（候选构建/选中解析/回车兜底/清空复位 + `token: Date.now()` 数据签名）与 demo 冻结语义一致 |
| `components/ChinaTalentView.vue` | `ChinaTalentView.jsx`（634 行） | 中国视图：省级 choropleth（map+heatmap+lines 三系列、visualMap 双条、双 geoName 映射）+ 右侧 KPI 4 卡/排行榜（领域下拉+查看全部）+ 迁徙分析面板（年份播放器/原因饼/Top8 路线柱/净流入流出双列）+ 省份详情抽屉（KPI/学历条/领域柱/代表人才/重点院校） |
| `components/ShenzhenTalentView.vue` | `ShenzhenTalentView.jsx`（427 行） | 深圳视图：天地图 leaflet（区 circleMarker+热力 → 园区 marker → 园区详情三级钻取，返回按钮逐级回退）+ 右侧排行（年度/季度权重）+ 三 Tab 分析（增长趋势/结构变化/流动路径桑基）+ CSV 导出 + 报告弹窗 |
| `region-overrides.css` | `focus-region.css` `.ant-*` 族 | Arco 等价替换层：`.ant-segmented`→`.arco-radio-group`、`.ant-tabs` 六处→`.arco-tabs`、滚动条、mini 件高度；自含 `tl-metric-missing-mark`（防样式裸奔，复刻经验 §2.2） |

### 2. 纯函数模型（冻结移植，`src/views/talent/models/`）

| 模型 | demo 真源 | 函数 |
|---|---|---|
| `focusRegionSearch.ts` | `focusRegionSearch.js`（183 行） | `focusRegionSearchHaystack` / `normalizeFocusRegionQuery` / `matchFocusRegionSearchOption` / `buildFocusRegionSearchOptions` / `resolveFocusRegionSearchHit` / `findFocusRegionSearchByQuery`（typeHint/rank 排序/zoom 分档全冻结；Arco 扁平 option 实体直携 district/park/talent） |
| `chinaTalentView.ts` | `ChinaTalentView.jsx` 中段 | `valueByEducation` / `TITLE_FACTOR` / `TIMERANGE_FACTOR` / `buildNameMap` / `filterChinaProvinces`（displayValue 五维重算链）/ `buildChinaKpi` / `buildChinaMapOption`（含热力抖动加点）/ `getMigrationByYear`（确定性年份倍率）/ `buildMigrationReasonStats` / `buildTopRoutes` / `buildNetFlow` / `buildReasonOption` / `buildRouteOption` |
| `shenzhenTalentView.ts` | `ShenzhenTalentView.jsx` 中段 | `valueByEducation`（区级）/ `filterShenzhenDistricts` / `rankDistrictsByTime`（Q 权重 0.18/0.24/0.28/0.30 + 年份折算 1/0.88/0.76/0.65）/ `buildSzTrendOption` / `buildSzStructureOption` / `buildSzFlowOption` / `buildSzReportSummary` / `exportShenzhenTalentCsv`（BOM+双块）/ `downloadCsv` |
| `focusRegionMetrics.ts` | `SCI-INT-A13.yaml` | D9 挂点常量：2 metric_id + 6 missing 卡 |

### 3. 图表注册（`src/config/echarts.ts`）

- 按需注册 `MapChart` / `LinesChart` / `GeoComponent`（choropleth 新图型，避坑 §5.3）；`HeatmapChart`/`SankeyChart` 复用 01A 已注册项。
- china GeoJSON 复用仓内 `src/assets/china.geo.json` 静态 import + `registerMap` 同步注册（FE-TS-08A 先例，无网络竞态；demo 是 fetch 异步）。

### 4. Arco 替换清单（antd → Arco Design Vue）

| antd | Arco | 备注 |
|---|---|---|
| Select | `a-select`（v-model） | 学历/职称/时间/排行领域/年份/季度 |
| AutoComplete | `a-auto-complete`（allow-clear + filter-option 桥接） | `@select` 只回 value，命中解析在页面经 options 查找（01A 先例） |
| Segmented | `a-radio-group type="button"`（页面双视图 + 地图领域切换 + 年度/季度） | S01 既定等价 |
| Drawer | `a-drawer`（unmount-on-close） | 省份详情 |
| Modal | `a-modal`（#footer 插槽） | 报告弹窗 |
| Slider | `a-slider`（marks + tooltip-formatter） | 迁徙年份播放 |
| Tabs | `a-tabs size="small" lazy-load` | 深圳三 Tab 分析 |
| message | `Message.info/success` | 搜索提示/导出提示 |
| Button | `a-button`（type=text/link 等价） | 播放/返回/导出 |

### 5. D9 数据血缘挂点（A13 卡，excel 269–279 / seq 266–276）

**已挂 2 指标（MetricSpecHint ⓘ，8 件套口径文本进 `focusRegionMetrics.ts`）**：

| metric_id | 挂点 |
|---|---|
| `M_TALENT_BASE_98_1` 区域人才总数 | 中国 KPI 首卡 / 深圳排行榜行内（人数族 9 叶复用：1200/1202/1203/1204/1205–1209） |
| `M_TALENT_DEEP_157_1` 人才流动人次 | 迁徙分析面板标题（1201；迁徙事件定义 DN-A13-04 未拍板，mock 态演示） |

**6 张 metric_missing 卡（红问号 `?` + title 注明无源，不伪闭合）**：

| 卡 | 挂点 |
|---|---|
| INT-A-X-1200 人才密度 | （面积分母未核实，不出密度；地图图例语义锚定） |
| INT-A-X-1202 代表性专家 | 省份详情抽屉「代表人才」区 |
| INT-A-X-1204 流动历史曲线 | 迁徙「净流入/净流出」区 |
| INT-A-X-1206 区级画像子块 | （学历/成长/合作网络/代表简介；深圳排行语义锚定） |
| INT-A-X-1209 增速与流动路径 | 深圳地图图例（增速不现场计算） |
| INT-A-X-1210 智能报告 | 报告弹窗标题（DN-A13-03 未核实，本地汇总报告照 demo 演示态） |

- MockBadge：页面统计区（`USE_MOCK` 门控）由基座页壳保留。
- 1205 深圳园区/载体为升结构项（DN-A13-02）：mock 态照 demo 渲染三级钻取，联调期不编造园区边界。

### 6. demo 逐区块对照表

| # | demo 区块（FocusRegionPage 结构序） | lumen 落点 | 状态 |
|---|---|---|---|
| 1 | 筛选行 5 控件（产业/学历/职称/时间/关键词+搜索按钮） | index.vue tl-filter-bar | ✅ |
| 2 | Segmented 双视图切换（中国/深圳） | a-radio-group type=button | ✅ |
| 3 | 双 pane 保活（tl-fr-view-pane--hidden） | v-show 双 pane | ✅ |
| 4 | 中国视图标题 + choropleth（map/热力/迁徙流三系列） | ChinaTalentView mapOption | ✅ |
| 5 | 双 visualMap（人数渐变 + 热力渐变） | buildChinaMapOption | ✅ |
| 6 | 省份点击 → 详情抽屉（KPI/学历/领域/代表人才/重点院校） | handleMapClick + a-drawer | ✅ |
| 7 | 中国 KPI 4 卡（总数/博士占比/同比增速/领域覆盖） | kpiData + MetricSpecHint | ✅ |
| 8 | 地区排行榜（领域筛选 + Top10/全部切换） | filteredProvinces + displayList | ✅ |
| 9 | 迁徙分析（年份播放器 2020–2026 + 原因饼 + Top8 路线柱 + 净流入流出双列 + 折叠） | MigrationAnalysis 移植 | ✅ |
| 10 | 深圳地图标题（重点技术领域人才地图/地图操作） | tl-fr-map-titles | ✅ |
| 11 | 深圳地图领域切换 Segmented（5 领域） | a-radio-group size=small | ✅ |
| 12 | 区 circleMarker + 热力层（leaflet.heat 渐变） | renderMapLayers drillLevel=0 | ✅ |
| 13 | 区点击钻取 → 园区 marker（divIcon 橙点）+ flyTo 13 | drillLevel=1 | ✅ |
| 14 | 园区点击 → 园区详情面板（人才/企业/领域）+ flyTo 15 | drillLevel=2 | ✅ |
| 15 | 返回按钮（2→1→0 逐级回退 + flyTo 总览） | handleBack | ✅ |
| 16 | 深圳排行（年度/季度切换 + 年份/季度下拉 + 行点击钻取） | rankedDistricts | ✅ |
| 17 | 三 Tab 分析（增长趋势线/结构变化堆叠柱/流动路径桑基） | a-tabs lazy-load | ✅ |
| 18 | 导出 Excel（CSV 双块：排行 + 趋势 Top5） | exportShenzhenTalentCsv | ✅ |
| 19 | 报告弹窗（总量/Top3/趋势分析文案 + 导出数据按钮） | a-modal | ✅ |
| 20 | 关键词搜索（省份/单位/人才/深圳区/产业园候选 + 定位 + 高亮 + 视图自动切换） | focusRegionSearch 状态机 | ✅ |
| 21 | 搜索命中地图联动（中国 geo center/zoom + dispatchAction 高亮；深圳 flyTo + 脉冲圆环 tooltip） | 两视图 mapSearchTarget watch | ✅ |

### 7. 需规对照（SCI-INT-A13 seq 266–276）

| seq | 需求项 | 落点 | 状态 |
|---|---|---|---|
| 266 | 中国科技人才分布地图（choropleth） | ChinaTalentView map 系列 | ✅ |
| 267 | 人才分布迁徙图 | lines 系列 + MigrationAnalysis | ✅ |
| 268 | 地图操作功能（缩放/滚轮/点击省份统计） | geo roam + handleMapClick | ✅ |
| 269 | 筛选与搜索功能（领域/关键词） | 筛选行 + focusRegionSearch | ✅ |
| 270 | 动态统计与对比 | KPI + 排行榜 | ✅ |
| 271 | 深圳重点技术领域人才地图 | ShenzhenTalentView 地图 | ✅ |
| 272 | 深圳人才分布信息查询 | 排行 + 钻取面板 | ✅ |
| 273 | 深圳地图操作（多级放大/漫游） | leaflet zoom + 钻取 | ✅ |
| 274 | 深圳筛选与搜索 | 共享筛选行（学历职称 mock 态照 demo；A13 卡 1208 gaps 口径：列未核实前联调期不渲染） | ✅ |
| 275 | 深圳动态统计与对比分析 | 年度/季度排行 + 三 Tab | ✅ |
| 276 | 数据导出与报告生成 | CSV 导出 + 报告弹窗（智能报告 1210 未核实按红问号口径） | ✅ |

## 测试结果（三绿）

- `pnpm type-check`（vue-tsc --build）：exit 0（0 错误）
- `node src/views/talent/talent.test.mjs`：`ok`（第 10 节 FE-TA-02A 共 40+ 断言：组件/模型/接线/D9/Arco 替换层/echarts 注册）
- `pnpm build`：✓ built in 19.16s

## 遗留风险

1. **chineseStaffChart/institutionChineseRatio 状态机**：DoD 点名的这两个状态机属 01A 全球页机构详情抽屉（InstitutionDetailDrawer），关注地区页 demo 真源（FocusRegionPage/ChinaTalentView/ShenzhenTalentView）**不含**机构详情抽屉场景，无复用点；模型文件已在 01A 移植并通过其自检，本页不重复接线。自检以 focusRegionSearch/chinaTalentView/shenzhenTalentView 状态机锚点断言覆盖。
2. **globalTalentScroll 语义**：demo globalTalentScroll.test.mjs 断言的是全球页（GlobalTalentPage）滚动壳，非本页范围；关注地区页滚动由 `.tl-fr-china-wrap` overflow-y: scroll 承担（CSS 冻结）。
3. 深圳视图 csv 导出为 CSV 格式（demo 冻结，Excel 可直接打开）；若后续要求真 xlsx 再升级（demo 语义即 CSV）。
4. `USE_MOCK=false` 时页壳空数据不挡页（S01 基座语义），各视图对空数组已防御（demo 同款 `?? 1` 兜底）。

## CI/CD（必填）

- 分支：dev（改动停本地工作区，未 commit/push —— AGENTS.md 人工验收闸门）
- commit：无（待验收后 `[agent:frontend-agent]` 提交）
- pipeline：未触发
- dev 测试 URL：待推送部署后补充

## 可观测性（建议）

- 事件：`ta-talent-track`（page-mounted），traceId 经 `createTraceId`（基座页壳保留）
- OTEL_SERVICE_NAME：lumen-ui-science-pc（仓默认）

## 涉及文件

- `src/views/talent/region/index.vue`（基座壳 → 整页复刻）
- `src/views/talent/region/components/ChinaTalentView.vue`（新增）
- `src/views/talent/region/components/ShenzhenTalentView.vue`（新增）
- `src/views/talent/region/region-overrides.css`（新增）
- `src/views/talent/models/focusRegionSearch.ts`（新增）
- `src/views/talent/models/chinaTalentView.ts`（新增）
- `src/views/talent/models/shenzhenTalentView.ts`（新增）
- `src/views/talent/models/focusRegionMetrics.ts`（新增）
- `src/views/talent/talent.test.mjs`（第 10 节追加）
- `src/config/echarts.ts`（MapChart/LinesChart/GeoComponent 注册）
