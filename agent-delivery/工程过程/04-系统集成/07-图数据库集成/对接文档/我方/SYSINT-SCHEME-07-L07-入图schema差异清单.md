# SYSINT-SCHEME-07-L07 · 入图 schema 差异清单

> 对照日：2026-10-30。清单先落盘，随后按第 3 节改了代码。认领：`agent:algorithm-agent`，监管人 `human:淮政玮`。
> ponytail: full
> diagram_id: `ENT-STORAGE-FLOW`、`CHAIN-STORAGE-FLOW`、`POLICY-STORAGE-FLOW`（另参考 `SVC-STORAGE-FLOW`）
> 图 diff: 无。三张 L2 会签态均为 `approved`，本单不改图、不另画全局图。
> 真源：`diagram-as-contract.md`；各域 `pipeline-to-nebula.md` 目标态。存储设计文档本单不改。

## 1. 目标态（改代码以此为准）

| 对象 | 目标 | 出处 |
|---|---|---|
| space | 只写 `demo_gkx_chain`。禁止 `CREATE SPACE` / `DROP SPACE`。禁止写 `gkx_chain` 与正式库 | 本单边界；ENT §3.2 / CHAIN §3 / POLICY §3 |
| 企业点 | Tag `enterprise` 列 `name, node_type, weight, props`。VID `ent:{org_id}`。A 档 `ENT_NER_ORG` 只建点，不挂边 | ENT §4、§17.1、§17.4 |
| 产业点 | A 档 `CHAIN_NER_INDUSTRY` 只 `INSERT VERTEX chain` / `segment` | CHAIN §14、§17.1、§17.4 |
| 链内边 | B 档 `belongs_to`、`depends_on`。`supplies` 本波不上图 | CHAIN §14.1–§14.3 |
| 产业–企业 | C 档先 `FETCH` 已有 `ent:`，再 `INSERT EDGE participates` 到 `chain:` 或 `segment:`。禁止把 `enterprise_code`、`chain_role` 写进企业点。`chain_role` 留在边 `participates` 上 | CHAIN §14.4、§17.4；本单口径 |
| 政策点 | `policy(name, weight, props)`。不新建 `enterprise` 点 | POLICY pipeline §4；`stores/nebula.md` Tag 行 |
| 服务机构 | 复用 `institution`。`DESCRIBE` 有列才写。不新建 space | `graph-svc.md`；SVC pipeline §4 |

## 2. 现网谁在写点、谁在写边

