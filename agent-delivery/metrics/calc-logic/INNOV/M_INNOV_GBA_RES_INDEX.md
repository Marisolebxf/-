# 创新资源指数（M_INNOV_GBA_RES_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_RES_INDEX |
| 指标名称 | 创新资源指数 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q133 / Q-MO-DS05-02 |

## 口径定义

湾区 11 城的专利、论文与研发投入综合分，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：专利资源 / 论文资源 / 研发投入。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 专利资源 |  | 该城专利去重件数。 | COUNT(DISTINCT pn) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 |
| 论文资源 |  | 该城论文去重件数。 | COUNT(DISTINCT 论文id) | dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 研发投入 |  | 上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入,统计期；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 96「分解为多个子指标（如创新资源指数、创新机构指数、创新机制指数、创新环境指数）」。总指数子指标「创新资源」（xlsx 44 / seq 96）。标签「资源」≠ 186「科技」维（Q-MO-DS05-02）。参考权威机构方案。
