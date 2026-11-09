# 创新载体创新能力指数（M_INNOV_CARRIER_INDEX_GLOBAL）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CARRIER_INDEX_GLOBAL |
| 指标名称 | 创新载体创新能力指数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 创新载体排行榜 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

创新载体（企业/科研机构）的综合创新能力。统计对象为全球范围内入集的载体，从创新资源、创新产出、创新能力三个维度综合评分，取值 0—100。分数越高，创新能力越强，用于排行榜。

## 计算逻辑说明

专利、论文一律用名称对齐，不用机构-专利/作者-机构关系表。

### 第一步：入集

国内：`dwd_org_base_info` 与 `dwd_research_institute_base_info` 按 `org_id` 去重合并；`reg_status` 含「存续」。  
海外：`dwd_forg_base_info` 按 `org_id` 去重。  
名称对齐：国内用 `name_cn`，海外用 `name_en` / `name_alias`。空间筛选用 `province`/`city`（海外用 `country`/`city`）。

### 第二步：三个子项

1. **创新资源**  
   研发人员优先取年报 `development_employee`，没有则用 `employees_number`；再取最近年报或上市 `operating_revenue`。两子项在本批载体内分别极值归一后等权。皆空则该维缺测。

2. **创新产出**  
   统计年专利去重件数 + 中英文论文去重件数。  
   - 专利：`first_applicant_name` 对齐载体名称，`apdt_year` 落年窗，`COUNT(DISTINCT pn)`  
   - 论文：`dwd_zh_author`/`dwd_en_author.institution` 对齐载体名称，`cover_year_start` 落年窗，`COUNT(DISTINCT id)`

3. **创新能力**  
   - 科技型标签：`dwd_org_tech_tag.org_tag` 含「高新技术」记 1，否则 0（海外无标签当缺测）  
   - 授权专利：上述企业专利中 `granted_number` 非空的去重件数  
   两子项本批归一后等权；标签缺测则只保留授权专利。

### 第三步：合成

三维在本批载体内极值归一，等权后 ×100。缺测维不补 0，剩余维权重按比例重归一。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新能力指数=\frac{norm(创新资源)+norm(创新产出)+norm(创新能力)}{3}\times 100
$$

输出：一行一个载体，含三子项原始值、`index_score`（0—100）、默认权重说明（三维等权）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新载体创新能力指数 | 创新资源 | 研发人力与经营规模。 | 0.5×norm(研发人员)+0.5×norm(营收) | dwd_org_annual_financial_info(org_id, year, development_employee, employees_number, operating_revenue) — 年报研发人员,从业人数,营收；dwd_org_stock_finance_info(org_id, occur_period, operating_revenue) — 上市营收 | 无 |
| 创新载体创新能力指数 | 创新产出 | 专利与论文产出规模。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,统计年；dwd_en_paper(id, cover_year_start) — 英文论文,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 创新载体创新能力指数 | 创新能力 | 科技型资质与授权专利。 | 0.5×norm(高企标签)+0.5×norm(授权专利数) | dwd_org_tech_tag(org_id, org_tag) — 高新技术等标签；dwd_patent(pn, first_applicant_name, granted_number, apdt_year) — 授权号,申请人对齐,申请年 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, org_type, reg_status, province, city) — 国内载体入集,名称对齐,存续过滤,空间筛选
- dwd_research_institute_base_info(org_id, name_cn, org_type, reg_status, province, city) — 科研机构入集,名称对齐,存续过滤
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外载体入集,名称对齐,国家城市
- dwd_org_annual_financial_info(org_id, year, development_employee, employees_number, operating_revenue) — 年报研发人员,从业人数,营收
- dwd_org_stock_finance_info(org_id, occur_period, operating_revenue) — 上市营收
- dwd_org_tech_tag(org_id, org_tag) — 高新技术等科技型标签
- dwd_patent(pn, first_applicant_name, granted_number, apdt_year) — 专利去重,申请人对齐,授权号,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

- 无

## 参考资料

[1]创新载体创新能力指数｜科学技术部｜国家高新技术产业开发区综合评价指标体系：国科发火〔2021〕106号｜2021-04-22｜[科技部关于印发《国家高新技术产业开发区综合评价指标体系》的通知-中华人民共和国科学技术部](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html).
