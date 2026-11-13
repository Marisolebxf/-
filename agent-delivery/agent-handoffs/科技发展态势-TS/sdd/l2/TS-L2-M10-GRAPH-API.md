# TS-L2-M10-GRAPH-API · 维护管理 · 维护技术图谱（34–40）· 后台接口设计（ENT-API 增量）

- 任务：`TS-L2-M10-GRAPH-API`
- 日期：2026-11-13
- 状态：**v2，会签条件已回应**。本册是 `TS-L2-M10-ENT-API.md` 的增量，不重写 ENT 已冻结的 7 op 形状与 R1–R6 语义；会签后由协调方把 §9「对 ENT-API 的追记」落到 ENT 册。
- 监管：`human:刘剑锋` · 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：全景序 34–40（需规 `bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md:260–363`）
- 上游（均已签收 / 已会签）：
  - `sdd/l2/TS-L2-M10-GRAPH-ARCH.md`（v2，2026-11-13 监管人 `human:刘剑锋` 签收；本册唯一架构真源）
  - `sdd/l2/会签/TS-L2-M10-GRAPH-L2-裁定.md`（**v2 必须与本单一致**：A1–A8 监管人拍板、B1–B20 跨稿统一口径）
  - `sdd/l2/会签/TS-L2-M10-GRAPH-L2-SIGNOFF-{ARCH,DATA,ALGO,PRODUCT,API}.md`（五身份有条件同意；条件逐条回应见 §14）
  - `sdd/l2/会签/TS-L2-M10-GRAPH-SIGNOFF-{API,DATA,ALGO,PRODUCT}.md`（一轮会签；「交 API 册」条目已在一轮落地）
  - `sdd/l2/TS-L2-M10-ENT-API.md`（先例；本册是其增量，ENT 已冻结部分只引用）
- as-built 核对（2026-11-13 自读，不采信稿述）：
  - Python `repos/lumen-algo-py/vendor/entan-py/api/tech_graph_maintain_routes.py`（**routes**）、`scripts/mysql/tech_graph_maintain.sql`（**DDL**）、`lumen_common/algorithms/tech_graph_read.py`（**read**）、`vendor/entan-py/entan/common/nebula.py`（**entanNebula**）
  - Java `gkxlumen-display/.../controller/SituationMaintainEntController.java`（**DispCtrl**）、`feign/RemoteTechGraphMaintainClient.java`（**DispFeign**）、`service/SituationPanoramaService.java`（**PanoSvc**）、`service/TechGraphReadAdapter.java`（**ReadAdapter**）；`gkxlumen-topic/.../techgraph/TechGraphMaintainController.java`（**TopicCtrl**）、`TechGraphMaintainClient.java`（**TopicFeign**）
  - FE `src/api/situation/maintain-ent.ts`（**FeApi**）、`src/types/maintainEnt.ts`（**FeTypes**）、`src/types/maintain.ts`（**FeModel**）、`src/views/situation/maintain/maintainModel.ts`（**FeGraph**）

## 0. 范围与增量边界

| 项 | 裁定 |
|---|---|
| op 枚举 | 由 ENT 的 **7 个扩到 10 个**：新增 `add_node` / `add_edge` / `delete_edge`（34 / 36 / 37）。`update_node`（38）与 `delete_node`（35）沿用 ENT 形状，本册只补取值域与查重规则 |
| 端点 | 在既有前缀下新增版本四端点；`/current`、`/nodes/{technology_id}/impact`、`changes`、`changes:validate`、`publish` 为既有端点加字段/加 body |
| 不改 | ENT 已冻结的 `hang_entities` / `unhang_entities` / `update_entity_overlay` / `delete_entity_edge` / `update_entity_edge` 形状、R1 推荐、R2 既有字段、conflicts、错误信封结构（`{code,msg,data}`）均不重写 |
| 写链 | 不新开链：FE → gateway → display → topic → entan-py → MySQL 工作集（ARCH §1）。Java 零 nGQL、零 DWD 读写，版本读写在 Python |
| 不返 mock | 所有新端点只返服务端真实数据；工作集为空返回空态（`items: []` / `nodes: []`），不造假行 |
| 不造指标 | 本册只定接口字段；`strengthManual` 等人工值不进任何 `M_TECH_*` 公式（ARCH §9、ALGO-C5） |

## 1. 写请求通用形状

所有写 op 沿用 ENT 的 `changes` 变更集语义（ENT-API §2、§6）：`ops[]` 单批上限 **50**（按 op 条数计，`routes:42`、`:307`；一个 `delete_node` 可带多个 `technology_ids` 仍算 1 条），每 op 必带 `client_op_id`（同批唯一），变更集带 `base_version` 乐观锁。

本册**新增**三个批次级字段（API-C8 / ARCH §1-8 / 裁定 A7）：

| 字段 | 层级 | 类型 | 必填 | 语义 |
|---|---|---|---|---|
| `client_batch_id` | `changes` / `publish` 的 body 顶层 | string ≤64 | **选填**（`changes` 缺省时服务端生成并回显） | 一次「保存图谱」可用同一个值贯穿 changes → publish；落 `graph_change_set.client_batch_id`。**只有客户端显式提供时才享受重试幂等**；服务端生成的批次不承诺重试去重（裁定 A7）。同批 `client_op_id` 仍须唯一 |
| `operator` | body 顶层 | string ≤64 | FE **不传** | display 用 `SecurityUtils.getUser()` 用户名覆盖，不信前端（API-C3，注入点见 §6.3） |
| `trace_id` | body 顶层 | string ≤64 | 选填 | 沿展示链写入 `change_log.trace_id` |

`changes` 的 body 形状（在 ENT 基础上加 `client_batch_id`）：

```json
{
  "base_version": 11,
  "client_batch_id": "batch-20261113-ab12cd",
  "operator": "<display 注入，FE 传了也覆盖>",
  "trace_id": "…",
  "ops": [ /* 10 op 封闭枚举 */ ]
}
```

`changes` 回执（既有，加 `client_batch_id`、`idempotent`）：`{change_set_id, status:"draft", client_batch_id, idempotent?:true}`。同一 `client_batch_id` 重试返回首次回执（§3.1）；服务端生成批次也回显，供 publish 透传。

## 2. op 契约冻结

### 2.1 新增 op：`add_node`（叶 34）

```json
{
  "op": "add_node",
  "client_op_id": "op-0001",
  "client_node_id": "draft-n1",
  "name_cn": "具身智能",
  "category": "算法",
  "description": "……",
  "importance_level": "高",
  "layout": { "x": 312.5, "y": 180.0 }
}
```

| 字段 | 类型 | 必填 | 取值域 / 规则 |
|---|---|---|---|
| `client_node_id` | string 1–64 | **是** | 临时号，**同批唯一**；只在本批有效，跨批引用一律用 `technology_id`。不写库，不作最终 id |
| `name_cn` | string 1–256 | **是** | 非空；**active 行查重**（`utf8mb4` 大小写不敏感，DDL 注释写明），与库内 active 行或**同批另一个 add_node** 重名 → 422/42201。唯一性只约束 active：软删后可同名重建；改名撞 active 才 422（裁定 A1 / B10） |
| `category` | string 1–64 | **是**（34-3 技术分类必填） | **维表下拉、空则手填**（裁定 A3）：选项来自 `dim_tech_domain`，显示并提交中文 `domain_name`，落 `technology_master.category`（VARCHAR(64)）；维表为空/不可用时允许手填。后端**只校验非空与长度 ≤64，不做外键、不做存在性校验**。演示分类由 DATA 在 SEED-L01 给一版 |
| `description` | string | 否 | 任意文本（TEXT）；缺省写 NULL |
| `importance_level` | enum `高\|中\|低` | 否 | 缺省（省略或 null）写 **NULL**，不吃 DDL 默认「中」（避免默认值被当成权威等级，ALGO-C6）；枚举外 → 422/42201 |
| `layout` | object `{x:number,y:number}` | **是**（34-4 指定位置） | **画布世界坐标（浮点，单位 px，允许负值）**，`x`/`y` 各在 ±1 000 000 内，否则 400/40001。落 **`technology_master.layout_x / layout_y`**（主表权威）与 ADS **`graph_entity_node.layout_x / layout_y`**（读侧镜像，发布时以主表覆盖）；种子点两列为 NULL（裁定 B2） |

- **不带 `technology_id`**：号在 `publish` 时生成，经 `node_id_map` 回传（§2.5）。
- 坐标口径冻结：`x`/`y` 为逻辑画布世界坐标，原点在画布左上、与画布初始缩放 1.0 对齐，可负。FE 现壳的 0–100 百分比（`FeModel:89`）由 FE-TS-10D 迁移（API-N1）；`maintainModel.ts:252–288` 的 mock 种子同步改口径。
- `category` 存中文名而非 `domain_code`，保证 `/current`、版本详情、全景叠加无需再查字典（PROD §5.2）；`domain_name` 若超 64 字符由 DATA 评估加宽，API 校验上限随之调整。

### 2.2 新增 op：`add_edge`（叶 36）

```json
{
  "op": "add_edge",
  "client_op_id": "op-0002",
  "src": { "client_node_id": "draft-n1" },
  "dst": { "technology_id": 34 },
  "rel_type": "依赖",
  "strength_manual": 7.5,
  "time_range": { "from": 2022, "to": 2024 }
}
```

