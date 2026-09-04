# 科技人才流动监控（M_INNOV_DS_09_COMPREHENSIVE_006）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_09_COMPREHENSIVE_006 |
| 指标名称 | 科技人才流动监控 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_PLAN_TALENT_FLOW-科技人才流动（产业界↔学术界）

## 计算逻辑说明

同M_INNOV_PLAN_TALENT_FLOW-科技人才流动（产业界↔学术界）

## 源表字段

dwd_scholar(scholar_id, name_zh, name_en, scholar_org_name_zh, h_index, paper_nums) — 学者入集,H指数；dwd_scholar_talent_flag(scholar_id, academician) — 院士标识；dwd_scholar_work_experience(scholar_id, org_name_zh, org_name_en, start_time, end_time, seq_no, is_current, status) — 工作经历,任职机构,起止年；dwd_org_base_info(org_id, name_cn, industry, industry_l1_code, city, province, reg_status) — 工商主体名称对齐,行业,空间；dwd_research_institute_base_info(org_id, name_cn, name_en) — 科研机构名称对齐；dwd_forg_university_org_info(name_std, name_alias, org_type) — 海外高校名称对齐

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_PLAN_TALENT_FLOW（科技人才流动（产业界↔学术界））。对照人才 157 对不上（缺学界流动+预警）。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
