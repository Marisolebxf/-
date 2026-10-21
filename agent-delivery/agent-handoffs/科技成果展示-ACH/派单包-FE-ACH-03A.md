# 派单包 · FE-ACH-03A 科技时空演进展示 — 整页复刻

> 认领：task-claim FE-ACH-03A（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--ach03-space-time`（分支 feat/ach03-space-time，基点 1834a50，node_modules/ 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰其他 ach01/02/04/05 worktree 与主工作区；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：bid-reference §1.1.1.1.4.6 时空演进 a/b/c 三项五级功能
- demo 真源（只读对照，禁 import/merge）：`D:\web\gkx-lumen\repos\demo-ui-science\src\pages\achievement-preview-new\space-time-evolution-new\`（SpaceTimeEvolutionNewPage.jsx 1441 / WorldEvolutionMap.jsx 200 / mockData.js 485）
- lumen 落点：`src/views/achievement/space-time-evolution/`（S01 页壳已建，本单补全整页）
- 路由：`tech-time-evolution` 已挂接（勿改 menu.ts）

## 2. S01 基座已提供的接口（必读，禁止重造）

- 数据：`fetchSpaceTimeEvolutionDataset()`（@/api/achievement）；类型 @/types/achievement
- 种子（已冻结，禁改动）：`src/mock/modules/achievementSpaceTimeSeed.ts`（**@ts-nocheck，20 城市画像 + 确定性数学生成器全套**：STE_YEARS/DIMENSIONS/THEMES/LEVELS/WARNING_LEVELS/getHotspots/getRegionStats/getThemeTopCities/getFrontierReport/FLOW_PATHS/RESEARCH_SUBJECTS/THEME_EVOLUTION… 直接消费）
- 公共件：`_shared/` 三组件 + `useAchievementTrack`；复刻经验清单 + 仓 AGENTS.md 开工必读

## 3. 交付要点（DoD 对照）

1. 时空控制台（左栏）：主题库多选（勾选后主题 Tab 并行出数）、四维度 Select、国家/省州/市层级 Radio、**时间轴选择/播放/暂停/回放**（interval 常量化、页面不可见暂停、卸载 clearTimeout）、热力层/密度轨迹 Checkbox、聚类口径 Radio、两区域/两时段对比（Select×2 或 年份×2）
2. 主区地图（世界视口 center [30,15] zoom 2）：点位大小随维度值、热力、流动路径（Polyline 三色：patent 紫/talent 绿/collab 蓝）、层级切换/热点定位/密度区 fitBounds 视口飞行；复用 `TiandituMap`，MapResizeHandler 语义保留
3. 三 Tab 全落点：① 热点预警与趋势报告（预警卡三级色 Tag、选中联动地图、趋势图、地域流动明细表+历史回溯）；② 主题时空分析（主题筛选、年度论文 Bar、季度对比、活跃区域行、主题演化路径 Stage 链、前沿报告）；③ 流动与协同网络（研究主体选择、世界地图流动、协作网络 graph、多维联动序列）
4. KPI 行（全球总量四维）挂 ⓘ+🧪；数据全部来自确定性生成器（**禁 Math.random、禁改生成器语义**——同一输入同一输出是时间轴播放的前提）
5. demo 原生控件全换 Arco Vue；图表容器显式高度；D9 全挂
6. 与 demo 逐区块截图对照进 handoff；三绿（type-check/自检/build）在本 worktree 执行

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技成果展示-ACH/FE-ACH-03A.md`（gkx-orchestration 主工作区），含对照表、架构合规、cost、`ponytail: full` 行；`task-update-fields` 回填
- 冲突预防：只新建/修改 `src/views/achievement/space-time-evolution/**`；禁改 `_shared/`、menu.ts、api、types、种子（需扩展时 note 登记 + handoff 说明）
