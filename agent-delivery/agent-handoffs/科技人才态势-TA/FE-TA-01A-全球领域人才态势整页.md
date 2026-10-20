# FE-TA-01A · 全球领域人才态势 — 整页复刻

- **任务**：FE-TA-01A（Epic：E-FE-TALENT）
- **执行**：agent:frontend-agent（监管 human:孔东）
- **日期**：2026-10-21
- **状态**：联调中（integration，AV-0 已过）；双仓已 commit + push dev（2026-10-21 01:15 用户放行：pc `d5e23cd` / 编排 `170e6721`）
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
| 说明 | 未用 YAGNI 跳过任何护栏项：D8 token 冻结、D9 6 指标 + 10 missing 卡、可观测埋点、handoff 全交付；纯函数模型全部冻结移植不重写。 |

## 修改内容

### 1. 组件层（demo 全球页 10 组件 1:1 移植，`src/views/talent/global/`）

| 组件 | demo 真源 | 说明 |
|---|---|---|
| `components/DistributionInsightView.vue` | `DistributionInsightView.jsx`（545 行） | Tab1 主体：筛选栏（产业级联/地区/行业/人才类型/时间范围）+ KPI 3 卡 + 左右 58/42 布局；`filteredData` 五维筛选链（fieldScopeShare 空选=全部、无映射空态、talentType/timeRange 数值模拟）与 demo 语义一致 |
| `components/TalentMap.vue` | `TalentMap.jsx`（456 行） | Leaflet 四图层：散点（动态密度阈值 p75/55% 峰值 + TopN 自动高亮脉冲标注）/ 热力（leaflet.heat）/ 迁徙（贝塞尔飞线 + 流入点）/ 气泡；机构标记层 + hover 高亮 class；搜索框内嵌地图左上角；图例随图层切换 |
| `components/InsightPanel.vue` | `InsightPanel.jsx`（383 行） | 4 子 Tab：华人占比堆叠柱 / 地区 Treemap（点击定位地图）/ 产研对比分组柱 / 热点流入流出（时间趋势图 + Top10 迁徙横向柱 + 双列热点卡） |
| `components/InstitutionListPanel.vue` | `InstitutionListPanel.jsx`（103 行） | Top20 排名横向柱图（按领域重排）+ 列表（hover 高亮、点击 flyTo+详情）；复用 `SectionPanel` |
| `components/TalentTimelineBar.vue` | `TalentTimelineBar.jsx`（71 行） | 年度播放条（2020–2026）；setInterval 卸载清理 + visibilitychange 不可见暂停 |
| `components/ActivityPanel.vue` | `ActivityPanel.jsx`（330 行） | Tab2：五维筛选 + 1–6 月时间轴播放器 + 气泡地图 + 动态列表分页 + 城市抽屉联动 |
| `components/RegionDetailDrawer.vue` | `RegionDetailDrawer.jsx`（236 行） | 区域详情：统计 4 卡 / 华人占比饼图 / 年度趋势（总量+净流入）/ 学历·类型分布条 / 分领域学历 / 主要院校 / 代表人才 / 优势领域 |
| `components/InstitutionDetailDrawer.vue` | `InstitutionDetailDrawer.jsx`（170 行） | 机构详情：基础信息 7 卡 / 华人占比饼图 / 华人教师·研究员柱图 / 学历结构 / 领域分布 / 核心成果 / 关联专家 |
| `components/CityActivityDrawer.vue` | `CityActivityDrawer.jsx`（166 行） | 城市动态：区域统计 / 优势领域 / 相关人才 / 类型汇总 chip / 动态 feed（高亮定位条目） |
| `components/ChineseResearcherRatioChart.vue` | `ChineseResearcherRatioChart.jsx` | 华人研究员占比环形饼图（graphic 中心文字 + 口径元信息行） |
| `global-overrides.css` | — | 21 处 `.ant-*` → `.arco-*` 等价替换层（select/tabs/pagination/drawer 尺寸 token + `tl-metric-missing-mark` 红问号样式） |

### 2. 纯函数模型（冻结移植，`src/views/talent/models/`）

