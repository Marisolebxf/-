# KG-7ELEM-LOAD-PATH-L04 · 政策上图路径

> 日期：2026-10-30  
> 任务：`KG-7ELEM-LOAD-PATH-L04`  
> 必须边只认已签收 `KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md`：政策点，以及 M16 `cite`、M11 `policy_relate`、M12–M14 `policy_apply_to`、M10 `publish`。不新增、不删除必须边。技术 `cite` 不并进 M16。  
> 我方写图入口：`repos/demo-algo-ent-analysis`。`lumen-algo-py` 的 `lumen_algo_service`、`lumen_common` 没有政策写图。`lumen-algo-py/vendor/entan-py/polan/graph/` 有同名文件，本叶不把它写成入口。  
> 燕大只对照 `yanda/tech-kg-api`（2026-10-30 工作区）。燕大代码不写成生产放行。  
> 未签收、只作索引：`对接文档/智谱/SYSINT-SCHEME-07-L03-算法中台上图台账.md`、`SYSINT-SCHEME-07-L06-算法中台入图流程.md`、`SYSINT-SCHEME-07-L04-燕大七要素上图对照.md`。已实现以仓库里能打开的代码为准。L03 第七章写「政策无 Nebula 写图」，与现行 demo 代码不符，不采。

七要素端点里，本叶写政策点。`publish` 的科研机构一端归 `KG-7ELEM-LOAD-PATH-L06`。`policy_apply_to` 到企业归 L02，到人才或科研机构归 L06。本叶写政策这一端的来源。

基数沿用 L03，全部待确认，下面不单列。

代码里还有 `support`、`apply_to`、`regulate`，以及 `policy_industry_rel` 挂产业。L03 写明产业链—政策不建。这三条边名对不上本叶必须边，不升成必须边，也不从必须表删行。

---

## 1. 关系库现在就能上

源是现行 DWD `policy_base_info`（结构见 `data/data-design/storage/POLICY/stores/mysql/dwd.md`）。库名 demo 为 `demo_gkxlumenx_dwd`，产线同表换 `gkxlumenx_dwd`。Java 只透传，不写 nGQL、不做 NLP：`repos/demo-svc-platform/gkx-innov/src/main/java/com/topcomm/gkx/innov/policy/PolicyGraphController.java`。

| # | 对象 | 我方 | 燕大 |
|---|---|---|---|
| 1 | 政策点 Tag `policy` | 能上。源表 DWD `policy_base_info`。字段 `policy_id`、`title`；属性进 `props` 的是 `rank`、`region`、`publish_year`、`policy_type`。Tag `policy`，VID `pol:{policy_id}`，列 `name string`、`weight double`、`props string`（L05 已签收；代码 `POLICY_DDL` 同此）。入口：`api/policy_routes.py` `policy_graph_ner` → `polan/graph/ops.py` `_ner` → `polan/graph/nebula_loader.py` `write_policy_graph`。步骤：`POST /internal/policy/graph/ner`（`op_id=POLICY_NER_POLICY`）读 `is_deleted=0` 的行，VID 长度 ≤80 则写 ADS `policy_graph_node`，再 `CREATE TAG IF NOT EXISTS policy` 与 `INSERT VERTEX policy`。空间由 `polan/common/nebula.py` 锁在 `demo_gkx_chain`。读图：`policy_graph` → `polan/graph/nebula_query.py` `subgraph`。 | 未实现。无政策抽取脚本，无 `INSERT VERTEX` 政策点。`backend/service/schema_catalog_seed.py` 只在 Schema 管理表登记名字 `Policy`，`backend/script/init_schema_management.py` 写入管理库，不写图。`backend/db_model/policy.py` 是贴源 ORM，本叶不用贴源库当上图源。无政策读图函数。 |
| 2 | M16 `cite` 政策→政策 | 能上其中已是约定格式的行。源字段 `pedigree`。`polan/graph/entity.py` `parse_cite_pid` 只认分号切开后、以 `上位政策:` 开头、且 pid 在本批 `policy_id` 集合内的 token。Edge `cite`，方向政策→政策，列 `weight double`、`props string`（L05 按 etl §4；`stores/nebula.md` 另一套列以 etl 为准）。入口：`policy_graph_intra` → `ops.py` `_cite` / `_add_cite` → `write_policy_graph` 的 `INSERT EDGE cite`。步骤：`POST /internal/policy/graph/intra`，`relation_whitelist=["cite"]`。对不上格式的 token 记 `empty_field`，本批没有的 pid 记 `no_stable_id`，不造悬挂点。 | 未实现。种子里没有政策—政策 `cite`。论文/专利 `CITES` 是技术引用，不并进 M16。 |

