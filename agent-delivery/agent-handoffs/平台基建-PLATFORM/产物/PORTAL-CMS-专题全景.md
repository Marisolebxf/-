# 门户 CMS 字段与读接口契约 · 专题全景

> **任务**：`PORTAL-CMS-FIELD-API-L01`  
> **状态**：草案。本文件只写专题全景。  
> **日期**：2026-10-20  
> **执行**：`agent:product-agent` · 监管 `human:淮政玮`  
> **指标查询**：metric-registry，2026-10-20。无 `metric_id` 的只记缺口，不新编口径。

招标锚点：`智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.1 专题全景（产业链全景、产业资讯、产业整体概况；开篇还包含发展历程和深圳产业现状）。

---

## 0. 约定

1. 门户只嵌入 CMS 已发布正文。草稿、审核中不下发。
2. 计算数字走指标服务，带 `metric_id`。CMS 正文里不写这些数字。
3. 调用链：浏览器 → 门户 Java REST → 读取任欢侧已发布内容。浏览器和 Python 不直连任欢。
4. 现有 `/cms/v1/*` 是任欢后台向智树要事实数据的集群内接口，不走公网网关。本文件的门户读接口给浏览器经网关使用，路径不用 `/cms/v1`。
5. `content_id` 只作内容引用。产业绑定用已发布的 `industry_id`，CMS 不自造正式产业码。

公共信封（每个 CMS 块都有）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `content_id` | string | 是 | 任欢内容实例 ID |
| `content_type` | string | 是 | 见 §2 |
| `page_key` | enum | 是 | `panorama` / `overview`。产业资讯页没有 CMS 块 |
| `industry_id` | string | 是 | 当前产业 |
| `version` | string | 是 | 内容版本 |
| `publish_status` | enum | 是 | `published` / `draft` / `archived`；门户只收 `published` |
| `publish_time` | datetime | 是 | ISO-8601 |
| `sort_order` | int | 是 | 同集合内升序 |
| `locale` | string | 否 | 默认 `zh-CN` |

`html` 只允许段落、标题、列表、引用、加粗、链接、图片 URL。不允许 `script`、内嵌框架、事件属性。图片和链接只传 URL。

图例：`metric` 计算数字；`cms` 运营正文；`record` 要素库表记录；`graph` 图谱结构。D1 `aligned` 表示口径已对齐；D4 `mock` 表示仍是模拟数。D1 `draft` 表示口径尚未终稿。

---

## 1. 区块对照

### 1.1 产业链全景 `page_key=panorama`

| 区块 | 归类 | 取数 |
|---|---|---|
| 上下游、环节、依赖关系 | graph | 产业链图谱。节点和边不进 CMS |
| 细分产业弹窗里的企业列表 | metric | 挂链企业，不由 CMS 填名单 |
| 节点上的统计数字 | metric | 见下表 |
| 节点简介、市场规模文案 | — | 本轮不进 CMS，也不在本文新造字段 |

| 展示 | metric_id | 库内名称 | 说明 |
|---|---|---|---|
| 关联企业数 | `M_CHAIN_ENTERPRISE_COUNT` | 产业链关联企业数 | D1 aligned，D4 mock。挂链企业按 `org_id` 去重。选链是接口过滤 |
| 关联机构数 | `M_CHAIN_INSTITUTION_COUNT` | 产业链关联机构数 | D1 aligned，D4 mock。高校和科研院所，与企业互斥 |
| 节点规模 | `M_CHAIN_NODE_COUNT` | 产业链节点数 | 已注册。就绪度矩阵未覆盖，不把节点数写进 CMS |

### 1.2 产业资讯 `page_key=news`

不进 CMS。门户 Java 读要素库 `dwd_industry_chain_news_info`（产业动态资讯），按当前产业链的 `industry_code` 过滤，`is_deleted=0`，按 `publish_date` 倒序。

| 展示 | 表字段 | 说明 |
|---|---|---|
| 标题 | `title` | |
| 发布时间 | `publish_date` | |
| 摘要 | `abstract` | 表内文本，不是 CMS HTML |
| 来源 | `source` | 来源名称。表上没有报道 URL |
| 资讯 ID | `id` | |
| 产业链 | `industry_code` / `industry_name` | 与 `dwd_industry_chain_info.industry_code` 一对多 |

没有记录时事件线为空，不从其他产业补，也不用大模型生成。任欢不维护、不发布这条。

客户决策清单 2026-08-25 曾记该表「合规交付、禁止业务使用」。本文件按本次确认：产业资讯不进 CMS，读这张表。是否允许上屏仍以那条决策为准。

### 1.3 产业整体概况与深圳现状 `page_key=overview`

同一页可以同时有正文和数字。正文不内嵌假的企业数。

| 区块 | 归类 | 取数 |
|---|---|---|
| 产业介绍 | cms | `pano_industry_intro.body_html` |
| 发展历程 | cms | `pano_dev_history`，按时间线条目 |
| 深圳特色优势 | cms | `pano_sz_feature.body_html` |
| 集群效应 | cms | `pano_cluster_effect.body_html` |
| 竞争地位 | cms | `pano_competitive_position.body_html` |
| 企业数 | metric | `M_CHAIN_ENTERPRISE_COUNT` |
| 机构数 | metric | `M_CHAIN_INSTITUTION_COUNT` |
| 深圳企业数 | metric | `M_CHAIN_SZ_ENTERPRISE_COUNT` 深圳产业链企业数。D1 aligned，D4 mock |
| 深圳机构数 | metric | `M_CHAIN_SZ_INSTITUTION_COUNT` 深圳产业链机构数。D1 aligned，D4 mock |
| 全球区域分布 | metric | `M_CHAIN_GLOBAL_REGION_COUNT` 全球分布区域数。D1 aligned，D4 mock。现阶段只计国内档 |
| 全国区域分布 | metric | `M_CHAIN_NATIONAL_REGION_COUNT` 全国分布区域数。D1 aligned，D4 mock |
| 深圳各区计数 | metric | 缺口。没有已注册的区级 metric_id |

切换产业后，CMS 块和指标都换成该 `industry_id` 的已发布内容和计算结果。

---

## 2. CMS 字段

### 2.1 `pano_industry_intro` / `pano_sz_feature` / `pano_cluster_effect` / `pano_competitive_position`

四块结构相同，用 `content_type` 区分。绑定 `industry_id`。门户嵌入 `body_html`。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `title` | text | 否 | 栏目标题 |
| `body_html` | html | 是 | 正文 |

### 2.2 `pano_dev_history`（发展历程）

绑定 `industry_id`。一条记录里有多条时间线，按 `event_date` 升序。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `events` | object[] | 是 | 见下表 |

`events` 每一项：

| 子字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `event_date` | date | 是 | 排序用 |
| `title` | text | 是 | 阶段或里程碑 |
| `body_html` | html | 是 | 说明 |
| `source_name` | text | 否 | 来源名称 |
| `source_url` | string | 否 | 来源地址 |

### 2.3 空态

| 场景 | 门户行为 |
|---|---|
| 某个文案块未发布 | 该块显示空态，不用大模型临时生成冒充已发布正文 |
| CMS 超时或 5xx | 只让 CMS 区显示「内容服务暂不可用」。企业数、分布、产业资讯照常，资讯不走 CMS |

---

## 3. 读接口

### 3.1 任欢侧

智树 Java 调用。浏览器不调用。

`GET {cms_base}/api/published/topic-panorama/blocks`

| 查询参数 | 必填 | 说明 |
|---|---|---|
| `industry_id` | 是 | 当前产业 |
| `page_key` | 否 | 不传则返回该产业全部已发布块 |
| `content_type` | 否 | 例如只要 `pano_industry_intro`。没有资讯类型 |
| `locale` | 否 | 默认 `zh-CN` |

只返回 `publish_status=published`。没有内容时 `200` 且 `blocks: []`。

`GET {cms_base}/api/published/topic-panorama/blocks/{content_id}`

未发布返回 404。

| HTTP | 门户处理 |
|---|---|
| 200 + 空数组 | 对应空态 |
| 404 | 同空态，不回退草稿 |
| 401 / 429 / 5xx / 超时 | CMS 区不可用，指标区照常 |

### 3.2 智树门户对浏览器（形状冻结，本单不实现）

`GET /portal/v1/topic-panorama/pages/{page_key}?industry_id=`

- `cms`：§3.1 的 `blocks`
- `metrics`：本节列出的 `metric_id` 与指标服务返回值，值不来自任欢
- `page_key=panorama` 和 `page_key=news` 时 `cms.blocks` 为空数组
- `page_key=news` 的列表来自 `dwd_industry_chain_news_info`，不来自任欢

路径走门户网关，不注册到 `/cms/v1`。

---

## 4. 给任欢

请为专题全景维护 §2 的字段，全部绑定 `industry_id`。产业介绍、深圳特色、集群效应、竞争地位、历程说明都是 HTML 富文本。

请提供 §3.1 两个只读接口，只出已发布内容。

产业资讯不进内容管理，也不要资讯接口。企业数、机构数、区域分布不在这些接口里。产业链节点和边也不在这些接口里。
