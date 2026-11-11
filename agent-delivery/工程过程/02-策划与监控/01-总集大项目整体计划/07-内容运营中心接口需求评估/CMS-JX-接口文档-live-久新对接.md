# CMS-JX 内容运营中心接口文档（已上线）

| 项 | 值 |
|---|---|
| 文档版本 | live-1.7（审计接口 action 筛选 + LIKE 转义 + 字段长度校验说明；2026-11-11） |（对应 OpenAPI `CMS-JX-OpenAPI-v1.0-live.json`；智能搜索四接口新增 country_location_ids 地区筛选） |
| 更新日期 | 2026-11-03 |
| 提供 | 科技专题服务系统项目组（智树侧） |
| 适用 | 久新 CMS 对接；**仅含已上线接口** |
| 接口数量 | **112**（v1.5 新增 smart-search/enterprise、industry、policy、service） |
| 范围说明 | 未上线能力（政策力度榜单/统计、企业全景等门户类）不在本文档 |

> 下文按模块列出全部已上线接口。若需在 Apifox / Postman 调试，可另导入同目录 `CMS-JX-OpenAPI-v1.0-live.json`（OpenAPI 3.0）。

---

## 1. 接入约定

### 1.1 服务地址与鉴权

- **Base URL**：久新当前经智树网关访问（见 §1.5 跨集群联调访问说明）：`http://10.50.69.111:30895` + 路径前加 `/cms`。集群内服务直连地址为 ClusterIP `http://gkxlumen-platform-cms.zhipu-tts.svc.cluster.local:7098`（仅集群内可用）。凭证随对接通知线下提供。
- 每个请求须携带：

```
X-CMS-Api-Key: {凭证}
Content-Type: application/json; charset=utf-8
```

- 写操作（create / update / delete / mark 等）建议另带：

```
X-CMS-Operator: {操作人姓名或账号}
```

缺省记为 `unknown`，用于审计归属。

### 1.2 通用约定

| 项 | 约定 |
|---|---|
| 请求方法 | 全部 `POST`，请求体 JSON |
| 路径参数 | **禁止**业务 id 走路径；业务 id / 筛选 / 分页一律在 body。路径中 `{entityType}` / `{domain}` 仅为有限枚举段 |
| 字段命名 | `snake_case` |
| 分页 | `page` 从 1 起；`size` 默认 20、上限 100（个别接口另有说明） |
| 列表默认 | 不返回已软删记录 |
| 实体写语义 | 真源表不写；编辑只写 overlay 字段级覆盖；删除=软删+审计 |

### 1.3 统一响应信封

```json
{ "code": 0, "msg": "ok", "data": { } }
```

列表类 `data`：

```json
{ "code": 0, "msg": "ok", "data": { "total": 123, "page": 1, "size": 20, "records": [ ] } }
```

### 1.3.1 响应 data.records 内字段说明

> 列表/详情类接口的信封 `data.records[]` 内的业务字段，**在该接口自己的小节内定义**（如"关系·列表"的定义区块）；本节只约定信封结构。若小节内响应表仅列 code/msg/data 三行，表示 `data` 结构见对应请求小节说明或为简单确认（如 `{id, deleted}`）。

### 1.4 错误码

| code | HTTP | 语义 |
|---|---|---|
| 0 | 200 | 成功 |
| 40001 | 400 | 参数缺失/格式错（`CMS_BAD_PARAM`） |
| 40101 | 401 | API Key 无效（`CMS_AUTH_FAILED`） |
| 40401 | 404 | 业务 ID 不存在或已软删（`CMS_NOT_FOUND`） |
| 40901 | 409 | 删除被引用（`CMS_DELETE_REFUSED`，`data.reasons` 列引用来源） |
| 42901 | 429 | 限流（`CMS_RATE_LIMITED`） |
| 50001 | 5xx | 查询失败（`CMS_QUERY_FAILED`） |

---

## 1.5 跨集群联调访问说明（网关入口，2026-10-23 起）

久新集群与智树集群为异集群，经智树 API 网关访问，**路径在文档原路径前统一加一层 `/cms`**：

```
文档路径:  /api/open/cms/v1/policy/list
网关调用:  http://10.50.69.111:30895/cms/api/open/cms/v1/policy/list
                                  ^^^^ 网关匹配段，转发时自动剥离
```

- **Base URL**：`http://10.50.69.111:30895`（智树网关内网地址，请先确认贵方网络到该节点可达）
- **路径规则**：网关 `/cms/**` → 剥离 `/cms` → 转发智树 CMS 服务的 `/api/open/**`；服务端收到的路径与本文档一致
- **鉴权**：`X-CMS-Api-Key` 不变（随对接通知线下提供）；写操作建议带 `X-CMS-Operator`
- **临时性**：该网关入口为跨集群联调临时开通（已限流 + Key 鉴权）；久新服务后续入智树集群后，将切换回集群内 Service 直连（届时路径回到文档原样，无 `/cms` 前缀），会提前通知
- **注意**：本文档其余章节的所有路径示例均为服务本征路径；经网关调用时统一在前面加 `/cms` 即可

---

## 2. 接口目录

| 模块 | 数量 |
|---|---|
| 读侧·企业 | 4 |
| 企业实体 | 3 |
| 企业动态资讯 | 5 |
| 深圳企业专项 | 5 |
| 读侧·政策 | 4 |
| 政策条目 | 4 |
| 读侧·服务机构 | 3 |
| 服务机构实体 | 3 |
| 服务机构动态 | 5 |
| 深圳服务机构专项 | 5 |
| 产品实体 | 5 |
| 自定义产业分类 | 6 |
| 自定义产业链环节 | 6 |
| 产业动态资讯 | 5 |
| 区域企业名录 | 5 |
| 图谱·阶段定义 | 4 |
| 图谱·实体生命周期 | 3 |
| 图谱·关系链 | 7 |
| 图谱·实体属性 | 4 |
| 专家知识 | 6 |
| 读侧·产业 | 2 |
| 读侧·批量 | 1 |

---

## 3. 接口明细

### 3.1 读侧·企业

#### 3.1.1 企业列表（join 视角：真源∪虚拟，软删剔除）

`POST /api/open/cms/v1/enterprise/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<enterprise> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.1.2 企业详情

`POST /api/open/cms/v1/enterprise/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | object | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.1.3 企业下拉

`POST /api/open/cms/v1/enterprise/suggest`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| limit | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.1.4 企业产品名称（真源∪overlay 合并）

`POST /api/open/cms/v1/enterprise/products`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | object | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.2 企业实体

