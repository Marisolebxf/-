# 科技政策推演 · LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS12-SIM-合规演示用例.md`
- 系统：科技信息展示系统。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

- 状态：第二轮 242 语序缺口已闭合（2026-11-08 晚，修法②文档分支：用例期望对齐库中自然语序，覆盖表+主路径两处；「缺项演示」零回潮）。至此 SIM 样本 5/5 按修订后期望成立（237/238/239/241 中午逐字 PASS，242 证据=午间线上实测+种子源码+修订用例三重一致）。缺口单随「签收，继续」口令派发执行，待签收。第一二轮明细见 handoff。
- 与效果预估共用 `POST https://edu.itic-sci.com/tid/api/display/v1/policy/simulation/jobs`。2026-11-07 该地址探测为 HTTP 404；2026-11-08 复探 HTTP 200，映射已恢复。

## 1. 要证明什么

可演行的填好请求返回期望输出。`设计无资源` 的行不请求、不派数据单。

通过线：探测 HTTP 200，且可演行与期望一致。对不上时按 §6.5 分类。历史测试用例里的 401、404 不改写成通过。原测试任务不标完成。

## 2. 验收单

届时新建 `POL-L2-DS12-SIM-DEMO-ACCEPT-LOOP`，`tech_task`，`qa-agent`。不签 `done`。

报告：`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-SIM-DEMO-ACCEPT-LOOP.md`

## 3. 后端调用

token 文件：`%USERPROFILE%\.gkx\display-loop-token`。请求头 `Authorization: Bearer`、`systemCode: display`。

| 步骤 | 调用 |
|---|---|
| 探测 | `POST https://edu.itic-sci.com/tid/api/display/v1/policy/simulation/jobs` ，body `{"kind":"文本解析","policy_id":"18318861"}` |
| 样本 | 用例覆盖表里每一条 `可演` 行的填好请求 |

探测 401、424 或令牌过期正文：验收单 `blocked`，通知 `human:淮政玮`，不建子任务。探测 404：停止，原因写「接口映射不存在」。

## 4. 缺口

DATA `POL-L2-DS12-SIM-DEMO-FIX-R{YYYYMMDD}-DATA`，QUERY 同形 `-QUERY`，ALGO 同形 `-ALGO`。每轮最多三张。子任务不改前端。同一缺口连续两轮仍在则停止，交给 `human:淮政玮`。
