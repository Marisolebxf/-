# KG-7ELEM-LOAD-PATH-L06 · 科研机构、人才、技术

> 日期：2026-10-30  
> 任务：`KG-7ELEM-LOAD-PATH-L06`  
> 必须边只认已签收 `KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md`。schema 只认已签收 `KG-7ELEM-BUILD-REQ-L05-建图schema与存储设计缺项.md`。  
> 久新原文只认 2026-10-22 两份快照（schema 5.11.0）。表清单、字段清单是我方整理，不是久新原文。  
> 现库只读探查日期：2026-10-30。探查连上。下文行数是这一天的 `COUNT`，不是只抄 10-22 清单。  
> 久新 `ads_*` 是对端库里的表，不是我方 ADS。`institution_type_id=company` 是企业，不是科研机构。`ads_technology_*` 不是七要素「技术」。  
> 三列：我方、燕大、久新。久新库有数不等于我方已经能上图。

## 0. 计数

按可单独判定的关系事实计。一条必须边里论文、专利、项目落点不同的，拆开计。M13、M14 只计本叶这一端。

| 项 | 条数 | 是哪些 |
|---|---:|---|
| 第 1 问 | 2 | M06 专利→论文；M09 人才→专利。只表示久新键对得上。我方没有写图入口，Tag/Edge 在 L05 是存储设计未写 |
| 第 2 问 | 9 | M03；M05；M06 论文→论文；M06 专利→专利；M07；M09 人才→论文；M10 科研机构端；M13 人才端；M14 科研机构端 |
| 第 3 问 | 0 | 没有一条必须边必须先做 NLP、向量或模型。无示例脚本 |
| 待确认 | 6 | M01、M20 共一张人才合作表；M02、M19 共一张机构合作年表；M04 隶属；M08 项目角色行。都卡在「算不算这条必须边」或「哪些类型算科研机构」 |
| 燕大有写边代码、我方没有该必须边写图入口 | 7 | M01、M04、M06、M07、M08、M09、M20。M01 与 M20 是同一份合著脚本，语义未覆盖合作全量 |
| 久新现库能对上字段、我方没有写图代码 | 2 | 同上第 1 问两条。待确认的 6 条不计入 |

我方第 1 问是 0 条：没有一条是我方现在就能上。

## 1. 本叶必须边

不新增、不删除。基数在 L03 全部是待确认，这里不补基数。

| 编号 | 起点 | 关系 | 终点 | 方向 | L03 要点 |
|---|---|---|---|---|---|
| M01 | 人才 | cooperate | 人才 | 无向 | 不并进 M20。合著只是对照，不是这条的全部 |
| M02 | 科研机构 | cooperate | 科研机构 | 无向 | 不并进 M19 |
| M03 | 人才 | cooperate | 科研机构 | 无向 | 任职不是合作 |
| M04 | 人才 | belong | 科研机构 | 有向 | 对照任职，机构不单是科研机构 |
| M05 | 科研机构 | belong | 科研机构 | 有向 | 企业子公司不是这条 |
| M06 | 技术 | cite | 技术 | 有向 | 消费来源含论文→论文、专利→论文、专利→专利 |
| M07 | 人才 | participate | 技术 | 有向 | 消费来源是人员参与项目。方向不是项目指向人 |
| M08 | 科研机构 | participate | 技术 | 有向 | 消费来源是机构参与项目。方向不是项目指向机构 |
| M09 | 人才 | author_of | 技术 | 有向 | 消费来源是作者与论文、作者与专利。方向不是成果指向人 |
| M10 | 科研机构 | publish | 政策 | 有向 | 本叶只写科研机构端。政策端归 L04 |
| M19 | 科研机构 | research_coop | 科研机构 | 双向 | 不并进 M02 |
| M20 | 人才 | talent_coop | 人才 | 双向 | 不并进 M01。合著对照不覆盖这条 |

M13 政策 `policy_apply_to` 人才、M14 政策 `policy_apply_to` 科研机构：整条边归 L04。本叶只查允许前缀里有没有这一端的表和字段，不重裁必须或不必须。

不建：企业—科研机构、企业—技术、企业—人才；产业链环节到这三类；服务机构互相 `participates`。技术点、学科、主题、研究问题不建 Tag，不拿来填 M06–M09。

