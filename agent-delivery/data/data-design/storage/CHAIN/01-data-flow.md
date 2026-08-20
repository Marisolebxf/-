# 产业链维 · 端到端数据流

```yaml
---
doc_id: CHAIN-STORAGE-FLOW
element: CHAIN
role: data-flow
status: approved
version: "2026-08-20"
updated: 2026-08-20
engine: multi
signoff_owner: human:李伟
signoff_status: approved
signoff_by: human:李伟
signoff_at: 2026-08-13
amendment_note: "S1 会签通过：同构 ENT 三图 + Demo ODS 真源锁定（doc/md-extract）+ demo_gkxlumenx_ods；放行 S2 建表。2026-08-20 增 §8 表级数据血缘图（S4 后人读；不改 §1–3 拓扑、不翻签）。"
---
```

> **会签 Owner：`human:李伟`**（2026-08-13 **approved**）。  
> 本流图会签通过后，允许启动 **S2**（sources/etl/seeds + **按在线文档在** `demo_gkxlumenx_ods` **建表**）与后续 S3。  
> **仍禁止**：在未完成对应 `stores/*` 文档评审前，将细表标为「结构已批准 / approved」。  
> **§7**：Demo「约定 ODS → ETL 模拟 GDF」口径（结构与 §1 同构）。  
> **§8**：S4 后表级血缘图（人主看）；**不翻签**、细表仍 draft。

## 1. 批处理主链（工厂）

```mermaid
flowchart LR
  ODS["三方供应库 ODS<br/>MySQL 贴源只读"] --> GDF["GDF / 数据工厂 ETL"]
  GDF --> DWD["MySQL DWD"]
  DWD --> ADS["MySQL ADS<br/>契约面"]
  DWD --> ES["Elasticsearch"]
  DWD --> NEB["NebulaGraph"]
  PY["Python 算法 / Mock"] -->|写| ADS
  PY -->|写| ES
  PY -->|写| NEB
  PY -->|写| MINIO["MinIO 对象"]
  JAVA["Java 聚合"] -->|只读| ADS
  JAVA -->|Feign /internal| PY
```




| 生产者                 | 消费者                       | 触发                                                          | 失败语义                                                                                | 禁止事项                                         |
| ------------------- | ------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------- |
| 三方 / GDF            | MySQL DWD                 | **批**：GDF 作业；具体 cron / DAG 名 → **OPEN-CHAIN-FLOW-01**（S2 填） | 本批失败则**不晋升**依赖该批的下游；保留上一成功 DWD 快照；飞书知会供应方 / GDF / 数据 Lead；不自动回滚 ADS                 | 业务 API / Java / 前端直读 ODS；Java 写 DWD          |
| DWD ETL（GDF/Python） | ADS / ES / Nebula         | **批**：DWD 门禁通过后串联；或算法刷新任务触发派生                               | 管道失败 → 该目标存储**不发布半成品**；ADS 保留上一成功契约切片；ES/Nebula 可降级，**ADS 仍为指标权威**；作业标 failed + 可重试 | Java 写 ADS；三方字段泄漏进 ADS 契约面（D7）；Neo4j         |
| Python（含 Mock）      | ADS / ES / Nebula / MinIO | **Demo 主路径见 §7**。可选旁路：直写 ADS（D7）。生产：批或任务写计算产物               | 写失败 → 任务态 `failed`；禁止静默部分成功；Java 只读既有成功数据                                           | 前端造假；Java/前端写 ADS；以现网 as-built 当 Demo ODS 真源 |
| Java                | （读）ADS；Feign→Python       | **在线** HTTP                                                 | 4xx/5xx 统一错误体；**不写回** ODS/DWD/ADS；不因读失败扫 DWD                                        | 扫 ODS/DWD；直连 nGQL；对前端暴露 `/internal`          |


**拓扑要点**

