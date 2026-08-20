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

---

## 2026-08-20 补丁 · Demo 算法库 M6/M8 空结果

监管人 `human:淮政玮` 确认开工。根因：Demo `read.py` 把 `/cycle`、`/key-nodes` 写死为空；ADS v2 有企业数/资讯序列，但算法页读的是旧 `ads.chain_cycle`。

### as-built

- `chainan/llm_ods/algo_demo.py`：确定性 mock 营收 2020–2025（**不是** `M_CHAIN_MARKET_SIZE`）；投融资趋势固定 `stable`（QC07 不造金额）；环节高端化指数用 DWD `node_level=2` + `entity_rel` 企业计数，公式同旧 `key_node.py`。
- `read_v2.cycle` / `key_nodes` 只读 `demo_*`；`read.py` Demo 平面改走 `read_v2`（正式平面仍 `read_live`）。
- 不重做灌数按钮，不跑 `LEGACY_CHAIN_STEPS`，不写 Q056/QC07 指标。

### 测试

- `python -m pytest tests/test_chain_read_v2.py -q`：6 passed

### 上线

改的是 `demo-algo-science` Python。推 `origin/dev` 后等 `demo-platform-innov-py` 新镜像，算法库「周期阶段 / 关键环节」才有数。

| 字段 | 值 |
|---|---|
| ponytail | full |
| honesty | cycle/stage `honesty=mock` `gap_ref=QC03`；营收非市场规模口径 |

---

## 2026-08-20 补丁 · Demo 算法库 M9 空结果

监管人截图：瓶颈堵点「暂无瓶颈数据（请先灌数）」。现网 `read.bottlenecks('INB1701')` 返回 `None`。根因同 M6/M8：Demo `read.py` 写死空；灌数主路径不跑旧 `LEGACY_CHAIN_STEPS` / 不写 `ads.chain_bottleneck`。再灌数无效。

### as-built

- `algo_demo.build_bottlenecks`：技术/人才/市场/政策用 DWD 企业·产品·节点计数；资金维确定性 mock（**不写** QC07 投融资金额）。阈值/建议文案复用 `evaluation.bottleneck`。
- `read_v2.bottlenecks` 只读 `demo_*`；`read.py` Demo 平面改走 `read_v2`。
- 不重做灌数按钮，不跑 LEGACY M9。

### 测试

- `python -m pytest tests/test_chain_read_v2.py -q`：7 passed

### 上线

须再 push `demo-algo-science` `origin/dev`，等 `demo-platform-innov-py` 吃到新 SHA。区域指数 / 深圳专题 / 竞争力 / 热点 / 路线图 / 布局建议仍写死空。

---

## 2026-08-20 补丁 · Demo 算法库 M10 空结果

监管人截图：区域指数「暂无数据」。根因同前：Demo `read.py` 把 `region_index` / `competitiveness` 写死 `[]`；ADS 已有 `industry_chain_region_dist`（INB1701 深圳/香港/台北）。

### as-built

- `score_region_index`：企业数读 ADS/DWD 城市分布；学术维确定性 mock（无机构指标）；配套用企业数。权重同旧 `region_index.py`。
- `score_competitiveness`：产业基础=region_index；增长=mock 营收增速；创新密度=区域企业数。
- `read.py` Demo 平面改走 `read_v2`。不跑 LEGACY M10。

### 测试

- `python -m pytest tests/test_chain_read_v2.py -q`：8 passed

### 上线

须再 push。深圳专题 / 热点 / 路线图 / 布局建议仍写死空。

---

## 2026-08-20 补丁 · Demo 算法库深圳专题 / 热点 / 路线图 / 布局建议

监管人要求检查余下空页。根因同前：Demo `read.py` 写死 `shenzhen` 空包、`hotspot`/`roadmap`/`recommendation` 为 `None`。

现网 Demo：INB1701 资讯 8 条、深圳企业分布（南山/福田）、城市分布（深圳/香港/台北）。

### as-built

- 深圳专题：节点+区分布读 DWD/ADS；优势用深圳份额/城市排名；问题复用五维计数；机遇趋势用 mock 营收增速，政策维 mock。
- 热点：资讯标题来自 DWD；浏览量 mock；**融资额不造**（QC07，字段为 null）。
- 路线图：只用资讯事件，不编融资里程碑。
- 布局建议：由优势/机遇/问题数加权，等级同旧 `layout.py`。

### 测试

- `python -m pytest tests/test_chain_read_v2.py -q`：9 passed

### 上线

须再 push `demo-algo-science` `origin/dev`。

---

## 2026-08-20 补丁 · 基础指标 A1–A9 空图

监管人截图：联调台「产业链分析算法库 → 基础指标」A1「暂无产业市场数据」。根因：Demo `read_v2` 把 A1 绑死 `M_CHAIN_MARKET_SIZE`（不写 Q056 故空）、A3/A4/A5 写死 `[]`；A6 把城市名当省名，全国地图质心对不上。

### as-built

- A1：复用 M6 `mock_revenue_trend`（QC03），**不写** `M_CHAIN_MARKET_SIZE` / `market_observation`。
- A2：ADS 企业数；缺则 DWD `entity_rel` 计数。
- A3：Demo 无机构实体，确定性 mock 存量。
- A4：读 DWD `industry_chain_investment_event`（Q054 合成行）；无行仍空，不另造 QC07。
- A5：城市归「中国」，不造美日欧。
- A6：深圳→广东 等，好对全国地图；M10/深圳专题仍用城市名（`_city_dist`）。
- A7/A8：序列/深圳企业数缺则回落 DWD；A8 营收用 mock 末年。

### 测试

- `python -m pytest tests/test_chain_read_v2.py -q`：10 passed

### 上线

须 push `demo-algo-science` `origin/dev`，等 `demo-platform-innov-py` 新 SHA。A4 若现网无投资事件仍空（Q054 未灌）。
