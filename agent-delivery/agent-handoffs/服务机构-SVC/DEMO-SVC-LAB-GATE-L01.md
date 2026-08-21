# DEMO-SVC-LAB-GATE-L01 · SVC F-GATE：50100 退出门 + 公式冻结（不开 50892）

> 日期：2026-08-21  
> Task：`DEMO-SVC-LAB-GATE-L01`  
> 仓：`gkx-orchestration`（冻结清单 + 本 handoff）；现场只认 **50100**  
> 拍板：`human:淮政玮` 2026-08-21 微信 **选 A · 否 C**。F-ALGO 三叶 `integration` 不挡本叶。  
> **禁止**：写 P 总控、施工 50892、改 lumen 四仓、F 绿自动续 P。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 阶段 F 总控已授权「不必再问」；锁定 24h。淮总指定本叶用 data-agent |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | 定义 + 现场核对，不写产品代码、不移植 50892。未用 YAGNI 跳过 D9 待核验 / D12 / 出数铁律。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CLI 认领；本机未挂载 Headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，未改工厂边） |
| 图 diff | 无。切法 A 写进公式冻结清单，不重签 §1 工厂拓扑 |
| 会签态 | 流图仍 2026-08-19 `approved` |
| 说明 | 本叶不改 `01-data-flow.md` |

## 范围与实现

1. **现场 50100**（`http://111.198.38.90:50100/`，平面 Demo）：核基础指标 A1–A6、图谱 hang、十模型 ADS。只认契约命中行，不认 fixture 24 家。  
2. **公式冻结清单**落盘：[`data-design/storage/SVC/formula-freeze-cut-a.md`](../../data/data-design/storage/SVC/formula-freeze-cut-a.md)（切法 A）。给下一份 P 总控，本叶不施工 50892。  
3. 微信确认稿归档：[`DEMO-SVC-F底座-淮政玮微信确认稿.md`](./DEMO-SVC-F底座-淮政玮微信确认稿.md)。  
4. 未做：双滤镜 UI、生态密度列、多元点 hang、P 总控、lumen 四仓。

## 偏离说明

- 进程内 `status.graph` / `status.models` 的 `last_run` 为空（算法进程重启后内存态丢失）。**读接口仍出 ADS/hang 契约数**，不把内存空当成库空。  
- 本机控制台中文名乱码，数字与 `org_id` / `space` / `rel` 以 JSON 为准。  
- 六类 layout 合计 2833，圈定 3525，差额为未入六类候选，**未**做成第 7 类。  
- Nebula 内网投影本叶未复跑；图谱读 hang.peers，边 `participates`。本机不报假成功。

## 产物清单

| 产物 | 路径 |
|------|------|
| 公式冻结清单（切法 A） | `agent-delivery/data/data-design/storage/SVC/formula-freeze-cut-a.md` |
| 本 handoff | `agent-delivery/agent-handoffs/服务机构-SVC/DEMO-SVC-LAB-GATE-L01.md` |
| 微信确认稿 | `agent-delivery/agent-handoffs/服务机构-SVC/DEMO-SVC-F底座-淮政玮微信确认稿.md` |

## 验收证据

现场时间：2026-08-21。前缀 **`/api/entan`**（无此前缀的 `/entan/...` 回 SPA HTML，不算接口）。

| 块 | 接口 | 结果 |
|----|------|------|
| 灌数/圈定 | `GET /internal/svc/status` | `code=0`；规则 `svc_rule_demo_kw_v1.1`；ODS `dwd_org_base_info=40000`；`svc_org_circle=3525`；`svc_org_graph_hang=3525`；`svc_org_card=3525`；灌数 `last_run=2026-08-20 21:45:47` `append` |
| A1–A6 | `GET /v1/svc/indicators?kind=all` | `code=0`；layout 六类 INNOV 1384 / CONSULT 592 / FINANCE 501 / MKT 203 / HR 120 / IP 33；global 1；new 40；invest 3 + events 20；sz_scale 1355；sz_dist 9 |
| 图谱 | `GET /v1/svc/graph?limit=20` 与 `limit=40` | `code=0`；`space=demo_gkx_chain`；`tag=institution`；`hang_total=3525`；shown 20/40；点 `cat=service`、id 前缀 `institution`；边 `rel=participates`、`mapped_from=cooperation`；样本无名「迈瑞/华为」 |
| 十模型 | `GET /v1/svc/models?kind=all` | `code=0`；`svc_proxy_v1.1`；`pending_client_confirm=1`；`list_cap=50`；gap 6 环节（`stage-pilot` **blank** / 0 家）；relation_summary density **0.000453**、link_count **2816**、node_count **3525**、batch `svcmodels_20260820_174345`；tech **283**（六类齐全、无第 7 类）；attract **50**；cultivate **50**；ADS 表行与上表一致 |
| 标签 | 50100 UI | 待核验；未标 live |

