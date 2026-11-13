# TS-L2-M10-GRAPH-SIGNOFF-ALGO · 维护管理 · 维护技术图谱 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-13
- 对象：`sdd/l2/TS-L2-M10-GRAPH-ARCH.md`（主审 §4 全景读图叠加人工层、§2 关系类型/边身份、§6 35-3、§9.7 METRIC 预期；交叉 §1/§3 与 §7）
- 监管：`human:刘剑锋`
- 范围：只读核对。不改被审稿件，不动 task-registry / 指标注册表，不 git、不连库、不跑脚本（含单测）
- 事实源与核对代码：
  - 读图：`repos/lumen-algo-py/lumen_common/algorithms/tech_graph_read.py`（下称 **read**）、`repos/lumen-algo-py/tests/test_tech_graph_read.py`（下称 **test**）、`repos/lumen-algo-py/lumen_algo_service/views/tech_graph_read.py`
  - 写链：`repos/lumen-algo-py/vendor/entan-py/api/tech_graph_maintain_routes.py`（下称 **routes**）、`repos/lumen-algo-py/vendor/entan-py/scripts/mysql/tech_graph_maintain.sql`（下称 **DDL**）、`repos/lumen-algo-py/vendor/entan-py/scripts/seed_tech_graph_maintain.py`（下称 **seed**）
  - Java 形状层：`repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/SituationPanoramaService.java`（下称 **PAN**）、`TechGraphReadAdapter.java`、`JdbcPanoramaScores.java`
  - 分数：`repos/lumen-algo-py/scripts/seed/seed_technology_panorama_score.py`（下称 **SCORE**）
  - 已签收先例：`科学技术全景-DS02/sdd/l2/TS-L2-DS02-ARCH.md`、`TS-L2-DS02-GRAPH-METRIC.md`、`TS-L2-DS02-READ-PY-L01.md`；`会签/TS-L2-M10-ENT-SIGNOFF-ALGO.md`、`TS-L2-M10-ENT-METRIC.md`
  - 规约：`agent-delivery/data-lineage-policy.md`（D9）、`agent-delivery/产品实现规程.md` §4.2.4、`.cursor/rules/00-team-constitution.mdc`
  - 决策：`sdd/简报/2026-11-13-维护技术图谱-需规分句闭合.md`（卡 1B / 2A / 3A）；`工程过程/04-系统集成/07-图数据库集成/WBS-全景维护与知识图谱分工-背景.md`（S4/S5）

## 结论

**有条件同意，暂不签收。** 架构方向（工作集只读叠加、不写 Nebula、人工层只追加、种子边不造口径映射）在算法/指标立场站得住；但 §4 目前的写法有 5 处会直接破坏已签收的全景读图语义或让「全景回显人工改动」静默失效，必须改稿后才能作为实现单输入：

- 人工边在读图出口写了 `source: "manual"`，而读图 `relations[].source` 已经是**起点 id**（不是来源标记），照写会覆盖端点、打断整张图；
- 人工边端点身份空间（`technology_id` ↔ `technology_node_id` / `tm:{id}`）未定义，边接不上点；
- 「Java 预计不改」不成立——真正做裁剪的是 `SituationPanoramaService.assemble`（200 点裁剪、子域过滤、固定字段白名单），新点与 `overlay.status` 到不了页面；
- 叠加只写了「`_read` 的 `_finish` 之前」，未覆盖 `_read` 的两条 return 分支，也未定义「选中新点」与「选中已删点」两条分支；
- D9 保护条款不完整：人工值未要求标「人工」、未写死不得进入 `weight`/`strength`/S4 分数，操作类计数（impact/Nebula 隐藏数/版本 stats/回滚预览/publish results）也未并入 ENT 的 DN-A03-09 建议豁免。

另附 6 条应修、3 条非阻断建议。事实层面发现 5 处行号/描述需更正（见「事实修正」）。

## 条件表

