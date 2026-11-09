# TS-L2-DS02-GRAPH-DEMO-FIX-R20261107-QUERY · DS02 图谱 LOOP · 搜索/连线/分数叠加拣不中

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | registry 已是 `in_progress` / `claimed_by=agent:api-agent`；本叶只改 `lumen-svc-platform`，未动 `lumen-algo-py`，未开工 SYSINT-TECHGRAPH-02-L02/L03 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最小改 assemble 顺序 + display 口令注入；未新造抽象、未改用例期望、未把 D4 改绿 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改架构图） |
| 图 diff | 无 |
| 会签态 | N/A |
| 说明 | 只修读路径装配与 ADS 口令，调用链仍是 前端→Java display→Python `/internal/tech-graph/read` + JDBC 只读分数表 |

## 修改内容

### 1. `display.graph.keyword`（nodes≈190）

- **根因**：Java `query()` 已透传 `keyword`；Feign / Python CONTAINS / assemble 均正常。LOOP 首轮在 Windows PowerShell 用字符串 body 发「人工智能」，按系统码页发出 → 网关收到乱码 → `nodes=0`/`GRAPH_EMPTY`。本机复测：UTF-8 字节 body → `nodes=190`，前三含 `tcn_fceeb0c7…`。
- **处置**：无业务代码改动。补单测 `keywordIsForwardedToReadQuery`；`TS-L2-DS02-GRAPH-LOOP计划.md` §3 写明 UTF-8 探测写法，防假阴性。

### 2. `display.graph.relations.afterFilter`（期望 65 / 三种类型）

- **根因**：`assemble()` 选中点分支先 `cap(nodes,200)` 再按端点砍边。Python 已把邻居并进 nodes（常 >200，含 MEDIUM）；Java 裁掉邻居后只剩碰巧落在前 200 的 HIGH（网关实测 `relations=2`）。`lowEvidence` 只剔 LOW，不是主因。
- **修复**：先滤低证据并 `cap(relations)`，再 `keepThenCap` 钉住选中点+关系端点，最后才做端点校验。默认仍不回 LOW（与 Python HIGH+MEDIUM 默认一致），满足用例 65 条口径。

### 3. `ads_technology_panorama_score` overlay（centrality/influence null）

- **根因**：`JdbcPanoramaScores` 连 `demo_gkxlumenx_ads`，口令取 `DISPLAY_ADS_PASSWORD` / `ELEMENT_MYSQL_PASSWORD`。`values-lumen.yaml` 的 **display** 段原先没有这两项（element 有），连库 Access denied → 三个数字留空。表与行（`tcn_000f21ac…` centrality=41.292）在 SCORE-L01 已灌，非缺数。
- **修复**：display 注入与 element 同源口令；`@Value` 改为 `${DISPLAY_ADS_PASSWORD:${ELEMENT_MYSQL_PASSWORD:}}`。D4 仍 mock，未改就绪度。

## 测试结果

- 本机无 `mvn`/`java`，未能本地跑模块测；已加单测：
  - `keywordIsForwardedToReadQuery`
  - `selectedKeepsMediumRelationsWhenNeighborsSitPastNodeCap`（MEDIUM 邻居在 cap 外仍保留）
- 网关复测（UTF-8 body，token 未打印）：
  - `{"keyword":"人工智能"}` → `nodes=190`，前三 `tcn_fceeb0c7…` / `tcn_e42a7a9e…` / `tcn_ba8b6167…`，无 `emptyReason`
  - `{"selectedNodeId":"tcn_000f21ac…"}` → 推送前仍 `relations=2`（待 display 镜像 rollout 后应≈65）
  - 推送前 `centrality` 仍 null（待 helm env rollout）
- 分数/关系两项依赖 CI→K8s 发布后复验。

## 遗留风险

- relations / overlay 需等 `gkxlumen-display` 带新镜像 + helm env 落地后再打网关；本会话 kubectl 无集群登录态，未能看 rollout。
- LOOP 探测若不按 UTF-8 发中文，会再次假报 keyword 缺口。
- 口令现与 element 一样明文写在 `values-lumen.yaml`（既有模式）；后续宜收 Secret。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `dev`
- fix commit：`e159cc18ef79a1d7cf3a9e401b08d5369b8692f9`
- 落地 merge（push 后 HEAD）：`19833fe0a08a788a567b10f3f06d5fc7744afc6b`
- push：`origin/dev`（先 `pull --no-rebase` 再推，未 force）
- pipeline / rollout：未查
- Python 仓：未改

## 架构合规自检

1. 算法仍在 Python；本叶只改 Java 装配与口令。✅
2. 调用链未越层。✅
3. 图谱仍 Nebula `demo_gkx_chain`，经 Python 只读。✅
4. 可观测未改。✅
5. 已 push `origin/dev`。✅
6. D12：未调 demo-*。✅
7. D18 / D4：分数表仍 mock 只读，未改绿。✅

## 涉及文件

- `gkxlumen-display/.../SituationPanoramaService.java`
- `gkxlumen-display/.../JdbcPanoramaScores.java`
- `gkxlumen-display/.../SituationPanoramaControllerTest.java`
- `helm/gkxlumen-platform/values-lumen.yaml`
- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/编排计划/TS-L2-DS02-GRAPH-LOOP计划.md`（UTF-8 探测注）
- 本 handoff

## 没做的事

- 未改 `lumen-algo-py`
- 未改合规用例期望
- 未开工 DATA 单 / SYSINT-TECHGRAPH-02-L02/L03
- 未改 `task-registry.yaml`（证据回填走 MCP）
