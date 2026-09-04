# 创新价值（M_INNOV_DS_04_ACHIEVE_OVERVIEW_001）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_04_ACHIEVE_OVERVIEW_001 |
| 指标名称 | 创新价值 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_ACHIEVE_VALUE-创新价值

## 计算逻辑说明

同M_INNOV_ACHIEVE_VALUE-创新价值

## 源表字段

dwd_patent(pn, value, first_applicant_name, apdt_year) — 专利去重,专利价值,申请人对齐,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_zh_paper(id, publication_id, download_num, cover_year_start) — 中文论文去重,挂刊,下载量,发表年；dwd_en_paper(id, publication_id, cover_year_start) — 英文论文去重,挂刊,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐；dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐；dwd_zh_journal(publication_id, impact_score, jn_zone) — 中文刊影响指数,分区；dwd_en_journal(publication_id, impact_score, jn_zone) — 英文刊影响指数,分区；dwd_zh_project(id, funded_amount, final_report_abstract, project_level, approval_year, funded_province) — 国内项目资助,结题,级别,立项年,资助省；dwd_en_project(id, funded_amount, final_report_abstract, project_level, approval_year) — 国外项目资助,结题,级别,立项年；dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_ACHIEVE_VALUE（创新价值）。05 无全球成果价值专叶。见 AOV-D01 / AOV-B01。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