- [x] 只认契约命中行，不认 fixture 24 家  
- [x] 公式冻结清单落盘（一张图两种滤镜 / 双密度并排 / 短板与技术力对象=机构 / 引入培育名单=机构 / 关联主体一跳复用 ENT hang）  
- [x] 不开 50892、不写 P 总控、不改 lumen 四仓  
- [x] Q060 / Q062 / Q063 / Q-SVC-010 / Q-SVCCHAIN-03 不因本叶变绿  

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本叶不写算法；读现有 `demo-algo-ent-analysis` |
| 2 | 调用链 | ✅ 50100 → `/entan/internal/svc/*` 与 `/entan/v1/svc/*`；不越层 |
| 3 | 图谱 Nebula，禁 Neo4j | ✅ 只认 `demo_gkx_chain`；边仍 `participates` |
| 4 | 可观测 | ✅ 沿用既有 TraceHeader；本叶无新服务 |
| 6 | demo 不污染 lumen | ✅ |
| 8 | ADS | ✅ 名单/卡/十模型读 Demo ADS；线上不 JOIN ODS |
| 9 | D8 | ✅ 不改 50100 栈、不另起 UI |
| 10 | D9 | ✅ 待核验保留；黄灯不改绿 |
| 12 | D12 | ✅ 未改 lumen 四仓、未调 demo 进正式站 |

## 测试结果

- [x] 50100 三块 GET 出契约数或诚实空态（本现场为契约数；`stage-pilot` 诚实 blank）  
- [x] 图例仅服务机构；无 22 点 fixture  
- [x] 切法 A 冻结清单可给 P 总控引用  
- [x] 本叶零产品代码  

## 遗留风险

- 滤镜 ② / 生态密度 / 多元 hang **故意未做**，等 GATE `done` 后另开 P 总控。  
- 算法进程内存 `graph`/`models` last_run 空，以表计数与 GET 为准。  
- 签收 `ready_to_sign → done` 仍是 `human:淮政玮`。Agent 不标 `done`。

## CI/CD（必填）

- 分支：`origin/dev`  
- commit：本叶编排仓提交（冻结清单 + handoff + 总控进度）  
- pipeline URL / ID：编排仓无业务 CI  
- 部署 namespace / 镜像 tag：未发新镜像；50100 跟既有 `demo-ui-system-test` / `demo-algo-ent-analysis` `dev`  
- K8s rollout：未改  
- dev 测试 URL：`http://111.198.38.90:50100/` · 接口前缀 `/api/entan`

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 50100 / entan  
- Tempo / Loki：无本叶新抽样  

## 涉及文件

- `agent-delivery/data/data-design/storage/SVC/formula-freeze-cut-a.md`  
- `agent-delivery/data/data-design/storage/SVC/README.md`  
- `agent-delivery/data/data-design/storage/SVC/00-context.md`  
- `agent-delivery/agent-handoffs/服务机构-SVC/DEMO-SVC-REOPEN-长任务总控.md`  
- `agent-delivery/agent-handoffs/服务机构-SVC/DEMO-SVC-F底座-淮政玮微信确认稿.md`  

## Cost 回填

| 字段 | 值 |
|------|-----|
| estimated_tokens | 40000 |
| actual_tokens | 95000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.48 |
| cost_warn | green |

联调通过。现场 50100 三块读契约表；冻结清单已入库。不开 P/50892。
