# POL-L2-DS12-EST-METRIC · 政策效果推演 · 效果预估 · 后台指标设计

- 任务：`POL-L2-DS12-EST-METRIC`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-06`
- 上游：`sdd/l2/POL-L2-DS12-EST-ARCH.md`（任务 `POL-L2-DS12-EST-ARCH` 于 2026-11-05 为 `integration`，定义单会签中。稿内写明待四角色会签，不标 done。本叶以工作区当前稿为准，不代签）
- 查询回退：动态工具目录中无 metric 命名空间，无 `metric-get` / `metric-query`。本叶未调用 metric MCP。身份改读 `sdd/指标与501.md` §3（推演键与 232–236 行）以及说明书第 2 节 DS-12 这五行的已有 `metric_id` 与三档。未读 seed、矩阵 YAML，未改指标注册表，未改 `cfg_model_registry.yaml`。下文凡未标明出处的身份字段，都不要当成已经查过

本叶只写政策效果推演二级「效果预估」的指标挂接。SRS 序号 **232–236**。

上游只引用，不改写：`sdd/l2/POL-L2-DS12-EST-ARCH.md`、`sdd/指标与501.md` §3、说明书第 2 节 DS-12 这五行、`sdd/l2/POL-L2-DS11-PLAN-METRIC.md`（篇章样板）。不新注册指标，不改 D4，不写假公式，不改算法代码，不调用 `polan.text.simulate.run`，不写 OpenAPI，不写 DDL。

与架构稿的差异：无。读表、行上 `metric_id`、D4=`mock`、501 判定、布局推荐不挂，都沿该稿。

## 1. 范围

五叶都在政策效果推演的效果预估里完成。挂接沿说明书第 2 节 DS-12 已有 `metric_id` 与三档，以及 `指标与501.md` §3.1 分键和 §3.2 的 232–236 行。读面沿当前 `POL-L2-DS12-EST-ARCH`。本叶不改那三份文件，也不把调研判定列改写成另一档。

说明书第 2 节三档只有：可接统计读面、501、跨项索引。推演页可接统计读面为 0。232、233、234 的拆解是 501，并带已有 `M_POLICY_SIMULATE`。235、236 的拆解是 501，没有专属 `metric_id`。这五叶都不是可接统计读面，也都不是跨项索引。本叶不改这三档，不把 501 改写成可接统计。

| 序号 | 叶子 | 指标与501 / 说明书第 2 节 | 本叶 |
|---|---|---|---|
| 232 | 未出台政策仿真模拟 | `M_POLICY_SIMULATE`；MODEL；D4=`mock`；判定 501。真路径：501，页面空态。无 STAT/COMPUTE 可挂 | 沿用这一条。D4 仍是 mock。未出台仿真行上的 `metric_id` 用这个已有号。读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 的未出台仿真行。参数档对不上则该次模拟空 |
| 233 | 新出台政策效果预测 | 同上，与 232 共用同一推演模型，没有独立指标 | 沿用同一条。D4 仍是 mock。新出台预测行上的 `metric_id` 用这个已有号。读同一张缺项表的新出台预测行。不调 `parse/jobs`。无行则该区空 |
| 234 | 区域经济发展空间模拟 | 同上。空间模拟没有独立指标 | 沿用同一条。D4 仍是 mock。区域空间行上的 `metric_id` 用这个已有号。读同一张缺项表的区域空间行。区域或类型对不上则空间结果空 |
| 235 | 多维度效果评估 | 未见 `metric_id`；判定 501。真路径：不借用 `M_POLICY_DEEP_168_1` | 不新注册。不挂 `M_POLICY_SIMULATE`。不借用 `M_POLICY_DEEP_168_1`。多维评估行上的 `metric_id` 留空。读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。无行则雷达/柱状空 |
| 236 | 利益攸关方参与评估 | 未见 `metric_id`；判定 501。真路径：关键词「利益」为 0 条 | 不新注册。不挂 `M_POLICY_SIMULATE`。参与意见行上的 `metric_id` 留空。读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。请求不插入。无行则意见列表空 |

232–234 的 D4 仍是 `mock`。235、236 没有专属 `metric_id`，没有可改的 D4。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿与 `指标与501` 视为未解开。本叶不把 mock 写成已上线。

`指标与501` 把 232–236 的判定列都写成「501，页面空态」。那是调研判定。当前架构稿规定这五叶读缺项表：有行则读表，无行则空，不用 501 充当功能。真模型未注册时，真推演种类仍是 501 空态；缺项行是说明书第 11 节允许的退路，两者并存。本叶采用这条读面，不回头改 `指标与501`，也不把判定列从 501 改成可接统计读面或跨项索引。

`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT` 是布局推荐键，不进入本二级。`M_POLICY_LAYOUT_REC_COUNT` 的类型是 STAT，只说明它是计数，不能当作推演页的统计读面，也不能把推演页的可接统计读面从 0 改成 1。

## 2. 本二级用到的已有 metric_id

挂接 1 条，只落在 232、233、234。235、236 不在此表。类型和 D4 只转述 `指标与501.md` 已有行，以及当前架构稿里写明的同一事实。不是 `metric-get` 的返回。

| metric_id | 中文名 | algorithm_type | D4 | 挂在 |
|---|---|---|---|---|
| `M_POLICY_SIMULATE` | 未见 metric MCP，不填注册中文名。三叶叶子名沿推演表「未出台政策仿真模拟」「新出台政策效果预测」「区域经济发展空间模拟」 | MODEL | mock | 232、233、234 |

这一条之外，本二级不新造 `metric_id`。

叶子名与数据行上的号不是一回事：

- 232、233、234 各有叶子名，展示读面身份是同一条已有的 `M_POLICY_SIMULATE`。本叶不另起三条推演指标。
- 235、236 的行上 `metric_id` 留空。不把 `M_POLICY_SIMULATE` 填进多维评估分或参与意见。
- 模型注册表 `vendor/entan-py/conf/cfg_model_registry.yaml` 的 `POLICY_SIMULATE` 把 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015` 列在同一 `metric_ids` 下，`handler_module` 是 `polan.text.simulate`，`ads_table` 是 `ads.policy_simulate`。本叶不改这份注册表。函数本身不产出 015，也不产出未出台四类参数、新出台预测或区域空间行，见第 3 节。232–234 因此不去读 `ads.policy_simulate`。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进八件套。

