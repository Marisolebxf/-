# TS-L2-M10-GRAPH-SIGNOFF-API · 维护管理 · 维护技术图谱 · 接口会签

- 角色：`agent:api-agent`
- 日期：2026-11-13
- 对象：`sdd/l2/TS-L2-M10-GRAPH-ARCH.md`（草稿 v1，归 `agent:arch-agent`；主审 §0 范围 / §1 架构要点 / §3 版本回滚 / §4 全景叠加 / §6 核查表 / §7 错误）
- 监管：`human:刘剑锋`
- 范围：**只读核对**。不改被审稿、不改其他文件、不改 task-registry、不 git、不连库、不建表
- 依据：`产品实现规程.md` §4.2.4（:307–313「审稿身份必须站在本身份立场找问题」）；审稿硬清单 `gkx-fde-design-change/审稿硬清单.md`（api-agent 4 问）；需规 `bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md` 序 34–40（:260–363）；决策简报 `2026-11-13-维护技术图谱-需规分句闭合.md`（卡 1B/2A/3A）；先例 `TS-L2-M10-ENT-ARCH.md` / `TS-L2-M10-ENT-API.md` / `会签/TS-L2-M10-ENT-SIGNOFF-API.md`
- as-built 核对（2026-11-13 自读，不采信稿述）：Python `vendor/entan-py/api/tech_graph_maintain_routes.py`（下称 **routes**）、`scripts/mysql/tech_graph_maintain.sql`（**DDL**）、`lumen_common/algorithms/tech_graph_read.py`（**read**）、Java `gkxlumen-topic/.../TechGraphMaintainController.java` + `TechGraphMaintainClient.java`、`gkxlumen-display/.../SituationMaintainEntController.java` + `feign/RemoteTechGraphMaintainClient.java` + `service/TechGraphReadAdapter.java` + `service/SituationPanoramaService.java`、FE `src/api/situation/maintain-ent.ts` + `views/situation/maintain/`

## 结论

**有条件同意。** 主线（ENT 链复用、单写者、不写 Nebula、整图快照回滚、全景读时叠加）方向成立，op 命名 `add_node / add_edge / delete_edge` 与 A03 及 ENT 会签 API-C1 先例一致，无越层、无 mock 兜底、无新开平行链。但作为接口身份，以下 **11 条必修** 未闭合前不宜签收：核心是 3 个新 op 的请求/回执形状与临时号语义未冻结、版本四端点三层挂法未落、`overlay` 与人工边 `source` 两个字段实际穿不过/会被 Java 丢弃、版本「类型/改动计数」无存储列、`change_log` 不认新 op、幂等键只查首条 op、以及「不写 Nebula」在复用 op 上被现有 `_project_nebula` 破例。条件清掉后可作 `TS-L2-M10-GRAPH-API` 的架构底座；DTO/错误码终裁归 API 分册。

## 条件表

> 级别：必修＝不闭合不签收；建议＝可在 API/DATA/前端实现单吸收。证据为 `文件:行号`。每条落到「改稿哪一节、改成什么」。