#### 3.2.1 企业实体·新增

`POST /api/open/cms/v1/enterprise/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 | 企业名称；覆盖写 overlay |
| regInfo | string | 否 | 工商注册信息摘录 |
| founded | string | 否 | 成立时间 |
| capital | string | 否 | 注册资本 |
| type | string | 否 | 运营分类标签；枚举: 高新技术企业/专精特新/上市公司/初创企业 |
| industry | string | 否 | 运营行业标签；枚举: 人工智能/生物医药/高端装备/新能源 |
| scale | string | 否 | 枚举: 大型/中型/小型 |
| isKey | string | 否 | 是否重点企业；枚举: 是/否 |
| flag | string | 否 | 枚举: 龙头/潜力/观察/风险关注 |
| priority | string | 否 | 枚举: P0/P1/P2/P3 |
| reason | string | 否 | 标识原因 |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.2.2 企业实体·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/enterprise/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 否 | 企业名称；覆盖写 overlay |
| regInfo | string | 否 | 工商注册信息摘录 |
| founded | string | 否 | 成立时间 |
| capital | string | 否 | 注册资本 |
| type | string | 否 | 运营分类标签；枚举: 高新技术企业/专精特新/上市公司/初创企业 |
| industry | string | 否 | 运营行业标签；枚举: 人工智能/生物医药/高端装备/新能源 |
| scale | string | 否 | 枚举: 大型/中型/小型 |
| isKey | string | 否 | 是否重点企业；枚举: 是/否 |
| flag | string | 否 | 枚举: 龙头/潜力/观察/风险关注 |
| priority | string | 否 | 枚举: P0/P1/P2/P3 |
| reason | string | 否 | 标识原因 |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.2.3 企业实体·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/enterprise/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.3 企业动态资讯

#### 3.3.1 企业动态资讯·列表

`POST /api/open/cms/v1/enterprise/news/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |
| keyword | string | 否 |  |
| kind | string | 否 |  |
| risk | string | 否 |  |
| status | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<enterprise_news> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.3.2 企业动态资讯·详情

`POST /api/open/cms/v1/enterprise/news/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| title | string | 是 |  |
| company | array<string> | 是 | 关联企业 org_id 数组（多选） |
| kind | string | 否 | 枚举: 新闻公告/财报摘要/法律诉讼/行政处罚/舆情事件 |
| content | string | 是 |  |
| risk | string | 否 | 枚举: 低/中/高 |
| status | string | 否 | 枚举: 有效/已过期/已归档 |
| date | string | 否 |  |
| sourceUrl | string | 否 |  |


#### 3.3.3 企业动态资讯·新增

`POST /api/open/cms/v1/enterprise/news/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | 是 |  |
| company | array<string> | 是 | 关联企业 org_id 数组（多选） |
| kind | string | 否 | 枚举: 新闻公告/财报摘要/法律诉讼/行政处罚/舆情事件 |
| content | string | 是 |  |
| risk | string | 否 | 枚举: 低/中/高 |
| status | string | 否 | 枚举: 有效/已过期/已归档 |
| date | string | 否 |  |
| sourceUrl | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.3.4 企业动态资讯·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/enterprise/news/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | 否 |  |
| company | array<string> | 否 | 关联企业 org_id 数组（多选） |
| kind | string | 否 | 枚举: 新闻公告/财报摘要/法律诉讼/行政处罚/舆情事件 |
| content | string | 否 |  |
| risk | string | 否 | 枚举: 低/中/高 |
| status | string | 否 | 枚举: 有效/已过期/已归档 |
| date | string | 否 |  |
| sourceUrl | string | 否 |  |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.3.5 企业动态资讯·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/enterprise/news/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.4 深圳企业专项

#### 3.4.1 深圳企业专项·列表

`POST /api/open/cms/v1/enterprise/sz/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |
| keyword | string | 否 |  |
| district | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<enterprise_sz> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.4.2 深圳企业专项·详情

`POST /api/open/cms/v1/enterprise/sz/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 | 企业 org_id（下拉回填，响应回显名称） |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华/光明 |
| industry | string | 是 |  |
| park | string | 否 |  |
| szNote | string | 否 | docx 扩展字段 |


#### 3.4.3 深圳企业专项·新增

`POST /api/open/cms/v1/enterprise/sz/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 | 企业 org_id（下拉回填，响应回显名称） |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华/光明 |
| industry | string | 是 |  |
| park | string | 否 |  |
| szNote | string | 否 | docx 扩展字段 |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.4.4 深圳企业专项·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/enterprise/sz/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 否 | 企业 org_id（下拉回填，响应回显名称） |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华/光明 |
| industry | string | 否 |  |
| park | string | 否 |  |
| szNote | string | 否 | docx 扩展字段 |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.4.5 深圳企业专项·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/enterprise/sz/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.5 读侧·政策

#### 3.5.1 政策列表（join 视角；默认过滤失效+软删）

`POST /api/open/cms/v1/policy/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| status | object | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.5.2 政策详情

`POST /api/open/cms/v1/policy/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | object | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.5.3 政策下拉

`POST /api/open/cms/v1/policy/suggest`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| limit | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.5.4 已失效政策列表

`POST /api/open/cms/v1/policy/expired`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.6 政策条目


**失效同步口径（2026-10-19 暂定，待书面确认）**：
- 存量失效不同步（对接日前的失效不推送）；仅同步增量
- 增量通知时效 **T+1**：建议每日 **02:00 后**调用本接口，`updated_after` 传上次拉取水位（首日不传=拉全量对账一次）
- 示例：`{ "updated_after": "2026-10-18 02:00:00", "page": 1, "size": 200 }`；分页拉完为止

#### 3.6.1 政策条目·新增

`POST /api/open/cms/v1/policy/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | 是 |  |
| body | string | 是 | 正文/粘贴文本 |
| attachment | string | 否 | 附件 fileId（PDF，上传后引用） |
| publisher | string | 是 |  |
| pubDate | string | 否 |  |
| docNo | string | 否 |  |
| sourceUrl | string | 否 |  |
| industryTag | array<string> | 否 | 枚举: 人工智能/绿色低碳/生物医药/低空经济 |
| regionTag | array<string> | 否 | 枚举: 深圳/广东/全国 |
| reviewStatus | string | 否 | 枚举: 待审核/已校正/需复核 |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.6.2 政策条目·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/policy/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | 否 |  |
| body | string | 否 | 正文/粘贴文本 |
| attachment | string | 否 | 附件 fileId（PDF，上传后引用） |
| publisher | string | 否 |  |
| pubDate | string | 否 |  |
| docNo | string | 否 |  |
| sourceUrl | string | 否 |  |
| industryTag | array<string> | 否 | 枚举: 人工智能/绿色低碳/生物医药/低空经济 |
| regionTag | array<string> | 否 | 枚举: 深圳/广东/全国 |
| reviewStatus | string | 否 | 枚举: 待审核/已校正/需复核 |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.6.3 政策条目·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/policy/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.6.4 删除操作审计·列表（只读，含全部写操作留痕）

