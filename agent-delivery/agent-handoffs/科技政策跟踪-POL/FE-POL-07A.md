# FE-POL-07A 智能研报生成 — 整页复刻（核增链终点）handoff

- **task**: FE-POL-07A · E-FE-POLICY-TRACKING · P1 · feature
- **claimed_by**: agent:frontend-agent · **supervised_by**: human:孔东
- **worktree**: `worktrees/lumen-ui-science-pc--pol07-insight-report`（分支 `feat/pol07-insight-report`，基点 f4edea4）
- **状态**: 完工停本地（⚠️ 未 commit/push，按 AGENTS.md 人工验收闸门 2026-10-20 等走查）
- **ponytail**: full（复刻不缩水：demo 语义逐段对照；新增代码仅页面 + 样式 + 自检，零新依赖、零新公共件）
- **demo 真源**: `repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx` PolicyInsightReport 段（L1724–2122）+ `policyPcData.js`（种子已冻结）+ `policyPcExport.js`（buildReportLines 语义移植）

## 1. 范围与实现（DoD 逐条对照）

| DoD | 实现 | 状态 |
|---|---|---|
| 四板块复刻（SRS 5 叶） | 政策深度分析（reportDepthSections 四节 + bg/cmp/insight/trace 正文）/ 洞察结论自动提炼（reportInsights + insightKindsReady 四类闸门，关则滤「风险提示」）/ 行业数据联动（industryDataset 双轨 + industryReady 闸门 + effect 节 a-table）/ 权威源引用（authorityType/Name/Library/URL 全链） | ✅ |
| 结论溯源 | activeSection/activeInsight 侧栏锚点；traceDir 双向（结论→原文：洞察→政策→条款→摘录→权威源→可验证判定；原文→结论：traceIndexRows→关联结论→可关联洞察→「查看」回切）；sourceClauseKey + traceDone 完成标记（canVerify = traceDone ∧ 定位 ∧ 关联 ∧ authorityUrl） | ✅ |
| 模板导出 | reportOutline 8 节大纲；exportReportPdf/Word → `exportHtmlDoc(…, '政策智能研报', fmt)`（PDF=可打印 HTML / Word=.doc）；templateReady + fourKindsReady 闸门（不全 canExport=false 双按钮禁用） | ✅ |
| ChainSteps 收尾 | 内联占位（a-steps current=3 治理→拆解→对比→研报 + changeable 回跳 router.push + 「返回科创政策全景」按钮），评审层自闸 | ✅（见 §3 偏离 1） |
| Arco 化 | demo antd Statistic/List/Descriptions/Steps/Select/Switch/Alert → PolicyStatCard（复用）+ a-descriptions/a-steps/a-select/a-switch/a-alert/a-empty/a-table；色 geekblue→#2F54EB（Arco 无该预设色） | ✅ |
| D9 ⓘ/🧪 | M_POLICY_EFFECT_SCORE（QPOL-02 ⚠️）/ M_POLICY_LAYOUT_REC_COUNT 经 PolicyStatCard ⇒ ⓘ + 🧪；正文卡角标「演示正文」 | ✅ |

## 2. 产物清单

| 文件 | 内容 |
|---|---|
| `src/views/policy/insight-report/index.vue` | 整页填充（+442/-22）：四板块 + 双向溯源 + 四开关（sessionStorage `pol-report-*-ready` 键持久化，loadFlag/saveFlag 复用冻结种子）+ 导出 + ChainSteps 内联占位 + 观测埋点 |
| `src/views/policy/styles/demo-policy-pc-pages.css` | 追加 `pol-report-` 前缀类 30 个（+201 行；未触碰 04A/05A/06A 的 ppc-/pol-* 类） |
| `src/views/policy/insight-report/FE-POL-07A.test.mjs` | 最小自检（新）：四类闸门 / 溯源双向互链 / 大纲+行业联动 / 页面锚点 / 样式锚点 |

## 3. 偏离说明

1. ~~**ChainSteps 内联占位**~~ **已闭环（2026-11-03）**：04A 正式件合入 dev 后，本页已替换为 `<PolicyChainSteps current="report" class="ppc-chain" />`（与 06A 同款消费；组件自含评审自闸与埋点，终点无 next 按钮），内联占位及 `CHAIN_ROUTES`/`chainGo` 残留一并移除，自检断言同步更新。
2. **导出实现**：demo `policyPcExport.js` 用 jsPDF + canvas 中文渲染；本仓未装 jsPDF → 按派单包 §2 指定走 `panorama/trackingExport.ts` 的 `exportHtmlDoc`（PDF=可打印 HTML 另存、Word=.doc），与 01B/02A 同策略。buildReportLines 的分节文案（bg/cmp/insight/trace）逐段移植。
3. **tag 色**：demo antd `geekblue` → Arco `#2F54EB`（视觉等价，Arco 无该预设名）。

## 3.1 合并记录（2026-11-03）

- worktree 提交 `2ef6128` → merge `b9e66d7` 入本地 `dev`（css 冲突按 05A/06A 先例解决：三方追加块并存）
- dev 三绿复跑 ✅（vue-tsc / FE-POL-07A.test.mjs / policy.test.mjs / vite build 27.49s）
- 临时分支 `feat/pol07-insight-report` 与 worktree 已删除（残留 vite 子进程 16536 已清）

## 4. 验收证据（三绿 + 浏览器实测）

- `pnpm exec vue-tsc --build` ✅（类型门；注：worktree node_modules 为 junction，pnpm 前置 install 报 hoist 警告不影响 exec 直跑）
- `node src/views/policy/insight-report/FE-POL-07A.test.mjs` ✅（本单自检）
- `node src/views/policy/policy.test.mjs` ✅（S01 基座 10 组断言未破坏：种子冻结/菜单/双轨/D9 镜像）
- `pnpm exec vite build` ✅（24.18s，既有 chunk 警告与本次无关）
- 浏览器实测（dev 5194 + review=1）：四板块渲染齐；关「四类提炼」→ 导出双禁用 + 风险提示滤除 + 效果分卡空态（demo 文案逐字）；点「结论→原文」→ 节切「八、溯源附录」+ 面板选中该洞察 + 摘录正确；traceDir 切「原文→结论」→ 默认条款 ti1 + 关联结论 + 2 条可关联洞察（核心观点/决策建议）；「可验证/可追溯/可复核」绿标在场。截图：`Temp/cursor/screenshots/pol07-full.png`（整页 1377×1318）

## 5. 架构合规自检

- D8 前端规范 ✅（Arco 全覆盖、主色 #165DFF、pol-report- 前缀、第二处出现才封装——本页全单次使用故页内类不抽公共件）
- D9 血缘 ✅（指标只读消费镜像 policyMetricsMirror.gen；QPOL ⚠️ 读 pendingRef；禁前端改绿）
- D10 交互 ✅（键盘可达走 Arco 原生；禁互斥 display 叠加）
- 评审层 ✅（开关族/分轨横幅/ChainSteps 全部 reviewMode 自闸；关闭后 DOM 零泄漏——核增链路字样仅评审态）
- 调用链 ✅（fetchPolicyInsightReport 双轨；未越层、未碰 demo-* 服务）
- 冲突预防 ✅（只动 `insight-report/**` + 共享 css 追加块；未碰 menu.ts/api/种子/兄弟单目录）

## 6. 开放项

- ~~ChainSteps 正式件待 04A 合入后替换~~ 已闭环（§3.1，2026-11-03）
- 对比槽空态（未选对象时）依赖 06A 的对比页写入会话槽；当前 loadCompareSlots 默认 2 项演示值，符合 demo 语义
