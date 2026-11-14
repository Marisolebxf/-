# POL-L2-DS10-TREND-205-FDE · 波次 C · algorithm-agent

- 身份：`agent:algorithm-agent`
- 日期：2026-11-15
- 被审：说明书「#### 205 重点领域政策分析（2026-11-15）」；`sdd/简报/2026-11-15-205-FDE-B-读法.md`
- 硬清单：`.cursor/skills/gkx-fde-design-change/审稿硬清单.md` algorithm-agent 三条
- 本签只审稿。不改说明书，不改读法，不改代码，不 commit
- 监管：`human:淮政玮`（2026-11-15 已确认计划）。总单 `POL-L2-DS10-TREND-205-FDE`
- 结论：有异议，4 条

## 硬清单核对

1. 统计数字：政策条数、平均评分是统计数字，本叶没有 `metric_id`。热度不是新的分数，是已有 `M_POLICY_TIMESERIES` 的走向标签。`metric-get`：`M_POLICY_TIMESERIES`，中文名「政策时序指标」，`algorithm_type=STAT`，D1=`aligned`，D2=`partial` 且 `provisional`，D4=`mock`。口径是发布量历史段（2015-01—2022-08）可复算，2022-09 之后当前段没有记录，不能单独承担趋势监测；连续性仍是 QPOL-07。本波读法写明不改 D2、不改 D4。
2. 新 `metric_id` / 改 D4：说明书和读法都不新造时序，不把「技术发展方向」写成第四条指标，不给热点、影响、深度报告注册 `metric_id`。`metric-query`（政策域，关键词含条数、评分、热度、重点领域）0 条。本波文本本身没有新 id，也没有改 D4。异议 1、2 要求把卡上两格也写成「不新注册」。
3. 非本叶口径：读法写明热点不读 `M_POLICY_FOCUS_INDEX` 和热度分，影响不读 `M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_SIMULATE`，深度报告不读序号 211、217。这三条本签同意。热度把整页一条时序贴进四张领域卡，见异议 3。平均评分有被上述分数误填的口子，见异议 2。

打开热点、影响、深度报告：按 2026-11-15 读法不调模型。现行展示也是只读。`PolicyPanoramaService.jobs` 在 body 带 `kind`（热点识别 / 政策影响评估 / 深度分析报告）时走 `syncTrendKind`，element `GET /trend/hotspot|impact|report` 读缺项表，不建任务，不打 `/internal/policy/jobs/execute`。`kind` 与 `sub_type` 同传则空记录。前端 `trendJobBodyOf` 只传 `kind` 和领域。导出 `POST /display/v1/situation/report/generate` 的契约是前端提交已有 HTML，域服务产出文件，不是模型生成。中台按领域写在 `demo_gkxlumenx_ads`，本波展示不读该库、不改展示页。正式库种子行（`lumen-algo-py/scripts/mysql/gapfill_policy_trend.sql`）正文都以「缺项演示」开头，`metric_id` 为空，`fill_method=manual`；按读法这些行不算结果。风险见异议 4。

## 异议

[algorithm] 1 · 政策条数是统计数字，成功态没有读列，也没有 `metric_id`。 · 说明书 205-1 仍要求每张卡看见政策条数；205-2 只规定没汇总时写「—」、不写 0。读法 205-2 不读种子 `totalPolicies`，也不给这一格表和列。METRIC 第 6.3 节只说热点、影响、报告不新注册，没点名政策条数。现行卡 `KeyFieldAnalysisPanel.vue` 把 `field.totalPolicies` 显示成「N 项政策」，种子是 128 / 86 / 102 / 74（`policySeed.ts` 的 `keyFieldPolicyAnalysis`）。D9：界面上的统计数字要有 `metric_id`。 · 本波这一格固定「—」或空，有两句举措时也不显示整数。不拿全景列表长度充数，不新注册 `metric_id`，不改任何 D4。后波若要件数，先注册再接线。

[algorithm] 2 · 平均评分是均分，没有 `metric_id`，缺项表和时序表都没有分列，成功态仍可能被填上别的分数。 · 说明书 205-1 仍要求看见平均评分；205-2 只在没做时写「—」。读法不读种子 `avgScore`。DATA 第 5.2 节不放分数字段。METRIC 第 7 节禁止把 `M_POLICY_FOCUS_INDEX`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_SIMULATE` 改挂成热点或影响，没有写卡上「平均评分」不得用这些分。现行卡显示「平均评分：N 分」，种子是 89.2 / 86.4 / 84.7 / 88.0。 · 平均评分本波不是指标。成功态同样写「—」。禁止用焦点指数、实施效果、推演分、热度分或种子分填这一格。不新造 `metric_id`，不改 D4。

[algorithm] 3 · 热度不是新的统计数字，但四张领域卡共用整页一条 `M_POLICY_TIMESERIES`，上升 / 稳定 / 下降没有可复算阈值。 · 读法 205-3：热度对上 `GET /display/v1/policy/panorama/stats` 的 `gkxlumenx_ads.policy_timeseries`（`period_type`、`period_key`、`publish_count`），四张卡都对整页这一条；不读分领域时序，不读 `M_POLICY_FOCUS_INDEX`。`metric-get` 的公式是发布量过程复算，不是热度分类；D4 仍是 `mock`。说明书 205-3 把「往上 / 走平 / 往下」写成做完必须看见的字，没有写比较几期、变化多少算走平。现行卡热度来自种子 `trend`（只有上升、稳定），不读时序；本波不改展示页，卡上还对不上这条时序。 · 不新造热度 `metric_id`，D4 保持 `mock`，禁止用热度分代替。本波卡上热度保持现状，不要写成已经跟时序一致。后波接线时写明比较窗口和走平阈值，并在四张卡上标明这是整页时序走向，不是该领域自己的热度。

[algorithm] 4 · 「打开已生成的热点 / 影响 / 深度报告」还没压住旧稿里的现场生成；空态不能再去调模型。 · 读法：打开和点入口都不调模型，不提交 `sub_type=policy_trend_cache`，进度条只表示把已有行读完。现行 `jobs(kind)` 与此相符，是同步读表。说明书第 84 行把「中台已按领域生成」和「打开已经生成好的结果」写在一起，生成结果在 `demo_gkxlumenx_ads`，展示本波仍读 `gkxlumenx_gapfill`。正式库三张表的种子正文都以「缺项演示」开头，按读法应是空态。ARCH 第 7.4 节、METRIC 第 6.3 节仍写热点走 `jobs`、未缓存就 Python 写回；读法点名要改，本波四单不改。若实现按旧 7.4，打开就会打 `/internal/policy/jobs/execute`。 · 会签钉死：展示打开只读正式库缺项表里该领域的合格行；以「缺项演示」开头视为没有结果；不读演示库，不提交 `policy_trend_cache`，不调模型，空态不补生成。导出仍用已有 `situation/report/generate`，只排已有正文，不因此调模型。四单在后波改句之前，不以 ARCH 7.4 为准。