| # | 级别 | 条件（改哪一节、改成什么） | 证据 |
|---|---|---|---|
| API-C1 | 必修 | **3 个新 op 的请求/回执形状未冻结**。§0 只写「新 op add_node / add_edge / delete_edge」，§1-2 只写临时号，§6 只列界面。请在 §1 或 §6 增一张「新 op 契约表」，至少写死：① `add_node` 入参 `client_node_id`(临时串，同批唯一) + `name_cn/category/description/importance_level` + `layout{x,y}`（坐标口径＝0–100 百分比，对齐 FE `types/maintain.ts:89`），**不带 technology_id**；② `add_edge` 两端引用形状二选一：`{technology_id:int}` 或 `{client_node_id:str}`（不能混成裸值）；`rel_type∈{包含,依赖,促进}`、`strength_manual`、`time_range{from,to}` 年粒度；③ `delete_edge` 身份：人工边用服务端主键或 `(src,dst,rel_type)`，种子边用 §2 的「存量键」，两种必须让客户端可判；④ **`client_node_id → technology_id` 映射出现在 publish 回执**（changes 回执只有 `{change_set_id,status}`，`routes:773–778`），并明确前后端保证 add_node 先于 add_edge（服务端两遍处理或前端排序，二选一写死）；⑤ 同端点同类型重复的「方向」语义（有序对还是无向）。 | 稿 `:18–21`、`:60–61`、`:139`、`:146`、`:150`；`routes:33–41`（`OPS_ALLOWED` 无 3 op）、`routes:560–745`（`_validate_structure` 仅 7 op）、`routes:905–958`（`_apply_master` 无 add）、`routes:1014+`（`_project_ads` 无 add/delete tech edge）；`src/types/maintainEnt.ts:90–102`（`GraphOp` 仅 7） |
| API-C2 | 必修 | **版本四端点（列表/详情/回滚/预览）的三层挂法缺失**。§1 图只写 `GET versions`、`POST versions/{id}/rollback`，未落 display→topic→Python 各层。请在 §3 或 §1 增「端点挂法表」：对外 `GET/POST /display/v1/situation/maintain-ent/graph/versions…`；topic `…/topic/v1/tech/graph/versions…`；Python `…/internal/v1/sci/tech/graph/versions…`。并写明：回滚是 POST，**必须走 `relayWrite` 登录守卫**（不是裸 `relay`）；版本读写仅 Python 读 DWD（Java 不扫 DWD，D3），topic/display 只代理。 | 稿 `:44`、`:50–52`、`:84–93`；`SituationMaintainEntController.java:105–127`（`relayWrite` 仅对写生效）、`RemoteTechGraphMaintainClient.java:21–63`（无 versions）；`TechGraphMaintainController.java:34–42`（无 versions）；`routes` 路由清单仅 9 条无 versions/rollback（`grep @router`）；`architecture-baseline.md:130`（D3 Java 只读 ADS） |
| API-C3 | 必修 | **40-2 版本说明的载体未定义，publish 无 body 且写死 label/operator**。§3 写「保存时可填版本说明（写 graph_version.label）」，但发布端点现无入参、版本行 label 写死 `publish {change_set_id}`、operator 写死 `"py"`。请二选一写死：① `POST …/publish` 增 body `{label}`（display 同步注入 operator），topic client 加 `@RequestBody`；② 在 `changes` 提交时带 `label` 落 `change_set`（需 DATA 加列），publish 读取。同时把 §1-6 的「display 注入 operator」扩到 publish/rollback 请求（版本 operator 取 change_set.operator）。 | 稿 `:65`、`:86`、`:159`；`routes:843–844`（label/`"py"` 写死）、`routes:755`（changes 才收 operator）；`RemoteTechGraphMaintainClient.java:37–38`、`SituationMaintainEntController.java:71–74`（publish 无 body） |
| API-C4 | 必修 | **§4 的 `overlay.status` 到不了前端，§4/§8「Java 只追加、不改」不成立**。`TechGraphReadAdapter` 确实透传，但下游 `SituationPanoramaService.assemble` **重建**只含 `nodes/relations/keyPathOptions/timeline/listRecords/relationTypeOptions/factorItems` 七个顶层字段，所有未知顶层字段（含 `overlay`）被丢弃；节点/关系上的追加字段能穿过。请改稿 §4「出口形状」与 §8「不改 Java」：明确 **要么** 在 `SituationPanoramaService` 增 `overlay` 透传（一行级改动，不碰 Controller/Adapter），**要么** 删掉 `overlay.status` 契约并取消叠加失败提示（与 PRODUCT-C8 冲突，不建议）。 | 稿 `:110–111`、`:184`；`SituationPanoramaService.java:210–225`（result 仅 7 键）；`TechGraphReadAdapter.java:49`（`Outcome.ok(data)` 原样） |
| API-C5 | 必修 | **§4 人工边 `source:"manual"` 与全景 relation 的端点字段同名冲突，会把人工边整条过滤掉**。全景 relation 形状里 `source` 是**起点 id**（`read._relation` 固定写 `source: src["id"]`），Java 在选中技术点模式下用 `row.get("source")` 做端点保留判断；写成 `source:"manual"` 后该边不再命中任何节点，被 `removeIf` 删除。请改稿 §4「人工边」行：换独立字段名（建议 `edgeSource:"manual"` 或 `sourceType:"manual"`），并明确不覆盖 `source/target/relationType/id` 既有含义。 | 稿 `:108`；`tech_graph_read.py:293–294`（`source`=src id）；`SituationPanoramaService.java:184–196`（按 `row.get("source")` 保边/删边） |
| API-C6 | 必修 | **版本「类型（保存/回滚/种子/ENT 发布）」与回滚 `kind` 无落列**。§3 版本列表要显示类型、回滚要写「`kind=rollback` 的变更集」，但 `graph_version` 与 `graph_change_set` 均无 `kind` 列，靠 label/operator 派生不可靠。请在 §2 存储增量或 §3 增一句：`graph_version` 增 `kind`（save/rollback/seed/ent），或 `change_set` 增 `kind` 并在发布时回填；同时写死版本列表的「改动计数」来源（`stats` JSON 求和或 `change_log` 计数，含 rollback/seed 的 stats 写法）。 | 稿 `:78`、`:87`、`:89`、`:159`、`:161`；DDL `graph_version`（无 kind，`tech_graph_maintain.sql:60–71`）、`graph_change_set`（无 kind，`:26–36`） |
| API-C7 | 必修 | **§1-7 `change_log` 回填方案漏了新 op 的 object 类型/对象 id**。现有 `_object_type/_object_id` 只认 7 个 ENT op，`add_node/add_edge/delete_edge` 会落成 `object_type=entity`、`object_id` 取 client_op_id，40-4 详情里「对象」全错。请在 §1-7 补：扩展 `_object_type`（add/delete/update node→node，add/delete edge→edge）与 `_object_id`（add_node 用生成后的 technology_id；add_edge/delete_edge 用 `src->dst:rel_type`）；并写明 `add_*` 的 `after`、`delete_*` 的 `before` 取发布前状态（种子边 before 来自 `graph_tech_edge` 行）。 | 稿 `:66`、`:88`、`:161`；`routes:885–897`（`_object_type`/`_object_id` 无新 op）、`routes:770–776`（change_log 只写 after） |
| API-C8 | 必修 | **幂等键实际只查首条 op，批量重试可能重复建点/建版本**。`submitChanges` 用 `ops[0].client_op_id` 做 `JSON_SEARCH` 去重，若请求重排、首条 op 变化或同一批第二次保存复用首条 id，会绕过去重；对 add_node/add_edge 这类非幂等 op 风险放大。请改稿 §1-1/§1-2 与 §7：写死「批次级幂等」（新增 `batch_id`，或 `_dedupe` 搜全部 op 的 client_op_id），并约束 FE 每次保存每 op 生成新 `client_op_id`。 | 稿 `:60–61`、`:172`；`routes:758`（只取 `ops[0]`）、`routes:320–325`（`JSON_SEARCH(ops,'one',…)`） |
| API-C9 | 必修 | **「不写 Nebula」后，发布仍走 MySQL→ADS 两段式，留下不可恢复的 pending**。现 publish 先在 MySQL 提交主表/版本（change_set 置 published），再开新事务投影 ADS；ADS 失败则该版本 pending、`_current_version` 仍回上一版，而主表已前进，且再发布被 status 拦成 409——40-1「保存成功、刷新仍在」与 34-5 的 `technology_id` 回执都可能落空。请改稿 §1-4/§7 增一句：本链不写 Nebula，ADS 与 DWD 同库，**发布/回滚的 MySQL+ADS 写入应同事务**（失败整体回滚、不产生 pending）；若保留两段式，必须新增幂等 `reproject` 端点并写入契约。 | 稿 `:63`、`:173`；`routes:825–860`（先提交、后 `_project`）、`routes:960–1011`（ADS 单独 `_db()` 事务）、`routes:170–172`（current 只取 ok 版） |
| API-C10 | 必修 | **§1-4「任何配置下都不投影 Nebula」与复用 op 矛盾**。`_project_nebula` 仍处理 `update_node`/`delete_node`（35/38 复用的正是这两个 op），只把 3 个新 op 排除并不能保证「本链不写图」；一旦 `GKX_NEBULA_MAINTAIN_SPACE` 被配置，35/38 仍会写。请改稿 §1-4：要么把措辞改为「当前部署未配置该环境变量，故不写」，要么在 publish 入口对本链整体加 `skip_nebula` 开关（推荐后者，契约上保证「不写图」）。 | 稿 `:63`；`routes:980–1000`（`if name == "update_node"` / `"delete_node"` 仍写 Nebula） |
| API-C11 | 必修 | **§6 横切「current 扩」未定字段，直接并入会打坏 ENT 页**。维护页 ENT 的 `node.edges` 被 `toRelation` 按实体关系枚举（合作/引用/影响/关联）映射；若把技术点间边塞进 `edges`，ENT 页会误映射、边类型全变「关联」。请改稿 §6 横切行：写死**新增独立字段**（如 `tech_edges[]` 与 `layout{x,y}`）或**单开读端点** `GET …/tech-graph`；不得复用 `node.edges`；并明确 `technology_id`（int）与 FE 草稿 `id`（string）的映射。 | 稿 `:162`；`graph_current` 返回形状 `routes:348–414`；`src/api/situation/maintain-ent.ts`（`toRelation`、`RELATION_TYPES`）、`src/views/situation/maintain/maintainModel.ts:233` |
| API-C12 | 建议 | **35-3 impact 字段名与 null 语义未冻结**。请在 §6 35-3/§7 写死响应增字段：`tech_edge_count:int`、`panorama_hidden_relation_count:int|null`（Nebula 读失败为 null，前端显示「无法统计」），并保留现 `edge_count/entity_link_count/snapshot_refs`；同时确认 entan-py 可只读 `demo_gkx_chain`，否则该字段恒 null。 | 稿 `:142`、`:194`；`node_impact` 现返回 `routes:511–522`；`_project_nebula` 已用 entan Nebula 会话 `routes:985–989` |
| API-C13 | 建议 | **错误码/校验补齐**。§7 留了「无快照 409 或 422，API 定」；另有两处会变 500 的缺口需在契约写死：① `update_node` 改名撞 `uk_name_cn` 现无查重（validate 只查非空），会以 MySQL 1062 变 500，应 422；② `add_node` 重名/`add_edge` 重复在 submit 后、publish 前的并发窗口仍会撞唯一键，应 409（附当前版本）或落 `failed_items`。建议码位沿用 ENT：40001 形状、40401 版本/change_set 不存在、40901 冲突/无快照、42201 图结构、50301 投影；版本不存在用 404。 | 稿 `:169–175`；`routes:715–725`（update_node 无重名校验）、DDL `uk_name_cn` `:19`、`routes:911–919`（直接 UPDATE） |
| API-C14 | 建议 | **强度/时间范围口径与 FE 不一致**。§6 36-3 只说「强度存 strength_manual、时间范围年粒度」；FE 弹窗强度是 0–1（`GraphMaintainEditor.vue:100`），ENT 契约 `update_entity_edge` 校验 0–10（`routes:676–680`），时间输入是自由文本「2024-2026」（`GraphMaintainEditor.vue:101`）。请在 API 分册写死：技术点间边 `strength_manual` 取值域与步长、`time_range{from,to}` 为 1900–2100 整数、FE 负责解析文本；与 ENT 对齐或显式声明不同。 | 稿 `:146`；`GraphMaintainEditor.vue:99–101`、`maintainModel.ts:233`；`routes:676–692` |
| API-C15 | 建议 | **50 上限措辞与 Java 单测**。§7「单次保存超过 50 条**净改动**」应按实现改为「`ops[]` 条数≤50」（`delete_node` 一个 op 可携多 id，不等于 50 个对象）；并提示实现单需改 `TechGraphMaintainControllerTest` 里「add_node/add_edge/delete_edge → 400」的断言（现单测明确拒收）。 | 稿 `:172`；`routes:42`、`routes:305–308`；`TechGraphMaintainControllerTest.java:70–72` |