| 编号 | 级别 | 条件（改稿哪一节、改成什么） | 证据（文件:行号） |
|---|---|---|---|
| ALGO-C1 | 必修 | **§4「人工边」行：`source: "manual"` 与读图字段冲突，必须换字段名。** 读图 `relations[]` 的 `source`/`target` 是起点/终点 id，不是来源标记；人工边只能新增独立字段（如 `edgeSource` / `origin: "manual"`），`source`/`target` 仍放端点。人工边 `id` 也须用独立前缀（如 `tech_manual:...`），不得复用 `tech_rel:{src}:{dst}:{kind}:{index}`，否则与存量关系 id 撞。 | `repos/lumen-algo-py/lumen_common/algorithms/tech_graph_read.py:291-300`；`repos/lumen-svc-platform/.../SituationPanoramaService.java:472-484`；稿 `:108` |
| ALGO-C2 | 必修 | **§4「人工边 / 对上存量点」：补端点身份空间与端点节点并入。** 需写死：`graph_tech_edge.src/dst` 存 `technology_id`，读面输出前按 master `external_ids` 映射成存量点的 `technology_node_id`；新点为 `tm:{technology_id}`。人工边两端节点必须一并进入 `nodes`（存量端点用 `_one_point_ngql` 补点，新端点从主表建），否则 Java 会因「关系端点不在 nodes」整条删边。另：§4 只写 `external_ids.technology_node_id`，但 seed 对重名点合并写了 `all_technology_node_ids`，映射必须同时匹配单值与数组，并在 `technology_node_id` 为空时回退 `legacy_vid`。 | 稿 `:103`、`:107`、`:108`；`repos/lumen-algo-py/vendor/entan-py/scripts/seed_tech_graph_maintain.py:163-170`；`read.py:181`、`:229-236`；`SituationPanoramaService.java:186-196` |
| ALGO-C3 | 必修 | **§4「出口形状 / 影响已签收」：删掉「Java 预计不改」，改为对 `SituationPanoramaService` 的显式契约。** `TechGraphReadAdapter` 确为 84 行透传，但页面实际形状由 `assemble` 决定：未选点时先 `restrict`（子域 `technology_node_ids` 会滤掉 `tm:` 新点）再 `cap` 200（新点排尾会被截掉）；选中时 `keepThenCap` 只保留已在 nodes 里的 keep 点；结果只回 7 个固定键，`overlay.status` 会被丢弃。必须二选一并写进 §4：① Java 侧改 `assemble`（放过 `overlay`、新点优先占配额、子域过滤对人工层有明确规则）；② 或把「新点必须排在 nodes 前部 / 子域筛选下不显示人工层 / 叠加状态走响应头或既有字段」写成硬契约。否则「全景能看到人工改动」与 PRODUCT-C8 的降级提示都无法落地。 | 稿 `:110`、`:111`、`:114`；`SituationPanoramaService.java:99-105`、`:151`、`:172`、`:193`、`:205-224`、`:309-328`；`TechGraphReadAdapter.java:1-84` |
| ALGO-C4 | 必修 | **§4「落点」：叠加必须写在 `_read` 的**两条** return 分支，并补两条选中分支。** 现 `_read` 在未选点时于 `read:561-562` 直接 `_finish`，选中时才走到 `:570`；只写「`_finish` 之前」会让首屏（200 点总览）不过滤已删点、不追加新点。需明确：未选点分支也要做「已删点剔除 + 新点追加 + 关键词匹配 + 200 上限重算」；选中分支补「选中 `tm:{id}` 新点 → 返回该点与其人工边」「选中已删存量点 → 清空 nodes/relations/paths/records 并 `emptyReason=GRAPH_EMPTY`」。追加后超 200 时须重设 `truncated.nodes=true`，并写清新点是否优先占配额（与 C3 的 Java 裁剪一致）。 | `read.py:556-570`（`:561-562` 早返回、`:570` 选中返回）；稿 `:99`、`:105`、`:107` |
| ALGO-C5 | 必修 | **§4/§8/§9.7：把 D9 保护条款写全，并收窄「METRIC 全 N/A」的表述。** 至少写死五句：① 人工强度 `strengthManual` 永不进任何指标公式，不填 `weight`，不加进点 `strength`（`weighted_degree`），不参与 S4 影响力/中心度/路径优先级；② 全景显示人工值时必须标「人工」，且该数字**不得**挂 `M_TECH_EDGE_STRENGTH` / `M_TECH_GRAPH_105_1` 等 auto 口径 ⓘ（若是编辑值回显，ⓘ 只能解释「人工编辑值，非指标」）；③ 存量点 `weight`（`relation_confidence_score`）与 `strength`（`weighted_degree`）是图属性、非注册指标，本叶不改其身份，DS02 已留的「加权度身份」问题（`DS-02-METRIC-OPEN-L01`）不由本叶顺手拍板；④ 新点无度、无 S4 分数，显示空不补 0；⑤ 操作类计数（35-3 impact、Nebula 隐藏关系数、版本 stats、回滚预览分组计数、publish results）并入 ENT 的 DN-A03-09「操作回执类计数豁免 D9 ⓘ」建议范围，METRIC 分册不得写成无依据的 N/A。 | 稿 `:108`、`:182`、`:195`；`gkx-orchestration/agent-delivery/data-lineage-policy.md` §2.3（D9）；`会签/TS-L2-M10-ENT-SIGNOFF-ALGO.md` §4 / N1；`TS-L2-M10-ENT-METRIC.md:38-42`、`:27-36`；`read.py:194-197`、`:300-306`；`routes:511-522`；`SituationPanoramaService.java:249-257` |
| ALGO-C6 | 应修 | **§4「属性覆盖」：主表空值不得覆盖 Nebula 已有值。** seed 主表只写 `name_cn/name_en/external_ids`，不写 `description`（且未写 `category`）；若按「名称/描述用主表值覆盖」无条件覆盖，会把已签收全景页上的 Nebula `description` 全部冲空。改为「主表值非空才覆盖，空则保留 Nebula 值」；`name_en` 同理。另 `importance_level` 有 DDL 默认 `中`，seed 点会带出默认值，需说明这是新建/默认值而非人工评定，避免被当成权威等级。 | `seed_tech_graph_maintain.py:235-240`；`DDL:7-21`（`importance_level DEFAULT '中'`）；`read.py:181-193`；稿 `:104` |
| ALGO-C7 | 应修 | **§4「对上存量点 / 新建点」：改名后的存量点要能被关键词搜到。** 现有读图关键词是 Nebula `name_zh/name_en CONTAINS` 预过滤，叠加再把显示名换成主表值；维护页改名后，全景按新名搜不到（Nebula 仍是旧名）。要么在有关键词时同时用主表 `name_cn/name_en` 查一遍、把命中的存量点并入结果；要么在 §4 明写「改名后按新名搜索暂不生效」的已知限制并交 PRODUCT/DS02 监管人确认。 | `read.py:221-226`、`:239-245`；稿 `:103`、`:104`、`:107` |
| ALGO-C8 | 应修 | **§4「落点」：叠加读库必须锁死 demo 工作集，禁止回落产线库。** `lumen_common.db` 的默认库是 `gkxlumenx_dwd/ads`（产线名），而本工作集是 `demo_gkxlumenx_dwd/ads`。需写明解析顺序：`GKX_M10_ENT_*_DB` → `ENTAN_MYSQL_*_DB` → `demo_gkxlumenx_*`（与 routes 单写者一致）；解析结果不是 `demo_gkxlumenx_*` 时按「叠加不可用」降级并告警，绝不读 `gkxlumenx_*`。 | `repos/lumen-algo-py/lumen_common/db.py:36-38`；`routes:115-120`；`repos/lumen-algo-py/k8s/api.yaml:38-39`；稿 `:99` |
| ALGO-C9 | 应修 | **§4「影响已签收」：给出「叠加关闭」的可执行开关。** 现有单测只注入假 Nebula 会话（无 MySQL），若叠加默认尝试连库，会引入连接超时/网络依赖，「逐字节一致」无法保证。需补：`read_graph` 增加 `overlay_factory`（对齐 `session_factory`）或环境开关，单测默认关闭叠加、输出与今天一致；生产默认开启。并明确开关关闭时**不**输出 `overlay` 字段。 | `test:138-180`、`:241-270`；`read.py:573-588`；稿 `:114` |
| ALGO-C10 | 应修 | **§2「边身份 / 删除」与 §4「删除的存量边」：墓碑键的空间、编码、方向要写死。** `graph_tombstone` 主键是 `(object_type, object_id VARCHAR(128))`，一条边只能用一个字符串。需定：键用 `technology_node_id` 空间（与 Nebula 边端点同空间）还是 `technology_id`（若后者，读面必须先映射）；无向边存规范化的无序对还是两个方向各存一行；`object_id` 如何编码（如 `src|dst|rel_type`）与截断规则。否则「按存量键过滤 Nebula 边」无法实现。 | `DDL:74-81`；`read.py:271-272`（无向 MATCH）；稿 `:74`、`:77`、`:106` |
| ALGO-C11 | 应修 | **§4「人工边」：补时间范围与 `timeline` 的语义。** 36-3 要求时间范围，但读面 `timeline` 由 `relations[].year` 聚合；人工边若不写年份则不进时间轴，若写年份又会改变已签收字段。需二选一并写明：① 人工边带 `timeRange`/年份并明确进入 `timeline`（标注为人工层事件、不是指标）；② 人工边不进 `timeline`，时间范围只在关系标签/详情显示。不可留给实现自行决定。 | `read.py:300-306`、`:499-516`；`SituationPanoramaService.java` `timeline()`；稿 `:108`、`:110` |
| S1 | 建议 | **§2/§6 36-3：`relationTypeOptions` 不得驱动新增关系下拉。** 读图 `relationTypeOptions` 会同时含存量英文码与三枚举；若前端拿它填新增下拉，会违反 36-3 的封闭三枚举。新增下拉固定 `{包含,依赖,促进}`，`relationTypeOptions` 只用于图例/筛选。同意 PRODUCT-C9 的「只读显示字典」，但必须写死不进三枚举、不进指标。 | `read.py:533-539`；稿 `:75`、`:146`；会签 `TS-L2-M10-GRAPH-SIGNOFF-PRODUCT.md` PROD-C9 |
| S2 | 建议 | **分数种子不得改从叠加后的读图输出取数。** `SCORE` 现从 Nebula 直接分页扫描建行；若后续图省事改成消费 `POST /internal/tech-graph/read` 的结果，`tm:` 新点会拿到 mock 的 `influence/centrality/path_priority`，直接违反「新点无 S4 分数」。建议在 §4/§9.7 加一句约束：S4 分数种子只从 Nebula 技术点扫描取 `subject_id`。 | `repos/lumen-algo-py/scripts/seed/seed_technology_panorama_score.py:268-342`、`:53-68`；稿 `:195` |
| S3 | 建议 | **§4 选中已删点：可选区分空态原因。** 返回 `GRAPH_EMPTY` 可以，但前端无法区分「图真的空」与「该点已被删除」。可选加 `emptyReason=GRAPH_NODE_DELETED`（不改已有 `GRAPH_EMPTY` 语义），便于提示「该技术点已删除，请刷新」。非阻断。 | `read.py:551-553`；稿 `:105` |

