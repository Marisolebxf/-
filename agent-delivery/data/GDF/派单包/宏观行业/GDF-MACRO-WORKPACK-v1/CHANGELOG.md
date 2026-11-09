# CHANGELOG · GDF-MACRO-WORKPACK

## v1.0.0 · 2026-11-09

首版成包（任务 `GDF-MACRO-WORKPACK-L01`，WBS-06-05B；优先级：市场研究红标第 1 / P0）。

- 范围：供应方「宏观行业要素库」六表（`dwd_macro_index_data`、`dwd_dim_index_attribute`、`dwd_dim_admin_area`、`dwd_dim_index_cal`、`dwd_dim_index_dur`、`dwd_dim_source_code`）。不并入政策包，不与金融、行业分析合并。
- Wave A：六表贴源 `gkxlumenx_ods` 同名镜像（`02` / `05`）。
- Wave B：六张 `gkxlumenx_dwd.macro_*`（`09` / `10`）。事实表加区划反解派生列 `area_resolve` / `city_code` / `city_name` / `province_code`；UK 含 `area_code_type`。
- 区划反解与 `area_code_type=1` 写入 `04` §3 与 `09` §3.1.1。
- ②a：`gkxlumenx_ads.macro_city_section`（`12` §1–§4）。只收 `area_code_type=1` 且反解到城市的行。
- ②b：`12` §5 **仅附录**。不建作业、不建表；不得 silent 写入 `M_POLICY_IMPLEMENTATION_EFFECT` 正本三维。
- 证据：2026-11-09 在三方 `gkx` 只读实跑 `sql/check_area_resolve.sql`；用同口径 SQL 试算 ②a 得 2,201 序列 / 103 城 / 128 指标（`12` §1）。六表行数 20,000 / 867 / 20,000 / 3 / 7 / 4 与 2026-11-09 行数报告一致。
- **未做**：未在 GDF 上跑；未建表；未核产线库 `gkxlumenx_ods` / `_dwd` / `_ads` 现网结构（OPEN-MACRO-06）；`10` 与 `12` §2 的 DDL 未执行；`data-design/storage/` 无 MACRO 目录（OPEN-MACRO-05）；未登记 metric-registry（`12` §4 占位）。
- 登记 OPEN-MACRO-01…07（`00` §6）。
