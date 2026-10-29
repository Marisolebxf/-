# gkx-7chain MCP 使用与测试说明

> M1 只读包装网关。server：`scripts/7chain-mcp-server.mjs`。任务：`CROSS-MCP-7CHAIN-L02`。  
> 指标 8 件套仍用 `metric-registry`（`metric-mcp-usage-guide.md`）。本 MCP 不查任务、不改口径。

调用链：Cursor / WorkBuddy / 脚本 → 本 MCP → 网关。多数工具打 `GKX_MCP_API_BASE`（demo Java 网关）。`search-enterprise` 与 `search-policy` 的关键词检索打 `GKX_MCP_POLICY_BASE`（lumen Java 网关）。不要把基址指到 `demo-algo-*`、`lumen-algo-py`、Python `/internal/*` 或 Neo4j。WorkBuddy 接入见第 4 节。

---

## 1. 启用

仓库根目录是 `gkx-orchestration`。`.cursor/mcp.json` 里已有：

```json
"gkx-7chain": {
  "type": "stdio",
  "command": "node",
  "args": ["scripts/7chain-mcp-server.mjs"],
  "env": {
    "GKX_MCP_API_BASE": "https://edu.itic-sci.com/tts/alogp/api",
    "GKX_MCP_POLICY_BASE": "https://edu.itic-sci.com/tts/lumen/api"
  }
}
```

`GKX_MCP_API_BASE` 用验收表「科技专题服务算法库」的域名：`https://edu.itic-sci.com/tts/alogp`（内网对照 `http://10.50.69.111:30889`）。后面的 `/api` 由该站反代到 demo Java 网关。主机名是 `edu.itic-sci.com`。不要写开发节点 `10.50.69.111:30889`。专题页面 `https://edu.itic-sci.com/tts/svcz` 和展示系统 `https://edu.itic-sci.com/tid` 的 `/api` 会 401，不是这条 MCP 的基址。

`GKX_MCP_POLICY_BASE` 是 lumen 网关：`https://edu.itic-sci.com/tts/lumen/api`（内网对照 `http://10.50.69.111:30895`）。外层 Nginx 去掉 `/tts/lumen/api` 后转到该网关。企业智能搜索和政策关键词检索都用它。不要指到 `/tts/alogp/api` 或 `/tts/svcz/api`。

改完配置后重开 Cursor 的 MCP 面板，应看到 **gkx-7chain**，下面 13 个工具。Node 要 18 及以上，没有额外 npm 包。

| 变量 | 谁设置 | 作用 |
|------|--------|------|
| `GKX_MCP_API_BASE` | `mcp.json` 的 `env` | demo 网关根，末尾不要多写业务路径 |
| `GKX_MCP_POLICY_BASE` | `mcp.json` 的 `env` | lumen 网关根。`search-policy` 关键词检索与详情、以及未单独配置时的 `search-enterprise` |
| `GKX_MCP_ENTERPRISE_BASE` | 可选 | 只覆盖 `search-enterprise`。未设时用 `GKX_MCP_POLICY_BASE` |
| `GKX_MCP_TOKEN` | 本机环境，**不要写进 git / mcp.json** | 产业链 `/innov/**` 需要的 Bearer |
| `GKX_MCP_TIMEOUT_MS` | 可选，默认 30000 | 单次 HTTP 超时 |
| `GKX_MCP_SVC_BASE` | 可选 | 仅当 svc 网关返回 404 时，改打该域的 `/v1/svc/*`，结果带 `demo_only` |

demo 网关上，服务机构、综合、政策指标和 `search-policy` 的 `subject_id` 反查不带 token 也能 200。`search-industry`、`chain-panorama`、`chain-analyze` 打到 401/424 时，MCP 用 `client_credentials` 向同一基址的 `/auth/oauth2/token` 换票并重试一次。客户端默认 `pig:pig`，可用 `GKX_MCP_CLIENT_ID` / `GKX_MCP_CLIENT_SECRET` 覆盖。换到的 `access_token` 只留在进程内存，不进 git、不进 `mcp.json`。已设 `GKX_MCP_TOKEN` 时先用它，过期再换票。企业智能搜索和政策关键词检索不走这条 token，未设 `GKX_MCP_POLICY_BASE` 时直接失败、不打 demo 网关。

