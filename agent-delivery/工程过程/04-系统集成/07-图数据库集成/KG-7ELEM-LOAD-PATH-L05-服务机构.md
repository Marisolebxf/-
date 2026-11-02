# KG-7ELEM-LOAD-PATH-L05 · 服务机构上图路径

> 日期：2026-10-30  
> 任务：`KG-7ELEM-LOAD-PATH-L05`  
> 监管：`human:淮政玮`  
> 范围：服务机构端点 Tag `institution`，以及服务机构这一端的必须边。环节一端归 `KG-7ELEM-LOAD-PATH-L03`，企业一端归 `KG-7ELEM-LOAD-PATH-L02`。  
> 必须边只记两条：M18 `participates`（服务机构 → 产业链环节）、M21 `service_provide`（服务机构 → 企业）。基数沿用已签收 L03，均为待确认。  
> 服务机构互相 `participates` 不补。科研机构不写入本叶。  
> 我方写图入口在算法中台 demo 仓。`lumen-algo-py` 没有服务机构写图入口。  
> 燕大只读 `yanda/tech-kg-api`（2026-10-30 13:19 工作区）。不选燕大 space 作生产。  
> 本叶不执行 nGQL，不连图库，不连库。

已签收输入：`KG-7ELEM-BUILD-REQ-L03`、`KG-7ELEM-BUILD-REQ-L05`。  
存储设计：`data/data-design/storage/SVC/etl/pipeline-to-nebula.md`、`stores/nebula/graph-svc.md`（frontmatter 均为 draft）。  
台账 `SYSINT-SCHEME-07-L03`、`SYSINT-SCHEME-07-L06` **未签收**。下文「已实现」以仓库里能打开的代码为准。L03 台账把服务机构写图记在 `lumen-algo-py/vendor/entan-py`，与本叶补充不一致，不采纳。

## 0. 不纳入

| 项 | 处理 |
|---|---|
| 服务机构 `participates` 服务机构 | 代码有 `SVC_RE_SVC_SVC`（`demo-algo-ent-analysis/api/svc_routes.py` 的 `/v1/svc/graph/intra`）。已签收 L03 写明不建，A21 方向待确认。本叶不补进必须边 |
| 科研机构 | 链上 `CHAIN_RE_INDUSTRY_RESEARCH` 读 `entity_type=institution`。燕大 `org_kind=domestic_research_institute` 来自 `dwd_research_institute_base_info`。这两条都不是服务机构 |
| 服务机构—技术、人才、政策、科研机构 | 已签收 L03 写明不建。`SVC_RE_TECH` / `SVC_RE_TALENT` 在代码里记 `not_in_wave` |
| `lumen-algo-py` | `lumen_algo_service` 没有 `SVC_NER_ORG`。`vendor/entan-py` 是 demo 副本，不另计为我方入口 |

读图附注（不是上图）：`demo-algo-science/chainan/graph/nebula_project.py` 的 `overview_cat` 在已有 `institution` 点上，用名称含「服务」或 `institution_type` 为 `service` / `service_institution` 分成服务，其余标 `org`。这是浏览分类，不写点。名称里带「服务」的科研机构不会因此变成服务机构端点。

## 1. 关系库现在就能上

一条。服务机构端点。两条必须边都还不能从现有关系行直接写成已签收的边名和方向，见第 2 节。

| # | 对象 | 我方 | 燕大 |
|---|---|---|---|
| 1 | 服务机构端点 Tag `institution` | 能上。源表 Demo DWD `svc_org_circle`、ADS `svc_org_card`。字段：`org_id`、`name_cn`、`service_type_candidate`、`province`、`city`、`area`、`industry`、`org_size`、`employees_number`。Tag `institution`。VID `institution:{org_id}`，长度 ≤80。`props` 内 `role=service`，用来和科研机构分开。入口与步骤见下 | 没有服务机构 Tag，也没有服务机构写图入口。`Organization` 来自机构域多表，`org_kind` 只有高校、科研院所、港澳台公司、海外机构，其余默认 `domestic_organization`。不能把 `Organization` 当成服务机构端点 |

我方代码入口（都能在仓库打开）：

