# DEMO-CHAIN-UI-SEED-JOB-MOCK-L01 · 段 A LLM MOCK 补全（区域四力 scorecard + 周期序列）

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-UI-SEED-JOB-MOCK-L01`  
> 前序：`DEMO-CHAIN-UI-SEED-ODS-L01`  
> 触发：`CHAIN-20260814-011` `BASE_SCORE_MISSING`（ADS `industry_chain_region_scorecard` 被 TRUNCATE 后不回写）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控 A 段；lock 24h；结构未改 DDL（未升级李伟） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 scorecard 回写、多年度序列、handoff、只写 demo_*、D9 mock/GAP。最短 diff：在 `ads_v2.recalc_ads` 回写已有列 + JSON，不改 lumen 菜谱、不加列。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `mcp` |
| 说明 | `headroom_compress` hash=`0bfffe3d4663483e5ee28554`；本机 proxy `127.0.0.1:8787` 不可达，走 MCP noop 存储。 |

## 范围与实现

根因：`ads_v2.recalc_ads` 两种 mode 都 TRUNCATE 含 `industry_chain_region_scorecard` 的 ADS 表，但从不 INSERT。区域 Job `load_base_scores` 读空表 → `BASE_SCORE_MISSING`。

as-built（只改 `demo-algo-science` `chainan/llm_ods`）：

1. **SEED-09 scorecard**：`recalc_ads` 对每个 L0（`INB1303` / `INB1401`）× `GEO_MAP` 9 城写出 `industry_chain_region_scorecard`（必含 **深圳→440300**）。`dimension_json` 同时含指数四力与竞争力三维键；`gap_ref=GAP-CHAIN-REG-METRICS`；`honesty=mock`；`metric_id=M_CHAIN_REGION_INDEX`；`data_version=v2-demo-mock`；`score_total`=四力均值；分数哈希 55–90、城市间有区分。
2. **周期序列**：`build_news` 年份覆盖 **2020–2025**；`ads_v2` 对 L0 写出 `M_CHAIN_NEWS_COUNT` 序列，`object_id=industry_id`，补齐 2020–2025（无日期资讯映射当天 → 另有 2026 档，不挡 `min(year)≤2021`）。
3. **Q056/QC07**：ADS **不写** `M_CHAIN_MARKET_SIZE` / `M_CHAIN_MARKET_GROWTH` / `M_CHAIN_INVEST_*`（去掉原 `_try_market_size` 回写，避免 Q056 非空）。

未改 `lumen-algo-py` / Java / 前端；未建表、未加列、未改主键；未写正式 `gkxlumenx_*`。

## 偏离

- 未 curl 集群 `POST /internal/v1/chain/jobs/execute`（`algo-base-url` 为集群内 `http://lumen-platform-algo-py:8000`，本机不可达）。改用直连 demo ADS 的 `_row_dim_scores` 等价断言：`INB1303×440300` 四力均可解析。
- 无日期资讯经 GDF 落成当天（2026），序列多一档 2026；2020–2025 仍齐。

## 产物清单

- 代码：`demo-algo-science` `94f14ae`
- 编排：`storage/CHAIN/seeds/README.md` 增 SEED-09
- 本 handoff

## 测试结果

`PYTHONPATH=. python tests/test_chain_llm_ods.py` → `ok`（离线形状 + Demo MySQL **replace 实跑**）

| 项 | replace 后 |
|---|---|
| demo ODS `dwd_industry_chain_info` / tags / products / news | 106 / **104** / 169 / **90** |
| demo DWD `industry_chain` / node / node_rel / entity_rel | 10 / 96 / 88 / 273 |
| demo DWD news_event | 90 |
| demo ADS `industry_chain_metric_fact` | **50** |
| demo ADS `industry_chain_metric_series` | **14**（L0×2020–2026） |
| demo ADS `industry_chain_region_scorecard` | **18**（2 L0 × 9 城） |
| demo ADS `industry_chain_region_dist` | 65 |
| `INB1303`×`440300` | 1 行；`score_total=75.1`；四力 66.7 / 76.8 / 81.7 / 75.1（均可被 `_row_dim_scores` 解析） |
| `INB1303` 有分区域数 | **9**（≥2，可排名） |
| Q056 / QC07 ADS 非空 | **0** |
| 正式 `gkxlumenx_ods.dwd_org_industry_tags` | **20000 未变** |
| 正式 `gkxlumenx_dwd.chain` | **8 未变** |
| ES / Nebula | `skipped`（enabled=false） |