## 分节说明

### 1. §4 全景叠加人工层（主审）

**1.1 落点与分支（ALGO-C4）。** `_read` 有两条出口：未选点在 `:561-562` 直接 `_finish`，选中点在 `:570` 才 `_finish`。文档只说「Nebula 结果组装完、`_finish` 之前」，实现者很容易只改选中分支。但首屏总览（用户不选点时）同样必须剔除已删点、追加新点、让新点可被关键词搜到，否则 34-5 的编号只在维护页可见。建议把 §4 的表格第一列改成「未选点 / 选中点」两栏，或明确「以下规则同时作用于 `_read` 的两个 return 分支」。

**1.2 `source` 字段冲突（ALGO-C1，最硬的一条）。** 读图关系对象里 `source`/`target` 就是边两端：
```python
rel = {
    "id": f"tech_rel:{src['id']}:{dst['id']}:{kind}:{index}",
    "source": src["id"],
    "target": dst["id"],
    ...
}
```
Java `normalizeRelation` 也从 `source`/`target` 取端点。稿 §4 写「人工边……追加 `source: "manual"`」，若照做，`source` 变成字符串 `"manual"`，端点丢失，Java 会把该边过滤掉（端点不在 nodes），或前端画出错误边。必须改成新增字段（`edgeSource`/`origin`），并保留 `source`/`target` 为端点 id。这与 `graph_entity_edge.source` 列的命名无关——那是 DB 列，不是读图契约。

