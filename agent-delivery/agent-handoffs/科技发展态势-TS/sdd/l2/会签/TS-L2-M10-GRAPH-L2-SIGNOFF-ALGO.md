# TS-L2-M10-GRAPH-L2-SIGNOFF-ALGO · API / DATA 二级分册算法会签

| 项 | 内容 |
|---|---|
| 角色 | `agent:algorithm-agent`（算法 / 指标身份） |
| 日期 | 2026-11-13 |
| 对象 | `TS-L2-M10-GRAPH-API.md`（草稿 v1）、`TS-L2-M10-GRAPH-DATA.md`（草稿 v1） |
| 基准 | 已签收 `TS-L2-M10-GRAPH-ARCH.md` v2（§11 末尾「拍板结果」） |
| 参照 | `TS-L2-M10-GRAPH-METRIC.md` v1（**只查跨稿一致性，不审该册**；该册为同身份起草） |
| 监管 | `human:刘剑锋` |
| 范围 | **只读核对**：未改被审稿件、未改 task-registry、未 git、未连库、未跑脚本/单测 |
| 代码简写 | `read`=`repos/lumen-algo-py/lumen_common/algorithms/tech_graph_read.py`；`routes`=`.../vendor/entan-py/api/tech_graph_maintain_routes.py`；`DDL`=`.../vendor/entan-py/scripts/mysql/tech_graph_maintain.sql`；`SEED`=`.../vendor/entan-py/scripts/seed_tech_graph_maintain.py`；`PAN`=`repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/SituationPanoramaService.java`；`SCORE`=`repos/lumen-algo-py/scripts/seed/seed_technology_panorama_score.py`；`chainan`=`repos/lumen-algo-py/vendor/innov-py/chainan/graph/nebula_schema.py` |

## 结论

- **API 册：有条件同意**（必修 3 条、建议 6 条）。读图出口增量与 ARCH §4 的字段口径基本一致，`origin` / `strengthManual` / `timeRange` / `tm:` / `overlay` / 两条 `_read` 分支 / 选中新点均对得上；但 §5.2 的 chainan 依赖在**当前 entan 镜像里不存在**，§5.3 未禁止人工边携带 `evidenceLevel`、且「只追加、不改已有字段」与叠加开启后的删点/删边/截断语义不符，需改文。**未发现破坏已签收 `weight` / `strength` / S4 语义的硬伤**。
- **DATA 册：有条件同意**（必修 5 条、建议 7 条）。新表 / 唯一键 / 单事务 / 快照 N=1 / 整图回滚方向成立；`strength_auto` 经核实**不被 S4 分数种子、`weight`、`strength`、`M_TECH_*` 消费**，可作为历史快照保留。必修集中在：种子存量英文码 vs 人工三枚举同键、生成列 `name_cn_active` 回滚、`stats` 键形与 API 不一致、种子自环/已删端点、已删存量边过滤须用 `rel_code`。

---

## 一、TS-L2-M10-GRAPH-API 会签

### 1.1 与 ARCH §4 已签收语义逐项核对

| 语义 | ARCH §4 要求 | API 稿落点 | 结论 |
|---|---|---|---|
| 存量点 id | `technology_node_id`，否则 VID 原串（不去前缀） | §5.3「节点 id」行，`read:181` | 一致 |
| 新点 id | `tm:{technology_id}`；选中时按 `technology_node_id=tm:{id}` 请求 | §5.3 同表；§5.3 末段 | 一致 |
| 人工边 `origin` | 仅人工边追加 `"manual"` | §5.3 `relations[]` 人工边行 | 一致 |
| 人工强度 | `strengthManual`，不填 `weight`、不填 `year` | §5.3 同表 | 一致；但未写「不填 `strength` / 不计入度 / 不填 `evidenceLevel`」，见 ALGO-API-C1 |
| 人工时间 | `timeRange{from,to}`，不进 timeline | §5.3 同表 | 一致 |
| 人工边 id | `tech_manual:{edge_id}` | §5.3 同表 | 一致 |
| `source` / `target` | 保持端点 id，不得写成 `"manual"` | §5.3 同表 | 一致 |
| 端点合并 | 人工边端点必须并进 `nodes` | §5.3 第一条 bullet，引 `PAN:184–196` | 一致 |
| `overlay` | 顶层 `{status:ok|unavailable}`；关闭时不输出 | §5.3 顶层行；`overlay_factory=None` 关闭 | 一致；Java `assemble` 需补透传（§6.2） |
| 两条 `_read` 分支 | 未选点早返回、选中 `_finish` 都叠加 | §5.3 首段，`read:556–570` | 一致 |
| 200 上限 | 合并后截断、新点/改名点优先、置 `truncated.nodes` | §5.3 末条「归 ALGO 实现」 | 一致，但表头「只追加」措辞不准，见 ALGO-API-C4 |
| 选中已删点 | 返回空图 + `emptyReason` | **未写** | 缺，见 ALGO-API-C6 |
| `relationTypeOptions` | 三中文枚举可进图例；不得驱动加边下拉 | **未写** | 缺，见 ALGO-API-C5 |
| 已删存量边 | 按无序对 + 原关系码过滤 | API 未写（归 DATA/ALGO）；DATA 用 `rel_code` 的方向正确 | 见 DATA ALGO-DATA-C5 |
| 子领域过滤 | 新点被 `restrict` 隐藏（已知限制） | §6.2 已声明 | 一致 |

**字段级 D9 核对**：API §5.3 明确人工强度不填 `weight`、不填 `year`；未写「不填 `strength`」。`read:286–300` 的 `_relation` 会无条件产出 `evidenceLevel`，API 人工边行未禁止该字段，存在实现者照抄 `_relation` 给人工边编造 `HIGH`/`LOW` 的风险；`PAN:178`、`PAN:372–373` 的 `lowEvidence` 会按 `evidenceLevel` 删边。故 ALGO-API-C1 列为必修。

### 1.2 API 条件表

