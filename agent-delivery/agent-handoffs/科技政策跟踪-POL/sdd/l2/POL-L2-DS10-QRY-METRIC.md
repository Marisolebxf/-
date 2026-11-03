# POL-L2-DS10-QRY-METRIC · 科创政策全景 · 多维检索查询 · 后台指标设计

- 任务：`POL-L2-DS10-QRY-METRIC`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 查询：2026-11-03 经 MCP `metric-get` / `metric-query`。未读 seed、矩阵 YAML，未改注册表

本叶只写科创政策全景二级「多维检索查询」的指标挂接。SRS 序号 **197–202**。用户故事 `US-DS-POL-01`。

上游只引用，不改写：`sdd/l2/POL-L2-DS10-QRY-ARCH.md`、`sdd/指标与501.md`、说明书第 2 节 DS-10、`survey/DS-10.md` 197–202。不新注册指标，不改 D4，不写算法实现，不写 OpenAPI。

## 1. 范围

六叶都在检索工作区里完成。判定只沿用说明书第 2 节和调研三档，本叶不升第四档，不改判。

| 序号 | 叶子 | 说明书第 2 节 | 本叶 |
|---|---|---|---|
| 197 | 多维度检索条件设置 | 可接统计读面；五条 STAT | 挂已有五条，D4 仍是 mock |
| 198 | 高级检索功能 | 可接统计读面；五条 STAT | 挂已有五条，D4 仍是 mock |
| 199 | 检索结果智能排序 | 501 | 不是指标。排序模型未注册，501 空态 |
| 200 | 检索结果筛选与分类 | 可接统计读面；两条 STAT | 挂已有两条，D4 仍是 mock |
| 201 | 检索历史与收藏 | 501 | 不是指标。501 空态 |
| 202 | 检索结果导出与分享 | 501 | 不是指标。501 空态 |

197、198、200 的正式值在 `GDF-POLICY-MOCK-GATE-L01` 解开前仍是 mock。该闸门本叶不写成已解开。无行则统计卡或列表空，不造 0，也不改判 501。

## 2. 本二级用到的已有 metric_id

去重后 7 条。全部 `metric-get` 为 `found.seed=true`、`found.matrix=true`。`algorithm_type` 都是 STAT。D4 都是 `mock`。

| metric_id | 中文名 | 挂在 |
|---|---|---|
| `M_POLICY_TOTAL_COUNT` | 政策总数 | 197 |
| `M_POLICY_TYPE_DIST` | 政策类型分布 | 197、198、200 |
| `M_POLICY_LEVEL_DIST` | 政策级别分布 | 197、198 |
| `M_POLICY_NATIONAL_DIST` | 全国政策分布 | 197、198、200 |
| `M_POLICY_SZ_DIST` | 深圳政策分布 | 197 |
| `M_POLICY_TIMESERIES` | 政策时序指标 | 198 |
| `M_POLICY_VALIDITY_RATE` | 政策有效率 | 198 |

这 7 条之外，本二级不新造 `metric_id`。

`stats` 资源上还读得到 `M_POLICY_INDUSTRY_COVERAGE`、`M_POLICY_SUPPORT_STRENGTH`。说明书把前者放在没有 SRS 序号的行业覆盖，把后者放在序号 216。本二级不改挂到 197–202。身份见第 7 节，只作排除，不参与本二级计算。

## 3. 八件套

八件套只含身份：`metric_id`、中文名、口径、公式、`algorithm_type`、源表、源系统、更新频率、`version`。D1–D4、`lifecycle_stage`、`srs_refs` 不放进本节。

七条注册公式都是同一类过程指针：见 calc-logic「计算逻辑说明」与 20261021 正本 §二；公式是过程式复算，未浓缩为单行表达式；禁手抄，实现时以 `code/<metric_id>.py` 为准。本叶不手抄、不展开成可执行式，也不另写一条能算出数的式子。

源系统七条相同：`gkx @ 183.240.141.251:3318（只读）`。`version` 都是 `1`。