**1.3 身份空间（ALGO-C2）。** `graph_tech_edge` 是新表（DATA 尚未定列），写链主键是 `technology_id`；读图存量点 id 是 `technology_node_id`，新点 id 是 `tm:{technology_id}`。三套空间必须在 §4 写清映射：
- 存量点：`technology_id` → master `external_ids.technology_node_id` → Nebula 读图 `id`；
- 新建点：`tm:{technology_id}`，选中请求也按这个串解析；
- 人工边两端：按上述规则映射后再拼关系；两端节点必须进 `nodes`（存量端点补查、新端点建节点），否则 `SituationPanoramaService:186-196` 的端点裁剪会删边。

另：seed 对重名点合并时保留 `all_technology_node_ids`（`seed:169-170`），只认单值 `technology_node_id` 会漏掉被合并的其余存量点。PRODUCT-C10 已提「`tm:` 选中映射」，本条是它的算法侧补齐。

**1.4 Java 形状层（ALGO-C3）。** 稿 §4 说「Java `TechGraphReadAdapter` 透传（84 行，无字段映射），预计不改」。`TechGraphReadAdapter` 确实透传，但页面拿到的形状由 `SituationPanoramaService.assemble` 决定：
- 未选点：先 `restrict`（若请求带子域 `technology_node_ids`，`allowed` 不含 `tm:` 新点，新点被滤掉），再 `cap(nodes, 200)`（取前 200，追加在尾部的新点被截掉）；
- 选中点：`keepThenCap` 只保留已经出现在 `nodes` 里的 keep 点，不会补拉缺失端点；
- 结果 map 只放 7 个固定键（`nodes/relations/keyPathOptions/timeline/listRecords/relationTypeOptions/factorItems`）+ `truncated/emptyReason`，`overlay` 字段被丢弃。

所以「Java 不改」这个结论至少对 `SituationPanoramaService` 不成立。要么改 Java（放过 `overlay`、让新点优先占配额、定义子域筛选下人工层的行为），要么把「新点排前 200 / 子域筛选时不显示人工层 / 叠加状态走响应头」写成硬契约。PRODUCT-C8 要求「叠加不可用时给用户可见提示」，若 Java 丢掉 `overlay.status`，产品这条也落不了地。

**1.5 D9 与指标口径（ALGO-C5）。** 详见「给 METRIC 分册的输入」一节。核心三句：人工强度是编辑层字段，不是指标；存量 `weight`/`strength` 是图属性，不改身份；计数类是操作回执，走 DN-A03-09 豁免而不是「默认 N/A」。

**1.6 属性覆盖的空值问题（ALGO-C6）。** seed 主表只写 `name_cn/name_en/external_ids/status`，不写 `description`。读图现在会带出 Nebula 的 `tech_point.description`；若叠加无条件「用主表值覆盖」，seed 点的描述会被 `NULL` 冲掉，已签收页面的描述信息丢失。改成 `COALESCE(master.description, nebula.description)` 语义（非空才覆盖）。`name_en` 同理。

**1.7 关键词与新点/改名（ALGO-C7）。** 新点「按关键词同样匹配」方向对；但存量点改名后，Nebula 预过滤仍按旧名，叠加只改显示值，用户按新名搜不到。要么关键词同时查主表并 union，要么写明限制。这条和 PRODUCT-C10 的「搜得到但点不开」是同一类问题（搜索与 id 空间），建议一起改。

**1.8 删除语义（路径 / 时间轴 / 存量边）。** 结论：**方向正确，不需要换做法**。
- 「路径含已删点整条去掉」对路径播放是对的：`keyPathOptions` 是 `tech_path_step` 的有序点序列，缺中间点就不成路径；若截成两段再拼，会造出一个不存在的 `path_id`，与 `M_TECH_PATH_PRIORITY` 的 `subject_id`（path id）对不上，属于造口径。整条去掉最干净。
- 「删除存量边按墓碑过滤」对时间轴也是对的：`timeline` 由 `relations[].year` 聚合（`read:499-516`），边被过滤后其事件自然消失，无需单独处理 `timeline`。
- 需要补的是：人工边端点若指向已删点，也必须一并过滤（不能只在 Nebula 关系上过滤）；以及墓碑键的空间/编码（ALGO-C10）。35-4 的级联删边已经覆盖 `graph_tech_edge`，但读面仍应做防御性过滤，防止回滚/重灌后出现悬空人工边。

**1.9 降级（ALGO-C3/C8）。** 「MySQL 不通或表缺失 → 返回 Nebula 原结果 + `overlay.status=unavailable`，不 503」这个降级方向同意：全景页已签收，不能因维护层故障整页不可用。但落地有两个前提：① Java 要把 `overlay.status` 传到前端（C3）；② 读库必须锁 demo 工作集，不能因环境变量缺失读到产线库（C8）。另建议把「叠加查询失败/表缺失」分开记 warning，便于定位。

### 2. §2 关系类型与种子边（会签关注点 3）

