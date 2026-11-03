# POL-L2-DS10-QRY-API · 科创政策全景 · 多维检索查询 · 后台接口设计

- 任务：`POL-L2-DS10-QRY-API`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：`US-DS-POL-01`
- 上游：`sdd/l2/POL-L2-DS10-QRY-ARCH.md`（本分册以它为准，不改）、SRS `科创政策全景.md` 序号 197–202、`sdd/契约输入清单.md` 全景检索六条、`sdd/调用链与边界.md`

本分册只定科创政策全景二级「多维检索查询」的后台接口。它是 `BE-POL-CONTRACT-01` 的输入，不是第二份 API-POL。不另建契约文件。枚举闭包、响应字段名和 DTO 仍由那一张契约冻结。这里只写路径、方法、查询参数、响应要点、同步或 501。

不写实现代码。不改 `E-E7-POLICY-M1-L08`、`L09`、`L10`。不把 `lumen-svc-platform` 或 `lumen-algo-py` 工作区里未提交的门面改动当成契约。已提交门面（检索、选项、正文、指标、分布）可以对照；排序、历史与收藏、导出与分享在已提交门面上没有入口。

## 偏离

本二级 DoD 里「不复用 `/topic/v1/policy`」指浏览器不改打专题 URL。`gkxlumen-display` 内部委托 `gkxlumen-topic-policy` 是 A1 的本二级例外，不写成禁止这次内部委托。浏览器仍只打 `/display/v1/policy/**`。不改 `ARCH-DISPLAY-01` 的全局 A1。`E-E7-POLICY-M1-L06` 仍不是展示前端联调单。graph、timeline、portal 不进本二级。

## 1. 公开资源

六条都是 GET。浏览器经网关打 `gkxlumen-display`。网关只转 `/display/**`。不另开路径，不另开页。六条都不是 Job。

| 序号 | 公开资源 | 当前读法 |
|---|---|---|
| 197、198、200 | `GET /display/v1/policy/panorama/stats` | 同步。不返回 501 |
| 197、198、200 | `GET /display/v1/policy/panorama/search` | 同步。不返回 501 |
| 197、198、200 | `GET /display/v1/policy/panorama/{id}/detail` | 同步。不返回 501 |
| 199 | `GET /display/v1/policy/panorama/rank` | 当前 501 |
| 201 | `GET /display/v1/policy/panorama/favorites` | 当前 501。入口接上且没有记录时改空列表 |
| 202 | `GET /display/v1/policy/panorama/share` | 当前 501 |

`{id}` 是 `search` 目录项里的政策 id。

契约输入清单把 `rank`、`favorites`、`share` 写在「同步」列，意思是它们是 GET，不是 Job。成功读面未见。按该清单和架构稿，这三条当前由 display 直接 501，不建任务，不去读 ADS。

501 不清空同页已经返回的统计卡、目录和正文。

## 2. 内部委托

展示不直连 Python，不直连 `gkx_search_service`，不直连库，不为这六条建 `gkxlumen-element` 的 policy 包。Java 不写算法，不打分，不写 nGQL。

已提交门面的服务内前缀是 `/topic/v1/policy`。浏览器不打这个前缀，也不打网关上的 `/policy/topic/v1/policy/**`。

| 公开资源 | 当前 | 接通后 |
|---|---|---|
| `panorama/stats` | 同步委托 `GET /topic/v1/policy/metrics`，分布再取 `GET /topic/v1/policy/indicators` | 与当前相同。已接通 |
| `panorama/search` | 同步委托 `GET /topic/v1/policy/search`。筛选项用 `GET /topic/v1/policy/search/options` | 与当前相同。已接通 |
| `panorama/{id}/detail` | 同步委托 `GET /topic/v1/policy/docs/{id}` | 与当前相同。已接通 |
| `panorama/rank` | 门面没有排序入口。display 返回 501，不调用门面，不调用 Python | 仍是这一条 GET。display 委托门面新增的排序入口，再转到 Python `/internal/policy` 下的排序路径。同步，不进 `gkxlumen-topic-async-service` |
| `panorama/favorites` | 门面没有历史与收藏入口。display 返回 501 | 仍是这一条 GET。display 委托门面新增的历史与收藏入口。展示不自建用户态 |
| `panorama/share` | 门面没有导出与分享入口。display 返回 501 | 仍是这一条 GET。display 委托门面新增的导出与分享入口。展示不组装文件，不自建发信 |

199、201、202 接通后的门面子路径由 `E-E7-POLICY-M1-L08`、`L09`、`L10` 实现。本分册不冻结这些子路径，也不把工作区未提交改动写成已经存在的入口。展示对外资源名不新开。

trace 沿既有展示链。同步三条在 display → topic-policy 上带 traceId。501 三条在 display 返回，不另起算法 span。本分册不新设计观测点。

## 3. 197 / 198 / 200 · 同步

