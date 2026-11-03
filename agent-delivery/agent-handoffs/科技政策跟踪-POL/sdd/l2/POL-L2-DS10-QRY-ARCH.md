# POL-L2-DS10-QRY-ARCH · 科创政策全景 · 多维检索查询

- 任务：`POL-L2-DS10-QRY-ARCH`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 图：`POL-L2-DS10-QRY-ARCH-SEQ`（本叶新图，源文件无 frontmatter，不另填绿）
- 签收：2026-11-03 `human:淮政玮` 首次签收。同日按说明书第 11 节复核后再次签收。做不到的只允许缺项表灌 mock 后由接口读表，不允许接口直接返回 mock

本叶只定科创政策全景二级「多维检索查询」的实现架构和整体流程。SRS 序号 **197–202**。用户故事 `US-DS-POL-01`。不写 OpenAPI 字段、请求体、响应体、枚举。那是 `POL-L2-DS10-QRY-API`。

上游只引用，不改写：`科创政策全景.md` 197–202、说明书第 2 节 DS-10 与第 3–6 节、`sdd/调用链与边界.md`、`sdd/契约输入清单.md` 全景五条、`survey/DS-10.md` 197–202、`POL-DISPLAY-长任务总控.md`。不新造 `metric_id`，不改 D4。

对照 `科技政策跟踪-系统详细设计说明书.md` 第 11.1 节。197、198、200 已有 ADS / DWD 时读正式行；没有正式行时读 `gapfill_policy_qry_doc`、`gapfill_policy_qry_stat`。199 没有排序模型，只读 `gapfill_policy_qry_rank`。三张表都在 `gkxlumenx_gapfill`，由 `POL-L2-DS10-QRY-GAPFILL-L01` 灌数，本叶不灌。201、202 不建缺项表，不灌假记录。不写 ODS、DWD、ADS，不读 demo 库，不改 D4，不返回 `smartScore`。

## 1. 范围

六叶都在检索工作区里完成，不另开页，不另开路径。

| 序号 | 叶子 | 需规摘要 | 本叶流程 |
|---|---|---|---|
| 197 | 多维度检索条件设置 | 多源政策按类别、行业领域、发布部门、地区做筛选，并给出全景统计 | 同步，委托专题政策门面 |
| 198 | 高级检索功能 | 关键词、发布机构、效力级别、政策状态，以及 AND / OR / NOT 组合 | 同步，委托专题政策门面 |
| 199 | 检索结果智能排序 | 需规要按相关性、时效性、重要性智能排；没有排序模型 | 读 `gapfill_policy_qry_rank`。普通三列仍走 search |
| 200 | 检索结果筛选与分类 | 在已有结果上再按类型、时间、地域筛选，并按类别分组 | 同步，委托专题政策门面。没有正式行时读缺项表 |
| 201 | 检索历史与收藏 | 需规要记录检索历史并收藏政策 | 可实现：专题门面保存用户记录。不灌假收藏 |
| 202 | 检索结果导出与分享 | 需规要导出文件并以链接或邮件分享 | 可实现：导出当次检索目录。不灌假文件 |

197、198、200 的 D4 仍是 `mock`。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。闸门未解开时，正式值仍是 mock。本叶不把 mock 写成已上线，也不把该闸门写成已解开。

## 2. 实现架构

本二级只用全景已有五条，不新开路径。前缀 `/display/v1/policy/`。

