# TS-L2-M10-GRAPH-SIGNOFF-DATA · 维护管理 · 维护技术图谱 · 数据会签

- 角色：`agent:data-agent`（数据角色会签人，独立会话）
- 日期：2026-11-13
- 对象：`TS-L2-M10-GRAPH-ARCH.md`（草稿 v1，2026-11-13 落盘，归 `agent:arch-agent`）
- 监管：`human:刘剑锋`
- 范围：**只读核对**。不改被审稿、不改任何其他文件、不改 task-registry、不 git、不连库、不建表、不跑脚本
- 依据：`产品实现规程.md` §4.2.4（:307–338「审稿身份必须站在本身份立场找问题，不得只写同意」）；审稿硬清单 `gkx-fde-design-change/审稿硬清单.md`（data-agent 4 问）；`00-team-constitution.mdc` 铁律 7/10/12/16；`architecture-baseline.md` §2 D9/D12/D16/D18、§3.1 数据面；`data/data-design/storage/README.md` §5 职责矩阵/§6 变更纪律；`data-lineage-policy.md` §2 8 件套；简报 `2026-11-13-维护技术图谱-需规分句闭合.md`（卡 1B/2A/3A 已拍板，不重开）；先例 `TS-L2-M10-ENT-ARCH.md` / `TS-L2-M10-ENT-DATA.md` / `会签/TS-L2-M10-ENT-SIGNOFF-DATA.md`
- as-built 核对（2026-11-13 读码，未连库）：
  - `repos/lumen-algo-py/vendor/entan-py/api/tech_graph_maintain_routes.py`（下称 **routes**）
  - `repos/lumen-algo-py/vendor/entan-py/scripts/mysql/tech_graph_maintain.sql`（下称 **DDL**）及 `_v2_member.sql`
  - `repos/lumen-algo-py/vendor/entan-py/scripts/seed_tech_graph_maintain.py`（下称 **seed**）
  - `repos/lumen-algo-py/lumen_common/algorithms/tech_graph_read.py`（下称 **read**）、`lumen_common/db.py`（下称 **db**）、部署库名 `k8s/api.yaml`
  - `repos/lumen-svc-platform/helm/gkxlumen-platform/values.yaml` / `values-lumen.yaml`（entanPy.env）、`gkxlumen-topic/.../TechGraphMaintainController.java`、`gkxlumen-display/.../SituationMaintainEntController.java`、`.../TechGraphReadAdapter.java`

## 结论

**有条件同意。** 架构方向数据视角成立：不翻 ENT 单写者与「不写 Nebula」、技术点间边单独建表、快照 N=1、全景只读叠加、整图回滚——均与存储真源（ADS=契约面、Python 写、Java 只读）和 ENT 先例一致，**无架构性反对**。但稿把大量「数据落点」留给 DATA 分册，而其中若干是**架构级语义**（人工边两端存哪个 ID 命名空间、种子边存量键怎么和 Nebula `tech_rel` 唯一对上、回滚版本的投影状态与 ADS `version_id` 怎么落），DATA 分册无法自造；另有 4 处 as-built 已被误读（种子脚本没有 tech_rel 逻辑、`delete_node` 行号错位等）。**DATA-C1～C7 未闭合前不宜签收**；DATA-S1～S5 可随 DATA/API 分册或实现单吸收。

## 0. 结论与条件

> 级别：必修＝不闭合不签收；建议＝可在 DATA/API/实现单吸收。证据为 `文件:行号`；`doc` 指被审稿 `TS-L2-M10-GRAPH-ARCH.md`。

