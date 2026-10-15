# 企业智能搜索接口文档

| 项 | 值 |
|---|---|
| 文档版本 | v1.0 |
| 更新日期 | 2026-10-15 |
| 提供 | 科技专题服务系统项目组 |
| 适用 | 内容运营中心（CMS）企业检索场景对接 |

---

## 1. 能力概述

复用科技专题服务系统已上线的**企业智能搜索**能力，供 CMS 在企业关联、内容检索等场景调用：

- **智能检索**：输入一个或多个关键词，返回匹配企业分页列表
- **输入联想**：搜索框前缀补全
- **热门搜索词**：推荐填入搜索框的示例词
- **批量查询**：按企业代码批量获取企业信息

检索数据、排序与科技专题系统前端使用的完全一致。

## 2. 接入约定

### 2.1 服务地址与鉴权

- 服务地址（Base URL）与访问凭证（`X-CMS-Api-Key`）由项目组随对接通知提供；服务部署于同一 Kubernetes 集群内，仅限集群内服务间调用，不提供公网入口。
- 每个请求须携带请求头：

```
X-CMS-Api-Key: {凭证}
Content-Type: application/json; charset=utf-8
```

### 2.2 通用约定

| 项 | 约定 |
|---|---|
| 请求方法 | 全部 `POST`，请求体为 JSON |
| 字段命名 | `snake_case` |
| 分页 | `page` 从 1 起，默认 1；`size` 默认 10，上限 100 |
| 排序字段 `sort_field` | `competitiveness_score`（默认，综合竞争力得分）/ `patent_valid_count`（有效专利数）/ `latest_revenue`（最新营收）/ `incorporation_date`（成立日期） |
| 排序方向 `sort_order` | `desc`（默认）/ `asc` |
| 日期格式 | `yyyy-MM-dd`；年份为整数 |

### 2.3 统一响应信封

业务响应返回 HTTP 200 + JSON 信封：

```json
{ "code": 0, "msg": null, "data": { } }
```

| 字段 | 类型 | 说明 |
|---|---|---|
| code | integer | `0` 成功；`1` 失败 |
| msg | string | 失败原因描述；成功时为 `null` |
| data | object / array | 业务数据，结构见各接口 |

鉴权与限流类错误使用 HTTP 状态码（见 §4 错误处理），响应体同为 JSON。

## 3. 接口明细

### 3.1 企业智能检索

`POST /cms/v1/enterprise/search/smart`

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keywords | string[] | 与 keyword 二选一 | 关键词数组；**多关键词之间为 OR 关系**（任一命中即返回） |
| keyword | string | 否 | 单字符串；按空格拆分为多关键词，语义同 keywords |
| page | integer | 否 | 页码，默认 1 |
| size | integer | 否 | 每页条数，默认 10，上限 100 |
| sort_field | string | 否 | 默认 `competitiveness_score` |
| sort_order | string | 否 | 默认 `desc` |

#### 检索语义

- 每个关键词在以下字段范围内做**包含匹配**：企业名称（中文 / 英文）、所属产业链、企业标签、主要产品、经营范围、企业简介
- 名称类字段按关键词整体包含匹配；产品 / 经营范围 / 简介等长文本要求关键词为**连续片段**（不做拆字匹配）
- 默认按综合竞争力得分降序返回

#### 响应 `data`

| 字段 | 类型 | 说明 |
|---|---|---|
| list | SearchItem[] | 当前页企业列表，字段见下表 |
| total | integer | 命中总数 |
| page | integer | 当前页码 |
| size | integer | 每页条数 |

**SearchItem 字段**（字段缺值时为 `null`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| org_id | string | 企业唯一标识 |
| social_credit_code | string | 统一社会信用代码 |
| name_cn | string | 企业中文名称 |
| former_names | string[] | 曾用名 |
| lerep | string | 法定代表人 |
| province / city / district | string | 省 / 市 / 区县 |
| industry_class | string | 国民经济行业分类编码 |
| industry_class_name | string | 行业分类名称 |
| incorporation_year | integer | 成立年份 |
| incorporation_date | string | 成立日期 |
| listing_status | string | 上市状态 |
| registered_capital_value | number | 注册资本（数值） |
| tags_flat | string[] | 企业标签 |
| industry_chain_names_flat | string[] | 所属产业链名称 |
| enterprise_scale | string | 企业规模 |
| competitiveness_score | number | 综合竞争力得分 |
| risk_level | string | 风险等级 |
| operating_status | string | 经营状态 |
| chain_position_text | string | 产业链位置描述 |
| main_prod | string | 主要产品 |
| logo_url | string | 企业 Logo 地址 |
| company_type | string | 企业类型 |
| region_id | string | 区域编码 |
| tech_score / business_score | number | 技术力 / 商业力得分 |
| high_value_patent_count | integer | 高价值专利数量 |
| revenue_growth_rate / profit_margin | number | 营收增长率 / 利润率 |
| supply_chain_role | string | 供应链角色 |
| core_tech_tags_flat | string[] | 核心技术标签 |
| statistics | object[] | 统计信息，字段：`patent_total` 专利总数、`patent_valid` 有效专利数、`latest_revenue` 最新营收、`financing_count` 融资事件数、`bid_total` 招投标数、`news_count` 资讯数、`trademark_total` 商标数、`software_copyright_total` 软著数、`rd_ratio` 研发投入占比 |

