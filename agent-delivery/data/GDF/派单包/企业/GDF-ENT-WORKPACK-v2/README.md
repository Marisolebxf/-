# GDF-ENT-WORKPACK-v2

> **读者**：GDF 数据中台产线团队（不使用 Cursor）  
> **版本**：v2.1（2026-08-13）· **暂缓投递**（本侧对齐 Mapping 明细后再发）  
> **承诺表真源**：`third-party-source/doc/` + `md-extract/`  
> **Mapping 施工真源**：[09-企业域-ETL-Mapping明细-源表到DWD.md](09-企业域-ETL-Mapping明细-源表到DWD.md)  
> **建表 DDL**：[10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)  
> **本侧对接**：见 `00-派单说明书.md`

## 相对 v2.0 的增量

| 项 | v2.0 | **v2.1** |
|----|------|----------|
| Mapping | 短版 `09` v4 字段表 | **以 `企业域-ETL-Mapping明细` v1.2 全文为准**（包内嵌入） |
| Wave A | 40 表旧清单 | 对齐明细：纳入 financing/invest/tag/subsidiary/patent/chain_dtl 等 |
| DDL | 工商/风险/指标 | 刷新快照；强调 **recruit + forg_*** |

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 目标、边界、作废清单、Wave A/B、DoD |
| [01-命名与分层词典.md](01-命名与分层词典.md) | 命名对齐 |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 贴源清单（v2.1） |
| [03-连接与网络.md](03-连接与网络.md) | 连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | 过滤规则 |
| [05-WaveA-验收检查表.md](05-WaveA-验收检查表.md) | Wave A 回签（表名以 `02` 为准，验收表需按新清单勾选） |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | Mapping/ETL 派工 |
| [07-启动会材料.md](07-启动会材料.md) | 启动会 |
| [08-WaveB-Mapping基线刷新-v3-draft.md](08-WaveB-Mapping基线刷新-v3-draft.md) | 表级辅助（细节以明细为准） |
| [09-企业域-ETL-Mapping明细-源表到DWD.md](09-企业域-ETL-Mapping明细-源表到DWD.md) | **正式 Mapping 字段说明** |
| [09-企业维-ODS到DWD-Mapping说明-v4.md](09-企业维-ODS到DWD-Mapping说明-v4.md) | 导读（非字段全文） |
| [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/) | 建表 / ALTER 真源 |
| [11-作废与误源对照.md](11-作废与误源对照.md) | 误源对照 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更 |

## 投递约定

- **当前不对外投递**；定稿后再发 zip + 版本号 `GDF-ENT-WORKPACK-v2.1`。  
- 建表只认 `10/`；Mapping 只认 **`09-企业域-ETL-Mapping明细…`**。  
- 密码不进本包。