本问 2 条。待确认 0 条。燕大有可执行写图或读图、我方没有：0 条。

---

## 2. 缺项要先加工

只写方法。不建表，不灌数。不写 ODS，不写供应方库。建议层是 DWD/ADS 映射或 `gapfill_` 前缀。

| # | 必须边 | 缺什么 | 建议 | 我方代码 | 燕大 |
|---|---|---|---|---|---|
| 1 | M11 `policy_relate` 政策—政策，无向 | 没有关联表，也没有政策—政策外键列。表名待确认。L02 Q23 只写「政策关联网络」，没有表名。 | 若甲方给的是稳定 `policy_id` 对，在 DWD 或 ADS 做政策—政策映射（或 `gapfill_` 对照表），列至少两端 `policy_id`。映射完成后再投影无向 `policy_relate`。现在没有这条 Edge。 | 未实现。投影白名单只有 `support`、`apply_to`、`regulate`、`cite`（`nebula_loader.py` `EDGES`）。`cite` 是有向，边名不同，不能当成 `policy_relate`。 | 未实现。无同名边，无抽取脚本。 |
| 2 | M12 `policy_apply_to` 政策→企业 | 现行 DWD 目标列没有企业稳定 ID。`dwd.md` 写明 `related_entities` 不在目标列。`ops.py` `_load_pols` 的 SELECT 也没有这列。`iter_related_slots` 读 `related_entities.enterprise`，当前装载结果是空。缺的是「政策 `policy_id` → 企业 `org_id` / `enterprise_code`」这一列或对照表，列名待确认。企业点本身归 L02。 | DWD/ADS 映射或 `gapfill_`：政策 ID 对上 L02 已有的企业 VID 规则 `ent:`。有稳定 ID 且对端点已在图上，再写 Edge `policy_apply_to`。禁止用企业名称当 VID。 | 边名未实现。同文件把企业挂在 `support` 上（`entity.py` `HANG_ON`），且企业行要 `related_entities` 里的稳定 ID。L05 写明企业 `apply_to` 本波不上图。`support` 不改名为 `policy_apply_to`。 | 未实现。无政策→企业抽取。 |
| 3 | M13 `policy_apply_to` 政策→人才 | 没有人才稳定 ID 列，表名待确认。人才 Tag 无政策存储域（L05）。人才一端归 L06。 | 同上，映射到 L06 人才 VID。无 ID 不上图。 | 未实现。`talent` 在 `NOT_IN_WAVE`，hang 直接 `not_in_wave`。代码不写 `policy_apply_to`。 | 未实现。 |
| 4 | M14 `policy_apply_to` 政策→科研机构 | 没有科研机构稳定 ID 列，表名待确认。`publish_organization` 是发文机构名称，不是机构 ID。科研机构一端归 L06。 | 映射「政策 ID → 科研机构稳定 ID」，与发文名称分开。有 ID 再写 `policy_apply_to`。 | 未实现。`apply_to` 的终点白名单是 `industry` 与 `service`，不是科研机构。`regulate` 挂 `org`→`inst:`，边名和角色都不同，不并进 M14。 | 未实现。种子 `POLICY_RELATED_FIELD`、`POLICY_RELATED_CHAIN_NODE` 终点是领域和产业链节点，不在本叶。 |
| 5 | M10 `publish` 科研机构→政策 | 政策侧只有名称列 `publish_organization`。缺科研机构稳定 ID 列，列名待确认。Edge `publish` 存储设计未写（L05：无对应存储域）。科研机构一端归 L06。 | 名称先留在政策属性。要上图，先有「科研机构稳定 ID → `policy_id`」的 DWD/ADS 或 `gapfill_` 映射，方向保持科研机构→政策。 | 未实现。`publish_organization` 只进 ADS `policy_entity`（`entity.py` `iter_core_ner`，类型 `org`），不 `INSERT EDGE`。 | 未实现。种子有 `POLICY_PUBLISHED_BY`，方向是政策→机构，与 M10 相反，且没有抽取脚本。不把种子写成已上图。 |

