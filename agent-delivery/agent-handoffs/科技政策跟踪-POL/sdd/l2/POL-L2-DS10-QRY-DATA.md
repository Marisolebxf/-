# POL-L2-DS10-QRY-DATA · 科创政策全景 · 多维检索查询 · 数据落点

- 任务：`POL-L2-DS10-QRY-DATA`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 上游架构：`POL-L2-DS10-QRY-ARCH`（2026-11-03 human:淮政玮签收）。本单只写数据落点，不改那份架构，不改图。

本叶只定科创政策全景二级「多维检索查询」的数据落点。SRS 序号 **197–202**。用户故事 `US-DS-POL-01`。不写 SQL，不写代码，不写 OpenAPI。

上游只引用，不改写：架构第 2 节和第 7 节、`sdd/调用链与边界.md`、`survey/DS-10.md` 197–202、派单包 `GDF-POLICY-WORKPACK-v2/17-指标离线加工-POLICY-MDC.md`、存储说明 `storage/POLICY/stores/mysql/ads.md` 与 `dwd.md` 里已登记的表。指标 8 件套以 `metric-get` 为准。不新造 `metric_id`，不改 D4。

工作区有未签收 SQL（`lumen-svc-platform/db/9x_gkxlumenx_topic_policy.sql` 及其他未提交的门面代码），不作为本单输入。表名只认已签收的派单包 17、`ads.md`、`dwd.md`。

## 1. 范围

六叶都在检索工作区里完成。浏览器只打 `/display/v1/policy/**`。`gkxlumen-display` 不直连库，不直连 Python，不写对象存储。

| 序号 | 叶子 | 数据角色 | 当前读面 |
|---|---|---|---|
| 197 | 多维度检索条件设置 | 读已有统计结果和已落库政策目录 | 同步。无行则空，不造 0 |
| 198 | 高级检索功能 | 同上，另读时序与有效率挂接 | 同步。无行则空，不造 0 |
| 199 | 检索结果智能排序 | 不落新表 | 501 |
| 200 | 检索结果筛选与分类 | 在同一目录上收窄，分组读已有分布 | 同步。无行则空，不造 0 |
| 201 | 检索历史与收藏 | 登录用户行为，不是指标 | 入口未接上为 501 |
| 202 | 检索结果导出与分享 | 当前 search 目录的文件与下载记录 | 入口未接上为 501 |

197、198、200 的 D4 仍是 `mock`。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked。闸门未解开时，正式值仍是 mock。本叶不把 mock 写成已上线。

八件套源表都是供应库 `dwd_policy_base`。展示链不直查供应库。项目内用数表是已经洗入的 `gkxlumenx_dwd.policy_base_info`。统计结果表是 `gkxlumenx_ads` 里派单包 17 点名的表。D2 仍是 provisional，读面上保留「待核验」，本叶不改这一维。

## 2. 两条已有读路径

197、198、200 不在展示侧另读 ADS，也不另写一套聚合。

统计：前端 → 网关 → `gkxlumen-display` 的 `panorama/stats` → `gkxlumen-topic-policy` 的 `metrics` / `indicators` → Python `/internal/policy` → `gkxlumenx_ads` 已点名结果表。

目录和正文：同一跳上的 `panorama/search`、`panorama/{id}/detail`，分别委托 `search`（筛选项用 `search/options`）和 `docs/{id}` → Python `/internal/policy` → `gkxlumenx_dwd.policy_base_info`。

用数范围沿用派单包 17 第 1 节，本叶不改：`source_plane = domestic`，`is_deleted = 0`，`is_history` 为空视为当前。国际行不进这批分母。目录查询同一张主表，不另圈一批政策。

`GDF-POLICY-MDC-STAT-L01` 与 `BE-POL-DATA-01` 都仍是 backlog。第一批脚本还没进包，上述 ADS 表是已登记的落点，不是已经灌好的正式批次。2026-10-26 结构核对时，产线 `gkxlumenx_dwd.policy_base_info` 为 0 行，demo 库同表有 20,000 行。展示链不读 demo 库，不用 demo 行填正式值。无行则统计卡或列表空，不造 0。

