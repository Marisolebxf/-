# 事件重要性等级（M_INNOV_EVENT_IMPORTANCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_EVENT_IMPORTANCE |
| 指标名称 | 事件重要性等级 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q115 / Q-MO-DS01-08 |

## 口径定义

科技政策事件重要性分档。综合同一事件的关注度与影响力，输出高/中/低。

## 计算逻辑说明

同一id的事件关注度与事件影响力综合得分。综合分=0.5×attention+0.5×influence。本窗综合分：≥P70 为高，≤P30 为低，其余为中；样本<20 时改用固定阈 70/40，并标 rule=fallback。

## 源表字段

依赖 M_INNOV_EVENT_ATTENTION / M_INNOV_EVENT_INFLUENCE 结果；入集对齐 dwd_policy_base(id)

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 15「基于事件影响力、关注度等指标自动计算等级，用户可按高、中、低级别筛选事件」。SRS L6-2 点名自动分级 → 差集 missing，不是 CMS 手工打标。阈值未签（Q-MO-DS01-08）。
