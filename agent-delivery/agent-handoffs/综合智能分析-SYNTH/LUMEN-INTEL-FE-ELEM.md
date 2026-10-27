# LUMEN-INTEL-FE-ELEM — 要素分析三页复刻（三透镜/四维评分/贡献路径）

- 任务：LUMEN-INTEL-FE-ELEM（E8-综合智能分析 / implementation / P0 / lumen-ui-topic）
- 强度：ponytail full
- 状态：in_progress → integration（停本地待走查，未推远端）
- commit：worktree 分支 `intel/fe-elem` `6b45ffc`（基于 origin/dev 4c87b38）
- 监管人：human:淮政玮（认领）；走查对齐 L1C 指引
- 工作目录：`worktrees/lumen-ui-topic--intel-elem`

## 1. 范围与实现（对照 DoD）

### DoD-1 工作台（ElementsWorkbenchView.vue）
- 条件栏/记录 Tab：消费 L1C `SynthContextBar`（actions slot 填 指标与方法说明/分析记录/生成分析报告）+ `SynthAnalysisRecordsPanel(leaf=region_innovation_elements)`
- 四结果态：`elementResultSource.ts` 统一推导 —— `instant`（默认三元组×有跑批，mock `getElementBatchSnapshot` 秒开）/ `task`（URL `view=result&task_id=` → #104 校验成功+ctx 匹配 → #105 resultData）/ `config`+`no_batch`（Alert 引导「开始分析」）
- 任务四决策：`startOrResumeSynthAnalysis`（L1B 桥，E.3/E.4/E.5 单飞+当天复用）+ `applySynthStartDecision` 文案导航；task 态提供「重新分析」force=true
- 仪表盘+三指数卡：gauge（compositeIndex）/ 类型·层次·领域三指数 + 权重环（pie 45–70%）
- 四维评分卡：规模/质量/结构/活跃度 + 「固定演示快照 · 非正式算法」Tag + Q-SYNTH-02 诚实文案
- 三透镜 Tab：综合总览（类型条形图+优势短板）/ 类型·七要素表 / 层次·结构表（达标 Tag）/ 领域·覆盖表；`lens` URL 参数持久化（replace）
- 贡献路径：element→target 列表 + 百分比 + 「演示关联权重，非因果归因；正式口径待甲方确认（Q-SYNTH-E-02）」
- 排名点击切区：#rank 行点击 `patchQuery({region, view:'config'})`（当前区不可点）
- 趋势：line 60–100 区间
- 三叶互跳：返回活力/查看协同，query 带 region/compare/window 上下文
- D9 角标：11 个 `M_SYNTH_ELEM_*` 全部挂 `IntelMetricMount`（评审自闸；missing 红问号 / draft 橙点 / 🧪 由共享件渲染，本页零手写状态）

### DoD-2 过程页（ElementTaskPage.vue）
- 要素五阶段文案：`ELEMENT_TASK_STAGES`（submit→gather→typelevel→domain→assemble；L1 mock 真源）
- SSE 接入：#109 `analysisTaskStream` progress/success/failed/cancelled → 步骤推进；终态补 #104 拿 endTime
- 排队可撤回（#107 cancel）；完成不自动跳（「查看分析结果」按钮 `markLocalResultViewed` 后带 `view=result&task_id` 回工作台）
- 双卡片布局对齐 demo（任务信息卡 + Steps 过程卡 + 状态 Alert + 按钮组）

### DoD-3 报告页（ElementReportPage.vue + elementReportDocument.ts）
- 七段式：`buildIndustryAnalysisReportDocument` 共件（report-identity→limitations）
- template `synth-element-report-v1`；task_type `region_innovation_elements_report`
- PDF 下载：`renderIndustryAnalysisReportPdf`（STSong 中文）+ `downloadReportBlob`
- 数据优先级：URL task_id → mock `getElementTaskResult`（确定性）；无 task_id → 默认跑批快照；均无 → 诚实空态提示返回

### 埋点
`elementTelemetry.ts`：`synth_elem_view/ctx_change/start_analysis/page_tab/method_open/report/nav_vitality/nav_collab/task_view/stage/view_result/report_view/report_download`。仓内无事件通道（observability.ts 仅 trace 头），DEV console.debug 过渡，`ponytail:` 注释标注升级路径。

### 偏离说明
- **demo localStorage 任务总线 → lumen 任务中心 #102–109**：总纲 §1.1 明确的迁移方向（非偏离）
- **demo `data-system-report-trigger` 数据属性契约 → 路由跳报告页**：lumen 无 SystemTaskOperations 全局监听层；报告页自身完成七段式+PDF，报告产物任务键（`region_innovation_elements_report`/`snapshot:{taskId}`）已在 L1B mock 落位，AV 叶联调时验证闭环
- **menu.ts 改 3 行而非 1 行**：工作台+过程页+报告页三个路由的 component 都是本叶缺省（DevelopingView 兜底），同属「本叶 component」；三行无交叉，VIT/COLLAB 不受影响
- **L1C selfcheck 占位计数改动态**：`placeholderRefs===3` 在要素替换后必红；改为「占位+已接线=3」动态收口，VIT/COLLAB 落地后继续绿（11 行 diff，见 commit）

