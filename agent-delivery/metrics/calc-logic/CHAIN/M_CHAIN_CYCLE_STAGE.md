# 产业周期阶段（M_CHAIN_CYCLE_STAGE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_CYCLE_STAGE |
| 指标名称 | 产业周期阶段 |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业周期分析 |
| 三级模块 | 周期阶段判定 |
| 更新频率 | 年 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q053+QC03 |


## 口径定义

指定产业链在统计年度所处的生命周期阶段。只用国内年报，输出导入期、成长期、成熟期、衰退期之一；样本不足则不输出阶段。导入期对应算法库起始期。本指标与 `M_CHAIN_PHASE_DETERMINATION` 不是同一套算法。

## 计算逻辑说明

从 `dwd_industry_chain_info` 按 `industry_code` 定链。关联 `dwd_org_industry_tags` 取链上企业（`credit_code`）。`credit_code` 关联 `dwd_org_annual_financial_info.external_id`，按 `year` 取年报。只保留 `operating_revenue` 非空且大于 0 的企业；`total_profit` 空值按 0。不使用 `dwd_forg_base_info`、`dwd_foreign_org_annual_financial_info`（海外 `org_id` 对不上 tags，`occur_period` 不是年，且无币种，不能与人民币营收加总）。

本指标自算 \(S\)、\(g\)、\(m\)。窗口长度 \(k\) 优先 3，不足 3 年有 2 年则取 2，仅 1 年才退回单年。近零阈值 \($\theta=5\%$\)，甲方可改。

**第一步：市场规模**
$$
S_t = \sum operating\_revenue
$$
$S_t=0$或该年无有效企业，判定为样本不足。\(S_t\) 只作有效样本门槛，不再做「规模升降交叉校验」。

**第二步：可比同比与滚动增速**

相邻两年都有营收 \(>0\) 的同一批 `credit_code` 为可比企业。不可比企业不进同比，避免覆盖扩容/退库当成行业涨跌。
$$
g_t = \frac{\sum_{i\in C_t} operating\_revenue_{i,t}}{\sum_{i\in C_t} operating\_revenue_{i,t-1}} - 1
$$
其中$ C_t 为 t与 t-1 $都有有效营收的企业集合。集合为空或分母为 0，则$ g_t $缺失。

\($\tilde g_t$\) = 近 \(k\) 个可算出的年度同比$ g_t,g_{t-1},\ldots$ 的算术平均。近 \(k\) 年同比全部缺失则样本不足。

**第三步：滚动利润率**

同一窗口年$ \{t,t-1,\ldots,t-k+1\}$ 内，全部有效企业：
$$
\tilde m_t = \frac{\sum total\_profit}{\sum operating\_revenue}
$$
分母为 0 则样本不足。

第四步：四阶段

| 条件 | 阶段 |
| --- | --- |
| $\tilde g_t 缺失，或 S_t=0$ | 样本不足（不输出阶段） |
| $\tilde g_t < -\theta$ | 衰退期 |
| $\tilde g_t > \theta 且 \tilde m_t \le 0$ | 导入期 |
| $\tilde g_t > \theta 且 \tilde m_t > 0$ | 成长期 |
| $\lvert \tilde g_t\rvert \le \theta$ | 成熟期 |

$\tilde g_t=0$ 落在成熟期。不再用$ \tilde g_t $相对上期升降区分成长/成熟（减速仍可能是高增长，不应当作成熟）。

| 一级指标 | 二级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| 产业周期阶段 | 市场规模 | 国内链上企业统计年营收合计，仅作有效样本门槛 | dwd_org_annual_financial_info(operating_revenue, year) | 无 |
| | 行业增长率 | 可比企业同比再滚动平均，主判定；$\lvert \tilde g\rvert\le\theta $为成熟 | dwd_org_annual_financial_info(operating_revenue, year) | 无 |
| | 利润率 | 近 \(k\) 年利润合计/营收合计，切分导入与成长 | dwd_org_annual_financial_info(total_profit, operating_revenue, year) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联
- dwd_org_annual_financial_info(external_id, year, operating_revenue, total_profit) — 信用代码关联, 年报年度, 营业收入, 利润总额

## 待建字段

- 无

## 参考文献

- 产业周期阶段｜东南大学经济管理学院｜国家自然科学基金项目（71173116）；教育部哲学社会科学发展报告项目（13JBG004）｜季良玉, 李廉水. 中国制造业产业生命周期研究——基于1993—2014年数据的分析[J]. 河海大学学报(哲学社会科学版), 2016, 18(1): 30-37. DOI: 10.3876/j.issn.1671-4970.2016.01.007.
