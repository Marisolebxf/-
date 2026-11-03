# FE-POL-06A · 多维政策对比整页复刻 — Handoff

- 任务：FE-POL-06A 多维政策对比整页复刻（核增 4 叶）— 会话槽对比篮 + 维度/权重配置 + 差异发现 + 对比图谱 + 导出
- 执行：agent:frontend-agent · 监管：human:孔东 · 状态：in_progress → 停本地待人工验收（2026-10-20 闸门，未 commit/push）
- 工作区：worktree `D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--pol06-compare`（分支 `feat/pol06-compare`，基点 f4edea4）
- 派单包：`agent-delivery/agent-handoffs/科技政策跟踪-POL/派单包-FE-POL-06A.md`
- demo 真源：`repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx` PolicyCompareUpgrade 段（L1052–1723）+ `policyPcExport.js` exportCompareSummaryDoc 段（L165–179）
- ponytail: full

## 1. 范围与实现（DoD 对照）

| DoD | 实现 |
|---|---|
| 会话槽对比篮 | `loadCompareSlots/saveCompareSlots`（种子冻结函数，sessionStorage `display-policy-compare-slots`）接线；上限 3（demo `buildCompareFindings` slice(0,3) 语义 → 超选显式 warning + 截取）；配置/槽/维度变更即 `resetRun()`（demo setRan(false)+saveCompareRan(false)）。**分轨铁律**：无任何专题对比篮 API/存储调用（自检 §2 断言） |
| 对比配置 | `compareDimensions` 五维（clause/coreMetric/support/scope/pathway）勾选（demo 初始 4 维）；regionFilter（全部/深圳市/国家层面/欧盟）/ levelFilter（全部/国家级/市级/海外）；weight 0.8/1/1.2 · threshold 5/10/20/99 · timeWindow all/1y/3y（a-select，变更复位 ran） |
| 对比执行 | running（600ms 演示态）+ ran（loadCompareRan/saveCompareRan sessionStorage）；三重运行闸门（<2 对象 / 空维度 / 时间窗内 <2）文案照搬 demo；`buildCompareFindings` 四卡（共性/差异/互补/冲突）+ `diffIdentifiedByThreshold` 差异闸门（未识别→GateEmpty 语义 a-empty）；`buildCompareGraph` → VChart force graph（echarts.ts GraphChart 已注册，无新增注册）；雷达/柱状（scoreFromMetrics 计分，权重联动）；`coreFeaturesFromMetrics` 核心特征表+清单；secondaryNote 二次分析（reviewMode 门控，照搬 demo ReviewOnly） |
| 报告导出 | `exportCompareSummaryDoc` 语义 → 复用 01B `panorama/trackingExport.ts` 的 `exportHtmlDoc`（对象清单 + 对比摘要 + findings 四节 → `政策对比摘要_*.doc`）；分享（clipboard 摘要+核心结论）；生成研报 = saveCompareSlots + saveCompareRan(true) + router push `policy-insight-report`（07A 落地后接续） |
| Arco 化 | antd Select/Checkbox/Table/Steps/Alert/Empty/Tag → a-select/a-checkbox/a-table-column 声明式（#cell 插槽挂 D9 ⓘ）/a-steps/a-alert/a-empty/a-tag；图标显式 import（IconSwap/IconPlayCircle/IconFile/IconExport/IconShareAlt/IconRefresh/IconArrowRight/IconLeft/IconRight，均核过 arco-vue-icon 导出名） |
| D9 ⓘ/🧪 | 维度标签挂 PolicyMetricSpecTrigger（种子 metricId：M_POLICY_INTENSITY_SCORE / M_POLICY_SUPPORT_STRENGTH / M_POLICY_INDUSTRY_FIT）+ PendingBadge（QPOL-02）+ MockBadge；表格单元格 ⓘ 随行挂；读模块镜像 `policyMetricsMirror.gen`（不照抄 demo catalog） |

## 2. 产物清单（worktree 内，未 commit）

