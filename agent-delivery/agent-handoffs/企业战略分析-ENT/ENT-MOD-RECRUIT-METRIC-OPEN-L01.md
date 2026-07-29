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



---

## 6. 算法共签收尾（2026-07-29）

> **签署人**：human:唐绍祖（算法共签 · 方案 B §1.4.2） ｜ **口径主责**：human:王惠

2026-07-23 算法侧完成产出后，因飞书 inbound 同步回刷，registry 长期停留 status=in_progress（同 ENT-MOD-SEARCH-METRIC-OPEN-L01 现象）。2026-07-29 由算法负责人唐绍祖收尾：

1. 复核 3 件套证据齐全：METRIC-OPEN-ENT-RECRUIT-核对记录.md（含会签）、ENT-RECRUIT-data-gap-catalog.yaml（8 条 metric，pending_hint 均 ≥80 字）、cfg_metric-ENT-seed.yaml（5 个 RECRUIT metric 8 件套已落种子）。
2. 双仓《算法设计说明.md》登记：demo-algo-ent-analysis 第 18 章（完整口径/血缘/开放项）、demo-algo-science 第 14 章（交叉引用 §13.7 attraction/cultivation 真实算法）。
3. registry 认领收尾：claimed_by=human:唐绍祖、supervised_by=human:王惠、owner_semantic=human:王惠、cosigner_algorithm=human:唐绍祖（方案 B 双签字段保留），状态推进 in_progress → review。

算法共签结论：招引/培育推荐指数的三维加权公式、维度口径、临时默认权重（pending Q015）均与 bid-reference §5.7/§5.8 及 §13.7 已实现算法一致；深圳连接度（GAP-01）与企业潜力归属（GAP-02）按开放项登记，未替甲方闭合 Q015。算法侧交付完成，转 review 待 PM/口径侧验收。

后续：建议 PM 暂停飞书 inbound 对本任务的回刷，或手动关闭看板状态，避免再次回退。

## 5. 后续动作

1. 唐绍祖签署本 handoff，标志 METRIC-OPEN 交付完成
2. 推动甲方确认 Q015（权重/阈值/维度口径）
3. 跟进 GAP-RECRUIT-METRIC-01~05 的数据源采购/合成方案
4. ENT-MOD-RECRUIT-V1-HIFI 可并行启动
