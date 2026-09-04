# 湾区创新能力优势因素（M_INNOV_GBA_SWOT_STRENGTH）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_SWOT_STRENGTH |
| 指标名称 | 湾区创新能力优势因素 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

从四子指数 12 个分项中识别该城相对领先的优势，给出清单、表现与影响程度。

## 计算逻辑说明

复用四子指数分项。输出优势清单、表现与影响程度。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 优势清单 |  | 该城相对领先的分项。 | 11 城排名 ≤ 3 | 见四子指标分项计算结果 — 入选与展示 |
| 表现 |  | 分项原始值与排名。 | 原始值；rank | 同上 — 展示 |
| 影响程度 |  | 分项在 11 城内的归一值。 | norm(原始值) | 同上 — 影响程度 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 100「识别并分析粤港澳大湾区创新能力的优势因素，如丰富的创新资源、完善的创新机构、高效的创新机制、良好的创新环境」。禁止把 seq 186/188 区域指数优劣清单当 SWOT。库无 SWOT 专叶 → missing 保持。参考权威机构方案。
