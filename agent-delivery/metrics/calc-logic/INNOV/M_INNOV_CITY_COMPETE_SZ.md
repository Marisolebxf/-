# 深圳科技竞争力（M_INNOV_CITY_COMPETE_SZ）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CITY_COMPETE_SZ |
| 指标名称 | 深圳科技竞争力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 深圳创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

深圳市相对对标城的科技竞争力，由优势领域、薄弱环节、发展潜力三维合成。

## 计算逻辑说明

深圳与对标城入集。采用加权平均，三维：优势领域（区位商>1 的 IPC4 数）/ 薄弱环节（区位商偏低且全域份额高的 IPC4 数）/ 发展潜力（近窗产出增速）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 优势领域 |  | 相对对标宇宙区位商大于 1 的 IPC4 数。 | COUNT(IPC4 WHERE LQ>1) | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — IPC领域,申请人对齐 |
| 薄弱环节 |  | 区位商偏低且全域份额高的 IPC4 数。 | COUNT(IPC4 WHERE LQ<0.5 且全域份额≥中位数) | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — IPC领域,申请人对齐 |
| 发展潜力 |  | 近窗产出相对基线的增幅。 | (近3年均值-前5年均值)/max(前5年均值,1) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 深圳与对标城机构,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外对标机构；dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|深圳创新监测.md|竞争力分析 · 序号 132(包括优势领域、薄弱环节、发展潜力)