## 2. schema（只认 L05）

科研机构、技术、人才三个 Tag：名称、VID、属性都是「存储设计未写」，缺项类是「无对应存储域」。

M01–M10、M19、M20，以及 M13、M14 的人才端、科研机构端：边的属性是「存储设计未写」，缺项类是「无对应存储域」。M10 的终点 Tag 只有政策一端是 `policy`，起点仍无科研机构域。

同名但不能挪用：

- 企业域 `cooperate` 是企业→企业且有向，不是 M01、M02。
- 企业域 `research_coop` 是企业→科研机构且有向，不是 M19。
- 企业域 `talent_coop` 是企业→人才且有向，不是 M20。
- 政策域 `cite` 是政策→政策，不是 M06。
- 产业链 `participates` 不是 M07、M08。
- ENT 的 Tag `technology` 是技术点，VID 例是 `tech:` 加名称，对不上论文、专利、项目。
- `institution` 不拆成科研机构专属 Tag。服务机构和科研机构在产业链存储里写在同一个 Tag 上。

本叶不另造存储域，不给这些边起一套新的 Tag 名。

## 3. 三列入口

### 3.1 我方

写图入口在算法中台 demo 仓，对照的是当前工作区代码。`SYSINT-SCHEME-07-L03`、`SYSINT-SCHEME-07-L06` 未签收，只作索引。和代码不一致时以代码为准。

`demo-algo-ent-analysis/entan/graph/nebula_loader.py`：文件头写明只补企业 Tag，不新建 `industry` / `research` / `talent` / `service` / `chain_node` / `technology`。`_load_nodes` 只 `INSERT VERTEX enterprise`。边名列表里虽有 `research_coop`、`talent_coop`，没有对应的科研机构点、人才点写入。

`demo-algo-ent-analysis/entan/graph/ops.py`：`ENT_RE_RESEARCH` 的边名是 `research_coop`，`ENT_RE_TALENT` 的边名是 `talent_coop`，`ENT_RE_TECH` 的边名是 `produces`、对端类型是 `technology`。取数来自 `enterprise_cooperation`，起点是企业 `ent:`。对端要 `FETCH` 命中图上已有的 `inst:` / `institution:` 或 `talent:`，否则记 `no_stable_id`，不用名称猜 VID。`ENT_RE_TECH` 的取数函数直接返回空列表。`technology` 只接受已经带 `tech:` 的稳定 ID。这是技术点前缀，不是论文、专利、项目。

`demo-algo-ent-analysis/entan/yiji_sim/facts.py` 的合作方映射与上面一致：科研院所、高校走到 `research` + `research_coop`，人才走到 `talent` + `talent_coop`，另一端类型来自企业合作方，不是科研机构—科研机构，也不是人才—人才。

`demo-algo-ent-analysis/entan/graph/nebula_query.py` 的 `subgraph` 从 `ent:` 读邻域，是企业读图，不是这三类的写图入口。

`demo-algo-science/chainan/graph/nebula_schema.py` 的 Tag 只有 `chain`、`segment`、`enterprise`、`institution`。边只有 `belongs_to`、`participates`、`supplies`、`depends_on`。没有论文、专利、项目、人才、科研机构专属 Tag。`chainan/graph/nebula_project.py` 写明企业点和机构点不在这个文件 `INSERT`。

两个仓里没有论文、专利、项目的 `INSERT VERTEX` / `INSERT EDGE`。政策点在 `polan/graph/nebula_loader.py`，服务机构点在 `entan/svcgraph.py`，都不是本叶这三类。

结论：科研机构、人才、七要素「技术」没有独立写图入口。企业挂边上的 `research_coop`、`talent_coop` 字符串对不上 M19、M20。

未签收台账 `SYSINT-SCHEME-07-L03` 仍把通用灌图写成含 `research`、`talent` Tag 的旧 loader 行号。当前 `nebula_loader.py` 已经不建这两个 Tag。本叶不沿用那段当已实现。

### 3.2 燕大

