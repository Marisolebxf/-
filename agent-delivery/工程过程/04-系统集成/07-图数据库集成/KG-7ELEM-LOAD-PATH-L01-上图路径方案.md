# KG-7ELEM-LOAD-PATH-L01 · 七要素上图路径方案

> 日期：2026-10-30  
> 任务：`KG-7ELEM-LOAD-PATH-L01`  
> 监管：`human:淮政玮`。`claim_type=coordinator_dispatch`。  
> 本叶只汇总 L02–L06 已写结论。不重查代码，不重裁必须边，不改五张子单正文，不改它们的示例脚本。  
> 必须边与 schema 仍只认子单所引的已签收 `KG-7ELEM-BUILD-REQ-L03`、`KG-7ELEM-BUILD-REQ-L05`。  
> 我方写图入口只认子单点名的 `demo-algo-science`、`demo-algo-ent-analysis`。`lumen-algo-py` 不补成我方入口。  
> 燕大只作已实现对照，不选燕大 space 作生产。久新 `ads_*` 不是我方 ADS。  
> 未实现保持未实现。`technology` 技术点不计入七要素「技术」。服务机构互相 `participates` 不补。企业—科研机构、企业—技术、企业—人才不建。

同一条边跨两域时，两叶各写一端，下面合成一行，两套说法都保留。子单之间数字或入口不一致时，以子单正文为准，冲突写在第 8 节，不改子单。

---

## 0. 合成计数

| 项 | 条数 | 口径 |
|---|---:|---|
| 第 1 问 | 13 | 子单放在「关系库现在就能上」的行，跨域合成后。含我方未实现、只是对照或久新能对上的行 |
| 第 2 问 | 17 | 缺项要先加工。跨域合成后 |
| 第 3 问 | 8 | 不能靠源表、要先用其他技术。跨域合成后 |
| 我方已实现 | 10 | 正文写「能上」或「已实现」，且没有「不能当成必须边」。跨域计一次 |
| 燕大有代码、我方没有 | 12 | 子单已计入的对照。`BELONGS_TO_NODE` 两叶都计，汇总计 1 |
| 久新现库能对上、我方没有写图 | 2 | 只取 L06 第 1 问那两条。待确认 6 条不计入 |
| 待确认 | 25 | 子单待确认相加 27，两处同一问题合成后减 2 |
| 子单冲突 | 4 | 见第 8 节。另有归位 3 处，不是改判 |

我方已实现 10 条：企业点、M23 `supply`、M24 `parent_sub`、环节 `segment`、M15 白名单 `depends_on`、M17 产业链仓 `participates`、政策点、M16 约定格式 `cite`、M16 的 `mode=llm` `cite_pids`、服务机构点。

未实现保持未实现。M22 的有向 `cooperate` 会写，双向必须边不能算已经上，不计入这 10 条。M21 会写反向边，不能当成必须边，不计入。L06 写明我方第 1 问是 0 条。

### 0.1 叶计数与合成差额

数字取各叶正文的计数节，不取 handoff 缩句。

| 叶 | 问 1 | 问 2 | 问 3 | 待确认 | 燕大有、我方没有 |
|---|---:|---:|---:|---:|---:|
| L02 | 6 | 5 | 2 | 5 | 3 |
| L03 | 4 | 3 | 1 | 6 | 3 |
| L04 | 2 | 5 | 4 | 5 | 0 |
| L05 | 1 | 2 | 2 | 5 | 0 |
| L06 | 2 | 9 | 0 | 6 | 7 |
| 相加 | 15 | 24 | 9 | 27 | 13 |
| 合成 | 13 | 17 | 8 | 25 | 12 |

差额：

- 问 1：15 减去 M17 在 L02、L03 各占一行，再减去 M21。M21 按正文「不能当成必须边」收到问 2，见第 8 节归位。
- 问 2：24 减去 7。M17 的企业表路径收到问 1 的合成行；M18、M21、M12、M13、M14、M10 各由两叶合成一行。L03 问 2 的燕大 `downstream_link_code` 仍单独占一行。
- 问 3：9 减去 1。L02 的政策正文抽企业，与 L04 的 M12/M13/M14 正文抽取，合成一行。
- 待确认：27 减去 2。服务机构关系行有无，L03 与 L05 是同一问；M18 基数，L05 已写在 L03 的「M15、M17、M18 基数」里。
- 燕大：13 减去 1。`BELONGS_TO_NODE` 在 L02 与 L03 各计 1，L05 不计。
- 久新：2。无跨叶重复。L02–L05 未做久新探查，汇总不补。

