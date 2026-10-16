# 产业瓶颈堵点识别 · 全量执行顺序（BATCH32 回炉）

入口：`/industry-center/diagnosis?workspace=bottleneck&tab=bottleneck`  
A 档金样（零 allow_skip）：P0-01 → P0-02 → P0-03 → P0-04 → P0-05（00601/003/006/009/002）  
env-gate：`fixtures/scout/env-gate.json`（partial：g5 无已完成任务）

## 推荐顺序

1. **配置态 A/B**：金样 P0-01～P0-05 → P0-06～P0-09、P1-01～P1-03（先关对比篮；脏会话勿盲点重置）
2. **异步门控**：P0-04 仅验 enabled / 显式触发 / 切对象不自动起；过程词 P0-10 为 skip+ticket
3. **诊断记录**：P1-04 列表可跑；结果代表条 P0-11 skip（`ENV-CHAIN-BOTTLENECK-NO-DONE-TASK`）
4. **隔离 / 评审**：P1-05 → P1-06
5. **版本绑定**：P0-12 skip（过程 UI 同源）

## 易错点

- 金样**禁止** allow_skip；结果态不进 A（g5 fail）
- 生物产业黑名单：只验联动，勿依赖开始分析成功
- P3：关评审用 `aria-label="内部评审模式"`
- P7：点 `.arco-select-view`，勿点隐藏 input
- 同路由勿写周期 / 关键环节正向
- 父 agent 验收：`node tools/run-scripts.mjs …/bottleneck --only P0-01,P0-02,P0-03,P0-04,P0-05`（子 agent 禁止自跑刷分）
