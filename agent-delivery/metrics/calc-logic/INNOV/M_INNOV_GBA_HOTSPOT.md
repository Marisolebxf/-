# 湾区创新热点区域（M_INNOV_GBA_HOTSPOT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_HOTSPOT |
| 指标名称 | 湾区创新热点区域 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

识别湾区区县中成果更密的区域，给出创新密度、主要类型与是否热点。

## 计算逻辑说明

按区县汇总专利、论文、项目。输出创新密度、主要创新类型与热点标签。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 创新密度 |  | 区县单位机构的成果件数。 | (专利数 + 论文数 + 项目数) / 存续机构数 | dwd_org_base_info(org_id, name_cn, city, province, area, reg_status) — 机构入集,区县主键；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年 |
| 主要创新类型 |  | 该区县成果件数最大的类型。 | 专利 / 论文 / 项目取最大（并列专利优先） | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利件数,IPC众数；dwd_zh_paper(id, cover_year_start) — 中文论文件数；dwd_en_paper(id, cover_year_start) — 英文论文件数；dwd_zh_project(id, funded_institution, approval_year) — 项目件数 |
| 热点标签 |  | 密度是否达到本批高位。 | 密度 ≥ P70 且机构数≥3 记 1 | 同上密度结果 — 分位判定 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, addr_lng, addr_lat) — 湾区机构入集,区县主键,名称对齐,落图；dwd_research_institute_base_info(org_id, name_cn, city, province, area, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC类型,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|湾区创新监测.md|序号 92「自动识别并标注大湾区内的创新热点区域，用户可查看热点区域的创新密度、主要创新类型等详细信息」。密度与类型共核，不另造 CNT ID。参考权威机构方案。
