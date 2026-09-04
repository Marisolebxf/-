# 监测趋势预测（M_INNOV_DS_FACTORS_018）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_FACTORS_018 |
| 指标名称 | 监测趋势预测 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_FACTOR_FORECAST-监测趋势预测

## 计算逻辑说明

同M_INNOV_FACTOR_FORECAST-监测趋势预测

## 源表字段

dwd_zh_journal(publication_id, publication_type) — 会议/期刊入集,出版物类型；dwd_en_journal(publication_id, publication_type) — 会议/期刊入集,出版物类型；dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文论文去重,会议/期刊区分,发表年；dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文论文去重,会议/期刊区分,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐；dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐；dwd_zh_project(id, approval_year, funded_province) — 国内项目去重,立项年,资助省；dwd_en_project(id, approval_year) — 国外项目去重,立项年；dwd_patent(pn, apdt_year, first_applicant_name) — 专利去重,申请年,申请人对齐；dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_FACTOR_FORECAST（监测趋势预测）。功能要要素趋势预测，05 仅有区域指数趋势报告。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
