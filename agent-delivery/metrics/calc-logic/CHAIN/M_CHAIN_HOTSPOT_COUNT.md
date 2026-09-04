# 热点/历程事件数（M_CHAIN_HOTSPOT_COUNT）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_HOTSPOT_COUNT |
| 指标名称 | 热点/历程事件数 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 周 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

指定产业链内，基于企业增速、投融资热度、专利密度综合评分达到阈值的产业链/环节（热点领域）去重数。对象=热点领域（环节），不是热点资讯条数。阈值与权重待甲方确认。

## 计算逻辑说明

算法库「产业热点领域识别模型」（1.1.1.1.1.1.1.3.4，约 468–479 行）要求「依据产业特征定义市场份额、行业增长率、竞争格局等热点指标，设定阈值，利用热点识别算法锁定热点领域，输出产业热点领域列表」。据此以三路信号识别热点环节，达阈则计为热点领域。

### 计算步骤

1. 按 `chain_id` 定链，逐环节计算三个信号：企业增速（新增企业增速）、投融资热度（融资事件/金额）、专利密度（环节专利数/企业数）。
2. 各信号 min-max 归一后加权得热点综合分（权重待甲方）。
3. 综合分 ≥ 阈值的环节去重计数。

$$
热点领域数 = COUNT(DISTINCT 环节 \mid 热点综合分 \ge 阈值)
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 热点/历程事件数 | 企业增速 | 新增企业增速热点环节数 | 企业增速超阈值的环节去重数 | COUNT(DISTINCT 环节 WHERE 企业增速≥阈值) | chain_enterprise_stat(chain_id, stat_year, enterprise_count, growth_rate) — 企业增速；chain_hotspot(chain_id, new_enterprise_count) — 新增企业 | 环节级企业增速字段 |
|  | 投融资热度 | 投融资热度热点环节数 | 融资事件/金额超阈值的环节去重数 | COUNT(DISTINCT 环节 WHERE 融资热度≥阈值) | chain_investment(chain_id, investment_count, total_amount, amount_growth_rate) — 投融资；chain_hotspot(chain_id, investment_total) — 投融资金额 | 环节级融资字段 |
|  | 专利密度 | 专利密度热点环节数 | 环节专利密度超阈值的去重数 | COUNT(DISTINCT 环节 WHERE 专利密度≥阈值) | dwd_org_industry_chain_pat_dtl(chain_code, node_id, pn, pbdt) — 环节专利；chain_enterprise(chain_id, enterprise_id) — 环节企业 | 环节级专利密度字段 |

## 源表字段

- chain_hotspot(chain_id, chain_name, news_count, investment_total, new_enterprise_count, hotspot_score, is_hot, rank_overall) — 热点识别结果（gkxlumenx_ads / demo_gkxlumenx_ads，已有 is_hot/hotspot_score）
- chain_enterprise_stat(chain_id, chain_name, stat_year, enterprise_count, high_tech_count, growth_rate) — 企业增速
- chain_investment(chain_id, chain_name, stat_year, investment_count, total_amount, amount_growth_rate) — 投融资热度
- chain_news_stat(chain_id, chain_name, stat_month, news_count, hot_count, total_views) — 资讯热度
- dwd_org_industry_chain_pat_dtl(chain_code, chain_name, node_id, pn, pbdt, apno) — 环节专利（gkxlumenx_ods）

## 待建字段

- 环节级企业增速、融资、专利密度字段（现多为产业链粒度）
- 热点判定阈值与三路信号权重（待甲方确认）
- 去重「热点环节数」字段（现 `chain_hotspot` 为产业链粒度，缺环节粒度热点计数）

## 参考资料

[1] 产业热点领域识别模型｜科技专题服务算法库 1.1.1.1.1.1.1.3.4（热点指标与阈值、热点领域列表）。

[2] 产业热点监测｜工业和信息化部｜产业运行监测与热点识别指标体系（企业增速/投融资热度/专利密度）。
