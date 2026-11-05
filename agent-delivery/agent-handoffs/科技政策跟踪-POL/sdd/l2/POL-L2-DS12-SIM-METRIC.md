# POL-L2-DS12-SIM-METRIC · 政策效果推演 · 科技政策推演 · 后台指标设计

- 任务：`POL-L2-DS12-SIM-METRIC`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-06`
- 上游：`sdd/l2/POL-L2-DS12-SIM-ARCH.md`（含 2026-11-05 第 7、9 节）。本叶以该稿的读法为准。该文件抬头仍写待四角色会签、不标 done。本叶不改那份抬头，不代签，不标 done
- 查询：未见 metric MCP。本叶未调用 `metric-get` / `metric-query`。回退 `sdd/指标与501.md` §3。未读 seed、矩阵 YAML，未改指标注册表，未改 `cfg_model_registry.yaml`。下文凡未标明出处的身份字段，都不要当成已经查过

本叶只写政策效果推演二级「科技政策推演」的指标挂接。SRS 序号 **237–242**。

上游只引用，不改写：`sdd/l2/POL-L2-DS12-SIM-ARCH.md`、`sdd/指标与501.md` 推演表 237–242 行、说明书第 2 节 DS-12 这六行与第 11.2 节。232–236 归 `POL-L2-DS12-EST-METRIC`，本叶只交叉引用。不新注册指标，不改 D4，不写假公式，不改算法代码，不调用 `polan.text.parse.run`，不写 OpenAPI。

## 1. 范围

六叶都在政策效果推演的科技政策推演工作区里完成。挂接沿说明书第 2 节 DS-12 已有 `metric_id` 与三档，以及 `指标与501.md` §3.2 的 237–242 行。读面沿 `POL-L2-DS12-SIM-ARCH`（含 2026-11-05 第 7、9 节）。本叶不改那三份文件，也不把调研判定列改写成另一档。

说明书第 2 节三档只有：可接统计读面、501、跨项索引。推演页可接统计读面为 0。237、238、239、241、242 的拆解是 501。240 的拆解是跨项索引，纸面带已有 `M_POLICY_RELATION_DEGREE`。本叶六叶都不是可接统计读面。本叶不改这三档。

推演页只认已有 `M_POLICY_SIMULATE`。该号只挂 232–234，归 `POL-L2-DS12-EST-METRIC`。本叶 237–242 不把这条写进行上。

| 序号 | 叶子 | 指标与501 / 说明书第 2 节 | 本叶 |
|---|---|---|---|
| 237 | 政策文本智能解析 | `M_POLICY_TEXT_PARSE`；MODEL；D4=`mock`；判定 501。真路径：501，页面空态。`FE-POL-05A` 不顶替 | 不新注册。行上已有的 `M_POLICY_TEXT_PARSE` 保持原号。展示读已有 `ads.policy_text_parse` 的解析行。请求不调用 `polan.text.parse.run`。不灌缺项文本解析行 |
| 238 | 政策重点可视化展示 | 未见 `metric_id`；判定 501。`M_POLICY_FOCUS_INDEX` 不挂本行 | 不新注册。不挂 `M_POLICY_SIMULATE`，不挂 `M_POLICY_FOCUS_INDEX`。重点行上的 `metric_id` 留空。读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的重点行 |
| 239 | 政策影响范围分析 | 未见 `metric_id`；判定 501。推演模型仍是 501，本行不改挂成统计读面 | 不新注册。不挂 `M_POLICY_SIMULATE`。影响范围行上的 `metric_id` 留空。读同一张缺项表的影响范围行，跟随该政策上下文 |
| 240 | 政策关联分析 | `M_POLICY_RELATION_DEGREE`；GRAPH；D4=`mock`；判定跨项索引。展示只消费读图 | 不另造独立 `metric_id`。不设种类，不设 HTTP 资源。页面消费第 7 项已有政策子图。纸面号留在跨项，不写进本叶资源 |
| 241 | 政策实施路径预测 | 未见 `metric_id`；判定 501。`M_POLICY_LAYOUT_REC_COUNT` 与 `M_POLICY_DS_11_POLICY_EVAL_015` 都不顶替 | 不新注册。不挂上述两条，不挂 `M_POLICY_SIMULATE`。路径环节行上的 `metric_id` 留空。读同一张缺项表的路径环节行 |
| 242 | 政策解读报告生成 | 未见 `metric_id`；判定 501。未注册研报能力。`FE-POL-07A` 不顶替 | 不新注册。解读段落行上的 `metric_id` 留空。读同一张缺项表的解读段落行。页面呈现正文。不产生文件 |

`M_POLICY_TEXT_PARSE` 与 `M_POLICY_RELATION_DEGREE` 的 D4 仍是 `mock`。`M_POLICY_SIMULATE` 的纸面 D4 也是 `mock`，本叶不改。238、239、241、242 没有专属 `metric_id`，没有可改的 D4。`GDF-POLICY-MOCK-GATE-L01` 在 `指标与501` 里仍是 blocked。本叶不把 mock 写成已上线，也不把该闸门写成已解开。

`指标与501` §8 把 237–239、241、242 的真路径写成「501，页面空态」，并写明解析行 237 同此。那是调研判定。已会签架构规定：237 读已有解析表，238、239、241、242 读缺项表，有行则读表，无行则该区空，不用 501 充当功能。240 仍是跨项索引，不设资源。本叶采用这条读面，不回头改 `指标与501`，也不把 501 改成可接统计读面，不把 240 改出跨项索引。

### 1.1 相对旧 DoD 与说明书 11.2 的收窄

`task-get` 返回的 DoD 仍写：只使用说明书第 2 节已有 `metric_id` 与三档；未注册模型保持 501；不写可算出数的假公式；不改 D4；不新注册指标。说明书第 11.2 节「推演 · 仿真 235–242」的要灌清单仍含「文本解析」，并写「240 关联只消费已有子图。不灌报告文件」。

本叶不改 DoD、不改说明书。收窄只写在本分册，读法以架构稿第 7、9 节为准：

- 三档保持原列。237、238、239、241、242 仍是 501。240 仍是跨项索引。六叶都不是可接统计读面。
- 237 不灌缺项文本解析。解析行已经在 `ads.policy_text_parse`。展示只读解析行。`POL-L2-DS12-SIM-GAPFILL-L01` 的「文本解析」按架构 §9 不灌。
- 242 读解读段落行。不产生 PDF、Word 或其他文件。不灌自定义格式。
- 238、239、241 与 242 同读 `gapfill_policy_sim_result`。行上 `metric_id` 留空。
- `M_POLICY_SIMULATE` 只被本叶认作已有推演号，不挂到 237–242。

## 2. 本二级用到的已有 metric_id

行上保持的已有号只有 237 的 `M_POLICY_TEXT_PARSE`。238、239、241、242 不在此表。240 没有独立号，不在此表。类型和 D4 只转述 `指标与501.md` 已有行，以及架构稿里写明的同一事实。不是 `metric-get` 的返回。

| metric_id | 中文名 | algorithm_type | D4 | 挂在 |
|---|---|---|---|---|
| `M_POLICY_TEXT_PARSE` | 未见 metric MCP，不填注册中文名。叶子名沿推演表「政策文本智能解析」 | MODEL | mock | 237。行上已有此号，本叶不改、不新造 |

这一条之外，本二级不新造 `metric_id`。

推演页只认的已有号是 `M_POLICY_SIMULATE`。`指标与501` §3.1：MODEL，D4=`mock`，判定 501。它只挂 232–234，归 `POL-L2-DS12-EST-METRIC`。本叶认它、不挂它、不改它的 D4。

叶子名与数据行上的号不是一回事：

- 237 的叶子名是「政策文本智能解析」。行上展示身份是已有的 `M_POLICY_TEXT_PARSE`。本叶不另起一条解析指标，也不把摘要升成第二指标。
- 238、239、241、242 的行上 `metric_id` 留空。
- 240 不设行，因此没有可填的独立 `metric_id`。纸面跨项号 `M_POLICY_RELATION_DEGREE` 留在第 7 项，见第 7 节。
- 模型注册表 `vendor/entan-py/conf/cfg_model_registry.yaml` 的 `POLICY_TEXT_PARSE` 把 `M_POLICY_TEXT_PARSE` 与 `M_POLICY_DS_11_POLICY_EVAL_012` 列在同一 `metric_ids` 下，`handler_module` 是 `polan.text.parse`，`ext.ads_table` 是 `ads.policy_text_parse`。本叶不改这份注册表。函数写入行的号只有 `M_POLICY_TEXT_PARSE`，见第 3 节。012 留在评价页 226，不挂 237。

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

因此本节不列八件套全表。不手抄公式，也不另写一条能算出解析、重点、影响范围、路径或解读正文的式子。

`指标与501` 237 行真路径列的原句是「501，页面空态」。这是判定说明，不是本叶查到的注册 `definition`。需求来源即序号 237，这句话写在说明书第 2 节与 `指标与501` 的 237 行，不是本叶新挂的 `srs_refs`。240 的「展示只消费读图」同样是判定说明，不是本叶查到的注册 `definition`。

已会签架构规定的是读哪张表，不是注册源表。读表只说明展示从哪里取数。无行则空。查询函数自己不跑解析，不生成重点，不拼影响范围，不编路径，不写解读正文。

| metric_id | 本叶能写的身份 | 读表（架构稿，不是注册源表） | 本叶不写的 |
|---|---|---|---|
| `M_POLICY_TEXT_PARSE` | MODEL。D4 转述为 mock，不改 | `ads.policy_text_parse` 的解析行。行上 `metric_id` 保持这个已有号 | 注册中文名、口径、公式、注册源表、源系统、更新频率、`version` |

237 的展示读数不在接口里重算，也不替换上表未抄的注册公式。类型仍是 MODEL。本叶不把它改成 STAT 或 GRAPH，也不在请求里调用 `run()`。

模型注册表 `POLICY_TEXT_PARSE.ext.ads_table` 写的是 `ads.policy_text_parse`。这是注册项上的表名，本叶不把它当成已经查过的八件套源表。`ext.is_mock` 为 true。这不是 metric MCP 的 D4。D4 只转述 `指标与501` 的 mock。

核对了 `lumen-algo-py` 的 `vendor/entan-py/polan/text/parse.py`。`run()` 从 `dwd.policy_base_info` 取未删除政策，用规则写出摘要、结构化要素和自动标签，然后 `truncate` 整张 `ads.policy_text_parse` 再插入。每一行的 `metric_id` 固定为字面量 `M_POLICY_TEXT_PARSE`。摘要取 abstract，空则取 content，并截断。结构化要素写入政策类型、级别、区域、发布年、要点；源对象里已有的适用对象、支持方式、申报条件会抄进同一结构。自动标签来自关键词、政策类型、主题。函数不写推演曲线，不写重点项、影响对象、路径环节、解读段落，插入行里也没有 `M_POLICY_SIMULATE`。

本叶不把这套截取收成 237 的公式，不在展示请求里调用 `run()`。一次展示请求若调用 `run()`，会清空整表，条款行一并被清掉。解析批次仍由已有灌数与条款跑批管道执行。

`M_POLICY_SIMULATE`、`M_POLICY_RELATION_DEGREE` 的八件套本叶同样未查。除 `指标与501` 已经写在纸面上的类型与 D4 外，不补口径和公式。

## 4. 接入状态

接入状态不是八件套。未见 metric MCP，本叶不写 D1、D2、D3，也不写 `d2_assessed`、`is_mock` 的注册布尔、`d4_note`、`srs_refs`、`lifecycle_stage`。这些字段没有查到，不能补成 `aligned`、`partial`、`full` 或空引用。

D4 只转述已有行，本叶不改：

| metric_id | D4 的出处 | 本叶 |
|---|---|---|
| `M_POLICY_TEXT_PARSE` | `指标与501` 237 行写 `mock`；架构稿写 D4=`mock` | 保持 mock。解析行已落在 ADS，不因此升 live |
| `M_POLICY_RELATION_DEGREE` | `指标与501` 240 行写 `mock`；架构稿写 D4=`mock` | 保持 mock。本叶不设独立号，也不改这条纸面 D4 |
| `M_POLICY_SIMULATE` | `指标与501` §3.1 写 `mock` | 保持 mock。本叶不挂、不改 |

238、239、241、242 没有专属 `metric_id`。没有可改的 D4。缺项表里灌入的行仍是 mock。本叶不把缺项写成已上线。

`M_POLICY_FOCUS_INDEX`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1`、`M_POLICY_DS_11_POLICY_EVAL_015`、`M_POLICY_DS_11_POLICY_EVAL_012` 的 D1–D4 本叶都未用 metric MCP 核对。除 `指标与501` 已经写在纸面上的类型外，不补维度。本叶不改它们的 D4，也不把它们改挂进 237–242。

