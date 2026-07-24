# 派单包：ENT-PY-ANALYSIS-CALLBACK

## 1. 任务信息

- 执行角色：`data-agent`
- 仓库：`demo-svc-topic-py`
- 依赖：`ENT-ARCH-ANALYSIS-TASK-DOC`
- 状态：`backlog`

## 2. 目标

在 `gkx_ai_service` 新增统一内部回调入口：

`POST /internal/gkx-ai/analysis/callback`

算法只能回调 Python；Python 根据 `analysisType` 转发到 Java：

- `enterprise_eval` → `/api/analysis/callback/eval`
- `risk_insight` → `/api/analysis/callback/risk`
- `talent_recommend` → `/api/analysis/callback/recommend`

## 3. 实现要求

1. 校验 `taskId`、`analysisType`、`eventType`、节点和终态结果字段。
2. Java callback base URL、超时和重试参数走 Nacos/环境变量。
3. 业务结果透明透传，不在 Python 解析三类多态结果。
4. 使用 `taskId + eventType + nodeIndex` 或等价键记录重复回调，保证转发幂等。
5. 结构化日志必须含 taskId、analysisType、traceId、下游状态和重试次数。
6. Java 不可达时有限重试并返回明确错误；禁止无限阻塞算法线程。
7. 保留 `/internal/*`、鉴权和 OTel，禁止对前端暴露。

## 4. 验收

- 三类 callback 路由、节点事件、成功、失败和重复回调单测通过。
- 错误 analysisType、缺字段、Java 超时和非 2xx 有明确响应和日志。
- 与 Java callback Mock 联调通过。
- CI、handoff、架构合规和 cost 四字段齐全。