| 层 | 路径 |
|---|---|
| HTTP | `repos/demo-algo-ent-analysis/api/svc_routes.py`：`POST /v1/svc/graph/ner`、`POST /internal/svc/graph/ner`，函数 `svc_graph_ner` |
| 算子 | 同仓 `entan/svcgraph_ops.py`：`execute()`，`op_id=SVC_NER_ORG` |
| 写点 | 同仓 `entan/svcgraph.py`：`TAG="institution"`，`VID_PREFIX="institution:"`，`_upsert_nebula()` 写 `INSERT VERTEX` |
| 旧入口 | 同文件 `run_graph()`，HTTP `POST /internal/svc/run-graph`。它调用 A 档全量，不传 `dry_run` |

上图步骤：

1. 圈定结果已在 `svc_org_circle`（规则 A，`entan/svcseed.py`）。灌数本身不写 Nebula。
2. 顶栏产业服务平面须为 Demo。正式平面时 `svc_graph_ner` 直接拒绝。
3. 调用 `POST /internal/svc/graph/ner`，body 带 `op_id=SVC_NER_ORG`，`scope=one` 且 `id=org_id`，或 `scope=batch` 且带 `org_ids` / `service_type` / `province` / `city` / `filter.all=true`。
4. `execute` 读 `svc_org_circle` 左连 `svc_org_card`，用 `node_id_of` 生成 `institution:{org_id}`。
5. `DESCRIBE TAG institution` 里有的列才写入。候选列是 `name`、`institution_type`、`node_type`、`weight`、`props`、`role`。`props` JSON 固定带 `role=service`。
6. 空间只认 `demo_gkx_chain`。缺 Tag 则整批 skipped，不 `CREATE TAG`。
7. 代码里 `dry_run` 默认是 `bool(body.get("dry_run"))`，未传等于写。未签收 L06 写「未传 dry_run 只预览」，与这段代码不一致，以代码为准。要只预览须显式 `dry_run=true`。

沿用已签收 L05，不新开待确认：现网 VID 是 `institution:{org_id}`，目标 VID 是 `inst:{org_id}`，两条都写了，没有收成一条。`node_type`、`role` 的类型存储设计未写；代码按 DESCRIBE 有则写。

D 档 `GET /v1/svc/graph` 读的是 DWD `svc_org_graph_hang` 加卡面，不读 Nebula。

## 2. 缺项要先加工

两条。只写方法。不建表，不灌数，不写 ODS，不写供应方库。

| # | 必须边 | 缺什么 | 建议加工层 | 我方已有代码（不能直接当本边已上图） | 燕大 |
|---|---|---|---|---|---|
| 1 | M18 服务机构 `participates` 产业链环节。环节一端归 L03 | 没有「服务机构 `org_id` → 环节 `node_id`」的关系行。卡面只有展示列 `industry`（`svc_ddl_demo_empty.sql` 的 `svc_org_card`），没有环节码。`SVC_RE_INDUSTRY` 把 `industry_link_code` 写成空字符串，行业名对不上 `chain:` / `segment:` 就 `no_stable_id`，边名还是 `belongs_to`，不是 `participates`。CHAIN 的 ODS→DWD 映射只写了 `entity_type=enterprise` 和 `product`，没有 `service_institution` | 在项目 DWD `industry_chain_entity_rel` 上补映射：`entity_type=service_institution`，`entity_id` 用 `svc_org_circle.org_id`，`node_id` 用已有环节主键，`relation_type` 用代码白名单里的 `belongs_to` 或 `participates`（投影时都写成 Nebula `participates`）。对不上环节主键的行业名不要写入。不要新造边名 | 见下。行不存在就上不了 | 没有这条边。`BELONGS_TO_NODE` 的中文是「企业归属产业链节点」，源表 `dwd_org_industry_chain_dtl`，方向 `Organization` → `IndustryNode`。已签收 L03 写明这是归属，不是 M18。不计入本叶 |
| 2 | M21 服务机构 `service_provide` 企业。企业一端归 L02 | 没有「服务机构 `org_id` → 企业 `org_id`」且方向为服务机构指向企业的关系列。`SVC_RE_ENTERPRISE` 对非产业终点返回空字典，对端 ID 为空，结果是 `empty_field`，边名是 `participates` 不是 `service_provide`。企业侧 `enterprise_cooperation` 有 `partner_org_id`，但 `ENT_RE_SERVICE` 的起点是企业 VID，`partner_type=service_org` 时对端才是服务机构；这是企业 → 服务，Tag 兜底是 `service`，不是 `institution` | 在项目 DWD 或 `gapfill_` 前缀表写两列：服务机构 `org_id`、企业 `org_id`。加工时只保留两端都能对上已有 `org_id` 的行。方向保持服务机构 → 企业。企业侧那一列的读法归 L02。不要用 `partner_name` 造 VID | `demo-algo-ent-analysis/entan/svcgraph_ops.py` `_hang_item`；同仓 `entan/graph/ops.py` `ENT_RE_SERVICE`、`_hang_rows` | 边清单里没有 `service_provide`，也没有服务机构到企业的写边脚本 |

