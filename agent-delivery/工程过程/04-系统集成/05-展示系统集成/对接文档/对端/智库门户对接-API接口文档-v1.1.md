# 智库报告与成果数据 API 接口文档

| 项 | 内容 |
|---|---|
| 版本 | v1.1（2026-11-03） |
| 提供方 | 智能报告写作平台（zwrite-backend） |
| 接口前缀 | `{BASE_URL}/admin-api/v1`（BASE_URL 以各环境实际部署地址为准，测试环境另行提供） |
| 协议 | HTTPS / HTTP，`GET`，响应 `application/json; charset=utf-8` |

---

## 1. 鉴权

所有接口使用统一用户中心（门户）的 `access_token`，置于请求头：

```
Authorization: Bearer <access_token>
```

| 状态 | HTTP | code | 说明 |
|---|---|---|---|
| 令牌缺失或无效 | 401 | 10001 | 重新获取 access_token |
| 统一用户中心暂不可用 | 503 | 50004 | 非令牌问题，稍后重试 |

## 2. 通用约定

### 2.1 响应信封

```json
{ "code": 0, "message": "ok", "data": { } }
```

`code=0` 为成功，`data` 为业务数据；失败时无 `data`，`message` 为可读错误说明。

### 2.2 通用错误码

| code | HTTP | 说明 |
|---|---|---|
| 10001 | 401 | 令牌缺失/无效 |
| 10002 | 400 | 请求参数非法（具体原因见 message） |
| 10004 | 429 | 触发限流，稍后重试 |
| 50000 | 500 | 服务端内部错误 |
| 50004 | 503 | 统一用户中心暂不可用 |

### 2.3 数据格式

| 类型 | 格式 |
|---|---|
| 时间 | `YYYY-MM-DD HH:MM:SS`（北京时间）；时间窗参数为左闭右开区间 `[time_from, time_to)` |
| 日期 | `YYYY-MM-DD` |
| 分页 | `page` 默认 1；`page_size` 默认 20，最大 100（越界按默认值处理） |
| 金额 | 人民币元 |

---

## 3. 接口一：报告列表

### 3.1 基本信息

| 项 | 内容 |
|---|---|
| 路径 | `GET /admin-api/v1/reports` |
| 说明 | 分页查询报告，支持按类型、领域/行业、关键词、时间范围等筛选 |

### 3.2 请求参数（Query，全部可选）

| 参数 | 类型 | 说明 | 示例 |
|---|---|---|---|
| q | string | 报告标题关键词，模糊匹配 | `新能源` |
| report_type | int | 报告类型：`1` 研究报告 / `2` 洞察报告 / `3` 战略咨询报告 | `1` |
| entry_mode | string | 入库方式：`user` 用户创作 / `platform` 平台制作 / `external` 外部研报。**筛选"外部研报"用本参数**（见接口三枚举项的 param 字段） | `external` |
| strategy_sub_type | string | 战略子分类：`成果` / `建议` / `案例`（仅战略咨询报告有值） | `成果` |
| industry | string | 领域/行业分类名，精确匹配（取值见接口三） | `集成电路` |
| theme_class | string | 主题分类（取值见接口三） | `新能源专题库` |
| status | string | 状态：`draft` / `pending_publish` / `published` / `offline` / `rejected`。**第三方查询公开可见数据请固定传 `published`** | `published` |
| time_from | string | 入库时间起（含），`YYYY-MM-DD HH:MM:SS` | `2026-10-01 00:00:00` |
| time_to | string | 入库时间止（不含） | `2026-11-01 00:00:00` |
| sort_by | string | 排序依据：`created_at`（默认，入库时间）/ `report_type` / `industry` / `entry_mode` | `created_at` |
| order | string | `asc` / `desc`（默认 `desc`）。置顶报告恒排最前，不受排序影响 | `desc` |
| page | int | 页码，默认 1 | `1` |
| page_size | int | 页大小，默认 20，≤100 | `20` |

### 3.3 响应参数

`data` 结构：

| 字段 | 类型 | 说明 |
|---|---|---|
| items | array | 报告列表，元素见下表 |
| total | int | 符合条件的总条数 |
| page / page_size | int | 回显分页参数 |

