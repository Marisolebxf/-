# METRIC-OPEN-ENT-COMPARE-核对记录

> **任务**：`ENT-MOD-COMPARE-METRIC-OPEN-L01`（**done**，本文件补磁盘缺口，**不改**任务状态）
> **日期**：2026-08-22（`METRIC-OPEN-DEBT-L01` 乙表收口）
> **角色**：algorithm-agent + data-agent（历史派单）；本工作流口径主责 `human:淮政玮`；公式共签 `human:唐绍祖`
> **上游 PACK**：`ENT-MOD-COMPARE-PACK-L01` ✅ done
> **本文件角色**：五件套 #4/#5 适用性书面依据。A2/catalog **不得**再因「磁盘无核对记录」把对比篮标成缺 OPEN 叶。禁止另开平行 OPEN。

---

## §1 适用性结论（Track-MS #4 / #5）

| 五件套项 | 状态 | 依据 |
|----------|------|------|
| #4 指标语义卡 | **N/A**（有据） | TRACE `metrics_required: 0` · `statistical_metrics_required: 0`；Decision 088：对比篮是派生暂存/分发容器，**不拥有**竞争力/雷达/排名等统计 metric |
| #5 开放项 | 适用 · 实现缺口 | TRACE `implementation_gaps`：GAP-IMPL-01～09；非统计口径 🟡，不进 A2 `missing` |
| PDR-05 | 有 PACK/TRACE | 四件套在 `ENT-COMPARE/` |
| PDR-06 | N/A 有据 | 无本模块统计 `metric_id` 需 8 件套齐 |

**结论**：OPEN 叶已存在且已签收。缺的是**本核对记录文件**，不是缺任务。

## §2 路径与消费指针

| 产物 | 路径 |
|------|------|
| 本核对记录 | `agent-handoffs/产品整体定义/ENT-COMPARE/METRIC-OPEN-ENT-COMPARE-核对记录.md` |
| 派单包（#4 N/A 要求） | `agent-handoffs/企业战略分析-ENT/ENT-MOD-COMPARE-METRIC-OPEN-L01-派单包.md` |
| TRACE | `agent-handoffs/产品整体定义/ENT-COMPARE/TRACE-ENT-COMPARE.yaml`（v2.9） |
| 评审纪要 | `agent-handoffs/企业战略分析-ENT/PM-PDR-ENT-COMPARE-评审纪要.md` |
| Decision 088 | `agent-handoffs/产品整体定义/p2a-session/DECISIONS.md#Decision-088` |
| A2 页（展示） | `metrics/request/展示系统/pages/ENT-COMPARE.yaml` |
| seed | **不消费** `cfg_metric-ENT-seed.yaml` 的分析类 `M_ENT_*` 作为本模块指标 |

A2 / catalog 应收口：`metric_open_status: present`；`metric_open_path` = 本文件；`metric_open_task: ENT-MOD-COMPARE-METRIC-OPEN-L01`。本 DEBT 叶不改 A2 yaml、不把 COMPARE 从 `done` 改状态。

## §3 #4 N/A 书面依据（≥3 条）

1. **TRACE**：`metrics_required = 0`，`statistical_metrics_mapped = 0`。
2. **Decision 088**：禁止把对比篮包装成「轻量对比分析」或新增本模块统计 `metric_id`。
3. **boundary**：分析结果、雷达、排名、推荐指数归目标模块（评估 / 风险 / 招引等）；篮内 `basket_count` / `selected_count` = **交互状态**，不是 ADS 统计指标。
4. **卡片字段**（企业名、区域等）= 展示字段，真实 metric 归目标分析页。

## §4 #5 开放项（实现缺口，非库 missing）

派单包要求的 `ENT-COMPARE-data-gap-catalog.yaml` **现网仍缺**。⑤ 以 TRACE `implementation_gaps` 为准（GAP-IMPL-01～09：容量上限、持久化 API、return_context 等）。后续 data-agent 可在同目录补 catalog 文案；**不**因此新开 OPEN 叶，也**不**把 GAP-IMPL 打成 A2 `missing`。

甲方 🟡 不升 🟢。不改 seed。

## §5 签署

| 角色 | 姓名 | 结论 |
|------|------|------|
| 口径 / 适用性（本工作流） | `human:淮政玮` | #4 N/A 有据；本文件补磁盘；任务保持 done |
| 公式 / `algorithm_type` | `human:唐绍祖` | N/A（无本模块公式） |