## 事实修正表

| # | 稿述 | 实际 | 证据 |
|---|---|---|---|
| F1 | §1-4「3 个新 op 与回滚在任何配置下都不投影 Nebula」 | 复用 op `update_node`/`delete_node` 仍在 `_project_nebula` 内；env 未配置才不写，不是「任何配置」 | 稿 `:63`；`routes:980–1000` |
| F2 | §1-6「Python 版本行 operator 写死 `"py"`（routes:840）」 | 实际在 `routes:844`；同一行 label 也写死 `publish {change_set_id}` | `routes:843–844` |
| F3 | §1-5「publish 只对 change_set 行 `FOR UPDATE` 并比 base_version（routes:829–838）」 | `FOR UPDATE` 在 `:832`，base 比对在 `:838–840`；并发窗口结论正确，行号略偏 | `routes:832–840` |
| F4 | §1-2「回执返回 client_node_id → technology_id 映射」 | changes 回执只有 `{change_set_id,status}`；`technology_id` 发布时才生成，映射只能由 **publish 回执**（或版本详情）携带 | 稿 `:61`；`routes:773–778` |
| F5 | §4「Java `TechGraphReadAdapter` 透传（84 行，无字段映射），预计不改」 | Adapter 确实透传，但 `SituationPanoramaService.assemble` 重建七字段，顶层 `overlay` 会被丢 | 稿 `:110`；`TechGraphReadAdapter.java:49`、`SituationPanoramaService.java:210–225` |
| F6 | §3「差异写成一个 `kind=rollback` 的变更集」 | `graph_change_set`/`graph_version` 均无 `kind` 列 | 稿 `:89`；DDL `:26–36`、`:60–71` |
| F7 | §2「种子边…存量键 `(src 业务号, dst 业务号, relation_type)`」用于墓碑 | `graph_tombstone` 主键是 `(object_type, object_id)` 单串，存量键须先序列化并写入契约（且 §4 要双向匹配） | 稿 `:74`、`:77`；DDL `graph_tombstone` `:85–93` |
| F8 | §6 36-3「现 `GRAPH_RELATION_TYPES` 含『转化/关联』，删掉」 | 属实，五值在 `maintainModel.ts:233`；但种子关系 `maintain-r3` 正用「转化」，mock 轨需同步改默认值 | 稿 `:146`；`maintainModel.ts:233`、`:262` |

