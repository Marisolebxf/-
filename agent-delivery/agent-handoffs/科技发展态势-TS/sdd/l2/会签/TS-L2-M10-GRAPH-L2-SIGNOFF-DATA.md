# TS-L2-M10-GRAPH-L2-SIGNOFF-DATA · API / METRIC 二级分册会签（数据身份）

- 审稿：`agent:data-agent`（独立会话）
- 日期：2026-11-13
- 对象：`TS-L2-M10-GRAPH-API.md`（草稿 v1）、`TS-L2-M10-GRAPH-METRIC.md`（草稿 v1）
- 基准：`TS-L2-M10-GRAPH-ARCH.md` v2（2026-11-13 监管人 `human:刘剑锋` 签收，§11 末尾「拍板结果」）
- 参照：`TS-L2-M10-GRAPH-DATA.md`（只查跨稿一致性，不审；该册由本身份起草）
- 方法：只读核对稿内字段与 as-built DDL / routes / read / seed；未改被审稿、未改其他文件、未 git、未连库、未建表、未跑脚本。
- 结论：**API 有条件同意（3 必修）**；**METRIC 有条件同意（4 必修）**。

## 一、`TS-L2-M10-GRAPH-API.md`（草稿 v1）

### 1.1 结论

接口形状、幂等、失败码、软删复活、版本读写方向与 ARCH v2 拍板一致；作为数据身份，有 **3 处会直接导致写错列或读不对数**，须改后再签：坐标列名与 DATA 不一致、`stats` 持久化形状与 DATA 冲突、种子边 `time_range` 无法按现契约表达。

### 1.2 必修条件

| 编号 | 级别 | 位置 | 问题 | 改成什么 | 证据 |
|---|---|---|---|---|---|
| DATA-API-C1 | 必修 | §2.1 `add_node` 字段表 `layout` 行；§5.1 节点 `layout` | API 写“落 `technology_master.x/y` 与 ADS `graph_entity_node.x/y`”，DATA 已定列名为 `layout_x` / `layout_y`。照 API 实现会写不存在的列，MySQL 1054 缺列，再按 API §7 被映射成 50302。 | 改为“落 `technology_master.layout_x/layout_y` 与 `graph_entity_node.layout_x/layout_y`（DATA §3.1/§3.3）”；§5.1 明确节点 `layout` 由 `graph_entity_node.layout_x/y` 组装，种子点两列为 NULL 时输出 `layout:null`。 | API:79、API:344；DATA:131-135、DATA:573-575、DATA:167；`tech_graph_maintain.sql:125-132`（现无坐标列） |
| DATA-API-C2 | 必修 | §3.4 `stats` 规范分组；§3.3 回执示例；§4.3 `counts` 示例 | API 的固定键是嵌套分组 `{tech_nodes:{added,updated,removed}, tech_edges:{added,removed}, …}`；DATA §5.2 的固定键是扁平 `node_add/node_del/node_upd/tech_edge_add/…`。两处都自称“固定键”，`graph_version.stats` 落库、版本列表与回滚预览会出现两套结构，40-3 与 40-4 对不上。 | §3.4 声明本节嵌套 JSON 是 `graph_version.stats` 与 `rollback:preview.counts` 的**唯一**持久化形状，给出完整键模板（沿用 §3.3 示例即可）；写明 DATA §5.2 扁平键列表废止、由 DATA 回改；历史版本旧扁平键原样返回、不回填、缺键不补 0。 | API:195-206、API:180-182、API:274-281；DATA:338、DATA:177、DATA:352；ARCH:99 |
| DATA-API-C3 | 必修 | §2.2 `time_range`；§5.1 `tech_edges[].time_range`；§8.2 前端类型 | API 把 `time_range` 定义为 `{from:int,to:int}`；DATA 种子边 `time_from=first_evidence_year`、`time_to=NULL`。只填 from 的种子边无法按该 shape 返回，前端类型也不接受 `to:null`。 | 明确两种合法形状：人工边 `{from,to}` 均非空；种子边允许 `{from:int,to:null}`（或整体省略，推荐保留 from）。§8.2 前端类型改 `time_range?: {from:number|null; to:number|null}`，§5.1 表格写清。 | API:104、API:340、API:465；DATA:81-82、DATA:426 |

### 1.3 建议条件

