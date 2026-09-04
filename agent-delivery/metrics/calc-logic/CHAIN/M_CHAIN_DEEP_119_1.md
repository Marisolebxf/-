# 产业发展路线历程模型（M_CHAIN_DEEP_119_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_119_1 |
| 指标名称 | 产业发展路线历程模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

针对目标产业，基于产业基础指标与资讯基础指标，利用事件识别算法判定「指标数值超出阈值」的重大事件（政策发布、投融资、里程碑、重大资讯四类），按时间排序生成产业发展历程的重大事件时间线，反映产业历史演进逻辑与关键拐点。对象=产业重大事件，不是普通资讯流水。

## 计算逻辑说明

① 事件采集与清洗：政策事件取 `dwd_policy_base`（publish_date 非空且 status 有效），投融资事件取 `dwd_org_financing_info`（completion_date），里程碑事件取 `industry_chain_milestone_event`，资讯事件取 `dwd_news_base`/`dwd_industry_chain_news_info`。② 事件识别：按「重大事件指标体系与阈值」判定事件级别，指标值超阈值才计入。③ 时间线生成：按 event_date/publish_time 升序，统计事件总数、时间跨度（首末事件年份差）、事件密度。

- 政策事件数 = COUNT(DISTINCT id) WHERE 政策主题命中目标产业 AND 指标超阈值
- 投融资事件数 = COUNT(DISTINCT org_id+completion_date) WHERE 金额/轮次超阈值
- 里程碑事件数 = COUNT(DISTINCT event_id) FROM industry_chain_milestone_event
- 资讯事件数 = COUNT(DISTINCT news_id) WHERE 热度/重要性超阈值
- 时间跨度(年) = MAX(事件年) − MIN(事件年)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业发展路线历程模型 | 重大事件识别 | 政策事件数 | 与产业相关的重大政策发布去重数。 | COUNT(DISTINCT id) WHERE 主题命中 AND 级别≥阈值 | dwd_policy_base(id, title, publish_code, publish_date, publish_year, rank, type, theme, status, ministry) | 重大事件指标体系及阈值设定表 |
|  |  | 投融资事件数 | 产业内重大投融资事件去重数。 | COUNT(DISTINCT org_id, completion_date) WHERE 金额≥阈值 | dwd_org_financing_info(org_id, name_cn, external_id, funding_round, funding_amount, completion_date, investors_name)；demo_gkxlumenx_dwd.industry_chain_investment_event(event_id, chain_id, investment_type, financing_round, amount, event_date) | 重大事件指标体系及阈值设定表 |
|  |  | 里程碑事件数 | 产业里程碑类型重大事件去重数。 | COUNT(DISTINCT event_id) | demo_gkxlumenx_dwd.industry_chain_milestone_event(event_id, chain_id, node_id, event_name, milestone_type, phase_name, event_date, event_level, region_code) | 无 |
|  |  | 资讯事件数 | 产业相关重大资讯去重数。 | COUNT(DISTINCT news_id) WHERE 热度≥阈值 | dwd_news_base(yqwyj, fbsj, lymc, lx, bt, zy, xgqyxx)；dwd_industry_chain_news_info(industry_code, industry_name, id, title, publish_date, abstract, source)；demo_gkxlumenx_dwd.industry_chain_news_event(event_id, chain_id, title, summary, news_type, source_name, publish_time) | 重大事件指标体系及阈值设定表 |
| 产业发展路线历程模型 | 事件时间线 | 事件总数 | 时间线中全部重大事件去重数。 | COUNT(DISTINCT 事件ID) 跨四类事件 | dwd_policy_base(id)；dwd_org_financing_info(org_id, completion_date)；demo_gkxlumenx_dwd.industry_chain_milestone_event(event_id)；demo_gkxlumenx_dwd.industry_chain_news_event(event_id) | 无 |
|  |  | 时间跨度(年) | 时间线首末事件的年份差。 | MAX(事件年) − MIN(事件年) | dwd_policy_base(publish_year)；dwd_org_financing_info(completion_date)；industry_chain_milestone_event(event_date)；industry_chain_news_event(publish_time) | 无 |
|  |  | 事件密度(件/年) | 平均每年重大事件数。 | 事件总数 ÷ 时间跨度 | 同上 | 无 |
| 产业发展路线历程模型 |  | 发展路线汇总 | 时间线 JSON 与事件总数汇总。 | 读取 timeline/total_events/year_span | gkxlumenx_ads.chain_roadmap(chain_id, chain_name, timeline, total_events, year_span, model_version) | 无 |

## 源表字段

- dwd_policy_base(id, title, publish_code, publish_date, publish_year, rank, type, theme, status, ministry) — 政策事件
- dwd_org_financing_info(org_id, name_cn, external_id, funding_round, funding_amount, completion_date, investors_name) — 投融资事件
- dwd_news_base(yqwyj, fbsj, lymc, lx, bt, zy, xgqyxx) — 资讯事件
- dwd_industry_chain_news_info(industry_code, industry_name, id, title, publish_date, abstract, source) — 产业资讯
- demo_gkxlumenx_dwd.industry_chain_milestone_event(event_id, chain_id, node_id, event_name, milestone_type, phase_name, event_date, event_level, region_code) — 里程碑事件
- demo_gkxlumenx_dwd.industry_chain_news_event(event_id, chain_id, node_id, title, summary, news_type, source_name, publish_time, region_code) — 归一化资讯事件
- demo_gkxlumenx_dwd.industry_chain_investment_event(event_id, chain_id, node_id, investment_type, financing_round, amount, currency, event_date, region_code) — 归一化投融资事件
- gkxlumenx_ads.chain_roadmap(chain_id, chain_name, timeline, total_events, year_span, model_version) — 路线历程汇总结果

## 待建字段

- 重大事件指标体系及阈值设定表（事件类型、关联指标、判定阈值、权重）——用于事件识别算法的阈值判定

## 参考资料

[1] 产业生命周期理论|Gort, M. & Klepper, S. (1982). Time Paths in the Diffusion of Product Innovations, The Economic Journal, 92(367), 630-653.

[2] 产业链供应链韧性与安全|工业和信息化部|产业链重大事件监测相关|https://www.miit.gov.cn/

[3] 中华人民共和国国民经济和社会发展统计公报|国家统计局|https://www.stats.gov.cn/sj/tjgb/ndtjgb/