`load_base_scores`：SQL 侧四力非空，不再满足「全空 → BASE_SCORE_MISSING」。未实跑 Job 进程。

## 回归矩阵

| 用例 | 结果 |
|---|---|
| 区域指数 `INB1303`×`440300` | scorecard 四力非空 |
| 区域竞争力 同上 | 同一 JSON 三维非空 |
| 周期窗 2021–2025 | 非 Q056 序列覆盖 2020–2025，`min(year)≤2021` |
| 门户企业数等 | fact 仍写；Q056/QC07 仍 null |
| 关键环节 / 深圳负例 | 未改菜谱 |

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| **OPEN：METRIC 重跑会清空 scorecard** | 禁止跑 `lumen-algo-py` `metric_engine --self-check`（会 DELETE 指标 6 表并把 scorecard 清回 0）。若必须重跑 METRIC，等 coordinator 派投影补单。 |
| 未 curl execute | 集群 Job 是否 succeeded 待段 E / 专题前端再点一次「生成区域产业指数」 |
| 无日期资讯 → 2026 | 多一档序列，不挡 cycle |
| OPEN-CHAIN-FLOW-01 | 正式 GDF DAG/cron 仍开；本单手工/API 灌数 |

## CI/CD

- 分支：`demo-algo-science` `dev` → `origin/dev`；`gkx-orchestration` `dev` → `origin/dev`
- commit：`demo-algo-science` `94f14ae`
- pipeline URL / ID：push 后由 CI 接管
- K8s rollout：demo-algo-science 随 CI；灌数已在 Demo MySQL 实跑，不依赖新镜像才能有 scorecard
- 本地：`python tests/test_chain_llm_ods.py`；`python scripts/run_all.py --self-check`

## 可观测性

- 本单未改 OTel 埋点
- 原缺陷 Python execute trace `0ba2055ff9b67d8183d173914b7e6839` 根因已在 ADS 回写侧闭合

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ MOCK 底分在 `chainan/llm_ods/ads_v2.py` |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ 未改调用链；未改 Job 菜谱 |
| 3 | 图谱 Nebula | ✅ 投影仍 fail-soft skipped |
| 4 | 可观测 | ✅ 未拆已有中间件 |
| 5 | CI/CD | ✅ push `origin/dev`；禁止 force / main |
| 6 | demo 不 merge lumen | ✅ 只改 demo-algo-science |
| 7 | Java 不写算法 | ✅ 本单无 Java |
| 8 | 只写 demo_* | ✅ `assert_demo_mysql_targets`；正式库行数未变 |
| 9 | D8 Design | N/A |
| 10 | D9 血缘 | ✅ `gap_ref` / `honesty=mock` / `data_version` 含 mock；Q056/QC07 不造假 |
| 11 | D12 lumen 不调 demo | ✅ 未改 lumen-* |
| 12 | 不建表不加列 | ✅ 只写已有 `score_total` + `dimension_json` |

## 涉及文件

- `repos/demo-algo-science/chainan/llm_ods/ads_v2.py`
- `repos/demo-algo-science/chainan/llm_ods/generate.py`
- `repos/demo-algo-science/chainan/llm_ods/self_check.py`
- `repos/demo-algo-science/tests/test_chain_llm_ods.py`
- `agent-delivery/data/data-design/storage/CHAIN/seeds/README.md`
- 本 handoff

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 4.2 |
| cost_warn | green |

## 联调确认

脚本侧 **replace 实跑联调通过**：`demo_gkxlumenx_ads.industry_chain_region_scorecard=18`，`INB1303+440300` 四力可解析；L0 `M_CHAIN_NEWS_COUNT` 覆盖 2020–2025；Q056/QC07 仍 NULL；正式库 `gkxlumenx_ods.dwd_org_industry_tags=20000`、`gkxlumenx_dwd.chain=8` 未变。本 agent **不**把任务标 `done`。
