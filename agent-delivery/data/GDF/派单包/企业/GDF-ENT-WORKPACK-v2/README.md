# GDF-ENT-WORKPACK-v2

> **读者**：GDF 数据中台产线团队（不使用 Cursor）  
> **版本**：v2.0（2026-08-13）  
> **承诺表真源**：`third-party-source/doc/` + `md-extract/`  
> **范围**：企业维 Wave A **40** 张贴源 + **Mapping v4（`09`）** + **MySQL DWD DDL（`10/`）**  
> **本侧对接**：数据 Lead / GDF 对接人见 `00-派单说明书.md`

## 相对 v1 的关键纠偏

| 项 | v1.3（已作废建表） | **本包 v2.0** |
|----|-------------------|---------------|
| DWD 建表真源 | 误指已归档 PG 稿 `DWD表结构设计-企业模块.md` | **只认本包 `10-DWD-MySQL-DDL/`** |
| 引擎 / 库 | 易混用 PG / `demo_gdf_data` | **仅 MySQL 8 · `gkxlumenx_dwd`** |
| 企业主表 | 旧宽表 `enterprise` **禁止** | **`enterprise_base`（`org_id`）** |
| Mapping | `09` v3 | **`09` v4**（字段矩阵同 v3 + DDL 差集附录） |

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 目标、边界、作废清单、Wave A/B、DoD |
| [01-命名与分层词典.md](01-命名与分层词典.md) | 命名对齐（必读） |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 承诺表清单 + P0/P1（同 v1.3） |
| [03-连接与网络.md](03-连接与网络.md) | 源/目标连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | `is_deleted`、技术字段、禁止写源库 |
| [05-WaveA-验收检查表.md](05-WaveA-验收检查表.md) | Wave A 表级回签 |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | Mapping/ETL 派工；DDL 验收对照 `10/` |
| [07-启动会材料.md](07-启动会材料.md) | 口播稿、议程、网络互通、密钥渠道 |
| [08-WaveB-Mapping基线刷新-v3-draft.md](08-WaveB-Mapping基线刷新-v3-draft.md) | 表级对照（辅助） |
| [09-企业维-ODS到DWD-Mapping说明-v4.md](09-企业维-ODS到DWD-Mapping说明-v4.md) | **正式 Mapping 字段说明（施工真源）** |
| [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/) | **建表 / ALTER 唯一真源（快照）** |
| [11-作废与误源对照.md](11-作废与误源对照.md) | 旧 PG 9 表 / 三方参考 / v1 指针 → 新表 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更 |

## 投递约定

- 飞书群 / 云盘只发**本目录链接或 zip + 版本号 `GDF-ENT-WORKPACK-v2.0`**，不散发表名；**同时声明 v1 作废**。
- 变更只走 `CHANGELOG.md` 增量，口头改表无效。
- 密码、账号密钥**不进本包**，走线下密钥渠道（见 `07-启动会材料.md`）。
- 建表/ALTER：**只认 `10/`**；Mapping：**只认 `09` v4**。历史 v1 / Mapping v2/v3 / 「三方参考 DWD 清单」**勿施工**。