| metric_id | 中文名 | algorithm_type | 源表 | 更新频率 |
|---|---|---|---|---|
| `M_POLICY_TOTAL_COUNT` | 政策总数 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_TYPE_DIST` | 政策类型分布 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_LEVEL_DIST` | 政策级别分布 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_NATIONAL_DIST` | 全国政策分布 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_SZ_DIST` | 深圳政策分布 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_TIMESERIES` | 政策时序指标 | STAT | `dwd_policy_base` | daily |
| `M_POLICY_VALIDITY_RATE` | 政策有效率 | STAT | `dwd_policy_base` | weekly |

口径按 `metric-get` 的 `kit.definition` 摘录，不改写：

| metric_id | 口径 |
|---|---|
| `M_POLICY_TOTAL_COUNT` | 政策总数就是底表行数。主键 `id` 无重复，`is_deleted` 全 0，`COUNT(*)` 与 `COUNT(DISTINCT id)` 相等。库内没有现成汇总表，由一条聚合生成。注册判定为完全转换支持 |
| `M_POLICY_TYPE_DIST` | 文种维 `type` 可转换；主题维 `theme` / `keywords` / `keypoints` 数据不足。合成后按部分支持。需规里的主题分类本叶不改写成已经可算。口径标记 QPOL-01，本叶不改口径 |
| `M_POLICY_LEVEL_DIST` | `rank` 列有值。空字符串过滤后记为未标注，五档合计与底表行数闭合。注册判定为完全转换支持 |
| `M_POLICY_NATIONAL_DIST` | `province` 单列可归省，未归省可拆开解释，合计与底表行数闭合。注册判定为完全转换支持 |
| `M_POLICY_SZ_DIST` | 城市层可对账；区县层 `district` 有效值不足。缺的是区县，不是城市。注册判定为部分支持 |
| `M_POLICY_TIMESERIES` | 历史段可逐月复算；当前段库内没有记录。可以发布历史趋势，不能单独承担趋势监测。注册判定为部分支持。连续性口径 QPOL-07，本叶不改口径，也不改挂焦点指数 |
| `M_POLICY_VALIDITY_RATE` | `status` 与 `expire_date` 列在，取值没有判别力。注册口径写完全不支持。`srs_refs` 为空。本叶不因此新造 id，也不把它从 198 的已有挂接上拿掉 |

`extras.algo_server_location` 指向 demo 仓既有计算文件。那是注册表索引，不是本二级的展示调用链。本叶不改那些文件，也不把展示改去调 demo 服务。展示仍按架构稿：浏览器只打 `/display/v1/policy/**`，`gkxlumen-display` 内部委托 `gkxlumen-topic-policy`，再转到 Python `/internal/policy`。

## 4. 接入状态

接入状态不是八件套。下表来自 `metric-get` 的 `readiness`。七条 D1 都是 `aligned`，D2 都是 `partial` 且 `d2_assessed=provisional`（待核验），D4 都是 `mock`。本叶不改任何一维。

| metric_id | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| `M_POLICY_TOTAL_COUNT` | aligned | partial，待核验 | full | mock |
| `M_POLICY_TYPE_DIST` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_LEVEL_DIST` | aligned | partial，待核验 | full | mock |
| `M_POLICY_NATIONAL_DIST` | aligned | partial，待核验 | full | mock |
| `M_POLICY_SZ_DIST` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_TIMESERIES` | aligned | partial，待核验 | partial | mock |
| `M_POLICY_VALIDITY_RATE` | aligned | partial，待核验 | partial | mock |

`is_mock=true`。`d4_note` 写算法服务未上线，保持 mock。对齐前数值仍是 mock。

需求来源不是八件套。沿用查询结果，本叶不改挂：

| metric_id | srs_refs | 本叶用法 |
|---|---|---|
| `M_POLICY_TOTAL_COUNT` | 展示 02/215 部门政策对比；专题 05/100 基础指标 | 说明书第 2 节把总数挂在 197。215 是另叶复用，本叶不把 197 改成只剩部门对比 |
| `M_POLICY_TYPE_DIST` | 05/100。QPOL-01 | 197、198、200 |
| `M_POLICY_LEVEL_DIST` | 05/100 | 197、198 |
| `M_POLICY_NATIONAL_DIST` | 05/100。说明里点到 206 热力 | 197、198、200。206 不在本二级实现 |
| `M_POLICY_SZ_DIST` | 05/100 | 197。页面是否已挂接不在本叶改 `FE-POL-01A` |
| `M_POLICY_TIMESERIES` | 展示 02/205、02/206；05/100 | 说明书第 2 节把时序挂在 198。205、206 另叶，本叶不实现 |
| `M_POLICY_VALIDITY_RATE` | 空 | 仍留在 198 |

## 5. 197、198、200 怎么读

读面沿架构稿，不新开路径。统计在 `GET /display/v1/policy/panorama/stats`。目录在 `search`。正文在 `{id}/detail`。力度和匹配不在详情上。

### 5.1 197 多维度检索条件设置

可接统计读面。挂：

- `M_POLICY_TOTAL_COUNT`
- `M_POLICY_TYPE_DIST`
- `M_POLICY_LEVEL_DIST`
- `M_POLICY_NATIONAL_DIST`
- `M_POLICY_SZ_DIST`

类别、行业领域、发布部门、地区是 `search` 的查询条件，没有独立 `metric_id`。打开一条时读正文，正文不是这五条指标。

### 5.2 198 高级检索功能

可接统计读面。挂：

- `M_POLICY_TIMESERIES`
- `M_POLICY_NATIONAL_DIST`
- `M_POLICY_LEVEL_DIST`
- `M_POLICY_TYPE_DIST`
- `M_POLICY_VALIDITY_RATE`

关键词、发布机构、效力级别、政策状态，以及 AND / OR / NOT，是 `search` 的查询条件。布尔组合没有独立 `metric_id`，本叶不新造布尔指标。

### 5.3 200 检索结果筛选与分类

可接统计读面。挂：

- `M_POLICY_TYPE_DIST`：类别分组
- `M_POLICY_NATIONAL_DIST`：地域分组

在已有命中上再按政策类型、发布时间、地域收窄，是 `search` 的查询条件。二次筛选没有独立 `metric_id`。不改走 `compare/stats`。深度交叉对比是序号 207 及以后。

## 6. 不是指标

199、201、202 在说明书第 2 节只有「501」，没有 `metric_id`。`survey/DS-10.md` 记 algorithm_type、D4 均为未见。本叶保持这个判定。

2026-11-03 `metric-query`（domain=政策）：

| 关键词 | 命中 | 本叶 |
|---|---|---|
| 智能排序 | 0 | 未查到排序模型 |
| 相关性 | 0 | 未查到 |
| 收藏 | 0 | 未查到 |
| 检索历史 | 0 | 未查到 |
| 导出 | 0 | 未查到 |
| 分享 | 0 | 未查到 |
| 排序 | 1 | 命中 `M_POLICY_DS_11_POLICY_EVAL_015`（实施路径与风险辅助，GRAPH）。它是评价页序号 229，不是检索排序。本二级不挂 |

### 6.1 199 检索结果智能排序

不是指标。不造 `metric_id`，不写公式，不写 `smartScore`。

需规要按相关性、时效性、重要性做智能排序。注册表没有这条模型。架构稿的当前路径是 `GET /display/v1/policy/panorama/rank` 由 display 返回 501，智能排序空。未提交的门面代码不算已注册模型。`E-E7-POLICY-M1-L08` 是实现单，本叶不认领，也不把它写成模型已经注册。

普通排序不是指标。按发布时间、效力级别、浏览量排列留在 `search` 的目录顺序上，不进 `rank`，不新造 `metric_id`。需规里的「政策级别」与已有判定里的效力级别是同一排序维。不因 `rank` 的 501 清空已经返回的目录。

### 6.2 201 检索历史与收藏

不是指标。收藏卡没有 `metric_id`。历史与收藏是登录用户的行为记录，不进算法，不算得出一个统计数。不写公式。

`GET /display/v1/policy/panorama/favorites` 当前 501，历史与收藏空。页面 localStorage 不是这条资源。`E-E7-POLICY-M1-L09` 是实现单，未提交的门面代码不算已接通的用户态服务。

### 6.3 202 检索结果导出与分享

不是指标。导出与分享是文件和送达，不是统计读面。不写公式，不把导出条数写成指标。

`GET /display/v1/policy/panorama/share` 当前 501，导出与分享空。前端表格导出和打印窗不是这条资源。序号 217 的对标报告、核增研报（614–618）和 `report/jobs` 不是全景分享。`E-E7-POLICY-M1-L10` 是实现单，未提交的门面代码不算已注册导出模型。

## 7. 点名不挂

下列已注册指标出现在说明书第 2 节的其他行，或出现在 `stats` 读面上。本二级不改挂到 197–202，也不把它们的 D4 改掉。

| metric_id | 注册身份（metric-get） | 不挂本二级的原因 |
|---|---|---|
| `M_POLICY_INDUSTRY_COVERAGE` | 政策产业链覆盖率；STAT；D4=`mock`；`srs_refs` 为空 | 行业覆盖没有 SRS 序号。留给无序号的行业覆盖，不进 197–202 |
| `M_POLICY_SUPPORT_STRENGTH` | 支持力度；COMPUTE；D4=`mock`；需求来源含展示 02/216 | 序号 216 的标杆比对。不写成检索结果 |

序号 203–218 的其余指标（实施效果、匹配、力度分、子图等）沿架构稿第 5 节排除。本叶不读、不改挂、不把 MODEL 改判成统计读面。

`M_POLICY_BASE_100_1` 是边界索引，全景用拆开的总数、类型、级别、全国、深圳、时序，不挂这一条。

## 8. 明确不做

- 不新注册指标，不改 D4，不把 mock 写成已上线。
- 不给 199、201、202 写能算出数的公式，不写 `smartScore`。
- 不把普通三列排序写成智能排序或新指标。
- 不把未提交的门面代码当成已注册模型。排序模型未注册时，199 保持 501 空态。
- 不改唐绍祖锁定的合规算法。本单不写算法实现，不改 demo 仓计算文件。
- 不重开 GDF，不把 `GDF-POLICY-MOCK-GATE-L01` 写成已解开。
- 不改说明书、调研分册、架构稿、注册表和指标 seed。
- 不写 OpenAPI 字段、请求体、响应体、枚举。
