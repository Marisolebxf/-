# GDF 派单包（人类可读）

> GDF 数据中台团队**不使用 Cursor**。对外沟通用本目录工作包 + 飞书/例会，不用智能体派单话术。

| 工作包 | 范围 | 版本 |
|--------|------|------|
| [企业/GDF-ENT-WORKPACK-v2](企业/GDF-ENT-WORKPACK-v2/) | 贴源 + **MySQL DDL（`10/`）** + **Mapping 明细（`09-企业域-…`）** → `gkxlumenx_dwd` | **v2.1**（2026-08-13）· **现行草稿 · 暂缓投递** |
| [企业/GDF-ENT-WORKPACK-v1](企业/GDF-ENT-WORKPACK-v1/) | 历史包；DWD 指针误指旧 PG 稿 | v1.3 · **建表已作废** |
| [产业链/GDF-CHAIN-WORKPACK-v1](产业链/GDF-CHAIN-WORKPACK-v1/) | 产业链四表贴源+洗链树/`entity_rel`；分析六表只贴不洗 | **v1.0**（2026-09-01）· **Mapping 已确认；待 GDF 预填/导入核对** |

企业建表 / ALTER：**只认企业 v2 包内 `10-DWD-MySQL-DDL/`**。
Mapping：各域只认各自现行包 README 指定的 `09-*Mapping明细*`；短版导读不作施工真源。
