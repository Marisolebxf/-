# LUMEN-INTEL-ELEM-FE-L01 · handoff

- 任务：综合智能分析要素 — lumen-ui-topic 三透镜真链接线 + 136 全景模块
- Epic：E8-综合智能分析 ｜ 执行：agent:frontend-agent ｜ 监管：human:徐滕强
- 仓：`repos/lumen-ui-topic`（origin/dev；**本地 commit `e26603d`，未 push**——按派单「coordinator 统一推」执行）
- 日期：2026-11-05
- 强度：ponytail full（完整复用活力叶 `vitalityResultSource.ts` 真链接线模式，不另起炉灶）

## 1. 范围与实现（对照 ELEM 册 v1.0.6 §7 差距审计逐项）

| §7 差距项 | 实现 |
|---|---|
| **三透镜真链接线**（137① 类型/层次/领域） | ✅ `elementResultSource.ts` 仿活力叶重写：instant 态 `USE_MOCK=false` 走 `synthElementBatch` defineApi（`GET /topic/v1/synth/elements/batch-snapshot`，404/400 → `IntelBatchSnapshotNotFound` → 页面 `no_batch`，禁 fixture）；task 态 #104 success + ctx 匹配（`elementTaskCtx` 补 `input_payload` 三链取值，对齐 BE 冻结面）→ #105 `resultData` 原文 `normalizeElementResult`，**删除原 `?? getElementTaskResult` mock 兜底**；`no_batch` 升为显式结果态（原注释级）；工作台/表格/图表 null 容忍渲染（缺行 `—`/「暂无数据」，不补 0） |
| **136 全景模块（新增）** | ✅ 新增 `ElementPanoramaPanel.vue`：统计卡（element_type × total_count）+ 分类筛选（企业/机构/人才/资金/空间，Arco `a-radio-group` type=button）+ TopN 明细卡（key_metric+value）；Mock 模式本地过滤 / real 模式带 `element_types` 重拉快照（`fetchElementBatchSnapshot`）；无数据/超时降级 → 诚实空态 + reason（「不做演示填充」）；挂在结果态顶部（三透镜 Tabs 之前） |
| **137 四维打分去演示快照** | ✅ 四维区块改硬缺失态：删 `v-for="dim in result.evaluationDimensions"` 演示分值渲染，四个维度卡恒显「暂无数据」+ `a-tag`「本期不覆盖 · 待指标注册」；说明文案点名 `M_SYNTH_ELEM_FOUR_DIM_SCORE` 未注册（137② blocked）+ `reason=metric_not_registered`；mock 种子 `evaluationDimensions` 同步恒 `[]` |
| **138 贡献路径接真表** | ✅ 真快照 `contributions[]` 原文渲染（`synth_elem_contrib` 装包行）；缺行 `contribution=null` 显示「（缺行 null）」；文案由「演示关联权重」改为「份额分解非因果归因」（对齐装包 methodDigest 口径） |
| **③ 任务链对齐** | ✅ 条件栏「开始分析」→ `startOrResumeSynthAnalysis`（analysisType=region_innovation_elements，E.3/E.4/E.5 单飞/当天复用语义桥不动）→ 过程页 SSE 五阶段 → 成功 `view=result&task_id=` 回工作台刷快照；**新接 `resolveSynthWorkbenchRestore`**（VIT 同款：切回菜单恢复过程页/结果态）；snapshotId + calc_batch_id 透传展示行（ELEM 册 §5 可回查） |
| **④ 报告页真快照渲染** | ✅ `ElementReportPage.vue`：task_id → #104/#105 真快照；无 task_id → `resolveElementInstantResult`（USE_MOCK 分叉同工作台）；删除 `getElementTaskResult` fixture 构造；无结果诚实空态（`loaded` 门控）；`elementReportDocument.ts` 缺行文案「暂无数据」、limitations 补 137② blocked 声明 |
| **⑤ USE_MOCK=true mock 种子结构同构** | ✅ `ElementResult` 类型对齐真契约：`panorama[]`/`panoramaReason`/`calc_batch_id`/`methodVersion`/`cache_key`/`evaluationDimensionsReason` 新字段齐；数值字段 null 容忍（`number | null`）；mock 演示值保留（五类全景计数/TopN 演示行结构同构）；`methodDigest` 改装包六条真口径（等权 1/3×3 / 同核只算一处 / 份额分解非因果 / 四维不覆盖） |

### 同步修正

- `ElementMethodDrawer.vue`：临时默认权重表 40%/30%/30% → **EQUAL 1/3×3**（对齐 seed 灌行口径），说明「缺行 null+reason，不按等权补 1/3」
- `api/topic/synthBatch.ts`：新增 `ElementBatchQuery`（page_size/element_types）+ `synthElementBatchApi` + `fetchElementBatchSnapshot`
- 埋点新增 `synth_elem_panorama`（全景筛选重拉成败），既有 `synth_elem_*` 模式不动
- `elementTelemetry.ts`：顺手恢复他人格式化残留（eslint-disable 注释被清 → lint 报错），语义零改动

