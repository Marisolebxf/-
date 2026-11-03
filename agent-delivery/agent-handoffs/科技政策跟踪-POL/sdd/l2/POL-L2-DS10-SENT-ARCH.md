# POL-L2-DS10-SENT-ARCH · 科创政策全景 · 政策舆情评估

- 任务：`POL-L2-DS10-SENT-ARCH`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 图：`POL-L2-DS10-SENT-ARCH-SEQ`（本叶新图，源文件无 frontmatter，记 `draft`）

本叶只定科创政策全景二级「政策舆情评估」的实现架构和整体流程。SRS 序号 **207–212**。用户故事 `US-DS-POL-03`。不写 OpenAPI 字段、请求体、响应体、枚举。那是 `POL-L2-DS10-SENT-API`。

上游只引用，不改写：`科创政策全景.md` 207–212、`sdd/调用链与边界.md`、`sdd/契约输入清单.md`、`sdd/指标与501.md`、`survey/DS-10.md` 207–212、`sdd/l2/POL-L2-DS10-QRY-ARCH.md`。不新造 `metric_id`，不改 D4。

## 1. 范围

六叶都在全景里完成，不另开页，不另开路径。前缀 `/display/v1/policy/`。

| 序号 | 叶子 | 需规摘要 | 本叶流程 |
|---|---|---|---|
| 207 | 政策查询与对比 | 按类型、地域、时期查询，并同时查看多条政策正文 | 同步，复用多维检索已定的门面委托 |
| 208 | 区域政策差异性分析 | 按地区对比覆盖、力度、实施条件 | 跨项读图。本叶不新开资源 |
| 209 | 政策实施效果跟踪 | 执行情况、受益反馈、社会影响和效果指标 | 501。Job，模型未以可调用服务接通 |
| 210 | 政策受众反馈收集 | 问卷、在线评价、意见征集及汇总 | 501。没有采集服务，也没有反馈指标 |
| 211 | 政策效果评估报告 | 自动生成达成度、社会影响、问题与建议，并可下载 | 501。没有评估报告通道 |
| 212 | 政策匹配与推送 | 按企业规模、行业、发展阶段匹配，并以通知或邮件推送 | 501。Job，两条模型都未接通 |

207 的 D4 仍是 `mock`。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。闸门未解开时，正式值仍是 mock。本叶不把 mock 写成已上线。

## 2. 实现架构

本二级只用契约输入清单里已经点名的资源。208 不设资源。

| 叶子 | 资源 | 流程 |
|---|---|---|
| 207 | `GET /display/v1/policy/panorama/stats`、`search`、`{id}/detail` | 同步。浏览器只打这三条。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy`，对照与 `POL-L2-DS10-QRY-ARCH` 相同 |
| 208 | 不设 `/display/v1/policy` 资源 | 只消费第 7 项已有子图。挂接可空 |
| 209、212 | `POST /display/v1/policy/panorama/jobs` | 当前 501。模型接通后：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-async-service` → Python `/internal/*` |
| 210 | `GET /display/v1/policy/panorama/feedback` | 501。`gkxlumen-display` 直接返回 |
| 211 | `GET /display/v1/policy/panorama/assessment-report` | 501。同上 |

```mermaid
flowchart LR
  fe["全景 · 政策舆情评估 207-212"]
  gw["gkxlumen-gateway"]
  bff["gkxlumen-display /display/v1/policy"]
  tp["gkxlumen-topic-policy"]
  py["Python /internal/policy"]
  async["gkxlumen-topic-async-service"]
  graph["第 7 项已有子图"]
  empty["501 空态"]
  fe --> gw --> bff
  bff -->|"207：stats / search / detail"| tp --> py
  bff -->|"208：只消费，可空"| graph
  bff -->|"209 212：jobs，模型未接通则 501"| async --> py
  bff -->|"210 feedback · 211 assessment-report"| empty
```

