# 三方原始库 `gkx`（MySQL）— 数据源表结构

> **本目录根下只描述：已确定表结构的入站数据源。**  
> **加工 / 映射 / 全量对照 / 工具** → 见子目录 [`加工/`](加工/)。

## 数据源文件（根目录）

| 文件 | 说明 |
|------|------|
| [SOURCE-TABLES.md](SOURCE-TABLES.md) | **当前工作面**：已确认结构的入站表（供应方 `dwd_*` 活跃表） |
| [gkx_schema_ddl.sql](gkx_schema_ddl.sql) | 完整 CREATE TABLE 沙箱（结构真源落盘） |
| [CONNECTION.md](CONNECTION.md) | 连接元数据（密码仅本地 `.env.local`，勿提交） |
| `.env.local` | 本地密码（gitignore） |

## 分层（一眼分清）

```text
供应方：  ods_*（不正式暴露）──清洗──► dwd_*（对项目开放 = 本目录工作面）
本项目：  读取入站 dwd_* ──数据工厂──► 自建 DWD / ADS
                                      ↑
                               文档在 加工/ 与 GDF/Mapping/
```

**命名风险**：供应方 `dwd_*` ≠ 项目自建 `dwd.*`。

## 统计（结构沙箱）

- DDL 去重表数：约 **421**（见 `加工/table_inventory.md`）
- 入站工作面：见 `SOURCE-TABLES.md`（约 **206** 张活跃 `dwd_*`）

## 加工文档

→ **[`加工/README.md`](加工/README.md)**（约束、差异分析、全量清单、提取脚本）

## 铁律

| 允许 | 禁止 |
|------|------|
| 只读连库；盘点 / 对照入站 `dwd_*` 表结构 | 在本目录根下写 Mapping/ETL 加工结论 |
| 缺表登记待供应方核验 | 以 `ods_*` 作正式输入；对本库写操作 |