| 编号 | 级别 | 位置 | 问题 | 改成什么 | 证据 |
|---|---|---|---|---|---|
| DATA-API-S1 | 建议 | §3.3 `results` 持久化；§4.4 回滚回执 | 仍写“候选 `graph_version.publish_results`”，DATA 已定列；回滚 `results` 是否持久化未写。 | 去掉“候选”，写死 `graph_version.publish_results`；补一句回滚结果同列持久化，版本详情/审计可查（回滚本身不幂等，重试仍按 `base_version` 409）。 | API:189、API:296-306；DATA:177、DATA:332、DATA:352 |
| DATA-API-S2 | 建议 | §2.2 `src/dst`、§2.3 `edge_id`、§5.1 `tech_edges[].id/src/dst` | 列是 BIGINT（`technology_id` / `edge_id`），API 只写 `int`；JSON number 超过 2^53 会丢精度。 | 标注“int64（JSON number；实际值域远小于 2^53；Java 侧用 Long）”，并明确 id 不用字符串传输。 | API:100、API:118、API:337；DATA:75-76、DATA:85 |
| DATA-API-S3 | 建议 | §2.4 `update_node.patch.importance_level` | 只写枚举 高/中/低；DDL 列可空且默认 `'中'`。用户若要把等级清回 NULL，传 null 会被当枚举外 422 还是“不改”未定义。 | 明确 `importance_level:null` 表示写 NULL（清除），省略表示不改；validate 接受三枚举或 null。 | API:132、API:78；`tech_graph_maintain.sql:11`；DATA:323 |
| DATA-API-S4 | 建议 | §3.1 `changes` 幂等 | 同 `client_batch_id` 并发提交会撞唯一键 1062；DATA 只把 1062 映射 409/422，会把幂等重试变成失败。 | submit 捕获 1062 后按 `client_batch_id` 重读已存在 change_set，返回 `idempotent:true` 原回执；publish 的 1062 仍按 409。 | API:155-157；DATA:189、DATA:379 |
| DATA-API-S5 | 建议 | §2.5 / §3.3 `node_id_map` 复原 | 只说按 `change_log.after` 重建，未写过滤条件；`graph_change_log` 有 `op` 列，同 change_set 还含 `update_node`。 | 明确只扫 `op='add_node'` 且 `after.client_node_id` 非空的 after；无新增点返回 `{}`。 | API:146、API:189；`tech_graph_maintain.sql:44`；DATA:387 |
| DATA-API-S6 | 建议 | §3.4 历史 `stats`；§10-Q7 | 留了“是否由 DATA 回填规范键”的口子；DATA 的回填清单只含 `kind` / `snapshot_status`，不含 `stats`。 | 冻结“DATA 不回填 stats”；历史版本原样返回旧扁平键、缺键不补 0；§10-Q7 写死结论。 | API:205、API:505；DATA:203-230 |
| DATA-API-S7 | 建议 | §2.2 重复判定 | “命中同键已软删行 → 复活……种子边原强度字段保留”易被读成“种子边可由 add_edge 复活”；`add_edge` 的 `rel_type` 只收中文三枚举，种子边是英文原码，唯一键不同，实际命不中，种子边只能靠版本回滚恢复。 | 补一句“复活仅适用于同 `(src,dst,rel_type)` 的人工边；种子边英文码不因 add_edge 复活，恢复走回滚”；“种子边原强度字段保留”改为“若复活行原为 auto，`strength_auto` 保留不动”。 | API:106；DATA:89、DATA:109、DATA:112、DATA:119 |
| DATA-API-S8 | 建议 | §2.1 `category`；§10-Q1 | 默认自由文本，但未写落哪列、是否外键；`technology_master.category` 现为 `VARCHAR(64)`，`dim_tech_domain` 只是候选。 | 写明落 `technology_master.category`（VARCHAR(64) 自由文本），首版不做 FK、不做存在性校验；`dim_tech_domain.domain_code` 仅下拉候选；Q1 按此收口。 | API:76、API:499；`tech_graph_maintain.sql:10`、`:118-122` |
| DATA-API-S9 | 建议 | §3.3 publish body `client_batch_id` | 只写“一致性护栏”，未定义与 change_set 已存批次不一致时的行为；DATA 只在 change_set 已 published 时按批次匹配判幂等。 | 明确：提供了且 ≠ change_set.client_batch_id → 409/40901；未提供则忽略。 | API:171；DATA:317 |

### 1.4 无条件核对

- op 枚举 7→10，`add_node` / `add_edge` / `delete_edge` 字段与 DATA 列类型对得上：`name_cn` 1–256 对 `VARCHAR(256)`、`category` 1–64 对 `VARCHAR(64)`、`importance_level` 对 `VARCHAR(8)` 可空、`strength_manual` 0–10 对 `DECIMAL(10,4)`、`time_range` 年对 `INT`、`layout` 浮点对 `DOUBLE`。
- `client_batch_id`：`changes` 必填、`publish` 选填，与 DATA `VARCHAR(64)` + 唯一键（历史行 NULL 不冲突）一致。
- 失败码：1213/1205 → 409、1062 → 409/422、1146/1054/1049 → 50302、50301 退役，与 DATA §5.4 一致；50303 是 Java 下游不可达，数据层不产生，无冲突。
- 软删复活字段语义（status/source/strength_manual/time/version_id，`strength_auto` 与 `rel_code` 不动）与 DATA §2.3 一致，仅 S7 措辞需收紧。
- `results` 与版本、`change_log.after` 同事务写入、历史版本 `results:null`，与 DATA §3.4/§5.2/§5.5 一致，仅 S1 列名确定性需补。
- `node_id_map` 由 add_node 的 after 重建、`technology_id` 在发布事务内回填，与 DATA §5.5 一致，仅 S5 过滤条件需补。
- `/current.tech_edges[]` 只回 `status='active'`、不并入 `node.edges`，与 DATA §11-10 一致。
- `impact` 两项计数口径（工作集 active 边、Nebula 无向 HIGH/MEDIUM、失败 null）与 DATA §7.4 一致。
- 版本 `kind` / `snapshot_status` / `rollbackable` / `not_rollbackable_reason` 与 DATA §3.4 一致。

