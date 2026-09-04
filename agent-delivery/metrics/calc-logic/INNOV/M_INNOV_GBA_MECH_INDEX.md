# 创新机制指数（M_INNOV_GBA_MECH_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_MECH_INDEX |
| 指标名称 | 创新机制指数 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q133 / Q-MO-DS05-02 |

## 口径定义

湾区 11 城联合专利、合作项目与成果转化综合分，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：联合专利 / 合作项目 / 成果转化。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 联合专利 |  | 多申请人专利件数。 | COUNT(DISTINCT 共申请人pn) | dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 共申请人,申请人对齐,申请年 |
| 合作项目 |  | 多机构项目件数。 | COUNT(DISTINCT 多机构项目id) | dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年 |
| 成果转化 |  | 转移专利占专利比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人；dwd_patent(pn, first_applicant_name, apdt_year) — 专利分母,申请人对齐 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 96「分解为多个子指标（如创新资源指数、创新机构指数、创新机制指数、创新环境指数）」。总指数子指标「创新机制」（xlsx 41）。需求未给内部构成维度，参考权威机构方案。