- 工厂主链：`ODS → GDF → DWD → ADS`（D7）；派生：`DWD → ES / Nebula`。
- **Demo**：同构；调度**模拟 GDF**；ODS 按**三方在线约定**写入 `demo_`*（§7）。
- Java **只读 ADS**；图谱 = **NebulaGraph**；关系库 = **仅 MySQL**（禁止 PostgreSQL 叙述）。



## 2. 在线读路径

```mermaid
flowchart TB
  FE["前端"] --> GW["gkxlumen-gateway"]
  GW --> JAVA["Java 聚合<br/>topic / metrics / …"]
  JAVA -->|只读| ADS["MySQL ADS"]
  JAVA -->|Feign /internal| PY["Python"]
  PY --> ES["ES 检索"]
  PY --> NEB["Nebula 图谱"]
  JAVA --> ASSET["下载门面 API"]
  ASSET --> MINIO["MinIO"]
```




| 生产者    | 消费者  | 触发                  | 失败语义                                     | 禁止事项                                      |
| ------ | ---- | ------------------- | ---------------------------------------- | ----------------------------------------- |
| Java   | 前端   | 用户操作 → HTTP         | 统一错误体 + trace；不把存储异常细节泄给前端               | 前端直连 ES / MinIO / Nebula / MySQL / Python |
| Python | Java | Feign `/internal/*` | 同步失败 → Java 映射 5xx/业务码；长任务 → 任务态可查，禁止假成功 | 对前端暴露 `/internal`；Java 直连 nGQL            |
| 下载门面   | 前端   | 鉴权后下载               | 对象缺失 → 业务错误；**不**下发直连凭证                  | 前端持 MinIO 永久密钥；门面扫 DWD                    |




## 3. 对象 / 报告产物

```mermaid
flowchart LR
  TASK["分析/导出任务"] --> PY["Python / 编排"]
  PY -->|写对象字节| MINIO["MinIO"]
  META["任务/资产元数据<br/>MySQL"] --- TASK
  JAVA["Java 下载门面"] -->|鉴权读| MINIO
  FE["前端"] -->|仅经 Java| JAVA
```




| 生产者         | 消费者               | 触发                  | 失败语义                           | 禁止事项                        |
| ----------- | ----------------- | ------------------- | ------------------------------ | --------------------------- |
| Python / 编排 | MinIO + MySQL 元数据 | 分析/导出完成时写对象；元数据同步落库 | 对象写失败 → 任务 `failed`，元数据不标可下载   | 用 MinIO 替代业务表；元数据只放对象桶      |
| Java 下载门面   | 前端                | 鉴权下载                | 鉴权失败 401/403；对象不存在 404；不回源 DWD | 前端直连 MinIO；下载 API 扫 ODS/DWD |


平台约定见 [`../platform/minio.md`](../platform/minio.md)；本域对象前缀见 [`etl/README.md`](./etl/README.md)（S2 补 `pipeline-to-minio.md`）。  
现网 Endpoint / bucket / TTL → **OPEN-CHAIN-FLOW-02**。

## 4. 架构师会签清单

- [x] 主链与在线读路径与 `architecture-baseline` 一致（D3 ADS / 调用链 / D6 Nebula / D7 工厂）  
- [x] ADS 为唯一 Java 契约面已在图中明示  
- [x] MinIO 仅为对象面、元数据在 MySQL  
- [x] 无 PostgreSQL / Neo4j  
- [x] ODS 真源 = `doc/` xlsx（优先 `md-extract/`）；Demo 落 `demo_gkxlumenx_ods` 已写死  
- [x] 调度与失败语义已填（具体 cron/DAG/bucket 为开放项，不阻塞拓扑会签）

> 已由 `human:李伟` 于 2026-08-13 会签：`signoff_status=approved`。



## 5. 开放项（不阻塞本流图拓扑会签）