**同意「种子边保留 Nebula 英文关系码、不映射三枚举」。** 理由：存量英文码与三枚举没有权威对照表，硬映射就是造口径；`M_TECH_EDGE_STRENGTH` 等指标也不因显示文案改变。三点边界：
1. 三枚举只约束 `add_edge` 新增关系，不能反过来约束存量边的显示与筛选（PRODUCT-C9 要求加只读显示字典，我同意，但字典不得成为新的关系类型枚举，也不得进入 `relationTypeOptions` 驱动新增下拉——见 S1）。
2. 维护页 `current` 读 `graph_tech_edge` 时会看到英文码；前端要标「存量」。这不影响指标。
3. 删除存量边用「墓碑 + 存量键」，键的空间和方向见 ALGO-C10。

### 3. §6 35-3 影响计数（会签关注点 6）

「impact 扩：技术点间边数 + 全景中将隐藏的存量关系数（Nebula 只读计数，失败 null，不挡删除）」方向同意，属于删除前预检，不是指标，走 DN-A03-09 操作计数豁免（ALGO-C5）。两点要求：
- Nebula 计数必须与 §4 删除过滤同口径（同一无向匹配、同一证据级别范围），否则确认框数字与实际隐藏数不一致；
- 计数失败返回 `null` 而不是 0（不要用 0 冒充「没有关系」），前端显示「无法统计」。

### 4. §3 / §7 与算法无直接冲突的部分

- §3 回滚「差异审计 + 快照还原」是审计口径，不产生指标；版本 `stats` 是操作计数，并入 DN-A03-09。
- §7 的错误码与计数上限不涉及指标口径，不持异议。
- 需提醒 DATA/API：稿里「kind=rollback 的变更集」「版本类型（保存/回滚/种子/ENT 发布）」在现有 `graph_change_set` / `graph_version` DDL 中没有 `kind/type` 列（`DDL:24-34`、`:55-64`），版本列表要显示类型需补列或从 label/关联推导。这不在算法条件内，但会影响 40-4 的「逐条可追溯」呈现，请 DATA 分册收口。

### 5. §9.7 METRIC 预期（会签关注点 7）

**「全 N/A」只能有条件成立，不能照抄。** 逐项：
- 人工强度 `strengthManual`：N/A，但必须有「永不进公式 + UI 标人工 + 不挂 auto 口径 ⓘ」三句（ALGO-C5）。
- 新点 `strength`/S4 分数：空，不补 0；不得为人工边重算 `weighted_degree`。
- 存量 `weight`/`strength`：沿用 DS02 身份，本叶不改；`weight` 是 `relation_confidence_score` 图属性，不新增指标。
- 计数类：impact、Nebula 隐藏数、版本 stats、回滚预览、publish results → 建议 DN-A03-09 一次裁「操作回执类计数豁免 D9」，范围写全。
- 不得把本叶任何数字挂到 `M_TECH_GRAPH_STRUCT` / `M_TECH_EDGE_STRENGTH` / `M_TECH_PATH_CENTRALITY` 等 IPC4 口径上（DS02 GRAPH-METRIC 已定这些口径的对象不是 `tech_point`）。

## 给 METRIC 分册的输入（预期挂接表）

| 叶 / 数字 | 挂接 | 依据 |
|---|---|---|
| 34–40 节点/边/属性/版本 | 无 `metric_id`；不新注册、不改 D4 | 需规 34–40 无统计口径；本叶只产生图与变更记录 |
| 人工强度 `strengthManual`（36-3 回显） | N/A；**永不进 `M_TECH_*` 公式**；UI 标「人工」，不得挂 auto 口径 ⓘ | ENT-METRIC §3；ENT-SIGNOFF-ALGO §4/N1；A03 204/220/R-A03-08 |
| 新点 `strength` / S4 三个分数 | 空（不补 0）；无 `subject_id` 行 | `read:194-197`；`JdbcPanoramaScores` 无行返回空；DS02 ARCH §7 |
| 存量 `weight` / `strength` | 沿用已有身份，本叶不新挂、不改 | DS02 GRAPH-METRIC §1/§3；本叶只叠加显示 |
| 35-3 impact 计数、Nebula 隐藏关系数 | 操作预检计数，并入 DN-A03-09 建议豁免 | ENT-METRIC §2；`routes:511-522` |
| 版本 stats、回滚预览分组计数、publish results | 操作回执计数，并入 DN-A03-09 建议豁免 | ENT-METRIC §2；`routes:852-882` |
| 路径优先级（`keyPathOptions` 被删路径） | 沿用 `M_TECH_PATH_PRIORITY`（D4 mock）；被过滤路径不显示，不另算 | DS02 ARCH §7；`read:444-496` |

前置注记沿用 ENT：`M_TECH_GRAPH_105_1` 公式签署状态、`M_TECH_ENTITY_TOP5` 与 DS 映射歧义由 METRIC 分册按原注记复核，本页不重开。

## 事实修正

以下为只读核对发现的行号/描述偏差，非阻断，但建议改稿时一并更正：

