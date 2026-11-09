# 创新影响预测（M_INNOV_IMPACT_FORECAST）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_IMPACT_FORECAST |
| 指标名称 | 创新影响预测 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 全球创新实时数据 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

对与创新影响分数同一套实体，预测其未来产出件数及对同类总体的贡献度。输出点预测、约 80% 区间与贡献度。

## 计算逻辑说明

影响分数是截面相对分，不能直接外推。本指标预测**逐年产出件数**，实体集合与 `M_INNOV_IMPACT_SCORE` 一致。

### 第一步：拼装年序列

| entity_type | 观测值 y_t | 年键 |
| --- | --- | --- |
| org | 该年专利去重件数 + 中英文论文去重件数 | 专利 `apdt_year`；论文 `cover_year_start` |
| domain | 该 IPC4 下专利去重件数 | `apdt_year` |

首尾观测年之间按自然年对齐，缺年补0（仅适用于当年新增计数型指标，org年专利申请量、domain年专利量）。有效期数 `n`：若 `n < 8`，不出预测，标记 `skip_reason=short_series`。

### 第二步：点预测（默认 Holt）

用 \($y_{t_{\min}},\ldots,y_{t_{\max}}$\) 拟合 Holt 线性趋势，年频向前 \(h=2\) 期：

$$
\hat{y}_{T+k}=\ell+k\cdot b,\quad k=1,2
$$

下限截到 0。业务指定且 `n≥12` 时可用 AIC 选阶 ARIMA 替换 Holt。ARIMA 搜索范围限制：`p ≤ min(3, floor(n/4))`，`d ∈ {0,1,2}`，`q ≤ min(3, floor(n/4))`。若 ARIMA 的 AIC 低于 Holt 的 AIC 则选用 ARIMA，否则仍用 Holt。`algo` 写入结果（`holt` / `arima`）。

### 第三步：区间与贡献度

残差标准差 \(\hat{\sigma}\)，约 80% 区间：

$$
\left[\max(0,\hat{y}_{T+k}-1.28\hat{\sigma}\sqrt{k}),\ \hat{y}_{T+k}+1.28\hat{\sigma}\sqrt{k}\right]
$$

残差 < 5 时只出点预测，区间留空。标记 `interval=na`。增加 `interval_quality` 字段：残差 ≥5 时为 `normal`，<5 时为 `low`。

同类实体（同一 `entity_type`）贡献度：

$$
贡献度_{i,T+k}=\frac{\hat{y}_{i,T+k}}{\sum_j \hat{y}_{j,T+k}}
$$

分母为 0 时，所有实体贡献度返回 0（非空值）。输出中增加 `contrib_scope` 字段，取值为 `global`（全局同类实体）。

### 第四步：输出

一行一个实体一期：

| 字段             | 含义                             |
| :--------------- | :------------------------------- |
| entity_type      | 实体类型（org / domain）         |
| 主键             | 实体主键（org_id / IPC4）        |
| period           | 预测期（年）                     |
| yhat             | 点预测值                         |
| yhat_lo          | 区间下界                         |
| yhat_hi          | 区间上界                         |
| contrib          | 贡献度（同类实体预测值占比）     |
| contrib_scope    | 贡献度分母范围（`global`）       |
| algo             | `holt` / `arima`                 |
| rmse_train       | 训练集RMSE（拟合质量指标）       |
| mae_train        | 训练集MAE（拟合质量指标）        |
| interval_quality | `normal` / `low`（区间质量标记） |

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新影响预测 | 点预测 | 未来各期产出件数。 | Holt：\($\hat{y}_{T+k}=\ell+kb$\) | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利年序列,申请人对齐,IPC领域；dwd_zh_paper(id, cover_year_start) — 中文论文年序列；dwd_en_paper(id, cover_year_start) — 英文论文年序列；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 创新影响预测 | 预测区间 | 约 80% 上下界。 | \($\hat{y}\pm 1.28\hat{\sigma}\sqrt{k}$\) | 同上监测时序 — 残差与区间 | 无 |
| 创新影响预测 | 贡献度 | 该实体预测件数占同类合计的比例。 | \($\hat{y}_i/\sum\hat{y}_j$\) | 同上点预测结果 — 贡献度 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, province, city) — 机构对齐,空间过滤
- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

- 无

## 参考资料

创新影响预测｜Stanford University，University of Washington，University of Southern California｜James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning: with Applications in R[M]. New York: Springer, 2013. ISBN: 978-1-4614-7137-0.