取 token（demo 网关默认 OAuth 客户端 `pig:pig`，`access_token` 不要提交）：

```powershell
$base = "https://edu.itic-sci.com/tts/alogp/api"
$basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("pig:pig"))
$resp = Invoke-RestMethod -Method Post -Uri "$base/auth/oauth2/token" `
  -Headers @{ Authorization = "Basic $basic" } `
  -ContentType "application/x-www-form-urlencoded" `
  -Body "grant_type=client_credentials"
$env:GKX_MCP_API_BASE = $base
$env:GKX_MCP_POLICY_BASE = "https://edu.itic-sci.com/tts/lumen/api"
$env:GKX_MCP_TOKEN = $resp.access_token
```

---

## 2. 怎么用

先查实体，再分析。一次 `chain-analyze` 只传一个 `aspect`。

统计数字上的 `metric_id`、`data_source` 原样保留。`search-policy` 的关键词结果不再强制 `mock`；每条带详情，正文在 `content`。`honesty` 按 lumen 检索原样说。综合活力若返回 `data_source=mock`，就按 mock 说。图谱节点超过 80 时 `truncated=true`。`policy-apply` 的 `simulate` 成功时带 `model_output=true`；后端失败会进 `error`，不会编一份推演。

返回里看这几处：

| 字段 | 含义 |
|------|------|
| `route.path` / `route.status` | 实际打到的网关路径和 HTTP 状态 |
| `route.trace_id` | 本次 `X-Trace-Id`（网关回显在 `upstream_trace_id`） |
| `data` | 上游 JSON。分数旁边的 `metric_id` 在这里 |
| `truncated` / `node_count` | 是否按 80 个节点截断 |
| `error` | 校验失败、424、或上游 `code!=0`。有 `error` 就没有业务结论 |

在对话里直接点工具名即可，例如：「用 search-industry 查信息技术，再对返回的 chain_id 做 chain-analyze，aspect 用 cycle」。

### 2.1 查询

| 工具 | 必填 | 示例参数 |
|------|------|----------|
| `search-enterprise` | `q`、`industry`、`region`、`type` 至少一项。`type` 只许 外企\|高企\|小微\|上市。`limit` 默认 20，上限 50。词会拼成一条智能搜索关键词 | `{ "q": "固态电池", "limit": 5 }` 或 `{ "q": "固态电池", "region": "深圳" }` |
| `search-industry` | `q`。`limit` 默认 10 | `{ "q": "信息技术", "limit": 5 }` |
| `search-policy` | `q`、`level`（国家\|省\|市）、`industry`、`subject_id` 至少一项。有 `subject_id` 走 demo 反查；否则走 lumen 检索并带正文 | `{ "q": "固态电池", "limit": 5 }` |

企业检索走专题页智能搜索 `POST /enterprise/topic/v1/search/smart`（`keyword` / `keywords` / `q` 同词）。基址是 `GKX_MCP_ENTERPRISE_BASE`，未设时用 `GKX_MCP_POLICY_BASE`（lumen 网关 `https://edu.itic-sci.com/tts/lumen/api`）。`enterprise_code` 取返回的 `org_id`。排序与页面默认相同：`competitiveness_score desc`。

产业清单走 `GET /innov/v1/industry/list`，关键词在 MCP 里做包含匹配。需要 token。

政策关键词走 `GET /policy/topic/v1/policy/search`（`q` 与 `keyword` 同词），再对每条 `GET /policy/topic/v1/policy/docs/{id}`。`content` 是政策正文。`subject_id` 反查仍是 demo 网关 `GET /policy/v1/policy/match`，不拉正文。未设 `GKX_MCP_POLICY_BASE` 时关键词检索失败，不会退回 mock 清单。

### 2.2 企业