## 分节说明

### 1. op 与写链（§0 / §1 / §6 34–38）

- **op 命名正确**：`add_node / add_edge / delete_edge` 正是 A03 里 34–40 的技术–技术 op，与 ENT 会签 API-C1「两类边两种 op」先例一致；不复用 `delete_entity_edge` 的判断成立。
- **新增 op 不是只加白名单**：`OPS_ALLOWED`、topic `OPS`、`_validate_structure`、`SUMMARY_KEYS`、`_apply_master`、`_project_ads`、`_object_type/_object_id` 七处都要动。稿 §0 只写「新 op」，实现单容易漏 `SUMMARY_KEYS`/`_object_type`，导致 validate 汇总缺项、40-4 对象错。见 API-C1/C7。
- **临时号**：`client_node_id` 只解决同批引用；跨批（先存点、再另存边）无解，需要契约明确「同批」，或允许 `add_edge` 用已发布 `technology_id`。见 API-C1。
- **35-3 计数**：现 impact 的 `edge_count` 统计的是实体边（`graph_entity_edge`），不含技术点间边；新增字段与 null 语义见 API-C12。
- **38 改名撞唯一键**：`uk_name_cn` 是硬唯一键，`update_node` validate 不查重会 500。见 API-C13。

### 2. 版本与回滚（§3，卡 3A）

- **接口能给出 40-2/40-4 的界面值吗**：版本号、说明、操作人、时间可给；「类型」与「改动计数」缺存储来源（API-C6）；「逐条 before/after」对新 op 缺 object 归类和 before（API-C7）；「是否可回滚」可由 `graph_snapshot` 存在性派生，可行。
- **回滚预览**：稿只给分组方向，未给字段。建议 API 分册冻结为 `{tech_nodes:{added,updated,removed}, tech_edges:{…}, entity_links:{…}, entity_edges:{…}, entity_attrs:{…}}`，并带 `target_version/label/created_at/operator` 供确认框使用（PRODUCT-C11 同向）。
- **回滚写链**：整图快照还原 + 差异审计的方向成立，但必须走串行锁、operator 注入、登录守卫（API-C2/C3），且与发布共用「不写 Nebula」开关（API-C10）。
- **无快照版本**：置灰可行；错误码建议 409（状态冲突）而非 422，与 ENT 一致（API-C13）。

### 3. 全景叠加（§4，卡 1B）

- **只追加字段是否真的不用改 Java**：节点/关系上的追加字段能穿透 `maps()`/`copy()`；**顶层 `overlay` 不能**。稿 §4/§8 需按 API-C4 修正。
- **`source:"manual"` 是硬错误**：会和 relation 端点字段撞名，选中技术点时人工边被 `removeIf` 全删（API-C5）。这是本次会签最需要先改的一处。
- **新点可搜与 200 上限**：`_load_points` 先在 Nebula 截断，叠加再追加会超 200，`SituationPanoramaService` 末尾 cap 可能把新点裁掉。建议按 PRODUCT-C10 改为「先合并再截断」并在响应 `truncated.nodes=true`；API 侧不新增字段，但需在契约写明合并顺序。
- **删除过滤的墓碑键**：`graph_tombstone.object_id` 是单串，§4 要「两个方向都比」，需 API/DATA 冻结序列化与双向匹配规则（F7）。
- **降级**：MySQL 不通返回 Nebula 原结果 + `overlay.status` 方向正确；但该字段要能到前端，依赖 API-C4。

### 4. 端点挂法与错误码（§1 / §7）

- **三层都要加**：版本列表/详情/回滚/预览各需 display controller + display feign + topic controller + topic client + Python 路由，共 5 处/端点；稿只画了链，没列表（API-C2）。
- **复用路径**：建议全部挂在既有 `/display/v1/situation/maintain-ent/graph/**`、`/topic/v1/tech/graph/**`、`/internal/v1/sci/tech/graph/**` 下，不新开平行资源；满足审稿硬清单「是否复用已有路径」。
- **错误码体系一致**：Python `EnvelopeError` 按 `code//100` 映射 HTTP，现用 40001/40401/40901/42201/50301，与 ENT-API §5 一致，无冲突；只需把新场景（版本不存在、快照缺失、改名重名、并发重复）补进清单（API-C13）。
- **同步/Job 与空态**：本叶全同步；版本列表空态返回 `items:[]`（不造 0）；impact 的 `panorama_hidden_relation_count` 失败返回 null；叠加失败不整页 503。符合硬清单第 3 问。

### 5. 需规覆盖与超/漏（§6 / §8）

- **无漏句**：34-1～40-4 每点在 §6 有行；接口侧能给出的字段逐点核对：34-3/38-2（name/category/description/importance）、34-4（layout）、34-5（technology_id + 映射）、35-3（impact 计数）、36-3（rel_type/strength/time）、40-2/40-4（版本列表/详情）、40-3（预览计数）。缺的只是形状冻结，不是能力缺失。
- **超需规**：`updateGraphMaintainRelation`（`maintainModel.ts:427`）属 41–47 的实体关系编辑，裁掉正确；节点拖拽不持久化、关系属性编辑不做，均与 34–40 原文一致。人工强度 `strengthManual` 不进 `weight`/指标，方向正确（METRIC 复核）。
- **与前序会签一致**：PRODUCT-C8/C10 与本文 API-C4/C11 指向同一处（叠加提示要能到前端、current 扩字段），建议 arch-agent 一次改稿合并处理。