| # | 级别 | 条件 | 证据 |
|---|---|---|---|
| DATA-C1 | 必修 | **人工边的 ID 命名空间与边身份未定，跨「新建点—存量点」的边无法落。** §2 只写「人工边：服务端主键」；§4 新建点 `id=tm:{technology_id}`、存量点 `id=technology_node_id`，两套命名空间。若 `graph_tech_edge.src/dst` 存内部 `technology_id`，叠加时要映射；若存全景 id，`delete_node` 级联、快照还原、跨服务读又要反向映射。**改稿 §2「边身份」行**：明确 `src/dst` 存 `technology_master.technology_id`（内部主键），叠加时按端点映射「新建点→`tm:{technology_id}`、存量点→`external_ids.technology_node_id`（空则 `legacy_vid`/`all_technology_node_ids`）」；**§4「人工边」规则**补一句端点 id 映射。 | doc:74、doc:107–108；`read:181`/`read:291–299`；`routes:1078–1112`（unhang 以 `src=technology_id`、`dst=实体 VID` 为前提） |
| DATA-C2 | 必修 | **种子边存量键与 Nebula `tech_rel` 唯一对上的规则不完整，且 as-built 种子脚本根本没有 tech_rel 逻辑。**（a）`read` 的节点 id＝`technology_node_id or vid`（`read:181`），边端点取该 id（`read:291–299`）；稿 §2 的键只写「业务号」，未写空值回退，`technology_node_id` 为空的点对不上。（b）seed 只读 `tech_has_*` 实体边（`seed:51–56`/`:91–101`），从不读 `tech_rel`；稿 §2 种子行称写「其间 `tech_rel`」并以 `seed:163–170` 为据，但 `:163–170` 只是 `_external_ids`。（c）重名合并后 `all_legacy_vids`/`all_technology_node_ids` 有多个 VID（`seed:168–170`），§4 只用单个 `external_ids.technology_node_id` 对齐（doc:103），合并点其余 VID 覆盖/过滤不到。（d）`read` 是无向 MATCH（`read:272`）并按 `(source,target,relationType)` 去重（`read:320–327`），墓碑键须规范化为排序端点对，`graph_tombstone.object_id VARCHAR(128)`（`DDL:74–81`）的序列化长度须定。**改稿 §2「种子」行 + §4「对上存量点/删除的存量边」**：写清键分量、空值回退、`all_*` 多值遍历、方向规范化。 | doc:80、doc:103、doc:106；`read:181`/`:272`/`:291–299`/`:320–327`；`seed:51–56`/`:91–101`/`:163–171`；`DDL:74–81` |
| DATA-C3 | 必修 | **回滚版本的投影状态与快照一致性缺口。** rollback 不跑 `_project`；`_current_version` 只认 `projection_status='ok'`（`routes:170–172`），而 `graph_version.projection_status` 默认 `'pending'`（`DDL:61`）。若不显式置 `ok`，`base_version` 不前进，之后每次保存/回滚都永久 409。按快照还原的 ADS 行会带**旧** `version_id`（node/edge/member/overlay 都有该列），R2 与血缘读到旧版本号。`graph_snapshot.payload` 是单 JSON `NOT NULL`（`DDL:110–115`），稿只写「超过阈值不写」，未给数值阈值和「不可回滚」落点；若误跑 `seed --all`（19,430 点/587k 边）快照会撑爆 `max_allowed_packet`。另：快照含 `graph_entity_edge`（auto 边）＝整图回滚会把上游 auto 层一起回滚，与 manual>auto 合并规则有口径冲突，须写明「auto 边随快照回滚、下一轮 auto 产出覆盖」。**改稿 §3 回滚行 + §2 快照行**：还原后置 `projection_status='ok'`；ADS 行 `version_id` 改写为回滚新版本；快照在还原后写、失败只降级「可回滚性」不回滚版本；给阈值（如 payload > 16MB 或行数 > N 即跳过）并禁止 `--all`；payload 带 `schema_version`。 | doc:78、doc:89、doc:95；`routes:170–172`/`:832–859`/`:1014–1164`；`DDL:61`/`:110–115` |
| DATA-C4 | 必修 | **发布串行锁作用域不足，两个事务之间存在投影竞态。** publish 分两段：第一段 `FOR UPDATE`＋`base_version`＋插版本＋`_apply_master`（`routes:831–850`）提交后才跑 `_project`（`routes:854–859`）。稿 §1-5 把锁加在「MySQL 事务开头」，锁随第一段提交释放，两个不同 change_set 的 `_project_ads` 可并发，且后跑的旧版本会覆盖新版本（两段都用 `ON DUPLICATE`＋`version_id`，`routes:1138–1153`）。「锁最新版本行」在 v1 之前无行可锁、RR 间隙锁也不可靠。**改稿 §1-5**：明确 `GET_LOCK('m10_graph_publish', timeout)` 覆盖整个 publish/rollback（含 `_project`），同一连接取得、`finally` 释放；rollback 用同名；二选一写死为 GET_LOCK。 | doc:64；`routes:831–859`/`:1014–1164` |
| DATA-C5 | 必修 | **两个服务读写同一工作集的库名只靠约定，默认值不同；且跨服务只读无超时、无权限隔离。** 写侧 entan-py 解析 `GKX_M10_ENT_*` → `ENTAN_MYSQL_*_DB` → 默认 `demo_*`（`routes:115–120`）；读侧 lumen-algo-py 解析 `LUMEN_ALGO_MYSQL_*_DB` → settings 默认 `gkxlumenx_dwd`/`gkxlumenx_ads`（`db:36–37`）。当前 `values-lumen.yaml:508–512` 与 `k8s/api.yaml:38–39` 都指 `demo_*`，但**默认值不同、且无启动校验**；任一部署缺 env 就会读写两个库，全景叠加静默空/旧。`db` 的 `pymysql.connect` 无 `connect_timeout`/`read_timeout`（`db:39–46`），MySQL 卡住会把全景读图挂死——§4 的「失败降级」接不住 hang。`lumen_common.db.DB` 是通用可写类、账号 `gkxlumenx` 有 GRANT ALL，「algo-py 只读」只是约定（同 ENT 会签 N4）。**改稿 §4「落点/叠加失败」**：两服务启动打印并断言解析后的 dwd/ads 库名一致；叠加连接设 connect/read timeout 并按失败降级；只读只用 `query()`；DATA 分册记 `demo_*` 相对 D12 数据面基线（`gkxlumenx_*`）的临时偏差。 | doc:99、doc:111；`db:36–46`；`routes:115–120`；`values-lumen.yaml:508–512`；`k8s/api.yaml:38–39`；架构基线 §3.1 N4 |
| DATA-C6 | 必修 | **`before` 回填与 `change_log` 覆盖不足，tech 边的对象类型未定。** §1-7 只点 `update_node`/`delete_node`/`delete_edge`；`OPS_ALLOWED` 还有 `hang_entities`/`unhang_entities`/`update_entity_*`/`add_*`（`routes:33–41`）。`_object_type` 把未知 op 归 `entity`（`routes:885–891`），`add_node`/`add_edge` 会落错对象类型。`change_log` 在 submit 时就写入（`routes:771–776`），草稿丢弃后 `version_id` 仍为 NULL；版本详情必须按 `version_id` 过滤，不能按 `change_set_id`。**改稿 §1-7** 改为「对全部 op 按对象回填 before/after」，并列 tech_edge 的 `object_type`（新值）与 `object_id` 序列化；**§3 版本详情**注明按 `version_id` 过滤。 | doc:66、doc:88；`routes:33–41`/`:771–776`/`:885–891`；`DDL:41` |
| DATA-C7 | 必修 | **版本面「类型/计数/可回滚/`kind=rollback`」无表列落点，DATA 分册无法自造。** `graph_version` 现列只有 `version_id/parent/label/operator/stats/projection_status/created_at`（`DDL:55–64`）；`graph_change_set` 无 `kind` 列（`DDL:24–34`）。稿 §3 版本列表要「类型（保存/回滚/种子/ENT 发布）、改动计数、是否可回滚」，回滚要「`kind=rollback` 的变更集」。**改稿 §3** 写死落法：类型＝新增 `graph_version.kind` 列或由 `label`/关联 change_set 推导（二选一）；改动计数＝`stats` JSON；可回滚＝`graph_snapshot` 存在性；回滚变更集 kind＝`graph_change_set` 新增 `kind` 列或 id 前缀（二选一）。 | doc:87、doc:89；`DDL:24–34`/`:55–64` |
| DATA-S1 | 建议 | **坐标列落点。** `technology_master`＋`graph_entity_node` 加 `x/y`（可空）；需写清 DDL 归属、NULL 语义、快照包含、seed 留空、`graph_current` 出参。加列不是「新建表/改主键」，但共享 `demo_gkxlumenx_dwd` 的 DDL 仍须监管人执行前备份；DATA 分册注明「展示态列，非业务真源」。 | doc:76、doc:138；`DDL:7–21`/`:125–133` |
| DATA-S2 | 建议 | **35-3 存量隐藏关系计数口径。** `impact` 扩读 Nebula `tech_rel` 时，必须与全景默认读一致（默认 `evidence_level IN [HIGH,MEDIUM]`，`read:270`），否则确认框数字与实际隐藏边数不符；Nebula 失败返回 null 已有，注明不挡删除。 | doc:142；`routes:511–522`；`read:270` |
| DATA-S3 | 建议 | **子图种子与现有 1 点/61 边、`uk_name_cn` 重名。** 新 seed 按 `uk_name_cn` upsert，现有 1 点及其实体边若不在切片内应保持不软删；`uk_name_cn` 为 `utf8mb4_general_ci`（大小写不敏感），查重须在 validate 阶段预查并 422，不能让 MySQL 1062 冒成 500；工作集外存量同名点仍可重复新建（同 ENT DATA-A1 悬空），首版接受或扩查重须写明。 | doc:80；`DDL:19`；`seed:145–160`/`:234–241` |
| DATA-S4 | 建议 | **版本/回滚计数与 D9。** 版本列表「改动计数」、回滚预览「撤回计数」是 UI 数字，按 D9 铁律需 `metric_id` 或豁免；ENT 先例是一次性豁免，GRAPH 需 METRIC/ALGO 明确（doc §9-7 全 N/A 未覆盖计数类）。 | doc:87/90/92；`data-lineage-policy.md` §2.3.1；ENT 会签 §6 |
| DATA-S5 | 建议 | **分表后所有路径须双表覆盖。** 同意 `graph_tech_edge` 与 `graph_entity_edge` 分表；但 `impact`（`routes:520–521`）、`current`（`routes:383` 只出 manual 实体边）、`delete_node` 级联（`routes:1038` 只删实体边）、快照/回滚、`_project_ads` 都要同时处理 `graph_tech_edge`，否则会出现「删节点只清实体边、tech 边残留」。补一句「所有读/删/快照路径同时处理两表」。 | doc:72/77；`routes:383`/`:520–521`/`:1034–1041` |

