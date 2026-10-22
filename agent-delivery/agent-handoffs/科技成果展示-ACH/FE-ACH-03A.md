# FE-ACH-03A · 科技时空演进展示 — 整页复刻交付

> 任务：FE-ACH-03A（科技时空演进展示整页复刻，bid-reference §1.1.1.1.4.6.3 时空演进 a/b/c）
> 工作区：`worktrees/lumen-ui-science-pc--ach03-space-time`（分支 feat/ach03-space-time，基点 1834a50；**2026-10-21 已合并 dev 并清理**：`89a43c0` 交付 → `3c3a523` merge，worktree 与 feature 分支已删除）
> 状态：**integration（联调中）**，dev 本地领先 origin 2 个提交待 push（联调放行后统一推）
> ponytail: full

## 1. 范围与实现（DoD 对照）

| DoD（派单包 §3） | 实现 |
|---|---|
| 时空控制台（左栏） | ✅ 主题库 Checkbox×6（勾选联动主题 Tab）、四维度 Radio-button、国家/省州/市层级 Radio、时间轴 a-slider(2018-2026 marks)+播放/暂停/回放（INTERVAL_MS=800 常量化、document.visibilitychange 页面不可见暂停、onUnmounted clearTimeout）、热力层/密度轨迹 Checkbox、聚类口径 Select（成果产出/科研数量）、两区域/两时段对比 a-select×2（城市 20 项/年份 9 项） |
| 主区地图 | ✅ `WorldEvolutionMap.vue` 复用 `TiandituMap`（getMap() 拿 Leaflet 实例）：世界视口 center [30,15] zoom 2；CircleMarker 半径随维度值分级、热点预警红圈脉冲、聚集优势区紫圈；Polyline 三色（patent 紫 #722ED1 / talent 绿 #00B42A / collab 蓝 #165DFF）；密度演化轨迹红线 #F53F3F + fitBounds 视口飞行；层级切换 LEVEL_ZOOM 自动定焦；点击区域回抛 select-region |
| 三 Tab 全落点 | ① 热点预警与趋势报告 ✅ 预警卡三级色 Tag（高红/中橙/低蓝）+ 🏆 首位标记 + 「定位」按钮联动地图 flyTo、趋势 Line（当年 markLine）+ 文字简报 + 导出趋势报告/预警清单（Message 演示）、历史回溯表（2018→当年 增幅/CAGR）+ 趋势总结、多维度雷达对比（两区域/两时段归一化 + 对比结论）② 主题时空分析 ✅ 六要素汇总卡（论文/专利/资金/人才/主体/主题数）、论文发布趋势 Line + 季度 Bar + 活跃区 Top3 表、专利流动表 + Top 通道 Bar、资金 Top10 Bar + 主题进度 a-progress、人才净流入 Top8 Bar + 迁徙热区 Tag、主题演化阶段链（2018→2026 横向 Stage）、创新前沿报告（getFrontierReport）③ 流动与协同网络 ✅ 研究主体 a-select（RESEARCH_SUBJECTS 16 项：机构/载体/团队）、主体流动世界地图（第 2 张 WorldEvolutionMap，里程碑 Timeline 侧栏）、协作网络 ECharts graph（force 布局/按强度 slider 筛边/roam）、多维联动卡（四维度 sparkline） |
| KPI 行 | ✅ 5 卡（研究主体总数/热点区域数+高预警 Tag/学术论文/专利交易/人才净流入）全挂 ⓘ（MetricSpecHint metric-id ACH-STE-Q0201~Q0205）+ 🧪（MockBadge） |
| 确定性数据 | ✅ 全部消费 `achievementSpaceTimeSeed.ts` 冻结生成器（STE_YEARS/DIMENSIONS/THEMES/LEVELS/WARNING_LEVELS/RESEARCH_SUBJECTS/COLLAB_EDGES/FLOW_PATHS/THEME_EVOLUTION/getHotspots/getRegionStats/getGlobalTotals/getThemeProgress/getFrontierReport）；零 Math.random；种子未改（achievement.test.mjs 断言仍绿） |
| Arco + 图表容器高度 | ✅ demo 原生 select/input/button 全换 a-select/a-input/a-button/a-radio-group(type=button)/a-checkbox-group/a-slider/a-table/a-tag/a-alert/a-spin/a-progress；全部图表容器显式 height（地图 520/420、Line/Bar 260-320、雷达 300、graph 460、sparkline 48） |
| D9 全挂 | ✅ 5 KPI + 地图 Q0210 + 流动地图 Q0211 + 主题检索 Q0206（THEME-SEARCH）+ 各图表卡 MetricSpecHint；lineage 文案直读种子冻结口径 |

## 2. 产物清单

