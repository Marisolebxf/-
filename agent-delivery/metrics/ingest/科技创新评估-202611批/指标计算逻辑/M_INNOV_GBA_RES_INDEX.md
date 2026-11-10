# 创新资源指数（M_INNOV_GBA_RES_INDEX）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_RES_INDEX |
| 指标名称 | 创新资源指数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

湾区各城的创新资源禀赋。统计对象为粤港澳大湾区 11 城，从专利、论文、研发投入综合评分，取值 0—100。分数越高，资源越厚。

## 计算逻辑说明

湾区城市：广州、深圳、珠海、佛山、惠州、东莞、中山、江门、肇庆、香港、澳门。`city`/`province` 去「市」「特别行政区」后命中即入集。港澳也可从 `dwd_forg_base_info.country`/`city` 命中。无常住人口字段，不做人均。

### 第一步：入集

湾区内存续机构：`dwd_org_base_info`、`dwd_research_institute_base_info` 按 `org_id` 去重，`reg_status` 含「存续」；港澳补 `dwd_forg_base_info`。名称对齐：国内 `name_cn`，海外 `name_en`/`name_alias`。专利、论文一律名称对齐。

### 第二步：三个子项

同一维在**本批 11 城**内极值归一。

1. **专利资源**：统计年 `first_applicant_name` 对齐该城机构后 `COUNT(DISTINCT pn)`，`apdt_year` 落年窗。
2. **论文资源**：作者 `institution` 对齐该城机构后，中英文论文 `COUNT(DISTINCT id)`，`cover_year_start` 落年窗。
3. **研发投入**：该城机构上市 `research_development_amount` 合计（`occur_period` 落年窗）；全空则改用年报 `development_employee` 合计（`year` 落年窗）。皆空则该维缺测。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新资源指数=\frac{norm(专利资源)+norm(论文资源)+norm(研发投入)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。输出：一行一城，含三子项原始值、`res_index`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新资源指数 | 专利资源 | 该城专利去重件数。 | COUNT(DISTINCT pn) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 | 无 |
| 创新资源指数 | 论文资源 | 该城论文去重件数。 | COUNT(DISTINCT 论文id) | dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 创新资源指数 | 研发投入 | 上市研发经费，否则研发人员。 | SUM(research_development_amount)；空则 SUM(development_employee) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入,统计期；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员

## 待建字段

- 无

## 参考资料

 [1]创新资源指数数｜科技部｜创新型国家评价指标体系｜2017年https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/P020131204326192340968.pdf.

[2]创新资源指数｜科技部｜—｜国家高新技术产业开发区综合评价指标体系｜2021年｜https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html
