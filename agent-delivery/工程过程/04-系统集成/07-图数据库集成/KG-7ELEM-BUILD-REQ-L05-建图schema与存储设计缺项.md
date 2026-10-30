# KG-7ELEM-BUILD-REQ-L05 · 建图 schema 与存储设计缺项

> 日期：2026-10-30  
> 任务：`KG-7ELEM-BUILD-REQ-L05`  
> 必须三元组只认现在磁盘上的 `KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md`：必须 24 条，可选 0 条。编号以该文 M01–M24 为准，不沿用旧编号。  
> 服务机构之间的 `participates` 不加。L03 已写明这条不升必须。  
> VID 与属性只抄存储设计或 `SYSINT-SCHEME-07-L06` 已写明的前缀。没写的写「存储设计未写」。  
> 不改 storage 原文，不改 L03，不改图空间，不重做 `SYSINT-SCHEME-07-L07` 的代码差异。

七要素：企业、产业链环节、科研机构、技术、人才、服务机构、政策。技术只含论文、专利、项目。ENT 的 Tag `technology` 是技术点，不当作技术。

## 1. 读过的存储

| 域 | 入图流程 | stores/nebula | 本叶怎么用 |
|---|---|---|---|
| ENT | `data/data-design/storage/ENT/etl/pipeline-to-nebula.md` | `stores/nebula/graph-enterprise.md` | 企业 Tag。M23 `supply`、M24 `parent_sub`。`cooperate` 是有向，对不上 M22 双向 |
| CHAIN | `CHAIN/etl/pipeline-to-nebula.md` | `stores/nebula/graph-chain.md` | 环节 Tag、M15 `depends_on`。`participates` 是环节→对象，对不上 M17、M18 |
| POLICY | `POLICY/etl/pipeline-to-nebula.md` | **无**目录 `stores/nebula/`。有单文件 `stores/nebula.md`，已读 | 政策 Tag。M16 `cite` 是政策→政策。`policy_relate` 无同名边 |
| SVC | `SVC/etl/pipeline-to-nebula.md` | `stores/nebula/graph-svc.md` | 服务机构 Tag `institution`。服务→服务的 `participates` 不进必须表 |
| COMP | `COMP/etl/pipeline-to-nebula.md` | **无** `stores/nebula` | 只读。不定义 Tag/Edge，不计入建图 schema |

`data/data-design` 下的 `pipeline-to-nebula.md` 只有这五份。人才、科研机构、论文/专利/项目没有对应存储域。

对照规则：边名、起点 Tag、终点 Tag、方向四项都对上，才标「存储设计已有」。同名但起终点或方向不同，不算已有，也不把那条边的属性挪过来。双向和有向算方向不同。

必选或可选：上述 CREATE 与属性清单都没有写 NOT NULL 或必选。单元格统一写「存储设计未写」。这一项不另升成「缺属性」，避免把没声明的约束算成缺列。

## 2. Tag

必须端点 7 个。Tag 名只用存储里已经写给该端点的名字。

| 端点 | Tag 名称 | VID 规则 | 属性名与类型 | 必选或可选 | 缺项类 |
|---|---|---|---|---|---|
| 企业 | `enterprise` | `ent:{org_id}`。目标长度 80。见 ENT etl §3.2、L06 §3.3。as-built 的 64 不采用（ENT etl §3.1） | 两套并列，不合并。ENT etl §4：`name string`、`node_type string`、`weight double`、`props string`。CHAIN etl §4：`name string`、`enterprise_code string`、`chain_role string`、`weight double`、`props string` | 存储设计未写 | 存储设计已有。属性集合另见 §4 |
| 产业链环节 | `segment` | `segment:{node_id}`。长度 80。见 CHAIN etl §3、§5、§13.2，L06 §2.3 | CHAIN etl §4：`name string`、`segment_key string`、`chain_id string`、`chain_stage string`、`weight double`、`props string` | 存储设计未写 | 存储设计已有 |
| 科研机构 | 存储设计未写 | 存储设计未写 | 存储设计未写 | 存储设计未写 | 无对应存储域 |
| 技术 | 存储设计未写 | 存储设计未写 | 存储设计未写 | 存储设计未写 | 无对应存储域 |
| 人才 | 存储设计未写 | 存储设计未写 | 存储设计未写 | 存储设计未写 | 无对应存储域 |
| 服务机构 | `institution` | 现网 `institution:{org_id}`（SVC etl §3，L06 §5.3）。目标 `inst:{org_id}`（SVC etl §3）。长度 ≤80。两条都写了，没有收成一条 | CHAIN etl §4：`name string`、`institution_type string`、`weight double`、`props string`。SVC etl §4 另点名 `node_type`、`role`，类型存储设计未写。区分服务用 `role=service`（graph-svc.md §2，L06 §5.3） | 存储设计未写。SVC 只写「按 DESCRIBE 有则写」 | 存储设计已有。`node_type` / `role` 另见 §4 |
| 政策 | `policy` | `pol:{policy_id}`。长度 80。见 POLICY etl §3、`stores/nebula.md`、L06 §4.3 | `name string`、`weight double`、`props string`。POLICY etl §4 与 `stores/nebula.md` 一致 | 存储设计未写 | 存储设计已有 |