`items[]` 元素（报告对象）：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | string | 报告唯一标识（UUID） |
| title | string | 报告标题 |
| report_type | int | 报告类型 1/2/3 |
| entry_mode | string | 入库方式 user/platform/external |
| column | string | 所属栏目（派生）：`研究报告` / `洞察报告` / `战略咨询报告` / `研报库` |
| strategy_sub_type | string | 战略子分类：成果/建议/案例；非战略报告为空串 |
| industry_tags | string[] | 领域/行业分类，恒为数组（可能为空） |
| theme_class | string | 主题分类，空串表示未设置 |
| content_tags | string[] | 内容标签 |
| summary | string | 报告摘要 |
| author | string | 公开署名 |
| publishing_org | string | 发布机构（外部研报） |
| published_date | string \| null | 原发布日期 `YYYY-MM-DD` |
| version | string | 版本号，如 `V1.0`、`V1.1` |
| version_at | string \| null | 版本时间 |
| status | string | 状态（见 3.2） |
| listed_at | string \| null | 最近上架（发布）时间 |
| created_at / updated_at | string | 入库时间 / 更新时间 |
| detail_url | string | **详情页跳转地址**：仅已上架且前台可见时非空，否则空串，可直接跳转 |
| platform_certified | bool | 平台认证标识 |
| source_flag | string | 来源标识，如 `平台示范案例` |
| achievements | object \| null | 战略咨询成果数据（结构见 4.3 附注） |
| 其余字段 | — | `fs_file_id` / `file_name` / `license_*` / `auth_scope` / `usage_perms` / `desensitize` / `reject_reason` / `pinned` 为平台管理用字段，第三方可忽略 |

### 3.4 请求示例

```
GET /admin-api/v1/reports?status=published&report_type=1&industry=集成电路&page=1&page_size=10
Authorization: Bearer <access_token>
```

### 3.5 响应示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "集成电路产业链招商策略研究",
        "report_type": 1,
        "entry_mode": "platform",
        "column": "研究报告",
        "strategy_sub_type": "",
        "industry_tags": ["集成电路"],
        "theme_class": "",
        "content_tags": ["产业链", "招商策略"],
        "summary": "梳理集成电路产业链结构、关键技术与招商机会。",
        "author": "国科信研究中心",
        "publishing_org": "",
        "published_date": null,
        "version": "V1.2",
        "version_at": "2026-09-29 21:40:00",
        "status": "published",
        "listed_at": "2026-09-30 10:00:00",
        "created_at": "2026-09-29 20:00:00",
        "updated_at": "2026-09-30 10:00:00",
        "detail_url": "https://zk.example.com/research/detail/9c8d7e6f-...",
        "platform_certified": false,
        "source_flag": "",
        "achievements": null
      }
    ],
    "total": 42,
    "page": 1,
    "page_size": 10
  }
}
```

---

## 4. 接口二：成果列表

### 4.1 基本信息

| 项 | 内容 |
|---|---|
| 路径 | `GET /admin-api/v1/achievements` |
| 说明 | 分页查询战略咨询成果。成果不单独发布，数据来源为**已上架、已选定统计归类且已填写成果数据**的战略咨询报告；按报告更新时间倒序 |

### 4.2 请求参数（Query，全部可选）

| 参数 | 类型 | 说明 | 示例 |
|---|---|---|---|
| sub_type | string | 统计归类：`成果` / `建议` / `案例`（空=全部；白名单外返回 400） | `成果` |
| industry | string | 领域/行业分类名，精确匹配 | `人工智能` |
| q | string | 成果名称关键词，模糊匹配 | `供应链` |
| time_from | string | 报告更新时间起（含），`YYYY-MM-DD HH:MM:SS` | `2026-10-01 00:00:00` |
| time_to | string | 报告更新时间止（不含） | `2026-11-01 00:00:00` |
| page / page_size | int | 分页，默认 1 / 20，≤100 | |

### 4.3 响应参数

`data.items[]` 元素（成果对象）：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | string | 成果标识 = 所属报告 UUID |
| name | string | 成果名称（关联项目名称），恒非空 |
| strategy_sub_type | string | 统计归类：成果/建议/案例 |
| title | string | 所属报告标题 |
| industry_tags | string[] | 领域/行业分类 |
| content_tags | string[] | 标签（取所属报告的内容标签） |
| summary | string | 摘要（取所属报告的摘要） |
| commission_org | string | 委托机构 |
| completed_date | string | 项目完成日期 `YYYY-MM-DD`，可能为空串 |
| updated_at | string | 报告更新时间 |
| detail_url | string | 详情页跳转地址（口径同接口一） |

`data.total / page / page_size` 同接口一。

> 附注：接口一报告对象中的 `achievements` 为成果数据原始结构，主要字段：`project_name` 关联项目名称、`commission_org` 委托机构、`completed_date` 项目完成日期、`actual_investment` 实际投资额（元）、`roi_period_start/roi_period_end` ROI 评价期、`net_profit` 评价期内净收益（元）、`roi_percent` ROI（系统计算，无完整数据时为 null，展示为 `—`）、`satisfaction` 客户满意度（百分制）、`public_confirmed` 公开确认标记。

### 4.4 请求示例

```
GET /admin-api/v1/achievements?sub_type=成果&industry=人工智能&page=1&page_size=10
Authorization: Bearer <access_token>
```

### 4.5 响应示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [
      {
        "id": "dd034745-903f-4df3-b5af-25786cc604a0",
        "name": "供应链金融平台建设",
        "strategy_sub_type": "成果",
        "title": "新能源汽车渠道下沉战略方案",
        "industry_tags": ["智能网联汽车"],
        "content_tags": ["渠道策略"],
        "summary": "围绕新能源汽车渠道下沉主题……",
        "commission_org": "某产业集团",
        "completed_date": "2025-12-31",
        "updated_at": "2026-10-29 15:00:00",
        "detail_url": "https://zk.example.com/strategy/detail/9c8d7e6f-..."
      }
    ],
    "total": 8,
    "page": 1,
    "page_size": 10
  }
}
```