`ads.md` 的展示窗口把类型分布映到 `policy_type_dist`，把有效率映到 `policy_level_dist` 的有效率列。派单包 17 第 3 节明确这两处不写。本叶按 17 读，不改 `ads.md`。

## 3. 197 多维度检索条件设置

### 3.1 统计

读 `stats` 上已有五条。类型都是 STAT，D1 为 aligned，D4 为 mock。

| metric_id | 已有落点 | 本叶怎么读 |
|---|---|---|
| `M_POLICY_TOTAL_COUNT` | `gkxlumenx_ads.policy_level_dist` | 读 `metric_id` 为本指标、`level` 为空的那一行的 `policy_count`。分母是第 2 节的用数范围 |
| `M_POLICY_LEVEL_DIST` | 同一张 `policy_level_dist` | 读本指标的五行。层级编码以派单包 17 为准：4 国家级、3 省级、2 市级、1 区县级、0 未标注。不用该列注释里的「1 国家 / 2 省 / 3 市 / 4 区县」。五行之和等于本批总数 |
| `M_POLICY_NATIONAL_DIST` | `gkxlumenx_ads.policy_national_dist` | 按 `province` 读。空串和字面 `'NULL'` 是一行，`province_name` 为未归省 |
| `M_POLICY_SZ_DIST` | `gkxlumenx_ads.policy_sz_dist` | 只读全市合计一行，`district_name` 为深圳市。不读各区行 |
| `M_POLICY_TYPE_DIST` | 表名 `policy_type_dist` 已在 `ads.md` 登记 | 第一批不写这张表。QPOL-01 未闭合：库里的 `policy_type` 是文种，不是产业 / 人才 / 企业扶持。本叶不补写、不灌数。无正式行则类型分布空，仍挂这条指标号，D4 保持 mock |

替换结果时只删本指标的行。`policy_level_dist` 上总数和级别分布并存，不能互相清掉。`calc_batch_id` 用 `gdf_` 前缀。这些规则属于已有统计任务，本叶不写第二套脚本。

### 3.2 目录和正文

`search` 读 `gkxlumenx_dwd.policy_base_info` 的当前国内行。下列维度是目录查询条件，没有独立 `metric_id`。

| 需规维度 | 落在已有列 | 不读什么 |
|---|---|---|
| 类别 | `policy_type`（文种） | 不把 `theme` 当成已闭合的主题分布，不写 `policy_type_dist` |
| 行业领域 | 条件原样交给已有 `search` | 不挂 `M_POLICY_INDUSTRY_COVERAGE`。不把 `policy_industry_rel` 改成 197 的必读，不重做产业抽取 |
| 发布部门 | `publish_organization` | 不新造部门指标 |
| 地区 | `province`、`city`。深圳条件与深圳分布一致：`city` 为深圳或深圳市 | 不按 `district` 分组 |

打开一条时，`docs/{id}` 读同一行的正文（`title`、`content` 及该行已有字段）。业务键是 `policy_id`。力度和匹配不在这条读面上。

空态：不返回 501。无行则统计卡或列表空，不造 0。

## 4. 198 高级检索功能

统计仍走第 2 节的 `stats`，不另建查询。

| metric_id | 已有落点 | 本叶怎么读 |
|---|---|---|
| `M_POLICY_TIMESERIES` | `gkxlumenx_ads.policy_timeseries` | 只读年：`period_type = Y`，`period_key` 为发布年，`publish_count` 为该年行数。`growth_rate`、`continuity_rate` 留空。连续性仍是 QPOL-07 |
| `M_POLICY_NATIONAL_DIST` | `policy_national_dist` | 与 197 同一张结果 |
| `M_POLICY_LEVEL_DIST` | `policy_level_dist` | 与 197 同一张结果 |
| `M_POLICY_TYPE_DIST` | `policy_type_dist` | 与 197 相同：第一批不写，无正式行则空 |
| `M_POLICY_VALIDITY_RATE` | `ads.md` 把它映在 `policy_level_dist` | 第一批不写 `valid_count`、`validity_rate`，不建废止事实表。口径未指定，本叶不补数。挂接保留，`srs_refs` 为空也不新造 id |