---

## 1. 第 1 问 · 关系库现在就能上

13 行。其中计入我方已实现的是 1、2、3、5、6、7、9、10、11，共 9 条。第 12、13 行是久新键对得上，我方没有写图。第 4 行双向必须边未上。第 8 行我方未实现。M16 的大模型路径在第 3 问，另行计入已实现。

| # | 对象 | 子单结论 | 回指 | 我方已实现 |
|---|---|---|---|---|
| 1 | 企业点 Tag `enterprise` | 我方能上。VID `ent:{org_id}`。源表 DWD `enterprise_base`。入口 `demo-algo-ent-analysis` 的 `entan_graph_routes.py`、`ops.py` `ENT_NER_ORG`、`nebula_loader.py`。`demo-algo-science` 只声明该 Tag，不 `INSERT` 企业点。燕大对照 Tag `Organization`，不选作生产 | L02 问 1 #1 | 是 |
| 2 | M23 `supply` 企业→企业 | 我方能上，方向与已签收 L03 一致。源表 `enterprise_supply_chain`。入口 `ENT_RE_SUPPLY` 与 `nebula_loader`。燕大没有同名边 | L02 问 1 #2 | 是 |
| 3 | M24 `parent_sub` | 我方能上，代码方向母→子。源表 `enterprise_parent_subsidiary`。入口 `ENT_RE_BELONG`。燕大没有 `parent_sub`，对照边 `SUBSIDIARY_OF` 方向相反，不复用 | L02 问 1 #3 | 是 |
| 4 | M22 `cooperate` | 有向边能写，双向必须边不能算已经上。源表 `enterprise_cooperation`，方向本企→对方。入口 `ENT_RE_COOP`。燕大没有 `cooperate`。`invest` 不进必须 | L02 问 1 #4；加工见问 2 #1 | 否 |
| 5 | 环节 Tag `segment` | 我方能上。DWD `industry_chain_node`，VID `segment:{node_id}`。入口 `demo-algo-science` `_ner` / `CHAIN_NER_INDUSTRY`。同时会写 Tag `chain`，`chain` 不是环节。燕大能上 `IndustryNode`，不选作生产 | L03 问 1 #1 | 是 |
| 6 | M15 `depends_on` 白名单行 | 能上的只是白名单行。DWD `industry_chain_node_rel`，入口 `_depends` / `CHAIN_RE_DEPENDS_ON`。方向 segment→segment。燕大没有边名 `depends_on`。正式加工的 `parent_child` 见问 2 | L03 问 1 #2 | 是（仅白名单行） |
| 7 | M17 `participates` 企业→环节 | 企业端：产业链仓能写同名同向边，源不是企业表。企业仓把 `enterprise_industry_chain` 写成 `industry_belong`，不能当成 M17。环节端：DWD `industry_chain_entity_rel`，`entity_type=enterprise`，入口 `CHAIN_RE_INDUSTRY_ENTERPRISE`；`node_id` 对上已有 `segment:` 才算 M17，否则挂 `chain:` 不是必须边。`demo-algo-ent-analysis` 没有这条边的写图。燕大 `BELONGS_TO_NODE` 是归属，不并进 | L02 问 1 #5、问 2 #3；L03 问 1 #3 | 是（产业链仓菜单路径）。企业表路径未实现，不另计 |
| 8 | 燕大环节父子 `CHILD_OF` | 我方未实现，不写 `CHILD_OF`。燕大能上：`dwd_industry_chain_info.parent_id` → `CHILD_OF`。已签收 L03 写明这是上下级，不是 `depends_on`，不复用 | L03 问 1 #4 | 否 |
| 9 | 政策点 Tag `policy` | 我方能上。DWD `policy_base_info`，VID `pol:{policy_id}`。入口 `demo-algo-ent-analysis` 的 `policy_routes.py`、`polan/graph/ops.py`、`nebula_loader.py`。空间字面量 `demo_gkx_chain`。燕大未实现政策点写图。Java `PolicyGraphController` 只透传，不是写图入口 | L04 问 1 #1 | 是 |
| 10 | M16 `cite` 政策→政策 | 能上其中已是约定格式的行：`pedigree` 里 `上位政策:{pid}` 且 pid 在本批。入口 `policy_graph_intra`，边 `cite`。对不上格式不造点。燕大未实现。技术 `cite` 不并进。自由文本见问 3 | L04 问 1 #2 | 是（仅约定格式） |
| 11 | 服务机构点 Tag `institution` | 我方能上。源表 Demo DWD `svc_org_circle`、ADS `svc_org_card`。VID `institution:{org_id}`，`props` 内 `role=service`。入口 `demo-algo-ent-analysis` 的 `svc_routes.py`、`svcgraph_ops.py` `SVC_NER_ORG`、`svcgraph.py`。燕大没有服务机构 Tag。`lumen-algo-py` 没有这条入口 | L05 问 1 #1 | 是 |
| 12 | M06 专利 `cite` 论文 | 久新库 `ads_patent_cited_paper` 的 `patent_id`、`paper_id` 能对上，方向专利→论文。这是久新表，不是我方 ADS。我方没有写图入口。Tag/Edge 在已签收 L05 是存储设计未写，步骤不能执行。燕大没有专利→论文写边脚本 | L06 §4.1 | 否。计入久新 2 条 |
| 13 | M09 人才 `author_of` 专利 | 久新库 `ads_talent_patent` 的 `talent_id`、`patent_id` 能对上，方向人才→专利。位次列为空。我方没有写图入口，存储设计未写，步骤不能执行。燕大 `invented_by` 是专利→人，源是发明人姓名 | L06 §4.2 | 否。计入久新 2 条 |

