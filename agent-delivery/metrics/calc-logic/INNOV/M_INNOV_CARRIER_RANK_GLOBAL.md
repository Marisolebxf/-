# 创新载体多维度排名（M_INNOV_CARRIER_RANK_GLOBAL）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CARRIER_RANK_GLOBAL |
| 指标名称 | 创新载体多维度排名 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

对全球入集载体按与 M_INNOV_CARRIER_INDEX_GLOBAL 同一套指数排序。对象=载体，可切总体 / 领域 / 地区三个名次宇宙。名次从 1 起。

## 计算逻辑说明

存续载体入集。指数同创新能力指数三维：创新资源 / 创新产出 / 创新能力。总体、领域、地区三个宇宙分别降序排名。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 总体排名 |  | 全部载体按指数降序的名次。 | RANK(index_score) 全局 | 同 M_INNOV_CARRIER_INDEX_GLOBAL — 创新能力指数 |
| 领域排名 |  | 同 IPC4 有专利的载体宇宙内名次。 | RANK(index_score) 领域内 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 申请人对齐,IPC领域 |
| 地区排名 |  | 同城（或同国家）载体宇宙内名次。 | RANK(index_score) 地区内 | dwd_org_base_info(org_id, city, province) — 地区切宇宙；dwd_forg_base_info(org_id, country, city) — 海外地区 |

## 源表字段

dwd_org_base_info(org_id, name_cn, org_type, reg_status, province, city) — 国内载体入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, org_type, reg_status, province, city) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外载体入集；dwd_org_annual_financial_info(org_id, year, development_employee, employees_number, operating_revenue) — 年报研发人员,从业人数,营收；dwd_org_stock_finance_info(org_id, occur_period, operating_revenue) — 上市营收；dwd_org_tech_tag(org_id, org_tag) — 高新技术等标签；dwd_patent(pn, first_applicant_name, granted_number, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,授权号,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|全球创新监测.md|多维度排名展示 · 序号 74(包括总体排名、领域排名、地区排名)
