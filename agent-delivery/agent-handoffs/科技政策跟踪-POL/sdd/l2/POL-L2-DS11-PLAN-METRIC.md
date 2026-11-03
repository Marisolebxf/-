# POL-L2-DS11-PLAN-METRIC · 政策分析评价 · 推荐方案报告交互展示 · 后台指标设计

- 任务：`POL-L2-DS11-PLAN-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`（任务 `POL-L2-DS11-PLAN-ARCH` 于 2026-11-03 已 done，note 为 `human:淮政玮` 签收。本叶以该稿为准）。本叶会签态 `draft`，不代签，不标 done
- 查询：未见 metric MCP。本叶未调用 `metric-get` / `metric-query`。未读 seed、矩阵 YAML，未改指标注册表，未改 `cfg_model_registry.yaml`。下文凡未标明出处的身份字段，都不要当成已经查过

本叶只写政策分析评价二级「推荐方案报告交互展示」的指标挂接。SRS 序号 **227–231**。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`、`sdd/指标与501.md` 评价表 227–231 行、说明书第 2 节 DS-11 这五行、`sdd/l2/POL-L2-DS11-READ-METRIC.md`（篇章样板）。不新注册指标，不改 D4，不写假公式，不改算法代码，不调用 `polan.text.simulate.run`，不写 OpenAPI。

## 1. 范围

五叶都在政策分析评价的推荐方案工作区里完成。挂接沿说明书第 2 节 DS-11 已有 `metric_id` 与三档，以及 `指标与501.md` 评价表 227–231 行。读面沿已签收的 `POL-L2-DS11-PLAN-ARCH`。本叶不改那三份文件，也不把调研判定列改写成另一档。

说明书第 2 节三档只有：可接统计读面、501、跨项索引。227、228、230、231 的拆解是 501。229 的拆解是 501，并带已有 `M_POLICY_DS_11_POLICY_EVAL_015`。230、231 在说明书里是交互壳，调研记未见，并入 501，不升第四档。这五叶都不是可接统计读面，也都不是跨项索引。本叶不改这三档。

| 序号 | 叶子 | 指标与501 / 说明书第 2 节 | 本叶 |
|---|---|---|---|
| 227 | 多方案对比展示 | 未见 `metric_id`；判定 501。真路径：不把布局建议条数写入本页 | 不新注册。不挂 `M_POLICY_LAYOUT_REC_COUNT`。方案对照行上的 `metric_id` 留空。读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 的方案对照行。少于两行则对比空 |
| 228 | 方案参数自定义模拟 | 未见 `metric_id`；判定 501。真路径：不挂 `M_POLICY_SIMULATE`，不写推演页 | 不挂 `M_POLICY_SIMULATE`。不读 `ads.policy_simulate`。不调用 `polan.text.simulate.run`。参数模拟行上的 `metric_id` 留空。按方案和参数档读同一张缺项表。对不上则该块空 |
| 229 | 实施路径与风险辅助 | `M_POLICY_DS_11_POLICY_EVAL_015`；GRAPH；D4=`mock`；判定 501。真路径：口径是路径与风险生成，不是第 7 项在线读图 | 沿用这一条。D4 仍是 mock。路径与风险行上的 `metric_id` 用这个已有号。读同一张缺项表的路径与风险行。不读图。不被序号 241 顶替 |
| 230 | 互动意见收集与专家参与 | 未见 `metric_id`；判定 501。交互壳，调研记未见。无指标，没有可调用模型 | 不新注册。意见行上的 `metric_id` 留空。只读已灌的意见行。请求不插入 |
| 231 | 方案报告导出与归档 | 未见 `metric_id`；判定 501。交互壳，调研记未见。无导出 Job，不是核增智能研报 | 不新注册。不单独占种类，行上没有可填的 `metric_id`。导出从当次读到的方案对照行和意见行生成。不灌文件 |

229 的 D4 仍是 `mock`。227、228、230、231 没有专属 `metric_id`，没有可改的 D4。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿视为未解开。本叶不把 mock 写成已上线。

`指标与501` 把 227–231 的判定列都写成「501，页面空态」。那是调研判定。已签收架构规定这五叶读缺项表：有行则读表，无行则空，不用 501 充当功能。本叶采用这条读面，不回头改 `指标与501`，也不把判定列从 501 改成可接统计读面或跨项索引。

`evaluation/counts` 上的短板条数、机遇条数不在本二级。

## 2. 本二级用到的已有 metric_id

挂接 1 条，只落在 229。227、228、230、231 不在此表。类型和 D4 只转述 `指标与501.md` 已有行，以及已签收架构稿里写明的同一事实。不是 `metric-get` 的返回。

| metric_id | 中文名 | algorithm_type | D4 | 挂在 |
|---|---|---|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_015` | 未见 metric MCP，不填注册中文名。叶子名沿评价表「实施路径与风险辅助」 | GRAPH | mock | 229 |