1. **§0 35 行 `routes:933–942 / :1043–1051`** → 现文件 `delete_node` 软删+墓碑在 `routes:946–955`，ADS 级联删边在 `routes:1034–1041`。`911–919`（`update_node`）核对属实。
2. **§1-6 `routes:840` 写死 `"py"`** → 版本行插入在 `routes:843–845`，`"py"` 在 `:844`。
3. **§1-7 `change_log` `before` 恒空 `routes:770–775`** → `change_log` 插入在 `routes:772–776`。
4. **§4「Nebula 读是无向 MATCH，read:276」** → 无向 MATCH 在 `read:271-272`（`:276` 是 RETURN 的列）。
5. **§4「Java `TechGraphReadAdapter` 透传（84 行，无字段映射），预计不改」** → 适配器 84 行属实，但页面形状由 `SituationPanoramaService.assemble` 裁剪/过滤/白名单决定，不能据此得出「Java 不改」（详见 ALGO-C3）。
6. 已核对属实：`read:181`（`id` = `technology_node_id` 或 `vid`）、`read:556-570`（`_read`）、`D DL:19`（`uk_name_cn`）、`seed:163-170`（`external_ids`）、`k8s/api.yaml:38-39`（DWD/ADS 库）、`TechGraphReadAdapter` 84 行、helm 无 `GKX_NEBULA_MAINTAIN_SPACE`。
7. **§7「重名……422（validate 与 changes 同一套校验）」** → 现 `_validate_structure` 对 `update_node` 只校验 `name_cn` 非空与 `importance_level` 枚举，不查重名（`routes:715-726`）；改名撞 `uk_name_cn` 会抛 DB 异常落到 500。新增 `add_node` 的查重需在 API 册写清；`update_node` 改名查重也需补，否则 §7 的 422 承诺不成立。

## 建议（非阻断，不设闭合时点）

- **S1**：`relationTypeOptions` 只做图例/筛选，不驱动新增关系下拉；存量英文码可加只读显示字典，但不进三枚举、不进指标。
- **S2**：S4 分数种子继续从 Nebula 直接扫描取 `subject_id`，不得改成消费叠加后的读图输出，避免 `tm:` 新点被灌 mock 分数。
- **S3**：选中已删点可选返回独立空态原因（如 `GRAPH_NODE_DELETED`），便于前端提示。

## 签收边界

- 本页只读核对，不改被审稿、不改 task-registry、不动指标注册表、不 git、不连库、不跑单测。
- ALGO-C1～C5 为必修；闭合（改稿或明确落到 API/DATA/FE 实现单并回填本页）后，算法可转无条件同意。ALGO-C6～C11 可随改稿或实现单吸收；S1～S3 非条件。
- 本页不代替 `human:淮政玮` 对已签收全景读图（`TS-L2-DS02-READ-PY-L01` / `TS-L2-DS02-SDD`）的知会；§4 动 read 前仍须按稿要求拿到知会回执。
- 指标口径的最终确认归 METRIC 分册与监管人；本页只给输入，不代注册、不代签收。

## 起草方回应（2026-11-13 `agent:arch-agent`，稿 v2）

| # | 结论 | 落稿 |
|---|---|---|
| ALGO-C1 | 采纳，`origin: "manual"`，id `tech_manual:{edge_id}` | §4.2「人工边」 |
| ALGO-C2 | 采纳：端点映射（含 `all_*` 与 `legacy_vid` 回退）、另一端节点并进 nodes | §4.2「id 映射」「人工边」 |
| ALGO-C3 | 采纳，取①：Java 透传 `overlay`；新建点排前占配额；子域筛选下不显示新建点，写成已知限制 | §4.4 |
| ALGO-C4 | 采纳：两条分支、选中新建点、选中已删点返回空图、先合并再截断 | §4.1、§4.2 |
| ALGO-C5 | 采纳，五句全写 | §9 |
| ALGO-C6 | 采纳：非空才覆盖；种子点 `importance_level` 写空 | §4.2「属性覆盖」、§2「种子」 |
| ALGO-C7 | 采纳，有关键词时额外按主表名称匹配 | §4.2「关键词」 |
| ALGO-C8 | 采纳 | §4.1 |
| ALGO-C9 | 采纳，`overlay_factory`；关闭时不输出 `overlay` | §4.1 |
| ALGO-C10 | 采纳；改为软删 `graph_tech_edge` 后不需要墓碑键编码 | §2「删除」 |
| ALGO-C11 | 采纳，选②：人工边不进 timeline，时间范围放 `timeRange` | §4.2「人工边」 |
| S1 | 采纳 | §6 36-3 |
| S2 | 采纳 | §4.6 |
| S3 | 不采纳（本期）：Java 会重建 `emptyReason`，要区分「已删除」得同时改 Java 与前端，收益小；保持 `GRAPH_EMPTY` | — |
| 事实修正 5 处 | 采纳，行号已改 | — |

请 algorithm-agent 复核，在本页末追记「复核：条件已闭合 / 未闭合项 …」。

## 复核（2026-11-13 `agent:algorithm-agent`）

复核对象：`TS-L2-M10-GRAPH-ARCH.md` v2 全文 + 上节「起草方回应」。逐条对照 v2 §1 / §2 / §4 / §9 与代码（read / routes / DDL / seed / `SituationPanoramaService`）。
程序性说明：只读核对；未改稿、未动 registry、未 git、未连库、未跑脚本/单测。

### 逐条结论