只读 `yanda/tech-kg-api`。写边以 `backend/script/relation_extractors_one_relation/` 里的转换为准。`backend/service/schema_catalog_seed.py` 的 `FACT_RELATION_SPECS` 是边名目录，没有对应转换脚本的不算已实现。读图有按边名查询的服务，没有按本叶必须边各做一个上图管道。

| 对照 | 写图 | 方向与源 | 读图 | 对本叶必须边 |
|---|---|---|---|---|
| 合著 | `coauthor_with_relation.py` | `dwd_scholar_coauthor` 的 `scholar_id`、`co_scholar_id` → `COAUTHOR_WITH`，Person→Person，主键抽取 | `backend/service/expert_direct_relation.py` 按这个边名查 | 只覆盖合著。不是 M01 全量，也不是 M20 |
| 任职 | `affiliated_with_relation.py` | `dwd_scholar` → `AFFILIATED_WITH`，Person→Organization。有机构 ID 则直接连，否则机构名做桩 VID | 测试与任职关系服务读这个边名 | 接近 M04 的对照，Organization 不单是科研机构。不是 M03 |
| 论文作者 | `authored_by_relation.py` | `dwd_zh_author`、`dwd_en_author` → `AUTHORED_BY`，Paper→Person | 专家关系服务在代表成果上读这个边名 | 方向与 M09 相反 |
| 专利发明人 | `invented_by_relation.py` | `dwd_patent` 发明人姓名对图内 Person。未唯一命中则挂起待人裁。文件写明 Milvus 不在本脚本 | 无单独的本叶读入口 | 方向与 M09 相反。源表没有人才—专利主键，才做姓名匹配 |
| 项目参与 | `has_participant_relation.py` | `dwd_zh_project`、`dwd_en_project` 的参与人姓名 → `HAS_PARTICIPANT`，Project→Person | 无本叶专用读入口 | 方向与 M07 相反 |
| 项目负责 | `leads_relation.py` | 同上，主持人 → `LEADS`，Project→Person | 无本叶专用读入口 | 方向与 M07 相反。L03 把它和参与放在同一条对照里 |
| 项目资助 | `funded_by_relation.py` | 资助机构名 → `FUNDED_BY`，Project→Organization。参与单位只记报告，不写 `PARTICIPATES_IN` | 无本叶专用读入口 | 方向与 M08 相反。资助不是 L03 写的参与 |
| 论文引用 | `paper_cites_relation.py` | 中英文 reference 表 → `CITES`，论文指向 DOI 桩，confidence 0.5 | 无本叶专用读入口 | 只对照 M06 的论文→论文，端点经常不是已落地的论文点 |
| 专利引用 | `patent_cites_relation.py` | `dwd_patent_cited` → `CITES`，专利→专利，标识符要唯一命中 | 无本叶专用读入口 | 只对照 M06 的专利→专利。没有专利→论文 |
| 子公司 | `subsidiary_of_relation.py` | 机构域子公司关系 → `SUBSIDIARY_OF` | 无本叶专用读入口 | L03 写明这是企业子公司，不算 M05 |

目录里有、`backend/script` 下没有写边脚本的，不算已实现：`PUBLISH`（目录写成专家→论文，不是科研机构→政策）、`PARTICIPATE_IN_PROJECT`、`INVENT_PATENT`、`PATENT_CITES` 这个名字本身。专利引用的已实现边名是 `CITES`，在专利脚本里。

没有科研机构—科研机构合作的写边脚本，所以 M02、M19 燕大侧也没有。没有人才—科研机构合作脚本，M03 没有。没有科研机构发布政策的脚本，M10 没有。

### 3.3 久新

允许前缀：`ads_talent_*`、`ads_institution_*`、`ads_paper_*`、`ads_patent_*`、`ads_project_*`。

2026-10-22 快照与我方 `调研/表清单.csv` 已列、并且 2026-10-30 现库 `SHOW TABLES` 仍在的关系表，见第 4–6 节。现库多出来、快照和我方清单都没写的，见第 8 节，不升成第 1 问。

人才画像上的 `birth_year`、`telephone`、`email` 只记字段名。探查没有取这三列的值。

