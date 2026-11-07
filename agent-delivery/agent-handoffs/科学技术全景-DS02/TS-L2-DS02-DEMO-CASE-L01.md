# TS-L2-DS02-DEMO-CASE-L01 · 科学技术全景 · 合规演示用例与 LOOP 计划

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:qa-agent`（协作 data / api） |
| supervised_by | `human:淮政玮` |
| 说明 | 本会话按派单不碰 task-registry、不 git commit、不改代码、不写库、不打开页面。状态推进与 cost 字段回填由 coordinator 经 MCP 完成 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 只写规程 §6.4 / §6.5 要求的文档；没有新增脚本或代码。取数用一次性 pod 内只读脚本，跑完即删 |

## 范围与实现

按 `agent-delivery/产品实现规程.md` §6.4（合规演示用例）与 §6.5（LOOP），为展示系统「科学技术全景」（`/trend/tech-panorama`，需规序号 17–33，对照 `bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md`）写三份用例、一份索引、三份 LOOP 计划。

- 需规每条至少一行；同一序号部分能演、部分缺数据时拆成「可演」与「覆盖不到」两行，参照专题样板 `区域政策对比-合规演示用例.md` 的拆法。
- 接口地址一律写展示网关 `POST /display/v1/situation/panorama/graph`（17 写 `/import`，26 写 `/entity-relations`）。请求体字段按 `sdd/l2/TS-L2-DS02-{GRAPH,ENTITY,PATH}-API.md` 的页面实发字段（`selectedNodeId`、`keyword`、`selectedFieldValues`、`currentYear`）。
- 期望值当日取自集群内 Python 读图与分数表只读查询，用例里注明「网关一跳由 LOOP 首探核对」。
- 选中点断点（Java `techPointId` / Python `technology_node_id`）：依赖选中点的行按数据本身定为可演，加脚注挂 `TS-L2-DS02-SEL-FIX-L01`；LOOP 计划把它归 QUERY。

### 各二级计数

| 二级 | 可演 | 覆盖不到 | 设计无资源 |
|---|---|---|---|
| GRAPH 17–21 | 6：18 节点、18 连线 ¹、19 ¹、20 模糊、20 精确、21 名称与属性 | 1：21 描述与发展状态 | 1：17 |
| ENTITY 22–27 | 5：22 选点后 Top5 ¹、23 ¹、24 基本属性 ¹、25 按类型 ¹、27 按影响力名称类型 ¹ | 4：22 初始化与关联强度、24 描述时间线统计、25 按时间、27 按强度时间 | 1：26 |
| PATH 28–33 | 5：28 节点序列 ¹、29、30 步序与端点 ¹、32 ¹、33 ¹ | 3：28 重要性、30 正文、31 | 0 |

¹ 待 `TS-L2-DS02-SEL-FIX-L01`。不选点就能演、不受断点影响的：18 节点、20 模糊、20 精确、21 名称与属性、29。

## 偏离

- 没有打展示网关：本机没有 `display-loop-token`。期望值来自 pod 内 `POST /internal/tech-graph/read` 与分数表，网关条数（Java 200 上限、`truncated` 透出）留给 LOOP 首探记录。
- 20 精确那一笔没有单独打：期望只写「含 `tcn_fceeb0c7…`、不多于 190 条」，条数由首探记录，不写死。
- 实体行 `name_zh` 抽查为空，名称退为编号；用例照实写，22 的名称与关联强度另拆为覆盖不到。
- 人（`tal_*`）的影响力当日未逐个核对；`TS-L2-DS02-SCORE-L01` 记人未灌，用例写「无分数行不进影响力档」。

## 产物清单

根 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/`：

- `合规演示用例/TS-L2-DS02-GRAPH-合规演示用例.md`
- `合规演示用例/TS-L2-DS02-ENTITY-合规演示用例.md`
- `合规演示用例/TS-L2-DS02-PATH-合规演示用例.md`
- `合规演示用例/科学技术全景-索引.md`（注明 34–40 报价划掉不写、41–47 归维护管理另走）
- `编排计划/TS-L2-DS02-GRAPH-LOOP计划.md`
- `编排计划/TS-L2-DS02-ENTITY-LOOP计划.md`
- `编排计划/TS-L2-DS02-PATH-LOOP计划.md`
- 本 handoff

