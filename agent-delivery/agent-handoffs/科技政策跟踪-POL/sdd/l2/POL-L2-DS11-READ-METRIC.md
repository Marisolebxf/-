# POL-L2-DS11-READ-METRIC · 政策分析评价 · 结果解读报告多维展示 · 后台指标设计

- 任务：`POL-L2-DS11-READ-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-05`
- 上游：`sdd/l2/POL-L2-DS11-READ-ARCH.md`（2026-11-03 已签收，本叶以它为准）。本叶会签态 `draft`，不代签，不标 done
- 查询：未见 metric MCP。本叶未调用 `metric-get` / `metric-query`。未读 seed、矩阵 YAML，未改注册表。下文凡未标明出处的身份字段，都不要当成已经查过

本叶只写政策分析评价二级「结果解读报告多维展示」的指标挂接。SRS 序号 **223–226**。

上游只引用，不改写：`sdd/l2/POL-L2-DS11-READ-ARCH.md`、`sdd/指标与501.md` 评价表 223–226 行、`sdd/l2/POL-L2-DS10-SENT-METRIC.md`（篇章样板）。不新注册指标，不改 D4，不写假公式，不改算法代码，不写 OpenAPI。

## 1. 范围

四叶都在政策分析评价里完成。挂接沿 `指标与501.md` 评价表 223–226 行。读面沿已签收的 `POL-L2-DS11-READ-ARCH`。本叶不改那两份文件，也不把调研判定列改写成另一档。

| 序号 | 叶子 | 指标与501 | 本叶 |
|---|---|---|---|
| 223 短板 | 热点问题分析看板 · 短板条数 | 可接统计读面；`M_POLICY_SHORTBOARD_COUNT`；STAT；D4=`mock` | 挂这一条。读 `ads.policy_effect` 里 `scope_type=region_gap` 的 `shortboard_cnt`。源模型 `M_POLICY_DEEP_169_1` 仍是 MODEL，不在同步链上计算。QPOL-02 未闭合。无行则空，不造 0。不改 `gap.run` |
| 223 焦点 | 热点问题分析看板 · 焦点指数 | `M_POLICY_FOCUS_INDEX`；MODEL；D4=`mock`；判定列写 501 | 挂这一条。读 `ads.policy_focus` 且 `policy_id` 非空的 `focus_score`。名称和一句说明用该行 `ext.title`、`ext.explanation`。无行则空。不改 `focus.run` 权重 |
| 224 | 分主题分指标互动解读 | 未见 `metric_id`；判定列 501 | 不新注册。指不到专属 id，条目上的 `metric_id` 留空 |
| 225 | 多媒体辅助解读 | 未见 `metric_id`；判定列 501 | 不新注册。指不到专属 id，条目上的 `metric_id` 留空 |
| 226 | 智能摘要与结论推送 | `M_POLICY_DS_11_POLICY_EVAL_012`；MODEL；D4=`mock`；判定列写 501 | 展示读面挂这一条。读 `ads.policy_text_parse.summary`。行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。写入是规则截取。无行则空。不另写摘要模型 |

223 短板与 226 的 D4 仍是 `mock`。223 焦点的 D4 同样仍是 `mock`。`QPOL-02` 未闭合。`GDF-POLICY-MOCK-GATE-L01` 仍按架构稿视为未解开。本叶不把 mock 写成已上线。

`指标与501` 把 223 焦点、224、225、226 的判定列写成「501，页面空态」。那是调研判定。已签收架构规定这几叶读表：有行则读表，无行则空，不用 501 充当功能。本叶采用这条读面，不回头改 `指标与501`。223 短板的判定列不是 501，是可接统计读面；接上前数值仍是 mock，对齐前没有真批次。`GDF-POLICY-MDC-STAT-L01` 不含短板条数，本叶不把它写成已覆盖本指标。

机遇条数 `M_POLICY_OPPORTUNITY_COUNT` 不挂本二级。

## 2. 本二级用到的已有 metric_id

挂接 3 条，落在 223 短板、223 焦点、226 的展示读面。224、225 不在此表。类型和 D4 只转述 `指标与501.md` 已有行，以及已签收架构稿里写明的同一事实。不是 `metric-get` 的返回。

