# SYNTH 三叶 · 系统任务队列 / 状态维持 — lumen 实现注意

> **用途**：Track-MS / lumen（`lumen-ui-topic` 等）正式实现时必读。  
> **范围**：区域创新活力 / 要素 / 协同（`SYNTH-VITALITY` · `SYNTH-ELEMENT` · `SYNTH-COLLAB`）「开始分析」与系统任务浮层。  
> **Demo 已落地参照**（语义真源，勿整文件复制）：`${GKX_ROOT}/repos/demo-ui-topic`  
> **契约对齐**：`SYS-ANALYSIS-JOBS` + 各叶 UX-SPEC「同条件运行中不重复建」+ `CT-SYN-CTX` / `CT-SYN-JOBS`。

---

## 1. 产品铁律（验收口径）

| # | 铁律 | 说明 |
|---|------|------|
| R1 | **同条件禁止重复入队** | 同一用户 + 同一叶子 `taskType` + **相同分析条件**（区域 × 对比范围 × 时间窗）下，不得再新建一条系统分析任务 |
| R2 | **同条件再次「开始分析」= 恢复** | 进行中 → 打开原过程页；已成功 → 打开/恢复结果态；**不得**再 `submit` 一条队列任务 |
| R3 | **切回菜单维持状态** | 用户离开本叶再从侧栏进入时，若条件未变：有进行中任务 → 进过程页；有已成功任务 → 维持结果展示；**不要**回到空白「待分析」 |
| R4 | **条件变更才新建** | 仅当 fingerprint 变化（或用户显式「按此配置新建 / 重新分析」）才允许创建新任务 |
| R5 | **已完成不得再推进队列** | 本地/服务端已有同条件 `succeeded` 时，只绑结果快照并导航结果；**禁止**为「对齐浮层」再 `submit` 一条 running 任务 |
| R6 | **显式 config 不抢恢复** | URL `mode=config`（用户刚改条件进入待分析）时，**不要**自动跳过程/结果，尊重当前配置意图 |
| R7 | **过程完成不自动跳结果** | 过程页 succeeded 停留；由用户点「查看分析结果」进结果（与 SYS-ANALYSIS-JOBS / Demo 一致） |

---

## 2. 条件指纹（fingerprint）

三叶共享 `CT-SYN-CTX`，去重与恢复一律按指纹，**不要只按 `taskType` 判断「同任务」**。

建议指纹（与 Demo 对齐）：

```text
analysis_fp = `${region}|${compareScope}|${windowUrl}`
# 例：深圳|全国重点城市|3y
# window 建议 URL 短码：最近1年→1y / 最近3年→3y / 最近5年→5y
```

实现要求：

1. 写入系统任务的 `sourceRoute` / `processingRoute` / `resultRoute` 时带上 `analysis_fp=...`（或等价结构化字段进任务元数据）。
2. 查重时：`userId + kind=analysis + taskType + analysis_fp + status∈{queued,running,succeeded}`。
3. **注意**：若底层系统任务 Store 仍按「同 taskType 仅一条非终态」互斥，与「不同条件可并行」冲突时，以产品确认的互斥策略为准；**同条件去重仍必须做**，不可因 Store 粗粒度互斥而省略 fingerprint。

---

## 3. 「开始分析」决策表（前端/网关任一侧实现均可，语义须一致）

```
输入：leafKind, ctx, userId

1. 同条件本地/服务 进行中(queued|running)
   → resume_processing（打开原 process 路由）；不新建

2. 同条件已成功(succeeded) 且有结果快照
   → resume_result（绑快照 + 结果 URL）；不新建、不 submit

3. 系统任务浮层中同 fingerprint 进行中 / 已成功
   → 同上恢复；不新建

4. 否则
   → create task + submit 系统队列 → started（进过程页）
```

用户提示建议：

| 决策 | Toast |
|------|--------|
| `resume_processing` | 该条件下已有进行中任务，已打开原过程页 |
| `resume_result` | 该条件下已有分析结果，已恢复结果 |
| `started` | 任务已加入系统分析队列 |
| 队列满 | 当前分析队列已满，请稍后重试 |

---

## 4. 切回菜单 / 工作台挂载时的恢复

工作台路由（如 `/intelligence/vitality|elements|collaboration`）**mount 或 ctx 变化**时：

```
if mode === 'config' → 不自动恢复
else if 同条件进行中 → replace 导航到过程页
else if 已在 result / result_task → 保持（勿二次跳转死循环）
else if 同条件已成功 → replace 导航到结果态（带 taskId + analysis_fp）
else → 保持秒开批结果 / 待分析（按各叶 UX：默认三元组秒开等）
```

注意：