浏览器只打 `/display/v1/policy/**`，不改去打 `/policy/topic/v1/policy/**`。`E-E7-POLICY-M1-L06` 不是本二级的实现路径。

207 复用多维检索已经定下的内部委托：`stats` 对 metrics / indicators，`search` 对 search，正文对 `docs/{id}`。展示不直连 Python，不直连 `gkx_search_service`，也不再为这三条建 `gkxlumen-element` 的 policy 包。并列查看是多次读正文，不新开对比引擎。

209、212 不进专题政策门面。任务表、SSE、并发锁复用 `gkxlumen-topic-async-service`。切条件不自动起任务。Job 失败不清空 207 已经返回的统计卡、目录和正文。

`gkxlumen-display` 不直连库，不写算法，不写 nGQL。

## 3. 整体流程

1. 用户做政策查询或页内并列查看。前端调 `stats`、`search`，打开一条时调 `{id}/detail`。207 读政策总数、类型分布、级别分布，以及目录和正文。无行则对应位置空，不造 0。数值在对齐前仍是 mock。
2. 用户要看区域差异。本叶不发新的政策资源。子图能读到则只消费第 7 项已有结果；读不到则该块空。地区件数若只画统计，走第 1 步里已有的全国分布、深圳分布，不把 208 改判成统计读面。
3. 用户要看实施效果。前端向 `jobs` 提交。`M_POLICY_IMPLEMENTATION_EFFECT` 未以可调用服务接通时，display 返回 501，效果跟踪空。不展示写死的效果数。
4. 用户要收集或查看受众反馈。前端调 `feedback`。display 返回 501。问卷、在线评价、意见征集的页面演示不是这条资源。
5. 用户要看或下载效果评估报告。前端调 `assessment-report`。display 返回 501。前端 HTML 不是评估报告服务。
6. 用户要做政策匹配或推送。前端向 `jobs` 提交。`M_POLICY_MATCH`、`M_POLICY_INDUSTRY_FIT` 未接通时，display 返回 501，匹配与推送空。不展示演示打分。通知和邮件不走序号 202 的 `share`，也不走序号 204 的 `subscriptions`。

## 4. 六叶

### 4.1 207 政策查询与对比 · 同步

读已有资源：

- `stats`：`M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`
- `search`：类型、地域、时期落在目录查询上
- `{id}/detail`：同时查看多条政策时，按条读正文