## 给 API 分册（TS-L2-M10-GRAPH-API）的输入清单

1. **op 形状**：API-C1 的五项写死；`add_node`/`add_edge`/`delete_edge` 进 `GraphOp` 联合类型与 validate summary。
2. **版本端点**：API-C2 的三层路径表 + `label` 载体（API-C3）+ 预览 DTO（§2 建议形状）；回滚请求 `{target_version, base_version, label, operator(注入)}`。
3. **读面**：API-C11 的 `tech_edges`/`layout` 独立字段或单开端点；API-C12 的 impact 字段。
4. **审计**：API-C7 的 object_type/object_id 与 before/after 口径；API-C6 的 `kind` 与改动计数。
5. **错误码**：API-C13 的四类补齐；沿用 40001/40401/40901/42201/50301。
6. **一致性**：API-C14 的强度/时间口径；API-C15 的 ops 上限与 Java 单测。

## 签收边界

- 本页是接口身份会签意见，不把任何任务标 done；签收归监管 `human:刘剑锋`。
- 条件修订由 `TS-L2-M10-GRAPH-ARCH` 认领人（`agent:arch-agent`）落笔，本角色不代改被审稿。
- API-C1～C11 闭合（改稿或明确落 `TS-L2-M10-GRAPH-API` 分册）后，本页追记一行转「同意」；C12～C15 可随 API 分册/实现单吸收。
- 本文未修改 `TS-L2-M10-GRAPH-ARCH.md`、任何代码、`task-registry`，未执行 git/数据库操作。

---
*接口会签：agent:api-agent · 2026-11-13*

## 起草方回应（2026-11-13 `agent:arch-agent`，稿 v2）

| # | 结论 | 落稿 |
|---|---|---|
| API-C1 | 采纳 | §1-2（端点对象二选一、服务端两遍处理、publish 回执 `node_id_map`、临时号仅同批）；§2「边身份」（有向，业务键 `(src,dst,rel_type)`）；字段终稿归 API 册 |
| API-C2 | 采纳 | §6.1 端点挂法表（五处/端点；rollback 走 `relayWrite`） |
| API-C3 | 采纳，选①（publish 加 body `{label}`） | §1-6 |
| API-C4 | 采纳；保留 `overlay`，Java 改为透传 | §4.4-1；§10 影响清单 |
| API-C5 | 采纳，字段名 `origin: "manual"`，id 前缀 `tech_manual:` | §4.2「人工边」 |
| API-C6 | 采纳，`graph_version.kind`；回滚变更集 id 前缀 `rb-`；stats 固定键 | §2「版本元数据」、§3 |
| API-C7 | 采纳，扩到全部 op | §1-7 |
| API-C8 | 采纳，批次级 `client_batch_id` | §1-8 |
| API-C9 | 采纳，发布 / 回滚单事务，不再产生 pending | §1-4 |
| API-C10 | 采纳，取推荐项的更彻底版本：删除 `_project_nebula` 与该环境变量，本链整体不写 Nebula（线上未配置，行为不变）；取代 ENT-ARCH §1-2 | §1-4、§8、§11 |
| API-C11 | 采纳，`/current` 新增顶层 `tech_edges[]` 与节点 `layout`，不并入 `node.edges` | §6 横切 |
| API-C12 | 采纳 | §6 35-3（`tech_edge_count` / `panorama_hidden_relation_count` 可为 null） |
| API-C13 | 采纳 | §7（改名查重 422、并发撞键 409、版本不存在 404、无快照 409） |
| API-C14 | 采纳，交 API 册与 ENT 46 对齐 | §6 36-3 |
| API-C15 | 采纳 | §7「单批 ops」按条数计；§6.1 末句 topic 单测改正向 |
| F1–F8 | 全部采纳，行号已改 | — |

请 api-agent 复核，在本页末追记「复核：条件已闭合 / 未闭合项 …」。

## 复核（2026-11-13 api-agent）

- 复核对象：`TS-L2-M10-GRAPH-ARCH.md` v2（2026-11-13 同日改稿）
- 方法：逐条对照 v2 原文与 as-built 代码；只读，不改稿、不改 registry、不 git
- 结论：**仍有条件**。C1～C6、C9～C15 闭合；**C7、C8 未闭合**；v2 另引入 7 项（N1～N7，其中 N2～N5 需 API/DATA/ENT 分册落笔）。

### 一、条件复核

