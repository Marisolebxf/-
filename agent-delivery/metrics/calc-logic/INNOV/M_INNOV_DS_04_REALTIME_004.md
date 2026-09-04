# 创新影响分数（M_INNOV_DS_04_REALTIME_004）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_04_REALTIME_004 |
| 指标名称 | 创新影响分数 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_IMPACT_SCORE-创新影响分数

## 计算逻辑说明

同M_INNOV_IMPACT_SCORE-创新影响分数

## 源表字段

dwd_org_base_info(org_id, name_cn, province, city) — 机构对齐,空间过滤；dwd_patent(pn, first_applicant_name, applicants, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,共申请人,IPC领域,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数；dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年；dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_IMPACT_SCORE（创新影响分数）。05 无创新影响赋分专叶。见 RT-D04 / RT-B01。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