| 模型 | demo 真源 | 函数 |
|---|---|---|
| `talentMapSearch.ts` | `talentMapSearch.js` | `talentSearchHaystack` / `matchTalentSearchOption` |
| `talentSearchResolve.ts` | 同上 | `buildTalentSearchOptions` / `resolveTalentSearchHit`（Arco 扁平 option 类型化重写，regionData/instData 直携实体） |
| `migrationHotspots.ts` | `migrationHotspots.js` | `aggregateNetByCity` / `formatHotspotAnnotation` / `buildMigrationHotspots` |
| `globalTalentTime.ts` | `globalTalentTime.js` | `GLOBAL_TALENT_YEARS` / `flowsAtYear` / `regionSeriesFor` / `regionPointAtYear` / `regionValueAtYear` / `applyYearToRegions` / `globalPointAtYear` |
| `chineseResearcherRatio.ts` | `chineseResearcherRatio.js` | `buildResearcherStats` / `buildChineseResearcherPieOption`（研究员口径注释冻结） |
| `chineseStaffChart.ts` | `chineseStaffChart.js` | `splitChineseStaffCounts` / `buildChineseStaffChartOption` |
| `institutionRanking.ts` | `institutionRanking.js` | `rankInstitutionsByField` / `buildInstitutionRankChartOption` |
| `globalTalentExport.ts` | `DistributionInsightView.jsx` handleExport | `exportTalentDistributionXlsx`（三 sheet：区域汇总/顶尖机构/概览信息）/ `exportTalentDistributionCsv`（BOM+引号包裹） |
| `talentMetrics.ts` | `SCI-INT-A12.yaml` | D9 挂点常量：6 metric_id + 10 missing 卡 |

### 3. 页面与接线

- `index.vue`：双 Tab（distribute/activity）；`handleRegionClick` 代表专家匹配（城市锚定院校优先，经纬度 `Math.hypot < 3°` 邻近兜底，空则全局前 5）——demo 冻结语义；搜索清除复位（地图回 30,20 zoom2 + 清高亮清抽屉）；`goProfile`/`goRecommend` 带 `talentId` query。
- `src/config/echarts.ts`：按需注册 `TreemapChart`（避坑 §5.3）。

### 4. Arco 替换清单（antd → Arco Design Vue）

| antd | Arco | 备注 |
|---|---|---|
| Select | `a-select`（`:model-value` + `@update:model-value`） | 值联合类型经 `onFilterSelect` 收口 String 化 |
| AutoComplete | `a-auto-complete` | `filter-option` 适配 Arco `SelectOptionData` 签名（经 `filterSearchOption` 桥接，命中解析在父级） |
| Dropdown + menu.items | `a-dropdown` + `#content` + `a-doption` | 导出菜单 |
| Button | `a-button` | 含 `#icon` 插槽 |
| Drawer | `a-drawer`（`popup-container` 默认 body，即 Teleport） | unmount-on-close |
| Tabs | `a-tabs` + `a-tab-pane`（lazy-load） | InsightPanel 子页签 |
| Slider | `a-slider`（marks 等价） | 时间轴 |
| Pagination | `a-pagination`（show-total 布尔） | 动态列表 |
| message | `Message.info`（Arco 指令式） | 搜索提示 |
| Tag | `a-tag` | — |

### 5. D9 数据血缘挂点

**已挂 6 指标（MetricSpecHint ⓘ，8 件套口径文本进 `talentMetrics.ts`）**：

| metric_id | 挂点 |
|---|---|
| `M_TALENT_BASE_98_1` 区域人才总数 | Tab1 KPI 首卡 / RegionDetailDrawer 首统计 / InstitutionDetailDrawer「汇聚人才」/ InstitutionListPanel 排名图说明行 / CityActivityDrawer（region 首统计） |
| `M_TALENT_DEEP_157_1` 人才流动人次 | 迁徙飞线 tooltip 语义（模型层 flowsAtYear 注释锚定） |
| `M_TALENT_DEEP_162_1` 学术力指标 | 机构详情「近3年论文/专利」区（chineseResearcherRatio 口径注释） |
| `M_TALENT_DEEP_164_1` 招入推荐匹配度 | 跨页跳转 goRecommend 语义锚定 |
| `M_TALENT_GRAPH_110_1` 人才实体识别 | 搜索候选（buildTalentSearchOptions 城市实体）注释锚定 |
| `M_TALENT_GRAPH_111_1` 人才关系网络 | 机构详情「合作网络与关联专家」区注释锚定 |

**10 张 metric_missing 卡（红问号 `?` + title 注明无源，不伪闭合）**：

