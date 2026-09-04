# 协同绩效与影响力智能评估（M_INNOV_DS_26_ECO_012）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_26_ECO_012 |
| 指标名称 | 协同绩效与影响力智能评估 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 科技专题战略分析 |
| 三级模块 | 服务生态分析 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对生态内机构从产出规模、网络协同、协同绩效综合评分，取值 0—100。

## 计算逻辑说明

机构名作节点，共现作边。三维等权 ×100：产出规模（专利+论文）/ 网络协同（合作邻居数）/ 协同绩效（合作成果占比）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 产出规模 |  | 机构专利与论文件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 网络协同 |  | 合作邻居数。 | COUNT(DISTINCT 合作机构名) | dwd_patent(pn, applicants, first_applicant_name) — 共申请人；dwd_zh_project(id, funded_institution, participating_institution) — 项目合作机构 |
| 协同绩效 |  | 合作成果占自身成果比。 | 合作成果数 / 成果数 | 同上专利论文项目 — 合作占比 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 机构入集,名称对齐；dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集；dwd_patent(pn, first_applicant_name, applicants, apdt_year) — 专利去重,申请人对齐,共申请人,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

无

## 备注

OPEN draft 身份。05 无生态协同绩效专叶，不发明 M_*，见 ECO-D12 / ECO-B02。04-科技专题服务系统 服务生态协同绩效与影响力，参考权威机构方案。
