# 影响力评价与应用反馈（M_INNOV_DS_25_SOFTSCI_012）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_25_SOFTSCI_012 |
| 指标名称 | 影响力评价与应用反馈 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 科技专题战略分析 |
| 三级模块 | 软科学课题分析 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对软科学课题从课题能级、成果影响、应用反馈综合评分，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：课题能级/成果影响/应用反馈。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 课题能级 |  | 资助金额与项目级别。 | 0.5×norm(funded_amount)+0.5×norm(级别映射) | dwd_zh_project(id, funded_amount, project_level, approval_year) — 资助金额,项目级别,立项年 |
| 成果影响 |  | 论文、专利与奖项产出件数。 | 期刊+会议+专利+奖项件数 | dwd_zh_project_output(id, journal_articles_count, conference_papers_count, patents_count, awards_count, total_outputs) — 期刊文章,会议论文,专利,奖项,总产出 |
| 应用反馈 |  | 结题摘要与报告产出。 | I(结题摘要非空)+reports_count | dwd_zh_project(id, final_report_abstract) — 结题摘要；dwd_zh_project_output(id, reports_count) — 报告数量 |

## 源表字段

dwd_zh_project(id, title, discipline, keywords, fund_category, funded_amount, project_level, funded_institution, funded_province, final_report_abstract, approval_year) — 软科学入集,资助,级别,机构对齐,结题摘要,立项年；dwd_zh_project_output(id, journal_articles_count, conference_papers_count, patents_count, awards_count, reports_count, total_outputs) — 课题产出对齐,论文专利奖项报告；dwd_org_base_info(org_id, name_cn, city, province) — 受资助机构名称对齐,空间过滤

## 待建字段

无

## 备注

OPEN draft 身份。05 无软科学课题影响力专叶，不发明 M_*，见 DS25-D12 / DS25-B04。04-科技专题服务系统 软科学课题影响力与应用反馈，参考权威机构方案。软科学课题实体评价数据源标准缺失，需郭经理与数据采购方沟通。