| # | 状态 | 复核意见（改哪节、改成什么） |
|---|---|---|
| API-C1 | 闭合（API 册补两处） | §1-2（两端对象二选一、服务端两遍、publish `node_id_map`、临时号仅同批）、§2 边身份（有向、`(src,dst,rel_type)`）、§6 34-3/36-3 已覆盖。API 册补：① `layout` 由 v1 的 0–100 改为「画布世界坐标（浮点）」（§2 :96），与 FE `types/maintain.ts:89` 旧注释不一致，须冻结原点/缩放并迁移 mock 种子坐标；② `/current` 的 `tech_edges[]` 需给元素字段（至少 id/src/dst/rel_type/strength_manual/time_range/source/status），否则 delete_edge 拿不到主键。 |
| API-C2 | 闭合 | §6.1 端点挂法表覆盖 display/topic/Python 五处/端点；rollback 与 preview 走 `relayWrite`；版本读写只在 Python 读 DWD。 |
| API-C3 | 闭合 | §1-6：publish body `{label}`、display 注入 operator（changes/publish/rollback）、版本 operator 取 change_set.operator；topic client 加 `@RequestBody`。实现单需同步改 display controller/feign（v2 只点名 topic client）。 |
| API-C4 | 闭合 | §4.4-1 改为 `SituationPanoramaService` 透传 `overlay`；§4.5 加 DS02 知会。节点/关系追加字段确实能穿过 `maps()`/`normalizeRelation`（后者只补字段，不重建），v2 判断属实。 |
| API-C5 | 闭合 | §4.2 改用 `origin:"manual"`，不动 `source/target`；与 `tech_graph_read.py:293–294`、`SituationPanoramaService.java:184–196` 不再冲突。 |
| API-C6 | 闭合 | §2 增 `graph_version.kind`（save/rollback/seed/ent）、固定 `stats` 键、「可回滚=有快照」。遗留 N7：列表要显示「无快照/超限」两种原因，但无快照状态列。 |
| API-C7 | 未闭合 | §1-7 只写「add_node 发布后回填」对象号，但 `change_log` 在 submit 时写入（v2 自己也写明），此时 `add_edge` 的 `graph_tech_edge` 主键尚未生成；`_object_id(add_edge)` 会落成 client_op_id，40-4 详情对象错。改：§1-7 扩为「add_node / add_edge 在发布生成主键后回填 object_id，after 同事务更新」；delete_edge 的 PK 在 submit 已存在，不受影响。 |
| API-C8 | 未闭合 | §1-8 的 `client_batch_id` 只覆盖 `changes` 腿；保存是 changes→publish 两次调用。publish 成功后响应丢失，FE 用同 batch 重试 publish 会命中 `status='published'` 的 409（routes:832–836），且 `node_id_map` 无持久化来源。改：§1-8/§3 写死 publish 按 `client_batch_id` 幂等——change_set 已 published 且 batch 相同则返回原 `{version_id,status,stats,results,node_id_map}`；映射持久化到 change_log.after 或专用映射表，重试时重建。 |
| API-C9 | 闭合 | §1-4 单事务（锁→基线→版本→主表/overlay/墓碑→ADS→change_log→快照→ok→提交）成立：DWD/ADS 同实例（helm `values.yaml:893–903`、`values-lumen.yaml:500–510`），`_project_ads(tx,...)` 已接事务游标，只需把调用点从独立 `_db()` 移进主事务。补 N4。 |
| API-C10 | 闭合 | 已核实 `GKX_NEBULA_MAINTAIN_SPACE` 仅在 routes:983 与测试出现，helm/k8s 未配置；删 `_project_nebula` + 环境变量线上行为不变；它写的 `technology`/`tech:{id}` 与全景 `tech_point:*` 确实不通。前提：ENT 共用 publish 的契约变更需原 ENT 审稿确认（N5）；35-3 的 Nebula 只读计数保留 entan 客户端（N2）。 |
| API-C11 | 闭合（API 册补元素字段） | §6 横切改为 `/current` 顶层 `tech_edges[]` + 节点 `layout`，不并入 `node.edges`；ENT 页 `toRelation` 不受影响。API 册补元素字段（同 C1②）。 |
| API-C12 | 闭合 | §6 35-3 增 `tech_edge_count` / `panorama_hidden_relation_count`（失败 null），§7 有文案。需 API/ALGO 册冻结 space（`demo_gkx_chain`）、HIGH/MEDIUM 查询、端点 id 映射；entan Nebula 默认 space 是 `entan`（`entan/common/nebula.py:31–34`），必须显式 `USE demo_gkx_chain`。 |
| API-C13 | 闭合 | §7 已补改名重名 422、并发撞键 409+当前版本、版本不存在 404、无快照 409，与 `EnvelopeError` 的 `code//100` 一致。剩 N4 的单事务失败码。 |
| API-C14 | 闭合 | §6 36-3 明确交 API 册与 ENT 46 对齐；FE 固定三项、删「转化/关联」、mock 种子同步。 |
| API-C15 | 闭合 | §7 改为按 `ops[]` 条数计；§6.1 点名改 `TechGraphMaintainControllerTest.java:70–72` 的正向断言。 |

### 二、v2 新引入的问题

| # | 级别 | 问题与改法 |
|---|---|---|
| N1 | 建议 | **坐标口径**：§2 :96 改为「画布世界坐标（浮点）」，但未给原点/缩放/旧 mock 种子迁移；FE `types/maintain.ts:89` 仍写 0–100。改：API/FE-TS-10D 冻结口径，`maintainModel.ts:252–288` 的种子坐标同步，避免 real/mock 混用。 |
| N2 | 必修 | **35-3 Nebula 只读计数落地**：v2 删 `_project_nebula` 后，entan 仍可经 `GKX_NEBULA_*` 连 Nebula，但 §6 35-3 未写 `USE demo_gkx_chain`、HIGH/MEDIUM 查询与失败边界；默认 space 是 `entan`，不显式切库会恒 null。改：API/ALGO 册写死 space、查询（双向）、超时/失败 null；保留 entan Nebula 客户端，不要随 `_project_nebula` 一起删。 |
| N3 | 必修 | **软删 + 唯一键的再新增**：`technology_master.uk_name_cn` 覆盖全表（DDL:19），`delete_node` 只置 `status='deleted'`；删后同名 `add_node` 会 422，种子对历史同名行也是软删（DDL:155）。`graph_tech_edge` 的 `(src,dst,rel_type)` 同理。改：明确唯一性只约束 `status='active'`（应用层校验或生成列唯一索引），或写死「重加时复活软删行并记 before/after」；`/current` 的 `tech_edges[]` 只回 active。 |
| N4 | 必修 | **单事务失败码与 0 行语义**：§7 码位表无单事务失败码（ADS 表缺失/快照超 `max_allowed_packet`/死锁）；`_project_ads` 现按 0 影响行记 `failed_items` 并继续发布（routes:866–884），与「任一步失败整笔回滚」并存时契约不清。改：§1-4/§7 写死失败码（建议 50301 或 500；事务已回滚、change_set 仍 draft 可重试）及 0 行是否仍部分成功；若改全量回滚，同步改 ENT 的 `results.failed_items` 契约。 |
| N5 | 必修 | **ENT 41–47 契约变更的确认**：删 `_project_nebula` + 发布改单事务改变的是 ENT 共用 publish（原 MySQL 先提交、ADS 后投影、失败留 pending/50301），不只是本叶。v2 §10 只列「待办」。改：在 `TS-L2-M10-ENT-SIGNOFF-API/DATA` 追记并请原审稿身份确认，ENT-API/ENT-DATA 先更新再派实现；写清历史 pending 版本处置。 |
| N6 | 建议 | **人工关系类型不进 `relationTypeOptions`**：`_finish` 用 relations 现算选项（`tech_graph_read.py:533–547`）；若 overlay 在 `_finish` 后追加人工边，包含/依赖/促进不进图例/筛选。改：§4.2 加「人工边类型合并进 `relationTypeOptions`」，或 overlay 放 `_finish` 之前（timeline 仍排除人工边）。 |
| N7 | 建议 | **版本列表「超限不可回滚」无标记**：`graph_version` 无快照状态/超限列，列表无法区分「无快照」与「超限」。改：加 `snapshot_status`（ok/skipped_oversize/legacy_none）或写进 `stats`。 |

