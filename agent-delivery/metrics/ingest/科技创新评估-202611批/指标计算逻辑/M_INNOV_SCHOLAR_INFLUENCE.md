# 专家学者影响力（M_INNOV_SCHOLAR_INFLUENCE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_SCHOLAR_INFLUENCE |
| 指标名称 | 专家学者影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

专家学者的学术影响程度。统计对象为学者实体，从 H 指数、被引数量、论文数量综合，取值 0—100。

## 计算逻辑说明

第一步至合成：入集：`dwd_scholar` 按 `scholar_id` 去重（`status=1` 优先）。三子项直读 `h_index`、`citation_nums`、`paper_nums`，本批极值归一等权 ×100。`dwd_scholar_talent_flag.academician` 仅展示，不进分。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
学者影响力=\frac{norm(H指数)+norm(被引数量)+norm(论文数量)}{3}\times 100
$$

输出：按二级子项给出原始值与合成结果（评分类为 0—100；聚类/异常/预测输出标签或期次）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 专家学者影响力 | H指数 | H 指数。 | h_index | dwd_scholar(scholar_id, h_index) — H指数 | 无 |
| 专家学者影响力 | 被引数量 | 总被引。 | citation_nums | dwd_scholar(scholar_id, citation_nums) — 被引数量 | 无 |
| 专家学者影响力 | 论文数量 | 发文量。 | paper_nums | dwd_scholar(scholar_id, paper_nums) — 论文数量 | 无 |

## 源表字段

- dwd_scholar(scholar_id, name_zh, name_en, scholar_org_name_zh, h_index, citation_nums, paper_nums, status) — 学者入集,姓名,所属机构,H指数,被引数量,论文数量,有效状态
- dwd_scholar_talent_flag(scholar_id, academician) — 学者对齐,院士标签(仅展示)

## 待建字段

- 无

## 参考资料

[1]专家学者影响力｜河北联合大学｜刘智群，李颖，安凤妹. 科学计量指标在科研人员评价中应用[J]. 科技管理研究, 2011(14): 72-75. 
