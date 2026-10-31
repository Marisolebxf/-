# FE-ENT-EVAL-REPORT-REAL-L01 · 企业技术力评估 HTML 报告内容真实化 + PDF 直下导出（重开 v2）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 锁定窗口 | 2026-10-23 14:30 – 18:30（4h，重开轮） |
| 说明 | 监管人走查判定首轮交付不符预期（模板仍旧版纯文字、导出走打印预览），聊天授权按新口径重做：①新作分块+图表的评估报告专用模板；②导出直下 PDF 文件。新依赖 `jspdf` + `html2canvas` 经监管人书面批准（会话选项确认）。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 依赖扩展经用户逐项批准（护栏 2 例外已授权）：`jspdf` 新增、`html2canvas` 声明为直接依赖（包管理器锁内已有同版本 1.4.1，`@antv/g` 传递依赖，零新增下载）。图表 option 与 KPI 卡复用结果工作区现有口径（同数据同色板）；PDF 复用 `downloadReportBlob` 下载链路与 `ReportExportButton` 权限闸门。 |

## 首轮偏差与重开口径（监管人 2026-10-23 裁定）

| # | 监管人预期 | 首轮交付（不符） | 重开 v2 |
|---|-----------|----------------|---------|
| 1 | 新作模板：清晰美观、有分块、有文字、有图表，涵盖结果展示内容 | 数据真实化但仍用通用 `SystemReportReader`（七章节纯 `<ul><li>` 文字列表，无 KPI 卡/图表/分块） | 新模板 `EvalReportReader.vue`：A4 分页（封面页 + 内容页），KPI 卡片块 / 排名条形图 / 维度雷达图 / 排名明细表 / 维度差距表 / 文字块，全 D8 token |
| 2 | 导出下载 PDF 文档 | `window.print()` 打印预览，需手动「另存为 PDF」 | 逐页 `html2canvas` 截图 → `jsPDF` A4 拼装 → `downloadReportBlob` 直接触发浏览器文件下载，全程不弹打印预览 |

范围裁定（监管人选项确认）：新模板仅用于企业评估报告；其余 6 个报告消费域（风险/招引/重点/深圳现状/服务商×2）不动，`window.print` 与 print CSS 已随之拆除、通用视图恢复只读展示。

## 范围与实现

### 1. 报告文档模型 v2（分块结构化）

