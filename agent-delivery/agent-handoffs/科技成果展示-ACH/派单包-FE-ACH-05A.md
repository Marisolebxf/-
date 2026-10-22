# 派单包 · FE-ACH-05A 创新载体孵化载体 — 整页复刻

> 认领：task-claim FE-ACH-05A（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--ach05-incubation`（分支 feat/ach05-incubation，基点 1834a50，node_modules/ 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰其他 ach01~04 worktree 与主工作区；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：bid-reference §1.1.1.1.4.6 孵化载体 a/b/c/d 四项五级功能
- demo 真源（只读对照，禁 import/merge）：`D:\web\gkx-lumen\repos\demo-ui-science\src\pages\achievement-preview-new\incubation-carrier-new\`（IncubationCarrierNewPage.jsx 1471 / CarrierMap.jsx 116 / mockData.js 833）
- lumen 落点：`src/views/achievement/incubation-carrier/`（S01 页壳已建，本单补全整页）
- 路由：`innovation-carrier` 已挂接（勿改 menu.ts）

## 2. S01 基座已提供的接口（必读，禁止重造）

- 数据：`fetchIncubationCarrierDataset()`（@/api/achievement）；类型 @/types/achievement
- 种子（已冻结，禁改动）：`src/mock/modules/achievementIncubationSeed.ts`（carriers/enterprises/policies/operations/faqs/newsFeed/MAP_LEVELS/STAGE_COLORS/…）
- 公共件：`_shared/` 三组件 + `useAchievementTrack`；复刻经验清单 + 仓 AGENTS.md 开工必读

## 3. 交付要点（DoD 对照）

1. KPI 行：监测载体总数/入驻企业/累计融资/平均毕业率/企业满意度（M_IC_* 占位 id，S01 已建，随筛选联动）
2. Tab a 分布全景：层级地图（MAP_LEVELS）、载体类型/区域/行业筛选、点位着色（TYPE_COLOR_MAP）、载体增长趋势 Bar+势能指数、载体列表
3. Tab b 入驻企业与成果：企业列表（行业/融资/专利）、行业聚集 Pie（可切换维度，M_IC_ENT_INDUSTRY）、在孵企业成长轨迹、项目亮点、**投资人图文报告**：生成（buildInvestorGraphicReport 语义，IMAGE_GRADIENTS 卡片）→ 预览 Modal → 打印/PDF → 下载 HTML → localStorage 归档（PROJECT_ARCHIVE_KEY 语义，演示态不替 BE 拍板）
4. Tab c 政策资源联动：政策筛选（POLICY_LEVELS/POLICY_TYPES 着色 Tag）、**申报流程 Steps + 申报材料清单 + 咨询互动 FAQ（IconQuestionCircle/客服语义）**——这是 demo New 页补齐旧页缺口的重点，必须完整
5. Tab d 绩效监控：满意度（Rate+优劣项）、毕业率、运营指标、carrierGrowthTrend/potentialIndexTrend 图表
6. 载体详情 Modal 四 Pane：详细资料 Descriptions / 图片（渐变占位语义）/ 视频 / 资讯 newsFeed
7. 地图复用 `TiandituMap`；demo 原生控件全换 Arco Vue；图表容器显式高度；D9 ⓘ+🧪 全挂
8. 与 demo 逐区块截图对照进 handoff；三绿（type-check/自检/build）在本 worktree 执行

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技成果展示-ACH/FE-ACH-05A.md`（gkx-orchestration 主工作区），含对照表、架构合规、cost、`ponytail: full` 行；`task-update-fields` 回填
- 冲突预防：只新建/修改 `src/views/achievement/incubation-carrier/**`；禁改 `_shared/`、menu.ts、api、types、种子（需扩展时 note 登记 + handoff 说明）