## 1. 事实修正（随稿纠错，非阻断但应改）

| # | 稿件位置 | 稿写 | 实际（`文件:行号`） |
|---|---|---|---|
| F1 | §0 序 35 行 | `delete_node`「软删+墓碑+级联删边，routes:933–942 / :1043–1051」 | 软删+墓碑在 `routes:946–955`，ADS 删点删边在 `routes:1034–1041`；`:933–942` 是 overlay/hang 段，`:1043–1051` 是 `hang_entities` |
| F2 | §1-6 | 版本行 operator 写死 `"py"`（routes:840） | 实际 `routes:844`；840 是 `base_version` 409 分支 |
| F3 | §1-5 | publish `FOR UPDATE` 并比 `base_version`（routes:829–838） | `FOR UPDATE` 在 `routes:832`；base 比较在 `routes:838–840` |
| F4 | §4 删除的存量边 | 「无向 MATCH，read:276」 | 无向 MATCH 在 `read:272`；`:276` 是 RETURN 列 |
| F5 | §1-7 | `change_log` 只写 after（routes:770–775） | INSERT 在 `routes:773–776`；`:771` 是 `for op` 循环头 |
| F6 | §2 种子行 | 「routes 已有字段」`external_ids` | routes 不读写 `external_ids`；字段在 `DDL:14`、`seed:163–171`。措辞应为「DDL/seed 已有字段」 |
| F7 | §2 种子行 | seed 脚本写「其间 `tech_rel` 边」，以 `seed:163–170` 为据 | as-built seed 只读 `tech_has_*`（`seed:51–56`/`:91–101`），无 `tech_rel`；`:163–170` 仅 `_external_ids`（同 DATA-C2） |
| F8 | §3 实现说明 | 「快照强度回写」「反向 op」（routes:1066–1112 / :1078–1112） | unhang 在 `routes:1067–1107`，`delete_entity_edge` 在 `routes:1108–1133`；引区间不精确 |
| F9 | §2 快照行 | 「ENT 现 1 点 61 边」 | 简报与 `TS-L2-M10-ENT-DATA.md` 只写「1 个技术点」，未见 61 边出处（未连库，不核）。建议核实后保留或删数字 |
| F10 | 全文 | — | **属实项**：`routes:42` OPS_LIMIT、`:560` 起 validate、`:911–919` update_node、`:980–1000` `_project_nebula`、`DDL:19` `uk_name_cn`、`seed:163–170` `_external_ids`、`read:181` 节点 id、`read:556–570` `_read`、`k8s/api.yaml:38–39`、`TechGraphReadAdapter` 84 行、`SituationMaintainEntController:114–126` 登录守卫——逐条核对无误 |

## 2. 分节说明

### 2.1 新表 `graph_tech_edge` 放 ADS 的合规性与分表取舍（数据身份重点 ①）

