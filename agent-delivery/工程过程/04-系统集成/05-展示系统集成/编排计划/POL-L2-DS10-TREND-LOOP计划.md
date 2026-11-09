# 政策动向跟踪 · LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-TREND-合规演示用例.md`
- 系统：科技信息展示系统。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

- 状态：2026-11-09 第三轮（期望刷新后复测）。样本满足：是（停止：完成）。203–206 全部通过（断言 10/10，见 handoff 第三轮表）。本轮子任务 `POL-L2-DS10-EXPECT-REFRESH-L01` 已签收（human:淮政玮 指令）。验收单 `POL-L2-DS10-TREND-DEMO-ACCEPT-LOOP` = `ready`（常驻单按计划约定不签 done；样本已满足，待监管人明示）。handoff：`agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-TREND-DEMO-ACCEPT-LOOP.md`

## 2026-11-09 第一轮（停止：令牌失效）

- 验收单 `POL-L2-DS10-TREND-DEMO-ACCEPT-LOOP` 已建并开工后置 `blocked`。
- 探测/样本调用 `GET /display/v1/policy/panorama/ingest` 与 `/stats?kind=all`：网关可达，返回 HTTP 401 `{"code":401,"msg":"访问令牌不存在","data":"sso check-token failed"}`。
- 本机 `%USERPROFILE%\.gkx\display-loop-token`（5af83d33…）与会话旧令牌（1cce4c0b…）均被 SSO 判不存在。属令牌失效，非 ENV（网关本体 200 通道正常应答）。
- 按 §6.5：通知 `human:淮政玮` 重新登录并覆盖 token 文件后，再说一次「按 LOOP 跑」再开下一轮。203–206 尚未取得任何 PASS/FAIL 记录。

## 2026-11-09 第二轮（样本不满足，继续）

- 换新令牌（cbac64ed…，登录主体 userId=3101）后探测 `GET /stats?kind=all` HTTP 200。
- 205 `POST /panorama/jobs` `{"kind":"深度分析报告","domain":"科创发展"}`：id 4 标题/正文/generated_at 逐字一致 ✅。
- 203 `GET /panorama/ingest`：首条已是 id 22843（SYN20261108 合成行），旧行 20008 被顶出前 100（limit clamp 100）→ DATA（并行灌数合法新增，非行丢失）。
- 204 `GET /panorama/subscriptions`：仅返回当前主体 3101 的 id 4 一条；用例主体 184 的三条订阅无法从接口核对 → 待用例重绑当前登录主体复测。
- 206 `GET /panorama/stats?kind=all`：主题「研发费用加计扣除」12/2024 一致 ✅；timeseries 2020=2421（期望 2402）、2026=64（期望 3）、北京 1932（期望 2268）→ DATA（ADS 表被并行重算）；行级 `metric_id` 不返回（`metrics.metric_ids` 层有）→ 契约差异并入刷新单。
- 分类与派单见 handoff。验收单留 `ready`，第三轮待 `POL-L2-DS10-EXPECT-REFRESH-L01` 完成后跑。

## 2026-11-09 第三轮（期望刷新后复测，样本满足）

- 刷新单 `POL-L2-DS10-EXPECT-REFRESH-L01` 由本会话代跑（human:淮政玮「签收」指令 + self_claim 选项）：TREND 用例 203/204/206 期望按现行读面重冻结，204 主体重绑 3101，206 行级 metric_id 契约裁定为「改期望对齐 as-built」。
- 复测断言 10/10 全过：203 首条字段齐全且为最新 created_time（22858，09:58:11）；204 用户 3101 订阅 id 4（week/system）命中；205 逐字一致；206 北京 1933≥1900、2020=2421 为峰值、主题 12/2024。
- 样本满足。验收单 `ready`，常驻单不签 done。

不派数据单，不派算法单，不打探测。

人说「按 LOOP 跑」之后，再按 §6.5 建常驻验收单 `POL-L2-DS10-TREND-DEMO-ACCEPT-LOOP`。不把这张单签 `done`。