| 工具 | 必填 | 示例参数 |
|------|------|----------|
| `ent-evaluate` | `enterprise_codes`（1～20）、`sub_type`：`tech`\|`business`\|`competitiveness` | `{ "enterprise_codes": ["企业码"], "sub_type": "tech" }` |
| `ent-recommend` | `kind`：`attract`\|`cultivate`，`industry`。`limit` 默认 10，上限 30 | `{ "kind": "cultivate", "industry": "半导体" }` |
| `ent-diagnose` | `action`：`diagnose`\|`rank`\|`score`\|`risk`。前三个除 `rank` 外要 `enterprise_code`；`rank` 要 `industry` 或 `region` | `{ "action": "diagnose", "enterprise_code": "00046d67552ba38386ee97a03d851cba" }` |

`tech` 发给后端时写成 `technology`。培育默认区域是深圳，招引默认全国。推荐 body 里带了 `industry`，现网接口可能不按产业过滤，名单以返回为准。

### 2.3 产业链

都要 token。`chain_id` 从 `search-industry` 来，例如 `INB1701`。

| 工具 | 示例参数 |
|------|----------|
| `chain-panorama` | `{ "chain_id": "INB1701" }` |
| `chain-analyze` | `{ "chain_id": "INB1701", "aspect": "cycle" }` |

`aspect` 只能是一个：`cycle`、`key-nodes`、`bottlenecks`、`region-index`、`shenzhen`、`roadmap`、`recommendation`、`competitiveness`。`cycle,bottlenecks` 会在发请求前被拒绝。

### 2.4 政策

| 工具 | 示例参数 |
|------|----------|
| `policy-indicators` | `{ "kind": "level" }`。`kind`：`timeseries`\|`national`\|`sz`\|`level`\|`type`\|`all` |
| `policy-apply` parse | `{ "action": "parse", "policy_id": "18318860", "limit": 1 }` |
| `policy-apply` match | `{ "action": "match", "subject_id": "E0001", "subject_type": "enterprise", "limit": 2 }` |
| `policy-apply` simulate | `{ "action": "simulate", "scope_code": "4403" }` |

`parse` 必须有 `policy_id`。`match` 必须有 `subject_id` 和 `subject_type`。`simulate` 必须有 `scope_code`。空数组是后端结果，不是 MCP 编的。

### 2.5 服务机构与综合

| 工具 | 示例参数 |
|------|----------|
| `svc-analysis` 指标 | `{ "kind": "indicators", "topic": "field" }`。`topic`：`field`\|`trend`\|`shenzhen` |
| `svc-analysis` 模型 | `{ "kind": "models", "topic": "tech" }`。`topic`：`tech`\|`gap`\|`attract`\|`cultivate`，或改传 `model_id` |
| `synth-index` 活力 | `{ "index": "vitality", "region": "深圳", "year": 2024 }` → `M_SYNTH_186_1` |
| `synth-index` 要素 | `{ "index": "elements", "facet": "composite", "region": "深圳" }`。`facet`：`composite`\|`type`\|`level`\|`domain` → `M_SYNTH_190_1` / `187_1` / `188_1` / `189_1` |
| `synth-index` 目录 | `{ "index": "catalog" }` |
| `synth-collab` 指数 | `{ "action": "index", "region": "深圳", "year": 2024 }` → `M_SYNTH_191_1` |
| `synth-collab` 图谱 | `{ "action": "graph", "region": "深圳", "hops": 1 }`。`hops` 最大 2 |

`region` 在综合计算里会同时作为 `city`（省、自治区、特别行政区则作为 `province`）。服务机构模型未就绪时，原样返回后端错误。

未注册、不要调用：`ent-graph`、`chain-list`、`chain-stats`、`policy-analysis`、`svc-orgs`、`svc-graph`（M2）。

---

## 3. 测试

### 3.1 离线自检（不连网关）

在 `gkx-orchestration` 根目录：

```powershell
node scripts/7chain-mcp-selfcheck.mjs
```

最后一行是 `7chain-mcp-selfcheck: ok`。它检查：

- `tools/list` 正好这 13 个，且没有 M2
- 缺参、非法 `aspect` / `hops` / `limit` 时零次 HTTP
- 合法参数打到上面的路径，并带 `X-Trace-Id`、`traceparent`
- `tech` 写成 `technology`；政策关键词检索打 lumen `/policy/topic/v1/policy/search` 并再取 `docs` 的 `content`，不强制 `mock`
- 100 个节点截成 80，并丢掉落在截断外的边
- `simulate` 的 HTTP 500 变成 `error`，正文里没有编造的推演得分
- 未设 `GKX_MCP_API_BASE`、基址指向算法进程、302 重定向、svc 404 且无 `GKX_MCP_SVC_BASE`，都会失败且不越出网关
- 设了 `GKX_MCP_SVC_BASE` 时，第二次请求才是该域的 `/v1/svc/*`，并带 `demo_only`
- 返回文本里不出现 `GKX_MCP_TOKEN` 的值

