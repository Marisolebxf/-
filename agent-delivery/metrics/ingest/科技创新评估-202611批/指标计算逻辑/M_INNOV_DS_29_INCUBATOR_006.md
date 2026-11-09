# 影响力评价（M_INNOV_DS_29_INCUBATOR_006）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_29_INCUBATOR_006 |
| 指标名称 | 影响力评价 |
| 使用位置 | 科技专题服务系统 / 科技专题内容运营中心 / 服务机构管理 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

孵化载体的影响力。统计对象为名称或类型含孵化、众创、加速器的存续机构，从在孵规模、创新产出、服务能力综合评分，取值 0—100。

## 计算逻辑说明

专利、论文用名称对齐。在孵企业用子公司表代理，不另建在孵名录。

### 第一步：入集

`dwd_org_base_info` 按 `org_id` 去重；`reg_status` 含「存续」。入集（满足任一）：

- `name_cn` 或 `org_type` 含「孵化器」「众创空间」「加速器」「孵化」
- 或 `dwd_org_tech_tag.org_tag` 含「孵化」

空间用 `province`/`city`。名称用 `name_cn`。子公司：`dwd_org_subsidiary_info.org_id` 对齐载体，取 `sub_org_id` / `sub_name_cn`。

### 第二步：三个子项

同一维在**本批孵化载体**内极值归一。

1. **在孵规模**  
   `COUNT(DISTINCT sub_org_id)`。无子公司当 0。

2. **创新产出**  
   载体及其子公司统计年专利去重件数 + 中英文论文去重件数。专利 `first_applicant_name` 对齐 `name_cn` 或 `sub_name_cn`；论文作者 `institution` 同样对齐。

3. **服务能力**  
   子公司中 `org_tag` 含「高新技术」的去重数；载体自身有该标签再加 1。无标签当 0。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
孵化影响力=\frac{norm(在孵规模)+norm(创新产出)+norm(服务能力)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。

输出：一行一个载体，含三子项原始值、`influence_score`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 影响力评价 | 在孵规模 | 子公司代理的在孵企业数。 | COUNT(DISTINCT sub_org_id) | dwd_org_subsidiary_info(org_id, sub_org_id, sub_name_cn) — 子公司 | 无 |
| 影响力评价 | 创新产出 | 载体与子公司的专利论文。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 影响力评价 | 服务能力 | 高企标签覆盖。 | 高企子公司数 + 载体高企标记 | dwd_org_tech_tag(org_id, org_tag) — 高新技术等标签 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 孵化载体入集,名称对齐
- dwd_org_tech_tag(org_id, org_tag) — 孵化/高新技术标签
- dwd_org_subsidiary_info(org_id, sub_org_id, sub_name_cn) — 在孵企业代理
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

- 无

## 参考资料

[1] 影响力评价｜廊坊市科学技术局｜—｜关于开展2024年度科技企业孵化器和众创空间绩效评价工作的通知｜2025-08-04｜https://kjj.lf.gov.cn/tongzhigonggao/2025-08-06/8432.html.

[2]影响力评价｜宿州市科学技术局｜—｜宿州市科技企业孵化器管理和绩效评价实施细则（修订）｜2025-07-29｜https://kejiju.ahsz.gov.cn/public/2655581/195803021.html#1.