| 编号 | 级别 | 改哪一节 | 改成什么 | 证据 |
|---|---|---|---|---|
| **ALGO-API-C1** | **必修** | §5.3「`relations[]`（人工边）」行 | 在「人工强度不填 `weight`、不填 `year`」后补：**人工边不得输出 `evidenceLevel`（也不得输出任何 `evidence`/`evidenceType` 字段）；不得填 `strength`；不计入 `weighted_degree`；不得进入 35-3 `panorama_hidden_relation_count` 的任何统计**。理由：`_relation` 默认产出 `evidenceLevel`；`lowEvidence` 会据此删边，编造等级会改变可见集合与证据语义 | `read:286–300`（`_relation` 固定产出 `evidenceLevel`）；`PAN:178`、`PAN:372–373`（`lowEvidence`）；`METRIC:125–128`、`METRIC:147–148` |
| **ALGO-API-C2** | **必修** | §5.2 `panorama_hidden_relation_count` 行 | 二选一改写：**(a) 推荐** 改为「entan 用自有 Nebula 只读会话（`entan.common.nebula`），显式 `USE demo_gkx_chain`，启动断言 space 前缀 `demo_gkx_`，非该 space 直接拒」；或 **(b)** 在 `docker/Dockerfile.entan-api` 补 `COPY vendor/innov-py/chainan/` 与 `vendor/innov-py/conf/settings.yaml`，并把 `vendor/innov-py` 加入 `sys.path`。**不能按现文直接引 chainan**：entan 镜像未打包 chainan，且 entan 代码无 chainan import，按现文实现会 `ModuleNotFoundError`，35-3 的隐藏计数恒为 null | `Dockerfile.entan-api:17–30`（只 COPY `vendor/entan-py/*`，无 chainan）；`Dockerfile.api:14–17`（algo-py 才打包 chainan）；`chainan:52–59`；`routes:511–522` |
| **ALGO-API-C3** | **必修** | §3.4 `stats` | 保留本册**分组 JSON**为唯一契约，并加一句「DATA §5.2 的扁平键必须改为同一分组结构」；`publish_results` 的 `results` 不得另起键名。理由：DATA §5.2 现写 `node_add/node_del/...`，与本册 `tech_nodes{added,updated,removed}`、§4.1 版本详情、METRIC §2.2 均冲突，会导致 40-3 回滚预览与 40-4 版本列表同源失真 | `API:180–182`、`API:199–203`、`API:275–279`；`DATA:338`；`METRIC:108–109`、`METRIC:116` |
| ALGO-API-C4 | 建议 | §5.3 表头「**只追加、不改已有字段**」 | 改为：「**叠加关闭时与今天逐字节一致；叠加开启时只改集合与追加字段，不改存量行字段值**。集合变化按 ARCH §4.2：已删点/已删存量边/含删点的路径被移除，关键词补读可能新增存量点，合并后按 200 截断并置 `truncated.nodes`。」保留末条「归 ALGO 实现」，但删掉会被读成「集合不变」的表述 | `API:364–377`；`ARCH §4.2`；`read:556–570` |
| ALGO-API-C5 | 建议 | §5.3 增一行「`relationTypeOptions`」 | 写明：叠加开启后 `relationTypeOptions` 可能同时含**存量英文码**（`KNOWLEDGE_DEPENDENCY` 等）与**人工三中文枚举**；它只用于图例/筛选，**不得作为 `add_edge.rel_type` 的下拉数据源**（`rel_type` 仍固定三枚举）。`factorItems` 不受影响 | `API:106–107`（不从 `relationTypeOptions` 取）；`read:533–539`；`METRIC:135–137` |
| ALGO-API-C6 | 建议 | §5.3 增一行「选中已删点 / 选中新点」 | 补：选中 `tm:` 新点按 `technology_node_id=tm:{id}` 请求；选中**已软删点**返回空图并置 `emptyReason=GRAPH_EMPTY`（不 404、不回落默认点）；`truncated` 按合并后重算 | `ARCH §4.2`；`read:551–553`；`PAN:219–224` |
| ALGO-API-C7 | 建议 | §2.3 `delete_edge` 说明 | 补一句边界：**只有工作集 `graph_tech_edge` 内的边可删**；Nebula 中未被 L01 种子纳入的 `tech_rel` 不在 `/current.tech_edges[]`，前端无从取得 `edge_id`，也就不可能删；`panorama_hidden_relation_count` 只服务「删点」确认框，不用于删边 | `API:116–118`；`DATA:78–89`；`routes:511–522` |
| ALGO-API-C8 | 建议 | §5.1 `tech_edges[]` 字段表 | 补一句：`src`/`dst` 是 `technology_master.technology_id`（int），与同响应 `nodes[].id`（string，存量可能是 VID 原串）**不是同一命名空间**；前端须用 `nodes[].technology_id` 做 int→节点映射，禁止拿 `src/dst` 直接与 `nodes[].id` 比较 | `routes:348–414`（`nodes[].technology_id`）；`API:330–344`；`DATA:676` |
| ALGO-API-C9 | 建议 | §5.3 `nodes[]` 行 | 补一句字段名差异：全景出口是 `importance`（ARCH §4.2 定名），`/current` 与主表是 `importance_level`；两者不得在前端混用，也不得把 `importance` 回写成主表列 | `API:369`；`API:326–344`；`DATA:68–84` |

### 1.3 分节意见（非条件，供起草方参考）

