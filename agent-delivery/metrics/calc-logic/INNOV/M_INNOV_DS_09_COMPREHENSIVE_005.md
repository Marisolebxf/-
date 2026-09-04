# 本地特色与优势分析（M_INNOV_DS_09_COMPREHENSIVE_005）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_09_COMPREHENSIVE_005 |
| 指标名称 | 本地特色与优势分析 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_PLAN_LOCAL_ADV-本地科技创新特色与优势

## 计算逻辑说明

同M_INNOV_PLAN_LOCAL_ADV-本地科技创新特色与优势

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤；dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,申请人对齐,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_org_annual_financial_info(org_id, year, development_employee) — 研发人员

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_PLAN_LOCAL_ADV（本地科技创新特色与优势）。禁止硬挂 186。见 COMP-D04。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
