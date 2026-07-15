# 三方 ODS 源连接（只读）

> **身份**：项目上总集交付的采购数据输出库 = **本项目当前 ODS 贴源真源（运行时）**。  
> **角色**：`gkx_reader_zp` 为只读账号；禁止写库、禁止改算法 demo 灌数目标。  
> **密码**：不进本文件；见同目录 `.env.local`（已被编排仓 `.gitignore` 忽略）或本地密钥库。

## 连接元数据（可提交）

| 项 | 值 |
|----|-----|
| 引擎 | MySQL（供应方标注 8.0；2026-07-15 实测 `VERSION()` = **9.7.0-commercial**） |
| Host | `183.240.141.251` |
| Port | `3318` |
| Database | `gkx` |
| User | `gkx_reader_zp` |
| 权限 | 只读（reader） |
| 来源 | 项目上总集 / 采购数据输出库（人工确认可直连） |

## 环境变量约定（数据工厂 / 只读 profile 用）

```text
GKX_ODS_MYSQL_HOST=183.240.141.251
GKX_ODS_MYSQL_PORT=3318
GKX_ODS_MYSQL_USER=gkx_reader_zp
GKX_ODS_MYSQL_PASSWORD=<见 .env.local>
GKX_ODS_MYSQL_DB=gkx
```

## 与仓库内其他库的边界

| 对象 | 关系 |
|------|------|
| 本库 `gkx` @ `183.240.141.251:3318` | **当前 ODS 贴源（运行时）** |
| `要素库建表语句.sql`（约 186/192 表） | 旧文档基线，仅作差异对照 |
| 本目录 `gkx_schema_ddl.sql`（421 表） | 同库结构沙箱快照（与 live 表数一致） |
| `demo-algo-science` → MySQL `innov` | 算法 demo 灌数目标，**不是**本 ODS |
| `demo-algo-ent-analysis` → PG `demo_gdf_data` | 企业算法 demo，**不是**本 ODS |

## 连通抽检（2026-07-15）

- AUTH：OK（`gkx_reader_zp` → `gkx`）
- `SHOW TABLES`：421（dwd 256 / ods 165 / bak 57）——与本目录 DDL 沙箱一致
- 行数粗看（`information_schema.TABLE_ROWS`，非精确）：如 `dwd_en_paper_cited_by` ~22 万级

## 铁律

1. 对三方库只读查询 / 结构 profile / 字段映射；**不** `INSERT/UPDATE/DDL`
2. **不**把本连接写入 `repos/demo-algo-*/conf/settings.yaml`（除非 PM + 架构师明示切源）
3. 供应方表名 `dwd_*` 在本项目分层仍视为 **ODS 原料**，勿与自建 `dwd.enterprise*` 混淆

## Demo 映射灌数（已做）

| 项 | 说明 |
|----|------|
| 脚本 | `repos/demo-algo-science/scripts/seed_ods_chain_to_innov.py` |
| 源 | `dwd_industry_chain_info` / `dwd_industry_chain_news_info` |
| 目标（现） | PG `demo_gdf_data@117.50.223.145` → `dwd.chain` / `dwd.chain_node` / `dwd.chain_news`（1B+2B） |
| 整库迁移 | `repos/demo-algo-science/scripts/migrate_innov_mysql_to_pg.py`（MySQL innov → 同上 PG） |
| 链 | `IC0007` 集成电路、`IC9901` 低空经济（追加，保留 `CH001`–`CH008` mock） |
