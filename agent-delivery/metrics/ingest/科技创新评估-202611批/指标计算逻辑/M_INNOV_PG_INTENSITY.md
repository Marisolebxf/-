# 政策扶持力度（M_INNOV_PG_INTENSITY）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PG_INTENSITY |
| 指标名称 | 政策扶持力度 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 政策与条件保障力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

评估政策扶持的广度与深度。对象=城市（可切领域）。从政策数量、政策类型、政策覆盖面综合，取值 0—100。

## 计算逻辑说明

选定城市入集。采用加权平均，三维：政策数量（有效政策）/ 政策类型（类型去重）/ 政策覆盖面（区县或主题）。与综合评估扶持力度维同一套。

政策：`dwd_policy_base` 按 `id` 去重；`status` 含「有效」或 `expire_date` 晚于统计年末；`publish_year` 落年窗。

1. **政策数量**：去重件数。
2. **政策类型**：`type` 去重数。
3. **政策覆盖面**：`district` 去重数；全空则改 `theme` 去重数。

本批城内极值归一后等权 ×100。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 政策扶持力度 | 政策数量 | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, status, expire_date, publish_year) — 政策件数,有效 | 无 |
| 政策扶持力度 | 政策类型 | 政策类型覆盖数。 | COUNT(DISTINCT type) | dwd_policy_base(id, city, type, status, expire_date, publish_year) — 政策类型 | 无 |
| 政策扶持力度 | 政策覆盖面 | 区县广度；全空则主题数。 | COUNT(DISTINCT district)；全空则 COUNT(DISTINCT theme) | dwd_policy_base(id, city, district, theme, status, expire_date, publish_year) — 区县,主题 | 无 |

## 源表字段

- dwd_policy_base(id, title, theme, city, province, district, type, status, expire_date, publish_year) — 政策去重,类型,区县,主题,有效

## 待建字段

- 无

## 参考资料

[1] 政策扶持力度|浙江大学科教发展战略研究中心|浙江省科技厅重点软科学项目（2016C25G2010003）|张炜, 费小燕, 方辉. 区域创新政策多维度评价指标体系设计与构建[J]. 科技进步与对策, 2016, 33(1): 142-147.
