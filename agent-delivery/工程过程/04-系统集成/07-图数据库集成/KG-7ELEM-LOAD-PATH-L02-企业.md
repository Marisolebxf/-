# KG-7ELEM-LOAD-PATH-L02 · 七要素上图路径 · 企业

> 日期：2026-10-30  
> 任务：`KG-7ELEM-LOAD-PATH-L02`  
> 必须边只认已签收 `KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md`。Schema 缺项只认已签收 `KG-7ELEM-BUILD-REQ-L05-建图schema与存储设计缺项.md`。  
> 我方写图入口只认两个 demo 仓里能打开的代码：`repos/demo-algo-ent-analysis`、`repos/demo-algo-science`。`lumen-algo-py` 不作为本叶入口；正式仓没有对应写图，不把这件事写成我方未实现。  
> 燕大只对照 `yanda/tech-kg-api`（2026-10-30 工作区）。不选燕大 space 作生产。  
> `SYSINT-SCHEME-07-L03`、`SYSINT-SCHEME-07-L06` 未签收，只作台账索引。和代码不一致时以代码为准。`SYSINT-SCHEME-07-L02` 至 `L05`、`L07` 同样未签收；下文若点到，都标未签收。  
> 本叶未连图库，未连库，未执行 nGQL。表名、列名来自已打开的代码和已签收/storage 原文。代码在 `SELECT` 里点了名、storage 正文没列细列的，写「代码读取的列，本叶未连库核对现存列」。

本叶范围：企业端点；两端都是企业的 `cooperate`、`supply`、`parent_sub`。`participates`（企业→环节）、`policy_apply_to`（政策→企业）、`service_provide`（服务→企业）只在源能落到企业表或企业仓已读的表时写来源，另一端分别归 L03 / L04 / L05。不新增、不删除必须边。企业—科研机构、企业—技术、企业—人才不建。`technology` 技术点不计入七要素「技术」。`invest` 不进必须。

## 计数

| 项 | 条数 |
|---|---|
| 问 1 我方 | 6 |
| 问 1 燕大 | 3 |
| 问 2 我方 | 5 |
| 问 2 燕大 | 4 |
| 问 3 | 2 |
| 待确认 | 5 |
| 燕大有写图或对齐代码、我方 demo 没有同名实现 | 3 |

问 1 的 6 条里，和必须边同名且方向一致的是：企业点、`supply`、`parent_sub`，以及产业链仓的 `participates`（源不是企业表）。`cooperate`、`service_provide` 代码会写，方向对不上 M22、M21。

## 问 1 · 关系库现在就能上

「能上」指当前代码在 `dry_run=false` 且两端标识齐时会 `INSERT`。默认不传 `dry_run` 时，企业菜单入口只预览，不写库。