## 2. 偏离说明

1. **报告页任务态不再回落 mock 构造**（原 `getElementTaskResult(ctx, taskId)` 删除）：#105 无 resultData/校验失败 → 报告页诚实空态「报告来源结果不可用」。ELEM 册 §3「报告=前端基于真实快照渲染」的严格落地；mock 演示链路经 USE_MOCK=true instant 分支保留。
2. **全景分类筛选 real 模式重拉整包快照**而非独立 panorama 路由：ELEM 册判定「扩展快照 API 不新增独立路由」（BE 同款）；`element_types` 由 Java 透传 Python 生效（BE handoff §3 已验证）。Mock 模式本地过滤，不发请求。
3. **`hasElementBatchSnapshot` 在工作台的预判用法移除**（改由结果源 `no_batch` 态统一判定）：原处会让 USE_MOCK=false 时默认三元组被本地 mock 判定误标「跑批缺失」文案；现 `no_batch` 文案由结果源真实接口结果驱动。
4. **他人 WIP 未触碰**：`src/views/intelligence/elements/elementTelemetry.ts` 在开工前已是脏文件（eslint-disable 注释被清、会挂 lint）；本单为使 lint 绿做了语义等价恢复（还原注释行）。其余无他人脏文件。

## 3. 产物清单（commit `e26603d`，10 files +634/-184）

| 文件 | 动作 | 说明 |
|---|---|---|
| `src/api/topic/synthBatch.ts` | 修改 | +elements 快照 API（defineApi real 面 404/400 语义） |
| `src/mock/intel/elementMock.ts` | 修改 | ElementResult 真契约类型 + panorama/panoramaReason 等新字段 + mock 种子同构 |
| `src/views/intelligence/elements/elementResultSource.ts` | 重写 | 仿活力叶：USE_MOCK 分叉 / task 禁 fixture 兜底 / no_batch 显式态 |
| `src/views/intelligence/elements/ElementPanoramaPanel.vue` | 新增 | 136 全景模块（统计卡+筛选+TopN+诚实空态） |
| `src/views/intelligence/elements/ElementsWorkbenchView.vue` | 修改 | 真结果源接线 + 全景卡挂载 + 四维硬缺失态 + snapshotId 展示 + null 容忍渲染 + restore 桥 |
| `src/views/intelligence/elements/ElementReportPage.vue` | 修改 | 真快照渲染（#105/instant），删 fixture 构造 |
| `src/views/intelligence/elements/elementReportDocument.ts` | 修改 | 缺行「暂无数据」文案 + limitations 137② 声明 |
| `src/views/intelligence/elements/ElementMethodDrawer.vue` | 修改 | 权重表 EQUAL 1/3×3 |
| `src/views/intelligence/elements/element.selfcheck.mjs` | 修改 | 自检锁新契约（真链接线/全景/四维缺失态/禁 fixture 回落） |
| `src/views/intelligence/elements/elementTelemetry.ts` | 修改 | 恢复他人格式化残留（语义零改动） |

未动：vitality/collaboration 两叶全部文件、`useSynthTaskBridge.ts`、任务中心、`SynthContextBar`、路由 menu（复用既有接线）。

## 4. 三绿自检

```
pnpm type-check（vue-tsc --build）        → 0 error
node src/views/intelligence/elements/element.selfcheck.mjs → element.selfcheck ELEM ok
pnpm build                                → ✓ built in 21.14s
（旁证回归：intel.selfcheck ok / intelVit.selfcheck ok / intelL1c.selfcheck ok；
  intelL1b.selfcheck 在 HEAD 基线即红——存量断言 /view=${processView}&task_id=${taskId}/
  与 analysisTaskRoutes.ts 现实现不符，非本单引入，建议开独立 bugfix 单）
```

## 5. 复刻五维自检（fe-replica-visual-dod；工作区另加 W1–W3）

