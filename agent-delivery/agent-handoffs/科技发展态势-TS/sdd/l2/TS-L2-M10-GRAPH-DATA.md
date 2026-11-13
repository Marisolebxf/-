# TS-L2-M10-GRAPH-DATA · 维护管理 · 维护技术图谱（34–40）· 数据落点

- 任务：`TS-L2-M10-GRAPH-DATA`
- 日期：2026-11-13
- 状态：**v2，会签条件已回应**
- 监管：`human:刘剑锋` · 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：全景序 34–40（本册是 `TS-L2-M10-ENT-DATA.md` 的**增量**，不重写 ENT）
- 上游：
  - `sdd/l2/TS-L2-M10-GRAPH-ARCH.md`（v2 四身份会签 + 2026-11-13 监管人 `human:刘剑锋` 签收）
  - **`sdd/l2/会签/TS-L2-M10-GRAPH-L2-裁定.md`（A1～A8 监管人拍板、B1～B20 跨稿统一口径；v2 以其为准）**
  - 二级会签单 `sdd/l2/会签/TS-L2-M10-GRAPH-L2-SIGNOFF-{ARCH,API,ALGO,PRODUCT}.md`（DATA 条件：ARCH-DATA-C1～C5、API-DATA-C1～C19、ALGO-DATA-C1～C12、PROD-DATA-C1～C8）
  - 一级会签单 `sdd/l2/会签/TS-L2-M10-GRAPH-SIGNOFF-{DATA,API,ALGO,PRODUCT}.md`（DATA-S1～S5、DATA-C1～C7、复核 N1～N5、补充复核 ①～③、API R4/R5、ALGO-N3、PRODUCT-N2）
  - 先例 `sdd/l2/TS-L2-M10-ENT-DATA.md`（已签收，本册增量）
  - 存储真源 `agent-delivery/data/data-design/storage/README.md`（§5 职责矩阵 / §5.1 Demo 结构合一 / §6 改表纪律）
  - 铁律 `.cursor/rules/00-team-constitution.mdc`、`architecture-baseline.md`（D9 / D12 / D18）、`data-lineage-policy.md`（D9 8 件套）
- as-built 核对（2026-11-13 读码，未连库）：
  - `repos/lumen-algo-py/vendor/entan-py/scripts/mysql/tech_graph_maintain.sql`（下称 **DDL**）、`tech_graph_maintain_v2_member.sql`
  - `repos/lumen-algo-py/vendor/entan-py/api/tech_graph_maintain_routes.py`（下称 **routes**）
  - `repos/lumen-algo-py/vendor/entan-py/scripts/seed_tech_graph_maintain.py`（下称 **seed**）
  - `repos/lumen-algo-py/lumen_common/algorithms/tech_graph_read.py`（下称 **read**）、`lumen_common/db.py`（下称 **db**）
  - 部署 env：`repos/lumen-algo-py/k8s/api.yaml`、`repos/lumen-svc-platform/helm/gkxlumen-platform/values.yaml`、`values-lumen.yaml`

本册只定存储面：表、列、键、索引、快照结构、事务写序、锁、种子灌入、库名一致性与 DDL 草案。op 形状与 DTO 归 `TS-L2-M10-GRAPH-API`；指标口径归 METRIC。**不执行任何 DDL、不连库、不跑脚本、不 git**；DDL 只写在稿里，执行人 = 监管人。

## 0. 结论与条目落点

**有条件可落，v2 已按裁定单与五身份条件回应。** 架构方向（新表 `graph_tech_edge`、名称唯一键只约束 active、快照每版一份、加锁单事务、整图回滚）在数据身份成立。v2 与 `TS-L2-M10-GRAPH-L2-裁定.md` 一致：A1 名称唯一键**不需**数据平台 Owner；A2 种子默认切片取 **#2「人工智能 / 大模型」**；A3 分类维表下拉、空则手填、演示清单见 §6.8；A4 快照阈值与每版保留；A7 `client_batch_id` 可缺省；B1 `stats` 改 API §3.4 分组 JSON；B4 保留 `rel_code`；B5 种子跳过中文码；B10/B11 1062 与幂等边界；B13 回滚整表还原；B16/B17 `kind`/`operator`；B18 ENT 追记。

**唯一不采纳**：`API-DATA-C10`（删除 `rel_code`）。理由见 §14——裁定 B4 明确保留 `rel_code` 并用于全景过滤已删存量边，API 不出参即可，不需要删列。其余 DATA 条件与建议均采纳或按裁定覆盖。

| 上游条目 | 落点 |
|---|---|
| 裁定 A1 / ARCH-DATA-C3 / API-DATA-C9 | §3.2、§5.4、§10、§12 |
| 裁定 A2 / PROD-DATA-C5 | §6.2 |
| 裁定 A3 / PROD-DATA-C4 | §6.3、§6.8 |
| 裁定 A4 / API-DATA-C16 | §4.2、§4.3、§8-G |
| 裁定 A6 / B14 / API-DATA-C14 | §2.1、§6.3 |
| 裁定 A7 / B11 / API-DATA-C4/C5 | §3.5、§5.5 |
| 裁定 B1 / ARCH-DATA-C1 / API-DATA-C1 / ALGO-DATA-C3 / PROD-DATA-C3 | §5.2、§6.3、§8-H |
| 裁定 B4 / ALGO-DATA-C5 / API-DATA-C10（不采纳删除） | §2.1、§2.3、§4.2 |
| 裁定 B5 / ALGO-DATA-C1/C4 | §6.1、§6.3 |
| 裁定 B7 / ARCH-DATA-C5 / API-DATA-C12 | §2.4、§12 |
| 裁定 B10 / API-DATA-C9 / ALGO-DATA-C12 | §5.4 |
| 裁定 B12 | §5.3、§7.6 |
| 裁定 B13 / API-DATA-C6/C7 / ALGO-DATA-C2 | §4.1、§5.3 |
| 裁定 B16 / API-DATA-C2 / ALGO-DATA-C9 | §3.4、§5.2、§5.3 |
| 裁定 B17 / API-DATA-C3 | §5.2、§5.3 |
| 裁定 B18 / ARCH-DATA-C2 / API-DATA-C8 | §11 |
| API-DATA-C13 / C18 / C19 / ALGO-DATA-C6/C7/C10/C11 / PROD-DATA-C1/C2/C6/C7/C8 | §2.3、§3.4、§4.1、§5.2、§5.3、§5.5、§6.1、§6.3、§6.4 |
| DATA-S1～S5、复核 N1～N5、补充复核 ①～③、API R4/R5、ALGO-N3、PRODUCT-N2 | 沿用 v1 落点，v2 微调 |

## 1. 本册定什么

| 项 | 裁定 |
|---|---|
| 新表 | `demo_gkxlumenx_ads.graph_tech_edge`：技术点↔技术点有向边，服务端自增主键，软删占唯一键 |
| 加列 | `technology_master` 坐标 + `name_cn_active` 生成列；`graph_entity_node` 坐标；`graph_version` 三列；`graph_change_set` 一列；`graph_change_log` 注释；`graph_version.stats` 注释 |
| 快照 | 每版发布 / 回滚在同一事务写全量快照（每版一份、按 `version_id` 保留、不裁剪），payload 带 `schema_version`，含软删行；超限在 INSERT 前预判并降级 |
| 事务 | publish / rollback 共用 `GET_LOCK('m10_graph_publish', 10)`，单事务覆盖全部写；1213/1205 → 409 |
| 种子 | `TS-L2-M10-GRAPH-SEED-L01`：Nebula `demo_gkx_chain` 诱导子图 ≤50 点 + 其间 `tech_rel`，**默认切片 #2「人工智能 / 大模型」**，写主表 / ADS node / `graph_tech_edge`，产 `kind=seed` 版本 + 快照 |
| 库名 | entan-py 与 algo-py 都解析到 `demo_gkxlumenx_*`，启动断言前缀并打印；D12 偏差记档 |
| 不写 | 不改 ENT-DATA 本体；不执行 DDL；不建表不灌数；不注册 metric_id |

## 2. 新表 `demo_gkxlumenx_ads.graph_tech_edge`

### 2.1 列定义（列级语义，非可执行 SQL）

| 列 | 类型 | 空 | 默认 | 语义 |
|---|---|---|---|---|
| `edge_id` | BIGINT AUTO_INCREMENT | N | — | 主键；`delete_edge` 参数、`graph_change_log.object_id` |
| `src` | BIGINT | N | — | 起点 `technology_master.technology_id`（内部主键） |
| `dst` | BIGINT | N | — | 终点 `technology_master.technology_id`（有向，A→B 与 B→A 是两条） |
| `rel_type` | VARCHAR(64) | N | — | 人工边 = `包含` / `依赖` / `促进`；种子边 = Nebula `tech_rel.relation_type` 英文原码。参与唯一键 |
| `rel_code` | VARCHAR(64) | Y | NULL | 种子边原关系码（auto 行）；人工边恒 NULL。**保留（裁定 B4）**：用于全景过滤已删存量边；不参与唯一键 / 指标 / 接口出参 |
| `strength_auto` | DECIMAL(10,4) | Y | NULL | auto 原强度（种子边取 `tech_rel.relation_confidence_score` 的组内 MAX）；**不出参、不进任何指标**（裁定 B9） |
| `strength_manual` | DECIMAL(10,4) | Y | NULL | 人工强度；永不进 `M_TECH_*` 公式（METRIC §3 边界） |
| `time_from` | INT | Y | NULL | 起始年，1900–2100；种子边取组内 `MIN(first_evidence_year)` |
| `time_to` | INT | Y | NULL | 结束年，1900–2100；**选填（裁定 A6/B14）**，种子边不补 `to`，保持 NULL |
| `source` | VARCHAR(8) | N | `'auto'` | `auto` / `manual`；命中人工复活时改 manual |
| `status` | VARCHAR(16) | N | `'active'` | `active` / `deleted`（软删） |
| `version_id` | BIGINT | N | — | 最后写入版本；发布 / 复活 / 回滚都改写为新版本 |
| `created_at` | DATETIME | N | CURRENT_TIMESTAMP | — |
| `updated_at` | DATETIME | N | CURRENT_TIMESTAMP ON UPDATE | — |

**`rel_type` / `rel_code`**：`rel_type` 是生效类型并参与唯一键（人工中文枚举与种子英文码因此不同键，闭合 DATA-N1③）；`rel_code` 只保存 auto 行原文，今天与 `rel_type` 同值，**用于全景过滤已删存量边**（§4.2），不参与唯一键、指标与接口出参。ARCH-DATA-C4 的「仅供追溯」按裁定 B4 扩为「追溯 + 已删存量边过滤」。

