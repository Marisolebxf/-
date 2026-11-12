# POL-L2-DS12-EST-API · 政策效果推演 · 效果预估 · 后台接口设计

- 任务：`POL-L2-DS12-EST-API`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-06`
- 上游：`sdd/l2/POL-L2-DS12-EST-ARCH.md`（2026-11-04 落盘。2026-11-05 只改第 5.4、5.5 节的库.表写法，读法未改。本分册以工作区这份为准，不改它）
- 对照只读：`sdd/l2/POL-L2-DS12-SIM-ARCH.md`（共用同一条 `simulation/jobs`。235/236 的读法在 EST-ARCH，灌数在 `POL-L2-DS12-SIM-GAPFILL-L01`。本分册不改 SIM-ARCH，不改那两张表的行内容）

2026-11-07 修订（`human:淮政玮`）：232 未出台仿真增加目标产业等值过滤。请求字段与列名都是 `target_industry`。比较值是产业级联的回显全文，不是内部编码，也不是 `industry_text`。提交了才 `target_industry = ?`；没提交不参与过滤。五类里至少提交一类，五类都空则不查。对不上则该次模拟空。多选回显整串参与等值，不拆成 OR。233–236 不改。不新指标，D4 仍是 mock。会签原文仍记四类参数，实现以本修订和 `POL-L2-DS12-EST-DATA` 同日修订为准。修复单 `POL-L2-DS12-INDUSTRY-EQ-FIX-L01`。

本分册只定政策效果推演二级「效果预估」的后台接口。SRS 序号 **232–236**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件，不写契约仓代码。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、内部委托、同步或 Job、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS12-EST-ARCH` 为准。契约输入清单里推演页已经点名的 `simulation/jobs` 只作资源名对照。清单、`指标与501.md`、说明书、WBS、调研里仍写的 501 空态不覆盖本分册。

签收口径：推演整页对外只有一条资源 `POST /display/v1/policy/simulation/jobs`。232–236 在这一条上按种类分发，一次请求只带一种类。232–234 读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。235 读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。236 读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。五叶都是同步读，不建任务。不允许接口直接返回 mock，也不用 501 充当这五叶的功能。无行则空。237–242 的种类由 `POL-L2-DS12-SIM-API` 定义，本分册只交叉引用。

## 偏离

三处与上游 DoD 或仍在架上的旧空态字面不一致。本分册写明，不回头改那些文件。

1. DoD「不复用 `/topic/v1/policy`」在本二级是：浏览器只打 `/display/v1/policy/**`。232–236 的内部委托也不打专题政策 URL，不调用 `POST /topic/v1/analysis/tasks`，不进 `gkxlumen-topic-async-service`。233 选已出台政策时，候选列表复用已有全景检索，那次检索不代替本叶的 `jobs`。本分册不改全景检索。
2. DoD 完成标准里的「501 空态」，`指标与501.md` §3.2 仍把 232–236 写成 501、页面空态，契约输入清单把整条 `POST /display/v1/policy/simulation/jobs` 标成 Job，并把仿真、预测曲线、区域空间、多维评估、利益攸关方的空态写在这一条 Job 上。2026-11-05 架构把这五叶改成读缺项表：同步，不建任务。本分册按该架构写。空态是空，HTTP 成功，不返回 501。架构第 2 节另有一行「真推演」：模型未注册时该种类 501。232–236 不走那一行。本分册不新增这个 kind，不把五叶的空态写成 501。不改 `指标与501.md`、说明书、WBS、调研、契约输入清单，也不改 SIM-ARCH。
3. 不把整条 `jobs` 改成只读 `gapfill_policy_sim_forecast`。235 只读结果表里的多维评估行，236 只读参与意见表。237、238、239、241、242 的种类留给 `POL-L2-DS12-SIM-API`。240 按 SIM-ARCH 不设种类。本分册不改写那些种类的语义。

## 1. 公开资源

