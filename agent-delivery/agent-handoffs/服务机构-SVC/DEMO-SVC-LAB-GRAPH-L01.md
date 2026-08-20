# DEMO-SVC-LAB-GRAPH-L01 · 圈定 hang 到 Demo 一张 G

> 日期：2026-08-20  
> Task：`DEMO-SVC-LAB-GRAPH-L01`  
> 仓：`demo-algo-ent-analysis` + `demo-ui-system-test`  
> 总控：阶段 F-ALGO 图谱叶。不开十模型 / 50892 / lumen 四仓。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；看板先 claimed，本会话转 in_progress 后落地 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短通路：circle+card → `svc_org_graph_hang` → 尝试 UPSERT `demo_gkx_chain` Tag `institution`。不造 Edge、不新建 space/Tag、不改 `settings.yaml` 全局 space。50100 去掉 22 点 Mock。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CLI 认领；本机未挂载 Headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，未改边） |
| 图 diff | 无工厂边变更。实现投影时序：circle → hang →（尽力）Nebula `demo_gkx_chain` |
| 会签态 | 流图仍 2026-08-19 approved |
| 说明 | 写库方 = 本仓 Python；Java 不直连 nGQL |

## 范围与实现

1. `entan/svcgraph.py`：读 `svc_org_circle` + `svc_org_card`，重写 `demo_gkxlumenx_dwd.svc_org_graph_hang`（`space_name=demo_gkx_chain`，`tag_name=institution`，`node_id=institution:{org_id}`）。  
2. Nebula：每次 `USE demo_gkx_chain`，复用已有 Tag `institution`，`props.role=service`。禁止 `gkx_service` / 正式 `gkx_chain` / `demo_entan`。不 CREATE space/tag，不写边（Q062）。  
3. `POST /internal/svc/run-graph`、`GET /v1/svc/graph`；status 带 hang 计数。live 拒绝写。  
4. 50100 `GraphView.vue`：删内置 22 点 / 38 边；读 hang；「投影到图谱」按钮。无 hang 则空图。

## 实测（Demo NAT MySQL）

| 项 | 值 |
|---|---|
| 圈定 | 3525 |
| hang | **3525**（`svcgraph_20260820_140108`） |
| 边 | **0**（Q062 诚实空） |
| GET `/v1/svc/graph?limit=3` | hang_total=3525，shown=3，edges=[] |
| Nebula | **failed**（本机 `192.168.88.43:9669` Timeout / BAD；hang 仍可查，未报假成功） |
| pending | 一律 1 |
| 未做 | 十模型、50892、正式库、造边、CHAIN 表 |

## 偏离说明

- 本机算法解释器起初无 `nebula3`；仓 `requirements.txt` 已有 `nebula3-python`。装上后仍连不上内网 graphd，故 Nebula 写入留给 **50100 / K8s 内网点「投影到图谱」**。  
- 图上默认最多 200 点，避免 3525 个力导向卡死；检索可缩小。不是 Mock 抽样充数。  
- Q062 未钉边类型：**未**对 `belongs_to` / `participates` 等底图边做 GO；请 `human:侯佳伟` / `human:李伟` 裁是否用现有边展开邻域。

## 产物清单

| 产物 | 路径 |
|---|---|
| 引擎 | `demo-algo-ent-analysis/entan/svcgraph.py` |
| 路由 | `demo-algo-ent-analysis/api/svc_routes.py` |
| CI smoke | `.gitlab-ci.yml` 增加 `entan.svcgraph` |
| 50100 图谱 | `demo-ui-system-test/src/views/industry-service/components/GraphView.vue` |
| API | `demo-ui-system-test/src/api/industry-service/index.ts` |

## 测试结果

- [x] `py -3 -m entan.svcgraph --check` ok  
- [x] hang 3525 = circle；不写正式库；不 DROP ODS  
- [x] GET 读 hang，edges=[]  
- [x] GraphView 无内置节点；无 hang 不充 `svcModelCatalog`  
- [x] Q-SVC-010 / Q062 待核验  

## 遗留风险

- 内网 Nebula 本机不可达；需 50100 部署后点投影才能确认 Tag `institution` 是否已在 `demo_gkx_chain`。若缺 tag，本叶 **不** CREATE（不自创 schema），将 skipped 并升级结构。  
- 灌数据 replace 后 hang 会过期，须再投影。  
- 同仓 `DEMO-SVC-LAB-MODELS-L01` 仍 backlog，等本叶联调闸门。

## 验收证据

- [x] Python 从 Demo `svc_org_circle` hang 到一张 G 约定  
- [x] `/internal` 供 50100 图谱页  
- [x] 不开十模型 / 50892 / lumen  
- [x] 一次 Demo hang 跑  
- [x] 失败诚实  

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | 调用链 | ✅ 50100 → `/entan/internal/svc/*` → Python |
| 3 | 图谱 Nebula，禁 Neo4j | ✅ space 写死 `demo_gkx_chain` |
| 4 | 可观测 | ✅ 沿用 API TraceHeader；前端 request 抽 traceId |
| 6 | demo 不污染 lumen | ✅ |
| 8 | ADS / hang | ✅ 名单仍只读 card；图读 hang |
| 10 | D9 | ✅ 权重占位 1，不伪中心性 |
| 12 | D12 | ✅ 未改 lumen 四仓 |

## CI/CD

- 分支：`origin/dev`  
- 部署：随 entan / 50100 CI；本机已写 Demo hang  

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 80000 |
| actual_tokens | 140000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.72 |
| cost_warn | green |
