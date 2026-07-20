# ALGO-PROGRESS-20260720 —— 算法工程师任务进度更新（数据库状态 + PG 迁移验证）

> 任务：算法工程师全局维护 ｜ 角色：algorithm-agent ｜ 日期：2026-07-20
> 仓：`demo-algo-ent-analysis` + `demo-algo-science`
> 更新内容：POL-B3 验证、science 仓库 PG 迁移验证、产业链 chainan 验证

---

## 1. 本次更新摘要

| 领域 | 状态 | 说明 |
|------|------|------|
| POL-B3 政策基础统计 | ✅ 已验证 | 299 行真实数据，39 行指标落 `ads.realdata_policy_metrics` |
| sci-P1~P9 创新监测流水线 | ✅ PG 迁移完成 | MySQL innov→PG demo_gdf_data。P5 真实图+P9 科研统计已上线 |
| chain-1~5 产业链分析 | ✅ PG 验证通过 | 与 science 共用 demo_gdf_data，完整 13 模型流水线 |

## 2. POL-B3 政策基础统计验证

| 项 | 值 |
|---|-----|
| 数据源 | `gkx_szc_ods.ods.gkx_ods_zh_policy_6` | 
| 真实行数 | 299 条 |
| 级别分布 | 地市级 40 / 国家级 46 / 市级 100 / 省级 113 |
| ADS 指标 | `ads.realdata_policy_metrics` 39 行 |
| 运行方式 | SQLite 零依赖（`python run_all_policy.py`）或 PG（`POLAN_DB_BACKEND=pg`）|
| 全流水线 | 15 步全部通过（0.4s SQLite）|

未完成：剩余 14 指标（Q010~Q018 口径待甲方确认）

## 3. Science 仓库 PG 迁移

| 项 | 值 |
|---|-----|
| 原 MySQL | `192.168.88.43:3306/innov` — 无外网映射 |
| 新 PG | `111.198.38.90:20644/demo_gdf_data` — 外网可连 |
| 新增文件 | 39 个（含迁移脚本 + PG schema）|
| 迁移脚本 | `scripts/migrate_innov_mysql_to_pg.py` |
| PG mock 表 | 70 张 ods 表（poc_tb_cn_*，1000+行/张）|
| 流水线 | 11 步 P1~P9 + 17 步 chainan，全部 demo 完成 |

运行方式：
```bash
export INNOV_PG_HOST=111.198.38.90
export INNOV_PG_PORT=20644
export INNOV_PG_PASSWORD=123456
export INNOV_PG_DATABASE=demo_gdf_data
cd scripts && python -c "import run_all; run_all.main_all()"
```

## 4. 算法设计说明更新

| 仓库 | 文件 | 更新内容 |
|------|------|----------|
| demo-algo-ent-analysis | 算法设计说明.md | 新增第15章「POL-B3 当前状态与 PG pipeline」|
| demo-algo-science | 算法设计说明.md | 新增第12章「PG 迁移与流水线运行」|

## 5. 数据库状态（2026-07-20）

| 数据库 | 状态 | 可用数据 |
|--------|------|----------|
| PG gkx_szc_ods (111.198.38.90:20644) | ✅ 可连 | 企业真实数据 + 政策 299 行 |
| PG demo_gdf_data (111.198.38.90:20644) | ✅ 可连 | 70 ODS mock 表 |
| MySQL innov (192.168.88.43:3306) | ❌ 不可达 | 无外网映射 |
| NebulaGraph (192.168.88.43:9669) | ❌ 不可达 | 内网 |

## 6. 当前可推进任务

| 任务 | 优先级 | 前置条件 | 说明 |
|------|--------|----------|------|
| 企业域 A1~A4 真实数据 | P0 | 无 | 但部分 ODS 表行数为 0（如 reg_info），需确认数据是否迁移 |
| 政策 POL-B3 剩余 14 指标 | P0 | Q010~Q018 甲方确认 | 口径确认后可立即推进 |
| sci-Demo P1~P9 全流水线 | P1 | 无 | PG demo_gdf_data 已可用 |
| 产业链 chain-Demo M1~M13 | P1 | 无 | 同 science PG 环境 |
