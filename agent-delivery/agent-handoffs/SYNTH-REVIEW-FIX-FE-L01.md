# SYNTH-REVIEW-FIX-FE-L01 — SYNTH 两 commit 评审修复 handoff

> 任务：SYNTH（efaee24 / 4d0a24d）评审结论「需修后放行」修复单
> 仓：`lumen-ui-topic`（origin/dev）；commit：**a06e677**（本地 dev，未 push，待人工确认）
> 强度：ponytail full；执行：agent:frontend；监管人：当前会话用户
> 日期：2026-11-06

## 1. 范围与实现（逐项修法）

### Critical

**C1 — ElementsWorkbenchView 趋势 yAxis 硬编码 min:60/max:100（D9 诚实展示）**
- 修法：`trendOption` 的 `yAxis: { type: 'value', min: 60, max: 100 }` → `{ type: 'value', scale: true }`（VIT 工作台 `trendOption` 同款）。
- 效果：real 面低值趋势数据不再被 60 下限静默截除；轴范围随数据自适应。

**C2 — CollabWorkbenchView 图谱 snapshotId 竞态**
- 根因：`watch([taskIdParam, viewParam])` 与 ctx watch 里 `refreshResult` / `refreshGraph` 并发发起；图谱先完成时 `result.value` 尚为 null，请求不带 snapshotId（任务态首屏必中，图与数字不同批）。
- 修法（顺序化）：两处 watch 统一改为 `refreshResultThenGraph()` —— `await refreshResult()` 完成后再 `await refreshGraph()`；图谱请求读到的 `result.value?.snapshotId` 必为本次结果批。任务态首轮 `refreshGraph()` 现在必带 `task:<id>` snapshotId。
- 等价性：`watch(result.value?.snapshotId)` 方案被否——`snapshotId` 字符串变化才触发，首轮 null→有值虽会触发，但会造成「双拉」（首轮竞态拉 + 回调再拉），顺序化是更小且确定正确的 diff。

### Important

**I1 — 关系输入条形图 `?? 0` 补零**
- 修法：`relationBarOption` 改为先按 `input?.xxx != null` 过滤行再进 `series.data`（缺行不画柱），y 轴类目同步只保留有值行——同 `corrScatterOption` 既有做法。`relationInput` 整体 null 时模板已有「暂无关系输入行」分支不渲染图（`v-if="!result!.relationInput"`）。

**I2 — CollabReportPage 负值文案失真**
- 修法：`executive-summary` 第 2 行照 `elementReportDocument.ts` 双分支抄齐：`deltaVsCompare >= 0 ? '高' : '低'` + `Math.abs(...)`；`yoy >= 0 ? '增长' : '下降'` + `Math.abs(...)`。不再出现「高 -3.2 分」「增长 -1%」。

**I3 — normalizeCollabResult 校验弱 + 两文件重复**
- 修法：抽共享模块 `views/intelligence/collaboration/collabResultSource.ts`（唯一定义）；校验补 `Array.isArray(row.nodes) && Array.isArray(row.strengths)`（任一非数组 → null，禁 fixture 兜底）。`CollabWorkbenchView.vue` / `CollabReportPage.vue` 均改 import，本地重复定义删除。

**I4 — D9 错挂正名**
- Collab（对照 `collabMock.ts` `metrics` 追溯块 + `synthReadinessSeed.ts` 就绪度登记，只挂 registry 已有 ID）：
  - 「高效协同集群」`M_SYNTH_COLLAB_INDEX` → **`M_SYNTH_COLLAB_CLUSTER`**（mock 追溯块已有该键：`{ confidence:'null', reason:'cluster_rule_unclosed' }`，与集群语义精确对应）；
  - 「横向对比」「纵向趋势」`M_SYNTH_COLLAB_INDEX` → **`M_SYNTH_COLLAB_COMPLETENESS`**（对比盘/趋势序列的核心字段是完整度/中心度/密度三元组，COMPLETENESS 是已登记 ID 中最贴近的；未新增未登记 ID）；
  - 「区域创新协同指数」主卡保留 `M_SYNTH_COLLAB_INDEX`（语义本就正确）。