目录条件仍在 `search`，没有独立 `metric_id`。

| 需规条件 | 落在已有列或已有查询 |
|---|---|
| 关键词 | `search` 的文本条件。不新开全文索引 |
| 发布机构 | `publish_organization` |
| 效力级别 | `rank`。与 197 的政策级别是同一列 |
| 政策状态 | `status`。有效率没有第一批结果行，状态筛选不改写成有效率指标 |
| AND / OR / NOT | `search` 的组合条件。不新造布尔指标 |

打开正文与 197 相同，走 `docs/{id}`。

时序和全国分布也出现在序号 205、206。本叶只用它们服务高级检索字段。205、206 的页面流程不在这里写。

空态：不返回 501。无行则对应统计卡或列表空，不造 0。D4 保持 mock。

## 5. 200 检索结果筛选与分类

不另开资源，不改走 `compare/stats`。

| 读什么 | 落点 |
|---|---|
| 类别分组 | `M_POLICY_TYPE_DIST`。第一批不写 `policy_type_dist`，无正式行则分组空 |
| 地域分组 | `M_POLICY_NATIONAL_DIST`，表 `policy_national_dist` |
| 二次筛选 | 仍是 `search`。政策类型收 `policy_type`，发布时间收 `publish_date` / `publish_year`，地域收 `province` / `city`。没有独立 `metric_id` |
| 正文 | `docs/{id}`，同一张 `policy_base_info` |

空态：不返回 501。无行则分组或列表空，不造 0。D4 保持 mock。深度交叉对比是序号 207 及以后，本叶不读。

## 6. 199 检索结果智能排序

不落新表，不读新的 ADS，不注册排序模型。

发布时间、效力级别留在 `search` 的顺序上，对应 `publish_date`、`rank`。浏览量在已签收的 `policy_base_info` 列上未见，本叶不补列。这三列都不是新指标，也不进 `rank`。

相关性、时效性、重要性接通后由专题门面转到 Python `/internal/policy` 当次计算，不把分数写入 ADS，不返回演示权重 `smartScore`。入口未接上时，`panorama/rank` 为 501。实现单是 `E-E7-POLICY-M1-L08`，本叶不认领。

## 7. 201 检索历史与收藏

历史和收藏是登录用户的行为记录，不是指标，没有 `metric_id`，不进算法，不进 ADS 统计表。

展示侧不建 `display_user_*`，不自建用户主数据。身份沿用已有 `gkxlumen-upms` / `gkxlumen-auth`。记录落在专题政策门面 `gkxlumen-topic-policy`，由该门面新增的历史与收藏入口持有。本叶不写 DDL。实现单是 `E-E7-POLICY-M1-L09`，本叶不认领、不改门面代码。

接通后仍是 `GET /display/v1/policy/panorama/favorites`：前端 → 网关 → `gkxlumen-display` → 专题门面。浏览器不改打专题 URL。

| 记录 | 存什么 | 怎么用 |
|---|---|---|
| 检索历史 | 当前用户身份，加上当时的检索条件 | 再次执行时把条件交回门面上的 `search`，不另存一份目录快照 |
| 收藏 | 当前用户身份，加上政策 `policy_id` | 打开时走门面上的 `docs/{id}` |

页面 localStorage 不是这张记录，不写入这条资源。

空态分两种：

- 门面入口未接上：display 返回 501，历史与收藏空。
- 入口已接上，且该用户没有记录：返回空列表，不返回 501。

