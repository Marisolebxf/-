# 创新价值评估（M_INNOV_DS_04_MONITOR_002）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_04_MONITOR_002 |
| 指标名称 | 创新价值评估 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_POINT_VALUE-创新点价值评估

## 计算逻辑说明

同M_INNOV_POINT_VALUE-创新点价值评估

## 源表字段

dwd_patent(pn, keywords, main_classification_ipcr, granted_number, first_applicant_name, apdt_year) — 专利关键词,IPC领域,授权号,申请人对齐,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文论文关键词；dwd_en_paper_classification(id, keywords) — 英文论文关键词；dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数；dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐；dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐；dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_POINT_VALUE（创新点价值评估）。页面要创新点评估算法，05 无对口叶。见 MON-D02 / MON-B02。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
