# LUMEN-INTEL-COLLAB-FE-L01 · handoff

- 任务：综合智能分析协同 — 产业筛选 + 图谱 API 接线 + 空态分态展示（COLLAB 册 v1.0.8 §6 差距闭合）
- Epic：E8-综合智能分析 ｜ 执行：agent:frontend-agent ｜ 监管：human:徐滕强
- 仓：`repos/lumen-ui-topic`（origin/dev，commit 见 §3，**未 push**——任务文明示不 push，coordinator 统一推）
- 日期：2026-11-05
- 强度：ponytail full
- 真源：`agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/l2/SYNTH-L2-COLLAB.md` **v1.0.8**（§3.2 图谱契约 / §6 页面差距审计=范围真源 / §7 验收）；`LUMEN-INTEL-COLLAB-GRAPH-L01.md`（BE 门面：三键必填/四分支绑定/200 空图 reason/graph_upstream_unavailable 降级）；`LUMEN-INTEL-COLLAB-PY-L01.md`（CollabResult 契约 + batch_meta 回显 + strategies 待审核 + relationInput null 偏离 4）
- 同构样板：`efaee24`（要素叶：fetchElementBatchSnapshot / elementResultSource / ElementPanoramaPanel / 真结果源接线 / 自检脚本模式全复用）；复刻五维模板 `templates/fe-replica-visual-dod.md`

## 1. 范围与实现（COLLAB 册 §6 差距逐项）