本问 5 条。待确认 5 条（M11 表名，M12、M13、M14、M10 的稳定 ID 列或表名）。燕大有可执行写图、我方没有：0 条。

---

## 3. 不能靠源表、要先用其他技术

Java 不做 NLP、向量或模型推理。没有写图代码的写成未实现。示例脚本只说明判定，不是已实现：`KG-7ELEM-LOAD-PATH-L04/policy_relate_core_example.py`。不接库，不加依赖，本叶不执行。

| # | 对象 | 技术 | 我方 | 燕大 | 建议的 Python 入口 |
|---|---|---|---|---|---|
| 1 | M16 自由文本谱系 | 大模型抽出本批 `policy_id`。`pedigree` 列注释是「引用政策原文」。多数行不是 `上位政策:{pid}`。 | 已实现，仅 `mode=llm`。`ops.py` `_llm_extra` 把标题、摘要、谱系交给 `entan.common.llm_client.OpenAICompatibleClient`，只要 JSON 里的 `cite_pids`，且 pid 必须在本批。无 Key 或失败则 `llm_fallback`，回到规则。不按名称造边。向量或语义相似未实现：没有政策—政策向量检索去补 `cite`。 | 未实现。 | 已有：`polan/graph/ops.py` `execute`，`op_id=POLICY_RE_CITE`，`mode=llm`。不新造入口。 |
| 2 | M11 `policy_relate` | 政策文本向量或语义相似（没有外键时）。 | 未实现。`polan/industry_embed.py` 与 `polan/industry_enrich.py` 已有向量：政策标题、关键词、正文对产业链锚点，余弦分写入 `policy_industry_rel`。这是产业对码，L03 产业链—政策不建，不写成 `policy_relate`。`demo-algo-science` 无政策向量写图（机构名 `difflib`、资讯 SimHash 都不写政策边）。 | 未实现。`backend/script/semantic_research_entity_extract.py` 是科研文本语义抽取，不写政策必须边，也不写 Nebula 政策点。 | 若以后做，放在 `demo-algo-ent-analysis` 的 Python，与 `ops.execute` 的 B 档分开，避免和 `cite` 混成一条边。当前没有该函数。 |
| 3 | M12、M13、M14 正文里的受益对象 | 从正文抽出企业、人才、科研机构并链到已有 VID。 | 未实现。`_llm_extra` 只返回 `keywords` 与 `cite_pids`。设计稿 pipeline-to-nebula §15 L2 是升级清单，代码没有这条抽取。无稳定 ID 不上图。企业端归 L02，人才与科研机构归 L06。 | 未实现。 | 建议落在 `polan/graph/ops.py` 的 hang 路径旁，新函数尚未写。Java 只转发。 |
| 4 | M10 发文机构名称 | 机构名对齐到科研机构 VID。 | 未实现。没有把 `publish_organization` 链到 `inst:` 或科研机构点的解析。名称相似度禁止在投影层造边（etl §9、§13.3）。 | 未实现。种子文案写「发布部门对齐后生成」，没有对齐脚本。 | 建议落在 Python，科研机构 VID 规则等 L06。当前没有该函数。 |

本问 4 条。其中向量或语义相似：对 M11 以及用向量补 M16，都是未实现。M16 的大模型 `cite_pids` 是已实现。待确认 0 条（表名待确认已计在第 2 问）。燕大有可执行代码、我方没有：0 条。

---

## 4. 计数

| 问 | 条数 | 其中待确认 | 燕大有可执行写图或读图、我方没有 |
|---|---:|---:|---:|
| 1 关系库现在就能上 | 2 | 0 | 0 |
| 2 缺项要先加工 | 5 | 5 | 0 |
| 3 其他技术 | 4 | 0 | 0 |
| 合计 | 11 | 5 | 0 |

燕大 Schema 种子另有 3 个关系名（`POLICY_PUBLISHED_BY`、`POLICY_RELATED_FIELD`、`POLICY_RELATED_CHAIN_NODE`），无抽取脚本，不计入上表「已实现」，也不计入「燕大独有可执行」条数。后两条终点不是本叶七要素对。

向量或语义相似：未实现（产业对码向量不计入本叶必须边）。