- `src/views/achievement/space-time-evolution/index.vue`（S01 占位壳 → 整页，~1500 行：KPI 行 + 控制台/地图双栏 + 3 Tab）
- `src/views/achievement/space-time-evolution/WorldEvolutionMap.vue`（新，TiandituMap 包装：overlays 渲染/heat 同步/focus 飞行/region 点击回抛）
- `src/views/achievement/space-time-evolution/worldEvolutionMap.ts`（新，Leaflet 覆盖物配置纯函数 + 模块级 `_selfCheck()`：buildMapRegion 分级半径/flowPolylineOptions 三色/ROUTE_LINE_OPTIONS 等 12 断言）
- `src/views/achievement/space-time-evolution/spaceTimeEvolution.css`（新，demo 内联样式 token 化：ste-kpi-row/ste-main-row 13-11/ste-console/ste-hotspot-cards/ste-element-cards/ste-evolution-chain/ste-linkage-row）

未动（闸门遵守）：`_shared/`、`menu.ts`、`api/`、`types/`、种子、`TiandituMap.vue` 本体、其他 ach01/02/04/05 worktree 与主工作区。

## 3. 浏览器走查（dev :5203，DOM 快照逐区块验证）

| 区块 | 验证证据 | 结论 |
|---|---|---|
| KPI 行 | 5 卡 Q0201~Q0205 ⓘ 按钮 + 数值 | ✅ |
| 控制台 | 主题×6/维度×4/层级×3/播放/回放/slider/热力/轨迹/自动定位/两区域/两时段全 refs | ✅ |
| 主地图 | Zoom in/out 控件 + 图例（区域强度/热点预警/聚集优势区/协作通道/流动路径/密度轨迹）+ Q0210 ⓘ | ✅ |
| Tab1 | 预警卡×5「地图定位」按钮、导出趋势报告/预警清单、从 2018 回放、导出趋势变化报告、输出定制报告、深圳热点简报/演化轨迹/新晋区域结论/雷达对比结论文案（种子冻结值 9,075 篇/14.9%/173.8% 全对上） | ✅ |
| Tab2 | 主题/年份/国家/主体 四筛选下拉、导出前沿阵地报告、创新前沿报告（多模态智能体阶段/北京·深圳·新加坡）、主题演化链 2018→2026（9 Stage） | ✅ |
| Tab3 | 主体下拉 16 项（斯坦福 HAI/DeepMind/深圳湾实验室/深智大模型团队…）、第 2 张地图 + Q0211 ⓘ、协同强度 slider、四维度 sparkline 卡 | ✅ |

截图：`.walkthrough/ste-tab1-top.png`（Tab1 顶部全览）；Tab2/Tab3 因 Cursor 内置浏览器截图通道白屏，以 DOM 快照逐区块验证（上表），走查时可现场点验。

## 4. 偏离说明

1. **worktree 路径**：用户指令写 `ach03-soft-science`，实际按派单包真源 `ach03-space-time`（soft-science 是 ach01 主题）。
2. **控制台布局**：demo 是左栏绝对定位滚动区，lumen 按 Design.md 13-11 grid 双栏（左控制台 sticky、右地图+Tab），交互语义逐条对齐；复刻经验「样式自含」不跨页复用类名。
3. **协作网络 graph**：demo 用 AntV G6，lumen 按 S01 基座既有 ECharts graph（force）实现（仓内 graph 先例已用 ECharts，无 G6 依赖——复刻经验 §2.2「已有依赖优先」）；节点/边/布局/筛选语义对齐。
4. **页壳滚动（走查修正 2026-10-21）**：fullBleed 路由 shell `overflow:hidden` 裁切 2636px 内容；`.ach-page.ste-page` 自管滚动（attrs fallthrough 挂 class，不污染其他 ach 页）。
5. **高预警 Tag 位置（走查裁定 2026-10-21）**：demo KpiTile `extra` 渲染在数值行下方（独立行）；走查要求移入数值行同行。已按裁定改为本页自排（复用 `_shared` 类名，公共件未动），代码有注释标记。

## 5. 架构合规自检（公约 §2）

- ✅ 调用链：只经 `fetchSpaceTimeEvolutionDataset`（USE_MOCK=true 走冻结种子），未越层
- ✅ D8：#165DFF 主色/#D8E7FC 底/卡片圆角 8px/阴影 token、Arco Vue 全量、控件 32px 体系
- ✅ D9：每个统计数字旁 ⓘ 或 ?（MetricSpecHint）；🧪 MockBadge 全挂；lineage 直读种子
- ✅ D10：a-tabs role=tablist 键盘可达（走查已用点击切换验证）、slider/select/checkbox 键盘操作语义保留
- ✅ D12：零 demo import/merge；demo 只读对照
- ✅ 可观测：trackAchievementInteraction（page-mounted/tab-change/export/locate/subject-change/play）
- ✅ 未 commit/push（人工验收闸门 2026-10-20）

## 6. 三绿证据（worktree 内执行）

- `pnpm type-check`：vue-tsc 0 错误
- 自检：`achievement.test.mjs`（种子冻结）+ `worldEvolutionMap.ts _selfCheck()`（12 断言：半径分级/三色 flow/轨迹配置/tooltip HTML）全绿
- `pnpm build`：vite build 成功（~37s）

## 7. cost

- actual_tokens: ~0.6M（glm-5.3）
- model_used: glm-5.3
- actual_cost: ~$1.5
- cost_warn: false
