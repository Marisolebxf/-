# 技术创新趋势预测（M_INNOV_TINN_FORECAST）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_TINN_FORECAST |
| 指标名称 | 技术创新趋势预测 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 技术创新力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

对选定领域专利数量、专利质量、技术市场潜力的逐年件数做短期外推。输出未来各期点预测与约 80% 区间。不另建技术创新力时序表。综合得分是截面相对分，不直接外推。

## 计算逻辑说明

按 IPC 前 4 位入集技术领域。采用加权平均，三维：专利数量（年申请量）/ 专利质量（年被引）/ 技术市场潜力（年转移）。对逐年件数 Holt 外推，输出点预测与区间。

### 第一步：入集

页面年窗（拼装历史序列用，默认取有数据的首尾年）、空间（可选）、领域（IPC 前 4 位或关键词落到 `main_classification_ipcr`）。

专利：`dwd_patent` 按 `pn` 去重；领域键 = `main_classification_ipcr` 前 4 位。空间：`first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`。无命中不剔除领域，只缩小计入的专利。

一行一个 IPC4。

### 第二步：三个子项的年序列

对每个领域，按自然年对齐，缺年补 0。年键见下表。

1. **专利数量**  
   该年 `apdt_year` 落年的专利去重件数。

2. **专利质量**  
   该年申请专利在 `dwd_patent_cited` 的 `cited_by_nums` 合计。无被引行当 0。

3. **技术市场潜力**  
   该年 `transfer_effective_date` 落年、且 `pn` 属于该领域的转移专利去重件数。无转移行当 0。

有效期数 \($n=t_{\max}-t_{\min}+1$\)：\(n<8\) 不出预测，标记 `skip_reason=short_series`。

### 第三步：拟合与外推

短年序列默认 **Holt 线性趋势**（ETS(A,A,N)）。三维各自拟合，不先合成 0—100 分。

$$
\hat{y}_{T+k}=\ell+k\cdot b,\quad k=1,\ldots,h
$$

年频 \(h=2\)。点预测下限截到 0。业务指定 `algo=arima` 且 \(n≥12\) 时，用 AIC 选阶 ARIMA 替换 Holt，`algo` 写入结果。

页面展示综合趋势时，三维预测值先在本批领域内极值归一再等权平均；缺测维不补 0，剩余维权重重归一。

### 第四步：预测区间

训练残差标准差 \($\hat{\sigma}$\)，约 80% 区间（\(z_{0.9}\approx 1.28\)）：

$$
\left[\max(0,\hat{y}_{T+k}-1.28\hat{\sigma}\sqrt{k}),\ \hat{y}_{T+k}+1.28\hat{\sigma}\sqrt{k}\right]
$$

有效残差 < 5 时只出点预测，区间留空，标记 `interval=na`。

### 第五步：输出

一行一个领域一维一期：`ipc4`，维名，`period`，`yhat`，`yhat_lo`，`yhat_hi`，`algo`（`holt` / `arima`）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 技术创新趋势预测 | 专利数量 | 年申请量外推。 | Holt(年申请量) | dwd_patent(pn, main_classification_ipcr, apdt_year) — IPC领域,申请年 | 无 |
| 技术创新趋势预测 | 专利质量 | 年被引合计外推。 | Holt(年被引合计) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利去重,IPC领域,申请年 | 无 |
| 技术创新趋势预测 | 技术市场潜力 | 年转移专利外推。 | Holt(年转移专利数) | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, main_classification_ipcr) — IPC领域 | 无 |

## 源表字段

- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 趋势预测|Monash University|—|Hyndman R J, Athanasopoulos G. Forecasting: Principles and Practice[M]. 3rd ed. Melbourne: OTexts, 2021.
[2] 统计学习（聚类/预测）|Stanford University|—|James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning[M]. New York: Springer, 2013.

