# 派单包 · ALGO-LIB-SEED-TYPE-L01

> **状态**：ready · **Agent**：`algorithm-agent` · **supervised_by**：`human:唐绍祖` · **collaborators**：`data-agent`  
> **仓**：`gkx-orchestration` · **claim_type**：`pull`（本包不代认领）  
> **生产派单说明（贴 /goal 前先读）**：[`给人说明-ALGO-LIB-SEED-TYPE-L01-2026-08-24.md`](./给人说明-ALGO-LIB-SEED-TYPE-L01-2026-08-24.md)  
> **effort_points**：5 · **difficulty**：M

闸门已齐：`ALGO-LIB-METRIC-DEPS-L01`=`done`；`METRIC-SEED-REGISTER-L01`=`done`。

## 目标

把 A1 表2 里**已签**的 `algorithm_type` / `formula` 回填进已有 seed 行。相交仅 **11 条 `M_ENT_*`**。90 条 `TEMP_ALGO_*` 列 skip，不编造 `M_*`。OPEN 新号保持 `UNKNOWN`。

## 必读

1. `给人说明-ALGO-LIB-SEED-TYPE-L01-2026-08-24.md`  
2. `metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`  
3. `data-lineage-policy.md` §2.1  
4. `METRIC-SEED-REGISTER-L01.md`（YAML 子集语法）

## 禁止

- 赋号卡 `suggested_unsigned` 当已签；改 definition/源表；A2 missing→mapped  
- 改 `metrics/algo-results/`（A2 两叶仍 `in_progress`）  
- 本叶开 OPEN 贴源 / GDF / T0-X；`D1=aligned`；权重/双阈值写死  
- 产业链全景 `TEMP_ALGO_ALGO-CHAIN-DEEP-117_1` 写入 seed 或生产公式

## `/goal`

```text
/goal
task: ALGO-LIB-SEED-TYPE-L01
agent: algorithm-agent
supervised_by: human:唐绍祖
claim_type: pull
强度：ponytail off（定义·seed 会签回填；禁止用 YAGNI 跳过 D9 回填清单、data-agent 校验与 handoff）。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
上下文：headroom 可选。表2 / policy §2.1 / REGISTER handoff 读原文，禁止 compress 代替精读。

先读 给人说明-ALGO-LIB-SEED-TYPE-L01-2026-08-24.md。
MCP 认领后再改 YAML。只回填表2∩seed 的 11 条 M_ENT_* 的 algorithm_type 与 formula（API→third_party）。
90 条 TEMP_ALGO_* skip；OPEN 新号保持 UNKNOWN。D1 保持 draft。handoff 含回填清单。
```
