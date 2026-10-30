---
name: gkx-trace
description: >
  按 X-Trace-Id 查 GKX 线上链路与日志，定位请求为何没成功。
  用户说出 trace: <traceID>（如 trace: fa3376781751c56ee32fffdd74d597db）即触发。
  不从仓库里找，默认从线上日志上找。
---

# GKX trace 排查

用户说 `trace: <traceID>` 即开始。traceID 即响应头 `X-Trace-Id`，32 位十六进制，去掉空格和连字符。

**不从仓库里找。默认从线上日志上找。** 结论必须来自 Tempo span 和 Loki 日志。仓库、设计文档、本地代码只在用户接着追问「代码为什么这样」时才打开。

## 入口

只查 `10.50.69.111` 的 NodePort。旧集群 Tempo/Grafana 作废。本机往往访问不到，用 MCP `user-ssh-executor`：`ssh_connect` 的 `serverName` = `10.50.69.111`，在远端执行 curl。**用 `http://10.50.69.111`，不要用 `127.0.0.1`**（NodePort 不在 localhost）。该节点没有可用 kubeconfig，不要 kubectl。

| 平面 | Tempo | Loki |
|---|---|---|
| demo / system-test | `http://10.50.69.111:30200` | `http://10.50.69.111:30310` |
| lumen | `http://10.50.69.111:30202` | `http://10.50.69.111:30311` |

两个平面都拉。HTTP 404 或 body 为空 = 不在该平面。两边都没有：直接说线上没有这条 trace，停止，不要改去翻仓库。

Tempo：`GET /api/traces/<traceID>`，把 body 写到 `/tmp/gkx-trace-<id前8位>.json`（每次覆盖，不要读旧文件）。

## 读 span

OTLP JSON：`batches[].resource.attributes` 里 `service.name`；`scopeSpans[].spans[]` 的 `name`、`startTimeUnixNano`、`status`、`attributes`、`events`。时间用东八区显示。

每个 span 抽出：服务、名称、耗时、`http.response.status_code` 或 `http.status_code`、`url.path` 或 `http.route` 或 `http.target`、`db.statement`（过长则截断）、`status.message`、events 里的 `exception.message` / `exception.stacktrace`。

断点 = 时间上第一个非 2xx，或 `status.code == STATUS_CODE_ERROR`。调用链顺序是前端 → 网关 → Java → Python。

## 读日志

Loki 标签用 `service_name`。先用 span 里出现的服务名。

时间窗：最早 span 前 2 分钟到最晚 span 后 15 分钟，query_range 的 start/end 用纳秒。

1. `{service_name="<svc>"} |= "<traceID>"`，`limit` 50，`direction=forward`。
2. 行数为 0：去掉 traceID 过滤，同一时间窗拉这些服务的日志，丢掉 `GET /health` 和 `GET /metrics`。trace 经常不进日志行，时间窗对得上的错误行、业务计数行才是证据。
3. HTTP 全是 200 且没有 exception：传输成功。业务成不成功只看日志里的计数、`error`、跳过原因。没有这些行就说明日志没记下业务结果，不要用代码推测。

日志提到的内网状态地址如果**已经出现在本条 trace 的 span 里**（例如随后的 `GET /internal/status`，host 来自 span），可以再 GET 一次取当前结果。地址不许猜，不许扫集群。

## 回答

用中文，先结论。模板：

```
结论：<一句话：没成功的直接原因>
平面：demo 或 lumen
时间：<CST>
断点：<服务 方法 路径 状态码>；若全是 200，写「传输成功，业务结果如下」
证据：
- span：<关键 span>
- 日志：<关键行，原文截断>
```

没有线上证据的原因不要写。不要附仓库文件路径，除非用户要求对照代码。
