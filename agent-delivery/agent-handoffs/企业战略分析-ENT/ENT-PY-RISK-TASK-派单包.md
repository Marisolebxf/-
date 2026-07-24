# 派单包：ENT-PY-RISK-TASK

## 1. 任务信息

- 执行角色：`data-agent`
- 仓库：`demo-svc-topic-py`
- 依赖：架构任务、既有风险 PDR、Python callback、science 异步框架
- 状态：`backlog`
- 产品边界：产品定义文档只读，不在本任务修改

## 2. 目标

在 `gkx_ai_service` 新增 `/internal/gkx-ai/risk/tasks` 场景适配，屏蔽 science 算法接口差异。
Python 不作为正式历史、状态和结果真源。

## 3. 实现要求

1. create/status/result/cancel 内部接口。
2. 支持 `subType=supply_chain|pain_points`。
3. Java `taskId`、`analysisType`、`callbackUrl` 向下透传。
4. 结果按 v3.0 契约透明返回；供应链包含最多 3 级完整快照。
5. 大结果可返回 `resultUrl`，由 Java 资产流程接管。
6. Mock 与真实算法切换不改变 Java 契约。
7. 不实现算法、不管候选数据 CRUD、不维护正式任务历史。

## 4. 验收

- 两个 subType 的创建、状态、结果、取消契约测试通过。
- 3 级图谱、痛难点四维结果、错误和超时场景覆盖。
- `/internal/*`、D9、OTel、CI、handoff 与 cost 四字段齐全。