| §6 差距 | 要求 | 实现 |
|---|---|---|
| ②产业筛选 | 条件栏 industry 下拉 + 服务端过滤 + 截断提示 | ✅ `CollabWorkbenchView` 图谱区块新增产业 `a-select`（选项=图谱响应节点 `industry_label` 去重，无数据禁用不伪造选项）；选择后带 `industry` 重拉 `GET /topic/v1/synth/collaboration/graph`（服务端过滤为主）；`truncated=true` 显「已按中心度截断」警示。位置在图谱区块内（`SynthContextBar` 共享件零改动，避免影响 VIT/ELEM 两叶——条件栏三键 region/compare/window 是全局上下文，industry 是图谱区块局部筛选，语义不同不放全局栏，见偏离 1） |
| ②图谱独立 API | 现页面仅前端过滤，无独立图谱请求 | ✅ 新增 `synthCollabGraph` defineApi（`api/topic/synthBatch.ts`：`fetchCollabGraph`，real 面 400/404 → 空图 `graph_request_rejected` 诚实降级）+ `collabGraphSource.ts` 数据源件；`graphData` ref 取代读 `result.nodes/edges`；`kindFilter/edgeFilter` 保留为前端叠加过滤（标注「叠加过滤」）；工作台从快照打开图谱**必带 `snapshotId: result.snapshotId`**（BE 经 batch_meta 解析 graph_batch_id，A/B 批不串） |
| ②截断/映射缺失提示 | truncated 显提示；空图按 reason 分态，不静默换图 | ✅ `collabGraphSource.ts` `COLLAB_GRAPH_REASON_TEXT` 三态文案：`no_year_on_source`（源无年，指数与网络统计本窗为空）/ `batch_meta_missing`（无映射禁回落）/ `graph_upstream_unavailable`（上游不可用稍后重试）+ 网络失败兜底同语义；空图显「不回填历史边、不静默换图」，禁 fixture |
| ④snapshotId 透传 | 从快照打开必带；展示批次回显 | ✅ 图谱请求带 `snapshotId`；结果区新增 `snapshotLine`（快照 ID + `calc_batch_id` + `batchMetaReason` + `publishedAt` 发布时间）+ 图谱标题旁 `graph_batch_id` 图批次回显 |
| ⑤collabIndex 三窗空态 | null+reason 渲染（模板已有卡片，接真数据源，禁编数） | ✅ CollabResult 类型全量 null 化（`collabIndex/completeness/centrality/density/deltaVsCompare/yoy/relationInput 各键/ranks 各列`）；三卡 null → `—` + reason（`indexReason/completenessReason` 读 `metrics.{metric_id}.reason` D9 追溯块，模板不裸 metric_id）；中心主体 TOP/集群/孤立/趋势/ranks 空数组各有诚实空态（集群显 `clustersReason=cluster_rule_unclosed` Q-SYNTH-C-02；孤立显「源无年无孤立结论不回填历史边」；趋势显「暂无历史批不编数」） |
| ⑤strategies 待审核 Tag | 接 LLM 产物（空态=策略生成不可用 reason） | ✅ mock 种子策略恒 `[]`（LLM 实时产物不伪造）+ `strategiesReason=strategy_llm_unavailable`；空态显「策略生成暂不可用（reason）：LLM 实时生成失败或未配置时诚实降级」；有产物时 Tag 逻辑不变（`已审核?green:orangered`）+「AI 生成·待审核（Q-SYNTH-C-04）」文案 |
| ⑤effectEval 三态 | ok/insufficient/none | ✅ 保留三分支；insufficient 显 `reason`；none 显 `reason ?? batch_not_published`；`relationResult` 数值/文案双形态容忍（real=数值 r → 渲染 `Pearson r=x.xx（仅关联，非因果）`）；散点缺行 null 不进 chart data（不补 0 编点） |
| ⑥报告页真快照 | 仿要素叶模式，无 fixture | ✅ `CollabReportPage` 重写结果源：URL task_id → #104 success → #105 resultData `normalizeCollabResult`（失败 null 禁 mock 兜底）→ 默认跑批 `USE_MOCK` 分叉（true 本地 mock / false `fetchCollabBatchSnapshot`，404/400/失败 → null）；无结果显「报告只消费真实结果快照，不伪造数据段」；报告段落 null → 「暂无数据」；新段落：图谱主体清单（含 industry_label）、集群无归属行 reason、策略降级 reason、图谱/计算批次 |
| ⑦mock 种子对齐新契约 | CollabResult 24 字段 + batch_meta 回显 | ✅ `collabMock.ts` 结构对齐 Python `pack.py` 实装（对照实码）：`graph_batch_id`（`graph:{calc_batch_id}` 派生同构）/ `calc_batch_id` / `publishedAt`+`published_at` / `cache_key` / `batchMetaReason` / `metrics` D9 追溯块（`_metric_meta` 同构 confidence+reason）/ `clustersReason` / `strategiesReason` / `graphReason`；三窗（1y/5y）+ 任务态 = 空态（null+`no_year_on_source`，nodes/edges 恒 []，与 v1.0.7 空图契约一致）；默认 3y = 演示行（batch 态秒开需要，仅 mock 种子）；`relationInput` 可 null（PY 偏离 4 canonical 全缺） |

## 2. 偏离说明

1. **industry 下拉落在图谱区块而非 `SynthContextBar`**：任务书话术「SynthContextBar（或协同工作台条件栏）加产业下拉」给出两可落点；选图谱区块内（「或」后半）。理由：SynthContextBar 是 VIT/ELEM/COLLAB 三叶共享件，加 industry 会把协同图谱的局部筛选渗入全局条件（切叶残留/语义混淆）；且 §3.2 契约 industry 只作用于图谱查询，不进分析任务指纹（`analysis_fp=region|compare|window` 三段）。共改共享件需跨叶回归，最小 diff 原则下不划算。F-COLLAB 页面下方另有「条件栏改条件即重拉图谱」的全局联动已实现（watch ctx）。
2. **产业选项数据源=图谱响应节点 `industry_label` 去重**（任务书「数据源=图谱响应或既有产业字典」两可）：选图谱响应，零新增字典依赖；代价是图谱空时下拉禁用（已显式提示「不伪造选项」）。后续如需全量产业字典，属契约增补另开单。
3. **mock 种子保留 3y batch 演示行**：v1.0.7 三窗空图口径下 Python real 面恒空态，但 USE_MOCK=true 的 instant 秒开（仅默认三元组）需要可演示数据（ELEM/VIT 同款先例：mock 种子演示值、real 面诚实空）；1y/5y/任务态种子同步空态，保证三窗分态可演示。
4. **图谱 mock 面（`mockCollabGraph`）本地 industry 过滤**：mock 面同构服务端语义（industry/快照绑定/空图 reason），注册进 `register.ts`（`USE_MOCK=false` 时 defineApi 不走 mock，零 fixture 泄漏）。