自检失败就先修 server，不要拿真实网关的空结果当自检失败。

### 3.2 对真实网关抽测

先按第 1 节设好 `GKX_MCP_API_BASE`、`GKX_MCP_POLICY_BASE` 和 `GKX_MCP_TOKEN`，再在仓库根目录执行。下面只打印状态、路径和有没有 `metric_id` / `mock`，避免把整包 JSON 打进终端。政策关键词的正文很长，抽测不打印 `content`。

```powershell
@'
import { callTool } from "./scripts/7chain-mcp-server.mjs";
const jobs = [
  ["search-industry", { q: "信息技术", limit: 3 }],
  ["search-policy", { q: "产业", level: "国家", limit: 2 }],
  ["ent-diagnose", { action: "diagnose", enterprise_code: "00046d67552ba38386ee97a03d851cba" }],
  ["chain-analyze", { chain_id: "INB1701", aspect: "cycle" }],
  ["policy-apply", { action: "parse", policy_id: "18318860", limit: 1 }],
  ["policy-apply", { action: "match", subject_id: "E0001", subject_type: "enterprise", limit: 1 }],
  ["svc-analysis", { kind: "indicators", topic: "field" }],
  ["synth-index", { index: "vitality", region: "深圳", year: 2024 }],
  ["synth-collab", { action: "index", region: "深圳", year: 2024 }],
];
for (const [name, args] of jobs) {
  const result = await callTool(name, args);
  const body = JSON.parse(result.content[0].text);
  const blob = JSON.stringify(body);
  const ok = result.isError ? "ERR" : "OK";
  process.stdout.write([
    ok, name,
    body.route?.status || "",
    body.route?.path || "",
    body.error ? String(body.error).slice(0, 120) : "",
    "metric=" + (blob.includes("metric_id") ? "yes" : "no"),
    "mock=" + (body.data?.mock === true || body.data?.data_source === "mock"),
  ].join(" ") + "\n");
}
'@ | Set-Content -Encoding utf8 "$env:TEMP\gkx-7chain-smoke.mjs"
node "$env:TEMP\gkx-7chain-smoke.mjs"
```

2026-10-28 在开发节点上抽测为 HTTP 200 的是当时的 demo 路径。验收基址改为 `https://edu.itic-sci.com/tts/alogp/api` 后，政策指标和综合目录已返回 `code:0`。`search-policy` 关键词检索已改走 lumen，不再期望 `data_source=mock`。对照：

- `search-industry` 能看到 `INB1701`
- `search-policy` 关键词结果 `mode=search`，每条有 `content`；`subject_id` 反查仍走 demo
- `ent-diagnose` 带 `M_ENT_SHORTBOARD_COUNT`
- `chain-analyze` 的周期阶段为「孕育期」（无 token 时应为 424，而不是空业务对象）
- `parse` 带 `M_POLICY_TEXT_PARSE`，`match` 带 `M_POLICY_MATCH`
- `synth-index` 为 `M_SYNTH_186_1` 且 `data_source=mock`
- `synth-collab` 为 `M_SYNTH_191_1`

网关不通就停。不要手写一份假的指标或推演填进结果。

### 3.3 对话里点一次

MCP 面板里 gkx-7chain 为绿之后，在本仓库对话说：

```text
调用 search-industry，q=信息技术，limit=3。
若返回 chain_id，再调用 chain-analyze，aspect=cycle。
把 route.status、metric_id 或 data_source、以及 error 原文发我。
```

424 且提示换票失败：客户端凭证被拒，检查 `GKX_MCP_CLIENT_ID` / `GKX_MCP_CLIENT_SECRET`。改完服务端脚本后要重开 MCP，旧进程不会热加载。`search-enterprise` 或 `search-policy` 报未设置 `GKX_MCP_POLICY_BASE`：lumen 基址没进 MCP 进程。空 `enterprises`：智能搜索没有命中，换关键词再试，不要把空列表补成名单。

