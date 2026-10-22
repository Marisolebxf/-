# 派单包 · FE-ACH-04A 大型科学仪器共享 — 整页复刻

> 认领：task-claim FE-ACH-04A（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--ach04-instrument`（分支 feat/ach04-instrument，基点 1834a50，node_modules/ 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰其他 ach01/02/03/05 worktree 与主工作区；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：bid-reference §1.1.1.1.4.6 仪器共享 a/b/c 三项五级功能
- demo 真源（只读对照，禁 import/merge）：`D:\web\gkx-lumen\repos\demo-ui-science\src\pages\achievement-preview-new\instrument-sharing-new\`（InstrumentSharingNewPage.jsx 1057 / InstrumentMap.jsx 158 / mockData.js 247，KPIS 自带 metricId+lineage，真实口径数值：入网 9,262 台套等）
- 报告生成语义对照（仅读语义，禁 import）：`demo-ui-science/src/pages/achievement-preview/modules/instrument-sharing/orgAnalysisReport.js`（buildOrgAnalysisReport/downloadOrgAnalysisReport/flattenInstitutionRows）
- lumen 落点：`src/views/achievement/instrument-sharing/`（S01 页壳已建，本单补全整页）
- 路由：`instrument-sharing` 已挂接（勿改 menu.ts）

## 2. S01 基座已提供的接口（必读，禁止重造）

- 数据：`fetchInstrumentSharingDataset()`（@/api/achievement）；类型 @/types/achievement
- 种子（已冻结，禁改动）：`src/mock/modules/achievementInstrumentSeed.ts`（INSTRUMENTS/KPIS/ORDERS/SERVICES/INSTITUTIONS/PLATFORM_PROFILE/各类 META…）
- 公共件：`_shared/` 三组件 + `useAchievementTrack`；复刻经验清单 + 仓 AGENTS.md 开工必读

## 3. 交付要点（DoD 对照）

1. Tab a 仪器盘点：KPI 卡（demo 真实口径数值）、类别/状态/区域筛选、三态着色地图（在用/闲置/维修）+ 聚合、仪器列表、状态分布/趋势图表
2. Tab b 预约服务：服务清单（类型/状态 Tag）、订单追踪表（ORDER_STATUS_META 着色）、预约与评价交互按 demo 演示态（Message 提示，不替 BE 拍板落库）
3. Tab c 服务机构：**机构分类地图**（ORG_TYPE_META 着色）、机构列表（flattenInstitutionRows 语义）、机构分析报告（buildOrgAnalysisReport/downloadOrgAnalysisReport 的 Vue/TS 等价实现放本模块目录，禁引用 demo 路径）
4. 地图复用 `TiandituMap`；demo 原生控件全换 Arco Vue；图表容器显式高度；D9 ⓘ+🧪 全挂（metricId 直读 KPIS）
5. 与 demo 逐区块截图对照进 handoff；三绿（type-check/自检/build）在本 worktree 执行

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技成果展示-ACH/FE-ACH-04A.md`（gkx-orchestration 主工作区），含对照表、架构合规、cost、`ponytail: full` 行；`task-update-fields` 回填
- 冲突预防：只新建/修改 `src/views/achievement/instrument-sharing/**`；禁改 `_shared/`、menu.ts、api、types、种子（需扩展时 note 登记 + handoff 说明）
