# DEMO-CHAIN-SIM-PROCESS-L01 · 产业链 Demo 全链路模拟过程（详细设计 + 映射诚实）

> 口径：`storage/CHAIN/etl/pipeline-demo-sim-process.md`  
> 日期：2026-08-16  
> Task ID：`DEMO-CHAIN-SIM-PROCESS-L01`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控；lock 24h；不重做 `DEMO-CHAIN-UI-SEED-ODS-L01` 灌数按钮；`map_entity_rel` 交 `ENT-CHAIN-HANG-MOCK-L01` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 过程文 + 字段矩阵为主；代码只新增 `gdf_sim_gaps.py` 并在 `seed.py` 后置调用。未改 `gdf_sim.py`。未用 YAGNI 跳过 handoff / demo_* 闸门 / 映射诚实 / 禁止假算法成功。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 范围与实现

产业链维完整 Demo 模拟过程说明书（对齐 ENT：离线样例 → demo ODS 四表 → 模拟 GDF → demo DWD v5 十四表 → ADS v2 / ES / Nebula），加 ODS→DWD 映射诚实与缺口 skip。灌数入口沿用 SEED-ODS 叶。

## 偏离

- 现行「LLM Mock」= `generate.py` 确定性种子，无 ENT `--llm` 入口（OPEN-CHAIN-SIM-01）。
- `gdf_sim.MAPPED_DWD` 含 `event_metric_observation`，但 `apply_ods_to_dwd` 未 INSERT；本叶不灌假浏览量（OPEN-CHAIN-SIM-02）。
- ES / Nebula / MinIO 投影仍 fail-soft / 未落地（OPEN-CHAIN-SIM-03）。
- 未现网联调灌数（本叶不跑 `--chain` replace/append）。

## 产物清单

- 过程文：`agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-demo-sim-process.md`
- 字段矩阵：`agent-delivery/data/data-design/storage/CHAIN/etl/ods-to-dwd-mapping.md`
- 代码：`repos/demo-algo-science/chainan/llm_ods/gdf_sim_gaps.py`；`seed.py` 后置 `apply_gaps`；`self_check.py` 断言
- 指针更新：`pipeline-demo-mock.md` / `pipeline-ods-to-dwd.md` / `seeds/README.md` / `CHAIN/README.md` / `CHANGELOG.md` / `dwd-chain.md`（仍 draft）
- 本 handoff

## 上链叶合并点

`seed.run_seed` 顺序：`apply_ods_to_dwd` → **`apply_gaps`** → `recalc_ads` → `project_safe`。  
后续叶（含 `ENT-CHAIN-HANG-MOCK-L01` 改 `map_entity_rel`）应继续只在 `seed.py`（或编排）调用 gaps，**不要**改 `gdf_sim.py` hook。`apply` 后续应调用 gaps。

## 映射矩阵摘要

| 类 | DWD |
|---|---|
| 直接 | `industry_chain` / `node` / `news_event`；`entity_rel` 企业 `credit_code` |
| 合成🧪 | `node_rel`；产品 `entity_id`；投融资三表；资讯 `event_entity_rel`；城市 geo |
| n.a. | `market_observation`（走 ADS）；`milestone_event`（CMS）；`extraction_result` / `model_run` / `model_result_detail`（不装成功）；`event_metric_observation`（listed 未写） |

行业分析六表切片：`industry_analysis_*` 仅去前缀；禁止 `dwd_industry_chain_news_info` 冒充 `documents`。

## 测试结果

- `python scripts/run_all.py --self-check`（仓根 `demo-algo-science`）exit 0：
  - `chain llm_ods self_check OK tree=106 tags=104 products=169 news=90 edges=88`
  - `chain llm_ods live OK ODS_tags=152 DWD_chain=10 ADS_fact=52 market_observation=0 formal_dwd_chain=None mapped=9`
- 未改 `gdf_sim.py`（`git status` 无该文件；仅 `seed.py` / `self_check.py` / 新 `gdf_sim_gaps.py`）
- 未改 `entan/yiji_sim/**`、未改 BasicPage、未 APPLY 正式 `gkxlumenx_*`、未翻签 `01-data-flow`

## 遗留风险 / OPEN

| ID | 说明 |
|---|---|
| OPEN-CHAIN-FLOW-01 | 正式 GDF DAG 未回写 |
| OPEN-CHAIN-SIM-01 | 无 `--llm` 入口 |
| OPEN-CHAIN-SIM-02 | `event_metric_observation` listed 未写 |
| OPEN-CHAIN-SIM-03 | ES/Nebula/MinIO 未真正投影 |
| Q054 | 投融资 mock 🧪；ADS 不写 INVEST_COUNT |
| ENT-CHAIN-HANG-MOCK-L01 | `entity_id` 语义并行叶 |

## CI/CD

- 分支：未 commit / 未 push（派单禁止）
- commit：无
- pipeline URL / ID：无
- K8s rollout：未做
- 本地：`--self-check`

## 可观测性

- OTEL_SERVICE_NAME：沿用 chainan 已有中间件
- 本单未改埋点

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | 前端 → Java → `/internal/*` | ✅ 未改入口 |
| 3 | Nebula，禁 Neo4j | ✅ |
| 4 | 可观测 | ✅ 未拆 |
| 5 | CI/CD | ✅ 禁止本叶 push |
| 6 | demo 不 merge lumen | ✅ |
| 7 | 只写 demo_* | ✅ 闸门未改 |
| 8 | D9 不灌假市场规模/模型成功 | ✅ gaps 五表空 |
| 9 | 不翻签 01-data-flow | ✅ |

## 涉及文件

- `repos/demo-algo-science/chainan/llm_ods/gdf_sim_gaps.py`
- `repos/demo-algo-science/chainan/llm_ods/seed.py`
- `repos/demo-algo-science/chainan/llm_ods/self_check.py`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-demo-sim-process.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/ods-to-dwd-mapping.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-demo-mock.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-ods-to-dwd.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-dwd-to-es.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-to-nebula.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/README.md`
- `agent-delivery/data/data-design/storage/CHAIN/seeds/README.md`
- `agent-delivery/data/data-design/storage/CHAIN/README.md`
- `agent-delivery/data/data-design/storage/CHAIN/CHANGELOG.md`
- `agent-delivery/data/data-design/storage/CHAIN/stores/mysql/dwd-chain.md`
- `agent-delivery/agent-handoffs/产业链分析-CHAIN/DEMO-CHAIN-SIM-PROCESS-L01.md`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 2.4 |
| cost_warn | green |

## 联调确认

本叶为过程设计 + 离线 self-check。**未**对 `demo_gkxlumenx_*` 做 replace/append 现网灌数，**不写「联调通过」**。UI 灌数按钮未改。本 agent **不**把任务标 `done`。
