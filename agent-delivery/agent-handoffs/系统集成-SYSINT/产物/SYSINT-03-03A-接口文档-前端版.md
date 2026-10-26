# 专题服务 · 前端联调接口文档（SYSINT-03-03A-JAVA-L01）

> **给谁**：运维内容管理页前端（Part A 写侧）+ 门户深圳页前端（Part B 展示合并）+ 专题服务五页前端（Part C 可视化展示全集）
> **真源**：`agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-03-03A-JAVA-L01.md` §5（本文为其前端摘录，两处不一致以真源为准）
> **契约**：PORTAL-CMS-专题服务.md §2.1（已确认 2026-10-24，字段冻结）
> **日期**：2026-10-26 · 执行 `agent:api-agent`

## 0. 通用约定

| 项 | 值 |
|---|---|
| 网关 Base（dev） | `http://10.50.69.111:30895` |
| 鉴权 | OAuth2 Bearer（网关统一鉴权后转发；**无 token 一律 401 fail-closed**） |
| 响应包络 | `{code:0, msg:"…", data:{…}}`；非 0 见错误码 |
| 错误码 | `40001` 字段校验失败（消息含字段名）/ `40401` 记录不存在或已软删 / `40901` 发布冲突（并发或状态机不符） |
| 联调状态 | **Part B 已在 dev 可调**（`deploy:topic-svc` 已发）；**Part A 待 `deploy:cms` 后可调** |

---

## Part A · 运营写侧（运维内容管理页）

路由前缀：`/cms-ops/v1/topic-service/content/svc-business-domain`

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `org_id` | string | ✅ | 服务机构码（对齐机构主数据） |
| `industry_id` | string | ✅ | 当前产业（从产业列表选择） |
| `body_html` | html | ✅ | 业务服务领域介绍；**白名单校验**：禁 `script`/`iframe`/事件属性（`on*`）/`javascript:` 等脚本协议（含实体编码形态），命中 40001 |
| `page_key` | enum | — | 信封可写；默认 `shenzhen`，可传 `overview/key-pano/star/shenzhen` |
| `sort_order` | int | — | 信封可写；同机构多段正文排序 |
| `locale` | string | — | 信封可写；默认 `zh-CN` |
| `version` / `publish_status` / `publish_time` | — | 🚫 | **动作列禁写**（body 传入被忽略/报错），仅随发布动作变化 |

### A1. 新建（草稿）

```bash
POST /cms-ops/v1/topic-service/content/svc-business-domain
{ "org_id": "ORG-001", "industry_id": "IND-01", "body_html": "<p>业务服务领域介绍</p>", "sort_order": 1 }
```

响应 `data`（信封形状，全部端点一致）：

```json
{ "content_id": "1", "content_type": "svc_business_domain", "page_key": "shenzhen",
  "org_id": "ORG-001", "industry_id": "IND-01", "version": "0", "publish_status": "draft",
  "publish_time": null, "sort_order": 1, "locale": "zh-CN",
  "body_html": "<p>业务服务领域介绍</p>", "updated_at": "2026-10-26T10:00:00" }
```

### A2. 编辑

```bash
PUT /cms-ops/v1/topic-service/content/svc-business-domain/{id}
{ "body_html": "<p>修订后的介绍</p>" }
```

draft/published 均可改；`version` 不动；body 至少带一个可写字段，否则 40001。

### A3. 发布 / 下架

```bash
POST /cms-ops/v1/topic-service/content/svc-business-domain/{id}/publish    # draft→published；version+1；publish_time=now
POST /cms-ops/v1/topic-service/content/svc-business-domain/{id}/unpublish  # published→draft；version 保留
```

非对应状态时 `40901`（含 msg 说明），前端按冲突提示处理。

### A4. 列表（draft+published 都出）

```bash
GET /cms-ops/v1/topic-service/content/svc-business-domain?industry_id=IND-01&org_id=ORG-001&publish_status=published&page=1&size=20
```

| query | 必填 | 说明 |
|---|---|---|
| `industry_id` / `org_id` | — | 过滤，可组合 |
| `publish_status` | — | `draft` / `published`（不传=全部） |
| `page` / `size` | — | 默认 1 / 20，size ≤ 200 |

响应 `data`：`{ "total": 1, "page": 1, "size": 20, "records": [ <同 A1 信封形状> ] }`

### A5. 详情 / 删除

```bash
GET    /cms-ops/v1/topic-service/content/svc-business-domain/{id}   # 40401=不存在/已软删
DELETE /cms-ops/v1/topic-service/content/svc-business-domain/{id}   # 软删 → { "content_id": "1", "deleted": true }
```

---

## Part B · 展示侧（门户深圳页介绍区）

```bash
POST /svc/topic/v1/service-portal/shenzhen        # 网关前缀 /svc，服务内 /topic/v1/service-portal/shenzhen
{ "org_id": "ORG-001", "industry_id": "IND-01" }  # 带机构上下文才返回介绍区；页级统计请求（不带）cms 块为 {}
```

**接口签名与既有字段零变动**，只新增 `data.cms` 块；指标字段（`sz_total`/`districts` 等）照旧。

`data.cms` 四种形态：

