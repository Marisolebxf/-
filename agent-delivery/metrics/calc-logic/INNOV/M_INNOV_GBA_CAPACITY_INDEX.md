# 粤港澳大湾区创新能力指标（M_INNOV_GBA_CAPACITY_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_CAPACITY_INDEX |
| 指标名称 | 粤港澳大湾区创新能力指标 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q133 / Q-MO-DS05-02 |

## 口径定义

湾区 11 城由资源、机构、机制、环境四子指数等权合成，取值 0—100。

## 计算逻辑说明

采用加权平均。四维：创新资源 / 创新机构 / 创新机制 / 创新环境。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 创新资源指数 |  | 专利、论文与研发投入。 | 取 M_INNOV_GBA_RES_INDEX | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 |
| 创新机构指数 |  | 载体数量、产出与科技型机构。 | 取 M_INNOV_GBA_ORG_INDEX | dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 湾区机构；dwd_research_institute_base_info(org_id, city, province, reg_status) — 科研院所；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_patent(pn, first_applicant_name, apdt_year) — 专利产出；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 创新机制指数 |  | 联合专利、合作项目与转化。 | 取 M_INNOV_GBA_MECH_INDEX | dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 共申请人；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移 |
| 创新环境指数 |  | 政策供给、主题覆盖与高企密度。 | 取 M_INNOV_GBA_ENV_INDEX | dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_org_base_info(org_id, city, province, reg_status) — 高企分母 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_tech_tag(org_id, org_tag) — 高新技术等科技型标签；dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 94「通过预设算法模型对大湾区的创新资源、创新机构、创新机制、创新环境等因素进行综合分析，实时计算出粤港澳大湾区创新能力指标」；序号 96「将创新能力指标分解为多个子指标（如创新资源指数、创新机构指数、创新机制指数、创新环境指数）」。对象=湾区（xlsx 45 误写「城市」不改对象）。口径≠ M_SYNTH_VIT_INDEX。权重待 Q-MO-DS05-02。
