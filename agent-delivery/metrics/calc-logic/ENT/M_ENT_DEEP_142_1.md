# 企业发展历程模型（M_ENT_DEEP_142_1）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DEEP_142_1 |
| 指标名称 | 企业发展历程模型 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业发展 |
| 三级模块 | - |
| 更新频率 | 周 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 |

## 口径定义

按企业深度分析需规（算法库 §.5.2，ALGO-ENT-DEEP-142），采集企业并购、上市、股权变更、重大投资等重大事件，对超出阈值的指标认定为重大事件，按时间倒序生成企业重大事件时间线，用于刻画企业演进路径。对象=企业重大事件，粒度=企业。区别于 `M_ENT_DEV_HISTORY`（财务/专利/资讯三流 merge 的基础时间线），本条是带阈值判定的重大事件 MODEL。

## 计算逻辑说明

定义四类重大事件，分别识别后按 `event_time` 归并排序生成时间线。

### 第一步：事件识别

1. **并购事件**：企业作为并购发起方或标的发生并购；`ma_amount` 非空或并购公告 `ggrq` 非空即入。
2. **上市/融资事件**：`listing_status` 为已上市且 `listing_date` 非空；融资轮次 `finance_round` 非空。
3. **股权变更事件**：股东/持股结构发生变动（当前股东快照可作存量，变更历史需待建）。
4. **重大投资事件**：`investment_amount` 超出阈值（如 >1000 万元，阈值待配置）。

### 第二步：时间线

$$ Timeline = \bigcup_{k} \{ (org\_id, event\_time_k, event\_type_k, payload_k) \} \; ORDER \; BY \; event\_time \; DESC $$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 企业发展历程模型 | 并购事件 | 并购事件次数与时间 | 企业并购事件数及公告时间。 | COUNT(并购) / 事件时间线 | dwd_org_merger_acquisition_info(acquiring_org_id, acquired_org_id, ma_amount, currency_code, acquiring_name, acquired_name) — 并购主表；dwd_merger_acquisition_events_party_info(jgid, ggrq, dsrmc, dsrjslx, dsrlx, zbdzzzjid) — 并购事件当事人+公告日期 | 无 |
|  |  | 并购金额 | 并购交易金额。 | SUM(ma_amount) | dwd_org_merger_acquisition_info(acquiring_org_id, ma_amount, currency_code) — 并购金额(元) | 无 |
| 企业发展历程模型 | 上市/融资事件 | 上市日期 | 企业上市时间节点。 | listing_date | dwd_org_base_info(org_id, listing_status, listing_date, external_id) — 上市状态+上市日期 | 无 |
|  |  | 融资轮次事件 | 融资轮次、金额、投资方。 | 融资事件时间线 | enterprise_financing(org_id, finance_round, amount, currency, investors, event_date) — 融资轮次+金额+时间 | 无 |
| 企业发展历程模型 | 股权变更事件 | 股东结构变动 | 股东/持股比例变动。 | 股东变更时间线 | dwd_org_shareholder_info(org_id, inv_org_id, owners_name, ownership_percentage) — 股东+持股占比 | 股权变更历史表（现为当前快照，无变更日期） |
| 企业发展历程模型 | 重大投资事件 | 对外投资金额 | 企业对外投资金额分档。 | SUM(investment_amount) | dwd_org_invest_info(org_id, inv_org_id, inv_name, investment_amount, investment_ratio) — 对外投资金额+股权占比 | 重大事件阈值配置表 |

## 源表字段

- dwd_org_merger_acquisition_info(acquiring_org_id, acquired_org_id, ma_amount, currency_code, acquiring_name, acquired_name) — 并购主表
- dwd_merger_acquisition_events_party_info(jgid, ggrq, dsrmc, dsrjslx, dsrlx, zbdzzzjid) — 并购事件当事人+公告日期
- dwd_org_base_info(org_id, listing_status, listing_date, external_id) — 上市事件
- enterprise_financing(org_id, finance_round, amount, currency, investors, event_date) — 融资轮次事件（DWD）
- dwd_org_shareholder_info(org_id, inv_org_id, owners_name, ownership_percentage) — 股权结构
- dwd_org_invest_info(org_id, inv_org_id, inv_name, investment_amount, investment_ratio) — 对外投资

## 待建字段

- 股权变更历史表：现 `dwd_org_shareholder_info` 仅当前股东快照，无变更日期/前后值，无法构成「变更」时间线。
- 重大事件阈值配置表：并购/投资/融资的「重大」阈值（金额门槛）现无配置，待建。

## 参考资料

[1] 企业发展历程模型 | 算法库 §1.1.1.1.1.1.1.5.2 | 需求ID ALGO-ENT-DEEP-142 | 并购/上市/股权变更/重大投资 | 关联 Q009。

[2] 企业发展历程（基础时间线） | 王惠已入库指标 M_ENT_DEV_HISTORY（三流 merge；本条为其 MODEL 阈值升级版）。
