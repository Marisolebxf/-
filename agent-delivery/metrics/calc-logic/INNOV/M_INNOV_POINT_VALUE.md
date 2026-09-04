# 创新点价值评估（M_INNOV_POINT_VALUE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POINT_VALUE |
| 指标名称 | 创新点价值评估 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对已发现创新点从新颖性、影响潜力、成熟度综合评分，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：新颖性 / 影响潜力 / 成熟度。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 新颖性 |  | 词条出现早晚。 | 1 / (1 + 统计年 − 首次出现年) | dwd_patent(pn, keywords, main_classification_ipcr, apdt_year) — 专利关键词,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_paper_classification(id, keywords) — 中文论文关键词；dwd_en_paper_classification(id, keywords) — 英文论文关键词 |
| 影响潜力 |  | 关联成果被引合计。 | 专利被引合计 + 中文论文被引合计 | dwd_patent(pn, keywords, main_classification_ipcr) — 专利对齐词条；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_zh_paper_classification(id, keywords) — 中文论文词条；dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数 |
| 成熟度 |  | 专利授权比例。 | 授权专利数 / 专利数 | dwd_patent(pn, keywords, main_classification_ipcr, granted_number) — 专利词条,授权号 |

## 源表字段

dwd_patent(pn, keywords, main_classification_ipcr, granted_number, first_applicant_name, apdt_year) — 专利关键词,IPC领域,授权号,申请人对齐,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文论文关键词；dwd_en_paper_classification(id, keywords) — 英文论文关键词；dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数；dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐；dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐；dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|全球创新监测.md|序号 79「对发现的创新点进行价值评估，用户可查看评估结果和价值分析报告」。对象=创新点（依赖 M_INNOV_POINT_DISCOVERY），≠ OVERVIEW 成果清单创新价值。参考权威机构方案。
