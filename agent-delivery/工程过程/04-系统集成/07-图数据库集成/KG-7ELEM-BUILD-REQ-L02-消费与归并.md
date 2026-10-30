# KG-7ELEM-BUILD-REQ-L02 · 七要素建图 · 消费清单与实体归并

> **任务**：`KG-7ELEM-BUILD-REQ-L02`  
> **日期**：2026-10-30  
> **认领**：`agent:data-agent`；监管 `human:淮政玮`；`claim_type=coordinator_dispatch`  
> **查询真源**：`知识图谱-实体关系属性需求清单.md` **v1.2**。数字只用 §1.5 / §9：保留 **98**、转背景 **16**、不相关 **457**、飞书收回 **84**。不用 §2.1 残留的 81 / 15 / 475。  
> **算法真源**：`SYSINT-SCHEME-07-L03-算法中台上图台账.md`、`SYSINT-SCHEME-07-L06-算法中台入图流程.md`。L06 写明：L03「政策无 Nebula 写图」已被现行 A/B/C 接口取代，政策写图以 L06 为准。  
> **本叶只写**：读图或写图的三元组（起点、关系、终点、用途），以及展示清单 14 类实体归并。  
> **本叶不写**：必须边裁决、关系总图、建图动作、schema 缺项。

七要素名称锁定为：企业、产业链环节、科研机构、技术、人才、服务机构、政策。技术 = 论文 / 专利 / 项目。

---

## 1. 条数

| 块 | 条数 | 怎么数 |
|---|---:|---|
| 查询侧 | **46** | §四 17 类关系展开端点对，去掉只由批量导入 / 写入 / 纯前端支撑的 `technology_hierarchy` 后为 41；保留叶写明了端点、但没写关系名的另 5 条 |
| 算法侧 | **36** | L06 现行写图 22；L03 台账里有 INSERT 的边 14 |
| **合计** | **82** | 同一逻辑边若入口不同，各记一行 |

统计指标、纯前端、图谱版本、批量导入不进表。只写点、明文「不写」的算子不进表。表名、关系名、终点类型、方向在真源里没写死的，行上标待确认，不补名字。

---

## 2. 查询侧消费三元组（46）

回指只用 v1.2 判为保留、且是在读实体或边的 seq。中心性、综合评分、预测、重叠度分数本身不作为回指。§四端点格已经写明的一对，即使某条保留叶没有单独点名这一对，仍列入；备注说明叶未单列。

### 2.1 §四端点对（41）

