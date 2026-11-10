# 科技人才流动监控（M_INNOV_DS_09_COMPREHENSIVE_006）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_09_COMPREHENSIVE_006 |
| 指标名称 | 科技人才流动监控 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 综合发展规划 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_PLAN_TALENT_FLOW（科技人才流动（产业界↔学术界））**。

## 计算逻辑说明

本指标与 **M_INNOV_PLAN_TALENT_FLOW（科技人才流动（产业界↔学术界））** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_scholar(scholar_id, name_zh, name_en, scholar_org_name_zh, h_index, paper_nums) — 学者入集,H指数
- dwd_scholar_talent_flag(scholar_id, academician) — 院士标识
- dwd_scholar_work_experience(scholar_id, org_name_zh, org_name_en, start_time, end_time, seq_no, is_current, status) — 工作经历,任职机构,起止年
- dwd_org_base_info(org_id, name_cn, industry, industry_l1_code, city, province, reg_status) — 工商主体名称对齐,行业,空间
- dwd_research_institute_base_info(org_id, name_cn, name_en) — 科研机构名称对齐
- dwd_forg_university_org_info(name_std, name_alias, org_type) — 海外高校名称对齐

## 待建字段

- 无

## 参考资料

[1]科技人才流动｜全国人民代表大会｜全国人大代表袁玉宇｜推进跨体制人才流动融合｜2025-09-18｜http://www.npc.gov.cn/c2/c30834/202509/t20250918_448081.html.

[2]科技人才流动（产业→学界）｜人民政协网｜全国政协委员李书鹏｜为人才流动“架桥”｜2026-05-13｜http://www.rmzxw.com.cn/c/2026-05-13/3914093.shtml.

[3]科技人才流动｜山东财经大学工商管理学院｜教育部人文社会科学研究一般项目（18YJA630122）；山东省社会科学规划重点研究项目（19BJCJ132019）；山东省社会科学规划优势学科项目（19BYSJ15）｜徐茜，崔霞，罗文卿. 区域科技人才流失风险预警机制研究[J]. 经济与管理评论, 2023, 39(1): 30-41. DOI: 10.13962/j.cnki.37-1486/f.2023.01.003.
