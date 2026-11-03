# POL-L2-DS11-READ-METRIC · 政策分析评价 · 结果解读报告多维展示 · 后台指标设计

- 任务：`POL-L2-DS11-READ-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`（已认领，本叶不再认领，不改任务状态）
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-READ-ARCH.md`（任务 `POL-L2-DS11-READ-ARCH` 于 2026-11-03 已签收，签收人 human:淮政玮；本叶读面以该稿与 `sdd/l2/会签/POL-L2-DS11-READ-SIGNOFF-ARCH.md` 为准）
- 会签态：未会签。本叶不代签，不标 done
- 查询：2026-11-03 经 MCP `metric-get`。未读 seed、矩阵 YAML，未改注册表，未改 D4

本叶只写政策分析评价二级「结果解读报告多维展示」的指标挂接。SRS 序号 **223–226**。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-READ-ARCH.md`、`sdd/l2/会签/POL-L2-DS11-READ-SIGNOFF-ARCH.md`、`sdd/指标与501.md` 评价表 223–226 行、说明书第 2 节 DS-11 同序号。不新注册指标，不改 D4，不写假公式，不改算法代码，不写 OpenAPI。

## 1. 范围

四叶都在政策分析评价里完成。指标身份沿说明书第 2 节与 `指标与501.md` 已有 `metric_id` 和三档判定。读面沿已签收的 `POL-L2-DS11-READ-ARCH`。本叶不改那几份文件。

| 序号 | 叶子 | 指标与501 / 说明书第 2 节 | 本叶 |
|---|---|---|---|
| 223 短板条数 | 热点问题分析看板 | `M_POLICY_SHORTBOARD_COUNT`；STAT；D4=`mock`；可接统计读面 | 只挂这一条。已有统计读面。同步 `counts` 只读已写入的 `shortboard_cnt`。无行则空，不造 0。不把源模型改挂上来 |
| 223 焦点指数 | 热点问题分析看板 | `M_POLICY_FOCUS_INDEX`；MODEL；D4=`mock`；判定列 501 | 只挂这一条。三档保持指标分册的 501。不改成可算公式。读已有 `ads.policy_focus` 的行。无行则空 |
| 224 | 分主题分指标互动解读 | 未见 `metric_id`；判定列 501 | 没有专属指标，不新造，不写公式。页面读 `gapfill_policy_eval_shell` 的解读条目。行内文字不是指标结果 |
| 225 | 多媒体辅助解读 | 未见 `metric_id`；判定列 501 | 没有专属指标，不新造，不写公式。页面读同一张缺项表的标题和一句说明。不灌视频 |
| 226 | 智能摘要与结论推送 | `M_POLICY_DS_11_POLICY_EVAL_012`；MODEL；D4=`mock`；判定列 501 | 只挂这一条。三档保持 501。请求只读已有 `summary` 列，不写成现算 `parse.run`。无行则空 |

223 短板与 226 的 D4 仍是 `mock`。焦点指数的 D4 也仍是 `mock`。`QPOL-02` 未闭合。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿视为未解开。本叶不把 mock 写成已上线。

机遇条数 `M_POLICY_OPPORTUNITY_COUNT` 没有 223–226 的序号，不挂进本二级。

## 2. 本二级用到的已有 metric_id

挂接去重后 3 条，落在 223 短板、223 焦点、226。224、225 不在此表。全部 `metric-get` 为 `found.seed=true`、`found.matrix=true`、`found.srs_map=true`。D4 都是 `mock`。中文名、`algorithm_type` 以 MCP 为准。

| metric_id | 中文名（MCP） | algorithm_type | D4 | 挂在 |
|---|---|---|---|---|
| `M_POLICY_SHORTBOARD_COUNT` | 政策短板清单条数 | STAT | mock | 223 短板 |
| `M_POLICY_FOCUS_INDEX` | 政策焦点指数 | MODEL | mock | 223 焦点 |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 智能摘要与结论推送 | MODEL | mock | 226 |

这 3 条之外，本二级不新造 `metric_id`。

叶子名与注册中文名不一致的，以 MCP 为准，挂接 id 不变：

- 223 短板的叶子语境是「短板条数」。注册中文名是「政策短板清单条数」。类型仍是 STAT。不改挂成源模型 `M_POLICY_DEEP_169_1`，也不改判成 MODEL。
- 223 焦点的叶子语境是「焦点指数」。注册中文名是「政策焦点指数」。类型仍是 MODEL。三档仍是指标分册的 501，不改判成可接统计读面，也不改写成可算公式。
- 226 的叶子名与注册中文名都是「智能摘要与结论推送」。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进本节。