| ID | 起点 | 关系 | 终点 | 方向 | 用途 | 回指 | 备注 |
|---|---|---|---|---|---|---|---|
| Q01 | person | cooperate | person | 无向 | 人才合作网络 | seq261、297、305、288、300、313、510 | §四还列了 seq26、137、283、306、493。26 未点名合作类型；137 是中心性；283 是成果穿透；306 是研究路径；493 归 Q39–Q41 |
| Q02 | institution | cooperate | institution | 无向 | 机构合作 | §四 `cooperate` 行 | 保留叶没有单独写「机构—机构」。seq137 是中心性，不回指 |
| Q03 | person | cooperate | institution | 无向 | 人才与合作机构 | seq261 | 同上，seq137 不回指 |
| Q04 | person | belong | institution | 有向 | 人员隶属机构 | seq261 | §四还列 seq9、283。9 只写多类要素关联；283 是成果穿透 |
| Q05 | institution | belong | institution | 有向 | 机构上下级 | §四 `belong` 行 | 保留叶没有单独写机构上下级 |
| Q06 | person | research | field | 有向 | 人员研究领域 | seq303、306 | |
| Q07 | person | research | topic | 有向 | 人员研究主题 | seq303、306 | |
| Q08 | institution | research | field | 有向 | 机构研究领域 | §四 `research` 行 | 保留叶没有单独写机构—领域 |
| Q09 | enterprise | research | field | 有向 | 企业研究领域 | seq191、194 | seq191 的重叠度分数是统计指标，不进表；本行只记研究边。194 展示的是企业、专家、文献、关键词，没有写 field 这个类型名 |
| Q10 | paper | cite | paper | 有向 | 论文引用 | seq340、511 | §四还列 seq100、374。100 判不相关；374 是数据集关联 |
| Q11 | patent | cite | paper | 有向 | 专利引用论文 | §四 `cite` 行；叶 seq340 | seq340 写文献/专利/项目上的引用边，没有单独写「专利→论文」 |
| Q12 | patent | cite | patent | 有向 | 专利引用 | seq340 | |
| Q13 | person | participate | project | 有向 | 人员参与项目 | seq283 | §四还列 seq15、417。15 判不相关；417 是综合评分 |
| Q14 | institution | participate | project | 有向 | 机构参与项目 | §四 `participate` 行 | 283 只写人员穿透项目 |
| Q15 | paper | belong_to | field | 有向 | 成果归属领域 | §四 `belong_to` 行 | 保留叶没有单独写论文—领域。seq71 是预测，不回指 |
| Q16 | patent | belong_to | field | 有向 | 成果归属领域 | §四 `belong_to` 行 | 同上 |
| Q17 | project | belong_to | field | 有向 | 成果归属领域 | §四 `belong_to` 行 | 同上 |
| Q18 | technology | belong_to | field | 有向 | 技术点落在领域图 | seq69 | |
| Q19 | person | author_of | paper | 有向 | 作者与论文 | seq283、340 | seq15 不回指 |
| Q20 | person | author_of | patent | 有向 | 作者与专利 | seq283 | |
| Q21 | technology | technology_influence | technology | 有向 | 技术弦线、影响路径 | seq51 | seq36 是关系新增（转背景），不回指。seq28 只写路径上的「节点间关系」，没有点名本关系 |
| Q22 | institution | publish | policy | 有向 | 政策发布主体 | seq609 | |
| Q23 | policy | policy_relate | policy | 无向 | 政策关联网络 | seq240、609 | |
| Q24 | policy | policy_apply_to | field | 有向 | 政策适用领域 | seq609 | seq240 也写了政策与科技领域，关系名在 §四记在本行 |
| Q25 | policy | policy_apply_to | enterprise | 有向 | 政策服务对象 | §四 `policy_apply_to` 行 | seq609 写「服务对象」，线索点名 institution，没有点名 enterprise |
| Q26 | policy | policy_apply_to | person | 有向 | 政策服务对象 | §四 `policy_apply_to` 行 | 叶没有点名 person |
| Q27 | policy | policy_apply_to | institution | 有向 | 政策服务对象 | seq609 | |
| Q28 | dataset | dataset_link | dataset | 无向 | 数据集引用、衔接、主题交叉 | seq339、374 | |
| Q29 | paper | about_topic | topic | 有向 | 成果与主题 | §四 `about_topic` 行 | 回指叶 337、339、374 写的是数据集。seq342 判纯前端剔除，不回指 |
| Q30 | patent | about_topic | topic | 有向 | 成果与主题 | §四 `about_topic` 行 | 同上 |
| Q31 | project | about_topic | topic | 有向 | 成果与主题 | §四 `about_topic` 行 | 同上 |
| Q32 | dataset | about_topic | topic | 有向 | 数据集与主题 | seq337、339、374 | |
| Q33 | event | event_link | event | 无向 | 科创事件之间 | seq16 | |
| Q34 | event | event_link | institution | 有向 | 事件与机构 | seq16 | |
| Q35 | event | event_link | person | 有向 | 事件与人员 | seq16 | |
| Q36 | activity | activity_link | person | 有向 | 活动与专家讲者 | seq576 | |
| Q37 | activity | activity_link | institution | 有向 | 活动主办机构 | §四 `activity_link` 行 | seq576、579 写了专家和资源，没有写机构 |
| Q38 | activity | activity_link | dataset | 有向 | 活动与科技资源 | seq576、579 | |
| Q39 | innovation_carrier | carrier_cooperate | innovation_carrier | 无向 | 跨载体协作 | seq493 | seq496 是协同绩效与影响力评分，不回指 |
| Q40 | innovation_carrier | carrier_cooperate | person | 有向 | 载体与人才协同 | seq493 | |
| Q41 | innovation_carrier | carrier_cooperate | institution | 有向 | 载体与机构协同 | seq493 | |

### 2.2 保留叶写了端点、没写关系名（5）