## 二、`TS-L2-M10-GRAPH-METRIC.md`（草稿 v1）

### 2.1 结论

34–40 零 `metric_id` 的结论与 ARCH §9、DATA-S4 一致，六类计数走 DN-A03-09 建议豁免的方向正确；但保护条款漏了 `graph_tech_edge.strength_auto`，S4 只有文档约束、没有可执行护栏，35-3 的 `tech_edge_count` 未写 active，40-3/40-4 的“同源”写法与 API 的回滚差异语义冲突。须改后再签。

### 2.2 必修条件

| 编号 | 级别 | 位置 | 问题 | 改成什么 | 证据 |
|---|---|---|---|---|---|
| DATA-METRIC-C1 | 必修 | §3.1 规则 1；§3.2 字段清单；§3.4 SEED-L01 行 | DATA 新增 `graph_tech_edge.strength_auto`，明确“留作历史快照，不参与人工强度与任何指标”；METRIC 字段清单只列 `strength_manual`，漏了 `strength_auto`。同库 `graph_entity_edge.strength_auto` 的列注释是“指标只取此列”，实现者极易照抄，把种子边原强度喂进 `M_TECH_EDGE_STRENGTH` 或 S4。 | §3.2 增行：`graph_tech_edge.strength_auto` 为 auto 原强度快照，只读展示/回滚保留，不映射 `weight` / `strength` / S4，不登记为任何指标源字段；§3.1 规则 1 的禁止清单加 `strength_auto`；§3.4 SEED-L01 行补“写 `strength_auto` 仅为快照，不产分数”。 | METRIC:125、METRIC:131-141、METRIC:160；DATA:79、DATA:680；`tech_graph_maintain.sql:140` |
| DATA-METRIC-C2 | 必修 | §3.4 S4 分数种子行；§7-4 | 目前只有文档约束“只扫 Nebula”，没有可执行护栏；S4 若被改为读 MySQL / 带 overlay 的读图结果，`tm:` 新点会拿 mock 分，人工强度也可能被消费。 | §3.4 写死脚本级 fail-closed 断言：只允许 Nebula 连接；出现 `technology_master` / `graph_tech_edge` / `overlay` 读取即抛错退出；`--check` 保持 fixture-only；§7-4 结论写“加断言”。 | METRIC:159、METRIC:223；ARCH:170-172；DATA:79、DATA:522 |
| DATA-METRIC-C3 | 必修 | §2.2 #1 `tech_edge_count` | 只写“工作集 `graph_tech_edge` 统计”，未写 `status='active'` 和双向；软删行仍占唯一键，会把已删边算进删除确认框。 | 写死 `WHERE status='active' AND (src=? OR dst=?)`，与 API §5.2、DATA §7.4 同口径。 | METRIC:104；API:353；DATA:518、DATA:96 |
| DATA-METRIC-C4 | 必修 | §2.3 规则 4 | “40-3 与 40-4 必须读同一份 `stats` 结构，避免同一版本两个数字对不上”语义混淆：40-4 的 `stats` 是某版本发布时的操作回执计数；40-3 的 `counts` 是“当前工作集 → 目标版本”的净差。两者不应相等，也不能拿版本 `stats` 当预览计数；按字面实现会强行让两个不同语义的数字相等。 | 改为“同一套分组键 + 同一快照差异函数”：`counts` 由 `rollback:preview` 的快照差异计算（added=目标有当前无，removed=当前有目标无，updated=两边都有但值不同），版本 `stats` 由发布回执计数；两者只共享键结构，不要求数值相同；禁止用某版本 `stats` 直接充当预览。 | METRIC:116；API:285；DATA:345、DATA:350 |

### 2.3 建议条件

| 编号 | 级别 | 位置 | 问题 | 改成什么 | 证据 |
|---|---|---|---|---|---|
| DATA-METRIC-S1 | 建议 | §3.2 `technology_master` 坐标行 | 写 `x` / `y`，DATA 定名 `layout_x` / `layout_y`。 | 改为 `layout_x` / `layout_y`，并注明“布局属性，不是度量”。 | METRIC:141；DATA:131-135 |
| DATA-METRIC-S2 | 建议 | §2.2 #4 回滚预览计数 | 文案“将撤回该版本之后的全部改动共 X 项”；API 的 `total` 是 added+removed+updated 之和，含“恢复”项，称“撤回”会误导。 | 拆成“撤回 R 项 / 恢复 A 项 / 更新 U 项”，或 X 只计 removed+updated；与 API §4.3 方向词对齐。 | METRIC:107；API:281-285 |
| DATA-METRIC-S3 | 建议 | §3.2 / §6 边界 | 未写 `graph_tech_edge` 与 D9 登记面的关系；只说“字段不得被读取”，未说表不作为任何指标源表。 | 补一句：`graph_tech_edge` 不登记为任何 metric 的源表，`strength_manual` / `strength_auto` 不进任何 8 件套；计数类不注册 `metric_id`，与 DATA §2.5/§7.5 一致。 | METRIC:131-141、METRIC:213-215；DATA:125、DATA:522 |
| DATA-METRIC-S4 | 建议 | §2.2 #6 `publish` 回执 `results` | 引 `routes:866-884` 说“随版本持久化”，但 routes 只负责现算；持久化落 `graph_version.publish_results`。 | 补 DATA 指针（`graph_version.publish_results`，同事务写入），避免实现只现算不落库。 | METRIC:109；DATA:177、DATA:332 |
| DATA-METRIC-S5 | 建议 | §2.2 #2 `panorama_hidden_relation_count` | 未说清是“该点关联总数”还是“扣掉已被其他已删端点过滤后实际少显示的条数”。 | 明确按“该点在 Nebula 的 HIGH/MEDIUM 关联数”计（gross），文案称“将隐藏（上限）”；与 API §5.2、DATA §7.4 同口径。 | METRIC:105；API:354；DATA:518 |
| DATA-METRIC-S6 | 建议 | §3.2 `rel_type` 行 | 只说“不映射成 `M_TECH_EDGE_STRENGTH` 的 `relation_type`”，未说种子英文码的长度/维度边界。 | 补“种子边英文码是显示原码，列宽 `VARCHAR(32)`，不作为指标维度、不拆 relation_type 维度”。 | METRIC:137；DATA:77、DATA:89 |