- **§1 通用形状 / §2 op**：`client_batch_id`、`operator` 注入、`trace_id` 与 ARCH 一致；`add_edge` 的 0–10 / 1900–2100 / from≤to 与 `routes:677–692` 对齐；自环 422 与 DATA 种子侧的自环处理应同口径（见 ALGO-DATA-C4）。
- **§2.1 / §2.4 `importance_level`**：省略写 NULL 正确，与 ALGO-C6、`METRIC:34–35`、`METRIC:139` 一致；`update_node` 允许把已有值改回 NULL 的语义建议在实现单写死（本册未禁止，属可接受）。
- **§2.2 重复判定「复活该行」**：在「auto 行 `rel_type` 为英文码、`add_edge.rel_type` 仅三中文枚举」的前提下，add_edge 实际**只会复活已删的人工行**；「种子边原强度字段保留」这句在 add_edge 路径不可达（auto 行键为英文码）。建议在 DATA §2.3 或 API §2.2 注明：**auto 行的复活只发生在回滚/种子重跑，不经 add_edge**；若未来允许中文码进种子，则必须禁止（见 ALGO-DATA-C1）。
- **§3.4 `stats`**：`tech_edges.removed` 含 `delete_node` 级联，正确；需与 DATA §5.2 的统计点一一对应（C3）。
- **§4.1 `kind` / `snapshot_status` / `operator_display`**：与 DATA §3.4 一致；历史 `stats` 扁平键「原样返回、缺键不补 0」是正确选择（API Q7），不建议 DATA 回填伪造历史计数。
- **§4.3 回滚预览 `counts`**：`counts` 取自目标版本 `stats`，与本册 §3.4 同源，符合 METRIC §2.2 #5 / #6；需保证 DATA 落库键形一致（C3）。
- **§5.2 `tech_edge_count`**：工作集 active 行数，含 auto + manual，定义清楚；与 `edge_count`（实体边）分开，避免 35-3 文案混用。
- **§6.2 Java 透传**：`assemble` 现返回 7 键（`PAN:210–217`），仅 `overlay` 需新增一行；`maps()`/`normalizeRelation` 不丢字段（`PAN:553–565`、`PAN:472–484`），与稿一致。
- **§7 错误码**：`42201` 覆盖名称/关系/端点/自环/强度/时间，足够；`50303` 替代 50301 与 DATA §5.4 一致。
- **§10 Q1–Q8**：见「四、需监管人拍板」逐条意见。

### 1.4 事实核对（API）

| 稿中引用 | 实际 | 判定 |
|---|---|---|
| `routes:511–522` impact | `routes:511–522` 为路由 + 查询 + 返回；`routes:517–519` 为 404 | 属实 |
| `routes:677–680` 强度 0–10 | 属实 | 属实 |
| `routes:681–692` 时间 1900–2100 | 属实 | 属实 |
| `read:181` id = `technology_node_id` 或 VID | `_point_node` `read:178–197`，`read:181` 为 `biz` 取值 | 属实 |
| `read:270–272` evidence 过滤 | `_rel_ngql` `read:265–282`，默认 `evidence_level IN [HIGH,MEDIUM]` | 属实 |
| `read:556–570` 两条分支 | 属实 | 属实 |
| `PAN:184–196` 端点合并/删边 | `keepThenCap` / 端点保留逻辑在该区间 | 属实 |
| `PAN:210–227` 只保留 7 键 | `PAN:210–217` 为 7 键，`218–227` 为 `truncated`/`emptyReason` | 基本属实（区间可缩为 210–217 更准） |
| `Dockerfile.entan-api` 可用 chainan | **不属实**：镜像未 COPY chainan；仅 algo-py 镜像有 | **必须改**（C2） |

---

## 二、TS-L2-M10-GRAPH-DATA 会签

### 2.1 数据面结论

- **新表 `graph_tech_edge` 方向成立**：`src/dst` 用内部 `technology_id`（BIGINT），人工边有向、种子边规范化为 min/max，`uk_tech_edge(src,dst,rel_type)` 不含 `status`（软删占键），PK `edge_id`，与 ARCH §2、API §2.2/§2.3 对得上。
- **`strength_auto` 合规**：经逐条核实，`SCORE` 只扫 Nebula `tech_point` / 实体 tag（`SCORE:268–342`），不读 `technology_master` / `graph_tech_edge`；`read` 的 `weight` 只来自 `tech_rel.relation_confidence_score`（`read:281`、`read:300–302`），`strength` 只来自 `tech_point.weighted_degree`（`read:194–197`）；`M_TECH_EDGE_STRENGTH` 的注册对象是 IPC4 共类网络边，不是 `tech_point` 边（`METRIC:170`）。**结论：`strength_auto` 不被任何指标消费，可作为历史快照保留**；但建议加守护（C8）。
- **`rel_code` 保留有意义**：今天与 auto 行 `rel_type` 同值，未来若统一 `rel_type` 口径，`rel_code` 是删除过滤与审计的锚点。**算法身份建议保留**，但删除过滤必须以 `rel_code` 为准（C5）。
- **种子码集合风险真实**：存量英文四码（`KNOWLEDGE_DEPENDENCY` / `PATENT_CONVERGENCE` / `CO_EVOLUTION` / `WEAK_DEPENDENCY`）与人工三枚举（`包含` / `依赖` / `促进`）**必须不相交**；一旦 `tech_rel.relation_type` 出现中文码，`(src,dst,rel_type)` 会与人工行同键，触发复活/混合语义（C1）。
- **种子 `importance_level=NULL` 正确**，与 ALGO-C6、`METRIC:139`、`METRIC:160` 一致；`SEED` 现 `MASTER_SQL` 省略该列会吃默认「中」（`DDL:11`、`SEED:234–241`），新种子必须显式 NULL。
- **诱导子图选法可接受**，但需 dry-run 计数 + 自环剔除 + 已删端点跳过（C4/C6）。

### 2.2 DATA 条件表