| 字段 | 类型 | 必填 | 取值域 / 规则 |
|---|---|---|---|
| `src` / `dst` | object，**二选一引用** | **是** | `{technology_id:int}` 或 `{client_node_id:str}`，**不收裸值**；不得同时给两者或都缺（400/40001）。`technology_id` 须为 active 技术点；`client_node_id` 须命中**同批** add_node，否则 422「临时号引用不到」 |
| 方向 | — | — | **有向**：`src → dst`。业务唯一键 `(src,dst,rel_type)`；`A→B` 与 `B→A` 是两条。`src` 解析后等于 `dst`（自环）→ 422 |
| `rel_type` | enum `包含\|依赖\|促进` | **是** | 监管人 2026-11-13 拍板（ARCH §11 拍板 P2）封闭三项；枚举外 → 400/40001。**不从全景 `relationTypeOptions` 取**，存量英文码不映射进这三项（ALGO-S1 / 裁定 B5） |
| `strength_manual` | number | **是**（36-3 关系强度） | **0–10，步长 0.01**（与 ENT 46 `update_entity_edge` 对齐，`routes:677–680`）；越界/非数字 → 422/42201。FE 弹窗按 0–10、步长 0.1 展示，后端仍收 0.01（PROD-API-C8） |
| `time_range` | object `{from:int,to:int}` | **否**（裁定 A6：36-3 为「可设置」，改选填） | 填则年份 **1900–2100** 整数、`from ≤ to`（与 ENT 46 对齐，`routes:681–692`）；省略/null 表示不设时间范围。FE 文案「时间范围（选填）」，把「2024-2026」文本解析成两个整数。**A6 覆盖 DATA-API-C3 中「人工边必填」的表述** |

- **重复判定**（422/42201）：命中同键且 `status='active'` 的行 → 「关系已存在」；命中同键**已软删的人工行** → **复活该行**（置 active、source 改 manual、写新强度/时间、`version_id` 改本次版本；若复活行原为 auto，`strength_auto`/`rel_code` 保持不动），不报错、不另插行（DATA-N1 / ARCH §2）。
- **种子边不经 add_edge 复活**：种子边 `rel_type` 为英文原码，与中文三枚举不同键，`(src,dst,rel_type)` 命不中；种子边恢复只走版本回滚或种子重跑（DATA-API-S7 / ALGO-API-C7）。补一句防止实现误解。
- **同一对点允许 auto 与 manual 并存**（裁定 B8）：两类键不相交；界面分别标「存量」「人工」，前端需渲染平行边（impact 按边计数）。
- 同批两个 add_edge 解析后同键 → 第二条 422。
- **两遍处理**：publish 先处理全部 `add_node` 拿到 `technology_id`，再处理其余 op；FE 不必排序（API-C1）。临时号只在同批有效（跨批引用已存点用 `technology_id`）。

### 2.3 新增 op：`delete_edge`（叶 37）

```json
{ "op": "delete_edge", "client_op_id": "op-0003", "edge_id": 123 }
```

| 字段 | 类型 | 必填 | 规则 |
|---|---|---|---|
| `edge_id` | int64（JSON number；Java 侧 Long） | **是** | `graph_tech_edge` 服务端自增主键（`/current` 的 `tech_edges[].id`）。人工边与种子边（source=auto）**同一身份**，一律按 `edge_id` 删；不接受端点键。不存在或已 deleted → 422「关系不存在或已删除」 |

- **软删**：`graph_tech_edge.status='deleted'`（不物理删、不写墓碑拼接串，ARCH §2 / DATA-C2）。
- 种子边同样可删（37-2）；删除只影响该边，两端节点保留（37-3）。
- **边界**：只有工作集 `graph_tech_edge` 内的边可删；Nebula 中未被种子纳入的 `tech_rel` 不在 `/current.tech_edges[]`，前端拿不到 `edge_id`，也就无法删。`panorama_hidden_relation_count` 只服务「删点」确认框，不用于删边（ALGO-API-C7）。

### 2.4 沿用 op：`update_node`（叶 38）的补正

形状沿用 ENT（ENT-API §2）：`{op, technology_id, patch{name_cn?, category?, description?, importance_level?}, client_op_id}`。本册只补**取值域与查重**（API-C13 / ALGO 事实修正 7）：

| patch 字段 | 类型 | 必填 | 规则 |
|---|---|---|---|
| `name_cn` | string 1–256 | 否 | 非空；改名后须在 **active 行**内唯一（排除自身），撞库或撞同批 add_node → 422/42201（现 as-built 无查重，会以 MySQL 1062 变 500，`routes:715–726`）。软删同名行不阻碍改名 |
| `category` | string 1–64 | 否 | 同 `add_node` 口径（中文名、无外键） |
| `description` | string | 否 | 省略=不改；传空串=写空 |
| `importance_level` | enum `高\|中\|低` \| null | 否 | 省略=不改；**传 `null`=写 NULL（清除等级）**；三枚举外 → 422（DATA-API-S3）。界面空值显示「未设置」，不得默认「中」 |
| `layout` | — | — | **不入 patch**：节点拖拽禁用（ARCH §0），只有 `add_node` 有落点。若后续要持久化拖拽，另加字段并升版 |

- `patch` 至少含上述 4 键之一，否则 422。`technology_id` 须为 active 技术点。
- **名称唯一性只约束 active 行**（ARCH §2 / 裁定 A1）：新增 `name_cn_active` 生成列唯一索引替换 `uk_name_cn`（DDL:19；DATA 定 DDL，监管人执行前备份，无需数据平台 Owner 书面确认）。validate 只查 active 行。

### 2.5 publish 回执的 `node_id_map`

`changes` 回执不含映射（`technology_id` 发布时才生成，`routes:773–778`）；映射只在 **publish 回执**给：

```json
"node_id_map": { "draft-n1": 101, "draft-n2": 102 }
```

- 由本次 **`op='add_node'` 且 `after.client_node_id` 非空** 的 `change_log.after`（发布后主表行 + `client_node_id`，含 `technology_id`）重建（DATA-API-S5 / ALGO-DATA-C10）；无新增点或未命中为 `{}`。不得把 `update_node`/`delete_node` 的 `node` 行混入。
- 前端据此把草稿临时号换正式编号；34-5 的「待保存 → 编号」由此实现。
- 34-5 编号可见性：节点详情显示 `technology_id`。

## 3. changes / validate / publish 的请求与回执

### 3.1 提交 `POST …/changes`

- body 见 §1；`ops` 收 10 op；`client_batch_id` 选填。
- 回执：`{change_set_id, status:"draft", client_batch_id, idempotent?}`。**客户端提供 batch** 且命中同批未放弃变更集 → 返回首次回执（`idempotent:true`），不重复建点/建版本；**未提供**时服务端生成新批次并回显，不承诺重试去重（裁定 A7）。
- **批次边界**（裁定 B11 / API-DATA-C4/C5）：
  - 命中 `rejected` 变更集 → 409/40901「批次已放弃，请重新生成 `client_batch_id`」，不返回旧回执；
  - 命中 `draft`/`published` 且 **`ops` 与首次一致** → 幂等返回；
  - 命中同批次但 `ops` 不同 → 409/40901（不得静默丢弃新 ops）。
  - 并发同批提交撞唯一键 1062 → 按 `client_batch_id` 重读已存在行并返回 `idempotent:true`，不把幂等重试报成失败（DATA-API-S4）。
- 提交前跑与 `changes:validate` **同一套**结构/存在性校验；不通过 → 422/42201 + `errors[]`（含 `index`/`client_op_id`/`op`/`msg`），不落库。
- **幂等改为批次级**：as-built 只查 `ops[0].client_op_id`（`routes:758`、`:320–325`），本册冻结为按 `client_batch_id` 查（DATA 定唯一键，允许多 NULL）；`client_op_id` 仍要求同批唯一。

### 3.2 预览 `POST …/changes:validate`

- body 同 changes（`base_version`、`ops`；`client_batch_id` 可不传）。不改库、不建 change_set。
- 成功回执 `{dry_run:true, op_count, summary, preview[]}`；`summary` 键扩到 10 op（`SUMMARY_KEYS`，`routes:53–60` 现仅 6 键）：
  `{add_node, add_edge, delete_edge, hang_entities, unhang_entities, delete_node, update_node, update_entity_overlay, delete_entity_edge, update_entity_edge}`。
- `preview[]` 每项 `{index, op, client_op_id, target, desc}`，`desc` 为简体中文（如「新增技术点「具身智能」」）。违例 → 422/42201 + `errors[]`。
- **39-1 的 N 由前端草稿栈计算**（净差 op 条数，与后端 `OPS_LIMIT=50` 同口径）；`validate.op_count` 只用于预览，不作为 39-1 取数来源（API-METRIC-C8）。
- **35-3 删除确认联动**：前端删除前调 `impact`（§5.2）取计数，validate 不负责该计数。

### 3.3 发布 `POST …/changes/{change_set_id}/publish`

- **新增 body（API-C3，选①）**：`{ "label": "…", "client_batch_id": "…" }`，两字段均可选。
  - `label` 空 → 服务端给「保存 {yyyy-MM-dd HH:mm}」；上限 **128**（`graph_version.label VARCHAR(128)`，PROD-API-C10），超长 → 400/40001。
  - `client_batch_id` **仅作一致性护栏**：提供了且 ≠ 变更集已存值 → 409/40901；未提供 → 忽略（DATA-API-S9）。
  - display controller 与 topic client 都要加 `@RequestBody`（现无 body，`DispFeign:37–38`、`TopicFeign:42–43`）。
- **幂等/状态边界**（ARCH-API-C2 收紧，裁定 B11）：
  - 变更集已是 `published`：**带 batch 且与已存值不符 → 409**；**不带 batch 或 batch 相同 → 返回原回执、不报 409**；
  - 变更集 `rejected` → 409/40901，不返回旧回执；
  - 其余（draft/approved）→ 正常发布。