### 2.4 无条件核对

- 34–40 零 `metric_id`、29 行中 24 行无数字、5 行有数字（4 计数 + 1 人工值），与 ARCH §9-5、DATA-S4 一致。
- 六类计数范围（35-3 两项、39-1、40-3、40-4、publish `results`）与 API/DATA 对应字段一致；不挂 ⓘ、不挂 MockBadge、不注册 ID 的方向正确。
- `strength_manual` 不进 `weight` / `strength` / S4 的五句与 ARCH §9 一致；DATA 列注释与 DATA §2.1 一致。
- `importance_level` 是表单枚举、种子点显式 NULL、不吃默认 `'中'`，与 DATA §6.3/§6.5、DDL 列可空一致。
- `category` / `description` / `name_cn` / `name_en` 只作显示覆盖、不进指标，与 DATA/API 一致。
- 12 项已签收 DS02 指标不受影响的结论方向成立：`weight` / `strength` / `keyPathOptions` / S4 三项 / `M_TECH_GRAPH_STRUCT` / `M_TECH_EDGE_STRENGTH` / `M_TECH_GRAPH_105_1` / `M_TECH_PATH_*` / 实体面。
- 人工边不写 `weight`、不写 `year`、不进 timeline；`relationTypeOptions` 会多出三个中文类型，与 API §5.3 一致。
- 新点 `tm:` 无 S4 分数、`centrality:null`、`influence` 不出现，与 API §5.3、ARCH §4.2 一致。

## 三、跨稿一致性

| 项 | API 册 | DATA 册 | METRIC / ARCH | 结论与动作 |
|---|---|---|---|---|
| `stats` 固定键 | 嵌套分组 `tech_nodes{added,updated,removed}…` | 扁平 `node_add/node_del/node_upd/tech_edge_add…` | METRIC §2.2 #5 只写分组语义；ARCH:99 只说“固定键” | **冲突**。以 API 嵌套为唯一形状，API 补“DATA §5.2 废止”；DATA §5.2 由 data-agent 回改（不在本单改） |
| 坐标列名 | `x/y` | `layout_x/layout_y` | METRIC §3.2 写 `x/y` | **不一致**。API C1、METRIC S1 改为 DATA 列名 |
| `time_range` | 人工 `{from,to}`；种子边未定义半开 | 种子边 `time_from` 有值、`time_to` NULL | METRIC 不管；ARCH 只写时间范围 | **缺口**。API C3 定义种子边 `{from,to:null}` 或省略 |
| `results` 列 | “候选 `graph_version.publish_results`” | 已定 `publish_results` JSON，发布/回滚都写 | METRIC 引 routes 说持久化 | **需收紧**。API S1 写死列名并补回滚持久化 |
| `client_batch_id` | `changes` 必填、`publish` 选填 | `VARCHAR(64)` 可空 + 唯一键，历史 NULL；新写必须有值 | ARCH:82 批次幂等 | 一致。API S4/S9 补并发 1062 与不一致批次处理 |
| 失败码 | 50303 新增；50301 退役；1213/1205→409；1062→409/422 | 50301 退役；1213/1205→409；1062→409/422 | ARCH §7 同 | 一致。50303 是 Java 下游不可达，数据层不产生 |
| 软删复活 | 命中同键已删行复活；种子边原强度保留 | UPDATE 复活，source=manual，`strength_auto`/`rel_code` 不动；种子重跑不改 status/source | ARCH §2 同 | 语义一致。API S7 补“种子英文码不经 add_edge 复活” |
| `node_id_map` | 由 `change_log.after` 重建 | after = 发布后主表行 + `client_node_id` | ARCH:82 同 | 一致。API S5 补 `op='add_node'` 过滤 |
| 历史旧 `stats` | 原样返回、缺键不补 0；Q7 问是否回填 | 回填清单只含 `kind`/`snapshot_status`，不含 `stats` | METRIC 不涉及 | **建议冻结“不回填”**（API S6） |
| `strength_auto` | `/current.tech_edges[]` 不暴露；`add_edge` 只写 `strength_manual` | 新增列，快照保留，不参与人工强度/指标 | METRIC 字段清单漏列 | **METRIC C1 必修**；API 是否需要展示原强度，可在 FE 实现单另定 |
| 字段类型 | `int` / `number` / 0–10 step 0.01 / 年 | `BIGINT` / `DOUBLE` / `DECIMAL(10,4)` / `INT` | METRIC 不涉及 | 兼容。API S2 补 int64/JSON number 精度说明 |
| `category` | 自由文本 1–64，首版无 FK | 现有列 `VARCHAR(64)`，DATA 不新增维表 FK | METRIC 列为显示覆盖值 | 一致。API S8 写死落列与无 FK |
| 名称唯一键 | 只查 active；`name_cn_active` 生成列 | 生成列 + 唯一索引替换 `uk_name_cn` | ARCH §2 同 | 一致；DDL 由监管人执行前备份（DATA §10） |
| 回滚预览方向 | added=目标有当前无（恢复）；removed=当前有目标无（撤回） | §5.3 只写“新增/修改/删除” | METRIC §2.3-4 误写“同源” | API 定义清楚；DATA §5.3 建议按 API 方向词回改（不在本单改）；METRIC C4 必修 |
| `rel_type` 列宽 | 人工三枚举；种子英文码不映射 | `VARCHAR(32)`；种子原码 | METRIC 不映射为指标维度 | 一致；DATA 种子脚本应断言英文码 ≤32（DATA 侧实现单） |
| `kind`/`snapshot_status` | save/rollback/seed/ent；ok/skipped_oversize/none | `VARCHAR(16)` 两列，历史回填 ent/none | ARCH §2 同 | 一致 |
| impact 两计数 | active 工作集边；Nebula 无向 HIGH/MEDIUM，失败 null | §7.4 同口径 | METRIC #1 未写 active、#2 未写 gross/net | API 一致；**METRIC C3 必修**，S5 建议 |