- **新文件** `src/components/enterprise/evaluation/evalReportDocument.ts`：
  - `EvalReportDocument` 分块模型：`kpi` / `ranking-chart` / `radar` / `table` / `text` 五种块；屏显与 PDF 共用同一数据源。
  - `buildEvalReportDocument` 接收 `mapEvalResultPayload` 映射后的真实结果（rows/indicators/dimensionRows/summary/**radarAxes/radarSeries** 新增），指纹升 `report-v2` 区分旧模板。
  - 八块内容：执行摘要（4 KPI 卡：最高分/企业数/平均分/高可信数，均带 metric_id 供 ⓘ 角标）、对象与范围（生效指标+权重）、关键发现、排名条形图、维度雷达（取前两家，对齐工作区对比口径）、排名明细表、维度差距表、来源说明、局限性（缺失指标/低可信诚实披露）。
  - 诚实空态保留：result 缺位或 rows 空时报告明确「不伪造数值」（AGENTS.md §D9-4）。
- `src/components/report/enterpriseDomainReports.ts`：eval 专用部分整体迁出（含 `EvalReportResultInput`/`confidenceLabel`），风险/招引/重点/深圳现状四域原样保留。

### 2. 报告模板 v2（分块 + 文字 + 图表）

- **新文件** `src/components/enterprise/evaluation/EvalReportReader.vue`：
  - A4 页容器（宽度自适应分析面板，PDF 按 A4 比例切页）：封面页（报告编号/任务/版本/生成时间）+ 内容页（八块顺序平铺）。
  - 图表复用现有 option 口径：排名条形图（0–100、主蓝 `#165DFF`/尾部灰，对齐 `EvalRankingChart`）、维度雷达（0–100、低透明面积、双色序列，对齐 `EvalRadarPanel`）。
  - KPI 卡复用 `ReviewMetricBadges`（D9 ⓘ 角标，评审模式门控自闸）；表格为纯 `<table>`（PDF 截图无 Arco 组件渲染风险）。
  - 平铺铁律：无 Tab / 无折叠 / 无目录点击依赖（DoD 原文要求保持）。

### 3. PDF 直下导出

- **新文件** `src/components/enterprise/evaluation/evalReportPdf.ts`：
  - `exportEvalReportPdf`：`.eval-report-page` 逐页 `html2canvas`（白底、scale≤2）→ `jsPDF` A4 拼装 → `downloadReportBlob` 触发下载，文件名 `标题_时间.pdf`。
  - `ponytail:` 天花板注释：PDF 文字为图片（不可选中复制）；单块超一页高时块内硬切（升级路径=块内细分或服务端生成）。
- `src/components/enterprise/evaluation/EvalResultWorkspace.vue`：评估报告视图换 `EvalReportReader`；导出按钮接 `exportEvalReportPdf`（loading/成功/失败反馈）；`reportDocument` 传入 radarAxes/radarSeries 与分模式 metric_id。
- `src/components/report/EnterpriseAnalysisReportView.vue`：回退 window.print，恢复只读展示（其余 6 域消费）。
- `src/assets/layout/system-report-reader.css`：`@media print` 块整体拆除（回到 HEAD 状态）。

### 4. 依赖变更（已获批）

- `package.json`：`+ jspdf@4.2.1`、`+ html2canvas@1.4.1`（后者 lock 内本有同版本，声明为直接依赖；pnpm `core-js` 构建脚本告警与本任务无关，未批准执行）。

## 验收证据

- 自检 `node src/components/report/reportExport.selfcheck.mjs`：ok（v2 契约五块齐全、radar 输入、模板无 Tab/折叠、PDF 走 jspdf+html2canvas+downloadReportBlob、无 window.print 残留、通用视图与 print CSS 回退干净、评估指纹 v2）
- 类型检查 `npx vue-tsc --build`：exit 0
- 回归：`enterpriseEvalLoaders.selfcheck.mjs` ok、`enterpriseEvaluation.indicators.selfcheck.mjs` ok、`industryChainTask.selfcheck.mjs` ok、`industryReplicaFix.selfcheck.mjs` ok
- ESLint（7 个改动文件）：0 问题
- 改动清单：8 文件（3 新增 + 5 修改，+261/−83；git status 本地未提交，等人工验收）

## 架构合规自检

- ✅ 调用链：报告数据来自前端已获取的任务结果 payload，无新接口、无越层
- ✅ D8：新模板全部使用 `--sci-*` token / 图表色板 / Design.md 字号圆角；主蓝 `#165DFF`
- ✅ D9：KPI 卡带 metric_id（ⓘ 经 ReviewMetricBadges 评审门控）；局限性章节如实披露缺失/低可信；USE_MOCK=false 时不读 fixture；诚实空态不伪闭合
- ✅ D10：模板纯平铺无切换交互；表格/文字黑白可读
- ✅ 权限与埋点：`ReportExportButton` permCode + 付费闸门原样保留；`data-report-download` 等标记保留
- ⚠️ 依赖：jspdf 新增（已获监管人书面批准）；PDF 文字不可选中（图片化），天花板已注释
- ✅ 其余报告域零影响（通用视图回退到只读，print CSS 拆除后行为与任务开始前一致）

## 走查修正记录

- **2026-10-24（监管人反馈：报告区域太窄、两侧大量空白、PDF 宽度不够）**：
  - 屏显：`.eval-report-page` 从固定 `794px` 改为 `width: 100%` 撑满分析面板；封面改 `aspect-ratio: 210/297` 保持 A4 比例。
  - PDF：废除「整页等比缩放」（缩放导致每页两侧留白、内容宽度不足），改为**按块边界切片**——内容页截图按 `.eval-report-block` 边界切多页，每页渲染到严格 A4 比例白底画布后满宽嵌入 PDF；单块超页高时块内硬切（`ponytail:` 已注释天花板）。
  - 验证：vue-tsc exit 0、selfcheck ok、eslint 0。
- **2026-10-24（监管人反馈：封面大面积空白）**：上一轮给封面加的 `aspect-ratio: 210/297` 把封面强制撑成整页 A4 高度（1079px 宽 → 1526px 高），内容只占顶部几百像素。改为紧凑自适应高度（`padding-top: 8px`）；PDF 侧封面页由 `renderSliceCanvas` 的 A4 比例白底画布天然渲染（内容在顶、下方留白 = 标准报告封面页形态）。

## 验收结论（2026-10-24）

监管人走查通过（「效果先这样」），授权 commit + push dev。走查过程含两轮反馈修正（见走查修正记录）。

| 项 | 值 |
|----|-----|
| 仓 / 分支 | `lumen-ui-topic` @ `origin/dev` |
| commit | `2df95de`（rebase 后最终 hash；本地原 `2bfbde0`，远端新提交 rebase 变更） |
| push | `6d145b9..2df95de  dev -> dev` ✅ |
| 授权方式 | 聊天明示（人工验收闸门放行） |
| 未入库遗留 | `.env.development`、`src/assets/layout/layout.css`（上轮会话遗留，非本任务，仍在本地工作区） |

## 开放项 / 后续

1. ~~人工验收~~ 已完成（2026-10-24 走查通过，见验收结论）。
2. `.env.development`（USE_MOCK=false + 真实网关地址）与 `layout.css`（门户嵌底色）为上一轮会话遗留本地改动，非本任务产物，未随本次提交入库，仍留在本地工作区待对应任务收口。
3. business/competitiveness 模式复用同一 build 函数与模板（顺带获益），建议走查确认观感。
4. 其余 6 个报告域若要升级到分块模板 v2，按同模式另立叶。
5. 若甲方要求 PDF 文字可选中/文件级归档，升级路径：服务端生成（ENT-JAVA-ANALYSIS-ARTIFACT 已有底子）。

## 续交付（2026-10-31）— 块式 HTML 报告扩域 + 服务端 PDF 存储 + API 导出

### 范围

| 项 | 实现 |
|----|------|
| 前端块式报告 | 评估/风险/引育/重点企业/深圳现状统一 `BlockReportReader` + `EnterpriseBlockReportView`；文案去提示词泄漏；产业链展示名；引育「推荐补充信息」表；分布图与排名图分块修复 |
| Java PDF 模板 | 非评估三模式走 `analysis/block-report.html` + `BlockReportModel`（KPI/文字/CSS 条形/表）；评估仍 `analysis/eval/{technology,business,competitiveness}` |
| PDF 存储与二次下载 | 沿用 `ArtifactExecutionServiceImpl` 上传 MinIO + 子任务 `resultAssetId`；`createAnalysisArtifactTask` 幂等复用已成功产物 |
| HTML 报告页 PDF | `reportPdfExport.ts`：`VITE_REPORT_PDF_EXPORT=api\|html2canvas`（默认 api）；`exportBlockReportPdf` 保留；有父任务时 API 轮询 + `analysisTaskAssetDownload`；无任务（重点/深圳）回退 html2canvas |
| 环境变量 | `.env.development` / `.env.production` / `env.d.ts` 同步 `VITE_REPORT_PDF_EXPORT=api` |

### 验证

- `node src/components/report/reportExport.selfcheck.mjs`：ok
- Java `ArtifactRenderServiceImplTest.rendersRecommendAsBlockReport`：本机未装 Maven，CI 待绿
- 浏览器走查：引育分布图/排名图、深圳产业链名称（会话内已验）

### 架构合规（续）

- ✅ D12：HTML 报告 PDF 仅调 topic 分析产物接口，无 demo 直连
- ✅ 权限：`ReportExportButton` / `useBlockReportExport` 闸门不变
- ⚠️ 服务端块式 PDF 与前端 ECharts 雷达/饼图不完全同构（条形用 CSS；章节来自快照 sections + export 表）

### 三仓提交（2026-10-31 push dev）

| 仓 | 分支 | commit |
|----|------|--------|
| lumen-ui-topic | dev | `7acdc3c` feat(report): 块式 HTML 报告扩域 + API PDF 导出 |
| lumen-svc-platform | dev | `39e4cd7` feat(artifact): 块式 PDF 模板 block-report |
| gkx-orchestration | dev | `e89de664` docs(handoff): FE-ENT-EVAL-REPORT-REAL-L01 + registry |

## Cost

| 字段 | 值 |
|-----|-----|
| actual_tokens | ≈380000（含 v2 重开 + 2026-10-31 扩域/Java/PDF API） |
| model_used | Composer（Cursor） |
| actual_cost | ≈$3.8 |
| cost_warn | green |