#### 请求示例

```json
{
  "keywords": ["无人机", "专精特新"],
  "page": 1,
  "size": 10
}
```

#### 响应示例（数据为虚构示例）

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "org_id": "ORG0000123456",
        "social_credit_code": "91440300MA5XXXXXX0",
        "name_cn": "深圳市示例无人机科技有限公司",
        "former_names": [],
        "lerep": "张三",
        "province": "广东省",
        "city": "深圳市",
        "district": "南山区",
        "industry_class": "C39",
        "industry_class_name": "计算机、通信和其他电子设备制造业",
        "incorporation_year": 2016,
        "incorporation_date": "2016-03-15",
        "listing_status": "未上市",
        "registered_capital_value": 5000.0,
        "tags_flat": ["专精特新", "高新技术企业"],
        "industry_chain_names_flat": ["无人机", "智能机器人"],
        "enterprise_scale": "中型",
        "competitiveness_score": 87.6,
        "risk_level": "低",
        "operating_status": "存续",
        "chain_position_text": "中游-整机制造",
        "main_prod": "消费级无人机、工业巡检无人机",
        "logo_url": null,
        "company_type": "有限责任公司",
        "region_id": "440305",
        "tech_score": 90.1,
        "business_score": 82.3,
        "high_value_patent_count": 45,
        "revenue_growth_rate": 0.21,
        "profit_margin": 0.15,
        "supply_chain_role": "供应商",
        "core_tech_tags_flat": ["飞控", "图传"],
        "statistics": [
          {
            "patent_total": 320,
            "patent_valid": 210,
            "latest_revenue": 88000.0,
            "financing_count": 3,
            "bid_total": 12,
            "news_count": 58,
            "trademark_total": 25,
            "software_copyright_total": 40,
            "rd_ratio": 0.12
          }
        ]
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10
  }
}
```

### 3.2 输入联想（搜索框补全）

`POST /cms/v1/enterprise/search/suggest`

输入前缀，返回企业名称候选列表，用于搜索框实时补全。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| prefix | string | 是 | 联想前缀；空串返回空列表 |
| size | integer | 否 | 默认 10，上限 20 |

#### 响应示例

```json
{
  "code": 0,
  "msg": null,
  "data": [
    { "org_id": "ORG0000123456", "name_cn": "深圳市示例无人机科技有限公司" },
    { "org_id": "ORG0000078901", "name_cn": "示例无人机（深圳）有限公司" }
  ]
}
```

### 3.3 热门搜索词

`POST /cms/v1/enterprise/search/hot`

返回推荐填入搜索框的热词列表（非企业列表）。热词由项目组运营维护，内容可能调整，调用方无需感知。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| size | integer | 否 | 默认 10，上限 20 |

#### 响应示例

```json
{
  "code": 0,
  "msg": null,
  "data": [
    { "keyword": "高新技术企业", "count": 0 },
    { "keyword": "专精特新", "count": 0 },
    { "keyword": "集成电路", "count": 0 }
  ]
}
```

### 3.4 按代码批量查询企业

`POST /cms/v1/enterprise/search/by-codes`

传入企业标识数组，返回匹配的企业列表。支持统一社会信用代码与企业唯一标识（org_id），可混传。

#### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| codes | string[] | 是 | 代码数组；自动去空、去重 |

#### 响应 `data`

| 字段 | 类型 | 说明 |
|---|---|---|
| list | SearchItem[] | 命中企业列表（字段同 §3.1） |
| total | integer | 命中数量 |

未命中的代码不会出现在返回列表中，调用方可自行比对。

#### 请求示例

```json
{ "codes": ["91440300MA5XXXXXX0", "ORG0000078901"] }
```

## 4. 错误处理

| 场景 | 表现 |
|---|---|
| 参数为空 / 类型错误 | HTTP 200，`code=1`，`msg` 为错误原因（如 `keywords 不能为空`） |
| 无命中 | HTTP 200，`code=0`，`data.list=[]`、`data.total=0`（非错误） |
| 凭证缺失或无效 | **HTTP 401**，`{"code":"CMS_AUTH_FAILED","msg":"..."}` |
| 触发限流 | **HTTP 429**，`{"code":"CMS_RATE_LIMITED","msg":"..."}` |
| 下游数据服务异常 | **HTTP 5xx**，`{"code":"CMS_QUERY_FAILED","msg":"..."}` |

**重试建议**：接口均为只读幂等操作。对 `code=1` 与 HTTP 5xx 可指数退避重试 2~3 次；HTTP 401 应检查凭证，429 应降低调用频率后重试。

## 5. 联系与支持

服务地址、凭证、联调环境信息由项目组另行提供。对接过程中的问题反馈请通过项目组对接渠道联系。