L02 问 1 还写了 M21：企业表能写出企业→服务的 `service_provide`，不能当成 M21。该句与 L05 问 2 合成，放在问 2 第 6 行，不在本问再占一行。

`project_from_dwd` 是否写 `participates`，三叶说法不一致，见第 8 节。M17 的「能上」只认两叶都写过的菜单入口 `CHAIN_RE_INDUSTRY_ENTERPRISE` / `_hang`。

---

## 2. 第 2 问 · 缺项要先加工

17 行。只复述子单的加工层：我方 DWD/ADS 映射，或 `gapfill_` 前缀。不建表，不灌数，不写 ODS，不写供应方库，不写久新库。本问全部不是我方已实现。

| # | 对象 | 两端结论与加工建议 | 回指 |
|---|---|---|---|
| 1 | M22 双向 `cooperate` | 不是缺 `enterprise_cooperation`。现码只写有向。加工落在 ADS 映射或建图投影：先定无向边还是两条有向，再投影。未定之前，不把有向 `INSERT` 报成 M22 已上图。燕大没有 `cooperate`，不能从 `INVESTS_IN` 改名补上 | L02 问 2 #1 |
| 2 | 合作、供给、母子缺对端稳定 ID | 三张表分别缺 `partner_org_id`、`related_org_id`、`parent_org_id`，或对端不在 `enterprise_base`。加工落在 DWD 映射，补已有稳定 ID，再交现有 `ops._intra`。不用名称生成 `ent:`。没有第二来源时，才考虑 `gapfill_` 存放人工确认过的 ID 对。燕大子公司边在无稳定 ID 时走唯一名称；境内母子表名待确认 | L02 问 2 #2 |
| 3 | M15 正式上下游 | 正式 Mapping 从父节点派生 `relation_type=parent_child`。`parent_child` 不在白名单，`_depends` 记 `not_in_wave`。建议在 DWD `industry_chain_node_rel` 把上下游写成白名单类型，两端用已有 `node_id`。父子边保持 `parent_child`，不改名充 `depends_on`。没有上游事实时，用 `gapfill_` 只存加工结果再映射进该 DWD 表 | L03 问 2 #1 |
| 4 | 燕大 `downstream_link_code` | 我方不把燕大列迁进生产，按上一行加工。燕大 `DOWNSTREAM_OF` 读该列，列空则无边。未连库，有没有值待确认。不复用为 `depends_on` | L03 问 2 #3 |
| 5 | M18 `participates` 服务机构→环节 | 环节端：`CHAIN_RE_INDUSTRY_SERVICE` 只认 `entity_type=service_institution` 且关系类型在白名单。正式加工只写 `entity_type=enterprise`。SVC 的 `belongs_to` 不是 M18。服务端：没有「服务机构 `org_id` → 环节 `node_id`」的关系行。建议在 DWD `industry_chain_entity_rel` 补服务机构行，`entity_id` 用 `svc_org_circle.org_id`，`node_id` 用已有环节主键。代码方向是服务机构→环节。已签收 CHAIN etl §12 写成「产业/环节 → 对象」，L05 要求汇总以代码 src/dst 为准，不改那份正文。写点 VID 是 `institution:`，链上 C 档只 FETCH `inst:`，L05 不新选前缀。燕大没有服务机构到环节的边；`BELONGS_TO_NODE` 不计入本边 | L03 问 2 #2；L05 问 2 #1 |
| 6 | M21 `service_provide` 服务机构→企业 | 企业端：`enterprise_cooperation` 且 `partner_type=service_org` 时，`ENT_RE_SERVICE` 写出企业→服务，边名 `service_provide`，不能当成 M21。建议 ADS 映射时调换端点，服务机构点归 L05。服务端：没有方向为服务机构→企业的关系列。`SVC_RE_ENTERPRISE` 边名是 `participates`，对端 ID 为空。建议在项目 DWD 或 `gapfill_` 写服务机构 `org_id`、企业 `org_id`，只保留两端都能对上的行，方向保持服务机构→企业。不用 `partner_name` 造 VID。燕大没有 `service_provide` | L02 问 1 #6、问 2 #5；L05 问 2 #2 |
| 7 | M12 `policy_apply_to` 政策→企业 | 企业端：企业侧无表，`ENT_RE_POLICY` 不上图。建议政策域定下政策 ID 之后，在 DWD/ADS 落「政策 ID + `org_id`」。政策端：现行 DWD 没有企业稳定 ID，`related_entities` 不在目标列，装载结果为空。缺的列名待确认。`support` 不改名为 `policy_apply_to`。禁止用企业名称当 VID | L02 问 2 #4；L04 问 2 #2 |
| 8 | M13 `policy_apply_to` 政策→人才 | 政策端：没有人才稳定 ID 列，表名待确认。代码里 `talent` 在 `NOT_IN_WAVE`。人才端：L06 允许前缀内没有政策适用到人才的表和字段。整条边归 L04，L06 不重裁必须或不必须。建议映射到人才 VID，无 ID 不上图。不从人才画像名称推断 | L04 问 2 #3；L06 §5.8 |
| 9 | M14 `policy_apply_to` 政策→科研机构 | 政策端：没有科研机构稳定 ID 列，表名待确认。`publish_organization` 是发文机构名称，不是机构 ID。`apply_to` 终点白名单不是科研机构，`regulate` 不并进。科研机构端：允许前缀内没有适用到机构的表和字段。建议映射「政策 ID → 科研机构稳定 ID」，与发文名称分开 | L04 问 2 #4；L06 §5.8 |
| 10 | M10 `publish` 科研机构→政策 | 政策端：只有名称列 `publish_organization`，缺科研机构稳定 ID，列名待确认。该名称只进 ADS `policy_entity`，不 `INSERT EDGE`。科研机构端：允许前缀没有「机构 ID + 政策 ID」。建议在我方 DWD/ADS 映射科研机构 ID 与政策 ID，方向保持科研机构→政策。政策 Tag 已有，科研机构 Tag 仍是存储设计未写。燕大种子 `POLICY_PUBLISHED_BY` 无抽取脚本，方向相反，不计入已实现 | L04 问 2 #5；L06 §5.7 |
| 11 | M11 `policy_relate` 政策—政策 | 没有关联表，也没有政策—政策外键列。表名待确认。若甲方给稳定 `policy_id` 对，在 DWD/ADS 或 `gapfill_` 做映射后再投影无向 `policy_relate`。现在没有这条 Edge。`cite` 是有向，边名不同，不能当成 `policy_relate`。燕大未实现 | L04 问 2 #1 |
| 12 | M03 人才 `cooperate` 科研机构 | 久新 `ads_talent_institution_cooperation` 现库 0 行。缺的是有行的合作事实。任职不并进合作。建议等对端发布后再映射到我方 DWD/ADS，并排除 `company`。发布前不用 `gapfill_` 编合作行。我方没有写图入口。燕大没有这条合作脚本 | L06 §5.1 |
| 13 | M05 科研机构 `belong` 科研机构 | 允许前缀没有机构—机构隶属表，画像没有上级机构 ID。燕大 `SUBSIDIARY_OF` 按已签收 L03 是企业子公司，不算这条。建议在我方 DWD/ADS 增加下级机构 ID、上级机构 ID；对端没有事实时才考虑 `gapfill_` 登记缺口 | L06 §5.2 |
| 14 | M06 论文 `cite` 论文 | 没有论文—论文引用边表。`cited_by_count` 不是边。燕大论文 `CITES` 源不在这套久新表，目标经常是 DOI 桩，不能写成我方或久新已经能上。建议映射到我方 DWD/ADS（引用论文 ID、被引论文 ID）。不用被引次数反推，也不做正文 NLP | L06 §5.3 |
| 15 | M06 专利 `cite` 专利 | 允许前缀没有专利→专利引用边表。燕大 `patent_cites_relation.py` 的源不是这套久新表。我方没有对应写图。建议映射到我方 DWD/ADS 的专利—专利引用。不从分析指标表猜测 | L06 §5.4 |
| 16 | M07 人才 `participate` 项目 | `ads_talent_project` 现库只有 `funded_output_author`，直接参与行数为 0。资助论文署名不能写成 `participate`。燕大 `HAS_PARTICIPANT`、`LEADS` 方向是项目→人。建议我方 DWD/ADS 只接收已确认的直接参与或负责关系 | L06 §5.5 |
| 17 | M09 人才 `author_of` 论文 | 允许前缀没有人才—论文署名表。`author_count` 不是作者 ID。代表成果表不拿来填 M09。燕大 `AUTHORED_BY` 方向是论文→人。建议映射人才 ID、论文 ID。署名不能靠姓名相等推断 | L06 §5.6 |

