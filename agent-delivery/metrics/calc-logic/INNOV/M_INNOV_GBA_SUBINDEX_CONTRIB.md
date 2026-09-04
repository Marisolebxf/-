# 子指标贡献度（M_INNOV_GBA_SUBINDEX_CONTRIB）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_SUBINDEX_CONTRIB |
| 指标名称 | 子指标贡献度 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q133 / Q-MO-DS05-02 |

## 口径定义

四子指数对总指数的结构占比，取值 0—1，四维合计为 1。

## 计算逻辑说明

四维指数各除以四维合计。资源 / 机构 / 机制 / 环境。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 创新资源贡献 |  | 资源指数占总指数结构的比例。 | res_index / 四维合计 | 取 M_INNOV_GBA_RES_INDEX — 资源指数 |
| 创新机构贡献 |  | 机构指数占总指数结构的比例。 | org_index / 四维合计 | 取 M_INNOV_GBA_ORG_INDEX — 机构指数 |
| 创新机制贡献 |  | 机制指数占总指数结构的比例。 | mech_index / 四维合计 | 取 M_INNOV_GBA_MECH_INDEX — 机制指数 |
| 创新环境贡献 |  | 环境指数占总指数结构的比例。 | env_index / 四维合计 | 取 M_INNOV_GBA_ENV_INDEX — 环境指数 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 96「用户可查看各子指标的数值和贡献度」。四子对总指数的贡献（xlsx 48）。禁止 reuse M_SYNTH_VIT_WEIGHT。