- 回执（新增 `node_id_map`、`results` 可空）：

```json
{
  "version_id": 12,
  "status": "published",
  "kind": "save",
  "stats": { "tech_nodes": {"added":1,"updated":0,"removed":0},
             "tech_edges": {"added":1,"updated":0,"removed":0},
             "entity_links": {"added":0,"removed":0},
             "entity_edges": {"added":0,"updated":0,"removed":0},
             "entity_attrs": {"updated":0} },
  "results": { "succeeded": 2, "failed": 0, "failed_items": [] },
  "node_id_map": { "draft-n1": 101 }
}
```

- `results` 语义沿 ENT（`routes:863–882`）：op 影响 0 行记 `failed_items`，但**发布照常成功**（不是整笔失败，ARCH §1-4 / N4）；逐条含 `{index, client_op_id, op, reason}`，`reason` 为中文或稳定 code（PROD-API-C4）。
- 回执 `results` 随版本行持久化 **`graph_version.publish_results`**（DATA 已定列，不再写「候选」），与版本、`change_log.after` **同一发布事务**写入；重试时按 change_set → version 原样返回。**历史版本无该列值时返回 `results: null`**（API-C8 三次确认），前端按「该版本未记录逐条结果」处理。
- `stats` 规范键见 §3.4；新版本恒写，`kind='save'`（含 ENT 页经同一 publish，裁定 B16）。
- 发布为**单事务 + 串行锁**（ARCH §1-4/§1-5）：取锁 → 比基线 → 插版本 → 主表 / overlay / 墓碑 → ADS node / edge / member / `graph_tech_edge` → change_log before/after 回填 → 全量快照 → `projection_status='ok'` → 提交 → 释放锁。**不再产生 pending 版本**（50301 退役，§7）。

### 3.4 `stats` / 回滚预览的规范分组计数（唯一口径）

**本节嵌套 JSON 是 `graph_version.stats` 与 `rollback:preview.counts` 的唯一持久化形状**（裁定 B1 / ARCH-API-C2 / DATA-API-C2 / ALGO-API-C3）。DATA 册的扁平键（`node_add` 等）废止并由 DATA 同步回改；实现、落库、前端只认本节。

| 组 | 键 | 来源 |
|---|---|---|
| `tech_nodes` | `added` / `updated` / `removed` | add_node / update_node / delete_node |
| `tech_edges` | `added` / `updated` / `removed` | add_edge / delete_edge（含 delete_node 级联）；`updated` 只在回滚差异中出现（同一 `edge_id` 两端都存在但强度/时间/类型有变，API-DATA-C7） |
| `entity_links` | `added` / `removed` | hang_entities / unhang_entities |
| `entity_edges` | `added` / `updated` / `removed` | hang / unhang / delete_entity_edge / update_entity_edge |
| `entity_attrs` | `updated` | update_entity_overlay |

- **按 `kind` 分别定义（裁定 B12 / DATA-API-N1）**：
  - `kind='save'`（含 `seed`、历史 `ent`）：`stats` 是**该版本发布时的操作回执计数**；
  - `kind='rollback'`：新版本的 `stats` **就是生成它的那次 `rollback:preview` 的 `counts`**（同一快照求差函数、同一次求差结果）；
  - `counts` 始终是「目标快照与当前工作集的净差」。
  三者共享同一套分组键；**唯一禁止**的是：不得拿**目标版本自己的** `stats` 直接充当预览计数（目标版本 `stats` ≠ 当前→目标的净差）。
- `counts` 方向：`added` = 目标有、当前无（回滚时**恢复**）；`removed` = 当前有、目标无（回滚时**移除**）；`updated` = 两边都有但值不同（回滚时**还原**）。`total` 为各组之和。
- **历史 ENT 版本不回填**（DATA-API-S6 / 裁定 B1）：`stats` 可能是四种形状——`{"ops":N}`（发布中断，`routes:844`）、旧扁平四键（`routes:852–858`）、`{}`、`NULL`。版本列表/详情**原样返回**，前端按 §4.1/§7 的兼容规则显示，缺组**不补 0**；DATA 回填清单不含 `stats`。
- 计数为操作回执计数，按 DN-A03-09 **建议豁免范围（34–40 范围九类：35-3 四项、39-1、40-3、40-4、publish `results`、rollback `results`；与请示单「七类」是同一批数字的不同拆法）** 豁免 D9（裁定 A8 / API-METRIC-C2），不注册 `metric_id`；未获 PM/数据 Lead 确认前文档维持「建议豁免」措辞。

## 4. 版本端点（新，叶 40-2 / 40-3 / 40-4）

均挂在既有前缀下，不新开平行资源；三层路径见 §6.1。读写只在 Python（Java 不扫 DWD，D3）。`operator` 由 display 注入（§6.3）。

### 4.1 版本列表 `GET …/versions?page&size`

- 分页：`page` 默认 1（≥1），`size` 默认 20（1–100）；按 `version_id` 倒序；非法参数 → 400/40001（沿 `routes:180–194`）。
- 回执：

```json
{
  "items": [
    { "version_id": 12, "parent_version_id": 11, "label": "保存 2026-11-13 14:30",
      "kind": "save", "operator": "张三", "operator_display": "张三",
      "created_at": "2026-11-13 14:30:12", "is_current": true,
      "stats": { "...": {} },
      "rollbackable": true, "snapshot_status": "ok", "not_rollbackable_reason": null }
  ],
  "total": 1, "page": 1, "size": 20
}
```

| 字段 | 语义 |
|---|---|
| `kind` | `save`（本次保存，含 ENT 页）/ `rollback` / `seed` / `ent`（**仅**历史回填；新保存一律 `save`，裁定 B16）。落 `graph_version.kind`（DATA） |
| `is_current` | `version_id == 当前版本`；当前版本行**不提供回滚**（PROD-API-C10） |
| `rollbackable` | `snapshot_status='ok'` 且存在快照行 → true；否则 false |
| `snapshot_status` | `ok` / `skipped_oversize` / `none`（DATA 定列）；**不在界面直接显示**，只用于派生 `rollbackable` 与 `not_rollbackable_reason`，原码不得直出（DATA §3.4） |
| `not_rollbackable_reason` | `null` / `"no_snapshot"` / `"snapshot_oversize"`，供列表显示不可回滚原因（PROD-C11 / API-N7） |
| `operator_display` | **后端计算**（见 §4.5），前端直接显示，不本地拼 |
| `stats` | §3.4；历史版本可能为 `{"ops":N}` / 旧扁平键 / `{}` / `NULL` |

- 空列表 → `items: []`（不造 0、不 404）。
- **中文显示映射**（PROD-API-C1 / 裁定 B19；界面不得出现原始码）：

| 码 | 中文 |
|---|---|
| `kind=save` / `rollback` / `seed` / `ent` | 保存 / 回滚 / 种子 / 历史版本 |
| `not_rollbackable_reason=no_snapshot` | 该版本无快照，不能回滚 |
| `not_rollbackable_reason=snapshot_oversize` | 该版本数据量超出快照上限，不能回滚 |
| `tech_nodes` / `tech_edges` / `entity_links` / `entity_edges` / `entity_attrs` | 技术点 / 技术点间关系 / 实体挂接 / 实体关系 / 实体属性 |
| 版本统计时态 `added` / `updated` / `removed` | 新增 / 修改 / 删除 |
| 回滚预览时态 `added` / `updated` / `removed` | **恢复 / 还原 / 移除**（不得译反） |

### 4.2 版本详情 `GET …/versions/{version_id}?page&size`

回执：版本元数据（同 §4.1 单行全部字段，含 `is_current`）+ `changes[]` + `changes_total`：

```json
{
  "version_id": 12, "parent_version_id": 11, "label": "…", "kind": "save",
  "operator": "张三", "operator_display": "张三", "created_at": "…", "is_current": true,
  "stats": {}, "rollbackable": true, "snapshot_status": "ok", "not_rollbackable_reason": null,
  "changes_total": 3, "page": 1, "size": 100,
  "changes": [
    { "change_id": 88, "object_type": "tech_edge", "object_id": "123", "op": "add_edge",
      "summary": "新增关系「具身智能→大模型（依赖）」",
      "src_name": "具身智能", "dst_name": "大模型",
      "before": null, "after": { "…": "…" },
      "operator": "张三", "at": "2026-11-13 14:30:12" }
  ]
}
```