## 5. 237 怎么读

行上保持 `M_POLICY_TEXT_PARSE`。`指标与501`：MODEL，D4=`mock`，判定列 501。说明书第 2 节同一行：501，并带这个已有号。

判定列仍留在 `指标与501` 里，本叶不改。读面按架构稿：不用 501 充当这块功能，也不把判定列升成可接统计读面或跨项索引。

解析结果行已由已有批产管道落在 `ads.policy_text_parse`。展示读的是这些已有行。本叶不新建指标。请求处理不调用 `polan.text.parse.run`。模型注册表里 `POLICY_TEXT_PARSE` 的 `status` 为 active，并有 `invoke_path`。架构规定展示不进异步白名单、不加 Job 键、不把该注册项当成展示侧可调用解析。本叶不改注册表，也不把 active 写成 237 已经在请求里真算。

资源是已有的 `POST /display/v1/policy/simulation/jobs`，种类为文本解析。链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `ads.policy_text_parse`。`gkxlumen-display` 不直连库，不直连 Python。element 只取解析行：`structured_elements` 不含条款键 `"clauses"` 的行。判别写法由 `POL-L2-DS12-SIM-DATA` 定。一次读取返回该政策的标题、摘要、自动标签、结构化要素。无行则报告空，不返回 501，不返回写死的报告，也不用条款行顶替。