`POST /api/open/cms/v1/policy/audit-logs/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<policy_audit_item> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


### 3.7 读侧·服务机构

#### 3.7.1 服务机构列表（join 视角：圈定池∪虚拟）

`POST /api/open/cms/v1/service-org/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code

**请求体补充（live-1.7）**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| action | string | 否 | `新增` / `编辑` / `删除`；**不传=全部写操作**（本接口是写操作审计，非仅删除） |
| keyword | string | 否 | 按政策标题模糊；`%`/`_` 按字面匹配（已转义，不再当通配符） | | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.7.2 服务机构详情

`POST /api/open/cms/v1/service-org/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | object | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.7.3 服务机构下拉

`POST /api/open/cms/v1/service-org/suggest`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| limit | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.8 服务机构实体

#### 3.8.1 服务机构实体·新增

`POST /api/open/cms/v1/service-org/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 |  |
| founded | string | 否 |  |
| contact | string | 否 |  |
| flag | string | 否 | 枚举: 是/否 |
| priority | string | 否 | 枚举: P0/P1/P2/— |
| type | string | 否 | 枚举: 孵化器/加速器/咨询公司/检测机构/路演平台 |
| scope | string | 否 |  |
| cert | string | 否 |  |
| ability | string | 否 |  |
| domain | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.8.2 服务机构实体·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/service-org/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 否 |  |
| founded | string | 否 |  |
| contact | string | 否 |  |
| flag | string | 否 | 枚举: 是/否 |
| priority | string | 否 | 枚举: P0/P1/P2/— |
| type | string | 否 | 枚举: 孵化器/加速器/咨询公司/检测机构/路演平台 |
| scope | string | 否 |  |
| cert | string | 否 |  |
| ability | string | 否 |  |
| domain | string | 否 |  |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.8.3 服务机构实体·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/service-org/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.9 服务机构动态

#### 3.9.1 服务机构动态·列表

`POST /api/open/cms/v1/service-org/news/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |
| keyword | string | 否 |  |
| kind | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<service_org_news> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.9.2 服务机构动态·详情

`POST /api/open/cms/v1/service-org/news/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| title | string | 是 |  |
| kind | string | 否 | 枚举: 服务案例/客户反馈/培训活动/路演对接会 |
| org | array<string> | 是 | 所属机构 org_id 数组 |
| content | string | 否 |  |
| date | string | 否 |  |
| sourceUrl | string | 否 |  |


#### 3.9.3 服务机构动态·新增

`POST /api/open/cms/v1/service-org/news/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | 是 |  |
| kind | string | 否 | 枚举: 服务案例/客户反馈/培训活动/路演对接会 |
| org | array<string> | 是 | 所属机构 org_id 数组 |
| content | string | 否 |  |
| date | string | 否 |  |
| sourceUrl | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.9.4 服务机构动态·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/service-org/news/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | 否 |  |
| kind | string | 否 | 枚举: 服务案例/客户反馈/培训活动/路演对接会 |
| org | array<string> | 否 | 所属机构 org_id 数组 |
| content | string | 否 |  |
| date | string | 否 |  |
| sourceUrl | string | 否 |  |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.9.5 服务机构动态·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/service-org/news/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.10 深圳服务机构专项

#### 3.10.1 深圳服务机构专项·列表

`POST /api/open/cms/v1/service-org/sz/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |
| keyword | string | 否 |  |
| type | string | 否 |  |
| district | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<service_org_sz> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.10.2 深圳服务机构专项·详情

`POST /api/open/cms/v1/service-org/sz/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 | 机构 org_id（下拉回填） |
| type | string | 否 | 枚举: 孵化器/加速器/咨询公司/检测机构 |
| domain | string | 是 |  |
| cert | string | 否 |  |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华 |
| cases | string | 否 | docx 扩展 |
| evaluation | string | 否 | docx 扩展 |
| szNote | string | 否 | docx 扩展 |


#### 3.10.3 深圳服务机构专项·新增

`POST /api/open/cms/v1/service-org/sz/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 | 机构 org_id（下拉回填） |
| type | string | 否 | 枚举: 孵化器/加速器/咨询公司/检测机构 |
| domain | string | 是 |  |
| cert | string | 否 |  |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华 |
| cases | string | 否 | docx 扩展 |
| evaluation | string | 否 | docx 扩展 |
| szNote | string | 否 | docx 扩展 |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.10.4 深圳服务机构专项·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/service-org/sz/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 否 | 机构 org_id（下拉回填） |
| type | string | 否 | 枚举: 孵化器/加速器/咨询公司/检测机构 |
| domain | string | 否 |  |
| cert | string | 否 |  |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华 |
| cases | string | 否 | docx 扩展 |
| evaluation | string | 否 | docx 扩展 |
| szNote | string | 否 | docx 扩展 |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.10.5 深圳服务机构专项·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/service-org/sz/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.11 产品实体

#### 3.11.1 产品实体·列表

`POST /api/open/cms/v1/product/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |
| keyword | string | 否 |  |
| chain | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<product> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.11.2 产品实体·详情

`POST /api/open/cms/v1/product/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 |  |
| orgId | string | 否 | 归属企业 org_id（虚拟产品必填） |
| models | string | 否 | 多型号，逗号分隔 |
| params | string | 否 |  |
| chain | string | 否 | 环节编码（标准∪自定义） |


#### 3.11.3 产品实体·新增

`POST /api/open/cms/v1/product/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 |  |
| orgId | string | 否 | 归属企业 org_id（虚拟产品必填） |
| models | string | 否 | 多型号，逗号分隔 |
| params | string | 否 |  |
| chain | string | 否 | 环节编码（标准∪自定义） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.11.4 产品实体·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/product/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 否 |  |
| orgId | string | 否 | 归属企业 org_id（虚拟产品必填） |
| models | string | 否 | 多型号，逗号分隔 |
| params | string | 否 |  |
| chain | string | 否 | 环节编码（标准∪自定义） |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.11.5 产品实体·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/product/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.12 自定义产业分类

#### 3.12.1 自定义产业分类·列表

`POST /api/open/cms/v1/industry/custom-class/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<industry_custom_class> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.12.2 自定义产业分类·详情