| metric_id | 中文名 | algorithm_type | D4 | 挂在 |
|---|---|---|---|---|
| `M_POLICY_SHORTBOARD_COUNT` | 未见 metric MCP，不填注册中文名 | STAT | mock | 223 短板 |
| `M_POLICY_FOCUS_INDEX` | 未见 metric MCP，不填注册中文名。看板上的名称用该行 `ext.title` | MODEL | mock | 223 焦点 |
| `M_POLICY_DS_11_POLICY_EVAL_012` | 未见 metric MCP，不填注册中文名。叶子名沿评价表「智能摘要与结论推送」 | MODEL | mock | 226 展示读面 |

这 3 条之外，本二级不新造 `metric_id`。

叶子名与数据行上的名称不是一回事：

- 223 焦点的叶子名是「热点问题分析看板 · 焦点指数」。注册中文名本叶未查。看板上显示的名称和一句说明，用 `ads.policy_focus` 该行 `ext` 里已有的 `title`、`explanation`。这就是架构稿写的、说明书第 11.2 节所说的「焦点问题名称和一句说明」，落在已有表上。本叶不新建指标去顶替这两列，也不另建 `gapfill_policy_eval_focus`。
- 226 的叶子名是「智能摘要与结论推送」。展示读面身份是已有的 `M_POLICY_DS_11_POLICY_EVAL_012`。本叶不另起一条摘要指标。

同一张焦点表上还写着 `M_POLICY_RELATION_DEGREE`。它留在该行的 `relation_degree`，不改挂到 223。见第 7 节。摘要表行上的 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。它不是 226 的第二套摘要。见第 5.3 节。

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

因此本节不列八件套全表。不手抄公式，也不另写一条能算出数的式子。

已签收架构规定的是读哪张表，不是注册源表。读表只说明展示从哪里取数。无行则空。查询函数自己不拼指数、不拼短板数、不拼摘要。

| metric_id | 本叶能写的身份 | 读表（架构稿，不是注册源表） | 本叶不写的 |
|---|---|---|---|
| `M_POLICY_SHORTBOARD_COUNT` | STAT。D4 转述为 mock，不改 | `ads.policy_effect`，`scope_type=region_gap`，列 `shortboard_cnt` | 注册中文名、口径、公式、注册源表、源系统、更新频率、`version` |
| `M_POLICY_FOCUS_INDEX` | MODEL。D4 转述为 mock，不改 | `ads.policy_focus`，`policy_id` 非空，列 `focus_score`；名称 `ext.title`，一句说明 `ext.explanation` | 同上 |
| `M_POLICY_DS_11_POLICY_EVAL_012` | MODEL。D4 转述为 mock，不改。需求来源即序号 226，这句话写在已签收架构稿，不是本叶新挂的 `srs_refs` | `ads.policy_text_parse.summary` | 同上 |

223 短板、223 焦点、226 的展示读数不在接口里重算，也不替换上表未抄的注册公式。

短板以仓库里已有的 `polan.eval.gap.run` 为准，本叶不重写。已签收架构写明：它按区域写入覆盖盲区、失效占比、平均力度不足；`ext` 里已有 `is_mock` 和 `QPOL-02`。本叶不把这三项收成一条可算出 `shortboard_cnt` 的新公式，不改权重。展示 `counts` 这次读取不调用 `gap.run`。中台 `GET /v1/policy/analysis/gap` 读的是同一张表、同一个范围。展示不打那条中台 URL，也不建 `ads.policy_gap`。

焦点以仓库里已有的 `polan.eval.focus.run` 为准，本叶不重写。已签收架构写明：`run()` 只删除 `policy_id` 非空的行再写入，不删除 `policy_id` 为空的机遇行。本叶不改这个删除范围。权重仍是 `QPOL-02` 待甲方确认的规则基线。本叶不改权重，不把 `is_mock` 改成已上线。展示 Job 调用这个已有 `run()`，再读表。不返回 `focus-one` 的当场计算结果。带 items 的既有 `policy_focus` 仍走 harness，不是本看板。

226 的写入以仓库里已有的 `polan.text.parse.run` 为准，本叶不重写。已签收架构写明：写入 `summary` 的是规则截取；该函数会清空整张 `ads.policy_text_parse`；条款结构化写在同一张表上。本叶不把规则截取写成 NLP 已经做到，不另写一套摘要模型，不在展示请求里调用 `parse.run`，也不调用大模型。需规写的是 NLP 生成可编辑摘要。那是需求表述。本叶的可实现读面是查已有列。