这一条之外，本二级不新造 `metric_id`。

叶子名与数据行上的号不是一回事：

- 229 的叶子名是「实施路径与风险辅助」。展示读面身份是已有的 `M_POLICY_DS_11_POLICY_EVAL_015`。本叶不另起一条路径指标。
- 227、228、230 的行上 `metric_id` 留空。231 不单独占种类，不另造一行去填号。
- 模型注册表 `vendor/entan-py/conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE` 把 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015` 列在同一 `metric_ids` 下，`handler_module` 是 `polan.text.simulate`，`ads_table` 是 `ads.policy_simulate`。本叶不改这份注册表。函数本身不产出 015，见第 3 节。229 因此不去读 `ads.policy_simulate`。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进八件套。

未见 metric MCP。本叶不把未查到的字段写成已查到。下列各项保持注册表原样，本叶不改、不抄、不补：

- 注册中文名
- 口径（`definition`）
- 注册公式
- 注册源表
- 源系统
- 更新频率
- `version`

因此本节不列八件套全表。不手抄公式，也不另写一条能算出路径、风险、方案分或参数结果的式子。

`指标与501` 229 行真路径列的原句是「口径是路径与风险生成，不是第 7 项在线读图」。这是判定说明，不是本叶查到的注册 `definition`。需求来源即序号 229，这句话写在说明书第 2 节与 `指标与501` 的 229 行，不是本叶新挂的 `srs_refs`。

已签收架构规定的是读哪张表，不是注册源表。读表只说明展示从哪里取数。无行则空。查询函数自己不生成路径，不拼风险，不套弹性。

| metric_id | 本叶能写的身份 | 读表（架构稿，不是注册源表） | 本叶不写的 |
|---|---|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_015` | GRAPH。D4 转述为 mock，不改 | `gkxlumenx_gapfill.gapfill_policy_eval_scheme` 的路径与风险行。行上 `metric_id` 用这个已有号 | 注册中文名、口径、公式、注册源表、源系统、更新频率、`version` |

229 的展示读数不在接口里重算，也不替换上表未抄的注册公式。类型仍是 GRAPH。本叶不把它改成 STAT 或 MODEL，也不因此去读政策子图。

核对了 `lumen-algo-py` 的 `vendor/entan-py/polan/text/simulate.py`。`run()` 只做省级力度情景：从 `ads.policy_intensity` 取 `scope_type='province'` 且力度指数非空的省，按指数从高到低最多 12 个省，用文件内已有的三条情景弹性写出基线、推演值、变化率和逐年曲线，写入 `ads.policy_simulate`。每一行的 `metric_id` 固定为字面量 `M_POLICY_SIMULATE`。函数不写方案、参数档、路径节点、风险、专家意见，插入行里也没有 `M_POLICY_DS_11_POLICY_EVAL_015`。

