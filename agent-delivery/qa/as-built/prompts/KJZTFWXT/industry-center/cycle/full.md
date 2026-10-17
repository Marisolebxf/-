# 产业周期分析 · 全量执行顺序（2026-10-14 BATCH32，16 条）

入口：`/industry-center/diagnosis?workspace=cycle&tab=cycle`  
金样：P0-01 → P0-02 → P0-03 → P0-04（烟测；用例册锁定 4 条）  
全量：金样后按 P0-05…P0-09 → P1-01…P1-07。

## 易错点

1. **先 `/login` 再深链**（survey-page 已内置）。
2. **对比篮关闭钮**可能 DOM 存在但不可见——仅 `isVisible` 时点。
3. **业务态先关「内部评审模式」**（`aria-label`，禁 `first()`）；P1-03/P1-06 需开评审读版本/追溯。
4. **Select 点 `.arco-select-view`**（集群/产业/近×年），禁止点隐藏 input（P7）。
5. **结果态**优先「诊断记录 → 查看结果」恢复已完成任务；无完成态允许 Pass-N/A。
6. **禁止**切到关键环节（`key_link`）/ 瓶颈（`bottleneck`）做正向断言。
7. 未选对象：按钮仍可点，看「尚未选择分析对象」拦截（非置灰）。

铁律见 `as-built/prompts/_result.md`（本文件不复制相反口径）。
