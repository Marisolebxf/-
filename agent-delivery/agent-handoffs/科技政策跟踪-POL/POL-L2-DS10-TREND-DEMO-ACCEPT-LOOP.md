# POL-L2-DS10-TREND-DEMO-ACCEPT-LOOP · 演示样本验收 handoff

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成\05-展示系统集成/合规演示用例/POL-L2-DS10-TREND-合规演示用例.md`
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景 · 政策动向跟踪（203–206）
- 监管人：`human:淮政玮`（口令「按 LOOP 跑」，2026-11-09 会话）
- 执行：`agent:qa-agent`（本会话代跑）
- 令牌：本机 `%USERPROFILE%\.gkx\display-loop-token`，不进 git、不打印。请求头 `Authorization: Bearer` + `systemCode: display`。

## 运行 2026-11-09（首轮）

- 样本满足：否
- 停止：令牌失效（按 §6.5 探测 401/令牌失效文案 → 验收单 `blocked`，不建子任务，不再开一轮）

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 203 | GET `/display/v1/policy/panorama/ingest`（兼探测） | 401 | `{"code":401,"msg":"访问令牌不存在","data":"sso check-token failed"}` | ⛔ 未执行（令牌失效） |
| 204 | GET `/display/v1/policy/panorama/subscriptions` | 未发 | 探测 401，按规程停止 | ⛔ 未执行 |
| 205 | POST `/display/v1/policy/panorama/jobs` `{"kind":"深度分析报告","domain":"科创发展"}` | 未发 | 同上 | ⛔ 未执行 |
| 206 | GET `/display/v1/policy/panorama/stats?kind=all`（兼探测） | 401 | 同 203 | ⛔ 未执行 |

- 网关本体可达（能返回结构化 401 JSON，非超时/DNS 失败），排除 ENV。
- 令牌核对：本机文件当前值（5af83d33…，32 字符）与会话旧令牌（1cce4c0b…）分别实测，均返回同一 401 文案，SSO 侧已判失效。

### 缺口

无 DATA/QUERY/ALGO 缺口。本轮属 §6.5「令牌失效」停止分支：通知 `human:淮政玮` 重新登录展示系统，覆盖 `%USERPROFILE%\.gkx\display-loop-token`，再说一次「按 LOOP 跑」后开第二轮。203–206 期望值已在断言脚本 `run_ds10_loop_tests.py`（本机 %TEMP%\gkx_loop\，不进 git）备好，换 token 后直接重跑。

### 结论

验收单 `POL-L2-DS10-TREND-DEMO-ACCEPT-LOOP` = `blocked`（阻塞原因已登记 registry）。样本未满足。不签 done。
