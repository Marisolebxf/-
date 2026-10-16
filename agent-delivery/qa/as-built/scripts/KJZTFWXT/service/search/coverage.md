# 服务机构查询 脚本→用例 覆盖表（2026-10-14）

蓝本 = `qa/test-cases/KJZTFWXT/service-产业服务链分析/SVCSEARCH-服务机构查询/FUNC-服务机构查询-用例.md` v2.0（01328~01350，23 条）。
脚本 **23 条**（金样 7 + 其余 16），与用例 **1:1**；未脚本化 **0**。
locator 基准 = `fixtures/scout/`（2026-10-14 无头实勘；`survey-page.mjs` 首跑卡在 login，二次探针 `scout-retry.*` / `scout-deep.*` / `scout-hits.json` 为准）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01328 | 入口·路由与页头 | P0 | goto /service-center/search |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01329 | 壳层·三 Tab 互斥 | P0 | 轮切智能检索/查机构/高级筛选 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01330 | 智能检索·表单构成 | P0 | 读 placeholder + 搜索按钮 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01331 | 智能检索·快捷示例 | P0 | 点示例 chip 回填 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01338 | 结果态·技术力分排序 | P0 | 搜「深圳」+ 核技术力分位（排序 manual） |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01340 | 结果态·行级入篮 | P0 | 点「加入对比篮」 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01342 | 初始态·技术力领先空态 | P0 | 浏览诚实空态文案 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01332 | 智能检索·示例直达 | P0 | 点示例（as-built 仅回填） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01333 | 智能检索·手输检索 | P0 | 填「深圳」+ 搜索 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01334 | 智能检索·解析 Chips | P0 | 搜「深圳 检验检测」 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01335 | 查机构·单关键词框 | P0 | 切 Tab + 搜「检验检测」 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01336 | 高筛·字段库与应用 | P0 | 切高级筛选 + 加条件应用 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01337 | 结果态·区构成 | P0 | 核总数 + 卡片 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01339 | 结果态·画像抽屉 | P0 | 点机构名开 .arco-drawer |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01341 | 结果态·卡片构成 | P0 | 浏览卡片字段 |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01343 | 结果态·再筛选 | P0 | 核原条件保留（叠加 manual） |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01344 | 智能检索·空输入 | P0 | 空框点搜索 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01345 | 空结果·建议话术 | P1 | 搜无命中词 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01346 | 高筛·应用禁用 | P1 | 读「应用筛选（0）」 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01347 | 评审·零泄漏 | P1 | 关评审 + reload |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01348 | 会话·刷新保留 | P1 | 检索后 reload |
| P2-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01349 | 异常·入口隔离 | P2 | 三 Tab + 检索不落兄弟路由 |
| P2-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01350 | 异常·对比篮开合 | P2 | 开合系统对比篮 |

## 未脚本化声明

无（23/23 已脚本化）。部分 expect 因现场控件缺失/未深勘标 `manual: true`，见下方偏差。

## as_built 主要偏差（相对用例预期）

| 点 | 用例口径 | 实勘 2026-10-14 | 脚本处置 |
|----|----------|-----------------|----------|
| 示例按钮语义 | 01332 一键发起检索 | 仅回填，不自动提交 | P0-08 抛 AS_BUILT 偏差供人判 |
| 查机构字段 | 01335 机构名/领域/环节三分 | 单关键词框 | P0-11 按单框断言 + note |
| 高筛分组 | 01336 基本信息/服务能力/资质规模 | 基本信息/技术能力；按钮「应用筛选（N）」 | P0-12 按现场分组 |
| 排序入口 | 01337/01338 技术力分/成立年份/覆盖广度 | 未见排序 Select；仅卡片「技术力分」位 | P0-05/P0-13 排序行为 manual |
| 空输入提示 | 01344 必填提示 | 未见 form message；未出结果区 | P0-17 核「未出结果」 |
| 空态文案 | 01342 无句号 | 文案末尾带「。」 | 正则含句号可选 |
| 命中词 | 示例「深圳 检验检测」 | 智能解析常 0 命中；「深圳」约 1.3 万 | fixtures `keyword_hit: 深圳` |

## 同路由兄弟隔离

本套 **只** 覆盖 `svc-search`（`/service-center/search`）。不写 `svc-org-field` / `svc-org-trend` / `svc-org-capability`（`/service/institution-judgment`）及对比篮 COMPARE 深交互。