| 卡 | 挂点 |
|---|---|
| INT-A-TAL-1105 华人占比 | ChineseResearcherRatioChart（两抽屉复用）/ InsightPanel 华人占比子 Tab |
| INT-A-TAL-1107 学历分布 | RegionDetailDrawer 学历区 |
| INT-A-TAL-1108 人才类型 | RegionDetailDrawer 类型区 |
| INT-A-TAL-1110 动态气泡 | ActivityPanel 布局区（ActivityPanel 内 cityMarkers 语义） |
| INT-A-TAL-1111 动态热力 | TalentMap 热力图层（图例区） |
| INT-A-TAL-1113 顶尖机构排名 | InstitutionListPanel 说明行（人数挂 base98 ⓘ，排名分配 `?`） |
| INT-A-TAL-1116 产研对比 | InsightPanel 产研子 Tab |
| INT-A-TAL-1119 最新动态 | ActivityPanel 列表区 / CityActivityDrawer 动态 feed |
| INT-A-TAL-1121 荣誉奖项 | 机构详情核心成果区（award 语义） |
| INT-A-TAL-1122 出访记录 | goProfile 跨页语义（画像页 01C 范围） |

- MockBadge：走查 2 移除（用户裁定：KPI 卡去 🧪 标识）；Mock 态语义仍由 USE_MOCK 数据轨保证。
- 缺口长文案全部走 `talentMetrics.ts` 集中常量（头注释注明 A12 真源），前端不散落硬编码。

### 6. demo 逐区块对照表

| # | demo 区块（GlobalTalentPage 结构序） | lumen 落点 | 状态 |
|---|---|---|---|
| 1 | 双 Tab（人才分布图/人才的最新动态） | index.vue + PageTabFrame | ✅ |
| 2 | 筛选栏 6 控件（产业/地区/行业/人才类型/时间范围/导出按钮） | DistributionInsightView | ✅ |
| 3 | 人才统计与流动趋势年度条（播放/暂停/拖拽/摘要） | TalentTimelineBar | ✅ |
| 4 | 左区标题「交互式操作与动态追踪」+ 地图 | DistributionInsightView + TalentMap | ✅ |
| 5 | 地图三图层切换按钮 + 图例（散点四色/迁徙三色） | TalentMap toolbar/legend | ✅ |
| 6 | 散点层（密度高亮脉冲 + 重点关注 tooltip） | TalentMap renderScatterLayer | ✅ |
| 7 | 热力层（渐变 + 筛选联动） | renderHeatLayer + filteredHeatData | ✅ |
| 8 | 迁徙层（贝塞尔飞线 + 热点标注 + 点击联动洞察） | renderMigrationLayer + renderHotspotLayer | ✅ |
| 9 | 搜索框（城市/机构候选 + 回车提交 + 清空复位） | TalentMap 内嵌搜索 + handleSearchSubmit/Change | ✅ |
| 10 | KPI 3 卡（总数/博士占比/领域覆盖） | DistributionInsightView kpiData | ✅ |
| 11 | 洞察面板 4 子 Tab | InsightPanel | ✅ |
| 12 | 华人占比堆叠柱（地区维度） | InsightPanel chineseOption | ✅ |
| 13 | 地区分布 Treemap（点击地图定位） | InsightPanel treemapOption + onTreemapClick | ✅ |
| 14 | 产研对比分组柱（领域维度） | InsightPanel irOption | ✅ |
| 15 | 热点双列卡 + 时间趋势线 + Top10 迁徙柱 | InsightPanel migration 子 Tab | ✅ |
| 16 | 顶尖机构洞察（排名柱 + 列表 + 领域筛选） | InstitutionListPanel | ✅ |
| 17 | 机构点击 → flyTo + 高亮 + 详情抽屉 | index.vue handleInstitutionClick | ✅ |
| 18 | 区域点击 → 代表专家匹配 + 详情抽屉 | index.vue handleRegionClick + RegionDetailDrawer | ✅ |
| 19 | Tab2 五维筛选 + 城市标记地图 | ActivityPanel | ✅ |
| 20 | 1–6 月播放器（播放/重置/拖拽） | ActivityPanel 时间轴区 | ✅ |
| 21 | 动态列表（分页 + 点击城市定位 + 查看画像） | ActivityPanel 列表区 | ✅ |
| 22 | 城市动态抽屉（统计/相关人才/类型汇总/feed） | CityActivityDrawer | ✅ |
| 23 | XLSX/CSV 导出下拉 | DistributionInsightView 导出按钮 + globalTalentExport | ✅ |

### 7. 需规对照（SCI-INT-A12 seq 243–265）