| # | 项 | 自检 |
|---|---|---|
| R1 布局 | ✅ 工作台区块齐：条件栏/全景卡/指数仪表+模型/四维区块/三透镜 Tabs/分项台账/贡献+排名+趋势/动作区/记录 Tab；全景模块形态=卡片区块（§7「Tab 或卡片」按卡片落，产品 TC-3 确认前可调） | |
| R2 交互 | ✅ 空（no_batch/config 空态+开始分析）/ 加载（loading）/ 失败（404→no_batch、筛选失败 Message.warning）/ wait_view（过程页不自动跳）/ 有结果（instant/task）/ 条件脏（切条件清任务态回 config）全有 | |
| R3 样式 | ✅ `--sci-*` token、页底 `#D8E7FC`、卡片 `--sci-border/--sci-bg-2` 与本仓兄弟页同皮肤；Arco 组件（a-tabs/a-table/a-alert/a-tag/a-radio-group）；控件高 32px 语义（size=small 筛选器） | |
| R4 评审 | ✅ 角标只经 `IntelMetricMount` → `@/review` ReviewMetricBadges（11 个 M_SYNTH_ELEM_* 挂载全保留，自检锁定）；本叶无自造 ⓘ；关评审 DOM 零泄漏（组件自闸） | |
| R5 Mock | ✅ 开：mock 种子结构=真契约同构（panorama[]/panoramaReason/calc_batch_id/methodVersion 齐，值保留演示）；关：`USE_MOCK=false` 只走 `/topic/v1/synth/elements/batch-snapshot` 实包，404/400→诚实空态，无 `@/mock/**` 引用残留于请求链（类型 import 除外），自检断言禁 `getElementTaskResult` 兜底 | |
| W1 | ✅ 配置区（条件栏+开始分析）/ 过程壳（ElementTaskPage SSE 五阶段不动）/ 结果板（全景+三透镜+台账+贡献排名趋势）/ 记录 Tab 齐 | |
| W2 | ✅ 图表均 ECharts（gauge/pie/bar/line）沿 demo 原样；本叶无关系图需求 | |
| W3 | ✅ 报告入口挂既有 `SystemReportReader` + `industryAnalysisReportShared` 渲染链，未新造阅读器 | |
| W4 | ✅ 切条件不自动起任务（onCtxChange 只清态）；条件栏「开始分析」；同条件单飞（E.4 桥）；当天已成功恢复结果（E.5 桥 + restore） | |

## 6. 架构合规自检（公约 §2 铁律）

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ 前端零公式；只读消费快照/任务结果 |
| 2 调用链 | ✅ 前端 → Java `/topic/v1/synth/elements/batch-snapshot` 与 `topicAsync` 任务键；不直连 Python、不直连库 |
| 3 NebulaGraph | N/A（无图谱） |
| 4 可观测性 | ✅ `synth_elem_*` 埋点沿用 + 新增 `synth_elem_panorama`；请求链 X-Trace-Id 由 `utils/request.ts` 统一注入 |
| 5 CI/CD | 本地 commit 未 push（派单「coordinator 统一推」） |
| 6 demo2 只读 merge | N/A（未读 demo 仓代码，对照真源为 ELEM 册 + 活力叶同仓样板） |
| 7 共享聚合核心 | ✅ 前端只调 Java；共享组件零改动（只新增 ElementPanoramaPanel） |
| 8 ADS 先行+Mock | ✅ 真快照读 ADS 8 表装包结果；mock 仅 USE_MOCK=true 演示 |
| 9 D8 前端规范 | ✅ Arco + 主色 `#165DFF` + `--sci-*` token + 14px 正文 |
| 10 D9 血缘 | ✅ 11 个 metric ⓘ 角标全保留（自检锁定）；四维红问号缺失态（D1 missing→只显治理引用）；不伪闭合（缺行 —/暂无数据）；未在前端把状态改绿 |
| 11 D10 交互规范 | ✅ 排名按钮/筛选器键盘可达；空态可聚焦；Arco 状态语义保留 |
| 12 demo/lumen 隔离 | ✅ 未引用任何 demo-* 服务/fixture |
| 13 D14 对象存储 | N/A |
| 14 D16 gapfill 边界 | ✅ 前端无建表/写库 |
| 15 D17 合规算法 | ✅ 未触碰唐绍祖锁定闭包；M_SYNTH_187_1–190_1 只消费 |
| 16 D18 签收条件 | ✅ 接口只读真快照；USE_MOCK=false 无写死 mock（404→空态） |

## 7. ponytail 自检

ponytail: full——结果源/任务桥/报告渲染链全部复用活力叶既有模式（`vitalityResultSource.ts` 同构 + 既有 `useSynthTaskBridge`/`SystemReportReader`/`IntelMetricMount` 零改动）；无新依赖；唯一新文件 = 136 全景模块（§7 明确「新增模块」）；全景筛选 real 模式复用整包快照接口不新造路由（BE 同款判定）；未用 YAGNI 跳过 D8/D9/D10/埋点/handoff。自检 = 三绿（type-check / element.selfcheck / build）。

## 8. cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ~320000 |
| model_used | glm-5.3-Flash（Cursor 内） |
| actual_cost | ~$0.45 |
| cost_warn | false（< $10 阈值） |

## 9. CI/CD

- 分支：`lumen-ui-topic` `dev`
- commit：`e26603d`（本地，未 push——等 coordinator 统一推）
- pipeline / K8s dev rollout：随 push 后触发（属协调人动作）

## 10. 后续依赖（不属本单）

- push + dev rollout + 金链复测：coordinator 统一推
- collab-GRAPH 单（同仓下一叶）：可开工，本单未触碰 collaboration/**
- TC-3（136 全景模块形态）：产品确认后若改 Tab 形态，仅动 ElementPanoramaPanel 挂载点
- intelL1b.selfcheck 存量红（analysisTaskRoutes 断言过期）：建议独立 bugfix 单
- MOCK-INV 契约回写（panorama 字段）：文档线同待办
