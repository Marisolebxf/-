# TS-L2-DS02-ENTITY-DATA · 科学技术全景 · 展示技术点关联实体 · 数据落点

- 任务：`TS-L2-DS02-ENTITY-DATA`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`（兼 data 分册）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 2026-11-07 复查：图上已有技术点连实体的边。样本 `tcn_000f21ac06aceb9cdd0575e82d0d85fc` 用 `technology_node_id` 直调 Python 读图：实体 61（论文 13、专利 20、机构 20 截断、人 8），实体中文名为空。influence 252363 行。正文 11-05 的现状保留作记录，以本行为准。见 `工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-ENTITY-合规演示用例.md`
- 强度：ponytail off（定义任务，不缩文档）
- 上游：`sdd/科学技术全景-系统详细设计说明书.md` §2.2、§4；`sdd/l2/TS-L2-DS02-ARCH.md` §3、§7；`方案-算法中台基础数据准备.md`（Tag / VID / Edge 命名）
- 代码核对：`lumen-algo-py` `lumen_common/algorithms/tech_graph_read.py`（HEAD `07ffa9f`）、`scripts/mysql/ads_technology_panorama_score.sql`；`lumen-svc-platform` `JdbcPanoramaScores`

本叶只写序号 22–27 读哪些数、落在哪。不写 SQL、nGQL、DDL 变更。图由 `SYSINT-TECHGRAPH-02` 写入，本页只读。

## 1. 两个数据源

| 源 | 位置 | 本二级读什么 | 写入方 |
|---|---|---|---|
| 技术点图 | Nebula 空间 `demo_gkx_chain` | 选中技术点的人、机构、论文、专利 | `SYSINT-TECHGRAPH-02-L01`（点）、`SYSINT-TECHGRAPH-02-L02`（边） |
| 分数表 | MySQL `demo_gkxlumenx_ads.ads_technology_panorama_score` | 实体影响力 | `TS-L2-DS02-SCORE-L01`（D18 mock） |

不读 `gkx_chain`、`entan`，不读 ODS、DWD、供应方库，不用 `gapfill_` 表，不读 `mock/modules/panorama.ts`。

## 2. 图上的点

VID 规则沿 `方案-算法中台基础数据准备.md`：`{Tag}:{业务编号}`。

| 实体 | Tag | VID | 读图取的顶点属性 |
|---|---|---|---|
| 技术点 | `tech_point` | `tech_point:` + `technology_node_id` | `technology_node_id`、`name_zh`、`name_en`、`community_role`、`weighted_degree` |
| 论文 | `tech_paper` | `tech_paper:` + `paper_id` | `paper_id`、`name_zh`、`name_en`；WHERE 用 `technology_node_id` |
| 专利 | `tech_patent` | `tech_patent:` + `patent_id` | `patent_id`、`name_zh`、`name_en`；WHERE 用 `technology_node_id` |
| 机构 | `tech_institution` | `tech_institution:` + `institution_id` | `institution_id`、`name_zh`、`name_en`；WHERE 用 `technology_node_id` |
| 人 | `tech_person` | `tech_person:` + `talent_id` | `talent_id`、`name_zh`、`name_en`、`source_paper`、`source_topic` |

`source_paper`、`source_topic` 是人顶点上的来源标记（论文一路、Topic 一路），读图转成布尔。

## 3. 技术点连实体的边

| 边 | 两端 | 读图取的边属性 | 强度 | 年份 |
|---|---|---|---|---|
| `tech_has_paper` | `tech_point` — `tech_paper` | 无 | 无 | 无 |
| `tech_has_patent` | `tech_point` — `tech_patent` | 无 | 无 | 无 |
| `tech_has_institution` | `tech_point` — `tech_institution` | 无 | 无 | 无 |
| `tech_has_person` | `tech_point` — `tech_person` | 无 | 无 | 无 |

读法：`MATCH (a:tech_point)-[e:tech_has_*]-(v:实体Tag) WHERE id(a) == "tech_point:{id}" OR a.tech_point.technology_node_id == "{id}"`，不限方向，`LIMIT 21`。论文、专利、机构另有一路按顶点属性 `v.{Tag}.technology_node_id == "{id}"` 扫，两路按 vid 去重。

读图对这四种边**不取任何边属性**。所以：

- 序号 22、27 的「关联强度」没有来源，页面为空，按名称兜底。
- 序号 25 的时间筛选没有年份可用，不截数据。
- 序号 24 的时间线为空。

对照：技术点之间的 `tech_rel` 读图取 `relation_type`、`evidence_level`、`relation_confidence_score`（→ `weight`）、`first_evidence_year`（→ `year`）。这些只属于技术点关系，不用于实体。

`tech_has_person` 的来源标记按方案写在边上；读图读的是人顶点上的 `source_paper` / `source_topic`。L02 落边时若只写在边上，人的来源标记会读空。

写边规格已在代码里：`lumen-algo-py` `tech_graph.py` `_EDGES` 定 `tech_has_paper`、`tech_has_patent`、`tech_has_institution` 无属性，`tech_has_person` 只有 `source_paper`、`source_topic`（布尔）。四种边都不带强度和年份。L02 按这份规格落边，强度、年份仍是空。要加须先改写边规格（归 `SYSINT-TECHGRAPH-02-L02`），再由读图同步取。`TS-L2-DS02-READ-PY-L01` 已 done，读图补取未建单。

## 4. 分数表

DDL 在 `lumen-algo-py` `scripts/mysql/ads_technology_panorama_score.sql`。

| 列 | 类型 | 约束 | 含义 |
|---|---|---|---|
| `subject_id` | VARCHAR(128) | NOT NULL，主键之一 | 读图返回的技术点、实体或路径编号 |
| `score_kind` | VARCHAR(32) | NOT NULL，主键之一；CHECK 闭集 | `influence` / `centrality` / `path_priority` |
| `score_value` | DOUBLE | NOT NULL | D18 mock 数，不是注册公式输出 |

| 项 | 值 |
|---|---|
| 主键 | (`subject_id`, `score_kind`) |
| 引擎 / 字符集 | InnoDB，utf8mb4，utf8mb4_unicode_ci |
| 建表 | `CREATE TABLE IF NOT EXISTS`，幂等 |
| 灌数 | `scripts/seed/seed_technology_panorama_score.py --apply`；按三列先删后插，可重复 |
| 本二级读 | `score_kind=influence`，`subject_id` ∈ `paper_id` / `patent_id` / `institution_id` / `talent_id` |
| 读法 | `gkxlumen-display` 只读连接，`WHERE subject_id IN (...)`，一次最多 400 个编号 |

库不在 ODS、DWD、供应方库，表名无 `gapfill_` 前缀。属 D18 结果表，D4 保持 mock。

## 5. 现状（截至 2026-11-05，另注 2026-11-06 代码变化）

| 项 | 事实 |
|---|---|
| 技术点点 | `tech_point` 19,430 |
| 实体点 | 论文 108,337；专利 126,484；机构 17,542；人 0 |
| 技术点连实体的边 | 0。图上没有 `tech_has_*`，也没有 `tech_rel`、`tech_path_step` |
| 写边任务 | `SYSINT-TECHGRAPH-02-L01` 进行中（点）；`SYSINT-TECHGRAPH-02-L02`（边、路径、关联实体）backlog |
| 按属性 WHERE | 2026-11-05：`v.{Tag}.technology_node_id ==` 扫描报 `IndexNotFound`，属读图查询缺口，归 `lumen-algo-py`。2026-11-06 `07ffa9f` 改为当空，继续走边查 |
| 分数表 | 271,793 行：`influence` 252,363，`centrality` 19,430，`path_priority` 0 |
| 人物影响力 | 0 行 |

结论：选中任一技术点，实体名单为空，影响力无对象可填。等 L02 落边后，实体名单才有数。

## 6. 落边后要核的三件事

1. 边名是否就是 `tech_has_paper` / `tech_has_patent` / `tech_has_institution` / `tech_has_person`。名字不同，读图取空。
2. 边上是否带强度与年份，属性名是什么。读图要按实际名补取。
3. 实体编号是否与分数表 `subject_id` 一致（`paper_id` 等）。不一致，影响力全空。
4. `subject_id` 不带类型前缀，论文、专利、机构编号若同串会落到同一行。现在 mock 值只由 (`score_kind`, `subject_id`) 决定，撞号时数值相同，不串值；接真算前须加类型维或前缀。

## 7. 不做

- 不写边，不建实体间关系表。
- 不给人物灌影响力，不另造编号。
- 不改分数表结构，不把 mock 行写成正式值。
- 不改 `dwd_technology_topic_industry` 等挂产业表。
