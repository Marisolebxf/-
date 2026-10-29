# CROSS-MCP-7CHAIN-L02 · gkx-7chain MCP M1 实装—查询入口与五域 P0 分析工具

> 只读包装 demo 网关已有 API。不重写 L01 盘点，不做 M2/M3。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 派单指定 coordinator_dispatch。`task-claim` 没有该字段，registry 未落 `claim_type`，记在 note。锁定 24h。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 单文件 server + 自检，复用指标 MCP 的 stdio 循环，HTTP 只用 Node `fetch`。未跳过 metric_id / mock 透传、trace header、调用链铁律。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `mcp` |
| 说明 | `user-headroom` 已挂载。验收在脚本里先裁成摘要，没有大到需要 `compress` 的原文。未用压缩代替方案 §4.1 / §5。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 不适用：只读包装既有网关，无新 diagram_id |
| 图 diff | 无 |
| 会签态 | 不适用 |
| 说明 | 不改 architecture-baseline，不新增图。 |

## 问题清单

- 方案字面路径 `GET /v1/chain/**` 在现网对不上 Java 控制器。控制器是 `/v1/industry/**`。`/chain/v1/chain/list` 为 404。`/topic/v1/industry/list` 被全局剥段再加路由 StripPrefix，落到 `/industry/list` 再 404。能通的网关路径是 `GET /innov/v1/industry/**`（全局过滤器只剥 `/innov`）。
- `/innov/**` 无 token 时 HTTP 424。token 只放进程环境变量 `GKX_MCP_TOKEN`，不进 git、不进 `mcp.json`。
- `search-enterprise` 用图谱 `center` 近似检索。`q=华为` 返回空节点（查询已是 UTF-8）。`industry=信息` 能返回企业码。
- `ent-recommend` 把 `industry` 放进 body。现网 attract/cultivate 不按产业过滤，MCP 不另编名单。
- 综合活力 `M_SYNTH_186_1` 的 `data_source=mock` 原样返回。协同指数 `M_SYNTH_191_1` 的 `data_source=real` 原样返回。
- `policy-apply simulate` 在 `scope_code=11` 时后端给空数组，已标 `model_output`，没有编造推演。`parse` / `match` 有记录。
- svc 指标 JSON 未见 `metric_id` 字段。MCP 不补造。政策等级与企业诊断的 `metric_id` 有透传。

## 修改内容

- `scripts/7chain-mcp-server.mjs`：stdio MCP，M1 共 13 个工具。网关基址 `GKX_MCP_API_BASE`，可选 `GKX_MCP_TOKEN` / `GKX_MCP_TIMEOUT_MS` / `GKX_MCP_SVC_BASE`。请求带 `X-Trace-Id` 与 `traceparent`。节点超过 80 截断并标 `truncated`。拒绝基址里出现 `demo-algo` / `lumen-algo` / `entan-py` / `innov-py` / `neo4j`。不跟随跨主机重定向。
- `scripts/7chain-mcp-selfcheck.mjs`：不连后端。校验 13 个工具都在、M2 六个不在、缺参不发请求、路由与 trace / token / mock / 截断 / svc 404 回退。
- `.cursor/mcp.json`：stdio server `gkx-7chain`，`env` 只注入 `GKX_MCP_API_BASE`。
- 未改 lumen-* / demo-*，未加 npm 依赖，未改 scope-baseline / architecture-baseline。

工具与网关路径（相对 `GKX_MCP_API_BASE`）：

| 工具 | 方法与路径 |
|------|------------|
| search-enterprise | `GET /entan/v1/entan/graph`，单家再 `GET /entan/v1/history` |
| search-industry | `GET /innov/v1/industry/list`，MCP 按 `q` 包含匹配 |
| search-policy | 列表 `GET /policy/v1/policy/mock/policies`（强制 `data_source=mock`）；反查 `GET /policy/v1/policy/match` |
| synth-index | `POST /entan/v1/synth-metric/metric/{id}/compute` 或 `GET .../catalog` |
| synth-collab | 指数同上 `M_SYNTH_191_1`；图谱 `GET /industry-comp/v1/comp/graph` 加 `/metrics`、`/viz` |
| ent-evaluate | `POST /entan/v1/evaluation/compute`（`tech` → `technology`） |
| ent-recommend | `POST /entan/v1/recommend/{attract\|cultivate}` |
| ent-diagnose | `GET /entan/v1/{diagnosis\|ranking\|score\|risk}` |
| chain-panorama | `GET /innov/v1/industry/{chain_id}/panorama` |
| chain-analyze | `GET /innov/v1/industry/{chain_id}/{aspect}`，一次一个 aspect |
| policy-indicators | `GET /policy/v1/policy/indicators` |
| policy-apply | `GET /policy/v1/policy/text/parse`、`/match`、`/simulate` |
| svc-analysis | `GET /entan/v1/svc/indicators` 或 `/models`。404 且设置了 `GKX_MCP_SVC_BASE` 时才直调该域 `/v1/svc/*` 并标 `demo_only` |

## 测试结果

- `node scripts/7chain-mcp-selfcheck.mjs` → `7chain-mcp-selfcheck: ok`（不连后端）。
- 真实基址：`http://10.50.69.111:30889/api`。这是 `gkx-demo-ui` NodePort 30889 的 `/api` 反代到 `demo-platform-gateway:9999`。本机直连 ClusterIP `10.105.230.86:9999` 超时；`30887` 拒绝连接。未改用 `gkxlumen-platform-gateway`（30899，属 M3）。
- 产业链请求带了 `GKX_MCP_TOKEN`（进程环境，不入库）。其余抽到的路径无 token 也是 200。