链路与多维检索 197、198、200 相同：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` → Python `/internal/policy`。

空态：不返回 501。无行则统计卡、列表或正文空，不造 0。D4 保持 mock。

不做什么：不新造对比指标。不把「识别优缺点」写成已有模型。深度交叉对比不在本叶，不改走 `compare/jobs`。不把序号 213 的新旧对比、214 的详情力度写进这三条资源。

### 4.2 208 区域政策差异性分析 · 跨项读图

读已有指标：`M_POLICY_GRAPH_107_1`。类型 GRAPH，D4 仍是 mock。本行不改判。

流程：不新开 `/display/v1/policy` 资源。政策子图任务 `E-E7-POLICY-M1-L02` 已完成。抽取脚本 `GDF-POLICY-GRAPH-EXT-L01` 仍是 backlog。展示只消费第 7 项已有子图，Java 不写 nGQL。挂接可空。

地区件数可以复用 `stats` 上已有的 `M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`。那是序号 197 的统计读面，不把 208 改成可接统计读面。需规里的支持力度、实施条件不在本行计算。支持力度是序号 216 的 `M_POLICY_SUPPORT_STRENGTH`。

不做什么：不走 `E-E7-POLICY-M1-L06`。不把专题门面的 `/graph` 改成展示浏览器地址。不重做抽取，不重开 GDF。

### 4.3 209 政策实施效果跟踪 · 501

读已有资源：`POST /display/v1/policy/panorama/jobs`。指标 `M_POLICY_IMPLEMENTATION_EFFECT`，MODEL，D4=mock。成功读面未见可调用服务。QPOL-02。

流程：模型未接通时，前端 → 网关 → `gkxlumen-display` 对这次 Job 返回 501。不进专题政策门面，不读 ADS 填效果数，不建第二套任务表。

空态：实施效果空。概览卡上写死的数不是这条服务。同一指标在推演页的 page_use 不在本叶展开。

接通之后：仍从 `/display/v1/policy/panorama/jobs` 进入，由 `gkxlumen-topic-async-service` 调用已注册的 Python `/internal/*`。Java 不计算效果。未注册则继续 501。

不做什么：不把本叶改判成统计读面。不因 501 清空 207 的目录和正文。

### 4.4 210 政策受众反馈收集 · 501

读已有资源：`GET /display/v1/policy/panorama/feedback`。成功读面未见。政策域没有反馈统计指标，也没有采集任务。

流程：前端 → 网关 → `gkxlumen-display` 直接 501。不进专题政策门面，不进 Python，不建 Job。

空态：问卷、在线评价、意见征集和汇总都空。页面演示不是采集服务。不用 fixture 填反馈。

不做什么：不新造反馈 `metric_id`。不把序号 201 的收藏、序号 204 的订阅写成受众反馈。

### 4.5 211 政策效果评估报告 · 501

读已有资源：`GET /display/v1/policy/panorama/assessment-report`。成功读面未见。本序号没有专属 `metric_id`。

流程：前端 → 网关 → `gkxlumen-display` 直接 501。不进专题政策门面，不进 Python，不建 Job，不写对象存储。

空态：达成度、社会影响、问题、建议和下载都空。前端 HTML 不是评估报告服务。

不做什么：不挂 `M_POLICY_DEEP_168_1`。不把序号 217 的对标报告、核增研报 `report/jobs` 当成这张报告。

### 4.6 212 政策匹配与推送 · 501

读已有资源：`POST /display/v1/policy/panorama/jobs`。指标 `M_POLICY_MATCH`、`M_POLICY_INDUSTRY_FIT`，都是 MODEL，D4=mock，`srs_refs` 为空。QPOL-03。

流程：与 209 同一条 Job。两条都未以可调用服务接通时，这次提交返回 501。不展示演示打分。

`E-E7-POLICY-M1-L03` 只索引焦点、力度、效果三类模型，不改展示 URL，也不把匹配计算搬进 `gkxlumen-display`。

接通之后：仍走 `panorama/jobs` 和 `gkxlumen-topic-async-service`。推送通道不是序号 202 的导出分享，也不是序号 204 的订阅外发。没有发信通道时，匹配结果与推送都保持空，不另造通道。

不做什么：不新造匹配指标。不把产业适配写成 207 的目录筛选。

## 5. 点名排除

| 资源或序号 | 不纳入本二级的原因 |
|---|---|
| `panorama/rank`、`favorites`、`share` | 序号 199、201、202。门面三单是 `E-E7-POLICY-M1-L08`、`L09`、`L10` |
| `panorama/ingest`、`subscriptions` | 序号 203、204 |
| 205、206 | 时序、热力、热点与深度报告。热点走 `jobs`，但是 205 的未见模型，不是 209、212 |
| 213–218 | 新旧对比、详情力度、部门件数、标杆力度、对标报告与对标可视化 |
| `compare/jobs`、`report/jobs` | 核增对比与研报。不是 207 的并列查看，也不是 211 的评估报告 |

## 6. 明确不做

- 不写 OpenAPI 字段表、请求体、响应体、枚举。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。
- 不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 浏览器不改打 `/topic/v1/policy`。不把 `E-E7-POLICY-M1-L06` 写成展示路径。
- 不改 `FE-POL-01A`、`FE-POL-01B`，不新建前端单。
- 不重开 GDF，不加表，不加字段，不写 nGQL。
- 不在本叶注册实施效果、匹配、产业适配模型，也不把它们送进专题政策门面。
- 不把页面演示、写死效果数、演示打分、前端 HTML 写成服务。
- 不会签。不把本单标 done。