| # | 对象 | 我方 | 燕大 |
|---|---|---|---|
| 1 | 企业点 | **能上。** Tag `enterprise`，VID `ent:{org_id}`，长度 ≤80。源表 DWD `enterprise_base`（storage `dwd-entity.md` 有这张表）。代码读取的列：`org_id`、`enterprise_name`、`industry_category`、`headquarters_city`、`registered_capital`、`revenue_latest`、`rd_staff_count`、`patent_grant_count`、`legal_representative`、`is_high_tech`、`is_listed`、`is_little_giant`。写入列是 `name`、`node_type`、`weight`、`props`。入口：`demo-algo-ent-analysis/api/entan_graph_routes.py` 的 `POST /v1/entan/graph/ner` 与 `/internal/entan/graph/ner`；算子 `entan/graph/ops.py` `execute()`，`op_id=ENT_NER_ORG`。第二条入口：`entan/graph/nebula_loader.py` `run()` 默认走 `yiji_sim`，`_load_nodes` 只 `INSERT VERTEX enterprise`。space 字面量都是 `demo_gkx_chain`。正式库平面 `is_live("ent")` 时路由拒绝。步骤：确认 Demo 平面 → `dry_run=false` → 读 `enterprise_base` → 空 `org_id` 记 `empty_field`，VID 超 80 记 `vid_too_long` → 先写 ADS `entity_recognition`、`graph_node` → `USE demo_gkx_chain` → 必要时 `CREATE TAG IF NOT EXISTS enterprise` → `INSERT VERTEX`。图写入失败则 `source=ads`。`demo-algo-science/chainan/graph/nebula_schema.py` 的 `TAG_DDL` 声明了 `enterprise`，`chainan/graph` 下没有 `INSERT VERTEX enterprise`。 | **对照能上，不是生产 Tag。** Tag `Organization`，VID `org_{org_id}`。入口 `backend/script/organization_entity_etl.py` 的 `load`（示例命令写 `--table dwd_org_base_info`）。`organization_graph_etl.py` 已改成只转调实体装载，不写边。space 默认环境变量，缺省字面量 `dev`。不选作生产。 |
| 2 | M23 `supply` | **能上，方向与 L03 一致（企业→企业）。** L05 标存储设计已有。源表 `enterprise_supply_chain`。代码读取的列：`org_id`、`related_org_id`、`relation_type`、`relation_strength`。两端都要在 `enterprise_base.org_id` 里，VID 都是 `ent:`。入口：`entan_graph_routes.py` `POST /internal/entan/graph/intra` 或 `/ops/ENT_RE_SUPPLY`；`ops.py` `_intra`。`nebula_loader.py` 的边白名单含 `supply`，由 yiji `facts.iter_supply` 供数后再 `INSERT EDGE`。步骤：`dry_run=false`，`op_id=ENT_RE_SUPPLY` → 读供给表 → 缺 `related_org_id` 或对端不在主表则 `empty_field` / `no_stable_id` → ADS `graph_edge` → `INSERT EDGE supply(weight, props)`。 | **没有同名边。** `dev_organization_schema.ngql` 与 `organization_relation_etl.py` 的关系目录里没有 `supply`。 |
| 3 | M24 `parent_sub` | **能上，有向，代码方向是母→子。** L03 只写两端都是企业，没写死谁是母公司。L05 标存储设计已有，并写明母→子。源表 `enterprise_parent_subsidiary`。代码读取的列：`org_id`（子）、`parent_org_id`、`ownership_ratio`。权重 `ownership_ratio/100`。入口：`ops.py` `ENT_RE_BELONG`；`facts.iter_parent_sub` 再经 `nebula_loader._load_edges`。步骤同供给边，边类型换成 `parent_sub`。 | **没有 `parent_sub`。** 有对照边 `SUBSIDIARY_OF`：子公司→母公司。源表 `dwd_forg_subsidiary_info`。列：`org_id`、`affiliate`、`affiliates_company_id`、`affiliates_name`。入口 `organization_relation_etl.py` `extract_candidates` 的 `subsidiary`，以及 `relation_extractors_one_relation/subsidiary_of_relation.py`。无稳定 ID 时走唯一名称对齐，对不上则抛错不上边。L03 写的是新建 `parent_sub`、对照 `SUBSIDIARY_OF`，不复用。`SYSINT-SCHEME-07-L04` 未签收，这里不引用它放行。 |
| 4 | M22 `cooperate` | **有向边能上，双向必须边不能算已经上了。** L05：存储里的 `cooperate` 是有向，对不上 M22 双向，缺 Edge。源表 `enterprise_cooperation`。菜单路径只取 `partner_type=enterprise` 且有 `partner_org_id`，两端都在 `enterprise_base`。代码读取的列：`org_id`、`partner_type`、`partner_org_id`、`partner_name`、`cooperation_type`、`project_count`。方向本企→对方，VID `ent:`→`ent:`。入口 `ops.py` `ENT_RE_COOP`。没有 `partner_org_id` 时记 `no_stable_id`，不用名称当 VID。`nebula_loader` 也会 `INSERT EDGE cooperate`；yiji `partner_id` 对企业仍要求 `partner_org_id`。步骤同供给边，边类型 `cooperate`。这不是 M22 的双向边。 | **没有 `cooperate`。** 机构间写图目录里的企业间边是 `INVESTS_IN`、`ACQUIRES`、`SUBSIDIARY_OF`。`invest` 不进必须，不把 `INVESTS_IN` 当成合作。 |
| 5 | M17 `participates` | **产业链仓能写同名同向边；源不是企业表。另一端归 L03。** `demo-algo-science/chainan/graph/graph_ops.py` `_hang`，`op_id=CHAIN_RE_INDUSTRY_ENTERPRISE`。源表 `industry_chain_entity_rel`（不是 `enterprise_*`）。`entity_type=enterprise`，`relation_type` 为 `belongs_to` / `participates` / `participates_in` / `所属` / `参与` 时映射成 Edge `participates`。VID：`ent:{entity_id}` → 优先 `segment:{node_id}`，否则 `chain:{chain_id}`。两端都要 `FETCH` 已存在，不造企业点，也不造环节点。`nebula_project.py` 的批量投影对这类行只计数跳过（`entity_rel_fetch_only`），那个函数不写 `participates`。企业表 `enterprise_industry_chain` 由企业仓 `ops.py` `ENT_RE_INDUSTRY` 读取（列含 `chain_code`、`node_id` 及链名字段别名），写出的边名是 `industry_belong`，不是 `participates`。 | **没有 `participates`。** 对照写图是 `BELONGS_TO_NODE`：`org_{antitypic}` → `node_{node_id}`。源表 `dwd_org_industry_chain_dtl`，列 `antitypic`、`node_id`、`chain_score`。入口 `organization_relation_etl.py` 的 `industry_node`，以及 `industry_chain_etl/load_industry_chain_graph.py`、`relation_extractors_one_relation/belongs_to_node_relation.py`。L03 写明 `BELONGS_TO_NODE` 是归属、不并进 M17。终点 Tag 是 `IndustryNode`，不是 `segment`。 |
| 6 | M21 `service_provide` | **企业表能写出一条反向边，不能当成 M21。另一端归 L05。** 源在 `enterprise_cooperation`，`partner_type=service_org`，列 `partner_org_id`、`partner_name`。`ops.py` `ENT_RE_SERVICE` 方向是企业→服务，边名 `service_provide`，对端 VID 候选 `inst:` 或 `institution:`，必须 `FETCH` 命中。L03 / L05 的必须方向是服务→企业。 | **没有 `service_provide`。** |

