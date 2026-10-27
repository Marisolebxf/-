# 企业查询 SEARCH · Playwright 脚本工程（2026-10-13 v2.0 重写）

- 蓝本：`qa/test-cases/KJZTFWXT/enterprise-企业分析/SEARCH-企业查询/FUNC-企业查询-用例.md` v2.0（00438~00480）
- 金样 `gold.yaml`（P0-01~05，id 锁定）；全量 `scripts.yaml`（includes 金样 + 36 条 = 41 条）
- 覆盖：`coverage.md`（脚本→用例主表 + 2 条未脚本化声明）
- 环境/词单：`fixtures/testdata.yaml`（https://edu.itic-sci.com/tts/svcz/ · admin）
- 执行顺序：`agent-delivery/qa/as-built/prompts/KJZTFWXT/enterprise/search/full.md`
- 判定与落盘规约：`agent-delivery/qa/as-built/schema.md` §4、`prompts/_result.md`

## 执行入口

1. 冒烟：先跑 gold.yaml 全部 5 条（P0-01~05），金样不过不继续。
2. 全量：按 full.md 顺序执行 scripts.yaml（含 includes 金样），结果落 `runs/{date}-50892-search-r2/scripts/{id}/`。
3. 每条落盘 `result.yaml` + `steps.md`（数据条加 `observed.yaml`；导出条加 `artifacts/` 文件）。

## 关键实勘口径（2026-10-13）

- 热门场景点击 = 立即检索进高筛（不待应用）；查询方案使用 = 直接应用。
- 无「全选本页」三态；行复选框 + 「已选 N 家企业」批量条。
- 结果工具区有「对比篮」按钮（系统级浮层）；导出弹层标题「确认导出查询清单」。
- 抽屉 `.arco-drawer` 十页签，默认工商概况；指标说明 `button.metric-spec-card`。
- 首层 tab 区另有系统级对比篮 tab（`system-compare-tabs`），非检索模式，勿混淆。
