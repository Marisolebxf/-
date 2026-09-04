# 区域科技创新竞争力水平（M_INNOV_KEYD_COMPETITIVENESS）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_KEYD_COMPETITIVENESS |
| 指标名称 | 区域科技创新竞争力水平 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

规划页选定区域的竞争力水平分值，取值 0—100。对象=区域（未选默认深圳）。三维：创新产出、创新主体、政策供给。

## 计算逻辑说明

选定区域入集。需求未列竞争力指标体系，二级按区域创新能力文献。采用加权平均，三维：创新产出 / 创新主体 / 政策供给。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 创新产出 |  | 专利与论文去重件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 创新主体 |  | 存续机构与高企。 | 0.5×norm(机构数)+0.5×norm(高企数) | dwd_org_base_info(org_id, city, province, reg_status) — 存续机构；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 |
| 政策供给 |  | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, province, theme, status, expire_date, publish_year) — 有效政策 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_policy_base(id, city, province, status, expire_date, publish_year) — 有效政策件数；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技发展规划.md|竞争力水平与潜力评估 · 序号 186(评估区域科技创新的竞争力水平和潜力情况)。需求未列竞争力指标体系，二级按《中国区域创新能力评价报告》收口为创新产出/创新主体/政策供给，参考权威机构方案。
