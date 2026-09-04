# 多企业竞争情报比对（M_INNOV_RES_CI_COMPARE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_RES_CI_COMPARE |
| 指标名称 | 多企业竞争情报比对 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

比对多家企业的竞争情报等级，并给出竞争矩阵与战略定位图。

## 计算逻辑说明

选定企业入集。三维：竞争情报等级 / 竞争矩阵 / 战略定位图。重叠度复用研究领域重叠度，不另起领域维。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 竞争情报等级 |  | 企业对重叠度换算后分高/中/低。 | overlap×100；≥P70 高；P30–P70 中；<P30 低 | 同 M_INNOV_RES_OVERLAP — IPC/关键词/学者 Jaccard |
| 竞争矩阵 |  | 所选企业两两分值表。 | n×n 矩阵，对角=100 | 同上企业对结果 — 矩阵 |
| 战略定位图 |  | 规模对平均重叠度的散点。 | 横轴=专利数+论文数；纵轴=平均 overlap | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐；dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文论文关键词；dwd_en_paper_classification(id, keywords) — 英文论文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|科技发展规划.md|多企业竞争情报比对 · 序号 193(比对竞争情报等级，并提供竞争矩阵和战略定位图)