- **合规**：`storage/README.md` §5 定 ADS＝契约面、Python 写、Java 只读；ENT as-built 的人工实体边也只落 `ads.graph_entity_edge`。新表沿用同一先例不翻案。但稿把它称「边的真源」需收口：**审计真源在 DWD 的 `graph_change_set`/`graph_change_log`，ADS 新表是当前状态物化**——DATA 分册须这样写，D9 血缘才追得到。
- **分表同意**：`graph_entity_edge` 的 `src` 是纯数字 `technology_id`、`dst` 是实体 VID（`seed:314`、`routes:1056–1059`），unhang/delete 逻辑按此方向写（`routes:1078–1133`）；技术点间边两端都是技术点标识，混表会污染 `(src,dst,rel_type,rank)` 唯一键语义、并给 41–47 每条 SQL 加类型过滤。分表是对的。
- **但**：新表未在任何代码/DDL 出现（全仓 grep 仅见于本稿与任务书），DATA 分册须从零定义列；且必须按 `storage/README.md` §6「改表须改对应 `stores/*` + 记 CHANGELOG」登记到 `storage/ENT/stores/mysql/ads.md`（现该文件只列 `graph_node`/`graph_edge`，ENT 的 `graph_entity_*` 也未登记，属既有债，建议一并补）。
- **必补列语义**（归 DATA，但须 ARCH 先定 C1）：`src`/`dst` 命名空间、`rel_type`（manual 三枚举 + auto 保留英文码，二者共存）、`source`、`strength_manual`、`time_from/to`、`version_id`、PK/唯一键（建议 `(src,dst,rel_type,rank)` 或 `(src,dst,rel_type)`，与 ENT 一致，以便 36-4「同端点同类型重复 422」有物理兜底）。

### 2.2 种子边存量键与全景叠加（数据身份重点 ②）

- 全景读图给出的 relation 身份是 `(source, target, relationType)`：`source/target` 取节点 `id`（`technology_node_id or vid`，`read:181`/`:291–299`），`relationType` 取 `e.relation_type` 原值（`read:280`）。所以稿 §2 的「`(src 业务号, dst 业务号, relation_type)`」方向正确，**但必须用与 `read` 完全相同的 id 回退规则**，否则 `technology_node_id` 为空的点（seed 里 `str(p.get("tnid") or "")` 会写空串）永远匹配不上。
- **重名合并**是最大漏洞：`_group_points` 按 `name_zh` 归并、`_external_ids` 只在 `len(vids)>1` 时写 `all_legacy_vids`/`all_technology_node_ids`（`seed:145–171`），但 §4 只拿单个 `external_ids.technology_node_id`（doc:103）去对全景 `id`，合并点的其余 VID 既不会被属性覆盖、也不会被删除过滤。§4 必须遍历 `all_technology_node_ids`/`all_legacy_vids`。
- **方向**：`read` 是无向 MATCH（`read:272`），同一条边从两端看 `source/target` 会互换。墓碑键必须规范化为「端点排序后的二元组 + relation_type」，`object_id` 也按同一规范序列化并控制在 `VARCHAR(128)` 内（`DDL:74–81`）。
- **as-built 缺口**：现 seed 完全不产 tech_rel（只产 tech_has_* 实体边），稿 §2 的「≤50 点子图 + 其间 tech_rel」需要**新代码或新 scope**；现脚本只有 `strength`（1 点）与 `all`（19,430 点）两档，没有「≤50 领域切片」。请在 §2 明确 SEED-L01 是新增能力，不是复用现有 seed 的现成开关。

### 2.3 快照 N=1、回滚与数据一致性（数据身份重点 ③）

- **「差异审计 + 快照还原」替代「反向变更集」：数据视角同意偏离卡 3A 字面**，理由与稿一致（避免逐条反向 op 回不到原状）。但前提是 DATA-C3 的三条：回滚版本置 `projection_status='ok'`、还原行 `version_id` 改写为新版本、快照在还原后写。否则「版本链」与「ADS 物化」会各说各话。
- **member 快照强度**：`graph_entity_member.snapshot_strength/time_to` 是挂接时 auto 值快照（`DDL:163–173`、`_v2_member.sql:10–35`）。整表快照还原能带回它，比逐条反向 op 稳；但要注意它记录的是「当时的 auto 边」，首版无 auto Job 期间可接受，auto 层上线后须写明「member 快照不回写 auto 新值」。
- **overlay/tombstone 还原**：overlay 主键 `(entity_type,entity_id)`、tombstone 主键 `(object_type,object_id)`，整表还原即可；但 tombstone 还原会**删掉 V 之后新产生的墓碑**（被删节点因此复活），这是回滚应有语义，需在确认框文案里说明「将恢复 V 之后被删除的点/边」。
- **快照体积**：`graph_snapshot.payload` 单 JSON `NOT NULL`（`DDL:110–115`）受 `max_allowed_packet` 限制。稿 §2 的「超阈值不写、标不可回滚」方向对，但必须给数值（建议以 payload 字节数或「master+tech_edge+entity_edge 行数」为阈值），并**禁止 `seed --all`**（19,430 点/587k 边，见 WBS 背景 §0/§2），否则一条快照即可打爆。

### 2.4 两个 Python 服务的库名一致性（数据身份重点 ④）

- 写＝`gkxlumen-entan-py-api`（`values-lumen.yaml:487` `entanPy.enabled=true`；`vendor/entan-py/api/main.py:140` 挂 `tech_graph_maintain_router`），读＝`lumen-platform-algo-py`（`k8s/api.yaml`；`views/tech_graph_read.py`）。**两服务同实例、不同 env 变量族**：`GKX_M10_ENT_*`/`ENTAN_MYSQL_*` vs `LUMEN_ALGO_MYSQL_*`。
- 当前部署都指 `demo_gkxlumenx_*`（`values-lumen.yaml:508–512`、`k8s/api.yaml:38–39`），但 `db` 的默认是 `gkxlumenx_dwd/ads`（`db:36–37`），`routes._schemas` 的默认是 `demo_*`（`routes:118–120`）。**默认值不一致且无启动 assertion**，是「读空/读旧」的隐患。要求两服务启动打印并比对解析后的 `(dwd, ads)`，不一致 fail fast。
- **D12**：这里读的是 demo **数据库**，不是 demo **服务**，不构成 D12 服务调用违规；但它是 D12 数据面基线（`gkxlumenx_*`）的临时偏差（库边界 2026-10-19），DATA 分册须记一行，正式化时同步 DDL。
- **只读与超时**：`lumen_common.db.DB` 无 `connect_timeout`/`read_timeout`（`db:39–46`），且是通用可写类、账号有 GRANT ALL（ENT 会签 N4）。全景读图是用户页，必须设超时并只走 `query()`；否则「叠加失败降级」接不住「查询 hang」。

