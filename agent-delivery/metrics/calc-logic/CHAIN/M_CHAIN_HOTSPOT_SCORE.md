# 热点综合评分（M_CHAIN_HOTSPOT_SCORE）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_HOTSPOT_SCORE |
| 指标名称 | 热点综合评分 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 周 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

指定产业链/环节在统计窗内的热度综合评分，从企业增速、投融资热度、专利密度、资讯热度四维加权评定，取值 0—100。分数越高表示该产业链/环节越热。评分维度与权重待甲方确认。

## 计算逻辑说明

采用加权平均。四维：企业增速 / 投融资热度 / 专利密度 / 资讯热度。算法库「产业热点领域识别模型」（1.1.1.1.1.1.1.3.4）定义热点指标（行业增长率、市场份额、竞争格局等）并设定阈值，但未冻结权重；seed 公式为四维加权，默认等权（ΣW=1），甲方可改。

### 第一步：入集

按 `chain_id`（或 `node_id`）定对象，取各维原始值。

### 第二步：四维标准化

各维原始值 min-max 归一到 0—100：
$$
维度得分_{i} = \frac{x_i - \min(x)}{\max(x) - \min(x)} \times 100
$$

- **企业增速**：`chain_enterprise_stat.growth_rate`。
- **投融资热度**：`chain_investment.investment_count`/`total_amount` 归一。
- **专利密度**：环节专利数（`dwd_org_industry_chain_pat_dtl` 聚合）÷ 环节企业数。
- **资讯热度**：`chain_news_stat.hot_count`/`news_count` 归一。

### 第三步：综合评分

$$
热点综合评分 = \sum_{k=1}^{4} W_k \times 维度得分_k
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 热点综合评分 | 企业增速 | 企业增速得分 | 新增企业增速归一得分 | min-max(enterprise_growth_rate) | chain_enterprise_stat(chain_id, stat_year, enterprise_count, growth_rate) — 企业增速；chain_hotspot(chain_id, enterprise_growth_score) — 企业增速分 | 无 |
|  | 投融资热度 | 投融资热度得分 | 融资事件/金额归一得分 | min-max(investment_total/count) | chain_investment(chain_id, stat_year, investment_count, total_amount) — 投融资；chain_hotspot(chain_id, investment_score) — 投融资分 | 无 |
|  | 专利密度 | 专利密度得分 | 环节专利密度归一得分 | min-max(专利数/企业数) | dwd_org_industry_chain_pat_dtl(chain_code, node_id, pn) — 环节专利；chain_enterprise(chain_id, enterprise_id) — 环节企业 | 专利密度分字段 |
|  | 资讯热度 | 资讯热度得分 | 热点资讯占比/浏览量归一得分 | min-max(hot_count/news_count) | chain_news_stat(chain_id, news_count, hot_count, total_views) — 资讯热度；chain_hotspot(chain_id, news_freq_score) — 资讯频率分 | 无 |

## 源表字段

- chain_hotspot(chain_id, chain_name, news_freq_score, investment_score, enterprise_growth_score, hotspot_score, is_hot, rank_overall) — 已有三维得分与综合分（gkxlumenx_ads / demo_gkxlumenx_ads）
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, growth_rate) — 企业增速
- chain_investment(chain_id, chain_name, stat_year, investment_count, total_amount) — 投融资热度
- chain_news_stat(chain_id, chain_name, stat_month, news_count, hot_count, total_views) — 资讯热度
- dwd_org_industry_chain_pat_dtl(chain_code, chain_name, node_id, pn, pbdt) — 专利密度

## 待建字段

- 专利密度得分字段（现 `chain_hotspot` 仅三维：资讯/投融资/企业增速，缺专利密度维）
- 四维权重（待甲方确认）
- 环节级热点综合分字段（现多为产业链粒度）

## 参考资料

[1] 产业热点领域识别模型｜科技专题服务算法库 1.1.1.1.1.1.1.3.4（热点指标与阈值）。

[2] 产业热度综合评价｜工业和信息化部｜产业运行监测指标体系（企业增速/投融资/专利密度/资讯热度四维加权）。