| 工具 | 结果摘要 |
|------|----------|
| search-enterprise `q=华为` | HTTP 200，节点 0。查询 UTF-8 已进 `center`。 |
| search-enterprise `industry=信息` | HTTP 200，返回企业码 `ent:000000d1e7cb4e27126fe30affc2e9f5` 等。 |
| search-industry `q=信息技术` | HTTP 200，`INB1701:新一代信息技术`。 |
| search-policy `q=产业&level=国家` | HTTP 200，`data_source=mock`，`mock=true`，样例 `policy_id=cn-gov-7067354`。 |
| ent-diagnose | HTTP 200，`total=1`，`metric_id=M_ENT_SHORTBOARD_COUNT`，企业 `00046d67552ba38386ee97a03d851cba`。 |
| chain-analyze `INB1701/cycle` | HTTP 200，阶段「孕育期」。需 token。 |
| chain-panorama `INB1701` | HTTP 200，26 个节点，`truncated=false`。 |
| policy-indicators `kind=level` | HTTP 200，`metric_id=M_POLICY_LEVEL_DIST`。 |
| policy-apply parse `18318860` | HTTP 200，`metric_id=M_POLICY_TEXT_PARSE`。 |
| policy-apply match `E0001/enterprise` | HTTP 200，2 条，`metric_id=M_POLICY_MATCH`。 |
| policy-apply simulate `scope_code=11` | HTTP 200，空数组，`model_output=true`。未编造推演。 |
| svc-analysis `indicators/field` | HTTP 200，键 `layout`、`layout_industry`。网关未 404，未走 demo-only。响应无 `metric_id`。 |
| synth-index vitality 深圳 2024 | HTTP 200，`metric_id=M_SYNTH_186_1`，`data_source=mock`。 |
| synth-collab index 深圳 2024 | HTTP 200，`metric_id=M_SYNTH_191_1`，`data_source=real`。 |

抽样 trace（请求头，网关回显同一值）：`c0fc3db269805d1ee5b3a475e635edf5`（synth-index）、`11322c3cfd7c2ea961ae8bd84724564f`（chain-analyze）。

## 遗留风险

- Cursor 拉起 MCP 时若只注入 `mcp.json` 里的 `GKX_MCP_API_BASE`，产业链工具会 424，直到本机另设 `GKX_MCP_TOKEN`。
- 企业检索仍是图谱近似，不是独立 search。
- 推荐接口忽略 `industry` 时，返回的是后端原名单。
- svc 模型/指标若以后从网关拿掉，需设 `GKX_MCP_SVC_BASE` 才会走 demo-only；现在不需要。

## CI/CD（必填）

- 分支：`dev`
- commit：与本 handoff 同一提交，标题含 `[agent:api-agent]`
- pipeline URL / ID：无。`cicd: skip`（编排仓本地 stdio，不发 K8s）
- 部署 namespace / 镜像 tag：不适用
- K8s rollout：不适用
- dev 测试 URL / 命令与结果：`node scripts/7chain-mcp-selfcheck.mjs` 绿；上表对 `http://10.50.69.111:30889/api` 的真实调用

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用网关 `gkx-gateway`，本 MCP 不另注册服务名
- traceId（dev 抽样）：`c0fc3db269805d1ee5b3a475e635edf5`
- Tempo / Loki：本叶未打开 Tempo。响应头 `X-Trace-Id` 与请求一致。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 MCP → Java 网关 → 下游 | ✅ 只请求 `GKX_MCP_API_BASE`。产业链打到 gkx-innov。企业图谱 / 综合图谱走已有 Java 门面路径。政策、评估、svc、synth 走网关上已发布的 `/policy`、`/entan`、`/industry-comp` 前缀，MCP 不直连算法进程。 |
| 禁止直连 demo-algo-* / lumen-algo-py、禁止绕过网关、禁止 Neo4j | ✅ 基址命中这些名字会拒绝。重定向不跟随。 |
| demo 网关，不切 gkxlumen-* | ✅ 未用 30899。 |
| D12 编排仓内部工具 | ✅ 未改 lumen-* / demo-*，不进 lumen 前端调用链。 |
| 算法只在 Python，本叶零算法 | ✅ |
| D9：metric_id 与 mock 原样 | ✅ 活力 mock、协同 real、政策列表 mock 均按后端或 mock 端点标明。未把 mock 说成已入库。 |
| 大图截断 80 | ✅ 全景本次 26 节点未截断；自检用 100 节点断言截成 80。 |
| 可观测 trace | ✅ 每个请求带 `X-Trace-Id` 与 `traceparent`。 |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000 |
| model_used | grok-4.7 |
| actual_cost | 0.97 |
| cost_warn | green |

口径：无 Console 分项。`actual_tokens` 取本叶估量（与派单 `estimated_tokens` 同量级）。`api-agent` 比例 input 0.80 / output 0.20。Grok 4.7 不在 `valid_model_enum` 与价表，成本按 Sonnet 4.5 公开价（输入 $3/M、输出 $15/M）作上限：`180000×0.8×3/1e6 + 180000×0.2×15/1e6 = 0.97`。低于 $5，`green`。

## 涉及文件

- `scripts/7chain-mcp-server.mjs`
- `scripts/7chain-mcp-selfcheck.mjs`
- `.cursor/mcp.json`
- `agent-delivery/agent-handoffs/CROSS-MCP-7CHAIN-L02.md`