- `src/views/policy/compare/index.vue` — 整页（壳骨架替换；~600 行）
- `src/views/policy/compare/PolicyCompareWorkbench.vue` — 对比工作台（对比表 + 核心特征表 + 雷达/柱状；样式自含；±280px 平滑滚动条查询 `.arco-table-body`）
- `src/views/policy/compare/FE-POL-06A.test.mjs` — 最小自检（20 组断言）
- `src/views/policy/styles/demo-policy-pc-pages.css` — **仅追加** `pol-compare-` 前缀段（S01 冻结主体未动）；另给 ppc-compare-table-wrap 滚动条组补 `.arco-table-body` 选择器（Arco 类名承接，数值不重写）

未改：menu.ts / api / 种子（policyPcSeed.ts 冻结）/ 其他单目录。

## 3. 交付三绿 + 走查证据

- `node src/views/policy/compare/FE-POL-06A.test.mjs` → 20 组全绿 ✓
- `node src/views/policy/policy.test.mjs`（基座自检回归）→ 全绿 ✓
- `vue-tsc --build` → 0 错 ✓
- `vite build` → 24.93s 绿 ✓
- 浏览器走查（dev :5199，`?review=1`）：页面挂载完整（默认 2 槽对象 + ran 态）；点「运行对比」→ 600ms 完成态（对比表 ×2 + findings 4 卡 + 核心特征 4 条 + 核心结论 5 条，sessionStorage ran=1）；二次分析 alert 渲染；雷达 460×280 / 柱状 460×260 / 图谱 970×260（无 0 高死锁）；`review=0` 关闭评审 → 角标/横幅/链路条全隐藏（DOM 命中仅为 Vue 模板注释，无 metric_id/QPOL/就绪度可见泄漏）

## 4. 偏离说明

1. **jsPDF 导出 → exportHtmlDoc .doc**：与 01B 同策略（仓内未装 jsPDF，PDF 走打印页策略沿用；01B handoff 已登记，本单不重复决策）。
2. **槽上限显式提示**：demo 多选不设限仅 `buildCompareFindings` 内静默 slice(0,3)；本单在 select 层截取 + warning 提示（复刻精度内增强诚实性，数值语义不变）。
3. **ChainSteps 内联占位**：04A 正式件 `PolicyChainSteps.vue` 并行未交付，按派单包 §2 内联同语义占位（current=2、「下一步：智能研报生成」→ router push 研报页），**04A 合并后替换消费**（与 05A 同款约定）。
4. **Arco 表格滚动条类名**：S01 冻结 css 仅 `.ant-table-*` 前缀选择器；Arco 下追加 `.arco-table-body` 并列选择器（不改数值、不动冻结声明本体，追加行集中在滚动条组）。
5. **生成研报跳转**：demo `onTopicChange('智能研报生成')` → router push `policy-insight-report`（07A 页现为 S01 壳，跳转已可达；07A 交付后自然承接）。

## 5. 架构合规自检（§2 铁律）

- D8 Design/Arco ✓（全 Arco 控件，token #165DFF，正文 13/14px）
- D9 血缘 ✓（ⓘ 读模块镜像；Mock 🧪；QPOL ⚠️；文案不自造）
- D10 交互 ✓（键盘可达沿用 Arco；空态 a-empty）
- D12 隔离 ✓（零 demo import/merge；语义等价 Vue 重写）
- 分轨铁律 R7/D8 ✓（会话槽仅展示侧 sessionStorage；BoundaryBanner 双横幅照搬语义；评审层 useReviewStore 自闸，关闭零泄漏）
- 可观测 ✓（trackPolicyInteraction：page-mounted / slots-change / run / go-report / export-summary / secondary-analysis）
- 互斥 display 不叠同一节点 ✓（自检断言）
- 完工停本地 ✓（无 commit/push，等孔东走查）

## 6. 开放项

- 04A 合并后：本页内联 ChainSteps 占位替换为 `PolicyChainSteps.vue` 正式件（消费替换，一处 import）。
- 07A 交付后：「生成研报」落地页从 S01 壳变整页（跳转无需改动）。
- BE-POL-CONTRACT-01 冻结后：`fetchPolicyCompare` real 路径接线 + USE_MOCK=false 联调。

## 7. cost 回填

- actual_tokens: ~215k（含走查浏览器轮次） · model_used: glm-5.3 · actual_cost: ~$0.9 · cost_warn: false
