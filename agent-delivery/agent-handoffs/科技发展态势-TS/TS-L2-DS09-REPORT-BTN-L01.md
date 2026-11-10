# TS-L2-DS09-REPORT-BTN-L01 — DS09 三页签报告/建议按钮接后端（184/195/190）

> 交付人：agent:zcode ｜ 日期：2026-11-10 ｜ Epic：E-FE-TECH-SITUATION
> 触发：用户逐按钮排查 DS09 三页签「生成报告/下载报告/查看证据/生成战略建议/查看建议/方案对比/资源详情」的接口响应与需规符合性后，要求「按最符合需规的方法优化，要求调用后端接口」。

## 1. 背景（排查结论 → 改造范围）

| 按钮 | 排查结论（改造前） | 本单动作 |
|---|---|---|
| 184 生成报告（OverviewTab） | 纯前端开弹窗，正文 FE 现拼；契约 report_meta 已定义但 FE 未消费（生成时间用 new Date()） | real 轨道点击先 GET direction-warnings 取最新数据 + report_meta，再开弹窗；报告构建消费 report_meta（生成时间/等级计数服务端口径） |
| 184 下载 Word | 走任务中心但 filter 只传 title，后端恒全量渲染 | filter 透传 field（单标签；复合级联标签走全量，见 §4 delta-3） |
| 195 生成报告（ResearchTab） | 同 184：FE 硬编码模板（含写死「华为、腾讯」） | real 轨道点击先 GET research-analysis；弹窗正文改消费 report_export.templates[] 模板行（与导出 Word 同源）；content_key 改读下发值 |
| 195 行内下载报告 | 全量报告，无行筛选、无 report_ref 回填（契约 §2 明文未实现） | filter 透传 row_id+field；job_id 回填行 report_ref（会话内展示任务号） |
| 195 查看证据 | 误开整份报告弹窗 | 改行级证据弹窗（evidence/regional_insight/action 行数据） |
| 195 生成战略建议 | demo 硬编码三节（契约 G-B3 方案 A：三节文案 FE 按模板渲染） | templates[] 可用时按模板行渲染，缺省回落 demo 冻结 |
| 190 查看建议/方案对比/资源详情（KeyAreaTab） | 三按钮同开同一弹窗；契约裁定 FE Modal 非端点（KEY-API delta-3） | 三视图分流（advice/compare/resource），打开时按需刷新 key-areas（既有端点，1 读 0 写不破约） |

## 2. 改动清单

### 后端 lumen-svc-platform（gkxlumen-display）
- `PlanningQueryService.researchAnalysis()`：`report_export` 块新增 `templates[]`（section_key/section_label/template_text/is_system/sort_no，sort_no 保序、缺行跳过不造文案）——FE 弹窗与导出 Word 文案同源的物理载体。
- `ExportJobService.create()`：
  - 184 通道 `filter.field`/`filter.warning_level` 透传 `directionWarnings(field, warningLevel)`；warning_level 出枚举 → 400（与读端点同语义）。
  - 195 通道 `filter.row_id`（精确）/`filter.field`（包含语义）过滤 `intelligence_rows` 后渲染；row_id 非整数 → 400；未传筛选 = 全量（兼容旧调用）；筛选零行 = 诚实空报告（rowCount 0）。
- 测试：`ExportJobServiceTest`（+directionWarningReportAppliesFieldFilter / +researchReportAppliesRowFilter）、`PlanningQueryServiceTest`（templates[] 下发断言）。

### 前端 lumen-ui-science-pc（src/views/situation/tech-development-plan + api/types）
- api 层：`DirectionWarningsResp.report_meta` / `ResearchAnalysisResp.report_export` 映射进 dataset（`directionWarningReportMeta` / `researchReportExport`，缺省 null = demo 冻结轨道）；新增三个单块刷新函数 `refreshDirectionWarningBlock` / `refreshResearchReportBlock` / `refreshKeyAreaPlanBlock`（既有 GET 端点，无新面）。
- model：`buildDirectionMonitorReport` 增 reportMeta 参（服务端口径优先）；`buildResearchIntelligenceReport` 重构为 sections 结构 + 模板行轨道（占位符键集与 BE `ExportReportRenderer.PLACEHOLDER` 一致，缺值落「—」）；新增 `renderStrategySections`（196 三节模板渲染）；报告 bodyHtml 统一 `escapeHtml`（对齐 BE esc()）；`ReportExportOptions.filter` 透传 + `downloadHtmlAsWord` real 轨道返回 `Promise<job_id|null>`。
- OverviewTab：生成报告按钮 loading + 按需刷新 + 回落提示；Word 导出 filter（单标签 field，复合标签全量）。
- ResearchTab：生成报告按需刷新；弹窗 sections 通用渲染 + caliber 口径行；行级下载 row_id/field + job_id 回填（`rowReportRefs`，行下任务号标签）；查看证据行级弹窗；战略弹窗双轨道；contentKey 读 `dataset.researchReportExport`。
- KeyAreaTab：三按钮分流 advice（原方案模拟结果）/ compare（三方案 a-table 对照）/ resource（载体类型 + 区县载体规模 TOP + 土地用途样例，均 key-areas 块行）；打开时按需刷新 + 失败回落提示。
- styles：`.tzp-research-row-jobref`。

