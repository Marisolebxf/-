# 产业技术影响力（M_INNOV_POT_TECH_INFL）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_POT_TECH_INFL |
| 指标名称 | 产业技术影响力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 产业发展潜力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

选定产业的技术影响力。从专利被引次数、同族规模综合评分，取值 0—100。分数越高技术影响力越强。`M_INNOV_POT_COMPOSITE` 技术影响力维复用本二维。不用标准必要专利字段。

## 计算逻辑说明

选定产业入集。采用加权平均，二维：专利被引次数（cited_by_nums）/ 同族规模（other_Versions）。

### 第一步：入集

页面年窗、空间（可选）、产业。

机构：`dwd_org_base_info` 按 `org_id` 去重；`reg_status` 含「存续」。产业用 `industry` / `industry_l1_code`，或 `external_id` 对齐 `dwd_org_industry_tags.credit_code`。名称用 `name_cn`。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；`first_applicant_name` 对齐机构名后继承产业。无命中不剔除产业，只缩小计入的专利。

一行一个产业。本批至少 2 个产业才做极值归一。

### 第二步：两个子项

同一维在**本批产业**内极值归一。分母为 0 的产业该维缺测。

1. **专利被引次数**  
   该产业专利命中 `dwd_patent_cited` 的 `cited_by_nums` 合计。无引用行当 0。

2. **同族规模**  
   该产业专利 `other_Versions` 数组成员数合计 / 专利去重件数。空数组或空值该件记 1。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
技术影响力=\frac{norm(专利被引)+norm(同族规模)}{2}\times 100
$$

缺测维不补 0，剩余维权重重归一。按 `score` 降序排名。

输出：一行一个产业，含两子项原始值、`score`（0—100）、`rank`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 产业技术影响力 | 专利被引次数 | 产业相关专利被其他专利引用的总次数。 | SUM(cited_by_nums) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 | 无 |
| 产业技术影响力 | 同族规模 | 产业专利海外布局广度，用同族成员数均值衡量。 | 同族成员数合计 / 专利数 | dwd_patent(pn, first_applicant_name, other_Versions, apdt_year) — 同族专利,申请人对齐,申请年 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_code, city, province, reg_status) — 机构入集,产业对齐,名称对齐
- dwd_org_industry_tags(credit_code, industry_code, industry_name) — 产业标签
- dwd_patent(pn, first_applicant_name, other_Versions, apdt_year) — 专利去重,申请人对齐,同族,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数

## 待建字段

- 无

## 参考资料

[1]产业技术影响力｜中国科学院文献情报中心，中国科学院大学经济与管理学院信息资源管理系｜无基金项目资助｜席崇俊，吕璐成，赵亚娟，孙文君，王翼虎. 基于全代引证的专利学术影响力成长路径及获奖因素影响研究[J]. 文献与数据学报, 2024, 6(3): 34-46. DOI: 10.31193/SSAP.J.ISSN.2096-6695.2024.03.04.
