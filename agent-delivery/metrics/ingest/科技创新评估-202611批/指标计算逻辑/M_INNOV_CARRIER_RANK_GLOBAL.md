# 创新载体多维度排名（M_INNOV_CARRIER_RANK_GLOBAL）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CARRIER_RANK_GLOBAL |
| 指标名称 | 创新载体多维度排名 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 创新载体排行榜 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

对全球入集载体按与 M_INNOV_CARRIER_INDEX_GLOBAL 同一套指数排序。对象=载体，可切总体 / 领域 / 地区三个名次宇宙。名次从 1 起。

## 计算逻辑说明

存续载体入集。指数同创新能力指数三维：创新资源 / 创新产出 / 创新能力。总体、领域、地区三个宇宙分别降序排名。

指数计算与 `M_INNOV_CARRIER_INDEX_GLOBAL` 完全一致，本指标只改排名宇宙。

### 第一步：入集与指数

国内 `dwd_org_base_info` + `dwd_research_institute_base_info` 存续合并，海外 `dwd_forg_base_info`。专利、论文名称对齐。得到每载体 `index_score`（0—100）。

### 第二步：三个排名宇宙

同一维在**该宇宙内**按 `index_score` 降序，`rank` 从 1 编（同分并列，下一排名跳过）。无有效指数不入榜。

1. **总体排名**：全部入集载体。
2. **领域排名**：载体在该 IPC 前 4 位有专利才入该领域宇宙；页面可切领域。
3. **地区排名**：按 `city`（海外 `country`/`city`）切宇宙。

输出：一行一个载体一个宇宙，含 `index_score`、`rank`、宇宙键。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新载体多维度排名 | 总体排名 | 全部载体按指数降序的名次。 | RANK(index_score) 全局 | 同 M_INNOV_CARRIER_INDEX_GLOBAL — 创新能力指数 | 无 |
| 创新载体多维度排名 | 领域排名 | 同 IPC4 有专利的载体宇宙内名次。 | RANK(index_score) 领域内 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 申请人对齐,IPC领域 | 无 |
| 创新载体多维度排名 | 地区排名 | 同城（或同国家）载体宇宙内名次。 | RANK(index_score) 地区内 | dwd_org_base_info(org_id, city, province) — 地区切宇宙；dwd_forg_base_info(org_id, country, city) — 海外地区 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, org_type, reg_status, province, city) — 国内载体入集,名称对齐,地区宇宙
- dwd_research_institute_base_info(org_id, name_cn, org_type, reg_status, province, city) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外载体入集
- dwd_org_annual_financial_info(org_id, year, development_employee, employees_number, operating_revenue) — 年报研发人员,从业人数,营收
- dwd_org_stock_finance_info(org_id, occur_period, operating_revenue) — 上市营收
- dwd_org_tech_tag(org_id, org_tag) — 高新技术等标签
- dwd_patent(pn, first_applicant_name, granted_number, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,授权号,IPC领域,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

- 无

## 参考资料

[1]创新载体多维度排名｜工业和信息化部｜—｜国家高新技术产业开发区综合评价指标体系：工信部规〔2024〕169号｜2024-09-04｜http://kjj.als.gov.cn/art/2026/5/29/art_6922_513542.html.