本叶不把这套弹性收成 228 或 229 的公式，不在展示请求里调用 `run()`，也不把 `ads.policy_simulate` 当成 229 的读表。模型注册表把 015 列在 `POLICY_SIMULATE` 下，只说明登记时并列表了两个号。函数不产出路径。本叶不改注册表来拆这两个号，也不调用这次 `run()` 去补路径。

## 4. 接入状态

接入状态不是八件套。未见 metric MCP，本叶不写 D1、D2、D3，也不写 `d2_assessed`、`is_mock` 的注册布尔、`d4_note`、`srs_refs`、`lifecycle_stage`。这些字段没有查到，不能补成 `aligned`、`partial`、`full` 或空引用。

D4 只转述已有行，本叶不改：

| metric_id | D4 的出处 | 本叶 |
|---|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_015` | `指标与501` 229 行写 `mock`；架构稿写 D4=`mock` | 保持 mock。不升 live |

227、228、230、231 没有专属 `metric_id`。没有可改的 D4。缺项表里灌入的行仍是 mock。本叶不把缺项写成已上线。

`M_POLICY_SIMULATE`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` 的 D1–D4 本叶都未用 metric MCP 核对。除 `指标与501` 已经写在纸面上的类型外，不补维度。推演键上 `M_POLICY_SIMULATE` 的纸面类型是 MODEL、D4=`mock`、判定 501。布局推荐键上 `M_POLICY_LAYOUT_REC_COUNT` 的纸面类型是 STAT、D4=`mock`、判定跨项索引。这两条都不在 227–231。本叶不改它们的 D4，也不把它们改挂进本二级。

## 5. 229 怎么读

挂 `M_POLICY_DS_11_POLICY_EVAL_015`。`指标与501`：GRAPH，D4=`mock`，判定列 501。说明书第 2 节同一行：501，并带这个已有号。

判定列仍留在 `指标与501` 里，本叶不改。读面按已签收架构：不用 501 充当这块功能，也不把判定列升成可接统计读面或跨项索引。

没有路径生成模型。`simulate.run` 不产出这条指标。本叶不调用它。

资源是已有的 `POST /display/v1/policy/evaluation/jobs`，种类为路径与风险。链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_eval_scheme`。`gkxlumen-display` 不直连库，不直连 Python。element 按方案读节点、时间进度和风险。一个方案可以有多行。无行则路径和风险都空，不返回 501，不返回写死的路径，也不返回推演曲线来顶替。

行上的 `metric_id` 用已有 `M_POLICY_DS_11_POLICY_EVAL_015`。不新注册，不改 D4，不把读到的行写成已上线。不写 nGQL，不读政策子图。第 7 项在线读图不是这条读面。

序号 241「政策实施路径预测」在推演页。`指标与501` 241 行是未见 `metric_id`、判定 501，并写明 `M_POLICY_LAYOUT_REC_COUNT` 与 `M_POLICY_DS_11_POLICY_EVAL_015` 都不顶替 241。本叶反过来也不让 241 顶替 229。015 留在 229。241 仍无专属号。本叶不把 015 改挂到 241，也不把 241 的空号写进路径行。

切条件不自动起任务。某一次 `jobs` 失败，不清空 `evaluation/counts` 已经返回的短板条数和机遇条数。

不做什么：不改 `cfg_model_registry.yaml`。不把 `POLICY_SIMULATE` 的并列表当成 229 已经能由 `run()` 写出。不读 `ads.policy_simulate`。不把省级力度曲线写成实施路径。

## 6. 227、228、230、231 没有专属 metric_id

227、228、230、231 在 `指标与501` 里 `metric_id` 为未见，判定列 501。230、231 的调研记交互壳，详设并入 501，不升第四档。说明书第 2 节与此相同。本叶不新注册，不改判定列，不改 D4。

真实的方案生成、真实的参数现算、真实的意见采集、真实的导出 Job，本叶都做不到。已签收架构的退路是缺项表：库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_scheme`。由下游把 mock 行写入表，接口只查询。本叶不执行灌数，不写字段级 DDL。查询请求不灌数。

