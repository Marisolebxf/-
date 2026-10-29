# SYSINT-SCHEME-07-L06 · 算法中台入图流程（产业链 / 企业 / 政策）

> **任务**：`SYSINT-SCHEME-07-L06`
> **日期**：2026-10-30
> **和 L03 的分工**：L03 是七要素「有没有写图代码」的台账。本文件只写产业链、企业、政策三条**现行入图怎么走**。L03 写于 2026-10-27，其中「政策无 Nebula 写图」已被现行 A/B/C 接口取代，以本文件为准。

## 1. 共同约定

三条都写同一张 Demo 图：Nebula space **`demo_gkx_chain`**（graphd `10.50.75.136:9669`）。正式空间 `gkx_chain`、`entan` 不在这三条的写入目标里。线上目前只有 `demo_gkx_chain`，已有标签 `chain`、`segment`、`enterprise`、`institution`、`policy`。

调用链固定为：

```text
前端 → 网关 → Java REST（透传，不写 nGQL）→ Python 图谱接口
```

Java 不改边名、不做抽取。三条都不进 `gkxlumenx_cfg.analysis_task`。那张表是企业评估 / 风险洞察 / 引育推荐的异步任务表，和这三条入图不是一条队列。

三档算子：

| 档 | 路径后缀 | 做什么 |
|---|---|---|
| A | `/graph/ner` | 只写本域的点 |
| B | `/graph/intra` | 只写本域内部的一类边 |
| C | `/graph/hang` | 只挂到图上已有的另一类点；对端没有稳定 ID 就跳过 |
| D | `GET /graph` | 只读，不写库 |

`dry_run=true` 只预览，不写 ADS、不写图。企业和政策在 body 里**没给** `dry_run` 时默认预览。产业链没给 `dry_run` 时按 `false` 处理，会真写图。

灌数流水线（`run-pipeline` / `run_all`）禁止调用这三条写图模块。入图只能从下面的图谱接口进来。

## 2. 产业链

### 2.1 入口

| 层 | 地址 |
|---|---|
| 网关 | `POST /chain/v1/chain/graph/ner`（intra / hang / `ops/{op_id}` 同前缀） |
| Java | `ChainGraphController`：`/v1/chain/graph/*`、`/internal/chain/graph/*` |
| Python | `demo-algo-science` `api/main.py`：`/v1/chain/graph/*`、`/internal/chain/graph/*` |
| 算子 | `chainan/graph/graph_ops.py` `run_graph_op()` |

Python 收到后**先返回** `{started: true}`，在 API 进程的后台线程里跑。同一进程同时只允许一条图谱操作。顶栏产业链平面是正式库（`is_live("chain")`）时直接拒绝，不启动线程。

另有 `POST /internal/graph-schema-init`：图空间不存在则建 `demo_gkx_chain`，再补产业链 Tag/Edge。不灌点边，不 DROP。

### 2.2 流程

```mermaid
flowchart TD
  A["POST /chain/v1/chain/graph/ner|intra|hang"] --> B["Java 原样透传"]
  B --> C{"产业链平面是正式库?"}
  C -->|是| Z["拒绝，不启动"]
  C -->|否| D["立即返回 started，后台线程 run_graph_op"]
  D --> E{"op_id"}
  E -->|CHAIN_NER_INDUSTRY| F["读 industry_chain、industry_chain_node"]
  E -->|CHAIN_RE_BELONGS_TO / DEPENDS_ON| G["读环节表，对端必须已在图上"]
  E -->|CHAIN_RE_SUPPLIES、技术、人才| H["跳过，本波不写"]
  E -->|企业/机构/服务/政策挂边| I["读 industry_chain_entity_rel 或 policy_industry_rel"]
  F --> J{"dry_run"}
  G --> J
  I --> J
  J -->|是| K["只返回将写入的点边"]
  J -->|否| L["补齐 demo_gkx_chain 的 Tag/Edge 后 upsert"]
```

### 2.3 点、边、来源