## 四、需监管人拍板

| # | 事项 | data-agent 意见 | 建议拍板人 |
|---|---|---|---|
| 1 | API Q1：`add_node.category` 是否强制 `dim_tech_domain` 外键 | 首版自由文本落 `technology_master.category VARCHAR(64)`，不做 FK、不做存在性校验；维表只在维表灌好后做下拉候选，避免未灌时 400。 | 监管人 / 产品 |
| 2 | API Q2：`update_node` 是否接受 `layout` | 不收。拖拽禁用，只有 `add_node` 持久化落点；后续要拖拽持久化则另加字段并升版。 | 产品 / 前端 |
| 3 | API Q3：`importance_level` 省略写 NULL 还是吃默认 `'中'` | 写 NULL；种子点同样显式 NULL。建议 `update_node` 也允许传 null 清除，否则默认值无法被清掉。 | API / DATA |
| 4 | API Q4：强度/时间口径 | 同意 0–10、步长 0.01（列 `DECIMAL(10,4)` 可容纳）；年份 1900–2100 整数、from≤to（列 `INT`）。FE 负责 0–1→0–10 与文本→整数换算。 | 前端 / 产品 |
| 5 | API Q5：50301 退役、Java 下游不可达改 50303 | 同意。数据层不再产生 50301；50303 只在 display/topic Feign 层产生，不与数据码冲突。 | API / 前端（跨仓契约） |
| 6 | API Q6：`operator_display` 归后端 | 同意。数据层只存原始 `operator`，展示规则由 Python 统一算，不新增列。 | 产品 / API |
| 7 | API Q7：历史版本旧扁平 `stats` 是否由 DATA 回填 | **不回填**。旧版本的操作计数无法可靠重建；版本列表/详情原样返回旧键，缺键不补 0。请把 Q7 结论写死。 | 监管人 / API / DATA |
| 8 | API Q8：`delete_edge` 只收 `edge_id` | 同意。`graph_tech_edge.edge_id` 是稳定主键，人工边与种子边同一身份，软删后仍可回滚恢复；前端从 `/current.tech_edges[].id` 取。 | API / 前端 |
| 9 | METRIC Q1：DN-A03-09 豁免范围是否一次裁全 | 同意六类（35-3 两项、39-1、40-3、40-4、publish `results`）；数据侧不注册 `metric_id`、不建指标事实表。建议 PM / 数据 Lead 一次裁定，未裁前维持“建议豁免”措辞。 | PM / 数据 Lead |
| 10 | METRIC Q2：删存量点/种子边导致全景可见集合变小，是否知会 DS02 监管人 | 需要知会 `human:淮政玮`。这不是口径变化，是已发布工作集的显示结果；但已签收页面的图例项、路径条数会变。 | 监管人 / 淮政玮 |
| 11 | METRIC Q3：人工强度“人工”标注落点 | 数据层只保证 `strength_manual` 是唯一人工强度来源；标注位置（36-3 弹窗或关系标签）由 FE 实现单定，必须出现“人工”字样。 | 前端 / 产品 |
| 12 | METRIC Q4：S4 分数种子是否加脚本断言 | 必须加。只允许 Nebula 连接；读取 `technology_master` / `graph_tech_edge` / 带 `overlay` 的读图结果即 fail-closed；`--check` 保持 fixture-only。已列 DATA-METRIC-C2。 | 算法 / DATA |
| 13 | METRIC Q5：40-3 与 40-4 数字是否强制同源 | 不要求数值相同。要求同一套分组键 + 同一快照差异函数：`counts` 是当前→目标的净差，版本 `stats` 是发布回执计数。按字面“同一份 stats”会实现错。已列 DATA-METRIC-C4。 | API / DATA |
| 14 | METRIC Q6：`weight` / `strength`（加权度）身份问题 | 维持留在 `DS-02-METRIC-OPEN-L01`，本次不收口。人工层不改这两者的取值与身份；若监管人要求本次收口，需另派任务。 | 监管人 / 算法 |
| 15 | 跨稿依赖：DATA §10 名称唯一键是否另需数据平台 Owner 书面确认 | ARCH 已同意“只约束 active”的停机变更；DATA §10 仍建议共享 demo 库改唯一键前拿 Owner 书面确认。属 DATA 册执行前置，不在本单改稿。 | 监管人 / 数据平台 Owner |