---

## 3. 第 3 问 · 不能靠源表、要先用其他技术

8 行。Java 不做 NLP、向量或模型推理。示例脚本只说明核心逻辑，不是已实现，本汇总不改、不执行。

| # | 对象 | 技术 | 我方 | 燕大 | 回指 |
|---|---|---|---|---|---|
| 1 | 名称到 `org_id` 的唯一对齐 | 精确匹配，多命中放弃 | 未实现。缺对端 ID 即 `no_stable_id`。LLM 分支不写边。示例 `KG-7ELEM-LOAD-PATH-L02/unique_name_to_org_id.py` | 已实现。`ExactOrganizationResolver`：底表名称只对应一个 `org_id` 才返回。用于子公司等无稳定 ID 的端点，不写在合作边上。向量索引不创建点、不创建边 | L02 问 3 #1 |
| 2 | M12、M13、M14 正文里的受益对象 | 从正文抽出企业、人才、科研机构，链到已有 VID | 未实现。企业端：`ENT_RE_POLICY` 不读正文。政策端：`_llm_extra` 只返回 `keywords` 与 `cite_pids`。无稳定 ID 不上图。L06 问 3 为 0，没有另写抽取路径 | 未实现 | L02 问 3 #2；L04 问 3 #3 |
| 3 | M16 自由文本谱系 | 大模型抽出本批 `policy_id` | 已实现，仅 `mode=llm`。入口已有：`polan/graph/ops.py` `POLICY_RE_CITE`。只要 JSON 里的 `cite_pids`，且 pid 在本批。无 Key 或失败则回到规则。向量或语义相似去补 `cite`：未实现 | 未实现 | L04 问 3 #1 |
| 4 | M11 `policy_relate` | 政策文本向量或语义相似 | 未实现。已有的政策向量是产业对码，写入 `policy_industry_rel`。已签收 L03 写明产业链—政策不建，不写成 `policy_relate`。示例 `KG-7ELEM-LOAD-PATH-L04/policy_relate_core_example.py` | 未实现。科研文本语义抽取不写政策必须边 | L04 问 3 #2 |
| 5 | M10 发文机构名称 | 机构名对齐到科研机构 VID | 未实现。没有把 `publish_organization` 链到科研机构点的解析。名称相似度禁止在投影层造边。L06 不把名称推断写成必须边路径，问 3 为 0 | 未实现。种子文案写「发布部门对齐后生成」，没有对齐脚本 | L04 问 3 #4；L06 §7 |
| 6 | M15 上下游 | 从正文抽上下游 | 未实现。`mode=llm` 仍然返回 `rule`，不调用模型。`CHAIN_NER_INDUSTRY` 是按表写点。示例 `KG-7ELEM-LOAD-PATH-L03/upstream_from_text.py` | 未实现。`DOWNSTREAM_OF` 只读列 | L03 问 3 #1 |
| 7 | M18 卡面上只有行业名 | 实体链指：名称对已知环节名或环节码。对不上就不上图 | 未实现。`_llm_extra` 禁止编造 VID。示例 `KG-7ELEM-LOAD-PATH-L05/q3_link_core.py` | 未实现。离线 Milvus 做机构消歧，不产出服务机构→环节 | L05 问 3 #1 |
| 8 | M21 正文里的服务关系 | 关系抽取。抽出的是短语，不是 `org_id`。没有稳定 ID 就不上图 | 未实现。`SVC_RE_ENTERPRISE` 不读正文。同一示例脚本 | 未实现 | L05 问 3 #2 |

