# 监测趋势预测（M_INNOV_FACTOR_FORECAST）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_FACTOR_FORECAST |
| 指标名称 | 监测趋势预测 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

对会议、项目、专利、期刊四类科创要素的年度监测时序做短期外推。输出未来各期点预测与约 80% 区间。

## 计算逻辑说明

与要素聚类同一套对象：会议、项目、专利、期刊。本指标预测的是**逐年件数时序**，不预测影响力得分（得分是截面相对分，不能直接外推）。

### 第一步：确定监测对象与观测值

页面传入：`factor_type`（conference / project / patent / journal，可多选）、空间（`province`/`city`，可选）、统计频度（默认**年**）。

| factor_type | 序列主键 | 观测值 y_t | 年键 |
| --- | --- | --- | --- |
| conference | 切片整体（或按 `publication_id`） | 统计年会议论文去重件数 | `dwd_zh_paper`/`dwd_en_paper.cover_year_start`（`publication_type` 为 conference / 会议） |
| project | 切片整体（或按资助来源） | 统计年立项项目去重件数 | `dwd_zh_project`/`dwd_en_project.approval_year` |
| patent | 切片整体（或按 IPC 前 4 位） | 统计年专利去重件数 | `dwd_patent.apdt_year` |
| journal | 切片整体（或按 `publication_id`） | 统计年期刊论文去重件数 | `cover_year_start`（`publication_type` 为 journal / 期刊） |

空间过滤（有则用）：专利用 `first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`；论文用作者单位 `institution` 对齐 `name_cn`；项目用 `funded_province`。无命中不剔除对象，只缩小计入 y_t 的记录。

不用学者存量字段（`paper_nums` 等）当年序列：表内无入驻年，无法逐年外推。

### 第二步：拼装规则年序列

对每个监测对象，在首尾观测年之间按自然年对齐：

$$
\{(t,y_t)\}_{t=t_{\min}}^{t_{\max}}
$$

件数类缺年补 0（该年无新记录即 0 件）。有效期数 \(n=t_{\max}-t_{\min}+1\)：

- **n ≥ 8**：进入第三步；
- **n < 8**：该对象不出预测，标记 `skip_reason=short_series`。

### 第三步：拟合与外推

短年序列（常见 8—20 期）默认用 **Holt 线性趋势**（ETS(A,A,N)），比无约束 ARIMA 更稳。
$$

$$

$$
1. 用 \(y_{t_{\min}},\ldots,y_{t_{\max}}\) 拟合 Holt，得到水平 \(\ell\)、趋势 \(b\)。
2. 向前 \(h\) 期：年频 \(h=2\)，季/月频 \(h=4\)。
$$

1. 用 \(y_{t_{\min}},\ldots,y_{t_{\max}}\) 拟合 Holt，得到水平 \(\ell\)、趋势 \(b\)。
2. 向前 \(h\) 期：年频 \(h=2\)，季/月频 \(h=4\)。

$$
\hat{y}_{T+k}=\ell+k\cdot b,\quad k=1,\ldots,h
$$

点预测下限截到 0（件数不为负）。

备选：业务指定 `algo=arima` 且 \(n≥12\) 时，用 AIC 选阶的 ARIMA 替换 Holt，`algo` 写入结果。

### 第四步：预测区间

用训练残差标准差 \(\hat{\sigma}\) 给约 80% 区间（\(z_{0.9}\approx 1.28\)）：

$$
\left[\max(0,\hat{y}_{T+k}-1.28\hat{\sigma}\sqrt{k}),\ \hat{y}_{T+k}+1.28\hat{\sigma}\sqrt{k}\right]
$$

残差不足（有效残差 < 5）时只出点预测，区间留空，标记 `interval=na`。

### 第五步：输出

一行一个对象一期：`factor_type`，`factor_id`，`period`（未来年），`yhat`，`yhat_lo`，`yhat_hi`，`algo`（`holt` / `arima`）。不输出 0—100 分。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 监测趋势预测 | 点预测 | 未来各期件数中心值。 | Holt：\(\hat{y}_{T+k}=\ell+kb\)；备选 ARIMA | dwd_zh_journal(publication_id, publication_type) — 会议/期刊入集；dwd_en_journal(publication_id, publication_type) — 会议/期刊入集；dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文论文去重,发表年；dwd_zh_project(id, approval_year, funded_province) — 国内立项年,资助省；dwd_en_project(id, approval_year) — 国外立项年；dwd_patent(pn, apdt_year, first_applicant_name) — 专利去重,申请年,申请人对齐；dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 监测趋势预测 | 预测区间 | 约 80% 上下界。 | \(\hat{y}\pm 1.28\hat{\sigma}\sqrt{k}\) | 同上监测时序 — 残差与区间 | 无 |

## 源表字段

- dwd_zh_journal(publication_id, publication_type) — 会议/期刊入集,出版物类型
- dwd_en_journal(publication_id, publication_type) — 会议/期刊入集,出版物类型
- dwd_zh_paper(id, publication_id, publication_type, cover_year_start) — 中文论文去重,会议/期刊区分,发表年
- dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文论文去重,会议/期刊区分,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐
- dwd_zh_project(id, approval_year, funded_province) — 国内项目去重,立项年,资助省
- dwd_en_project(id, approval_year) — 国外项目去重,立项年
- dwd_patent(pn, apdt_year, first_applicant_name) — 专利去重,申请年,申请人对齐
- dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 统计学习（聚类/预测）|Stanford University|—|James G, Witten D, Hastie T, Tibshirani R. An Introduction to Statistical Learning[M]. New York: Springer, 2013.

[1]监测趋势预测｜南京大学信息管理系，中国科学技术信息研究所｜国家十一五支撑计划项目（2006BAH03B05）；国家自然科学基金项目（70673019）｜俞立平，潘云涛，武夷山. 基于因子分析的学术期刊评价指标分类研究[J]. 图书情报工作, 2009, 53(8): 146-149.

[2]监测趋势预测｜同济大学上海国际知识产权学院，国家知识产权局｜国家自然科学基金项目（71874122、71403188）；国家知识产权局软科学研究项目（SS16-B-06）；江苏省社会科学基金重点项目（20WTA-010）；同济大学研究生课程思政研究项目（2021KCSZYJ28）｜刘谦，姜南，王亚利，等. 国内高价值专利研究热点演进与整合框架——基于SKM的可视化分析[J]. 科技进步与对策, 2022, 39(21): 151-160.



