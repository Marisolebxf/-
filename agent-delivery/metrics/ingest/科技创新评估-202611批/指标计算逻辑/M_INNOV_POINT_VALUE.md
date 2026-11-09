# 创新点价值评估（M_INNOV_POINT_VALUE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_POINT_VALUE |
| 指标名称 | 创新点价值评估 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 创新监测与分析 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

对已发现创新点从新颖性、影响潜力、成熟度综合评分，取值 0—100。分数越高价值越大。统计对象与 `M_INNOV_POINT_DISCOVERY` 同一套词条主键。

## 计算逻辑说明

入集：创新点发现输出的候选点。词条拆法、年键、空间过滤与发现指标一致，本指标不另造主键。

### 第一步：三个子项

同一维在**同一 `point_type` 内**极值归一。

1. **新颖性**

$$
新颖性=\frac{1}{1+T-t_0}
$$

\($t_0$\) 为该词条首次出现年，\(T\) 为统计年。越新越大。

2. **影响潜力**

词条关联成果被引合计：命中该词条的专利 `cited_by_nums` 之和（无行当 0）+ 中文论文 `citation_num` 之和（无行当 0）。英文论文无被引计数字段，该部分缺测。

3. **成熟度**

词条下 `granted_number` 非空的专利去重件数 / 该词条专利去重件数。无专利则该维缺测。

### 第二步：合成

三子项归一后等权 ×100。缺测维不补 0，剩余维权重按比例重归一。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新点价值=\frac{norm(新颖性)+norm(影响潜力)+norm(成熟度)}{3}\times 100
$$

输出：一行一个词条，含 `point_type`、主键、三子项原始值、`value_score`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新点价值评估 | 新颖性 | 词条出现早晚。 | 1 / (1 + 统计年 − 首次出现年) | dwd_patent(pn, keywords, main_classification_ipcr, apdt_year) — 专利关键词,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_paper_classification(id, keywords) — 中文论文关键词；dwd_en_paper_classification(id, keywords) — 英文论文关键词 | 无 |
| 创新点价值评估 | 影响潜力 | 关联成果被引合计。 | 专利被引合计 + 中文论文被引合计 | dwd_patent(pn, keywords, main_classification_ipcr) — 专利对齐词条；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_zh_paper_classification(id, keywords) — 中文论文词条；dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数 | 无 |
| 创新点价值评估 | 成熟度 | 专利授权比例。 | 授权专利数 / 专利数 | dwd_patent(pn, keywords, main_classification_ipcr, granted_number) — 专利词条,授权号 | 无 |

## 源表字段

- dwd_patent(pn, keywords, main_classification_ipcr, granted_number, first_applicant_name, apdt_year) — 专利关键词,IPC领域,授权号,申请人对齐,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数
- dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐
- dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1]创新点价值评估｜中国科学院文献情报中心，中国科学院大学｜席崇俊，吕璐成，赵亚娟，等. 基于全代引证的专利学术影响力成长路径及获奖因素影响研究[J]. 文献与数据学报, 2024, 6(3): 34-46.

[2]创新点价值评估｜天津工业大学经济与管理学院｜天津市知识产权局委托项目“面向2035年天津市提升知识产权创造能力的思路和重大举措研究”｜郑晓红，唐家龙. 京津冀地区专利质量动态演进趋势分析[J]. 安徽科技, 2021(3): 31-35.