| 编号 | 级别 | 改哪一节 | 改成什么 | 证据 |
|---|---|---|---|---|
| **ALGO-DATA-C1** | **必修** | §6.1 步骤 5 / §12-7 | 把「若出现中文码，需先与 API 确认键口径」改为硬规则：**种子只允许写入已确认的英文码白名单**（四码 + dry-run 中确认的其他英文码）；**凡命中 `包含`/`依赖`/`促进` 或任何非 ASCII 码，一律跳过该边并计数，dry-run 打印 `{code, count}`；若白名单外码占比 > 0，默认中止（除非监管人书面豁免）**。理由：auto 行与人工行同键会触发「复活为 manual 但保留 `rel_code`/`strength_auto`」的混合语义，且同一 Nebula 边会在全景里以「存量英文码 + 人工中文枚举」重复出现 | `DATA:89`、`DATA:409`、`DATA:680`；`API:105–107`；`DDL` 唯一键 `(src,dst,rel_type)`；`read:286–300` |
| **ALGO-DATA-C2** | **必修** | §3.2 / §4.1 / §5.3 还原表 | 在 §4.1 显式列清单与 §5.3 `technology_master` 还原行补：**生成列 `name_cn_active` 只读，不写入快照 payload、不进入 INSERT/UPDATE 列清单**；快照 `SELECT` 若用 `*`，还原时必须显式排除生成列。理由：MySQL 不允许对生成列 INSERT/UPDATE，回滚整表还原会直接失败 | `DATA:147–151`、`DATA:261`、`DATA:358–366`；`DDL` 生成列定义 |
| **ALGO-DATA-C3** | **必修** | §5.2 步骤 14 / §3.4 `stats` | 把 `node_add/node_del/node_upd`、`tech_edge_add/...` 扁平键**改为 API §3.4 的分组 JSON**：`tech_nodes{added,updated,removed}`、`tech_edges{added,removed}`、`entity_links{added,removed}`、`entity_edges{added,updated,removed}`、`entity_attrs{updated}`；`publish_results` 仍 `{succeeded,failed,failed_items}`。理由：与 API §3.4、§4.1、METRIC §2.2 同源要求冲突，否则 40-3 与 40-4 数字对不上 | `DATA:338`；`API:180–182`、`API:199–203`、`API:275–279`；`METRIC:108–109`、`METRIC:116` |
| **ALGO-DATA-C4** | **必修** | §6.1 步骤 3–4 / §6.4 | 补两条硬规则：①**映射后 `src_tech_id == dst_tech_id` 的边必须丢弃**（合并同名点会把多个 Nebula VID 映射到同一 `technology_id`，产生自环；add_edge 已把自环定为 422，种子不能绕过）；②**端点主表 `status != 'active'` 或映射不到时跳过该边**，dry-run 打印 `{self_loop, missing_endpoint}` 计数。理由：种子直接写表，没有 API 层 422 兜底 | `DATA:399–409`、`DATA:447`；`API:101`（自环 422）；`SEED:163–171`（`all_legacy_vids`/`all_technology_node_ids` 多值映射） |
| **ALGO-DATA-C5** | **必修** | §2.1 `rel_code` 说明 / §2.3 / §4.2 | 补：**叠加过滤已删存量边时，auto 行以 `(端点无序对, rel_code)` 匹配 Nebula；`rel_code` 为 NULL 时回退 `rel_type`；人工行 `rel_code` 恒 NULL，不参与存量边过滤**。理由：若未来把 auto 行 `rel_type` 统一成中文/别名，用 `rel_type` 过滤会静默失效，被删的 Nebula 边重新出现 | `DATA:78`、`DATA:109`、`DATA:424–426`；`ARCH §4.2`；`API:372–376` |
| ALGO-DATA-C6 | 建议 | §6.1 步骤 4 | 定义同一 `(unordered pair, relation_type)` 多条 Nebula 边的聚合：建议 `strength_auto = MAX(relation_confidence_score)`、`time_from = MIN(first_evidence_year)`、`time_to = MAX(first_evidence_year)`（或 NULL），并在 dry-run 打印重复组数；文档写明**删除该行会隐藏该无序对+类型下的全部 Nebula 边**（表是 pair+type 粒度，不是单条边粒度） | `DATA:407`；`read:286–300`（`index` 区分多条）；`ARCH §4.2` |
| ALGO-DATA-C7 | 建议 | §6.4 末段 | 把「多出的 tnid 单独加入**或**跳过并 warning」二选一写死：**建议两列表按 `min(len)` 同下标 zip；多出的 tnid/VID 一律跳过并 warning，不单独加入**。理由：单独加入会让一个技术点拥有超出配对语义的 id，读侧映射与去重规则不确定 | `DATA:447`；`ARCH §4.2`；ALGO-SIGN C2 |
| ALGO-DATA-C8 | 建议 | §2.1 `strength_auto` / §12-6 | 保留「不被任何指标消费」的结论，并补一条可执行守护：**`read` / S4 种子 / 任何指标脚本不得从 `graph_tech_edge` 读 `strength_auto` 或 `rel_code`；建议在 `SCORE` 加断言（拒绝 `technology_master` / `graph_tech_edge` 表名）并在读图单测断言人工边无 `weight`/`strength`/`evidenceLevel`** | `DATA:79`、`DATA:680`；`METRIC:125–128`、`METRIC:135–137`、`METRIC:159–160`；`SCORE:268–342` |
| ALGO-DATA-C9 | 建议 | §3.4 `kind` | `kind` 的 `DEFAULT 'ent'` 只用于历史回填；补一句：**新 publish / rollback / seed 必须在 INSERT 时显式写 `kind`**（`save`/`rollback`/`seed`），不得依赖默认值；可加代码断言或 `CHECK (kind IN ('save','rollback','seed','ent'))`。理由：漏写会把新保存误标成「系统（历史）」 | `DATA:175`；`API:259–263`（`operator_display`） |
| ALGO-DATA-C10 | 建议 | §5.5 `node_id_map` 复原 | 「按 `change_set_id` 扫 `object_type='node'` 的 after 重建」补过滤条件：**只取 `op='add_node'` 且 `after` 含 `client_node_id` 的行**；`update_node`/`delete_node` 也是 `object_type='node'`，不能进映射 | `DATA:387`；`API:157–161`；`routes:772–776` |
| ALGO-DATA-C11 | 建议 | §5.2 步骤 10–11 | `graph_tech_edge` 在步骤 10（逻辑删/级联）与步骤 11（ADS 写）两处出现，需写清是**同一条 UPDATE 的两次描述**还是两次写；建议合并为一次写入（逻辑状态 + `version_id` 一起），避免双写/漏写 | `DATA:326–329` |
| ALGO-DATA-C12 | 建议 | §5.4 错误映射 | 「1062 → 409 或 422」二选一写死：**publish 提交阶段撞唯一键 → 409（附当前版本，提示重试）；validate 阶段 → 422**，与 API §7 一致 | `DATA:379`；`API:413–418` |