科研机构过滤：用到机构时必须能排除 `institution_type_id=company`。现库类型维表有 10 个代码：`archive`、`company`、`education`、`facility`、`funder`、`government`、`healthcare`、`nonprofit`、`other`、`unknown`。快照第 14 节当时写的是 8 类，没有 `funder`、`unknown`。两套都保留。画像行数 83745，与 10-22 我方清单一致；其中 `company` 15392、`education` 16991、`unknown` 15516。只滤掉 `company` 之后，剩下的并不都是科研机构。快照没有写哪些代码算科研机构。

## 4. 第 1 问 · 关系库现在就能对上的

这两条是久新库有行、两端键非空、端点就是已签收的七要素、方向与必须边一致。我方列都是「没有写图入口」。燕大列有的是对照脚本，不是这条边已经按 L05 上图。Tag 和 Edge 仍是存储设计未写，所以步骤停在「不能执行」。

### 4.1 M06 专利 cite 论文

| 列 | 内容 |
|---|---|
| 我方 | 没有写图入口。L05：M06 无论文/专利/项目域，政策 `cite` 不并进 |
| 燕大 | 没有专利→论文的写边脚本。`paper_cites_relation.py` 是论文→论文桩，`patent_cites_relation.py` 是专利→专利 |
| 久新 | 久新库 `ads_patent_cited_paper`。字段 `patent_id`、`paper_id`。不是我方 ADS |

现库 322951 行，两端空键 0。抽样 100 行都能连上 `ads_patent_profile` 和 `ads_paper_profile`。快照写明这是全局专利—论文引用，论文端限定发布的论文主体。方向专利→论文，落在 M06 有向里面。10-22 我方清单行数也是 322951，这一天没有变。

上图步骤（不能执行）：用非空 `patent_id`、`paper_id` 作为两类技术端点的业务键；VID 规则存储设计未写，不能现造；有向边名用 L03 的 `cite`。我方没有函数可读这张久新表并写入图。

不把 `ads_talent_patent_cited_paper` 并进这条。那是人才、专利、论文三元，快照写明不能代替这张二元表。

### 4.2 M09 人才 author_of 专利

| 列 | 内容 |
|---|---|
| 我方 | 没有写图入口。L05 没有边名 `author_of` |
| 燕大 | `invented_by_relation.py` 是专利→人，源是发明人姓名，不是人才 ID 对专利 ID |
| 久新 | 久新库 `ads_talent_patent`。字段 `talent_id`、`patent_id`。`inventor_order` 列在，现库 85069 行全部为空 |

两端空键 0。抽样 100 行的 `patent_id` 都能连上 `ads_patent_profile`。方向人才→专利，与 M09 一致。位次没有值，边不能带顺序。10-22 我方清单行数 85069，这一天没有变。

上图步骤（不能执行）：用 `talent_id`、`patent_id` 作端点业务键；不填位次；VID 与 Edge 属性存储设计未写。我方没有写图函数。

## 5. 第 2 问 · 缺关系数据，要先加工

建议只写方法。加工落在我方 DWD/ADS 映射，或库 `gkxlumenx_gapfill` 的 `gapfill_` 前缀。不写 ODS，不写供应方库，不写久新库。不建表，不灌数。

### 5.1 M03 人才 cooperate 科研机构

快照把 `ads_talent_institution_cooperation` 标成预留。键是 `talent_id`、`institution_id`，并带 `institution_type_id`（企业为 `company`）。10-22 我方清单 0 行。2026-10-30 现库仍是 0 行。

缺的是有行的合作事实，不是缺列名。任职经历不能拿来填这条，任职归 M04 的待确认，不并进合作。

建议：等对端发布这张表之后，再映射到我方 DWD/ADS 的人才—科研机构合作关系，并排除 `company`。在发布前不要用 `gapfill_` 编合作行。

我方没有写图入口。燕大没有这条合作边的脚本。

### 5.2 M05 科研机构 belong 科研机构

`ads_institution_profile` 没有上级机构 ID。允许前缀里也没有机构—机构隶属表。快照和我方清单都未列这种表。现库 `SHOW TABLES` 同样没有。

燕大 `SUBSIDIARY_OF` 按 L03 是企业子公司，不算这条。