三条叶子共用 stats、search、detail，不拆三套后端。注册表 D4 仍是 mock。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。闸门未解开时，统计数值仍是 mock。无行则对应统计卡或列表空，不造 0，也不改判 501。

### 3.1 `GET /display/v1/policy/panorama/stats`

查询参数可空。本资源不承接布尔组合、二次筛选和排序。那些在 `search` 或 `rank`。

display 内部先读 metrics（已提交门面无必填查询项，原样透传），再读 indicators。`kind` 取 level、type、timeseries、national、sz、all。分布走 indicators，总数和有效率走 metrics。数字原样上送，Java 不改口径，不把 D4 改绿。

响应要点（按叶子消费，不新造 `metric_id`）：

| 叶子 | 响应里要有的读面 |
|---|---|
| 197 | `M_POLICY_TOTAL_COUNT`、`M_POLICY_TYPE_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_SZ_DIST` |
| 198 | `M_POLICY_TIMESERIES`、`M_POLICY_NATIONAL_DIST`、`M_POLICY_LEVEL_DIST`、`M_POLICY_TYPE_DIST`、`M_POLICY_VALIDITY_RATE` |
| 200 | `M_POLICY_TYPE_DIST`、`M_POLICY_NATIONAL_DIST`。类别分组挂类型分布，地域分组挂全国分布 |

无行则对应统计卡空，HTTP 成功，不造 0。对齐前数值仍是 mock。同一资源上另有 `M_POLICY_INDUSTRY_COVERAGE`、`M_POLICY_SUPPORT_STRENGTH`，不挂本二级，本分册不展开。

筛选项不在 stats 上返回。选项走下一节的内部 `search/options`。

### 3.2 `GET /display/v1/policy/panorama/search`

政策目录。布尔组合和二次筛选没有独立 `metric_id`，只是本资源的查询条件，原样委托已提交的 `GET /topic/v1/policy/search`。已提交门面按未知查询参数原样转发，不在展示侧另写目录引擎。

对外查询参数：

| 参数 | 叶子 | 要点 |
|---|---|---|
| `keyword` | 198 | 政策关键词。内部转发为门面已有的 `keyword`。不另造第三套关键词参数 |
| `ministry` | 197、198 | 发布部门 / 发布机构 |
| `publish_code` | 198 | 发布机构编码，可空 |
| `level` | 198 | 效力级别。需规里的「政策级别」与效力级别是同一维 |
| `policy_type` | 197、200 | 政策类别 / 政策类型。197 的需规范围含科创、行业、园区、招商、人才，以及地方、国家、海外的来源筛选；取值闭包留给契约单 |
| `region` | 197、200 | 地区 / 地域 |
| `status` | 198 | 政策状态。需规取值：有效、失效、修订中 |
| `industry_code`、`industry_vid` | 197 | 行业领域。Java 不解释产业码 |
| `publish_year_from`、`publish_year_to` | 200 | 发布时间范围，用于二次筛选 |
| `logic` | 198 | AND / OR / NOT 组合。无独立 `metric_id`。作为 search 条件原样委托 |
| `order` | 199 的普通排序 | 只接受发布时间、效力级别、浏览量，取值 `publish_time`、`level`、`views`。这是目录查询顺序，不是新指标，不进 `rank` |
| `limit`、`offset` | 目录分页 | 与已提交门面同名透传 |

`level` 出现在两个位置：单独的 `level` 是筛选；`order=level` 是按效力级别排。两者可同时出现。

响应要点：政策目录列表。无命中则列表空，HTTP 成功，不造 0，不返回 501。目录项带政策 id，供 detail 使用。响应不含 `smartScore`。智能排序不在本资源。

普通排序成功时仍是本资源的同步目录，不调用 `rank`。

筛选项（内部，浏览器不打）：display 调 `GET /topic/v1/policy/search/options`。查询可带 `industry_code`。响应要点是去重后的效力级别、政策状态、政策类型，以及该产业码下的节点。无选项则选项空，不造选项，也不把 search 改成 501。

### 3.3 `GET /display/v1/policy/panorama/{id}/detail`

无额外查询参数。display 把 `{id}` 交给 `GET /topic/v1/policy/docs/{id}`。不走门面的 `/{id}` 兜底，避免和静态段混在一起。

响应要点：政策正文。无正文则详情空，HTTP 成功，不返回 501。力度和匹配不在本资源。

## 4. 199 / 201 / 202 · 当前 501 与接通后

当前三句相同：专题门面没有对应入口，display 直接 501，不临时直连 Python，不建 Job，不把页面演示写成服务。接通后浏览器仍打下面这三条展示资源。

### 4.1 `GET /display/v1/policy/panorama/rank` · 199

智能排序只覆盖相关性、时效性、重要性。

