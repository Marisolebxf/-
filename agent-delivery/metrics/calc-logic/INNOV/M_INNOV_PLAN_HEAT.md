# 热度指数（M_INNOV_PLAN_HEAT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_HEAT |
| 指标名称 | 热度指数 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

热门技术领域当前周期受关注程度，取值 0—100。对象=IPC 前 4 位。三维：专利热度、论文热度、项目热度。

## 计算逻辑说明

按 IPC 前 4 位入集。需求未列热度构成维度，二级按文献计量。采用加权平均，三维：专利热度 / 论文热度 / 项目热度。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 专利热度 |  | 该 IPC4 年申请量。 | COUNT(DISTINCT pn) | dwd_patent(pn, main_classification_ipcr, apdt_year) — IPC领域,申请年 |
| 论文热度 |  | 题名命中该方向的年论文数。 | COUNT(DISTINCT 论文id) | dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文题名,发表年；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文题名,发表年 |
| 项目热度 |  | 名称命中该方向的年立项数。 | COUNT(DISTINCT 项目id) | dwd_zh_project(id, title, approval_year) — 国内项目；dwd_en_project(id, title, approval_year) — 国外项目 |

## 源表字段

dwd_patent(pn, main_classification_ipcr, apdt_year) — IPC领域,申请年；dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文题名,发表年；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文题名,发表年；dwd_zh_project(id, title, approval_year) — 国内项目名称,立项年；dwd_en_project(id, title, approval_year) — 国外项目名称,立项年

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技发展规划.md|全球热点技术捕捉 · 序号 178(提供热度指数、增长速度等关键指标)。需求未列热度构成维度，二级按文献计量专利/论文/项目热度，参考权威机构方案。