### 2.3 分节意见（非条件）

- **§2.2 唯一键不含 `status`**：软删占键 + 复活更新，正确；但复活路径的实际可达性受 C1 约束（auto 行英文码不会被 add_edge 命中）。
- **§2.3 级联**：`delete_node` 级联软删 `graph_tech_edge` 与 API §3.4 `tech_edges.removed` 对得上；建议在级联时同步写 `version_id`，便于回滚/血缘。
- **§2.4 方向**：人工有向、种子 min/max 归一，正确；`A→B` 与 `B→A` 在人工侧是两条，与 API 一致。
- **§3.1 / §3.3 `layout`**：`technology_master.layout_x/y` 与 `graph_entity_node` 冗余存储是刻意的读侧优化，可接受；种子点 NULL。
- **§3.2 名称唯一键**：生成列 + 只约束 active 正确；`utf8mb4` 大小写敏感性需与 ENT 现网一致（`utf8mb4_0900_ai_ci` 下大小写不敏感，建议在 DDL 注释写明）。
- **§3.4 `snapshot_status`**：`none/ok/oversize` 三态够用；历史行回填 `none` 合理。
- **§3.5 `client_batch_id` 唯一**：NULL 历史行不冲突，正确；新客户端必填由 API 保证。
- **§4 快照七表**：含软删行、显式列清单、INSERT 前预判，方向正确；C2 是唯一硬坑。
- **§5.1 锁**：`GET_LOCK('m10_graph_publish', 10)` 覆盖 publish/rollback，与 ARCH 一致；建议在锁内再校验 `change_set.status`（步骤 3/4 已写）。
- **§5.2 写序**：先版本后日志、同事务回填 `object_id`，正确；C11 是措辞问题。
- **§5.3 整表还原**：语义正确（V 后新增消失、V 后删除复活）；需在确认框文案与 PRODUCT-C11 对齐（DATA §12-5）。
- **§6.1 诱导子图**：`id(a) IN [...]` 若 nGQL 不支持，可改 `OR` 展开；点集上限 50、两端都在集合内，符合 ARCH。
- **§6.2 候选切片**：算法身份推荐**候选 1**（现有 ENT 点一跳）做首个种子：与现网 1 点/61 实体边同源，回归成本最低，且能覆盖增删边/回滚；候选 2 适合演示，候选 3 适合压力。三者都必须 dry-run。
- **§6.3 写入**：`importance_level=NULL`、`category=NULL`、`layout=NULL` 正确；`graph_entity_node` 只写 active 点，正确。
- **§6.5 重跑**：命中 `deleted` 整组跳过、不复活，正确；`INSERT IGNORE` 对已删 auto 行保持 deleted，符合「种子不覆盖人工删除」。
- **§7.1–7.5**：DB 名前缀、启动断言、D12 偏差、D9 计数，均与 ARCH/METRIC 一致；`strength_auto` 的守护见 C8。

### 2.4 事实核对（DATA）

| 稿中引用 | 实际 | 判定 |
|---|---|---|
| `DDL:11` `importance_level` 默认「中」 | 属实（`VARCHAR(8) DEFAULT '中'`，可空） | 属实 |
| `DDL:19` `uk_name_cn` | 属实 | 属实 |
| `DDL:55–64` `graph_version` | 属实 | 属实 |
| `DDL:110–115` `graph_snapshot` | 属实 | 属实 |
| `SEED:234–241` `MASTER_SQL` 省略 `importance_level` | 属实 | 属实 |
| `SEED:163–171` `_external_ids` | 属实（含 `all_*` 多值） | 属实 |
| `routes:348–414` `/current` | 属实；当前无 `tech_edges`，节点有 `technology_id` | 属实 |
| `routes:511–522` impact | 属实 | 属实 |
| `read:270` 对齐 | `read:265–282` 的 `_rel_ngql`，默认 HIGH/MEDIUM | 属实（行号可写 265–282） |
| `Dockerfile`/chainan | 见 API C2，不属 DATA | — |

---

## 三、跨稿一致性

