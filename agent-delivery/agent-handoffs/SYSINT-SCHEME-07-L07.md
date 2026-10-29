# SYSINT-SCHEME-07-L07 · 算法中台入图 schema 对齐存储设计

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 开工前由用户从花名册确认监管人。锁定 4 小时。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。未用 YAGNI 跳过可观测日志、幂等 `IF NOT EXISTS`、space 拒写和架构铁律（算法只在 Python，Java 不写 nGQL）。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ENT-STORAGE-FLOW`、`CHAIN-STORAGE-FLOW`、`POLICY-STORAGE-FLOW` |
| 图 diff | 未改图。未加边、未改虚线、禁止事项未变。不另画全局图。 |
| 会签态 | 三张 L2 frontmatter 均为 `approved` |
| 说明 | 代码对齐已会签流图和各域 `pipeline-to-nebula` 目标态。差异清单：`工程过程/04-系统集成/07-图数据库集成/对接文档/我方/SYSINT-SCHEME-07-L07-入图schema差异清单.md` |

## 范围

企业点列改成 `name, node_type, weight, props`。产业 A 档批量投影不再造企业点 / 机构点，也不再把 `enterprise_code` / `chain_role` 写进企业点。C 档挂边仍只走 `graph_ops` 的 `FETCH` + `INSERT EDGE participates`（`chain_role` 在边上）。政策点语句未改，已是 `policy(name, weight, props)`。服务机构仍 `DESCRIBE TAG institution` 后按列写，不新建 space。只写 `demo_gkx_chain`。初始化不再 `CREATE SPACE` / `DROP SPACE`。

## 改了的语句

| 文件 | 语句 |
|---|---|
| `demo-algo-science/chainan/graph/nebula_schema.py` | `TAG_DDL["enterprise"]` 改为 `name string, node_type string, weight double, props string`。`init_schema_from_code` 去掉 `CREATE SPACE`；space 不存在则 `RuntimeError`，已存在才 `CREATE TAG/EDGE IF NOT EXISTS` |
| `demo-algo-science/chainan/graph/nebula_project.py` `map_graph` | 去掉 `add_vertex(enterprise\|institution)` 和随之的 `INSERT VERTEX` / `participates`。`entity_rel` 计入 `skipped.entity_rel_fetch_only` |
| `demo-algo-science/chainan/graph/graph_ops.py` | 只删掉已无定义的 `_ext` 导入。A/B/C 的 INSERT 语句没改 |
| `demo-algo-ent-analysis/entan/graph/nebula_loader.py` | `ensure_schema` 去掉 `DROP SPACE` / `CREATE SPACE`。`USE demo_gkx_chain` 失败则拒绝。只 `CREATE TAG IF NOT EXISTS enterprise (name, node_type, weight, props)`。`_load_nodes` 只 `INSERT VERTEX enterprise(name, node_type, weight, props)`，其它 `node_type` 跳过。`_load_nodes` / `_load_edges` 先 `USE demo_gkx_chain` |
| `entan/yiji_sim/persist.py`、`entan/graph/incremental.py`、`entan/llm_ods/demo_graph.py` | 写会话改为 `use_space=False`，由 loader 切到 `demo_gkx_chain`。`render_ngql` 去掉 `CREATE SPACE`。删除顶点前 `USE demo_gkx_chain` |
| `entan/yiji_sim/pipeline.py`、`scripts/seed_demo_graph.py`、`entan/llm_ods/self_check.py` | 帮助文案和自检改为不承诺建库，space 断言为 `demo_gkx_chain` |

## 未改及原因

| 位置 | 原因 |
|---|---|
| `entan/graph/ops.py` 的 `CREATE TAG` / `ALTER TAG ADD (node_type)` / `INSERT VERTEX enterprise(name, node_type, weight, props)` | `ae16471` 已是企业四列，A 档不挂边。本单不把它当成产业链已对齐 |
| `graph_ops.py` 的 `INSERT VERTEX chain/segment`、`FETCH PROP ON *`、`INSERT EDGE participates(chain_role, ...)` | 已符合 CHAIN §17.4。`chain_role` 在边列上 |
| `polan/graph/nebula_loader.py` 的 `INSERT VERTEX policy(name, weight, props)` 与四边 `(weight, props)` | 点列已对齐。边列跟 pipeline §4 as-built，不跟 `stores/nebula.md` 未采纳的 `factor_type` / `src_table`（`OPEN-POLICY-GRAPH-03`） |
| `entan/svcgraph.py` | 已是 DESCRIBE 有则写、不新建 space。VID 仍 `institution:`，目标 `inst:` 在 `OPEN-SVC-GRAPH-02`，本单口径不迁点 |
| `chain` / `segment` / `institution` / `belongs_to` / `depends_on` / `participates` / `supplies` 列名 | 链上列与企业点四列不是同一件事 |
| 灌数 `run_all` / `run_seed` | 已经不调用这些写图模块，没有接回去 |
| `project_from_dwd` 的 `CLEAR SPACE`（`replace=True`） | 不是 `CREATE/DROP SPACE`。灌数已不调用该函数。菜单 C 档不走它 |
| 存储设计文档、`DATA-CHAIN-db-design.md` §7 | 冲突只记在差异清单 §5，不改那些文档 |

## 存储设计内部冲突

1. `DATA-CHAIN-db-design.md` §7.1 企业 Tag 含 `enterprise_code`、`chain_role`。代码以 ENT pipeline 目标态为准，不写进企业点。
2. CHAIN pipeline §4 as-built DDL 仍印着旧企业列；§14.4 / §17.4 规定不造企业点。代码跟后者。
3. POLICY `stores/nebula.md` 边列与 loader 的 `(weight, props)` 不一致，维持 loader，不改文档。

## 测试结果

- `demo-algo-science`：`py -3 -m pytest tests/test_chain_nebula_schema.py tests/test_chain_graph_ops.py -q` → 24 passed
- `demo-algo-ent-analysis`：`py -3 -m pytest tests/test_entan_graph_ops.py tests/test_policy_nebula.py -q` → 17 passed
- 锁住的列名：企业 Tag / `INSERT VERTEX enterprise` 为 `name, node_type, weight, props`；语句中不得 `CREATE SPACE` / `DROP SPACE`；`map_graph` 不再把 `entity_rel` 写成企业点或 `participates`

未连真实 graphd。space 不存在时的拒绝是假会话单测，不是现网 `USE`。

## 架构合规

| 铁律 | 结果 |
|---|---|
| 算法只在 Python，Java 不写 nGQL | 保持 |
| 只写 `demo_gkx_chain`，不写 `gkx_chain` | 保持；缺 space 拒绝建库 |
| 可观测 | 沿用现有 logger；企业菜单路径的 tracer 在 `ops.py`，本单未拆 |
| 幂等 | `CREATE TAG/EDGE IF NOT EXISTS`；同 VID 的 `INSERT` 覆盖。`rebuild=True` 改为拒绝删库 |

## 遗留

- 已存在的 `enterprise` Tag 若仍带 `enterprise_code` / `chain_role`，`CREATE TAG IF NOT EXISTS` 不会改旧列。企业菜单写入仍只列四列，并在缺 `node_type` 时 `ALTER TAG ADD`。旧列留在 Tag 上，插入未列出的列回到默认值。
- yiji `--rebuild` 现在直接拒绝，不再清图。
- 服务机构 VID 前缀未改。

## CI/CD

- 分支：`dev`（`demo-algo-science`、`demo-algo-ent-analysis`、`gkx-orchestration`）
- commit：见各仓本次提交
- pipeline：push 后由 GitLab 跑；本机未等绿
- 部署：未触发 rollout 验收

## 成本

- actual_tokens: 未单列（随会话）
- model_used: grok-4.7
- actual_cost: 未单列
- cost_warn: false

## 涉及文件

- 差异清单与本 handoff（编排仓）
- 上表代码与单测
