# 创新机构指数（M_INNOV_GBA_ORG_INDEX）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_ORG_INDEX |
| 指标名称 | 创新机构指数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

湾区各城创新载体的数量与产出。统计对象为粤港澳大湾区 11 城，从载体数量、载体产出、科技型机构综合评分，取值 0—100。分数越高，载体越强。

## 计算逻辑说明

湾区城市清单、入集与名称对齐同创新资源指数。不用机构-专利、作者-机构关系表。

### 第一步：入集

该城存续机构（企业库 + 科研院所 + 港澳海外库）按 `org_id` 去重。

### 第二步：三个子项

同一维在**本批 11 城**内极值归一。

1. **载体数量**：该城入集机构 `COUNT(DISTINCT org_id)`。
2. **载体产出**：统计年专利去重件数 + 中英文论文去重件数（名称对齐，年键同资源指数）。
3. **科技型机构**：`dwd_org_tech_tag.org_tag` 含「高新技术」的机构去重数；另加科研院所去重数（`dwd_research_institute_base_info`）。两者相加。无标签且无院所则该维为 0。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新机构指数=\frac{norm(载体数量)+norm(载体产出)+norm(科技型机构)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。输出：一行一城，含三子项原始值、`org_index`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新机构指数 | 载体数量 | 该城存续机构数。 | COUNT(DISTINCT org_id) | dwd_org_base_info(org_id, city, province, reg_status) — 企业入集,湾区城市；dwd_research_institute_base_info(org_id, city, province, reg_status) — 科研院所；dwd_forg_base_info(org_id, country, city) — 港澳机构 | 无 |
| 创新机构指数 | 载体产出 | 该城专利与论文件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 创新机构指数 | 科技型机构 | 高企与科研院所数。 | 高企去重数 + 科研院所去重数 | dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_research_institute_base_info(org_id, city, province) — 科研院所 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_org_tech_tag(org_id, org_tag) — 高新技术等科技型标签
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

- 无

## 参考资料

[1]创新机构指数数｜科技部｜创新型国家评价指标体系｜2017年https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/P020131204326192340968.pdf.

[2]创新机构指数｜科技部｜—｜国家高新技术产业开发区综合评价指标体系｜2021年｜https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html
