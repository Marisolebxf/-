# DEMO-COMP-GRAPH-TRIPLE-UI-L01 · 综合图谱 API 三元组（116）

> 叶内四步：步1 data-agent → 步2 algorithm-agent → 步3 api-agent → 步4 frontend-agent。本文按步追加，不覆盖他人段落。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent`（本步 1/4） |
| supervised_by | `human:徐滕强`（全程不准改） |
| claim_type | `coordinator_dispatch` |
| 说明 | 厚包 `COORD-GRAPH-TRIPLE-UI-DISPATCH-20260831.md` §0.2/§7.0；前序企业叶四步已完（`pending_test`）。本叶无 A/B/C |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 文档完整性优先；未用 YAGNI 裁掉 116 五查询行 / 过程图。本步不改 UI。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | SRS 与厚包读原文，禁止 compress 代替精读。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `COMP-GRAPH-TRIPLE` |
| 图 diff | 综合只读：灌数零图谱 → D 浏览 + 五查询；写入不在本叶；space=`demo_gkx_chain`；禁止第二张图 |
| 会签态 | 不新建流图；不翻签 ENT `01-data-flow.md` |

---

## 数据设计（步1 · agent:data-agent · 2026-09-02）

**步1 只写编排仓。** Python 目标 = `demo-algo-ent-analysis`（进程 `demo-platform-entan-py`）；Java = `demo-svc-platform`。正式 lumen 链不在本叶。

### 范围与实现（对照 SRS 116）

| 项 | 产业全要素图谱 API |
|---|---|
| seq | **116** |
| metric_id | `M_COMP_GRAPH_116_1`（占位，不伪 8 件套） |
| 落点 | D `COMP_GRAPH_BROWSE` + 检索 / 关系 / 可视化 / 语义相似 / 网络指标 |
| 本波诚实 | 不写图；名称不猜 VID；语义相似默认 rule；词云=频次 |

真源：`agent-delivery/data/data-design/storage/COMP/etl/pipeline-to-nebula.md`。

### 关系 × op_id × I/O 摘要

| op_id | 档 | HTTP | 本波 |
|---|---|---|---|
| `COMP_GRAPH_BROWSE` | D | `GET /v1/comp/graph` → `/internal/comp/graph` | 只读；`hops`/`limit` |
| `COMP_ENTITY_SEARCH` | 查询 | `GET /v1/comp/graph/entities` | 分页；已有点 |
| `COMP_REL_QUERY` | 查询 | `GET /v1/comp/graph/relations` | 已有边；未知 rel=`not_in_wave` |
| `COMP_GRAPH_VIZ` | 查询 | `GET /v1/comp/graph/viz` | graph / wordcloud |
| `COMP_SEMANTIC_SIM` | 查询 | `POST /v1/comp/graph/similar` | rule 字面；llm 可选 |
| `COMP_NETWORK_METRIC` | 查询 | `GET /v1/comp/graph/metrics` | 密度 / 中心度，空图为 0 |
| A/B/C 写入 | — | — | **不实现** `not_in_wave` |

Java（步3）：网关在 `/industry-comp/**` 前插 graph → `gkx-innov` → Feign **entan-py** `/internal/comp/graph*`。禁止 innov-py。禁止 catch-all 直连写图。

### 灌数剥离清单

| 位置 | 动作 |
|---|---|
| `industry-comp/pages/BasicPage.vue` | 灌数据已 disabled；保持零图谱 |
| 综合 `run_all_*` | 现网无独立贴源；禁止新建来建图 |
| `compModelCatalog.ts` Mock 图 | 步4：`USE_MOCK=false` 禁止 fixture 填 116 |
| 企业 `run_all.py` | **不改**（企业叶已收口） |

### 偏离说明

| 项 | 说明 |
|---|---|
| 无 `storage/COMP` 细表 / 流图 | 按厚包只建 draft 管道 + README，不翻签 |
| metric 8 件套 | `M_COMP_GRAPH_116_1` 占位；MCP 未挂，不编造口径 |
| Feign 进程 | 与企业同 `demo-platform-entan-py`，换 Path `/comp/graph*`，不另起 Pod |
| 现网无 graph 菜单 / 无网关插队 | 步3/4 补；步1 只写清 |

### 产物清单

| 路径 | 说明 |
|---|---|
| `storage/COMP/README.md` | 域入口 draft |
| `storage/COMP/etl/pipeline-to-nebula.md` | 116 契约 + mermaid |
| `storage/README.md` | COMP 指针 |
| 本文 | 步1 handoff |

### 验收证据

- 步1 范围 = 编排仓文档；未改 Python/Java/Vue
- `diagram_id=COMP-GRAPH-TRIPLE`
- 116 五查询 + D 全表，无静默删行

### 架构合规自检

| 铁律 | 本步 |
|---|---|
| 算法只在 Python | ✅ 本步无代码；契约写查询在 Python |
| 前端→Java→`/internal` | ✅ 步3 才接线；文档已写 Path |
| 图谱 Nebula / 一张 G | ✅ `demo_gkx_chain`；禁第二张图 |
| 可观测 | ✅ 步4 补 |
| CI/CD | ✅ 文档 push `origin/dev` |
| demo 不 merge lumen | ✅ |
| 共享聚合 / Java 不写算法 | ✅ Java 只透传 |
| 数据 ADS / Mock | ✅ 查询可 pg 回退；不灌数建图 |
| D8/D9/D10 | ✅ 步4 |
| D9 metric 占位 | ✅ 不伪 8 件套 |
| D12 | ✅ 不改 lumen Java |
| 只做自己工单 | ✅ 未开别人的叶 |

### Cost（估算 · 非 console 实测）

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | grok-4.6 |
| actual_cost | 0.22 |
| cost_warn | green |
