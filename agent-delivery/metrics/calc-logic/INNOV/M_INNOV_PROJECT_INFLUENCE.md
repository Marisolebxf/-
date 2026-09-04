# 项目（含课题）影响力（M_INNOV_PROJECT_INFLUENCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PROJECT_INFLUENCE |
| 指标名称 | 项目（含课题）影响力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q110 / Q-MO-DS01-03 |

## 口径定义

单个科技项目/课题的影响程度。从资助金额、参与机构数、结题完备度综合，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：资助金额 / 参与机构数 / 结题完备。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 资助金额 |  | 项目获资助经费。 | 项目受资助金额（空则该维缺测） | dwd_zh_project(id, funded_amount) — 国内资助金额；dwd_en_project(id, funded_amount) — 国外资助金额 |
| 参与机构数 |  | 参与研究的机构规模。 | 参与机构去重数（没有则受资助机构计 1） | dwd_zh_project(id, participating_institution, funded_institution) — 国内参与机构,受资助机构；dwd_en_project(id, participating_institution, funded_institution) — 国外参与机构,受资助机构 |
| 结题完备 |  | 是否已有结题摘要。 | 有结题摘要记 1 / 无记 0 | dwd_zh_project(id, final_report_abstract) — 国内结题摘要；dwd_en_project(id, final_report_abstract) — 国外结题摘要 |

## 源表字段

dwd_zh_project(id, title, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国内项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年；dwd_en_project(id, title, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国外项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 11「支持要素影响力分析，通过算法模型评估各要素的重要性和影响力」。默认含课题（Q-MO-DS01-03）。05 无项目评价专叶，库缺口保持 missing。seq 145 仅把项目库当企业技术力输入。参考权威机构方案。