- **按 `version_id` 过滤** change_log，不按 `change_set_id`（草稿丢弃后 `version_id` 仍为空，`routes:771–776`；DATA-C6）。
- 分页：`page` 默认 1，`size` 默认 100（1–500）；`changes_total` 为总条数（PROD-API-C12；`delete_node` 级联可能产生大量行）。
- `object_type`：`node`（add/update/delete_node）、`tech_edge`（add/delete_edge，新值）、`entity`、`edge`（ENT 既有）。`object_id`：node 用 `technology_id`；tech_edge 用 `graph_tech_edge` 主键（add_edge 在发布事务内回填，API-C7）。
- **`summary` 为服务端生成的中文摘要**（PROD-API-C2 / 裁定 B19）：新增技术点「X」、编辑技术点「X」（描述）、删除技术点「X」、新增关系「A→B（依赖）」、删除关系「A→B（依赖）」、挂接实体「X」、实体关系变更等；不得只给 `add_node` 等 op 码。`object_type` 中文：`node`→技术点、`tech_edge`→技术点间关系、`entity`→实体、`edge`→实体关系。
- **`tech_edge` 变更必须带两端节点名**：change 行附 `src_name` / `dst_name`（发布时从主表快照，删除端点用删除前名）；界面不得只显示 `src`/`dst` 数字（PROD-DATA-C7）。
- `before`/`after`：新增类 before 为空、`after` 为发布后行；删除类 `after` 为空、`before` 为发布前行；`add_node` 的 `after` 额外带 `client_node_id`（回执元数据，不改变审计语义）。
- **历史行显示规则**（PROD-API-C2/C6）：`before=null` →「修改前未记录」；历史 `after` 是提交的 op 请求而非发布后行（`routes:771–776`）→ 界面标「历史记录：仅保留操作请求」，按动作白名单展示；隐藏 `client_op_id`、`client_node_id`、`trace_id`、`base_version`、`op` 等内部字段。`before/after` 字段中文标签真源由 FE-TS-10D 落实（名称/分类/描述/重要性/位置/关系类型/强度/时间范围/状态/来源）。
- `delete_node` 级联删除的 `graph_tech_edge` **逐条记一行 `object_type='tech_edge'`、`op='delete_edge'`**（采纳 DATA-API-C18 / PROD-DATA-C7 建议），保证 40-4 明细可展示；`stats` 中 `tech_edges.removed` 同步计数。
- 版本不存在 → 404/40401。ENT 发布的版本同样可看。

### 4.3 回滚预览 `POST …/versions/{version_id}/rollback:preview`

- body：`{ "base_version": 11 }`（必填；不符当前 → 409/40901 + `data.current_version`）。
- 回执：

```json
{
  "target_version": 8, "label": "…", "created_at": "…",
  "operator": "李四", "operator_display": "李四",
  "base_version": 11,
  "rollbackable": true, "snapshot_status": "ok", "not_rollbackable_reason": null,
  "counts": {
    "tech_nodes":   { "added": 0, "updated": 0, "removed": 2 },
    "tech_edges":   { "added": 0, "updated": 1, "removed": 3 },
    "entity_links": { "added": 0, "removed": 1 },
    "entity_edges": { "added": 0, "updated": 0, "removed": 4 },
    "entity_attrs": { "updated": 1 }
  },
  "total": 12
}
```

- `counts` 由**目标快照与当前工作集求差**得出，分组同 §3.4；与回滚生成的新版本的 `stats` 使用**同一求差函数**（裁定 B12 / DATA-API-C7），不是目标版本自己的 `stats`。
- 求差口径：存在性按 `status='active'` 判（软删行不算「当前有」）；行键 `technology_id` / `edge_id`；比较字段排除 `version_id`、`updated_at` 及生成列 `name_cn_active`（裁定 B13）。
- **无快照 / 超限**：仍返回 200，`rollbackable=false`、`not_rollbackable_reason`、`counts:null`；前端置灰回滚按钮并显示原因（PROD-C11 / R2）。不返回 409（预览不改库）。
- `counts.total` 含「恢复 + 移除 + 还原」三类，界面文案不得只写「撤回 X 项」（PROD-DATA-C1 / METRIC-C7）；双向语义见 §7。
- 预览是 POST，走写守卫（§6.3）。

### 4.4 回滚 `POST …/versions/{version_id}/rollback`

- body：`{ "base_version": 11, "label": "回滚到 v8" }`（`label` 可选，默认「回滚到 v{n}」，上限 128）。
- 回执（形状对齐 publish，`kind=rollback`；回滚不生成新 `technology_id`，`node_id_map` 为 `{}`）：

```json
{
  "version_id": 13, "status": "published", "kind": "rollback",
  "stats": { "...": {} },
  "results": { "succeeded": 12, "failed": 0, "failed_items": [] },
  "node_id_map": {}
}
```

- 单事务 + `GET_LOCK('m10_graph_publish',10)`（与 publish 同一把锁，ARCH §1-5）：读目标快照与当前工作集**用与预览相同的求差函数** → 每条差异写一行 change_log（before=当前、after=目标）→ 按快照还原各表、ADS 行 `version_id` 改为新版本 → 写新版本（`kind=rollback`、parent=当前、operator=display 注入值、`projection_status='ok'`）→ 写快照 → 提交。回滚变更集 id 用 `rb-` 前缀。
- **`technology_master` 还原顺序**（裁定 B13 / DATA-API-C6）：**先整表 `DELETE`，再按快照 `INSERT` 并显式带 `technology_id`**（避免先插后删撞 active 唯一键）；排除生成列 `name_cn_active` 与 `updated_at`。其余表同法按 §4.1 显式列清单还原，快照不含生成列。
- `results`：`succeeded` = 实际应用的差异条数，`failed=0`、`failed_items=[]`；随版本行持久化到 `graph_version.publish_results`（DATA-API-S1/C17），版本详情/审计可查。
- 无快照版本：409/40901（防御；按钮本已置灰）。`base_version` 不符或目标即当前版本：409/40901。
- 回滚版本也写快照 → **可再回滚**；但受快照上限约束（超限标 `skipped_oversize`、不可再回滚，确认框须提示「若数据量超出快照上限，本次回滚生成的新版本将不能再次回滚」，ARCH §3 / R2 / PROD-DATA-C6）。
- **不幂等**：回滚成功后再重试会因 `base_version` 已前进得 409（乐观锁兜底，无需 `client_batch_id`）。

### 4.5 operator 显示规则（归后端）

`operator_display` 由 Python 统一计算，前端只显示（PRODUCT §5.1 / 裁定 B17；优先级从高到低）：

| 优先级 | 条件 | 显示 |
|---|---|---|
| 1 | `kind='seed'` 或 `operator ∈ {seed, system}` | 「系统（种子）」 |
| 2 | `kind='ent'` 或 `operator='py'`，且 operator 不是真实用户名 | 「系统（历史）」 |
| 3 | `operator` ∈ {空串, `unknown`, `null`}（不区分大小写） | 「未知」 |
| 4 | `kind='ent'` 但 `operator` 是真实用户名 | 用户名（可后缀「（历史）」，不得被 kind 掩盖） |
| 5 | 其余 | 原样 `operator` |

- `unknown` 是 as-built 默认值（`routes:755`），必须归「未知」，不能直出英文；`py` 是 as-built 发布写死值（`routes:844`），归「系统（历史）」。
- 列表、详情、审计区、悬浮提示**一律显示 `operator_display`**，不直出 `operator` 原值；`py` / `unknown` 由后端映射为中文（见上表）。版本类型列说「是什么」（保存/回滚/种子/历史版本），操作人列说「谁」，避免两列都写「历史」。
- 历史版本 `operator` 缺失时详情加注「历史版本未记录操作人」，不推测姓名。
- 保存的 `operator` 取 `change_set.operator`；回滚取 display 注入的请求 operator（DATA-API-C3 / API-DATA-C3）。新保存不再写 `py`。

## 5. 既有读端点增量

### 5.1 `GET …/current`（R2）

在既有 `{nodes[], base_version, projection_status, schema_ready}`（`routes:348–414`）上**只追加**，不改已有字段：

- **顶层新增 `tech_edges[]`**（API-C11）：只回 `graph_tech_edge.status='active'` 的行，**不并入 `node.edges`**（否则 ENT 页会把技术点间边当实体关系映射，`FeApi:152–171` 的 `toRelation`）：

```json
{ "id": 123, "src": 12, "dst": 34, "rel_type": "依赖",
  "strength_manual": 7.5, "time_range": { "from": 2022, "to": 2024 },
  "source": "manual", "status": "active" }
```

| 字段 | 语义 |
|---|---|
| `id` | `graph_tech_edge.edge_id` 主键（int64 / JSON number；Java 侧 Long），`delete_edge` 的入参 |
| `src` / `dst` | `technology_master.technology_id`（int64 / JSON number；有向），**与 `nodes[].id`（string，存量可能是 VID 原串）不是同一命名空间**；前端须用 `nodes[].technology_id` 做 int→节点映射，禁止拿 `src/dst` 与 `nodes[].id` 直接比较（ALGO-API-C8 / 裁定 B7） |
| `rel_type` | 人工边为中文三枚举；种子边为 Nebula 英文原码（`KNOWLEDGE_DEPENDENCY` 等），**不映射**；`rel_code` 保留在库内供过滤/审计，**不出参**（裁定 B4） |
| `strength_manual` | 人工强度，可为 null；`strength_auto` **不出参**（裁定 B9 / API-DATA-C15） |
| `time_range` | 人工边 `{from:int,to:int}` 或省略；种子边允许 `{from:int,to:null}` 或整体省略（**不补 `to`**，裁定 B14 / DATA-API-C3） |
| `source` | `manual` / `auto`（auto = 存量种子边，前端标「存量」） |
| `status` | 恒 `active`（只回 active，保留字段便于前端判别） |

- **节点新增 `layout`**：由 **`graph_entity_node.layout_x/layout_y`** 组装 `"layout": {"x":312.5,"y":180.0}`；两列为 NULL（种子点）时输出 `"layout": null`（DATA-API-C1）。
- 存量英文字典由前端显示层处理（§5.3），接口只给原码 + `source`。

### 5.2 `GET …/nodes/{technology_id}/impact`（35-3）

在既有 `{edge_count, entity_link_count, snapshot_refs}`（`routes:511–522`）上追加两字段（API-C12）：

