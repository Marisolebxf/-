# CHAIN · Demo / 约定 ODS 全链路（模拟 GDF）

> **口径**：对齐 ENT `pipeline-demo-mock.md`；CHAIN S1 锁定真源与库名；S2 回填建表脚本。  
> **建表 Owner**：`human:李伟`（`DATA-CHAIN-STORAGE-S2-L01`）  
> 流图：[`../01-data-flow.md`](../01-data-flow.md) §7

```yaml
---
doc_id: CHAIN-ETL-DEMO-MOCK
element: CHAIN
role: etl
status: draft
version: "2026-08-13"
updated: "2026-08-13"
engine: multi
---
```

## 1. 意图

Demo 灌数基于 **ETL 调度模拟 GDF**。ODS 结构以 **`third-party-source/doc/`** 为准（优先 `md-extract/`），不以现网 as-built 为准。落 `demo_*`。

## 2. 主路径

```text
约定文档(md-extract 产业链要素库)
  → CREATE / 灌入 demo_gkxlumenx_ods
  → ETL 模拟 GDF → demo_dwd / ads / ES / Nebula / MinIO
```

## 3. 命名表

| 角色 | 开发默认 | 禁止作 Demo 默认 |
|---|---|---|
| MySQL ODS | `demo_gkxlumenx_ods` | `gkxlumenx_ods` |
| MySQL DWD | `demo_gkxlumenx_dwd` | `gkxlumenx_dwd` |
| MySQL ADS | `demo_gkxlumenx_ads` | `gkxlumenx_ads` |

## 4. 建表脚本（S2）

| 项 | 路径 |
|---|---|
| 入口脚本 | `${GKX_ROOT}/repos/demo-algo-ent-analysis/scripts/run_chain_ods.py` |
| 共享解析/DDL | `entan/llm_ods/schema.py` · `load.py`（表头解析「是否为主键」） |
| 仓内 DDL 快照 | [`demo_gkxlumenx_ods_chain_tables.sql`](./demo_gkxlumenx_ods_chain_tables.sql) |
| 表清单 | [`../sources/inventory.md`](../sources/inventory.md) |
| seeds | [`../seeds/README.md`](../seeds/README.md) |

```text
# 仓根：repos/demo-algo-ent-analysis
set GKX_ROOT=...
python scripts/run_chain_ods.py --self-check
python scripts/run_chain_ods.py --sql-out <path>/demo_gkxlumenx_ods_chain_tables.sql
python scripts/run_chain_ods.py --apply   # 仅 demo_gkxlumenx_ods；拒正式库
```

**证据**：`--self-check` 绿；DDL 已提交；**`--apply` 已成功**（`111.198.38.90:34306` → `demo_gkxlumenx_ods` 四表；`SHOW CREATE` → `repos/demo-algo-ent-analysis/out/chain_demo_ods_show_create.sql`）。

## 5. 旁路

直写 ADS 仅冒烟，见 [`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md)。