未见 metric MCP，已改读 `指标与501.md`。该文件的 232–234 行只给出 `metric_id`、`algorithm_type`、D4 与判定，没有注册中文名、口径、公式、注册源表、源系统、更新频率、`version`。本叶不把未查到的字段写成已查到。下列各项保持注册表原样，本叶不改、不抄、不补：

- 注册中文名
- 口径（`definition`）
- 注册公式
- 注册源表
- 源系统
- 更新频率
- `version`

因此本节不列八件套全表。不手抄公式，也不另写一条能算出经济效益、社会影响、创新促进、短长期效果、GDP、产业结构、就业率、维度得分或意见汇总的式子。

`指标与501` 232 行真路径列的原句是「无 STAT/COMPUTE 可挂」。233 行写「与 232 共用同一推演模型，没有独立指标」。234 行写「空间模拟没有独立指标」。这是判定说明，不是本叶查到的注册 `definition`。需求来源即序号 232–234，这句话写在说明书第 2 节与 `指标与501` 的对应行，不是本叶新挂的 `srs_refs`。

当前架构稿规定的是读哪张表，不是注册源表。读表只说明展示从哪里取数。无行则空。查询函数自己不生成预测，不套弹性，不拼曲线。

| metric_id | 本叶能写的身份 | 读表（架构稿，不是注册源表） | 本叶不写的 |
|---|---|---|---|
| `M_POLICY_SIMULATE` | MODEL。D4 转述为 mock，不改 | `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。232 未出台仿真行、233 新出台预测行、234 区域空间行。三行上的 `metric_id` 都用这个已有号 | 注册中文名、口径、公式、注册源表、源系统、更新频率、`version` |

232–234 的展示读数不在接口里重算，也不替换上表未抄的注册公式。类型仍是 MODEL。本叶不把它改成 STAT 或 COMPUTE，也不因此把推演页写成可接统计读面。

核对了 `lumen-algo-py` 的 `vendor/entan-py/polan/text/simulate.py`。`run()` 写入 `ads.policy_simulate`。每一行的 `metric_id` 固定为字面量 `M_POLICY_SIMULATE`。函数写的是已出台政策的省级力度情景，不收需规四类参数（政策类型、覆盖范围、支持力度、实施时间），不写新出台短长期效果，不写区域 GDP、产业结构、就业率，不写 235 的维度得分，不写 236 的意见，插入行里也没有 `M_POLICY_DS_11_POLICY_EVAL_015`。

本叶不把这套情景弹性收成 232、233 或 234 的公式，不在展示请求里调用 `run()`，也不把 `ads.policy_simulate` 当成这三叶的读表。模型注册表把 015 列在 `POLICY_SIMULATE` 下，只说明登记时并列表了两个号。函数不产出路径，也不产出本二级的预估行。本叶不改注册表来拆这两个号，也不调用这次 `run()` 去补 232–234。

## 4. 接入状态

接入状态不是八件套。未见 metric MCP，本叶不写 D1、D2、D3，也不写 `d2_assessed`、`is_mock` 的注册布尔、`d4_note`、`srs_refs`、`lifecycle_stage`。这些字段没有查到，不能补成 `aligned`、`partial`、`full` 或空引用。

D4 只转述已有行，本叶不改：

| metric_id | D4 的出处 | 本叶 |
|---|---|---|
| `M_POLICY_SIMULATE` | `指标与501` §3.1 与 232–234 行写 `mock`；架构稿写 D4=`mock` | 保持 mock。不升 live |

235、236 没有专属 `metric_id`。没有可改的 D4。缺项表里灌入的行仍是 mock。本叶不把缺项写成已上线。

`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT`、`M_POLICY_DS_11_POLICY_EVAL_015`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_TEXT_PARSE`、`M_POLICY_DEEP_168_1` 的 D1–D4 本叶都未用 metric MCP 核对。除 `指标与501` 已经写在纸面上的类型外，不补维度。布局推荐键上 `M_POLICY_DEEP_171_1` 的纸面类型是 MODEL、D4=`mock`、判定跨项索引；`M_POLICY_LAYOUT_REC_COUNT` 的纸面类型是 STAT、D4=`mock`、判定跨项索引。这两条都不在 232–236。本叶不改它们的 D4，也不把它们改挂进本二级。

