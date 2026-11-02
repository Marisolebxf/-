# FE-POLICY-REPORT-REAL-L01 · 政策分析三项 HTML 报告覆盖结果板 + 下载

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
| 说明 | 复用 `EnterpriseBlockReportView` + `useBlockReportExport`；无新 npm 依赖；报告正文经 `reportBodyText` 清洗；未跳过 D8/D9 评审门控（块内不传 metricId 进正文）。 |

## 范围与实现

- 三 Host（时序 / 区域对比 / 深圳现状）改为块式报告：`buildPolicyBlockReportDocument` + `EnterpriseBlockReportView`；`view=report` 时隐藏重复 `AnalysisPageHeader`。
- **时序**：时序指标摘要、政策数据自动关联（8 列）、历年发布量、效力层级趋势、支持强度趋势、关键节点、关键节点洞察；解析复用 `policyTimeseriesResult`。
- **区域对比**：区域对比指标摘要、标准化对比矩阵、跨区域政策采集；雷达图 / 热力图 / 差异与竞争优势按顺序平铺三节（阅读页无 Tab）。
- **深圳现状**：支持力度、产业适配性、落地实效性、优化建议；`reportChapters` 额外章节按需追加。
- 下载：默认 `pdfSource=null`，走 html2canvas 导出当前 HTML；权限 `btn:topic:policy:report-export`。
- 接口侧同批交付：`lumen-svc-platform` 块式 PDF 模板 `domain-block-report.html` + `PolicyBlockReportAssembler`（章节与前端对齐），见同 push 中 Java 子集 commit。

## 验收证据

- `node src/components/report/reportExport.selfcheck.mjs`：ok
- `policyTimeseries.selfcheck.mjs` / `policyRegional.selfcheck.mjs` / `policyShenzhen.selfcheck.mjs`：ok
- `npx vue-tsc --noEmit`：exit 0
- 浏览器：政策时序报告 `view=report` 块序与 KPI/表一致；导出 toast 无报错

## 架构合规自检

- ✅ D12：只读父任务结果 payload，无 demo 直连
- ✅ D8/D10：Arco 结果页不变；报告为平铺块、无 Tab
- ✅ 报告正文：无平铺/页签/USE_MOCK/产业编码/Q-GAP 裸编号；空字段为 —
- ✅ 调用链：前端 → 已有 REST，报告不重新跑算法

## CI/CD（必填）

- 分支：`lumen-ui-topic` @ `dev`
- commit：（见 push 后 hash）
- pipeline / K8s：待 CI 绿后 QA 抽验

## cost（回填 registry）

| actual_tokens | model_used | actual_cost | cost_warn |
|---------------|------------|-------------|-----------|
| 180000 | composer | 0.45 | false |

## 联调确认

联调通过：前端块式报告与 Java `policy:report:export` / `domain-block-report` 章节标题一致；PDF 侧图表以表/条形展开。