---

## 5. 接口三：筛选枚举

### 5.1 基本信息

| 项 | 内容 |
|---|---|
| 路径 | `GET /admin-api/v1/enums` |
| 说明 | 下发报告/成果两页签的筛选枚举。 |

### 5.2 请求参数（Query）

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| tab | string | 否 | 页签：`report`（报告）/ `achievement`（成果）；不传返回全量 |

### 5.3 响应参数

`data.enums[]` 枚举组：

| 字段 | 类型 | 说明 |
|---|---|---|
| type | string | 枚举组标识：`report_type` 报告类型 / `sub_type` 统计归类 / `industry` 领域行业 / `theme_class` 主题分类 |
| name | string | 枚举组展示名 |
| items | array | 枚举项 |

`items[]` 枚举项：

| 字段 | 类型 | 说明 |
|---|---|---|
| name | string | 展示文案 |
| value | string | 筛选时回传的值 |
| param | string | **回传时使用的查询参数名**。注意：报告类型组中「外部研报」项 `param=entry_mode, value=external`，其余三项 `param=report_type`——请按 param 字段分发，勿统一回传 report_type |

页签与枚举组对应关系：`tab=report` → report_type、industry、theme_class；`tab=achievement` → sub_type、industry。

> **行业字典（2026-11-02 起）**：领域/行业枚举全集为以下 12 项：
> 传感器、低空经济、合成生物、机器人、集成电路、具身智能、人工智能、软件与信息服务、生物医药、数字创意、智能网联汽车、智能终端。
> 存量报告的历史行业值已统一迁移：仅「低空经济」「人工智能」原值保留，其余并入「其他」（「其他」不在枚举下发中，但会出现在报告数据与成果统计里，可作为 `industry` 筛选值回传）。
> 字典后续仍可能由运营调整，**请以本接口实时返回为准，勿在门户侧硬编码行业名**。

### 5.4 响应示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "enums": [
      {
        "type": "report_type",
        "name": "报告类型",
        "items": [
          { "name": "研究报告",     "value": "1",        "param": "report_type" },
          { "name": "洞察报告",     "value": "2",        "param": "report_type" },
          { "name": "战略咨询报告", "value": "3",        "param": "report_type" },
          { "name": "外部研报",     "value": "external", "param": "entry_mode" }
        ]
      },
      {
        "type": "sub_type",
        "name": "统计归类",
        "items": [
          { "name": "成果", "value": "成果", "param": "sub_type" },
          { "name": "建议", "value": "建议", "param": "sub_type" },
          { "name": "案例", "value": "案例", "param": "sub_type" }
        ]
      },
      {
        "type": "industry",
        "name": "领域/行业",
        "items": [
          { "name": "传感器",   "value": "传感器",   "param": "industry" },
          { "name": "低空经济", "value": "低空经济", "param": "industry" }
        ]
      }
    ]
  }
}
```

---

## 6. 接口四：成果统计

### 6.1 基本信息

| 项 | 内容 |
|---|---|
| 路径 | `GET /admin-api/v1/achievements/stats` |
| 说明 | 按领域/行业聚合成果、建议、案例数量。数据口径同接口二；一份报告标注多个领域时计入每个领域；未标注领域的计入「其他」 |

### 6.2 请求参数（Query）

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| industry | string | 否 | 领域/行业分类名；不传返回全部领域，按总数倒序 |

### 6.3 响应参数

`data.items[]`：

| 字段 | 类型 | 说明 |
|---|---|---|
| industry | string | 领域/行业名称（名称即筛选回传值） |
| achievement_count | int | 统计归类=成果 的数量 |
| suggestion_count | int | 统计归类=建议 的数量 |
| case_count | int | 统计归类=案例 的数量 |
| total | int | 该领域合计 |

### 6.4 响应示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [
      { "industry": "人工智能", "achievement_count": 2, "suggestion_count": 1, "case_count": 0, "total": 3 },
      { "industry": "低空经济", "achievement_count": 1, "suggestion_count": 0, "case_count": 0, "total": 1 },
      { "industry": "其他",     "achievement_count": 0, "suggestion_count": 0, "case_count": 1, "total": 1 }
    ]
  }
}
```

---

## 7. 变更记录

| 日期 | 版本 | 说明 |
|---|---|---|
| 2026-11-03 | v1.1 | 行业字典更换为 12 项新枚举（见接口三附注），存量报告行业值已迁移（仅 低空经济/人工智能 保留，其余归「其他」）；四接口的路径、参数与响应结构均无变化 |
| 2026-10-29 | v1.0 | 首版：报告列表、成果列表、筛选枚举、成果统计四接口 |
