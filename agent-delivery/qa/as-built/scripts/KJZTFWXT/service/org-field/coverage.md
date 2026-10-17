# 服务机构产业领域分析 脚本→用例 覆盖表（R3 新写）

蓝本 = `qa/test-cases/KJZTFWXT/service-产业服务链分析/SVCFIELD-服务机构产业领域分析/FUNC-服务机构产业领域分析-用例.md` v2.0（00641~00655）。
env-gate overall=pass（2026-10-14）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 档 | 可见动作 / skip ticket |
|---------|----------|---------------|---|----|------------------------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00641 | 入口·路由与双 Tab | P0 | A | 直达 field/coverage |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00642 | 配置空态 | P0 | A | 三控件 + 无结果区 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00643 | 选择机构回显 | P0 | A | 选 1 家确定回显 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00645 | 开始分析门控 | P0 | A | 空态引导文案（勿硬判 disabled）+ 显式触发 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00646 | 结果·热力/诚实空 | P0 | A | 跟诚实空「当前结果快照没有覆盖矩阵」as-built |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00644 | 机构集合操作·加选/取消/移除 | P0 | B | 自含构造 2 家；tag close-btn 移除（D1，无「移除」按钮）；footer 取消；执行时记 observed 编码 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00647 | 结果·热力图 hover 与 ⓘ/演示角标 | P0 | B | ENV-SVC-ORG-FIELD-HEATMAP-EMPTY（热力图诚实空：hover 明细 X3 代理验壳+诚实空；ⓘ/待核验角标现场渲染，成对可见断言；兜底 allow_skip 归票） |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00648 | 矩阵图与图型切换 | P0 | B | ENV-SVC-ORG-FIELD-HEATMAP-EMPTY（结果态热力图诚实空：前置「热力图已呈现」不满足 → allow_skip 归票；scout-p008 实勘 switch 往返互斥可点，非空环境全量机跑） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00649 | 领域筛选不改指纹 | P0 | B | 零归票真实机检（scout-p009 实勘：配置态筛选键入收窄 15→1、清除恢复；URL 无任务参数；不依赖热力图数据） |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00650 | 分析记录·列表/当天复用/显式重析 | P1 | B | D3-SVCORG-SAME-DAY-REUSE-MISSING（当天同条件复用判定红挂第五工作区侧票，与 sz/graph/chain/cultivate 四票并注同根因；绿则转例外对照）；列表呈现与记录行直达 0 重跑真实机检；变更显式重析真实机检；诚实空板按 ENV-SVC-ORG-FIELD-HEATMAP-EMPTY 同票注记（scout-p010/p010b 实勘：列表 5 列 6 条全已完成、查看结果直达、同条件 088→089 仍新建、变更 090 新任务） |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00651 | URL 直达与刷新保留 | P1 | B | 零 allow_skip；scout-p011 实勘冷加载恢复 workspace/tab/org_ids、reload 保留、回 coverage 已选 1 家；新标签=同 page 冷加载（D1） |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00652 | 备选·三兄弟 workspace 隔离 | P0 | B | 侧栏 field→trend→capability→field；隔离+切回落位+0 POST 机检；「切回保留」manual+ticket **D3-SVCORG-WS-SWITCH-STATE-LOST**（与 sz/graph/short 姊妹票并注同根因；REWORK：不硬红挡交卷、不假绿抹设计红）；scout-p012；不进 gold |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00653 | 备选·评审模式零泄漏 | P1 | B | 零泄漏+已选保留机检；「开关不改领域筛选」manual+ticket **D3-SVCORG-REVIEW-TOGGLE-FILTER-LOST**（REWORK：不硬红挡交卷、不假绿抹设计红；对照 P0-12）；scout-p013-review；零 allow_skip；不进 gold |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00654 | 异常·配置空态与无覆盖数据行 | P1 | B | 配置空态无图表 + 结果诚实空/不排名真实机检；精确「暂无覆盖数据」行 manual+ticket **ENV-SVC-ORG-FIELD-UNCOVERED-ROW-UNREACHABLE**（并注 HEATMAP-EMPTY；scout-p014：hasMatrix=false 诚实空矩阵代理，D1 不假绿）；不进 gold |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00655 | 异常·分析失败态（断链局部错误与重试） | P1 | B | 零 allow_skip；route.abort：①失败态 .arco-alert Network Error/traceId 非白屏（scout-p015-fail.json aborted=1）②壳+领域筛选/机构回显+「开始分析」仍可用（D1 无独立重试文案）③unroute 重试四分支联合轮询 processing\|CREATE404\|局部错误\|静默配置态（探针本轮 create_404；D4 **ENV-SVC-ORG-FIELD-CREATE-404** / **ENV-SVC-ORG-FIELD-RETRY-SILENT-CONFIG**）；防御票 **D3-SVCORGFIELD-FAILURE-STATE-MISSING**；深链 org_ids；不进 gold |

00641~00655 十五用例脚本已齐（P0-01~P0-15）；金样仍锁 P0-01~05。
