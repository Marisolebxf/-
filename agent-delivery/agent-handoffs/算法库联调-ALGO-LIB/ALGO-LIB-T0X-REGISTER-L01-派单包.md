# 派单包 · ALGO-LIB-T0X-REGISTER-L01

> **状态**：`ready` · **claim_type**：`pull`（**不代认领**）  
> **Agent**：`data-agent` · **supervised_by**：`human:淮政玮`  
> **collaborators**：`product-agent`（覆盖清单）、`algorithm-agent`（本叶不签类型）  
> **仓**：`gkx-orchestration` · Epic `E-ALGO-LIB-DEMO` · P0 · effort 13 · difficulty XL  
> **说明**：[`给人说明-ALGO-LIB-T0X-REGISTER-L01-2026-08-24.md`](./给人说明-ALGO-LIB-T0X-REGISTER-L01-2026-08-24.md)

闸门：REGISTER-L01 / ID-ASSIGN / A1 / TOPIC-L02 / DS-L02 = `done`。  
下游：`ALGO-LIB-T0X-L01` 仍 `blocked`，等本叶闸门表。

## 目标

把 T0-X 要核对的分析指标写入 `metrics/registry`（身份，`D1=draft`，`algorithm_type=UNKNOWN`）。  
完成标志：F−L **77** 行都能 `metric-get` → `found.seed=true`。

覆盖数字（2026-08-24 json）：无号 72（F−L）+ 已有号未入 seed 49+3+`M_ENT_KEY_TOTAL` + mapped 无号行 + 90 `TEMP_ALGO_*`（去重后注册）。

## 禁止

- 本叶指定 STAT/MODEL/GRAPH（留给 T0-X 复会）  
- missing→mapped；`D1=aligned`；改存量口径  
- `TEMP_*` 进 seed 当 `metric_id`  
- 四桶 / OPEN 贴源 / GDF / 业务代码  

## `/goal`

```text
/goal
task: ALGO-LIB-T0X-REGISTER-L01
agent: data-agent
supervised_by: human:淮政玮
claim_type: pull
强度：ponytail off（定义·seed 身份注册；禁止用 YAGNI 跳过 D9 注册清单、lib 解析自检与 handoff）。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
上下文：headroom 可选。覆盖 json / L02 / A1 表2 / REGISTER-L01 handoff 读原文，禁止 compress 代替精读。

先读 给人说明-ALGO-LIB-T0X-REGISTER-L01-2026-08-24.md。
MCP 认领后再改 YAML。
分析清单先入 metrics/registry，再交给 T0-X 逐条分桶/定类型。
D1=draft，algorithm_type=UNKNOWN。F-L 77 闸门表必须全 found.seed=true。
禁 TEMP_ 当 seed id；禁 missing→mapped；禁改存量口径。
```