| ID | 起点 | 关系 | 终点 | 方向 | 用途 | 回指 | 待确认 |
|---|---|---|---|---|---|---|---|
| Q42 | technology | 待确认 | person | 待确认 | 技术点的关联实体 | seq22 | 关系名、方向 |
| Q43 | technology | 待确认 | institution | 待确认 | 同上 | seq22 | 关系名、方向 |
| Q44 | technology | 待确认 | paper | 待确认 | 同上 | seq22 | 关系名、方向 |
| Q45 | technology | 待确认 | patent | 待确认 | 同上 | seq22 | 关系名、方向 |
| Q46 | policy | 待确认 | 产业发展（类型待确认） | 待确认 | 政策与产业发展的关联 | seq240 | 关系名、终点类型。展示清单没有产业链实体 |

---

## 3. 算法侧消费三元组（36）

只收真源写了「会写这条边」的入口。L03 与 L06 入口不同，不并成一行。方向、终点、关系名以该行所引文件为准，不把另一份文件的端点抄过来。

### 3.1 L06 现行写图（22）

空间写法以 L06 为准，四条都写 `demo_gkx_chain`。本叶不据此改空间。

| ID | 起点 | 关系 | 终点 | 方向 | 用途 | 回指 | 待确认 |
|---|---|---|---|---|---|---|---|
| A01 | segment | belongs_to | chain | segment → chain | 产业链入图 | `CHAIN_RE_BELONGS_TO` | 无。来源 `industry_chain_node.chain_id` |
| A02 | segment | depends_on | segment | segment → segment | 环节上下游 | `CHAIN_RE_DEPENDS_ON` | 来源只写「环节上下游」，表名待确认 |
| A03 | enterprise | participates | 待确认 | 待确认 | 企业挂到产业链 | `CHAIN_RE_INDUSTRY_ENTERPRISE` | 另一端类型。VID 只写企业端 `ent:`。来源 `industry_chain_entity_rel` |
| A04 | 科研机构（tag 待确认） | participates | 待确认 | 待确认 | 科研机构挂到产业链 | `CHAIN_RE_INDUSTRY_RESEARCH` | 起点 tag、另一端。VID 前缀只写 `inst:`。来源同上 |
| A05 | 服务机构（tag 待确认） | participates | 待确认 | 待确认 | 服务机构挂到产业链 | `CHAIN_RE_INDUSTRY_SERVICE` | 同 A04 |
| A06 | policy | 待确认 | chain 或 segment | 政策挂到链或环节 | 政策挂到产业链 | `CHAIN_RE_INDUSTRY_POLICY` | 关系名。来源 `policy_industry_rel`。VID `pol:` |
| A07 | enterprise | cooperate | enterprise | 待确认 | 企业域内部边 | `ENT_RE_COOP` | 方向。B 档是本域内部边，两端都是企业。业务来源表未写 |
| A08 | enterprise | invest | enterprise | 待确认 | 企业域内部边 | `ENT_RE_INVEST` | 方向。业务来源表未写 |
| A09 | enterprise | parent_sub | enterprise | 待确认 | 企业域内部边 | `ENT_RE_BELONG` | 方向。业务来源表未写 |
| A10 | enterprise | supply | enterprise | 待确认 | 企业域内部边 | `ENT_RE_SUPPLY` | 方向。业务来源表未写 |
| A11 | enterprise | industry_belong | 待确认 | 待确认 | 企业挂到另一类点 | `ENT_RE_INDUSTRY` | 终点类型 |
| A12 | enterprise | produces | 待确认 | 待确认 | 企业挂技术 | `ENT_RE_TECH` | 终点类型 |
| A13 | enterprise | talent_coop | 待确认 | 待确认 | 企业挂人才 | `ENT_RE_TALENT` | 终点类型。不把 L03 的人才—人才抄到本行 |
| A14 | enterprise | research_coop | 待确认 | 待确认 | 企业挂科研 | `ENT_RE_RESEARCH` | 终点类型。不把 L03 的科研—科研抄到本行 |
| A15 | enterprise | 待确认 | 待确认 | 待确认 | 企业挂政策 | `ENT_RE_POLICY` | L06 边名只写「政策」 |
| A16 | enterprise | service_provide | 待确认 | 待确认 | 企业挂服务 | `ENT_RE_SERVICE` | 终点类型 |
| A17 | policy | cite | policy | policy → policy | 政策引用 | `POLICY_RE_CITE` | 无。两端 VID `pol:` |
| A18 | policy | support | 产业或 enterprise | policy → 产业或企业 | 政策支撑 | `POLICY_RE_SUPPORT` | 「产业」的 tag。企业端类型名写了 |
| A19 | policy | apply_to | 机构或服务 | policy → 机构或服务 | 政策适用 | `POLICY_RE_APPLY_TO` | 机构、服务的 tag |
| A20 | policy | regulate | 待确认 | policy → 受规范对象 | 政策规范 | `POLICY_RE_REGULATE` | 终点类型 |
| A21 | institution | participates | institution | 待确认 | 服务机构之间的合作或投资 | `SVC_RE_SVC_SVC` | 方向。合作是本批两两配对；投资要 `svc_org_finance_event.ext.inv_org_id` 也在本批。边上 `chain_role=service` |
| A22 | institution | belongs_to | chain 或 segment | institution → chain 或 segment | 服务机构挂产业 | `SVC_RE_INDUSTRY` | 无。只有行业字段已经是 `chain:` / `segment:` 才写 |