行上的 `metric_id` 保持已有 `M_POLICY_TEXT_PARSE`。不新注册，不改 D4，不把读到的行写成已上线。不走核增拆解页的 `parse/jobs`、`parse/clauses`。那是 606/607/608 的资源。

说明书 11.2 把「文本解析」写在 SIM 组要灌清单里。架构 §9 收窄：已有表与已有产出的，不建缺项行。237 不灌 `gapfill_policy_sim_result`。`POL-L2-DS12-SIM-GAPFILL-L01` 开工时按该裁定执行，本叶不认领、不执行。

切条件不自动起任务。某一次 `jobs` 失败，不清其他种类已经返回的区块。缺项读面不进 `gkxlumen-topic-async-service`，无 SSE。

不做什么：不把中台 `GET /v1/policy/text/parse` 或 demo「文本解析」签迁进展示。不把评价页 226 的摘要读法当成 237 的全部列。226 的 `policy_text_parse` Job 键保持原状，本叶不加新键。不把 `M_POLICY_DS_11_POLICY_EVAL_012` 改挂到 237。

## 6. 238、239、241、242 没有专属 metric_id

238、239、241、242 在 `指标与501` 里 `metric_id` 为未见，判定列 501。说明书第 2 节与此相同。本叶不新注册，不改判定列，不改 D4，不挂 `M_POLICY_SIMULATE`。

