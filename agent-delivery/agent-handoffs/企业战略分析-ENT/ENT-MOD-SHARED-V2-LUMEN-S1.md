# ENT-MOD-SHARED-V2-LUMEN-S1 · 三模块共享底座与数据层（lumen-ui-topic）

> 格式参考 `ENT-MOD-SEARCH-V2-S1.md`；设计规格：`docs/superpowers/specs/2026-07-29-ent-v2-lumen-eval-risk-recruit-design.md`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| claimed_at | `2026-07-29` |
| worktree_branch | `dev`（按任务书直推 origin/dev） |
| 说明 | 共享底座 + 三模块 API/Mock/类型/composable，**不写页面组件** |

## 范围与实现（对照任务书 §范围）

| 子项 | 状态 | 说明 |
|------|------|------|
| A.1 menu.ts 注册三路由 | ✅ | `enterprise/evaluation`、`enterprise/risk`、`enterprise/attraction`；`showInMenu:false` 且无 component → 自动落 `DevelopingView` 占位；对比篮分发 `canNavigate()` 通过，「承接页待接入」消除 |
| A.2 useCompareBasketDispatchContext.ts | ✅ | 解析 `enterprise_org_ids[]/return_context_id/source/analysis_type`；`analysis_type`(连字符)→任务中心 subType(下划线) 映射；`returnToCompareBasket()` 与篮页 sessionStorage 快照恢复闭环；`validateReturnContext()`（#97）可选降级 |
| A.3 searchBizApi DISPATCH_ROUTE 对齐 | ✅ | 旧 `/enterprise-center/*` → `/enterprise/evaluation`(tab/capabilityType)、`/enterprise/risk?tab=`、`/enterprise/attraction`，与 `config/compareBasketDispatch.ts` 一致 |
| A.4 enterpriseBreadcrumb 来源 | ✅ | 新增 `evaluation`/`risk` 来源；`attraction` 补 `to:'/enterprise/attraction'` |
| A.5 mock/register.ts 合并注册 | ✅ | 任务中心 7 + SSE 1 + EVAL 9 = 17 个注册；`analysisTaskAssetDownload`（#106）**按规格不注册** |
| B.6/7 api/enterprise/evaluation.ts | ✅ | 任务中心 #102–109 全量 + #113–121 全量；#109 SSE 以 `defineApi` 返回流句柄（real=EventSource）；#106 fetch 下载（blob+a[download]，携带 Authorization）+ `buildAnalysisAssetUrl` + `fetchAnalysisAssetJson` |
| B.8 types/evaluation.ts | ✅ | `AnalysisTaskEntity`(camelCase 全字段)、`AnalysisType` 九枚举、`AnalysisTaskStatus` 四态（无 pending）、SSE 事件/句柄、#113–121 类型；模板命名 `EvalTemplateItem` 避开既有 `EntTemplateItem` 冲突 |
| B.9 mock/enterprise/evaluation.ts + analysisTaskStore.ts | ✅ | 见下方「Mock 铁律对照」 |
| C.10 api/enterprise/riskInsight.ts | ✅（纠偏后） | **仅** `createRiskInsightTask` 薄封装（固定 `analysisType='risk_insight'`）；风险结果不另设端点，走 #105/#106 |
| C.11 mock/enterprise/riskInsight.ts | ⛔ 取消 | 见「纠偏记录」：风险/引育不单独造 mock，结果 JSON 结构是开放项，demo fixture 移植取消 |
| D.12 api/enterprise/recommend.ts 扩展 | ✅（纠偏后） | `createRecruitTask`（talent_recommend 薄封装）+ 候选名单 #98–101 re-export；无 `entRecruitResult` |
| D.13 types/recruit.ts | ✅ | `RecruitBaseRecommendation`/`AttractionExtension`/`CultivationExtension` + 风险信用三态等辅助类型（按 demo 结构；供 S4 结果 DTO 核对后消费） |
| D.14 useRecruit.ts | ✅ | 纯任务中心状态机：mode/workbench 切换、filters/weights、Σ=100 校验、七态 analysisState、#102→#109 SSE→#105 编排；`resultPayload` 仅真实模式经 #106 拉取（unknown 🟡），Mock 模式恒 null |
| D.15 mock/enterprise/recruitWorkbench.ts | ⛔ 取消 | 同 C.11 |