前缀 `/display/v1/policy/`。五叶都在政策效果推演页里完成，不另开页，不另开路径，不另开 dispatcher。本二级对外只有下面这一条，且一次请求只带一种类。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 232 未出台仿真 | `POST /display/v1/policy/simulation/jobs` | 同步。种类为未出台仿真。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 的未出台仿真行。政策类型、覆盖范围、支持力度、实施时间、目标产业五类至少一类。提交了的类与行上等值。对不上则该次模拟空。不建任务。不返回 501 |
| 233 新出台预测 | 同一条 `POST /display/v1/policy/simulation/jobs` | 同步。种类为新出台预测。同一张表按已出台政策拣预测行。无行则该区空。不调 `parse/jobs`。不建任务。不返回 501 |
| 234 区域空间 | 同一条 `POST /display/v1/policy/simulation/jobs` | 同步。种类为区域空间。同一张表按区域与政策类型拣行。对不上则空间结果空。不建任务。不返回 501 |
| 235 多维评估 | 同一条 `POST /display/v1/policy/simulation/jobs` | 同步。种类为多维评估。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。无行则雷达和柱状空。不建任务。不返回 501 |
| 236 利益攸关方 | 同一条 `POST /display/v1/policy/simulation/jobs` | 同步。种类为利益攸关方，必须 `policy_id`。element 读该政策下参与意见行与评估识别行。无政策或无行则空。请求不插入。不建任务。不返回 501 |

`simulation/jobs` 上还有 237–242。那些种类的定义在 `POL-L2-DS12-SIM-API`，读法以 `POL-L2-DS12-SIM-ARCH` 为准。本分册不改写，也不把查预估表的读法套到它们身上。

| 留给谁 | 种类 | 本分册不改的读法 |
|---|---|---|
| `POL-L2-DS12-SIM-API` | 文本解析（237） | 同一条 `jobs`。element 只读 `ads.policy_text_parse` 的解析行。语义以 SIM-ARCH §5.1 为准 |
| `POL-L2-DS12-SIM-API` | 重点可视化（238）、影响范围（239）、路径预测（241）、解读报告（242） | 同一条 `jobs`。读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 里各自的行种类。与 235 的多维评估行不是同一种类 |
| `POL-L2-DS12-SIM-ARCH` | 240 无种类 | 不走 `simulation/jobs`。页面消费第 7 项子图。本分册不设资源 |

布局推荐键 `M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT` 不进这五叶，不顶替推演。`FE-POL-03A` 页头「布局建议」卡槽是复刻壳。评价页序号 228 的参数模拟走 `evaluation/jobs`，不共用本资源。

`PolicyAnalysisTypes` 与 `JOB_SUB_TYPES` 现无 `policy_simulate`。本分册不加这个子类型，也不把 232–236 塞进白名单里已有的任何一项。这五叶不进 `POST /internal/policy/jobs/execute`。

