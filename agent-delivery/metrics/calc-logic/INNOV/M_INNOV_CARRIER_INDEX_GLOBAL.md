# 创新载体创新能力指数（M_INNOV_CARRIER_INDEX_GLOBAL）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CARRIER_INDEX_GLOBAL |
| 指标名称 | 创新载体创新能力指数 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

创新载体（企业/科研机构）的综合创新能力。从创新资源、创新产出、创新能力综合评分，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：创新资源 / 创新产出 / 创新能力。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 创新资源 |  | 研发人力与经营规模。 | 0.5×研发人员 + 0.5×营收（研发人员优先取年报研发人员，没有则用从业人数） | dwd_org_annual_financial_info(org_id, year, development_employee, employees_number, operating_revenue) — 年报研发人员,从业人数,营收；dwd_org_stock_finance_info(org_id, occur_period, operating_revenue) — 上市营收 |
| 创新产出 |  | 专利与论文产出规模。 | 专利去重件数 + 中英文论文去重件数（名称对齐） | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,统计年；dwd_en_paper(id, cover_year_start) — 英文论文,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 创新能力 |  | 科技型资质与授权专利。 | 0.5×高企标签 + 0.5×授权专利去重件数 | dwd_org_tech_tag(org_id, org_tag) — 高新技术等标签；dwd_patent(pn, first_applicant_name, granted_number, apdt_year) — 授权号,申请人对齐,申请年 |

## 源表字段

dwd_org_base_info(org_id, name_cn, org_type, reg_status, province, city) — 国内载体入集,名称对齐,存续过滤,空间筛选；dwd_research_institute_base_info(org_id, name_cn, org_type, reg_status, province, city) — 科研机构入集,名称对齐,存续过滤；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外载体入集,名称对齐,国家城市；dwd_org_annual_financial_info(org_id, year, development_employee, employees_number, operating_revenue) — 年报研发人员,从业人数,营收；dwd_org_stock_finance_info(org_id, occur_period, operating_revenue) — 上市营收；dwd_org_tech_tag(org_id, org_tag) — 高新技术等科技型标签；dwd_patent(pn, first_applicant_name, granted_number, apdt_year) — 专利去重,申请人对齐,授权号,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年；dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|全球创新监测.md|序号 73「基于数据模型对各创新载体的创新成果数据进行计算，生成创新能力指数，用户可查看指数计算方法和权重设置」。对象=创新载体（企业/机构），宇宙=全球。不是城市排名、不是深圳载体价值排名。参考权威机构方案。