**人工边不带 `evidenceLevel`**（裁定 B6）：本表无该列；读侧人工边不得输出 `evidenceLevel` / `evidence` / `evidenceType`，也不得填 `weight` / `strength`，避免 Java `lowEvidence` 误删。

**auto / manual 可并存**（裁定 B8）：同一对点上的英文码 auto 边与中文枚举 manual 边是不同键，允许并存；界面分别标「存量」「人工」（PROD-API-C7 / B20），本册只保证键不冲突。

### 2.2 主键 / 唯一键 / 索引

| 键 | 定义 | 理由 |
|---|---|---|
| PK | `edge_id` | 自增，作 `delete_edge` 参数与 change_log 对象号 |
| UK | `uk_tech_edge (src, dst, rel_type)` | 业务唯一；**不含 `status`**，软删行仍占键（与 ARCH 拍板一致） |
| KEY | `idx_src (src)` | `delete_node` 级联、按起点查 |
| KEY | `idx_dst (dst)` | 级联、按终点查、无向叠加匹配 |
| KEY | `idx_status_source (status, source)` | 叠加 / `/current` 只扫 active、按 auto/manual 过滤 |
| KEY | `idx_version (version_id)` | 回滚 / 血缘核对 |

不使用外键（沿 ENT 先例，跨 DWD/ADS 同实例但不设 FK）。表放 **ADS**：ENT as-built 的人工实体边也只落 `ads.graph_entity_edge`（`routes:1056–1059`），沿用同一先例，不翻案。

### 2.3 软删行复活规则（DATA-N1、API-DATA-C13、API R4）

| 场景 | 行为 |
|---|---|
| `add_edge` 命中同 `(src,dst,rel_type)` 且 `status='active'` | 422 / 42201「关系已存在」 |
| `add_edge` 命中同键已删**人工行** | **UPDATE 复活**，不 INSERT：`status='active'`、`source='manual'`、写 `strength_manual` / `time_from` / `time_to`、`version_id=本次版本`；`strength_auto` 与 `rel_code` **保留不动**，不参与人工强度 |
| `add_edge` 命中已删**种子行** | **不可达**：种子行 `rel_type` 为英文码，`add_edge.rel_type` 只收三中文枚举，键不同，不会命中。auto 行的复活只发生在**回滚 / 种子重跑**，不经 `add_edge`（ALGO-DATA-C13） |
| `delete_edge` | 只改 `status='deleted'`，不物理删；不写墓碑拼接串（替代方案见 ARCH §2 删除行） |
| 节点删除级联 | `delete_node` 同时 `UPDATE … SET status='deleted'` 该点作为任一端的 `graph_tech_edge`；**同步写 `version_id`**，不物理删，便于快照与回滚 |
| 种子重跑命中已删行 | 不改 status / source（§6.5） |

`src/dst` 存内部 `technology_master.technology_id`（BIGINT），全景叠加时由读侧映射成全景 id（`technology_node_id`，空则 VID 原串，新建点 `tm:{technology_id}`）；删除过滤、快照还原、跨服务读都不再做二次命名空间换算。

### 2.4 端点与方向（裁定 B7/B8、API-DATA-C12）

- 有向：`(A,B,rel)` 与 `(B,A,rel)` 是两条不同键。人工 `add_edge` 保留用户指定方向（先点为起点）。
- 种子边：Nebula `read` 用无向 MATCH（`read:272`），`tech_rel` 无可靠方向；种子脚本按**端点无序对去重**，落库时规范化为 `src=min(technology_id)`、`dst=max(technology_id)`（DATA-N3）。人工边不套用此规范化。
- **出参类型**：`/current.tech_edges[].src/dst` 保持 JSON number（int），与 `/current` 现有 `nodes[].technology_id` 一致，不做字符串化；全景叠加里的 id 仍映射成字符串（裁定 B7）。`strength_manual` / `layout_x/y` 出参 number。

### 2.5 数据身份

- 审计真源仍是 DWD 的 `graph_change_set` / `graph_change_log`；`graph_tech_edge` 是**当前状态物化**（ADS 契约面），不是审计真源（复核 N4）。
- 新增表须按 `storage/README.md` §6 登记到 `storage/ENT/stores/mysql/ads.md` + `CHANGELOG.md`（本册不改其他文件，列入 §11/§12 待办）。
- 血缘：UI 技术点间关系 → Python overlay 读本表 → DWD change_log 回溯；本表不注册 metric_id。
- 指标护栏（ALGO-DATA-C8 / B9）：`read`、S4 分数种子、任何指标脚本**不得**从本表读 `strength_auto` / `rel_code`；建议在 `SCORE` 加断言（拒绝 `technology_master` / `graph_tech_edge` 表名），读图单测断言人工边无 `weight` / `strength` / `evidenceLevel`。METRIC §3.2 黑名单补 `graph_tech_edge.strength_auto`。

## 3. 既有表加列

### 3.1 `technology_master` 坐标

| 列 | 类型 | 空 | 语义 |
|---|---|---|---|
| `layout_x` | DOUBLE | Y | 画布世界坐标 x；**展示态，非业务真源**；只有新建点有值，种子点 NULL |
| `layout_y` | DOUBLE | Y | 同上 y |

- `/current` 出参为节点 `layout{x,y}`（API-C11），源列为 `layout_x/layout_y`（裁定 B2）。
- **权威与双写**（API-DATA-C19）：`technology_master.layout_*` 为权威，发布时用主表值覆盖 ADS `graph_entity_node.layout_*`；若发现漂移，以主表为准重刷 ADS，并记 `change_log`。
- 快照含主表全列，故含坐标，无需额外处理。

### 3.2 名称唯一键改造（补充复核 ①、裁定 A1）

现状 `uk_name_cn (name_cn)` 覆盖全表（`DDL:19`），软删点占名，删后不能同名重建（API-N3）。改为**只约束 active 行**：

```sql
-- 生成列 + 唯一索引（MySQL 8.0.x；STORED + UNIQUE 自 5.7 起支持，见 §10 版本核）
ALTER TABLE `demo_gkxlumenx_dwd`.`technology_master`
  ADD COLUMN `name_cn_active` VARCHAR(256)
      GENERATED ALWAYS AS (IF(`status` = 'active', `name_cn`, NULL)) STORED
      COMMENT 'active 行名称（唯一性只约束 active；deleted 行为 NULL）',
  ADD UNIQUE KEY `uk_name_cn_active` (`name_cn_active`),
  DROP INDEX `uk_name_cn`;
```

- 唯一索引允许多个 NULL，故任意多个 deleted 行可同名；active 行仍唯一。
- `name_cn` 与生成列同为 256 utf8mb4 = 1024 B，远低于 MySQL 8 InnoDB 3072 B 索引上限，无新增长度风险。
- **上线前置检查**：`SELECT name_cn, COUNT(*) c FROM technology_master WHERE status='active' GROUP BY name_cn HAVING c>1;` 有结果则 ALTER 会失败，须先人工归并。
- 备选：MySQL 8.0.13+ 函数索引 `UNIQUE KEY ((IF(status='active',name_cn,NULL)))`；生成列更可查，取生成列。
- 应用侧：validate 只查 active（`_validate_structure` 现无名称查重，`routes:560–750`）；种子不再依赖 `ON DUPLICATE`（§6.5）；publish 兜底把名称 1062 映射 422 / 42201（§5.4）。
- 名称比较按列排序规则（本册 DDL 用 `utf8mb4_general_ci`，大小写不敏感）；若未来要大小写敏感，需单独 `COLLATE`，不在本波。
- **Owner 口径**（裁定 A1）：**不需要**数据平台 Owner 书面确认，由监管人定；DDL 由监管人执行前备份（§10）。

### 3.3 `graph_entity_node` 坐标

| 列 | 类型 | 空 | 语义 |
|---|---|---|---|
| `layout_x` | DOUBLE | Y | 画布世界坐标 x，与主表同值（主表权威，发布覆盖） |
| `layout_y` | DOUBLE | Y | 同上 |

发布 / 种子写 node 时同步主表坐标；`/current` 读本表出 `layout`。

### 3.4 `graph_version` 三列（DATA-C7、复审、裁定 B16/B17）

现列 `version_id / parent_version_id / label / operator / stats / projection_status / created_at`（`DDL:55–64`）。加：

| 列 | 类型 | 空 | 默认 | 语义 |
|---|---|---|---|---|
| `kind` | VARCHAR(16) | N | `'ent'` | `save` / `rollback` / `seed` / `ent`。**`kind` 是动作类型：新保存（含 ENT 页经同一 publish）一律 `save`；回滚 `rollback`；种子 `seed`；`ent` 仅历史回填（含 v0）**。所有 INSERT 必须显式写 `kind`，禁止依赖默认值（ARCH-DATA-C3 / API-DATA-C2 / ALGO-DATA-C9） |
| `snapshot_status` | VARCHAR(16) | N | `'none'` | `ok` / `skipped_oversize` / `none`。可回滚 = `ok` 且 snapshot 行存在 |
| `publish_results` | JSON | Y | NULL | 发布回执 `results{succeeded,failed,failed_items}` 持久化；幂等重试原样返回；历史版本 NULL |

- 新版本 `projection_status` 恒写 `'ok'`（单事务成功即 ok，无需补偿）；列保留作历史兼容。
- `kind=rollback` 的回滚变更集 id 用 `rb-` 前缀（ARCH §3），故 `graph_change_set` 不加 `kind`。
- `operator` 来源（裁定 B17）：保存取 `change_set.operator`；回滚取 display 注入的 `body.operator`；种子写 `'seed'`。Python 不再写死 `'py'`（`routes:844` 现状）。
- **界面显示映射**（PROD-DATA-C2；实际渲染归 API/FE，本册给口径）：
  - `kind`：`save`→「保存」、`rollback`→「回滚」、`seed`→「种子」、`ent`→「历史版本」。
  - `snapshot_status`：**不在界面直接显示**，只用于派生 `rollbackable` 与 `not_rollbackable_reason`（API §4.1）；`ok` / `skipped_oversize` / `none` 原码不得直出。
  - `rollbackable=false` 的原因：`no_snapshot`→「该版本无快照，不能回滚」；`snapshot_oversize`→「该版本数据量超出快照上限，不能回滚」。
  - 上述英文码不得直出界面。

### 3.5 `graph_change_set.client_batch_id`（API-C8、裁定 A7/B11）

| 列 | 类型 | 空 | 语义 |
|---|---|---|---|
| `client_batch_id` | VARCHAR(64) | Y | 批次级幂等键；前端生成；缺省时服务端生成，不享受重试幂等；同批唯一；历史行 NULL |

