# 专家学者影响力（M_INNOV_SCHOLAR_INFLUENCE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCHOLAR_INFLUENCE |
| 指标名称 | 专家学者影响力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q109 / Q-MO-DS01-02 |

## 口径定义

专家学者的学术影响程度。统计对象为学者实体，从 H 指数、被引数量、论文数量综合，取值 0—100。

## 计算逻辑说明

采用加权平均。三维：H指数 / 被引数量 / 论文数量（院士标签仅展示，不进分）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| H指数 |  | 学者 H 指数。 | 学者 H 指数 | dwd_scholar(scholar_id, h_index) — H指数 |
| 被引数量 |  | 学者论文总被引。 | 学者论文总被引 | dwd_scholar(scholar_id, citation_nums) — 被引数量 |
| 论文数量 |  | 学者发文量。 | 学者已发表论文数 | dwd_scholar(scholar_id, paper_nums) — 论文数量 |

## 源表字段

dwd_scholar(scholar_id, name_zh, name_en, scholar_org_name_zh, h_index, citation_nums, paper_nums, status) — 学者入集,姓名,所属机构,H指数,被引数量,论文数量,有效状态；dwd_scholar_talent_flag(scholar_id, academician) — 学者对齐,院士标签(仅展示)

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 11「支持要素影响力分析，通过算法模型评估各要素的重要性和影响力」。内部默认取第三方学术力（seq 162）且不展开公式；半成品 H 指数/引用/论文数为叙事维，不进本 ID 公式（Q-MO-DS01-02）。禁止 M_CHAIN_ACADEMIC_POWER 顶替。参考权威机构方案。