真实的重点生成、真实的影响范围计算、真实的路径预测、真实的解读报告模型，本叶都做不到。架构的退路是缺项表：库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_result`。由 `POL-L2-DS12-SIM-GAPFILL-L01` 把 mock 行写入表，接口只查询。本叶不执行灌数，不写字段级 DDL。查询请求不灌数。字段级 DDL 由 `POL-L2-DS12-SIM-DATA` 定。

这四叶指不到专属 id。行上的 `metric_id` 留空。不把 237 的 `M_POLICY_TEXT_PARSE` 指进这四叶。不把 `M_POLICY_SIMULATE` 指进这四叶。

灌数行带 `metric_id`（留空）、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。D4 保持 mock。本叶不认领、不执行该灌数单。

资源同是 `POST /display/v1/policy/simulation/jobs`。一次只带一种类。链路同第 5 节，element 只读缺项表。无行则该区空，不返回 501，不返回写死的重点、范围、路径或全文。

### 6.1 238 政策重点可视化展示

没有已挂 `metric_id`。中台没有重点可视化模块。

不挂 `M_POLICY_FOCUS_INDEX`。焦点指数留在评价页 223。

读面种类为重点可视化。element 只读该政策的重点行：组别为政策目标、支持领域、实施路径、资金安排，加标题和一句明细。思维导图和图表在前端渲染。服务端只返回行。

行上 `metric_id` 留空。

不把 237 的解析标签改挂成重点项。不返回预渲染图片。

### 6.2 239 政策影响范围分析

没有已挂 `metric_id`。需规写明基于政策效果推演结果。推演号未挂到本行，判定仍是 501。本行不改成可接统计读面。

读面种类为影响范围。element 按该政策的推演上下文拣行：类别为受益对象、影响区域、影响行业，加名称、一句说明、时间变化说明。区域维度数据在行上，热力图和地图在前端渲染。

真推演接通之后，影响范围改随该次真结果，资源与种类键不变。那次改挂不在本叶。当前行是已灌的模拟上下文行，行上 `metric_id` 留空。无行则该区空，不造全国通用兜底行。

不把 234 的区域空间预测行复制成本叶。不把第 7 项图谱查询写成影响范围的计算源。

### 6.3 241 政策实施路径预测

没有已挂 `metric_id`。路径预测模型未见。

不挂 `M_POLICY_LAYOUT_REC_COUNT`。布局建议条数留在布局推荐键。不挂 `M_POLICY_DS_11_POLICY_EVAL_015`。015 留在评价页 229，由 `POL-L2-DS11-PLAN-METRIC` 挂接。241 不顶替 229，229 也不顶替 241。

读面种类为路径预测。element 只读路径环节行：环节为政策发布、申报受理、评审评估、资金拨付、效果评估，加时间安排、责任主体、一句说明。流程图在前端渲染。环节是预测展示。请求不推进环节状态，不写执行记录。

行上 `metric_id` 留空。无行则该区空，不在接口里编时间表。

### 6.4 242 政策解读报告生成

没有已挂 `metric_id`。关键词「解读」在调研里为 0 条。报告生成是未注册研报能力。

读面种类为解读报告。element 只读解读段落行：段落为政策背景、主要内容、预期效果、实施建议，加正文。页面呈现正文即查看。

不产生文件。下载在导出服务存在前不实现。不灌 PDF、Word。不灌自定义格式配置。无行则报告区空，不在接口里写死全文。

行上 `metric_id` 留空。

不把核增研报 `report/jobs`、`gapfill_policy_report_body` 当成本叶表。`FE-POL-07A` 不顶替本叶。不把 226 的摘要或评价页 224 的解读条目复制成这四段。

## 7. 240 没有独立 metric_id

`指标与501` 240 行：`M_POLICY_RELATION_DEGREE`，GRAPH，D4=`mock`，判定跨项索引。说明书第 2 节同一行：跨项索引，并带这个已有号。真路径是展示只消费读图。`GDF-POLICY-GRAPH-EXT-L01` 为 backlog，`E-E7-POLICY-M1-L02` 为 done。`E-E7-POLICY-M1-L06` 不是实现路径。

本叶不给 240 另造独立 `metric_id`。纸面号留在第 7 项。本叶不改它的类型，不改它的 D4，不把它写成可接统计读面，也不把它写进 `simulation/jobs` 的某一种类。

没有 HTTP 资源。不设种类。页面关联网络直接消费第 7 项政策子图。Java 不写 nGQL。本页不新建查图任务，不重画查图时序。浏览器不改打专题 URL。

模型注册表里 `POLICY_RE` 与 `POLICY_FOCUS` 的 `metric_ids` 都列了 `M_POLICY_RELATION_DEGREE`。本叶不调用这两条 `invoke_path`，不改注册表，也不据此给 240 单开展示 URL。`M_POLICY_FOCUS_INDEX` 与这条纸面号同列在 `POLICY_FOCUS` 下，仍不挂 238。

空态沿架构：本页没有可接统计读面。关联网络无图可消费时，该区块按页面已有读图空态呈现。本叶不返回 501 假网络，也不灌一张关联表来顶替。

## 8. 232–236 只交叉引用

232、233、234、235、236 的指标挂接归 `POL-L2-DS12-EST-METRIC`。本叶不写它们的口径、公式和行上号。

`指标与501` §3.2：232–234 共用 `M_POLICY_SIMULATE`，MODEL，D4=`mock`，判定 501。235、236 未见 `metric_id`，判定 501。架构：推演键只挂 232–234 的预测行。235 的多维评估行、236 的参与意见行已由 EST 半区裁定读法。灌数仍由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行：235 进 `gapfill_policy_sim_result`，236 进 `gapfill_policy_sim_stakeholder`。本叶不改这两行的行内容，也不把 `M_POLICY_SIMULATE` 补挂到 235、236。

`POL-L2-DS12-EST-METRIC` 当前未见落盘文件。交叉引用只指该任务，不代写其分册。

## 9. 点名不挂

下列号或序号在架构稿或 `指标与501` 里已经出现。本二级不把它们改挂到 237–242，也不改它们的 D4。身份未经过 metric MCP。下表只写本叶能从这两份已有文字、`parse.py` 和模型注册表里确认的内容。

| 号或序号 | 已有文字或代码里能确认的 | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_SIMULATE` | `指标与501` §3.1：MODEL，D4=`mock`，判定 501。说明书：推演只认这一条。模型注册表列在 `POLICY_SIMULATE` 下，`ads_table` 为 `ads.policy_simulate`。架构：只挂 232–234 | 本叶只认、不挂。237–242 的行不写这个号。不读 `ads.policy_simulate`，不调用 `polan.text.simulate.run` |
| `M_POLICY_TEXT_PARSE` 改去灌缺项或在请求里重跑 | 行上已有此号。`parse.run` 会清空 `ads.policy_text_parse`。架构 §9：237 不灌缺项行 | 237 只读已有解析行。不新建指标。不调用 `run()` |
| `M_POLICY_RELATION_DEGREE` 收成 240 的独立号或 HTTP 资源 | `指标与501` 240 行：GRAPH，D4=`mock`，跨项索引。架构：不设种类、不设资源 | 纸面号留在第 7 项。本叶不新造独立号，不设资源 |
| `M_POLICY_FOCUS_INDEX` | `指标与501` 238 行写明不挂。注册表与 `M_POLICY_RELATION_DEGREE` 同列在 `POLICY_FOCUS` | 238 不挂 |
| `M_POLICY_LAYOUT_REC_COUNT` | `指标与501`：布局推荐键 STAT，D4=`mock`，跨项索引。需规引用写过展示序号 241，该引用不改变分键 | 241 不挂。布局建议条数留在布局推荐键 |
| `M_POLICY_DEEP_171_1` | `指标与501` §3.1：MODEL，D4=`mock`，跨项索引。架构：不进 237–242 | 不挂 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | `指标与501` 241 行：不顶替 241。229 由 PLAN-METRIC 挂接 | 241 不挂。015 留在 229 |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 模型注册表与 `M_POLICY_TEXT_PARSE` 同列在 `POLICY_TEXT_PARSE`。`parse.run` 不写这个号 | 237 不挂。012 留在评价页 226 |
| `M_POLICY_EFFECT_SCORE` | `指标与501` 评价页 KPI：MODEL，D4=`mock`，判定 501。需求来源写过 232/233 | 不进 237–242 |
| 232–236 | 归 `POL-L2-DS12-EST-METRIC`。235、236 的读法在 EST-ARCH | 本叶只交叉引用 |
| `ads.policy_simulate`、`polan.text.simulate`、`/v1/policy/simulate` | 架构 §6：效果推演读面与批产闭包归 EST | 留在 EST。展示不直连 |
| `GET /v1/policy/text/parse` | 算法中台读面。架构：留原地 | 237 的展示读法走 `simulation/jobs`，不打 `/v1` |
| `parse/jobs`、`parse/clauses` | 核增拆解 606/607/608 | 不为 237 复用 |
| `report/jobs`、`gapfill_policy_report_body` | 核增智能研报 | 242 不读、不产生文件 |
| `E-E7-POLICY-M1-L06`、专题政策 URL | 架构：不是展示实现路径 | 240 不改打 |