- `UNIQUE KEY uk_client_batch (client_batch_id)`：唯一索引允许多 NULL，历史行不冲突。
- **`changes` 可缺省**（裁定 A7）：缺省时服务端生成一个批次号并落库，该批次**不享受重试幂等**；ENT 前端 FE-TS-10C 不强制改，建议后续补上。
- submit 去重从「只查 `ops[0].client_op_id`」（`routes:320–325`、`routes:758`）改为按本列查；publish 按本列做三态判定（§5.5）。

### 3.6 `graph_change_log.object_type` 注释

`object_type` 已是 `VARCHAR(32)`（`DDL:41`），收 `tech_edge` 无需改类型，仅改注释：

```sql
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_change_log`
  MODIFY COLUMN `object_type` VARCHAR(32) NOT NULL
  COMMENT 'node|entity|edge|tech_edge';
```

### 3.7 历史数据回填 SQL

新列 `NOT NULL DEFAULT` 会让既有行自动取值，下列语句为**显式回填 + 幂等核对**：

```sql
-- kind：历史 ENT 版本（含 v0）统一 ent；新写入必须显式 save/rollback/seed
UPDATE `demo_gkxlumenx_dwd`.`graph_version`
   SET `kind` = 'ent'
 WHERE `kind` NOT IN ('save','rollback','seed','ent');

-- snapshot_status：历史版本无快照
UPDATE `demo_gkxlumenx_dwd`.`graph_version`
   SET `snapshot_status` = 'none'
 WHERE `snapshot_status` NOT IN ('ok','skipped_oversize','none');

-- 核对：历史版本均不可回滚（无 graph_snapshot 行）
SELECT v.version_id, v.kind, v.snapshot_status, s.version_id AS snap
  FROM `demo_gkxlumenx_dwd`.`graph_version` v
  LEFT JOIN `demo_gkxlumenx_dwd`.`graph_snapshot` s ON s.version_id = v.version_id
 WHERE s.version_id IS NULL
 ORDER BY v.version_id;

-- 名称唯一键前置检查（有行则先归并）
SELECT `name_cn`, COUNT(*) c FROM `demo_gkxlumenx_dwd`.`technology_master`
 WHERE `status` = 'active' GROUP BY `name_cn` HAVING c > 1;
```

- v0（`version_id=1`）是初始空版本，回填为 `kind='ent'`；SEED-L01 另写自己的 `kind='seed'` 版本。
- **历史 `stats` 不回填**（裁定 B1 / API Q7）：旧行保留原值，前端兼容 `{ops:N}` / 扁平四键 / `{}` / NULL 四种形状，缺组不补 0。

## 4. 快照

### 4.1 payload 结构（DATA-C3、PRODUCT-N2、ALGO-DATA-C2、API-DATA-C19）

`graph_snapshot.payload` 是单 JSON（`DDL:110–115`），**每版发布 / 回滚都写一份，按 `version_id` 全量保留、不裁剪**（裁定 A4；原「每 N=50」作废）。结构：

```json
{
  "schema_version": "m10-graph-1",
  "taken_at": "2026-11-13T12:00:00",
  "version_id": 12,
  "parent_version_id": 11,
  "tables": {
    "technology_master":   [{"technology_id":3,"name_cn":"…","status":"active","layout_x":null,"layout_y":null,"…":"…"}],
    "graph_tech_edge":     [{"edge_id":1,"src":3,"dst":8,"rel_type":"包含","rel_code":null,"strength_auto":null,"strength_manual":7.5,"source":"manual","status":"active","version_id":12,"…":"…"}],
    "graph_entity_node":   [{"technology_id":3,"name_cn":"…","layout_x":null,"layout_y":null,"version_id":12}],
    "graph_entity_edge":   [{"src":"3","dst":"tech_paper:W…","rel_type":"关联","rank":0,"source":"auto","version_id":12,"…":"…"}],
    "graph_entity_member": [{"technology_id":"3","entity_id":"tech_paper:W…","entity_type":"paper","version_id":12}],
    "graph_entity_overlay":[{"entity_type":"paper","entity_id":"tech_paper:W…","version_id":12,"…":"…"}],
    "graph_tombstone":     [{"object_type":"node","object_id":"7","reason":"delete_node"}]
  }
}
```

| 规则 | 说明 |
|---|---|
| 全表全行 | 七张工作集表**全部行**，含 `status='deleted'` 的主表行与 `graph_tech_edge` 行（PRODUCT-N2：只存 active 会把已删关系回滚复活） |
| 物理删表 | `graph_entity_node` / `edge` / `member` 删点删边是物理删，快照即当前行；`graph_tombstone` 全量 |
| 不含审计表 | 不含 `graph_change_set` / `graph_change_log` / `graph_version` / `graph_snapshot` 自身（append-only，不还原） |
| 显式列清单 | **必须含各表主键**（`technology_id` / `edge_id` / 复合键），否则整表还原会改主键、`change_log.object_id` 对不上（API-DATA-C19）；**排除生成列 `name_cn_active`**（ALGO-DATA-C2）；含新列 `layout_x/y`、`rel_code`、`strength_auto` |
| `updated_at` | 可读入 payload 供审计展示，但**还原 INSERT/UPDATE 时排除**，由库自动写当前时间（B13） |
| 还原精度 | 数值按原类型写回（DECIMAL/DOUBLE/INT），日期转字符串；`technology_id`/`edge_id` 显式带 id 写回 |
| 保留策略 | 每版一份、不裁剪；存储增长随版本数线性，当前工作集远低于阈值（§4.3） |

### 4.2 阈值与「INSERT 前预判」（补充复核 ②、裁定 A4）

单事务里先 INSERT 超大 JSON 会中止事务、无法捕获后继续提交，因此**必须在 INSERT 前判定**：

| 条件 | 处置 |
|---|---|
| 主表 active 行数 > 2000 | `snapshot_status='skipped_oversize'`，不写快照，发布 / 回滚照常成功 |
| payload UTF-8 字节 > 8 MB | 同上 |
| 任一表行数 > 50000（硬保护） | 同上 |
| 种子 `--all` | 脚本层**硬禁用**（§6.6），不进快照路径 |

实现顺序（伪代码，交 PY-IMPL）：

```
rows = 读七表全部行（同一事务，事务内一致性读）
master_active = count(status='active')
payload_text = json.dumps({schema_version, ...}, ensure_ascii=False)
estimate = len(payload_text.encode("utf-8"))
oversize = master_active > 2000 or estimate > 8*1024*1024 or any(len(v) > 50000 for v in rows.values())
if oversize:
    写 version.snapshot_status = 'skipped_oversize'   # 不 INSERT graph_snapshot
else:
    INSERT INTO graph_snapshot(version_id, payload) VALUES (v, payload_text)
    写 version.snapshot_status = 'ok'