这四叶指不到专属 id。行上的 `metric_id` 留空。不把 229 的 `M_POLICY_DS_11_POLICY_EVAL_015` 指进 227、228、230、231。不把 `M_POLICY_SIMULATE` 指进 228。不把 `M_POLICY_LAYOUT_REC_COUNT` 或 `M_POLICY_DEEP_171_1` 指进 227。

`POL-L2-DS11-PLAN-GAPFILL-L01` 灌方案对照、参数模拟、路径与风险、互动意见。没有已挂指标的，`metric_id` 留空。路径与风险行才写 `M_POLICY_DS_11_POLICY_EVAL_015`。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。本叶不认领、不执行该单。字段级 DDL 由 `POL-L2-DS11-PLAN-DATA` 定。

### 6.1 227 多方案对比展示

没有已挂 `metric_id`。也没有方案生成模型。

不挂 `M_POLICY_LAYOUT_REC_COUNT`。布局建议条数留在布局推荐键。`M_POLICY_DEEP_171_1` 同样不写入方案对照。

读面是 `POST /display/v1/policy/evaluation/jobs`，种类为方案对照。element 只读缺项表里的方案对照行：名称、一句说明、对照维度和数值、优劣结论、实施建议。雷达和 KPI 的数就是这些行上的对照值。少于两行则对比空，不造第二个方案，不补演示分。表里没有行则对比空。不在接口里写死方案。

行上 `metric_id` 留空。

不把算法中台效果推演签、`policyData.js` 的本地方案常量迁进本叶。

### 6.2 228 方案参数自定义模拟

没有已挂 `metric_id`。推演函数写的是省级力度情景，指标是 `M_POLICY_SIMULATE`。`指标与501` 228 行已经写明不挂这条。本叶沿用，不改挂。

不读 `ads.policy_simulate`。不调用 `polan.text.simulate.run`。请求内不按弹性现算。

读面是同一个 `jobs`，种类为参数模拟。element 按方案和参数档拣同一张缺项表的行：参数档、评估结果、一句趋势、一条归档说明。对得上的行原样返回。对不上则预览和趋势空。采纳不写库。归档只来自已经灌入的行。

行上 `metric_id` 留空。

不写推演页六子区。不把序号 232–234 的推演读面搬到评价页。

### 6.3 230 互动意见收集与专家参与

没有已挂 `metric_id`。没有意见采集服务。

调研把它记为交互壳，判定仍是 501，不升第四档。已签收架构规定交互壳同样读缺项表，不用 501 充当这块功能。本叶采用这条读面，不改判定列。

读面是 `GET /display/v1/policy/evaluation/shells`，种类为互动意见。element 按方案读意见行：主体、分类、意见正文、时间。分类只用评价、评论、建议。请求处理不插入、不更新、不删除。无行则列表空，不造一条专家意见。

行上 `metric_id` 留空。

不把序号 210 的受众反馈表 `gapfill_policy_audience_feedback` 当成方案意见。

### 6.4 231 方案报告导出与归档

没有已挂 `metric_id`。没有方案报告模型和导出 Job。

调研把它记为交互壳，判定仍是 501，不升第四档。读面按已签收架构：从当次读到的行生成，不用 501 充当这块功能，也不另挂指标。

读面是同一个 `shells`，种类为方案报告。element 读该范围的方案对照行和互动意见行。有方案对照行则从行生成导出内容。没有方案对照行则导出空。不返回一份写死的文件。不写对象存储。

231 不单独占种类，不另建报告行，因此没有一行可填 `metric_id`。方案对照行和意见行上的号仍按 227、230 留空。不把 229 的号抄进导出。

核增研报 `report/jobs`（614–618）和评价页序号 222 的分析报告模板不是这条资源。