`POST /api/open/cms/v1/industry/custom-class/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| code | string | 是 | 建议 CUS-{seq} |
| name | string | 是 |  |
| level | string | 否 | 枚举: 一级/二级/三级/四级/五级 |
| parent | string | 否 | 上级自定义分类 code；一级为空 |
| order | integer | 否 |  |


#### 3.12.3 自定义产业分类·新增

`POST /api/open/cms/v1/industry/custom-class/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | string | 是 | 建议 CUS-{seq} |
| name | string | 是 |  |
| level | string | 否 | 枚举: 一级/二级/三级/四级/五级 |
| parent | string | 否 | 上级自定义分类 code；一级为空 |
| order | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.12.4 自定义产业分类·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/industry/custom-class/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | string | 否 | 建议 CUS-{seq} |
| name | string | 否 |  |
| level | string | 否 | 枚举: 一级/二级/三级/四级/五级 |
| parent | string | 否 | 上级自定义分类 code；一级为空 |
| order | integer | 否 |  |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.12.5 自定义产业分类·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/industry/custom-class/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.12.6 合并树（标准只读+自定义，自定义可覆盖排序）

`POST /api/open/cms/v1/industry/tree-merged`

**请求体**

_（本接口无额外字段说明，见通用约定）_

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.13 自定义产业链环节

#### 3.13.1 自定义产业链环节·列表

`POST /api/open/cms/v1/industry/custom-link/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<industry_custom_link> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.13.2 自定义产业链环节·详情

`POST /api/open/cms/v1/industry/custom-link/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| code | string | 是 | 建议 CUS-CHAIN-{seq} |
| name | string | 是 |  |
| definition | string | 是 |  |
| order | integer | 否 |  |


#### 3.13.3 自定义产业链环节·新增

`POST /api/open/cms/v1/industry/custom-link/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | string | 是 | 建议 CUS-CHAIN-{seq} |
| name | string | 是 |  |
| definition | string | 是 |  |
| order | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.13.4 自定义产业链环节·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/industry/custom-link/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | string | 否 | 建议 CUS-CHAIN-{seq} |
| name | string | 否 |  |
| definition | string | 否 |  |
| order | integer | 否 |  |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.13.5 自定义产业链环节·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/industry/custom-link/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.13.6 合并环节下拉（标准∪自定义）

`POST /api/open/cms/v1/industry/chain-links-merged`

**请求体**

_（本接口无额外字段说明，见通用约定）_

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.14 产业动态资讯

#### 3.14.1 产业动态资讯·列表

`POST /api/open/cms/v1/industry/news/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |
| keyword | string | 否 |  |
| kind | string | 否 |  |
| status | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<industry_news> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.14.2 产业动态资讯·详情

`POST /api/open/cms/v1/industry/news/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| title | string | 是 |  |
| kind | string | 否 | 枚举: 政策/报告/重大事件/市场动态 |
| content | string | 是 |  |
| date | string | 否 |  |
| status | string | 否 | 枚举: 有效/归档 |
| sourceUrl | string | 否 |  |


#### 3.14.3 产业动态资讯·新增

`POST /api/open/cms/v1/industry/news/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | 是 |  |
| kind | string | 否 | 枚举: 政策/报告/重大事件/市场动态 |
| content | string | 是 |  |
| date | string | 否 |  |
| status | string | 否 | 枚举: 有效/归档 |
| sourceUrl | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.14.4 产业动态资讯·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/industry/news/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | 否 |  |
| kind | string | 否 | 枚举: 政策/报告/重大事件/市场动态 |
| content | string | 否 |  |
| date | string | 否 |  |
| status | string | 否 | 枚举: 有效/归档 |
| sourceUrl | string | 否 |  |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.14.5 产业动态资讯·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/industry/news/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.15 区域企业名录

#### 3.15.1 区域企业名录·列表

`POST /api/open/cms/v1/industry/region-roster/list`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |
| keyword | string | 否 |  |
| district | string | 否 |  |
| scale | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| records | array<industry_region_roster> | 否 |  |
| total | integer | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |


#### 3.15.2 区域企业名录·详情

`POST /api/open/cms/v1/industry/region-roster/detail`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 | 企业名称（下拉回填或手填） |
| industry | string | 是 |  |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华/光明 |
| scale | string | 否 | 枚举: 大型/中型/小型/微型企业 |


#### 3.15.3 区域企业名录·新增

`POST /api/open/cms/v1/industry/region-roster/create`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 | 企业名称（下拉回填或手填） |
| industry | string | 是 |  |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华/光明 |
| scale | string | 否 | 枚举: 大型/中型/小型/微型企业 |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.15.4 区域企业名录·编辑（body 只带被改字段，字段级合并）

`POST /api/open/cms/v1/industry/region-roster/update`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 否 | 企业名称（下拉回填或手填） |
| industry | string | 否 |  |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华/光明 |
| scale | string | 否 | 枚举: 大型/中型/小型/微型企业 |
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.15.5 区域企业名录·删除（软删+审计；被引用返回 40901）

`POST /api/open/cms/v1/industry/region-roster/delete`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.16 图谱·阶段定义

#### 3.16.1 阶段定义·列表（类型级通用配置）

`POST /api/open/cms/v1/kg/{entityType}/stages/list`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.16.2 阶段定义·新增

`POST /api/open/cms/v1/kg/{entityType}/stages/create`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| stageName | string | 是 |  |
| feature | string | 是 |  |
| metric | string | 否 | 衡量指标，如：产值增速 > 25% |
| order | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.16.3 阶段定义·编辑

`POST /api/open/cms/v1/kg/{entityType}/stages/update`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| stageName | string | 否 |  |
| feature | string | 否 |  |
| metric | string | 否 |  |
| order | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.16.4 阶段定义·删除

`POST /api/open/cms/v1/kg/{entityType}/stages/delete`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.17 图谱·实体生命周期

#### 3.17.1 实体能量列表（实体 join 当前状态）

`POST /api/open/cms/v1/kg/{entityType}/entities`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| stage | any | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.17.2 状态标记（新增或更新当前状态；extra 按类型装专属字段）

`POST /api/open/cms/v1/kg/{entityType}/status/mark`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| entityId | string | 是 |  |
| stage | string | 是 |  |
| since | string | 是 |  |
| event | string | 是 | 关键事件 |
| extra | object | 否 | 类型专属：enterprise=financing/operation；industry=stageInfo/linkedMetric；policy=scope/effect；service=scale/customers |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.17.3 状态历史（时间倒序）