```

- 8 MB / active 2000 / 总行 50000 为裁定 A4 确认值；`max_allowed_packet` 取保守下界。
- 超限不是发布失败：版本成功、`snapshot_status='skipped_oversize'`；列表按 `not_rollbackable_reason='snapshot_oversize'` 显示「该版本数据量超出快照上限，不能回滚」（API §4.1）。
- **可再回滚提示**（PROD-DATA-C6）：回滚产生的版本若也超限，则不可再回滚；确认框须提示「若数据量超出快照上限，本次回滚生成的新版本将不能再次回滚」，不承诺一定可再回滚。
- `schema_version` 用常量 `m10-graph-1`，未来加列递增，回滚时按版本分派列映射。
- **已删存量边过滤**（ALGO-DATA-C5 / 裁定 B4）：全景叠加过滤已删存量边时，auto 行以 `(端点无序对, rel_code)` 匹配 Nebula；`rel_code` 为 NULL 时回退 `rel_type`；人工行 `rel_code` 恒 NULL，不参与存量边过滤。

### 4.3 上限保护

- 快照写入前做上表判定；`graph_snapshot.payload` 是 `NOT NULL`，判定失败即不写，绝不尝试超大 INSERT。
- SEED-L01 禁用 `--all`：全量约 19430 点 / 587k 边（`TS-L2-M10-ENT-SEED-L01.md` 调研），必然超限且会拖垮读面。
- 建议运维给该库设 `max_allowed_packet >= 16M` 并在执行单注明；8 MB 阈值已留余量。
- 每版保留、不裁剪（裁定 A4）；当前工作集 1 点 / 61 实体边，按版本数增长的存储量可接受；若未来需要清理，另立迁移单，不在本波。

## 5. 发布 / 回滚事务

### 5.1 串行锁（DATA-C4）

| 项 | 裁定 |
|---|---|
| 锁名 | `GET_LOCK('m10_graph_publish', 10)` |
| 覆盖 | publish 与 rollback **同一把锁**，同一连接，覆盖整个事务（含快照） |
| 释放 | `finally` 里 `RELEASE_LOCK('m10_graph_publish')` |
| 超时 | `GET_LOCK` 返回 0/NULL（或整体超过 10s）→ 409 / 40901「他人正在保存，请稍后重试」 |
| 理由 | 单写者 + 整段锁，消除原两段式（`routes:831–859` 提交后再 `_project`）的投影竞态 |

### 5.2 发布会话写序（单事务）

1. `GET_LOCK`。
2. `SELECT status, ops, base_version, client_batch_id, operator FROM graph_change_set WHERE id=%s FOR UPDATE`。
3. **幂等**：按 §5.5 三态判定；命中可幂等时读 `version_cs → graph_version`，返回原回执，释放锁。
4. 状态 `draft/approved` 才继续；`rejected` → 409；否则 409。
5. `_current_version`（`MAX(version_id) WHERE projection_status='ok'`，`routes:170–172`）比对 `base_version`，不符 409（附 `current_version`）。
6. `INSERT graph_version (parent_version_id, label, operator, stats, kind='save', projection_status='ok', snapshot_status='none')`；`version_id = LAST_INSERT_ID()`。**`operator = change_set.operator`**（裁定 B17）；`kind` 必须显式写 `'save'`（含 ENT 页保存）。
7. `INSERT graph_version_change_set (version_id, change_set_id)`。
8. `UPDATE graph_change_log SET version_id=%s WHERE change_set_id=%s`。
9. **第一遍**：全部 `add_node` → `INSERT technology_master`（含 `layout_x/y`、`importance_level` 空字面量）→ 得到 `technology_id`；同事务回填该 op 的 `change_log.object_id` 与 `after`（发布后行 + `client_node_id`）。
10. **第二遍**：其余 op：
    - `update_node` / `delete_node` → 主表 / 墓碑；`delete_node` 级联同时处理 `graph_entity_edge` **与** `graph_tech_edge`（DATA-S5），级联边**各写一行 `object_type='tech_edge'`、`op='delete_edge'`** 的 change_log，并在 `after` JSON 内带 `"reason":"cascade"`（`graph_change_log` 无 `reason` 列，不加列、不改 DDL），便于版本详情看到被级联删的边（API-DATA-C18 / ALGO-N1）；过滤 `node_id_map` 时只取 `op='add_node'`。
    - `add_edge` / `delete_edge` → `graph_tech_edge`（复活 / 422 / 软删）；`add_edge` 回填 `change_log.object_id=edge_id`、`after`。
    - `hang_entities` / `unhang_entities` / `update_entity_*` → 既有 ENT 逻辑。
11. 写 ADS：`graph_entity_node`（含坐标，主表权威）、`graph_entity_edge`、`graph_entity_member`、`graph_tech_edge`；所有写入行 `version_id=新版本`（DATA-C3）。**`graph_tech_edge` 的逻辑状态与 `version_id` 在同一条 UPDATE 内完成，不拆两次写**（ALGO-DATA-C11）。
12. 回填全部 op 的 `change_log.before/after`：新增类 before 空、删除类 after 空；tech 边 `before/after` 至少带 `src`/`dst` 对应节点名与中文 `rel_type`（auto 行带 `rel_code`），`edge_id` 只作内部号（PROD-DATA-C7）。
13. 组装快照（§4），预判；写 / 跳过；更新 `graph_version.snapshot_status`。
14. `UPDATE graph_version SET stats=%s, publish_results=%s`。
15. `UPDATE graph_change_set SET status='published'`。
16. COMMIT；`RELEASE_LOCK`。

> 0 行影响（如「关系不存在」）**不是失败**：照常提交、生成版本，`results.failed_items` 逐条记（沿用 `routes:866–884` 契约）。快照超限也不是失败。任一步 SQL 异常 → 整笔 ROLLBACK，无 pending 版本，草稿保留。

**`stats` 形状**（裁定 B1 / API §3.4，唯一口径；`graph_version.stats` 列注释同步）：

```json
{
  "tech_nodes":   {"added": 0, "updated": 0, "removed": 0},
  "tech_edges":   {"added": 0, "updated": 0, "removed": 0},
  "entity_links": {"added": 0, "removed": 0},
  "entity_edges": {"added": 0, "updated": 0, "removed": 0},
  "entity_attrs": {"updated": 0}
}
```

- `tech_edges.updated` 仅在两端都 active 且 `strength_manual` / `time_from` / `time_to` / `rel_type` 有差异时计数（API-DATA-C7；API v2 §3.4 已正式包含该键）。
- 历史版本保持 `{ops:N}` / 扁平四键 / `{}` / `NULL` 原样，**不回填、缺组不补 0**（裁定 B1、API Q7）。
- **`publish_results`** 存 `{succeeded, failed, failed_items}`，与 `stats` 不同结构，不得混用键名。

### 5.3 回滚会话写序（单事务、整图、裁定 B12/B13）

1. `GET_LOCK`。
2. 读目标 `graph_version`；`snapshot_status != 'ok'` 或 `graph_snapshot` 无行 → 409 / 40901「该版本无快照，不可回滚」。
3. `_current_version` 比对请求 `base_version`，不符 409。
4. **读目标快照，与当前工作集逐表求差**（存在性按 `status='active'` 判断；行键 `technology_id` / `edge_id`；比较字段排除 `version_id`、`updated_at` 与生成列；`tech_edges` 两端都 active 但 `strength_manual/time_from/time_to/rel_type` 有差异记 `updated`）。**回滚预览与回滚必须复用同一求差函数**（只读、不取锁的 preview 与取锁的 rollback 同函数；API-DATA-C7 / B13）。
5. `INSERT graph_change_set (id='rb-<uuid12>', base_version=current, ops=差异摘要, status='published', operator=body.operator)`（裁定 B17）。
6. `INSERT graph_version (parent=current, label, operator=body.operator, kind='rollback', projection_status='ok', snapshot_status='none')`；`version_id = LAST_INSERT_ID()`。**`kind` 显式写 `'rollback'`**；**先建版本行，再写日志**，闭合复核 N2。
7. `INSERT graph_version_change_set`。
8. **按快照还原七表**（整表语义，见下）。
9. 每条差异写一行 `graph_change_log`（`version_id=新版本`、`change_set_id='rb-…'`、`before=当前`、`after=目标`、`op` 用对应动作词：`add_node/update_node/delete_node/add_edge/delete_edge/hang_entities/…`；tech 边带 `src_name/dst_name/rel_type/rel_code`）。
10. 写还原后的全量快照（§4，超限同样降级）；更新 `snapshot_status`。
11. `UPDATE graph_version SET stats, publish_results`。回滚回执形状：`succeeded = 实际应用差异条数`、`failed = 0`、`failed_items = []`；`succeeded` 与 preview `counts.total` 同源（同一求差函数，API-DATA-C17）。
12. COMMIT；`RELEASE_LOCK`。

**还原各表的方法**（B13 / API-DATA-C6 / ALGO-DATA-C2）：

| 表 | 方法 | `version_id` 改写 |
|---|---|---|
| `technology_master` | **先 `DELETE` 本表全部行，再按快照 INSERT（显式 `technology_id`）**；显式列清单**排除生成列 `name_cn_active`、排除 `updated_at`**，避免 1062 / 3105（API-DATA-C6） | 无该列 |
| `graph_tech_edge` | 先 `DELETE` 本表全部行，再按快照 INSERT（显式 `edge_id`；列清单同上排除生成列/`updated_at`） | 改写为新回滚版本 |
| `graph_entity_node` | 同上 | 改写 |
| `graph_entity_edge` | 同上 | 改写 |
| `graph_entity_member` | 同上 | 改写 |
| `graph_entity_overlay` | 同上 | 改写 |
| `graph_tombstone` | 先 `DELETE` 本表全部行，再按快照 INSERT | 无该列 |

- 整表还原 = 回滚到目标版本的**当前状态**：目标版本之后新增的点 / 边将被**移除**，之后删除的点 / 边将**恢复**（tombstone 一并还原），之后修改的将**还原**为当时的值。**确认框必须同时说明「之后新增的将被移除、之后删除的将恢复、之后修改的将还原」**；回滚预览时态 `added/updated/removed` 译「恢复 / 还原 / 移除」，不得译反（PROD-DATA-C1、裁定 B19、API §4.1）。
- ADS 行 `version_id` 改为本次回滚新版本，避免 R2 / 血缘读到旧版本号（DATA-C3）。
- 审计表（change_set / change_log / version / snapshot）**不还原**，只追加。
- `source=auto` 的种子边随快照回滚属应有含义；后续 auto 层若重新产出，按 manual > tombstone > auto 覆盖（ARCH §3）。

### 5.4 失败码映射（补充复核 ③、裁定 B10、PROD-API-C3）

| 异常 | 映射 | 处理 |
|---|---|---|
| 缺表 / 缺列 / 缺库（1146/1054/1049） | 503 / 50302 | 沿 `_MISSING_SCHEMA_ERRNO`（`routes:62–63`）；例外：`graph_entity_member` 缺表 / 缺列仍按 `routes:247–266` 静默兼容，不报 50302（API R1）。提示「维护功能暂不可用，请联系管理员」，**不写「可重试」** |
| 死锁 1213 / 锁等待超时 1205 | 409 / 40901 | 在 `enveloped` 增 `_DEADLOCK_ERRNO = {1213,1205}` → 409「他人正在保存，请稍后重试」，草稿保留；死锁回滚后 change_set 仍可重试、无半版本 |
| `GET_LOCK` 超时 | 409 / 40901 | 文案同上 |
| **名称 1062**（active 重名） | **422 / 42201** | validate 预查可挡常规；publish 兜底也映射 422「名称已存在（不区分大小写），请换一个」，不落 `failed_items` |
| **`graph_tech_edge` 1062**（active 同键） | **409 / 40901** | 整笔回滚；validate 已挡常规重复，publish 命中即并发 / 脏数据，提示重试；不落 `failed_items`（API-DATA-C9 / 裁定 B10） |
| 其他 SQL | 500 / 50001 | 整笔回滚，草稿保留 |
| 50301 | **退役** | 单事务后不再有 projection_pending；`EnvelopeError` 文档串同步删 |
| 50303 | 仅 Java 层 | 下游不可达，display / topic `relayStatus` 使用；DATA / entan-py 不产生该码（裁定 A5） |

### 5.5 幂等（API-C8、裁定 B11、ALGO-DATA-C10）

**submit**（按 `client_batch_id` 唯一键查 `graph_change_set`）：
- 未命中 → 新建 `draft`。
- 命中 `draft` / `published` 且 `ops` 相同 → 幂等返回旧 `{change_set_id,status,idempotent:true}`。
- 命中 `rejected` → 409 / 40901「批次已放弃，请重新生成 `client_batch_id`」。
- 命中同 batch 但 `ops` 不同 → 409（不得静默用旧回执）。

**publish**（按 `change_set` + `client_batch_id` 三态）：
- 带 batch 且 ≠ `change_set.client_batch_id` → 409 / 40901。
- 不带 batch → 若 `status='published'`，视为幂等重放，返回原回执（不报 409）；若 `draft/approved`，正常发布。
- `status='rejected'` → 409，不返回旧回执。

**回执复原**：
- `node_id_map`：按 `change_set_id` 扫 `object_type='node'`，**只取 `op='add_node'` 且 `after` 含 `client_node_id` 的行**；`update_node` / `delete_node` 不进映射（ALGO-DATA-C10）。
- `results`：`graph_version.publish_results`（§3.4）；历史版本 NULL → 返回 `results:null`。
- **对象号回填**：`add_node` → `technology_id`；`add_edge` 提交时先记 `client_op_id`，发布后回填 `edge_id`；`delete_edge` 的 `edge_id` 提交时已存在，不回填。`before/after` 都按对象落在发布事务内。

## 6. 种子 `TS-L2-M10-GRAPH-SEED-L01`

**这是新能力**：as-built seed 只读 `tech_has_*` 实体边（`seed:51–56`、`seed:91–101`），从不读 `tech_rel`；现脚本只有 `strength`（1 点）与 `all`（19430 点）两档，没有 ≤50 领域切片。SEED-L01 需新增独立脚本（或新 scope），不复用现有开关。

### 6.1 子图选取方法（DATA-N3、裁定 B5、ALGO-DATA-C1/C4/C6）

1. 候选中心：按 §6.2 选领域切片（**默认 #2**）。
2. 读 `demo_gkx_chain` 的 `tech_point`（`id(v)`、`technology_node_id`、`name_zh`、`name_en`、`weighted_degree`）。
3. 取**诱导子图**：先定 ≤50 个点，再只取**两端都在该点集内**的 `tech_rel`：
   ```
   MATCH (a:tech_point)-[e:tech_rel]-(b:tech_point)
   WHERE id(a) IN [...] AND id(b) IN [...]
   RETURN id(a), a.tech_point.technology_node_id, id(b), b.tech_point.technology_node_id,
          e.relation_type, e.relation_confidence_score, e.first_evidence_year
   ```
4. **类型白名单（硬规则）**：只允许写入 dry-run 确认的英文码白名单（当前四码：`KNOWLEDGE_DEPENDENCY` / `PATENT_CONVERGENCE` / `CO_EVOLUTION` / `WEAK_DEPENDENCY` 及其他 dry-run 确认的英文码）。**凡命中 `包含` / `依赖` / `促进` 或任何非 ASCII 码，一律跳过该边并计数，dry-run 打印 `{code, count}`，不中止**（裁定 B5）；**仅白名单外的英文码**默认中止，除非监管人书面豁免（ALGO-DATA-C1）。
5. **自环 / 端点剔除（硬规则）**：① 映射后 `src_tech_id == dst_tech_id` 的边丢弃（合并同名点会产自环，`add_edge` 已定 422，种子不能绕过）；② 端点主表 `status != 'active'`，或端点**无法映射到 `technology_master.technology_id`**（既不在既有 `external_ids` 中、也不在本次新建点集内）时跳过该边；dry-run 打印 `{self_loop, missing_endpoint, deleted_endpoint}` 计数（ALGO-DATA-C4 / ALGO-N4、裁定 B5）。
6. **无向去重与聚合**：Nebula MATCH 无向，A→B 与 B→A 会各返回一次；按 `(unordered pair, relation_type)` 去重，落库方向规范化为 `src=min(technology_id)`、`dst=max(technology_id)`。同一 `(pair, type)` 多条边聚合：`strength_auto = MAX(relation_confidence_score)`、`time_from = MIN(first_evidence_year)`、**`time_to = NULL`（不补 `to`，裁定 B14）**；dry-run 打印重复组数。文档写明**删除该行会隐藏该无序对+类型下的全部 Nebula 边**（表是 pair+type 粒度，ALGO-DATA-C6）。
7. dry-run 输出：`点数 / 边数 / distinct relation_type / {code,count} / {self_loop,missing_endpoint,deleted_endpoint} / 重复组数`，确认 ≤50 点、在快照阈值内。

### 6.2 领域切片（裁定 A2、PROD-DATA-C5）

| # | 切片 | 取法 | 角色 |
|---|---|---|---|
| **2（默认）** | 关键词「人工智能 / 大模型」 | `name_zh CONTAINS '人工智能' OR '大模型'` 命中点，按 `weighted_degree` 取前 50 + 其间 `tech_rel` | **演示默认**；可读性好、关系密度足够覆盖增删边与回滚 |
| 1（回归） | 现有 ENT 点的一跳诱导子图 | 以「神经性厌食症治疗的临床视角」（`tech_point:tcn_000f21ac06aceb9cdd0575e82d0d85fc`，现有 ENT 工作集唯一 active 点）为中心，经 `tech_rel` 无向扩 1～2 跳，截 50 点 | 只做与现有 1 点 / 61 实体边的回归，不作默认 |
| 3（压测） | 核心子图 | `tech_point` 按 `weighted_degree` 降序取前 50 + 其间 `tech_rel` | 只做压测（软删 / 复活 / 快照还原） |

> 不连库，无法预知各切片点数与关系类型分布；**执行前必须 `--dry-run`**，输出点数、边数、`distinct relation_type`、丢弃数（自环 / 缺端点 / 已删端点 / 中文码 / 重复组），确认 ≤50 点且在快照阈值内（主表 active ≤2000、payload ≤8 MB）。结果附在 SEED-L01 执行记录。

### 6.3 写入哪些表与字段

| 表 | 写什么 |
|---|---|
| `demo_gkxlumenx_dwd.technology_master` | 每点一行：`name_cn`、`name_en`、`external_ids`、`category=NULL`（未分类；**分类存中文名，空则手填**，裁定 A3）、`importance_level=NULL`（不吃 DDL 默认「中」，ALGO-C6）、`status='active'`（新建）/ 不改（已存在） |
| `demo_gkxlumenx_ads.graph_entity_node` | active 点：`technology_id`、`name_cn`、`category=NULL`、`importance_level=NULL`、`display_name=name_cn`、`layout_x/y=NULL`、`version_id=新 seed 版本` |
| `demo_gkxlumenx_ads.graph_tech_edge` | 每条诱导边：`src`、`dst`、`rel_type=原码`、`rel_code=原码`、`strength_auto=组内 MAX(relation_confidence_score)`、`time_from=组内 MIN(first_evidence_year)`、**`time_to=NULL`**、`source='auto'`、`status='active'`、`version_id=新 seed 版本` |
| `demo_gkxlumenx_dwd.graph_version` | 一行新版本：`parent_version_id=当前 max ok`、`label`（如「种子：人工智能 / 大模型」）、`operator='seed'`、`kind='seed'`、`stats=分组计数`（§5.2 结构）、`projection_status='ok'`、`snapshot_status`（按 §4 预判） |
| `demo_gkxlumenx_dwd.graph_snapshot` | 灌后全量快照（§4）；超限则跳过并标 `skipped_oversize` |

不写 `graph_change_set` / `graph_change_log`（种子是系统灌入，不是人工改动）；不写 `graph_tombstone`（种子不删点）；不写 `graph_entity_edge` / `member` / `overlay`（本单只做技术点间图，实体边留 ENT 既有路径）。

> 写入顺序（ALGO-N3/N4）：先 upsert `technology_master` 取得 `technology_id` → 建立「Nebula 端点 → technology_id」映射（新点按本次新建点集补齐）→ 再写 `graph_entity_node` 与 `graph_tech_edge`；映射不到且不在新建点集的端点按 §6.1-5 跳过并计数。

> 与现有 ENT 工作集（1 个 active 技术点 / 61 条实体边）**并存**：不软删切片外的点，不动现有实体边与 overlay。种子点 `category=NULL` 显示「未分类」；`strength_auto` 不出参，若维护页展示种子边强度，标「存量强度（只读）」（PROD-DATA-C8）。

### 6.4 `external_ids` 写法（DATA-C2、ALGO-DATA-C7）

沿用 `seed:163–171` 的 `_external_ids`：

```json
{"legacy_vid":"tech_point:tcn_<32hex>",
 "technology_node_id":"<tnid 或空串>",
 "all_legacy_vids":["…","…"],
 "all_technology_node_ids":["…","…"]}
