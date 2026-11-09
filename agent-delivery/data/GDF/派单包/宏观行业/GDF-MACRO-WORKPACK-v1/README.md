# GDF-MACRO-WORKPACK-v1

> **读者**：GDF 数据中台产线（不使用 Cursor）  
> **版本**：v1.0.0（2026-11-09）· **首版成包** · 可投递草稿；**未建表、未灌数、未在 GDF 上跑通**  
> **优先级**：**市场研究红标第 1（P0）**。现行「深圳政策现状分析」落地实效城市卡读宏观表，产线化优先于金融、行业分析。  
> **任务**：`GDF-MACRO-WORKPACK-L01`（WBS-06-05B，成包）· 跑通叶 `SYSINT-06-05-L01`（WBS-06-05，另叶，本包 done 不等于它 done）· Owner `human:淮政玮`  
> **范围**：供应方「宏观行业要素库」六张表。① 贴源 + Mapping 到项目 DWD；② 城市宏观截面 ADS（②a）；落地实效结果面代理只作附录（②b）。  
> **不含**：金融数据（另包 `GDF-FIN-WORKPACK`）、行业分析（只贴 ODS，另裁定）、政策主路径（不并入 `GDF-POLICY-WORKPACK-v2`）。  
> **口径真源**：[pipeline-macro-effect-proxy.md](../../../../data-design/storage/POLICY/etl/pipeline-macro-effect-proxy.md)（白名单 `macro-eff-v1`、区划键、已知局限）  
> **三方源结构真源**：`third-party-source/gkx-mysql-raw/加工/GKX数据源表及行数报告-20261109-1026.MD`（宏观行业要素库六表）  
> **Mapping 施工真源**：[09-宏观行业域-ETL-Mapping明细-源表到DWD.md](09-宏观行业域-ETL-Mapping明细-源表到DWD.md)  
> **建表 DDL**：本包 [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)（草稿，见该目录 README）  
> **环境红线**：GDF 只读真源 `gkx` + 写 `gkxlumenx_*` 正式库，禁读写 demo（`demo_gkxlumenx_*`）

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 优先级声明、目标、边界、A → B → ②a、作废清单、OPEN 项 |
| [01-命名与分层词典.md](01-命名与分层词典.md) | 供应方 `gkx.dwd_*` = 本项目 ODS；六表在 ODS / DWD 的名字 |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 六张 P0 贴源；`default_filter` 为空 |
| [03-连接与网络.md](03-连接与网络.md) | 连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | 取数无行过滤；**区划反解**；`area_code_type=1`；维度键 join；单位坑 |
| [05-WaveA-验收检查表.md](05-WaveA-验收检查表.md) | 贴源回签 |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | 六张 DWD 的洗法与顺序（维度先于事实） |
| [09-宏观行业域-ETL-Mapping明细-源表到DWD.md](09-宏观行业域-ETL-Mapping明细-源表到DWD.md) | **正式 Mapping**（逐表逐字段 + 派生列） |
| [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/) | 六张 DWD 建表草稿 + 现网核对说明 |
| [11-作废与误源对照.md](11-作废与误源对照.md) | 误源 |
| [12-DWD后加工-城市截面ADS与实效代理附录.md](12-DWD后加工-城市截面ADS与实效代理附录.md) | ②a 城市截面 ADS（建表草稿 + 灌数 SQL + 血缘占位）；②b 实效代理**仅附录** |
| [sql/check_area_resolve.sql](sql/check_area_resolve.sql) | 只读自检：区划反解分布、键唯一、维度孤儿（已在 gkx 实跑一次） |
| [CHANGELOG.md](CHANGELOG.md) | 版本 |

## 投递约定

- 顺序：Wave A（六表贴源）→ Wave B（五张维度 → 事实表）→ ②a（事实表成功后灌城市截面 ADS）。
- Wave A/B 只覆盖贴源 + Mapping，**不含**写 ES、Nebula、图谱，**不含**任何算法。②a 是纯 SQL 聚合，不是算法。
- **②b 不是交付物**。不建作业、不建表。它是落地实效代理改读 ADS 时的口径附录，要等 QPOL-02 / 新决策会签。禁止把宏观代理写进 `M_POLICY_IMPLEMENTATION_EFFECT` 的正本三维。
- 当前不代表已建表或已灌数。CDC 预填归下一叶；导入核对归 GDF。通用 `parse_workpack.py` 对本包字段矩阵的识别**未验证**，预填前须补解析规则或按 **09** 人工配置，禁止把空字段矩阵当完成。
- 数据是供应方样本：事实表与区划表行数都恰为 20,000（整数上限）。补全量后行数、白名单覆盖会变，见 `00` §6 OPEN-MACRO-02。
- 密码不进本包。不要用 Demo `polan/ods_sync.py` / `demo_gkxlumenx_*` 当产线目标。