| seq | 需求项 | 落点 | 状态 |
|---|---|---|---|
| 243 | 人才分布信息查看（散点图层） | TalentMap scatter | ✅ |
| 244 | 地图多层级浏览与筛选 | 筛选栏 + 图层切换 | ✅ |
| 245 | 交互式操作与动态追踪 | 地图交互 + 搜索 + 联动 | ✅ |
| 246 | 人才流动和迁移图示 | 迁徙层 + 热点 + 时间轴 | ✅ |
| 247 | 地图数据联动与报表导出 | XLSX/CSV 三 sheet | ✅ |
| 248 | 华人占比分析 | InsightPanel 子 Tab1 + 饼图 | ✅ |
| 249 | 地区分布洞察 | Treemap 子 Tab2 | ✅ |
| 250 | 顶尖机构洞察 | InstitutionListPanel | ✅ |
| 251 | 产研对比分析 | irOption 子 Tab3 | ✅ |
| 252 | 人才迁徙情况展示 | migration 子 Tab4 | ✅ |
| 253 | 气泡消息展示 | ActivityPanel 气泡层 | ✅ |
| 254 | 热力图分布与密度分析 | renderHeatLayer | ✅ |
| 255 | 交互式地图导航 | ActivityPanel 地图 | ✅ |
| 256 | 区域动态筛选与趋势追踪 | ActivityPanel 筛选 + 播放器 | ✅ |
| 257 | 基础信息展示 | RegionDetailDrawer / InstitutionDetailDrawer | ✅ |
| 258 | 科研成果统计 | InstitutionDetailDrawer 成果区 | ✅ |
| 259 | 学术影响力分析 | 机构详情论文/专利卡（DEEP_162 锚定） | ✅ |
| 260 | 研究领域与方向标签 | 机构详情领域分布图 | ✅ |
| 261 | 合作网络与关联专家 | 机构详情代表人才区（GRAPH_111 锚定） | ✅ |
| 262 | 最新动态跟踪 | ActivityPanel + CityActivityDrawer | ✅ |
| 263 | 人才评估与匹配度分析 | goRecommend 跨页（01D 范围，本页入口+跳转） | ✅（入口） |
| 264 | 荣誉及奖项展示 | 机构详情核心成果区（award 类型动态） | ✅（列表态） |
| 265 | 国际合作与出访记录 | goProfile 跨页（画像页 01C 范围） | ✅（入口） |

> 注：263/264/265 的完整形态属画像页（FE-TA-01C）与推荐页（FE-TA-01D）任务范围；本页按 demo 冻结语义交付入口 + 跨页跳转 + 相关区块。

## 测试结果（三绿）

- `pnpm type-check`（vue-tsc --build）：exit 0（0 错误）
- `node src/views/talent/talent.test.mjs`：`ok`（种子冻结 + 01A 组件/模型/接线/D9/导出/Treemap 注册/Arco 替换层断言全过，第 9 节共 30+ 断言）
- `pnpm build`：✓ built in 19.75s（走查 2 后复测）
- 浏览器 CDP 实测（走查 3 后）：右列布局 KPI 71px / 洞察 body 267px / 机构卡 248px，无裁切无塌缩

## 遗留风险

1. **迭代损坏恢复**：4 个 `.vue` 文件（RegionDetailDrawer/CityActivityDrawer/DistributionInsightView/InstitutionListPanel）曾被 PowerShell 替换脚本字符级损坏（每字符断行），已全部用 Write 干净重写；建议人工走查时重点核对这 4 个文件的模板区块完整性。
2. **Arco a-auto-complete @select 只回 value**（不带 option 对象）：命中解析在 TalentMap 内经 `searchOptions.find` 恢复实体后向上 emit；极端同名城市/机构时按数组序取首个（demo 语义同）。
3. 迁徙飞线为 polyline 虚线（demo 同款），未做移动光点动画——demo 真源即如此，非缺失。
4. `lock_until` 已过期（2026-10-20T20:04Z），registry 续期由 task-update-status 顺带处理。

## 走查修正记录

### 2026-10-21 走查 1：顶尖机构洞察区样式裸奔（用户反馈）

**现象**：「顶尖机构洞察」面板标题/副标题/边框全裸奔（无 `tt-module-header__title` 的 20px 粗体、无面板白底圆角边框）。

**根因**：demo `SectionPanel.jsx` 自带 `import './techTrendComponents.css'`（样式自含）；lumen 移植版 `SectionPanel.vue`（FE-TS-04A 产物）漏掉这行导入，`tt-section-panel` / `tt-module-header` 系列样式只存在于 `global-innovation/index.vue` 引入的 `demo-tech-trend.css`——人才页引用该组件时类名裸奔（复刻经验 §2.2 场景复发）。

**修法**（对齐 `PageTabFrame` 组件目录自含 CSS 先例）：
- 新增 `src/views/situation/global-innovation/components/section-panel.css`：只抽 demo `techTrendComponents.css` 中 SectionPanel/ModuleHeader 相关块（panel 密度/tone、header 布局、title 20px/700、subtitle 13px、accent 竖条），不重复 KPI 卡与 filter bar 块。
- `SectionPanel.vue` 加 `import './section-panel.css'`——对 global-innovation 页为同规则重复声明（层叠无害），对 talent 等跨模块引用恢复完整样式。