```

- 单值：`legacy_vid` = 首个 VID 原串；`technology_node_id` = 首个 tnid，**空则写空串**（不写 null，与读侧回退规则一致）。
- 重名合并（同一 `name_zh` 多点）：`all_legacy_vids` / `all_technology_node_ids` 写全量。
- 读侧映射：两列表按 `min(len)` 同下标 zip，tnid 非空取 tnid、否则取 VID 原串，空串跳过；**多出的 tnid / VID 一律跳过并 warning，不单独加入**（ALGO-DATA-C7，取代 v1 的「多出的 tnid 单独加入」）。本册定 `external_ids` 的写法，跨端规则归 `TS-L2-M10-GRAPH-API` / DS02 知会。

### 6.5 重跑保护（DATA-N1、补充复核 ①）

| 表 | 规则 |
|---|---|
| `technology_master` | 显式按 `external_ids`（`JSON_EXTRACT`）或 active 同名查找，**不用 `ON DUPLICATE KEY` 依赖名称唯一键**（新索引只约束 active）。命中 active → 只更新 `name_en` / `external_ids`，**不覆盖 `status`**。命中任意 `status='deleted'` 的行 → **整组跳过**：不复活、不新建同 `external_ids` 的 active 行。未命中 → `INSERT status='active'` |
| `graph_entity_node` | `ON DUPLICATE KEY UPDATE name_cn=VALUES(name_cn), display_name=VALUES(display_name), version_id=VALUES(version_id)`；**不覆盖 `layout_x/y`**（保留用户已设坐标） |
| `graph_tech_edge` | `INSERT IGNORE`（或 `ON DUPLICATE KEY UPDATE edge_id=edge_id` 空更新）；已有行（含 `status='deleted'`、`source='manual'`）**status / source / 强度一律不动** |
| 切片外 | 不软删、不改任何行 |
| `importance_level` | 显式写 NULL，不吃默认「中」 |
| 中文码 / 非 ASCII 码 | 跳过并计数，不中止（§6.1） |
| 白名单外英文码 | 默认中止，除非监管人书面豁免（§6.1） |

### 6.6 `--all` 禁用

- 新脚本拒绝 `--all`（`parser.error` / exit 2），并在 `--dry-run` 报告里提示「快照开启后禁用全量」。
- 设硬上限：点数 > 50 直接中止；`--max-write` 默认 5000 保留；`planned_total` 超限中止。
- 原因：19430 点 / 587k 边必撑爆快照与读面（`TS-L2-M10-ENT-SEED-L01.md` 调研）。

### 6.7 执行后核对 SQL

```sql
-- 版本 / 快照
SELECT version_id, kind, snapshot_status, label, operator, stats
  FROM `demo_gkxlumenx_dwd`.`graph_version` ORDER BY version_id DESC LIMIT 3;
SELECT version_id, JSON_EXTRACT(payload, '$.schema_version') sv,
       JSON_LENGTH(payload, '$.tables.technology_master') master_rows,
       JSON_LENGTH(payload, '$.tables.graph_tech_edge') tech_edge_rows
  FROM `demo_gkxlumenx_dwd`.`graph_snapshot` ORDER BY version_id DESC LIMIT 1;

-- 技术点 / 边
SELECT COUNT(*) total, SUM(status='active') active, SUM(status='deleted') deleted
  FROM `demo_gkxlumenx_dwd`.`technology_master`;
SELECT COUNT(*) total, SUM(status='active') active, SUM(source='auto') auto,
       SUM(source='manual') manual, COUNT(DISTINCT rel_type) rel_types
  FROM `demo_gkxlumenx_ads`.`graph_tech_edge`;
SELECT src, dst, rel_type, rel_code, strength_auto, time_from, time_to, status
  FROM `demo_gkxlumenx_ads`.`graph_tech_edge` ORDER BY edge_id LIMIT 10;
-- 自环 / 非 active 端点（期望 0 行）
SELECT e.edge_id FROM `demo_gkxlumenx_ads`.`graph_tech_edge` e
  JOIN `demo_gkxlumenx_dwd`.`technology_master` a ON a.technology_id=e.src
  JOIN `demo_gkxlumenx_dwd`.`technology_master` b ON b.technology_id=e.dst
 WHERE e.src=e.dst OR a.status<>'active' OR b.status<>'active';

