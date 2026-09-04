# 科研机构影响力（M_INNOV_ORG_INFLUENCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_ORG_INFLUENCE |
| 指标名称 | 科研机构影响力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

科研机构在产出、合作、领域布局上的影响程度。统计对象为科研机构实体，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：科研产出 / 合作广度 / 领域覆盖。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 科研产出 |  | 专利与论文产出规模。 | 专利去重件数 + 中英文论文去重件数（第一申请人对齐机构名；作者单位对齐机构名） | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年；dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年 |
| 合作广度 |  | 跨机构合作邻居数。 | 同项目其他参与机构去重数（可加专利共申请人邻居数） | dwd_zh_project(id, funded_institution, participating_institution) — 受资助机构,参与机构；dwd_patent(pn, applicants, first_applicant_name) — 共申请人,申请人对齐 |
| 领域覆盖 |  | IPC 主类覆盖面。 | 专利IPC前4位去重数 | dwd_patent(pn, first_applicant_name, main_classification_ipcr) — 申请人对齐,IPC领域 |

## 源表字段

dwd_research_institute_base_info(org_id, name_cn, org_type, reg_status, province, city) — 科研机构入集,名称对齐,类型过滤,存续过滤,空间筛选；dwd_org_base_info(org_id, name_cn, org_type, reg_status, province, city) — 机构入集补充,名称对齐,类型过滤,存续过滤,空间筛选；dwd_patent(pn, first_applicant_name, applicants, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,共申请人合作,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年；dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 11「支持要素影响力分析，通过算法模型评估各要素的重要性和影响力」。内部默认对照 seq 99 综合科研实力，第三方不展开。禁止用 M_SVC_ORG_TECH_SCORE 顶替。参考权威机构方案。