## 5. 232、233、234 怎么读

挂 `M_POLICY_SIMULATE`。`指标与501`：MODEL，D4=`mock`，判定列 501。说明书第 2 节同一三行：501，并带这个已有号。三叶共用这一条，没有第二条、第三条推演指标。

判定列仍留在 `指标与501` 里，本叶不改。读面按当前架构稿：不用 501 充当这块功能，也不把判定列升成可接统计读面或跨项索引。模型未以可调用服务注册。Java `PolicyAnalysisTypes` 与 Python `JOB_SUB_TYPES` 无 `policy_simulate` 子类型这一事实沿架构稿 §1.3，本叶不改白名单。真推演种类因此仍是 501 空态。缺项表种类照常可读。

没有未出台政策仿真模型，没有新出台预测模型，没有区域经济空间模拟模型。`simulate.run` 写的是省级力度情景，指标号虽是这一条，维度对不上这三叶。本叶不调用它。

资源是已有的 `POST /display/v1/policy/simulation/jobs`。链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。`gkxlumen-display` 不直连库，不直连 Python。一次只带一种类。无行则该区空，不返回 501 文案充当结果，不返回写死的预测，也不返回中台曲线来顶替。

行上的 `metric_id` 用已有 `M_POLICY_SIMULATE`。不新注册，不改 D4，不把读到的行写成已上线。列定义归 `POL-L2-DS12-EST-DATA`。本叶不写 DDL。灌数由 `POL-L2-DS12-EST-GAPFILL-L01` 执行，本叶不认领、不执行。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。查询请求不灌数。

切条件不自动起任务，也不现算。某一次 `jobs` 失败，不清其他种类已经返回的区块。本页没有可接统计读面，没有会被异步失败清掉的同步统计卡。

不做什么：不改 `cfg_model_registry.yaml`。不把 `POLICY_SIMULATE` 的并列表当成 232–234 已经能由 `run()` 写出需规预估。不读 `ads.policy_simulate`。不把省级力度曲线写成未出台仿真、新出台预测或区域空间结果。

### 5.1 232 未出台政策仿真模拟

没有未出台政策仿真模型。中台情景不收四类参数。

读面是 `jobs`，种类为未出台仿真。element 只读缺项表里的未出台仿真行。一行是一组参数档：政策类型、覆盖范围、支持力度、实施时间，以及经济效益、社会影响、创新促进的预测值和一句说明。四类至少一类；参数档对不上行则该次模拟空，不补默认值。多方案比较由前端并排，或一次读多行。服务端不建对比槽，不存用户模拟历史。

行上 `metric_id` 用 `M_POLICY_SIMULATE`。Java 不按弹性现算。

### 5.2 233 新出台政策效果预测