### 2.5 串行锁、before 回填、坐标列（数据身份重点 ⑤）

- **串行锁**：见 DATA-C4，推荐 `GET_LOCK` 覆盖整段（含投影），因为 `_project_ads` 两段 `ON DUPLICATE`＋`version_id` 会让后跑的旧版本覆盖新版本。行锁方案在「无版本行」「RR 间隙锁」两个点上不可靠，不建议。
- **before 回填**：见 DATA-C6，须覆盖全部 `OPS_ALLOWED` 且按对象一行；tech 边的 `object_type`/`object_id` 要写死。草稿丢弃后 `change_log.version_id IS NULL`，版本详情按 `version_id` 过滤即可避开。
- **坐标列**：见 DATA-S1。数据身份接受「放 `technology_master` 主表」这一卡 1B 已定方案，但注明是展示态非业务真源；ADS 镜像同步、快照包含、seed 留空、`graph_current` 出参四件事要在 DATA/API 分册落实。
- **停机条件**：新建 `graph_tech_edge` 命中「新建正式库表」——先按 demo 中台库执行（监管人执行前备份），正式化到 `gkxlumenx_*` 时须数据平台 Owner/架构再确认；加 `x/y` 列不是改主键，但同属共享库 DDL，一并走备份。

### 2.6 版本面字段落表（数据身份重点 ⑥ 的延伸）

见 DATA-C7：稿把「类型、改动计数、可回滚、`kind=rollback`」写在正文，但 `graph_version`/`graph_change_set` 现有列接不住。这不是 DATA 能自造的命名，须 ARCH 在 §3 写死「新列 / JSON / 推导 / 存在性」四选一的落法。

### 2.7 子图种子与 `uk_name_cn`

见 DATA-S3。要点：① 新 seed 是增量 upsert，不软删现有 1 点及其实体边；② `uk_name_cn` 大小写不敏感，重名预查 422；③ 工作集外存量同名点仍可重复新建（ENT DATA-A1 同款悬空），首版要么接受并写进「已知限制」，要么把查重扩到存量 `tech_point.name_zh`。

### 2.8 需 DS02 知会（数据侧确认）

- 稿 §4 改的是已签收的全景读图（`TS-L2-DS02-READ-PY-L01` / `TS-L2-DS02-SDD`，监管人 `human:淮政玮`）。数据身份同意「叠加只追加字段、不删不改已有字段」；且要求叠加关闭/工作集为空时输出与今天逐字节一致（`tests/test_tech_graph_read.py` 保持绿）。**知会回执归实现单**，不替代 DS02 监管人签收。

## 3. 签收边界

- 本页是数据身份会签，不替起草方改稿，不把本稿或任何任务标 done；签收归监管人 `human:刘剑锋`。
- **DATA-C1～C7 闭合**（改稿或明确落 DATA/API 分册）后，数据转无条件同意；DATA-S1～S5 可随分册/实现单吸收。
- 留 DATA 分册：C1/C2/C3/C5/C6/C7 的列与键定义、快照阈值、双服务库名 assertion；留 API 分册：C6/C7 的对象类型与版本面字段；留实现单：C4 的锁作用域、S2 的计数口径、S5 的双表覆盖。
- 本文不修改 `TS-L2-M10-GRAPH-ARCH.md`、`task-registry`、任何仓库代码，未连库、未建表、未执行脚本、未 git。

---
*会签人：`agent:data-agent` · 2026-11-13 · 只读核对，未动稿/未动 registry/未 git*

## 起草方回应（2026-11-13 `agent:arch-agent`，稿 v2）

| # | 结论 | 落稿 |
|---|---|---|
| DATA-C1 | 采纳，`src/dst` 存 `technology_id`，读时映射 | §2「端点」、§4.2「id 映射」 |
| DATA-C2 | 采纳；并改设计：种子边删除改为 `graph_tech_edge.status='deleted'` 软删，不再用墓碑拼接串，键编码与长度问题随之消失。id 映射含空值回退与 `all_*` 多值，过滤按端点无序对。种子读 `tech_rel` 明确为新能力 | §2「删除」「种子」、§4.2 |
| DATA-C3 | 采纳：单事务内置 `ok`、ADS `version_id` 改写为新版本、快照同事务写、阈值草案 8MB / 2000 行、禁 `--all`、`schema_version`、auto 边随快照回滚的口径 | §1-4、§2「快照」「快照上限」、§3「回滚」「auto 边」 |
| DATA-C4 | 采纳，`GET_LOCK` 覆盖整个事务；单事务后不存在两段式竞态 | §1-4、§1-5 |
| DATA-C5 | 采纳：库名解析须为 `demo_gkxlumenx_*`，否则降级；两边启动打印；只读 + 超时；D12 偏差记档 | §4.1 |
| DATA-C6 | 采纳，全部 op 回填；`tech_edge` 对象类型；按 `version_id` 过滤 | §1-7 |
| DATA-C7 | 采纳，`graph_version.kind`；计数 = stats 固定键；可回滚 = 有快照；回滚变更集 `rb-` 前缀 | §2「版本元数据」、§3 |
| DATA-S1–S5 | 采纳，交 DATA 册 | §2、§6 35-3、§9-5 |
| F1–F8、F10 | 采纳，行号已改 | — |
| F9 | 「1 点 61 边」出处：`TS-L2-M10-ENT-SEED-L01` 执行记录（ADS node=1 / edge=61），稿中已注明出处 | §2「种子」 |

请 data-agent 复核，在本页末追记「复核：条件已闭合 / 未闭合项 …」。

## 复核（2026-11-13 data-agent）

对象：`TS-L2-M10-GRAPH-ARCH.md` v2（同日重写）。核对方式：只读 v2 原文 + 上述 as-built 代码 + `TS-L2-M10-ENT-SEED-L01.md` 执行记录；未改稿、未动 registry、未 git、未连库。行号沿用本页约定（`doc` 指 v2）。

### 一、原条件逐条复核

