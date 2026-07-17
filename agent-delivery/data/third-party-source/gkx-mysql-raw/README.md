# 三方原始库 `gkx`（MySQL）— 隔离沙箱

> **用途**：当前项目 **入站贴源**（运行时连接 + 结构沙箱）。  
> **连接说明**：[CONNECTION.md](CONNECTION.md)（密码仅在本地 `.env.local`）。  
> **供应方工作约束**：[SUPPLIER-WORK-CONSTRAINTS.md](SUPPLIER-WORK-CONSTRAINTS.md)（2026-07-17 起必读）。  
> **不影响**：算法 demo 库（`innov` / `demo_gdf_data`）、自建 DWD/ADS——未获明示前不改其 settings。

## 边界（铁律）

| 允许 | 禁止 |
|------|------|
| 只读连库、对 **`dwd_*`** 做 DDL / 清单 / 对照 / profile | 改 `repos/demo-algo-*/conf/settings.yaml` |
| 对照 `要素库建表语句.sql` / ODS v2 清单 | 往生产 / demo ADS 灌数；对本库写操作 |
| 为 `E-PLATFORM-P1-L01` 等提供结构/连接真源 | 把供应方 `dwd_*` 当成自建 DWD 直接上线 |
| 登记「查不到的表」待供应方核验 | 以 `ods_*` 作为正式映射或算法输入真源 |

## 分层口径（供应方 + 本项目）

| 视角 | 口径 |
|------|------|
| **供应方** | `ods_*` = 贴源（其侧清洗加工，**不对项目暴露**）；**`dwd_*` = 对项目开放的明细** |
| **本项目** | 入站只读 **`dwd_*`** → 数据工厂 → 自建 DWD / DWS / ADS |
| **命名风险** | 供应方 `dwd_*` ≠ 本项目自建 `dwd.*` / `dwd.enterprise*` |

另：`*_bak_20260710` 等备份表做结构分析时可排除，勿进映射主路径。

## 本批产物

| 文件 | 说明 |
|------|------|
| `CONNECTION.md` | 连接元数据 + 铁律（无密码） |
| `SUPPLIER-WORK-CONSTRAINTS.md` | **供应方工作约束**（分层暴露、技术字段、字段未定稿、缺表核验） |
| `.env.local` | 本地密码（gitignore，勿提交） |
| `gkx_schema_ddl.sql` | 从对话粘贴的完整 CREATE TABLE（~0.9MB） |
| `table_list.txt` | 去重表名列表（421） |
| `table_inventory.md` | 统计 + 全量表名 |
| `ANALYSIS.md` | 与旧要素库 DDL 的对照摘要 |
| `_extract_ddl.py` | 从 agent transcript 再提取用的脚本 |

## 统计（2026-07-15）

- CREATE TABLE（去重）：**421**
- `dwd_*`：**256**（含 bak）— **正式工作面**
- `ods_*`：**165**（含 bak）— 可见但不作正式输入
- `*_bak_*`：**57**
- 活跃表（排除 bak）：**364**（dwd 206 + ods 158）

## 来源

- 用户粘贴的 `gkx` 库定义（chat / agent transcript）
- 供应方 2026-07-17 澄清（工作约束 + 公网直连）
- 提取脚本：`_extract_ddl.py`（读 transcript JSONL → 写本目录）

## 下一步（未做）

1. 字段级映射到自建 DWD/ADS（认领 `E-PLATFORM-P1-L01` 后；**仅 `dwd_*` + 识别六技术字段**）
2. 与公司 PG `gkx_szc_ods`（`ods.gkx_dwd_*`）命名对照
3. 只读 profile（精确行数 / 空值 / 主键）；缺表清单交供应方核验后回写
