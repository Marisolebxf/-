# 专题服务内容管理 · 前端联调接口文档（SYSINT-03-03A-JAVA-L01）

> **给谁**：运维内容管理页前端（Part A 写侧）+ 门户深圳页前端（Part B 展示侧）
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