`M_POLICY_TEXT_PARSE` 的注册八件套同样未查。本叶只沿架构稿确认：摘要行上的 `metric_id` 仍是这个号。不改它，不把它换成 `M_POLICY_DS_11_POLICY_EVAL_012`，也不用它再定义一套摘要。

## 4. 接入状态

接入状态不是八件套。未见 metric MCP，本叶不写 D1、D2、D3，也不写 `d2_assessed`、`is_mock` 的注册布尔、`d4_note`、`srs_refs`、`lifecycle_stage`。这些字段没有查到，不能补成 `aligned`、`partial`、`full` 或空引用。

D4 只转述已有行，本叶不改：

| metric_id | D4 的出处 | 本叶 |
|---|---|---|
| `M_POLICY_SHORTBOARD_COUNT` | `指标与501` 223 短板行写 `mock`；架构稿写 D4=`mock` | 保持 mock。不升 live |
| `M_POLICY_FOCUS_INDEX` | `指标与501` 223 焦点行写 `mock`；架构稿写 D4=`mock` | 保持 mock。不升 live |
| `M_POLICY_DS_11_POLICY_EVAL_012` | `指标与501` 226 行写 `mock`；架构稿写 D4=`mock` | 保持 mock。不升 live |

224、225 没有专属 `metric_id`。没有可改的 D4。缺项表里灌入的行仍是 mock。本叶不把缺项写成已上线。

`M_POLICY_DEEP_169_1`、`M_POLICY_RELATION_DEGREE`、`M_POLICY_TEXT_PARSE`、`M_POLICY_OPPORTUNITY_COUNT` 的 D1–D4 本叶都未用 metric MCP 核对。除 `指标与501` 已经写在纸面上的类型外，不补维度。短板行写明源模型 `M_POLICY_DEEP_169_1` 仍是 MODEL。226 的行上身份只确认 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`，不在这里给它填一套新的就绪度。

## 5. 223、226 怎么读

读面沿架构稿，不新开路径，不新造指标。

### 5.1 223 短板条数

可接统计读面。挂 `M_POLICY_SHORTBOARD_COUNT`。`指标与501`：STAT，D4=`mock`。

资源是已有的 `GET /display/v1/policy/evaluation/counts`。同步。链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `ads.policy_effect`。`gkxlumen-display` 不直连库。GET 不调用 `gap.run`。

读 `scope_type=region_gap` 的 `shortboard_cnt`。有行则返回这个计数。没有行则该计数空，不造 0，不返回 501。数值在对齐前仍是 mock。

源模型 `M_POLICY_DEEP_169_1` 仍是 MODEL。它不在这条同步链上计算。本叶不把它改挂成短板条数的展示指标，也不改它的类型。

`QPOL-02` 未闭合。`GDF-POLICY-MDC-STAT-L01` 不含本指标。本叶不把该单写成已覆盖，也不新开灌数单。要补批次时只跑已有 `polan.eval.gap.run`，由 `POL-L2-DS11-READ-DATA` 排。本叶不执行灌数。

不做什么：不改 `gap.run` 的公式和权重。不建 `ads.policy_gap`。不把中台页 `/policy/gap` 嵌进展示。

### 5.2 223 焦点指数

挂 `M_POLICY_FOCUS_INDEX`。`指标与501`：MODEL，D4=`mock`，判定列 501。

判定列仍留在 `指标与501` 里，本叶不改。读面按已签收架构：不用 501 充当这块功能。

资源是已有的 `POST /display/v1/policy/evaluation/jobs`，`sub_type=policy_focus_ads`。链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-async-service` → `POST /internal/policy/jobs/execute`。Python 调用已有 `polan.eval.focus.run`，再读 `ads.policy_focus`。

读 `policy_id` 非空的行：`focus_score`，以及 `ext.title`、`ext.explanation`。表里没有行则焦点块空，不返回 501，不返回写死的指数。不返回 `focus-one` 的当场计算结果。`focus-one` 不写 ADS。`GET /v1/policy/analysis/{modelId}` 与 `POST /v1/policy/analysis/focus-one` 留给算法中台。展示不打这两条，也不嵌 `/policy/focus`。

`E-E7-POLICY-M1-L03` 只索引专题侧的焦点、力度、效果。展示不改打 `/topic/v1/policy`，也不等它来实现本叶。`E-E7-POLICY-M1-L06` 不是本二级的实现路径。

