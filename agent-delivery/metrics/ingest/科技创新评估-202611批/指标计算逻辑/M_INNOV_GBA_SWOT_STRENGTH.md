# 湾区创新能力优势因素（M_INNOV_GBA_SWOT_STRENGTH）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_SWOT_STRENGTH |
| 指标名称 | 湾区创新能力优势因素 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力分析（SWOT） |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

在选定湾区城市下，从四子指数的 12 个分项中识别相对领先的优势因素，给出清单、表现与影响程度。本指标不是 0—100 评分。

## 计算逻辑说明

湾区 11 城、入集与名称对齐同创新能力总指数。分项原始值一律复用四子指标，不另造口径。

| 来源指标 | 分项 |
| --- | --- |
| M_INNOV_GBA_RES_INDEX | 专利资源、论文资源、研发投入 |
| M_INNOV_GBA_ORG_INDEX | 载体数量、载体产出、科技型机构 |
| M_INNOV_GBA_MECH_INDEX | 联合专利、合作项目、成果转化 |
| M_INNOV_GBA_ENV_INDEX | 政策供给、政策覆盖、高企密度 |

### 第一步：取分项并排名

按同一年窗跑四个子指标，得到每城 12 个分项原始值。每个分项在 11 城内降序排名 `rank`（1 最好；缺测不参评）。

页面传入城市（默认深圳）。看湾区整体时：某分项在 ≥4 城进入优势则记为湾区优势。

### 第二步：三个子项

1. **优势清单**：该城 `rank ≤ 3` 的分项。无命中则取 `rank` 最小的 1 项，并标记 `weak_signal=1`。
2. **表现**：该分项原始值 + 11 城排名。
3. **影响程度**：该分项在 11 城内的极值归一值（与对应子指标相同的 `norm`）。越大说明该项越拉高总指数。

输出：一行一个优势分项，含 `city`、`factor`、`raw`、`rank`、`impact`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 湾区创新能力优势因素 | 优势清单 | 该城相对领先的分项。 | 11 城排名 ≤ 3 | 见四子指标分项计算结果 — 入选 | 无 |
| 湾区创新能力优势因素 | 表现 | 分项原始值与排名。 | 原始值；rank | 同上 — 展示 | 无 |
| 湾区创新能力优势因素 | 影响程度 | 分项在 11 城内的归一值。 | norm(原始值) | 同上 — 影响程度 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

- 无

## 参考资料

[1]湾区创新能力优势因素｜中国科技发展战略研究小组、中国科学院大学｜—｜《中国区域创新能力评价报告2025》｜2025-09-27｜http://gdstc.gd.gov.cn/kjzx_n/gdkj_n/content/post_4779246.html.

[2]湾区创新能力优势因素｜江苏省科学技术情报研究所｜2023年度江苏省知识产权科研项目（KY20230077_05）｜陈长益，吴华珠，李向辉，姜迪. 专利导航在区域创新质量评价中的应用研究——以长三角城市群为例[J]. 情报探索, 2025(2): 51-58.
