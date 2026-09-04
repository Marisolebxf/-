# 创新热点区域识别（M_INNOV_DS_05_GBA_ACHIEVE_004）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_05_GBA_ACHIEVE_004 |
| 指标名称 | 创新热点区域识别 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_GBA_HOTSPOT-湾区创新热点区域

## 计算逻辑说明

同M_INNOV_GBA_HOTSPOT-湾区创新热点区域

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, addr_lng, addr_lat) — 湾区机构入集,区县主键,名称对齐,落图；dwd_research_institute_base_info(org_id, name_cn, city, province, area, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集；dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC类型,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_GBA_HOTSPOT（湾区创新热点区域）。05 无湾区地理热点区域专叶。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
