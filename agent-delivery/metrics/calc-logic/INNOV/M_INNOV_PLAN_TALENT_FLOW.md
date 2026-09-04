# 科技人才流动（产业界↔学术界）（M_INNOV_PLAN_TALENT_FLOW）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_TALENT_FLOW |
| 指标名称 | 科技人才流动（产业界↔学术界） |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q150 / Q-MO-DS09-02 |

## 口径定义

核心技术人才跨界流动。任职性质由机构名对齐现表判定，不另建性质/方向字段。只计学术界↔产业界。

## 计算逻辑说明

核心技术人才入集。按工作经历相邻任职性质变化识别流动。二维：学界→产业 / 产业→学界。近窗相对基线增速超阈预警。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 学界→产业 |  | 学术界转入产业界的去重学者数。 | COUNT(DISTINCT scholar_id) WHERE 旧=学术 AND 新=产业 | dwd_scholar_work_experience(scholar_id, org_name_zh, org_name_en, start_time, seq_no, is_current, status) — 工作经历；dwd_org_base_info(org_id, name_cn, industry, industry_l1_code, city, province) — 工商主体对齐；dwd_research_institute_base_info(org_id, name_cn, name_en) — 科研机构对齐；dwd_forg_university_org_info(name_std, name_alias, org_type) — 海外高校对齐 |
| 产业→学界 |  | 产业界转入学术界的去重学者数。 | COUNT(DISTINCT scholar_id) WHERE 旧=产业 AND 新=学术 | dwd_scholar_work_experience(scholar_id, org_name_zh, org_name_en, start_time, seq_no, is_current, status) — 工作经历；dwd_org_base_info(org_id, name_cn, industry, industry_l1_code, city, province) — 工商主体对齐；dwd_research_institute_base_info(org_id, name_cn, name_en) — 科研机构对齐；dwd_forg_university_org_info(name_std, name_alias, org_type) — 海外高校对齐 |
| 流动预警 |  | 近窗流动人数相对基线突增。 | burst≥1为2；burst≥0.5为1；否则0 | 上两年序列 — 近窗相对基线 |

## 源表字段

dwd_scholar(scholar_id, name_zh, name_en, scholar_org_name_zh, h_index, paper_nums) — 学者入集,H指数；dwd_scholar_talent_flag(scholar_id, academician) — 院士标识；dwd_scholar_work_experience(scholar_id, org_name_zh, org_name_en, start_time, end_time, seq_no, is_current, status) — 工作经历,任职机构,起止年；dwd_org_base_info(org_id, name_cn, industry, industry_l1_code, city, province, reg_status) — 工商主体名称对齐,行业,空间；dwd_research_institute_base_info(org_id, name_cn, name_en) — 科研机构名称对齐；dwd_forg_university_org_info(name_std, name_alias, org_type) — 海外高校名称对齐

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技发展规划.md|序号 182「对核心技术人才信息进行全面监控，用户可查看科技人才在产业界和学术界的流动情况，提供人才流动趋势分析和预警功能」。对象≠ M_TALENT_FLOW_TRACK（专题区域/行业流入流出），≠ 人才 05 seq 157。参考权威机构方案。
