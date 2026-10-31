# LUMEN-INTEL-FE-L1B — 综合智能分析 任务中心扩展（白名单/路由分支/任务桥/记录面板）

- 任务：LUMEN-INTEL-FE-L1B（E8-综合智能分析 / implementation / P0 / lumen-ui-topic）
- 强度：ponytail full
- 状态：in_progress → 待走查（本 handoff 后转 integration）
- commit：lumen-ui-topic dev `6a60ef6`（**未 push**，按仓级人工验收闸门 2026-10-20 停本地待验收）
- 监管人：human:孔东

## 1. 范围与实现（对照 DoD 逐条）

### DoD-1 AnalysisType 白名单 +6 键 + 路由分支
`src/api/enterprise/types/analysisTask.ts`：
- `INTEL_ANALYSIS_LEAVES` 三叶 + `IntelAnalysisType`（3 分析 + 3 `_report`）
- 守卫 `isIntelAnalysisType` / `isIntelReportAnalysisType` / `intelAnalysisLeafOf`
- 中文标签真源 `INTEL_ANALYSIS_LABEL`（浮层/记录/mock 任务名共用，禁另造）
- `AnalysisType` 联合类型并入 intel 六键

`src/composables/analysisTaskRoutes.ts`：
- `buildAnalysisTaskRoute` 增 intel 分支：完成未查看停 `processing`（wait_view，对齐 svc/政策），看过进 `result`；目标 = 工作台 `?view=&task_id=&analysis_fp=`
- `buildReportViewerTarget` 增 intel 分支：报告任务/带结果分析任务 → `intelligence/{leaf}/report?task_id=`（L0 intel-*-report 路由），anchor = parentTaskId ?? taskId

### DoD-2 useSynthTaskBridge 四决策（附录 E）
`src/composables/useSynthTaskBridge.ts`（新建，demo `synthSystemTaskBridge.ts` 语义移植）：
- demo 的 localStorage 系统任务总线在 lumen 对应 #102–109 任务中心，**不另造存储**
- `startOrResumeSynthAnalysis`：E.4 同用户同条件单飞（`findInFlightAnalysis`）→ `resume_processing`；E.5 当天已成功（`findSucceededAnalysisToday`）→ `resume_result`（含 `markLocalResultViewed`）；force=true 跳过当天复用走 create（mock #102 单飞仍拦截）；#102 失败 → `queue_full`
- `applySynthStartDecision`：四决策 → Message 文案 + router.push（demo onStartAnalysis 同款话术）
- `resolveSynthWorkbenchRestore`：切回工作台条件未变恢复过程/结果；`view=config/result/report` 不拽回
- `isIntelRelatedReport`：报告关联键正式约定 `snapshot:{taskId}`（兼容 `snapshot:task:{id}` 与 parentTaskId）
- 路径助手 `intelWorkbenchPath` / `intelTaskPath`；`intelTaskCtxParams` 从 targetParams 冻结条件反解（复制配置用）

### DoD-3 记录面板 + 浮层 label + SSE 五阶段
- `src/views/intelligence/SynthAnalysisRecordsPanel.vue`（新建）：复用 `SvcAnalysisRecordsTable` diagnosis 布局（demo SynthAnalysisRecordsPanel 同列同操作）；#103 按本叶 analysisType 过滤；查看结果（wait_view 检查）/复制配置（回填 region/compare/window + view=config）/查看报告（snapshot 关联最新报告）
- `SvcAnalysisRecordsTable.vue` 最小扩展：新增 `openReport` emit（intel 时父级接管，svc/chain 行为不变）；intel 报告计数走 reportTasks（parentTaskId / snapshot 键）
- `SystemTaskFloat.vue`：`taskLabel` 增 intel 中文映射（INTEL_ANALYSIS_LABEL）；recent 过滤并入 intel
- `analysisTaskStore.ts`（mock）：`INTEL_NODE_NAMES` 接线 L1 三叶五阶段（VITALITY/ELEMENT/COLLAB_TASK_STAGES，禁互串话术）；taskId 前缀 `INTEL-`；任务名 INTEL_ANALYSIS_LABEL；`freezeIntelTargetParams` 冻结 region/compare/window + analysis_fp + object_summary（`深圳 · 全国重点城市 · 最近3年` demo 同款）；running 单飞复用（同 type+fp 返回已有任务 reused）；`finishIntelWaitView` 成功 payload 接线 `getVitalityTaskResult` / `getElementTaskResult` / `getCollabTaskResult`（确定性 mock，无随机数）；`finishIntelReportArtifact` 报告产物立即成功 + 回写父任务 report_generated/source_snapshot_id；SSE events `I{N}` 节点码；intel `*_report` 校验父任务须 success

