# 服务机构新增趋势分析 脚本→用例 覆盖表（R3 新写）

蓝本 = `qa/test-cases/KJZTFWXT/service-产业服务链分析/SVCTREND-服务机构新增趋势分析/FUNC-服务机构新增趋势分析-用例.md`
env-gate overall=pass（2026-10-14）。tickets：`ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD` 等。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 档 | 可见动作 / skip ticket |
|---------|----------|---------------|---|----|------------------------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00656 | 入口·深链双 Tab | P0 | A | workspace=trend |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00657 | 配置·产业 15 | P0 | A | 配置区构成 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00658 | 选择机构回显 | P0 | A | 选机构确定 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00659 | 门控+显式开始 | P0 | A | 文案门控；→processing；不断言有数折线 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00667 | 分析记录/查看结果 | P0 | A | 或 00668 评审零泄漏 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00660 | 结果态趋势图（X 时间/Y 数量/明细同源） | P0 | B | allow_skip 前置 `.svc-org-trend__legend button`→n/a · ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`（REWORK：禁 SKIP throw→fail；深链结果壳；scout-p006-series.json；有序列后 canvas+明细实跑） |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00661 | 趋势图数据点悬停明细 + 新增数量角标 | P0 | B | allow_skip 前置 `.svc-org-trend__legend button`→n/a · ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`（REWORK/SKIP_FIELD：补 ticket；禁 SKIP throw→fail；深链结果壳；scout-p007-hover.json；有序列后 hover+角标实跑） |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00662 | 明细表下钻画像（机构名→抽屉→关闭滚动保留） | P0 | B | allow_skip 前置 `.svc-org-trend__legend button`→n/a · ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`（REWORK/SKIP_FIELD：补 ticket；禁 SKIP throw→fail；深链结果壳；scout-p008-detail.json；有序列后 svc-org-link→抽屉→滚动保留实跑） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00663 | 研判面板与依据（斜率/波动+星级/文字评级+依据行+未闭合口径标识） | P0 | B | allow_skip 前置 `.svc-org-trend__legend button`→n/a · ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`（REWORK/SKIP_FIELD：补 ticket；禁 SKIP throw→fail；深链结果壳；scout-p009-heat.json；有序列后斜率/星级/依据行+GAP 口径标识实跑） |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00664 | 配置·领域筛选不改指纹（键入收窄/清除恢复/不自动分析/不改已选） | P0 | B | 零 allow_skip；配置态真实机检（scout-p010-filter.json：15→1→15；已选 tag 保持；URL 无任务参数） |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00665 | 结果态·切换主领域重算 + 对比曲线≤3 + 图例可见性 | P1 | B | allow_skip 前置 `.svc-org-trend__legend button`→n/a · ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`（REWORK：禁 SKIP throw→fail；深链结果壳；scout-p011-switch.json；D1「重新分析」） |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00666 | 结果态·时间窗切换刻度/曲线/明细同步 | P1 | B | allow_skip 前置 `.svc-org-trend__legend button`→n/a · ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`（REWORK：禁 SKIP throw→fail；对齐 P0-11；深链结果壳；scout-p012-window.json；D1 近3/5/8 年无近10年） |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00668 | 评审模式零泄漏（两枚追溯显隐） | P1 | B | 零 allow_skip；配置态真实机检（scout-p013-review.json：开态 2 追溯可点+弹层；关评 reload 零泄漏；产业/URL 指纹保留） |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00669 | 异常·研判诚实空态（不足 3 年 / 全 0 不出伪评级） | P1 | B | allow_skip 前置 `.svc-org-trend__legend button`→n/a · ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`（GAP：scout-p014-honest-empty.json 仅 no_series；两文案需 hasYearSeries 构造） |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00670 | 异常·分析失败态（断链局部错误与重试） | P1 | B | 零 allow_skip；route.abort：①失败态 .arco-alert Network Error/traceId 非白屏（scout-p015-fail.json aborted=1）②壳+领域/机构回显+「开始分析」仍可用（D1 无独立重试文案）③unroute 重试四分支联合轮询 processing\|CREATE404\|局部错误\|静默回配置态「分析条件已就绪」+壳筛选保留（D4 `ENV-SVC-ORG-TREND-CREATE-404` / `ENV-SVC-ORG-TREND-RETRY-SILENT-CONFIG`；REWORK×2 修 r3-runner C6 环境漂移）；防御票 `D3-SVCORGTREND-FAILURE-STATE-MISSING`；深链 org_ids 绕过空名单 |

有数折线/热度研判（00661/00663）→ B + `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`。00660 趋势图默认呈现 REWORK P0-06（2026-10-15）：B 档 allow_skip 前置图例按钮→n/a（禁 SKIP→fail）；scout-p006-series.json；有序列后 canvas+明细实跑；不进 gold。
00661 悬停明细 REWORK P0-07（2026-10-15 SKIP_FIELD）：B 档 allow_skip 前置图例按钮→n/a（对齐 P0-06；补顶栏 ticket；禁 SKIP→fail）；scout-p007-hover.json；有序列后 hover sweep→tooltip + ⓘ/演示角标实勘（开放项 3 不硬断言）；不进 gold。
00662 明细表下钻 REWORK P0-08（2026-10-15 SKIP_FIELD）：B 档 allow_skip 前置图例按钮→n/a（对齐 P0-06/07；补顶栏 ticket；禁 SKIP→fail）；scout-p008-detail.json；深链结果壳；有序列后 svc-org-link → .arco-drawer 可达 → 关闭 → scrollY 差 ≤2px + 明细区块回归（抽屉内容归画像用例集不硬断言，开放项 3）；不进 gold。
00663 研判面板 REWORK P0-09（2026-10-15 SKIP_FIELD）：B 档 allow_skip 前置图例按钮→n/a（对齐 P0-06~08；补顶栏 ticket；禁 SKIP→fail）；scout-p009-heat.json；深链结果壳；有序列后斜率/波动 + 星级/文字评级 + 依据行 + GAP-SVC-ORG-HEAT/Q-SVCCHAIN-02/演示口径 note 四 expect 实跑；不进 gold。
00664 领域筛选不改指纹已落 P0-10（2026-10-15）：B 档零 allow_skip；配置态真实机检（scout-p010-filter.json：键入收窄 15→1、清除恢复 15、已选 tag 保持、URL 无任务参数）；与 ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD 无交集；同构姊妹 org-field P0-09。
00665 切换领域与对比曲线 REWORK P0-11（2026-10-15）：B 档 allow_skip 前置命中图例按钮→runner 记 n/a（对齐 org-field；禁断言内 SKIP→fail）；深链 `view=result&demo_state=result`；expect-0 P7 点 `.arco-select-view`+双 popup 选项 selector、无可选项门控红禁假绿；有序列图例可见后全量实跑（切换重算不残留 / 对比≤2 tag+超限提示 / 图例开关不改已选集合）；scout-p011-switch.json；不进 gold。
00666 时间窗切换 REWORK P0-12（2026-10-15）：B 档 allow_skip 前置命中图例按钮→runner 记 n/a（对齐 P0-11；禁断言内 SKIP→fail）；深链 `view=result&demo_state=result`；scout-p012-window.json——近3/5/8 年（无近10年=D1）；有序列后 expect-0/1 时间窗控件可绿 + expect-2 X3 明细年份跨度代理；不进 gold。
00668 评审模式零泄漏已落 P0-13（2026-10-15 GAP）：B 档零 allow_skip；scout-p013-review.json——开态 main「服务机构分析工作区」「分析配置」两枚 `trace-info-icon` 可见可点、弹层含 US-SVC-ORG 锚点（D1 无 REQ 前缀）；壳层共享 2 枚不计；关评 reload 后 trace/metric 卡/metric_id·Q0xx·Q-·GAP- 字样全 0；产业「新一代信息技术」+ `industry=INB1701` 与 workspace=trend 主 Tab 保留。与 ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD 无交集；不进 gold。
00669 研判诚实空态已落 P0-14（2026-10-15 GAP）：B 档 allow_skip 前置图例按钮→runner 记 n/a（对齐 P0-11；禁 SKIP→fail）；scout-p014-honest-empty.json——仅 no_series「暂无趋势序列，无法给出热度研判」、星级=0、insufficient/no_activity 均未现；目标态文案「数据长度不足，暂不给出热度研判」/「该领域暂无服务供给活动」源码已备（svcTrendModel），有序列后扫产业实跑；ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`；不进 gold。
00670 分析失败态已落 P0-15（2026-10-15 GAP；REWORK×2 修 r3-runner C6）：B 档零 allow_skip；route.abort 同构 sz P0-20/graph P0-29（useSvcAnalysisJob）；scout-p015-fail.json——aborted=1、Network Error/traceId 壳层 alert、双 Tab/分析配置/产业+已选机构保留、「开始分析」即重试（D1）；深链 org_ids[]=79bbcfc0… 绕过 search/orgs 空名单（D1）；unroute 重试四分支联合轮询（processing / CREATE404 文案 / 壳层局部错误 / 静默回配置态「分析条件已就绪」+壳筛选保留；前三分支 20s 未命中后终态认④，防抢跑；用例预期不要求必落任务态）→ D4 `ENV-SVC-ORG-TREND-CREATE-404` / `ENV-SVC-ORG-TREND-RETRY-SILENT-CONFIG`；防御票 `D3-SVCORGTREND-FAILURE-STATE-MISSING`；不进 gold。
