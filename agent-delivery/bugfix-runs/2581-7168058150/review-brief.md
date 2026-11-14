# 2581 独立评审简报（M 级 · 需独立会话评审）

## 评审对象

- 仓库：`e:\zhipu\gkx-lumen\repos\lumen-ui-science-pc` @ `be918a73ec4bb6a7ffdffaa1768639841b782451`（origin/dev 已推送）
- 本单 diff：`agent-delivery/bugfix-runs/2581-7168058150/review-diff.patch`（5 文件：FeedbackPanel.vue / SentimentTab.vue / FE-POL-SENT-LIVE.test.mjs / types/policy.ts / InterpretWorkbench.vue）
- 基线：`cdd4f487…`；其余 base..candidate 差异文件为 merge 带入的他单已评审提交（不在本评审核对范围，仅确认无本单语义交集）

## 缺陷与裁定背景

- 飞书 Bug 7168058150（2581）：需规 210「提供政策受众反馈收集工具，通过问卷调查、在线评价、意见征集等方式收集…用户可查看受众反馈的汇总统计和详细内容」——现实现只有查看面板（渠道切换+统计+列表+详情），缺「收集工具」入口。
- 用户裁定 2026-11-14（human:淮政玮，当会话）：卡片标题右侧（图2红框位）加「政策受众反馈收集工具」按钮；点击弹窗三渠道 tab（问卷调查/在线评价/意见征集），每 tab 展示工具使用面（提交表单+已收集反馈列表，参照图1 交互推理适配，不照抄）；**提交留浏览器会话、不落库不新增写接口**（先例 230 opinionRows / 236-1 提交不回写接口）。

## 实现要点（评审基准）

1. `SentimentTab.vue`：卡片 `#extra` 加按钮 → `feedbackPanelRef?.openTool()`。
2. `FeedbackPanel.vue`：`defineExpose({ openTool })`；弹窗内 `toolChannel` 独立切换（打开时跟卡内渠道，不回流）；提交表单（评分 a-rate + 文本域 500 字 + 提交意见）→ `collectedInSession` 头插；下半列表/统计 = 本会话增量 + 同源基础数据（USE_MOCK 走种子聚合，live 走 GET /feedback 行）；无评分渠道（意见征集）平均评分显示 — 不造 0。
3. 自检锚点：`FE-POL-SENT-LIVE.test.mjs` 加 5 断言（openTool 暴露/弹窗标题/submitDraft/collectedInSession/禁写接口正则）。
4. 顺带类型修复（`4f2e637` 遗漏，远端 `c5da830` 同修，冲突取显式实参）：`types/policy.ts` 白名单补 `policy_sim_path`；`InterpretWorkbench` 预测按钮 `@click="runPath(false)"`。

## 评审关注点（按 P0-DESIGN M 级清单）

- 调用方影响：`FeedbackPanel` 还有谁引用？`openTool`/`defineExpose` 对父级是否有副作用？
- 相邻 Tab / 默认空数据语义：弹窗三渠道空列表、平均评分 null、`toolChannel` 与卡内 `channel` 切换是否互扰？
- 写路径：是否确实零写接口（正则锚点是否真能防回归）？提交行 `id: local-${Date.now()}` 是否有键冲突风险？
- 失败态：提交被拦（空内容）提示是否明确；USE_MOCK=false 时统计口径是否与 feedbackStatsOf 一致。
- 类型顺带修：`policy_sim_path` 入白名单是否与后端 sub_type 闭包一致（对照 `InterpretWorkbench.vue` L571 实际调用）。
- 评审模式关后业务文案是否零黑话（无「演示/gapfill/fixture」字样混入工具弹窗）。

## 结论要求

给出 verdict（PASS/FAIL）+ findings（逐条，含严重度与位置）；如 FAIL 给最小修法。
