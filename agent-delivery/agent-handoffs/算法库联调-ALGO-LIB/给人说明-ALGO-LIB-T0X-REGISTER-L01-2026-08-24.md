# 生产派单说明 · ALGO-LIB-T0X-REGISTER-L01

> **给谁**：监管人 `human:淮政玮` 新开 **1** 个 Cursor 会话，执行 Agent = `data-agent`；`product-agent` 可同会话对覆盖清单。  
> **日期**：2026-08-24  
> **状态**：`ready` · `definition` · Epic `E-ALGO-LIB-DEMO` · P0 · effort 13 · difficulty XL  
> **短包**：[`ALGO-LIB-T0X-REGISTER-L01-派单包.md`](./ALGO-LIB-T0X-REGISTER-L01-派单包.md)  
> **触发**：T0-X 主持纠偏——**先入库，再分桶/定类型**。`ALGO-LIB-T0X-L01` 已 `blocked`，等本叶。

闸门：`METRIC-SEED-REGISTER-L01` / `METRIC-ID-ASSIGN-L01` / A1 / 专题 L02 / 展示 L02 = `done`。

本叶只写 **身份进 seed**。`algorithm_type` 保持 `UNKNOWN`，留给 T0-X 复会逐条指定。不写公式、不拍四桶。

---

## 1. 做什么

覆盖真源（禁止凭记忆）：`metrics/request/_work/ALGO-LIB-T0X-L01-registry-coverage.json`

| 批次 | 做什么 |
|------|--------|
| A · F−L 72 无号 | 赋正式 `M_*` + 写入 seed + 矩阵。行清单 = T0X `pre-meeting.yaml` `f_minus_l` 中 `metric_id` 空的 72 条 |
| B · 已有号未入 seed | 专题 mapped **49** + 展示 mapped **3** + `M_ENT_KEY_TOTAL`（Q038 仍挂 `d1_pending_ref`，只注册身份） |
| C · mapped 行无号 | 专题 53 行 + 展示 113 行：按 `A1指标叶ID` 赋号或 reuse 已有 `M_*`，再注册 |
| D · A1 `TEMP_ALGO_*` 90 | **先赋正式号**再注册；**禁止** `TEMP_*` 写入 seed 的 `metric_id`。与 C 去重（同一 A1 叶只一个 `M_*`） |

F−L 已在 seed 的 5 条（`M_CHAIN_PRODUCT_COUNT` / `M_CHAIN_PATENT_COUNT` / `M_POLICY_INDUSTRY_FIT` / `M_SYNTH_ELEM_CONTRIB` / `M_SYNTH_COLLAB_OUTPUT_CORR`）**reuse 跳过、不改口径**。

会前闸门（给 T0-X 复会）：F−L **77** 行都能 `metric-get` → `found.seed=true`。把闸门表写进 `_work/ALGO-LIB-T0X-REGISTER-L01-t0x-gate.md`。

写法跟 `METRIC-SEED-REGISTER-L01`：**`metric-registry-lib.mjs` 子集语法**（CRLF+BOM 按该域现文件），禁止 PyYAML 默认 dump。

---

## 2. 不做什么

| 禁止 | 原因 |
|------|------|
| `algorithm_type` 写成 STAT/MODEL/GRAPH | T0-X 复会才逐条指定 |
| 把赋号卡 `suggested_unsigned` 或 A1 表2 type 当已签 | 与 REGISTER-L01 同一铁律 |
| `D1=aligned`；改 D2/D3/D4 为绿 | 只补身份 |
| A2 `missing` → `mapped` | 入库 ≠ 库已覆盖功能 |
| `TEMP_*` 当 seed `metric_id` | 页面终态必须是正式 `M_*` |
| 改存量 seed 的 definition / formula / 源表 | 已在 seed 的 reuse 跳过 |
| 现场四桶 / 开 OPEN 贴源 / GDF / 写业务代码 | 本叶是注册 |
| 发明 `M_ZHIKU_*` | 与 L01 相同 |

`M_ENT_KEY_TOTAL`：要入库（主持「分析出来的都进 registry」），**不要**当王惠已正式化；`d1=draft`，`d1_pending_ref=Q038`。

---

## 3. 必读（按序）

1. 本文件 + 短包 `/goal`  
2. T0-X 纠偏纪要 `metrics/request/T0X/ALGO-LIB-T0X-L01-minutes.md`  
3. `ALGO-LIB-T0X-L01-registry-coverage.json`  
4. `METRIC-SEED-REGISTER-L01.md`（YAML 写法、UNKNOWN、pending_ref）  
5. `data-lineage-policy.md` §2.1  
6. A2：`TOPIC-ALGO-GAP-L02.yaml` / `DS-ALGO-GAP-L02.yaml` + T0X `pre-meeting.yaml`  
7. A1 表2：`metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`  

查库只走 MCP `metric-registry` 或 `metric-registry-lib.mjs`，禁止整文件读 seed 来「看 8 件套」。

---

## 4. 交付

| 产物 | 路径 |
|------|------|
| seed / 矩阵增量 | `metrics/registry/cfg_metric-*-seed.yaml` + `metric-readiness-matrix-*.yaml` |
| 赋号+注册清单 | `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-new-ids.md` |
| T0-X 闸门表 | `metrics/request/_work/ALGO-LIB-T0X-REGISTER-L01-t0x-gate.md`（F−L 77 全 `found.seed`） |
| skip / whitelist | 同清单：reuse 跳过、仍不注册及原因 |
| handoff | `agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-T0X-REGISTER-L01.md`（`ponytail: off`） |

架构铁律：不写算法、不越层。D9：不把 missing 改绿、不把类型签成已对齐。