切条件不自动起任务。Job 失败不清空已经返回的短板计数和解读条目。

不做什么：不改 `focus.run` 的权重，不改删除范围。不把算法中台的 Top15 图和区间图当成展示接口。不把演示页上的主题卡片写成新指标。不把 harness 的返回当成热点看板。

### 5.3 226 智能摘要与结论推送

展示读面挂 `M_POLICY_DS_11_POLICY_EVAL_012`。`指标与501`：MODEL，D4=`mock`，判定列 501。判定列不改。读面按已签收架构：不用 501 充当这块功能。

这是该列的展示读面身份，不是第二套摘要。算法中台「文本解析 · 智能摘要」已经把这条展示身份定义成读 `ads.policy_text_parse.summary`。本叶沿用，不另写模型。

资源是同一个 `jobs`，`sub_type=policy_text_parse`。Python 只查询 `ads.policy_text_parse`。请求里不调用 `parse.run`。没有行则摘要空，不返回 501，不返回写死的段落。

行上 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。本叶不改这个号。`指标与501` 评价表的引言写明：`M_POLICY_TEXT_PARSE` 的需求来源不在序号 219–231，不进入评价表。本叶不把它改挂进 226，也不把推演页上的解析行搬过来当摘要模型。

写入该列的已有解析是规则截取。本叶不把截取说成 NLP 已经做到。不调用大模型。不另写一套摘要模型。不建 `gapfill_policy_eval_summary`。

可编辑和推送没有登记的用户表，也没有发信通道。本叶不建编辑表，不把改过的句子写回 ADS，不灌假通知，也不为推送新挂指标。用户当时在页面上改字，不构成本条资源。

不做什么：不把序号 242 的推演解读报告、核增研报 `report/jobs` 当成这条摘要。不把 `focus-one` 当成摘要。不把对比页的结果智能输出改挂到这个号。

### 5.4 同一行上不改挂的号

焦点行上的 `metric_id` 仍是已有的 `M_POLICY_FOCUS_INDEX/M_POLICY_RELATION_DEGREE`。本叶只把前者挂到 223 焦点。后者见第 7 节。

摘要行上的 `metric_id` 仍是 `M_POLICY_TEXT_PARSE`。展示挂接用 `M_POLICY_DS_11_POLICY_EVAL_012`。两个号不是两套摘要。

## 6. 224、225 没有专属 metric_id

224、225 在 `指标与501` 里 `metric_id` 为未见，判定列 501。225 的调研记交互壳，详设并入 501，不升第四档。本叶不新注册，不改判定列。

真实的分主题解读生成、真实的视频和动画嵌入，本叶都做不到。已签收架构的退路是缺项表：库 `gkxlumenx_gapfill`，表 `gapfill_policy_eval_shell`。由下游把 mock 行写入表，接口只查询。本叶不执行灌数，不写字段级 DDL。查询请求不灌数。

条目可以指向已经存在的 `metric_id`。本叶指不到专属 id，因此不指定任何一条。shell 行上的 `metric_id` 留空。不把 223 的 `M_POLICY_SHORTBOARD_COUNT`、`M_POLICY_FOCUS_INDEX` 指进 224 或 225。不把 226 的 `M_POLICY_DS_11_POLICY_EVAL_012` 或行上的 `M_POLICY_TEXT_PARSE` 指进去。

`POL-L2-DS11-READ-GAPFILL-L01` 只灌解读条目和多媒体条目。没有已挂指标的，`metric_id` 留空。`fill_method` 用 `manual`。`gap_item` 写序号和叶子名。本叶不认领、不执行该单。

### 6.1 224 分主题分指标互动解读

没有已挂 `metric_id`。也没有已注册的解读模型。

读面是 `GET /display/v1/policy/evaluation/shells`。`gkxlumen-element` 只读 `gapfill_policy_eval_shell` 里的解读条目：专题或指标名、一句结论、一句应用建议。点选只筛选已经返回的行，不另起计算，不新开路径。表里没有行则解读块空。不在接口里写死结论。

不把 226 的摘要行复制成解读条目。不把 223 的焦点说明改挂到本序号。

### 6.2 225 多媒体辅助解读

没有已挂 `metric_id`。没有视频通道，没有可调用模型。