### 种子/数据侧 gkx-orchestration
- `scripts/ts_plan_seed/seed_ts_plan.py`：`advantage_section` 劣势文案「与华为、腾讯等高重叠主体相比」→「与{compare}等高重叠主体相比」（BE researchVars 已填 compare，渲染器零改动）。
- ⚠️ **需 ops 重灌** `ts_plan_research_report_template`（仅该行文案变更；未重灌前线上仍显旧文案，FE/BE 行为不破）。

## 3. 验证

- FE：`npm run type-check` ✅；`techDevelopmentPlan.test.mjs` ✅；eslint 改动文件零新增错误（存量 4 个基线错误不变：index.vue multi-word / unwrap / buildCarrierPopupHtml / PlanningResourcePackage 未用）。
- BE：`mvn -pl gkxlumen-display test` 全量 **BUILD SUCCESS**（含新增筛选用例 17+ 全绿）。
- mock 轨道：所有新逻辑经 `USE_MOCK` 门控，demo 冻结行为不变（生成报告直接开弹窗、Blob 下载、无刷新请求）。

## 4. 契约 delta 注记（待架构会签，agent 不擅改 SDD）

1. **OV-API §2.7**：report_meta FE 消费落地（原契约已定义、无 FE 行为变更）；export filter.field 透传属契约「行筛选参数」语义在 184 通道的自然延伸——建议 §2.7 边界补一句「建任务 filter 可携 field/warning_level」。
2. **RES-API §2**：`report_export` 块**新增 `templates[]` 子字段**（additive；原 content_key/default_format/template_source 不变）——弹窗与 Word 同源的载体，建议批 5 会签补录；「行筛选参数 + job_id 回填 report_ref」为契约原文落地，无变更。
3. **复合级联标签 184 导出**：technologyField 复合串（「A / B」「A、B等N项」）后端 field 精确匹配无法承接 → FE 该态走全量导出（不导空报告）；若要行级一致需后端 field 支持列表语义，待 M0 拍板。
4. **190 按钮语义**：KEY-API delta-3（FE Modal 非端点）保持；三视图分流 + 按需刷新均在「1 读 0 写」内；按钮行为目标仍 FE 派生（文案列已有表行携带），behavior 列化未做（可选优化）。

## 5. 遗留 / 并行注记

- PDF 导出维持浏览器打印（两分册契约明文允许），不受 184 闸门约束——契约 §3「报告导出入口禁用」的字面争议沿袭上单注记，未改。
- advantage_section {compare} 占位符化需 DB 重灌（§2 数据侧⚠️）。
- 实施期间并行会话提交 `143b369`（方向预警产业口径匹配，wangzizhen）先落 dev；本单在其上适配（monitorReportExportFilter 复用 cascadeLabelParts），无冲突。
- FE 仓 4 个存量 lint 错误（§3）建议另开 chore 单清理。

## 6. DoD 对照

- [x] 生成报告/下载报告/查看证据/生成战略建议/查看建议/方案对比/资源详情全部经后端数据驱动（real 轨道；mock 轨道 demo 冻结不变）
- [x] 195 行筛选参数 + job_id 回填 report_ref 契约落地
- [x] 弹窗与导出 Word 文案同源（templates[]）
- [x] FE type-check / FE test / BE 全量测试绿
- [x] 本 handoff + 三仓本地提交（未 push，待用户确认）


## 7. 追加修复（2026-11-10 下午 · 用户线上截图反馈「生成报告还是不符合」）

线上截图（比对主体=字节跳动、领域=合成生物学）暴露三缺口 + 一个存量 BE 缺陷：

1. **截图走 demo 兜底轨道的根因**：部署包验证含新代码（chunk `index-GKt1R39S.js` 含「口径说明/researchReportExport」标记）→ 用户浏览器是部署前打开的旧 SPA 会话，**强刷即切新代码**。非部署问题。
2. **overlap_text 不跟随选中比对主体**：报告构建改走 G-B4 真值对口径——`getPairOverlapCompute(target, compare, matrix, timeScope, factor, field)`（真值对 → 复算值带口径描述；无对 → 「—（暂无重叠数据）」诚实空）；基准清单仅保留给 cooperation 节 `benchmark_list`（契约定义源）。
3. **发展建议空节**：领域过滤后无情报行 → 节内渲染诚实说明「当前研究领域（X）暂无情报行，发展建议待数据接入后生成」，两轨道一致，不再渲染空标题。
4. **Word 与弹窗变量级同源**：`buildResearchIntelligenceReport` 返回 `vars` 快照，导出建任务经 `filter.vars` 透传；BE 渲染器新增 varOverrides 合并（白名单=15 占位符键、值截 500 字符、esc() 照常转义、非白名单静默忽略、非字符串值 400）。行级下载按该行覆盖 action/regional_insight/field + 映射方案三元组。
5. **存量缺陷（本次顺修）**：种子模板 `advantage_section` 用 `{catching_score}`，但 BE `PLACEHOLDER` 正则与 `researchVars` 均无此键 → 后端 Word 输出字面 `{catching_score}`。已补：正则加键 + catching 等级卡现算（缺卡落「—」）。

验证：BE `gkxlumen-display -am test` 全量 BUILD SUCCESS（新增 researchReportAppliesVarOverrides：白名单覆盖/转义/非白名单忽略/非字符串 400）；FE type-check + techDevelopmentPlan.test.mjs 绿；eslint 零新增。

契约注记（待会签）：RES-API §2 补「filter.vars 变量覆盖（白名单=占位符键集）」与 overlap_text 真值对/复算口径说明。