`POST /api/open/cms/v1/kg/{entityType}/status/history`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| entityId | object | 是 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.18 图谱·关系链

#### 3.18.1 关系·列表

`POST /api/open/cms/v1/kg/{entityType}/relations/list`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 | 命中源/目标实体名 |
| status | object | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |

**`data.records[]` 字段**：id（关系行id）、fromEntityId/fromName（源实体）、type（关系类型）、toEntityId/toName（目标实体）、status（状态）、since（建立时间）、**remark（关系说明）**、breakTime（断裂时间，仅已断裂）。


#### 3.18.2 关系·详情

`POST /api/open/cms/v1/kg/{entityType}/relations/detail`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |

**`data` 字段**：id、fromEntityId/fromName（源实体）、type（关系类型）、toEntityId/toName（目标实体）、status（状态）、since（建立时间）、**remark（关系说明）**、breakTime（断裂时间，仅已断裂）。


#### 3.18.3 关系·新建

`POST /api/open/cms/v1/kg/{entityType}/relations/create`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromEntityId | string | 是 |  |
| type | string | 是 | 自由文本：上游供给/合作/竞争 |
| toEntityId | string | 是 |  |
| status | string | 否 | 已断裂仅 break 动作置入；枚举: 新建/稳定/强化中/演进中 |
| since | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.18.4 关系·编辑

`POST /api/open/cms/v1/kg/{entityType}/relations/update`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromEntityId | string | 否 |  |
| type | string | 否 | 自由文本：上游供给/合作/竞争 |
| toEntityId | string | 否 |  |
| status | string | 否 | 已断裂仅 break 动作置入；枚举: 新建/稳定/强化中/演进中 |
| since | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.18.5 关系·删除（软删+审计；误建清理用）

`POST /api/open/cms/v1/kg/{entityType}/relations/delete`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.18.6 关系·标记断裂（不物理删，badge 灰化）

`POST /api/open/cms/v1/kg/{entityType}/relations/break`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | object | 是 |  |
| reason | object | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.18.7 关系·演变历史

`POST /api/open/cms/v1/kg/{entityType}/relations/history`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.19 图谱·实体属性

#### 3.19.1 属性·列表（扁平+base/dyn 双分组）

`POST /api/open/cms/v1/kg/{entityType}/attrs/list`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| group | object | 否 | 枚举: base/dyn |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |

**`data.records[]` 字段**：id（属性行id）、name（属性名）、group（base基础/dyn动态）、dtype（数据类型）、**definition（定义）**、**unit（单位）**、constraint（约束条件）、value（当前值）、order（排序）。


#### 3.19.2 属性·新增

`POST /api/open/cms/v1/kg/{entityType}/attrs/create`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 是 |  |
| group | string | 否 | 枚举: base/dyn |
| dtype | string | 否 | 枚举: 文本/数值/整数/枚举/日期/百分比/多值 |
| constraint | string | 否 |  |
| value | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |

**`data.records[]` 字段**：id（属性行id）、name（属性名）、group（base基础/dyn动态）、dtype（数据类型）、**definition（定义）**、**unit（单位）**、constraint（约束条件）、value（当前值）、order（排序）。


#### 3.19.3 属性·编辑

`POST /api/open/cms/v1/kg/{entityType}/attrs/update`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 否 |  |
| group | string | 否 | 枚举: base/dyn |
| dtype | string | 否 |  |
| constraint | string | 否 |  |
| value | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |

**`data.records[]` 字段**：id（属性行id）、name（属性名）、group（base基础/dyn动态）、dtype（数据类型）、**definition（定义）**、**unit（单位）**、constraint（约束条件）、value（当前值）、**version（版本号，每次编辑 +1）**、order（排序）。


#### 3.19.4 属性·删除

`POST /api/open/cms/v1/kg/{entityType}/attrs/delete`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.19.5 属性·变更记录 / 多版本管理

`POST /api/open/cms/v1/kg/{entityType}/attrs/history`

> 对应原型：产业「变更记录」、政策「多版本管理」。数据来自 `cms_op_audit`（`KG_ATTR`），按属性表 `entity_type` 过滤；**任一字段编辑成功后 `version` 累加 +1**。

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| attrId | string | 否 | 只看某属性行 |
| name | string | 否 | 按属性名精确过滤 |
| group | string | 否 | `base` / `dyn`；传 `basic` 视同 `base`（兼容前端）；政策「多版本管理」传 `base` 只看基础属性 |
| page | integer | 否 | 默认 1 |
| size | integer | 否 | 默认 20，上限 100 |

**响应 `data`**

| 字段 | 类型 | 说明 |
|---|---|---|
| total / page / size | integer | 分页 |
| records[] | array | 变更行 |

**`data.records[]` 字段**：attrId、action（新增/编辑/删除）、operator、reason、name、group、version、snapshot（改前/创建快照对象）、time。


#### 3.19.6 属性·当前值 + 版本号

`POST /api/open/cms/v1/kg/{entityType}/attrs/current`

> 多版本对比时拉取当前态。

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| attrId | string | 是 | 属性行 id |

**响应 `data` 字段**：attrId、name、definition、unit、value、version。


#### 3.19.7 属性·下载 CSV 导入模板

`POST /api/open/cms/v1/kg/{entityType}/attrs/template`

> 对应原型：企业基本信息管理「下载 CSV 模板」。四列：`属性名称,属性定义,数据类型,单位`。

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service（企业为主入口，其他类型同样可用） |

**请求体**：可空 `{}`。

**响应 `data` 字段**：filename、contentType（`text/csv;charset=utf-8`）、csv（含 BOM 的 CSV 原文，前端直接落盘即可）。


#### 3.19.8 属性·批量导入

`POST /api/open/cms/v1/kg/{entityType}/attrs/import`

> 对应原型：企业基本信息管理「批量导入」。四列均必填；`dtype` 枚举同新增；同名未删行则更新（version+1），否则新增；`group` 缺省 `base`。

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {entityType} | 取值: industry / enterprise / policy / service |

**请求体（二选一）**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| rows | array | 与 csv 二选一 | `[{name, definition, dtype, unit}, ...]` |
| csv | string | 与 rows 二选一 | CSV 原文（可含表头） |
| group | string | 否 | `base` / `dyn`，缺省 `base` |

**响应 `data` 字段**：total、created、updated、failed、records[]（每项：name、id、action=`created|updated|failed`、error?）。


### 3.19.9 智能搜索·企业

