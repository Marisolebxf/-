# 管道 · ODS → DWD（产业链）

> S2 指针 · `DATA-CHAIN-STORAGE-S2-L01` · 禁止大段 SQL  
> Demo 主路径见 [`pipeline-demo-mock.md`](./pipeline-demo-mock.md)

## 意图

将 `demo_gkxlumenx_ods`（约定四表）清洗写入 `demo_gkxlumenx_dwd`（目标对齐 v5 `industry_chain_*`）。与正式 GDF **同构**；Demo 侧调度 **模拟 GDF**。

## 脚本 / 工作包指针

| 类型 | 路径 |
|---|---|
| ODS 四表清单 | [`../sources/inventory.md`](../sources/inventory.md) |
| 流图开放项 | [`../01-data-flow.md`](../01-data-flow.md)（映射缺口登记） |
| 项目 DWD 目标 | v5 `industry_chain_*`（**非** S2 建表范围） |
| Demo 模拟 GDF | `${GKX_ROOT}/repos/demo-algo-science/chainan/llm_ods/gdf_sim.py` |
| ENT 同构参考 | [`../../ENT/etl/pipeline-ods-to-dwd.md`](../../ENT/etl/pipeline-ods-to-dwd.md) |

## 调度

| 项 | 状态 |
|---|---|
| 正式 GDF DAG | 开放（产线未回写）· OPEN-CHAIN-FLOW-01 |
| Demo 模拟 | `run_all.py --chain` / `POST /internal/run-chain-pipeline` |
| 门禁 | `assert_demo_mysql_targets`；失败不晋升 ADS |
