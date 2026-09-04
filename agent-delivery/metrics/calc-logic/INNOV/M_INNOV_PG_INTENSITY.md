# 政策扶持力度（M_INNOV_PG_INTENSITY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PG_INTENSITY |
| 指标名称 | 政策扶持力度 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

评估政策扶持的广度与深度。对象=城市（可切领域）。从政策数量、政策类型、政策覆盖面综合，取值 0—100。

## 计算逻辑说明

选定城市入集。采用加权平均，三维：政策数量（有效政策）/ 政策类型（类型去重）/ 政策覆盖面（区县或主题）。与综合评估扶持力度维同一套。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 政策数量 |  | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, status, expire_date, publish_year) — 政策件数,有效 |
| 政策类型 |  | 政策类型覆盖数。 | COUNT(DISTINCT type) | dwd_policy_base(id, city, type, status, expire_date, publish_year) — 政策类型 |
| 政策覆盖面 |  | 区县广度；全空则主题数。 | COUNT(DISTINCT district)；全空则 COUNT(DISTINCT theme) | dwd_policy_base(id, city, district, theme, status, expire_date, publish_year) — 区县,主题 |

## 源表字段

dwd_policy_base(id, title, theme, city, province, district, type, status, expire_date, publish_year) — 政策去重,类型,区县,主题,有效

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|科技创新评估.md|政策扶持力度分析 · 序号 153(政策数量、政策类型、政策覆盖面)