`POST /api/open/cms/v1/smart-search/enterprise`

> 复用专题系统企业智能检索链路（关键词包含匹配，多词 AND）。行内字段原样透传，不解释不改写。

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | string | 是 | 关键词（多词空格分隔） |
| country_location_ids | string[] | 否 | 久新地区码数组（live-1.6 新增；不传=不过滤） |
| industry_ids | string[] | 否 | 产业码（INB*）或产业领域码（CL-*）数组（live-1.6 新增；领域自动展开旗下产业；不传=不过滤）。匹配语义：产业码前缀覆盖子链。返回 records 纯新增 `industry_id`/`industry_name`（数据所属产业就近上浮，可能为 null） |
| page | integer | 否 | 默认 1 |
| size | integer | 否 | 默认 20，上限 100 |

**地区筛选语义**：`country_location_id` 经智树侧映射为自有国家码后真实过滤（国内+海外企业均覆盖）；映射不上的码（如多数小国）→ 查询结果为空；国内索引现全为 CHN，海外索引数据接入后自动生效。


**调用示例**

```json
// 请求（关键词 + 产业 + 地区组合筛选）
{
  "keyword": "半导体",
  "industry_ids": ["INB1303", "CL-SEI-01"],
  "country_location_ids": ["loc_B56D89F0452662FBF49EAAD21C2A630E"],
  "page": 1,
  "size": 2
}
```

```json
// 响应（截断；records 行内为透传字段 + 新增 industry_id/industry_name）
{
  "code": 0,
  "msg": "ok",
  "data": {
    "total": 3547,
    "page": 1,
    "size": 2,
    "records": [
      {
        "org_id": "29961637",
        "name_cn": "深圳市红阳电池有限公司",
        "social_credit_code": "91440300757642670R",
        "industry_id": "INB1303",
        "industry_name": "集成电路",
        "...": "其余透传字段略"
      }
    ]
  }
}
```

> `country_location_ids` 里的码为久新侧 `country_location_id` 原值（如中国=`loc_B56D89F0452662FBF49EAAD21C2A630E`），智树侧自动映射自有国家码；映射不上的码查询结果为空。

**响应 `data`**：`{total, page, size, records[]}`；records 为企业文档（org_id / name_cn / social_credit_code / 行业 / 地区等，全量字段以实际返回为准）。

### 3.19.10 智能搜索·产业

`POST /api/open/cms/v1/smart-search/industry`

**请求体**：同 3.19.9。
> live-1.6：支持 `country_location_ids`（收下忽略——产业无地区概念）与 `industry_ids`（按 id/stableId 前缀后置过滤，返回 total 同步收缩）。


**调用示例**

```json
// 请求（纯产业筛选，keyword 可省略）
{
  "keyword": "",
  "industry_ids": ["INB1303"],
  "page": 1,
  "size": 5
}
```

```json
// 响应（截断）
{
  "code": 0,
  "msg": "ok",
  "data": {
    "total": 7,
    "page": 1,
    "size": 5,
    "records": [
      {"id": "INB1303", "stableId": "industry:INB1303", "objectType": "industry", "name": "集成电路", "...": "略"},
      {"id": "INB130301", "name": "半导体材料", "...": "略"},
      {"id": "INB130302", "name": "EDA/IP核", "...": "略"}
    ]
  }
}
```

**响应 `data`**：`{total, page, size, records[]}`；records 为产业链节点（id / stableId / objectType / name / aliases / tags 等）。

### 3.19.11 智能搜索·政策

`POST /api/open/cms/v1/smart-search/policy`

**请求体**：同 3.19.9（page/size 自动换算下游 limit/offset）。
> live-1.6：支持 `country_location_ids`；当前仅国内数据——传「中国」放行正常查，传其他地区快速返回空。


**调用示例**

```json
// 请求（关键词 + 中国地区码；政策当前仅国内数据）
{
  "keyword": "人才",
  "country_location_ids": ["loc_B56D89F0452662FBF49EAAD21C2A630E"],
  "industry_ids": ["INB1303"],
  "page": 1,
  "size": 2
}
```

```json
// 响应（截断）
{
  "code": 0,
  "msg": "ok",
  "data": {
    "total": 9,
    "page": 1,
    "size": 2,
    "records": [
      {"policy_id": "18359183", "title": "关于开展…人才…培训工作的通知", "...": "略"}
    ]
  }
}
```

> 传非中国的 `country_location_id` → 直接返回空 `records`（当前政策仅国内数据）。

**响应 `data`**：`{total, page, size, records[]}`；records 为政策条目（policy_id / title 等）。

### 3.19.12 智能搜索·服务机构

`POST /api/open/cms/v1/smart-search/service`

**请求体**：同 3.19.9。
> live-1.6：支持 `country_location_ids`；当前仅国内数据——传「中国」放行正常查，传其他地区快速返回空。


**调用示例**

```json
// 请求（关键词 + 产业 + 中国地区码）
{
  "keyword": "检验",
  "industry_ids": ["INB1303"],
  "country_location_ids": ["loc_B56D89F0452662FBF49EAAD21C2A630E"],
  "page": 1,
  "size": 2
}
```

```json
// 响应（截断）
{
  "code": 0,
  "msg": "ok",
  "data": {
    "total": 95,
    "page": 1,
    "size": 2,
    "records": [
      {"org_id": "79bbcfc0e68027808f1f4caf1b6f0469", "service_org_code": "…", "name_cn": "东莞兰卫医学检验实验室有限公司", "...": "略"}
    ]
  }
}
```

> 传非中国的 `country_location_id` → 直接返回空 `records`（当前服务机构仅国内数据）。

**响应 `data`**：`{total, page, size, records[]}`；records 为服务机构文档（org_id / service_org_code / name_cn 等）。

### 3.20 专家知识

#### 3.20.1 专家知识·列表

`POST /api/open/cms/v1/expert/{domain}/list`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {domain} | 取值: industry / enterprise / policy / service / region |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| keyword | object | 否 |  |
| sectionId | object | 否 |  |
| page | integer | 否 |  |
| size | integer | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.20.2 专家知识·详情

`POST /api/open/cms/v1/expert/{domain}/detail`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {domain} | 取值: industry / enterprise / policy / service / region |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.20.3 专家知识·新增

