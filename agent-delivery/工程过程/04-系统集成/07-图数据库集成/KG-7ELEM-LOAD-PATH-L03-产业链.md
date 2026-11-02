# KG-7ELEM-LOAD-PATH-L03 · 七要素上图路径 · 产业链

> 日期：2026-10-30  
> 任务：`KG-7ELEM-LOAD-PATH-L03`  
> 必须边只认已签收 `KG-7ELEM-BUILD-REQ-L03`：Tag `segment`，M15 `depends_on`（segment→segment），M17 `participates`（enterprise→segment），M18 `participates`（service_institution→segment）。不新增、不删除必须边。  
> 产业链到科研机构、技术、人才不建。`technology` 技术点不是七要素「技术」。`chain` 不是产业链环节。  
> 我方写图入口以 `repos/demo-algo-science` 为准。`lumen-algo-py` 没有 `/v1/chain/graph` 与 `/internal/chain/graph`。  
> 燕大只对照 `yanda/tech-kg-api`（2026-10-30 工作区）。不选燕大 space 作生产，不把燕大边名复用放行。  
> `SYSINT-SCHEME-07-L03`、`L06` 未签收，只当索引。已实现以代码为准。未连库，未执行 nGQL。

企业点的来源归 `KG-7ELEM-LOAD-PATH-L02`。服务机构点的来源归 `KG-7ELEM-LOAD-PATH-L05`。本叶只写环节这一端，以及边落到 `segment:` 的条件。

## 0. 不进三问的代码

这些代码在，本叶不算必须路径。

| 代码 | 为什么不进 |
|---|---|
| `CHAIN_RE_BELONGS_TO` | 边 `belongs_to`，segment→chain。`chain` 不是环节 |
| `CHAIN_RE_INDUSTRY_RESEARCH` | 会写 `participates` 到 `inst:`。L03 产业链—科研机构不建 |
| `CHAIN_RE_INDUSTRY_TECH` / `_TALENT` | `graph_ops.py` 里 `on_graph=False`，记 `not_in_wave`。L03 明文不写 |
| `CHAIN_RE_INDUSTRY_POLICY` | 终点可以是 chain 或 segment。L03 产业链—政策不建 |
| 燕大 `HAS_NODE` | IndustryChain→IndustryNode。链不是环节 |
| `demo-algo-ent-analysis` `SVC_RE_INDUSTRY` | 边名是 `belongs_to`，不是 M18 的 `participates`。机构端归 L05 |

`chainan/graph/nebula_project.py` 的 `project_from_dwd` 仍能写点边，并会新建企业、机构点。`tests/test_chain_graph_ops.py` 断言灌数脚本不再调用它。菜单入口是下面的 `/chain/graph/*`。

## 1. 关系库现在就能上

白名单在 `repos/demo-algo-science/chainan/graph/nebula_project.py`：`NODE_REL_EDGE`、`ENTITY_REL_EDGE`。Schema 在同仓 `chainan/graph/nebula_schema.py` 的 `TAG_DDL` / `EDGE_DDL`。路由在 `api/main.py`：`/v1/chain/graph/*` 转到同名 `/internal/chain/graph/*`。`ner` 固定 `CHAIN_NER_INDUSTRY`。`intra` / `hang` 不代填 `op_id`，body 里要带。`/ops/{op_id}` 用路径上的算子名。实现是 `chainan/graph/graph_ops.py` 的 `run_graph_op`。

上图步骤（我方，只写本叶这三条）：