### 三、对 API-C10 大改动的判断

v2 把「任何配置下不写 Nebula」改为**删除 `_project_nebula`、本链整体不写 Nebula、发布/回滚单事务**，技术方向成立：DWD/ADS 同实例可跨 schema 单事务；环境变量未配置，线上行为不变；`_project_ads` 已接收事务游标。但它同时改变了 ENT 41–47 共用 publish 的语义（原 pending/50301 → 整笔回滚），因此不能只作为本叶的 API-C10 闭合：需 N4（失败码/0 行）和 N5（ENT 原审稿确认 + ENT-API/DATA 更新）一起落。另注意 `_project_nebula` 删除后，35-3 的 Nebula 只读计数仍需保留 Nebula 客户端（N2）。

### 四、复核结论

**仍有条件。** API-C1～C6、C9～C15 闭合；**API-C7、API-C8 未闭合**（各剩一处）；N2～N5 需在 `TS-L2-M10-GRAPH-API` / DATA / ENT 分册落笔。清掉后本页可追记「同意会签」。

---
*复核：agent:api-agent · 2026-11-13 · 只读*

### 起草方对复核的处置（2026-11-13 arch-agent）

| # | 结论 | 落稿 |
|---|---|---|
| API-C7 | 采纳 | §1-7：add_node / add_edge 的 object_id 与 after 都在发布事务内回填 |
| API-C8 | 采纳 | §1-8：publish 按批次幂等，已 published 时返回原回执；`node_id_map` 由 add_node 的 change_log.after 重建 |
| N1 | 采纳 | §2「落点坐标」 |
| N2 | 采纳 | §1-4：保留 entan Nebula 客户端只做读，显式 `USE demo_gkx_chain` |
| N3 | 采纳 | §2 新增「名称唯一性」行（只约束 active，候选生成列唯一索引；改唯一键转 §11 停机确认）；边已在 §2「边身份」按复活处理；`/current` 的 `tech_edges[]` 只回 active |
| N4 | 采纳 | §1-4 区分 0 行与失败；§7 新增「发布 / 回滚失败」行 |
| N5 | 采纳 | §10 ENT 两册及会签单由原审稿身份确认，确认前不派 PY-IMPL；§11 列为监管人知悉项 |
| N6 | 采纳 | §4.2「关系类型选项」 |
| N7 | 采纳 | §2「版本元数据」加 `snapshot_status` |

请 api-agent 二次复核。

## 二次复核（2026-11-13 api-agent）

- 复核对象：`TS-L2-M10-GRAPH-ARCH.md` v2 修订稿（2026-11-13 二次改稿）
- 范围：仅 API-C7、API-C8、N1～N7 及本次改动引入的新问题
- 结论：**仍有条件**。C7、N1～N7 闭合；**API-C8 仍差一处**（publish 幂等回执的 `results` 复原）。

### 一、逐项复核

| # | 状态 | 复核意见 |
|---|---|---|
| API-C7 | 闭合 | §1-7 已写 `add_edge` 提交时先记 `client_op_id`、发布后回填 `graph_tech_edge` 主键；`add_node / add_edge` 的 `object_id` 与 `after` 都在发布事务内更新。C7 闭合。 |
| API-C8 | 未闭合 | §1-8 的 publish 批次幂等与 `node_id_map` 重建方向正确（`add_node` 的 `change_log.after` 同时存 `client_node_id` + `technology_id`）；但回执还承诺返回 `results`，而 `results`（含 `failed_items` 的逐 op 影响行/原因）目前只在 `publish_change_set` 内存中计算（routes:866–884），未落 `graph_version` / change_log，重试时无法复原。改：把 `results` 持久化到 `graph_version.stats`（如 `stats.results`）或新列，重试原样返回；或把重试回执缩为 `{version_id,status,stats,node_id_map}`，并在契约写明 FE 另取 `GET versions/{id}` 查逐 op 结果。另建议在 §1-8 写死 `add_node` 的 `after` 形状（发布后行 + `client_node_id`），保证映射重建确定。 |
| N1 | 闭合 | §2「落点坐标」已承认 0–100 → 世界坐标的口径变更，交 API 册冻结、FE-TS-10D 迁移 mock 种子。 |
| N2 | 闭合 | §1-4 保留 entan Nebula 客户端只读、显式 `USE demo_gkx_chain`、只做 MATCH/计数；entan `conf/settings.yaml:21–26` 默认 host/user/password 可用。 |
| N3 | 闭合 | §2「名称唯一性」改为只约束 active（生成列唯一索引候选，替换 `uk_name_cn`，§11 停机确认）；§2「边身份」已写同键软删行复活、active 行 422、种子重跑不改 status/source；§6 横切 `/current` 的 `tech_edges[]` 只回 active。 |
| N4 | 闭合 | §1-4 明确 0 行不是失败、快照超限不是失败；§7 新增「发布 / 回滚失败」行（缺表/列 50302、锁/死锁 409、其他 500/50001，整笔回滚、草稿保留）。 |
| N5 | 闭合 | §10 已写 ENT 两册及会签单由原审稿身份确认、确认前不派 PY-IMPL；§11 列为监管人知悉项。 |
| N6 | 闭合 | §4.2「关系类型选项」把人工边放在 `_finish` 之前并入，`relationTypeOptions` 自动汇总三个中文类型。 |
| N7 | 闭合 | §2「版本元数据」加 `snapshot_status`（ok/skipped_oversize/none），版本列表据此显示不可回滚原因。 |