| 字段 | 类型 | 语义 |
|---|---|---|
| `tech_edge_count` | int | 工作集内 `WHERE status='active' AND (src=? OR dst=?)` 的行数；**只数 active、两个方向都算**（裁定 B15 / DATA-METRIC-C3） |
| `panorama_hidden_relation_count` | int \| null | 全景中将隐藏的存量关系数：**entan 用自有 Nebula 只读会话**（`entan.common.nebula`），会话内**显式 `USE demo_gkx_chain`**（用 `session(use_space=False)` 建会话后手动 USE），**断言查询目标为字面量 `demo_gkx_chain`（或 `GKX_CHAIN_NEBULA_SPACE`，须以 `demo_gkx_` 开头）**，非该 space 直接拒；**不得对 entan 配置的默认 space 做断言**（其默认是 `entan`）；只做 MATCH/计数（无向、`evidence_level IN [HIGH,MEDIUM]`，对齐 `read:265–282`）。按该点在 Nebula 的关联数计（gross，非扣减后净数，DATA-METRIC-S5）；超时/失败返回 **null**（不用 0 冒充），不挡删除。**不得引用 chainan / `chain_space()`**（arch 未打包进 entan 镜像，裁定 B3 / ARCH-API-C3 / ALGO-API-C2） |
| `edge_count` / `entity_link_count` / `snapshot_refs` | 不变 | 实体边 / 人工挂接 / 快照引用，沿用 ENT |

- 技术点不存在 → 404/40401（沿用 `routes:517–519`）。
- 以上四项计数并入 DN-A03-09 操作回执计数建议豁免（34–40 范围九类，裁定 A8 / ARCH §9-5）。
- **35-3 确认框文案**（PROD-API-C11；ARCH §6 已同步为四项）统一为：「将同时删除该节点的全部关系：技术点关系 N 条、实体关系 E 条、实体挂接 L 条；全景图中将隐藏存量关系 M 条」。字段对照：`tech_edge_count`→技术点关系（N）、`edge_count`→实体关系（E）、`entity_link_count`→实体挂接（L）、`panorama_hidden_relation_count`→全景隐藏存量关系（M）。注明工作集与全景是两个视图、可能重叠；`M=null` 显示「无法统计」。

### 5.3 全景读图出口增量（algo-py → display 透传，卡 1B）

`lumen_common/algorithms/tech_graph_read.py` 的 `_read` 两条 return 分支都叠加（`read:556–570`）；`overlay_factory=None` 时关闭叠加、不输出 `overlay`、与今天逐字节一致（ALGO-C9）。合并在 Java `SituationPanoramaService` 里透传（§6.2）。

**改写后的总原则**（ALGO-API-C4）：**叠加关闭时与今天逐字节一致；叠加开启时只改集合（按 ARCH §4.2：已删点/已删存量边/含删点的路径被移除，关键词补读可能新增存量点，合并后按 200 截断并置 `truncated.nodes`）并追加字段，不改存量行已有字段值**。不再表述为「只追加、不改已有字段」。

| 位置 | 追加字段 | 说明 |
|---|---|---|
| 顶层 | `overlay: {"status":"ok"}` / `{"status":"unavailable"}` | 叠加失败降级为 Nebula 原结果 + `unavailable`，不整页 503（ARCH §4.3）；Java `assemble` 须原样放进 result（现只保留 7 键会丢弃，`PanoSvc:210–217`，API-C4 / ALGO-C3） |
| `nodes[]` | `category`、`importance` | 主表值**非空才覆盖**对应展示字段，空则保留 Nebula 原值（ALGO-C6）；`importance` 为 null 时不输出。**字段名差异**：全景出口是 `importance`（ARCH §4.2 定名），`/current` 与主表是 `importance_level`；前端不得混用，也不得把 `importance` 回写主表列（ALGO-API-C9） |
| `relations[]`（人工边） | `origin:"manual"`、`strengthManual`、`timeRange:{from,to}` | **保持 `source`/`target` 为端点 id 不变**（不得写成 `source:"manual"`，否则 Java 会按端点删边，API-C5 / ALGO-C1）；人工强度**不填 `weight`、不填 `strength`、不填 `year`**（不进 timeline、不计入 `weighted_degree`，ALGO-C11 选②） |
| `relations[]`（人工边） | **禁止输出** `evidenceLevel` 及任何 `evidence`/`evidenceType` 字段 | 人工边不得携带证据等级（否则 Java `lowEvidence` 会误删边，也等于伪造证据等级，ALGO-API-C1 / 裁定 B6）；人工边也不进入 35-3 `panorama_hidden_relation_count` 统计 |
| `relations[]`（人工边 id） | `id = "tech_manual:{edge_id}"` | 不复用 `tech_rel:…` 前缀，避免撞号 |
| 节点 id | 新建点 `id = "tm:{technology_id}"` | 存量点沿用 `technology_node_id` 或 VID 原串（`read:181`）；选中新建点时请求 `technology_node_id=tm:{id}`；**选中已软删点**返回空图并置 `emptyReason=GRAPH_EMPTY`（不 404、不回落默认点，ALGO-API-C6） |
| `relationTypeOptions` | 叠加开启后可能同时含存量英文码与人工三中文枚举 | 只用于图例/筛选，**不得作为 `add_edge.rel_type` 的下拉数据源**（`rel_type` 仍固定三枚举，ALGO-API-C5）；`factorItems` 不受影响 |
| `relations[]`（存量边，PROD-C9） | 前端显示层把英文码映射为中文（`KNOWLEDGE_DEPENDENCY`→知识依赖 / `PATENT_CONVERGENCE`→专利趋同 / `CO_EVOLUTION`→协同演进 / `WEAK_DEPENDENCY`→弱依赖 / 未知→「其他关系」），加「存量」标注 | 字典真源 `TrackingController.relationZh:185–193`；**不动 `relationType` 原值**，只做显示 |
| 已删存量边过滤 | 由内部按 `(端点无序对, rel_code)` 匹配 Nebula；`rel_code` 为 NULL 时回退 `rel_type`；人工行不参与存量边过滤 | API 不返回 `rel_code`（裁定 B4 / ALGO-DATA-C5）；该规则归 ALGO 实现，接口契约只保证人工边输出 `origin` 与 `tech_manual:*` id |

- 人工边的端点节点必须并进 `nodes`（存量端点补读、新端点从主表建），否则 Java `SituationPanoramaService:184–196` 会因端点不在 nodes 删边（ALGO-C2）。
- `overlay.status=unavailable` 时前端给非阻塞提示「人工维护的改动暂未显示，请稍后刷新」（ARCH §4.3 / P4 已拍板）。
- 已删点/已删存量边/路径过滤、关键词新点匹配、先合并再截断 200 等排序规则归 ALGO 实现（ARCH §4.2），不影响本册字段契约。

## 6. 三层端点挂法与写守卫

### 6.1 端点挂法总表（API-C2；路径参数统一 `{version_id}` / `{change_set_id}`）

| 能力 | display（对外 `/display/v1/situation/maintain-ent/graph/**`；服务内 `/v1/...`） | topic（内部 `/topic/v1/tech/graph/**`） | entan-py（`/internal/v1/sci/tech/graph/**`） |
|---|---|---|---|
| 提交 / 校验 / 发布 | `POST /changes`、`POST /changes:validate`、`POST /changes/{change_set_id}/publish`（**加 body**） | 同名 | 同名 |
| 现状读 / 影响 | `GET /current`、`GET /nodes/{technology_id}/impact`（**加字段**） | 已有 | 已有，加字段 |
| 版本列表 / 详情 | `GET /versions`、`GET /versions/{version_id}`（新） | 新 | 新 |
| 回滚预览 / 回滚 | `POST /versions/{version_id}/rollback:preview`、`POST /versions/{version_id}/rollback`（新） | 新 | 新 |

- 每个新端点要动**五处**：display controller + display Feign + topic controller + topic Feign + Python 路由（ARCH §6.1）。现有 `DispFeign:21–63`、`TopicFeign:27–72`、`routes`（`grep @router` 仅 9 条）均无 versions/rollback。
- 复用既有前缀，不新开平行资源（审稿硬清单「是否复用已有路径」）。
- `TechGraphMaintainControllerTest` 里断言「add_node / add_edge / delete_edge → 400」的用例（`TechGraphMaintainControllerTest.java:69–78`）改成正向透传断言（API-C15）。

### 6.2 Java 全景门面改动（`SituationPanoramaService`）

- `PanoSvc.assemble` 现只放 7 个顶层键（`PanoSvc:210–217`，`218–227` 为 `truncated`/`emptyReason`），需**原样透传 `overlay`**（一行级改动，不碰 Controller / Adapter）；节点/关系追加字段本就能穿过 `maps()`/`normalizeRelation`，只需单测覆盖（API-C4 / ALGO-C3）。
- 未选点时先 `restrict` 再 `cap(200)`、选中时 `keepThenCap`：新建点已由 Python 排在前面/端点并入，按 ARCH §4.4 处理；学科子域筛选下不显示新建点（已知限制，§4.4-3）。本册不改这些规则，只要求 `overlay` 不被丢弃。

### 6.3 写守卫与 operator 注入

- display `relayWrite`（`DispCtrl:106–112`）覆盖以下 **POST 写/半写**端点：
  `POST /changes`、`POST /changes:validate`、`POST /changes/{change_set_id}/publish`、`POST /versions/{version_id}/rollback:preview`、`POST /versions/{version_id}/rollback`。
  （rollback 与 preview 都是 POST，统一走登录门槛；GET 版本列表/详情走 `relay`，允许匿名只读——若后续要求登录再收。）
