# 关系强度（M_ENT_RELATION_STRENGTH）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_RELATION_STRENGTH |
| 指标名称 | 关系强度 |
| 一级模块 | 企业分析 |
| 二级模块 | 风险洞察 |
| 三级模块 | - |
| 更新频率 | 月度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 / Q017 |

## 口径定义

企业间关系紧密度，以投资金额分档代理关系强度——>1亿元=强 / 1000万~1亿元=中 / <1000万元=弱；有 `chain_score`（产业链评分）时作辅证。对象=企业间关系（边），粒度=关系对。口径 Q017 临时默认闭合（2026-08-11）。

## 计算逻辑说明

主口径为投资金额分档，辅证为供应链关系强度与产业链评分。

### 第一步：投资金额分档

$$ Strength =
\begin{cases}
\text{强} & investment\_amount > 1\,亿元 \\
\text{中} & 1000\,万 \leq investment\_amount \leq 1\,亿元 \\
\text{弱} & investment\_amount < 1000\,万
\end{cases}
$$

金额单位以 `investment_amount` 元为准（需与 `enterprise_invest.investment_amount` 统一）。

### 第二步：辅证

- 供应链 `enterprise_supply_chain.relation_strength` 直接给关系强度；
- `enterprise_industry_chain.chain_score` 作产业链协同辅证。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 关系强度 | 投资关系强度 | 对外投资金额分档 | 投资金额分档代理关系强度。 | >1亿强/1000万~1亿中/<1000万弱 | dwd_org_invest_info(org_id, inv_org_id, inv_name, investment_amount, investment_ratio) — 对外投资金额(元)+股权占比 | 投资金额单位统一映射 |
|  |  | 股权占比强度 | 股权投资比例作关系强度辅证。 | investment_ratio 分档 | dwd_org_invest_info(org_id, inv_org_id, investment_amount, investment_ratio) — 股权占比(%)；enterprise_invest(org_id, inv_org_id, investment_amount, investment_ratio, event_date) — 投资（DWD） | 股权占比分档阈值 |
| 关系强度 | 供应链关系强度 | 供应链 relation_strength | 供应链关系紧密度（辅证）。 | relation_strength | enterprise_supply_chain(org_id, related_org_id, relation_type, relation_strength, is_core_supplier, risk_level) — 供应链关系强度 | 无 |
|  |  | 产业链评分辅证 | 产业链协同评分作关系强度辅证。 | chain_score | enterprise_industry_chain(org_id, chain_code, chain_name, node_id, node_name, is_chain_leader, chain_score) — 产业链评分 | 无 |

## 源表字段

- dwd_org_invest_info(org_id, inv_org_id, inv_name, investment_amount, investment_ratio) — 对外投资金额(元)+股权占比
- enterprise_invest(org_id, inv_org_id, inv_name, investment_amount, investment_ratio, event_date) — 投资关系（DWD）
- enterprise_supply_chain(org_id, related_org_id, relation_type, relation_strength, is_core_supplier, risk_level) — 供应链关系强度（DWD）
- enterprise_industry_chain(org_id, chain_code, chain_name, node_id, node_name, is_chain_leader, chain_score) — 产业链评分（DWD）

## 待建字段

- 投资金额单位统一映射：`dwd_org_invest_info.investment_amount`（元）与 `enterprise_invest.investment_amount` 单位需统一，避免分档错档。
- 分档阈值配置表：>1亿/1000万~1亿/<1000万 阈值现无配置表，待建（Q017 正式闭合）。

## 参考资料

[1] 企业供应链关系分析模型 | 算法库 §1.1.1.1.1.1.1.5.4 | 需求ID ALGO-ENT-DEEP-144 | 关系紧密度 | 关联 Q009 / Q017。

[2] 供应链图谱构建与多级下钻 | 需规 SRS《企业分析.md》序号53 | 供应商/客户/合作伙伴关系。
