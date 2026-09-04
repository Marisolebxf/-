# 技术创新力综合评估（M_TECH_DS_07_TECH_INNOV_004）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-TECH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_DS_07_TECH_INNOV_004 |
| 指标名称 | 技术创新力综合评估 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

同M_INNOV_TINN_COMPOSITE-技术创新力综合评估

## 计算逻辑说明

同M_INNOV_TINN_COMPOSITE-技术创新力综合评估

## 源表字段

dwd_patent(pn, kind, granted_number, first_applicant_name, main_classification_ipcr, further_classification_ipcr, claims, other_Versions, apdt_year) — 专利去重,授权号,申请人对齐,主分类,附加分类,权利要求,同族,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent_legal(pn, status, expiration_year, legal_events) — 专利状态,到期年,法律事件；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_TINN_COMPOSITE（技术创新力综合评估）。禁止硬挂 182/186/190。见 TINN-D04。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