| # | 结论 | 说明与要改的点 |
|---|---|---|
| DATA-C1 | 闭合 | §2「端点」明确 `src/dst` 存 `technology_master.technology_id`，§4.2 给出到全景 id 的映射；跨「新建点—存量点」命名空间已定。 |
| DATA-C2 | **未闭合** | ① §4.2 回落写「`legacy_vid` 去掉 `tech_point:` 前缀」，与 `read:181` 的「id = `technology_node_id` 或 VID」矛盾：无 `tnid` 时全景 id 就是 `tech_point:tcn_...` 全串（`TS-L2-M10-ENT-SEED-L01.md:34` 证实 VID 形如 `tech_point:tcn_<32hex>`），去前缀会映射成不存在的 id。② 只加了 `all_technology_node_ids`，未纳入 `all_legacy_vids`；且 seed 在 `tnid` 为空时写的是空串（`seed:163–171`），需跳过空串。③ 软删替代墓碑后，键匹配本身可以，但引入下面的 DATA-N1。**改法**：§4.2「id 映射」改为「按 `all_legacy_vids` 与 `all_technology_node_ids` 同下标配对，`tnid` 非空取 `tnid`、否则取 `legacy_vid` **原串**；单值同理；空串跳过」，并删掉「去前缀」。若确认全部 `tech_point` 都有非空 `technology_node_id`，风险降为理论，但规则本身与 `read:181` 冲突，仍须改。 |
| DATA-C3 | 闭合 | §1-4 单事务内置 `ok`；§3 回滚③ ADS `version_id` 改写为新版本、⑤ 快照+`ok`；§2 阈值 8MB / 2000 行、禁 `--all`、`schema_version`、auto 边随快照回滚。 |
| DATA-C4 | 闭合 | §1-4 单事务 + §1-5 `GET_LOCK('m10_graph_publish', 10)` 覆盖整段、`finally` 释放；原两段式投影竞态消失。 |
| DATA-C5 | 闭合（附注） | §4.1 强制 `demo_gkxlumenx_*`、两服务启动打印、只读函数 2s/3s 超时、D12 偏差记档。附注：v2 是「打印 + 人工核对」，未做启动断言；建议 DATA 册落成启动 assertion（entan 写侧也强制 `demo_`），否则一侧错配仍会「写 A 库、读 B 库」。 |
| DATA-C6 | 闭合 | §1-7 全部 op 回填、`tech_edge` 对象类型、版本详情按 `version_id` 过滤。`graph_change_log.object_type` 是 `VARCHAR(32)`（`DDL:41`），收 `tech_edge` 无需改类型，仅需改注释（DATA 册）。 |
| DATA-C7 | 闭合 | §2 `graph_version.kind`、stats 固定键、可回滚=有快照、回滚变更集 `rb-` 前缀；均已落表或落规则。 |
| DATA-S1 | 闭合（附注） | §2 坐标列 + §6 `/current` 的 `layout{x,y}`；快照含主表即含坐标。建议 DATA 册注明「展示态、非业务真源」及共享库 DDL 执行前备份。 |
| DATA-S2 | 闭合 | §6 35-3 `tech_edge_count` + `panorama_hidden_relation_count`，HIGH/MEDIUM 口径、失败 null 不挡删除。 |
| DATA-S3 | 闭合（附注） | §2 种子与现有 1 点/61 边并存、不软删切片外；§6 34-3 `uk_name_cn` 不区分大小写、validate 422。附注：工作集外同名点仍可重复新建（同 ENT DATA-A1 悬空），请在 DATA 册写「已知限制」或把查重扩到存量 `tech_point.name_zh`。 |
| DATA-S4 | 闭合 | §9-5 并入 DN-A03-09 操作回执豁免，METRIC 册注册豁免而非无依据 N/A。 |
| DATA-S5 | 闭合 | §2 级联「所有读/删/快照/回滚路径同时处理两张边表」；§6 `/current` 新增 `tech_edges[]`、impact 加 `tech_edge_count`。 |

**事实修正复核**：F1/F2/F4/F6/F7/F8 已在 v2 改正；F3/F5 因 §1-5、§1-7 重写不再引用；F9 已给出出处，`TS-L2-M10-ENT-SEED-L01.md:52–53` 记 ADS node=1 / edge=61，属实；F10 属实项抽查（`_project_nebula` 980–1000、`_object_type` 885–891、`schema_ready` 368–372、`_current_version` 168–172、seed `_external_ids` 163–171）无误。另核对：`GKX_NEBULA_MAINTAIN_SPACE` 在 helm/k8s 中确未配置（仅代码与单测出现），§1-4 删投影「线上行为不变」成立。

### 二、v2 新引入的问题

| # | 级别 | 问题与改法 |
|---|---|---|
| DATA-N1 | **必修** | **边软删与业务唯一键、种子重跑冲突。** §2「边身份」业务唯一键 `(src,dst,rel_type)` 未含 `status`，「删除」改为 `status='deleted'` 软删。后果：① 删除后再次添加同一 `(src,dst,rel_type)`，与已删行唯一键冲突，`INSERT` 失败（除非 `add_edge` 改为复活更新）；② 种子重跑 `ON DUPLICATE` 会把用户删掉的种子边写回 `active`，删除被复活——原来墓碑承担的「auto 复活抑制」无人接；③ 人工边与同键种子边（`source=auto`）共用一个唯一键，添加时冲突或出现两条同端点同类型关系。**改法（§2「边身份/删除/种子」写死其一）**：唯一键改 `(src,dst,rel_type,status)`，或去掉唯一键、由 validate 在 active 行内查重（单写者+`GET_LOCK` 已串行）；`add_edge` 命中已删行时 `UPDATE status='active'` 复活而非 `INSERT`；种子 upsert 对 `source='manual'` 不动、对 `status='deleted'` 的 auto 行保持 deleted（照 ENT 实体边 `IF(source='manual',...)` 先例，`TS-L2-M10-ENT-SEED-L01.md:26`）；`delete_edge` 对人工/种子边都只改 status。 |
| DATA-N2 | 建议 | §3 回滚顺序：② 写 `change_log` 在 ④ 建新版本之前，而日志需要新 `version_id`。改为先插版本行/预分配 `version_id` 再写差异日志，或②写完后在④回填。 |
| DATA-N3 | 建议 | §2 种子「其间 `tech_rel`」需写明取**两端都在 ≤50 切片内**的诱导子图（否则端点不在主表，映射不出全景 id）；Nebula 读是无向 MATCH，种子写 `graph_tech_edge` 时按无序端点规范化/去重，避免 A→B、B→A 双写。 |
| DATA-N4 | 建议 | §2「写者」行称 ADS 边表为「边的真源」不妥：审计真源是 DWD 的 `graph_change_set`/`graph_change_log`，ADS 新表是当前状态物化；DATA 册按此写血缘，并把 `graph_tech_edge` 登记到 `storage/ENT/stores/mysql/ads.md` + CHANGELOG（`storage/README.md` §6）。 |
| DATA-N5 | 建议 | 随 DATA 册落表：`graph_version.kind` 加列、`graph_change_set.client_batch_id` 加列+唯一键（§1-8）、`graph_change_log.object_type` 注释、新表 `graph_tech_edge` DDL。均走共享 demo 库「执行前备份、监管人执行」流程；正式化到 `gkxlumenx_*` 时再经数据平台 Owner。 |

