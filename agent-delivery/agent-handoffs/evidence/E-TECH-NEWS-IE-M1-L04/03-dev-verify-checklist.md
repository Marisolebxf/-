# Dev 联调点验清单 · 科技新闻四要素（L04/L05 后）

日期：2026-07-28  
执行：`agent:algorithm-agent`

## 环境可达性

| # | 检查项 | 期望 | 本机结果 | 状态 |
|---|--------|------|----------|------|
| E1 | Python `GET :8000/tech-news/healthz` | 200 ok | `{"status":"ok","mode":"llm","persist":true}` | ✅ |
| E2 | Java demo `GET :7090/...` | 可达 | 连接失败（本机未起 gkx-innov） | ❌ 残留 |
| E3 | 网关 `192.168.88.50:9999/innov/v1/tech-news/**` | 200/业务体 | HTTP 502 | ❌ 残留 |

## Python 行为点验（直连 `/internal`）

| # | 用例 | 期望 | 结果 | 状态 |
|---|------|------|------|------|
| V1 | 政策 IPv6 文 | HTTP 200 + `policy_or_legal_noise` + 0 事件 | PASS | ✅ |
| V2 | 零售开售文 | HTTP 200 + `consumer_retail_noise` + 0 事件 | PASS | ✅ |
| V3 | 工业视觉样例 | ≥1 事件且 impact 非空 | PASS（llm） | ✅ |

原始 JSON：`%TEMP%\tech-news-ie\dev-verify.json`

## Java / 前端（配置层，本机未起进程）

| # | 检查项 | 期望 | 状态 |
|---|--------|------|------|
| J1 | Feign/RestTemplate read-timeout ≥ 120s | demo `d8f2456` / lumen `59d9f6c` 已 push | ✅ 配置 |
| J2 | 透传 `error` Map | Service 原样返回 | ✅ 代码 |
| F1 | 门控 warning UX | L05 `546ebb1f` 已 push | ✅ 代码 |
| F2 | impact 空显示「暂无」 | 同上 | ✅ 代码 |
| F3 | UI 登录截图 `/service/tech-news-review` | 需网关+Java+登录 | ❌ 残留 |

## 监管人补验（建议）

1. 起 innov Java（或 K8s rollout 吃到 timeout commit）  
2. 网关 502 恢复后：前端打开复核页  
3. 粘贴 V1/V2/V3 三类正文，确认 warning / 四要素 /「暂无」

## 结论

- **算法侧点验通过**（门控软拒绝 + impact 填充）  
- **端到端 UI/网关仍阻塞于环境**（与 L03 残留同类）  
- 不阻塞算法质量关单；端到端截图待 devops/监管人补