| 算子 | 点 / 边 | VID | 来源表 |
|---|---|---|---|
| `CHAIN_NER_INDUSTRY` | 点 `chain`、`segment` | `chain:{chain_id}`、`segment:{node_id}` | `industry_chain`、`industry_chain_node` |
| `CHAIN_RE_BELONGS_TO` | 边 `belongs_to`：segment → chain | 两端都必须已在图上，否则 `no_stable_id` | `industry_chain_node.chain_id` |
| `CHAIN_RE_DEPENDS_ON` | 边 `depends_on`：segment → segment | 同上 | 环节上下游 |
| `CHAIN_RE_INDUSTRY_ENTERPRISE` | 边 `participates` | 企业端 `ent:` | `industry_chain_entity_rel` |
| `CHAIN_RE_INDUSTRY_RESEARCH` / `_SERVICE` | 边 `participates` | 机构端 `inst:` | 同上 |
| `CHAIN_RE_INDUSTRY_POLICY` | 政策挂到链或环节 | `pol:` | `policy_industry_rel` |
| `CHAIN_RE_SUPPLIES` | 不写 | — | 本波没有供给边表 |
| `CHAIN_RE_INDUSTRY_TECH` / `_TALENT` | 不写 | — | `not_in_wave` |

`scope=one` 要 `id=chain_id`。`scope=batch` 要 `filter.chain_ids` 或 `filter.all=true`。L0 编码会带上子环节（`INB13` 覆盖 `INB1301`），不会把「一条」扫成全表，除非 `all=true`。

成功时 `source=nebula`。这条链路不先落 MySQL 镜像再补图。

## 3. 企业

### 3.1 入口

| 层 | 地址 |
|---|---|
| 网关 | `POST /entan/v1/entan/graph/ner`（intra / hang / `ops/{op_id}` 同前缀） |
| Java | `EntanGraphController`：`/v1/entan/graph/*` |
| Python | `demo-algo-ent-analysis` `api/entan_graph_routes.py` |
| 算子 | `entan/graph/ops.py` `execute()`，span 名 `ent.graph.write` |

请求在接口进程里同步做完再返回。顶栏企业平面是正式库时拒绝，提示切回 Demo。MySQL 只允许 `demo_gkxlumenx_*`。

### 3.2 流程

```mermaid
flowchart TD
  A["POST /entan/v1/entan/graph/ner"] --> B["Java 透传 /internal/entan/graph/ner"]
  B --> C{"企业平面是正式库?"}
  C -->|是| Z["拒绝"]
  C -->|否| D["ENT_NER_ORG"]
  D --> E["没给 scope 则 batch；batch 无过滤则全量；没给 dry_run 则只预览"]
  E --> F["读 demo_gkxlumenx_dwd.enterprise_base"]
  F --> G{"dry_run"}
  G -->|是| H["最多 500 家，不写库"]
  G -->|否| I["规则抽取属性；llm 最多 8 家，失败回退规则"]
  I --> J["ADS 先删后插 entity_recognition、graph_node"]
  J --> K{"探活并写入 demo_gkx_chain 标签 enterprise"}
  K -->|成功| L["source=nebula"]
  K -->|失败| M["ADS 保留，source=ads"]
```

### 3.3 点、边、来源

A 档 `ENT_NER_ORG` 只写企业点，不写边。VID = `ent:{org_id}`。没有 `org_id` 或 VID 超过 80 字符则跳过。属性来自工商字段（名称、行业、城市、法人、注册资本、营收、研发人数、授权专利、高新/上市/专精特新）。

| 档 | 算子 | 边 |
|---|---|---|
| B | `ENT_RE_COOP` / `INVEST` / `BELONG` / `SUPPLY` | `cooperate` / `invest` / `parent_sub` / `supply` |
| C | `ENT_RE_INDUSTRY` / `TECH` / `TALENT` / `POLICY` / `RESEARCH` / `SERVICE` | `industry_belong` / `produces` / `talent_coop` / 政策 / `research_coop` / `service_provide` |

B/C 一次只写一类边。对端不在 `enterprise_base` 或图上没有稳定 ID 时记 `no_stable_id`，不用名称猜 VID。

ADS 表：`entity_recognition`、`graph_node`、`graph_edge`（库 `demo_gkxlumenx_ads`）。插入按 500 行一批；图写入按 80 点一批。

### 3.4 图写入失败时