| ID                 | 项                                                       | Owner           | 关闭阶段                                                |
| ------------------ | ------------------------------------------------------- | --------------- | --------------------------------------------------- |
| OPEN-CHAIN-FLOW-01 | GDF ODS→DWD / DWD→ADS 具体调度（cron、DAG、门禁脚本路径）             | 数据 Lead / GDF   | S2+                                                 |
| OPEN-CHAIN-FLOW-02 | MinIO 现网 Endpoint、默认 bucket、TTL（可复用平台 OPEN-ENT-FLOW-02） | 平台 / 架构         | `platform/minio.md`                                 |
| OPEN-CHAIN-FLOW-03 | CHAIN 对象前缀与任务表字段对照                                      | data / GDF      | S2（建议 `chain/{task_id}/`）                           |
| OPEN-CHAIN-FLOW-04 | ES / Nebula 同步失败告警与重试 SLA                               | data + 算法       | S2/S3                                               |
| OPEN-CHAIN-FLOW-05 | 产业链 ODS **在线约定**入口与 `sources/inventory` 表级清单            | 数据 / 李伟         | **S1 已钉真源**；表级清单 S2 充实；权威 xlsx + **md-extract 优先读** |
| OPEN-CHAIN-FLOW-06 | `demo_*` 建表 + 灌数脚本（对齐 ENT `llm_ods` 模式）                 | 李伟 / data-agent | **S2 主责**：按要素库在 `demo_gkxlumenx_ods` 建表             |
| OPEN-CHAIN-FLOW-07 | seeds 覆盖矩阵                                              | Demo / 数据       | S2                                                  |
| OPEN-CHAIN-FLOW-08 | ODS（4 表）→ 项目 DWD（v5 `industry_chain_*`）字段映射与拆分规则        | 架构 / 数据         | S2 后 Mapping；不挡 S1                                  |
| OPEN-CHAIN-FLOW-09 | 旧稿废弃声明（`DATA-CHAIN-db-design` PG 版、7 Mock 映射）           | 架构              | S1 handoff 起标注冲突以本树为准；S4 stub                       |
| OPEN-CHAIN-INDANA-01 | Demo `demo_gkxlumenx_dwd` 行业分析六张 `dwd_industry_analysis_*` 2026-08-16 抽检不存在；结构暂以三方 `gkx` live `SHOW CREATE` 复制 | data / 李伟 | 增量切片 · 未会签 |
| OPEN-CHAIN-INDANA-02 | CSV 主键=`document_id` vs 现表 PRI=`pk_id`；技术列 CSV 无。**现表 DDL 赢** | 数据 Lead | 增量切片 · 未会签 |
| OPEN-CHAIN-INDANA-03 | GDF 派单包无行业分析 Mapping 作业名（现行仅「企业」域），禁止编造 | GDF | 增量切片 · 未会签 |
| OPEN-CHAIN-INDANA-04 | 行业分析正文不并入 CHAIN ADS v2；图谱抽边读 DWD `industry_analysis_*` | 算法后续叶 | 增量切片 · 未会签 |
| OPEN-CHAIN-INDANA-05 | 本附录行业分析切片待 `human:李伟` 会签；**不**把主图 `signoff_status=approved` 改成本叶批准 | `human:李伟` | 增量切片 · 未会签 |




## 6. 下游放行（会签通过后生效）


| 阶段                                 | 结论                                                                                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **S2** `DATA-CHAIN-STORAGE-S2-L01` | **放行开工**：sources/etl/seeds + **必须按 md-extract「产业链要素库」在** `demo_gkxlumenx_ods` **建表**（表名/字段对齐文档；禁止只写清单不建表；禁止写正式 `gkxlumenx_ods`） |
| **S3** `stores/`*                  | 会签流图**不**等于细表 approved；S3 另单灌清单                                                                                                 |
| **S4** 旧路径 stub                    | 另单；冲突以本树为准                                                                                                                      |
| `data-design/产业链/*` legacy         | 输入可参考；**ODS 建表真源不认**旧稿，只认 `doc/`                                                                                                |




## 7. Demo / 约定 ODS 全链路

> 不改变 §1–3 拓扑；细化 Demo 如何稳定供数。细则：`[etl/pipeline-demo-mock.md](./etl/pipeline-demo-mock.md)`。

