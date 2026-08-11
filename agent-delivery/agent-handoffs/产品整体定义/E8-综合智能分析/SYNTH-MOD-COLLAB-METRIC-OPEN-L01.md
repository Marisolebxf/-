# SYNTH-MOD-COLLAB-METRIC-OPEN-L01 — 任务完成说明
# 区域创新协同分析 · 指标语义卡开放项核对（METRIC-OPEN）

> **任务**：SYNTH-MOD-COLLAB-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:王惠（口径主责）
> **算法共签**：human:唐绍祖（方案 B）
> **日期**：2026-08-11
> **产出**：以下 3 件套 + cfg_metric-SYNTH-seed 6 条 + readiness-matrix-SYNTH 6 条

---

## 1. 任务概述

根据 PM 淮政玮 2026-08-10 PACK 会签通过后派单，完成 Track-MS 五件套 **#4 指标语义 + #5 开放项** 闭合：

- **区域创新协同分析（E8-COLLAB）** — 完整度/中心度/密度三指标 + 协同指数 + 关系输入 + 产出关联的指标语义核对

上游依赖 **SYNTH-MOD-COLLAB-PACK-L01** ✅ done。旧 SYNTH-REGION 遗漏完整度指标已修正，密度×强度合成已废止。

## 2. 产出清单

| # | 产出文件 | 路径 |
|---|---------|------|
| 1 | METRIC-OPEN 核对记录 | `agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/METRIC-OPEN-SYNTH-COLLAB-核对记录.md` |
| 2 | 数据缺口目录 | `agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/SYNTH-COLLAB-data-gap-catalog.yaml` |
| 3 | 本 handoff 文档 | `agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-MOD-COLLAB-METRIC-OPEN-L01.md` |
| 4 | cfg_metric-SYNTH-seed.yaml（6 条已登记） | `agent-delivery/metrics/cfg_metric-SYNTH-seed.yaml` COLLAB 段 |
| 5 | metric-readiness-matrix-SYNTH.yaml（6 条已登记） | `agent-delivery/metrics/metric-readiness-matrix-SYNTH.yaml` COLLAB 段 |

### 2.1 cfg_metric 登记情况

| metric_id | D1 | 说明 |
|-----------|----|------|
| M_SYNTH_COLLAB_COMPLETENESS | draft(Q-SYNTH-C-01) | 临时公式已定义；正式分母待确认 |
| M_SYNTH_COLLAB_CENTRALITY | draft(Q-SYNTH-C-01) | 临时度中心性；正式算法待确认 |
| M_SYNTH_COLLAB_DENSITY | draft(Q-SYNTH-C-01) | 临时无向图密度；正式图模型待确认 |
| M_SYNTH_COLLAB_INDEX | missing(Q-SYNTH-C-02) | 协同指数；公式不存在 |
| M_SYNTH_COLLAB_RELATION_INPUT | draft(Q-SYNTH-C-01) | SQL 已定义；校验规则待确认 |
| M_SYNTH_COLLAB_OUTPUT_CORR | missing(Q-SYNTH-C-03) | 关联结果；方法/样本门槛未定 |

### 2.2 readiness-matrix 四维状态

| metric_id | D1 | D2 | D3 | D4 |
|-----------|----|----|----|----|
| M_SYNTH_COLLAB_COMPLETENESS | draft | pending | pending_ods | mock |
| M_SYNTH_COLLAB_CENTRALITY | draft | pending | pending_ods | mock |
| M_SYNTH_COLLAB_DENSITY | draft | pending | pending_ods | mock |
| M_SYNTH_COLLAB_INDEX | missing | n/a | n/a | n/a |
| M_SYNTH_COLLAB_RELATION_INPUT | draft | pending | pending_ods | mock |
| M_SYNTH_COLLAB_OUTPUT_CORR | missing | n/a | n/a | n/a |

## 3. 指标核对结论

6 个指标全部为算法依赖型（mapping_status=🔧）。核心阻塞为 Q-SYNTH-C-01（三指标正式分母/图类型/边权口径）和 Q-SYNTH-C-02（协同指数标准化/权重/校准/判据）。

COLLAB 模块特殊禁止项：
- 密度×强度冒充正式公式已废止
- 完整度指标遗漏已修正（新增 M_SYNTH_COLLAB_COMPLETENESS）
- 关联结果禁止因果表述

## 4. 禁止项合规

- ✅ 未替甲方闭合 Q-SYNTH-03/C-01~C-05
- ✅ 密度×强度已废止为权威；仅允许三指标归一等权作为临时演示
- ✅ 完整度指标已新增并贯穿 TRACE/USM/UX/Wireframe
- ✅ 关联结果禁止因果表述
- ✅ D1=missing 指标 D2~D4 = n/a

## 5. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 仅改动 agent-delivery 文档 | ✅ |
| 2 | metric 口径引用 TRACE/bid-reference | ✅ |
| 3 | pending_hint ≥80 字（6 条全部达标） | ✅ |
| 4 | 唐绍祖算法共签 | ✅（2026-08-11） |
| 5 | cost 四字段已填写 | ✅ |

## 6. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 200_000 |
| actual_tokens | 61_000 |
| model_used | gpt-5 |
| actual_cost | 0.46 |
| cost_warn | green |

## 7. 语义双签（方案 B · 2026-08-11）

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 算法共签 | human:唐绍祖 | 2026-08-11 | ✅ 算法侧交付完成：6 指标 mapping_status 评估、全部如实标记🔧、Q-SYNTH-03/C-01~C-05 不伪闭合、密度×强度已废止、完整度已新增 |
| 口径主责 | human:王惠 | — | ⏳ 待王惠口径会签（方案 B 铁律，缺一不可） |