没有新出台政策预测模型。需规写「基于政策文本解析和历史相似政策效果数据」。调用链不给推演单开 `M_POLICY_TEXT_PARSE` 通道。

读面是同一个 `jobs`，种类为新出台预测。element 按一条已出台政策拣同一张缺项表的行：短期与长期效果、经济增长、产业发展、科技创新影响、时间变化、空间分布说明、相似政策依据说明。依据写在行内。字段名归 DATA 分册。无行则该区空，不返回解析结果顶替。

不调 `parse/jobs`，不调 `policy_text_parse`。候选政策列表复用全景检索目录，不新建政策列表读面。「新出台」的判定口径需规未定义，本叶不拍板，留给 `POL-L2-DS12-EST-DATA` / `POL-L2-DS12-EST-GAPFILL-L01` 的临时默认。

行上 `metric_id` 用 `M_POLICY_SIMULATE`。

### 5.3 234 区域经济发展空间模拟

没有区域经济空间模拟模型。热力图和地图在前端渲染，服务端只回行。

读面是同一个 `jobs`，种类为区域空间。element 按区域 × 政策类型拣同一张缺项表的行：GDP 增长、产业结构变化、就业率变化，以及空间分布数据。区域必选。区域或类型对不上行则空间结果空，不造全国通用行。区域粒度归 DATA 分册。

行上 `metric_id` 用 `M_POLICY_SIMULATE`。

## 6. 235、236 没有专属 metric_id

235、236 在 `指标与501` 里 `metric_id` 为未见，判定列 501。说明书第 2 节这两行只有 501，没有 `metric_id`。本叶不新注册，不改判定列，不改 D4。

真实的多维评分模型、真实的意见采集、真实的「汇总各方意见并纳入效果评估模型」，本叶都做不到。当前架构稿的退路是缺项表：库 `gkxlumenx_gapfill`。235 读 `gapfill_policy_sim_result`，236 读 `gapfill_policy_sim_stakeholder`。表归属沿架构稿 §0，与说明书 11.2 的 SIM 组两表同名；本叶不改说明书的分组写法。由下游把 mock 行写入表，接口只查询。本叶不执行灌数，不写字段级 DDL。查询请求不灌数。

这两叶指不到专属 id。行上的 `metric_id` 留空。不把 232–234 的 `M_POLICY_SIMULATE` 指进 235、236。不把 `M_POLICY_DEEP_168_1` 指进 235。不把 `M_POLICY_LAYOUT_REC_COUNT` 或 `M_POLICY_DEEP_171_1` 指进这两叶。

`POL-L2-DS12-SIM-GAPFILL-L01` 灌多维评估行和参与意见行。没有已挂指标的，`metric_id` 留空。本叶不认领、不执行该单。字段级 DDL 由 `POL-L2-DS12-SIM-DATA` 定。

### 6.1 235 多维度效果评估

没有已挂 `metric_id`。也没有多维评分模型。

不挂 `M_POLICY_SIMULATE`。推演键只挂 232–234 的预测行，不拿它填评估分。不借用 `M_POLICY_DEEP_168_1`。

读面是 `POST /display/v1/policy/simulation/jobs`，种类为多维评估。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行：经济、社会、环境、创新各维的得分与说明。雷达图、柱状图的数就是这些行。无行则空，不造得分，不在接口里写死分数。

行上 `metric_id` 留空。

### 6.2 236 利益攸关方参与评估

没有已挂 `metric_id`。调研关键词「利益」为 0 条。没有意见采集服务。

判定仍是 501。当前架构稿规定同样读缺项表，不用 501 充当这块功能。本叶采用这条读面，不改判定列，也不把「利益」0 条改写成一条可接统计。

读面是同一个 `jobs`，种类为利益攸关方。element 只读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行：主体（决策者、评估者、利益攸关方）、渠道（在线问卷、意见征集、专家评审）、意见正文、时间。请求处理不插入、不更新、不删除。用户在页面新提交的意见留在浏览器，直到另有采集单。本叶不建那张单。无行则列表空，不造一条意见。

「汇总各方意见并纳入效果评估模型」在模型接通前不实现。呈现侧的汇总只对已灌行计数。这个计数不是新指标，不新注册，不改挂成可接统计读面。

行上 `metric_id` 留空。

## 7. 点名不挂

下列号或序号在当前架构稿、或 `指标与501` 里已经出现。本二级不把它们改挂到 232–236，也不改它们的 D4。身份未经过 metric MCP。下表只写本叶能从这两份已有文字和 `simulate.py`、模型注册表里确认的内容。

