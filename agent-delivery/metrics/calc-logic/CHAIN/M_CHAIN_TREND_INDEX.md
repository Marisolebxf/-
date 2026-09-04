# 产业链变化趋势指数（M_CHAIN_TREND_INDEX）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_TREND_INDEX |
| 指标名称 | 产业链变化趋势指数 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 月度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

指定产业链在近期统计窗内的变化趋势综合指数，从企业增减、专利增速、资讯热度变化、投融资变化四因子加权评定，取值 0—100。分数越高表示产业链越趋向活跃扩张，越低表示收缩。口径与权重待甲方确认。

## 计算逻辑说明

采用加权平均。四因子：企业增减 / 专利增速 / 资讯热度变化 / 投融资变化。算法库「产业发展路线历程模型」（1.1.1.1.1.1.1.3.3）输出「产业发展趋势分析报告、趋势变化可视化」，要求「记录重大事件及发生时间节点，生成覆盖全产业发展历程的重大事件时间线」。趋势指数按四因子环比变化加权，默认等权（ΣW=1）。

### 第一步：四因子取值

- **企业增减**：`chain_enterprise_stat.growth_rate`（或 `enterprise_count` 环比）。
- **专利增速**：`dwd_org_industry_chain_pat_dtl` 按 `pbdt` 年度计数后的环比增速。
- **资讯热度变化**：`chain_news_stat.news_count`/`total_views` 环比变化。
- **投融资变化**：`chain_investment.amount_growth_rate`。

### 第二步：标准化与综合

各因子环比值 min-max 归一到 0—100：
$$
因子得分_{i} = \frac{x_i - \min(x)}{\max(x) - \min(x)} \times 100
$$
$$
产业链变化趋势指数 = \frac{1}{4}(企业增减得分 + 专利增速得分 + 资讯热度变化得分 + 投融资变化得分)
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业链变化趋势指数 | 企业增减 | 企业增减得分 | 链上企业数环比增速归一得分 | min-max(enterprise growth_rate) | chain_enterprise_stat(chain_id, stat_year, enterprise_count, growth_rate) — 企业增速 | 无 |
|  | 专利增速 | 专利增速得分 | 链上专利年度计数环比增速归一得分 | min-max(专利数环比增速) | dwd_org_industry_chain_pat_dtl(chain_code, node_id, pn, pbdt) — 专利年度计数 | 专利增速字段 |
|  | 资讯热度变化 | 资讯热度得分 | 链上资讯量/浏览量环比变化归一得分 | min-max(资讯量环比变化) | chain_news_stat(chain_id, stat_month, news_count, total_views, growth_rate) — 资讯热度 | 无 |
|  | 投融资变化 | 投融资变化得分 | 链上投融资金额环比增速归一得分 | min-max(amount_growth_rate) | chain_investment(chain_id, stat_year, total_amount, amount_growth_rate) — 投融资变化 | 无 |

## 源表字段

- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, high_tech_count, growth_rate) — 企业增减
- dwd_org_industry_chain_pat_dtl(chain_code, chain_name, node_id, pn, pbdt, apdt) — 专利增速（gkxlumenx_ods）
- chain_news_stat(chain_id, chain_name, stat_month, news_count, hot_count, total_views, growth_rate) — 资讯热度
- chain_investment(chain_id, chain_name, stat_year, investment_count, total_amount, amount_growth_rate) — 投融资变化
- chain_cycle(chain_id, chain_name, growth_rate, investment_trend, enterprise_trend, cycle_stage, trend) — 周期趋势（已有 trend）
- chain_roadmap(chain_id, chain_name, timeline, total_events, year_span) — 路线历程

## 待建字段

- 专利增速字段（`dwd_org_industry_chain_pat_dtl` 仅 gkxlumenx_ods，无结构化增速字段，需自算）
- 四因子权重与综合公式（待甲方确认）
- 趋势指数与 `chain_cycle.trend` 口径区分（周期趋势≠四因子综合趋势）

## 参考资料

[1] 产业发展路线历程模型｜科技专题服务算法库 1.1.1.1.1.1.1.3.3（产业发展趋势分析报告、趋势变化）。

[2] 产业趋势监测｜工业和信息化部｜产业运行监测与趋势指标体系（企业增减/专利增速/资讯热度/投融资变化四因子）。