`POST /api/open/cms/v1/expert/{domain}/create`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {domain} | 取值: industry / enterprise / policy / service / region |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| sectionId | string | 是 | section 标识（12 个，见规格 §6.1–§6.5） |
| title | string | 是 |  |
| entity | object | 是 | {entityType, entityId, name}；region 为自由文本 |
| expert | string | 否 |  |
| content | object | 是 | 按 section 字段定义的有序键值对（键=拼音蛇形） |
| view | string | 否 | 缺省取 content 首个非空值 |
| conclusion | string | 否 | 缺省取 content 末字段 |
| evidence | string | 否 |  |
| sourceType | string | 否 |  |
| source | string | 否 |  |
| advice | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.20.4 专家知识·编辑

`POST /api/open/cms/v1/expert/{domain}/update`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {domain} | 取值: industry / enterprise / policy / service / region |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| sectionId | string | 否 | section 标识（12 个，见规格 §6.1–§6.5） |
| title | string | 否 |  |
| entity | object | 否 | {entityType, entityId, name}；region 为自由文本 |
| expert | string | 否 |  |
| content | object | 否 | 按 section 字段定义的有序键值对（键=拼音蛇形） |
| view | string | 否 | 缺省取 content 首个非空值 |
| conclusion | string | 否 | 缺省取 content 末字段 |
| evidence | string | 否 |  |
| sourceType | string | 否 |  |
| source | string | 否 |  |
| advice | string | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.20.5 专家知识·删除

`POST /api/open/cms/v1/expert/{domain}/delete`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {domain} | 取值: industry / enterprise / policy / service / region |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.20.6 专家知识·section 元数据（id/名称/字段定义有序数组，供前端动态渲染表单）

`POST /api/open/cms/v1/expert/{domain}/sections`

**路径枚举段**

| 字段 | 说明 |
|---|---|
| {domain} | 取值: industry / enterprise / policy / service / region |

**请求体**

_（本接口无额外字段说明，见通用约定）_

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.21 读侧·产业

#### 3.21.1 标准产业分类树

`POST /api/open/cms/v1/industry/tree`

**请求体**

_（本接口无额外字段说明，见通用约定）_

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


#### 3.21.2 标准产业链环节

`POST /api/open/cms/v1/industry/chain-links`

**请求体**

_（本接口无额外字段说明，见通用约定）_

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


### 3.22 读侧·批量

#### 3.22.1 实体基础信息批量查询（ids；不返关系/属性）

`POST /api/open/cms/v1/bulk/entities`

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| ids | array<string> | 否 |  |

**响应 `data`**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | integer | 否 |  |
| msg | string | 否 |  |
| data | object | 否 |  |


---

### 3.18.1.1 关系类型字典（2026-10-27 新增，四端点）

`{entityType}` ∈ enterprise | policy | service

| 操作 | 接口 | body |
|---|---|---|
| 列表 | `POST .../relation-types/list` | `{}` |
| 新增 | `POST .../relation-types/create` | `{"name":"类型名"}` |
| 编辑 | `POST .../relation-types/update` | `{"id":"1","name":"新名"}` |
| 删除 | `POST .../relation-types/delete` | `{"id":"1","reason":"原因"}`（被关系引用时 40901） |

新建关系弹窗的"关系类型"建议改从此接口下拉取值（替代手填）。

### 3.18.1.2 关系定义层（2026-10-27 新增，四端点，方案 A）

带富字段的关系定义层：除名称外含定义描述 + 该类实体专属字段（extra 对象：enterprise=mode 合作模式/terms 合同条款；policy=effect 执行效果/feedback 反馈；service=content 服务内容/effect 服务效果；industry=participants 参与方）。

| 操作 | 接口 | body |
|---|---|---|
| 列表 | `POST .../rel-defs/list` | `{}` |
| 新增 | `POST .../rel-defs/create` | `{"name":"…","definition":"…","extra":{…},"order":1}` |
| 编辑 | `POST .../rel-defs/update` | `{"id":"…","name":"…","definition":"…","extra":{…}}` |
| 删除 | `POST .../rel-defs/delete` | `{"id":"…","reason":"原因"}`（被关系实例引用时 40901） |

原型对照：企业=企业合作链定义（联合研发/供应链协作）、政策=政策传导关系定义（纵向/跨部门）、服务=服务机构引扶（客户服务/合作伙伴）、产业=产业链关系定义（上游供给/下游应用）——seed 已按原型预置八条。

---



```
POST /api/open/cms/v1/kg/{entityType}/relations/insight
{entityType} ∈ enterprise | policy | service
```

对一条已存在的关系链，调用大模型生成「策略/分析意见」文本。

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 | 关系行 id（从 `/relations/list` 返回的 `id` 取） |
| force | boolean | 否 | `true`=忽略缓存强制重新生成；缺省 false |

**响应 data**

| 字段 | 说明 |
|---|---|
| id | 关系行 id |
| insight | 生成的策略/分析意见文本（中文） |
| model | 生成模型（如 glm-5.3-flash） |
| cached | `true`=命中缓存直接返回；`false`=本次新生成 |
| generatedAt | 生成时间（缓存命中时为上次生成时间） |

**缓存规则**：结果落库保存，同一关系再次调用直接秒回缓存；关系内容被编辑后缓存自动失效、下次调用重新生成；`force: true` 跳过缓存强制重生成。LLM 失败/超时（约 60s）→ 返回 `insight: ""` 且 `degraded: true`（HTTP 仍 200），稍后重试即可。

**前端注意**：不要进页面就自动调（会重复消耗配额）；用户点「生成/重新生成」按钮才调用，期间提示"AI 生成中（约 10-30 秒）"。

curl 示例：

```bash
curl -X POST 'http://10.50.69.111:30895/cms/api/open/cms/v1/kg/policy/relations/insight' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -H 'X-CMS-Api-Key: <Key>' \
  -d '{"id":"1"}'
```

---

## 4. 数据模型（摘录）

以下为 OpenAPI `components.schemas` 中与对接相关的主要模型；字段以接口实际返回为准。

### 4.DeleteBody

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |
| reason | string | 是 | 删除原因（必填，入审计） |


### 4.DetailBody

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 |  |


