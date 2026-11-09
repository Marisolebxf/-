# 政策实施效果（M_INNOV_PG_EFFECT）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PG_EFFECT |
| 指标名称 | 政策实施效果 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 政策与条件保障力指标展示 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

基于实施后数据变化评估实际效果。对象=城市（可切领域）。看近窗相对基线的成果增幅，取值可正可负。

## 计算逻辑说明

选定城市入集。需求未列关键指标字段，二级按实施前后成果变化。采用加权平均，三维：专利增幅 / 论文增幅 / 项目增幅。近 3 年均值相对前 5 年均值。

与 `M_INNOV_PG_COMPOSITE` 的政策实施效果维同一公式，本指标拆成三维输出。

近窗 (T-2,…,T)，基线 (T-7,…,T-3)：增幅=(近窗均值-基线均值)/max(基线均值,1)。

专利、论文名称对齐；项目用 `funded_institution` 对齐或 `funded_province` 命中。本批城内对增幅极值归一后等权 ×100 作展示分；原始增幅一并输出。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 政策实施效果 | 专利增幅 | 近窗专利相对基线。 | (近3年专利均值-前5年均值)/max(前5年均值,1) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 | 无 |
| 政策实施效果 | 论文增幅 | 近窗论文相对基线。 | (近3年论文均值-前5年均值)/max(前5年均值,1) | dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 政策实施效果 | 项目增幅 | 近窗立项相对基线。 | (近3年项目均值-前5年均值)/max(前5年均值,1) | dwd_zh_project(id, funded_institution, funded_province, approval_year) — 项目去重,立项年 | 无 |

## 源表字段

- dwd_policy_base(id, city, province, theme, status, expire_date, publish_year) — 政策空间,领域切片
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 机构对齐,空间
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位
- dwd_zh_project(id, funded_institution, funded_province, approval_year) — 项目去重,立项年

## 待建字段

- 无

## 参考资料

[1]政策实施效果｜中国科学技术信息研究所｜国家自然科学基金项目“科学基金项目产出专利对产业技术发展的影响研究”（L1624039）；国家社会科学基金项目“面向科技型中小企业创新的技术竞争情报方法体系研究”（12CTQ030）｜毛一雷，刘志辉，刘洢颖，姚长青. 公共基金资助产出及影响研究述评[J]. 情报探索, 2017(11): 97-103.
