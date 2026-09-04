# 区域创新协同分析模型（M_SYNTH_191_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_191_1 |
| 指标名称 | 区域创新协同分析模型 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新协同分析 |
| 三级模块 | 协同度计算模型 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SYNTH-C-01 |

## 口径定义

选定区域内、统计年度的区域创新协同指数，由完整度、中心度、密度三项标准化后加权合成，取值 0—100。分数越高表示创新合作越紧密、网络覆盖越好。对象=区域协同网络，不是要素贡献路径。与 `M_SYNTH_COLLAB_INDEX` 同核、本 ID 为算法库序号 191 模型入口。

## 计算逻辑说明

采用加权平均。三维：完整度 / 中心度 / 密度。算法库序号 191 已给这三项。需求序号 140 所列联合专利、合作项目、人才流动作为建网边，不另起一套二级。各维极值归一后等权（也可按评估重点改权，ΣW=1）。本指标不建作者合作网专表，边从现表现算。完整度目标类型固定为企业、科研机构、人才机构三类，不含服务机构。

### 第一步：入集与建网

节点：区域内企业、科研机构、学者所属机构，键=`org_id`（学者机构对齐 `name_cn`）。孤立主体也进节点集。

边：无向，去重。三类边并集，有一次合作即连：

- 联合专利：`dwd_patent.applicants` 解析出不少于 2 个本区域申请人，每对申请人连边。
- 合作项目：`dwd_zh_project.funded_institution` 解析出不少于 2 个本区域机构，每对连边。
- 人才流动：同一 `scholar_id` 在 `dwd_scholar_work_experience` 中出现不少于 2 个不同 `org_name_zh`，且两机构都在本区域，按任职顺序相邻机构连边。

不落中间表。区域内有效节点不足 2 个则三维记空。

### 第二步：三个子项

1. **完整度**  
   已至少有一条边的主体类型数除以 3。目标类型固定为企业、科研机构、人才机构。某类有节点且该类至少 1 个节点有合作边，则该类算已覆盖。

2. **中心度**  
   全部节点度数的平均值，再极值归一。不跑介数、不跑最短路。

3. **密度**  
   实际无向边数除以完全图边数（节点两两都相连时的边数）。节点不足 2 个则空。

三维等权得协同指数。高效协同 = 度数不低于本批七十分位的连通分量；孤立主体 = 度数为 0。输出区域一行，含三维得分、指数与孤立主体清单。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 区域创新协同分析模型 | 完整度 | 企业协同覆盖 | 企业类节点是否至少有一条合作边。 | 企业类有节点且至少 1 个企业有合作边则记覆盖 | dwd_patent(pn, applicants, first_applicant_name, pbdt_year) — 联合专利边；dwd_zh_project(id, funded_institution, approval_year) — 合作项目；dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构流动；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 科研机构协同覆盖 | 科研机构类节点是否至少有一条合作边。 | 科研机构类有节点且至少 1 个机构有合作边则记覆盖 | dwd_patent(pn, applicants, first_applicant_name, pbdt_year) — 联合专利边；dwd_zh_project(id, funded_institution, approval_year) — 合作项目；dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构流动；dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 人才机构协同覆盖 | 人才所属机构是否至少有一条合作边。 | 人才机构类有节点且至少 1 个机构有合作边则记覆盖 | dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构流动；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者存量,所属机构；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
| 区域创新协同分析模型 | 中心度 | 平均点度中心性 | 协同网节点平均度数。 | 全部节点度数求和后除以节点数，再极值归一 | dwd_patent(pn, applicants, first_applicant_name, pbdt_year) — 联合专利边；dwd_zh_project(id, funded_institution, approval_year) — 合作项目；dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构流动；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
| 区域创新协同分析模型 | 密度 | 网络密度 | 实际合作边占完全图边数的比重。 | 实际无向边数除以节点两两相连时的边数 | dwd_patent(pn, applicants, first_applicant_name, pbdt_year) — 联合专利边；dwd_zh_project(id, funded_institution, approval_year) — 合作项目；dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构流动；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域节点入集,名称对齐,机构类型
- dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构节点
- dwd_patent(pn, applicants, first_applicant_name, pbdt_year) — 联合专利边
- dwd_zh_project(id, funded_institution, approval_year) — 合作项目边
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 人才所属机构
- dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 人才流动边

## 待建字段

- 无