1. `POST /internal/graph-schema-init` 只补 Tag/Edge，不灌点。space 必须已是 `demo_gkx_chain`。
2. `POST /internal/chain/graph/ner`，body 带 `scope=one|batch`。`_ner` 读 `industry_chain_node`，写 Tag `segment`，VID `segment:{node_id}`。同时会写 Tag `chain`，那不是环节。
3. `POST /internal/chain/graph/ops/CHAIN_RE_DEPENDS_ON`。`_depends` 读 `industry_chain_node_rel`。`relation_type` 不在白名单则 `not_in_wave`。`relation_direction=reverse` 时对调两端。两端都要 `FETCH` 到已有 `segment:`，否则 `no_stable_id`。
4. 企业点 `ent:` 先由 L02 上图。然后 `POST /internal/chain/graph/ops/CHAIN_RE_INDUSTRY_ENTERPRISE`。`_hang` 读 `industry_chain_entity_rel`。`FETCH` 不到企业点则不新建。`node_id` 能对上已有 `segment:` 才算 M17；对不上就改挂 `chain:`，那条不是必须边。
5. 服务机构点归 L05。`CHAIN_RE_INDUSTRY_SERVICE` 的代码路径与第 4 步相同，但正式加工不产这种行，见第 2 问。

| # | 对象 | 我方 | 燕大 |
|---|---|---|---|
| 1 | 环节 Tag | 能上。DWD `industry_chain_node`：`node_id`、`node_name`、`node_code`、`chain_id`、`stage_code` → Tag `segment`（`name`、`segment_key`、`chain_id`、`chain_stage`、`weight`、`props`）。入口 `_ner`。正式加工 `产业链域-ETL-Mapping明细-源表到DWD.md` §3.2：`level>=2` 的链树行洗进这张表 | 能上，Tag 名不同。`backend/script/entity_extractors_one_entity/industry_node_entity.py` 读 `dwd_industry_chain_info`，`mappers.py` `industry_node_record` 写 `IndustryNode`，VID `node_{node_id}`。字段：`node_id`、`node_name`、`node_type`、`level`、`node_seq`、`node_imp_level`、`node_stage`、`node_path`。同逻辑还在 `backend/script/workflow/paper_journal_chain_etl.py` `_load_industry_chain`。不选这个 Tag 作生产 |
| 2 | M15 `depends_on` | 能上的只是白名单行。DWD `industry_chain_node_rel`：`source_node_id`、`target_node_id`、`relation_type`、`relation_direction`、`relation_weight`、`relation_id`、`chain_id`。白名单：`upstream` / `downstream` / `depends` / `depends_on` / `dependency` / `上下游` / `依赖`。入口 `_depends`。方向 segment→segment | 没有边名 `depends_on`。`CHILD_OF` 见本问第 4 条，不并进 |
| 3 | M17 `participates` 企业→环节 | 能上。DWD `industry_chain_entity_rel`：`entity_type=enterprise`，`entity_id`，`relation_type` 为 `belongs_to` / `participates` / `participates_in` / `所属` / `参与`，`node_id`，`role_type`，`relation_id`。起点 `ent:{entity_id}`，终点 `segment:{node_id}`。入口 `CHAIN_RE_INDUSTRY_ENTERPRISE`。正式加工同 Mapping §3.4：`dwd_org_industry_tags` 拆行后写 `relation_type=belongs_to`，`entity_id` 取 `enterprise_base.org_id`。企业端归 L02。`demo-algo-ent-analysis` 没有这条边的写图 | 代码写的是另一条边。`backend/script/relation_extractors_one_relation/belongs_to_node_relation.py` 读 `dwd_org_industry_chain_dtl` 的 `antitypic`、`node_id`、`chain_score`，写 `BELONGS_TO_NODE`（Organization→IndustryNode）。`organization_etl_common.py` 有同名 `RelationSpec`。L03 写明这是归属，不是参与，不复用 |
| 4 | 燕大环节父子 | 未实现。我方不写 `CHILD_OF` | 能上。`child_of_relation.py` 的 `child_of`：`dwd_industry_chain_info.parent_id`、`node_id` → `CHILD_OF`，`node_{node_id}`→`node_{parent_id}`。`paper_journal_chain_etl.py` 同样在 `parent_id` 非空时写。L03：这是上下级，不是 `depends_on`，不复用 |

L02 消费行 A02、A24、A27 的表名写的是待确认。上表我方表名来自代码和 DWD 设计，不把消费行的「待确认」改成已闭合。

## 2. 缺项要先加工

只写方法。不建表，不灌数，不写 ODS，不写供应方库。

