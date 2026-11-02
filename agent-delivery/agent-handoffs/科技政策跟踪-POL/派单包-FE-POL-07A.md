# 派单包 · FE-POL-07A 智能研报生成 — 整页复刻（核增链终点）

> 认领：已 task-claim（agent:frontend-agent，监管 human:孔东）→ 开工 `task-update-status in_progress`
> 工作区：**仅在此 worktree 作业**：`D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol07-insight-report`（分支 `feat/pol07-insight-report`，基点 f4edea4，node_modules 已 junction，.env 已复制）
> 强度：ponytail full
> 本单为**独立窗口并行任务**：禁止触碰 pol03/04/05/06 worktree、主工作区与其他仓；本 worktree 内只改本单文件

## 1. 真源与范围

- 需规：SRS `政策对比功能升级（核增需求）/` 智能研报生成 5 叶（excel 617–621）
- demo 真源（只读对照，禁 import/merge）：`repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx` 的 `PolicyInsightReport` 段（L1724–2051）+ `policyPcExport.js`（165）
- lumen 落点：`src/views/policy/insight-report/`（S01 页壳已建，本单填充整页；样式入 `styles/demo-policy-pc-pages.css` 追加 `pol-report-` 前缀类，避免与 04A/05A/06A 类名冲突）
- 路由已挂接（勿改 menu.ts）

## 2. S01 基座 + 04A 并行件

- 数据：`fetchPolicyInsightReport({})`（@/api/policy，双轨）；`createInsightReportDataset()`（@/mock/modules/policy）
- 种子（policyPcSeed.ts 已冻结，禁改动）：`reportOutline` / `reportInsights` / `INSIGHT_KINDS`（四类）/ `insightKindsReady()` / `industryDataset` / `reportDepthSections` / `traceIndexRows` / `buildEffectConclusion()` / `loadFlag()`/`saveFlag()`
- **PolicyChainSteps**（04A 首装共享件）：并行期处理同 05A 派单包 §2（内联占位 + handoff 登记，勿自建正式版）；**本单是 ChainSteps 链终点**（report 节点高亮 + 收尾态）
- 公共件：`PageTabFrame` / `PolicyStatCard` / `MockBadge` / `useReviewStore` / `usePolicyTrack`
- 导出：复用 `panorama/trackingExport.ts` 的 `exportHtmlDoc`（PDF 走可打印 HTML，Word 走 .doc，与 01B/02A 同策略）

## 3. 交付要点（DoD 对照）

1. **四板块复刻**（SRS 5 叶）：政策深度分析（reportDepthSections）/ 洞察结论自动提炼（reportInsights + insightKindsReady 四类就绪闸门）/ 行业数据联动（industryDataset + industryReady）/ 权威源引用（权威源列表 + 引用格式）
2. **结论溯源**：activeSection/activeInsight 侧栏导航锚点 + **结论↔条款溯源**（traceIndexRows + traceDir 双向：结论→条款 / 条款→结论 + sourceClauseKey + traceDone 完成标记）
3. **模板导出**：reportOutline 大纲 + exportReportPdf/exportReportWord 双格式（exportHtmlDoc）+ **模板就绪 templateReady 闸门 + 四类就绪 fourKindsReady**（不全不亮导出）
4. **ChainSteps 收尾**：核增 4 页串联终点（report 高亮 + 前序节点可回跳 vue-router push）
5. demo 原生控件全换 Arco；D9 ⓘ/🧪

## 4. 闸门与交付

- **完工停本地 worktree，严禁自动 commit/push**；handoff 写 `agent-delivery/agent-handoffs/科技政策跟踪-POL/FE-POL-07A.md`（gkx-orchestration 主工作区）；`task-update-fields` 回填
- 三绿在本 worktree 执行
- 冲突预防：只改 `src/views/policy/insight-report/**` + `styles/demo-policy-pc-pages.css` 追加 `pol-report-` 前缀类；禁改 menu.ts / api / 种子 / 其他单目录
