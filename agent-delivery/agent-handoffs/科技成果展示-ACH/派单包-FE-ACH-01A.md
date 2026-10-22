# 派单包 · FE-ACH-01A 软科学成果展示 — 整页复刻

> 认领：task-claim FE-ACH-01A（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--ach01-soft-science`（分支 feat/ach01-soft-science，基点 1834a50，node_modules/已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰其他 ach02~05 worktree 与主工作区；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：bid-reference §1.1.1.1.4.6 软科学 a–g 七项五级功能
- demo 真源（只读对照，禁 import/merge）：`D:\web\gkx-lumen\repos\demo-ui-science\src\pages\achievement-preview-new\soft-science-new\`（SoftScienceNewPage.jsx 460 / MapSection.jsx 337 / BottomTabs.jsx 1084 / mockData.js 244 / softScienceNewUtils.js + test.mjs）
- lumen 落点：`src/views/achievement/soft-science/`（S01 已建页壳：KPI 行 + 表格骨架，本单替换骨架区为整页）
- 路由：`soft-science-achievements` 已挂接（勿改 menu.ts）

## 2. S01 基座已提供的接口（必读，禁止重造）

- 数据：`fetchSoftScienceDataset()`（@/api/achievement，defineApi 双轨）；类型 @/types/achievement
- 种子（已冻结，禁改动）：`src/mock/modules/achievementSoftScienceSeed.ts`（SS_TOPICS/CATEGORIES/STAGES/REGION_TREE/PROVINCE_COORDS…）+ `achievementSoftScienceUtils.ts`（enrichSoftScienceTopics/buildStageTimeline/buildArchives/…）
- 公共件：`_shared/AchievementPageShell|AchievementSectionCard|AchievementKpiTile`（已复用 MetricSpecHint+MockBadge）、`useAchievementTrack`
- 复刻经验（开工必读）：`agent-delivery/agent-handoffs/科技发展态势-TS/TS-demo-lumen复刻经验清单.md` + 仓 AGENTS.md「demo→lumen 复刻经验」

## 3. 交付要点（DoD 对照）

1. 左侧组合筛选：年度范围 Slider / 单位类型 / 课题主题 Checkbox / 成果标签 Tag 可选 / 省市区 Cascader（changeOnSelect+hover 展开）/ 筛选方案 localStorage 保存·复用·删除·重置
2. 五级地图（country→province→city→district→unit）：逐级下钻、热力层、flyTo 视口、**列表悬停↔地图节点高亮联动**（getNodeKeyForTopic 语义）；复用 `TiandituMap`（props 传 marker/热力/视口，禁页内手写 leaflet init）；Leaflet `isolation:isolate` + 瓦片 `max-width:none`
3. 智能检索列表：7 种排序、难题类型优选（优选置顶+紫标）、热词/新兴主题点击回填、课题详情 Modal（Descriptions）
4. 底部 5 Tab 全落点：成果详情与案例 / 多维统计分析 / 互动传播中心（点赞收藏评论） / 导出与报告管理 / 进展跟踪监控（阶段评价+滞后课题）
5. demo 原生控件全换 Arco Vue（已知坑按经验清单 §1 根因修法：#option 插槽 {data}、label 不包裹 a-select、图标显式 import、32px/4px token）
6. 图表容器显式高度防 init 0 高死锁；新图表类型查 `src/config/echarts.ts` 是否已注册（已含全量，若缺再补）
7. D9：KPI/统计数字旁 ⓘ（MetricSpecHint）+ 🧪（MockBadge），metricId 沿用种子与占位 id；评审门控关闭后 DOM 零泄漏
8. 写操作（筛选方案/评价/收藏）保持 localStorage 会话级，不替 BE 拍板
9. 自检：`softScienceNewUtils.test.mjs` 按 demo 断言语义摘选移植最小 test.mjs；交付三绿（`pnpm type-check` / 自检 / `pnpm build`）
10. 验证命令均在本 worktree 目录执行

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**（2026-10-20 用户裁定）；handoff 写 `agent-delivery/agent-handoffs/科技成果展示-ACH/FE-ACH-01A.md`（在 gkx-orchestration 主工作区写，不改业务仓），含逐区块与 demo 截图对照表、架构合规、cost 回填、`ponytail: full` 行
- handoff 后 `task-update-fields` 回填 evidence + cost；等 human:孔东 人工验收授权后再 commit/push
- 冲突预防：只新建/修改 `src/views/achievement/soft-science/**` 与 `src/mock/modules/achievementSoftScienceUtils.ts`（若需）；禁改 `_shared/`、menu.ts、api、types（需要扩展时在 note 登记并在 handoff 说明，交协调统一处理）