```mermaid
flowchart LR
  DOC["doc/ xlsx 权威<br/>md-extract 优先读"] -->|表结构约定| ODS["demo_gkxlumenx_ods"]
  MOCK["LLM / 离线样例"] -->|按约定写入| ODS
  ODS --> ETL["ETL 调度<br/>模拟 GDF"]
  ETL --> DWD["demo_* DWD"]
  DWD --> ADS["demo_* ADS"]
  DWD --> ES["ES"]
  DWD --> NEB["Nebula demo_**"]
  ETL --> MINIO["MinIO demo_** 桶"]
  JAVA["Java"] -->|只读| ADS
```




| 项               | 约定                                                                                                                                              |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| ODS 结构真源        | **权威** = `agent-delivery/data/third-party-source/doc/` xlsx；**优先读** = `doc/md-extract/`；**不是** `gkx-mysql-raw` as-built                         |
| 产业链要素库（S2 建表范围） | `dwd_industry_chain_info`、`dwd_org_industry_tags`、`dwd_org_industry_product_tags`、`dwd_industry_chain_news_info`（供应方命名带 `dwd_`，**角色为约定 ODS 表**） |
| 落库实例            | `demo_gkxlumenx_ods`（账号 `gkxlumenx`）；**禁止**默认写 `gkxlumenx_ods`                                                                                  |
| 调度              | Demo 灌数基于 ETL **模拟 GDF**（与正式同构）                                                                                                                 |
| 项目 DWD          | v5 `industry_chain_*` 经映射灌入 `demo_gkxlumenx_dwd`（后续）；**S2 不要求**一次建齐 14 张项目 DWD                                                                  |
| 旁路              | 直写 ADS 仅冒烟；**全链路验收以本图为准**                                                                                                                       |
| 行业分析六表（增量） | 入站现表 `dwd_industry_analysis_documents` / `_companies` / `_industries` / `_topics` / `_content_types` / `_countries` → 项目 DWD **仅去前缀** `industry_analysis_*`。**不**并入 ADS v2 十表。详见附录 A。 |


## 8. 表级数据血缘图

> **不改变** §1–3 工厂拓扑会签。本图给人看表怎么走；细表仍 **draft**。字段对照见 [`etl/ods-to-dwd-mapping.md`](./etl/ods-to-dwd-mapping.md)，步骤见 [`etl/pipeline-demo-sim-process.md`](./etl/pipeline-demo-sim-process.md)。  
> **灌数时序就一句**：ODS 四表 → 模拟 GDF 写十四表 → **同一批**重算 ADS + 投影 Nebula → 线上只读 ADS。名单/详情要名称时读 ADS（`topn` / `graph_snapshot` / `metric_*`），**不要再回 ODS**。  
> 本域 **没有** SVC 那种 circle / card：主体就在 DWD 树里。行业分析六表 **不并入** 本图（附录 A）。产业集群 DIM（`CL-*`→L0）是对照表，不是灌数主链。