| 场景 | cms 块 | 前端行为 |
|---|---|---|
| 有已发布正文 | `{"content_type":"svc_business_domain","present":true,"body_html":"<p>…</p>"}` | 渲染介绍区（富文本按白名单渲染兜底） |
| 无已发布正文 | `{"present":false}` | 隐藏介绍区（契约 §2.2 空态，**不生成假介绍**） |
| cms 故障 | `{"present":false,"data_source":"cms:unavailable"}` | 同空态；指标区照常（失败隔离，HTTP 仍 200） |
| 页级请求（无 org 上下文） | `{}` | 不渲染介绍区 |

dev 已实测三态通过（含插入 published 正文后 `present:true` 原样返回）。

---

## 联调注意

1. 写侧接口**必须带 Bearer token**，先过网关登录态；401 时检查 token 而不是重试
2. `body_html` 编辑器建议按 Arco 白名单渲染（段落/标题/列表/引用/加粗/链接/图片 URL），服务端黑名单是最后防线
3. 列表页如需「机构维度聚合摘要」（enterprise-summary 类）暂未提供 svc 版，当前按 A4 列表 + 双键过滤使用；需要再说
4. 完整 curl 清单与异常场景见真源 handoff §5/§7

---

## Part C · 可视化展示接口全集（专题服务五页 + 机构检索/画像/图谱）

> 均为既有上线接口（非本单新增，本单只给 shenzhen 增加了 `cms` 块）。网关前缀 `/svc`（剥后转发服务内 `/topic/v1/service**`）。
> **统一降级语义**：下游缺数/Feign 失败一律 **HTTP 200** + `empty:true` + `data_source:"unavailable:*"`，**不抛 5xx、不造假数据**；前端按 `empty` 判空态即可。

### C1. 门户五页（`/svc/topic/v1/service-portal/*`）

| 端点 | 页面/用途 | 请求 body 要点 | `data` 响应要点 |
|---|---|---|---|
| `POST /overview` | 全球服务机构概况 | 可选筛选，通常 `{}` | `kpi{}`、`new_org_series[]`、`invest_series[]`、`industry_layout[]`、`org_type_dist[]`、`region_province[]`；缺 KPI 省略该键 |
| `POST /ranking` | 招引/培育/技术力榜单 | `list_type`: `ATTRACT`(默认)/`CULTIVATE`/`TECH`；`limit` | `items[]`（榜单条目）、`total` |
| `POST /industry-distribution` | 服务机构产业分布 | 可选筛选 | `by_service_type[]`、`stages[]`（链上环节分布） |
| `POST /region-map` | 区域分布（全国/全球） | `country` 传则出全球，缺省只出省 | `china[]`、`global[]`、`geo_level_used` |
| `POST /shenzhen` | **深圳页统计 + 介绍区** | 页级：`year`；机构级：`org_id`+`industry_id`（触发 cms 合并，见 Part B） | `sz_total`、`sz_metric_id`、`districts[]`、`cms{}`（Part B）；无独立 series 不出 `trend` |
| `POST /key-orgs` | 重点机构（技术力 Top） | 可选筛选 | `items[]`（按 org_id 去重，含 score/pending） |
| `GET  /health` | 探活 | — | `java{}`/`python{}`/`degraded` |

### C2. 检索/画像/图谱/字典（`/svc/topic/v1/service/*`）

| 端点 | 用途 | 请求 body 要点 | `data` 响应要点 |
|---|---|---|---|
| `POST /search/orgs` | 服务机构检索列表 | `keyword` 或 `q`、`service_type`、`city`、`industry`、`page`、`size` | `items[]`、`total`、`gap[]`（黄灯） |
| `POST /profile/get` | 机构画像卡 | `org_id`（兼容 orgId/service_org_code 别名） | 卡面原样；无卡/失败 `data:null`（不填样例机构） |
| `POST /eco-graph` | 机构生态图谱 | 筛选域 | `nodes[]`、`edges[]`、`subnet_density`、`eco_density`（Java 不重算，原样透传） |
| `POST /rec-list` | 招引/培育推荐名单 | `kind`: `attract`/`cultivate`（或 `list_type`）；`limit` | 同 C1 ranking；未知 kind 诚实空（**不会**回落 TECH 榜） |
| `POST /meta` | 检索/分析字典 | `{}` | `service_types[]`、`org_kinds[]`、`cities[]`、`industries[]`、`links[]`、`analysis{}` |
| `GET  /health` | 探活 | — | 同上 |

### C3. 对比篮（`/svc/topic/v1/service/compare-basket`）

| 端点 | 用途 |
|---|---|
| `GET /` | 查当前篮内机构 |
| `POST /items` | 加入机构（body 带 org 维度） |
| `DELETE /items/{org_id}` | 移出单个 |
| `DELETE /items/batch` | 批量移出 |

### C4. 页面 → 接口速查（专题服务五页）

| 页面 | 调哪些 |
|---|---|
| 全球服务机构概况 | C1 overview |
| 服务机构产业分布 | C1 industry-distribution |
| 服务机构区域分布 | C1 region-map |
| 服务机构技术能力 | C1 ranking(`TECH`) + key-orgs |
| 深圳产业服务介绍 | C1 shenzhen（页级）+ 每机构卡：shenzhen（机构级，出 cms 介绍区）+ C2 profile/get + C1 key-orgs；检索/对比另用 C2 search/orgs、C3 |
