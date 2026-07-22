# ENT-MOD-RECRUIT-METRIC-OPEN-L01 — 任务完成说明
# 引育推荐 — 指标语义与 ODS/DWD 缺口核对（METRIC-OPEN）

> **任务**：ENT-MOD-RECRUIT-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-23
> **产出**：以下 3 件套

---

## 1. 任务概述

根据 PM 淮政玮 2026-07-22 PACK 通过后派单，完成 Track-MS 五件套 **#4 指标语义 + #5 开放项** 闭合：

- **招引推荐（E-26）** — 全国企业招引推荐指数指标体系与数据缺口
- **培育推荐（E-27）** — 深圳本地企业培育推荐指数指标体系与数据缺口

上游依赖 **ENT-MOD-RECRUIT-PACK-L01** ✅ done。与 **ENT-MOD-RECRUIT-V1-HIFI** 并行不阻塞。

## 2. 产出清单

| # | 产出文件 | 路径 |
|---|---------|------|
| 1 | METRIC-OPEN 核对记录 | `agent-handoffs/产品整体定义/E-26_E-27-引育推荐/METRIC-OPEN-ENT-RECRUIT-核对记录.md` |
| 2 | 数据缺口目录 | `agent-handoffs/产品整体定义/E-26_E-27-引育推荐/ENT-RECRUIT-data-gap-catalog.yaml` |
| 3 | cfg_metric 种子更新 | `metrics/cfg_metric-ENT-seed.yaml`（5 个 metric 已更新） |

## 3. 指标核对结论

### 3.1 algorithm-agent 侧

| 指标 | 招引(E-26) | 培育(E-27) |
|------|-----------|-----------|
| 推荐指数 | M_ENT_ATTRACTION_INDEX 🔧 Q015 | M_ENT_CULTIVATION_INDEX 🔧 Q015 |
| 产业相关度 | M_ENT_INDUSTRY_MATCH_SCORE 🔧 Q015（候选校准） | 共用 |
| 政策匹配度 | M_ENT_POLICY_MATCH_SCORE 🔧 Q015 | 共用 |
| 深圳连接度 | GAP-RECRUIT-METRIC-01 ❌ 无源 | — |
| 企业潜力 | — | M_ENT_GROWTH_POTENTIAL 🔧 Q015 + GAP-RECRUIT-METRIC-02 |
| 行业领域排名 | GAP-RECRUIT-METRIC-03 ⚠️ | — |
| 行业分布 | — | GAP-RECRUIT-METRIC-04 ⚠️ |
| 关键指标集合 | GAP-RECRUIT-METRIC-05 ⚠️ | 共用 |

### 3.2 data-agent 侧

**数据可用性摘要**：
- ✅ 可用：M_ENT_INDUSTRY_MATCH_SCORE（ODS dwd_org_industry_chain_dtl.chain_score）
- 🔧 formula 待算法：M_ENT_ATTRACTION_INDEX, M_ENT_CULTIVATION_INDEX, M_ENT_POLICY_MATCH_SCORE, M_ENT_GROWTH_POTENTIAL
- ❌ 无源：GAP-RECRUIT-METRIC-01（深圳连接度）

### 3.3 开放项跟踪

| 编号 | 主题 | 状态 |
|------|------|------|
| Q015 | 招引与培育推荐指数、维度阈值及权重 | 🟡 待甲方确认 |
| GAP-RECRUIT-METRIC-01 | 深圳连接度数据源 | 🆕 需决定采购/合成 |
| GAP-RECRUIT-METRIC-02 | 企业潜力在培育下的归属 | 🆕 待数据评审 |
| GAP-RECRUIT-METRIC-03 | 排名范围与排序规则 | 🆕 待下游定义 |
| GAP-RECRUIT-METRIC-04 | 行业分布统计方式 | 🆕 待下游定义 |
| GAP-RECRUIT-METRIC-05 | 关键指标集合组成 | 🆕 待下游定义 |

## 4. 禁止项合规

- ✅ **未替甲方闭合 Q015**：权重/阈值停留 pending
- ✅ **前端不计算官方指数**：已标注
- ✅ **未混用招引/培育语义**：对象范围分离（全国 vs 深圳）

## 5. 后续动作

1. 唐绍祖签署本 handoff，标志 METRIC-OPEN 交付完成
2. 推动甲方确认 Q015（权重/阈值/维度口径）
3. 跟进 GAP-RECRUIT-METRIC-01~05 的数据源采购/合成方案
4. ENT-MOD-RECRUIT-V1-HIFI 可并行启动
