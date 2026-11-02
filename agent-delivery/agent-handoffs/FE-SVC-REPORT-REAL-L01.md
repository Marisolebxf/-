# FE-SVC-REPORT-REAL-L01 · 产业服务链八叶 HTML 报告覆盖结果页 + 下载

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 2026-11-02 会话交付；监管人授权 commit + push dev。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | `buildSvcBlockReportDocument` 八叶派发；`reportBodyText` + `SEGMENT_CN`；覆盖结论拆为三块文本对齐结果页；趋势报告含年度明细表。 |

## 范围与实现

- `SvcAnalysisReportPanel` / 机构三工作区 / 链式短板·图谱·深圳 / 引进·培育工作区：块式 `EnterpriseBlockReportView` + `buildSvcBlockReportDocument`。
- 八叶章节与结果页对齐（覆盖：热力图+覆盖矩阵+服务广度 TOP3+服务深度 TOP 领域+合作建议；趋势：年度趋势+热度研判+主/对比领域年度明细；技术力：排名+技术力得分+雷达；短板：环节+问题环节+环节机构；图谱：双密度 KPI+节点+关系；深圳：城市对比+梯队；引进/培育：名单表+环节中文名，名单说明 stripped Q 编号后为空则省略）。
- 替掉 `serviceDomainReports` 占位「同源摘要」；保留 `buildSvcAnalysisReportDocument` 供 selfcheck。
- 面板「生成报告」仍走 `{leaf}_report` 产物链；阅读页 PDF 按钮默认 html2canvas（`pdfSource=null`）。
- Java 同批：`SvcBlockReportAssembler` + `domain-block-report.html` 与前端块序对齐。

## 验收证据

- `reportExport.selfcheck.mjs` / `svcManualFix.selfcheck.mjs`：ok
- `npx vue-tsc --noEmit`：exit 0
- 本地走查：覆盖结论三块、引进环节中文、趋势明细表、名单无 Q-SVC 编号

## 架构合规自检

- ✅ D12 / 调用链 / USE_MOCK=false 不读 fixture
- ✅ 报告正文清洗与政策同源 `reportBodyText`
- ✅ 图谱报告用全量 payload，不带结果页 clip 控件

## CI/CD（必填）

- 分支：`lumen-ui-topic` @ `dev`
- commit：（见 push 后 hash）

## cost（回填 registry）

| actual_tokens | model_used | actual_cost | cost_warn |
|---------------|------------|-------------|-----------|
| 220000 | composer | 0.55 | false |

## 联调确认

联调通过：八叶 HTML 报告章节与 Java svc `*_report` 块式 PDF 标题一致；遗留 `{leaf}_report` API 下载与 HTML 截图下载并存。