不收进上表的点名：

- Tag `chain` 是产业链，不是产业链环节（CHAIN etl §13.1）。
- ENT as-built 的 `chain_node`、前缀 `chn:` 不是 `segment`（ENT etl §3.1、§4）。目标只 FETCH `segment:`（ENT etl §5）。
- ENT as-built 的 Tag `research`、`talent`、`service`、`technology` 不作为这四个端点的本体。ENT etl §4 写明禁止在企业侧新建第二套本体。`technology` 的 VID 例是 `tech:先进封装`，并写明禁止 `patent_no`（ENT etl §3.1），对不上论文/专利/项目。
- CHAIN / SVC / POLICY 的 `institution` 不拆成科研机构专属 Tag。CHAIN etl §13.3 把科研机构和服务机构都写进这一个 Tag。

## 3. Edge

必须边 24 条，一行对应 L03 当前 M01–M24。方向抄 L03 该行。属性只在「存储设计已有」那几行抄 CREATE。

| 编号 | 边名 | 起点 Tag | 终点 Tag | 方向 | 属性 | 必选或可选 | 缺项类 | 回指 |
|---|---|---|---|---|---|---|---|---|
| M01 | `cooperate` | 存储设计未写 | 存储设计未写 | 无向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 无人才域。ENT etl §12 的 `cooperate` 是企业→企业且有向，端点和方向都不同 |
| M02 | `cooperate` | 存储设计未写 | 存储设计未写 | 无向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 无科研机构域。ENT etl §12 终点是 enterprise |
| M03 | `cooperate` | 存储设计未写 | 存储设计未写 | 无向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 人才、科研机构都无域。ENT etl §12 终点是 enterprise |
| M04 | `belong` | 存储设计未写 | 存储设计未写 | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 五份流程都没有边名 `belong`。ENT `parent_sub` 是企业→企业 |
| M05 | `belong` | 存储设计未写 | 存储设计未写 | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 同上 |
| M06 | `cite` | 存储设计未写 | 存储设计未写 | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 无论文/专利/项目域。POLICY etl §12 的 `cite` 是政策→政策，端点不同，不并进本条 |
| M07 | `participate` | 存储设计未写 | 存储设计未写 | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 无人才域、无论文/专利/项目域。CHAIN 的 `participates` 不是这条 |
| M08 | `participate` | 存储设计未写 | 存储设计未写 | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 无科研机构域、无论文/专利/项目域 |
| M09 | `author_of` | 存储设计未写 | 存储设计未写 | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 五份流程都没有边名 `author_of` |
| M10 | `publish` | 存储设计未写 | `policy` | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 起点无科研机构域。POLICY etl §4 无 `publish` |
| M11 | `policy_relate` | `policy` | `policy` | 无向 | 存储设计未写 | 存储设计未写 | 缺 Edge | POLICY etl §4、§12 只有有向 `cite`，边名和方向都不同 |
| M12 | `policy_apply_to` | `policy` | `enterprise` | 有向 | 存储设计未写 | 存储设计未写 | 缺 Edge | POLICY etl §12、§17.3：边名是 `apply_to`，企业行写明不上图，企业只走 `support` |
| M13 | `policy_apply_to` | `policy` | 存储设计未写 | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 终点人才无域。POLICY etl §17.3：`apply_to` 到人才不上图，且无 talent Tag |
| M14 | `policy_apply_to` | `policy` | 存储设计未写 | 有向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 终点科研机构无域。POLICY etl §17.3：`apply_to` 到科研机构不上图 |
| M15 | `depends_on` | `segment` | `segment` | 有向，segment→segment | `dependency_type string`、`weight double`、`props string` | 存储设计未写 | 存储设计已有 | CHAIN etl §4、§14.2、§17.3。`relation_direction=reverse` 时对调，仍是有向 |
| M16 | `cite` | `policy` | `policy` | 有向，policy→policy | `weight double`、`props string` | 存储设计未写 | 存储设计已有 | POLICY etl §4、§12、§19：两端 `pol:`，方向政策→对象。`stores/nebula.md` 写成 `relation string`、`weight double`，流程写明以 etl §4 为准，不另造列 |
| M17 | `participates` | `enterprise` | `segment` | 有向，enterprise→segment | 存储设计未写 | 存储设计未写 | 缺 Edge | CHAIN etl §12、§17.3：方向是产业/环节→企业。与本条相反。§14.4 流程图有「participates → segment」字样，与 §12 终点列不一致，不以该字样算已有 |
| M18 | `participates` | `institution` | `segment` | 有向，service_institution→segment | 存储设计未写 | 存储设计未写 | 缺 Edge | CHAIN etl §12、§17.3：`participates` 是环节→服务。SVC etl §12 服务→环节的边名是 `belongs_to` |
| M19 | `research_coop` | 存储设计未写 | 存储设计未写 | 双向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 无科研机构域。ENT etl §4、§12 的 `research_coop` 是企业→科研机构且有向，端点和方向都不同，属性不挪 |
| M20 | `talent_coop` | 存储设计未写 | 存储设计未写 | 双向 | 存储设计未写 | 存储设计未写 | 无对应存储域 | 无人才域。ENT etl §4、§12 的 `talent_coop` 是企业→人才且有向，端点和方向都不同，属性不挪 |
| M21 | `service_provide` | `institution` | `enterprise` | 有向，service→enterprise | 存储设计未写 | 存储设计未写 | 缺 Edge | ENT etl §12、§14.6：`service_provide` 是企业→服务机构。SVC etl §12 服务→企业的边名是 `participates` |
| M22 | `cooperate` | `enterprise` | `enterprise` | 双向 | 存储设计未写 | 存储设计未写 | 缺 Edge | ENT etl §4、§12、§14.1 有同名边，方向默认本企→对象，是有向，不是双向 |
| M23 | `supply` | `enterprise` | `enterprise` | 有向，enterprise→enterprise | `weight double`、`props string` | 存储设计未写 | 存储设计已有 | ENT etl §4、§12、§14.8。CHAIN 的 `supplies` 是环节→环节，边名不同，不算这条 |
| M24 | `parent_sub` | `enterprise` | `enterprise` | 有向，enterprise→enterprise | `weight double`、`props string` | 存储设计未写 | 存储设计已有 | ENT etl §4、§12、§14.3：母→子。L03 没写死谁是母公司；方向仍是有向，两端都是企业 |