源系统三条相同：`gkx @ 183.240.141.251:3318（只读）`。`version` 都是 `1`。

| metric_id | 中文名 | algorithm_type | 源表 | 更新频率 |
|---|---|---|---|---|
| `M_POLICY_SHORTBOARD_COUNT` | 政策短板清单条数 | STAT | `dwd_patent`、`dwd_policy_base` | weekly |
| `M_POLICY_FOCUS_INDEX` | 政策焦点指数 | MODEL | `dwd_industry_chain_info`、`dwd_policy_base` | weekly |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 智能摘要与结论推送 | MODEL | `dwd_patent`、`dwd_policy_base`、`dwd_policy_summary`、`dwd_policy_summary_edit_log` | pending |

短板条数和焦点指数的注册公式都是过程指针：见 calc-logic「计算逻辑说明」与 20261021 正本 §二；公式是过程式复算，未浓缩为单行表达式；禁手抄，实现时以 `code/<metric_id>.py` 为准。注册指针分别为 `metrics/calc-logic/POLICY/M_POLICY_SHORTBOARD_COUNT.md`、`metrics/calc-logic/POLICY/M_POLICY_FOCUS_INDEX.md`。本叶不手抄、不展开成可执行式。焦点指数不另写一条能算出指数的式子，三档仍是 501。

226 的注册 `kit.formula` 是一行表达式：`D1=(主料率+上下文率)/2；D2=min(1, 平均句数/3)；D3 缺维不进平均；可算维等权 ×100`。`d1_note` 写公式未签，`pending_ref` 为 `GAP-ALGO-TYPE-UNSIGNED`。这行是身份，不是 226 这次请求的计算。本叶不签、不执行、不把它改写成摘要生成式。请求只读已有摘要列。

口径按 `metric-get` 的 `kit.definition` 摘录，不改写。

| metric_id | 口径 |
|---|---|
| `M_POLICY_SHORTBOARD_COUNT` | 合规维有真触发（34.16% < 90%）。覆盖维与有效维被代理成 100%，原生子项主题覆盖、时效不可算。注册口径里的「条数 = 1」是「一维真短板 + 两维不可判」的合成说明，不是三维体检后只有一处问题。注册判定为部分支持。口径标记 QPOL-02，本叶不改口径，不闭合。这次 `counts` 不把「条数 = 1」当作返回值 |
| `M_POLICY_FOCUS_INDEX` | 四维里三维靠正文词频可算，第四维「措施执行情况」因 `policy_support` 全为 JSON null 不可读。按缺失维度不进平均，注册判定为部分支持。口径标记 QPOL-02，本叶不改口径，不闭合，不把这段判定改写成可算公式。三档仍是指标分册的 501 |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 信息覆盖度与结论条数可算。推送就绪所需的 `dwd_policy_summary(push_status)` 与编辑日志表在 gkx 中不存在，整维不可算。按缺维不进平均合成的分数是就绪度，不是质量；库内没有人工参考摘要、人工评分和推送回流。注册判定为部分支持。本叶不把该分数写成摘要正文 |

223、226 的展示读数不在接口里重算，也不替换上表的注册公式。已签收架构指认：短板条数读 `ads.policy_effect` 里已经写下的 `shortboard_cnt`；焦点读 `ads.policy_focus` 里已经写下的行；226 读 `ads.policy_text_parse.summary`。上表源表是注册身份，不是这三条展示读表。本叶不把 `dwd_policy_summary` 写成 226 的读表。

`extras.algo_server_location` 指向 demo 仓 `polan/metrics/metrics.py` 与 `polan_metric_routes.py`。那是注册表索引，不是本二级的展示调用链。本叶不改那些文件，也不把展示改去调 demo 服务。展示仍按架构稿：浏览器只打 `/display/v1/policy/**`。

## 4. 接入状态

接入状态不是八件套。下表来自 `metric-get` 的 `readiness`。D1 都是 `aligned`，D2 都是 `partial` 且 `d2_assessed=provisional`（待核验），D4 都是 `mock`。本叶不改任何一维。D2 的 provisional 保留「待核验」，不在本叶改绿。

| metric_id | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| `M_POLICY_SHORTBOARD_COUNT` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_FOCUS_INDEX` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_DS_11_POLICY_EVAL_012` | aligned | partial，待核验 | partial | mock |

`is_mock=true`。`d4_note` 写算法服务未上线，保持 mock。对齐前数值仍是 mock。本叶不改 D4。

需求来源不是八件套。沿用查询结果，本叶不改挂：

