# CHANGELOG — GDF-ENT-WORKPACK

## v2.0 — 2026-08-13

- **纠偏 DWD 建表真源**：新建本目录（v2），取代 v1 用于 Wave B 建表/ALTER。
- 新增 `10-DWD-MySQL-DDL/`：嵌入工商 MySQL-v3.1、风险/模块 MySQL-v3.0、指标汇总 MySQL-v3.1 **冻结快照** + 建表总览。
- 新增 `11-作废与误源对照.md`：明确禁止 PG `demo_gdf_data`、宽表 `enterprise`、`_公共/三方参考-DWD标准表结构清单.md`、v1 错误指针。
- Mapping 升为 **`09` v4**：页眉指向 `10/`；附录相对 v3 的 DDL 差集（`org_id`、禁造 org_id、financing 契约等）。
- Wave A 贴源清单（40 表）**沿用 v1.3**，不重开范围。
- 目标库仍为正式 **`gkxlumenx_dwd`（MySQL）**；不含 `demo_gkxlumenx_*`。

## 历史（v1 系列 · 建表已作废）

详见 [`../GDF-ENT-WORKPACK-v1/CHANGELOG.md`](../GDF-ENT-WORKPACK-v1/CHANGELOG.md)。v1.3 及以前的 Mapping/贴源叙述可作背景阅读，**不得再按 v1 内 DWD 设计路径建表**。