- ELEM：三处「要素评价模型构建」（:401 类型指数卡 / :462 类型得分图 / :599 排名卡）统一挂 **`M_SYNTH_ELEM_TYPE_SCORE`**（原 :401 挂 WEIGHT、:599 挂 RANK）。
- 说明：`M_SYNTH_COLLAB_CLUSTER` 在 `synthReadinessSeed.ts` 镜像暂无条目（UNKNOWN 态，红问号诚实态，符合「未登记不伪绿」）；其 seed/矩阵登记属 data-agent 职责，已在下方「遗留」登记。

**I5 — ElementPanoramaPanel 全景筛选**
- 跨上下文残留：新增 `watch(() => props.ctx, …)` 重置 `remotePanorama/remoteReason`（上一次筛选的 remote 行是旧上下文数据）。
- 非默认三元组静默假死：`filterDisabled = !USE_MOCK && !isSynthDefaults(props.ctx)`；radio-group `:disabled="remoteBusy || filterDisabled"` + 下方一行说明文案「全景分类筛选仅系统默认条件可用…」（无 Message 轰炸）；`watch(filter)` 内兜底同判。
- `pullFiltered` 原有 `isSynthDefaults(props.ctx)` 早退保留（双保险）。

**I6 — 死参数**
- `synthBatch.ts` `CollabGraphQuery`：`entity_types/relation_types/limit_nodes/limit_edges` 补「本期不启用：…契约保留」注释。
- `ElementBatchQuery.page_size` 注释注明「全景拉取按 §2 透传 page_size:10」；`ElementPanoramaPanel.pullFiltered` 实际透传 `page_size: 10`。

**I7 — 图谱响应裸断言 + NaN**
- `refreshGraph` 改 source 层归一化：新增 `normalizeCollabGraphNode`（id 必填；`name ?? id`、`kind ?? 'enterprise'`、`centrality` 非 finite 数字 → 0）；边归一（`id ?? source->target`、`type ?? 'joint_patent'`、weight 非 finite → 0）。删除 `resp.nodes as CollabGraphNode[]` / `resp.edges as CollabResult['edges']` 裸断言。
- `graphOption.symbolSize = 16 + n.centrality * 28` 因 centrality 已保证为 finite number，NaN 路径消除（未改 symbolSize 表达式本身）。

### Minor（仅修派单点名的 M3/M4/M5/M7）

**M3** — `:loading="restoring"`（恒 false 挂在恢复按钮）删除；连带死变量 `restoring` ref 一并清除（`onMounted` 两处赋值只剩空 finally 注释说明）。`resultLoading`（真实使用中）不受影响。

**M4** — 两叶 `snapshotLine` 补 `cache_key` 段：Collab `· cache_key ${r.cache_key}`；ELEM 同款。`CollabResult`/`ElementResult` 类型已有 `cache_key` 字段（mock 种子已回填），无类型改动。

**M5** — `ElementsWorkbenchView.onCtxChange` 照 VIT `patchCtx` defaults 判定恢复语义：`next` 为默认三元组（深圳×全国重点城市×最近3年）→ 只清 `task_id`（保留 view，回 result 态秒开）；非默认 → 清 `view + task_id` 进 config 态。删除原 `void next` 死参。

**M7** — 全景空态 div 补 `tabindex="0"` + `role="status"`（`:focus-visible` 样式仓内已有）。

## 2. 自检证据（三绿）

| 项 | 结果 |
|---|---|
| `pnpm type-check`（vue-tsc --build） | ✅ 0 error（15.2s） |
| collab.selfcheck（补 12 条断言：C2 顺序化/禁并行、I3 共享+校验、I1 禁补零、I4 三处正名、I6/I7 归一化、M3/M4、I2 双分支） | ✅ ok |
| element.selfcheck（补 9 条断言：C1 scale/禁硬编码、M4、M5 backToResult、M7、I5 filterDisabled/重置/说明/page_size、I4 三处 TYPE_SCORE 计数） | ✅ ok |
| intel.selfcheck / intelVit.selfcheck / intelL1c.selfcheck（回归） | ✅ 全 ok |
| intelL1b.selfcheck | 🔴 存量红（修前即红，`analysisTaskRoutes` 断言过时；派单明示不计入） |
| `pnpm build` | ✅ built in 25.1s（chunk 体积 warning 为存量，非本次引入） |
| D9 评审零泄漏自检（collab.selfcheck 既有断言） | ✅ 通过（模板文案无裸 metric_id；新挂 ID 均走 IntelMetricMount 组件 data 面） |

