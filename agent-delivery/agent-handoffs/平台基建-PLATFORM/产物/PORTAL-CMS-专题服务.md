# 门户 CMS 字段与读接口契约 · 专题服务

> **任务**：`PORTAL-CMS-FIELD-API-L01`  
> **状态**：草案。本文件只写专题服务。  
> **日期**：2026-10-20  
> **执行**：`agent:product-agent` · 监管 `human:淮政玮`  
> **指标查询**：metric-registry，2026-10-20。无 `metric_id` 的只记缺口，不新编口径。

招标锚点：`智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.1 专题服务（全球服务机构概况、服务机构产业分布、服务机构区域分布、服务机构技术能力、深圳产业服务介绍）。

---

## 0. 约定

1. 门户只嵌入 CMS 已发布正文。草稿、审核中不下发。
2. 计算数字走指标服务，带 `metric_id`。CMS 正文里不写人数、营收、排名。
3. 调用链：浏览器 → 门户 Java REST → 读取任欢侧已发布内容。浏览器和 Python 不直连任欢。
4. 现有 `/cms/v1/*` 是任欢后台向智树要事实数据的集群内接口，不走公网网关。本文件的门户读接口给浏览器经网关使用，路径不用 `/cms/v1`。
5. `content_id` 只作内容引用。机构绑定用 `org_id`。产业绑定用已发布的 `industry_id`。

公共信封：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `content_id` | string | 是 | 任欢内容实例 ID |
| `content_type` | string | 是 | 见 §2 |
| `page_key` | enum | 是 | 本模块只有 `shenzhen` 上有 CMS 块 |
| `industry_id` | string | 是 | 当前产业 |
| `org_id` | string | 是 | 服务机构码 |
| `version` | string | 是 | 内容版本 |
| `publish_status` | enum | 是 | `published` / `draft` / `archived`；门户只收 `published` |
| `publish_time` | datetime | 是 | ISO-8601 |
| `sort_order` | int | 是 | 同机构多段正文时的顺序 |
| `locale` | string | 否 | 默认 `zh-CN` |

`html` 只允许段落、标题、列表、引用、加粗、链接、图片 URL。不允许 `script`、内嵌框架、事件属性。

图例：`metric` 计算数字；`cms` 运营正文；`master` 机构主数据。D1 `aligned` 表示口径已对齐；D1 `draft` 表示口径尚未终稿。D4 `mock` 表示仍是模拟数。

重点机构由指标选出，不在 CMS 里另做一份名单。

---

## 1. 区块对照

### 1.1 全球服务机构概况 `page_key=global`

本页没有 CMS 字段。

| 区块 | 归类 | metric_id | 库内名称 | 说明 |
|---|---|---|---|---|
| 服务机构数量 | metric | `M_SVC_PT_GLOBAL_TOTAL` | 全球服务机构总数 | D1 draft，D4 mock |
| 数量的历年趋势 | metric | — | 缺口 | 没有单独的历年趋势 ID。不用总数 ID 假装趋势序列已经定义 |
| 类型分析 | metric | `M_SVC_PT_GLOBAL_TYPE_DIST` | 全球服务机构类型分布 | D1 draft，D4 mock |
| 规模分析 | metric | `M_SVC_PT_GLOBAL_SCALE_DIST` | 全球服务机构规模分布 | D1 draft，D4 mock |

### 1.2 服务机构产业分布 `page_key=industry`

| 区块 | 归类 | 取数 |
|---|---|---|
| 产业链节点上的服务机构数 | metric | `M_SVC_CHAIN_SEGMENT_ORG_COUNT` 环节服务机构数。D1 aligned，D4 mock |
| 节点名称与图谱 | graph | 产业链图谱。不进 CMS |

### 1.3 服务机构区域分布 `page_key=region`

| 区块 | 归类 | 取数 |
|---|---|---|
| 全球 / 全国区域分布 | metric | `M_SVC_PT_REGION_ORG` 区域服务机构数。D1 draft，D4 mock |

### 1.4 服务机构技术能力 `page_key=tech`

| 区块 | 归类 | 取数 |
|---|---|---|
| 技术力前 30 | metric | 按 `M_SVC_ORG_TECH_SCORE` 服务机构影响力从高到低取 30 名。该 ID 的口径是技术力综合评分，0–100。D1 aligned，D4 mock。权重仍待确认（Q-SVCCHAIN-01）。没有单独的「前 30 名」ID |
| 名次、分数 | metric | 同上。CMS 不填名次和分数 |

### 1.5 深圳产业服务介绍 `page_key=shenzhen`

| 区块 | 归类 | 取数 |
|---|---|---|
| 产业服务机构数量及历年趋势 | metric | 数量用 `M_SVC_PT_SZ_TOTAL` 深圳产业服务机构数量。D1 draft，D4 mock。历年趋势没有单独 ID，记缺口 |
| 机构类型统计 | metric | `M_SVC_PT_SZ_TYPE_DIST` 深圳机构类型统计。D1 draft，D4 mock |
| 产业领域分布 | metric | `M_SVC_PT_SZ_FIELD_DIST` 深圳机构产业领域分布。D1 draft，D4 mock |
| 区域分布 | metric | `M_SVC_PT_SZ_REGION_ORG` 深圳机构区域分布。D1 draft，D4 mock |
| 重点机构名单 | metric | 按技术力等指标选取。CMS 不维护另一份重点名单 |
| 名称、成立时间、主要领导人 | master | 机构主数据。CMS 不覆盖法定名称 |
| 当前人数、营收、规模 | metric | `M_SVC_PT_KEYORG_SCALE` 重点机构规模档案值。D1 draft，D4 mock |
| 业务服务领域介绍 | cms | `svc_business_domain.body_html` |
| 业务分布区域上的数量 | metric | 与区域分布相同，走 `M_SVC_PT_SZ_REGION_ORG` 或机构自身统计，不写进 HTML |

---

## 2. CMS 字段

只有重点机构的业务介绍进 CMS。

### 2.1 `svc_business_domain`

页面 `shenzhen`。绑定 `industry_id` + `org_id`。门户把 `body_html` 嵌进该机构的「业务服务领域」。

| 字段            | 类型     | 必填  | 说明                   |
| ------------- | ------ | --- | -------------------- |
| `org_id`      | string | 是   | 服务机构码，对齐主数据          |
| `industry_id` | string | 是   | 当前产业，从产业列表中选择        |
| `body_html`   | html   | 是   | 业务涉及领域的介绍。不写人数、营收、排名 |

未发布时隐藏这段介绍。名称、规模和分布仍可展示。

### 2.2 空态

| 场景 | 门户行为 |
|---|---|
| 该机构没有已发布业务介绍 | 不显示介绍正文，不生成一段假介绍 |
| CMS 超时或 5xx | 只隐藏介绍区。数量、分布、技术力排名照常 |

---

## 3. 读接口

### 3.1 任欢侧

智树 Java 调用。浏览器不调用。

`GET {cms_base}/api/published/topic-service/blocks`

| 查询参数 | 必填 | 说明 |
|---|---|---|
| `industry_id` | 是 | 当前产业 |
| `org_id` | 否 | 传了则只返回该机构 |
| `content_type` | 否 | 目前只有 `svc_business_domain` |
| `locale` | 否 | 默认 `zh-CN` |

只返回 `publish_status=published`。没有内容时 `200` 且 `blocks: []`。

`GET {cms_base}/api/published/topic-service/blocks/{content_id}`

未发布返回 404。

| HTTP | 门户处理 |
|---|---|
| 200 + 空数组 | 隐藏业务介绍 |
| 404 | 同空态 |
| 401 / 429 / 5xx / 超时 | 介绍区不可用，指标区照常 |

### 3.2 智树门户对浏览器（形状冻结，本单不实现）

`GET /portal/v1/topic-service/pages/{page_key}?industry_id=`

- `global`、`industry`、`region`、`tech`：`cms.blocks` 为空数组，只有 `metrics`
- `shenzhen`：`cms` 为 §3.1 的块；`metrics` 为数量、类型、领域、区域、规模和技术力

路径走门户网关，不注册到 `/cms/v1`。

---

## 4. 给任欢

专题服务只维护一种内容：重点服务机构的「业务服务领域」，字段 `svc_business_domain.body_html`，类型 HTML，绑定机构和产业。

请提供 §3.1 两个只读接口，只出已发布内容。

机构数量、类型、规模、区域分布、技术力前 30、重点名单、机构名称和领导人，都不在这些接口里。