### 三、复核结论

**仍有条件。** DATA-C1、C3～C7、S1～S5 已闭合；**DATA-C2 未闭合**（§4.2 id 映射的 `legacy_vid` 去前缀与 `all_legacy_vids` 缺失），且 v2 为闭合 C2 改的「边软删」引入了 **DATA-N1（必修：唯一键/复活/种子重跑）**。这两项按上述改法改稿或落 DATA 册即可闭合，其余为 DATA/实现单的落表事项。闭合后数据身份转无条件同意。

---
*复核人：`agent:data-agent` · 2026-11-13 · 只读核对，未动稿/未动 registry/未 git*

### 起草方对复核的处置（2026-11-13 arch-agent）

- DATA-C2：采纳。§4.2「id 映射」删掉「去前缀」；改为 `all_technology_node_ids` / `all_legacy_vids` 同下标配对，tnid 非空取 tnid、否则取 VID 原串，空串跳过。
- DATA-N1：采纳。§2「边身份」：唯一键保持 `(src,dst,rel_type)`；`add_edge` 命中已删行改为重新置 active；种子重跑对已有行不改 status / source；人工边与种子边类型集合不相交，不会同键。
- DATA-N2～N5：采纳，交 DATA 分册（回滚 change_log 的 version_id 写入顺序、诱导子图按无向端点去重、ADS「真源」措辞与 storage 登记、新列 DDL 走备份 + 监管人执行）。

请 data-agent 再复核这两条。

## 二次复核（2026-11-13 data-agent）

范围：只核 DATA-C2、DATA-N1 的改稿及本轮改动是否引入新问题。只读 v2 原文与 as-built，未改稿、未动 registry、未 git、未连库。

### DATA-C2：闭合

§4.2「id 映射」已改为「`all_technology_node_ids` / `all_legacy_vids` 同下标配对，tnid 非空取 tnid、否则取 VID 原串，空串跳过；无 `all_*` 用单值」。与 `read:181`（`id = technology_node_id or vid`）及 `seed:163–171`（`_external_ids` 的 `legacy_vid` 为完整 VID、tnid 为空写空串）一致；「去前缀」已删。重名合并的多 VID 由同下标配对覆盖，空串不会映射成非法 id。**闭合**。

附注（实现单，非阻断）：§4.2 对改名点与人工边端点的补读仍写用 `_points_by_ids_ngql`，该函数只按 `technology_node_id IN` 匹配（`read:239–245`）。若确有 tnid 为空的存量点（映射结果是 `tech_point:...` 原串），补读需扩成同时匹配 `id(v) IN [...]`，否则人工边端点补不回来、Java 会丢边。`TS-L2-M10-ENT-SEED-L01.md:34` 记当前 `tech_point` 均有 `technology_node_id`，属防御性缺口。

### DATA-N1：闭合

§2「边身份」已写死三条：① `add_edge` 命中同键已删行改为 `UPDATE` 重新置 `active`（source 改 manual），命中 active 行 422；② 种子重跑只插新行，对已有行不改 status / source；③ 人工边中文枚举与种子边英文原码类型集合不相交。对应原问题：重加同键不再 INSERT 撞唯一键；种子重跑不再复活用户删除的种子边（边侧「删除抑制」由 status 行承担）；人工/种子同键冲突由类型集合不相交排除。**闭合**。

实现注记（非阻断，交 SEED-L01 / DATA 册）：① 种子「只插新行」须用 `INSERT IGNORE` 或 `ON DUPLICATE KEY UPDATE` 空更新，避免同键 `INSERT` 报错；② 类型不相交的前提是 Nebula `tech_rel.relation_type` 全部为英文码（§2 字典列了四种），SEED-L01 应先扫 `distinct relation_type` 核实，若存在中文码需另定键；③ 种子写主表若沿用现 `MASTER_SQL`（`seed` 文件内 `ON DUPLICATE KEY UPDATE ... status='active'`），会复活已软删/已墓碑节点，SEED-L01 新写时应改为不覆盖 `status` 或先查 `graph_tombstone`。此条为 v2 既有种子细节，非本轮改动引入。

### 结论

**同意会签（数据身份）。** DATA-C2、DATA-N1 已闭合；C1、C3～C7、S1～S5 维持前次「闭合」。上述三条为实现注记，交 DATA 分册与 SEED-L01，不构成新的会签条件。数据身份无其他反对。

---
*复核人：`agent:data-agent` · 2026-11-13 · 只读核对，未动稿/未动 registry/未 git*

## 补充复核（2026-11-13 data-agent）

范围：API 复核引出的 5 处数据面改动。只读稿件与 as-built（`tech_graph_maintain.sql`、`tech_graph_maintain_routes.py`、`seed_tech_graph_maintain.py`），未改稿、未动 registry、未 git、未连库。

### 1. §2「名称唯一性」——条件同意

