# 三方原始库 `gkx`（MySQL）— 隔离沙箱

> **用途**：当前项目 **ODS 贴源**（运行时连接 + 结构沙箱）。  
> **连接说明**：[CONNECTION.md](CONNECTION.md)（密码仅在本地 `.env.local`）。  
> **不影响**：算法 demo 库（`innov` / `demo_gdf_data`）、自建 DWD/ADS——未获明示前不改其 settings。

## 边界（铁律）

| 允许 | 禁止 |
|------|------|
| 只读连 ODS、DDL / 清单 / 对照笔记 | 改 `repos/demo-algo-*/conf/settings.yaml` |
| 对照 `要素库建表语句.sql` / ODS v2 清单 | 往生产 / demo ADS 灌数；对本库写操作 |
| 为后续 `E-PLATFORM-P1-L01` 提供结构/连接真源 | 把供应方 `dwd_*` 当成自建 DWD 直接上线 |

## 分层口径（本项目）

- 供应方大量表名是 `dwd_*`，在本项目数据分层中视为 **ODS 贴源原料**，勿与自建 `dwd.enterprise*` 等混淆。
- `ods_*`：贴源侧镜像 / 上游表。
- `*_bak_20260710`：历史备份，结构分析时可排除。

## 本批产物

| 文件 | 说明 |
|------|------|
| `gkx_schema_ddl.sql` | 从对话粘贴的完整 CREATE TABLE（~0.9MB） |
| `table_list.txt` | 去重表名列表（421） |
| `table_inventory.md` | 统计 + 全量表名 |
| `ANALYSIS.md` | 与旧要素库 DDL 的对照摘要 |
| `_extract_ddl.py` | 从 agent transcript 再提取用的脚本 |

## 统计（2026-07-15）

- CREATE TABLE（去重）：**421**
- `dwd_*`：**256**（含 bak）
- `ods_*`：**165**（含 bak）
- `*_bak_*`：**57**
- 活跃表（排除 bak）：**364**（dwd 206 + ods 158）

## 来源

- 用户粘贴的 `gkx` 库定义（chat / agent transcript）
- 提取脚本：`_extract_ddl.py`（读 transcript JSONL → 写本目录）

## 下一步（未做）

1. 字段级映射到自建 ODS/DWD/ADS（需认领 `E-PLATFORM-P1-L01` 后进行）
2. 与公司 PG `gkx_szc_ods`（`ods.gkx_dwd_*`）命名对照
3. 只读 profile（精确行数 / 空值 / 主键），仍不落生产、不改算法灌数目标
