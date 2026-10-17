# coverage · svc-sz 深圳服务链现状分析（脚本 → 用例）

> 主表列：脚本 id → 用例编号 → 页面区块/状态 → P（用例优先级）→ 档(A/B) → 可见动作 / skip ticket。
> 脚本 id 前缀与用例优先级列独立（勿混读）。金样 `index.gold` = P0-01~P0-05，本表不重复维护金样清单。
> 真源：`qa/test-cases/KJZTFWXT/service-产业服务链分析/SVCSZ-深圳服务链现状分析/FUNC-深圳服务链现状分析-用例.md`（v2.0，01283~01305）。

| 脚本 id | 用例编号 | 页面区块/状态 | P | 档 | 可见动作 / skip ticket |
|---|---|---|---|---|---|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01283 | 入口路由 / 页头双 Tab | P0 | A | 直达深链；断言 URL + title + 双 Tab 选中态 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01284 | 分析配置区 / 产业集群下拉 | P0 | A | 展开下拉；断言配置区构成 + 15 短名 + placeholder |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01286 | 开始分析门控（空态/选齐） | P0 | A | 空态软文案；选「新一代信息技术」后 enabled（勿点） |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01289 | 结果态统一评价框架说明卡 | P0 | A | 经历史「查看结果」；框架名/口径/待确认声明 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01294 | 结果态五城市对比图/诚实空 | P0 | A | 经历史「查看结果」；对比区三指标；无城市场景跟现场诚实空 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01285 | 配置区集群选定回显/改选/清空 | P0 | B | 选「新一代信息技术」→改选「新能源」→清空→Tab 往返；断言回显与 URL industry= 持久化、不自动起任务 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01287 | 显式触发开始分析 / 过程态 / 记录新增 | P0 | B | 选「新一代信息技术」→点「开始分析」；断言 view=processing&task_id 过程壳、分析记录新增已完成行、停过程页引导空态不自动跳结果 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01288 | 同用户同条件单飞拦截 | P0 | B | 点「开始分析」后在跑窗口内同条件立即复点一次；断言会话 POST /analysis/tasks 恰 1 次、过程页「开始分析」入口 0 残留、记录中本条任务恰 1 行已完成 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01290 | 结果态框架卡指标清单就绪度标注 / 指标集一致 | P0 | B | 经历史「查看结果」；逐项点 ⓘ 弹卡验就绪度四行区块（三项已登记待核验、完整度未登记 GAP 治理引用）；清单三项与对比区可选项逐一同名且完整度不在其中 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01291 | 结果态完整度诚实排除（红问号 / 治理引用 / 不参与渲染） | P0 | B | 经历史「查看结果」；断言完整度行「不参与后续对比图」标注 + aria-label=指标未登记：服务链完整度 + question 图标 + data-review-metric=GAP-SVC-SZ-CHAIN-COMPLETENESS；点开短卡仅治理引用无伪 8 件套；框架卡排除原因说明；对比可选项恰 3 项无完整度；无城市场景跟现场诚实空、无结论区 DOM 记 observed |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01292 | 结果态对比指标可选项构成与默认勾选 | P0 | B | 经历史「查看结果」；断言可选项=框架清单三项可用指标逐一同名（双向核对）、完整度零出现且区级口径段「服务链完整度不参与对比」明示排除、三项默认全选（.arco-checkbox-checked）；图区双分支（无城市场景诚实空记 observed） |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01293 | 结果态对比指标增减即时反映/刷新持久化 | P0 | B | 经历史「查看结果」；断言取消单项→勾选=2 且 URL 即时现 sz_metrics=tech,density、重新勾选→三项全选回显且参数清除、组合 reload 后 sz_metrics 与勾选态保留；图区双分支（无城市场景诚实空不出全取消越界提示，序列层记 observed）；收尾还原全选（P8） |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01295 | 结果态数值角标与梯队仪表盘 | P0 | B | 经历史「查看结果」（P8 双入口：goto 后 SPA 恢复结果态则短路消费）；断言对比区+框架清单 3 指标项逐项 ⓘ info-circle + 待确认角标（Q-SVC-010/Q060/Q062）+ data-review-metric 挂点；mock 角标随部署 USE_MOCK 双分支（50892=false 不渲染记 observed）；梯队双分支——有城市场景验梯队区标题+Q-SVCCHAIN-04 待确认角标+gauge/标签择一+描述一致，无城市场景（本环境实态）compare-empty 诚实空+梯队区结构性零渲染+正文无伪梯队词 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01296 | 结果态优势短板梯队结论引用图表数值 | P0 | B | 经历史「查看结果」（P8 双入口+基线归一残留 sz_metrics 补勾清参）；结论双分支——有城市场景验梯队/结论区三组构成（优势/短板/梯队软核对，快照缺组记 observed）+ 结论行数值逐一属 echarts 柱值集合无图外数值（filterSzConclusions 机制双保险）+ 取消「服务机构数量」后 scale 结论行随集合移除且剩余数值⊆新图柱值，无城市场景（本环境实态）compare-empty 诚实空+结论区/梯队区结构性零渲染+正文无优势/短板伪结论词+勾选变化不造伪结论负断言；收尾还原全选（P8） |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01297 | 备选-变更条件重析 | P0 | B | fresh 首发（新一代信息技术）→查看结果进结果态（前置「结果态可见」）→「返回配置重新分析」（sz as-built 落 tab=records&draft=1 切回主 Tab 恢复草稿）→改选「新能源」3s 静置断言 POST 增量 0（01285 互证）→显式「开始分析」重析：新 task_id≠首发+URL 零残留 INB1701+过程页「产业领域：新能源」重算+POST 恰 2 次→查看结果验新结果态：URL/正文零残留旧 task_id/旧产业名；框架卡按新任务承载；图表双分支（无城市场景诚实空+梯队/结论零渲染+无伪结论词，实跑 honest_empty） |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01298 | 页头双 Tab / 配置草稿保留 | P1 | B | 选「新能源」构造非默认草稿（industry= 持久化）→切「分析记录」Tab（激活互斥+选择器卸载+列表双分支：SVC-* 行有据/空态不报错，深验归 01299）→切回主 Tab；断言草稿回显保留不重置+URL industry= 保留码不变+POST 增量 0（任务只在开始分析显式触发，01287 互证）；实跑有据分支 pass |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01299 | 分析记录 Tab 列表与状态如实呈现 | P1 | B | fresh 发起一任务锚定本会话 task_id（前置「无则先发起一次」）→切「分析记录」Tab：互斥三证据（aria 互斥+选择器卸载+开始分析入口 0）+SVC-* 行有据+本条行流转勘察与「已完成」主判定（本条未达则既有已完成行承载，全无已完成才红）→全列表逐行巡检：已完成行必带可点「查看结果」（不伪装成功机检代理）、非完成行不得标已完成、状态词冲突记红；非完成行双分支（有据验状态多样性/全已完成验无伪装形态）；表头/时间/分页记 observed；实跑 pass（未捕到在跑窗口=任务秒完如实记） |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01300 | 备选-当天同条件已成功直接复用 | P1 | B | fresh 首发（新一代信息技术，指纹 svc\|shenzhen\|INB17xx 以现场 URL 为准）→查看结果验结果态「重新分析」入口（预期②承载面）→返回配置（sz as-built 落 tab=records&draft=1 切回主 Tab，P0-15 教训）→不改条件再点「开始分析」→复用三判据（POST 增量 0/落点=首发/toast 无「任务已创建」）→记录行查看结果直达既有结果壳 0 重跑；实跑 fail=设计红挂 D3-SVCSZ-SAME-DAY-REUSE-MISSING（078→079 仍新建、toast「任务已创建」，与 graph/chain/cultivate 三票并注同根因——四工作区全灭坐实共享闸门层 decideAnalysisTaskGate 指纹不等值） |
| P0-19 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01301 | 备选-兄弟 workspace 隔离（chain/graph 隔离） | P2 | B | sz 选「新一代信息技术」（industry=INB1701 持久化）→URL 直切 workspace=chain（落位/零泄漏：无 industry/task_id/view= 携带、无任务态文案、配置区完整）→切回 sz→URL 直切 workspace=graph（同口径）→再切回 sz：①同路由三 workspace 参数区分（URL 断言）②兄弟页零泄漏+全程创建任务 POST 0（01287 互证）③两次切回集群选定保留（探针 _probe-p019.json 实测 back1/back2 均回显空+industry 丢）——预期①②现场通过、预期③设计红挂 ticket **D3-SVCSZ-WS-SWITCH-STATE-LOST**（与 D3-SVCSHORT-WS-SWITCH-STATE-LOST / D3-SVCGRAPH-WS-SWITCH-STATE-LOST 姊妹票同根因：query 整体替换、产业参数纯 URL 驱动无草稿存储，三工作区同形态）；run=20261015-50892-sz-p0-19-r1（fail=设计红 2/6，其余 4 绿含 chain/graph 隔离与 0 POST 互证） |
| P0-20 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01305 | 异常-分析失败态（断链局部错误与重试） | P1 | B | route.abort 拦截创建任务 POST（精确尾段，不误伤 list/running 轮询）断链：①失败态 .arco-alert Network Error/traceId 局部错误提示在屏非白屏（与 graph P0-29/FUNC-00731 同构，useSvcAnalysisJob 共用层）②页面壳（title/页头双 Tab/分析配置）+集群回显保留+URL 停配置态不漂移+零任务态文案泄漏+「开始分析」仍可用（重试承载，无独立重试文案 D1 记档）③unroute 后重试 POST 200 落 view=processing&task_id 且 analysis_fp=svc\|shenzhen\| 前缀+产业上下文保留+alert 清除；防御票 D3-SVCSZ-FAILURE-STATE-MISSING 内置（探针未命中白屏/吞错形态）；实跑 pass（r1 脚本时序红 1/5 即修稿，r2 5/5 全绿） |
| P0-21 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01302 | 备选-评审模式零泄漏 | P1 | B | 评审开自适应（勘察=true）→三追溯按钮（深圳服务链现状分析/横向对比分析/分析配置，开启态现场 5 枚含 2 枚壳层共享不计泄漏）可见可点→逐一点击验弹层锚点（REQ-SVC-ECO-FRAMEWORK / REQ-SVC-ECO-COMPARE / 分析配置挂 US-SVC-ECO-05 无 REQ 前缀记 D1；Arco Trigger 单例常驻，唯一收场=空白点击）→关评审 reload 两 Tab 零泄漏三重断言（trace 0/评审层 DOM 0/字样 0 含指标标识与治理编号）→业务态不变（集群回显「新一代信息技术」+industry=INB1701+记录 26 行不变+配置骨架+0 POST）→联动可达分支：开态查看结果角标在场（data-review-metric=7+红问号 1，task SVC-20261015-085）→关态清零结果保留；模拟角标 USE_MOCK=false 不渲染记 observed；收尾还原评审开+配置态；run=20261015-50892-sz-p0-21-r1（pass 5/5） |
| P0-22 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01303 | 异常-全部取消对比指标（至少一指标提示） | P1 | B | 经历史「查看结果」→默认全选基线→逐项取消全部：checked=0 + URL sz_metrics=- + compare-none「请至少选择一个对比指标」（D1：用例「选一个」vs 现场「选择一个」）→保留/空轴双分支（有城市 lastRows 保留 grid 序列；无城市本环境诚实空+canvas=0 不绘空轴）→P8 还原全选；探针 _probe-p022.json 实证；与 P0-12 划界（01293 组合≥2 负断言 none 不可见） |
| P0-23 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01304 | 异常-无数据柱位占位（缺值「无数据」不以 0 填） | P2 | B | GAP：首包前挂窄 **/tasks/*/result* inject cities（禁宽 **/tasks* 误伤 task/events）；grid+canvas + 口径「无数据」+ parse 北京 null≠0；B 档零 allow_skip；与 P0-05 划界 |

## 未脚本化（本轮声明）

- （无）本入口 01283~01305 已全部脚本化（P0-01~P0-23）；入口末缺口 01304 已交 P0-23。

## 备注

- 实勘真源：`fixtures/scout/`（env-gate.json + scout-b32-s1~s6 + scout-after-pick 等）。
- D1-SVCSZ-CLUSTER-SHORT-NAME：现场短名跟用例附录 A 全名差异，expect 跟现场短名。
- D4-SVCSZ-RESULT-VIA-HISTORY：结果态一律经历史「查看结果」，禁默认 fresh 起任务。