| metric_id | srs_refs | 本叶用法 |
|---|---|---|
| `M_POLICY_SHORTBOARD_COUNT` | 专题 05/169 政策短板识别模型；`page_ids` 含 `DS-11-POLICY-EVAL`、`E7-POLICY`；`systems` 为专题、展示 | 只挂 223 短板。需求来源序号不是 02/223。本叶不改 `srs_refs`，也不把 05/169 改挂成展示新指标 |
| `M_POLICY_FOCUS_INDEX` | 专题 05/166 政策焦点识别模型；`page_ids` 为 `DS-11-POLICY-EVAL`；`systems` 为展示 | 只挂 223 焦点。需求来源序号不是 02/223。三档仍是 501。本叶不改 `srs_refs` |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 展示 02/226 智能摘要与结论推送；`page_ids` 为 `DS-11-POLICY-EVAL`；`systems` 为展示 | 只挂 226。不改挂到 224，也不改挂成 `M_POLICY_TEXT_PARSE` |

## 5. 223、226 怎么读

读面沿架构稿与架构会签页，不新开路径，不新造指标。切条件不自动起任务。Job 失败不清空已经返回的短板计数和解读条目。无行则空，不写假公式。

### 5.1 223 短板条数

只挂 `M_POLICY_SHORTBOARD_COUNT`。MCP：中文名「政策短板清单条数」，STAT，D4=`mock`，QPOL-02。这是已有统计读面，三档与 `指标与501` 一致：可接统计读面。

同步读，不进 Job：

- 浏览器读 `GET /display/v1/policy/evaluation/counts`。
- `gkxlumen-element` 只读 `ads.policy_effect` 里 `scope_type=region_gap` 的 `shortboard_cnt`。
- 这次 GET 不调用 `polan.eval.gap.run`。写入仍由已有 `gap.run()` 完成。本叶不改该函数，不抄公式。
- 源模型 `M_POLICY_DEEP_169_1` 仍是 MODEL，不在这条同步链上计算，也不改挂成这条短板条数。

无 `region_gap` 行则该计数空，不造 0，不回填注册口径里的「条数 = 1」。不返回 501 充当这个数。D4 保持 mock。`GDF-POLICY-MDC-STAT-L01` 不含本指标，本叶不把它写成已覆盖。不建 `ads.policy_gap`。

### 5.2 223 焦点指数

只挂 `M_POLICY_FOCUS_INDEX`。MCP：中文名「政策焦点指数」，MODEL，D4=`mock`，QPOL-02。

`指标与501` 的三档判定是 501：已注册 MODEL，页面空态。说明书第 2 节写「焦点指数：501」。本叶保持这一档。不改成可接统计读面，不把注册过程指针展开成词频、权重或 `focus_score` 的计算式。

读面沿已签收架构，只读已经写下的行，不在本叶定义怎么算出指数：