### 4.enterprise

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 | 企业名称；覆盖写 overlay |
| regInfo | string | 否 | 工商注册信息摘录 |
| founded | string | 否 | 成立时间 |
| capital | string | 否 | 注册资本 |
| type | string | 否 | 运营分类标签；枚举: 高新技术企业/专精特新/上市公司/初创企业 |
| industry | string | 否 | 运营行业标签；枚举: 人工智能/生物医药/高端装备/新能源 |
| scale | string | 否 | 枚举: 大型/中型/小型 |
| isKey | string | 否 | 是否重点企业；枚举: 是/否 |
| flag | string | 否 | 枚举: 龙头/潜力/观察/风险关注 |
| priority | string | 否 | 枚举: P0/P1/P2/P3 |
| reason | string | 否 | 标识原因 |
| external_id | string | 否 | 只读回显（不可改） |
| province | string | 否 | 只读回显（不可改） |
| city | string | 否 | 只读回显（不可改） |
| area | string | 否 | 只读回显（不可改） |
| org_type | string | 否 | 只读回显（不可改） |
| reg_status | string | 否 | 只读回显（不可改） |
| industry_l1_name | string | 否 | 只读回显（不可改） |
| industry_code | string | 否 | 只读回显（不可改） |
| is_high_tech | string | 否 | 只读回显（不可改） |
| is_little_giant | string | 否 | 只读回显（不可改） |
| is_listed | string | 否 | 只读回显（不可改） |
| is_unicorn | string | 否 | 只读回显（不可改） |
| is_gazelle | string | 否 | 只读回显（不可改） |


### 4.enterprise_news

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| title | string | 是 |  |
| company | array<string> | 是 | 关联企业 org_id 数组（多选） |
| kind | string | 否 | 枚举: 新闻公告/财报摘要/法律诉讼/行政处罚/舆情事件 |
| content | string | 是 |  |
| risk | string | 否 | 枚举: 低/中/高 |
| status | string | 否 | 枚举: 有效/已过期/已归档 |
| date | string | 否 |  |
| sourceUrl | string | 否 |  |


### 4.enterprise_sz

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 | 企业 org_id（下拉回填，响应回显名称） |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华/光明 |
| industry | string | 是 |  |
| park | string | 否 |  |
| szNote | string | 否 | docx 扩展字段 |


### 4.policy

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| title | string | 是 |  |
| body | string | 是 | 正文/粘贴文本 |
| attachment | string | 否 | 附件 fileId（PDF，上传后引用） |
| publisher | string | 是 |  |
| pubDate | string | 否 |  |
| docNo | string | 否 |  |
| sourceUrl | string | 否 |  |
| industryTag | array<string> | 否 | 枚举: 人工智能/绿色低碳/生物医药/低空经济 |
| regionTag | array<string> | 否 | 枚举: 深圳/广东/全国 |
| reviewStatus | string | 否 | 枚举: 待审核/已校正/需复核 |
| status | string | 否 | 只读回显（不可改） |
| level | string | 否 | 只读回显（不可改） |
| source | string | 否 | 只读回显（不可改） |
| region | string | 否 | 只读回显（不可改） |


### 4.policy_audit_item

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| time | object | 否 |  |
| operator | object | 否 |  |
| action | object | 否 | CREATE\|UPDATE\|DELETE... |
| title | object | 否 |  |
| reason | object | 否 |  |


### 4.service_org

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 |  |
| founded | string | 否 |  |
| contact | string | 否 |  |
| flag | string | 否 | 枚举: 是/否 |
| priority | string | 否 | 枚举: P0/P1/P2/— |
| type | string | 否 | 枚举: 孵化器/加速器/咨询公司/检测机构/路演平台 |
| scope | string | 否 |  |
| cert | string | 否 |  |
| ability | string | 否 |  |
| domain | string | 否 |  |
| province | string | 否 | 只读回显（不可改） |
| city | string | 否 | 只读回显（不可改） |
| area | string | 否 | 只读回显（不可改） |
| org_size | string | 否 | 只读回显（不可改） |
| phone_num | string | 否 | 只读回显（不可改） |


### 4.service_org_news

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| title | string | 是 |  |
| kind | string | 否 | 枚举: 服务案例/客户反馈/培训活动/路演对接会 |
| org | array<string> | 是 | 所属机构 org_id 数组 |
| content | string | 否 |  |
| date | string | 否 |  |
| sourceUrl | string | 否 |  |


### 4.service_org_sz

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 | 机构 org_id（下拉回填） |
| type | string | 否 | 枚举: 孵化器/加速器/咨询公司/检测机构 |
| domain | string | 是 |  |
| cert | string | 否 |  |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华 |
| cases | string | 否 | docx 扩展 |
| evaluation | string | 否 | docx 扩展 |
| szNote | string | 否 | docx 扩展 |


### 4.product

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 |  |
| orgId | string | 否 | 归属企业 org_id（虚拟产品必填） |
| models | string | 否 | 多型号，逗号分隔 |
| params | string | 否 |  |
| chain | string | 否 | 环节编码（标准∪自定义） |


### 4.industry_custom_class

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| code | string | 是 | 建议 CUS-{seq} |
| name | string | 是 |  |
| level | string | 否 | 枚举: 一级/二级/三级/四级/五级 |
| parent | string | 否 | 上级自定义分类 code；一级为空 |
| order | integer | 否 |  |


### 4.industry_custom_link

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| code | string | 是 | 建议 CUS-CHAIN-{seq} |
| name | string | 是 |  |
| definition | string | 是 |  |
| order | integer | 否 |  |


### 4.industry_news

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| title | string | 是 |  |
| kind | string | 否 | 枚举: 政策/报告/重大事件/市场动态 |
| content | string | 是 |  |
| date | string | 否 |  |
| status | string | 否 | 枚举: 有效/归档 |
| sourceUrl | string | 否 |  |


### 4.industry_region_roster

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| name | string | 是 | 企业名称（下拉回填或手填） |
| industry | string | 是 |  |
| district | string | 否 | 枚举: 南山/福田/宝安/龙岗/龙华/光明 |
| scale | string | 否 | 枚举: 大型/中型/小型/微型企业 |


### 4.expert_item

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 否 | 业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8} |
| sectionId | string | 是 | section 标识（12 个，见规格 §6.1–§6.5） |
| title | string | 是 |  |
| entity | object | 是 | {entityType, entityId, name}；region 为自由文本 |
| expert | string | 否 |  |
| content | object | 是 | 按 section 字段定义的有序键值对（键=拼音蛇形） |
| view | string | 否 | 缺省取 content 首个非空值 |
| conclusion | string | 否 | 缺省取 content 末字段 |
| evidence | string | 否 |  |
| sourceType | string | 否 |  |
| source | string | 否 |  |
| advice | string | 否 |  |


---

## 5. 导入 Apifox / Postman

1. 打开 Apifox → 项目 → **导入** → OpenAPI
2. 选择同目录文件：`CMS-JX-OpenAPI-v1.0-live.json`
3. 导入后在 Apifox 内生成**分享链接**发给联调同学（分享链需贵司 Apifox 空间权限，本侧无法代开公网链接）

如只需阅读，直接使用本文档即可。
