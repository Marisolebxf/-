# GDF-ENT-WORKPACK-v3

> **读者**：GDF 数据中台产线团队（不使用 Cursor）  
> **版本**：v3.1.5（2026-10-19）· **可对外投递** · 四块收口见 `00` §9 · 加工逻辑补遗见 CHANGELOG v3.1.5  
> **GDF 作业面**：贴源只 `gkx`→`gkxlumenx_ods`；洗数只 `gkxlumenx_dwd`。不管 `demo_gkxlumenx_*`。  
> **task**：`GDF-ENT-WORKPACK-V3-L01` · Owner `human:徐滕强`  
> **承诺表真源**：`third-party-source/doc/` + `md-extract/`  
> **Mapping 施工真源**：[09-企业域-ETL-Mapping明细-源表到DWD.md](09-企业域-ETL-Mapping明细-源表到DWD.md)  
> **建表 DDL**：[10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)  
> **ES 更新**：[12-DWD到ES.md](12-DWD到ES.md)（17 模块分开触发；写库 = `lumen-etl-es-py`）  
> **图谱更新**：[14-DWD到图谱.md](14-DWD到图谱.md)（GDF 表→op 日批 + 菜单）  
> **GDF 调度**：[15-GDF触发调度与回执.md](15-GDF触发调度与回执.md)（**当前 §6.1** 飞书值班；§4 Java/callback 未上线；GDF 不写库）  
> **本侧对接**：见 `00-派单说明书.md`

相对 v2.1：继承贴源 / Mapping / DDL，新增 ES 更新逻辑卷 + 图谱更新边界卷；七项遗留已在 `00` §8 留下核验与监管人确认记录。`OPEN-ENT-FLOW-01/04` 与图谱 OPEN 保持独立，不能写成事实已补齐。

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 目标、边界、§8 确认、**§9 四块 as-built** |
| [01-命名与分层词典.md](01-命名与分层词典.md) | 命名对齐 |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 贴源清单（继承 v2.1） |
| [03-连接与网络.md](03-连接与网络.md) | 连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | 过滤规则 |
| [05-WaveA-验收检查表.md](05-WaveA-验收检查表.md) | Wave A 回签（表名以 `02` 为准） |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | Mapping/ETL 派工 |
| [07-启动会材料.md](07-启动会材料.md) | 启动会 |
| [08-WaveB-Mapping基线刷新-v3-draft.md](08-WaveB-Mapping基线刷新-v3-draft.md) | 表级辅助（细节以明细为准） |
| [09-企业域-ETL-Mapping明细-源表到DWD.md](09-企业域-ETL-Mapping明细-源表到DWD.md) | **正式 Mapping 字段说明** |
| [09-企业维-ODS到DWD-Mapping说明-v4.md](09-企业维-ODS到DWD-Mapping说明-v4.md) | 导读（非字段全文） |
| [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/) | 建表 / ALTER 真源 |
| [11-作废与误源对照.md](11-作废与误源对照.md) | 误源对照 |
| [12-DWD到ES.md](12-DWD到ES.md) | **v3**：17 模块分开触发 / 水位 / Painless |
| [13-现网DDL差集-GDF开工必读.md](13-现网DDL差集-GDF开工必读.md) | **开工必读**：正式库 as-built + 源表阻塞；GDF 不管 demo |
| [14-DWD到图谱.md](14-DWD到图谱.md) | **v3**：表→op 日批 + 菜单 / VID / 禁止灌数建图 |
| [15-GDF触发调度与回执.md](15-GDF触发调度与回执.md) | **v3**：GDF 触发、异步、回执、现网缺口 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更 |

## 投递约定

- **可对外投递给 GDF**；仍不得把未回签的 Wave A/B 当成「已导入绿」。  
- 开工必读 [13-现网DDL差集-GDF开工必读.md](13-现网DDL差集-GDF开工必读.md)。  
- 建表只认 `10/`；Mapping 只认 **`09-企业域-ETL-Mapping明细…`**。  
- 写 ES 只认 `lumen-etl-es-py`；GDF **当前**只飞书通知本侧（`15` §6.1），不直连 Python、不配 `/ent/v1`。  
- 写图谱：日批按 `14` 表→op 触发；菜单给人用；GDF / 灌数不准写 Nebula。  
- 密码不进本包。  
- **不要**抄 `GDF-ENT-WORKPACK-v2` / v2.1 当现行施工包。