`policy_apply_to` 不在问 1。企业仓 `ENT_RE_POLICY` 在 `ops.py` 里直接 `not_in_wave`（`OPEN-ENT-GRAPH-POLICY`），不读企业表。源不在企业表，另一端归 L04。见问 2。

`nebula_loader.ensure_schema` 还会 `CREATE EDGE`：`industry_belong`、`research_coop`、`talent_coop`、`service_provide`、`cooperate`、`supply`、`parent_sub`、`located_in`、`produces`、`invest`。其中科研、人才、技术应用、投资不在本叶必须边里，不因为 schema 里有名字就升成必须边。`_load_nodes` 只写企业点，不建第二套 Tag。

## 问 2 · 缺项，要先加工

只写方法。不建表，不灌数，不写 ODS，不写供应方库。`gapfill_` 只在下面点名的那一格作为可选层，本叶不建。

| # | 缺什么 | 我方建议 | 燕大对照 |
|---|---|---|---|
| 1 | M22 要双向，现码只写有向 `cooperate` | 不是缺 `enterprise_cooperation` 这张表。加工落在 ADS 映射或建图投影：同一对 `org_id` 若业务要双向，先定无向边还是两条有向，再投影。在未定之前，不要把现有有向 `INSERT` 报成 M22 已上图。L05 已标缺 Edge。 | 没有 `cooperate` 边，也没有我方这张合作表的装载。不能从 `INVESTS_IN` 改名补上。 |
| 2 | 合作、供给、母子有行但缺对端稳定 ID | 三张表分别缺 `partner_org_id`、`related_org_id`、`parent_org_id`（或对端不在 `enterprise_base`）。加工落在 DWD 映射：用已有稳定 ID 补列，再交给现有 `ops._intra`。不要在投影层用名称生成 `ent:`。补不到 ID 的行继续跳过。没有第二来源时，才考虑 `gapfill_` 前缀表存放人工确认过的 ID 对，仍不在本叶建表。 | 子公司边在没有 `affiliate` / `affiliates_company_id` 时依赖唯一名称。名称不唯一就不上。合作、供给没有对应装载，无从加工成那两条必须边。境内母子公司表：机构关系目录这条 spec 只绑了 `dwd_forg_subsidiary_info`，境内表名待确认。 |
| 3 | 企业表产不出 M17 `participates` | `enterprise_industry_chain` 有链码/节点码，企业仓写成 `industry_belong`。建议在 ADS 映射把 `org_id` + 已确认的环节 ID 收成 `participates`，方向企业→`segment:`，环节点仍由 L03 先落。映射未核对前不要把 `industry_belong` 或 `chn:` 当成 M17。 | `BELONGS_TO_NODE` 已能从 `dwd_org_industry_chain_dtl` 写入，终点不是 `segment`。要变成 M17 需要另做 Tag/边名映射，本叶不把对照边改名。 |
| 4 | M12 `policy_apply_to` 企业侧无表 | storage 与 `ops.py` 都没有企业→政策的 DWD 边。`ENT_RE_POLICY` 不上图。建议由政策域（L04）定政策 ID 之后，在 DWD/ADS 映射落「政策 ID + `org_id`」；没有稳定政策 ID 时不要造 `pol:`。可选层才是 `gapfill_`。不在企业仓发明边名。 | 机构 schema 有 `POLICY_PUBLISHED_BY`（政策→机构，发布），不是 `policy_apply_to`。本叶不把它当成适用关系。 |
| 5 | M21 方向是服务→企业，企业表行是企业→服务 | 列在 `enterprise_cooperation`。建议 ADS 映射时调换端点，服务机构点归 L05，且 `partner_org_id` 必须能 `FETCH` 到 `institution`。缺 ID 的行同问 2，不猜 VID。 | 没有 `service_provide`。没有可直接调向的同名边。 |