## 3. 产物清单

| 文件 | 说明 |
|---|---|
| `src/api/topic/synthBatch.ts` | +`synthCollabBatch`（§3.1 快照）+`synthCollabGraph`（§3.2 图谱：CollabGraphQuery/CollabGraphResp/truncated/snapshotId/industry）+`fetchCollabBatchSnapshot`/`fetchCollabGraph` |
| `src/mock/intel/collabMock.ts` | CollabResult 全量 null 契约 + batch_meta 回显九键 + metrics 追溯块 + 三窗空态种子 + strategies 恒空 + clustersReason |
| `src/mock/intel/intelBatchApi.ts` | +`mockCollabGraph`（mock 面同构服务端语义：industry 过滤/快照绑定/batch_meta_missing/no_year_on_source） |
| `src/mock/register.ts` | +`registerApiMock('synthCollabGraph', ...)` |
| `src/views/intelligence/collaboration/collabGraphSource.ts` | 新增：图谱数据源件（resolveCollabGraph + COLLAB_GRAPH_REASON_TEXT 三态文案） |
| `src/views/intelligence/collaboration/CollabWorkbenchView.vue` | 结果源异步化（真快照/#105 + USE_MOCK 分叉）+ 图谱独立数据源 + 产业筛选 + 截断/空图分态 + snapshotId 透传 + null 容忍渲染 + snapshotLine |
| `src/views/intelligence/collaboration/CollabReportPage.vue` | 真快照渲染重写（仿要素叶模式；normalize 禁 mock 兜底；USE_MOCK 分叉；新段落图谱/集群 reason/策略降级） |
| `src/views/intelligence/collaboration/collab.selfcheck.mjs` | +L01 断言 30+（§1 ①–⑦ 逐项锁定：图谱 API/产业筛选/叠加过滤/截断/三态 reason/快照透传/mock 契约/报告页禁 fixture） |

commit：`<hash> feat(intel-collab): 产业筛选+图谱API接线+空态分态展示 [agent:frontend]`
边界：未动 elements/vitality 两叶文件；共享组件（SynthContextBar/IntelMetricMount）零改动；`git status` 他人 WIP 未触碰。

## 4. 三绿 + 回归

| 检查 | 结果 |
|---|---|
| `pnpm type-check`（vue-tsc --build） | ✅ 0 error |
| `node src/views/intelligence/collaboration/collab.selfcheck.mjs`（含新增 L01 断言） | ✅ ok |
| `pnpm build`（vite production） | ✅ built in 21.19s |
| 回归：intel.selfcheck / intelL1c / intelVit / element | ✅ 全 ok（无回归） |
| intelL1b | 🔴 存量红（基线即红，stash 验证与本单无关：`view=${processView}` 断言与 routes.ts 现实现不符，属前序遗留） |
| ESLint 本单 7 文件 | ✅ 0 error（仓内存量 78 error 在他人文件，stash 验证基线一致，不属本单） |

## 5. 复刻五维自检（templates/fe-replica-visual-dod.md）