- **operator 注入点**：display controller 的 `relayWrite` 路径，对 `changes`、`publish`、`rollback` 三个落审计的写请求，用 `SecurityUtils.getUser().getUsername()` 覆盖 body.operator；`publish`/`rollback` 原 body 可能为空，display 需**合成 body** 再转发。`validate` 不落 operator。
- topic / Python 不再单独鉴权（沿 `@Inner` / `@NoToken` 内部轨）；Python 版本行 operator 取 change_set.operator（保存）或请求 operator（回滚，裁定 B17）。

## 7. 错误码全表

码位沿用 ENT 的 `EnvelopeError`（`code//100` 映射 HTTP，`routes:70–85`）。**50301 随单事务退役**；`EnvelopeError` 文档串同步（R3）。**50303 为 ARCH §7 增补，已由监管人 2026-11-13 拍板（裁定 A5），仅 Java 层使用。**

| HTTP / code | 场景 | 触发层 |
|---|---|---|
| 400 / `40001` | op 枚举外；缺 `base_version`；缺 `client_op_id`；`ops` 为空或 >50；`add_edge` 的 `rel_type` 不在三枚举；端点引用对象形状错（既非 `technology_id` 也非 `client_node_id`、或两者都给）；`layout` 非数字/越界；`label` >128；`client_batch_id` >64 | topic 本地校验 + Python |
| 401 / `40101` | 未登录写操作（`gkxlumen.maintain.write-require-login=true`） | display `relayWrite` |
| 404 / `40401` | change_set 不存在；version 不存在；impact 的 technology_id 不存在 | Python |
| 409 / `40901` | `base_version` 不符（附 `data.current_version`）；取锁超时「他人正在保存」；发布时 `graph_tech_edge` 撞 active 唯一键 1062（附当前版本，整笔回滚）；发布时 change_set 已是 published 但**提供了不同 batch**；change_set 状态 rejected 再发布；提交命中同批次但 `ops` 不同或批次已 rejected；死锁/锁等待超时（MySQL 1213/1205）；回滚无快照、目标即当前版本 | Python / Java |
| 422 / `42201` | 名称重名（新建/改名，只查 active；1062 落此码）；关系重复（active 同键）；端点不存在或非 active；`client_node_id` 引用不到；自环；强度越界；时间范围越界或 from>to；`importance_level` 枚举外；`patch` 为空；`category` 为空或 >64 | Python `_validate_structure` |
| 500 / `50001` | 其他 SQL 异常 / 内部错误（整笔回滚，草稿保留） | Python |
| 503 / `50302` | 工作集表或列缺失（1146/1054/1049）。**例外**：`graph_entity_member` 缺表或缺列仍按 ENT 兼容路径静默跳过（`routes:225–235`、`:269–278`，R1），不报 50302 | Python |
| 503 / `50303` | **下游不可达**（display/topic Feign 连不上或超时）。Java 两处 `relayStatus` 现按 `status*100+1` 会产出 50301，冻结改为显式 `50303`，避免与退役码撞车（裁定 A5 / §14） | display / topic |
| ~~503 / 50301~~ | **退役**：单事务后不再有「投影中」。任何层不得再产生 50301 | — |

前端配合（PROD-API-C1/C3/C4/C6/C7/C13 / 裁定 B19；归 FE-TS-10D）：

| 场景 | 用户可见文案 / 行为 |
|---|---|
| 422 逐条 | 对应草稿项标红，草稿保留；直接显示 `errors[].msg` 中文；名称重复补「名称已存在（不区分大小写），请换一个」；自环/端点不存在/时间越界给字段级中文 |
| 409 基线过期 | 弹窗「他人已保存了新版本 v{n}」，草稿重放 + 失效项列出，两个动作「丢弃失效项并继续 / 放弃全部草稿」 |
| 409 取锁超时 / 死锁 | 「他人正在保存，请稍后重试」，草稿保留 |
| 409 change_set rejected / 不存在 | 「本次改动已失效，请刷新后重试」 |
| 401 | 写控件禁用 + 顶部提示「登录后可使用编辑功能」；草稿本地保留 |
| 50303 | 「服务暂不可用，请稍后重试」；草稿保留；不得显示 50303 |
| 50302 | 「维护功能暂不可用，请联系管理员」；**不写「可重试」**（缺表重试不会修复） |
| 50001 | 「保存失败，改动未丢失，可重试」 |
| 网络超时 | 「网络超时，改动未保存，可重试」（区别于 409） |
| 保存成功 | 「保存成功：N 项已生效，M 项未生效」；`M>0` 可展开中文原因；不出现 `results`/`failed_items`/`succeeded` 字段名；历史 `results:null` 显示「该版本未记录逐条结果」，不当 0 项 |
| 单批 50 条 | `N=50` 时「本批已满，请保存图谱后继续」+「保存后继续」；N 与 39-1 同口径（op 条数） |
| 历史 `stats` | `{"ops":N}`→「N 项改动」；旧扁平→「技术点 +a/−b · 关系 +c/−d」；`{}`/`NULL`→「—」+ tooltip「历史版本未记录分组计数」；缺组不补 0 |
| 回滚确认 | 标题「回滚到「{label}」（v{n}）？」；正文必须同时说「之后新增的将移除、之后删除的将恢复、之后修改的将还原」；分组明细只显示非零组；`added=恢复`、`removed=移除`、`updated=还原` 不得译反；`rollbackable=false` 按钮置灰 + 原因；当前版本不提供回滚 |
| 35-3 确认框 | 「将同时删除该节点的全部关系：技术点关系 N 条、实体关系 E 条、实体挂接 L 条；全景图中将隐藏存量关系 M 条」；注明工作集与全景是两个视图、可能重叠；`M=null`→「无法统计」 |
| 空态 / 加载态 | `N=0`「保存图谱」禁用 + tooltip「没有待保存的改动」；版本列表空「暂无版本记录」；工作集空「暂无技术点，右键或点击『添加节点』开始」；保存中禁用编辑；骨架屏 |
| 人工/存量标识 | 36-3 弹窗「关系强度（人工）」；画布常驻只显示类型，强度与「人工」放悬浮/详情；种子边标「存量」、强度若显示标「存量强度（只读）」；不挂 ⓘ；界面不出现 `strength_manual`/`strength_auto` 等字段名 |

## 8. 对 FE-TS-10A as-built 的差异与类型改动

### 8.1 接口差异（接线单输入）

| 项 | as-built（FE-TS-10A 演示态） | 本册契约 | 接线动作 |
|---|---|---|---|
| op 枚举 | `GraphOp` 仅 7（`FeTypes:90–102`） | 10 op | 扩联合类型 |
| 新增节点 | 页面内存 `createInitialGraphMaintainState` 4 节点（`FeGraph:252–288`） | `add_node` → `changes` → `publish` | fe api 层新增 builder |
| 关系类型 | `GRAPH_RELATION_TYPES` 含「转化/关联」（`FeGraph:233`） | 封闭三项 | 删「转化/关联」；mock 种子 `maintain-r3` 的「转化」改「促进」 |
| 关系编辑 | `updateGraphMaintainRelation`（超需规，`FeGraph:427`） | 不做 | 移除入口 |
| 坐标 | 0–100 百分比（`FeModel:89`） | 世界坐标浮点；列 `layout_x/layout_y` | 改注释 + 迁移 mock 种子 |
| 保存 | 只 `changes`+`publish`，无批次 id | `client_batch_id` 选填（建议客户端生成以享幂等）+ publish body `{label,client_batch_id}` | fe api 层改造 |
| 503 处理 | `code===50301` 视为投影中（`FeApi:372–374`） | 50301 退役；50303=下游不可达 | 删 50301 分支 |
| 版本 | 页面内存 `versions`（`FeGraph:283–296`） | 版本四端点 | 新面板 |
| 当前图 | 只读 `nodes[].edges`（实体边） | 另读顶层 `tech_edges[]` + `node.layout` | 不并入 `node.edges` |
| 分类 / 重要性 | 本地字段 | `category` 中文名（维表下拉、可手填）；`importance_level` 空显示「未设置」 | 表单改造（FE-TS-10D） |

### 8.2 前端类型要改（`src/types/maintainEnt.ts` / `src/types/maintain.ts`）

- `GraphOp` 增三支：

```ts
| { op: 'add_node'; client_node_id: string; name_cn: string; category: string;
    description?: string | null; importance_level?: '高'|'中'|'低' | null;
    layout: { x: number; y: number }; client_op_id: string }
| { op: 'add_edge'; src: {technology_id:number} | {client_node_id:string};
    dst: {technology_id:number} | {client_node_id:string};
    rel_type: '包含'|'依赖'|'促进'; strength_manual: number;
    time_range?: { from: number; to: number } | null; client_op_id: string }
| { op: 'delete_edge'; edge_id: number; client_op_id: string }
```

- `ServerGraphCurrent` 加 `tech_edges: ServerTechEdge[]`；`ServerGraphNode` 加 `layout?: {x:number;y:number} | null`。新类型 `ServerTechEdge = { id:number; src:number; dst:number; rel_type:string; strength_manual:number|null; time_range?: {from:number; to:number|null} | null; source:'auto'|'manual'; status:'active' }`。
- `ValidateSummary` 加 `add_node/add_edge/delete_edge`。
- `PublishResult`：`stats` 改为 §3.4 分组结构（含 `tech_edges.updated`；兼容旧四种形状），`results: {...} | null`，新增 `kind?`、`node_id_map?: Record<string,number>`。
- 新类型：`GraphVersion`（含 `is_current`）、`GraphVersionDetail`（含 `changes_total`/`summary`/`src_name`/`dst_name`）、`RollbackPreview`（含 `counts`/`rollbackable`/`snapshot_status`）、`RollbackResult`。
- `RelationPatch.strength` 口径 0–10；FE 弹窗由 `min:0,max:1`（`GraphMaintainEditor.vue:100`）改 0–10、步长 0.1（PROD-API-C8）。
- `GraphMaintainNode.x/y` 注释由「画布百分比 0-100」改为「画布世界坐标（浮点 px）」；`GraphMaintainRelation.timeRange` 改选填。