建议：在我方 DWD/ADS 增加「下级机构 ID、上级机构 ID」的映射；对端没有事实时，才考虑 `gapfill_` 前缀登记缺口，不在本叶建表。

### 5.3 M06 论文 cite 论文

`SHOW TABLES LIKE 'ads_paper%'` 只有 `ads_paper_profile`。该表有 `cited_by_count`（现库 4000000 行，该列空值 0），没有被引论文 ID，也没有引用边表。计数不是边。

燕大有论文 `CITES` 脚本，源不在这套久新 ADS 里，而且目标经常是 DOI 桩。不能写成我方或久新已经能上。

建议：把论文—论文引用映射到我方 DWD/ADS（引用论文 ID、被引论文 ID）。没有边表之前，不用被引次数反推边，也不做正文 NLP。

### 5.4 M06 专利 cite 专利

允许前缀里没有专利→专利的引用边表。`ads_patent_profile` 的 `cited_paper_count` 是引用论文数，不是专利被引。第 8 节的分析表也没有 `patent_id` 指向另一个 `patent_id` 的列。

燕大 `patent_cites_relation.py` 写的是专利→专利，源是他们的 `dwd_patent_cited`，不是这套久新 ADS。我方没有对应写图。

建议：同 5.3，映射到我方 DWD/ADS 的专利—专利引用。不从分析指标表猜测。

### 5.5 M07 人才 participate 项目

`ads_talent_project` 现库 7702366 行，与 10-22 清单一致。`GROUP BY` 只有一种：`relation_type=funded_output_author`，`is_direct_investigator=0`，`is_lead=0`。

快照写明 `funded_output_author` 只表示这个人署名了项目资助的论文，不是负责人，也不是正式成员。直接参与行数为 0。

缺的是 `direct_investigator` 或 `is_lead=true` 的关系行。列名在快照里有，现库没有这种行。

燕大 `HAS_PARTICIPANT`、`LEADS` 方向是项目→人，源是项目表上的姓名，不是这张久新表。

建议：我方 DWD/ADS 只接收已确认的直接参与或负责关系（人才 ID、项目 ID、角色）。不要把资助论文署名写成 `participate`。

### 5.6 M09 人才 author_of 论文

允许前缀没有人才—论文署名表。`SHOW TABLES LIKE 'ads_talent_p%'` 没有 `ads_talent_paper`。`ads_paper_profile` 只有 `author_count`，没有作者 ID。`ads_talent_research_achievement` 在快照里是代表成果一行，不是署名边，本叶不拿它填 M09。

燕大 `authored_by_relation.py` 方向是论文→人。我方没有写图入口。

建议：把署名事实映射到我方 DWD/ADS（人才 ID、论文 ID，可选作者顺序）。快照写过署名不能靠姓名相等推断；对不齐的不要用姓名去填。

### 5.7 M10 科研机构 publish 政策（只写科研机构端）

允许前缀的机构表、人才表、论文表、专利表、项目表都没有「机构 ID + 政策 ID」的发布关系。`ads_technology_policy_evidence`、`ads_research_problem_policy_evidence` 不在本叶前缀里，而且主体是技术点或研究问题，不是科研机构发布政策。

政策端归 L04。燕大目录里的 `PUBLISH` 写成专家→论文，没有写边脚本，更不是科研机构→政策。

建议：发布主体若要上图，在我方 DWD/ADS 映射科研机构 ID 与政策 ID。政策 Tag 已有，科研机构 Tag 仍是存储设计未写。本叶不写政策一端的步骤。

### 5.8 M13 人才端、M14 科研机构端

整条 `policy_apply_to` 归 L04。本叶允许前缀内没有政策适用到人才、或适用到机构的表和字段。不在这里重裁必须或不必须。

建议：适用对象若以后要加工，落在我方 DWD/ADS 或 `gapfill_`，由政策叶汇总。不要从人才画像或机构画像的名称字段推断适用对象。

## 6. 待确认

这些表有行，键也能连上，但不能写进第 1 问。原因是必须边编号会撞车，或机构类型没有收成「科研机构」。

### 6.1 M01 与 M20 · 同一张人才合作表

久新库 `ads_talent_collaborator`。键 `talent_id`、`collaborator_talent_id`。现库 5051578 行，两端空键 0，自环 0。与 10-22 清单行数一致。