-- ADS 节点 / 版本推进
SELECT COUNT(*) FROM `demo_gkxlumenx_ads`.`graph_entity_node`;
SELECT MAX(version_id) FROM `demo_gkxlumenx_dwd`.`graph_version` WHERE projection_status='ok';
```

再用读面核对：`GET /internal/v1/sci/tech/graph/current`（节点 / `tech_edges[]` / `layout`）；全景读图开 overlay 后人工层字段可见。

### 6.8 演示分类清单（裁定 A3、PROD-DATA-C4）

`dim_tech_domain` 现有三行演示值（`DDL:117–122`）不足时，由 SEED 补种子行，**不改表结构**。演示清单建议如下（`domain_code` 仅维表内部用，`technology_master.category` 存中文 `domain_name`，VARCHAR(64)，不做外键、只校验非空与长度）：

| domain_code | domain_name |
|---|---|
| AI | 人工智能 |
| BIGDATA | 大数据 |
| CLOUD | 云计算 |
| IOT | 物联网 |
| BLOCKCHAIN | 区块链 |
| SECURITY | 网络安全 |
| BIOMED | 生物医药 |
| NEWENERGY | 新能源 |
| NEWMATERIAL | 新材料 |
| EQUIPMENT | 高端装备 |
| AEROSPACE | 航空航天 |
| QUANTUM | 量子信息 |

- 34 / 38 表单用下拉单选，选项来自 `dim_tech_domain` 的 `domain_name`；维表为空 / 不可用时降级为文本输入（allow-create），34-3 **不因下拉为空而无法提交**。
- 种子点 `category=NULL` 显示「未分类」；历史自由文本原样显示；不写英文 `domain_code` 到 `category`。
- 分类体系选型仍是甲方待定项 `OI-C02-02`，本清单只作演示默认，不是最终分类体系。

## 7. 两服务库名一致性（DATA-C5）

### 7.1 解析链

| 服务 | 用途 | 解析顺序 | 默认 |
|---|---|---|---|
| entan-py（写） | `_schemas()` | `GKX_M10_ENT_DWD_DB` → `ENTAN_MYSQL_DWD_DB` → `demo_gkxlumenx_dwd`；ADS 同理（`routes:115–120`） | `demo_gkxlumenx_dwd/ads` |
| algo-py（读） | `DB.__init__` | `LUMEN_ALGO_MYSQL_DWD_DB` → `cfg.dwd_db` → `gkxlumenx_dwd`；ADS 同理（`db:36–37`） | `gkxlumenx_dwd/ads` |

当前部署都指 `demo_*`：entan `values.yaml:893–905` / `values-lumen.yaml:508–512`；algo `k8s/api.yaml:38–39`。**默认值不同**是隐患（漏配 env 会写 A 库、读 B 库）。

### 7.2 启动断言（复核附注）

- entan-py：启动时解析 `(dwd, ads)`，断言**两者都以 `demo_gkxlumenx_` 开头**，否则 fail fast；打印 `[schema] dwd=… ads=…`。
- algo-py：叠加前解析，断言 `demo_gkxlumenx_` 前缀；不合规则**关闭叠加**（`overlay.status=unavailable`）并告警，绝不读 `gkxlumenx_*`；打印同一行。
- 部署核对：两边日志的 `dwd/ads` 必须逐字一致；建议在 helm / k8s 同时显式设 `GKX_M10_ENT_*` 与 `LUMEN_ALGO_MYSQL_*`，不依赖默认。
- 只读：algo-py 叠加只走 `DB.query()`（`db:63–66`），连接设 `connect_timeout=2s` / `read_timeout=3s`（现 `db:39–46` 未设，需在叠加用独立连接补）；超时按 ARCH §4.3 降级。

### 7.3 D12 偏差记档

- 工作集在 `demo_gkxlumenx_dwd/ads`，相对 D12 数据面基线（`gkxlumenx_*`，`architecture-baseline.md:139`）是**临时偏差**，沿库边界 2026-10-19（开发写入不进产线库）。
- 这是读 **demo 数据库**，不是调 **demo 服务**，不构成 D12 服务调用违规（`architecture-baseline.md:139`）。
- 正式化时同步 DDL 迁 `gkxlumenx_*`，届时须数据平台 Owner / 架构再确认（§10）。

### 7.4 impact 计数口径（DATA-S2、裁定 B3/B15）

35-3 的 `tech_edge_count` 读 `graph_tech_edge`（`src=? OR dst=?`，**只数 `status='active'`，两个方向都算**，裁定 B15）；`panorama_hidden_relation_count` 用 **entan-py 自有 Nebula 只读会话**（`entan.common.nebula`），会话内显式 `USE demo_gkx_chain`，只做 MATCH / 计数，**不走 chainan**（`chain_space()` 未打进 entan 镜像，裁定 B3）；无向、`evidence_level IN [HIGH,MEDIUM]`（`read:265–282`），超时 / 失败返回 `null` 不挡删除。人工边不计入该隐藏计数（B6）。本册不新增列。

### 7.5 计数类 D9（DATA-S4、裁定 A8/B9/ALGO-DATA-C8）

`impact` 两项、版本 `stats`、回滚预览分组计数、回滚回执 `results`、`publish_results` 均属操作回执类计数，按 DN-A03-09「操作回执类计数豁免 D9」**建议范围（七类）**处理；PM / 数据 Lead 回执前，METRIC 册写「按 DN-A03-09 建议范围，待 PM / 数据 Lead 确认」，不阻塞会签。本册不注册 metric_id。

`graph_tech_edge.strength_auto` / `rel_code` 不得被任何指标脚本读取；METRIC §3.2 黑名单已补 `strength_auto`。建议实现单加断言（§2.5）。

### 7.6 版本统计与回滚预览的关系（裁定 B12）

- 40-4 版本列表展示的是**该版本自己**的 `stats`；40-3 回滚预览的 `counts` 是**目标版本快照与当前工作集求差**的结果。二者**同一套分组键**，但不是同一份数据。
- 真正同源的是 40-3 `counts` 与**回滚生成的新版本** `stats`（同一求差函数、同一事务内）；不等于目标版本自己的 `stats`。
- 实现单须写死「preview 与 rollback 复用同一求差函数」；`counts.total` 与回滚 `results.succeeded` 同源（§5.3）。

## 8. DDL 草案全文（UP）

> 库：`demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`；引擎 MySQL 8.0.x（`db.py:1` 标注 8.0，GDF 连接文档 `MySQL 8.0.x`）。MySQL 8 **无 `ADD COLUMN IF NOT EXISTS`**，执行前用 `information_schema` 判存；整体执行前**备份**。执行人：监管人 `human:刘剑锋`。名称唯一键改造**不需**数据平台 Owner（裁定 A1）。

```sql
-- ============================================================
-- TS-L2-M10-GRAPH-DATA UP · 2026-11-13 · v2
-- 执行前备份 demo_gkxlumenx_dwd / demo_gkxlumenx_ads
-- ============================================================

-- A. 新表：技术点间边（ADS 当前状态物化；软删行占唯一键）
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`graph_tech_edge` (
  `edge_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '边主键（delete_edge 参数 / change_log 对象号）',
  `src` BIGINT NOT NULL COMMENT '起点 technology_master.technology_id',
  `dst` BIGINT NOT NULL COMMENT '终点 technology_master.technology_id（有向）',
  `rel_type` VARCHAR(64) NOT NULL COMMENT '人工边=包含/依赖/促进；种子边=Nebula 原关系码；参与唯一键',
  `rel_code` VARCHAR(64) DEFAULT NULL COMMENT '种子边原关系码（auto 行；人工边 NULL）；用于已删存量边过滤，不出参',
  `strength_auto` DECIMAL(10,4) DEFAULT NULL COMMENT 'auto 原强度快照（不出参，不参与任何指标）',
  `strength_manual` DECIMAL(10,4) DEFAULT NULL COMMENT '人工强度（永不进指标）',
  `time_from` INT DEFAULT NULL COMMENT '起始年 1900-2100（选填）',
  `time_to` INT DEFAULT NULL COMMENT '结束年 1900-2100（选填，允许开放端）',
  `source` VARCHAR(8) NOT NULL DEFAULT 'auto' COMMENT 'auto|manual',
  `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT 'active|deleted（软删）',
  `version_id` BIGINT NOT NULL COMMENT '最后写入版本',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`edge_id`),
  UNIQUE KEY `uk_tech_edge` (`src`,`dst`,`rel_type`),
  KEY `idx_src` (`src`),
  KEY `idx_dst` (`dst`),
  KEY `idx_status_source` (`status`,`source`),
  KEY `idx_version` (`version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='技术点间边（M10 维护工作集；软删行占唯一键）';

-- B1. 主表坐标（展示态，非业务真源；主表权威）
ALTER TABLE `demo_gkxlumenx_dwd`.`technology_master`
  ADD COLUMN `layout_x` DOUBLE DEFAULT NULL COMMENT '画布世界坐标 x（展示态；主表权威）',
  ADD COLUMN `layout_y` DOUBLE DEFAULT NULL COMMENT '画布世界坐标 y（展示态；主表权威）';

-- B2. 名称唯一键：只约束 active（前置：active 无重名；裁定 A1 不需 Owner）
ALTER TABLE `demo_gkxlumenx_dwd`.`technology_master`
  ADD COLUMN `name_cn_active` VARCHAR(256)
      GENERATED ALWAYS AS (IF(`status` = 'active', `name_cn`, NULL)) STORED
      COMMENT 'active 行名称（唯一性只约束 active；deleted 行为 NULL）',
  ADD UNIQUE KEY `uk_name_cn_active` (`name_cn_active`),
  DROP INDEX `uk_name_cn`;

-- C. ADS 节点坐标（发布时由主表覆盖）
ALTER TABLE `demo_gkxlumenx_ads`.`graph_entity_node`
  ADD COLUMN `layout_x` DOUBLE DEFAULT NULL COMMENT '画布世界坐标 x',
  ADD COLUMN `layout_y` DOUBLE DEFAULT NULL COMMENT '画布世界坐标 y';

-- D. 版本元数据（kind 必须由所有 INSERT 显式写入，禁止依赖默认）
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_version`
  ADD COLUMN `kind` VARCHAR(16) NOT NULL DEFAULT 'ent' COMMENT 'save|rollback|seed|ent（ent 仅历史回填）',
  ADD COLUMN `snapshot_status` VARCHAR(16) NOT NULL DEFAULT 'none' COMMENT 'ok|skipped_oversize|none',
  ADD COLUMN `publish_results` JSON DEFAULT NULL COMMENT '发布回执 results 持久化（历史 NULL）';

-- E. 批次幂等键（changes 可缺省，缺省时服务端生成、不享重试幂等）
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_change_set`
  ADD COLUMN `client_batch_id` VARCHAR(64) DEFAULT NULL COMMENT '批次级幂等键（可缺省；历史 NULL）',
  ADD UNIQUE KEY `uk_client_batch` (`client_batch_id`);

-- F. 审计对象类型注释
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_change_log`
  MODIFY COLUMN `object_type` VARCHAR(32) NOT NULL COMMENT 'node|entity|edge|tech_edge';

-- G. 快照表注释（每版一份、按 version_id 保留、不裁剪）
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_snapshot`
  COMMENT='每版发布/回滚全量快照（每版一份、不裁剪；payload 含 schema_version 与软删行）';

-- H. 版本统计注释（形状见 §5.2；历史行保留旧形状、不回填）
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_version`
  MODIFY COLUMN `stats` JSON DEFAULT NULL
  COMMENT '分组计数：tech_nodes{added,updated,removed}/tech_edges{...}/entity_links{...}/entity_edges{...}/entity_attrs{updated}；历史行可为 {ops:N}/扁平四键/{} /NULL';

-- I. 历史回填（新列已带默认，下面为幂等核对）
UPDATE `demo_gkxlumenx_dwd`.`graph_version`
   SET `kind` = 'ent' WHERE `kind` NOT IN ('save','rollback','seed','ent');
UPDATE `demo_gkxlumenx_dwd`.`graph_version`
   SET `snapshot_status` = 'none' WHERE `snapshot_status` NOT IN ('ok','skipped_oversize','none');
```

> `stats` 的 `MODIFY COLUMN` 以现列类型为 `JSON` 为前提；执行前用 `SHOW COLUMNS` 核对，若类型不同则只 `ALTER TABLE ... ALTER COLUMN stats COMMENT`（MySQL 8 支持列注释变更），不改类型。`kind` 保留 `DEFAULT 'ent'` 是为了让 ADD COLUMN 平滑，但**代码必须显式写 `kind`**，并在启动 / 单测断言新版本 `kind ∈ {save,rollback,seed}`（ARCH-DATA-C3）。

## 9. 回滚脚本（DOWN）

> 同样由监管人执行，执行前备份。**注意**：DOWN 会把 `uk_name_cn` 加回全表；若库内存在「active 与 deleted 同名」的行，`ADD UNIQUE KEY uk_name_cn` 会失败。届时优先用备份恢复，不要强改。DOWN 不删数据行（除非另选 `DROP TABLE` 后整库恢复）。

```sql
-- 前置检查：全表重名（有结果则不能直接 DOWN）
SELECT `name_cn`, COUNT(*) c FROM `demo_gkxlumenx_dwd`.`technology_master`
 GROUP BY `name_cn` HAVING c > 1;

-- 1) 审计对象类型注释还原
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_change_log`
  MODIFY COLUMN `object_type` VARCHAR(32) NOT NULL COMMENT 'node|entity|edge';

-- 2) 批次幂等键
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_change_set`
  DROP INDEX `uk_client_batch`, DROP COLUMN `client_batch_id`;

