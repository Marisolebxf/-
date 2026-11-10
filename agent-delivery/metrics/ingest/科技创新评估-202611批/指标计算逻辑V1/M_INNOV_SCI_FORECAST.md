# 科学创造力趋势预测（M_INNOV_SCI_FORECAST）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_SCI_FORECAST |
| 指标名称 | 科学创造力趋势预测 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 科学创造力指标展示 |
| 口径版本 | V2.0-20261108 |
| 更新频率 | 待确认（pending） |

## 口径定义

同 **M_INNOV_DS_07_SCI_CREATE_004（科学创造力趋势预测）**

## 计算逻辑说明

本指标与 **M_INNOV_DS_07_SCI_CREATE_004（科学创造力趋势预测）** 为同一口径，完整步骤与公式见该指标。要点：

- 对论文数量、网络中心性、科学研究前沿性三组**逐年件数**分别拟合 Holt 线性趋势（ETS(A,A,N)），不先合成 0—100 分再外推。
- 有效年数 n<8 不出预测，标 `skip_reason=short_series`；年频默认 h=2，点预测下限截到 0。
- 展示综合趋势时，三维预测值先在本批领域内极值归一，再等权平均；缺测维不补 0，剩余维重新归一。
- 区间取约 90%（z=0.9≈1.645），有效残差<5 时区间留空并标 `interval=na`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 科学创造力趋势预测 | 预测得分 | 未来第 h 期的三维件数预测值与综合趋势预测值。 | Holt：ŷ(t+h)=l(t)+h×b(t)，α、β 以最小化 SSE 确定 | dwd_zh_paper(id, cover_year_start)；dwd_en_paper(id, cover_year_start)；dwd_zh_author(paper_id, institution)；dwd_en_author(paper_id, institution) | 无 |
| 科学创造力趋势预测 | 置信区间宽度 | 预测区间上下界之差。 | 宽度 = 2×1.645×σ̂ = 3.29σ̂，σ̂ 为训练残差标准差 | 同上 | 无 |

## 源表字段

- dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文去重,题名入集,发表年
- dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文去重,题名入集,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 趋势预测|Monash University|—|Hyndman R J, Athanasopoulos G. Forecasting: Principles and Practice[M]. 3rd ed. Melbourne: OTexts, 2021.
[2] 统计学习（聚类/预测）|Stanford University|—|James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning[M]. New York: Springer, 2013.