## 7. 点名不挂

下列号或序号在已签收架构、或 `指标与501` 里已经出现。本二级不把它们改挂到 227–231，也不改它们的 D4。身份未经过 metric MCP。下表只写本叶能从这两份已有文字和 `simulate.py`、模型注册表里确认的内容。

| 号或序号 | 已有文字或代码里能确认的 | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_SIMULATE` | `指标与501` 推演键：MODEL，D4=`mock`，判定 501。228 行写明不挂。`simulate.run` 写入 `ads.policy_simulate`，行上 `metric_id` 固定为这个号。模型注册表列在 `POLICY_SIMULATE` 下 | 228 不挂，不读 `ads.policy_simulate`。229 的路径行不写这个号。本叶不调用 `run()` |
| `M_POLICY_LAYOUT_REC_COUNT` | `指标与501`：不进入评价表。布局推荐键 STAT，D4=`mock`，跨项索引。需规引用写过展示序号 241，该引用不改变分键 | 227 不挂。布局建议条数留在布局推荐键 |
| `M_POLICY_DEEP_171_1` | `指标与501` 布局推荐键：MODEL，D4=`mock`，跨项索引。架构稿：不写入方案对照 | 227 不挂 |
| `M_POLICY_DS_11_POLICY_EVAL_015` 改挂到 241 或由 241 顶替 | `指标与501` 241 行：未见 `metric_id`，判定 501。015 与布局建议条数都不顶替 241。架构稿：241 在推演页，不顶替 229 | 015 只留在 229。241 不顶替 229。本叶不改 241 的空号 |
| `ads.policy_simulate` | `simulate.run` 的写入表。模型注册表 `POLICY_SIMULATE.ext.ads_table` | 228、229 都不读。继续只服务推演键 |
| `evaluation/counts` | 短板条数、机遇条数。架构稿：不在本二级 | 本叶不读、不改 |
| 219–226 | 趋势、分区、结构关联、模板、焦点、短板、解读、多媒体、摘要 | 可视化与解读两个二级。本叶不改挂 |
| 232–234、241 | 推演页。推演只认 `M_POLICY_SIMULATE`。241 无专属号 | 不把推演页六子区或路径预测写进 227–231 |
| `report/jobs` | 核增研报 | 不是 231 |
| `gapfill_policy_audience_feedback` | 序号 210 的受众反馈 | 不是 230 的方案意见 |
| `POLICY_SIMULATE` 注册项 | `metric_ids` 同时列出 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`。函数只写前者 | 本叶不改这份注册表，也不据此让 229 去读推演表 |

`M_POLICY_SIMULATE`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` 的 D1–D3 未查。本叶只核对「不改挂」，不展开它们的计算。

## 8. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不给 227、228、230、231 补 `metric_id`。指不到就留空。不把 229 的号指进这四叶。
- 不把 `M_POLICY_LAYOUT_REC_COUNT` 挂到 227。不把 `M_POLICY_SIMULATE` 挂到 228。不读 `ads.policy_simulate`。
- 不把序号 241 写成 229 的顶替。不把 `M_POLICY_DS_11_POLICY_EVAL_015` 改挂到 241。
- 不手抄注册公式，不把 `simulate.run` 的情景弹性收成 228 或 229 可算出数的新公式。
- 不调用 `polan.text.simulate.run`。不改 `simulate.py`。不改 `cfg_model_registry.yaml`。
- 不把 GRAPH 类型当成第 7 项在线读图。不写 nGQL。
- 不改 `指标与501.md`、`POL-L2-DS11-PLAN-ARCH.md`、`POL-L2-DS11-READ-METRIC.md`、说明书、WBS、指标 seed 与矩阵。
- 不写 OpenAPI 字段、请求体、响应体、枚举。
- 不见 metric MCP 就不填中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3、`srs_refs`。
- 不会签。不把本单标 done，也不标 `ready_to_sign`。