1. 浏览器提交 `POST /display/v1/policy/evaluation/jobs`，`sub_type=policy_focus_ads`。
2. `gkxlumen-display` 调用已有 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`。display 不算指数，也不直接调 `jobs/execute`。
3. 已有 `PolicyAnalysisAdapterImpl` 再调 `POST /internal/policy/jobs/execute`。
4. 写入仍由仓库里已有的 `polan.eval.focus.run` 完成。本叶不重写该函数。看板再读 `ads.policy_focus` 里 `policy_id` 非空的行：`focus_score`，以及 `ext` 里已有的 `title`、`explanation`。

`run()` 只删除 `policy_id` 非空的行再写入，不删除 `policy_id` 为空的机遇行。本叶不改这个删除范围。名称和一句说明落在已有 `ext` 上，不另建 `gapfill_policy_eval_focus`。

`sub_type` 尚未放行，或表里没有 `policy_id` 非空的行时，焦点块空。不返回写死指数，不返回 `focus-one` 的当场计算结果，不用 501 这个词充当一个数值。D4 保持 mock。QPOL-02 的权重保持待确认。

带 items 的既有 `policy_focus` 仍走 `harness.dispatch`。展示看板不走那条，也不把 harness 的返回当成热点看板。

`M_POLICY_RELATION_DEGREE` 写在同一行的 `relation_degree` 上。本叶不把它改挂到 223，也不为此读图。

### 5.3 226 智能摘要与结论推送

只挂 `M_POLICY_DS_11_POLICY_EVAL_012`。MCP：中文名「智能摘要与结论推送」，MODEL，D4=`mock`。需求来源即序号 226。

`指标与501` 的三档判定是 501：NLP 摘要未见单独模型任务，页面空态。本叶保持这一档。不把注册式 `D1/D2/D3` 当成这次请求的现算，也不另写一条从正文生成摘要的式子。

请求只读已有摘要列，不现算：

1. 浏览器提交 `POST /display/v1/policy/evaluation/jobs`，`sub_type=policy_text_parse`。
2. 内部跳与第 5.2 节相同：`gkxlumen-display` → `POST /topic/v1/analysis/tasks` → `PolicyAnalysisAdapterImpl` → `POST /internal/policy/jobs/execute`。
3. Python 只查询 `ads.policy_text_parse.summary`。这次请求不调用 `polan.text.parse.run`，不调用大模型。

`parse.run` 会清空整张 `ads.policy_text_parse`。所以 226 的请求路径只查询。摘要列仍由已有解析批次写入；该写入是规则截取，不是本叶新定的公式。行上的 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。本叶不改这个行上 id，不把 226 改挂成文本解析，也不把截取升级成大模型。`M_POLICY_DS_11_POLICY_EVAL_012` 是这列的展示读面身份，不是第二套摘要。

不把 `dwd_policy_summary` 或 `policy_summary` 当成这叶的读表。不建 `gapfill_policy_eval_summary`。

无行则摘要空。不返回写死段落，不返回注册口径里的就绪度分数，不用 501 充当正文。可编辑和推送没有登记的用户表，也没有发信通道。本叶不建编辑表，不把改过的句子写回 ADS，不灌假通知。用户当时在页面上改字，不构成本条资源。D4 保持 mock。

## 6. 224、225 没有专属指标

224、225 在说明书第 2 节和 `指标与501` 里 `metric_id` 为未见，三档都是 501。本叶不新注册，不写能算出数的公式。页面读缺项表行。行内文字不是指标结果。

### 6.1 224 分主题分指标互动解读

没有专属 `metric_id`。没有已注册的解读模型。

读面是 `GET /display/v1/policy/evaluation/shells`。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_shell` 的解读条目：专题或指标名、一句结论、一句应用建议。点选只筛选已经返回的行，不另起计算，不新开路径。

条目若要指向指标，只能指向已经存在的 `metric_id`。本叶不指定新 id，也不把 223 的焦点说明、226 的摘要行复制成解读条目。没有已挂指标的，行上 `metric_id` 留空。无行则解读块空。接口不写死结论。本叶不灌数。灌数单 `POL-L2-DS11-READ-GAPFILL-L01` 本叶不认领。

### 6.2 225 多媒体辅助解读

没有专属 `metric_id`。没有视频通道，也没有可调用模型。调研交互壳为「未见」，`指标与501` 并入 501，不升第四档。

同一张 `gapfill_policy_eval_shell`，只读多媒体条目：标题、一句说明。不灌视频、动画或图形文件，不写对象存储，前端不直连 RustFS。页上已有的短板计数和焦点结果留在原资源上。本序号不新做一套图。无行则该块空。标题和一句说明不是视频已经交付。

## 7. 点名不挂

下列 id 已用 `metric-get` 核对。本二级不挂。不改它们的 D4。

| metric_id | 注册身份（metric-get） | 不挂 223–226 的原因 |
|---|---|---|
| `M_POLICY_OPPORTUNITY_COUNT` | 政策机遇清单条数（王惠机遇计数 v2 全维复现）；STAT；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；QPOL-02。`found.seed=true`，`found.matrix=true`，`found.srs_map=true`。需求来源只有专题 05/170，`page_ids` 为 `DS-11-POLICY-EVAL`，没有 223–226 的序号 | 机遇条数不挂进 223–226。`counts` 上留给它的读面本叶不改。`指标与501` 把它放在页 KPI，可接统计读面，源模型仍是 MODEL。本叶不把该源模型挂进这四叶 |
| `M_POLICY_RELATION_DEGREE` | 政策关联度；GRAPH；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；QPOL-03；注册判定完全不支持。`found.srs_map=false`，`srs_refs` 为空 | 它在焦点行的 `relation_degree` 上。不改挂到 223。本叶不为此读图，Java 不写 nGQL |
| `M_POLICY_DEEP_169_1` | 政策短板识别模型；MODEL；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；`pending_ref=GAP-ALGO-TYPE-UNSIGNED`。需求来源是专题 05/169，`role=algo_leaf` | 223 短板的同步读面只挂 `M_POLICY_SHORTBOARD_COUNT`。源模型不在这条 GET 上计算 |
| `M_POLICY_TEXT_PARSE` | 政策文本解析；MODEL；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；QPOL-02。`found.srs_map=false`，`srs_refs` 为空 | 226 的展示身份是 `M_POLICY_DS_11_POLICY_EVAL_012`。解析行上的 `metric_id` 仍是这一条，本叶不改，也不把 226 改挂成它。`指标与501` 把它放在推演序号 237，不在 223–226 |
| `M_POLICY_EFFECT_SCORE` | 政策效果评分（王惠三维口径 v2 复现）；MODEL；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；QPOL-02。需求来源是展示 02/232、02/233 与专题 05/168 | 在 `jobs` 上，不是 223–226。本叶不挂 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | 实施路径与风险辅助；GRAPH；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；`pending_ref=GAP-ALGO-TYPE-UNSIGNED`。需求来源是展示 02/229 | 属于 227–231，不进本四叶 |

