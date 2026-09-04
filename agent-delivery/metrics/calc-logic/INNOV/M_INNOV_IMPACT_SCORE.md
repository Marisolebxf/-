# 创新影响分数（M_INNOV_IMPACT_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_IMPACT_SCORE |
| 指标名称 | 创新影响分数 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对领域内机构与技术领域实体赋创新影响分并排名，取值 0—100。

## 计算逻辑说明

采用加权平均。二维：产出规模 / 网络影响。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 产出规模 |  | 机构或领域的成果件数。 | 机构：专利数 + 论文数；领域：专利数 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,统计年；dwd_en_paper(id, cover_year_start) — 英文论文,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 网络影响 |  | 机构合作面或领域被引合计。 | 机构：合作邻居数；领域：专利被引合计 | dwd_patent(pn, applicants, first_applicant_name) — 共申请人；dwd_zh_project(id, funded_institution, participating_institution) — 项目合作机构；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数 |

## 源表字段

dwd_org_base_info(org_id, name_cn, province, city) — 机构对齐,空间过滤；dwd_patent(pn, first_applicant_name, applicants, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,共申请人,IPC领域,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数；dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年；dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|全球创新监测.md|序号 70「对知识图谱中的实体节点进行创新影响赋分，用户可查看各实体节点的影响分数和排名」。不是网络密度/中心度（seq 116(5)），禁止 M_SVC_GRAPH_* 顶替。参考权威机构方案。