| 叶子 | 资源 | 流程 |
|---|---|---|
| 197、198、200 | `GET /display/v1/policy/panorama/stats`、`GET /display/v1/policy/panorama/search`、`GET /display/v1/policy/panorama/{id}/detail` | 同步。浏览器只打这三条。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy`。正式行读已有表；没有正式行时 Python 读两张缺项表，不在接口里造数 |
| 199 | `GET /display/v1/policy/panorama/rank` | 展示委托专题门面，Python 只读 `gapfill_policy_qry_rank`。不返回 `smartScore` |
| 201 | `GET /display/v1/policy/panorama/favorites` | 可实现。展示只委托专题门面。没有记录则空列表。不建缺项表 |
| 202 | `GET /display/v1/policy/panorama/share` | 可实现。展示只委托专题门面，导出当次目录。不建缺项表，不在接口里放文件字节 |

197、198、200 的内部对照（展示不新开查询引擎）：

| 展示资源 | 委托 `gkxlumen-topic-policy` |
|---|---|
| `panorama/stats` | `GET /topic/v1/policy/metrics`，分布再取 `GET /topic/v1/policy/indicators`（`kind` 为 level / type / timeseries / national / sz / all） |
| `panorama/search` | `GET /topic/v1/policy/search`。筛选项用 `GET /topic/v1/policy/search/options` |
| `panorama/{id}/detail` | `GET /topic/v1/policy/docs/{id}` |
| `panorama/rank` | 门面排序入口转到 Python。Python 只读 `gapfill_policy_qry_rank` |
| `panorama/favorites` | 门面历史与收藏入口。不读缺项表 |
| `panorama/share` | 门面导出与分享入口。不读缺项表 |

stats、search、detail 已由专题门面转到 Python `/internal/policy`。有正式行读 ADS / DWD；没有正式行时 Python 改读两张缺项表，不在响应里写死一份数。rank 由同一门面转到 Python，只读名次表。favorites、share 只委托门面，展示不自己落库、不自己出文件。展示不直连 Python，不直连 `gkx_search_service`，也不再为这些读面建 `gkxlumen-element` 的 policy 包。

契约输入清单把 `rank`、`favorites`、`share` 写在「同步」下，意思是它们是 GET，不是 Job。本叶不把「同步」理解成去读 ADS 统计表。199 读缺项名次表。201、202 读门面自己的用户记录和导出记录。

```mermaid
flowchart LR
  fe["全景 · 多维检索 197-202"]
  gw["gkxlumen-gateway"]
  bff["gkxlumen-display /display/v1/policy"]
  tp["gkxlumen-topic-policy /topic/v1/policy"]
  py["Python /internal/policy"]
  gap["gkxlumenx_gapfill 三张 qry 表"]
  fe --> gw --> bff
  bff -->|"197 198 200：stats / search / detail"| tp --> py
  py -->|"有正式行"| ads["已有 ADS / DWD"]
  py -->|"没有正式行 · 199 名次"| gap
  bff -->|"201 favorites · 202 share"| tp
