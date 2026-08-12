# GDF-ENT-WORKPACK-v1

> **【已作废 · 禁止用于建表 / ALTER】** 2026-08-13 起由  
> [`../GDF-ENT-WORKPACK-v2/`](../GDF-ENT-WORKPACK-v2/) **v2.0** 取代。  
> 本包内指向 `DWD表结构设计-企业模块.md`（旧 PG）的路径 **无效**。请改用 v2 的 `10-DWD-MySQL-DDL/` + `09` Mapping v4。

> **读者**：GDF 数据中台产线团队（不使用 Cursor）  
> **版本**：v1.3（2026-07-31）— **建表用途已作废**  
> **承诺表真源**：`third-party-source/doc/` + `md-extract/`  
> **范围**：企业维 Wave A **40** 张贴源 + **Mapping v3（`09`）**；不含量子 company / 海洋 / 专利  
> **本侧对接**：数据 Lead / GDF 对接人见 `00-派单说明书.md`

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 目标、边界、Wave A/B、DoD、节奏 |
| [01-命名与分层词典.md](01-命名与分层词典.md) | 命名对齐（必读） |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 承诺表清单 + P0/P1 |
| [03-连接与网络.md](03-连接与网络.md) | 源/目标连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | `is_deleted`、技术字段、禁止写源库 |
| [05-WaveA-验收检查表.md](05-WaveA-验收检查表.md) | Wave A 表级回签 |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | Mapping/ETL 派工与交付 |
| [07-启动会材料.md](07-启动会材料.md) | 口播稿、议程、网络互通、密钥渠道 |
| [08-WaveB-Mapping基线刷新-v3-draft.md](08-WaveB-Mapping基线刷新-v3-draft.md) | 表级对照（辅助） |
| [09-企业维-ODS到DWD-Mapping说明-v3.md](09-企业维-ODS到DWD-Mapping说明-v3.md) | **正式 Mapping 字段说明（施工真源）** |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更 |

## 投递约定

- 飞书群 / 云盘只发**本目录链接或 zip + 版本号**，不散发表名。
- 变更只走 `CHANGELOG.md` 增量，口头改表无效。
- 密码、账号密钥**不进本包**，走线下密钥渠道（见 `07-启动会材料.md`）。
- Mapping：**只认 `09` v3**；历史 v2 勿施工。