**验证**：type-check 0 错 / talent.test.mjs ok / build 24.34s 三绿；教训已沉淀真源经验清单 §2.3 + 出处索引 FE-TA-01A 行。

### 2026-10-21 走查 2：右列布局与 UI 细节四项（用户反馈）

**四项要求与修法**（全在 `global-overrides.css` + 组件模板，demo 冻结 CSS 不动）：

1. **KPI 首卡去 🧪 Mock 标识**：`DistributionInsightView.vue` 删 `<MockBadge v-if="i === 0 && USE_MOCK" />` 与相关 import；`talent.test.mjs` 9.6 断言同步改（MockBadge 断言移除并注明用户裁定，MetricSpecHint ⓘ 断言保留）。
2. **KPI 卡高度收到两行**：去 MockBadge 后 `.tl-kpi-item` 收紧（padding 12px 14px→10px 12px、gap 4px→2px，`__value` nowrap），104px→71px。
3. **洞察面板空 tabs-content 去除 + 图表高度压缩**：Arco `a-tab-pane` 自闭合空壳（内容在 `.tl-insight-body` v-show 自绘）仍渲染 24px 空 `.arco-tabs-content` → `display:none`；图表 280→220（华人占比/Treemap）、260→210（产研）、200→170 / 160→140（迁徙子 Tab 两图，保持比例）。
4. **机构洞察卡吃满腾出空间**：`.tl-dist-right .tl-institution-list { flex:1 1 auto; min-height:160px }`。

**验证**：type-check 0 错 / talent.test.mjs ok / build 19.75s 三绿。

### 2026-10-21 走查 3：洞察面板 body 塌缩修复（用户反馈「高度增加三倍」）

**现象**：走查 2 后 `.tl-insight-body` 塌到 65px（原 ~200px），图表被裁。

**根因**（CDP 实测）：机构卡 grow=1 自然高度 450px，把 shrink=1 的洞察面板压到 103px——flex 收缩链上洞察面板没有保底。

**修法**：`.tl-dist-right .tl-insight-panel { flex: 0 0 auto; min-height: 0; max-height: 330px }`——按内容自然高、不收缩；迁徙子 Tab 内容超高时 330px 封顶由 body `overflow:auto` 内部滚动。

**验证**（CDP 复测）：insight 305px / body 267px（65→267 ≈ 4 倍，覆盖「三倍」要求）/ 机构卡 248px（仍高于走查前 170px）/ KPI 71px。三绿状态沿用走查 2（纯 CSS 改动）。

## CI/CD（必填）

- 分支：dev
- commit：lumen-ui-science-pc `d5e23cd`（43 文件 +11368）；gkx-orchestration `170e6721`（handoff + registry + 经验清单；经 rebase 合并远端 coordinator 并行 registry 写入）
- pipeline：待 CI 触发（push → Pipeline）
- dev 测试 URL：本地 dev 5199 `http://localhost:5199/talent/global-talent-situation` 已走查通过；K8s dev 待 CI 部署后复核
- 用户放行记录：2026-10-21 01:15 用户指令「双仓代码commit、push dev」（人工验收闸门解除）

## 可观测性（建议）

- 事件：`ta-talent-track`（page-mounted / view-profile / view-evaluation），traceId 经 `createTraceId`
- OTEL_SERVICE_NAME：lumen-ui-science-pc（仓默认）

## 涉及文件

- `src/views/talent/global/`（index.vue + global-overrides.css + components/ ×10）
- `src/views/talent/models/`（×9：talentMapSearch / talentSearchResolve / migrationHotspots / globalTalentTime / chineseResearcherRatio / chineseStaffChart / institutionRanking / globalTalentExport / talentMetrics）
- `src/views/talent/talent.test.mjs`（第 9 节追加）
- `src/config/echarts.ts`（TreemapChart 注册）
- 走查 1 追加：`src/views/situation/global-innovation/components/SectionPanel.vue`（+自含样式 import）、`components/section-panel.css`（新增）
- 走查 2/3 追加：`src/views/talent/global/global-overrides.css`（tabs-content 隐藏 / KPI 紧凑 / 机构卡 flex / 洞察面板防塌缩）、`components/DistributionInsightView.vue`（去 MockBadge）、`components/InsightPanel.vue`（图表高度压缩）、`talent.test.mjs`（9.6 断言更新）