## 9. 对 ENT-API 的追记（共享发布路径的变化）

> 本节只写在 GRAPH 册；签收后由协调方落到 `TS-L2-M10-ENT-API.md`，并在 `会签/TS-L2-M10-ENT-SIGNOFF-API.md` 追加由原审稿身份确认的一节。**确认前不派 PY-IMPL（含单测）**（ARCH §10 第 3 行 / N5）。

| # | ENT 契约变化 | 对 ENT 前端（FE-TS-10C）影响 |
|---|---|---|
| E1 | `publish` 增可选 body `{label?, client_batch_id?}`，回执增 `node_id_map`（ENT 为 `{}`）与 `results`（可空） | 调用可继续不带 body；若要显示版本说明则传 `label`。`node_id_map` 可忽略 |
| E2 | 发布/回滚改**单事务 + 串行锁**，`projection_status` 恒 `ok`，不再产生 pending | 不再出现 50301；`projection_status` 判断可保留但恒 ok |
| E3 | `changes` 增 `client_batch_id`（**选填、服务端可生成**，裁定 A7）；同批重试回原回执；`publish` 可选回传同一值 | **ENT 页不强制改**；建议后续补上以享重试幂等 |
| E4 | `graph_version` 增 `kind` / `snapshot_status`；版本四端点对 ENT 版本同样可用 | 可显示版本类型/可回滚原因；详情按 `version_id` |
| E5 | 技术点名称唯一性只约束 active（替换 `uk_name_cn`）；`update_node` 改名撞 active 名 → 422；软删后可同名重建 | ENT 页若改名，需按 422 提示 |
| E6 | `/current` 追加顶层 `tech_edges[]`、节点 `layout`，**不并入 `node.edges`** | 现 `toPanorama` 忽略未知顶层键，契约上无需改；**禁止**把 `tech_edges` 当实体关系映射 |
| E7 | `delete_node` 级联同时软删该点的 `graph_tech_edge` 行，并逐条记 `tech_edge` 删除日志 | 无（ENT 页不发 delete_node） |
| E8 | `graph_entity_member` 缺表/缺列仍静默跳过（1146/1054），不报 50302 | 无 |
| E9 | 删除 `_project_nebula` 与 `GKX_NEBULA_MAINTAIN_SPACE`，本链不写 Nebula | 无（线上本就未配置） |
| E10 | 50301 退役；Java 下游不可达改 **50303**（监管人 A5 已批） | `FeApi:372–374` 的 50301 分支删除；50303 走通用失败提示 |
| E11 | **ENT 共用单测更新**：`SituationMaintainEntControllerTest:49`（50301 断言→50303）、`:70`（`publish("cs-1")` 签名加 body）；`TechGraphMaintainControllerTest:72`（add_node/add_edge/delete_edge 由 400 改放行）、`:129`/`:137`/`:149`（50301 断言）、`:135`（publish 签名）；`PanoramaReadAssemblyTest` 补 `overlay` 与键集断言 | 进 CI 前必须同步改，否则改签名/码位会卡流水线；闸门含单测 |
| E12 | **`impact` 新增两字段**：`tech_edge_count`（工作集 active 双向）与 `panorama_hidden_relation_count`（entan 自有 Nebula 只读会话 + 显式 `USE demo_gkx_chain`，失败 `null`） | 无（ENT 页不调 impact）；新增 Nebula 只读依赖需在 ENT 追认 |
| E13 | **版本 operator 署名变化**：保存取 `change_set.operator`（display 注入用户名），回滚取请求 operator；历史行仍 `py`/`unknown`；`operator_display` 规则见 §4.5 | 版本列表/详情/审计区/悬浮提示只显示 `operator_display`，不直出原值 |
| E14 | **`stats` 结构**：新版本统一 §3.4 分组键；历史 ENT 版本保留旧四形状、不回填 | FE-TS-10C 若展示改动计数，需兼容四种旧形状（缺组不补 0） |
| E15 | **快照 payload 扩表/扩列**：新增 `graph_tech_edge`、`layout_x/layout_y`，并带 `schema_version`；`technology_master` 还原排除生成列 `name_cn_active` 与 `updated_at` | 无（DATA/ENT-DATA 追认项） |

**FE-TS-10C 结论**：不强制新增 `client_batch_id`（裁定 A7）；仅随共享 api 模块做两处清理——移除 50301 分支、`publish` 支持空 body。若版本列表展示计数，需兼容历史四种 `stats` 形状。其余字段增量可忽略（`tech_edges`/`layout` 不并入 `node.edges`）。

## 10. 会签关注点（已按裁定单收口）

| # | 关注点 | 最终口径 | 依据 |
|---|---|---|---|
| Q1 | `add_node.category` 是否强制 `dim_tech_domain` 外键 | **维表下拉、空则手填；存中文名；只校验非空+≤64，不做外键** | 裁定 A3 / PROD §5.2 / DATA-API-S8 |
| Q2 | `update_node` 是否接受 `layout` | 不收（节点拖拽禁用，仅 add_node 落点）；要做拖拽持久化另加字段升版 | 裁定单未翻案 / DATA 意见 2 |
| Q3 | `importance_level` 省略写 NULL 还是吃默认「中」 | 写 NULL；`update_node` 传 null 表示清除 | ALGO-C6 / DATA-API-S3 |
| Q4 | 强度/时间口径 | 强度 0–10 步长 0.01（UI 0.1）；时间**选填**，填则 1900–2100、from≤to；FE 负责换算 | 裁定 A6 / PROD-API-C8 |
| Q5 | 50301 退役后 Java 下游不可达用 50303 | **新增 `50303`，仅 Java 层；ARCH §7 增补，监管人已批** | 裁定 A5 |
| Q6 | `operator_display` 归后端计算 | 见 §4.5（含 `unknown` 与真实用户名优先级） | 裁定 B17 / PROD §5.1 |
| Q7 | 历史版本 `stats` 旧形状 | **不回填**；原样返回、缺组不补 0；前端兼容四种形状 | 裁定 B1 / DATA-API-S6 |
| Q8 | `delete_edge` 只收 `edge_id` | 人工边与种子边统一按主键删；仅工作集边可删 | 裁定 B4 / ALGO-API-C7 |

## 11. 需规覆盖（接口侧）

| 功能点 | 接口能力 | 落点 |
|---|---|---|
| 34-3/34-4/34-5 | `add_node`（名称/分类/描述/重要性 + `layout` + `client_node_id`）；发布回执 `node_id_map` | §2.1、§2.5 |
| 35-3/35-4 | `delete_node`（沿用）+ `impact` 增 `tech_edge_count`/`panorama_hidden_relation_count`；`delete_node` 级联 `graph_tech_edge` | §5.2、§9-E7 |
| 36-3/36-4 | `add_edge`（三枚举 + 强度 + 时间范围选填 + 有向）；重复 422 | §2.2 |
| 37-3 | `delete_edge`（软删、保留两端节点、仅工作集边） | §2.3 |
| 38-2/38-3 | `update_node`（4 字段取值域 + 改名查重 422 + 等级可清空） | §2.4 |
| 39-x | 前端草稿栈；后端仅 `change_log` 追溯（无新端点） | §4.2 |
| 40-1/40-2/40-3/40-4 | `changes`+`publish`（`label`/`client_batch_id`）；`versions`/`versions/{version_id}`/`rollback:preview`/`rollback` | §3、§4 |

## 12. 不做

- 不写实现代码；不返内存 mock；不新造 `metric_id`（ARCH §9）。
- 不做关系属性编辑（`updateGraphMaintainRelation` 属超需规，移除）、不做节点拖拽持久化、不做技术点合并（ARCH §8）。
- 不把种子边英文码映射成三枚举（只做前端显示字典）；不返回 `rel_code` / `strength_auto`。
- 不写 Nebula；不含投影 pending / `reproject` 端点（单事务后无 pending）。
- 不做审批流引擎（change_set 的 approved 状态继续不用）。
- 不改 ENT 已冻结的 5 个实体类 op 与 R1 推荐形状。

## 13. 会签关注点之外的事实修正

- `routes` 现无 versions/rollback 路由（`grep @router` 仅 9 条），需新增；`_object_type`/`_object_id` 现无新 op（`routes:885–902`）。
- `DispCtrl`/`DispFeign` 现无 versions/rollback 方法（`DispCtrl:52–103`、`DispFeign:21–63`）。
- `PanoSvc.assemble` 只放 7 键（`PanoSvc:210–217`），`overlay` 会被丢，须透传。
- `FeApi` 的 50301 分支（`FeApi:372–374`）需随退役删除。
- 前端弹窗强度 `min:0,max:1`（`GraphMaintainEditor.vue:100`）与 ENT 0–10 不一致，接 0–10。
- as-built 历史 `stats` 至少四种形状：`{"ops":N}`（`routes:844`）、旧扁平四键（`routes:852–858`）、`{}`、`NULL`（PROD §5.3）。

## 14. 会签回应

> 逐条对应 `TS-L2-M10-GRAPH-L2-SIGNOFF-{ARCH,DATA,ALGO,PRODUCT}.md` 的 API 条件、`TS-L2-M10-GRAPH-L2-SIGNOFF-API.md` 的「API 册自查项」与裁定单。**全部采纳，无「不采纳」条目**；与裁定单冲突的一律以裁定单为准（尤其 A3/A5/A6/A7、B1/B3/B4/B11/B12/B13/B16/B17/B18/B19）。

