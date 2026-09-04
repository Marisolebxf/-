# 创新价值（M_INNOV_ACHIEVE_VALUE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_ACHIEVE_VALUE |
| 指标名称 | 创新价值 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

单条创新成果的综合分值。统计对象为专利、论文、项目，从技术价值、应用价值、潜在影响力综合评分，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：技术价值 / 应用价值 / 潜在影响力（按成果类型分别标准化后等权）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 技术价值 |  | 成果技术含量代理。 | 专利评估价值/论文影响指数/项目资助金额 | dwd_patent(pn, value, apdt_year) — 专利价值,申请年；dwd_zh_journal(publication_id, impact_score) — 中文刊影响指数；dwd_en_journal(publication_id, impact_score) — 英文刊影响指数；dwd_zh_paper(id, publication_id, cover_year_start) — 中文论文挂刊,统计年；dwd_en_paper(id, publication_id, cover_year_start) — 英文论文挂刊,统计年；dwd_zh_project(id, funded_amount, approval_year) — 国内资助金额,立项年；dwd_en_project(id, funded_amount, approval_year) — 国外资助金额,立项年 |
| 应用价值 |  | 成果落地与传播代理。 | 专利转移件数 / 论文下载量 / 项目结题有无（有记 1，无记 0） | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_zh_paper(id, download_num) — 中文论文下载量；dwd_zh_project(id, final_report_abstract) — 国内结题摘要；dwd_en_project(id, final_report_abstract) — 国外结题摘要 |
| 潜在影响力 |  | 成果扩散潜力代理。 | 专利被引次数 / 论文期刊分区映射 / 项目级别映射 | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_zh_journal(publication_id, jn_zone) — 中文刊分区；dwd_en_journal(publication_id, jn_zone) — 英文刊分区；dwd_zh_project(id, project_level) — 国内项目级别；dwd_en_project(id, project_level) — 国外项目级别 |

## 源表字段

dwd_patent(pn, value, first_applicant_name, apdt_year) — 专利去重,专利价值,申请人对齐,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_zh_paper(id, publication_id, download_num, cover_year_start) — 中文论文去重,挂刊,下载量,发表年；dwd_en_paper(id, publication_id, cover_year_start) — 英文论文去重,挂刊,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐；dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐；dwd_zh_journal(publication_id, impact_score, jn_zone) — 中文刊影响指数,分区；dwd_en_journal(publication_id, impact_score, jn_zone) — 英文刊影响指数,分区；dwd_zh_project(id, funded_amount, final_report_abstract, project_level, approval_year, funded_province) — 国内项目资助,结题,级别,立项年,资助省；dwd_en_project(id, funded_amount, final_report_abstract, project_level, approval_year) — 国外项目资助,结题,级别,立项年；dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|全球创新监测.md|序号 59「根据创新价值数值计算模型对创新成果进行排序」；序号 56「按照创新价值进行自动分类」。统计对象=全球创新成果清单条目（专利/论文/资讯/机构/企业动态，去重以 innov 主键为准）。窗口=自然年（未甲方确认）。参考权威机构方案。