未改：`POL-L2-DS10-QRY-合规演示用例.md`（只读样板）、`测试用例/TS-L2-DS02-TEST-L01.md`、task-registry、任何业务仓。

## 验收证据

取数时间 2026-11-07 19:58–20:00。SSH MCP 连接 `10.50.69.111`（已有连接）成功。取数共 2 次业务调用，另 1 次准备 kubeconfig、1 次 sudo 清理；未 `echo` 探活。跳板机临时 kubeconfig 与脚本已删，`ls /tmp/qa-ds02*` 无文件。pod：`zhipu-tts/lumen-platform-algo-py-c6cb87d4-m68p9`，端口 8000。

| 读法 | 结果 |
|---|---|
| 未选点 `{"space":"demo_gkx_chain"}` | 200，`nodes` 200（`truncated.nodes=true`），`relations` / `listRecords` / `keyPathOptions` 0，`factorItems` 仅技术点 |
| `keyword=人工智能` / `深度学习` / `不存在的词zzq` | `nodes` 190 / 140 / 0（`GRAPH_EMPTY`） |
| `technology_node_id=tcn_000f21ac06aceb9cdd0575e82d0d85fc`（神经性厌食症治疗的临床视角，CORE，strength 36.98626428） | `nodes` 263，`relations` 65，关系类型 3（CO_EVOLUTION、KNOWLEDGE_DEPENDENCY、PATENT_CONVERGENCE），`listRecords` 61（论文 13、专利 20、机构 20 截断、人 8），`keyPathOptions` 2（`tep_8392b7f8…` 三步、`tep_6cddc27a…` 两步），关系无年份、`timeline` 空 |
| `technology_node_id=tcn_008a8b3f1dd54fcac52ebcb2ca81e160` | `relations` 10，`listRecords` 29，`keyPathOptions` 1（`tep_981d5e3d…`） |
| `techPointId=` 同一类点 | 与未选点相同，证实断点 |
| 分数表 `GROUP BY score_kind` | `influence` 252363，`centrality` 19430，`path_priority` 0 |
| 分数表抽查 | `tcn_000f21ac…` centrality 41.292；`W2093980670` influence 16.4、`W2940909888` 12.085、`W3049509808` 10.413、`W2981451354` 13.435 |

## 架构合规自检

1. 算法只在 Python：本单不写代码；中心度、影响力仍由 D18 mock 表供给。✅
2. 调用链：用例按 前端 → `gkxlumen-display` → `lumen-algo-py /internal/tech-graph/read` 写；本单取证在 pod 内直打 Python 只是只读核数，不是给前端的调用路径。✅
3. 图谱 NebulaGraph：只经 Python 只读接口读 `demo_gkx_chain`，没有直连 nGQL、没有写图。✅
4. 可观测：未改服务，沿用现有埋点。✅
5. CI/CD：文档任务，`cicd: skip`。✅
6. demo2 只读：未碰 demo 仓。✅
7. D12：用例与 LOOP 只调 `gkxlumen-display` / `lumen-algo-py`，没有任何 `demo-*` 服务。✅
8. D9 / D18：没有新造 `metric_id`，三条分数 D4 保持 mock，未改绿。✅
9. 数据：库只 `SELECT`（会话 READ ONLY），未 `--apply`，口令只用 pod 环境变量，未打印、未落盘。✅
10. 前端推送闸门：未改前端，未 push。✅

## 遗留

- `TS-L2-DS02-SEL-FIX-L01`（选中点字段名）不修，网关上 11 行可演行（GRAPH 2、ENTITY 5、PATH 4）会返回空块。
- `path_priority` 0 行：图上已有 `tech_path_step`，可按 `TS-L2-DS02-SCORE-L01` 的灌数脚本重跑补齐，由 LOOP 分类派单。
- 演示样本循环未建、未跑；三张验收单只在人说「按 LOOP 跑」后建。

## Cost 回填

- actual_tokens: 约 180000（估算）
- model_used: claude-opus-5.5（会话模型）
- actual_cost: 约 2.7（估算，美元）
- cost_warn: green