## 2. 产物清单

| 文件 | 类型 |
|---|---|
| `src/views/intelligence/elements/ElementsWorkbenchView.vue` | A |
| `src/views/intelligence/elements/ElementTaskPage.vue` | A |
| `src/views/intelligence/elements/ElementReportPage.vue` | A |
| `src/views/intelligence/elements/ElementMethodDrawer.vue` | A（§10.6–10.9 步骤+临时权重表+七要素清单） |
| `src/views/intelligence/elements/elementResultSource.ts` | A（四结果态推导） |
| `src/views/intelligence/elements/elementReportDocument.ts` | A（七段式组装） |
| `src/views/intelligence/elements/elementTelemetry.ts` | A（synth_elem_* 埋点） |
| `src/views/intelligence/elements/element.selfcheck.mjs` | A |
| `src/router/menu.ts` | M（要素三行 +component） |
| `src/mock/intel/intelL1c.selfcheck.mjs` | M（占位计数动态收口） |

## 3. 验收证据

- `node src/views/intelligence/elements/element.selfcheck.mjs` ✅（五阶段互斥/四结果态/三透镜/11 角标/13 埋点/七段式/诚实态引用/禁随机数）
- `node src/mock/intel/{intel,intelL1b,intelL1c}.selfcheck.mjs` ✅（共享件无回归）
- `npm run type-check` ✅ / `npm run build-only` ✅（23s，既有 chunk 警告非本叶引入）
- **未推远端**：按人工验收闸门（2026-10-20 裁定）停 `intel/fe-elem` 本地待走查

## 4. 架构合规自检

- ✅ 调用链 D12：只经任务中心 #102–109（Java topic-async）+ mock synthElementBatch；无 demo 服务/Python 直连
- ✅ D8：Arco Design Vue + sci token；主色 #165DFF；卡片/边框对齐 demo `--sci-*` 语义
- ✅ D9：指标只读消费 `intelMetricSeed`/`synthReadinessSeed`（L1 全局 fallback）；ⓘ/红问号/draft 橙点/🧪 走 IntelMetricMount；无前端改绿；诚实态 Q-SYNTH-02/E-01/E-02 逐字保留
- ✅ D10：表格/Tab/Select/Steps Arco 原生键盘语义；排名行用 button+aria-current
- ✅ 评审零泄漏：角标全部经共享件自闸（isReviewFeatureEnabled && reviewMode）
- ✅ Mock 铁律：确定性数据（selfcheck 断言无 Math.random）；USE_MOCK=false 时 mock 不注册、结果源走 #104/#105 真接口
- ✅ 附录 E：切条件不自动起任务；「开始分析」显式触发；单飞/当天复用走 L1B 桥；完成不自动跳
- ponytail: full（无新依赖；复用 L1/L1B/L1C 全部共享件；新增文件收敛在 elements/ 一目录）

## 5. 防漏扫描（附录 D 摘要）

- D.1 页面差集：demo RegionalInnovationElements/ElementAnalysisTaskPage/ElementReportPage/ElementMethodDrawer 四文件全部复刻（区块级对照见 §1）
- D.2 本地 KPI 接线：11 个 M_SYNTH_ELEM_* 角标全部挂载（selfcheck 断言）
- D.3 镜像 vs 矩阵：synthReadinessSeed 头注释已声明 SYNTH 矩阵待 data-agent 登记（L1 范围，本叶无改）
- D.4 错挂/正名：metric_id 全部经 `metric-id` prop 传入共享件，无本地别名
- D.5 契约防漏：analysisType/fingerprint/snapshot 键与 L1B 桥一致
- 附录 E（E.1–E.5）：过程页 CTA/禁自动 create/单飞/当天复用/重新分析 force 全部落位
- 完整扫描由 LUMEN-INTEL-FE-AV 叶统一执行（依赖 VIT+COLLAB 合流）

## 6. 遗留与下游

- 三叶 merge 顺序：VIT/ELEM/COLLAB 全部走查通过后合 dev；menu.ts 三行互不冲突
- `synthElementBatch` 的 defineApi real 面（GET `/topic/v1/synth/elements/batch-snapshot`）归 LUMEN-INTEL-BE-1 联调；本叶 mock 直连 `getElementBatchSnapshot` 等价消费
- 埋点生产通道：待可观测组在 observability.ts 提供 track() 后替换 elementTelemetry.ts 一行