改动面：8 文件，+167/-56（含新增 `collabResultSource.ts`）；自检断言 +31 行。

## 3. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 调用链（前端→Java→Python /internal/*） | ✅ 未越层；图谱/快照仍走 `/topic/v1/synth/*` Java 门面 |
| D8 设计规范 | ✅ 未动视觉 token/组件栈；仅逻辑与挂载正名 |
| D9 数据血缘 | ✅ C1 消数据截除；I4 错挂正名；全部 ⓘ 走 IntelMetricMount（ReviewMetricBadges 评审自闸）；未手写就绪度、未在前端改绿 |
| D10 交互规范 | ✅ M7 a11y（tabindex+role=status）；I5 禁用态+说明（非 Message 轰炸） |
| demo 只读 merge（D12） | ✅ 未触碰 demo 仓；lumen 仓内修改 |
| USE_MOCK=false 禁 fixture | ✅ I3 收紧校验仍返回 null 不兜底；I1 缺行不补 0 |
| git 策略 | ✅ dev 分支 commit `a06e677`，未 push（等待人工确认）；message 含 `[agent:frontend]` |
| 前端推送人工确认闸门（2026-11-05） | ✅ 遵守：停在本地，未获「推」指令不 push |

## 4. 偏离说明

1. **I4 横向对比/纵向趋势挂 `M_SYNTH_COLLAB_COMPLETENESS`**：派单给出「挂更贴近的已有 ID 或降为不挂」两选项；选择挂已有 ID（对比/趋势区块的表格与图表主体即完整度/中心度/密度序列）。如评审认为这两处应降为不挂，改动为删 2 个 `<IntelMetricMount>` 行即可。
2. **M3 顺手删死变量 `restoring`**：删除死绑定后 ref 只写不读；保留会留误导性死代码，删除属 M3 完整落地。
3. **element.selfcheck D9 必挂清单移除 `M_SYNTH_ELEM_RANK`**：I4 统一后排名卡挂 TYPE_SCORE（三处同标题同 ID），RANK 不再单独挂载；seed 中该 ID 保留（drawer/其他叶未来可用）。

## 5. 不修清单（派单指定登记）

- **M1**（mock 面空态 reason 失真）：不修，登记在案。
- **M2**（治理术语进 DOM）：已登记到 `lumen-ui-topic` **`src/review/README.md` 上线清理清单第 6 条**（检索 `Q-SYNTH` / `no_year_on_source` / `batch_not_published` / `cluster_rule_unclosed` / `strategy_llm_unavailable`，随评审层一并下线，业务态空态改中性话术）。
- **M6**（window 映射重复实现）：不修。
- **M8**（报告默认区硬编码）：不修。

## 6. 遗留 / 交下游

1. `M_SYNTH_COLLAB_CLUSTER` 在 `src/mock/intel/synthReadinessSeed.ts` FE 只读镜像暂无条目（ⓘ 显示未登记红问号，诚实态）。待 data-agent 在 SYNTH 矩阵登记后按镜像同步规则补行（禁止 FE 手写改绿）。
2. intelL1b.selfcheck 存量红（`analysisTaskRoutes.ts` 断言过时）需另单修复，非本单范围。
3. 本 commit 停在本地 dev（`a06e677`），按 2026-11-05 人工确认闸门等会话用户明示「推」后再 push。

## 7. 产物清单

- commit：`a06e677 fix(intel): 评审修复——趋势轴scale/图谱snapshotId竞态/补零/错挂正名/全景跨ctx [agent:frontend]`（lumen-ui-topic dev，本地未推）
- 新增：`src/views/intelligence/collaboration/collabResultSource.ts`
- 修改：`CollabWorkbenchView.vue`、`CollabReportPage.vue`、`collab.selfcheck.mjs`、`ElementsWorkbenchView.vue`、`ElementPanoramaPanel.vue`、`element.selfcheck.mjs`、`api/topic/synthBatch.ts`
- 附带 commit：`d337367 chore(review): 登记M2治理术语进上线清理清单 [agent:frontend]`（`src/review/README.md` 清理清单第 6 条）

ponytail: full——全部为最小 diff 修复（顺序化优于响应式链、归一化在 source 层一次做全），无新依赖、无新抽象；非平凡语义（C2/I3/I5）均留下可运行的自检断言。