M18 我方链上代码（环节一端归 L03，本叶只写服务机构这一端的来源）：

| 层 | 路径 | 行为 |
|---|---|---|
| 菜单 C | `repos/demo-algo-science/api/main.py` `POST /internal/chain/graph/hang`、`POST /v1/chain/graph/hang`，转入 `chainan/graph/graph_ops.py` `run_graph_op` | `op_id=CHAIN_RE_INDUSTRY_SERVICE` 时只认 `industry_chain_entity_rel` 里 `entity_type=service_institution` 且 `relation_type` 能映射的行。起点 VID 用 `inst:{entity_id}`，终点优先 `segment:{node_id}`。图上没有这两个点就跳过，不新建点 |
| 批量投影 | 同仓 `chainan/llm_ods/project.py` → `chainan/graph/nebula_project.py` `project_from_dwd` / `map_graph` | 同一张表、同一套映射。现网会新建 Tag `institution` 的点，VID 前缀是 `inst:`，再写 `participates`，起点是机构 VID，终点是环节或链 |

代码方向是服务机构 → 环节，与已签收 M18 一致。已签收 L05 引用的 CHAIN etl §12 文字写成「产业/环节 → 对象」。本叶不改那份已签收正文。汇总时以代码的 src/dst 为准。  
服务机构点若已由第 1 节写成 `institution:`，链上 C 档只 FETCH `inst:`，两边对不齐。加工映射时 VID 前缀要跟端点写点入口收成同一条，仍沿用 L05 尚未收口的那两条，本叶不新选。

`entity_type=service_institution` 的行现在有没有：映射没写，本叶不连库，**待确认**。

`enterprise_cooperation` 里 `partner_type=service_org` 的 `partner_org_id` 有没有值：本叶不连库，**待确认**。即便有值，现有 `ENT_RE_SERVICE` 的方向仍是企业 → 服务，不能直接当成 M21。

## 3. 不能靠源表、要先用其他技术

两条。Java 不做 NLP、向量或模型推理。下面「未实现」是仓库里没有这条逻辑。同目录示例脚本只说明核心判断，不是已实现。

| # | 场景 | 技术 | 我方代码 | 建议 Python 入口 | 燕大 |
|---|---|---|---|---|---|
| 1 | 卡面上只有行业名，要连到环节 VID | 实体链指（名称对已知环节名 / 环节码）。对不上就不上图 | 未实现。`_llm_extra` 只补人数、规模短语，并禁止编造 VID。链指 L6 在 SVC etl §15 写明默认关闭、须拍板 | `demo-algo-ent-analysis/entan/svcgraph_ops.py` 的 `SVC_RE_INDUSTRY` 旁。只在已有环节主键表上比对，不新建依赖 | 未实现。离线 Milvus 用于机构消歧，不产出服务机构 → 环节 |
| 2 | 正文里有「为某企业提供服务」，要连到企业 VID | 关系抽取。抽出的是短语，不是 `org_id`。没有稳定 ID 就不上图 | 未实现。`SVC_RE_ENTERPRISE` 不读正文 | 同上，`SVC_RE_ENTERPRISE` 旁。短语只作候选，企业 `org_id` 仍要关系库对上 | 未实现。没有服务机构到企业的抽取脚本 |

示例（未实现）：`工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L05/q3_link_core.py`。只含标准库，不接数据库，本叶未执行。

## 4. 计数

| 项 | 数 |
|---|---|
| 第 1 问 | 1 |
| 第 2 问 | 2 |
| 第 3 问 | 2 |
| 待确认 | 5。见下 |
| 燕大有代码、我方没有 | 0 |

待确认：

1. `industry_chain_entity_rel.entity_type=service_institution` 是否已有行（不连库）。
2. `enterprise_cooperation` 中 `partner_type=service_org` 的 `partner_org_id` 是否有值（不连库）。
3. M18 基数。已签收 L03 写待确认。
4. M21 基数。已签收 L03 写待确认。
5. A21 服务机构互相 `participates` 的方向。已签收 L03 写待确认。本叶不补这条边。

燕大 `BELONGS_TO_NODE`、`Organization` 写点都有代码，端点和边名都不是本叶必须三元组，不计入「燕大有而我方没有」。