| 模块 | 语句 | 写什么 | 和目标态 |
|---|---|---|---|
| `demo-algo-ent-analysis/entan/graph/ops.py` | `CREATE TAG IF NOT EXISTS enterprise (name string, node_type string, weight double, props string)`；缺 `node_type` 时 `ALTER TAG enterprise ADD (node_type string)`；`INSERT VERTEX enterprise(name, node_type, weight, props)` | 企业 A 档只写企业点。`ENT_NER_ORG` 的 `written_edges` 为空。边走 B/C，列是 `(weight, props)`。space 常量 `demo_gkx_chain`，本文件无 `CREATE/DROP SPACE` | 企业点列已对齐（`ae16471`）。不是全量闭合 |
| `demo-algo-science/chainan/graph/nebula_schema.py` `TAG_DDL["enterprise"]` | `CREATE TAG IF NOT EXISTS enterprise (name string, enterprise_code string, chain_role string, weight double, props string)` | 图谱初始化会把企业点建成产业链列 | **不一致** |
| 同文件 `init_schema_from_code` | space 不存在时 `CREATE SPACE demo_gkx_chain (...)` | 建库 | **本单禁止**。灌数 `run_seed` / `run_all` 已不调用它；初始化菜单和 `graph_ops._open_write_sess` 仍调用 |
| `demo-algo-science/chainan/graph/nebula_project.py` `map_graph` | `add_vertex("enterprise", ... enterprise_code, chain_role ...)` 后 `upsert` → `INSERT VERTEX enterprise(name, enterprise_code, chain_role, weight, props)` | 批量投影造企业点，并把角色写在点上。同一循环也 `add_vertex("institution", ...)` | **不一致**。CHAIN §14.4：不 `INSERT VERTEX enterprise\|institution` |
| `demo-algo-science/chainan/graph/graph_ops.py` | A：`INSERT VERTEX` 只有 `chain` / `segment`。C：`FETCH PROP ON *` 未命中则 `no_stable_id`，命中才 `INSERT EDGE participates(chain_role, participation_depth, chain_score, props)` | 不造企业点。`chain_role` 在边上 | 写入已对齐。它仍调用 `init_schema_from_code`，会带上错误的企业 Tag DDL |
| `demo-algo-ent-analysis/polan/graph/nebula_loader.py` | `CREATE TAG IF NOT EXISTS policy (name string, weight double, props string)`；`INSERT VERTEX policy(name, weight, props)`；四边 `INSERT EDGE {support\|apply_to\|regulate\|cite}(weight, props)`。企业/产业只 `FETCH`，不 `INSERT VERTEX enterprise` | 政策点 | 点列已对齐。无 `CREATE/DROP SPACE` |
| `demo-algo-ent-analysis/entan/svcgraph.py` | 无 `CREATE SPACE` / `CREATE TAG`。`SHOW TAGS` + `DESCRIBE TAG institution`，有列才 `INSERT VERTEX institution(...)`。VID 现网 `institution:{org_id}` | 服务机构点 | 与「复用 institution、DESCRIBE 有则写、不新建 space」一致。目标 VID `inst:` 见开放项，本单不改前缀 |
| `demo-algo-ent-analysis/entan/graph/nebula_loader.py` | `rebuild` 时 `DROP SPACE IF EXISTS`；随后 `CREATE SPACE IF NOT EXISTS`。`INSERT VERTEX {tag}(name, node_type, weight, props)`，tag 含 `enterprise` 以及 `industry` / `research` / `talent` / `service` / `chain_node` / `technology`。默认 space 来自配置，缺省 `demo_entan` | yiji / `persist_graph` / `incremental` / `demo_graph` 仍进这里。中台 A/B/C 菜单走 `entan/graph/ops.py`，不走本文件 | 企业点四列与目标相同，但 **会建库删库**，且会在图上补第二套 Tag。ENT §4 目标禁止 |

灌数：`demo-algo-science/scripts/run_all.py` 与 `chainan/llm_ods/seed.py` 不调用 `project_from_dwd` / `init_schema_from_code`。企业仓 `run_all` 不调用 `nebula_loader` / `svcgraph` / `entan.graph.ops`。这条保持，不把写图接回灌数。

## 3. 要改的语句

1. `chainan/graph/nebula_schema.py`  
   企业 Tag 列改为 `name string, node_type string, weight double, props string`。  
   `init_schema_from_code` 去掉 `CREATE SPACE`。space 不存在则拒绝，不建库。仍只 `USE demo_gkx_chain`，仍 `CREATE TAG/EDGE IF NOT EXISTS`（`chain` / `segment` / `institution` 与四类边保持 CHAIN §4 的链上列；企业 Tag 用上面的四列，避免初始化先把错误列建出来）。

2. `chainan/graph/nebula_project.py` `map_graph`  
   去掉对企业点、机构点的 `add_vertex`。不再生成带 `enterprise_code` / `chain_role` 的 `INSERT VERTEX enterprise`。  
   `entity_rel` 不在这条批量投影里落 `participates`（没有 FETCH，不能假装对端已在）。计数跳过。  
   `chain` / `segment` / `belongs_to` / `depends_on` 仍由本函数写出。  
   C 档挂边只留 `graph_ops` 的 FETCH + `INSERT EDGE participates`。