| # | 项 | API 稿 | DATA 稿 | METRIC 稿 | 判定 |
|---|---|---|---|---|---|
| 1 | `stats` 键形 | 分组 JSON（§3.4/§4.1） | **扁平键**（§5.2） | 分组描述（§2.2 #5） | **不一致，必修**（API-C3 / DATA-C3）；以 API 分组为准 |
| 2 | `rel_type` 语义 | 人工三枚举；存量英文码不进枚举 | 人工中文；auto 英文原码；`rel_code` 存原文 | 表内只描述「包含/依赖/促进」，未写 auto 英文码 | 不冲突，但 METRIC §3.2 描述可补「人工行」；守护条款仍成立 |
| 3 | `strength_auto` | 不出现在读出口 | 快照列，不参与指标 | 未列；`graph_entity_edge` 的 `strength_auto` 是另一张表 | 一致（不消费）；建议加守护（DATA-C8） |
| 4 | `strength_manual` | 人工边 `strengthManual`，不填 `weight` | 不进公式 | 不进 `weight`/`strength`/S4 | 一致 |
| 5 | `weight` / `strength` | `weight` 只存量边；未写 `strength` | 不涉及 | `weight`←`relation_confidence_score`；`strength`←`weighted_degree` | 一致；API 需补「人工边无 `strength`」（API-C1） |
| 6 | `evidenceLevel` | 未禁止人工边携带 | 不涉及 | 未写 | **缺保护**（API-C1） |
| 7 | `overlay` | 顶层 `{status}`；`overlay_factory=None` 关闭 | 不涉及 | §4 承认可见集合变化 | 一致；API 措辞需改（API-C4） |
| 8 | `tm:` id / 新点无分数 | `tm:{technology_id}` | 种子不写 `tm:`（存量点） | 新点 `centrality:null`、无 `strength` | 一致 |
| 9 | 200 上限 / `truncated` | 归 ALGO；表头「只追加」不准 | 不涉及 | 未写 | API-C4 |
| 10 | 35-3 计数 | `tech_edge_count` + `panorama_hidden_relation_count`（Nebula HIGH/MEDIUM） | `tech_edge_count` 同义 | 两项计数同属 DN-A03-09 建议豁免 | 一致；C2 修依赖 |
| 11 | 40-3 / 40-4 同源 | `counts` 取目标版本 `stats` | `stats` 落库 | 强制同源 | 一致（C3 修键形后） |
| 12 | 快照 N=1 | 版本详情 `snapshot_status` | 每次 publish/rollback 写 N=1 全量 | 未写 | 一致 |
| 13 | 50301 退役 | 50301 退役、50303 下游不可达 | 未涉及 | 未涉及 | 一致 |
| 14 | D9 人工强度标注 | 字段 `strengthManual` | 不入公式 | UI 标「人工」 | 一致；FE 落地 |
| 15 | `relationTypeOptions` | 未写 | 不涉及 | 三中文枚举可进图例 | **API 缺**（API-C5） |
| 16 | `rel_code` 删除过滤 | 未写 | 有列，但未定过滤键 | 未写 | **DATA 缺**（DATA-C5） |

**跨稿结论**：两份分册的字段契约与 ARCH §4 无结构性冲突；真正会跨稿打架的是 **stats 键形**（#1）和 **人工边证据字段**（#6），其次是 **`rel_code` 过滤键**（#16）。METRIC 的保护条款（人工强度不进化公式、新点不补 0、S4 只扫 Nebula、`importance_level` 非分值）在 API/DATA 中均未被破坏；`strength_auto` 的确认结论为「不消费」。

---

## 四、需监管人拍板

| # | 事项 | 算法身份意见 | 建议拍板人 |
|---|---|---|---|
| 1 | **同一对点同时存在 auto 英文码边与 manual 中文边**是否允许 | 现设计允许（唯一键含 `rel_type`，两类不同键），全景会出现两条平行边。**建议允许，但前端必须用「存量 / 人工」标签区分**；若产品认为视觉重复不可接受，则 `add_edge` 应对「该无序对已有任意 active 边」返回 422（需改 API §2.2 与 DATA 唯一键语义，代价较大）。请产品/前端定 | 产品 + 前端 + API |
| 2 | **种子切片选哪个**（DATA §6.2 三候选） | 推荐候选 1（现有 ENT 点一跳，≤50 点）做首个 L01；候选 2 用于演示、候选 3 用于压力；三者执行前 dry-run 并打印点数/边数/丢弃数（自环、缺端点、中文码） | DATA + ALGO + 监管人 |
| 3 | **`category` 是否强制 `dim_tech_domain` 外键**（API Q1） | 首版自由文本可接受；`category` 不参与 `restrict`/指标，维表未灌时不应 400。建议「自由文本 + 前端下拉提示」，不做存在性校验 | 产品 + API + DATA |
| 4 | **`relationTypeOptions` 是否纳入人工三枚举** | 应纳入图例/筛选，但**不得驱动加边下拉**（ALGO-S1 已定）；需前端确认图例能同时展示英文存量码与中文枚举 | 前端 + API |
| 5 | **`rel_code` 是否保留**（DATA §12-1） | **建议保留**；它是未来 `rel_type` 统一后的删除过滤锚点，成本仅一列。若删，则 DATA-C5 失效，删除过滤只能绑 `rel_type`，未来改口径需数据迁移 | 监管人 + DATA |
| 6 | **名称唯一键 DDL 的 Owner 书面确认**（DATA §10 / §12-3） | 非算法身份；同意 DATA 的判断：共享 demo 库改唯一键语义，至少需监管人书面确认 + 备份 + 变更窗口；Owner 是否豁免由监管人定 | 监管人 + 数据平台 Owner |
| 7 | **快照阈值 8MB / 2000 行 / 50000 行、`--all` 硬禁用**（DATA §12-4） | 当前工作集 1 点/61 实体边，阈值充裕；`--all` 禁用正确（防止超大 payload 破坏事务）。建议保留，并在超限时返回 `snapshot_status=oversize` 而非失败 | 监管人 + DATA |
| 8 | **回滚整表还原语义确认**（DATA §12-5） | 语义正确（整图回滚到 V 的当前状态，V 后新增消失、V 后删除复活）；确认框文案须写「将恢复 V 之后被删除的点/边，并移除 V 之后新增的点/边」，与 PRODUCT-C11 对齐 | 产品 + 监管人 |
| 9 | **`panorama_hidden_relation_count` 的实现通道**（API §5.2） | 推荐 entan 自有 Nebula 只读会话 + 显式 `USE demo_gkx_chain` + 启动断言；不建议为 35-3 一个计数给 entan 引入 chainan 打包（C2 方案 a） | API + 运维 + 监管人 |
| 10 | **历史版本 `stats` 扁平键是否回填**（API Q7） | **不回填**：历史计数按当时实际落库值原样返回，缺键不补 0；回填等于伪造历史。新版本统一用分组键（C3） | 产品 + DATA + API |
| 11 | **`operator_display` 口径**（API Q6） | 后端计算正确；`kind=ent/operator=py`→「系统（历史）」、`kind=seed/operator=system`→「系统（种子）」、其余原样；需与 DATA §3.4 `kind` 取值一致（含 C9 的显式写入） | 产品 + API + DATA |
| 12 | **`delete_edge` 是否只收 `edge_id`**（API Q8） | 同意；人工边与种子边同一身份，按 `graph_tech_edge.edge_id` 删最稳。需在 UI 明确「只有工作集内的边可删」（API-C7） | API + 前端 |

