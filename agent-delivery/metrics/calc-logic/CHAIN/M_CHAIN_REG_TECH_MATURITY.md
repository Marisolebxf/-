# 区域技术成熟度（M_CHAIN_REG_TECH_MATURITY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_TECH_MATURITY |
| 指标名称 | 区域技术成熟度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上，以该区域链上企业专利按公开年汇总的近3年复合增速判定技术所处生命周期位置，输出0—100分。分值越高表示技术越趋近成熟（公开量增速趋缓）；持续负增长按衰退回落计分。口径对齐M_CHAIN_TECH_MATURITY_SCORE，仅增加区域筛选。不采用产品去重代理，也不输出TRL等级。

## 计算逻辑说明

时间戳用公开年 `pbdt_year`。窗口长度 \(k\) 优先取3，不足3年有2年则取2，仅1年才退回单年同比。

第一步：定区域链上专利

从 `dwd_industry_chain_info` 按 `industry_code` 取目标产业链。关联 `dwd_org_industry_tags` 取链上企业（`credit_code`、`company_name`）。用 `credit_code` 关联 `dwd_org_base_info`，按 `province`/`city` 筛目标区域。专利按 `first_applicant_name` 或 `first_current_assignee_name` 与 `company_name` 匹配，按 `patent_id` 去重。不要求已授权：公开年反映技术被披露的时点；若只留 `granted_number` 非空再按公开年计数，近两年发明专利会因审查未结而右截断，把最新增速压低，误判成熟或衰退。

第二步：年度公开量

对统计年 \(t\)、目标区域：
$$
P_t = \text{COUNT(DISTINCT patent\_id WHERE pbdt\_year}=t)
$$

第三步：近 \(k\) 年复合增速

$$
g_t =
\begin{cases}
\left(\dfrac{P_t}{P_{t-k}}\right)^{1/k}-1, & P_{t-k}>0 \\
\text{萌芽（无上期基数）}, & P_{t-k}=0,\ P_t>0 \\
\text{无公开}, & P_{t-k}=0,\ P_t=0
\end{cases}
$$

上期增速 \(g_{t-k}\) 用同一窗口回算，供加速/减速判定。缺上期增速时，不判减速。

第四步：阶段判定与评分映射

记近零阈值 \(\theta=5\%\)。评分越高表示越趋近成熟。映射与M_CHAIN_TECH_MATURITY_SCORE相同。

| 判定条件 | 技术阶段 | 评分 |
| --- | --- | --- |
| \(P_t=0\) 且 \(P_{t-k}=0\) | 无公开 | 0 |
| \(P_{t-k}=0\) 且 \(P_t>0\) | 萌芽 | 25 |
| \(g_t>\theta\) 且（缺 \(g_{t-k}\) 或 \(g_t\ge g_{t-k}\)） | 成长 | 50 |
| \(g_t>\theta\) 且 \(g_t<g_{t-k}\) | 趋于成熟 | 70 |
| \(\lvert g_t\rvert\le\theta\) | 成熟 | 90 |
| \(g_t<-\theta\) | 衰退 | \(90\times P_t/P_{t-k}\)，截断到 \([0,90)\) |

衰退评分按公开量相对上期窗口的回落比例从成熟分下探。\(\theta\) 默认 5%。

| 指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- |
| 区域技术成熟度 | 区域链上企业专利按公开年近 \(k\) 年复合增速所对应的生命周期评分 | dwd_org_base_info(province, city); dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, pbdt_year) | 无 |

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配专利权人
- dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市(区域筛选)
- dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, pbdt_year) — 专利去重, 申请人匹配, 专利权人匹配, 公开年(年度公开量)

## 待建字段

- 无

## 参考文献

[1]区域技术成熟度｜Ernst, H. The Use of Patent Data for Technological Forecasting: The Diffusion of CNC-Technology in the Machine Tool Industry[J]. Small Business Economics, 1997, 9(4): 361-381. DOI: 10.1023/A:1007921808138.

[2]区域技术成熟度｜Haupt, R., Kloyer, M., Lange, M. Patent indicators for the technology life cycle development[J]. Research Policy, 2007, 36(3): 387-398. DOI: 10.1016/j.respol.2006.12.004.