| 号或序号 | 已有文字或代码里能确认的 | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_DEEP_171_1` | `指标与501` §3.1：布局推荐键，MODEL，D4=`mock`，跨项索引。不能当作推演结果。架构稿：不进推演页任何区 | 232–236 都不挂。布局推荐留在布局推荐键 |
| `M_POLICY_LAYOUT_REC_COUNT` | `指标与501` §3.1：布局推荐键，STAT，D4=`mock`，跨项索引。口径是建议条数。类型为 STAT 不能当作推演页的统计读面。需规引用写过展示序号 241，该引用不改变分键。`FE-POL-03A` 页头「布局建议」卡槽是复刻壳 | 232–236 都不挂。不把推演页可接统计读面从 0 改掉 |
| `M_POLICY_SIMULATE` 改挂到 235、236 | 说明书与 `指标与501`：232–234 才带这个号。235、236 为未见。架构稿 §5.4、§5.5：推演键只挂 232–234 的预测行 | 235、236 行上留空。不拿它填评估分或意见 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | 模型注册表与 `M_POLICY_SIMULATE` 并列表。`simulate.run` 不写这个号。`指标与501` 229 行才挂它。241 行写明它不顶替 241 | 不写进 232–234 的预估行。本叶不改 229、不改 241 |
| `M_POLICY_DEEP_168_1` | `指标与501` 235 行写明不借用。评价页 211 行也不挂它 | 235 不挂 |
| `M_POLICY_EFFECT_SCORE` | `指标与501` 评价页 KPI：MODEL，D4=`mock`，判定 501。展示侧需求来源写过 232/233，并写明推演能力不在评价页展开。架构稿：效能得分留评价页 | 232、233 不改挂这条。效能得分留评价页 |
| `M_POLICY_INTENSITY_SCORE` | 架构稿：力度分留全景 | 不挂预估行 |
| `M_POLICY_TEXT_PARSE` | `指标与501` 237 行。架构稿：233 不调 `parse/jobs` | 233 不调，不把解析结果顶替预测行。237 不在本叶 |
| `M_POLICY_RELATION_DEGREE` | `指标与501` 240 行，跨项索引 | 240 不在本叶。本二级不设读图资源 |
| `ads.policy_simulate` | `simulate.run` 的写入表。模型注册表 `POLICY_SIMULATE.ext.ads_table` | 232–234 都不读。继续只服务算法中台读面 |
| 237–242 | 仿真二级。241 未见 `metric_id`，判定 501。布局建议条数与 015 都不顶替 241 | 本叶不实现、不改挂 |
| `evaluation/jobs` 序号 228 | `指标与501` 228 行写明不挂 `M_POLICY_SIMULATE`，不写推演页 | 不把本页参数档写成评价方案 |
| `report/jobs` | 核增研报 | 242 不是本单 |
| `POLICY_SIMULATE` 注册项 | `metric_ids` 同时列出 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015`。函数只写前者，且写入省级力度情景 | 本叶不改这份注册表，也不据此让 232–234 去读推演表 |

`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT` 的 D1–D3 未查。本叶只核对「不改挂」，不展开它们的计算。

## 8. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不给 235、236 补 `metric_id`。指不到就留空。不把 `M_POLICY_SIMULATE` 指进这两叶。
- 不把 `M_POLICY_LAYOUT_REC_COUNT` 或 `M_POLICY_DEEP_171_1` 挂到 232–236。不把 STAT 类型写成推演页的可接统计读面。
- 不把 501 改写成可接统计读面或跨项索引。真推演未注册仍是 501。缺项读面不用 501 充当功能。
- 不手抄注册公式，不把 `simulate.run` 的情景弹性收成 232、233、234 可算出数的新公式。
- 不调用 `polan.text.simulate.run`。不改 `simulate.py`。不改 `cfg_model_registry.yaml`。不读 `ads.policy_simulate`。
- 不改 `指标与501.md`、`POL-L2-DS12-EST-ARCH.md`、说明书、调研分册、WBS、指标 seed 与矩阵。
- 不写 OpenAPI 字段、请求体、响应体、枚举、参数档名。
- 不写 DDL。不写 `gapfill_policy_sim_forecast`、`gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` 的列定义。
- 不见 metric MCP 就不填中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3、`srs_refs`。回退只使用 `指标与501` 与说明书第 2 节已经写出的号、类型、D4 和三档。
- 不会签。不把本单标 done，也不标 `ready_to_sign`。