### 3.2 L03 台账里有 INSERT 的边（14）

| ID | 起点 | 关系 | 终点 | 方向 | 用途 | 回指 | 待确认 |
|---|---|---|---|---|---|---|---|
| A23 | segment | belongs_to | chain | segment → chain | 产业链写图 | `lumen_common/algorithms/chain/graph_project.py` `map_graph` / `NebulaSink` | 来源只写「DWD chain 表 / DWD node 表」，表名待确认 |
| A24 | enterprise | participates | segment | enterprise → segment | 产业链写图 | 同上 | 来源「DWD 企业表」，表名待确认 |
| A25 | institution | participates | segment | institution → segment | 产业链写图 | 同上 | 来源「DWD 机构表」，表名待确认。L03 写明 institution 端点是企业/机构混装 |
| A26 | service_institution | participates | segment | service_institution → segment | 产业链写图 | 同上 | 同 A25 |
| A27 | segment | depends_on | segment | segment → segment | 产业链写图 | 同上 | 来源表名未写 |
| A28 | industry | industry_belong | enterprise | industry → enterprise | 通用灌图 | `vendor/entan-py/entan/graph/nebula_loader.py` | 无。读 PG `ads.graph_node` / `ads.graph_edge` |
| A29 | research | research_coop | research | 双向 | 通用灌图 | 同上 | 无。L03 写明久新是否灌入 PG 未验证；入口仍索引了这条边 |
| A30 | talent | talent_coop | talent | 双向 | 通用灌图 | 同上 | 同 A29 |
| A31 | service | service_provide | enterprise | service → enterprise | 通用灌图 | 同上 | 无。`node_type` 不在五个硬编码 TAG 里时兜底写入 `service` |
| A32 | enterprise | cooperate | enterprise | 双向 | 通用灌图 | 同上 | 无 |
| A33 | enterprise | supply | enterprise | enterprise → enterprise | 通用灌图 | 同上 | 无 |
| A34 | enterprise | parent_sub | enterprise | enterprise → enterprise | 通用灌图 | 同上 | 无 |
| A35 | institution | participates | 产业环节（L03 同文 segment） | institution → 产业环节 | 服务机构写图 | `vendor/entan-py/entan/svcgraph.py` `upsert_participates` | 机构数据源的表名未写 |
| A36 | institution | belongs_to | 产业 | institution → 产业 | 服务机构写图 | 同上 `upsert_belongs_to` | 「产业」的 tag。表名未写 |

`demo-algo-science` `chainan/graph/nebula_project.py` 在 L03 里写了会生成 INSERT，没有另列与 A23–A27 不同的边，不另造行。`incremental.py` 与 `POST /v1/graph/nodes` 走的是同一灌图入口，不另造行。

---

## 4. 不进消费表

