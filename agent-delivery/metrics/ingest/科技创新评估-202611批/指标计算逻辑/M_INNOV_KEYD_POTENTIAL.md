# 区域科技创新发展潜力（M_INNOV_KEYD_POTENTIAL）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_KEYD_POTENTIAL |
| 指标名称 | 区域科技创新发展潜力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 重点领域规划 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

同一规划区域的发展潜力评分，取值 0—100。对象=区域，不是单技术产业化潜力，不是产业产值。

## 计算逻辑说明

选定区域入集。需求未列潜力构成维度，二级按增长动量/新进入者/成果转化收口。采用加权平均，三维：产出增速（近窗专利论文）/ 新机构（当年新出现机构）/ 转化活跃（年转移专利）。本批区域内极值归一。

入集同竞争力水平。

1. **产出增速**：近 3 年专利+论文均值相对前 5 年均值的增幅。
2. **新机构**：当年有专利或论文、且前 3 年未出现的机构去重数。
3. **转化活跃**：`transfer_effective_date` 落年、权利人名称对齐该区域机构的转移专利去重件数。

本批归一后等权 ×100。输出一行一区域。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 区域科技创新发展潜力 | 产出增速 | 近窗成果相对基线的增幅。 | (近3年均值-前5年均值)/max(前5年均值,1) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 区域科技创新发展潜力 | 新机构 | 当年新出现的有产机构。 | COUNT(DISTINCT 当年新机构) | dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 城市机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外机构入集；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 区域科技创新发展潜力 | 转化活跃 | 年转移专利去重件数。 | COUNT(DISTINCT pn) | dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 区域机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人

## 待建字段

- 无

## 参考资料

[1] 区域科技创新竞争力水平|中国科技发展战略研究小组|中国科学院大学中国创新创业管理研究中心|中国科技发展战略研究小组, 中国科学学与科技政策研究会. 中国区域创新能力评价报告[M]. 北京: 科学技术文献出版社, 2025.

[2]区域科技创新竞争力水平｜内蒙古大学经济管理学院，中国科学院科技政策与管理科学研究所，中国科学院创新发展研究中心，中国科学院研究生院管理学院｜国家自然科学基金青年项目（71103078、71103173）；内蒙古自然科学基金项目（2011BS1002）；中国博士后科学基金第四批特别项目（201104158）；中国科学院王宽诚博士后工作奖励项目（2011年度）｜高霞，陈凯华，官建成. 标度无关性视角下的我国区域科技创新绩效评价研究[J]. 中国软科学, 2012(8): 65-74.

[3]区域科技创新竞争力水平｜浙江工商大学统计与数学学院｜浙江省重点建设高校优势特色学科（浙江工商大学统计学）和“统计数据工程技术与应用协同创新中心”资助｜杨双双，解静. 基于改进CRITIC的中国区域创新能力测度分析[J]. 统计与管理, 2023, 38(9): 40-54. DOI: 10.16722/j.issn.1674-537x.2023.09.007.