---

## 五、会签边界

- 本会签只覆盖算法 / 指标身份关心的字段语义、D9 血缘、跨稿一致性；不代替 DATA 身份对 DDL 可执行性、OWNER、备份窗口的判断，也不代替 PRODUCT 对交互文案的判断。
- 本会签**未**修改 API/DATA/METRIC/ARCH 任何稿件，未改 task-registry，未 git，未连库，未跑脚本/单测。
- 上述「必修」项闭合后，算法身份同意 API/DATA 进入实现；「建议」项不阻塞会签，但建议在实现单中逐条落点。

---

## 复核（2026-11-13 algorithm-agent）

**复核对象**：`TS-L2-M10-GRAPH-API.md` v2、`TS-L2-M10-GRAPH-DATA.md` v2（文末「会签回应」）。
**基准**：本会签单 ALGO-API-C1～C9、ALGO-DATA-C1～C12；`TS-L2-M10-GRAPH-L2-裁定.md` A/B 条；已签收 ARCH §4/§11。
**方法**：只读核对 v2 原文与代码，不改稿、不 git、不连库、不跑脚本。

### 一、ALGO-API 条件逐条

| 编号 | 级别 | 判定 | v2 落点 / 依据 |
|---|---|---|---|
| ALGO-API-C1 | 必修 | **闭合** | §5.3 新增「人工边**禁止输出** `evidenceLevel` 及任何 `evidence`/`evidenceType`」；同表人工边行补「不填 `weight`、不填 `strength`、不填 `year`、不计入 `weighted_degree`」；并写明人工边不进 35-3 hidden 计数（`API:419–421`；`PAN:178`、`PAN:372–373`；`read:286–300`） |
| ALGO-API-C2 | 必修 | **闭合** | §5.2 改为「entan 用自有 Nebula 只读会话（`entan.common.nebula`），显式 `USE demo_gkx_chain`，启动断言 `demo_gkx_` 前缀，非该 space 拒绝」，并明写「不得引用 chainan / `chain_space()`」（`API:402`）。经核 `session(use_space=False)` + `execute(sess, "USE …")` 可实现（`vendor/entan-py/entan/common/nebula.py:75–99`），不依赖未打包的 chainan |
| ALGO-API-C3 | 必修 | **闭合** | §3.4 明确「本节嵌套 JSON 是 `graph_version.stats` 与 `rollback:preview.counts` 的唯一持久化形状」，DATA 扁平键废止；DATA §5.2 已改为同一分组结构（`API:207–221`；`DATA:349–360`） |
| ALGO-API-C4 | 建议 | **闭合** | §5.3 总原则改为「叠加关闭逐字节一致；开启只改集合（删点/删边/路径移除、关键词补读、200 截断）并追加字段，不改存量行字段值」，不再写「只追加、不改已有字段」（`API:413`） |
| ALGO-API-C5 | 建议 | **闭合** | §5.3 新增 `relationTypeOptions` 行：可同时含存量英文码与人工三枚举，只作图例/筛选，不得驱动加边下拉（`API:423`） |
| ALGO-API-C6 | 建议 | **闭合** | §5.3 节点 id 行补「选中已软删点返回空图 + `emptyReason=GRAPH_EMPTY`，不 404、不回落默认点」；选中新点按 `tm:{id}`（`API:422`） |
| ALGO-API-C7 | 建议 | **闭合** | §2.3 新增边界：只有工作集 `graph_tech_edge` 内的边可删；Nebula 未纳入种子的 `tech_rel` 前端拿不到 `edge_id`；hidden 计数只服务删点确认框（`API:127–129`） |
| ALGO-API-C8 | 建议 | **闭合** | §5.1 `src/dst` 行补「int64，与 `nodes[].id`（string）不是同一命名空间；用 `nodes[].technology_id` 映射，禁止直接比较」（`API:385`） |
| ALGO-API-C9 | 建议 | **闭合** | §5.3 `nodes[]` 行补「全景出口 `importance` vs 主表 `/current` `importance_level` 不得混用、不得回写」（`API:418`） |

**API 小结**：3 条必修、6 条建议全部闭合；未发现 v2 对已签收 `weight` / `strength` / S4 / timeline 语义的破坏。

### 二、ALGO-DATA 条件逐条

