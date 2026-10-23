# GDF-POLICY-WORKPACK-v1

> **读者**：GDF 数据中台产线（不使用 Cursor）  
> **版本**：v1.0.3（2026-10-23）· **Mapping 已冻结可投递；待 GDF 预填/导入核对** · MAP-01 已关（永远分 UK） · Wave C 为 DWD 之后的抽取/条款，不进 CDC 字段矩阵；两作业交付 Python 脚本，逻辑与算法 demo 中台同一模块  
> **贴源结构真源**：`data-design/storage/POLICY/sources/ods-ddl.md`  
> **Mapping 施工真源**：[09-政策域-ETL-Mapping明细-源表到DWD.md](09-政策域-ETL-Mapping明细-源表到DWD.md)  
> **建表 DDL**：本包 [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)（产线目标列快照）  
> **本侧对接**：见 `00-派单说明书.md` · task `GDF-POLICY-WORKPACK-V1-L01`

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 目标、边界、Wave A/B、DoD |
| [01-命名与分层词典.md](01-命名与分层词典.md) | 命名对齐 |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 贴源清单 |
| [03-连接与网络.md](03-连接与网络.md) | 连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | 过滤规则 |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | Mapping 派工 |
| [09-政策域-ETL-Mapping明细-源表到DWD.md](09-政策域-ETL-Mapping明细-源表到DWD.md) | **正式 Mapping** |
| [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/) | 建表指针 + 产线列快照 |
| [11-作废与误源对照.md](11-作废与误源对照.md) | 误源对照 |
| [12-DWD后加工-抽取产业与条款结构化.md](12-DWD后加工-抽取产业与条款结构化.md) | Wave B 成功后的抽取产业、条款结构化 |
| [CHANGELOG.md](CHANGELOG.md) | 版本 |

## 投递约定

- Wave A/B 只覆盖贴源 + Mapping，**不含**写 ES、Nebula。  
- Wave C（[12](12-DWD后加工-抽取产业与条款结构化.md)）在 B 成功之后触发：抽取产业写 `policy_industry_rel`（DWD 再同步 ADS），条款结构化只合并 ADS `policy_text_parse` 的条款。两作业都不改主表。交付物是 Python 脚本，逻辑与算法 demo 中台同一模块，禁止 CDC 另写。正式 Java 门面未落地前，不要把 Demo 路由配进生产 DAG。  
- 当前不代表已建表或已灌数。CDC 预填归胡森泉下一叶；导入核对归辜少彬。  
- 通用 `parse_workpack.py` 已能读出 Wave A=2、Wave B 目标表 1 张（`policy_base_info`），**字段行仍为 0**（解析器只认 `enterprise_*`/`risk_*` 节标题）。须补解析规则或按 **09** 人工配置。禁止把空字段矩阵当完成。  
- 建表认 `10`；Mapping 只认本包 **09 明细**。`storage/POLICY/etl/ods-to-dwd-mapping.md` 仍是 draft 对照，**不是**施工真源。  
- 密码不进本包。  
- **不要**用 Demo `polan/ods_sync.py` / `demo_gkxlumenx_*` / 旧 v1 37 列当产线目标或贴源结构。
