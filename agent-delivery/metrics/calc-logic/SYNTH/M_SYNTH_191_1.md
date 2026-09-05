# 区域创新协同分析模型（M_SYNTH_191_1）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SYNTH_191_1 |
| 指标名称 | 区域创新协同分析模型 |
| 使用位置 | 综合智能分析 / 区域创新协同分析 / 协同度计算模型 |
| 口径版本 | V1.3-20260904 |
| 更新频率 | 年度 |

## 口径定义

选定区域内、统计年度的区域创新协同指数，由完整度、中心度、密度三项标准化后加权合成，取值 0—100。分数越高表示创新合作越紧密、网络覆盖越好。对象=区域协同网络，不是要素贡献路径。与 `M_SYNTH_COLLAB_INDEX` 同核、本 ID 为算法库序号 191 模型入口。

## 计算逻辑说明

采用加权平均。三维：完整度 / 中心度 / 密度。算法库序号 191 已给这三项。需求序号 140 所列联合专利、合作项目、人才流动作为建网边，不另起一套二级。各维极值归一后等权（也可按评估重点改权，$ΣW=1$）。本指标不建作者合作网专表，边从现表现算。完整度=节点覆盖度，即“已进入协同的主体数 ÷ 区域内应纳入的主体总数”；应纳入主体类型由用户选择，不固定为企业、科研机构、人才机构三类。

### 第一步：入集与建网

节点：区域内用户所选主体类型（默认企业、科研机构、学者所属机构），键=`org_id`（学者机构对齐 `name_cn`）。孤立主体也进节点集。

边：无向，去重。三类边并集，有一次合作即连：

- 联合专利：`dwd_patent.applicants` 解析出不少于 2 个本区域申请人，每对申请人连边。
- 合作项目：`dwd_zh_project.funded_institution` 解析出不少于 2 个本区域机构，每对连边。
- 人才流动：同一 `scholar_id` 在 `dwd_scholar_work_experience` 中出现不少于 2 个不同 `org_name_zh`，且两机构都在本区域，按任职顺序相邻机构连边。

不落中间表。区域内有效节点不足 2 个则三维记空。

### 第二步：三个子项

1. **完整度**  
   节点完整度 = 已进入协同的节点数（至少有一条合作边，即度 ≥ 1）÷ 区域内应纳入节点总数（用户所选主体类型在区域内的节点并集，含孤立节点）。

2. **中心度**  
   全部节点度数的平均值，再极值归一，N<3 记空。不跑介数、不跑最短路。

3. **密度**  
   实际无向边数除以完全图边数（节点两两都相连时的边数），即密度 = 2×实际无向边数 ÷ [N×(N−1)]。节点不足 2 个则空。

三维等权得协同指数。高效协同 = 度数不低于本批七十分位的连通分量；孤立主体 = 度数为 0。输出区域一行，含三维得分、指数与孤立主体清单。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 区域创新协同分析模型 | 完整度 | 节点覆盖度 | 已进入协同的节点数占应纳入节点总数的比重。 | 已进入协同的节点数（至少一条合作边）÷ 区域内应纳入节点总数 × 100 | dwd_patent(pn, applicants, first_applicant_name, pbdt_year) — 联合专利边；dwd_zh_project(id, funded_institution, approval_year) — 合作项目；dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构流动；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续；dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构节点；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 人才所属机构 | 无 |
| 区域创新协同分析模型 | 中心度 | 平均点度中心性 | 协同网节点平均度数。                       | 全部节点度数求和后除以节点数，再极值归一                     | dwd_patent(pn, applicants, first_applicant_name, pbdt_year) — 联合专利边；dwd_zh_project(id, funded_institution, approval_year) — 合作项目；dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构流动；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
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

## 参考资料

[1] 区域创新协同指数|科学技术部|区域创新能力监测指标体系|https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110674.html

[2] 区域创新协同指数|中国科技发展战略研究小组|中国科学院大学中国创新创业管理研究中心|中国科技发展战略研究小组, 中国科学学与科技政策研究会. 中国区域创新能力评价报告[M]. 北京: 科学技术文献出版社, 2025.
