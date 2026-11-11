# POL-L2-DS10-CMP-API · 科创政策全景 · 政策重点比对 · 后台接口设计

- 任务：`POL-L2-DS10-CMP-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-04`
- 上游：`sdd/l2/POL-L2-DS10-CMP-ARCH.md`（2026-11-03 `human:淮政玮` 已签收，含当日会签修订。本分册以它为准，不改它）

本分册只定科创政策全景二级「政策重点比对」的后台接口。SRS 序号 **213–218**。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、内部委托、同步或 Job、空态。不写 OpenAPI 字段表，不写实现代码。

流程以 `POL-L2-DS10-CMP-ARCH` 为准，包括 2026-11-03 会签修订：缺项表同步读走 `gkxlumen-element`；214 的力度分与 218 的可视化走 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`；216 的支持力度走 `GET panorama/stats` 同步读，不进 Job。契约输入清单里全景的 `stats`、`search`、`{id}/detail`、`jobs`、`version-diff`、`benchmark-report` 只作资源名对照。清单里「未见」和旧空态不覆盖本分册。

签收口径：做不到的只允许缺项表灌 mock 后由接口读表。216 读已有 `ads.policy_intensity`，不另建表。不允许接口直接返回写死的差异、分数或 PDF，也不用 501 充当这六叶的功能。

## 偏离

本二级 DoD 里「不复用 `/topic/v1/policy`」指浏览器不改打专题 URL。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy`，以及 214、218 内部调用 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`，都算内部委托。浏览器仍只打 `/display/v1/policy/**`。对外不把 `/topic/v1/policy`、`/v1/policy` 或 `/topicAsync/**` 写成入口。不改 `ARCH-DISPLAY-01`。`E-E7-POLICY-M1-L06` 不是展示联调单，也不是本二级的实现路径。

## 1. 公开资源

前缀 `/display/v1/policy/`。六叶都在全景比对工作区里完成，不另开页，不另开路径。本分册不新开资源。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 213 | `GET /display/v1/policy/panorama/version-diff` | 同步。element 只读 `gapfill_policy_version_diff`。时点用已有发布时间。无行则空 |
| 214 正文 | `GET /display/v1/policy/panorama/search` 与 `GET /display/v1/policy/panorama/{id}/detail` | 同步。正文委托 topic-policy。受理部门读正文 |
| 214 条件、材料、优缺点 | 同一条 `GET /display/v1/policy/panorama/{id}/detail` | 同步。同一次详情。element 只读 `gapfill_policy_detail_compare`（含 `pros_text`/`cons_text`） |
| 214 力度分 | `POST /display/v1/policy/panorama/jobs` | Job。`sub_type=policy_intensity`。display 只提交 `analysis/tasks` |
| 215 区域、类别、总件数 | `GET /display/v1/policy/panorama/stats` | 同步。区域和类别委托 topic-policy。总件数仍是 `M_POLICY_TOTAL_COUNT` |
| 215 实施部门 | 同一条 `GET /display/v1/policy/panorama/stats` | 同步。element 只读 `gapfill_policy_impl_dept` |
| 216 | 同一条 `GET /display/v1/policy/panorama/stats` | 同步。element 只读 `ads.policy_intensity` 上的 `M_POLICY_SUPPORT_STRENGTH`；「政策类型」列同一次统计由 element 只读 DWD `policy_base_info` 文种按省聚合（2026-11-11 增补，QPOL-01 临时默认）。不进 Job |
| 217 | `GET /display/v1/policy/panorama/benchmark-report` | 同步。element 只读 `gapfill_policy_benchmark_report`。不内嵌写死的 PDF。浏览器从当次行用 `trackingExport` 导出 Word/PDF |
| 218 | 同一条 `POST /display/v1/policy/panorama/jobs` | Job。`sub_type=policy_intensity`。无行则图空 |

`{id}` 是 `search` 目录项里的政策 id，与 `POL-L2-DS10-QRY-API` 相同。

`panorama/stats`、`search`、`{id}/detail`、`jobs` 在契约输入清单里还挂着其它叶子。本分册只定上表这些读法。197–212 已写的委托不在这里重列，也不改写成 213–218。`jobs` 在本分册只覆盖 214 的力度分和 218 的可视化。

用户要提交的选择沿架构第 3 节的闭集。少了必选选择时，该对比空，不补一套默认对象。参数名留给 `BE-POL-CONTRACT-01`。

## 2. 内部委托

浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。

展示不直连 Python，不直连库，不写算法，不打分，不写 nGQL。不打算法中台 `/v1/policy/**`。不调用任何 `demo-*` 服务。

| 公开资源 | 内部委托 |
|---|---|
| `panorama/version-diff` | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_version_diff` |
| `panorama/search` | `gkxlumen-display` → `gkxlumen-topic-policy`：`GET /topic/v1/policy/search`。正文委托这一条 |
| `panorama/{id}/detail` | `gkxlumen-display` → `gkxlumen-topic-policy`：`GET /topic/v1/policy/docs/{id}`。申报条件、申报材料、优点、缺点由 `gkxlumen-element` 在同一次详情只读 `gapfill_policy_detail_compare`。受理部门只取正文 |
| `panorama/stats` | 区域、类别、总件数委托 `gkxlumen-topic-policy`（已有地区分布、已有选项、`M_POLICY_TOTAL_COUNT`）。实施部门由 `gkxlumen-element` 只读 `gapfill_policy_impl_dept`。`M_POLICY_SUPPORT_STRENGTH` 由 `gkxlumen-element` 同步只读 `ads.policy_intensity`。勾「政策类型」时同一次统计由 element 只读 `dwd.policy_base_info` 文种按省聚合（2026-11-11 增补） |
| `panorama/jobs` | `gkxlumen-display` 只提交 `gkxlumen-topic-async-service` 的 `POST /topic/v1/analysis/tasks`。已有 `PolicyAnalysisAdapterImpl` 再调 `POST /internal/policy/jobs/execute`，`sub_type=policy_intensity`。display 不直接打 `jobs/execute` |
| `panorama/benchmark-report` | `gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_benchmark_report` |

214 的正文、215 的区域和类别不进 `gkxlumen-element` 的缺项表。213、214 的条件与材料、215 的实施部门、217 不进专题政策查询门面。216 的这次统计不调用 `intensity.run()`，也不进异步任务管道。214 与 218 的任务表、SSE、并发锁复用 `gkxlumen-topic-async-service`。`/internal/policy/jobs/execute` 的下游是已有 Python `/internal/policy`。算法中台页面留在 `demo-ui-system-test`，展示不嵌力度页。

`policy_intensity` 尚未放进这条执行入口的白名单。未挂上时，这次 Job 的力度结果为空，不返回演示分。本分册不改白名单代码。

切筛选不自动起任务。用户提交 `jobs` 之后才建 214、218 的任务。216 不建任务。某一块读失败，不清空已经返回的目录和正文。Job 失败同样不清空已经返回的 `stats`、`search` 和 `{id}/detail`。

trace 沿既有展示链。同步读在 display 往下带 traceId。Job 沿已有异步任务链。本分册不新设计观测点。

## 3. 213 政策新旧对比 · version-diff

公开资源：`GET /display/v1/policy/panorama/version-diff`。同步。

一条政策，两个时点。时点由 `GET /display/v1/policy/panorama/versions` 给出（参数 `policy_id` 可空、`limit` 默认 50 硬顶 200）：`gkxlumen-element` 读 DWD `policy_base_info` 上新版与 `-H1` 历史版成对的行，返回 `policy_id`、`title`、`publish_date`、`history_policy_id`、`history_title`、`history_publish_date`。不另编版本号，不接受任意日期，也不从缺项表反查可选时点。没有历史版的政策不出现在列表里，对比空。（2026-11-07 由「同一正文的发布时间」改为成对行，见 `POL-L2-DS10-CMP-DATA` 第 3 节。）

`gkxlumen-element` 按这条政策和两个发布时间只读 `gkxlumenx_gapfill.gapfill_policy_version_diff`。一行是同一政策的一个变更：两个发布时间、变更类型（新增、修改、删除）、一句摘要。表不写入 ODS、DWD、ADS。

灌数是独立脚本（`POL-L2-DS10-CMP-GAPFILL-L01`），不是请求处理。本分册不写 DDL。列由 `POL-L2-DS10-CMP-DATA` 定。

两个发布时间对不上行则对比空。HTTP 成功。不在接口里拼一段高亮，不返回写死差异。不返回 501。

## 4. 214 政策详情对比 · search、detail、jobs

至少两条政策。维度不选则六维都出。闭集只有：申报时间、受理部门、产业类别、申报条件、支持力度、申报材料。未勾选的维不读。

### 4.1 正文 · search 与 detail

`GET panorama/search` 与 `GET panorama/{id}/detail` 的正文都委托 `gkxlumen-topic-policy`。检索走已有 `GET /topic/v1/policy/search`，正文走已有 `GET /topic/v1/policy/docs/{id}`。不走门面的 `/{id}` 兜底。不另开对比查询。

申报时间、受理部门、产业类别从这篇正文读出。受理部门读正文，不读 `gapfill_policy_impl_dept`。受理部门不是 215 的实施部门。这三列不进缺项表。

无命中则列表空。无正文则详情空。HTTP 成功。不造一条政策。不返回 501。

### 4.2 申报条件、申报材料、优缺点 · 同一次 detail

仍是 `GET /display/v1/policy/panorama/{id}/detail`。正文走专题门面。申报条件、申报材料、优点（`pros_text`）、缺点（`cons_text`）由 `gkxlumen-element` 在同一次详情只读 `gkxlumenx_gapfill.gapfill_policy_detail_compare`。不把这些列写进接口常量。display 贴进正文后前端画差异柱图（力度分来自当次 Job；无分轴空）与每策优缺点块。display 不直连库，不直连 Python。

某一列无行则该列空。HTTP 成功。不返回写死的条件或材料。不返回 501。

灌数是 `POL-L2-DS10-CMP-GAPFILL-L01`，不是请求处理。本分册不写 DDL。表不写入 ODS、DWD、ADS。

### 4.3 力度分 · jobs

公开资源：`POST /display/v1/policy/panorama/jobs`。指标 `M_POLICY_INTENSITY_SCORE`。`sub_type=policy_intensity`。216 的支持力度不进这条 Job。

链路：

1. 浏览器只打 `POST /display/v1/policy/panorama/jobs`。不打开算法中台页，不打 `/v1/policy/**`。
2. `gkxlumen-display` 不打分，也不直接调 `jobs/execute`。它只调用 `POST /topic/v1/analysis/tasks`。浏览器不打 `/topicAsync/**`。
3. 已有 `PolicyAnalysisAdapterImpl` 再调 `POST /internal/policy/jobs/execute`，`sub_type=policy_intensity`。
4. Python 调用仓库里已有的 `polan.eval.intensity.run`（`lumen-algo-py/vendor/entan-py`）。`run()` 写入 `ads.policy_intensity`，再按所选政策读力度分。Java 不打分，不抄公式。

`M_POLICY_INTENSITY_INDEX` 不挂本页。QPOL-02 的权重保持待确认。D4 保持 mock。三维缺数据时，`run()` 写不出力度分就让该格空，不在接口里补一个分数。

`policy_intensity` 尚未挂上白名单时，这次 Job 的力度结果为空，不返回演示分。挂上之后，表里无行则该格空，也不造 0。

切条件不自动起任务。Job 失败时，已经返回的统计、目录和正文保持原样。

## 5. 215 部门政策对比 · stats

公开资源：`GET /display/v1/policy/panorama/stats`。同步。同一次统计带出区域、类别、总件数和实施部门。

区域、类别委托 `gkxlumen-topic-policy`。区域用已有地区分布。项目类别用已有政策类型，技术类别用已有产业节点。类别的词不从部门缺项表取，也不迁 demo 的扶持类、技术类。桶空则区域下拉空。没有产业节点则技术类别空。不另开路径。

总件数仍是 `M_POLICY_TOTAL_COUNT`。不新造部门指标。缺项表里的件数不改挂成政策总数。

实施部门由 `gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_impl_dept`。一行有区域、实施部门、方面（项目类别或技术类别）、件数、清单标题。现网收集不到实施部门，不按发布机构去重，不扩 `search/options`。方面的取值仍用已有词表里的政策类型或产业节点。

目录按发布机构筛不到这些部门。清单标题只在缺项表里。标题对不上已有政策时只显示标题，不编详情。表无行则部门对比空。HTTP 成功。不造 0。不返回 501。不在接口里写部门名单。

灌数是 `POL-L2-DS10-CMP-GAPFILL-L01`，不是请求处理。本分册不写 DDL。表不写入 ODS、DWD、ADS。D4 仍是 mock。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。本分册不把 mock 写成已上线，不改 D4。

## 6. 216 标杆比对功能 · stats 同步读

公开资源仍是 `GET /display/v1/policy/panorama/stats`。同步。不进 `panorama/jobs`。

指标 `M_POLICY_SUPPORT_STRENGTH`。`gkxlumen-display` 不直连库。`gkxlumen-element` 只读 `ads.policy_intensity` 里已经写下的支持力度。这次统计请求不调用 `intensity.run()`，也不把这一行放进 `POL-L2-DS10-CMP-GAPFILL-L01`。写入仍由已有 `run()` 在 214、218 的 Job 里完成。

对标范围、至少两个对标对象、至少一个字段，是这次查询的条件。范围只有全球科创领先城市、国内先进地区。字段只有政策类型、支持力度、覆盖范围。少了必选条件则该卡空，不补默认对象。金额档缺失时该维空。无行则该卡空，不造 0。HTTP 成功。不返回 501。

对标对象从 `ads.policy_intensity` 已有的地区范围在同一次读取里带出。不另开对象接口，不打 `/v1/policy/**`。没有海外城市。未勾选的字段不进 217 的报告，也不进 218 的图。

D4 仍是 mock。本分册不改 D4，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。对标报告正文不在本叶生成，见第 7 节。

### 6.1 政策类型块（2026-11-11 增补，`POL-L2-DS10-CMP-PTYPE-FDE`）

同一资源 `GET /display/v1/policy/panorama/stats`，同步，不进 Job、不建任务。响应在既有三块之外增一块 `policy_types`。

- 条件门与支持力度一致：`benchmark_scope=国内先进地区`、`benchmark_object` 至少两个、且 `compare_field` 含「政策类型」。条件不齐则该块为空列表，不补默认对象。
- `gkxlumen-element` 只读 `dwd.policy_base_info`（`is_deleted=0`、`source_plane IN ('domestic','global')`）：`SELECT province, policy_type, COUNT(DISTINCT policy_id)` GROUP BY 下推库端，Java 不做内存聚合；返回每省每文种件数与 Top 文种（件数多者，同数取字典序首个）。对象→省映射沿用 `benchmark_objects` 的 `scope_code`/`scope_name`。
- 某省 `policy_type` 全空或无行 → 该省条目缺席，不造 0、不造「无类型」。display 只透传该块，不聚合、不改名。
- 不新造 `metric_id`，不建 gapfill 表，不写 ODS/ADS。口径 = QPOL-01 增补的文种临时默认（DWD `policy_type`），UI 带 🟡「待甲方确认」；甲方归一后若切 ODS 主题分类，只改这一块的 SELECT，不动链路。

## 7. 217 对标报告生成与导出 · benchmark-report

公开资源：`GET /display/v1/policy/panorama/benchmark-report`。同步。

没有 216 的选择则报告空。导出可以不做。格式只有 PDF、Word。不选格式则只在线看行。

`gkxlumen-display` 不直连库，不直连 Python。`gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_benchmark_report`。一行有对标对象、对照字段、差异、优劣、借鉴建议、报告正文。正文写在行里。条件对不上的行不返回。

导出若要文件，从这次读到的行生成。响应里不内嵌一份写死的 PDF 或 Word。不写对象存储。不建邮件。不走 `report/jobs`。核增研报 614–618 和序号 211 的 `assessment-report` 不是这条资源。

无行则报告空。没有行就不产生文件。HTTP 成功。不返回 501。

灌数是 `POL-L2-DS10-CMP-GAPFILL-L01`，不是请求处理。本分册不写 DDL。表不写入 ODS、DWD、ADS。D4 保持 mock。

## 8. 218 对标结果可视化展示 · 同一 jobs

公开资源与 214 力度分相同：`POST /display/v1/policy/panorama/jobs`。`sub_type=policy_intensity`。216 不进这条 Job。

对象和字段沿用 216。图种不选则不出图。对象视角只有地区、政策。图种只有雷达、柱状、热力。政策视角用 214 已选的政策，不另收一批政策。

勾「政策类型」时，地区视角图以各省 Top 文种件数为量，数据来自 `stats` 的 `policy_types` 块（见 6.1 增补），不进本 Job、不改挂力度分；某省无文种不进图。政策视角本字段无量，保持空态。（2026-11-11 增补）

链路与第 4.3 节同一条管道。display 只提交 `POST /topic/v1/analysis/tasks`。适配器再调 Python：先跑已有 `polan.eval.intensity.run`，再按地区或政策读 `ads.policy_intensity` 的力度分。不建 `gapfill_policy_benchmark_viz`。

图上若只画件数，仍用 215 的目录命中和 `M_POLICY_TOTAL_COUNT`，不改挂成力度分。`M_POLICY_INTENSITY_INDEX` 不挂本页。

`policy_intensity` 未挂上白名单时，这次结果为空，不返回演示分，也不返回演示序列。挂上之后，表无行则图空。HTTP 成功意义上的空结果，不返回 501 来充当图。Job 失败不清空已经返回的统计、目录和正文。

切条件不自动起任务。

## 9. 空态对照

六叶的签收读法都是查已有读面或查表。无行则空。不用 501 充当功能。不返回写死的差异、分数、部门名单或 PDF。

| 序号 | 资源 | 无数据 |
|---|---|---|
| 213 | `versions`、`version-diff` | 无成对历史版则不列该政策；两个发布时间对不上行则对比空。不返回写死差异。变化统计由前端聚合 diff 行 |
| 214 正文 | `search` / `{id}/detail` | 无命中则列表空。无正文则详情空。受理部门无正文则该格空，不改读部门缺项表 |
| 214 条件、材料、优缺点 | 同一次 `{id}/detail` | 缺项表该列无行则该列空。不返回写死条件、材料或优缺点 |
| 214 力度分 | `jobs` · `policy_intensity` | 未挂上白名单则结果空，不返回演示分。挂上后无行则该格空，不造 0。失败不清空统计、目录和正文 |
| 215 | `stats` | 区域桶空、类别无节点、部门缺项表无行，则对应块空。总件数无行则该卡空，不造 0。缺项件数不补成政策总数 |
| 216 | `stats` | `ads.policy_intensity` 无支持力度行则该卡空，不造 0。不进 Job。金额档缺失则该维空。「政策类型」块条件不齐或某省无文种行则该省空，不造 0（2026-11-11 增补） |
| 217 | `benchmark-report` | 没有 216 的选择，或表无行，则报告空。不内嵌写死的 PDF。没有行就不产生文件 |
| 218 | `jobs` · `policy_intensity` | 未挂上白名单则结果空，不返回演示序列。挂上后无行则图空。图种不选则不出图。失败不清空统计、目录和正文 |

## 10. 明确不做

- 不另建 API-POL。不冻结枚举、响应字段名和 DTO。交给 `BE-POL-CONTRACT-01`。
- 不写 OpenAPI 字段表。不写实现代码。不改 Python，不改 Java。
- 不新开资源。不把 `/topic/v1/policy`、`/v1/policy`、`/topicAsync/**` 写成浏览器入口。
- 不改 `POL-L2-DS10-CMP-ARCH`、`POL-L2-DS10-QRY-API`、`POL-L2-DS10-SENT-API`、`POL-L2-DS10-TREND-API` 及它们的架构稿，以及说明书、WBS、契约输入清单、调用链与边界、指标与 501。
- 不改 `ARCH-DISPLAY-01`。不把 `E-E7-POLICY-M1-L06` 写成展示联调单。
- `gkxlumen-display` 不直连 Python，不直连库。214、218 的 display 不直接打 `jobs/execute`。
- 216 不进 Job。213、217 不改成 Job。218 不建 `gapfill_policy_benchmark_viz`。
- 不用 501 充当 213–218 的功能。无行则空，不造 0。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不把缺项件数改挂成 `M_POLICY_TOTAL_COUNT`。不把 `M_POLICY_INTENSITY_INDEX` 挂到本页。
- 受理部门不读 `gapfill_policy_impl_dept`。实施部门不按发布机构去重。
- 不把 `compare/jobs`、`report/jobs`、序号 211 的 `assessment-report` 写成 217。
- 查询不灌数。缺项表的建表与灌数不在本分册执行。
- 不改 `FE-POL-01A`、`FE-POL-01B`，不新建前端单。
- 不会签。不把本单标 done。