-- 3) 版本元数据
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_version`
  DROP COLUMN `publish_results`, DROP COLUMN `snapshot_status`, DROP COLUMN `kind`;

-- 4) ADS 节点坐标
ALTER TABLE `demo_gkxlumenx_ads`.`graph_entity_node`
  DROP COLUMN `layout_y`, DROP COLUMN `layout_x`;

-- 5) 主表：名称唯一键 + 坐标
ALTER TABLE `demo_gkxlumenx_dwd`.`technology_master`
  DROP INDEX `uk_name_cn_active`,
  DROP COLUMN `name_cn_active`,
  ADD UNIQUE KEY `uk_name_cn` (`name_cn`),
  DROP COLUMN `layout_y`, DROP COLUMN `layout_x`;

-- 6) 快照表注释还原
ALTER TABLE `demo_gkxlumenx_dwd`.`graph_snapshot`
  COMMENT='每 N 版全量快照（回滚加速）';

-- 7) 新表
DROP TABLE IF EXISTS `demo_gkxlumenx_ads`.`graph_tech_edge`;
```

## 10. 执行人与数据平台 Owner 判断（裁定 A1）

| 变更 | 性质 | 执行 | Owner 确认 |
|---|---|---|---|
| 新建 `graph_tech_edge` | 新建正式库表（demo 实例） | 监管人 `human:刘剑锋`，执行前备份 | demo 库：监管人执行 + 备份即可；正式化到 `gkxlumenx_*` 时须数据平台 Owner / 架构再确认（停机条件，ARCH §11 / §2） |
| 加 `layout_x/y`（主表、node） | 纯增量加列 | 监管人，备份 | 不需要 |
| 名称唯一键改造（`name_cn_active` + 删 `uk_name_cn`） | 改唯一键（非纯增量） | 监管人，备份 | **不需要数据平台 Owner**（裁定 A1：监管人定；DDL 执行前备份） |
| `graph_version` / `graph_change_set` / `graph_change_log` 加列改注释 / `stats` 注释 | 纯增量 | 监管人，备份 | 不需要 |

**结论**：整体 DDL 由监管人执行、执行前备份；名称唯一键**不再需要**数据平台 Owner 书面确认（裁定 A1）。正式化迁移 `gkxlumenx_*` 时另走 Owner / 架构确认。

## 11. 对 ENT-DATA 的追记（ENT 共用路径的变化）

> 本册不改 `TS-L2-M10-ENT-DATA.md` 本体；下列为 ENT 数据面的结构 / 语义变化，供 ENT-DATA 及其会签单由原审稿身份追认。**确认前不派 PY-IMPL**（ARCH §10、API-N5、裁定 B18）。

| # | ENT 原状 | 变化 |
|---|---|---|
| 1 | 发布两段式：MySQL 先提交 → Nebula → ADS，失败留 `projection_status='pending'` / 50301（ENT-DATA §4） | **加锁单事务**，DWD/ADS 同事务；任一步失败整笔回滚，无 pending；新版本 `projection_status` 恒 `ok`；50301 退役 |
| 2 | 发布写 Nebula（`_project_nebula`，`routes:980–1000`） | **删除** `_project_nebula` 与 `GKX_NEBULA_MAINTAIN_SPACE`；ENT 7 个 op 与本叶 3 个新 op 都不写图（35-3 只读计数除外）。线上 env 未配置，行为不变 |
| 3 | `graph_version` 无类型 / 快照状态 / 回执列（`DDL:55–64`） | 加 `kind` / `snapshot_status` / `publish_results`；历史回填 `kind='ent'`、`snapshot_status='none'`；**新保存（含 ENT 页）`kind='save'`** |
| 4 | 快照每 N=50 版（`DDL:109–115` 注释） | **每版一份、不裁剪**：每次发布 / 回滚同事务写全量快照；payload 加 `schema_version`，含软删行 |
| 5 | `graph_change_set` 无批次键（`DDL:24–34`） | 加 `client_batch_id` + 唯一键；submit / publish 批次幂等；changes 可缺省（服务端生成、不享重试） |
| 6 | `technology_master.uk_name_cn` 覆盖全表（`DDL:19`） | 改为生成列 `name_cn_active` + `uk_name_cn_active`，只约束 active；**软删后可同名重建，改名撞 active 才 422**；**seed `MASTER_SQL`（`seed:234–241`）的 `ON DUPLICATE … status='active'` 不再适用**，须改为显式查找 + 不覆盖 status + 跳过 deleted |
| 7 | `graph_entity_edge` 是唯一技术点相关 ADS 边表 | 新增 `graph_tech_edge`（技术点↔技术点）；**所有读 / 删 / 快照 / 回滚路径同时处理两张边表**（`routes:383`、`:520–521`、`:1034–1041` 都要扩） |
| 8 | `graph_change_log.object_type` 仅 node/entity/edge（`DDL:41`） | 扩 `tech_edge`；`add_node` / `add_edge` 的 `object_id` 与 `after` 在发布事务内回填；级联删边各记一行 |
| 9 | `_current_version` 只认 `projection_status='ok'`（`routes:170–172`） | 保留；因新版本恒 `ok`，语义不变 |
| 10 | `/current` 出参无技术点间边 / 坐标（`routes:348–414`） | 新增顶层 `tech_edges[]`（只 active，`src/dst` 为 number）与节点 `layout{x,y}`；不并入 `node.edges`（ENT 页不受影响） |
| 11 | 失败码仅 1146/1054/1049 → 503（`routes:62–63`） | 增死锁 1213 / 锁等待 1205 → 409；名称 1062 → 422、边 1062 → 409；`graph_entity_member` 缺表 / 缺列仍静默兼容；50303 仅 Java 层 |
| 12 | 历史 ENT 版本无快照 | 列表照常显示，回滚置灰 / 后端 409；`snapshot_status='none'` |
| 13 | 版本 `operator` 写死 `'py'`（`routes:844`） | 保存取 `change_set.operator`、回滚取 display 注入的 operator；历史 `'py'` 显示「系统（历史）」；`operator_display` 规则见 API/PRODUCT |
| 14 | 版本 `stats` 为 `{ops:N}` / 扁平四键（`routes:844`、`:852–858`） | 新版本用分组 JSON（§5.2）；历史行原样保留、不回填、缺组不补 0 |
| 15 | `impact` 只有实体计数 | 新增 `tech_edge_count`（工作集 active，双向）与 `panorama_hidden_relation_count`（entan 自有 Nebula 只读会话 + `USE demo_gkx_chain`，超时 `null`），后者引入 Nebula 只读依赖 |
| 16 | 快照 payload 无 `graph_tech_edge` / 坐标 | payload 新增 `graph_tech_edge`、`technology_master.layout_x/y`、`graph_entity_node.layout_x/y`、`rel_code`、`strength_auto`、`schema_version` |
| 17 | ENT 共用单测 / 文档未列 | **ENT 共用单测与文档更新**：`SituationMaintainEntControllerTest:49`（50301→50303）、`:70`（`publish("cs-1")` 签名）；`TechGraphMaintainControllerTest:72`（add_node/add_edge/delete_edge 由 400 改放行）、`:129/:137/:149`（50301 断言）、`:135`（publish 签名）；`PanoramaReadAssemblyTest` 补 `overlay` 与键集断言；`storage/ENT/stores/mysql/ads.md` + `CHANGELOG.md` 登记新表 / 新列；ENT-DATA 正文与 ENT 会签单追认 |