`M_POLICY_SIMULATE` 与上表其余号的 D1–D3 未查。本叶只核对挂接边界，不展开它们的计算。

## 10. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不把 `M_POLICY_SIMULATE` 挂到 237–242。推演只认这一条已有号，挂接归 232–234。
- 不给 238、239、241、242 补 `metric_id`。指不到就留空。不把 237 的号指进这四叶。
- 不给 240 另造独立 `metric_id`，不设 HTTP 资源，不写 nGQL，不建查图任务。
- 237 不调用 `polan.text.parse.run`，不灌缺项文本解析，不把截取规则收成可算出数的公式。
- 242 不产生文件，不灌 PDF、Word 或自定义格式。
- 不改 `cfg_model_registry.yaml`。不改 `parse.py`。不进 `PolicyAnalysisTypes`，不加 Job 键。
- 不改 `指标与501.md`、`POL-L2-DS12-SIM-ARCH.md`、说明书、调研分册、WBS、指标 seed 与矩阵。判定列保持 501 与跨项索引。
- 不写 232–236 的指标分册。不代写 `POL-L2-DS12-EST-METRIC`。
- 不写 OpenAPI 字段、请求体、响应体、枚举、种类键名落库格式。
- 不见 metric MCP 就不填中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3、`srs_refs`。
- 不会签。不把本单标 done，也不标 `ready_to_sign`。不改任务状态。
