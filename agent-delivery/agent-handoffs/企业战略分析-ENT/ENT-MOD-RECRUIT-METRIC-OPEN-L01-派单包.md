# 派单包：ENT-MOD-RECRUIT-METRIC-OPEN-L01

- **派单方**：coordinator（PM 淮政玮确认 PACK 通过后解锁）
- **时间**：2026-07-22
- **双 Agent 分工**：
  - **`algorithm-agent`**：招引（E-26）/ 培育（E-27）推荐指数与维度口径、公式、DEMO 临时阈值；算法边界（前端不计算官方指数）
  - **`data-agent`**：ODS→DWD→ADS 贴源存在性 + `pending_hint` catalog（≥80 字）
- **监管人**：human:唐绍祖（语义 Owner 临时代行 §1.4.1）
- **Sprint**：2026-W30
- **上游**：`ENT-MOD-RECRUIT-PACK-L01` ✅ done（PM 淮政玮 2026-07-22 通过）
- **并行**：`ENT-MOD-RECRUIT-V1-HIFI`（不互相阻塞；METRIC-OPEN 阻塞门1完整闭合）

## 1. 目标

闭合 Track-MS 五件套 **#4 指标语义 + #5 开放项**，支撑：

1. **招引推荐（E-26）** — ⓘ MetricSpecCard + ⚠️ PendingBadge（Q015 / GAP-RECRUIT-METRIC-*）
2. **培育推荐（E-27）** — 同上

Wave0 / Demo 允许 🧪 Mock + 🟡 团队临时默认；**不得**把临时权重/阈值写成甲方已确认。

## 2. 范围真源

| 项 | 路径 |
|----|------|
| TRACE | `E-26_E-27-引育推荐/TRACE-ENT-RECRUIT.yaml` |
| 开放项 | **Q015**；GAP-RECRUIT-METRIC-01～05；GAP-RECRUIT-UX-01；GAP-RECRUIT-EXPORT-01 |
| 算法 bid | `bid-reference/科技专题服务算法库.md` §招引/培育 |
| seed | `metrics/cfg_metric-ENT-seed.yaml` |
| DDL | `data/third-party-source/gkx-mysql-raw/gkx_schema_ddl.sql` |
| 企业域 | `data/企业域数据库设计(v1).md` |

**重点校准 metric（候选/GAP）**：

| 字段 | metric_id / GAP |
|------|-----------------|
| 产业相关度 | `M_ENT_INDUSTRY_MATCH_SCORE`（候选校准） |
| 政策匹配度 | `M_ENT_POLICY_MATCH_SCORE` |
| 深圳连接度 | `GAP-RECRUIT-METRIC-01` |
| 企业潜力 | `GAP-RECRUIT-METRIC-02` / `M_ENT_GROWTH_POTENTIAL` 候选 |
| 行业领域排名 | `GAP-RECRUIT-METRIC-03` |
| 行业分布 | `GAP-RECRUIT-METRIC-04` |
| 关键指标集合 | `GAP-RECRUIT-METRIC-05` |

## 3. 联合产出

1. `agent-handoffs/产品整体定义/METRIC-OPEN-ENT-RECRUIT-核对记录.md`
2. `agent-handoffs/产品整体定义/E-26_E-27-引育推荐/ENT-RECRUIT-data-gap-catalog.yaml`
3. 更新 `cfg_metric-ENT-seed.yaml` 相关条目 + TRACE open_items
4. handoff：`agent-handoffs/企业战略分析-ENT/ENT-MOD-RECRUIT-METRIC-OPEN-L01.md` + 唐绍祖会签

## 4. 禁止

- 替甲方闭合 Q015 正式权重/阈值
- 前端计算官方推荐指数
- 混用招引/培育模型维度或对象范围语义

## 5. 认领话术

```text
/goal ENT-MOD-RECRUIT-METRIC-OPEN-L01
监管：human:唐绍祖
双 Agent：algorithm-agent + data-agent
必读：ENT-MOD-RECRUIT-METRIC-OPEN-L01-派单包.md + TRACE-ENT-RECRUIT.yaml + PACK 四件套
交付：METRIC-OPEN-ENT-RECRUIT-核对记录.md + ENT-RECRUIT-data-gap-catalog.yaml
并行：不阻塞 ENT-MOD-RECRUIT-V1-HIFI
```