| # | 自检 |
|---|---|
| R1 布局 | ✅ §6 各区块结构保持（三卡/关系构成/图谱+子图/集群孤立/横向纵向/散点/策略）；新增产业下拉嵌入图谱区块头、空图占位框同尺寸 |
| R2 交互 | ✅ 空（图谱空态+结果加载态）/加载（graphLoading/resultLoading）/失败（graph_upstream_unavailable+reason）/有结果/条件脏（切条件清 industry 重拉）全态保留；`a-select` allow-clear + disabled 语义 |
| R3 样式 | ✅ 全部沿用 `--sci-*` token / `var(--sci-border)` / `#165DFF` 主色；无新样式文件 |
| R4 评审 | ✅ 指标挂载仍全走 `IntelMetricMount`（@/review 门控自闸）；模板文案零 metric_id 裸露（自检断言守护）；reason 经 script computed 转 UI 文案 |
| R5 Mock | ✅ 开：只走 `USE_MOCK` + `registerApiMock('synthCollabGraph'/'synthCollabBatch')`，形状=BE 实包（GRAPH-L01 门面 + PY-L01 CollabResult）；关：`USE_MOCK=false` 走 real 面，404/400/失败 → 诚实空态+reason，零 fixture（自检断言「禁 mock 兜底」） |
| W4 | ✅ 切条件不自动起任务（仍 `view: 'config'` 进配置态）；「开始分析」入口不变；任务桥/恢复逻辑零改动 |

## 6. 架构合规自检（公约 §2 铁律，FE 相关项）

| # | 铁律 | 自检 |
|---|---|---|
| 2 | 调用链 | ✅ 前端只调 Java 门面 `/topic/v1/synth/collaboration/{batch-snapshot,graph}`；无越层直连 Python / demo-* |
| 7 | 共享聚合核心 | ✅ 只经 `gkxlumen-topic`；图谱过滤/截断在 Python 服务端执行，FE 只传参+叠加展示过滤 |
| 9 | D8 前端规范 | ✅ Arco `a-select`（32px 语义 size=small 图谱区块内）、`--sci-*` token、主色 `#165DFF`、无新依赖 |
| 10 | D9 血缘 | ✅ 六个 metric 挂载点保持 IntelMetricMount；空态 reason 读 `metrics.{metric_id}.reason`（PY 回显块）；不补 0 不改绿；`graph_batch_id`/`calc_batch_id`/`snapshotId` 追溯回显 |
| 11 | D10 交互 | ✅ 空/加载/失败态文案明确；`allow-clear`；筛选器 `aria-label`；空态提示可聚焦容器 |
| 12 | D12 隔离 | ✅ 零 demo 引用；mock 面为本仓 `@/mock` 注册，`USE_MOCK=false` 零 fixture（R5） |
| 18 | D18 签收=可实现 | ✅ 空图/空态=读真快照/真图谱后的诚实结果；Python graph 端点挂载后本 FE 零改动拿真图（GRAPH-L01 契约已对齐） |

## 7. ponytail 自检

ponytail: full——复用要素叶全套模式（fetchXxxBatchSnapshot defineApi / normalize / USE_MOCK 分叉 / snapshotLine / selfcheck 锁契约），不新造框架；新增文件仅 1 个（collabGraphSource.ts，40 行数据源+文案表）；`SynthContextBar` 共享件零改动（industry 落图谱区块，避免跨叶回归）；mock 面复用 intelBatchApi 同文件（mockCollabGraph 同构 mockSynthBatchSnapshot 模式）；无新依赖；`ponytail:` ceiling——产业下拉选项依赖图谱响应（图空即禁用），升级路径=产业字典接口就绪后换数据源一行。

## 8. cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ~150000 |
| model_used | glm-5.3-Flash（Cursor 内） |
| actual_cost | ~$0.19 |
| cost_warn | false（< $10 阈值） |

## 9. 后续依赖（不属本单）

- Python `/internal/v1/synth/collaboration/graph` 挂载（COLLAB-PY 增量 / C-05 单）→ 挂载后本 FE 即拿真图，零改动
- Java 门面 `084b2d1` push + CI 绿（监管人验收后）
- C-05 解锁后：node/edge 有行 → 产业选项来自真实 `industry_code/industry_label`；非空验收移 `COLLAB-C05-SRC`
- intelL1b 存量红：建议 coordinator 开小单收口（routes.ts 实现与断言漂移，影响三叶回归信噪）
