# POLICY · ETL 管道索引

```yaml
---
doc_id: POLICY-ETL-INDEX
element: POLICY
role: etl
status: draft
version: "2026-08-31"
updated: 2026-08-31
task_id: DATA-POLICY-STORAGE-ETL-FILL-L01
---
```

> 本目录只写**写入路径**；表结构在 [`../stores/`](../stores/README.md)，贴源结构在 [`../sources/ods-ddl.md`](../sources/ods-ddl.md)。
> `status` 三态：`as-built` = 已施工并可回源代码；`draft` = 设计在、施工未起；`not-built` = **明确不做**（占位说明，别当待办）。

| 管道 | 文档 | 状态 |
|---|---|---|
| ODS → DWD | [`pipeline-ods-to-dwd.md`](./pipeline-ods-to-dwd.md) | **as-built** · `polan/mockgen/{generate,incr}.py` |
| ODS→DWD 字段矩阵 | [`ods-to-dwd-mapping.md`](./ods-to-dwd-mapping.md) | draft · 列对照真源 |
| Demo 贴源 Mock 全景 | [`pipeline-demo-mock.md`](./pipeline-demo-mock.md) | draft · E0→E1→T2→L3→L4 + T+1 增量 |
| DWD → ADS | [`pipeline-dwd-to-ads.md`](./pipeline-dwd-to-ads.md) | **as-built** · `basic` / `graph` / `eval` / `text` 十二步 |
| → Nebula | [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) | **as-built** · `POLICY-NEBULA-PROJECT-CHAIN-L01` |
| → MinIO | [`pipeline-to-minio.md`](./pipeline-to-minio.md) | draft · 前缀 `policy/{task_id}/` |
| DWD → ES | [`pipeline-dwd-to-es.md`](./pipeline-dwd-to-es.md) | **not-built** · 本域不建独立索引 |
| Mock 直写 ADS | [`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md) | **not-built** · 本域无此旁路 |

## 主链一句话

```text
ODS dwd_policy_base ──映射──> DWD policy_base_info ──12 步算法──> ADS policy_*
                                                          └──图两表──> Nebula demo_gkx_chain
```

编排入口 `demo-algo-ent-analysis` `scripts/run_all_policy.py`（15 步串行，幂等可重跑）。ODS/DWD 走差集增量，**ADS 一律按当前 DWD 全量重算**。

## 全域铁律

- 库：Demo `demo_gkxlumenx_{ods,dwd,ads}`；**零写入**正式 `gkxlumenx_*` / `gkx`。
- 图：仅 `demo_gkx_chain` 一张 G；禁 `gkx_policy` 目标态、禁写 `gkx_chain`。
- 引擎：关系库仅 MySQL；算法仅 Python；Java 只读 ADS、不直连 nGQL。
- 诚实：缺表缺列（`OPEN-POLICY-DISP-*`）一律空态 + 角标，禁止 fixture 计数冒充 live。
