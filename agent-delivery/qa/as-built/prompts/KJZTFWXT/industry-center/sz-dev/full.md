# 深圳产业发展分析 · 全量执行顺序（2026-10-14 BATCH32，25 条）

入口：`/industry-center/shenzhen?workspace=development&tab=development`  
金样：P0-01 → P0-02 → P0-03 → P0-04 → P0-05 → P0-06（烟测；用例册锁定 6 条）  
全量：金样后按 P0-07…P0-14 → P1-01…P1-11。

## 易错点

1. **先 `/login` 再深链**（survey-page 已内置）。
2. **对比篮关闭钮**可能 DOM 存在但不可见——仅 `isVisible` 时点。
3. **业务态先关「内部评审模式」**（`aria-label`，禁 `first()`）；P1-09 需开评审。
4. **Select 点 `.arco-select-view`**（产业/绑定），禁止点隐藏 input（P7）。
5. **分析对象单级**：placeholder「请选择产业」直出 15 集群项——**不要**套用对比册 `aria-label=集群/产业`。
6. **门控关键**：产业 + 有效绑定齐备后「开始分析」才可点；仅产业仍 disabled。
7. **无效绑定**：`（无效）导出 PDF 报告 · 不可作为输入` disabled，force click 不绑定。
8. **结果态**优先「分析记录 → 查看结果」；失败态查看结果常 disabled → Pass-N/A。
9. **禁止**切到 `workspace=comparison` 做对比正向断言（仅 P1-08 隔离）。

铁律见 `as-built/prompts/_result.md`（本文件不复制相反口径）。
