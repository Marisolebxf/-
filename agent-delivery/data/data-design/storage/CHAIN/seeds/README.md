# CHAIN · seeds 覆盖样例索引

```yaml
---
doc_id: CHAIN-SEEDS-INDEX
element: CHAIN
role: source
status: as-built
version: "2026-08-14"
updated: 2026-08-14
---
```

> 少量样例，先闭环后性能。非第二套 DDL。确定性种子在 `demo-algo-science/chainan/llm_ods/generate.py`。

## 覆盖矩阵

| 场景 ID | 场景 | 数据特点 | 主要触达表 | 状态 |
|---|---|---|---|---|
| SEED-01 | ≥2 条链多层树 | 集成电路 INB1303 + 智能机器人 INB1401；`parent_code` | `dwd_industry_chain_info` | 脚本入口 |
| SEED-02 | 节点挂企业 | 同一节点多 `credit_code`；深圳/外地 | `dwd_org_industry_tags` | 脚本入口 |
| SEED-03 | 企业×产品 | 一企多产品；`product_top5` 空/非空 | `dwd_org_industry_product_tags` | 脚本入口 |
| SEED-04 | 链上资讯 | 有/无 `publish_date`；长摘要 | `dwd_industry_chain_news_info` | 脚本入口 |
| SEED-05 | 跨表关联 | 同一 `industry_code` 贯穿四表 | 四表 | 脚本入口 |
| SEED-06 | 空节点 | `INB13030212` 结构在、企业为 0 | tree + tags | 脚本入口 |
| SEED-07 | 上下游边 | 同 L1 内相邻 L2 | `industry_chain_node_rel` | 脚本入口 |
| SEED-08 | 企业域对齐 | 若干 `credit_code` 与 ENT 样例可对上 | tags | 脚本入口 |
| SEED-09 | 区域 MOCK 底分 + 周期序列 | L0×城市 `industry_chain_region_scorecard`（四力+三维 JSON，`gap_ref=GAP-CHAIN-REG-METRICS`，`honesty=mock`）；资讯/ADS `M_CHAIN_NEWS_COUNT` 序列覆盖 **2020–2025**；不写 Q056/QC07 | ADS `region_scorecard` + `metric_series`；ODS 资讯 | 脚本入口（`ads_v2.recalc_ads` 全量回写） |

## 灌数入口

| 项 | 说明 |
|---|---|
| ODS 建表 | `chainan.llm_ods.load.ensure_ods_tables`（CREATE IF NOT EXISTS；解析复用 `entan.llm_ods.schema`） |
| 样例 INSERT | `python scripts/run_all.py --chain --mode append`（仓根 `demo-algo-science`） |
| UI | `demo-ui-system-test` 产业链「灌数据」split-button |
| 自检 | `python scripts/run_all.py --self-check` |
| 禁止 | 写正式 `gkxlumenx_*`；`init_schema` |

## 开放

| ID | 说明 |
|---|---|
| OPEN-CHAIN-SEED-01 | 样例行业/企业是否用甲方脱敏清单 — 待确认后定具体值 |
| OPEN-CHAIN-FLOW-01 | 正式 GDF DAG/cron 仍开；本单手工/API 灌数 |
| OPEN-CHAIN-SEED-09 | `lumen-algo-py` `metric_engine --self-check` 会清空 `industry_chain_region_scorecard`；须重跑 METRIC 时另派投影补单，勿在本入口自跑 |
