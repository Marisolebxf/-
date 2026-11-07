# TS-L2-DS02-PATH-DATA · 科学技术全景 · 展示关键路径和关键节点 · 数据落点

- 任务：`TS-L2-DS02-PATH-DATA`
- 日期：2026-11-07
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`（arch-agent 代写）
- 强度：ponytail off（定义任务，不缩文档）
- 状态：as-built 稿已落盘；四角色已会签（`sdd/l2/会签/TS-L2-DS02-L2SET-SIGNOFF-*.md`），未签收
- 2026-11-07 复查：图上已有路径步。样本 `tcn_000f21ac06aceb9cdd0575e82d0d85fc` 用 `technology_node_id` 直调 Python 读图：路径 2 条（三步、两步）。`path_priority` 仍 0 行，可按原灌数脚本重跑补齐。正文 11-05 的现状保留作记录，以本行为准。见 `工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-PATH-合规演示用例.md`
- 上游：说明书第 4 节；`sdd/l2/TS-L2-DS02-ARCH.md` 第 3、7 节；`方案-算法中台基础数据准备.md` 第 2 项；`sdd/l2/TS-L2-DS02-PATH-ARCH.md`
- as-built 依据：`lumen-algo-py` `lumen_common/algorithms/tech_graph.py`（写边规格）、`tech_graph_read.py`（读图）、`scripts/mysql/ads_technology_panorama_score.sql`、`scripts/seed/seed_technology_panorama_score.py`（`828315a`）

本叶只写序号 **28–33** 读到的数据在哪、长什么样。不写 SQL，不改表，不灌数，不改图。

## 1. 两处数据

| 数据 | 存储 | 谁写 | 谁读 |
|---|---|---|---|
| 路径步与端点 | Nebula 空间 `demo_gkx_chain`：Tag `tech_point`，Edge `tech_path_step` | `SYSINT-TECHGRAPH-02-L02`（边与路径上图） | `lumen-algo-py` `POST /internal/tech-graph/read` |
| 中心度、路径优先级 | MySQL `demo_gkxlumenx_ads.ads_technology_panorama_score` | `TS-L2-DS02-SCORE-L01` 灌数脚本 | `gkxlumen-display` `JdbcPanoramaScores` 只读 |

本页不写这两处。

## 2. 图：`demo_gkx_chain`

只读这个空间。请求或环境里是别的空间（`gkx_chain`、`entan`、`demo_entan` 等）一律拒绝。

### 2.1 路径步边 `tech_path_step`

| 项 | 值 |
|---|---|
| 边名 | `tech_path_step`（读图与写边代码一致） |
| 方向 | `tech_point` → `tech_point` |
| 起点键 | 上游行的 `previous_technology_node_id` |
| 终点键 | 上游行的 `technology_node_id` |
| 属性 | `path_id`（string）、`step_order`（int） |
| rank | `10 + crc32("{path_id}:{step_order}") % 1e9`。同一对点可在多条路径上各有一条边 |
| 上游来源 | `ads_technology_evolution_path_step` 的相邻步（`方案-算法中台基础数据准备.md` 第 73 行）。这是路径序列，不是 `tech_rel` |
| VID | 端点 vid 为 `tech_point:{technology_node_id}` |

步序：读图按 `step_order` 升序排。首步取起点，之后每步取终点，组成 `nodes[]`。`step_order` 不是数字时按 0 处理。

路径编号：`path_id` 为空时，读图与灌数脚本都用 `{起点 id}->{终点 id}` 代替。两处规则相同，所以分数行仍能对上。

### 2.2 端点属性（`tech_point`）

| 属性 | 用于 |
|---|---|
| `technology_node_id` | 端点编号，也是分数表 `subject_id` |
| `name_zh` | 端点名。空就空，不抄英文 |
| `name_en` | `name_zh` 空时作显示名 |
| `community_role` | 关键节点样式（`role`） |
| `weighted_degree` | 关键节点样式与强度（`strength`） |

### 2.3 读取范围

只读与选中技术点直接相连的步（选中点为起点或终点）。单次 `LIMIT 168`。按 `path_id` 归组后最多 20 条。不按 `path_id` 回查同一路径上的其他步。

## 3. 分数表 `ads_technology_panorama_score`

| 项 | 值 |
|---|---|
| 库 | `demo_gkxlumenx_ads`（`10.50.11.76:3306`） |
| 性质 | D18 mock 结果表。不在 ODS、DWD、供应方库，表名无 `gapfill_` 前缀 |
| 主键 | (`subject_id`, `score_kind`) |
| 字符集 | `utf8mb4` / `utf8mb4_unicode_ci` |

| 列 | 类型 | 说明 |
|---|---|---|
| `subject_id` | VARCHAR(128) NOT NULL | 读图返回对象的 `id` |
| `score_kind` | VARCHAR(32) NOT NULL | CHECK 闭集 `influence`、`centrality`、`path_priority` |
| `score_value` | DOUBLE NOT NULL | mock 数，不是注册公式输出 |

本二级用到的两种：

| score_kind | subject_id 取自 | 值域 | 对应 metric_id |
|---|---|---|---|
| `centrality` | 技术点 `technology_node_id` | 40.000–48.999 | `M_TECH_PATH_CENTRALITY` |
| `path_priority` | 路径 `path_id`（或 `{起点}->{终点}`） | 70.000–78.999 | `M_TECH_PATH_PRIORITY` |

`influence` 属于关联实体功能，不在本二级。

### 3.1 灌数规则（as-built）

- 数值：`基数 + (sha256("{kind}\n{subject_id}") 前 2 字节 % 9000) / 1000`，保留 3 位。同编号同种类重复跑得到同一个数。
- 技术点：按 vid 分页扫全部 `tech_point`，每页 8000。扫到的数与 `count` 不一致则不灌。
- 路径：扫全部 `tech_path_step`，按 `path_id` 归组，每条路径一行。不受读图 20 条上限限制。
- 写法：三种 `score_kind` 先删后插，每批 500 行，一个事务。失败回滚。
- 口令：MySQL 读 `LUMEN_ALGO_MYSQL_PASSWORD`，Nebula 读 `GKX_CHAIN_NEBULA_PASSWORD`；没有则读仓内已有配置。不写进脚本。
- 不在 `graph` 请求里写表。`--check` 会核对读图代码里没有出现表名。

## 4. 现状（截至 2026-11-05）

| 项 | 现状 |
|---|---|
| `tech_point` | 19430 |
| `tech_path_step` | 0。边类型里没有这条，`tech_rel`、`tech_has_*` 也没有 |
| `centrality` 行 | 19430 |
| `path_priority` 行 | 0 |
| `SYSINT-TECHGRAPH-02-L01`（点入图） | in_progress |
| `SYSINT-TECHGRAPH-02-L02`（边、路径、关联实体） | backlog |

路径步由 `SYSINT-TECHGRAPH-02-L02` 写入。写入后要做两件事：重跑 `seed_technology_panorama_score.py --apply` 补 `path_priority`；用读图实测路径能带回。

## 5. 边界

- 不用演示种子 `mock/modules/panorama.ts` 的路径灌图，不在接口返回种子路径。
- 不读 `gkx_chain`、`entan`，不读燕大产业链全景。
- 路径步不进分数表。分数表只放数字。
- 本页不写 `ads_technology_evolution_path_step`，不写挂产业表。
- 不加列，不改 `score_kind` 闭集。

## 6. as-built 风险（只登记）

- 读图选中键与 Java 不一致（Java 发 `techPointId`），完整链路下即使 L02 写入路径，Python 也不会查路径步。见 `TS-L2-DS02-PATH-ARCH` 第 8 节，归 `TS-L2-DS02-SEL-FIX-L01`。
- 读图只带与选中点相连的步。灌数按整条路径给 `path_priority`，但页面看到的是局部路径。两者编号相同，分数仍能对上。
- `path_id` 若在 L02 写入时为空，路径编号退为单步 `{起点}->{终点}`，一条长路径会被拆成多条。L02 须保证 `path_id` 非空。