L06 第 3 问是 0 条，无示例脚本。相似度表、发明人姓名匹配、分析表里的人名，L06 都不写成必须边路径。论文引用、机构上下级、直接参与项目归第 2 问。

---

## 4. 待确认

25 条。材料里没有的，子单已写「待确认」，汇总不闭合。

| # | 待确认 | 回指 |
|---|---|---|
| 1 | M22 双向在 Nebula 里落成无向边，还是一对有向边。两份 demo 代码都没有无向 `cooperate` 的 `CREATE EDGE` | L02 待确认 1 |
| 2 | `enterprise_industry_chain.node_id` 是否就是 `segment:{node_id}`。企业仓同时候选 `chain:`、`segment:`、`chn:` | L02 待确认 2 |
| 3 | 燕大 `dwd_org_industry_chain_dtl.antitypic` 与我方 `enterprise_base.org_id` 是不是同一套标识 | L02 待确认 3 |
| 4 | 燕大境内母子公司源表名。已打开的机构关系 spec 只绑境外表 `dwd_forg_subsidiary_info` | L02 待确认 4 |
| 5 | 服务机构 VID 用 `inst:` 还是 `institution:`。L02 列为待确认。L05 写沿用已签收 L05、本叶不新开、不新选。汇总保留这一条，并在第 8 节标口径冲突 | L02 待确认 5；L05 §1 末段 |
| 6 | L02 消费行表名。L03 第 1 节写 A02、A24、A27；第 4 节待确认写 A02、A24、A26、A27。两句都保留，见第 8 节。条数仍按 L03 的 1 条，不因多一个编号加条 | L03 §1 末段；L03 §4 待确认 1 |
| 7 | `parent_child` 能不能写成 `depends_on`。L03 不并。已签收 L03 把上下级和上下游分开 | L03 待确认 2 |
| 8 | 燕大 `downstream_link_code` 有没有值。未连库 | L03 待确认 3 |
| 9 | 我方 `industry_chain_entity_rel` 里有没有 `entity_type=service_institution` 行。L03 与 L05 是同一问，计 1 条 | L03 待确认 4；L05 待确认 1 |
| 10 | M15、M17、M18 的基数。已签收 L03 写待确认。L05 的 M18 基数含在本条，不另计 | L03 待确认 5；L05 待确认 3 |
| 11 | 燕大 `dwd_org_industry_chain_dtl` 有没有行。未签收 L04 曾写本地无此表，当前燕大代码仍读它 | L03 待确认 6 |
| 12 | M11 `policy_relate` 的表名 | L04 问 2 #1 |
| 13 | M12 的企业稳定 ID 列或表名 | L04 问 2 #2 |
| 14 | M13 的人才稳定 ID 列或表名 | L04 问 2 #3 |
| 15 | M14 的科研机构稳定 ID 列或表名 | L04 问 2 #4 |
| 16 | M10 的科研机构稳定 ID 列名 | L04 问 2 #5 |
| 17 | `enterprise_cooperation` 中 `partner_type=service_org` 的 `partner_org_id` 是否有值。即便有值，方向仍是企业→服务，不能直接当成 M21 | L05 待确认 2 |
| 18 | M21 基数。已签收 L03 写待确认 | L05 待确认 4 |
| 19 | A21 服务机构互相 `participates` 的方向。已签收 L03 写待确认。本汇总不补这条边 | L05 待确认 5 |
| 20 | M01：`ads_talent_collaborator` 归 M01、归 M20，还是两条都还不算。确认前不加工成边 | L06 §6.1 |
| 21 | M20：与 M01 同一张表。L06 禁止并进，故 M20 仍单列待确认 | L06 §6.1 |
| 22 | M02：非 `company` 里哪些 `institution_type_id` 算科研机构；确认之后 `ads_institution_collaboration_yearly` 归 M02 还是 M19 | L06 §6.2 |
| 23 | M19：与 M02 同一张表。L06 禁止并进，故 M19 仍单列待确认 | L06 §6.2 |
| 24 | M04：科研机构类型集合。确认前，经历表只能说明人与机构 ID 对得上、企业行可以排除 | L06 §6.3 |
| 25 | M08：同一套科研机构类型。确认前，不把 17426 行负责/参与隶属写成已经能上，也不把资助论文署名写成参与 | L06 §6.4 |