| 读法 | 行为 |
|---|---|
| 当前 | HTTP 501。智能排序空。不返回 `smartScore`。不清空已经返回的目录 |
| 接通后 | 仍是本 GET。display → 门面新增排序入口 → Python `/internal/policy` 的排序路径。当次检索同步返回，不进异步任务服务。Java 不打分 |

接通后的查询参数：

| 参数 | 要点 |
|---|---|
| `factor` | 只接受 `relevance`（相关性）、`timeliness`（时效性）、`importance`（重要性） |
| 与当次 search 相同的筛选条件 | 在同一目录上排。不含 `order` |

`order` 的发布时间、效力级别、浏览量留在 search。送进 rank 不是本资源的读法。需规里的政策级别就是效力级别，走 search 的 `order=level`。

接通后响应要点：按 `factor` 排好的政策目录，目录项与 search 同类。响应不含 `smartScore`。前端演示权重不是排序服务。入口和模型都未接上之前，继续 501。

### 4.2 `GET /display/v1/policy/panorama/favorites` · 201

收藏卡没有 `metric_id`。历史和收藏是登录用户的行为记录，不是指标，不进算法。

| 读法 | 行为 |
|---|---|
| 当前 | 入口未接上。HTTP 501。检索历史与收藏空。localStorage 不是本资源 |
| 接通后，该用户没有记录 | HTTP 成功。历史列表和收藏列表都是空列表。这不是 501 |
| 接通后，有记录 | HTTP 成功。历史是检索条件，收藏是政策 id |

接通后仍是本 GET：display → 门面新增的历史与收藏入口。展示不自建用户态，不新建 `display_user_*`。用户身份沿用已复用的 `gkxlumen-upms` / `gkxlumen-auth`。

响应要点：`history`（检索条件列表）、`favorites`（政策 id 列表）。再次执行一条历史时，前端仍调公开的 search。打开一条收藏时，前端仍调公开的 `{id}/detail`，内部仍走 `docs/{id}`。

展示侧公开资源只有这一条 GET。写入留在门面新增入口，本分册不另开展示路径，也不写写入方法。

### 4.3 `GET /display/v1/policy/panorama/share` · 202

导出对象是当前 search 已经返回的政策目录。对标报告、核增研报和 `report/jobs` 不走本资源。本分册不展开那些序号。

| 读法 | 行为 |
|---|---|
| 当前 | 入口未接上。HTTP 501。导出与分享空。前端表格导出和打印窗不是本资源 |
| 接通后 | 仍是本 GET。display → 门面新增的导出与分享入口。目录为空时导出空结果，不改判 501 |

接通后的查询参数：

| 参数 | 要点 |
|---|---|
| 与当次 search 相同的筛选条件 | 导出哪一次目录。展示不另存一份结果集 |
| `format` | `excel` 或 `pdf` |
| `channel` | `link` 或 `email` |

接通后响应要点：分享链接，或文件的桶名与对象键。展示不组装文件字节，不直连对象存储，不自建发信。文件若进对象存储，只写桶 `gkx-lumen` 已有目录，落点沿架构稿第 7.3 节：PDF 用 `gkx-user-reports/science/pdf/{用户}/{日期}/`，Excel 放 `gkx-others/{用途}/{日期}/`，不新造顶层目录。库里只存桶名、对象键和下载权限。邮件由门面侧处理，不在展示侧自建发信服务。

入口未接上之前，本资源继续 501。

## 5. 空态对照

| 资源 | 无数据 | 入口未接上 |
|---|---|---|
| stats | 对应统计卡空，不造 0 | 不适用。已接通，不返回 501 |
| search | 列表空 | 不适用。已接通，不返回 501 |
| detail | 详情空 | 不适用。已接通，不返回 501 |
| rank | 接通后按 factor 返回目录；未接通不把空目录当成智能排序已实现 | 501 |
| favorites | 接通后空列表，HTTP 成功 | 501 |
| share | 接通后目录为空则空导出，不改 501 | 501 |

## 6. 明确不做

- 不另建 API-POL，不冻结枚举和响应字段名。交给 `BE-POL-CONTRACT-01`。
- 不写实现代码。不改 L08 / L09 / L10，不改门面。
- 不把未提交的门面改动写成已有入口。
- 序号 203–218 不在本分册。资源边界以架构稿第 5 节为准，这里不展开。
- 浏览器不改打 `/topic/v1/policy` 或 `/policy/topic/v1/policy`。
- 普通三列排序不改判成智能排序。Java 不打分，响应不带 `smartScore`。
- 收藏没有记录时不返回 501。只有入口未接上才 501。
- 不新造 `metric_id`，不改 D4，不把 mock 写成已上线，不把灌数闸门写成已解开。
- 不把 localStorage、前端表格导出、打印窗写成已经接通的服务。
- 不重开 GDF，不加表，不加字段。不改说明书、WBS、注册表、调研分册、指标分册、数据分册。