| 编号 | 级别 | 判定 | v2 落点 / 依据 |
|---|---|---|---|
| ALGO-DATA-C1 | 必修 | **闭合** | §6.1 步骤 4 改为英文码白名单硬规则：命中 `包含`/`依赖`/`促进` 或非 ASCII 码跳过并计数，dry-run 打印 `{code,count}`，白名单外占比 >0 默认中止（除非监管人书面豁免）（`DATA:447`）。与裁定 B5 一致；auto/manual 不再同键 |
| ALGO-DATA-C2 | 必修 | **闭合** | §4.1 显式列清单补「排除生成列 `name_cn_active`」；§5.3 `technology_master` 还原行补「排除生成列 `name_cn_active`、排除 `updated_at`，避免 1062 / 3105」（`DATA:273`、`DATA:388`） |
| ALGO-DATA-C3 | 必修 | **闭合** | §5.2 改为 API §3.4 的分组 JSON（`tech_nodes` / `tech_edges` / `entity_links` / `entity_edges` / `entity_attrs`）；§6.3 种子版本、§8-H 列注释同步（`DATA:349–360`、`DATA:469`、`DATA:687`） |
| ALGO-DATA-C4 | 必修 | **闭合** | §6.1 步骤 5 新增硬规则：映射后 `src_tech_id == dst_tech_id` 丢弃；端点 `status != 'active'` 或映射不到跳过；dry-run 打印 `{self_loop,missing_endpoint,deleted_endpoint}`（`DATA:448`）。与 `API:101` 自环 422 同口径 |
| ALGO-DATA-C5 | 必修 | **闭合** | §2.1 明确 `rel_code` 用于已删存量边过滤；§2.3 删除过滤、§4.2 均写「auto 行按 `(端点无序对, rel_code)` 匹配，NULL 回退 `rel_type`，人工行不参与」；API §5.3 同步（`DATA:75/86/110/308`；`API:424`） |
| ALGO-DATA-C6 | 建议 | **闭合** | §6.1 步骤 6 定义同 `(pair,type)` 聚合：`strength_auto=MAX(confidence)`、`time_from=MIN(year)`、`time_to=NULL`；dry-run 打印重复组数；写明删除该行会隐藏该 pair+type 下全部 Nebula 边（`DATA:449`） |
| ALGO-DATA-C7 | 建议 | **闭合** | §6.4 读侧映射改为「按 `min(len)` zip；多出的 tnid/VID 一律跳过并 warning，不单独加入」，删除 v1 的二选一（`DATA:489`） |
| ALGO-DATA-C8 | 建议 | **闭合** | §2.5 增指标护栏：`read` / S4 种子 / 指标脚本不得读 `strength_auto` / `rel_code`；建议 `SCORE` 断言拒绝 `technology_master` / `graph_tech_edge`；单测断言人工边无 `weight`/`strength`/`evidenceLevel`；§7.5 复述（`DATA:129`、`DATA:595`）。METRIC v2 §3.2 已补 `graph_tech_edge.strength_auto` 黑名单（`METRIC:146`） |
| ALGO-DATA-C9 | 建议 | **闭合** | §3.4 `snapshot_status` 与 `kind` 取值明确；§5.2 步骤 6 写死 `kind='save'` 显式；§5.3 回滚写 `kind='rollback'`；§6.3 种子 `kind='seed'`；§8 注明默认 `'ent'` 只为历史平滑、代码必须显式写并断言（`DATA:182`、`DATA:336`、`DATA:376`、`DATA:469`、`DATA:687`） |
| ALGO-DATA-C10 | 建议 | **闭合** | §5.5 `node_id_map` 复原补「只取 `op='add_node'` 且 `after` 含 `client_node_id`；`update_node`/`delete_node` 不进映射」（`DATA:430`） |
| ALGO-DATA-C11 | 建议 | **闭合** | §5.2 步骤 11 写明 `graph_tech_edge` 逻辑状态与 `version_id` 在同一条 UPDATE 完成，不拆两次写（`DATA:344`） |
| ALGO-DATA-C12 | 建议 | **闭合** | §5.4 写死：名称 1062 → 422/42201；`graph_tech_edge` 1062 → 409/40901、整笔回滚、不落 `failed_items`（`DATA:408–409`），与 API §7 一致 |

**DATA 小结**：5 条必修、7 条建议全部闭合；`strength_auto` / `rel_code` 的「不消费」结论在 DATA 与 METRIC v2 中一致，S4 种子只扫 Nebula 的守护未被削弱。

### 三、v2 新引入问题（不阻塞，建议实现前澄清）

| # | 位置 | 问题 | 改法 |
|---|---|---|---|
| N1 | `DATA:340`（§5.2 步骤 10） | 级联边「各写一行 … `reason='cascade'` 的 change_log」，但 `graph_change_log` 实际列为 `change_id/change_set_id/version_id/object_type/object_id/op/before/after/operator/trace_id/at`，**没有 `reason` 列**（`DDL:36–52`）。按字面实现会 SQL 报错 | 改为「`after` JSON 内带 `{"reason":"cascade","edge_id":…}`」，或明确新增 `reason` 列并进快照/回滚；不要写不存在的列 |
| N2 | `API:419`（§5.3 人工边行） | 仍写 `timeRange:{from,to}`，未反映裁定 A6（36-3 时间范围选填）与 B14（种子允许 `to:null`）。人工边未填时间时，读出口应省略 `timeRange` 还是给 `{from:null,to:null}` 未定 | 改为 `timeRange?: {from:int,to:int|null}`；注明人工边未填则省略、种子边 `to` 可为 null；与 §5.1 `ServerTechEdge.time_range?` 一致 |
| N3 | `DATA:448`（§6.1 步骤 5） | 「端点主表 `status != 'active'` 或映射不到时跳过」中的「映射不到」有歧义：若按「当前主表无行」理解，切片内**新点**尚未 INSERT，会被误判而丢弃所有连边 | 明确「映射不到」指「不在本次切片点集」；切片内新点先写主表 `status='active'`，再按 `technology_id` 映射边，不得因主表暂无行而跳过 |
| N4 | `DATA:447`（§6.1 步骤 4） | 同一句既写「命中中文码/非 ASCII 一律**跳过**并计数」，又写「白名单外码占比 >0 默认**中止**」；与裁定 B5「跳过并记数」不完全一致，且两种模式互斥 | 拆开：三中文枚举 → 跳过并计数（B5）；白名单外其他非 ASCII → 默认中止（或按监管人书面豁免改跳过并 warning）；dry-run 先打印再决定 |

### 四、复核结论

- **API 册：同意会签。** ALGO-API-C1～C3 必修全部闭合，C4～C9 建议全部采纳；仅 N2 为实现措辞，不影响字段契约与已签收语义。
- **DATA 册：同意会签。** ALGO-DATA-C1～C5 必修全部闭合，C6～C12 建议全部采纳；N1/N3/N4 为数据面实现口径，建议实现单落一句话，不回退表结构 / 事务 / 快照方向。
- 裁定单落点核对：B1（`stats` 分组）、B3（entan Nebula 通道）、B4（`rel_code` 保留+过滤）、B5（种子跳过中文码/自环/缺端点）、B6（人工边无 `evidenceLevel`）、B7（`src/dst` number）、B8（auto/manual 并存）、B9（`strength_auto` 不出参）、B10（1062 分流）、A2（默认切片 #2）、A6（时间范围选填）均已在 v2 落文；未发现与裁定单冲突的算法语义。
- 本次复核未改 API/DATA/METRIC/ARCH 任何稿件，未改 task-registry，未 git，未连库，未跑脚本/单测。