不因 501 或空列表清空同页已经返回的目录和正文。

## 8. 202 检索结果导出与分享

导出对象只是当前 `search` 已经返回的政策目录，也就是 `policy_base_info` 上这一次命中的行。不是序号 217 的对标报告，不是核增研报 614–618，也不是 `report/jobs`。

展示不组装文件，不写对象存储，不自建发信。接通后仍是 `GET /display/v1/policy/panorama/share`：前端 → 网关 → `gkxlumen-display` → 专题门面的导出与分享入口。浏览器不改打专题 URL。实现单是 `E-E7-POLICY-M1-L10`，本叶不认领。

文件若进对象存储，只写桶 `gkx-lumen` 已有目录，不新造桶，不新造顶层目录。

| 文件 | 对象键 |
|---|---|
| PDF | `gkx-user-reports/science/pdf/{用户}/{日期}/{文件}` |
| Excel | `gkx-others/policy-panorama-search-export/{日期}/{文件}` |

Excel 没有专目录。`policy-panorama-search-export` 只是 `gkx-others/{用途}/{日期}/` 里的用途段。

库里只存三样：桶名、对象键、下载权限。记录由专题门面持有，不进展示库，不进 ADS 指标表。本叶不写 DDL。文件字节不进 MySQL。下载权限只认当前登录用户，经 Java 校验后下载。前端不直连对象存储，不拿 RustFS 凭证。

分享链接若要发出，仍由门面按这条下载权限校验，不把对象做成公开读。邮件不在展示侧建发信数据，本叶不另建外发台账。

空态：入口未接上时 `share` 为 501。前端表格导出和打印窗不是这条记录。

## 9. 跨项只写消费边界

这些资源本叶不读、不改、不新开替代落点。

| 序号或资源 | 边界 |
|---|---|
| 203 `ingest` | 来源监控只读已有入库。不重开 GDF。LLM 合成行落 DWD `policy_base_info`，检索计入，按 `source='llm-synth'` 可识别（2026-11-07） |
| 204 `subscriptions` | 订阅与外发。不是 201 的收藏 |
| 205、206 | 与本叶共用 `policy_timeseries`、`policy_national_dist`。本叶不实现趋势、热力、热点、影响、深度报告 |
| 207 | 深度交叉对比不在检索五条里 |
| 208 | 区域差异只消费已有子图。本叶不读图，不写 nGQL，不走 `E-E7-POLICY-M1-L06` |
| 215 | 部门件数复用 `M_POLICY_TOTAL_COUNT`。本叶不新造部门指标 |
| 216 | 不读 `M_POLICY_SUPPORT_STRENGTH` |
| `M_POLICY_INDUSTRY_COVERAGE` | 挂在同一条 `stats` 上，留给无序号的行业覆盖。本叶不挂 |
| `M_POLICY_BASE_100_1` | 不挂进本叶。可算子项已在第一批，不单开作业 |
| 217 `benchmark-report` | 对标报告。不是 202 的导出 |
| 614–618 | 核增研报。不是 202 的导出，不进本二级落点 |
| 209–214、218 | 效果、反馈、评估、匹配、版本差、力度、对标可视化。本叶不落它们的表 |

## 10. 明确不做

- 不写 SQL，不写代码，不写 DDL，不写 nGQL。
- 不新开 GDF，不加表，不加字段，不写第二套统计脚本。
- 不把 D4 从 mock 改绿，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不把第一批明确不写的 `policy_type_dist`、有效率列补上正式值。
- 不读 demo 库填展示。不用未签收门面 SQL 当表结构。
- 不建 `display_user_*`。不把 localStorage、`smartScore`、前端导出或打印窗写成已接通的存储。
- 不把 217 和研报 614–618 写进本二级的数据落点。
- 不改架构稿、说明书、WBS、注册表、调研分册、`ads.md`、`dwd.md`。
- 不把本单标成 done。