L04 写政策边基数沿用已签收 L03、下面不单列。汇总不加政策基数新条。L06 的待确认 6 条不计入「久新能对上但我方没有写图」。

---

## 5. 燕大有代码、我方没有

12 条。都不选燕大 space 作生产，都不复用为必须边的生产放行。

| # | 对照 | 子单怎么写 | 回指 |
|---|---|---|---|
| 1 | `SUBSIDIARY_OF` | 子公司→母公司。我方写的是 `parent_sub` 母→子。不复用 | L02 计数；L02 问 1 #3 |
| 2 | `BELONGS_TO_NODE` | Organization→IndustryNode，归属。不并进 M17，也不计入 M18。L02 与 L03 各计 1，汇总计 1。L05 明确不计入 | L02 计数；L03 计数；L05 §4 末段 |
| 3 | `ExactOrganizationResolver` | 唯一名称对齐，已实现，不写合作边。我方未实现。向量索引不计入 | L02 问 3 #1 |
| 4 | `CHILD_OF` | 环节父子。我方未实现。不并进 `depends_on` | L03 问 1 #4 |
| 5 | `DOWNSTREAM_OF` | 读 `downstream_link_code`。有无值待确认。不并进 `depends_on` | L03 问 2 #3 |
| 6 | M01 `COAUTHOR_WITH` | 只覆盖合著，不是 M01 全量 | L06 计数；§3.2 |
| 7 | M20 同一份合著脚本 | L06 与 M01 点名同一脚本，仍把 M20 计入 7 条。未覆盖 `talent_coop` 全量。汇总不把 7 改成 6 | L06 计数 |
| 8 | M04 `AFFILIATED_WITH` | 人→机构的任职对照。Organization 不单是科研机构。不是 M03 | L06 §3.2 |
| 9 | M06 论文 `CITES`、专利 `CITES` | L06 计为 M06 一条。没有专利→论文。论文目标经常是 DOI 桩 | L06 计数；§4.1、§5.3、§5.4 |
| 10 | M07 `HAS_PARTICIPANT`、`LEADS` | L06 计为 M07 一条。方向是项目→人 | L06 §3.2、§5.5 |
| 11 | M08 `FUNDED_BY` | 方向是项目→机构。资助不是已签收 L03 写的参与。目录里的机构参与项目没有写边脚本 | L06 §3.2、§6.4 |
| 12 | M09 `AUTHORED_BY`、`INVENTED_BY` | L06 计为 M09 一条。方向与必须边相反。专利脚本靠姓名，不是人才 ID 对专利 ID | L06 §3.2、§4.2、§5.6 |