下列边界沿架构稿、架构会签页与 `指标与501`，本叶不改挂：

| 对象 | 本叶 |
|---|---|
| 序号 222 报告模板定制与批量导出 | 不挂。`指标与501` 写未见 `metric_id`，判定 501。模板选用不灌入 `gapfill_policy_eval_shell`。`POL-L2-DS11-READ-GAPFILL-L01` 不灌模板 |
| 序号 227–231 | 不挂。方案、参数模拟、实施路径、意见与归档不进本四叶。不把 `M_POLICY_DS_11_POLICY_EVAL_015` 改挂到 223–226 |
| `counts` 上的机遇条数 | 留给页 KPI。不计入 223 短板 |
| `policy_focus` 的 harness 路径 | 带 items 的既有焦点作业。看板走 `policy_focus_ads`，不把 harness 返回写成焦点指数 |
| `focus-one` | 不写 ADS。看板不返回它的当场计算结果，也不把它当成 226 的摘要 |
| 序号 219–221 | 趋势、分区、结构关联。不收进本叶。结构关联不挂 `M_POLICY_RELATION_DEGREE` |
| `compare/jobs`、`report/jobs`、`simulation/jobs`、序号 242 | 核增对比、研报、推演解读。不是本四叶的摘要 |
| 门户或算法中台页 `/policy/focus`、`/policy/gap`、`/policy/parse` | 展示不嵌这些页，不打 `/v1/policy/**` |

## 8. 偏离

任务 DoD 写「未注册模型保持 501」。本叶按这句话保持三档，不把焦点指数改成可算公式。

说明书第 2 节和 `指标与501.md` 的判定列是：223 短板为可接统计读面；223 焦点、224、225、226 为 501。本叶不改这两份文件，也不改这四档的归类。短板仍是已有统计读面。焦点、224、225、226 仍是 501。

已签收架构把这四叶的功能空态收成读表：有行则读已有列或已有缺项行，无行则空。接口不直接返回写死的 mock，也不用 501 这个词充当返回值。本叶按签收写读面，同时不把「读表」写成一条新公式。

- 223 短板：判定保持可接统计读面。`counts` 只读已写入的 `shortboard_cnt`。GET 不调用 `gap.run`。无行则空。
- 223 焦点：判定保持 501。不展开 `focus.run`。无行则焦点块空。
- 224、225：仍然没有 `metric_id`。判定保持 501。读缺项表行。行内文字不是指标结果。
- 226：判定保持 501。请求只读已有 `summary`，不写成现算 `parse.run`。无行则摘要空。

本叶未会签。不把本单标 done。不改任务状态。

## 9. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不手抄注册公式。不把焦点指数的 501 改写成可算公式。不把 226 的注册式或 `parse.run` 写成这次请求的现算。无行则空，不写假公式。
- 不挂 `M_POLICY_OPPORTUNITY_COUNT`。不挂 `M_POLICY_RELATION_DEGREE`。不挂序号 222 的模板。不挂 227–231，也不挂 `M_POLICY_DS_11_POLICY_EVAL_015`。
- 不把 `M_POLICY_DEEP_169_1` 放到短板的同步链上。不把 `M_POLICY_TEXT_PARSE` 改成 226 的展示身份。不挂 `M_POLICY_EFFECT_SCORE`。
- 不给 224、225 写能算出数的公式。行内文字不是指标结果。225 不灌视频，不写对象存储。
- 不把 222 的模板选用灌进 shell。
- 不闭合 QPOL-02，不签 226 的公式，不把 D2 provisional 改绿。
- 不改唐绍祖锁定的合规算法。本单不写算法实现，不改 demo 仓与 vendor 里的计算文件。
- 不重开 GDF，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开，不把 `GDF-POLICY-MDC-STAT-L01` 写成已覆盖短板条数。
- 不改说明书、`指标与501.md`、架构稿、会签页、注册表和指标 seed。
- 不写 OpenAPI 字段、请求体、响应体、枚举。不写代码。
- 不会签。不把本单标 done。不改任务状态。