`source=ads` 表示 MySQL 已经写入，Nebula 没写成。写图前的探活若打到配置空间 `demo_entan`，会失败：这个 space 在线上不存在。失败后函数直接返回，不会再写 `demo_gkx_chain`。

2026-10-30 已在 `demo-algo-ent-analysis` 把企业入图、挂边和读图的探活改成 `demo_gkx_chain`。该改动还在本地，未发布。未发布前重跑企业 NER，仍会停在 ADS。

## 4. 政策

### 4.1 入口

| 层 | 地址 |
|---|---|
| 网关 | `POST /policy/v1/policy/graph/ner`（intra / hang / `ops/{op_id}` 同前缀） |
| Java | `PolicyGraphController`：`/v1/policy/graph/*` |
| Python | `demo-algo-ent-analysis` `api/policy_routes.py` |
| 算子 | `polan/graph/ops.py` `execute()`，span 名 `policy.graph.write` |

同步返回。图谱接口本身不读「政策平面是否正式库」开关。图空间被锁成 `demo_gkx_chain`：`POLAN_NEBULA_SPACE` 若不是这个名字，连接配置会直接拒绝。政策点挂到产业链那张图上，不另建政策空间。

### 4.2 流程

```mermaid
flowchart TD
  A["POST /policy/v1/policy/graph/ner"] --> B["Java 透传 /internal/policy/graph/ner"]
  B --> C["POLICY_NER_POLICY"]
  C --> D["没给 scope 则 batch；batch 无过滤则全量；没给 dry_run 则只预览"]
  D --> E["读 policy_base_info，is_deleted=0"]
  E --> F{"dry_run"}
  F -->|是| G["最多 500 条，不写库"]
  F -->|否| H["抽取标题、层级、地域、年份、类型，以及正文中的实体名"]
  H --> I["ADS 先删后插 policy_entity、policy_graph_node"]
  I --> J{"探活 demo_gkx_chain 并写标签 policy"}
  J -->|成功| K["source=nebula"]
  J -->|失败| L["ADS 保留，source=ads"]
```

### 4.3 点、边、来源

| 算子 | 点 / 边 | VID | 说明 |
|---|---|---|---|
| `POLICY_NER_POLICY` | 点 `policy` | `pol:{policy_id}` | 不写边。属性进 ADS `policy_entity` |
| `POLICY_RE_CITE` | 边 `cite` | 两端都是 `pol:` | 谱系里的上位政策必须能解析成已有 `policy_id` |
| `POLICY_RE_SUPPORT` | 边 `support` | 政策 → 产业或企业 | 对端必须已在图上 |
| `POLICY_RE_APPLY_TO` | 边 `apply_to` | 政策 → 机构或服务 | 同上 |
| `POLICY_RE_REGULATE` | 边 `regulate` | 政策 → 受规范对象 | 同上 |

空名称、无法对齐的实体记 `empty_field` 或 `no_stable_id`，不另造一套点。`chain` / `segment` / `enterprise` / `institution` 复用图上已有顶点。

ADS 表：`policy_entity`、`policy_graph_node`、`policy_graph_edge`。

## 5. 三条对照

| 项 | 产业链 | 企业 | 政策 |
|---|---|---|---|
| 网关前缀 | `/chain/v1/chain/graph/*` | `/entan/v1/entan/graph/*` | `/policy/v1/policy/graph/*` |
| Python 仓 | `demo-algo-science` | `demo-algo-ent-analysis` | `demo-algo-ent-analysis`（`polan`） |
| 执行方式 | 后台线程，接口先返回 | 同步 | 同步 |
| 未传 `dry_run` | 真写 | 只预览 | 只预览 |
| 正式平面 | 产业链平面为正式库则拒绝 | 企业平面为正式库则拒绝 | 图谱接口不看该开关；空间仍锁 Demo 图 |
| 图空间 | `demo_gkx_chain` | `demo_gkx_chain` | `demo_gkx_chain` |
| A 档点 | `chain`、`segment` | `enterprise` | `policy` |
| 图写失败 | 后台线程记 `graph_op_error` | `source=ads`，ADS 保留 | `source=ads`，ADS 保留 |

读图（D 档）图库不可用时回退 ADS 镜像，不把回退结果说成 Nebula 命中。
