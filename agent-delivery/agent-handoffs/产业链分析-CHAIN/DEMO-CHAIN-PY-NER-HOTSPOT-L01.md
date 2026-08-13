# DEMO-CHAIN-PY-NER-HOTSPOT-L01 · 产业链 Python — NER/RE 抽取 + 资讯热点（非查询引擎）

> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-PY-NER-HOTSPOT-L01`  
> 仓：`lumen-algo-py` · 分支 `dev`  
> 厚包：[`DEMO-CHAIN-PY-B-总派单.md`](./DEMO-CHAIN-PY-B-总派单.md) §6 NER、§8 明确不做「为查询上 ES」  
> 字段真源：[`产业链-DWD表设计-业务需求驱动(v5).md`](../../data/data-design/产业链/产业链-DWD表设计-业务需求驱动(v5).md) §5.8 / §5.12 / §5.13 · [`dwd-chain.md`](../../data/data-design/storage/CHAIN/stores/mysql/dwd-chain.md)  
> 依赖：[`DEMO-CHAIN-PY-SHARED-L01`](./DEMO-CHAIN-PY-SHARED-L01.md)（已落地 Demo 闸门）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| lock | 24h（coordinator 开工写入） |
| 说明 | 已 claimed + in_progress 后本会话落地；feature 完工进 `integration`，不标 done |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过「抽取落 DWD」「热点不得当查询引擎」「Demo 库闸门」、handoff、pytest。未改 Java、七键 Graph、REPORT、SEARCH/SYNC 成功语义。无新 pip 包；规则/词典抽取。热点失败诚实空列表。未上 ES、未挂厨房（避免进七键白名单）。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 派单要求 DWD v5 抽取/资讯表章节禁止 compress 代替精读；本单对 v5 §3.3 公共治理字段、§5.8 `news_event`、§5.12 `extraction_result`、§5.13 `model_run`、PY-B §6/§8、长任务总控、dwd-chain.md 均精读，未 compress。 |

## 范围与实现

NLP 只在 Python。入口均在已有 `/internal/v1/chain/`，**禁止第二套 chain 包**。

| 入口 | 行为 |
|---|---|
| `POST /internal/v1/chain/ner/extract` | 同步小批量：规则词典抽 entity/relation，组 **v5 全字段形状**；`insert_filtered` 只写入 Demo 表已有列；可写 `industry_chain_model_run`（`run_type=extraction`） |
| `GET /internal/v1/chain/hotspot` | 只读聚合 `industry_chain_news_event`（标题/时间）；热度仅当 `industry_chain_event_metric_observation` 有浏览/热度类观测才填，**不造假热度**。失败 → `items=[]` HTTP 200 |

抽取输入：请求 `documents[]`，或 Demo DWD 资讯 `title`+`summary`（v5 资讯主表无正文列，不复制全文）。  
词典：内置少量产业词 + 可选 DWD `chain_name`/`node_name`；谓词 `上游/下游/投资/并购/供应/合作`。  
指纹：v5 §5.12 长度前缀 SHA-256。`document_version` = 文本 SHA-256。

### 禁止（已测）

- 热点接入 SEARCH `mode` / 替换产业目录查询 / 当 `/search` 后端
- 新建 `gkx_chain_news`、import ES、改 SEARCH
- 七键 / 全景 / REPORT Graph 白名单
- 非 `demo_` 库写入；建新 DWD 表 / ALTER / 改主键
- 把 v5 明细列塞进 `ext` 代替正式建模

## 偏离

| 项 | 说明 |
|---|---|
| Demo 抽取表瘦于 v5 | 段 A `ddl.py` 的 `industry_chain_extraction_result` **仅核心列**（`extraction_id/run_id/result_type/document_*/confidence/result_fingerprint` + 治理字段），缺 `mention_text` / `char_*` / `entity_type` / 关系与属性列。本单 **不 ALTER**。落库走列交集；响应仍带 v5 全形状。见 OPEN |
| 实写 Demo MySQL | **本机 pytest 走 sqlite mock**。`conf/settings.yaml` MySQL host=`localhost`、密码空，本会话 **未实写** `demo_gkxlumenx_dwd`。真库不可达不假成功（`persisted=false`） |
| 无深度学习模型 | 无网/无现成模型；规则词典最小抽取，置信度 entity=0.7 / relation=0.5 |
| 未挂厨房 | HTTP 同步即可；不注册 `chain:ner:*`，避免误进七键白名单 |
| 热点热度 | v5 规定热点得分不进 `news_event`。观测表空则 `heat=null`，按 `publish_time` 排序 |

## 产物清单

- 代码：`lumen-algo-py`（push `origin/dev`，sha 见 CI/CD）
- 本 handoff
- 未改 Java / 前端 / SEARCH / SYNC / 七键 / REPORT / GRAPH

## 验收证据

测试命令：

```text
python -m compileall -q lumen_algo_service lumen_common
python -m pytest -q -p no:cacheprovider
```

输出摘要：

- 全量：**252 passed**, 1 skipped, 1 warning（Starlette TestClient deprecation，与本单无关；REPORT 后 243 绿，本单 +9）
- sqlite v5 全列：entity 含 `mention_text`/`entity_type`，relation 含 `predicate_code`，`model_run.run_type=extraction`
- Demo 瘦 DDL：核心列可落库；`schema_gap` 升级 `human:李伟`；响应仍有明细
- 非 `demo_` 库名写入拒绝；HTTP extract 指向 `gkxlumenx_dwd` → 422
- 真库不可达 → `persisted=false`，不假成功
- 热点不调用 `search_chain` / 不 import ES；SEARCH `mode` 仍仅 smart/industry/advanced
- 热点失败 → `items=[]` HTTP 200；未挂七键 Graph

## 遗留风险 / 开放项

| 项 | Owner | 说明 |
|---|---|---|
| **OPEN** Demo `industry_chain_extraction_result` 缺 v5 明细列；防重键 Demo 仅 `UK(extraction_id)`，无 v5 `UK(run_id, result_fingerprint)` | `human:李伟` | 结构歧义。本单不改主键、不建表。整仓 **不 blocked** |
| 现网 Demo MySQL 实写 | 联调 | host/密码配齐后 `POST /ner/extract` 才写入 `demo_gkxlumenx_dwd` |
| Java Feign 热点/抽取门面 | 段 C | 本单只提供 `/internal/v1/chain/ner/extract` 与 `/hotspot` |
| 前端热点页 | 段 D | 已弱壳；本单不做 |

## 架构合规自检（十条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 规则 NER 仅 lumen-algo-py；无新 pip NLP 包 |
| 2 | 前端 → Java → Python `/internal/*` | ✅ `/internal/v1/chain/ner/extract`、`/hotspot`；无前端直连 |
| 3 | 图谱 NebulaGraph；禁止 Neo4j | ✅ 未引入 Neo4j；本单不投影图 |
| 4 | 可观测 | ✅ 复用 OTel `trace_id` |
| 5 | CI/CD push → Pipeline | ✅ `origin/dev`（见下） |
| 6 | demo 不 merge lumen | ✅ 未改 demo-algo-science；未改 Demo DDL |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ 无 Java 改动；无 nGQL |
| 8 | ADS 契约；不建 DWD/ADS 业务表 | ✅ 闸门 `demo_*`；`insert_filtered` 交集列；禁止 DDL |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 8 件套 | ✅ 未写 `target_metric_id`（无属性抽取，避免未登记指标入库）；资讯热点不伪造互动量 |

## CI/CD

- 分支：`lumen-algo-py` `dev`（禁止 main、禁止 force）
- commit：见 push 后 sha（`feat(chain): add rule NER extract and news hotspot APIs [agent:algorithm-agent]`）
- pipeline：push `origin/dev` 触发 `py:test`
- 部署：ns=`dev`；镜像 `lumen-platform-algo-py`
- 本机 pytest：252 passed

## 可观测性

- `OTEL_SERVICE_NAME`：沿用 `lumen-platform-algo-py`
- 响应带 `trace_id`

## 涉及文件

- `repos/lumen-algo-py/lumen_common/algorithms/chain/ner_hotspot.py`（新）
- `repos/lumen-algo-py/lumen_common/algorithms/chain/__init__.py`
- `repos/lumen-algo-py/lumen_algo_service/views/chain.py`
- `repos/lumen-algo-py/tests/test_chain_ner_hotspot.py`（新）

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 165000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.99 |
| cost_warn | green |

口径：algorithm 默认 in/out=75/25，按 budget-estimate Sonnet 4.5 价表折算（Grok 无独立价行）。`source: session_estimate`。单任务 <$5。

公式：`165000 × (0.75×3 + 0.25×15) / 1e6 = 0.99`。

## 联调确认

**联调通过 / 联调确认**：pytest 252 绿；抽取结果能落到 extraction_result 形状（sqlite v5 全列 + Demo 瘦表交集）；热点不走 SEARCH、不上 ES；非 demo_ 写入拒绝；真库不可达不假成功；热点失败空列表。本 agent **不**把任务标 `done`（feature → `integration`）。