| 类别 | 依据 | 处理 |
|---|---|---|
| `technology_hierarchy` | §四回指 seq17、18、36、302。17 是批量导入，18 是自动构建，36 是关系新增，均在 §十转背景；302 是缩放聚焦，判纯前端剔除 | 不进表 |
| 统计指标 | §六的度/紧密/中介/PageRank/综合分、社群指标、影响力赋分、重叠度分数、综合评分、预测、风险评分；cfg_metric 全 mock | 不进表。seq70、71、137、191 的分数、417、496 只在备注里排除 |
| 纯前端 | 判定剔除 47 叶，含 seq302 | 不进表 |
| 图谱版本 | §十 seq39、40（修改历史、保存与版本） | 不进表 |
| 批量导入与写入 | §十 16 叶（seq17、18、34–40、42–47、449） | 不进表 |
| 不相关 | §9 的 457 叶 | 不进表 |
| 通用图计算 | 路径、切片、过滤、排序、社群、模式识别。不新起终点 | 不另造行。已有边仍看第 2 节 |
| 只写点 | `CHAIN_NER_INDUSTRY`、`ENT_NER_ORG`、`POLICY_NER_POLICY`、`SVC_NER_ORG` | 没有关系，不进表 |
| 明文不写 | `CHAIN_RE_SUPPLIES`；`CHAIN_RE_INDUSTRY_TECH` / `_TALENT`；服务机构人才流动、竞争；`SVC_RE_ENTERPRISE` / `GOV` / `RESEARCH` / `TECH` / `TALENT` / `POLICY` | 不进表 |
| 常量有、没有 INSERT | L03 `graph_project` 的 `supplies`（写明本单不造边）；`svcgraph` 的 `supplies`、`depends_on`（只在常量里，没有构造函数） | 不进表 |
| D 档读图 | 产业链、企业、政策的 D 档会读图，L06 没有列出三元组。产业服务 `GET /svc/graph` 读的是 DWD hang，不查 Nebula | 不进表。三元组待确认见 §6 |
| 同图未配对 | seq191、194 把企业、专家、文献、关键词放在同一张图，没有写两两端点。seq511 写论文、专利、资金、人才流动，没有写关系名；资金不是 14 类实体。seq339 的数据来源、服务模块、应用场景不是 14 类实体 | 不拆行 |

---

## 5. 展示清单 14 类实体归并

类型与定义以 v1.2 §三为准。归并规则以总控为准：技术只收论文、专利、项目。`technology` 技术点不并进技术。

| 实体ID | 中文名 | 归并 |
|---|---|---|
| enterprise | 企业 | **企业** |
| institution | 机构（科研机构、高校、院所、实验室） | **科研机构** |
| paper | 论文 | **技术** |
| patent | 专利 | **技术** |
| project | 项目 | **技术** |
| person | 人员/专家 | **人才** |
| policy | 政策 | **政策** |
| technology | 技术点 | **不进七要素建图** |
| field | 领域 | **不进七要素建图** |
| topic | 主题 | **不进七要素建图** |
| dataset | 数据集 | **不进七要素建图** |
| event | 科技事件 | **不进七要素建图** |
| activity | 科技活动 | **不进七要素建图** |
| innovation_carrier | 创新载体 | **不进七要素建图** |

14 类里没有产业链环节，也没有服务机构。v1.2 §三写明：服务机构不新增（seq535 判为机构卡片统计后剔除）；产业链/产业环节只在 seq94 提及，不足以定义实体，暂不单列。这两类的算法 tag（`chain`、`segment`、`industry`、`service`、`service_institution`）留在第 3 节，不在这里补实体。

---

## 6. 待确认（真源没写死）

三元组上缺关系名、终点或方向的行：Q42、Q43、Q44、Q45、Q46、A03、A04、A05、A06、A07、A08、A09、A10、A11、A12、A13、A14、A15、A16、A18、A19、A20、A21、A36。

表名没写死、但三元组本身已写明的：

- A02、A27：环节上下游，没有表名
- A07–A16：企业 B/C 档没有业务来源表名。L06 只写对端要在 `enterprise_base` 或图上已有稳定 ID；ADS 表名写了 `graph_edge`，那是落表不是边的业务来源
- A18–A20：政策挂边没有业务来源表名
- A23–A26：只写「DWD chain 表 / node 表 / 企业表 / 机构表」
- A35、A36：只写「机构数据源」

另外没有形成一行、因此不进表的缺口：D 档读图的三元组；seq191/194 同图实体两两怎么连；seq511 流动关系的端点与关系名。