```mermaid
flowchart TB
  subgraph ODS["ODS · 约定贴源 demo_gkxlumenx_ods（表名带 dwd_，角色仍是 ODS）"]
    INFO["dwd_industry_chain_info<br/>industry_link_code / level 树"]
    TAGS["dwd_org_industry_tags<br/>+ dwd_org_industry_product_tags"]
    NEWSO["dwd_industry_chain_news_info"]
  end

  subgraph DWD["DWD · 项目主表 demo_gkxlumenx_dwd · v5 十四表"]
    TREE["industry_chain + node + node_rel<br/>L0=INB / L1+ 子链"]
    ENTREL["industry_chain_entity_rel<br/>企业 credit / 产品挂节点"]
    EV["news_event<br/>+ invest mock 合成"]
    GAP["缺口五表诚实空<br/>市调 / 历程 / 抽取 / 模型"]
  end

  subgraph NEB["Nebula · 一张图"]
    G["demo_gkx_chain"]
  end

  subgraph ADS["ADS · 页面契约 demo_gkxlumenx_ads · v2 十表"]
    KPI["metric_fact / series / dist<br/>region_dist / scorecard / topn"]
    SNAP["graph_snapshot + graph_diff<br/>全景发布"]
    TXT["conclusion / narrative<br/>本灌数不写 CMS"]
  end

  subgraph ON["线上只读 ADS（不联 ODS）"]
    JAVA["50892 Java 只读 ADS<br/>专题产业链"]
    LAB["联调台产业链 BasicPage<br/>demo-algo-science"]
  end

  INFO -->|"模拟 GDF 写树"| TREE
  TAGS -->|"挂接"| ENTREL
  NEWSO -->|"资讯事件"| EV
  TREE -.->|"不灌假成功"| GAP
  TREE -->|"同一批 recalc_ads"| KPI
  ENTREL --> KPI
  EV --> KPI
  TREE -->|"同一批 project"| G
  ENTREL --> G
  EV --> G
  TREE --> SNAP
  G -.->|"全景优先图；空则回退 snapshot"| SNAP
  KPI -->|"名单/详情出名称"| JAVA
  SNAP --> JAVA
  KPI --> LAB
  SNAP --> LAB
  TXT -.-> JAVA
```

| 跳 | 谁写 | 失败 |
|---|---|---|
| ODS → DWD | Demo：Python `gdf_sim`（模拟 GDF）。生产：GDF（OPEN-CHAIN-FLOW-01） | 本批不晋升 ADS |
| DWD → ADS | Python `ads_v2.recalc_ads`（append/replace **都** TRUNCATE 后全量重算） | 不发布半成品；不写假 `M_CHAIN_MARKET_SIZE` / `M_CHAIN_INVEST_*` |
| DWD → Nebula | Python `project_nebula` | fail-soft，不阻断 ODS/DWD/ADS |
| 线上 | Java **只读** ADS；联调台可触发灌数/读 status | Java 不写库、不扫 ODS/DWD、不直连 nGQL |

**禁止**：Java/前端回 ODS 取名称；用 `industry_analysis_*` 冒充本图；平行第二张图；把 CMS 历程灌进 `narrative`/`conclusion` 装成功。

企业上链（`enterprise_industry_chain` → `entity_rel.entity_id=org_id`）是 ENT 侧 hang，投影进 **同一张** `demo_gkx_chain`，不另起主体表。


## 附录 A · 增量切片 · 未会签（行业分析六表）

> **本附录不是 2026-08-13 主图会签范围。** `signoff_status` 仍为 `human:李伟` **approved**（产业链拓扑）。  
> 任务 `DATA-CHAIN-INDANA-STORAGE-L01` 只登记切片，**禁止**把主图改签成本叶批准。待 `human:李伟` 会签增量（OPEN-CHAIN-INDANA-05）。

```mermaid
flowchart LR
  XLSX["md-extract 行业分析要素库<br/>英表 documents 等只对照"] --> INB["入站现表 dwd_industry_analysis_*"]
  INB --> ETL["ETL 模拟 GDF<br/>结构复制 仅去 dwd_"]
  ETL --> DWD["项目 DWD industry_analysis_*<br/>demo_gkxlumenx_dwd"]
  DWD --> PY["Python / 图谱抽边"]
  JAVA["Java"] -.->|不扫 DWD| DWD
  DWD -.->|不并入| ADS["CHAIN ADS v2 十表"]
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| 三方 `gkx` / 拟 Demo 入站六表 | 项目 DWD `industry_analysis_*` | 批：模拟 GDF（GDF 作业名缺席 → OPEN-CHAIN-INDANA-03） | 本批失败不晋升依赖下游；不半成品写 ADS | 用 `dwd_industry_chain_news_info` 冒充文档表；Java 扫 DWD；塞进 ENT `dwd-entity` |
| Python 算法 | Nebula（后续叶） | 读 DWD 正文及关联五表 | 读失败不伪造边 | 本叶写推理；Neo4j |

细表店面：[`stores/mysql/dwd-industry-analysis.md`](./stores/mysql/dwd-industry-analysis.md)（**draft**）。