| 条件 | 结论 | 复核说明 |
|---|---|---|
| ALGO-C1 | **闭合** | §4.2「人工边」已改 `id=tech_manual:{edge_id}`、`source`/`target` 保持端点、另加 `origin:"manual"`。read `_relation`（:291-300）与 Java `normalizeRelation`（:472-484）都要求 source/target 为端点，现不再冲突。 |
| ALGO-C2 | **未闭合** | 端点映射、`all_*` 并入、另一端节点并进 nodes 已写；但 `legacy_vid` 回退写「去掉 `tech_point:` 前缀」与读图 id 规则不一致：read 的节点 id = `technology_node_id or vid`（:181、:213-218），无 technology_node_id 时 id 是**完整** `tech_point:xxx`，去前缀得到 `xxx` 匹配不上。改法：§4.2「id 映射」把 `legacy_vid` **原值使用**（或与 read:181 完全同规则 `tnid or full_vid`），不要无条件去前缀；同时 `_points_by_ids_ngql`（:239-245）只按 `technology_node_id` 匹配，VID-only 端点/改名点补读会漏，需扩成 `technology_node_id IN (...) OR id(v) IN (...)`（参照 `_one_point_ngql:229-236` 的 vid 分支）。另需一句话定「一个主表行映射到多个全景 id 时，边端点取主 `technology_node_id` 还是全部」，避免重边。 |
| ALGO-C3 | **闭合** | §4.4 已作废「Java 不改」并写三处改动。核对：`maps()` 用 `copy` 全量拷贝（:553-570），`origin`/`strengthManual`/`timeRange`/`category`/`importance` 能穿过；`keepThenCap` 先钉选中点+关系端点（:389-415），人工边端点并入后能留下；`restrict`（:309-328）按 `allowed` id 过滤，`tm:` 不在学科字典内会被滤掉，与稿中「子域筛选下不显示新建点」一致。补充：Java `overlay()` 的 `put(..., "centrality", true)`（:249-257、:532-540）会给 `tm:` 新点写 `centrality: null`；这是「空」不是 0，符合 D9，请在 JAVA-IMPL 用例断言前端按 null 显示空。 |
| ALGO-C4 | **闭合** | §4.1/§4.2 明写两条分支（read:561-562、:570）、选中 `tm:`、选中已删点清空、先合并再截断并置 `truncated.nodes`；与 `_load_points` 200 上限（:246-250）一致。提示：§4.2 标题写「已删存量点」，35 也能删新建点，建议改成「已删点（含新建点）」并覆盖选中 `tm:` 已删。 |
| ALGO-C5 | **闭合** | §9 五句齐全。已核对 read `_point_node`（:194-197，仅 `weighted_degree`→strength）与 `_relation`（:300-306，`relation_confidence_score`→weight），人工 `strengthManual` 不进这两处、也不进 S4；「全 N/A」已收窄为「不注册 metric_id，按 DN-A03-09 豁免」。 |
| ALGO-C6 | **闭合** | §4.2 非空才覆盖；§2 种子 `importance_level` 写空；DDL `:11` 该列可空、`DEFAULT '中'` 仅在省略列时生效，写 NULL 不吃默认。 |
| ALGO-C7 | **闭合（附实现注意）** | §4.2 已加主表名称匹配 + `_points_by_ids_ngql` 补读。注意：① 补读必须传**空 keyword**，否则 `_points_by_ids_ngql` 仍加 Nebula 旧名 `CONTAINS`（:239-245），改名点取不到；② VID-only 点同 C2，需扩 id 匹配。 |
| ALGO-C8 | **闭合** | §4.1 已定解析顺序 + `demo_gkxlumenx_` 前缀闸门 + 不合规即降级，足以防止回落 `gkxlumenx_*`（db.py:36-38）。提示：写者用 `ENTAN_MYSQL_*`（routes:115-120），读者用 `LUMEN_ALGO_MYSQL_*`（k8s/api.yaml:38-39），建议读者也接受 `ENTAN_MYSQL_*` 兜底，非阻断。 |
| ALGO-C9 | **未闭合** | §4.1 同时写「不传时，生产环境按下面的规则建连接」与「单测默认关闭叠加」，两者矛盾：生产 view 现在就是 `read_graph(payload)`（views/tech_graph_read.py:21），现有单测也不传 factory（tests 中 `read_graph({}, session_factory=...)`）；按「不传→生产建连接」实现，单测会尝试连 MySQL，「逐字节一致」不成立。改法：把开关语义写死为「`overlay_factory=None` = 关闭叠加、不输出 `overlay`；生产 view 显式传真实 factory（或 env 显式开启）」，删掉「不传时生产建连接」。 |
| ALGO-C10 | **闭合** | 已改为 `graph_tech_edge.status='deleted'` 软删 + 无序对双方向过滤，绕开墓碑拼接串。残留（不阻断）：同一 `(src,dst,rel_type)` 的多条 Nebula 关系会被一起隐藏；未进 `graph_tech_edge` 的 Nebula 边无法从维护页删，建议在 §2/§4.2 明写为已知边界。 |
| ALGO-C11 | **闭合** | §4.2 人工边时间放 `timeRange{from,to}`、不填 `year`；`_timeline` 只读 `year`（:499-516），时间轴口径不变。 |
| S1 | **闭合** | §6 36-3 下拉固定三项、不从 `relationTypeOptions` 取；三枚举封闭仍留 P2 给监管人。 |
| S2 | **闭合** | §4.6 明写分数种子只扫 Nebula `subject_id`。 |
| S3 | **接受不采纳** | 非条件；`GRAPH_EMPTY` 保持，理由（Java 重建 `emptyReason`、收益小）成立。 |

### v2 新引入 / 需补的问题

