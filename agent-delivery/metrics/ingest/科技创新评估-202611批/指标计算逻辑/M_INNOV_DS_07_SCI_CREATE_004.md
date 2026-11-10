# 科学创造力趋势预测（M_INNOV_DS_07_SCI_CREATE_004）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_07_SCI_CREATE_004 |
| 指标名称 | 科学创造力趋势预测 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 科学创造力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

对选定领域论文数量、网络中心性、科学研究前沿性的逐年件数做短期外推。输出未来各期点预测与约 80%置信区间。不另建科学创造力时序表，不用学者存量字段当年序列。综合得分是截面相对分，不直接外推。

## 计算逻辑说明

按题名关键词入集领域论文。采用加权平均，三维：论文数量（中英论文）/ 网络中心性（作者单位去重）/ 科学研究前沿性（当年新单位）。对逐年件数 Holt 外推，输出点预测与区间。

### 第一步：入集

页面年窗（拼装历史序列用，默认取有数据的首尾年）、空间（可选）、领域（题名/摘要关键词落到 `dwd_zh_paper`/`dwd_en_paper` 的 `zh_name`、`en_name`）。

论文按 `id` 去重；`cover_year_start` 为年键。作者单位来自 `dwd_zh_author`/`dwd_en_author.institution`。空间：`institution` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`。无命中不剔除领域，只缩小计入的论文。

不用 `dwd_scholar.paper_nums` 等存量字段：表内无入驻年，无法逐年外推。

一行一个领域。

### 第二步：三个子项的年序列

对每个领域，按自然年对齐，缺年补 0。

1. **论文数量**  
   该年中英文论文去重件数。

2. **网络中心性**  
   该年论文作者单位 `institution` 去重数（合作网络规模的可算代理，不建引文网络）。

3. **科学研究前沿性**  
   该年新出现的作者单位去重数：当年有、且前 3 个自然年未出现的 `institution`。无单位行当 0。

有效期数 \($n=t_{\max}-t_{\min}+1$\)：\(n<8\) 不出预测，标记 `skip_reason=short_series`。

### 第三步：拟合与外推

短年序列默认 **Holt 线性趋势**（ETS(A,A,N)）。三维各自拟合，不先合成 0—100 分。

$$
\hat{y}_{T+k}=\ell+k\cdot b,\quad k=1,\ldots,h
$$

年频 \(h=2\)。点预测下限截到 0。业务指定 `algo=arima` 且 \(n≥12\) 时，用 AIC 选阶 ARIMA 替换 Holt，`algo` 写入结果。

页面展示综合趋势时，三维预测值先在本批领域内极值归一再等权平均；缺测维不补 0，剩余维权重重归一。

### 第四步：预测区间

训练残差标准差 \($\hat{\sigma}$\)，约 80% 区间（$z_{0.9}\approx 1.28$）：

$$
\left[\max(0,\hat{y}_{T+k}-1.28\hat{\sigma}\sqrt{k}),\ \hat{y}_{T+k}+1.28\hat{\sigma}\sqrt{k}\right]
$$

有效残差 < 5 时只出点预测，区间留空，标记 `interval=na`。

### 第五步：输出

一行一个领域一维一期：领域键，维名，`period`，`yhat`，`yhat_lo`，`yhat_hi`，`algo`（`holt` / `arima`）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 科学创造力趋势预测 | 论文数量 | 年论文数外推。 | Holt(年论文数) | dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文去重,题名,发表年；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文去重,题名,发表年 | 无 |
| 科学创造力趋势预测 | 网络中心性 | 年作者单位去重外推。 | Holt(年作者单位去重) | dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 科学创造力趋势预测 | 科学研究前沿性 | 当年新出现作者单位外推。 | Holt(当年新单位数) | dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_zh_paper(id, cover_year_start) — 中文发表年；dwd_en_paper(id, cover_year_start) — 英文发表年 | 无 |

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