L04：燕大有可执行写图或读图、我方没有，为 0。Schema 种子 `POLICY_PUBLISHED_BY`、`POLICY_RELATED_FIELD`、`POLICY_RELATED_CHAIN_NODE` 无抽取脚本，不计入。  
L05：燕大有代码、我方没有，为 0。`Organization` 写点与 `BELONGS_TO_NODE` 都不是本叶必须三元组。  
L06 另写明：M02、M19、M03、M10 燕大侧也没有对应写边脚本。这四条不放进上表。

---

## 6. 久新现库能对上、我方没有写图

2 条，与第 1 问第 12、13 行相同。

| # | 对象 | 久新表与键 | 我方 |
|---|---|---|---|
| 1 | M06 专利 `cite` 论文 | `ads_patent_cited_paper`：`patent_id`、`paper_id` | 没有写图函数。步骤不能执行 |
| 2 | M09 人才 `author_of` 专利 | `ads_talent_patent`：`talent_id`、`patent_id` | 没有写图函数。步骤不能执行 |

待确认的 M01、M20、M02、M19、M04、M08 不计入。第 8 节现库多出来的分析表，L06 不升成第 1 问，汇总也不升。`ads_*` 不是我方 ADS。`institution_type_id=company` 是企业，不是科研机构。探查日期与快照日的差别以 L06 第 8、9 节为准。账号、主机、端口、连接串不写入本文。

---

## 7. 不建、不计入

- 服务机构互相 `participates`。L05 不补。A21 方向仍待确认，不因此建边。
- 企业—科研机构、企业—技术、企业—人才。`research_coop`、`talent_coop`、`produces` 以及企业挂边上的这些字符串，对不上 M19、M20，也不建这三类边。
- `technology` 技术点不计入七要素「技术」。ENT 的 Tag `technology`、VID 前缀 `tech:` 对不上论文、专利、项目。
- `invest` / 燕大 `INVESTS_IN`、`ACQUIRES` 不进必须。
- 产业链到科研机构、技术、人才不建。`chain` 不是环节。产业链—政策不建。
- 服务机构—技术、人才、政策、科研机构不建。
- 政策域 `cite` 不并进技术 M16 以外的技术引用；技术 `cite` 不并进政策 M16。
- 燕大边名目录里没有转换脚本的，不算已实现。
- `lumen-algo-py` 及其 `vendor/entan-py` 不列为我方写图入口。未签收 `SYSINT-SCHEME-07-L03` 把入口写成 lumen 的句子，L02、L05 不采纳。