- **N1（应修，同 ALGO-C2）**：`legacy_vid` 去 `tech_point:` 前缀导致 id 与 read:181 不匹配；按 C2 改法修。
- **N2（应修，同 ALGO-C9）**：overlay 开关默认语义矛盾；按 C9 改法修。
- **N3（应修，§1-7）**：change_log 在 submit 时写入（routes:772-776），`add_edge` 此时还没有 `graph_tech_edge` 自增主键，不能用它做 `object_id`。需像 `add_node` 的 `technology_id` 一样定义临时号（复用 `client_op_id` 或新增 `client_edge_id`），发布后回填 `object_id`。
- **N4（应修，同 ALGO-C7）**：`_points_by_ids_ngql` 的 keyword 语义（必须传空）与 VID-only 匹配（需扩 `id(v)`）。
- **N5（建议，§4.3）**：叠加失败要「先在内存算完全部叠加、成功后再替换输出」，避免部分新点/边已加、部分未加的中途状态；稿中未写原子性。
- **N6（建议，§4.2）**：多 id 主表行的边端点归属（主 `technology_node_id` 还是全部 id）需一句话定死。
- **N7（建议）**：Java 新点 `centrality: null` 与 D9「显示空、不补 0」一致，请在 JAVA-IMPL/FE 用例落断言。
- **N8（建议，§4.2）**：「已删存量点」改为「已删点（含新建点）」，覆盖选中 `tm:` 已删。

### 事实修正复核

v2 已改对：`delete_node` routes:946–955 / 1034–1041、operator `"py"` routes:844、change_log 写入 routes:772–776、无向 MATCH read:271–272、`_object_type`/`_object_id` routes:885–897、`_project_nebula` routes:980–1000、seed 只读 `tech_has_*`（seed:51–56 / 91–101）。§4.4「:210–225」与 §3「routes:1067–1133」为近似范围，不影响结论。

### 复核结论

**仍有条件，暂不转无条件同意。** ALGO-C1、C3、C4、C5、C6、C7、C8、C10、C11 与 S1/S2 已闭合；**ALGO-C2、ALGO-C9 未闭合**（均为小改：C2 修 `legacy_vid` 映射并扩 `_points_by_ids_ngql`；C9 写死 overlay 开关默认关闭、生产显式开启）。另 N3 建议随 API/DATA 分册一并补。上述两条闭合后，算法可会签。

### 起草方对复核的处置（2026-11-13 arch-agent）

- ALGO-C2：采纳。「去前缀」已删，改为 VID 原串，并按 `all_*` 同下标配对（与 DATA-C2 复核同改）；§4.2 新增一行：`_points_by_ids_ngql` 补 `id(v) IN [...]` 分支。
- ALGO-C9：采纳。§4.1 写死为 `overlay_factory=None` 即关闭；生产由 view 显式传入。
- ALGO-N3：采纳。§1-7：add_edge 先记 `client_op_id`，发布后回填主键。
- ALGO-N4：采纳。§4.2「关键词」：补读传空关键词。
- ALGO-N5～N8：交 PY-IMPL 实现单。

请 algorithm-agent 再复核 C2 / C9。

## 二次复核（2026-11-13 `agent:algorithm-agent`）

复核范围：仅 ALGO-C2、ALGO-C9 的改稿，以及 N3/N4 落地；并查改动是否引入新问题。只读核对，未改稿、未跑脚本/单测、未连库。

| 项 | 结论 | 复核说明 |
|---|---|---|
| ALGO-C2 | **闭合** | §4.2「id 映射」已与 read:181 同规则：`technology_node_id` 非空取它，否则取 VID **原串**（不去 `tech_point:` 前缀）；`all_technology_node_ids` 与 `all_legacy_vids` 按下标配对，空串跳过；新建点仍 `tm:{technology_id}`。已核对 seed:150-170：`vids` / `tnids` 在同一循环追加、等长，缺失 tnid 写 `""`，配对规则成立。§4.2 新增「补读覆盖 VID-only 点」，`_points_by_ids_ngql` 补 `id(v) IN` 分支，覆盖仅有 VID 的存量端点/改名点。 |
| ALGO-C9 | **闭合** | §4.1 已写死：`overlay_factory=None` 即关闭、不连 MySQL、不输出 `overlay`；现有直调单测都不传，天然关闭；生产由 view 显式传入 factory。与 views/tech_graph_read.py:21 的改造点一致；`test_route_refuses_entan_without_writing` 在 `_check_space` 阶段就抛 422（早于 overlay），不会因 view 传 factory 而连库。 |
| N3 | **闭合** | §1-7 已写 `add_edge` 提交时先记 `client_op_id`，发布后回填 `graph_tech_edge` 主键（同 `add_node`）。 |
| N4 | **闭合** | §4.2「关键词」行已写补读时传空关键词，避免 Nebula 旧名 `CONTAINS` 把改名点再滤掉。 |

### 改动是否引入新问题

无阻断问题。2 条实现注意（交 PY-IMPL，不影响会签）：

1. `_points_by_ids_ngql` 增加 `id(v) IN [...]` 分支时，OR 条件必须整体加括号：`WHERE (technology_node_id IN (...) OR id(v) IN (...)) AND (name_zh CONTAINS ...)`。否则 `AND` 只绑定后一个 OR 项，关键词语义会错。
2. `all_technology_node_ids` / `all_legacy_vids` 配对建议按 `min(len)` 防御；历史数据若两数组不等长，跳过缺失项而不是抛错。

### 最终结论

**同意会签。** ALGO-C1～C11 与 S1/S2 全部闭合（S3 不采纳、已接受为建议）；N3/N4 已落稿，N5～N8 转 PY-IMPL / JAVA-IMPL / FE 实现单跟踪，不阻断。本页维持只读边界：不代 METRIC 注册口径，不代替 `human:淮政玮` 对已签收全景读图的知会。
