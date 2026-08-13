# 管道 · ODS → DWD

> S2 回填 · `DATA-ENT-STORAGE-S2-L01` · 禁止大段 SQL

## 意图

将 `gkxlumenx_ods`（或 Demo `demo_gkxlumenx_ods`）承诺表清洗写入 `gkxlumenx_dwd` / `demo_gkxlumenx_dwd`。与正式 GDF **同构**；Demo 侧调度 **模拟 GDF**。

## 脚本 / 工作包指针

| 类型 | 路径 |
|---|---|
| **Mapping 施工真源（仓内）** | `agent-delivery/data/data-design/企业/企业域-ETL-Mapping明细-源表到DWD.md`（v1.2） |
| GDF 派单包（企业 · 现行草稿） | `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v2/`（**v2.1 · 暂缓投递**） |
| 包内 Mapping 快照 | `…/09-企业域-ETL-Mapping明细-源表到DWD.md` |
| 导读 | `…/09-企业维-ODS到DWD-Mapping说明-v4.md` |
| DWD 建表快照 | `…/10-DWD-MySQL-DDL/` |
| 贴源表清单 | `…/02-WaveA-贴源表清单.yaml` |
| 作废对照 | `…/11-作废与误源对照.md` |
| 建议 ETL 顺序 | Mapping 明细 §2 / 导读 §2 |
| 历史包（建表勿用） | `…/GDF-ENT-WORKPACK-v1/` |

## 调度（OPEN-ENT-FLOW-01 · 部分）

| 项 | 状态 |
|---|---|
| 正式 GDF cron/DAG 名 | **仍开放**（产线未回写本仓） |
| Demo 模拟调度 | 与正式同构；按 Mapping 明细顺序 |
| 门禁 | 源侧默认 `is_deleted=0`；失败不晋升下游（见 `01-data-flow`） |
| 已知阻塞 | `enterprise_industry_chain` 信用代码空 → org_id 难回填（明细 §5 #6） |
