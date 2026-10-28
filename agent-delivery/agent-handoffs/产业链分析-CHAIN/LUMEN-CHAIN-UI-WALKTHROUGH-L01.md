# LUMEN-CHAIN-UI-WALKTHROUGH-L01 · 产业链分析模块页面 demo 布局对齐与人走查整改

> 格式参考 `templates/handoff-template.md`；本单 **进行中**，本文为首批（产业诊断关键环节/瓶颈 + 底部报告区）as-built。  
> Demo 真源：`repos/demo-ui-topic/src/app/pages/industry-center/IndustryDiagnosisPage.tsx`（`KeyLinkResult` 双栏 + `ResultReportPanel`）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 2026-10-28 孔东走查登记任务；本批关联 commit `2b8630c` 后认领并转 `in_progress`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对齐 demo 布局/双栏/报告区骨架；复用 G6、`SectionPanel`、`SystemReportReader` 路径；扩展 GetResult 解析不伪造代表企业/归因。未用 YAGNI 跳过 D8/D9/D10、评审自闸、诚实空态。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂 Headroom；对照 demo TSX 与 lumen Vue 页 DOM 结构。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（纯 FE 布局复刻，无架构图变更） |
| 图 diff | — |
| 会签态 | — |

## 范围与实现（首批 · 2026-10-28）

### 问题（走查）

- **关键环节识别**、**产业瓶颈堵点识别** 结果区与 demo 差距大：详情堆在主栏下方，缺 **右侧详情/归因栏**；结果区底部缺 **诊断报告生成** 区块。

### 已落地

1. **`IndustryKeyLinkResultBoard.vue`**（新）：指标条 + `diagnosis-result-grid` 双栏；左 G6 全链路；右 `diagnosis-link-detail`（`data-testid="key-link-detail"`），环节详情 / 代表企业 / 企业画像分区。
2. **`IndustryBottleneckResultBoard.vue`**（重写）：双栏；右侧「瓶颈智能识别与归因建议」`a-descriptions`；KPI 读 `kpi.bottleneck_count`、`kpi.max_severity`（对齐 `CHAIN-DIAG-NARRATE-L01` 实包语义）。
3. **`IndustryAnalysisResultReportPanel.vue`**（新）：底部 `SectionPanel`，文案键 `DIAGNOSIS_L6_REPORT`；「生成报告 / 查看报告」；有报告走 `openReport`，否则提示（与 demo `ResultReportPanel` 结构对齐，非终态交互）。
4. **`IndustryDiagnosisPage.vue`**：key_link / bottleneck 改用上述组件；`cycle` / `key_link` / `bottleneck` 成功结果末尾统一挂报告面板。
5. **解析**：`industryWorkspaceRuntime.js` 扩展 `parseKeyLinkDetail`（`representative_enterprises.items`、环节字段、竞争/技术趋势等）；`industryChainTask.ts` 新增 `parseBottleneckNodeDetail`（`sections.node_details.items`）。
6. **配置**：`industryWorkspace.ts` 增加 `DIAGNOSIS_L6_REPORT`。
7. **自检**：`industryReplicaFix.selfcheck.mjs` 更新 key-link / parse 断言。

### 同 commit 附带（非本单主范围）

- `enterprise/development` 重点企业/明星企业链域 scope 小改（commit message 标注 `SYSINT-04-04-L01`）；走查整改以诊断页为主。

### 未闭合（后续本单继续）

- 周期识别结果区：demo 级周期模型自定义 + 底部报告区信息密度。
- 产业链其余工作台（区域、深圳、查询、全景专业版等）五维走查清单与差距登记。
- `USE_MOCK=false` 下实包侧栏仍空时，区分 parser vs 后端字段并联调微调。
- Design §14 + 产品实现规程附录 D/E 扫描摘要（完工批补）。

## 偏离说明

- 报告「生成」仍为骨架：依赖既有 analysis 任务 / `SystemReportReader` 链路，未新增 Java 契约。
- 代表企业 / 画像无数据时保持诚实空文案，不用 Demo fixture 填名。

## 产物清单

- 代码：`repos/lumen-ui-topic` `origin/dev` commit **`2b8630c`**
- 本 handoff：`agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-UI-WALKTHROUGH-L01.md`

## 测试结果

- `node src/views/industry-center/industryReplicaFix.selfcheck.mjs` — 绿（本地 2026-10-28）
- CI：待本批 push 后 Pipeline（未在本 handoff 批次单独盯 Job ID）

## 遗留风险

- GetResult 字段名与 parser 不一致时侧栏为空（诚实），需 Java 实包对照 `CHAIN-DIAG-NARRATE-L01` 微调。
- 周期 / 其它模块布局仍可能与 demo 有差距，需人走查逐项闭合。

## CI/CD（必填 · 首批）

| 项 | 值 |
|----|-----|
| 分支 | `lumen-ui-topic` `origin/dev` |
| commit | `2b8630cbbb612eb9301f098518f467c24168aa39` |
| pipeline URL / ID | 待 GitLab dev 流水线 |
| K8s rollout | 待 CI deploy |
| dev 测试 URL | 专题 dev 网关 / 本地 Vite；诊断页 `key_link` / `bottleneck` 结果态目视 |

## 可观测性

- 沿用 analysisTask / industry 现有请求链；本批无新增埋点。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ |
| 2 调用链 FE→Java | ✅ |
| 3 Nebula | ✅ 不直连 |
| 4 可观测 | ✅ 沿用 |
| 5 CI | ✅ push `origin/dev` |
| 6 demo2 不 merge | ✅ Vue 组件重写 |
| 7 只调 Java | ✅ |
| 8 诚实空 | ✅ 无 fixture 填代表企业 |
| 9 D8 | ✅ Arco + 现有 diagnosis token |
| 10 D9 | ✅ 评审挂点未删 |
| 11 D10 | ✅ 双栏/报告区结构 |
| 12 D12 | ✅ 不打 demo 服务 |

## 涉及文件（本批）

- `src/components/industry-center/IndustryKeyLinkResultBoard.vue`（新）
- `src/components/industry-center/IndustryAnalysisResultReportPanel.vue`（新）
- `src/components/industry-center/IndustryBottleneckResultBoard.vue`
- `src/views/industry-center/IndustryDiagnosisPage.vue`
- `src/views/industry-center/industryDiagnosis.css`
- `src/assets/layout/diagnosis-shell.css`
- `src/config/industryWorkspace.ts`
- `src/utils/industryChainTask.ts`
- `src/utils/industryWorkspaceRuntime.js`
- `src/views/industry-center/industryReplicaFix.selfcheck.mjs`

## cost（进行中 · 首批回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000（本批走查+实现+派单登记估计，任务未完工） |
| model_used | composer（Cursor Agent） |
| actual_cost | 待账单核对 |
| cost_warn | green |
