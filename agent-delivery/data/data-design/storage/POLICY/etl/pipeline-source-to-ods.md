# 管道 · 三方源 → 项目 ODS（政策）

```yaml
---
doc_id: POLICY-ETL-SOURCE-TO-ODS
element: POLICY
role: etl
status: as-built
version: "2026-08-31"
engine: mysql
---
```

> Demo 算子级同步。正式 GDF DAG 仍是开放项 `OPEN-POLICY-FLOW-01`，lumen 长任务须按分区/水位/失败重试重写，禁止把本脚本当产线。

## 意图

把供应库 **`gkx`** 的政策贴源表，按**同表名、列交集**复制到项目 ODS。不算指标、不写 DWD/ADS。

| 角色 | 库.表 |
|---|---|
| 源（只读） | `183.240.141.251:3318` / `gkx.dwd_policy_base` · `gkx.dwd_global_policy_base`（账号 `gkx_reader_zp`） |
| Demo 目标 | `192.168.88.43` / `demo_gkxlumenx_ods` 同名表 |
| lumen 目标 | `192.168.88.43` / `gkxlumenx_ods` 同名表（须二次确认） |

DDL 真源 [`../sources/ods-ddl.md`](../sources/ods-ddl.md)。目标表须已存在；脚本**不** `CREATE DATABASE` / `CREATE TABLE`。

## 实现

| 项 | 值 |
|---|---|
| 仓 | `demo-algo-ent-analysis` |
| 模块 | `polan/ods_sync.py` |
| 入口 | `python scripts/run_policy_ods_sync.py`；中台「政策分析算法库 → 基础指标 → 数据同步」（仅 Demo upsert） |
| 默认 | `--plane demo --mode upsert --table all`，过滤 `is_deleted=0` 且非历史 |

```text
py -3 scripts/run_policy_ods_sync.py --self-check
py -3 scripts/run_policy_ods_sync.py --dry-run --table domestic --limit 20
py -3 scripts/run_policy_ods_sync.py --mode upsert --table all
```

写 lumen：`--plane lumen --confirm-lumen` 且 `POLICY_ODS_SYNC_ALLOW_LUMEN=1`。

| mode | 行为 |
|---|---|
| `upsert` | 跨机按批 `INSERT … ON DUPLICATE KEY UPDATE`（按 `id`；源/目标不是同一 MySQL） |
| `replace` | `TRUNCATE` 目标后全量插入 |
| `--since` | 源 `updated_time`（空则 `created_time`）大于水位 |

列策略：源∩目标，跳过 `_demo_id`。Demo 旧 Mock 表列少时只灌交集，不扩列。

## 禁止

写 `gkx`；默认写 `gkxlumenx_*`；写 DWD/ADS；在本脚本里跑 `run_all_policy` / 算指标；把 Mock `replace` 灌数当成三方同步。

同步完 Demo 要出 ADS：再跑 `run_all_policy` 的 `reload`（留 ODS、清政策 DWD 后重算）。
