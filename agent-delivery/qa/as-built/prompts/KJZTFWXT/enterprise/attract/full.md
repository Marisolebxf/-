# 招引企业推荐分析 · 全量执行顺序（2026-10-14 BATCH32，21 条；缺 P0-10/00985、P0-13/00990、P0-14/00991、P1-09/01003）

入口：`/enterprise/attraction?workspace=attraction&recommendation_tab=attraction`  
金样：P0-01 → P0-02 → P0-03 → P0-04 → P0-05（烟测）  
全量：金样后按 P0-06…P0-12、P0-15…P0-16 → P1-01…P1-08（无 P0-10/13/14、P1-09）。

## 易错点

1. **先 `/login` 再深链**（survey-page 直达偶发停登录页）。
2. **对比篮关闭钮**可能 DOM 存在但不可见——仅 `isVisible` 时点，否则跳过。
3. **业务态先关「内部评审模式」**（`aria-label`，禁 `first()` 盲点）；交付脚本 **禁止** 为断言而开评审（01003/P1-09 已删）。
4. **8 产业链**在「行业领域」下拉，不是页内 chip。
5. **价值三字段**主验「详情」抽屉；结果工具栏实勘为「加入对比篮」，P0-05 可能 allow_skip。
6. **禁止**切到培育兄弟页（`workspace=cultivation`）做正向断言。
7. 异步分析可能秒级复用同条件任务——过程态窗口短时属 observed。

铁律见 `as-built/prompts/_result.md`（本文件不复制相反口径）。
