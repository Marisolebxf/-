# GDF-FIN-WORKPACK-v1

> **读者**：GDF 数据中台产线（不使用 Cursor）  
> **版本**：v1.0（2026-11-09）· **成包绿 + DDL 绿**；CDC DRAFT 已预填。**不代表**已灌数、已回传、已跑通  
> **任务**：`GDF-FIN-WORKPACK-L01`（WBS-06-04B，成包）· 监管人 `human:淮政玮` · 跑通叶 `SYSINT-06-04-L01`  
> **完成门槛（强制）**：**成包绿 + DDL 绿 + `SYSINT-06-04-L01` 跑通**（回传后 Java 只读 ADS）。本包 done ≠ 跑通  
> **优先级**：市场研究红标 **第 2**（第 1 是 `GDF-MACRO-WORKPACK`）。可并行成包；与落地实效无关；**不与 MACRO 并包**  
> **范围**：金融要素库 **物理表 31 张**（行数报告列 32 行，`dwd_corp_basic_info` 重复一次）。v1 洗 19 张 → 11 张 `fin_*`；P2 / 0 行表只贴不洗；3 张归企业包  
> **结构真源**：源表列以 **live `gkx`** 为准（`00` §0.3）；09 / 09a 取自 20261109 行数报告，不是 live  
> **Mapping 施工真源**：[09-金融域-ETL-Mapping明细-源表到DWD.md](09-金融域-ETL-Mapping明细-源表到DWD.md)  
> **建表 DDL**：[10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)（**已绿**：`check_gdf_ddl.py --dimension fin` 通过）  
> **环境红线**：GDF 只读 `gkx` + 写 `gkxlumenx_*`，禁读写 demo 库

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 声明（优先级 / 与实效无关 / 不并包 / live 为准）、分期策略、边界、开放项 |
| [01-命名与分层词典.md](01-命名与分层词典.md) | 命名对齐 |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 31 张物理表分类：P0 / P1 洗，P2 / 0 行只贴，3 张归 ENT-v4（生成件） |
| [03-连接与网络.md](03-连接与网络.md) | 连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | `is_deleted = 0`、技术字段、大表策略 |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | 7 个作业，互不依赖 |
| [09-金融域-ETL-Mapping明细-源表到DWD.md](09-金融域-ETL-Mapping明细-源表到DWD.md) | **正式 Mapping**（P0 / P1 → 11 张 `fin_*`；§3.4 起由脚本生成） |
| [09a-源表业务列清单-金融31表.md](09a-源表业务列清单-金融31表.md) | 31 张源表业务列（生成件，非 live） |
| [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/README.md) | DWD 11 张 + ADS 4 张建表**草稿** |
| [11-作废与误源对照.md](11-作废与误源对照.md) | 误源 |
| [12-ADS后加工-金融.md](12-ADS后加工-金融.md) | ② 4 张金融 ADS 口径与 SQL 草稿；Java 只读 |
| [script/](script/gen_fin_pack.py) | 本侧生成 / 自检脚本（`--check`）。GDF 不需要运行 |
| [CHANGELOG.md](CHANGELOG.md) | 版本 |

## 投递约定

- 顺序：Wave A → DDL → Wave B → ② ADS。P0 先于 P1。
- **P2 日行情 / 期权 / 外汇、公募基金 0 行表本期只贴不洗**。融资 / 投资 / 并购事件三表归 ENT-v4，**本包不重复配贴源作业**。
- 本包没有写 ES、图谱、向量库的环节。
- 当前通用 `parse_workpack.py` 未识别 FIN 字段矩阵。自动预填前须补解析规则，或由 GDF 按 09 人工配置；**禁止把空字段矩阵当完成**。
- 客户决策 Q-SVC-006（金融要素库是否纳入交付范围、何时灌数，🟡 待甲方）未闭合：本包成包不代替答复。
- 密码不进本包。不要用 Demo `demo_gkxlumenx_*` 当产线目标。
