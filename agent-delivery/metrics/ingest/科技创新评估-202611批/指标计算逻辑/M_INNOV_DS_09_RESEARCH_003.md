# 竞争情报等级（M_INNOV_DS_09_RESEARCH_003）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_09_RESEARCH_003 |
| 指标名称 | 竞争情报等级 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 研究领域分析 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_RES_CI_LEVEL（竞争情报等级）**。

## 计算逻辑说明

本指标与 **M_INNOV_RES_CI_LEVEL（竞争情报等级）** 为同一口径，计算步骤完全一致。完整步骤、公式与指标体系表见该指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐,空间过滤
- dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

- 无

## 参考资料

[1]竞争情报等级｜上海理工大学管理学院，上海商学院｜国家自然科学基金项目（70472075、70672110）；教育部全国博士点基金项目（20060252004）；上海市重点学科建设项目（T0502）；上海市教育委员会重点科研项目（06ZS103）｜周丹，吴晓伟，徐福缘. 基于企业竞争力综合评价模型的竞争对手分析[J]. 情报杂志, 2008(3): 25-28.
