# 产业热点领域识别模型（M_CHAIN_DEEP_120_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_120_1 |
| 指标名称 | 产业热点领域识别模型 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 月度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

通过对接资讯数据库与投融资/企业增量数据，基于市场份额、行业增长率、竞争格局等热点指标与阈值，利用热点识别算法对目标产业动态进行分析，实时识别并跟踪产业热点领域。对象=产业细分热点领域，评分取值 0—100，分数越高热点越显著。

## 计算逻辑说明

三步：① 数据采集：资讯（`chain_news`/`dwd_industry_chain_news_info`）、投融资（`chain_investment`）、新企业增量（`chain_enterprise_stat`）。② 子评分：资讯热度分（news_freq_score，按资讯量/浏览量）、资本热度分（investment_score，按投融资额）、市场热度分（enterprise_growth_score，按新进入企业增长）。③ 综合：三子分加权得 hotspot_score，超过阈值标 is_hot，并输出 hot_news 与排名 rank_overall。

- 资讯热度分 = 归一化(资讯数量, 热点资讯数)
- 资本热度分 = 归一化(投融资事件数, 投融资总额)
- 市场热度分 = 归一化(新进入企业数, 增长率)
- 热点综合分 hotspot_score = Σ(Wi × 子评分)

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业热点领域识别模型 | 资讯热度 | 资讯数量 | 统计期内产业相关资讯去重数。 | COUNT(DISTINCT news_id) | chain_news(news_id, chain_id, chain_name, title, summary, views, is_hot, publish_time)；dwd_industry_chain_news_info(id, industry_code, title, publish_date, abstract)；gkxlumenx_ads.chain_news_stat(chain_id, chain_name, stat_month, news_count, hot_count, total_views, growth_rate) | 无 |
|  |  | 热点资讯数 | 被标注为热点或浏览量超阈值的资讯数。 | COUNT(DISTINCT news_id) WHERE is_hot=1 OR views≥阈值 | chain_news(news_id, views, is_hot)；chain_news_stat(hot_count) | 热点阈值参数表 |
| 产业热点领域识别模型 | 资本热度 | 投融资事件数 | 统计期内产业投融资事件去重数。 | COUNT(DISTINCT investment_id) | chain_investment(investment_id, chain_id, enterprise_name, round, amount, invest_date)；dwd_org_financing_info(org_id, funding_round, funding_amount, completion_date) | 无 |
|  |  | 投融资总额 | 统计期内产业投融资金额合计。 | SUM(amount) | chain_investment(amount)；gkxlumenx_ads.chain_investment(chain_id, chain_name, stat_year, investment_count, total_amount, amount_growth_rate, count_growth_rate) | 无 |
| 产业热点领域识别模型 | 市场热度 | 市场份额 | 该产业营收/企业占全部产业比重。 | 产业营收 ÷ 全部产业营收合计 | chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate) | 市场份额指标表（全产业分母口径） |
|  |  | 行业增长率 | 产业营收/企业数量同比增速。 | (本期 − 上期) ÷ 上期 | chain_market(growth_rate)；chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, growth_rate) | 无 |
|  |  | 竞争格局(新进入企业数) | 统计期内新进入该产业的企业数量。 | COUNT(DISTINCT enterprise_id) WHERE 新进入 | chain_enterprise_stat(enterprise_count, growth_rate)；dwd_org_base_info(incorporation_year) | 无 |
| 产业热点领域识别模型 | 热点判定 | 热点综合分 | 三子评分加权后的热点综合得分。 | Σ(Wi × 子评分)，超阈值 is_hot | gkxlumenx_ads.chain_hotspot(chain_id, chain_name, news_count, investment_total, new_enterprise_count, news_freq_score, investment_score, enterprise_growth_score, hotspot_score, is_hot, hot_news, rank_overall) | 热点权重与阈值参数表 |

## 源表字段

- chain_news(news_id, chain_id, chain_name, enterprise_id, enterprise_name, news_type, type_name, title, summary, views, is_hot, publish_time, data_year, data_month) — 产业资讯
- dwd_industry_chain_news_info(industry_code, industry_name, id, title, publish_date, abstract, source) — 产业资讯 ODS
- dwd_news_base(yqwyj, fbsj, lymc, lx, bt, zy, xgqyxx) — 全网资讯
- chain_investment(investment_id, chain_id, chain_name, enterprise_id, enterprise_name, round, amount, investor, invest_date, data_year) — 投融资明细
- dwd_org_financing_info(org_id, name_cn, funding_round, funding_amount, completion_date, investors_name) — 融资事件
- chain_market(chain_id, chain_name, stat_year, total_revenue, enterprise_count, growth_rate) — 市场规模与增长率
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, high_tech_count, growth_rate) — 企业数量与增长
- dwd_org_base_info(org_id, name_cn, incorporation_year, city, province) — 企业成立年（新进入判定）
- gkxlumenx_ads.chain_news_stat(chain_id, chain_name, stat_month, news_count, hot_count, total_views, growth_rate) — 资讯月度统计
- gkxlumenx_ads.chain_hotspot(chain_id, chain_name, news_count, investment_total, new_enterprise_count, news_freq_score, investment_score, enterprise_growth_score, hotspot_score, is_hot, hot_news, rank_overall) — 热点识别结果

## 待建字段

- 市场份额指标表（全产业分母口径：产业营收 ÷ 全产业营收合计）
- 竞争格局/行业集中度指标表（HHI 或 CR4，需企业营收份额明细）
- 热点识别权重与阈值参数表

## 参考资料

[1] 舆情与热点监测相关方法|国家统计局社科文司|中国创新指数指标体系|https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1900165.html

[2] 区域创新能力监测指标体系|科学技术部|https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110674.html

[3] 市场集中度（HHI/CR4）测算方法|国务院反垄断委员会|《关于相关市场界定的指南》|https://www.samr.gov.cn/