### 14.1 架构（ARCH-API）

| 编号 | 结论 | 改在哪节 |
|---|---|---|
| ARCH-API-C1 | 采纳：坐标列改 `layout_x/layout_y`，主表权威、ADS 镜像 | §2.1、§5.1 |
| ARCH-API-C2 | 采纳：`stats` 唯一嵌套分组；publish 幂等限定「同 batch/未传才幂等，不同 batch→409」 | §3.3、§3.4、§7 |
| ARCH-API-C3 | 采纳：35-3 改 entan 自有 Nebula 只读会话 + 显式 `USE demo_gkx_chain`，删 chainan 引用 | §5.2 |
| ARCH-API-C4 | 采纳：§9 增 E11「ENT 共用单测更新」，含具体测试行号，确认前不派 PY-IMPL（含单测） | §9-E11 |
| ARCH-API-C5（建议） | 采纳：50303 标注「ARCH §7 增补」，并按裁定 A5 记已拍板 | §7、§10-Q5 |
| ARCH-API-C6（建议） | 采纳：路径参数统一 `{version_id}` / `{change_set_id}` | §4、§6.1、§6.3 |

### 14.2 数据（DATA-API）

| 编号 | 结论 | 改在哪节 |
|---|---|---|
| DATA-API-C1 | 采纳：`layout_x/layout_y`，`/current.layout` 由 ADS 列组装，种子 `null` | §2.1、§5.1 |
| DATA-API-C2 | 采纳：§3.4 为 `stats`/`counts` 唯一形状，DATA 扁平键废止；历史四种形状不回填 | §3.4、§4.1 |
| DATA-API-C3 | 采纳（受裁定 A6 约束）：人工边 `time_range` **选填**、填则 from/to 非空；种子边允许 `{from,to:null}`/省略 | §2.2、§5.1、§8.2 |
| DATA-API-S1 | 采纳：写死 `graph_version.publish_results`，回滚 `results` 同列持久化 | §3.3、§4.4 |
| DATA-API-S2 | 采纳：`id`/`src`/`dst` 标 int64（JSON number，Java Long） | §2.3、§5.1 |
| DATA-API-S3 | 采纳：`importance_level:null`=写 NULL（清除），省略=不改 | §2.4 |
| DATA-API-S4 | 采纳：submit 撞 1062 按 batch 重读并返回幂等回执；publish 1062→409 | §3.1、§7 |
| DATA-API-S5 | 采纳：`node_id_map` 只扫 `op='add_node'` 且 `after.client_node_id` 非空 | §2.5 |
| DATA-API-S6 | 采纳：冻结「DATA 不回填 stats」，Q7 写死 | §3.4、§10-Q7 |
| DATA-API-S7 | 采纳：复活仅命中同键人工行；种子英文码不经 add_edge 复活；复活 auto 行时 `strength_auto` 不动 | §2.2 |
| DATA-API-S8 | 采纳：`category` 落 `technology_master.category`（VARCHAR(64)），无 FK | §2.1 |
| DATA-API-S9 | 采纳：publish 提供 batch 且不符→409；未提供→忽略 | §3.3 |

### 14.3 算法（ALGO-API）

| 编号 | 结论 | 改在哪节 |
|---|---|---|
| ALGO-API-C1 | 采纳：人工边禁止输出 `evidenceLevel`/任何 evidence 字段、不填 `strength`、不计 `weighted_degree`、不进 hidden 计数 | §5.3 |
| ALGO-API-C2 | 采纳：35-3 改 entan Nebula 通道（同 ARCH-API-C3，裁定 B3） | §5.2 |
| ALGO-API-C3 | 采纳：§3.4 分组键为唯一口径，DATA 扁平键必须改 | §3.4 |
| ALGO-API-C4（建议） | 采纳：改写 §5.3 总原则「叠加关闭逐字节一致；开启只改集合+追加字段、不改存量值」 | §5.3 |
| ALGO-API-C5（建议） | 采纳：`relationTypeOptions` 只作图例/筛选，不驱动加边下拉 | §5.3 |
| ALGO-API-C6（建议） | 采纳：选中已删点返回空图 + `emptyReason=GRAPH_EMPTY`；选中新点按 `tm:{id}` | §5.3 |
| ALGO-API-C7（建议） | 采纳：`delete_edge` 仅工作集边；hidden 计数只服务删点确认框 | §2.3、§5.3 |
| ALGO-API-C8（建议） | 采纳：`src/dst` 与 `nodes[].id` 不同命名空间，用 `nodes[].technology_id` 映射 | §5.1 |
| ALGO-API-C9（建议） | 采纳：全景 `importance` vs 主表 `importance_level` 不得混用 | §5.3 |

### 14.4 产品（PROD-API）

| 编号 | 结论 | 改在哪节 |
|---|---|---|
| PROD-API-C1 | 采纳：kind/reason/分组/两种时态中文映射表，界面不出现原始码 | §4.1、§4.3、§7 |
| PROD-API-C2 | 采纳：版本详情增 `summary` 中文摘要与 `src_name`/`dst_name`；`object_type` 中文；历史行显示规则 | §4.2、§7 |
| PROD-API-C3 | 采纳：401/50303/50302/50001/404/409/50 条/422 的用户提示补齐 | §7 |
| PROD-API-C4 | 采纳：「保存成功：N 项已生效，M 项未生效」；未生效项可展开；`results:null` 文案 | §3.3、§7 |
| PROD-API-C5 | 采纳：`stats` 唯一形状（裁定 B1） | §3.4 |
| PROD-API-C6 | 采纳：历史四种 `stats` 显示规则；`before/after` 历史规则 | §3.4、§4.1、§4.2 |
| PROD-API-C7 | 采纳：36-3「关系强度（人工）」、画布悬浮/详情「人工」、种子「存量」、不挂 ⓘ、不出现字段名 | §5.1、§5.3、§7 |
| PROD-API-C8（建议） | 采纳：强度 UI 0–10/0.1（后端收 0.01）；时间范围**选填**（裁定 A6） | §2.2、§8.2 |
| PROD-API-C9（建议） | 采纳：`category` 维表下拉、可手填、存中文名；`importance_level` 空显示「未设置」 | §2.1、§2.4 |
| PROD-API-C10（建议） | 采纳：`is_current`、当前版本不回滚、`label`+v{n}、列表只显示 `operator_display`、`label` ≤128 | §4.1、§4.4 |
| PROD-API-C11 | 采纳：35-3 确认框列四项计数 + 视图说明 + `null`「无法统计」 | §5.2、§7 |
| PROD-API-C12（建议） | 采纳：版本详情 `changes_total` + `page/size` 分页 | §4.2 |
| PROD-API-C13（建议） | 采纳：空态/加载态/禁编辑文案 | §7 |

### 14.5 API 册自查项（L2-SIGNOFF-API §11）

| 项 | 结论 | 改在哪节 |
|---|---|---|
| §5.1 注明 `src/dst` 对应 `nodes[].technology_id` | 采纳 | §5.1 |
| §9 补 impact、operator 两条 ENT-API 追记 | 采纳（E12、E13） | §9 |
| 按 B12/C7 决定 `tech_edges` 是否加 `updated` | 采纳：加 `tech_edges.updated`（回滚差异可出现） | §3.4、§4.3、§8.2 |
| §3.3 补缺省 batch、rejected 的处理 | 采纳（结合裁定 A7/B11） | §3.1、§3.3、§7 |

### 14.6 裁定单 A 部分

| # | 结论 | 改在哪节 |
|---|---|---|
| A1 名称唯一键 | 采纳：只约束 active；删除既有唯一键由监管人执行前备份，无需数据平台 Owner 书面确认 | §2.4 |
| A3 分类 | 采纳：维表下拉、空则手填、存中文名、只校验非空+≤64 | §2.1 |
| A5 50303 | 采纳：仅 Java 层，ARCH §7 增补 | §7 |
| A6 时间范围选填 | 采纳 | §2.2 |
| A7 `client_batch_id` 可缺省 | 采纳：缺省服务端生成、不享重试幂等；ENT FE 不强制改 | §1、§3.1、§9-E3 |
| A8 DN-A03-09 扩到七类 | 采纳：§3.4、§5.2 按七类「建议豁免」表述，待 PM/数据 Lead 确认 | §3.4、§5.2 |
| A2 种子切片 / A4 快照阈值 | 不涉及接口契约，归 DATA/SEED 册；本册仅在 §5.1/§4.1 引用其结果（无接口字段变化） | — |

**v2.1 清理**：DATA-API-N1（§3.4 按 `kind` 定义 `stats`/`counts`）、PROD-API-C11（35-3 四项中文文案 + 视图说明 + `null`「无法统计」，§5.2/§7）、PROD N2（审计区/悬浮提示只显示 `operator_display`，§4.5/§9-E13）、ARCH 复核 N1（§5.2 断言查询目标为字面量 `demo_gkx_chain`，`session(use_space=False)` + 显式 `USE`，不对配置断言）、DATA 清理项（§4.1 `snapshot_status` 显示口径对齐 DATA §3.4）。

---

*起草：agent:api-agent · 2026-11-13 · v2（会签条件已回应）· 只读核对 as-built，未改 ENT 册 / 代码 / registry，未 git、未连库*
- v2.1 协调方补记（2026-11-13）：§3.4、§5.2 计数改为「34–40 范围九类」，与 METRIC 册一致（PROD 最终确认建议）。