---

## 8. 冲突与归位

不改子单。下面只标明汇总怎么并列。

### 8.1 冲突 4 处

1. **`BELONGS_TO_NODE` 的燕大条数。** L02 正文计入「燕大有、我方没有」3 条中的 1 条。L03 正文同样计入自己的 3 条。L05 正文写明不计入。三叶对这条边的定性一致：归属，不并进 M17，也不当 M18。冲突在计数。汇总计 1。叶相加的 13 不改子单。
2. **服务机构 VID 算不算本批新增待确认。** L02 正文列为待确认第 5 条。L05 正文写「不新开待确认」，沿用已签收 L05，现网 `institution:` 与目标 `inst:` 都写了，没有收成一条，本叶不新选。汇总保留 L02 这一条，不把 L05 的「不新开」再加一条，也不删 L02 的第 5 条。
3. **L03 正文里消费行编号不一致。** 第 1 节写「L02 消费行 A02、A24、A27 的表名写的是待确认」。第 4 节待确认第 1 条写「A02、A24、A26、A27」。条数都是待确认 6 条里的 1 条。汇总两句并列，不删 A26，也不把第 1 节补成四个编号。
4. **`nebula_project.py` 是否写 `participates`。** L02：对企业这类行只计数跳过（`entity_rel_fetch_only`），该函数不写 `participates`。L03：`project_from_dwd` 仍能写点边，并会新建企业、机构点；测试断言灌数脚本不再调用它；菜单入口是 `/chain/graph/*`。L05：同一函数会新建 Tag `institution` 的点，VID 前缀 `inst:`，再写 `participates`。汇总不选第三套行为。M17「能上」只认菜单入口 `CHAIN_RE_INDUSTRY_ENTERPRISE` / `_hang`。

企业菜单与服务机构 `ner` 的 `dry_run` 默认值，两叶写的是两个入口，汇总不并成一条规则。

### 8.2 归位 3 处

结论没有改，只避免同一条边占两行、两套归类。

1. **M21** 放到问 2 第 6 行。L02 问 1 第 6 条写「会写反向边，不能当成 M21」，问 2 第 5 条写要调换端点。L05 只放在问 2。合成一行后，问 1 不再单列。
2. **M17 的企业表路径** 写在问 1 第 7 行。L02 问 2 第 3 条（企业表产不出 `participates`）与 L02 问 1 第 5 条、L03 问 1 第 3 条是同一条边的两端。问 2 不再单列。
3. **M18 方向** 按 L05 正文：代码 src 是服务机构，dst 是环节。已签收 CHAIN etl §12 的相反文字不改。

---

## 9. 我方入口（只抄子单）

| 域 | 仓 | 子单点名的入口 |
|---|---|---|
| 企业点与企业间边 | `demo-algo-ent-analysis` | `api/entan_graph_routes.py`，`entan/graph/ops.py`，`entan/graph/nebula_loader.py` |
| 企业→环节 `participates`、环节、`depends_on` | `demo-algo-science` | `api/main.py` 的 `/v1/chain/graph/*`、`/internal/chain/graph/*`；`chainan/graph/graph_ops.py`；`nebula_schema.py`；`nebula_project.py` 的白名单。M17 的写入认 `graph_ops._hang` |
| 政策点、政策 `cite` | `demo-algo-ent-analysis` | `api/policy_routes.py`，`polan/graph/ops.py`，`polan/graph/nebula_loader.py` |
| 服务机构点 | `demo-algo-ent-analysis` | `api/svc_routes.py`，`entan/svcgraph_ops.py`，`entan/svcgraph.py` |
| 服务机构→环节的链上路径 | `demo-algo-science` | `CHAIN_RE_INDUSTRY_SERVICE`。行未加工，见问 2 |
| 科研机构、人才、技术 | 两个 demo 仓 | L06：两个仓都没有论文、专利、项目写图。`nebula_loader.py` 只写企业点 |

燕大对照一律在 `yanda/tech-kg-api`，只作已实现对照。  
space 字面量以子单所写为准：我方代码写 `demo_gkx_chain`。L02 写明源码字面量不是集群已发布的证据。汇总不把字面量说成已发布。
