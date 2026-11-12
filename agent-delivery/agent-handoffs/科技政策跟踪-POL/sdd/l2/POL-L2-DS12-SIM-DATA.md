# POL-L2-DS12-SIM-DATA · 政策效果推演 · 科技政策推演 · 数据落点

- 任务：`POL-L2-DS12-SIM-DATA`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-06`
- 上游架构：`sdd/l2/POL-L2-DS12-SIM-ARCH.md` 第 5、7、9 节。该稿 2026-11-05 改过第 7、9 节的表张数与 235/236 灌数归属，读法未改。本单按该稿定列，不改那份架构，不改图。
- 读路径对照：同目录 `POL-L2-DS12-EST-ARCH.md` §5.4、§5.5、§9 只读。235、236 的读法归 EST。这两叶的列归本单。灌数归 `POL-L2-DS12-SIM-GAPFILL-L01`，与 EST §9 的灌数单名一致。本单不改 EST 已写的行内容：235 仍是一个维度的得分与说明；236 仍是一条参与意见。
- 写法对照：同目录 `POL-L2-DS11-PLAN-DATA.md`。本单不改那份方案分册。

本叶定政策效果推演里由本单落列的数据。SRS 序号 **235、236、237、238、239、240、241、242**。列级定义只定粒度和必要列。下面的列清单不是可执行 SQL。本单不建库、不灌数、不跑脚本。

上游只引用，不改写：`POL-L2-DS12-SIM-ARCH` 第 9 节、`POL-L2-DS12-EST-ARCH` §5.4 与 §5.5。不新造 `metric_id`，不改 D4。D4 保持 mock。空态是空。空表、无行、条件对不上，都返回空，不返回 501。

## 1. 范围

浏览器只打 `/display/v1/policy/**`。查询只读表。查询请求不灌数。接口不直接返回写死的 mock。

232、233、234 的列不在本单。那三叶的库是 `gkxlumenx_gapfill`，表是 `gapfill_policy_sim_forecast`，列归 `POL-L2-DS12-EST-DATA`，灌数归 `POL-L2-DS12-EST-GAPFILL-L01`。本单不写那张表的列，不把预测行抄进下面两张表。

本单新定列的表只有两张，都在库 `gkxlumenx_gapfill`。表名以 `gapfill_` 开头。两张表不并成一张，不加第三张。

| 序号 | 叶子 | 库 | 表 | 本单 |
|---|---|---|---|---|
| 235 | 多维度效果评估 | `gkxlumenx_gapfill` | `gapfill_policy_sim_result` 的多维评估行 | 本单定列。读法沿 EST §5.4。建表与灌数在灌数单 |
| 236 | 利益攸关方参与评估 | `gkxlumenx_gapfill` | `gapfill_policy_sim_stakeholder` 的参与意见行 | 本单定列。只放这一张。读法沿 EST §5.5 |
| 237 | 政策文本智能解析 | `gkxlumenx_ads` | `policy_text_parse` | 只读已有列。不建 gapfill 表，不加列，不灌 |
| 238 | 政策重点可视化展示 | `gkxlumenx_gapfill` | `gapfill_policy_sim_result` 的重点行 | 与 235 同一张结果表 |
| 239 | 政策影响范围分析 | `gkxlumenx_gapfill` | `gapfill_policy_sim_result` 的影响范围行 | 与 235 同一张结果表 |
| 240 | 政策关联分析 | （无 gapfill） | ADS `policy_graph_*` 只读 | 不设 jobs 表；样例可种子镜像 |
| 241 | 政策实施路径预测 | `gkxlumenx_gapfill` | `gapfill_policy_sim_result` 的路径环节行 | 与 235 同一张结果表 |
| 242 | 政策解读报告生成 | `gkxlumenx_gapfill` | `gapfill_policy_sim_result` 的解读段落行 | 内容只存正文列。不存文件路径 |

235、236、238、239、241、242 没有已挂指标。`metric_id` 留空，不因此新注册，也不把 D4 改绿。237 读已有行，行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`，本单不改。240 消费已有 `M_POLICY_RELATION_DEGREE`，本单不把这条指标写进 gapfill。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本叶不把 mock 写成已上线，也不把该闸门写成已解开。

本单只定列，不建库，不插入。不写 `gkxlumenx_ods`、`gkxlumenx_dwd`、`gkxlumenx_ads`，不写供应方库。237 对 `gkxlumenx_ads.policy_text_parse` 只读。

`gkxlumen-display` 不直连库。`gkxlumen-element` 按种类只读。235、236、237、238、239、241、242 走 `POST /display/v1/policy/simulation/jobs`。240 走 `GET .../simulation/relation-graph`，不走 jobs。Java 不生成得分、意见、重点、影响、路径、解读正文，不按公式现算，不插入意见，不跑 `polan.text.parse.run`，不写 nGQL。

## 2. 结果表

库 `gkxlumenx_gapfill`。表 `gapfill_policy_sim_result`。

235、238、239、241、242 共用这一张。236 不进这张表。237 不进这张表。240 不进这张表。不与 `gapfill_policy_sim_stakeholder` 合并。

一行是一个维度，或一个重点项，或一个影响对象，或一个路径环节，或一个解读段落。一行不是一份 PDF，不是一份 Word，不是一条预测曲线，不是政策子图上的一个点，不是一条参与意见。

`row_kind` 只有五个值：

| 值 | 序号 | 这一行放什么 |
|---|---|---|
| `多维评估` | 235 | 一个维度：维度名、得分、一句说明。维度只用经济、社会、环境、创新 |
| `重点` | 238 | 一个重点项：所属政策、组别、标题、一句明细。组别只用政策目标、支持领域、实施路径、资金安排 |
| `影响范围` | 239 | 一个影响对象：所属政策、类别、名称、一句说明、时间变化、区域维度原文；另有覆盖率三字段与渗透指数。类别只用受益对象、影响区域、影响行业 |
| `路径环节` | 241 | 一个环节：所属政策、环节、时间安排、责任主体、一句说明。环节只用政策发布、申报受理、评审评估、资金拨付、效果评估 |
| `解读段落` | 242 | 一个段落：所属政策、段落、正文。段落只用政策背景、主要内容、预期效果、实施建议。正文是文字，不是文件路径 |

没有第六个值。`参与意见` 不写入本表。

下列是必要列。建表语句由灌数单 `POL-L2-DS12-SIM-GAPFILL-L01` 落地。本单不执行该单，也不在这里给出可执行脚本。这张列清单不是可执行 SQL。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `row_kind` | varchar(16) | 否 | `多维评估`、`重点`、`影响范围`、`路径环节`、`解读段落` 五者之一 |
| `policy_id` | varchar(256) | 是 | 重点、影响范围、路径环节、解读段落必填。与 `gkxlumenx_ads.policy_text_parse.policy_id` 是同一条政策的标识。多维评估行空，写 NULL，不写空字符串 |
| `dimension_name` | varchar(16) | 是 | 多维评估行必填：`经济`、`社会`、`环境`、`创新` 四者之一。四个维度各一行。其余行空 |
| `score_value` | decimal(10,4) | 是 | 多维评估行必填：该维度得分。**重点行可用**（2026-11-12 238 COVER-FDE 卡1=B）：该组重点展示分，供柱图纵轴；无分写 NULL，不用 0 占位。影响范围 / 路径 / 解读行仍空 |
| `score_text` | text | 是 | 多维评估行必填：该维度一句说明。其余行空 |
| `group_name` | varchar(16) | 是 | 重点行必填：`政策目标`、`支持领域`、`实施路径`、`资金安排` 四者之一。其余行空 |
| `item_title` | varchar(256) | 是 | 重点行必填：标题。其余行空 |
| `detail_text` | text | 是 | 重点行必填：一句明细说明。其余行空 |
| `impact_kind` | varchar(16) | 是 | 影响范围行必填：`受益对象`、`影响区域`、`影响行业` 三者之一。其余行空 |
| `impact_name` | varchar(256) | 是 | 影响范围行必填：名称。其余行空 |
| `impact_text` | text | 是 | 影响范围行必填：一句说明。其余行空 |
| `time_change_text` | text | 是 | 影响范围行必填：时间变化说明。其余行空 |
| `region_text` | text | 是 | 影响范围行必填：区域维度的展示原文。热力图和地图用这段原文在前端画。不存地图文件，不存文件路径。其余行空 |
| `coverage_rate` | decimal(8,2) | 是 | 影响范围行可用：覆盖率 %。受益对象行宜填；其余种类行空，写 NULL |
| `eligible_count` | int | 是 | 影响范围行可用：应覆盖主体数。与 `coverage_rate` 同挂受益对象行；其余行空 |
| `covered_count` | int | 是 | 影响范围行可用：已覆盖主体数。与 `coverage_rate` 同挂受益对象行；其余行空 |
| `penetration_score` | decimal(8,2) | 是 | 影响范围行可用：渗透指数 0–100。影响区域、影响行业行宜填；受益对象行可空 |
| `stage_name` | varchar(16) | 是 | 路径环节行必填：`政策发布`、`申报受理`、`评审评估`、`资金拨付`、`效果评估` 五者之一。同一政策、同一环节只一行。其余行空 |
| `schedule_text` | varchar(256) | 是 | 路径环节行必填：时间安排，展示原文。其余行空 |
| `owner_name` | varchar(256) | 是 | 路径环节行必填：责任主体。其余行空 |
| `stage_text` | text | 是 | 路径环节行必填：一句说明。其余行空 |
| `section_name` | varchar(16) | 是 | 解读段落行必填：`政策背景`、`主要内容`、`预期效果`、`实施建议` 四者之一。同一政策、同一段落只一行。其余行空 |
| `body_text` | text | 是 | 解读段落行必填：正文。这是 242 唯一的内容列。不设文件路径、对象键、文件字节。其余行空 |
| `is_mock` | tinyint | 否 | 每行必须为 1。D4 仍是 mock |
| `metric_id` | varchar(64) | 是 | 五种行都留空，写 NULL，不写空字符串 |
| `gap_item` | varchar(128) | 否 | 序号加叶子名。见下表 |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间。由灌数单填写，本单不生成 |

`gap_item` 按种类固定：

| `row_kind` | `gap_item` |
|---|---|
| `多维评估` | `235 多维度效果评估` |
| `重点` | `238 政策重点可视化展示` |
| `影响范围` | `239 政策影响范围分析` |
| `路径环节` | `241 政策实施路径预测` |
| `解读段落` | `242 政策解读报告生成` |

`fill_method` 固定 `manual`，因此不设 `fill_model`。政策只在方法为 `llm` 时要求模型名。

D16 行级列是 `metric_id`、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。外加 `is_mock=1`，避免把缺项行读成已上线。谁写这张表：灌数单里的 Python 脚本。Java 与前端不建表、不灌数。谁读：仅功能验收链路上的 `gkxlumen-element`。生产配置不读 `gkxlumenx_gapfill`。本叶不把读到的行写入 ADS，因此不产生 `gapfill_` 前缀的 `calc_batch_id`。

拣行只用 `row_kind`。重点、影响范围、路径环节、解读段落再加 `policy_id`。多维评估不按政策拣。条件对不上的行不返回。查询不插入行来凑数。

## 3. 235 多维评估

粒度沿 EST §5.4，本单不改：一行一个维度。维度名在 `dimension_name`，只用经济、社会、环境、创新。得分在 `score_value`。一句说明在 `score_text`。雷达图、柱状图的数就是这些行的得分。说明不写进得分列。

`policy_id` 留空。这叶的行不挂到某一条政策上，也不挂参数档、区域、政策类型。那些是预测表上的拣行条件，列不进本表。

四个维度各一行。同一维度只保留一行。读取按经济、社会、环境、创新的固定顺序，不另设排序列。

`metric_id` 留空。不挂 `M_POLICY_SIMULATE`，不挂 `M_POLICY_DEEP_168_1`。推演键只挂 232–234 的预测行，那一行不在本表。

`jobs` 的多维评估只读 `row_kind=多维评估`。无行则雷达和柱状空。不返回 501。查询原样返回得分，请求内不现算。

## 4. 238 重点

粒度：一行一个重点项。政策在 `policy_id`。组别在 `group_name`。标题在 `item_title`。一句明细在 `detail_text`。思维导图和图表的节点由这些行构成，渲染在前端。

组别只用政策目标、支持领域、实施路径、资金安排。同一政策、同一组可以有多行。读取时组按这四组的固定顺序，同一组内按 `id` 从小到大。不设组内排序列。

**柱图数值（2026-11-12 COVER-FDE 卡1=B）**：复用已有列 `score_value`，**不 ALTER、不新造列**。重点行可写展示分（mock）；前端按 `group_name` 画柱（同组多行取非空最大）。全空则柱区业务空态，**禁止**从 `detail_text` 解析「名+分」顶替。不挂新 `metric_id`；与 235 同列分流：多维=维度分，重点=组重点分。

`metric_id` 留空。不挂 `M_POLICY_FOCUS_INDEX`。不把 237 的解析标签写进 `item_title` 或 `detail_text`。

`jobs` 的重点可视化按 `policy_id` 拣 `row_kind=重点`。政策必选。未给出政策，或没有对得上的行，该区空。不返回预渲染图片。样例可演：`policy_id=18363390` 四组宜带 `score_value`（建议 88/82/75/80，D 波灌数可微调）。

## 5. 239 影响范围

粒度：一行一个影响对象。政策在 `policy_id`，这就是该次推演上下文里的所属政策。类别在 `impact_kind`。名称在 `impact_name`。一句说明在 `impact_text`。时间变化在 `time_change_text`。区域维度原文在 `region_text`。

三类都要填 `region_text`。热力图、地图在前端用这段原文渲染。服务端只返回行。不存地图文件，不存文件路径。

覆盖面 KPI：`coverage_rate` / `eligible_count` / `covered_count` 挂在 `impact_kind=受益对象` 行；无值则覆盖面卡空态「暂无覆盖面数据」。渗透深度：`penetration_score` 挂在影响区域、影响行业行，驱动「渗透指数」柱图；`region_text` 若写成「地名+分」还可画分区域柱与地图。

`metric_id` 留空。不把 234 的区域空间预测行抄进本种类。不把第 7 项图谱结果写进 `region_text`。

`jobs` 的影响范围按 `policy_id` 拣 `row_kind=影响范围`。政策必选。无行则该区空。不造全国通用兜底行。真推演接通前，这些行就是已灌的模拟上下文行。本单不改资源，不改 `row_kind` 的值。

## 6. 241 路径

粒度：一行一个环节。政策在 `policy_id`。环节在 `stage_name`。时间安排在 `schedule_text`。责任主体在 `owner_name`。一句说明在 `stage_text`。流程图由这些行构成，渲染在前端。

五个环节各对应已灌的行。同一政策、同一环节只保留一行。读取按政策发布、申报受理、评审评估、资金拨付、效果评估的固定顺序，不按 `schedule_text` 的原文排序，不设 `sort_no`。

环节是预测展示。请求处理不推进环节状态，不写执行记录。本表不设状态列。

`metric_id` 留空。不挂 `M_POLICY_LAYOUT_REC_COUNT`，不挂 `M_POLICY_DS_11_POLICY_EVAL_015`。不把评价页 229 的路径与风险行抄进本种类。

`jobs` 的路径预测按 `policy_id` 拣 `row_kind=路径环节`。政策必选。无行则该区空。不在接口里编时间表。

## 7. 242 解读正文

粒度：一行一个段落。政策在 `policy_id`。段落名在 `section_name`。正文在 `body_text`。

`body_text` 是这一种类唯一的内容列。页面呈现的就是这段正文。不设文件路径、对象键、文件名、文件字节、PDF、Word。不灌自定义格式配置。

四个段落各一行。同一政策、同一段落只保留一行。读取按政策背景、主要内容、预期效果、实施建议的固定顺序。

`metric_id` 留空。不把 226 的 `summary` 抄进 `body_text`。不把核增研报 `gapfill_policy_report_body` 的行抄进本表。不把评价页 224 的解读条目抄进来。

`jobs` 的解读报告按 `policy_id` 拣 `row_kind=解读段落`。政策必选。无行则报告区空。不返回写死的全文，不返回文件。

## 8. 意见表

库 `gkxlumenx_gapfill`。表 `gapfill_policy_sim_stakeholder`。

只放 236。一行是一条已灌的参与意见。这张表不放 235、237、238、239、240、241、242。不与结果表合并，不加第三张。

`row_kind` 只有一个值：

| 值 | 序号 | 这一行放什么 |
|---|---|---|
| `参与意见` | 236 | 一条意见：所属政策、主体、渠道、意见正文、时间。主体只用决策者、评估者、利益攸关方。渠道只用在线问卷、意见征集、专家评审 |
| `评估识别` | 236 | 一条识别结论：所属政策、检查项、结论、一句说明。检查项只用目标是否合理、组织是否协调、程序是否公正规范、方法是否科学可行 |

下列是必要列。建表语句同样由 `POL-L2-DS12-SIM-GAPFILL-L01` 落地。这张列清单不是可执行 SQL。线上已有表须 ALTER 加列（见 `gapfill_policy_sim_stakeholder_236_alter.sql`），不建第二张意见表。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键。灌数单建表时自增 |
| `row_kind` | varchar(16) | 否 | `参与意见` 或 `评估识别` |
| `policy_id` | varchar(256) | 否 | 两种行都必填。与全景目录 / 新出台样例同一业务键 |
| `actor_role` | varchar(16) | 是 | 参与意见行必填：`决策者`、`评估者`、`利益攸关方` 三者之一。评估识别行空 |
| `channel_name` | varchar(16) | 是 | 参与意见行必填：`在线问卷`、`意见征集`、`专家评审` 三者之一。评估识别行空 |
| `opinion_text` | text | 是 | 参与意见行必填：意见正文。评估识别行空 |
| `opinion_at` | datetime | 是 | 参与意见行必填：意见时间。与 `generated_at` 不是同一列。评估识别行空 |
| `audit_item` | varchar(32) | 是 | 评估识别行必填：四项检查之一。参与意见行空 |
| `audit_result` | varchar(32) | 是 | 评估识别行必填：结论短词。参与意见行空 |
| `audit_text` | text | 是 | 评估识别行必填：一句说明。参与意见行空 |
| `is_mock` | tinyint | 否 | 每行必须为 1。D4 仍是 mock |
| `metric_id` | varchar(64) | 是 | 留空，写 NULL，不写空字符串 |
| `gap_item` | varchar(128) | 否 | 固定 `236 利益攸关方参与评估` |
| `fill_method` | varchar(16) | 否 | 固定 `manual` |
| `gapfill_batch_id` | varchar(64) | 否 | 灌数批次。由灌数单填写，本单不生成 |
| `generated_at` | datetime | 否 | 行写入时间。由灌数单填写，本单不生成 |

不设 `fill_model`。不加预测列。不设汇总列。呈现侧汇总只在读取时数该政策下的参与意见行。模型接通前，这个计数不写回结果表的得分。「纳入效果评估模型」不做。

`jobs` 的利益攸关方**必须**带 `policy_id`。无政策不查表。有政策则读该 `policy_id` 下 `row_kind IN (参与意见, 评估识别)`。参与意见按 `opinion_at`、`id`；评估识别按四项固定顺序。无行则空。请求处理不插入、不更新、不删除。用户在页面上新提交的意见留在浏览器，直到另有采集单。本叶不建那张单。

不把序号 210 的受众反馈、序号 230 的方案意见复制进本表。

## 9. 237 解析表 · 只读 + 真算 upsert（不加列）

不另建表，不加列，不建文本解析用的 gapfill 表。库 `gkxlumenx_ads`、表 `policy_text_parse`。

**读面**：按 `policy_id` 读。返回 `title`、`summary`、`auto_tags`，以及 `structured_elements` 里除 `clauses`、`clause_meta` 以外的内容（四中文键在内）。

**真算写回（2026-11-12）**：`policy_text_parse_run` 对单政策 **UPSERT**：写入/合并四中文键 + summary/tags；**必须保留**已有 `clauses`/`clause_meta`。禁止 `polan.text.parse.run` 整表清空。条款批次仍只改条款键，不另插行。

行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。D4 保持 mock。无行则读面空；真算失败不造假四键。

## 10. 240 无 gapfill 表（relation-graph）

不设 jobs 种类，不建 gapfill 关联表。页面经 display `relation-graph` 消费第 7 项子图（ADS `policy_graph_node/edge` / Nebula）。指标仍是已有 `M_POLICY_RELATION_DEGREE`。本单不把这条指标写进结果表或意见表，不写 nGQL，不建查图任务。样例不足时允许 ADS 最小种子（batch `seed-240-relation-20261112`，非 gapfill_sim）。

无图则该区业务空态「暂无政策关联网络」。本单不造 jobs 关联行来填。

## 11. 灌数单

灌数单 `POL-L2-DS12-SIM-GAPFILL-L01` 依赖本单和 `POL-L2-DS12-SIM-ARCH`。执行人是 `data-agent`，监管是 `human:淮政玮`。本单只点名，不认领，不执行，不建库，不插入行，不改那张任务的注册字段。

该单当前仍是 `backlog`。它的 DoD 写了两张缺项表，并写了要灌文本解析。文本解析按 `POL-L2-DS12-SIM-ARCH` 第 9 节收窄。执行时以本分册为准：

| 灌数单 DoD 里的项 | 本分册 |
|---|---|
| 建 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` | 保持。库只允许 `gkxlumenx_gapfill`。列按第 2 节和第 8 节 |
| 多维评估 | 灌进结果表，`row_kind=多维评估` |
| 参与意见 | 灌进意见表，`row_kind=参与意见` |
| 重点、影响范围、路径、解读正文 | 灌进结果表，种类分别为重点、影响范围、路径环节、解读段落 |
| 文本解析 | 不灌。不写 `gkxlumenx_ads.policy_text_parse`，不在两张 gapfill 表里加文本解析行 |
| 240 不建表 | 保持 |
| 不灌报告文件 | 保持。242 只灌 `body_text`，不灌文件路径 |
| 不改 D4，不新造 `metric_id` | 保持 |

灌数单要灌的最少内容，沿两份架构已写的行内容，本单仍不执行：

| 种类 | 灌数单以后要灌 | 不灌 |
|---|---|---|
| 多维评估 | 经济、社会、环境、创新各一行。每行有得分和一句说明 | 参数档、GDP、就业率、预测曲线、推演键 |
| 参与意见 | 若干条。每条有主体、渠道、意见正文、时间 | 页面当场提交的新意见、受众问卷、方案意见 |
| 重点 | 四组下的重点项。每项有组别、标题、一句明细 | 焦点指数、预渲染图片、解析标签 |
| 影响范围 | 三类影响对象。每行有类别、名称、一句说明、时间变化、区域维度原文；受益对象行带覆盖率三字段；区域/行业行带渗透指数 | 全国兜底行、地图文件、234 的空间预测行 |
| 路径环节 | 五环节。每行有环节、时间安排、责任主体、一句说明 | 布局推荐条数、流程执行记录、评价页 229 的方案路径 |
| 解读段落 | 四段正文 | PDF、Word、文件路径、自定义格式、核增研报正文 |
| 文本解析 | 不灌 | 解析行、条款行、对 `policy_text_parse` 的插入或清空 |
| 240 | 不灌 | 关联边、查图结果 |

六种业务行都带各自表上的 D16 列，`fill_method=manual`，`is_mock=1`，`metric_id` 留空。查询请求不调用这张灌数单。空表返回空。本单不写示例行。

## 12. 跨项只写消费边界

| 序号或资源 | 边界 |
|---|---|
| `gkxlumenx_gapfill.gapfill_policy_sim_forecast` | 232–234。列归 `POL-L2-DS12-EST-DATA`。本单不写那张表的列，不把预测行抄进结果表或意见表 |
| `M_POLICY_SIMULATE` | 只挂 232–234。不写入本单六种业务行 |
| `gkxlumenx_ads.policy_text_parse`、`M_POLICY_TEXT_PARSE`、`polan.text.parse.run` | 237 只读已有解析行。不灌，不加列，不在请求里调用 `run`。不把 `summary` 抄成 242 的正文 |
| `M_POLICY_DEEP_168_1` | 不拿来填 235 的得分 |
| `M_POLICY_FOCUS_INDEX` | 评价页焦点指数。不挂 238 |
| `M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DEEP_171_1` | 布局推荐键。不写入本单的表 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | 评价页 229。不顶替 241，不写入本单的表 |
| `M_POLICY_RELATION_DEGREE` | 240 跨项读图。本单不建表，不写 nGQL |
| `M_POLICY_EFFECT_SCORE` | 评价页。不挂本单的行 |
| 序号 234 | 区域空间预测。不抄进 239 |
| 序号 226 | 智能摘要。不抄进 242 |
| 序号 224 | 评价页解读条目。不抄进 242 |
| 序号 229、`gapfill_policy_eval_scheme` | 评价页路径与风险。不顶替 241 |
| 序号 210、`gapfill_policy_audience_feedback` | 受众反馈。不抄进 236 |
| 序号 230 | 方案互动意见。不抄进 236 |
| `report/jobs`、`gapfill_policy_report_body` | 核增研报。不是 242 |
| `parse/jobs`、`parse/clauses` | 核增拆解。不是 237 |
| `ads.policy_simulate`、`/v1/policy/simulate` | 中台推演读面。留在 EST 与中台，本单不读不写 |
| `GDF-POLICY-MOCK-GATE-L01` | 仍是 blocked。本单不把它写成已解开 |
| `E-E7-POLICY-M1-L06` | 不是本页实现路径 |

## 13. 明确不做

- 不写可执行 SQL，不建库，不灌数，不跑解析函数，不跑推演函数。
- 不重开 GDF，不写 nGQL，不加 ODS、DWD、ADS 表，不写供应方库，不改 `policy_text_parse` 的列。
- 不把结果表和意见表并成一张。不加第三张 gapfill 表。
- 不写 `gapfill_policy_sim_forecast` 的列。
- 不灌文本解析。不把文本解析行写进 gapfill。
- 240 不建表。242 不设文件路径列。
- 不新造 `metric_id`，不改 D4，不把缺项行写成已上线。
- 空态返回空，不返回 501。
- 查询不插入。236 的页面提交不写库。
- 列清单不是可执行 SQL。本单不写示例行。
- 不改架构稿、调研分册、`指标与501.md`、说明书、WBS、注册表、代码仓。
- 不认领 `POL-L2-DS12-SIM-GAPFILL-L01`。不改它的注册字段。
- 不把本单标成 done 或 ready_to_sign。
