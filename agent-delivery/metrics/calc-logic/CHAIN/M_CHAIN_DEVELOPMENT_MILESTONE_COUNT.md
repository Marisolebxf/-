# 发展里程碑数（M_CHAIN_DEVELOPMENT_MILESTONE_COUNT）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEVELOPMENT_MILESTONE_COUNT |
| 指标名称 | 发展里程碑数 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 月度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

指定产业链在统计窗内识别出的重大里程碑事件去重数，按重大技术突破、政策出台、龙头入驻三类归类。里程碑=对产业趋势产生显著影响、经事件识别算法判定超过阈值的关键事件。对象=产业链发展路线事件，不是普通资讯。

## 计算逻辑说明

算法库「产业发展路线历程模型」（1.1.1.1.1.1.1.3.3，约 456–466 行）要求「设定重大事件指标及判定阈值，利用事件识别算法判断指标数值超出阈值的重大事件及其对应时间节点，生成重大事件时间线」。据此，里程碑事件以 `industry_chain_milestone_event` 为真源，按里程碑类型分类去重计数。

### 计算步骤

1. 按 `chain_id` 定链，取 `industry_chain_milestone_event` 中 `is_deleted=0` 的记录。
2. 按 `milestone_type` 分类（重大技术突破 / 政策出台 / 龙头入驻，具体枚举以事件识别算法产出为准）。
3. 各分类内 `event_id` 去重计数，汇总为发展里程碑总数。

$$
发展里程碑数 = \sum_{类型} COUNT(DISTINCT event\_id \mid milestone\_type=类型)
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 发展里程碑数 | 重大技术突破 | 技术突破事件数 | 技术突破类里程碑去重事件数 | COUNT(DISTINCT event_id WHERE milestone_type=技术突破) | industry_chain_milestone_event(event_id, chain_id, milestone_type, event_date, event_level) — 里程碑事件 | 里程碑类型标准化枚举 |
|  | 政策出台 | 政策出台事件数 | 政策出台类里程碑去重事件数 | COUNT(DISTINCT event_id WHERE milestone_type=政策出台) | industry_chain_milestone_event(event_id, chain_id, milestone_type, event_date) — 里程碑事件；dwd_policy_base(id, title, publish_year) — 政策源 | 里程碑类型标准化枚举 |
|  | 龙头入驻 | 龙头入驻事件数 | 龙头企业入驻/投资类里程碑去重事件数 | COUNT(DISTINCT event_id WHERE milestone_type=龙头入驻) | industry_chain_milestone_event(event_id, chain_id, milestone_type, event_date) — 里程碑事件；chain_investment(investment_id, chain_id, enterprise_name, amount) — 投资源 | 里程碑类型标准化枚举 |

## 源表字段

- industry_chain_milestone_event(event_id, source_milestone_id, chain_id, node_id, event_name, milestone_type, phase_id, phase_name, event_date, event_level, region_code) — 里程碑事件真源（demo_gkxlumenx_dwd）
- chain_roadmap(chain_id, chain_name, timeline, total_events, year_span) — 路线图汇总（gkxlumenx_ads / demo_gkxlumenx_ads，已有 total_events）
- dwd_industry_chain_news_info(industry_code, industry_name, id, title, publish_date, abstract) — 资讯源（事件识别输入）
- dwd_policy_base(id, title, publish_year, rank) — 政策出台事件源
- chain_investment(investment_id, chain_id, enterprise_name, round, amount, invest_date) — 龙头入驻/投资事件源

## 待建字段

- milestone_type 三类标准化枚举（技术突破/政策出台/龙头入驻，当前取值未固化）
- 里程碑判定阈值与事件识别算法参数（对应算法库「重大事件指标体系及阈值设定」）
- gkxlumenx_dwd 无里程碑表，仅 demo_gkxlumenx_dwd 归一链路有，需同步到主链 DWD

## 参考资料

[1] 产业发展路线历程模型｜科技专题服务算法库 1.1.1.1.1.1.1.3.3（重大事件时间线、阈值判定）。

[2] 产业发展阶段与里程碑｜工业和信息化部｜产业高质量发展监测指标体系，重大事件（技术突破/政策/龙头）识别口径。