3. `entan/graph/nebula_loader.py` `ensure_schema`  
   去掉 `DROP SPACE` 与 `CREATE SPACE`。space 不是 `demo_gkx_chain` 则拒绝。  
   不再 `CREATE TAG` `industry` / `research` / `talent` / `service` / `chain_node` / `technology`（ENT §4：禁止企业侧第二套本体）。企业点若要补，只允许与 `ops.py` 相同的四列 `IF NOT EXISTS`。

单测改锁：企业 Tag 列名是 `name, node_type, weight, props`；产业链语句里不得出现 `INSERT VERTEX enterprise` 带 `enterprise_code` / `chain_role`；`init_schema_from_code` 与企业 `ensure_schema` 不得 `CREATE SPACE` / `DROP SPACE`。现有 `test_missing_space_creates_then_schema`、`test_schema_names_match_graph_chain` 里对企业列的假定、`test_seed_projection` 里 `participates == 1` 且来自造点的断言，随代码改。

## 4. 已对齐，本单不改这些语句

| 位置 | 原因 |
|---|---|
| `entan/graph/ops.py` 的 `CREATE TAG` / `ALTER TAG` / `INSERT VERTEX enterprise(name, node_type, weight, props)` | 已是企业四列。A 档不挂边。不把 `ae16471` 当成产业链、政策、服务机构已闭合 |
| `chainan/graph/graph_ops.py` 的 A 档点、B 档 `belongs_to`/`depends_on`、C 档 `FETCH` + `participates` | 与 CHAIN §17.4 一致。`chain_role` 在边列上，不在企业点上。schema 初始化改列后，这里不用再写一套 INSERT |
| `polan/graph/nebula_loader.py` 的 `INSERT VERTEX policy(name, weight, props)` 与四边 `(weight, props)` | 点列已是目标。边列跟 POLICY pipeline §4 的 as-built，不跟 `stores/nebula.md` 里未采纳的 `factor_type` / `src_table` / `relation`（见 §5） |
| `entan/svcgraph.py` 的 `DESCRIBE TAG institution` 与按列插入 | 已是「有则写、不新建 space」。VID 前缀仍是 `institution:`，目标 `inst:` 记在 `OPEN-SVC-GRAPH-02`，本单口径没有要求迁点 |
| `chain` / `segment` / `institution` / `belongs_to` / `depends_on` / `participates` / `supplies` 的链上列 | CHAIN §4 这些列与「企业点四列」不是同一件事。本单只改企业点列，不改链上点边的列名 |
| 灌数 `run_all` / `run_seed` | 已经不调用写图模块 |

## 5. 存储设计内部冲突（只记录，不改那些文档）

1. `agent-handoffs/产业链分析-CHAIN/DATA-CHAIN-db-design.md` §7.1  
   `CREATE TAG enterprise (name, enterprise_code, chain_role, weight, props)`。  
   与 ENT pipeline §4 / §17 的企业四列冲突。代码以 pipeline 目标态为准：企业点不写 `enterprise_code`、`chain_role`。

2. CHAIN `pipeline-to-nebula.md` §4 的 as-built DDL 仍印着同一套企业列；同文件 §14.4 / §17.4 的目标态是不造企业点、只 FETCH 后写 `participates`。  
   代码跟 §14.4 / §17.4，不跟 §4 那段 as-built 企业列。

3. POLICY `stores/nebula.md`「本波 DDL」把四边写成 `support(weight, factor_type, src_table)` 等；同文件与 pipeline §4 写明 loader 实际是 `(weight double, props string)`，属 `OPEN-POLICY-GRAPH-03`，升级 `human:淮政玮`。  
   本单不改边列，不改该文档。

4. SVC pipeline §3：现网 VID `institution:{org_id}`，目标 `inst:{org_id}`（`OPEN-SVC-GRAPH-02`）。`graph-svc.md` 只要求复用 `institution`、不新建 space。本单按后者，不改前缀。
