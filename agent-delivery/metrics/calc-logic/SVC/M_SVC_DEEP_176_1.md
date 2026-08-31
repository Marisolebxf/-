# 人力资源服务机构技术力评价模型（M_SVC_DEEP_176_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_DEEP_176_1 |
| 指标名称 | 人力资源服务机构技术力评价模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务机构技术力评估分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 已按算法库9.5展开；标准化/满意度待建 |
| 是否在数据库 | 否 |
| 关联Q编号 |  |

## 口径定义

选定人力资源服务机构在统计年度的技术力指数，从人才资源、服务标准化、客户满意度三个维度评定，取值 0—100。

## 计算逻辑说明

入集：人力资源服务机构认定读 demo_gkxlumenx_ads.svc_org_card(service_type_candidate=HR  )

第一步：入集并取人员、招聘、标签。

第二步：三维原始值。

第三步：合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权（默认权重待甲方确认）后 ×100。全市/全样本同值取 0.5。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 人力资源服务机构技术力评价模型 | 人才资源 | 从业人数 | 从人才供给规模与招聘活跃度评估人才资源。 | employees_number | dwd_org_annual_financial_info(org_id, employees_number, year) — 从业人数 | 无 |
| 人力资源服务机构技术力评价模型 | 人才资源 | 招聘岗位人数 | 从人才供给规模与招聘活跃度评估人才资源。 | SUM(hiring_number) WHERE release_date 落在统计年 | dwd_org_recruit_info(org_id, hiring_number, release_date, job_title) — 招聘供给 | 无 |
| 人力资源服务机构技术力评价模型 | 服务标准化 |  | 从资质标签或流程规范性评估服务标准化程度。 | COUNT(资质类 org_tag)；流程规范待建 | 无 | svc_process_standard_flag-服务流程规范性 |
| 人力资源服务机构技术力评价模型 | 客户满意度 |  | 从客户反馈评估服务体验。 | 待建直读 | 无 | svc_csat_score-客户满意度 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(service_type_candidate=HR  )
- dwd_org_annual_financial_info(org_id, employees_number, year) — 从业人数
- dwd_org_recruit_info(org_id, job_title, hiring_number, release_date) — 招聘供给
- dwd_org_tech_tag(org_id, org_tag) — 资质标签代理标准化

## 待建字段

- svc_process_standard_flag-服务流程规范性
- svc_csat_score-客户满意度
