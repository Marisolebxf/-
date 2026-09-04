# 创新价值排名（M_INNOV_DS_06_CARRIER_003）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_06_CARRIER_003 |
| 指标名称 | 创新价值排名 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 深圳创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_CARRIER_VALUE_RANK_SZ-深圳创新载体创新价值排名

## 计算逻辑说明

同M_INNOV_CARRIER_VALUE_RANK_SZ-深圳创新载体创新价值排名

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 深圳载体入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, org_type, reg_status) — 科研机构入集；dwd_patent(pn, first_applicant_name, value, apdt_year) — 专利去重,申请人对齐,专利价值,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人；dwd_zh_paper(id, publication_id, download_num, cover_year_start) — 中文论文,挂刊,下载量,发表年；dwd_en_paper(id, publication_id, cover_year_start) — 英文论文,挂刊,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_journal(publication_id, impact_score) — 中文刊影响指数；dwd_en_journal(publication_id, impact_score) — 英文刊影响指数；dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_CARRIER_VALUE_RANK_SZ（深圳创新载体创新价值排名）。05 无载体创新价值专叶。also_in: DS-04-CARRIER-RANK。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
