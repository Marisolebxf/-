# 科学影响力评估（M_ENT_DS_07_INDUSTRY_POTENTIAL_004）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DS_07_INDUSTRY_POTENTIAL_004 |
| 指标名称 | 科学影响力评估 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业评估 |
| 三级模块 | - |
| 更新频率 | 年度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 |

## 口径定义

基于论文引用与国际合作数据，评估特定产业的科学影响力，输出科学影响力指标（论文被引次数、国际合作论文比例）的分布情况与排名。对象=产业（领域）的科研产出集合，不是单篇论文。禁止 mapped 182 / 05 seq 149，禁止 also_in DS-01-FACTORS（见 POT-D04）。

## 计算逻辑说明

两维加权：论文被引影响力 / 国际合作论文比例。

### 第一步：入集

统计窗默认自然年，年键=`cover_year_start`。产业→论文映射：经机构（企业/科研机构）与论文作者单位对齐（`dwd_author_org_base_info_rel` / `dwd_org_base_info_en_paper_rel`）或学者归属。中文论文被引用 `dwd_zh_paper_citation.citation_num`；英文被引次数字段现库缺失（待建）。

### 第二步：两个子项

1. **论文被引影响力**：
   - 论文被引总次数 = `SUM(中文 citation_num)` + `SUM(英文 citation_count)`；
   - 篇均被引 = 被引总次数 ÷ 论文去重数。
2. **国际合作论文比例**：
   - 国际合作论文数 = 一篇论文作者单位同时含境内与境外机构（`dwd_author_foreign_org_base_info_rel` 非空）的去重论文数；
   - 国际合作论文比例 = 国际合作论文数 ÷ 论文总数 × 100%。

两维极值归一后等权得科学影响力，输出产业分布与排名。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 科学影响力评估 | 论文被引影响力 | 论文被引总次数 | 产业论文被引次数合计。 | SUM(citation_num)+SUM(citation_count) | dwd_zh_paper(id, doi, cover_year_start) — 中文论文；dwd_en_paper(id, doi, cover_year_start) — 英文论文；dwd_zh_paper_citation(id, doi, citation_num) — 中文被引 | 英文论文被引次数字段 |
|  |  | 篇均被引次数 | 论文被引总次数 ÷ 论文去重数。 | 被引合计/论文去重数 | dwd_zh_paper(id, cover_year_start) — 中文论文去重；dwd_en_paper(id, cover_year_start) — 英文论文去重；dwd_zh_paper_citation(id, citation_num) — 中文被引 | 英文论文被引次数字段 |
| 科学影响力评估 | 国际合作论文比例 | 国际合作论文数 | 作者单位含境内+境外机构的论文去重数。 | COUNT(DISTINCT 国际合作论文) | dwd_zh_author(paper_id, author_id, institution) — 中文作者机构；dwd_en_author(paper_id, author_id, institution) — 英文作者机构；dwd_author_org_base_info_rel(author_id, org_id) — 境内机构关联；dwd_author_foreign_org_base_info_rel(author_id, org_id) — 境外机构关联；dwd_forg_base_info(org_id, country, country_code) — 境外国家 | 无 |
|  |  | 国际合作论文占比 | 国际合作论文数 ÷ 论文总数。 | 国际合作论文/论文总数 | 同上 | 无 |

## 源表字段

- dwd_zh_paper(id, doi, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, doi, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_citation(id, doi, citation_num) — 中文被引次数
- dwd_zh_author(paper_id, author_id, institution) — 中文作者机构
- dwd_en_author(paper_id, author_id, institution) — 英文作者机构
- dwd_author_org_base_info_rel(author_id, org_id, base_external_id) — 作者-境内机构关联
- dwd_author_foreign_org_base_info_rel(author_id, org_id, base_external_id) — 作者-境外机构关联
- dwd_forg_base_info(org_id, country, country_code) — 境外机构国家

## 待建字段

- 英文论文被引次数字段：现 `dwd_en_paper_citation` / `dwd_en_paper_reference`（仅 gkxlumenx_ods）无被引次数字段，需补 `citation_count`。

## 参考资料

[1] 科学影响力评估 | 需规 SRS《科技创新评估.md》序号149 | 论文被引次数、国际合作论文比例分布与排名 | 关联 Q009。

[2] 产业科学影响力 | 学术计量通用口径：被引频次（citation count）与国际合作论文占比（internationally co-authored papers share）。
