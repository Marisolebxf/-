# 专利影响力（M_INNOV_PATENT_INFLUENCE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PATENT_INFLUENCE |
| 指标名称 | 专利影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

单件专利的影响程度。统计对象为专利实体，以被引次数为主、专利价值为辅，取值 0—100。

## 计算逻辑说明

第一步至合成：入集：`dwd_patent` 按 `pn` 去重；年窗取 `apdt_year`（或页面指定 `pbdt_year`）。被引：`dwd_patent_cited.cited_by_nums`（无行当 0）；不用 `reference_cited_count`。价值：`dwd_patent.value`（空则该维缺测）。默认权重被引 0.80、价值 0.20；缺测维重归一后 ×100。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
专利影响力=(0.8\times norm(被引次数)+0.2\times norm(专利价值))\times 100
$$

输出：按二级子项给出原始值与合成结果（评分类为 0—100；聚类/异常/预测输出标签或期次）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 专利影响力 | 被引次数 | 被他引次数。 | cited_by_nums | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn) — 专利对齐 | 无 |
| 专利影响力 | 专利价值 | 评估价值。 | value | dwd_patent(pn, value) — 专利价值 | 无 |

## 源表字段

- dwd_patent(pn, value, apdt_year, pbdt_year, first_applicant_name) — 专利去重,专利价值,申请年,公开年,申请人
- dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数

## 待建字段

- 无

## 参考资料

[1] 专利影响力｜中国科学院大学经济与管理学院信息资源管理系，中国科学院文献情报中心｜席崇俊，吕璐成，赵亚娟，孙文君，王翼虎. 基于全代引证的专利学术影响力成长路径及获奖因素影响研究[J]. 文献与数据学报, 2024, 6(3): 34-46.

[2]专利影响力｜国家知识产权局｜国家知识产权局. 专利价值分析指标体系[EB/OL].https://www.cnipa.gov.cn/tjxx/yjcg/201504/P020150422379449164888.pdf#13#6.