## 2. 防漏扫描（附录 D/E 对照）

- D.5 契约防漏：AnalysisType 六键全部入白名单；#102/#103/#104/#105/#108/#109 全链 mock 覆盖 intel；无新增 REST 端点（复用 ANALYSIS-CORE）
- E.3 禁自动 create：桥只在用户点「开始分析」时 create；切条件仅改 query 不建任务
- E.4 单飞：`findInFlightAnalysis` + mock #102 reused 双保险
- E.5 当天复用：`findSucceededAnalysisToday`（Asia/Shanghai 日界，复用 gate 工具）；另提供 force 重新分析
- wait_view：成功未查看停过程页（`readLocalResultViewed`），显式「查看结果」才进结果（记录面板 openResult 调 markLocalResultViewed）

## 3. 产物清单

| 文件 | 类型 |
|---|---|
| `src/api/enterprise/types/analysisTask.ts` | M（+44） |
| `src/composables/useSynthTaskBridge.ts` | A（新） |
| `src/composables/analysisTaskRoutes.ts` | M（+27） |
| `src/mock/enterprise/analysisTaskStore.ts` | M（+208） |
| `src/views/intelligence/SynthAnalysisRecordsPanel.vue` | A（新） |
| `src/views/service/SvcAnalysisRecordsTable.vue` | M（+17，openReport emit） |
| `src/components/system/SystemTaskFloat.vue` | M（+11） |
| `src/mock/intel/intelL1b.selfcheck.mjs` | A（新，自检） |

## 4. 验收证据

- `pnpm type-check` ✅（exit 0）
- `npx eslint <改动文件>` ✅（0 error）
- `node src/mock/intel/intelL1b.selfcheck.mjs` ✅（白名单/四决策/路由分支/mock 接线/记录面板/关联键断言全过）
- 回归：`intel.selfcheck.mjs`（L1）✅、`serviceOrgAnalysis.selfcheck.mjs` ✅、`menu.selfcheck.mjs` 未动路由无需重跑（L0 断言仍有效，未改 menu.ts）

## 5. 架构合规自检（§2 铁律）

- ✅ D8：记录面板复用 Arco Table/Select/Button + diagnosis-records 既有样式 token，无新 UI 体系
- ✅ D9：本任务无新指标；mock 结果 payload 沿用 L1 seed（8 件套引用不变）
- ✅ D12：未调用任何 demo-* 服务；demo 代码仅语义参考未复制
- ✅ 调用链：mock 模式走 registerApiMock 既有 #102–109；real 模式走 Java REST（AnalysisTaskPaths）
- ✅ USE_MOCK=false：intel 分支不执行 mock 生成器（mock 仅在 defineApi mock 通道）
- ✅ 多会话保护：未触碰 `IndustryKeyLinkGraph.vue`（他会在写，留在工作区未提交）

## 6. 偏离说明

- demo 的 `findSucceeded*Task`（永久恢复）在 lumen 收敛为**当天**复用（E.5 口径 + 复用 `findSucceededAnalysisToday` gate 工具）；隔天同条件重新点「开始分析」会建新任务，与政策/svc 行为一致。如评审要求恢复 demo 永久复用语义，改 `resolveSynthWorkbenchRestore`/`startOrResumeSynthAnalysis` 中 `findSucceededAnalysisToday` → `findSucceededAnalysisByFingerprint` 即可
- 报告产物任务（`*_report`）mock 侧为占位实现（立即成功 + pdf 指针）；真实报告页内容在 FE-VIT/ELEM/COLLAB 三叶报告页任务中落地

## 7. cost 回填

- actual_tokens: ~95k（含读码/实现/自检）
- model_used: glm-5.3
- actual_cost: ~$1.2
- cost_warn: false

ponytail: full