同一张 `gapfill_policy_eval_shell`，只读多媒体条目：标题、一句说明。不灌视频、动画或图形文件，不写对象存储，前端不直连 RustFS。页上已有的短板计数和焦点结果留在原来的 `counts` 和 `jobs` 上。本序号不新做一套图。表里没有行则该块空。

不把序号 219–221 的趋势图、分区图、结构关联收进本叶。不把前端占位动画写成多媒体服务。

## 7. 点名不挂

下列号或序号在已签收架构、或 `指标与501` 评价表里已经出现。本二级不把它们改挂到 223–226，也不改它们的 D4。身份未经过 metric MCP。下表只写本叶能从这两份已有文字里确认的内容。

| 号或序号 | 已有文字里能确认的 | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_OPPORTUNITY_COUNT` | `指标与501` 页 KPI 行：STAT，D4=`mock`，可接统计读面。源模型 `M_POLICY_DEEP_170_1` 仍是 MODEL。QPOL-02 未闭合 | 没有 223–226 的序号。`counts` 上的机遇读面留给页 KPI。本叶不改 |
| `M_POLICY_RELATION_DEGREE` | 架构稿：写在焦点行的 `relation_degree` 上。223 的两行都没有把它列为 `metric_id` | 留在同一行。不改挂到 223。不为此读图。Java 不写 nGQL |
| `M_POLICY_DEEP_169_1` | `指标与501` 短板行：仍是 MODEL | 短板的源模型。不在 `counts` 同步链上计算。不改挂成展示指标 |
| `M_POLICY_TEXT_PARSE` | 架构稿：摘要行上的 `metric_id` 仍是它。评价表引言：需求来源不在 219–231，不进入评价表 | 不改这个号。不把它当成 226 的第二套摘要，也不新挂进 223–225 |
| `M_POLICY_EFFECT_SCORE` | 架构稿：在 `jobs` 上，不是 223–226。`指标与501` 页 KPI 行另有该号，判定 501 | 页上效能。本叶不挂 |
| `M_POLICY_DS_11_POLICY_EVAL_015` | `指标与501` 229 行有该号。架构稿：不挂本叶 | 实施路径与风险。序号 229，不在 223–226 |
| 219–221 | 趋势、分区、结构关联 | 不收进本叶。221 不挂 `M_POLICY_RELATION_DEGREE` |
| 222 | 报告模板与批量导出。交互壳 | 模板选用不写入本叶的解读条目 |
| 227–231 | 方案、参数模拟、实施路径、意见与归档 | 不写入本叶 |
| `policy_focus` 的 harness 路径 | 带 items 的既有焦点作业 | 展示看板走 `policy_focus_ads` |
| `compare/jobs`、`report/jobs`、`simulation/jobs` | 核增对比、研报、推演 | 不是本四叶 |

`M_POLICY_RELATION_DEGREE`、`M_POLICY_DEEP_169_1`、`M_POLICY_TEXT_PARSE`、`M_POLICY_OPPORTUNITY_COUNT` 的 D1–D3 未查。本叶只核对「不改挂」，不展开它们的计算。

## 8. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不手抄注册公式，不把 `gap.run`、`focus.run`、`parse.run` 收成可算出数的新公式，不改这三处权重或删除范围。
- 不把规则截取写成 NLP 已经做到。不另写一套摘要模型。
- 不把 `M_POLICY_RELATION_DEGREE` 改挂到 223。不把 `M_POLICY_OPPORTUNITY_COUNT` 挂进本二级。不把 `M_POLICY_DEEP_169_1` 放进同步链上计算。
- 不给 224、225 补 `metric_id`。指不到就留空。不把 223、226 的号指进这两叶。
- 不把 `M_POLICY_TEXT_PARSE` 改成 `M_POLICY_DS_11_POLICY_EVAL_012`，也不反过来。
- 不改算法代码，不改 demo 仓与 vendor 里的 `gap.py`、`focus.py`、`parse.py`。
- 不改 `指标与501.md`、`POL-L2-DS11-READ-ARCH.md`、说明书、VIZ、PLAN、WBS、指标 seed 与矩阵。
- 不写 OpenAPI 字段、请求体、响应体、枚举。
- 不见 metric MCP 就不填中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3、`srs_refs`。
- 不会签。不把本单标 done，也不标 `ready_to_sign`。
