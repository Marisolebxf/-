# 区域科技创新竞争力水平（M_INNOV_KEYD_COMPETITIVENESS）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_KEYD_COMPETITIVENESS |
| 指标名称 | 区域科技创新竞争力水平 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 重点领域规划 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

规划页选定区域的竞争力水平分值，取值 0—100。对象=区域（未选默认深圳），可并列对标区域。不是全球城市榜，不是产业发展潜力。

## 计算逻辑说明

选定区域入集。需求未列竞争力指标体系，二级按《中国区域创新能力评价报告》收口。采用加权平均，三维：创新产出（专利+论文）/ 创新主体（机构+高企）/ 政策供给（有效政策）。本批区域内极值归一。

空间用 `city`/`province`。领域可选：政策 `theme`、专利 IPC 前 4 位。

三维在本批区域（含对标）内归一后等权 ×100。输出一行一区域，含三子项原始值、`score`、`rank`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 区域科技创新竞争力水平 | 创新产出 | 专利与论文去重件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 区域科技创新竞争力水平 | 创新主体 | 存续机构与高企。 | 0.5×norm(机构数)+0.5×norm(高企数) | dwd_org_base_info(org_id, city, province, reg_status) — 存续机构；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签 | 无 |
| 区域科技创新竞争力水平 | 政策供给 | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, province, theme, status, expire_date, publish_year) — 有效政策 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 区域机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_policy_base(id, city, province, theme, status, expire_date, publish_year) — 有效政策

## 待建字段

- 无

## 参考资料

[1]区域科技创新竞争力水平｜内蒙古大学经济管理学院，中国科学院科技政策与管理科学研究所，中国科学院创新发展研究中心，中国科学院研究生院管理学院｜国家自然科学基金青年项目（71103078、71103173）；内蒙古自然科学基金项目（2011BS1002）；中国博士后科学基金第四批特别项目（201104158）；中国科学院王宽诚博士后工作奖励项目（2011年度）｜高霞，陈凯华，官建成. 标度无关性视角下的我国区域科技创新绩效评价研究[J]. 中国软科学, 2012(8): 65-74.

[2]区域科技创新竞争力水平｜浙江工商大学统计与数学学院｜浙江省重点建设高校优势特色学科（浙江工商大学统计学）和“统计数据工程技术与应用协同创新中心”资助｜杨双双，解静. 基于改进CRITIC的中国区域创新能力测度分析[J]. 统计与管理, 2023, 38(9): 40-54. DOI: 10.16722/j.issn.1674-537x.2023.09.007.
