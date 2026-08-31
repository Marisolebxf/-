# 管道 · ODS → DWD（政策）

```yaml
---
doc_id: POLICY-ETL-ODS-TO-DWD
element: POLICY
role: etl
status: as-built
version: "2026-08-31"
updated: 2026-08-31
engine: mysql
task_id: DATA-POLICY-STORAGE-ETL-FILL-L01
---
```

> **字段矩阵不在本文件**：列对照真源 [`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md)，贴源结构 [`../sources/ods-ddl.md`](../sources/ods-ddl.md)。本文件只写**写入路径与调度**。
> Demo 主路径全景见 [`pipeline-demo-mock.md`](./pipeline-demo-mock.md)。

## 意图

把政策贴源表清洗映射进项目 DWD 单表 `policy_base_info`。国内与国际政策**同表**，用平面标记切片，不建第二张明细表。

| 层 | 库 | 表 |
|---|---|---|
| ODS 贴源 | `demo_gkxlumenx_ods` | `dwd_policy_base`（国内）· `dwd_global_policy_base`（国际） |
| 项目 DWD | `demo_gkxlumenx_dwd` | **`policy_base_info`**（主键 `policy_id` ← ODS `id`） |
| 正式 ODS | `gkxlumenx_ods` | **本管线零写入** |

> 供应表名带 `dwd_` 前缀，对本项目仍是 **ODS**。勿把 `gkx.dwd_policy_base` 当项目 DWD 表名。

## 实现（as-built）

| 项 | 值 |
|---|---|
| 仓 / 模块 | `demo-algo-ent-analysis` · `polan/mockgen/generate.py`（全量）· `polan/mockgen/incr.py`（增量） |
| 入口 | `mock.run(mode=...)`，由 `scripts/run_all_policy.py` 第 3 步调用 |
| 幂等 | `mode=replace` → TRUNCATE 后重建；`mode=append` → 只补差集，可重跑 |

两种模式语义不同，别混：

- **`replace`（重建灌数）**：内存造底数 → 同时写 ODS `dwd_policy_base` → 再映射入 DWD。
- **`append`（增量入库）**：**不**内存造数，读 **ODS − DWD 差集**映射入 DWD（`polan/mockgen/incr.py`）。增量只碰 ODS/DWD，**不重算 ADS**——ADS 由 `run_all_policy` 后续步骤统一重算。

## 调度与门禁

| 项 | 值 |
|---|---|
| Demo 编排 | `python scripts/run_all_policy.py`（15 步串行，幂等可重跑） |
| 模式开关 | `POLAN_SEED_MODE=append`（默认）\| `replace` |
| 后端开关 | `POLAN_DB_BACKEND=sqlite`（默认，本地零依赖）\| `pg` \| `mysql` |
| 库名门禁 | `mysql` 后端启动前跑 `assert_demo_mysql_targets()`，非 `demo_*` 目标直接拒绝 |
| 正式 GDF DAG | **开放项** `OPEN-POLICY-FLOW-01`（产线未回写） |

## 禁止

写正式 `gkxlumenx_*` / `gkx`；把 ODS 表名当项目 DWD 表名；在本管道里算 ADS 指标；用旧稿 v1 的 37 列当贴源结构。
