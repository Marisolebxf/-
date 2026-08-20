# DEMO-SVC-LAB-MODELS-L01 · 十模型回写 Demo ADS + participates 边

> 日期：2026-08-20  
> Task：`DEMO-SVC-LAB-MODELS-L01`  
> 仓：`demo-algo-ent-analysis`（引擎）+ `demo-ui-system-test`（50100「跑十模型」）  
> 总控：阶段 F-ALGO。`human:淮政玮` 2026-08-20 **按推荐**：GRAPH 有点无线过闸；边由本叶映射 `participates`；Q062 仍 🟡。不开 50892 / lumen 四仓 / UI-MODELS 十模型页。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；GRAPH 已 integration，联调闸门开十模型 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 移植 `demo-ui-topic` `service-center` **公式**（短板 0/≤1/均深&lt;55、密度 2E/(N(N-1))、Q060 等权、招引 35/30/20/15、培育 25/30/25/20）。不拷贝 24 家 fixture。边只映射已有 Edge `participates`。列表 N=50。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CLI 认领；本机未挂载 Headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，未改边） |
| 图 diff | 无工厂边变更。实现：circle/card → ADS 十模型表；hang.ext.peers → GET 图谱边；Nebula `INSERT EDGE participates` 尽力 |
| 会签态 | 流图仍 2026-08-19 approved |
| 说明 | 写库方 = 本仓 Python；Java 不直连 nGQL；不 CREATE Edge |

## 范围与实现

1. `entan/svcmodels.py`：读 circle/card/finance hang，回写 `svc_chain_gap` / `svc_relation_chain` / `svc_tech_power_score` / `svc_attraction_recommend` / `svc_cultivation_recommend`。  
2. 短板运行时 **只** Q-SVCCHAIN-03；`q061_score` 对照列 + `q061_pending_client=1`。均深代理 = 命中字段数（card 无覆盖度列）。  
3. 边：同城同环节按 `org_id` 串路径（映射 cooperation）+ 圈内 `inv_org_id` 投资（映射 investment）→ **`participates`**。禁止 `serve`/`coop`/`invest` 新 Edge。  
4. 失败软着陆：本机 Nebula 不可达时仍写 `hang.ext.peers`，GET `/v1/svc/graph` 出线。  
5. `POST /internal/svc/run-models`、`GET /v1/svc/models`。50100 图谱页加「跑十模型」。关系链/短板/技术力 **页**仍等 `DEMO-SVC-LAB-UI-MODELS-L01`。  
6. 发现 Demo `svc_tech_power_score` 仍是 Gate-0 窄表（`service_org_code`、无 `org_id`）：`ensure_schema` DROP 后按空库 DDL 重建。未 DROP ODS 33 表。

## 实测（Demo NAT MySQL `111.198.38.90:34306`）

| 项 | 值 |
|---|---|
| batch | `svcmodels_20260820_163323` · `svc_proxy_v1.1` |
| circle | 3525 |
| gap | 6 环节；`stage-pilot` **blank**；其余有机构且均深≥55，无 weak/bottleneck |
| Q061 | 对照列有值；`q061_used_for_runtime=false` |
| relation_edges | **2816**（密度 0.000453） |
| tech / 招引 / 培育 | 283 / **50** / **50** |
| hang peers | 3525 行已回写 |
| GET `/v1/svc/graph?limit=20` | shown=20，**edges=10**，`rel=participates` |
| GET `limit=200` | shown=200，edges=129 |
| 点中心 1 跳 | 3 点 / 2 边 |
| Nebula | **failed**（`192.168.88.43:9669` Timeout / BAD；未报假成功） |
| pending | 一律 1 |
| 未做 | UI-MODELS 十模型页、50892、正式库、CREATE Edge、拷贝 30999 fixture 机构 |

## 偏离说明

- 覆盖度/专利/研发投入等卡面列未到：技术力与招引/培育用六类+是否有融资事件代理，全部 `pending_client_confirm=1`。  
- 边是 Demo 代理拓扑，不是甲方钉死的 Q062 边类型。UI 保持待核验。  
- 概览默认 200 点：优先有 peers 的 hang，再拉一跳邻居，避免按机构名切片导致无线。不是 Mock 抽样充数。  
- 投影仍会清 hang（含 peers），50100 需 **先投影再跑十模型**。

## 产物清单

| 产物 | 路径 |
|---|---|
| 引擎 | `demo-algo-ent-analysis/entan/svcmodels.py` |
| 图谱读边 | `demo-algo-ent-analysis/entan/svcgraph.py` `fetch_graph` |
| 路由 | `demo-algo-ent-analysis/api/svc_routes.py` |
| 窄表修补 | `demo-algo-ent-analysis/entan/svcseed.py` `ensure_schema` |
| CI | `.gitlab-ci.yml` 增加 `entan.svcmodels` |
| 50100 | `GraphView.vue` + `industry-service/index.ts` |

## 测试结果

- [x] `py -3 -m entan.svcgraph --check` / `entan.svcmodels --check` ok  
- [x] 一次 Demo 跑；列表 cap 50；圈定全量算边  
- [x] GET 出 `participates`；无 hang/peers 不充 `svcModelCatalog`  
- [x] 不切 Q061 运行时；Q062/Q060/Q063 待核验  
- [x] 不开 50892 / lumen  

## 遗留风险

- 内网 graphd 本机不可达；K8s/50100 内网点「跑十模型」才能确认 `INSERT EDGE participates`。缺 Edge 则 skipped，**不 CREATE**。  
- `stage-pilot` 圈内 0 家（名称未命中「中试」），短板 blank 诚实。  
- UI-MODELS 未开工：服务关系链 / 短板 / 技术力 / 招引培育页仍可能读旧 Mock，须本叶联调闸门后另派。

## 验收证据

- [x] 十模型从契约表出数回写 Demo ADS  
- [x] `/internal` 供 50100  
- [x] 边映射 participates，不新建 Edge  
- [x] 一次 Demo 跑  
- [x] 失败诚实  

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | 调用链 | ✅ 50100 → `/entan/internal/svc/*` |
| 3 | 图谱 Nebula，禁 Neo4j | ✅ space 写死 `demo_gkx_chain`；Edge 仅 `participates` |
| 4 | 可观测 | ✅ 沿用 API TraceHeader |
| 6 | demo 不污染 lumen | ✅ |
| 8 | ADS | ✅ 名单/卡仍不联 ODS |
| 10 | D9 | ✅ 短板/权重待核验，不伪闭合 Q061/Q062 |
| 12 | D12 | ✅ 未改 lumen 四仓 |

## CI/CD

- 分支：`origin/dev`  
- 部署：随 entan / 50100 CI  

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 80000 |
| actual_tokens | 160000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.85 |
| cost_warn | green |