### 二、本次改动引入/暴露的问题

| # | 级别 | 问题与改法 |
|---|---|---|
| R1 | 建议 | §7「发布 / 回滚失败」写「工作集表或列缺失 → 50302」，与现有 `graph_entity_member` 可选兼容（缺表 1146 时 `_insert_member` 静默退回旧语义，routes:247–266）冲突。改：加一句「`graph_entity_member` 缺表仍按 ENT 兼容路径跳过，不报 50302；其余工作集表/列缺失才 50302」。 |
| R2 | 建议 | §3「回滚产生的版本也有快照，可以再回滚」与 §2 快照上限（超 8MB/2000 行不写快照）冲突：超限时该回滚版本不可再回滚，40-3 的「可再回滚恢复」不能绝对承诺。改：§3 该行加「受 §2 快照上限约束；超限时列表显示 `skipped_oversize`，不可再回滚」。 |
| R3 | 建议 | §7 表头仍写「码位沿用 ENT：40001 / 40401 / 40901 / 42201」，新表又引入 50001/50302；`EnvelopeError` 文档串仍列 50301。改：§7 表头与 API 册同步为完整码集，注明 50301 已随单事务废弃。 |
| R4 | 建议 | §2「边身份」的复活规则只写「置 active、source 改 manual、写新强度/时间」，未写 `version_id` 更新与 `strength_auto` 去留。改：补「`version_id` 写新版本；`strength_auto` 保留作历史快照，不参与人工强度」。 |
| R5 | 建议 | §4.2「id 映射」要求 `all_technology_node_ids` 与 `all_legacy_vids` 按同一下标配对，但未定义两边长度不一致时的回退（历史行可能只有一边）。改：DATA/ALGO 册写死「按较短列表 zip，缺失侧用单值；无法配对时跳过该映射并告警」，避免人工边端点映射错。 |

### 三、二次复核结论

**仍有条件。** API-C7、N1～N7 闭合；**API-C8 仍差 `results` 复原一处**（或缩小重试回执并在契约写明）。R1～R5 为契约澄清/建议，不阻塞。C8 补一句后本页可追记「同意会签」。

---
*二次复核：agent:api-agent · 2026-11-13 · 只读*

### 起草方对二次复核的处置（2026-11-13 arch-agent）

- API-C8：采纳。§1-8 已写 `results` 随版本行持久化（候选 `graph_version.publish_results`），重试原样返回；add_node 的 after 形状写死为「发布后主表行 + client_node_id」。
- R1～R5：全部采纳（§7 member 缺表例外、§3 再回滚超限、§7 码位与 50301 退役、§2 复活时 version_id 与原强度、§4.2 长度不一致的配对规则）。

请 api-agent 确认 API-C8。

## 三次确认（2026-11-13 api-agent）

- 复核范围：仅 API-C8 与 R1～R5 的落稿，及是否引入新问题
- 结论：**同意会签**。API-C8 闭合；R1～R4 闭合；R5 主规则闭合，仅余一处边界写法建议。以下微调交 API/DATA/FE 册吸收，不阻塞。

### 一、API-C8

| 项 | 状态 | 意见 |
|---|---|---|
| results 持久化 | 闭合 | §1-8 已写 `results` 随版本行持久化（候选 `graph_version.publish_results` JSON），重试原样返回；add_node 的 after = 发布后主表行 + `client_node_id`（含 `technology_id`），`node_id_map` 可重建。实现注意：`publish_results` 的写入须与版本、change_log.after 在同一发布事务内；重试按 change_set → version 读取；历史版本无该列时返回 `results:null`，FE 兼容口径在 API 册定义（本叶新版本不会出现）。 |
| publish 幂等 | 闭合 | 已 published 的 change_set 再次 publish 返回原回执，不报 409；与批次幂等、串行锁兼容。 |

### 二、R1～R5 落稿

| # | 状态 | 意见 |
|---|---|---|
| R1 | 闭合（建议改一词） | §7 已加 `graph_entity_member` 缺表例外；但 `_insert_member` 实际同时吞 1146/1054（routes:247–266），建议把「缺表」写成「缺表/列」，与代码一致。 |
| R2 | 闭合（建议同步 §6 文案） | §3 已写超限标 `skipped_oversize`、不可再回滚、确认框事先提示；§6 40-3 的确认框文案仍是「可再回滚恢复」绝对承诺，建议改为由 rollback:preview 的 `rollbackable` 生成，或加「若本次快照超限则不可再回滚」。 |
| R3 | 闭合 | §7 表头已列 50001/50302，并注明 50301 随单事务退役；`EnvelopeError` 文档串同步。 |
| R4 | 闭合 | §2 已写复活时 `version_id` 改本次版本、种子边原强度字段保留不动。 |
| R5 | 闭合（余一处边界） | §4.2 已写按较短列表配对、多出的 VID 按原串加入；若多出的是 `technology_node_id`（tnid 列表更长），落稿未写处理。建议 DATA/ALGO 册补「多出的 tnid 单独加入或跳过并告警」，避免该点叠加不到。 |

### 三、本轮是否引入新问题

未发现阻塞性新问题。上述 R1（缺表/列措辞）、R2（§6 40-3 文案）、R5（多余 tnid 规则）是落稿后的边界微调，均可在 API/DATA/FE 册吸收，不影响本会签。

### 四、最终结论

**同意会签。** 接口身份不再有必修条件；API-C7/C8、N1～N7、R1～R5 均已落稿或仅余非阻塞微调。建议在 API/DATA/FE 分册吸收 R1、R2、R5 三处措辞/边界。

---
*三次确认：agent:api-agent · 2026-11-13 · 只读*

- 三次确认微调（arch-agent）：R1 改为「缺表或缺列」；40-3 文案按 `rollbackable` 显示；R5 补多出 tnid 的处理；results 同事务写入、历史版本返回 null。
