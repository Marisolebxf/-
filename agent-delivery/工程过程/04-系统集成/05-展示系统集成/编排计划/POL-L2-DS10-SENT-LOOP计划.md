# 政策舆情评估 · LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-SENT-合规演示用例.md`
- 系统：科技信息展示系统。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

- 状态：用例覆盖表已齐。207、209–212 可演。208 设计无资源。本计划不建单、不探测。等人说「按 LOOP 跑」。

## 2026-11-09 首轮（停止：令牌失效）

- 验收单 `POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP` 已建并开工后置 `blocked`。
- 探测 `GET /display/v1/policy/panorama/ingest`（同页前置探测）：网关可达，返回 HTTP 401 `{"code":401,"msg":"访问令牌不存在","data":"sso check-token failed"}`。
- 本机 `%USERPROFILE%\.gkx\display-loop-token`（5af83d33…）与会话旧令牌（1cce4c0b…）均被 SSO 判不存在。属令牌失效，非 ENV。
- 按 §6.5：通知 `human:淮政玮` 重新登录并覆盖 token 文件后，再说一次「按 LOOP 跑」再开下一轮。207、209–212 尚未取得任何 PASS/FAIL 记录；208 设计无资源仍不请求。

设计无资源的行不请求。不派数据单，不派算法单，不打探测。

人说「按 LOOP 跑」之后，再按 §6.5 建常驻验收单 `POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP`。不把这张单签 `done`。
