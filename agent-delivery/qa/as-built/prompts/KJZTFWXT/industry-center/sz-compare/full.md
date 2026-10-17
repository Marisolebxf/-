# 深圳产业情况分析对比 · 全量执行顺序（2026-10-14 BATCH32，22 条）

入口：`/industry-center/shenzhen?workspace=comparison&tab=comparison`  
金样：P0-01 → P0-02 → P0-03 → P0-04 → P0-05（烟测；用例册锁定 5 条）  
全量：金样后按 P0-06…P0-12 → P1-01…P1-10。

## 易错点

1. **先 `/login` 再深链**（survey-page 已内置）。
2. **对比篮关闭钮**可能 DOM 存在但不可见——仅 `isVisible` 时点。
3. **业务态先关「内部评审模式」**（`aria-label`，禁 `first()`）；P1-09 需开评审。
4. **Select 点 `.arco-select-view`**（集群/产业/标杆），禁止点隐藏 input（P7）。
5. **分析对象双级**：用例「产业」口语 → 现场 `aria-label=集群` + `aria-label=产业`。
6. **Q016 标杆空** → 「开始分析」常 disabled；P0-05 创建任务允许 Pass-N/A；切条件不自动起仍须验。
7. **结果态**优先「分析记录 → 查看结果」；重跑入口=「按此配置新建分析」。
8. **禁止**切到 `workspace=development` 做发展分析正向断言（仅 P1-08 隔离）。

铁律见 `as-built/prompts/_result.md`（本文件不复制相反口径）。