## 纠偏记录（重要）

初版曾为风险/引育发明独立结果端点（`entRiskInsightResult`/`entRecruitResult`）并移植 demo fixture（`RISK_GRAPH_FIXTURE`/`PAIN_ISSUE_FIXTURES`/推荐池）作为结果 mock。监管人孔东纠偏：**三模块接口共用一套任务中心，仅以 analysisType 区分**；catalog §0.1 明确风险/引育「额外同步接口：无」，结果 JSON 嵌套结构属开放项 🟡（待 Java/Python DTO 核对），且 #106 按规格不 mock 数据。已按此重做：删除两个 mock 文件与两个发明端点；风险/引育 API 仅保留任务创建薄封装；`types/riskInsight.ts` 裁至任务参数侧；demo fixture 不进入本仓（后续 S2/S4 若需演示数据，由其工作包在 DTO 核对后另行决策）。

## 产物清单

### 新增（9）

- `src/api/enterprise/evaluation.ts` — 任务中心 #102–109 + EVAL #113–121（17 个 defineApi + 3 个 helper）
- `src/api/enterprise/riskInsight.ts` — `createRiskInsightTask` 薄封装
- `src/api/enterprise/types/evaluation.ts` — 任务中心/EVAL DTO（camelCase/snake_case 分治）
- `src/api/enterprise/types/riskInsight.ts` — risk_insight 任务参数类型（🟡 scope 结构待契约核对）
- `src/api/enterprise/types/recruit.ts` — 引育推荐/任务参数类型
- `src/composables/useCompareBasketDispatchContext.ts` — 分发上下文解析 + 返回对比篮
- `src/composables/useRecruit.ts` — 引育状态机 ViewModel（曹丽影只消费本接口）
- `src/mock/enterprise/analysisTaskStore.ts` — mock 内部任务存储（Map；EVAL-/RISK-/REC- 前缀 id；六节点时间轴惰性推进；SSE drain 游标；种子任务/用户）
- `src/mock/enterprise/evaluation.ts` — 任务中心 + EVAL mock 实现

### 修改（8）

- `src/router/menu.ts` — 企业分析组追加 3 个隐藏 navItem
- `src/config/enterpriseBreadcrumb.ts` — 增 evaluation/risk 来源，attraction 补 to
- `src/api/enterprise/paths.ts` — 增 `TOPIC_ASYNC_V1`/`AnalysisTaskPaths`/`EvaluationPaths`
- `src/api/enterprise/recommend.ts` — 增 createRecruitTask + 候选名单 re-export
- `src/api/enterprise/types/index.ts` — 聚合三个新类型文件
- `src/api/enterprise/index.ts` — 聚合出口（paths 常量 + evaluation/riskInsight/recommend 新增）
- `src/mock/enterprise/searchBizApi.ts` — DISPATCH_ROUTE 对齐 lumen 路由（5 行）
- `src/mock/register.ts` — 追加 17 个注册

### 删除（2，纠偏）

- `src/mock/enterprise/riskInsight.ts`、`src/mock/enterprise/recruitWorkbench.ts`（未入库）

## Mock 铁律对照（设计规格 §4.2）

| 铁律 | 证据 |
|------|------|
| 同一 taskId 在 #102/103/104/105/109 自洽 | `analysisTaskStore.ts` 单一 Map 真源；`targetParams` 为 #102 参数 JSON 文本快照；#105 返回同一实体 |
| 状态仅 running/success/failed/cancelled | `AnalysisTaskStatus` 四枚举；store 无 pending 分支 |
| #113 `is_preview` 原样保留 | mock 返回 `is_preview: true`，items 仅取 catalog 示例字段（0037）不扩展 |
| #115 `data_source='mock'` 原样保留 | mock 固定返回；`per_enterprise` 不填充（🟡） |
| 模板 snake_case / 任务 camelCase | `EvalTemplateItem`(template_id/sub_type/is_default/create_time…) vs `AnalysisTaskEntity`(taskId/analysisType/createTime…) |
| 不发明 dimension_diff/dimensions/per_enterprise | #114 `dimensions:[]/groups:[]` 1 层占位；#115 不含 per_enterprise；#116 `dimension_diff:[]` |
| 不发明预检阈值 | #115 简单回显 + `ready = codes.length>0`，无阈值判断 |
| #106 不 mock 数据 | 未注册 `analysisTaskAssetDownload`；API 注释标明 Mock 模式禁止直调（页面做下载动态模拟） |