- 用 `replace` 导航，避免污染浏览器历史。
- 比较「当前 path+search」与目标 path，相同则 **no-op**，防止 effect 循环。
- 侧栏菜单链到**干净工作台 URL**时，依赖本恢复逻辑，而不是要求菜单 URL 自带 `taskId`。
- 结果展示判定：**绑定任务的 frozenContext 与当前 ctx 一致**即可维持结果；不要仅依赖 URL 上的 `mode=result_task`（刷新/丢参时仍应能恢复）。

---

## 5. 与过程页 / 浮层的边界

| 场景 | 正确行为 |
|------|----------|
| Tab / 叶内切换视图 | **不得**因切 Tab 新建任务 |
| 浮层点任务 | 进该 `taskId` 过程或结果路由（与 Store `processingRoute` / `resultRoute` 一致） |
| 结果已查看 (`resultViewedAt`) | 按 SYS-ANALYSIS-JOBS：勿再把用户强拉回过程页（若正式 Store 有此字段） |
| 默认三元组 + 跑批秒开 | 无任务时秒开；**若同条件已有成功任务**，切回菜单应优先维持任务结果态（R3），而非悄悄退回秒开批 |

---

## 6. Demo 参照路径（lumen 对照实现，勿照搬 React mock 总线）

| 职责 | Demo 路径 |
|------|-----------|
| 开始/恢复/切回决策 | `demo-ui-topic/src/app/intelligence/synthSystemTaskBridge.ts`（`startOrResumeSynthAnalysis` · `resolveSynthWorkbenchRestore` · `synthCtxFingerprint`） |
| 自检 | `.../synthSystemTaskBridge.selfcheck.mjs` |
| 工作台接线 | `RegionalInnovationVitality.tsx` · `RegionalInnovationElements.tsx` · `RegionalInnovationCollaboration.tsx` |
| 分析记录 Tab | `SynthAnalysisRecordsPanel.tsx`（`?tab=records`；顶栏 Tab + 上下文条按钮；过程页「查看分析记录」；按本叶 `taskType` 过滤系统任务，对齐机构分析记录） |
| 报告关联 | 任务结果态生成报告时 `data-source-snapshot-id` **必须**为 `snapshot:{analysisTaskId}`（勿用 batchKey / `task:{id}`）；分析记录按此键统计报告；「查看报告」直接打开最新关联报告的 `resultRoute`，**不得先打开任务浮层** |
| 叶内 mock 任务（同条件 findRunning / findSucceeded） | `vitalityTasks.ts` · `elementTasks.ts` · `collabTasks.ts` |
| 系统浮层 Store | `src/app/system-tasks/systemTaskStore.ts` · `SystemTaskLayer.tsx` |
| 共享上下文 | `src/app/intelligence/synthCtx.ts`（`CT-SYN-CTX`） |

同类模式（机构分析等，可复用门控思路）：`demo-ui-topic/src/app/pages/service-center/analysisTaskGate.ts`。

---

## 7. lumen 落地检查清单（交付前勾选）

- [ ] 同条件连点两次「开始分析」：系统任务列表仍只有 **1** 条
- [ ] 同条件任务 succeeded 后再点「开始分析」：进入结果，**队列条数不增加**
- [ ] 过程中离开 → 侧栏再进同叶：条件未变时回到过程页
- [ ] 结果态离开 → 侧栏再进：条件未变时仍见结果（非待分析空白）
- [ ] 改条件（`mode=config`）后：不自动跳旧任务结果
- [ ] 条件改回曾分析过的三元组再点开始：恢复旧任务，不新建
- [ ] 路由带 `analysis_fp`（或服务端等价字段）；浮层恢复与工作台恢复指向同一 `taskId`
- [ ] 本叶有「分析记录」Tab：可查看结果 / 复制配置；`tab=records` 时不自动抢跳过程/结果
- [ ] 过程无伪造百分比；阶段文案用本叶五阶段（禁止抄产业链四力文案）
- [ ] D9 角标 / 可观测埋点随正式实现规范补齐（不得用 YAGNI 删）

---

## 8. 文档关系

| 文档 | 关系 |
|------|------|
| 本文件 | **实现约束 / demo→lumen 迁移注意**（工程必读） |
| 各叶 `UX-SPEC-SYNTH-*` | 交互与状态机权威；本文件是其「任务去重 + 菜单恢复」落地细则 |
| `SYS-ANALYSIS-JOBS/*` | 系统任务浮层 / 过程壳同构 |
| `E8-综合智能分析/README.md` | 三叶索引；链到本文件 |

修订时：改去重或恢复语义须同步改本文件 + 对应 UX-SPEC 一句，避免 demo 与 lumen 分叉。
