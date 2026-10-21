# 重点企业类型分析 KEYENT · Playwright 脚本工程（2026-10-14 v2.0 重写）

- 蓝本：`qa/test-cases/KJZTFWXT/enterprise-企业分析/KEYENT-重点企业类型分析/FUNC-重点企业类型分析-用例.md` v2.0（00379~00402，24 条）
- 金样 `gold.yaml`（P0-01~05 = 00379/00380/00381/00384/00386，id 锁定）；全量 `scripts.yaml`（includes 金样 + 19 条 = 24 条，与用例 1:1）
- 覆盖：`coverage.md`（24 行主表 + 覆盖说明，无未脚本化声明）
- 环境/控件档案：`fixtures/testdata.yaml`（http://10.50.69.111:30892/ · admin）
- 执行顺序：`agent-delivery/qa/as-built/prompts/KJZTFWXT/enterprise/key-type/full.md`
- 判定与落盘规约：`agent-delivery/qa/as-built/schema.md` §4、`prompts/_result.md`

## 执行入口

1. 冒烟：先跑 gold.yaml 全部 5 条（P0-01~05），金样任一 Fail → 停止，环境问题记 C2 后报告。
2. 全量：按 full.md 顺序执行 scripts.yaml（含 includes 金样），结果落 `runs/{date}-50892-keytype-r2/scripts/{id}/`。
3. 每条落盘 `result.yaml` + `steps.md`（数据条加 `observed.yaml`）。

## 关键实勘口径（2026-10-14）

- 现场无页内「类型/领域」Tab（侧栏两个二级入口）；筛选无「重置」按钮。
- 筛选四组 = 区域级联（placeholder「全国热门科创城市 / 深圳 / 全部」）/ 开始 2022 / 结束 2026 / 全部产业 / 全部类型。
- KPI 三卡：匹配企业数（家）/ 覆盖企业类型数（类）/ 覆盖区域数（个）；数值可为 0（不作判据，observed 记录）。
- 地图工具栏：放大/缩小/刷新/全屏 + switch「显示热力」默认开；图例「企业数量强度」低/中/高/极高。
- 单城默认态：区域徽标「深圳市」，「返回上一级」disabled；无同级排行与区域×类型矩阵。
- 企业清单抽屉 `.arco-drawer`；搜索框占位「企业名称、统一社会信用代码、产业或区域」。
- HTML 报告 = 只读演示页（正文 Mock，不当预期）；页头徽标「未付费」。
- 评审模式开关藏于右上 persona 菜单（「内部评审模式」switch，SEARCH retro R8 同款）；业务态断言前先关。