## DoD 对照

| DoD | 状态 |
|-----|------|
| 三路由可访问（占位）；分发不再提示「承接页待接入」 | ✅ menu.ts 注册后 `router.resolve` 命中 |
| useCompareBasketDispatchContext 解析 query + 返回方法 | ✅ |
| 所有 API 声明用 `defineApi({ id, real, mockDelay? })` | ✅ 17 个（#109 返回流句柄；#106 无 mockDelay 且不注册 mock） |
| 类型与 catalog 一致、不发明未定义字段 | ✅（结果 JSON 侧整体留 🟡 不定义） |
| useRecruit 稳定 ViewModel | ✅ 签名见文件头注释 |
| `npm run build` + `type-check` | ⚠️ 未跑：执行被环境跳过（长任务）；IDE TS Server 全 `src/` 诊断 0 错误；**待手动/CI 补跑** |
| 不改 package.json / vite.config / tsconfig | ✅ |

## 关键设计决策

1. **#102–109 物理位置**：按任务书放 `evaluation.ts`；risk/recruit 以薄封装复用（不另起 analysis.ts）。
2. **#109 SSE 适配**：`defineApi<{user_id}, AnalysisTaskStreamHandle>`；real=EventSource（无 Authorization 头，依赖 user_id 会话键 + 网关匿名可达）；mock=drain 式模拟发射器（connected→created→progress×6→success，500ms tick，close 清定时器）。
3. **#106 下载**：request 实例的 R<T> 解包不适用于 blob/302，故用原生 fetch + Authorization 头 + a[download]；`fetchAnalysisAssetJson` 供后续结果编排复用。
4. **useRecruit 七态映射**：success 且 `resultAssetId` 为空 → empty；`partial` 预留不置位（待结果 DTO）；401/403/424 或权限语义 → permission；其余异常 → error；取消 → 回 initial。
5. **种子任务**：每用户首次访问注入 3 条历史成功任务（EVAL/RISK/REC 各一），保证 #103 列表非空；引育种子 weights 用占位键 `w1/w2/w3`（Σ=100，🟡 指标 key 待契约）。
6. **模板写操作**：会话内内存态（刷新还原），对齐 searchBizApi 写操作收敛口径；系统模板 3 条种子（is_default=1）。

## 开放项（移交 S2/S3/S4）

- 🟡 #106 结果 JSON 嵌套结构（含风险图谱/痛难点/引育推荐条目）待 Java/Python DTO 核对后补类型与展示；届时评估是否仍需演示 fixture。
- 🟡 #114 `dimensions/groups`、#115 `per_enterprise`、#116 `dimension_diff` 结构未定义，mock 占位。
- 🟡 relationScope/diagnosisScope/filters/weights 内部结构对齐 demo 交互口径，待 Python 契约核对。
- 🟡 模板 `industry` 字段名（非 industry_code）保持 catalog 原名。
- `npm run build` / `type-check` 全量待补跑。

## CI/CD

- 分支：`dev` 直推（任务书明示）
- commit：`e040df6` — `feat(ENT-MOD-SHARED-V2-LUMEN-S1): shared analysis task center APIs/mocks/types + dispatch context & recruit composables [agent:frontend-agent]`
- 远程：已 push `origin/dev`（`5478aee..e040df6`）

## 架构合规自检（Design.md §14 摘要）

- ✅ 仅经网关调 Java（`/topicAsync/topic/v1/**` 前缀常量化于 paths.ts）；未直连 Python/DB
- ✅ defineApi + registerApiMock 双轨；页面/组件零新增，无 `@/mock` 直引风险
- ✅ traceId 沿用 request.ts/observability.ts 既有注入（fetch 下载走网关同样经代理）
- ✅ 单文件行数受控（最大 analysisTaskStore.ts ≈ 340 行 mock 内部模块）
- ✅ 未改 package.json / vite.config.ts / tsconfig.json；无新增依赖