种类字段名由 `BE-POL-CONTRACT-01` 冻结。本分册只定种类的中文名和一次一种类：未出台仿真、新出台预测、区域空间、多维评估、利益攸关方。236 的「参与意见」是行内容，不是第二种请求种类。架构第 5.5 节写「种类为参与意见」，与第 2、3、4 节的请求种类「利益攸关方」并存；公开 kind 取后者。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`，不打开算法中台页面，不打 `/v1/policy/**`，不打 `/v1/policy/simulate`。

`gkxlumen-display` 不直连库，不直连 Python，不做 NLP，不写算法，不写 nGQL。不调用任何 `demo-*` 服务。请求路径不进入 Python。Java 不生成预测，不按弹性公式现算，不拼空间分布，不插入意见，不返回写死的曲线、得分或意见。

| 公开资源 | 内部委托 |
|---|---|
| `jobs` 的未出台仿真、新出台预测、区域空间 | `gkxlumen-display` 不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python，不占并发锁，不发 SSE。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 里该次种类的行 |
| `jobs` 的多维评估 | 同样不建任务、不进异步、不调 Python。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。不读这张表上重点、影响范围、路径环节、解读段落的行 |
| `jobs` 的利益攸关方 | 同样不建任务、不进异步、不调 Python。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。请求不插入、不更新、不删除 |

若 `gkxlumen-display` 还没有推演控制器，实现时按契约补这一条 `simulation/jobs`。补上之后仍按种类分发。不能把整条 `jobs` 改成只读预估表，也不能为 232–236 再开第二条 dispatcher。本分册不补控制器，不写 Java。

五叶都不进异步任务管道。切条件、切参数不自动起任务。某一次 `jobs` 失败，不清其他种类已经返回的区块。本页可接统计读面为 0，没有会随这次失败被清空的同步统计卡。

trace 沿既有展示链。display 往 element 带 traceId。本分册不新设计观测点。

232–234 的字段级 DDL 由 `POL-L2-DS12-EST-DATA` 定，灌数由 `POL-L2-DS12-EST-GAPFILL-L01` 执行。235、236 的字段级 DDL 由 `POL-L2-DS12-SIM-DATA` 定，灌数由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行。本分册不改行内容，不执行灌数，不写 DDL。查询请求不灌数。库只允许 `gkxlumenx_gapfill`。不进 ODS、DWD、ADS，不写供应方库。

232–234 的行带 `metric_id`（三种都用已有推演键 `M_POLICY_SIMULATE`）、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`，以架构第 9 节为准。235、236 的行上 `metric_id` 留空，不新注册，不借用 `M_POLICY_SIMULATE`，不借用 `M_POLICY_DEEP_168_1`。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。D4 保持 mock。`GDF-POLICY-MOCK-GATE-L01` 不在本分册写成已解开。本分册不把 mock 写成已上线，不改 D4。

## 3. 232 未出台政策仿真模拟 · jobs · 未出台仿真

公开资源：`POST /display/v1/policy/simulation/jobs`。浏览器提交这一次，种类为未出台仿真。没有未出台政策仿真模型。不挂 `M_POLICY_DEEP_171_1`，不挂 `M_POLICY_LAYOUT_REC_COUNT`。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 的未出台仿真行。

- 同步。不建任务。不进 `PolicyAnalysisTypes`。不加 `policy_simulate`
- 一行是一组参数档：政策类型、覆盖范围、支持力度、实施时间、目标产业，加上经济效益、社会影响、创新促进的预测值、逐年趋势、一句可解释说明。雷达和曲线的数就是这些行。字段名归 `POL-L2-DS12-EST-DATA`
- 五类参数至少选一类。少了则该区空，不补默认值
- 用户提交了的参数必须与行上对应列相等。没提交的参数不参与过滤。目标产业的请求字段是 `target_industry`，值是级联回显全文。多选时整串等值，不拆开。参数档对得上的行原样返回。对不上则该次模拟空
- 多方案比较由前端把多次查询并排，或同一次请求带上多组参数档、一次读回多行。参数档怎么装箱由契约单冻结。服务端不建对比槽，不存用户模拟历史，不灌假历史
- 不调用 `polan.text.simulate`。不读 `ads.policy_simulate`。不把中台三条固定情景写成这张表的读法
- Java 不按弹性公式现算。切参数不自动起任务

空态：五类都没选，或参数档对不上行，则该次模拟空。HTTP 成功。不返回 501。不在接口函数里返回写死的预测值或曲线。

## 4. 233 新出台政策效果预测 · jobs · 新出台预测

公开资源与 232 相同：`POST /display/v1/policy/simulation/jobs`。浏览器另一次提交，种类为新出台预测。一次请求不带未出台仿真，也不带区域空间。

没有新出台政策预测模型。需规写「基于政策文本解析和历史相似政策效果数据」。推演不为 `M_POLICY_TEXT_PARSE` 单开通道。

链路与第 3 节相同，element 只读同一张预估表里的新出台预测行。

- 一条已出台政策必选。少了政策则该区空，不补一条默认政策
- 一行挂在一条已出台政策上：短期与长期效果、经济增长、产业发展、科技创新影响、时间变化趋势、空间分布特征、相似政策依据说明。依据是行内说明，字段名归 `POL-L2-DS12-EST-DATA`
- 行上 `metric_id` 用已有 `M_POLICY_SIMULATE`。不新注册
- 不调 `parse/jobs`，不调 `policy_text_parse`，不现做文本解析。无预测行时不返回解析结果顶替
- 候选政策列表复用已有全景检索 `panorama/search`。浏览器仍走展示入口。那次检索不代替这次 `jobs`，本分册不新定义检索资源，不改它的委托
- 「新出台」的判定口径需规未定义。候选范围与行挂哪些政策由 `POL-L2-DS12-EST-DATA` / `POL-L2-DS12-EST-GAPFILL-L01` 按临时默认定。本分册不替甲方拍板

空态：未选政策，或该政策没有预测行，则该区空。HTTP 成功。不返回 501。不在接口函数里返回写死的短长期效果。

## 5. 234 区域经济发展空间模拟 · jobs · 区域空间

公开资源仍是 `POST /display/v1/policy/simulation/jobs`。浏览器另一次提交，种类为区域空间。

没有区域经济空间模拟模型。热力图、地图在前端渲染。服务端只回行。

链路与第 3 节相同，element 只读同一张预估表里的区域空间行。

- 区域必选。少了区域则空间结果空，不补全国
- 一行挂在一个区域 × 政策类型上：GDP 增长、产业结构变化、就业率变化，加上空间分布数据。区域粒度由 DATA 单定
- 行上 `metric_id` 用已有 `M_POLICY_SIMULATE`
- 政策类型对不上行则空间结果空。不造全国通用行
- 不写 nGQL。不把第 7 项读图写成空间模拟

空态：未选区域，或区域、类型对不上行，则空间结果空。HTTP 成功。不返回 501。不在接口函数里返回写死的 GDP、就业率或地图。

## 6. 235 多维度效果评估 · jobs · 多维评估

公开资源仍是 `POST /display/v1/policy/simulation/jobs`。浏览器另一次提交，种类为多维评估。一次请求不带未出台仿真，也不带利益攸关方。

指标分册记 `metric_id` 未见。按架构，这块读缺项表，不用 501 充当功能。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。

- 同步。不建任务
- 一行是一个维度（经济、社会、环境、创新）的得分与说明。雷达图、柱状图的数就是这些行。字段名归 `POL-L2-DS12-SIM-DATA`
- 只拣多维评估行。同表上的重点、影响范围、路径环节、解读段落留给 SIM 分册的种类，这次不返回
- 行上 `metric_id` 留空。不新造，不借用 `M_POLICY_DEEP_168_1`，不借用 `M_POLICY_SIMULATE` 填评估分
- 灌数由 `POL-L2-DS12-SIM-GAPFILL-L01` 执行。本分册不改这些行的内容
- 查看发生在推演上下文内，或跟随 232–234 的当次结果。上下文怎么装箱由契约单冻结。无行则空，不补四个默认分

空态：没有多维评估行，则雷达和柱状空。HTTP 成功。不返回 501。不在接口函数里返回写死的得分。

## 7. 236 利益攸关方参与评估 · jobs · 利益攸关方

公开资源仍是 `POST /display/v1/policy/simulation/jobs`。浏览器另一次提交，种类为利益攸关方，**必须**带 `policy_id`。

指标未见。同款退路：读缺项表，不用 501 充当这块功能。2026-11-12 COVER-FDE 修订。

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`（该政策下参与意见行 + 评估识别行）。

- 同步。不建任务
- 请求种类是利益攸关方。无 `policy_id` 时 display/element 都不查表，返回空
- 有政策：读 `row_kind IN (参与意见, 评估识别)` 且 `policy_id` 等值。字段名归 `POL-L2-DS12-SIM-DATA`
- 参与意见行：主体、渠道、意见正文、时间。评估识别行：检查项、结论、说明
- 行上 `metric_id` 留空。不新造
- 请求处理不插入、不更新、不删除。页面上新提交的问卷和意见留在浏览器，直到另有采集单。本分册不建那张单
- 「纳入效果评估模型」有意不做。呈现侧汇总只对该政策已灌参与意见行计数
- 灌数由 `POL-L2-DS12-SIM-GAPFILL-L01`（及本 COVER 迁移）执行
- 不把评价页序号 230 的方案意见、序号 210 的受众反馈表 `gapfill_policy_audience_feedback` 当成参与意见

空态：未选政策、或没有该政策下行，则列表/识别空。HTTP 成功。不造一条意见。不返回 501。不在接口函数里返回写死的评论。

## 8. 空态对照

五叶的签收读法都是查缺项表。无行则空。不用 501 充当功能。接口不直接返回写死的 mock。mock 若存在，只能先由灌数单落入表，再被查询读出来。查询不灌数。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 232 | jobs · 未出台仿真 | 五类参数都没选，或参数档对不上行，则该次模拟空。不补默认值，不现算，不造用户模拟历史。不返回 501。失败不清其他种类 |
| 233 | jobs · 新出台预测 | 未选政策，或没有预测行，则该区空。不调解析，不用解析结果顶替。不返回 501 |
| 234 | jobs · 区域空间 | 未选区域，或区域、类型对不上行，则空间结果空。不造全国通用行。不返回 501 |
| 235 | jobs · 多维评估 | 没有多维评估行，则雷达和柱状空。不借用推演键填分。不返回 501 |
| 236 | jobs · 利益攸关方 | 无 `policy_id` 或没有该政策下行，则空。请求不插入。不返回 501 |

架构第 2 节的「真推演」种类在模型未注册时仍是 501。那不是上表五行。五叶在模型注册前照常读缺项表。

## 9. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名和 DTO。交给 `BE-POL-CONTRACT-01`。不写契约仓代码。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。不补推演控制器。
- 不改 `POL-L2-DS12-EST-ARCH`、`POL-L2-DS12-SIM-ARCH`，以及说明书、WBS、契约输入清单、调用链与边界、`指标与501.md`、调研分册和任何兄弟分册。
- 不把整条 `jobs` 改成只读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。
- 237–242 的种类留给 `POL-L2-DS12-SIM-API`。240 不设种类。本分册不改写它们的语义。
- 不加 `policy_simulate`。不把 232–236 写入 `PolicyAnalysisTypes` 或 `JOB_SUB_TYPES`。五叶不进 `POST /internal/policy/jobs/execute`，不进 `gkxlumen-topic-async-service`。
- 不设第二个 dispatcher。浏览器不改打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`、`/v1/policy/**`、`/v1/policy/simulate`。不把 `E-E7-POLICY-M1-L06` 写成展示路径。
- 展示不直连 Python，不直连库，不打算法中台。不调用 `demo-*`。不调用 `polan.text.simulate`。不读 `ads.policy_simulate`。Java 不做 NLP，不写 nGQL。
- 不用 501 充当 232–236 的功能。无行则空。真推演未注册种类的 501 不挂到这五叶。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。不改模型注册表。布局推荐键不顶替推演。
- 235 不读结果表上重点、影响范围、路径环节、解读段落的行。236 不读 `gapfill_policy_audience_feedback`。请求不插入、不更新、不删除意见。查询不灌数。本分册不改 235、236 的行内容。
- 不新建桶，不写对象存储，前端不直连 RustFS。
- 不纳入本分册：237–242、序号 228 的 `evaluation/jobs`、`report/jobs`、`parse/jobs`、`parse/clauses`、`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_INTENSITY_SCORE`、`M_POLICY_TEXT_PARSE` 的单开 URL。
- 不改 `FE-POL-03A`，不新建前端单。前端 mock 开关不是接口实现。
- 不会签。不把本单标 done，不标 ready_to_sign。不改任务状态。
