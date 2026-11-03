# POL-L2-DS11-PLAN-METRIC · 政策分析评价 · 推荐方案报告交互展示 · 后台指标设计

- 任务：`POL-L2-DS11-PLAN-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`（已认领，本叶不再认领，不改任务状态）
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`。任务 `POL-L2-DS11-PLAN-ARCH` 于 2026-11-03 已签收，签收人 human:淮政玮，note 为四角色会签同意。架构稿正文开头仍写未会签，本叶不改那份稿。读面以该稿与 `sdd/l2/会签/POL-L2-DS11-PLAN-SIGNOFF-ARCH.md` 为准
- 会签态：未会签。本叶不代签，不标 done
- 查询：2026-11-03 经 MCP `metric-get`。未读 seed、矩阵 YAML，未改注册表，未改 D4

本叶只写政策分析评价二级「推荐方案报告交互展示」的指标挂接。SRS 序号 **227–231**。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`、`sdd/l2/会签/POL-L2-DS11-PLAN-SIGNOFF-ARCH.md`、`sdd/指标与501.md` 评价表 227–231 行、说明书第 2 节 DS-11 同序号。不新注册指标，不改 D4，不写假公式，不改算法代码，不写 OpenAPI。

## 1. 范围

五叶都在政策分析评价的推荐方案工作区里完成。指标身份沿说明书第 2 节与 `指标与501.md` 已有 `metric_id` 和三档判定。读面沿已签收的 `POL-L2-DS11-PLAN-ARCH`。本叶不改那几份文件。

| 序号 | 叶子 | 指标与501 / 说明书第 2 节 | 本叶 |
|---|---|---|---|
| 227 | 多方案对比展示 | 未见 `metric_id`；判定列 501 | 没有专属指标，不新造，不写公式。页面读 `gapfill_policy_eval_scheme` 的方案对照行。行上 `metric_id` 留空。少于两行则对比空 |
| 228 | 方案参数自定义模拟 | 未见 `metric_id`；判定列 501 | 没有专属指标，不新造，不写公式。按方案和参数档读同一张表的参数模拟行。请求内不按 `simulate.run` 现算。对不上则该次预览空 |
| 229 | 实施路径与风险辅助 | `M_POLICY_DS_11_POLICY_EVAL_015`；GRAPH；D4=`mock`；判定列 501 | 只挂这一条。三档保持 501。D4 保持 mock。读同一张表的路径与风险行。不读图 |
| 230 | 互动意见收集与专家参与 | 未见 `metric_id`；判定列 501 | 没有专属指标，不新造，不写公式。读同一张表的意见行。请求不插入新意见 |
| 231 | 方案报告导出与归档 | 未见 `metric_id`；判定列 501 | 没有专属指标，不新造，不写公式。导出从当次读到的方案对照行和意见行生成。不灌文件 |

229 的 D4 仍是 `mock`。`指标与501` 把 227–231 都放在评价页的 501 里，本叶不改这五档的归类，不改该页「501 为 14」的计数。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿视为未解开。本叶不把 mock 写成已上线。

`evaluation/counts` 上的短板条数、机遇条数没有 227–231 的序号，不挂进本二级。

## 2. 本二级用到的已有 metric_id

挂接去重后 1 条，只落在 229。227、228、230、231 不在此表。`metric-get` 为 `found.seed=true`、`found.matrix=true`、`found.srs_map=true`。D4 是 `mock`。中文名、`algorithm_type` 以 MCP 为准。

| metric_id | 中文名（MCP） | algorithm_type | D4 | 挂在 |
|---|---|---|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_015` | 实施路径与风险辅助 | GRAPH | mock | 229 |

这一条之外，本二级不新造 `metric_id`。

叶子名与注册中文名一致，都是「实施路径与风险辅助」。类型仍是 GRAPH。三档仍是指标分册的 501。本叶不改判成可接统计读面，不改判成跨项索引，也不把 GRAPH 改写成在线读图。

按 `POLICY_EVAL` 检索，同名前缀另外还有 `M_POLICY_DS_11_POLICY_EVAL_012`。它属于解读二级的 226，本叶不改挂，不在此重述它的八件套。227、228、230、231 没有可复用的专属 id。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进本节。

源系统：`gkx @ 183.240.141.251:3318（只读）`。`version` 是 `1`。

| metric_id | 中文名 | algorithm_type | 源表 | 更新频率 |
|---|---|---|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_015` | 实施路径与风险辅助 | GRAPH | `dwd_policy_base` | pending |

