# 派单包 · FE-POL-06A 多维政策对比 — 整页复刻

> 认领：已 task-claim（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol06-compare`（分支 `feat/pol06-compare`，基点 f4edea4，node_modules 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰 pol03/04/05/07 worktree、主工作区与其他仓；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：SRS `政策对比功能升级（核增需求）/` 多维政策对比 4 叶
- demo 真源（只读对照，禁 import/merge）：`repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx` 的 `PolicyCompareUpgrade` 段（L1052–1723）+ `policyPcExport.js` 导出段（165）
- lumen 落点：`src/views/policy/compare/`（S01 页壳已建，本单填充整页；样式入 `styles/demo-policy-pc-pages.css` 追加 `pol-compare-` 前缀类，避免与 04A/05A 类名冲突）
- 路由已挂接（勿改 menu.ts）

## 2. S01 基座 + 04A 并行件

- 数据：`fetchPolicyCompare({})`（@/api/policy，双轨）；`createCompareDataset()`（@/mock/modules/policy）
- 种子（policyPcSeed.ts 已冻结，禁改动）：`COMPARE_SLOTS_KEY` / `compareDimensions`（四维：clause/support/scope/pathway）/ `compareScoreMatrix` / `buildCompareFindings()` / `buildCompareGraph()` / `diffIdentifiedByThreshold()` / `loadCompareSlots()` / `saveCompareSlots()` / `COMPARE_RAN_KEY` / `loadCompareRan()` / `saveCompareRan()`
- **PolicyChainSteps**（04A 首装共享件）：并行期处理同 05A 派单包 §2（内联占位 + handoff 登记，勿自建正式版）
- 公共件：`PageTabFrame` / `PolicyStatCard` / `MockBadge` / `useReviewStore` / `usePolicyTrack`
- 导出：可复用 `panorama/trackingExport.ts` 的 `exportHtmlDoc`（01B 已沉淀）做汇总文档导出

## 3. 交付要点（DoD 对照）

1. **会话槽对比篮**：loadCompareSlots/saveCompareSlots localStorage 持久化 + 槽位管理（添加/移除/清空，含上限提示）；**展示侧分轨铁律：对比对象仅存展示侧会话槽，禁止写入专题系统对比篮**（BoundaryBanner 语义照搬 + 评审层集中管理 + 关闭零泄漏，D8）
2. **对比配置**：维度勾选（compareDimensions 四维）/ 区域筛选（regionFilter）/ 级别筛选（levelFilter）/ **权重调节**（weight 滑杆，影响 buildCompareFindings 评分）
3. **对比执行**：running 进行态 + ran 完成态（loadCompareRan/saveCompareRan）+ **buildCompareFindings 差异发现**（diffIdentifiedByThreshold 阈值识别，阈值可调）+ **buildCompareGraph 对比图谱**（echarts graph，VChart 渲染）+ secondaryNote 补充说明
4. **报告导出**：exportCompareSummaryDoc 语义 → 用 exportHtmlDoc 生成对比汇总文档（对比结论 + findings 清单）
5. demo 原生控件全换 Arco；图表容器显式高度；D9 ⓘ/🧪

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技政策跟踪-POL/FE-POL-06A.md`（gkx-orchestration 主工作区）；`task-update-fields` 回填
- 三绿在本 worktree 执行
- 冲突预防：只改 `src/views/policy/compare/**` + `styles/demo-policy-pc-pages.css` 追加 `pol-compare-` 前缀类；禁改 menu.ts / api / 种子 / 其他单目录