## 12. 会签关注点（v2 剩余）

1. **`stats` 键矩阵以 API v2 §3.4 为准**（已正式包含 `tech_edges.updated`）：本册按裁定 B1 给分组结构，`tech_edges.updated` 已纳入。
2. **`dim_tech_domain` 演示分类清单范围**（§6.8）：DATA 已给一版 12 类，需监管人确认是否够演示；分类体系选型仍是 `OI-C02-02` 待定项，不在本波冻结。
3. **50303 属 Java 层**（裁定 A5），DATA / entan-py 不产生该码；ENT 追记中的单测断言需 API / JAVA 同步（§11-17）。
4. **已关闭项**（不再关注）：`rel_code` 保留（B4）、端点 number 出参（B7）、Owner 确认（A1）、种子默认切片（A2）、快照阈值（A4）、1062 映射（B10）、回滚整表语义（B13）、`kind` / `operator` 来源（B16/B17）。

## 13. 不做 / 边界

- 不执行任何 DDL、不连库、不跑脚本、不建表、不灌数、不 git。
- 不改 `TS-L2-M10-ENT-DATA.md` 本体、ARCH、其他分册、`task-registry`；ENT 变化只在 §11 记档。
- 不注册 metric_id；计数类按 DN-A03-09 建议范围（七类）处理，待 PM / 数据 Lead 确认（§7.5）。
- 不做关系属性编辑、节点拖拽、技术点合并（需规无）；不把种子码映射成三枚举（只做只读显示字典，归 API/前端）。
- 不写 Nebula；不做审批流；不扩 41–47 的实体挂接叠加。
- 新表登记 `storage/ENT/stores/mysql/ads.md` + `CHANGELOG.md`、ENT 两册及会签单追认、`DS-02-MAINTAIN-GRAPH.yaml` 等属其他文件，列入影响清单，本册不改。

## 14. 会签回应

> 逐条回应裁定单 A/B、ARCH-DATA、API-DATA、ALGO-DATA、PROD-DATA。除 `API-DATA-C10` 外均采纳；部分建议按裁定单覆盖或调整为等价落法。

### 14.1 裁定单 A（监管人拍板）

| 条目 | 处置 | 落点 / 理由 |
|---|---|---|
| A1 名称唯一键不需 Owner | 采纳 | §3.2、§10、§12-4 |
| A2 种子默认切片 #2 | 采纳 | §6.2；#1 回归、#3 压测 |
| A3 分类维表下拉 / 空可手填 / 演示清单 | 采纳 | §6.3、§6.8 |
| A4 快照阈值 8MB/2000/50000、`--all` 禁用、每版保留 | 采纳 | §4.2、§4.3、§6.6、§8-G |
| A5 50303 仅 Java 层 | 记录 | §5.4、§12-3；DATA 不产生 |
| A6 时间范围选填 | 采纳 | §2.1、§6.3（`time_to` 允许 NULL） |
| A7 `client_batch_id` 可缺省 | 采纳 | §3.5、§5.5 |
| A8 DN-A03-09 七类、待 PM/数据 Lead | 采纳 | §7.5；写「建议范围」 |

### 14.2 裁定单 B（跨稿统一口径）

| 条目 | 处置 | 落点 / 理由 |
|---|---|---|
| B1 `stats` 分组 JSON | 采纳 | §5.2、§6.3、§8-H；历史不回填 |
| B2 坐标列名 `layout_x/y` | 已一致 | §3.1、§3.3、§8 |
| B3 35-3 Nebula 走 entan 只读会话 | 采纳 | §7.4 |
| B4 保留 `rel_code`，用于已删存量边过滤 | 采纳 | §2.1、§2.3、§4.2；**不采纳 API-DATA-C10 删除** |
| B5 种子跳过中文三枚举 / 自环 / 缺端点 | 采纳 | §6.1 |
| B6 人工边不带 `evidenceLevel` | 采纳（存储/读侧声明） | §2.1；无该列 |
| B7 `src/dst` 出参 number | 采纳 | §2.4；关闭 v1 §12-2 |
| B8 auto/manual 同行并存 | 采纳 | §2.1、§2.4 |
| B9 `strength_auto` 不出参、不进指标 | 采纳 | §2.1、§2.5、§7.5 |
| B10 1062：名称 422 / 边 409 | 采纳 | §5.4 |
| B11 publish 批次三态 / submit rejected / ops 不同 | 采纳 | §5.5 |
| B12 40-3/40-4 同键不同数据 | 采纳 | §5.3、§7.6 |
| B13 回滚整表 delete+insert、排除生成列/updated_at、同求差函数 | 采纳 | §5.3 |
| B14 种子 time_range 允许开放端、不补 to | 采纳 | §2.1、§6.1、§6.3 |
| B15 `tech_edge_count` 只数 active、双向 | 采纳 | §7.4 |
| B16 `kind`：ent 仅历史，新保存 `save` | 采纳 | §3.4、§5.2、§5.3 |
| B17 `operator` 来源 | 采纳 | §5.2、§5.3 |
| B18 ENT 追记清单 | 采纳 | §11（含单测、文档、7 op、operator、stats、名称、impact、payload） |
| B19 文案中文化 / 回滚双向语义 | 采纳（口径） | §3.4、§5.3；渲染归 API/FE |
| B20 「人工」标识 | 采纳（口径） | §2.1、§2.4；渲染归 FE |

### 14.3 ARCH-DATA

| 条目 | 处置 | 落点 / 理由 |
|---|---|---|
| ARCH-DATA-C1 `stats` 分组 | 采纳 | §5.2、§8-H |
| ARCH-DATA-C2 ENT 单测/文档追记 | 采纳 | §11-17 |
| ARCH-DATA-C3 `kind` 默认风险 | 采纳（保留默认 + 显式写 + 断言） | §3.4、§5.2、§8 注 |
| ARCH-DATA-C4 保留 `rel_code` | 采纳 | §2.1；用途按 B4 扩为过滤 |
| ARCH-DATA-C5 端点 number 出参 | 采纳 | §2.4；关闭 v1 §12-2 |

### 14.4 API-DATA

| 条目 | 处置 | 落点 / 理由 |
|---|---|---|
| C1 stats 分组 | 采纳 | §5.2 |
| C2 `kind` 语义 | 采纳 | §3.4、§5.2、§5.3 |
| C3 `operator` 来源 | 采纳 | §5.2、§5.3 |
| C4 publish 幂等三态 | 采纳 | §5.5 |
| C5 submit rejected / ops 不同 | 采纳 | §5.5 |
| C6 回滚 master delete-all、排除生成列/updated_at | 采纳 | §5.3 |
| C7 求差语义 / `tech_edges.updated` | 采纳 | §5.3；键以 API 最终稿为准 |
| C8 ENT 追记 5 类 | 采纳 | §11-13～17 |
| C9 1062 二义 | 采纳 | §5.4 |
| **C10 删除 `rel_code`** | **不采纳** | 裁定 B4 保留；API 不出参即可；删列会使已删存量边过滤失去锚点 |
| C11 `rel_type` 长度 / 中文码 | 采纳（放宽到 64 + 跳过中文） | §2.1、§6.1；不采用「>32 中止」，改按 B5 跳过 |
| C12 出参 number | 采纳 | §2.4 |
| C13 复活仅人工行 | 采纳 | §2.3 |
| C14 开放时间不复制 fallback | 采纳 | §2.1、§6.3 |
| C15 `strength_auto` 不出参 | 采纳 | §2.1、§2.5 |
| C16 N=1 措辞 + 存储增长 | 采纳 | §4.1、§4.3、§8-G |
| C17 回滚 `results` 取值 | 采纳 | §5.3-11 |
| C18 级联删边各记 change_log | 采纳 | §5.2-10、§5.5 |
| C19 master 权威 / payload 含主键 | 采纳 | §3.1、§4.1 |

### 14.5 ALGO-DATA

| 条目 | 处置 | 落点 / 理由 |
|---|---|---|
| C1 英文码白名单 / 中文码跳过 / 超占比中止 | 采纳 | §6.1-4 |
| C2 生成列不写入快照/还原 | 采纳 | §4.1、§5.3 |
| C3 stats 分组 | 采纳 | §5.2 |
| C4 自环 / 非 active / 缺端点丢弃 | 采纳 | §6.1-5 |
| C5 已删存量边用 `rel_code` 过滤 | 采纳 | §4.2 |
| C6 同 pair+type 聚合 | 采纳（`time_to=NULL` 按 B14） | §6.1-6 |
| C7 extra tnid/VID 跳过 + warning | 采纳 | §6.4（取代 v1「单独加入」） |
| C8 `strength_auto`/`rel_code` 守护 | 采纳 | §2.5、§7.5 |
| C9 `kind` 显式写 | 采纳 | §3.4、§5.2、§5.3 |
| C10 node_id_map 过滤 | 采纳 | §5.5 |
| C11 tech_edge 一次写入 | 采纳 | §5.2-11 |
| C12 1062 固定 | 采纳 | §5.4 |

### 14.6 PROD-DATA

| 条目 | 处置 | 落点 / 理由 |
|---|---|---|
| C1 回滚确认框双向语义 | 采纳 | §5.3 |
| C2 不可回滚原因 / 历史版本显示 | 采纳（口径） | §3.4 |
| C3 stats 与 API 统一 | 采纳 | §5.2、§8-H |
| C4 分类下拉数据源就绪 | 采纳 | §6.8 |
| C5 演示切片 #2 | 采纳 | §6.2 |
| C6 快照超限再回滚提示 | 采纳 | §4.2 |
| C7 `tech_edge` change_log 可展示数据 | 采纳 | §5.2-12 |
| C8 种子边强度只读展示 | 采纳（口径） | §6.3；出参归 API |

### 14.7 v2.1 清理

- 级联删边的 `reason` 改放 `change_log.after` JSON（`"reason":"cascade"`），不加列、不改 DDL（API-DATA-C18 / ALGO-N1）。
- 删除 `stats` 中关于 API 键矩阵的兜底条件句，API v2 §3.4 已正式包含 `tech_edges.updated`。
- `client_batch_id` 措辞按裁定 A7：前端生成；缺省时服务端生成、不享受重试幂等。
- `snapshot_status` 显示口径与回滚「移除 / 恢复 / 还原」用词对齐 API §4.1。
- 种子中文码明确「跳过并计数、不中止」；澄清「映射不到」含义与「先写主表取得 id，再写 ADS 节点/边」顺序。
- 仅改本册，未执行 DDL / 未连库 / 未 git。

---
*起草：`agent:data-agent` · 2026-11-13 · v2.1 · 会签条件已回应 · 未执行 DDL / 未连库 / 未 git*