注册公式是过程指针：见 calc-logic「计算逻辑说明」与 20261021 正本 §二；公式是过程式复算，未浓缩为单行表达式；禁手抄，实现时以 `code/M_POLICY_DS_11_POLICY_EVAL_015.py` 为准。注册指针为 `metrics/calc-logic/POLICY/M_POLICY_DS_11_POLICY_EVAL_015.md`。`pending_ref` 为 `GAP-ALGO-TYPE-UNSIGNED`。`d1_note` 写公式未签，并记「读 D3 policy_simulate，不顶替 171」。本叶不手抄、不展开成可执行式，不签这行公式，也不另写一条能算出路径节点或风险的式子。这次请求不执行该指针，不读 `ads.policy_simulate`，不顶替 171。

口径按 `metric-get` 的 `kit.definition` 摘录，不改写。

| metric_id | 口径 |
|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_015` | 四要素要四类输入：环节词命中的正文、可排序的多个时间点、风险事件记录、政策层级。第一类有（18,763 条正文），第二类只剩一个点（`publish_date` 可用 19,994 行），第三类两库都没有，第四类有（`level` 五档）。两缺一残一足，落「部分支持」。注册判定为部分支持。本叶不改口径，不闭合，不把缺的时间进度和风险清单补成一条新式 |

229 的展示读数不在接口里重算，也不替换上表的注册公式。已签收架构指认：路径与风险读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 里已经写下的路径与风险行。上表源表是注册身份，不是这叶的展示读表。本叶不把 `dwd_policy_base` 写成 229 的读表。

`extras.algo_server_location` 指向 demo 仓 `polan/metrics/metrics.py` 与 `polan_metric_routes.py`。那是注册表索引，不是本二级的展示调用链。本叶不改那些文件，也不把展示改去调 demo 服务。展示仍按架构稿：浏览器只打 `/display/v1/policy/**`。

注册 `ui_mount` 写的是政策详情页「实施路径」标签页和对比页「风险提示」两个设计位。本叶的读面仍是评价页 `jobs` 的路径与风险行。不另开详情页，不把设计位写成第 7 项在线读图。

## 4. 接入状态

接入状态不是八件套。下表来自 `metric-get` 的 `readiness`。D1 是 `aligned`，D2 是 `partial` 且 `d2_assessed=provisional`（待核验），D4 是 `mock`。本叶不改任何一维。D2 的 provisional 保留「待核验」，不在本叶改绿。

| metric_id | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_015` | aligned | partial，待核验 | partial | mock |

`is_mock=true`。`d4_note` 写算法服务未上线，保持 mock。对齐前数值仍是 mock。本叶不改 D4。`lifecycle_stage` 为 `kit_complete`，不是八件套，本叶不改。

需求来源不是八件套。沿用查询结果，本叶不改挂：

| metric_id | srs_refs | 本叶用法 |
|---|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_015` | 展示 02/229 实施路径与风险辅助；`page_ids` 为 `DS-11-POLICY-EVAL`；`systems` 为展示；`role` 为 `page_use` | 只挂 229。不改挂到 227、228、230、231，也不改挂到推演序号 241 |

## 5. 229 怎么读

读面沿架构稿与架构会签页，不新开路径，不新造指标。切条件不自动起任务。这次读取失败，不清空 `counts` 上已经返回的短板条数和机遇条数。无行则空，不写假公式。

只挂 `M_POLICY_DS_11_POLICY_EVAL_015`。MCP：中文名「实施路径与风险辅助」，GRAPH，D4=`mock`，`pending_ref=GAP-ALGO-TYPE-UNSIGNED`。

`指标与501` 的三档判定是 501：口径是路径与风险生成，不是第 7 项在线读图，页面空态。本叶保持这一档。不把注册过程指针展开成环节词、时间排序或风险打分的计算式，也不把「部分支持」写成这次请求的返回值。

请求只读已经写下的路径与风险行，不在本叶定义怎么生成路径：

1. 浏览器提交 `POST /display/v1/policy/evaluation/jobs`，种类为路径与风险。方案必选。
2. `gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。
3. `gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 里该方案的路径与风险行：节点、时间进度、一句说明、风险标题、一句风险。
4. 行上的 `metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。本叶不新注册，不改 D4，不把读到的行写成已上线。

这次请求不调用 `polan.text.simulate.run`，不进入 `gkxlumen-topic-async-service`，不读政策子图。现有 `run()` 不产出这条指标。模型注册表虽把本 id 列在 `POLICY_SIMULATE` 下，本叶不改注册表，也不把这次 `run()` 迁到评价页。

该方案没有路径行时，路径和风险都空。不返回推演曲线来顶替，不返回写死节点，不用 501 这个词充当路径正文。D4 保持 mock。缺项表里的行是灌入的 mock，灌数单是 `POL-L2-DS11-PLAN-GAPFILL-L01`，本叶不认领、不执行。

## 6. 227、228、230、231 没有专属指标

这四叶在说明书第 2 节和 `指标与501` 里 `metric_id` 为未见，三档都是 501。本叶不新注册，不写能算出数的公式。页面读缺项表行，或从当次读到的行生成导出。行内文字和对照值不是新指标的计算结果。

五叶共用一张表 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。种类只有方案对照、参数模拟、路径与风险、互动意见。231 不单独占种类。227、228、230 的行上 `metric_id` 留空。

### 6.1 227 多方案对比展示

没有专属 `metric_id`。没有方案生成模型。

读面是 `POST /display/v1/policy/evaluation/jobs`，种类为方案对照。`gkxlumen-element` 只读方案对照行：名称、一句说明、对照维度和数值、优劣结论、实施建议。雷达和 KPI 用的就是这些行上已经写下的对照值。少于两行则对比空，不造第二个方案。Java 不生成方案。

不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DEEP_171_1`。布局建议条数留在布局推荐键。`metric-get` 显示布局建议条数的 `srs_refs` 含展示 02/227。`指标与501` 仍把 227 写成未见 `metric_id`，并写明不把布局建议条数写入本页。本叶不改 `srs_refs`，不把 227 改判成跨项索引，也不把对冲计数写进方案对照行。

无行则对比空。接口不写死方案。本叶不灌数。

### 6.2 228 方案参数自定义模拟

没有专属 `metric_id`。没有方案参数模型。

同一条 `jobs`，种类为参数模拟。按一个方案和一组关键参数档拣行，返回评估结果、一句趋势、一条归档说明。方案必选。参数档对不上则预览和趋势空。

请求内不按 `polan.text.simulate.run` 现算，不调用推演函数，不在 Java 或 Python 里按弹性现算。采纳不写库。归档只来自已经灌入的行。不挂 `M_POLICY_SIMULATE`，不写推演页。

### 6.3 230 互动意见收集与专家参与

没有专属 `metric_id`。没有意见采集服务。调研交互壳为「未见」，`指标与501` 并入 501，不升第四档。

读面是 `GET /display/v1/policy/evaluation/shells`，种类为互动意见。按方案读意见行：主体、分类、意见正文。分类只用评价、评论、建议。不选方案则意见列表空。

请求处理不插入、不更新、不删除。用户在页面上新打的评价留在浏览器，直到另有采集单。本叶不建那张单。无行则列表空，不造一条专家意见。

不把序号 210 的受众反馈表 `gapfill_policy_audience_feedback` 当成方案意见。

### 6.4 231 方案报告导出与归档

没有专属 `metric_id`。没有方案报告模型，也没有导出 Job。

同一条 `shells`，种类为方案报告。同一次读取方案对照行和互动意见行。有行则从这些行生成导出内容：方案描述、实施建议、对比分析和专家点评。没有方案对照行则导出空。

不另建报告行，不灌 PDF、Word、Excel，不写对象存储。核增研报 `report/jobs`（614–618）和评价页序号 222 的分析报告模板不是这条资源。分析报告份数那张统计卡也没有 `metric_id`，本叶不新编，不挂到 231。

## 7. 点名不挂

下列 id 已用 `metric-get` 核对。本二级不挂。不改它们的 D4。

| metric_id | 注册身份（metric-get） | 不挂 227–231 的原因 |
|---|---|---|
| `M_POLICY_SIMULATE` | 政策效果推演；MODEL；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；QPOL-02；注册判定完全不支持。`found.seed=true`，`found.matrix=true`，`found.srs_map=false`，`srs_refs` 为空 | 推演键。`指标与501` 把它放在推演页 232–234，并写明 228 不挂这条、不写推演页。`simulate.run` 只写省级力度情景，行上 id 固定为这一条，不写方案、参数档、路径节点、风险和专家意见，也不产出 015。本叶不改挂，不补 `srs_refs`，请求内不按 `run()` 现算 |
| `M_POLICY_LAYOUT_REC_COUNT` | 政策布局建议条数（王惠对冲计数 v2 复现）；STAT；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；QPOL-02；注册判定部分支持。`found.seed=true`，`found.matrix=true`，`found.srs_map=true`。`srs_refs` 含展示 02/227、展示 02/241、专题 05/171 | 布局推荐键。尽管 `srs_refs` 含 02/227，`指标与501` 写该指标不进入评价表，227 的 `metric_id` 为未见，并写不把布局建议条数写入本页。已签收架构同样不挂。本叶不改 `srs_refs`，不把 227 改判成跨项索引。02/241 仍是推演页路径预测，不顶替 229 |
| `M_POLICY_DEEP_171_1` | 政策布局推荐模型；MODEL；D1=`aligned`；D2=`partial` 且待核验；D3=`partial`；D4=`mock`；`is_mock=true`；`pending_ref=GAP-ALGO-TYPE-UNSIGNED`；注册判定部分支持。`found.seed=true`，`found.matrix=true`，`found.srs_map=true`。需求来源只有专题 05/171，`role=algo_leaf` | 布局推荐的源模型。不写入方案对照，不挂 227，不顶替 229 |

下列边界沿架构稿、架构会签页与 `指标与501`，本叶不改挂：

| 对象 | 本叶 |
|---|---|
| 序号 219–226 | 趋势、分区、结构关联、报告模板、焦点、短板、解读、多媒体、摘要。留在可视化与解读两个二级。不把 `M_POLICY_DS_11_POLICY_EVAL_012` 改挂进 227–231 |
| 序号 232–242，含 241 | 推演页。241 的路径预测不顶替 229。`M_POLICY_DS_11_POLICY_EVAL_015` 不改挂到 241 |
| `evaluation/counts` | 短板条数、机遇条数。本二级不读、不改 |
| `ads.policy_simulate`、`polan.text.simulate` | 推演键。五叶的请求都不调用 `simulate.run` |
| `report/jobs` | 核增研报。不是 231 |
| `gapfill_policy_audience_feedback` | 序号 210 的受众反馈。不是 230 的方案意见 |
| 门户或算法中台效果推演签、`/v1/policy/**`、`/internal/analysis/policy/simulate` | 展示不嵌这些页，不打这些路径。`E-E7-POLICY-M1-L06` 不是本页路径 |

## 8. 偏离

任务 DoD 写「未注册模型保持 501」。本叶按这句话保持三档。227、228、230、231 没有专属指标。229 已注册，判定列仍是 501，不改成可算公式，也不改成可接统计读面。

说明书第 2 节和 `指标与501.md` 的判定列是：227、228、229、230、231 都为 501。本叶不改这两份文件，也不改这五档的归类。

已签收架构把这五叶的功能空态收成读表：有行则读已有缺项行，或从当次读到的行生成导出；无行则空。接口不直接返回写死的 mock，也不用 501 这个词充当返回值。本叶按签收写读面，同时不把「读表」写成一条新公式。

- 227：判定保持 501。没有 `metric_id`。读方案对照行。少于两行则对比空。布局建议条数不写入本页。
- 228：判定保持 501。没有 `metric_id`。按方案和参数档读参数模拟行。请求内不按 `simulate.run` 现算。
- 229：判定保持 501。只挂 `M_POLICY_DS_11_POLICY_EVAL_015`。D4 保持 mock。读路径与风险行。不读图。无行则路径空。
- 230：判定保持 501。没有 `metric_id`。读意见行。请求不插入。
- 231：判定保持 501。没有 `metric_id`。从方案行和意见行生成导出。不灌文件。

`M_POLICY_LAYOUT_REC_COUNT` 的需求来源含展示 02/227。本叶不据此改挂，也不改 `srs_refs`。`M_POLICY_SIMULATE` 的 `srs_refs` 为空。本叶不把它补到 228，也不补注册来源。`M_POLICY_DS_11_POLICY_EVAL_015` 的需求来源是展示 02/229。本叶不改。

本叶未会签。不把本单标 done。不改任务状态。

## 9. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不手抄注册公式。不把 229 的 501 改写成可算公式。不把 `simulate.run` 或弹性计算写成这次请求的现算。无行则空，不写假公式。
- 不挂 `M_POLICY_SIMULATE`。不挂布局推荐 `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1`。
- 不给 227、228、230、231 写能算出数的公式。行内文字和对照值不是新指标结果。230 的请求不插入意见。231 不灌文件，不写对象存储。
- 不读图，不写 nGQL。不把 229 的 GRAPH 改成第 7 项在线读图。
- 不闭合 QPOL-02，不签 015 的公式，不把 D2 provisional 改绿。
- 不改唐绍祖锁定的合规算法。本单不写算法实现，不改 demo 仓与 vendor 里的计算文件，不改模型注册表。
- 不重开 GDF，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。不执行灌数单。
- 不改说明书、`指标与501.md`、架构稿、会签页、注册表和指标 seed。
- 不写 OpenAPI 字段、请求体、响应体、枚举。不写代码。
- 不会签。不把本单标 done。不改任务状态。