企业点能上。L05 另记 Tag `enterprise` 的属性在 ENT 与 CHAIN 各一套、没有收成一套。当前 `INSERT` 只用企业仓四列，不写 `enterprise_code` / `chain_role`。这不挡上点，本叶不另造列。

## 问 3 · 不能只靠源表，要先用其他技术

Java 不做 NLP、向量或模型推理。没有写图代码的写「未实现」。示例不代替已实现。

| # | 技术 | 我方 | 燕大 | 建议落点 |
|---|---|---|---|---|
| 1 | 名称到 `org_id` 的唯一对齐（精确匹配，多命中放弃） | **未实现。** `ops.py` 缺对端 ID 即 `no_stable_id`。`_llm_extra` 只在 `mode=llm` 时抽 `alias`、`industry_phrase`，提示语禁止编造 `org_id`，不写边。yiji `partner_id` 对非企业用名称当键；`nebula_loader._load_nodes` 不 `INSERT` 非企业点。不把名称键写成已对齐。 | **已实现，且不写在合作边上。** `organization_relation_etl.py` 的 `ExactOrganizationResolver`：底表名称只对应一个 `org_id` 才返回。用于子公司等无稳定 ID 的端点。`organization_milvus_index.py` 给已有点建向量索引，文件头写明不创建点、不创建边。向量索引不是上图。 | 若以后要做，放在 Python 关系装载里，位置与 `entan/graph/ops.py` 的 intra 同类：先得到唯一 `org_id`，再走现有 `INSERT`。示例只演示判定，见同目录 `KG-7ELEM-LOAD-PATH-L02/unique_name_to_org_id.py`。 |
| 2 | 从政策正文抽出「适用哪家企业」 | **未实现。** `ENT_RE_POLICY` 不读正文，直接 `not_in_wave`。LLM 分支不产政策边。 | **未实现 `policy_apply_to`。** 未见把政策正文抽成适用边的写图入口。 | Python 抽取入口，与政策域写图同类；抽出的必须是已有 `policy_id` 与 `org_id`。没有 ID 不上图。本叶不附政策抽取脚本，避免把未实现写成流程。另一端归 L04。 |

## 待确认

1. M22 双向在 Nebula 里落成无向边，还是一对有向边。存储和两份 demo 代码都没有无向 `cooperate` 的 `CREATE EDGE`。
2. `enterprise_industry_chain.node_id` 是否就是产业链 `segment:{node_id}` 的那个 ID。企业仓同时候选 `chain:`、`segment:`、`chn:`。
3. 燕大 `dwd_org_industry_chain_dtl.antitypic` 与我方 `enterprise_base.org_id` 是不是同一套标识。
4. 燕大境内母子公司源表名。已打开的机构关系 spec 只绑境外表 `dwd_forg_subsidiary_info`。
5. 服务机构正式 VID 用 `inst:` 还是 `institution:`。L05 写明两条都出现过，没有收成一条。企业仓 `FETCH` 两个都试。

## 不计入

- `invest` / 燕大 `INVESTS_IN`、`ACQUIRES`。L03：`invest` 不进必须。企业仓虽有 `ENT_RE_INVEST` 和 `enterprise_invest`，不升成必须边。
- 企业—科研机构、企业—技术、企业—人才。`research_coop`、`talent_coop`、`produces` 以及 Tag `technology` 不计入。`ENT_RE_TECH` 的挂接行查询直接返回空列表。
- 燕大 `Organization` 与论文、专利、项目、人才之间的边。那些端点归 L06。
- `lumen-algo-py`。本叶不把它列为写图入口。

## 入口索引（未签收台账，只帮助找文件）

`SYSINT-SCHEME-07-L06`（未签收）点名企业入口 `demo-algo-ent-analysis` 的 `api/entan_graph_routes.py` 与 `entan/graph/ops.py`。当前工作区这两份文件，以及 `nebula_loader.py`，space 字面量是 `demo_gkx_chain`。L06 里「改动还在本地、未发布」是台账句子；本叶不据此改写代码，也不把「源码里已是这个 space」说成集群已发布。

`SYSINT-SCHEME-07-L03`（未签收）把企业写图记在 lumen 路径下。本叶不采用。以 demo 仓打开的文件为准。
