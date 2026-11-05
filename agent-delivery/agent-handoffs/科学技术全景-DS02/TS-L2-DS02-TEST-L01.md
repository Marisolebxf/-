# TS-L2-DS02-TEST-L01 · 科学技术全景三个功能主路径测试

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 开工前已是 `in_progress`。本轮不改登记表，不标 done |
| 说明 | task-get：`status=in_progress`，`lock_until=2026-11-05T22:43:54.318Z` |

ponytail: full

## 范围与实现

对照说明书序号 17–33 的三个功能，只写主路径用例：打开、搜索、点技术点、看实体、看路径、播放。另用代码走查确认序号 17（导入、手工、撤销）与序号 26（实体与实体、多快照）为 501 或空，并确认 `USE_MOCK=false` 不把种子节点填进页面。

被测实现已在各仓 `dev`，本轮只读：

- `lumen-ui-science-pc` `e6fb1dd`（HEAD `05863d0` 的祖先；`liveGraph.ts`、自检、`panorama.ts`、全景页此后无新提交）
- `lumen-svc-platform` `cbd6f10`
- `lumen-algo-py` 读图 `a03c52b`、灌数 `828315a`（centrality 19430，influence 252363，path_priority 0）

QA 未改 lumen 业务仓，未重做 `FE-TS-02A`，未启动 `SYSINT-TECHGRAPH-02-L02` / `L03`，未改指标口径。

## 偏离

已发布镜像未核，打开、搜索、点选、播放没有在浏览器或集群上点过。本轮未打公开接口，没有可记录的状态码。K8s 不写成通过。

图上没有 `tech_path_step`，分数表 `path_priority` 为 0 行。点路径时路径列表和优先级格为空，按派单记通过。

## 产物清单

- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/TS-L2-DS02-TEST-L01.md`
- 本交接
- 业务仓：无改动，无 commit

## 验收证据

1. 用例八条覆盖 DoD 三条。每条有前置、步骤、预期、实际结果。
2. 2026-11-05 在 `lumen-ui-science-pc` 执行 `node src/lib/graph/liveGraph.selfcheck.mjs`，输出 `liveGraph.selfcheck ok`，退出码 0。
3. 序号 17：`src/api/situation/panorama.ts` 只 POST `graph`。`index.vue` 的导入、手动添加、撤销只改会话内 `importedGraphExtras`，提示写明 501、未落库。`SituationPanoramaController` 的 `/import`、`/manual` 以及带写入动作的 `/graph` 返回 501。
4. 序号 26：`GraphAnalysisPanel.vue` 在 `live` 时实体网为空。`graphReadParams` 的 `currentYear` 固定 null。`/entity-relations` 与 `entityRelations=true` 返回 501。
5. 种子：自检断言空图为 `GRAPH_EMPTY`，不补 `robot`，分析上下文无「鹏城实验室」，页面不引用 `mock/modules/panorama`。
6. Java 单测 `writeAndEntityRelationReturn501WithoutReading` 仅作走查对照，本轮未跑 Maven。Pipeline 未跑。部署镜像未核。

## 架构合规自检

1. 调用链是浏览器 → `gkxlumen-display` `POST /v1/situation/panorama/graph` → Python `POST /internal/tech-graph/read`。✅
2. 读图与 nGQL 在 `lumen-algo-py` `tech_graph_read.py`。Java 只装配，不写 nGQL。✅
3. 图空间按读图实现走 Nebula。控制器写明不经 `gkxlumen-graph`。✅
4. 展示页不调用 `demo-*` 服务。✅
5. `USE_MOCK=false` 只消费这一次 `graph`。空图是 `GRAPH_EMPTY`，自检证明不补种子。✅
6. 中心度、影响力、路径优先级只读 `ads_technology_panorama_score`。本单不改口径，不把 D4 改成 live。✅
7. 序号 17、26 在 Java 为 501；前端写操作留在本次浏览并标明未落库，实体网在 live 下为空。✅
8. 全景页用 `createTraceId` 派发 `ts-panorama-track`。Python 读图视图沿用进程内 OTel。本轮未把 Tempo 里的 trace 写成已见到。✅

## Cost 回填

- actual_tokens: 8000
- model_used: claude-sonnet-4.5
- actual_cost: 0.04
- cost_warn: green
- 会话模型是 Grok 4.7。注册表枚举无 Grok，按派单给定的 sonnet 档填写。本轮未改 task-registry。

ponytail: full