| # | 缺什么 | 我方建议 | 燕大 |
|---|---|---|---|
| 1 | M15 的上下游行。正式 Mapping §3.3 无独立边表，只从父节点派生 `industry_chain_node_rel.relation_type=parent_child`。`parent_child` 不在 `NODE_REL_EDGE`，`_depends` 会 `not_in_wave`。Demo 模拟映射按 `sort_no` 相邻生成 `upstream`，正式 Mapping 写明不要那样伪造 | 在 DWD `industry_chain_node_rel` 把上下游写成白名单里的 `relation_type`，两端用已有 `node_id`。父子边保持 `parent_child`，不要改名充 `depends_on`。没有上游事实时，用 `gapfill_` 前缀表只存加工结果，再映射进这张 DWD 关系表。`parent_node_id` 只补节点父子，不代替这条边 | 无 `depends_on`。`DOWNSTREAM_OF` 见本问第 3 条 |
| 2 | M18 服务机构→环节。`CHAIN_RE_INDUSTRY_SERVICE` 只认 `entity_type=service_institution` 且关系类型在 `ENTITY_REL_EDGE`。CHAIN 正式加工 §3.4 只写 `entity_type=enterprise`。`demo-algo-ent-analysis` `svc_routes.py` 的 `/v1/svc/graph/hang`、`/internal/svc/graph/hang` 走到 `SVC_RE_INDUSTRY`，边是 `belongs_to`，不是 `participates` | 在 DWD `industry_chain_entity_rel` 增加服务机构行：`entity_type=service_institution`，`relation_type=participates`（或白名单里的 `belongs_to`），`node_id` 指向已有环节，`entity_id` 用 L05 的机构键。机构主数据不在本叶加工。不要把 SVC 的 `belongs_to` 算成 M18 | 没有服务机构到环节的边。`BELONGS_TO_NODE` 的起点是 Organization，不区分服务机构。拆分列归 L05，本叶不补 |
| 3 | 燕大上下游列 | 不把燕大列迁进生产。我方按本问第 1 条加工 | `downstream_of_relation.py` 读 `dwd_industry_chain_info.downstream_link_code`。列空则返回空边。未连库，这列有没有值待确认。未签收 `SYSINT-SCHEME-07-L04` 记 0 边，不作本叶结论 |

## 3. 不能靠源表、要先用其他技术

| # | 技术 | 我方 | 燕大 |
|---|---|---|---|
| 1 | 从正文抽上下游来补 M15 | 未实现。`graph_ops.py` `_mode_effective`：`mode=llm` 仍然返回 `rule`，不调用模型。`CHAIN_NER_INDUSTRY` 是按表写点，不是实体识别模型。Java 不做这件事 | 未实现。`backend/script` 下产业抽取没有 llm、向量或 NER。`DOWNSTREAM_OF` 只读列 |

环节名、父子、企业挂节点都能从关系列来，不靠这一问。第 2 问的 `gapfill_` 或 DWD 映射仍是加工，不是模型。

示例（未实现，不能当已上图）：`KG-7ELEM-LOAD-PATH-L03/upstream_from_text.py`。只说明核心判断，不接库，不加依赖。

## 4. 计数

| 项 | 数 |
|---|---|
| 第 1 问 | 4 |
| 第 2 问 | 3 |
| 第 3 问 | 1 |
| 待确认 | 6 |
| 燕大有代码、我方没有 | 3 |

待确认：

1. L02 消费行 A02、A24、A26、A27 的表名仍是待确认。
2. `parent_child` 能不能写成 `depends_on`。本叶不并。L03 把上下级和上下游分开。
3. 燕大 `downstream_link_code` 有没有值。未连库。
4. 我方 `industry_chain_entity_rel` 里有没有 `entity_type=service_institution` 行。未连库。
5. M15、M17、M18 的基数。L03 写待确认。
6. 燕大 `dwd_org_industry_chain_dtl` 与我方 DWD 不是同一张表。未签收 L04 曾写本地无此表。当前燕大代码仍读它。有没有行待确认。

燕大有代码、我方没有：`CHILD_OF`、`BELONGS_TO_NODE`、`DOWNSTREAM_OF`。三条都不复用为必须边。
