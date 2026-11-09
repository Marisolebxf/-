# 多企业竞争情报比对（M_INNOV_DS_09_RESEARCH_004）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_09_RESEARCH_004 |
| 指标名称 | 多企业竞争情报比对 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 研究领域分析 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_RES_CI_COMPARE（多企业竞争情报比对）**。

## 计算逻辑说明

本指标与 **M_INNOV_RES_CI_COMPARE（多企业竞争情报比对）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐
- dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

- 无

## 参考资料

[1]多企业竞争情报比对｜西北工业大学管理学院｜无基金项目资助｜王吉林，刘西林. 构建现代企业竞争情报系统[J]. 情报杂志, 2007(3): 31-33.

[2]多企业竞争情报比对｜上海理工大学管理学院，上海商学院｜国家自然科学基金项目（70472075、70672110）；教育部全国博士点基金项目（20060252004）；上海市重点学科建设项目（T0502）；上海市教育委员会重点科研项目（06ZS103）｜周丹，吴晓伟，徐福缘. 基于企业竞争力综合评价模型的竞争对手分析[J]. 情报杂志, 2008, 27(3): 25-28.

[3]多企业竞争情报比对｜辽宁工业大学经济管理学院｜辽宁省社会科学规划基金项目（L07BJY030）；全国统计科学研究项目（2006C07）｜尹子民，佟会文. 增长率—企业竞争能力战略决策图的研究与应用[J]. 科技管理研究, 2008(8): 186-187+193.