---

## 4. 发布后接入 WorkBuddy

本叶发布物是 `origin/dev` 上的 `scripts/7chain-mcp-server.mjs`（stdio）。没有 npm 包，也没有可填 URL 的远程 MCP。WorkBuddy 在使用人自己的电脑上拉起这份脚本，电脑要能访问第 1 节的 demo 网关和 lumen 网关。腾讯云 MCP 市场上架不在本叶范围。

官方入口：[WorkBuddy MCP 说明](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide)。配置根键是 `mcpServers`。Cursor 的 `.cursor/mcp.json` 用相对路径 `scripts/7chain-mcp-server.mjs`，WorkBuddy 的工作目录不是这个仓库，相对路径会红灯。`command` 和脚本都写绝对路径。

### 4.1 本机先拉到脚本

```powershell
cd E:\zhipu\gkx-lumen\gkx-orchestration
git pull --no-rebase origin dev
node scripts/7chain-mcp-selfcheck.mjs
where.exe node
```

自检要打出 `7chain-mcp-selfcheck: ok`。`where.exe node` 的第一行就是下面 `command` 要填的路径。再按第 1 节取出 `access_token`，只放进本机配置。

### 4.2 写入 WorkBuddy 配置

用用户级，所有项目都能调，而且文件在仓库外面，token 不会被提交：

`C:\Users\<用户名>\.workbuddy\mcp.json`

文件不存在就新建。已有别的服务器时，只在 `mcpServers` 里加 `gkx-7chain` 这一段，不要整文件覆盖。

```json
{
  "mcpServers": {
    "gkx-7chain": {
      "type": "stdio",
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": [
        "E:\\zhipu\\gkx-lumen\\gkx-orchestration\\scripts\\7chain-mcp-server.mjs"
      ],
      "env": {
        "GKX_MCP_API_BASE": "https://edu.itic-sci.com/tts/alogp/api",
        "GKX_MCP_POLICY_BASE": "https://edu.itic-sci.com/tts/lumen/api",
        "GKX_MCP_TOKEN": "<第 1 节取出的 access_token>"
      }
    }
  }
}
```

`command` 换成 `where.exe node` 的结果。路径里的反斜杠在 JSON 里写成 `\\`。`GKX_MCP_TOKEN` 可以不写：产业链工具在 401/424 时会自己换票。手写的 token 大约 12 小时过期，过期后同样自动换票。

也可以在 WorkBuddy 里改同一份文件：侧边栏 **插件** → 右上角 **MCP 服务器** → **配置 MCP**。

项目级 `<仓库>\.workbuddy\mcp.json` 只对当前目录生效。里面如果写了 token，不要 `git add`。本仓库不提交这份文件。

### 4.3 信任并确认绿灯

保存后完全退出 WorkBuddy 再打开。在连接器里找到 `gkx-7chain`，点 **信任**。状态为绿表示 `tools/list` 已通，应能看到第 2 节的 13 个工具。红灯时在本机先跑：

```powershell
& "C:\Program Files\nodejs\node.exe" "E:\zhipu\gkx-lumen\gkx-orchestration\scripts\7chain-mcp-server.mjs"
```

进程应停住等 stdin，而不是立刻报找不到文件。`Ctrl+C` 结束。找不到 `node`、路径写成了相对路径、JSON 少了逗号，都是红灯的常见原因。

### 4.4 在对话里验收

新开一轮对话，说：

```text
用 gkx-7chain 的 search-industry 查「信息技术」，limit=3。
把 route.status、chain_id、以及有没有 error 发我。
若有 chain_id，再用 chain-analyze，aspect=cycle。
```

`route.status` 为 200 且能看到 `INB1701`，说明 WorkBuddy 已经打到 demo 网关。产业链工具若 424，是这份 `mcp.json` 的 `GKX_MCP_TOKEN` 没生效或已过期，不是工具没注册。政策关键词检索看 `content` 和 `honesty`，不再把列表说成 mock。活力指数的 `data_source=mock` 按第 2 节原文转述。
