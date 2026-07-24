# 派单包：ENT-PY-RECOMMEND-TASK

## 1. 任务信息

- 执行角色：`data-agent`
- 仓库：`demo-svc-topic-py`
- 依赖：架构任务、既有引育 PDR、Python callback、science 异步框架
- 状态：`backlog`
- 产品边界：产品定义文档只读，不在本任务修改

## 2. 目标

在 `gkx_ai_service` 新增 `/internal/gkx-ai/recommend/tasks` 场景适配，屏蔽 science 算法接口差异。
招引与培育共用一套推荐任务接口，用 `subType` 与 `selectionMode` 区分。

## 3. 实现要求

1. create/status/result/cancel 内部接口。
2. 支持 `subType=attraction|cultivation`。
3. 支持 `selectionMode=filter|candidate_workbench`。
4. filter 传筛选快照；candidate_workbench 传 `enterpriseCodes[]`。
5. Java `taskId`、`analysisType`、`callbackUrl` 向下透传。
6. 结果按 v3.0 招引/培育契约透明返回。
7. 不实现算法、不管对比篮候选池 CRUD、不维护正式任务历史。

## 4. 验收

- 两种 subType × 两种 selectionMode 契约测试通过。
- Mock/真实算法切换不改变 Java 契约。
- `/internal/*`、D9、OTel、CI、handoff 与 cost 四字段齐全。
