# FE-TOPIC-SMALL-POLICY-GAP-L01 · 专题小屏·政策分析差距完善（首版）

- **状态**：首版完成（in_progress → integration），待用户看效果
- **角色**：agent:frontend-agent（监管 human:孔东）
- **仓**：`repos/lumen-ui-topic-mobile`（改动停在本地工作区，按孔东 2026-11-12 裁定不自动 commit）
- **日期**：2026-11-17
- **ponytail**: full（复用 ChainAnalysisShell/ChainReportSheet/ProfileDrawer/StatCard 既有组件；结果解析器自 PC 仓对齐移植，未新造口径；未新增 npm 依赖）

## 范围与实现（对照 PC 真源）

任务将批 A（政策分析三叶）+ 批 B（政策查询）并入一个任务首版实施。

### 1. 政策分析三叶（`PolicyAnalysisConfigView.vue` 重写）

| 缺口 | 实现 |
|---|---|
| 提交契约缺口（extra 只传 analysis_fp） | `buildExtra()` 对齐 PC `buildCreateParams`：`sub_type/task_type/scope_kind/ui_scope_kind/industry_vid|industry_id/granularity/timeseries_dims/regions/dims/weights/selected_indicators`（`industrySubmitFields()` 对齐 PC：图上码→`industry_vid`，INB 短码补 `chain:` 形式） |
| 指纹裸 join | `policyAnalysisFingerprint()` 与 PC 同口径 SHA-256（canonical JSON），指纹输入覆盖全部配置参数（对象+粒度+维度+区域+权重+指标） |
| 配置控件缺失 | 时序叶：粒度 picker（年/季/月）+ 三维只读徽章；区域叶：锁定区（不可去）+ 可选区勾选（京津冀/成渝）+ 评价维度勾选（默认全开可去）；深圳叶：三维只读默认卡（34/33/33 + 默认指标） |
| 记录页签缺失 | 照搬 `IndustryDiagnosisView` records 模式：`analysisTaskList` 按类型过滤 + 状态筛选 + 查看结果（`showExternalResult`）+ 复制配置（`parsePolicyTaskConfig` 回填粒度/区域/维度）+ 删除 |
| 报告死按钮 | `@open-report` → `openReportFor()` → `ChainReportSheet`；`chainBlockReportDocument` 扩展政策三叶报告块（KPI/表格/条形，数值只读 PC 同源板） |
| 深链缺失 | `?task_id` 直接拉结果进结果态；`report=1` 连带开报告 |
| D9 缺失 | 时序四 KPI（`M_POLICY_TOTAL_COUNT/M_POLICY_TIMESERIES/M_POLICY_VALIDITY_RATE`）+ 区域三 KPI（`M_POLICY_SUPPORT_STRENGTH`）+ 深圳三卡（`M_POLICY_SUPPORT_STRENGTH/M_POLICY_INDUSTRY_FIT/M_POLICY_IMPLEMENTATION_EFFECT`）全走 `StatCard metric-id` |
| 结果解析走样 | 换用 PC 同源解析器（见下），替换原先简化 interface |

### 2. 新增文件

- `src/config/policyAnalysisRegistry.ts` — 常量真源（REGION_LOCKED/OPTIONAL、TIMESERIES_MODEL_DIMS、REGION_COMPARE_DIMS、DEFAULT_SZ_WEIGHTS、POLICY_ANALYSIS_STAGES、指纹输入、`parsePolicyTaskConfig` 回填、`toPolicyGraphVid`）
- `src/utils/policyTimeseriesResult.ts` — 时序结果板（PC 对齐移植；含 KPI metricId、密度/支持/层级趋势、节点、洞察）
- `src/utils/policyRegionalResult.ts` — 区域对比结果板（矩阵行、条文摘录、深圳位次 KPI）
- `src/utils/policyShenzhenResult.ts` — 深圳三维卡（support/fit/effect + strategies + reportChapters + 冻结快照权重；空分不写 0）

### 3. 修改文件

- `src/utils/chainBlockReportDocument.ts` — `blocksOf` 分发加政策三叶；`frozen` 入参（深圳权重/章节兜底）
- `src/views/policy/PolicySearchView.vue` — 详情抽屉改三页签（概览+政策原文+条款结构化）；四维因素卡（`M_POLICY_SUPPORT_STRENGTH` + MetricMarker）；筛选加类别列 + 地区全量（PC REGION_OPTIONS 八省）；热标签对齐 PC `POLICY_HOT_TAGS`（字段快捷筛，非关键词）；推荐态（空条件 limit 6）+ localStorage 搜索历史（PC 同 key `gkx-policy-topic-search-recents:v1`）
- `src/review/readiness.generated.ts` — 补 `M_POLICY_SUPPORT_STRENGTH`（D1 aligned + D2 partial/provisional + D3 partial + D4 mock，pendingRef QPOL-02；对齐 PC `policyReadinessSeed` + metric-registry MCP 实查）

### 4. 防漏扫描（附录 D 精简）

- D.1 页面差集：政策 6 路由（查询/门户/三分析叶/新闻）此前已闭合，本轮补三叶深度
- D.2 本地 KPI 接线：三叶结果区 KPI 全带 metric-id（测试断言）
- D.3 镜像 vs 矩阵：`M_POLICY_SUPPORT_STRENGTH` 按 metric-registry MCP 实查补入镜像
- D.4 错挂/正名：时序 KPI 用后端回传 metricId（`kpis.*.metricId`），不前端硬编码错配
- D.5 契约防漏：`policy-gap.test.mjs` 9 断言（提交字段/常量同文/记录页签/报告/深链/D9/查询页/解析器字段族/报告分发）

## 偏离说明

- 深圳权重/指标勾选工作台不进小屏（Design-mobile §10 红线），只读默认提交（34/33/33 + 默认勾选指标）——与 PC 指纹一致，跨端可复用判定
- 技术领域对象类型（tech_field）首版不做，提示去 PC（§10）
- 高级筛选 DSL 布尔树、对比篮分发不进小屏（§10）

## 验收证据

- `node --test scripts/policy-gap.test.mjs`：9/9 绿
- `npm test`：62/62 绿（全仓防漏）
- `npm run build`（含 `vue-tsc --build`）：✓ built in 11.93s（chunk 警告为存量 echarts/preset）
- K8s dev：待用户确认 commit + push 后走 CI 自动部署

## 架构合规自检

- ✅ 调用链：前端 → Java `/topicAsync` `/policy/topic/v1`（`analysisTask*`/`policyDocs`），无越层
- ✅ D9：统计数字旁 ⓘ（metric-id → MetricMarker，reviewMode 门控，关闭零泄漏——新镜像项同受控）
- ✅ D12：只读对照 PC 重写，未 merge
- ✅ I2-12：ChainAnalysisShell 闸门（切条件不自动 create、今日同指纹复用、重新分析、4s×75 轮询）
- ✅ 诚实性：解析器缺字段诚实空（—），不补 0；`USE_MOCK=false` 无 fixture 填数

## cost

- actual_tokens ≈ 210k（input+output 合计）；model_used: glm-5.3（Cursor agent）；actual_cost ≈ $0.9；cost_warn: false