`co_paper_count` 空 3398 行。`co_project_count` 全表为空。`co_patent_count` 空 5047058 行。有数的是论文合作次数，项目合作和专利合作次数没有发布。快照把这三列都写成合作指标，现库只有论文列大体有值。两套都写。

抽样 200 行都有反向行。这只说明抽到的行是成对出现，不是全表已经证明双向。

M01 是无向合作，M20 是双向 `talent_coop`，L03 禁止并进。一张表不能同时算两条都已经能上。有数的指标又接近合著，而 L03 写明合著对照不覆盖这两条的全部。

燕大只有合著脚本。我方 `talent_coop` 是企业→人才，不是人才→人才。

待确认：这张表归 M01、归 M20，还是两条都还不算。确认前不加工成边。若确认只采用论文合作，还要另定无向还是双向，以及空的项目、专利列是否继续空着。

### 6.2 M02 与 M19 · 同一张机构合作年表

久新库 `ads_institution_collaboration_yearly`。键 `institution_id`、`collaborator_institution_id`、`statistics_year`。快照要求 A—B 同时发布 A→B 和 B→A。现库 14380246 行，与 10-22 清单一致。

两端都不是 `company` 的 13137234 行。至少一端是 `company` 的 1243012 行。`company` 可以滤掉。滤掉之后仍有 `unknown`、`healthcare`、`government`、`facility`、`funder` 等，快照没有把它们定义成科研机构。

`co_paper_count>0` 的 14380180 行。`patent_coverage_status` 全表都是 `NOT_AVAILABLE`。快照写明当前没有 confirmed 的受让人，专利字段不得写成 0。`project_coverage_status` 为 `NOT_AVAILABLE` 的 13636728 行，`PARTIAL` 的 743518 行。所以这张表现在能看的是论文共现，不是专利合作，项目合作也只是部分覆盖。

M02 无向 `cooperate` 与 M19 双向 `research_coop` 禁止并进。我方企业挂边上的 `research_coop` 起点是企业，不是这条。燕大没有机构—机构合作写边脚本。

待确认：非 `company` 里哪些 `institution_type_id` 算科研机构；确认之后这张表归 M02 还是 M19。确认前不把年度论文共现写成必须边。

### 6.3 M04 人才 belong 科研机构

久新库 `ads_talent_experience`。键 `talent_id`、`experience_id`，机构字段 `institution_id`、`institution_type_id`。快照：`experience_type` 1 教育、2 工作。现库 140887 行，`institution_id` 空 0，与清单行数一致。`company` 423 行，非 `company` 且有机构 ID 的 140464 行。抽样 200 个非空机构 ID 都能连上机构画像，且抽到的都不是 `company`。这 200 行不是全表的类型比例；全表的 `company` 就是上面的 423。

教育、工作两类都有大量 `education`，也有大量 `unknown`。`company` 滤得掉。其余类型是不是科研机构，与 6.2 是同一个未写死的口径。

`ads_talent_profile.current_institution_ids` 由经历派生。现库画像 100000 行里该列空 50721。没有经历就保持空，快照禁止用姓名或自由文本猜机构。当前机构只是隶属的一个子集，不能代替经历表。

燕大 `AFFILIATED_WITH` 是人→机构的任职对照，机构不单是科研机构。我方没有人才→科研机构的写图入口。

待确认：科研机构类型集合。确认前，经历表只能说明「人与机构 ID 对得上，企业行可以排除」，不能写成科研机构隶属已经能上。

### 6.4 M08 科研机构 participate 项目

久新库 `ads_project_institution`。键 `project_id`、`institution_id`。现库合计 22571355 行，与 10-22 清单一致。

| relation_type | 行数 | institution_role_code |
|---|---:|---|
| `funded_output_affiliation` | 22553929 | 全空 |
| `affiliation_exact_name` | 17399 | `lead_affiliation` 17366，`investigator_affiliation` 33 |
| `affiliation_ror` | 27 | `lead_affiliation` 27 |

快照写明 `funded_output_affiliation` 只是受资助论文上的机构署名，不得参与联合项目计数。这 2255 万行不能当成 M08。

