# 深圳创新载体创新价值排名（M_INNOV_CARRIER_VALUE_RANK_SZ）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CARRIER_VALUE_RANK_SZ |
| 指标名称 | 深圳创新载体创新价值排名 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 深圳创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对深圳存续载体从技术价值、应用价值、潜在影响力综合评分后排名，价值分 0—100。

## 计算逻辑说明

采用加权平均。三维：技术价值 / 应用价值 / 潜在影响力。按价值分降序排名。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 技术价值 |  | 专利价值与期刊影响合计。 | SUM(patent.value)+SUM(impact_score) | dwd_patent(pn, first_applicant_name, value, apdt_year) — 专利价值,申请人对齐,申请年；dwd_zh_paper(id, publication_id, cover_year_start) — 中文论文挂刊,发表年；dwd_en_paper(id, publication_id, cover_year_start) — 英文论文挂刊,发表年；dwd_zh_journal(publication_id, impact_score) — 中文刊影响指数；dwd_en_journal(publication_id, impact_score) — 英文刊影响指数；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 应用价值 |  | 专利转移与论文下载。 | 转移专利数 + SUM(download_num) | dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人；dwd_zh_paper(id, download_num) — 中文论文下载量 |
| 潜在影响力 |  | 专利与论文被引合计。 | SUM(cited_by_nums)+SUM(citation_num) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 深圳载体入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, org_type, reg_status) — 科研机构入集；dwd_patent(pn, first_applicant_name, value, apdt_year) — 专利去重,申请人对齐,专利价值,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人；dwd_zh_paper(id, publication_id, download_num, cover_year_start) — 中文论文,挂刊,下载量,发表年；dwd_en_paper(id, publication_id, cover_year_start) — 英文论文,挂刊,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_journal(publication_id, impact_score) — 中文刊影响指数；dwd_en_journal(publication_id, impact_score) — 英文刊影响指数；dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|深圳创新监测.md|序号 114「展示各载体的创新价值排名，用户可查看不同载体的创新能力和表现，识别高价值创新载体」。对象=深圳创新载体（高校/研究机构/企业/工作室），不是城市/区域/全球载体榜。半成品行56。详情页与筛选键「创新价值」、对比视图消费同一结果。参考权威机构方案。
