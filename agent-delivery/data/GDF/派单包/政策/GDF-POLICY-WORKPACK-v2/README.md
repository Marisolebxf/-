# GDF-POLICY-WORKPACK-v2

> **读者**：GDF 数据中台产线（不使用 Cursor）  
> **版本**：v2.0.2（2026-10-26）· **现行政策包** · Mapping 继承 v1.0.4，可投递；待 GDF 预填 / 导入核对 · MAP-01 已关（永远分 UK） · 取数不过滤 `is_deleted` / `is_history`，原样进 DWD，应用侧再滤 · `16` 为字典核对，不改 `09` 列规则 · Wave C 脚本在 `scripts/`，流程图在 `12`  
> **任务**：`GDF-POLICY-WORKPACK-V2-L01` · Owner `human:淮政玮`  
> **贴源结构真源**：`data-design/storage/POLICY/sources/ods-ddl.md`  
> **Mapping 施工真源**：[09-政策域-ETL-Mapping明细-源表到DWD.md](09-政策域-ETL-Mapping明细-源表到DWD.md)  
> **建表 DDL**：本包 [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)  
> **历史包**：v1 只留对照，禁止当现行施工包

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 目标、边界、A → B → C |
| [01-命名与分层词典.md](01-命名与分层词典.md) | `gkx.dwd_*` = 本项目 ODS |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 两张 P0；`default_filter` 为空 |
| [03-连接与网络.md](03-连接与网络.md) | 连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | 取数无行过滤 |
| [05-WaveA-验收检查表.md](05-WaveA-验收检查表.md) | 贴源回签 |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | 洗入一张 `policy_base_info`；C 不进字段配置 |
| [09-政策域-ETL-Mapping明细-源表到DWD.md](09-政策域-ETL-Mapping明细-源表到DWD.md) | **正式 Mapping** |
| [16-Mapping过程与字典核对.md](16-Mapping过程与字典核对.md) | 过程是否清楚、字典实值是否齐。不改 09 |
| [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/) | 主表 + 产业关联表 |
| [11-作废与误源对照.md](11-作废与误源对照.md) | 误源 |
| [12-DWD后加工-抽取产业与条款结构化.md](12-DWD后加工-抽取产业与条款结构化.md) | C1 / C2 流程图、读写、脚本 |
| [scripts/](scripts/) | `policy_c1_industry.py`、`policy_c2_clauses.py`，复制到 GDF Python 节点 |
| [13-现网DDL差集-GDF开工必读.md](13-现网DDL差集-GDF开工必读.md) | 只核产线库；缺列只 ADD |
| [15-GDF触发调度与回执.md](15-GDF触发调度与回执.md) | B 成功后在 GDF 节点上跑两份脚本 |
| [CHANGELOG.md](CHANGELOG.md) | 相对 v1.0.4 |

## 投递约定

- 顺序：Wave A → Wave B → Wave B 当日 `success` 之后才触发 C。C 失败不回滚已成功的 B。
- Wave A/B 只覆盖贴源 + Mapping，**不含**写 ES、Nebula。C 不进 09，也不进 CDC 字段矩阵。
- C1 只写 `policy_industry_rel`（DWD 同一事务同步 ADS 同名表）。C2 只合并 ADS `policy_text_parse` 的条款。两作业都不改主表。
- 交付物是 `scripts/` 里两份 Python。GDF 复制到自己的 Python 节点后执行。不配置内部 HTTP。检索或模型失败不写假结果。本叶未在 GDF 上跑通。
- 国内政策、国外政策另叶不并进本包。不补企业包的 `07` / `08` / `14`。
- 当前不代表已建表或已灌数。CDC 预填归胡森泉下一叶；导入核对归辜少彬。包文件齐了才可以预填，本叶不出 xlsx。
- 通用 `parse_workpack.py` 能读出 Wave A=2、Wave B 目标表 1 张（`policy_base_info`），**字段行仍为 0**（解析器只认 `enterprise_*` / `risk_*` 节标题）。预填须先补解析规则，或按 **09** 人工配置。禁止把空字段矩阵当完成。
- 密码不进本包。不要用 Demo `polan/ods_sync.py` / `demo_gkxlumenx_*` / 旧 v1 37 列当产线目标。
