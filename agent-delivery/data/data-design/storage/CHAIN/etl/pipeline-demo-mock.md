# CHAIN · Demo / 约定 ODS 全链路（模拟 GDF）

> **口径**：对齐 ENT `pipeline-demo-mock.md`；CHAIN S1 锁定真源与库名；S2 回填建表脚本。  
> **建表 Owner**：`human:李伟`（`DATA-CHAIN-STORAGE-S2-L01`）  
> 流图：[`../01-data-flow.md`](../01-data-flow.md) §7

```yaml
---
doc_id: CHAIN-ETL-DEMO-MOCK
element: CHAIN
role: etl
status: as-built
version: "2026-08-16"
updated: "2026-08-16"
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

**逐步过程 + ODS→DWD 十四表映射诚实**（`DEMO-CHAIN-SIM-PROCESS-L01`）：[`pipeline-demo-sim-process.md`](./pipeline-demo-sim-process.md) · 字段级 [`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md)。缺口五表不装成功：`chainan/llm_ods/gdf_sim_gaps.py`（不改 `gdf_sim.py`）。

**行业分析主路径**（`DATA-CHAIN-INDANA-STORAGE-L01`）：与产业链四表**同 Demo 实例、不同 sheet/表族**。入站现表 `dwd_industry_analysis_*`（结构复制自现表 DDL）→ 项目 DWD `industry_analysis_*`（**仅去 `dwd_` 前缀**）。清单 [`../sources/inventory-industry-analysis.md`](../sources/inventory-industry-analysis.md)。GDF Mapping 作业名：**未找到，不编造**（OPEN-CHAIN-INDANA-03）。Demo `demo_gkxlumenx_dwd` 2026-08-16 抽检六表尚未建出（OPEN-CHAIN-INDANA-01）。

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

## 5. 灌数入口（as-built · DEMO-CHAIN-UI-SEED-ODS-L01）

| 项 | 路径 |
|---|---|
| 主仓 | `${GKX_ROOT}/repos/demo-algo-science` |
| 编排 | `scripts/run_all.py --chain --mode append\|replace` |
| 自检 | `python scripts/run_all.py --self-check` |
| API | `POST /internal/run-chain-pipeline` body `{ "mode": "append"\|"replace" }` |
| UI | `demo-ui-system-test` 产业链 BasicPage split-button |
| 闸门 | `chainan.llm_ods.dbconn.assert_demo_mysql_targets()`（库名不以 `demo_` 开头直接拒绝） |
| 旧旁路 | 仅 `CHAIN_SEED_LEGACY_MOCKGEN=1` 才走 `mock_chain` + 旧 A/M |

```text
append（默认）：保留 ODS/DWD 明细 → 写入缺失的 3.0 产业树节点（新领域/新产业链/新子链）+ 新批次企业资讯 → 模拟 GDF INSERT demo DWD v5 → ADS v2 全量重算
replace：TRUNCATE 约定四表 ODS + 映射 DWD → 同路径 → ADS 全量重算
```

禁止 `init_schema()`（会打到正式库名）。ES / Nebula 投影失败不阻断，`/internal/status.projection` 诚实。

## 6. 旁路

直写 ADS 仅冒烟，见 [`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md)。
旧 `mock_chain` 直写 `gkx_chain_dwd_*` **不算**本单验收。