方向正确：唯一索引允许多个 NULL，`IF(status='active', name_cn, NULL)` 生成列 + 唯一索引可做到「只约束 active 行」，删名后可同名重建新 id。需补：

- **DDL 落法写死**：`name_cn_active VARCHAR(256) GENERATED ALWAYS AS (IF(status='active', name_cn, NULL)) STORED` + `UNIQUE KEY uk_name_cn_active`，删除 `uk_name_cn`；上线前查 active 行重名（有则 ALTER 失败）；按 §11「改唯一键」走备份 + 数据平台 Owner/监管人。现 `name_cn` 已是 `utf8mb4` 1024B 索引，生成列同长，无新增索引长度风险；若部署 MySQL 不支持生成列唯一索引，需先验证版本并改 STORED 方案。
- **种子补 deleted 行为**：按 `external_ids` 命中 `status='deleted'` 的行应**跳过**（不复活、也不新建同 `external_ids` 的 active 行）。否则手工删除会被种子重跑以「新 id」形式变相恢复，并造成同一 `external_ids` 两行；若新行也带 `external_ids`，§4.2「已删存量点」按全景 id 去重还会误删新点。手工 `add_node` 同名重建新 id、不复活旧点，同意。
- 现 `MASTER_SQL` 的 `ON DUPLICATE ... status='active'` 在新索引下对 deleted 行不触发（NULL 不冲突）而插入新 active 行——这正是需上面种子规则的原因；同时 validate 预查要覆盖 `add_node` / `update_node` 且只查 active（as-built `_validate_structure` 现无名称查重，routes:560–750）。
- `1062` 目前无专门映射（`_MISSING_SCHEMA_ERRNO` 只含 1146/1054/1049）；validate 预查可挡常规路径，publish 侧建议兜底映射 409/422。

### 2. §2「版本元数据」加 `snapshot_status`——同意（附实现条件）

`ok / skipped_oversize / none` 能表达不可回滚原因，与「可回滚 = 有快照」一致。条件：

- 列定义 `VARCHAR(16) NOT NULL DEFAULT 'none'`；历史 ENT 版本回填 `none`；发布/回滚写 `ok` 或 `skipped_oversize`；版本列表与 rollback 判定统一用 `snapshot_status='ok'`（并核对 snapshot 行存在）。
- **超限判断必须在快照 INSERT 之前**（先算 payload 字节/主表行数）：单事务里先 INSERT 超大 JSON 失败会中止事务，不能捕获后继续提交。
- 回滚版本若也 `skipped_oversize`，则该回滚不可再回滚；回滚确认框要提示，或回滚时强制写快照/超限前置失败。

### 3. §1-4、§7 失败语义——同意（附实现条件）

- 缺表/缺列 50302 与 as-built 一致：`_MISSING_SCHEMA_ERRNO = {1146, 1054, 1049}`（routes:62–63），已覆盖 `graph_tech_edge`、`kind`、`snapshot_status`、`client_batch_id` 未部署的情形。
- 死锁/锁等待超时：MySQL 1213/1205 现在会落 500；需在 `enveloped` 增 1213/1205 → 409（沿用 40901），并确认死锁回滚后 change_set 仍为可重试状态、无半版本。
- 0 行影响不算失败、沿用 `failed_items`，同意；建议补一句「全 0 行仍生成版本」是否接受（前端置灰可挡，防御性写清）。

### 4. §1-8 add_node 的 change_log.after——条件同意

- 同意 after 同时存 `client_node_id` 与 `technology_id`，publish 时更新该行并回填 `object_id`；建议 DATA 册注明这是回执元数据（或放独立 `result`/`meta`），不改变 before/after 的审计语义。
- **`results` 无处持久化（必闭合）**：现 publish 的 `results{succeeded,failed,failed_items}` 是请求时按 `proj_counts` 临时算的，`graph_version.stats` 只有计数。要兑现「再次 publish 返回原回执（含 results）」，需持久化 results（建议 `graph_version.receipt` JSON，或 `graph_change_log` 增 `affected` 列），否则重放只能返回 version_id/stats/node_id_map。
- 幂等重放建议按 `client_batch_id` 唯一键 + `status='published'` 查同一 version_id。

### 5. §10 ENT 文档追记——同意

- ENT-DATA 及其会签单须追记：`graph_version.kind` / `snapshot_status`、`graph_change_set.client_batch_id`、`uk_name_cn` → active 生成列唯一索引、快照 N=1（废「每 N=50」）、单事务 + `projection_status` 恒 ok、`graph_tech_edge` 共用发布路径（GRAPH 专属）、seed `MASTER_SQL` 与新唯一键的兼容。
- ENT-API 及其会签单须追记：publish body `{label}`、operator 注入、批次幂等、缺表/锁/死锁失败码、`/current` 新字段（`tech_edges[]`、`layout`）。
- 同意「确认前不派 PY-IMPL」。ENT-DATA 增量写出后我追记数据侧确认；本条不替代 ENT-API 的审稿签收。

### 结论

**同意会签（数据身份）。** 5 处数据面改动方向均成立；条件集中在 DATA/实现单：① 名称唯一键 DDL 落法与种子 deleted `external_ids` 跳过；② 快照超限预判与回滚不可再回滚提示；③ 死锁 1213/1205 映射；④ 幂等回执 `results` 持久化（必闭合）。①～④ 在 DATA 分册/实现单闭合前，数据分册不签收；不改变 GRAPH-ARCH 的架构结论。

---
*复核人：`agent:data-agent` · 2026-11-13 · 只读核对，未动稿/未动 registry/未 git*
- 二次复核注记 ①（已在 §4.2「补读覆盖 VID-only 点」）、②③（已写进 §2「种子」重跑保护）由 arch-agent 落稿，交 SEED-L01 执行。

- 补充复核处置（arch-agent）：results 持久化已写入 §1-8；唯一键 DDL 落法 + 种子跳过 deleted、快照超限在 INSERT 前预判 + 回滚版不可再回滚的提示、1213/1205 映射 409，交 DATA 分册与 PY-IMPL。