## 五、会签边界

- 本单只审 API、METRIC 两册；DATA 册只用于跨稿一致性核对，不在此判其条件。
- 未改被审稿、未改 DATA/ARCH、未改 `task-registry`、未 git、未连库、未建表、未跑脚本。
- 条件闭合后，建议由起草方在各自册内回改并在本单追加“复核”节；跨稿项（尤其 `stats` 形状与坐标列名）需 API、DATA 两侧同时回改后再派实现。

---

*会签：`agent:data-agent` · 2026-11-13 · 只读核对 · 未改其他文件 / 未 git / 未连库*

## 复核（2026-11-13 data-agent）

- 复核对象：`TS-L2-M10-GRAPH-API.md` v2、`TS-L2-M10-GRAPH-METRIC.md` v2。
- 对照：`会签/TS-L2-M10-GRAPH-L2-裁定.md`（A1–A8、B1–B20）、`TS-L2-M10-GRAPH-DATA.md` v2。
- 边界：只读核对；本节只追加，未改被审稿或其他文件；未 git、未连库、未跑脚本。

### 一、API 册：原条件逐条核对

| 编号 | 级别 | 结论 | 核对证据 |
|---|---|---|---|
| DATA-API-C1 | 必修 | **闭合** | §2.1:81 明确坐标落 `technology_master.layout_x/layout_y`（主表权威）、ADS `graph_entity_node.layout_x/layout_y`（镜像）；§5.1:392 由 ADS 列组装出参 `layout{x,y}`，种子 NULL；DATA v2 DDL:640、:653 同名同类型。与裁定 B2 一致 |
| DATA-API-C2 | 必修 | **闭合** | §3.4:213 声明本节嵌套 JSON 是 `graph_version.stats` 与 `rollback:preview.counts` 的**唯一持久化形状**；§3.4:216–221 给出五组键矩阵；:225 历史四种旧形状原样返回、缺组不补 0；DATA v2 §5.2:353–367 已同结构，扁平键废止。与裁定 B1 一致 |
| DATA-API-C3 | 必修 | **闭合** | 人工边 §2.2:107 改为**选填**，填则 1900–2100、`from ≤ to`，省略/null 不设范围（A6）；种子边 §5.1:388 允许 `{from:int,to:null}` 或整体省略、不补 `to`（B14）；DATA v2:79、:623 `time_to` 可 NULL。与 A6/B14 一致 |
| DATA-API-S1 | 建议 | **闭合** | §3.3:204–205 `results` 随版本行持久化到 `graph_version.publish_results`，与版本、`change_log.after` 同事务；历史无值返回 `results:null`；§4.4:338–340 回滚同结构持久化 |
| DATA-API-S2 | 建议 | **闭合** | §2.3:123 `edge_id` 标 int64（JSON number，Java Long）；§5.1:384–385 `id` 同，`src/dst` 为 `technology_id` int64 并与 `nodes[].id` 明确区分命名空间 |
| DATA-API-S3 | 建议 | **闭合** | §2.4:138 `update_node.importance_level` 传 `null`=写 NULL 清除、省略=不改；§2.1:80 `add_node` 缺省/null 写 NULL，不吃 DDL 默认「中」 |
| DATA-API-S4 | 建议 | **闭合** | §3.1:166 并发同批撞 1062 → 按 `client_batch_id` 重读已存在行并返回 `idempotent:true`，不把幂等重试报成失败 |
| DATA-API-S5 | 建议 | **闭合** | §2.5:144–149 `node_id_map` 只由 `op='add_node'` 且 `after.client_node_id` 非空的记录重建，回滚返回 `{}`（§4.4:333） |
| DATA-API-S6 | 建议 | **闭合** | §3.4:225 明确历史 `stats` 原样返回、不回填，DATA 回填清单不含 `stats`；§10-Q7:569 写死「不回填」 |
| DATA-API-S7 | 建议 | **闭合** | §2.2:110 明确种子边英文 `rel_type` 与中文三枚举不同键，不能经 `add_edge` 复活，只走回滚或种子重跑 |
| DATA-API-S8 | 建议 | **闭合** | §2.1:78 `category` 落 `technology_master.category VARCHAR(64)`，只校验非空+≤64，不做外键/存在性校验；§10-Q1:563 同 |
| DATA-API-S9 | 建议 | **闭合** | §3.3:186 带 batch 且与已存值不符 → 409；不带或相同 → 返回原回执；§4.2:181–183 preview 的 batch 仅作一致性护栏 |