```

这是对 A1「展示不复用专题业务查询」的**本二级例外**：复用已经实装的政策检索、详情、指标和分布。智能排序、检索历史与收藏、导出与分享也加在同一门面上。浏览器仍只打 `/display/v1/policy/**`，不改去打 `/policy/topic/v1/policy/**`。`E-E7-POLICY-M1-L06` 仍不是展示前端联调单。其余要素域继续自建 L3，本叶不改 `ARCH-DISPLAY-01` 的全局 A1。

`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。布尔组合和二次筛选作为 `search` 的查询条件原样委托，不在展示侧另写一套目录引擎。正式表和缺项表都没有行时，统计卡或列表空，不造 0。注册表 D4 仍是 mock，本叶不改绿。

199、201、202 都只委托专题门面。展示不直连 Python，也不在展示侧另建用户态或导出通道。落点见第 7 节。

读空不清空同页已经返回的统计卡、目录和正文。普通列表排序留在 `search`。

trace 沿既有展示链走。display → topic-policy 上带 traceId。本叶不新设计观测点。

## 3. 整体流程

一次检索按下面六步走。197、198、200 共用前三步，不拆成三套后端。

1. 打开检索。前端经网关调 `stats`。197 读总数和四条分布，198 读时序、三条分布和有效率，200 读类型分布与全国分布。有正式行读已有表；没有正式行读 `gapfill_policy_qry_stat`。两处都没有行则对应统计卡空，不造 0。D4 仍是 mock。
2. 用户设置维度、高级条件或二次筛选。前端调 `search`。有正式目录读 `policy_base_info`；没有正式行读 `gapfill_policy_qry_doc`。布尔组合和二次筛选没有独立 `metric_id`，只是目录查询条件。两处都没有命中则列表空，不造 0。
3. 用户打开一条政策。前端调 `{id}/detail`，读正式正文或缺项目录里的同一条。无正文则详情空。力度和匹配不在这条资源上。
4. 用户要求按相关性、时效性、重要性做智能排序。前端调 `rank`。Python 只读 `gapfill_policy_qry_rank`。表空则名次空。不返回 `smartScore`。若用户只按发布时间、效力级别、浏览量排，仍走第 2 步的目录查询，不调用 `rank`。这三列是查询顺序，不是新指标。
5. 用户要看检索历史或收藏。前端调 `favorites`。展示只委托门面。该用户没有记录时返回空列表。不灌假收藏。页面 localStorage 不是这条资源。
6. 用户要导出或分享。前端调 `share`。展示只委托门面，导出的是当次目录。不灌假文件。前端表格导出和打印窗不是这条资源。

`stats` 这条资源上还挂着 `M_POLICY_INDUSTRY_COVERAGE`、`M_POLICY_SUPPORT_STRENGTH`。它们分别留给无序号的行业覆盖和序号 216。本二级不改这条资源的读面，也不把这两条写成 197–202 的挂接。

## 4. 六叶

### 4.1 197 多维度检索条件设置 · 同步

读已有资源：

- `stats`：`M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST`
- `search`：政策目录。类别、行业领域、发布部门、地区落在目录查询上
- `{id}/detail`：打开一条时读正文

链路：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` → Python `/internal/policy`。展示不直连 Python。

空态：正式表和 `gapfill_policy_qry_stat`、`gapfill_policy_qry_doc` 都没有行则统计卡或列表空，不造 0，也不在接口里写死数。D4 保持 mock。类型分布已有口径标记 QPOL-01，本叶不改口径，也不把类型 mock 写进 `ads.policy_type_dist`。深圳分布已挂在本叶，页面是否已挂接不在本叶改 `FE-POL-01A`。

不做什么：不新造全景汇总指标替代这五条。不把 `M_POLICY_BASE_100_1` 挂进本叶。不把行业覆盖、支持力度算进本叶。不重开 GDF。

### 4.2 198 高级检索功能 · 同步

读已有资源：

- `stats`：`M_POLICY_TIMESERIES`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_VALIDITY_RATE`
- `search`：关键词、发布机构、效力级别、政策状态，以及 AND / OR / NOT。布尔组合没有独立 `metric_id`
- `{id}/detail`：打开一条时读正文

链路与 197 相同。布尔组合作为 `search` 的查询条件委托专题门面，不在展示侧单开算法。

空态：正式表和缺项统计表都没有行则对应统计卡或列表空，不造 0。D4 保持 mock。有效率的 `srs_refs` 为空，本叶不因此新造 id，也不把它从已有挂接上拿掉，更不把有效率 mock 写进 ADS 的有效率列。

不做什么：不把时序改挂焦点指数。时序、全国分布也出现在 205、206，本叶只用它们服务高级检索字段，不实现重点领域分析和动态可视化。不新造布尔指标。

### 4.3 199 检索结果智能排序 · 读缺项名次表

读已有资源：`GET /display/v1/policy/panorama/rank`。没有排序模型，不能当次打分。

流程：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` → Python。Python 只读 `gapfill_policy_qry_rank`。不建 Job，Java 不打分。

空态：名次表没有行则列表空。不返回 `smartScore`。前端演示权重不是排序服务。

列表仍可按发布时间、效力级别、浏览量排。这三列留在 `search` 的目录查询上，不进 `rank`，也不新造 `metric_id`。需规里的「政策级别」与已有判定里的效力级别是同一排序维。

不做什么：不在本叶注册排序模型，不新写打分公式。不把普通三列排序改判成智能排序。不因名次表为空清空已经返回的目录。详见第 7.1 节。

### 4.4 200 检索结果筛选与分类 · 同步

读已有资源：

- `stats`：`M_POLICY_TYPE_DIST`、`M_POLICY_NATIONAL_DIST`。类别分组挂类型分布，地域分组挂全国分布
- `search`：在已有命中上再按政策类型、发布时间、地域收窄。二次筛选没有独立 `metric_id`
- `{id}/detail`：打开一条时读正文

链路与 197 相同。二次筛选是 `search` 的查询条件，不另开资源。

空态：正式分布和缺项统计都没有行则分组或列表空，不造 0。D4 保持 mock。

不做什么：不新造二次筛选指标。不改走 `compare/stats`。深度交叉对比是序号 207 及以后，不在本叶。

### 4.5 201 检索历史与收藏 · 门面用户记录

读已有资源：`GET /display/v1/policy/panorama/favorites`。收藏卡没有 `metric_id`。这叶做得到，不走缺项表。

流程：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy`。不在展示侧建用户态，不建 Job。

空态：该用户没有记录则空列表。不灌假历史或假收藏。localStorage 不是收藏服务。

不做什么：不在本叶改门面代码，不在展示侧另建收藏表。不因空列表清空已经返回的目录和正文。详见第 7.2 节。

### 4.6 202 检索结果导出与分享 · 门面导出当次目录

读已有资源：`GET /display/v1/policy/panorama/share`。这叶做得到，不走缺项表。

流程：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy`。展示不组装文件，不写对象存储，不建 Job。

空态：当次目录为空则导出空。不灌假文件。前端表格导出和打印窗不是分享服务。

不做什么：不把序号 217 的对标报告、核增研报（614–618）或 `report/jobs` 当成全景分享。不因导出空清空已经返回的目录。详见第 7.3 节。

## 5. 点名排除

这些全景资源不属于 197–202。本叶不读、不改、不新开替代路径。

| 资源 | 不纳入本二级的原因 |
|---|---|
| `panorama/ingest` | 序号 203 的入库列表 |
| `POST panorama/jobs` | 实施效果、匹配、力度、热点与深度报告 |
| `panorama/subscriptions` | 序号 204 |
| `panorama/feedback` | 序号 210 |
| `panorama/assessment-report` | 序号 211 |
| `panorama/version-diff` | 序号 213 |
| `panorama/benchmark-report` | 序号 217 |

序号 203–218 的边界见下表。本叶不展开它们的流程。

| 序号 | 与本二级的边界 |
|---|---|
| 203 | 来源监控只读已有入库。资源是 `ingest`。不重开 GDF |
| 204 | 订阅与外发。资源是 `subscriptions`。不是收藏 |
| 205 | 趋势另叶复用时序。热点、影响、深度报告另叶读缺项表。本叶不实现 |
| 206 | 时间与地域另叶读已有表。主题分布另叶读缺项表。本叶不实现 |
| 207 | 页内并列查看另叶。深度对比不在检索五条里 |
| 208 | 区域差异只消费已有子图。本叶不读图，不走 `E-E7-POLICY-M1-L06` |
| 209 | 实施效果另叶读 `ads.policy_effect`。不是检索排序 |
| 210 | 受众反馈另叶读缺项表 |
| 211 | 效果评估报告另叶读缺项表。不是 202 的导出 |
| 212 | 匹配与推送另叶读 `ads.policy_match`。不改展示 URL 去打专题 |
| 213 | 新旧对比另叶。本叶不实现 |
| 214 | 详情对比上的力度另叶。正文读面不带力度 |
| 215 | 部门件数另叶，复用政策总数。本叶不新造部门指标 |
| 216 | 标杆支持力度另叶。本叶不读 `M_POLICY_SUPPORT_STRENGTH` 作为检索结果 |
| 217 | 对标报告另叶。与 `share` 不是同一资源 |
| 218 | 对标可视化另叶。件数若只画统计，仍不改判本叶 |

## 6. 明确不做

- 不写 OpenAPI 字段表、请求体、响应体、枚举。
- 不新造 `metric_id`。不改 D4。不把 mock 写成已上线。
- 不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 浏览器不改打 `/topic/v1/policy` 或 `/policy/topic/v1/policy`。不把 `E-E7-POLICY-M1-L06` 写成展示前端联调单。已实装的内部委托是 stats / search / detail。199、201、202 接通后也只委托门面新增入口。不把 graph / timeline / portal 拉进本二级。
- 不改 `FE-POL-01A`，不新建前端单。契约冻结前前端继续 mock，本叶不猜字段。
- 不重开 GDF，不写 ODS、DWD、ADS。三张 `gapfill_` 表由灌数单建，本叶不灌数、不加字段。
- 不改说明书、WBS、注册表、调研分册。
- 199 不进异步 Job，不注册排序模型。201、202 不进 Python 打分。第 7 节是签收后的读法，本叶不改门面代码。
- 不把 localStorage、`smartScore`、前端导出或打印窗写成已经接通的服务。
- 2026-11-03 human:淮政玮首次签收。同日按说明书第 11 节再次签收。

## 7. 读表

下面三节是签收后的读法。资源名不新开。不新造 `metric_id`，不改 D4，不把本叶标成已灌数。

门面三单已建，本叶不认领、不实现：`E-E7-POLICY-M1-L08` 智能排序，`E-E7-POLICY-M1-L09` 历史与收藏，`E-E7-POLICY-M1-L10` 导出与分享。监管 `human:淮政玮`，执行 `api-agent`。灌数单是 `POL-L2-DS10-QRY-GAPFILL-L01`，执行 `data-agent`。这四张单都不是本叶的会签对象。

### 7.1 199 智能排序

普通排序留在 `search`。发布时间、效力级别、浏览量是目录查询的顺序，继续委托 `gkxlumen-topic-policy` 的 search。这三列不进 `rank`。

智能排序只覆盖相关性、时效性、重要性。没有排序模型，不新写公式。专题门面把 `GET /display/v1/policy/panorama/rank` 转到 Python `/internal/policy`。Python 只读 `gapfill_policy_qry_rank`，按行返回名次。Java 不打分，响应去掉 `smartScore`。

这是同步读，不进 `gkxlumen-topic-async-service`。浏览器不改打专题 URL。表空则名次空。本叶不改门面代码，也不在本叶注册模型。

### 7.2 201 检索历史与收藏

历史和收藏是登录用户的行为记录，不是指标，也不进算法。展示不自建用户态。接通后仍是 `GET /display/v1/policy/panorama/favorites`：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` 的新增历史与收藏入口。浏览器不改打专题 URL。

历史保存的是检索条件，再次执行时仍交给门面上的 `search`。收藏保存的是政策 id，打开时仍走门面上的 `docs/{id}`。用户身份沿用已复用的 `gkxlumen-upms` / `gkxlumen-auth`，不新建 `display_user_*`。

没有记录时返回空列表。不把缺项目录抄成这个用户的收藏。浏览器 localStorage 不写入这条资源。本叶不改门面代码。

### 7.3 202 导出与分享

导出的对象是当前 `search` 已经返回的政策目录。对标报告（217）、核增研报（614–618）和 `report/jobs` 不走这条资源。

展示不组装文件，不写对象存储，不自建发信。接通后仍是 `GET /display/v1/policy/panorama/share`：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` 的新增导出与分享入口。浏览器不改打专题 URL。

门面生成 Excel、PDF 和分享链接。文件若进对象存储，只写桶 `gkx-lumen` 已有目录：PDF 用 `gkx-user-reports/science/pdf/{用户}/{日期}/`，Excel 放 `gkx-others/policy-panorama-search-export/{日期}/`，不新造顶层目录。库里只存桶名、对象键和下载权限。前端不直连对象存储。邮件不在展示侧自建发信服务。

当次目录为空则导出空，不另造一份文件。前端表格导出和打印窗不写成这条服务。本叶不改门面代码。