剩下 17426 行的角色是负责隶属或参与者隶属，方向在表上是项目—机构，M08 要的是科研机构→项目，加工时要对调方向。我方字段清单注释里写过 `awarded_direct`，现库 `DISTINCT` 没有这个值。清单是我方整理，现库没有该代码。

抽样 200 行都能连上机构画像，其中 3 行是 `company`。这不是全表企业占比。`company` 可以在连接画像后排除。排除之后是否算科研机构，仍是 6.2 的待确认。

燕大 `FUNDED_BY` 是项目→机构的资助，方向相反，而且资助不是这 17426 行的角色名。目录中的机构参与项目没有写边脚本。我方没有写图入口。

待确认：科研机构类型集合。确认前，不把这 17426 行写成已经能上，也不把资助论文署名写成参与。

## 7. 第 3 问 · 不能靠源表、要先用其他技术

0 条。

下面这些看起来像「别的技术」，本叶不把它们写成必须边的路径，也不附示例脚本：

- `ads_talent_similarity` 现库有这张表。快照写明分数不表达合作关系。不填 M01、M20。
- 燕大发明人脚本靠姓名匹配，并写明向量步骤不在该脚本内。久新 `ads_talent_patent` 已经有人才 ID 和专利 ID，M09 的专利一半不需要先做向量。
- `ads_patent_analysis_institution_inventor` 现库 26379 行，`platform_talent_id` 全空，`identity_resolution_status` 全是 `SOURCE_NAME_ONLY`。这是分析表里的人名，不是带主键的署名边。不把它升成 M09 或 M04 的必经消歧。
- 论文引用、机构上下级、直接参与项目，缺的是关系表或关系行，归第 2 问的映射，不归模型推理。

Java 不做 NLP、向量或模型推理。没有代码的技术写成未实现；本叶没有一条要落到这类入口。

## 8. 快照没有、现库多出来的表

2026-10-30 `SHOW TABLES` 见到，2026-10-22 快照和我方表清单都没有。不升成第 1 问。久新材料也不是已放行的上图契约。

| 现库表 | 行数 | 为什么不填必须边 |
|---|---:|---|
| `ads_institution_collaboration_subfield_yearly` | 23363790 | 快照未列。列上有机构对、年份、子领域和论文/专利合作计数。子领域不是七要素。不另造边。机构类型口径仍待确认，专利覆盖未再拿它推翻年度表的全表 `NOT_AVAILABLE` |
| `ads_patent_analysis_institution_edge` | 915 | 快照未列。`relation_type` 全是 `CO_ASSIGNEE`，覆盖状态全是 `PARTIAL`。两端都能连上机构画像；两端都不是 `company` 的 835 行，触到 `company` 的 80 行。年度合作表的专利覆盖仍是全表 `NOT_AVAILABLE`。两套说法不一致，不拿这 915 行填 M02 或 M19 |
| `ads_patent_analysis_patent_institution` | 2767360 | 快照未列。专利与受让人/机构。M08 的消费来源是参与项目，不是专利受让。企业—技术不建 |
| `ads_patent_analysis_entity_patent` | 633456 | `entity_type` 只有 `INSTITUTION`、`JURISDICTION`、`IPC`。没有人才。IPC 不是七要素「技术」 |
| `ads_patent_analysis_institution_inventor` | 26379 | 见第 7 节。没有平台人才 ID |
| 其余 `ads_patent_analysis_*` | 见探查 | 分类、辖区、主题、年份指标或 Top 专利。主题和分类号不建 Tag |

`ads_institution_paper`、`ads_institution_patent` 在快照里是每机构最多 20 篇/件的代表作，不是全量参与或署名。不填 M08、M09。

## 9. 探查边界

- 日期：2026-10-30。只读。`SHOW`、`COUNT`、`DISTINCT`、空值、键能否连上。抽样最多 200 行，只用于键和类型，样例值不写入本文。
- 连上了。`information_schema.tables` 被拒绝，改用 `SHOW TABLES`。
- 范围只限第 3.3 节的五个前缀。没有 `INSERT`、`UPDATE`、`DELETE`、DDL。
- 账号、主机、端口、库名、连接串不在本文。