#### API 新问题（v2 引入）

| 编号 | 级别 | 问题 | 改法 |
|---|---|---|---|
| DATA-API-N1 | **必修（表述澄清，不改实现方向）** | §3.4:223 作为「唯一口径」写「`stats` 与 `counts` **不是同一份数据、数值不要求相等**；禁止拿某版本 `stats` 直接充当预览计数」。该句对 `kind='rollback'` 版本不成立：按 B12 与 §4.3:324，回滚生成的新版本 `stats` 就是生成它的那次回滚的 `counts`（同一求差函数、数值相等）。§3.4 的泛化表述与 §4.3 自相矛盾，实现方可能据此把回滚版本 `stats` 与预览 `counts` 做成两套算法，破坏 40-3/40-4 同源验收 | 把 :223 改为按 `kind` 分述：save/seed 版本 `stats` 是发布回执计数；`kind='rollback'` 版本 `stats` 是本次回滚的求差结果，与生成它的 `rollback:preview.counts` 同源相等。把「不是同一份数据」限定为「`counts` 与**目标版本自己的** `stats` 不是同一份数据」，禁止语同步限定为「禁止拿**目标版本** `stats` 充当预览计数」 |

**API 结论：仍有条件。** 原 DATA-API-C1～C3、S1～S9 全部闭合；仅新增 DATA-API-N1 一项必修（一句话澄清，不影响已定字段与接口形状）。

### 二、METRIC 册：原条件逐条核对

| 编号 | 级别 | 结论 | 核对证据 |
|---|---|---|---|
| DATA-METRIC-C1 | 必修 | **闭合** | §3.1:135 人工强度条款同时点名 `strength_manual` 与 `strength_auto` 不得进 `weight` / 点 `strength` / S4；§3.2:146 新增 `graph_tech_edge.strength_auto` 黑名单行，明确不得照抄 `graph_entity_edge`「指标只取此列」注释；§3.4:174 种子只作历史快照、不产分数 |
| DATA-METRIC-C2 | 必修 | **闭合** | §3.4:173 把 S4 分数种子改为**脚本级 fail-closed 断言**：只允许 Nebula 连接；读取 `technology_master` / `graph_tech_edge` / 带 `overlay` 的读图结果即抛错；不得改调 `read_graph`；`--check` 保持 fixture-only；§3.5:185 列为验收项 |
| DATA-METRIC-C3 | 必修 | **闭合** | §2.2 #1:112 `tech_edge_count` 明确 `status='active'` 且 `(src=? OR dst=?)`，双向都算；与 B15、DATA §7.4 一致 |
| DATA-METRIC-C4 | 必修 | **闭合** | §2.3-4:124 改为「同一套分组键 + 同一个快照求差函数」；明确 40-4 `stats` 是该版本自己的回执、40-3 `counts` 是目标快照与当前工作集求差，真正同源的是 40-3 `counts` 与**回滚产生的新版本** `stats`；禁止拿目标版本 `stats` 充当预览计数。与 B12 一致 |
| DATA-METRIC-S1 | 建议 | **闭合** | §3.2:152 补 `layout_x` / `layout_y`，标注为布局属性、不参与指标（B2） |
| DATA-METRIC-S2 | 建议 | **闭合（部分采纳，理由成立）** | §2.2 #4:114、§2.3-5 已拆分「恢复 / 撤回 / 还原」文案；`X` 保留 `total=added+removed+updated` 而非只计 `removed+updated`，与 API §4.3:329、PROD 文案一致，避免确认框漏掉恢复量。建议级部分不采纳可接受 |
| DATA-METRIC-S3 | 建议 | **闭合** | §3.2:154、§6:241 明确 `graph_tech_edge` 不登记为任何 `metric_id` 的源表；`strength_manual` / `strength_auto` 不进 8 件套 |
| DATA-METRIC-S4 | 建议 | **闭合** | §2.2 #6 补 `graph_version.publish_results` 同事务持久化；#7 回滚 `results` 同列持久化 |
| DATA-METRIC-S5 | 建议 | **闭合** | §2.2 #2:113 `panorama_hidden_relation_count` 按 gross 计、文案「将隐藏（上限）」、失败 `null`，不扣其他过滤 |
| DATA-METRIC-S6 | 建议 | **闭合（口径部分）；残留事实勘误见下** | §3.2:148 已写「列宽由 DATA DDL 定，不在本册写死」，符合建议本意；但括注「现 `VARCHAR(32)`」与 DATA v2 已定的 `VARCHAR(64)` 不符（DATA:74、:618），且与本册 §8:276「不采纳写死列宽」的回应自相矛盾 |

#### METRIC 新问题（v2 引入）

