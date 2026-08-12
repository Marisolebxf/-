# 管道 · ODS → DWD

> S2 回填 · `DATA-ENT-STORAGE-S2-L01` · 禁止大段 SQL

## 意图

将 `gkxlumenx_ods`（或 Demo `demo_gkxlumenx_ods`）承诺表清洗写入 `gkxlumenx_dwd` / `demo_gkxlumenx_dwd`。与正式 GDF **同构**；Demo 侧调度 **模拟 GDF**。

## 脚本 / 工作包指针

| 类型 | 路径 |
|---|---|
| GDF 派单包（企业 · **现行**） | `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v2/` |
| DWD 建表真源（包内快照） | `…/10-DWD-MySQL-DDL/` |
| 贴源表清单 | `…/02-WaveA-贴源表清单.yaml` |
| Mapping 施工真源 | `…/09-企业维-ODS到DWD-Mapping说明-v4.md` |
| 作废对照 | `…/11-作废与误源对照.md` |
| Mapping 目录指针 | `agent-delivery/data/GDF/Mapping/企业/`（施工以工作包 `09` v4 为准） |
| 建议 ETL 顺序 | Mapping §0：base → extra → finance → executive/news → bid → industry_chain → risk_* |
| 历史包（建表勿用） | `…/GDF-ENT-WORKPACK-v1/` |

## 调度（OPEN-ENT-FLOW-01 · 部分）

| 项 | 状态 |
|---|---|
| 正式 GDF cron/DAG 名 | **仍开放**（产线未回写本仓） |
| Demo 模拟调度 | 与正式同构；落地前可用手工/CI 作业串行调用 Mapping 顺序 |
| 门禁 | 源侧默认 `is_deleted=0`；失败不晋升下游（见 `01-data-flow`） |
