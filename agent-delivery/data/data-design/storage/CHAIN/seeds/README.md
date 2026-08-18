# CHAIN · seeds 覆盖样例索引

```yaml
---
doc_id: CHAIN-SEEDS-INDEX
element: CHAIN
role: source
status: as-built
version: "2026-08-16"
updated: 2026-08-16
---
```

> 少量样例，先闭环后性能。非第二套 DDL。确定性种子在 `demo-algo-science/chainan/llm_ods/generate.py`。  
> **过程说明书**（不重做灌数按钮）：[`../etl/pipeline-demo-sim-process.md`](../etl/pipeline-demo-sim-process.md)。

## 覆盖矩阵

| 场景 ID | 场景 | 数据特点 | 主要触达表 | 状态 |
|---|---|---|---|---|
| SEED-01 | ≥2 条链多层树 | 3.0 L0「新一代信息技术 INB1701」+「高端装备 INB1705」多层；半导体/智能机器人为 L1 | `dwd_industry_chain_info` | 脚本入口 |
| SEED-02 | 节点挂企业 | 同一节点多 `credit_code`；深圳/外地 | `dwd_org_industry_tags` | 脚本入口 |
| SEED-03 | 企业×产品 | 一企多产品；`product_top5` 空/非空 | `dwd_org_industry_product_tags` | 脚本入口 |
| SEED-04 | 链上资讯 | 有/无 `publish_date`；长摘要 | `dwd_industry_chain_news_info` | 脚本入口 |
| SEED-05 | 跨表关联 | 同一 `industry_code` 贯穿四表 | 四表 | 脚本入口 |
| SEED-06 | 空节点 | `INB13030212` 结构在、企业为 0 | tree + tags | 脚本入口 |
| SEED-07 | 上下游边 | 同 L1 内相邻 L2 | `industry_chain_node_rel` | 脚本入口 |
| SEED-08 | 企业域对齐 | 若干 `credit_code` 与 ENT 样例可对上（云启/格物/星辰/磐石/深极智机） | ODS tags；DWD hang 用 `org_id` | **as-built** · `generate.ENT_ALIGN` + `run_ent_chain_hang.py` |
| SEED-09 | 区域 MOCK 底分 + 周期序列 | L0×城市 `industry_chain_region_scorecard`（四力+三维 JSON，`gap_ref=GAP-CHAIN-REG-METRICS`，`honesty=mock`）；资讯/ADS `M_CHAIN_NEWS_COUNT` 序列覆盖 **2020–2025**；不写 Q056/QC07 | ADS `region_scorecard` + `metric_series`；ODS 资讯 | 脚本入口（`ads_v2.recalc_ads` 全量回写） |
| SEED-10 | 企业上链 | Demo 企业挂 INB 节点；`entity_id=org_id`；对不齐 drop | `enterprise_industry_chain` + `industry_chain_entity_rel` | **as-built** · `demo-algo-ent-analysis/scripts/run_ent_chain_hang.py` |
| SEED-11 | 深圳 20+8 **3.0** 产业树 | L0=10 战新领域+5 未来领域；L1=3.0 点名 20+8 集群；L2=公开口径子链。追加长出延伸链（工业互联网/虚拟电厂/无创脑机等）+ 额外子链 | 四表 + DWD chain/node | **as-built** · `generate._sz30_spec` |
| SEED-12 | 对外 15 集群目录 | 与 storage §3/§4 同编码；12 条 L0 映射；7 个空集群 | `industry_cluster` + `_map`（dim，非 DWD） | **draft** · `industry-cluster-sz-10+5-2026.yaml` + `data/ddl/gkxlumenx_dim_industry_cluster.sql` |

## 灌数入口

| 项 | 说明 |
|---|---|
| ODS 建表 | `chainan.llm_ods.load.ensure_ods_tables`（CREATE IF NOT EXISTS；解析复用 `entan.llm_ods.schema`） |
| 样例 INSERT | `python scripts/run_all.py --chain --mode append`（仓根 `demo-algo-science`） |
| UI | `demo-ui-system-test` 产业链「灌数据」split-button |
| 自检 | `python scripts/run_all.py --self-check`（CHAIN）；上链 `demo-algo-ent-analysis`：`python scripts/run_ent_chain_hang.py --self-check` |
| 禁止 | 写正式 `gkxlumenx_*`；`init_schema` |

## 开放

| ID | 说明 |
|---|---|
| OPEN-CHAIN-SEED-01 | 样例行业/企业是否用甲方脱敏清单 — 待确认后定具体值 |
| OPEN-CHAIN-FLOW-01 | 正式 GDF DAG/cron 仍开；本单手工/API 灌数 |
| OPEN-CHAIN-SEED-09 | `lumen-algo-py` `metric_engine --self-check` 会清空 `industry_chain_region_scorecard`；须重跑 METRIC 时另派投影补单，勿在本入口自跑 |
| OPEN-ENT-HANG-01 | Demo DWD 无 INB `industry_chain_node` 时上链 `--apply` 不写、不造树 |
| OPEN-CHAIN-SIM-02 | `event_metric_observation` 未实际 INSERT；互动量无 ODS，不灌假浏览量 |
| n.a. 五表 | `market_observation` / `milestone_event` / `extraction_result` / `model_run` / `model_result_detail` 保持空；`gdf_sim_gaps` replace 时 truncate |