| 编号 | 级别 | 问题 | 改法 |
|---|---|---|---|
| DATA-METRIC-N1 | 建议（事实勘误） | §3.2:148 `graph_tech_edge.rel_type` 行写「现 `VARCHAR(32)`，API-DATA-C11 建议放宽至 64」，但 DATA v2 已定为 `VARCHAR(64)`（DATA:74、:618），且本册 §8:276 声称不写死列宽。属过时事实 | 删掉「现 `VARCHAR(32)`，API-DATA-C11 建议放宽至 64」，改为「列宽以 DATA DDL 为准（v2 已定 `VARCHAR(64)`），不在本册写死」 |
| DATA-METRIC-N2 | 建议（口径同步） | §2.2 #4:114 `tech_edges{added,removed}` 后仍写「若 API 补 `updated` 则加」；API v2 §3.4:218 与 §4.3 示例已确定 `tech_edges.updated`，条件句已无必要，保留会让实现方以为可能没有该键 | 改为无条件 `tech_edges{added,updated,removed}`，与 API §3.4 键矩阵逐字一致 |

**METRIC 结论：同意会签。** 原 DATA-METRIC-C1～C4、S1～S6 全部闭合或建议级部分采纳且理由成立；N1/N2 为不阻塞的勘误与措辞同步，建议随下版一并修。

### 三、跨稿一致性（与 DATA 册 v2）

| 项 | API v2 | METRIC v2 | DATA v2 | 结论 |
|---|---|---|---|---|
| 坐标列名 | `technology_master.layout_x/layout_y`、ADS 同名（API:81、:392） | `layout_x/layout_y`（METRIC:152） | 主表:640、ADS:653 | **一致**（B2） |
| `stats` 形状 | 五组嵌套 JSON 为唯一形状（API:211–225） | 以 API §3.4 为唯一口径（METRIC:115、:124） | §5.2:353–367 同结构；历史不回填 | **一致**（B1）。DATA:360 仍留「若 API 最终键矩阵不含 `updated`」条件句，API 已含，建议 DATA 侧删条件句（跨稿备注，不构成本单条件） |
| `time_range` 开放端 | 人工选填；种子 `{from,to:null}` 或省略（API:107、:388） | 不涉及 | `time_to` 可 NULL、种子不补 `to`（DATA:79、:449、:623） | **一致**（A6/B14） |
| `client_batch_id` 选填 | 选填；缺省服务端生成并回显，仅显式提供才享重试幂等（API:39、:161） | 不涉及 | §3.5 正文:201、DDL:662、回填:750 同 | **行为一致**（A7）。DATA:198 表格仍写「前端每次『保存图谱』生成」，与下方:201 的「可缺省」冲突，建议 DATA 侧改为「可缺省；缺省服务端生成」（跨稿备注，不构成本单条件） |
| `rel_type` 列宽 | 不涉及 | §3.2:148 写 `VARCHAR(32)`（过时） | `VARCHAR(64)`（:74、:618） | **不一致，已列 DATA-METRIC-N1**（METRIC 侧勘误即可，不影响 DDL） |

### 四、复核结论

- **API 册：仍有条件。** 原 12 项条件全部闭合；新增 DATA-API-N1 一项必修，仅澄清 §3.4 对 `kind='rollback'` 的 `stats`/`counts` 关系，改一句话即可，不涉及字段、接口形状或 DDL。
- **METRIC 册：同意会签。** 原 10 项条件全部闭合；DATA-METRIC-N1（`rel_type` 列宽事实过时）、N2（`tech_edges.updated` 条件句）为不阻塞勘误。
- 跨稿四项（列名、`stats` 形状、`time_range` 开放端、`client_batch_id` 选填）实质一致；DATA 册两处措辞（:198、:360）建议起草方顺手同步，不作为本单会签条件。
- 本节只读核对，未改被审稿、DATA/ARCH、`task-registry`；未 git、未连库。

---

*复核：`agent:data-agent` · 2026-11-13 · 只读 · 未改其他文件 / 未 git / 未连库*

## 最终确认（2026-11-13 data-agent）

- 复核范围：仅 v2.1 对 DATA-API-N1、DATA-METRIC-N1、DATA-METRIC-N2 及 DATA 册两处措辞的修改；未重审其他内容。
- API §3.4:223–228 已按 `kind` 分别定义：`save`/`seed`/历史 `ent` 的 `stats` 是发布回执；`kind='rollback'` 的新版本 `stats` 就是生成它的那次 `rollback:preview` 的 `counts`（同一求差函数、同一次结果）；`counts` 始终是目标快照与当前工作集的净差；禁止语已限定为「不得拿目标版本自己的 `stats` 充当预览计数」。**DATA-API-N1 闭合**，与裁定 B12、API §4.3 一致。
- METRIC §3.2:148 已改为「列宽见 DATA 册，本册不写死」，不再出现 `VARCHAR(32)`；§2.2 #6 已改为确定的 `tech_edges{added,updated,removed}`，条件句删除；§8:298 记录 v2.1 清理。**DATA-METRIC-N1、N2 闭合**，API、DATA、METRIC 三册键矩阵一致。
- DATA 册附带清理已核：`:198` 改为「前端生成；缺省时服务端生成，不享受重试幂等」，与 A7、API §1 一致；`:365` 已删「若 API 最终键矩阵不含 `updated`」，写明 API v2 §3.4 已正式包含该键。无新增数据面问题。

**最终结论：API 册同意会签；METRIC 册同意会签。两份均无未闭合条件。**

---

*最终确认：`agent:data-agent` · 2026-11-13 · 只读 · 未改其他文件 / 未 git / 未连库*