M15、M16、M23、M24 的属性来自对应 CREATE，没有把另一套列并进来。

## 4. 缺属性

Tag 或 Edge 已经对上，但属性集合收不成一套时，另记缺属性。不新造列名。

| 对象 | 缺什么 | 回指 |
|---|---|---|
| Tag `enterprise` | ENT 与 CHAIN 各写了一套列，没有第三份收成一套。建图 schema 两套并列 | ENT etl §4；CHAIN etl §4 |
| Tag `institution` | CHAIN 的 CREATE 没有 `node_type`、`role`。SVC 点了这两列，类型没写，也没有写进同一条 CREATE | CHAIN etl §4；SVC etl §4；L06 §5.3 只复述列名 |

## 5. 不计入

- 不加服务机构 `participates` 服务机构。L03 禁止事项写明不画；A21 方向待确认。SVC etl §12 虽有服务→服务的 `participates`，不升成必须边。
- 不加 L03 §3 不建的对：企业—科研机构、企业—技术、企业—人才、产业链环节—科研机构、产业链环节—政策、科研机构—服务机构等。ENT 的 `research_coop`（企业→科研机构）、`talent_coop`（企业→人才）不算 M19、M20。
- COMP etl §1、§4.1：综合无 A/B/C，不 `INSERT VERTEX|EDGE`，不另造边。五查询只读已有边，不算建图 schema。COMP 无 `stores/nebula`。
- POLICY `stores/nebula.md` 的 `cite` 列与 etl §4 不一致。流程写明现网以 etl §4 为准。本叶按 etl §4 抄 M16 的属性，不重做 `SYSINT-SCHEME-07-L07`。
- 不改 `demo_gkx_chain`，不选别的 space。

## 6. 计数

| 缺项类 | Tag | Edge | 另记 | 合计 |
|---|---|---|---|---|
| 存储设计已有 | 4（企业、产业链环节、服务机构、政策） | 4（M15、M16、M23、M24） | 0 | 8 |
| 缺 Tag | 0 | — | 0 | 0 |
| 缺 Edge | — | 6（M11、M12、M17、M18、M21、M22） | 0 | 6 |
| 缺属性 | — | — | 2（`enterprise` 两套列、`institution` 的 `node_type`/`role`） | 2 |
| 无对应存储域 | 3（科研机构、技术、人才） | 14（M01–M10、M13、M14、M19、M20） | 0 | 17 |

Tag 7。必须 Edge 24。缺 Tag 0。M16 是存储设计已有。M19、M20 都是无对应存储域。
