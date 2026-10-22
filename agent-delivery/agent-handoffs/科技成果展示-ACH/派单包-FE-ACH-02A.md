# 派单包 · FE-ACH-02A 科技创新生态展示 — 整页复刻

> 认领：task-claim FE-ACH-02A（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--ach02-innovation-eco`（分支 feat/ach02-innovation-eco，基点 1834a50，node_modules/ 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰其他 ach01/03/04/05 worktree 与主工作区；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：bid-reference §1.1.1.1.4.6 创新生态 a/b/c 三项五级功能
- demo 真源（只读对照，禁 import/merge）：`D:\web\gkx-lumen\repos\demo-ui-science\src\pages\achievement-preview-new\innovation-ecosystem-new\`（InnovationEcosystemNewPage.jsx 1207 / EcoMap.jsx 100 / mockData.js 278，KPI_META 含 M_IE_* 原 metricId+lineage）
- lumen 落点：`src/views/achievement/innovation-ecosystem/`（S01 页壳 KPI 行已消费 KPI_META，本单补全三 Tab 整页）
- 路由：`innovation-ecology` 已挂接（勿改 menu.ts）

## 2. S01 基座已提供的接口（必读，禁止重造）

- 数据：`fetchInnovationEcosystemDataset()`（@/api/achievement）；类型 @/types/achievement
- 种子（已冻结，禁改动）：`src/mock/modules/achievementInnovationEcosystemSeed.ts`（carriers/talents/network/performance/KPI_META/CARRIER_TYPES…）
- 公共件：`_shared/` 三组件 + `useAchievementTrack`；复刻经验清单 + 仓 AGENTS.md 开工必读

## 3. 交付要点（DoD 对照）

1. Tab a 创新载体地图与增量分析：层级（大湾区/深圳/行政区）视口切换、点位/热力/增量高亮三模式、载体类型 Checkbox 筛选、季度新增 Bar（markPoint 峰值）/年度新增 Bar+同比 Line、分区对比表、类型结构 Pie、载体详情 Drawer（Descriptions+资料下载演示）
2. Tab b 人才态势分析：人才点位/聚集热力、类别 Pie、年度流入 Bar、学科分布 Bar、岗位层次 Bar、技术领域雷达（vs 全国基准）、典型案例、人才详情 Drawer
3. Tab c 载体人才协作关系分析：叠加图层 Checkbox（载体/人才热力/热点/连线）+ Polyline 网络、协作网络 ECharts graph（roam/emphasis adjacency）、协同项目进展 Timeline+Drawer、影响力雷达、联合产出四卡（M_IE_* metricId+lineage 直读种子）
4. 地图复用 `TiandituMap`（热力 props 已支持；视口飞行/尺寸刷新语义对齐 demo EcoMap 的 ViewportController/MapResizeHandler）；Tabs 切换重挂载时 `invalidateSize`
5. demo 原生控件全换 Arco Vue；图表容器显式高度；D9 ⓘ+🧪 全挂；写操作（资料下载提示）保持演示态
6. 与 demo 逐区块截图对照进 handoff；三绿（type-check/自检/build）在本 worktree 执行

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技成果展示-ACH/FE-ACH-02A.md`（gkx-orchestration 主工作区），含对照表、架构合规、cost、`ponytail: full` 行；`task-update-fields` 回填
- 冲突预防：只新建/修改 `src/views/achievement/innovation-ecosystem/**`；禁改 `_shared/`、menu.ts、api、types、种子（需扩展时 note 登记 + handoff 说明）
