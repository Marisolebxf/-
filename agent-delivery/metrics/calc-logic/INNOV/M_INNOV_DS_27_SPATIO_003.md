# 热点区域自动识别与预警（M_INNOV_DS_27_SPATIO_003）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_27_SPATIO_003 |
| 指标名称 | 热点区域自动识别与预警 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 科技专题战略分析 |
| 三级模块 | 空间布局分析 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

按区县识别创新热点并给出预警等级。

## 计算逻辑说明

按区县识别创新热点并给出预警等级。区域主键就是 `city`+`area`，创新密度 = (专利+论文+项目) / 机构数；密度 ≥ P70且机构数≥3为热点；预警：热点且近窗突增 ≥1 为 2，热点或突增 ≥0.5 为 1。

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, addr_lng, addr_lat) — 机构入集,区县主键,名称对齐,落图；dwd_research_institute_base_info(org_id, name_cn, city, province, area, reg_status) — 科研机构入集；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年

## 待建字段

无

## 备注

OPEN draft 身份。禁止改挂 134/182，无 also_in，不发明 M_*，见 SPATIO-D03。04-科技专题服务系统 空间热点区域自动识别与预警，参考权威机构方案。统计窗口与对象范围待 T0-X 核对。
