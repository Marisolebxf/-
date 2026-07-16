# Handoff：ENT-ARCH-API-CONTRACT（企业维度 OpenAPI 契约草案）

- 时间：2026-07-16
- 作者：api-agent（执行人：侯佳伟）
- 支撑基线：`agent-delivery/architecture-baseline.md`、`agent-delivery/task-registry.yaml`、`agent-delivery/agent-handoffs/企业战略分析-ENT/DATA-ENT-impl-path-signoff.md`、`demo-svc-topic-py/docs/API-接口文档.md`
- 仓库：`lumen-svc-platform`
- 模块：`gkxlumen-topic-enterprise`
- 分支：本地工作区（本次仅完成代码骨架与本地编译验证，未创建独立 commit / PR）
- 任务 ID：`ENT-ARCH-API-CONTRACT`
- 当前边界：本 handoff 仅提交执行事实、证据、偏离项与待处理事项；`task-registry.yaml` 状态更新、成本字段落库、后续派单由编排侧处理

## 任务范围说明

> 本任务目标是基于企业维度架构设计与 Python 76 端点文档，完成企业维度 Java 门面服务的 OpenAPI 契约草案与第一版实现骨架。

本次实际完成内容如下：

1. 在 `lumen-svc-platform` 中新建 `gkxlumen-topic-enterprise` 模块，并建立 `api / biz` 双层结构。
2. 在 `api` 层补齐企业维度第一版公共契约：
  - 请求 DTO
  - 对外 Feign 契约 `RemoteTopicEnterpriseService`
3. 在 `biz` 层将占位控制器调整为真实门面结构：
  - `Controller -> Service -> Python Feign Client`
4. 将网关路径 `gateway地址/enterprise/topic/v1/**`（`@EnableOpenApi("enterprise")` + `@RequestMapping("/topic/v1")`）下的第一版正式接口骨架映射完成，覆盖：
  - `search`
  - `compare-basket`
  - `profile`
  - 部分 `meta`
5. 按当前团队要求补齐类、字段、方法中文注释。
6. 完成本机 `Maven + JDK17` 编译链路验证。



## 产物清单


| 产物           | 路径（相对 `lumen-svc-platform/`）                                                                                                                                 | 说明                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| 企业模块父工程      | `gkxlumen-topic-enterprise/pom.xml`                                                                                                                          | 企业维度专题服务父模块                                                   |
| API 子模块      | `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/`                                                                                                   | 公共 DTO + 对外 Feign 契约                                          |
| Biz 子模块      | `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/`                                                                                                   | Controller / Service / Python Client                          |
| 对外 Feign 契约  | `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/src/main/java/com/topcomm/gkxlumen/topic/enterprise/api/feign/RemoteTopicEnterpriseService.java`    | 提供给其他 Java 服务调用企业专题服务                                         |
| Python 下游客户端 | `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/src/main/java/com/topcomm/gkxlumen/topic/enterprise/feign/RemoteEnterprisePythonClient.java`        | 仅供当前 biz 模块内部调用 Python                                        |
| 门面控制器        | `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/src/main/java/com/topcomm/gkxlumen/topic/enterprise/controller/EnterpriseOpenApiController.java`    | 暴露网关路径 `gateway地址/enterprise/topic/v1/**`（服务内 `/topic/v1/**`） |
| 门面服务接口       | `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/src/main/java/com/topcomm/gkxlumen/topic/enterprise/service/EnterpriseOpenApiService.java`          | 定义控制层与适配层之间的服务契约                                              |
| 门面服务实现       | `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/src/main/java/com/topcomm/gkxlumen/topic/enterprise/service/impl/EnterpriseOpenApiServiceImpl.java` | 将 Java 门面逐个映射到 Python 接口                                      |




## 范围与实现



### 1. 模块结构

本次在 `lumen-svc-platform` 中新增企业维度专题服务模块：

```text
gkxlumen-topic-enterprise/
├─ gkxlumen-topic-enterprise-api
└─ gkxlumen-topic-enterprise-biz
```

其中：

- `api` 负责公共 DTO、对外 Feign 契约、框架内跨服务调用接口。
- `biz` 负责 HTTP 门面、服务编排、调用 Python 下游服务。



### 2. 当前 Java 门面分层

```text
前端 / 其他 Java 服务
        ↓
gateway地址/enterprise/topic/v1/**
        ↓
EnterpriseOpenApiController  (@RequestMapping("/topic/v1"))
        ↓
EnterpriseOpenApiService
        ↓
RemoteEnterprisePythonClient
        ↓
Python: /api/gkx-search/**
```

本次已经将原占位返回改为真实门面调用链，控制器不再拼装假数据。

### 2.1 对外路由拼接规则（凡 `lumen-svc-platform` / `gkxlumen-*` 下新 Controller / 新服务统一遵守）

对外完整路径按以下四段拼接，**不要**再写成 `/topic/v1/enterprise/`**：

```text
gateway地址 / {EnableOpenApi value} / {Controller @RequestMapping} / {方法映射}
```

本模块当前取值：


| 段             | 来源                                | 当前值                        |
| ------------- | --------------------------------- | -------------------------- |
| gateway地址     | Swagger / 网关基址                    | 例如 `http://127.0.0.1:9999` |
| OpenAPI 前缀    | `@EnableOpenApi("enterprise")`    | `/enterprise`              |
| Controller 前缀 | `@RequestMapping("/topic/v1")`    | `/topic/v1`                |
| 方法路径          | 如 `@PostMapping("/search/query")` | `/search/query`            |


示例：

- 网关完整路径：`POST gateway地址/enterprise/topic/v1/search/query`
- 服务内路径（直连 biz / Feign 调服务本身）：`POST /topic/v1/search/query`

说明：网关通常按 OpenAPI 前缀做 `Path=/enterprise/**` 并 `StripPrefix=1`，下游实际命中 Controller 的 `/topic/v1/**`。

### 3. 已落地接口骨架与契约明细

以下接口说明按“文本说明 + 入参字段表 + 返回字段表 + JSON 示例”组织。接口路径一律写网关完整路径：`gateway地址/enterprise` + Controller 映射 + 方法映射。

#### 3.1 搜索类接口



##### 1. 企业复合检索

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/query`
- 接口用途：企业复合检索，支持关键词、筛选条件、排序和分页。
- 请求对象：`EnterpriseSearchRequest`
- 返回对象：`R<EnterpriseResponseDTOs.SearchResponse>`

入参字段表：


| 字段           | 类型                    | 必填  | 说明                      |
| ------------ | --------------------- | --- | ----------------------- |
| `keyword`    | `String`              | 否   | 关键词检索文本                 |
| `filters`    | `Map<String, Object>` | 否   | 扁平筛选条件集合                |
| `query_tree` | `Map<String, Object>` | 否   | 高级筛选查询树                 |
| `sort_field` | `String`              | 否   | 排序字段                    |
| `sort_order` | `String`              | 否   | 排序方向，通常为 `asc` / `desc` |
| `page`       | `Integer`             | 否   | 当前页码                    |
| `size`       | `Integer`             | 否   | 每页条数                    |


请求 JSON 示例：

```json
{
  "keyword": "科技",
  "filters": {
    "risk_level": "低"
  },
  "query_tree": {
    "logic": "AND",
    "conditions": []
  },
  "sort_field": "competitiveness_score",
  "sort_order": "desc",
  "page": 1,
  "size": 20
}
```

返回字段表：


| 字段           | 类型                 | 说明       |
| ------------ | ------------------ | -------- |
| `code`       | `Integer`          | 统一响应码    |
| `msg`        | `String`           | 统一响应消息   |
| `data.list`  | `List<SearchItem>` | 企业检索结果列表 |
| `data.total` | `Long`             | 命中企业总数   |
| `data.page`  | `Integer`          | 当前页码     |
| `data.size`  | `Integer`          | 每页条数     |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "org_id": "ent_001",
        "name_cn": "深圳某科技有限公司",
        "industry_class_name": "电子信息",
        "competitiveness_score": 87.5,
        "risk_level": "低"
      }
    ],
    "total": 128,
    "page": 1,
    "size": 20
  }
}
```



##### 2. 企业输入联想

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/suggest`
- 接口用途：企业名称输入联想。
- 请求对象：`EnterpriseSuggestRequest`
- 返回对象：`R<List<EnterpriseResponseDTOs.SuggestItem>>`

入参字段表：


| 字段       | 类型        | 必填  | 说明        |
| -------- | --------- | --- | --------- |
| `prefix` | `String`  | 是   | 联想前缀字符串   |
| `size`   | `Integer` | 否   | 期望返回的候选数量 |


请求 JSON 示例：

```json
{
  "prefix": "深",
  "size": 10
}
```

返回字段表：


| 字段               | 类型                  | 说明     |
| ---------------- | ------------------- | ------ |
| `code`           | `Integer`           | 统一响应码  |
| `msg`            | `String`            | 统一响应消息 |
| `data`           | `List<SuggestItem>` | 联想候选列表 |
| `data[].org_id`  | `String`            | 企业唯一标识 |
| `data[].name_cn` | `String`            | 企业中文名称 |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": [
    {
      "org_id": "ent_001",
      "name_cn": "深圳某科技有限公司"
    }
  ]
}
```



##### 3. 企业高级筛选检索

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/advanced`
- 接口用途：企业高级筛选检索。
- 请求对象：`EnterpriseSearchRequest`
- 返回对象：`R<EnterpriseResponseDTOs.SearchResponse>`

入参字段表：


| 字段           | 类型                    | 必填  | 说明      |
| ------------ | --------------------- | --- | ------- |
| `query_tree` | `Map<String, Object>` | 是   | 高级筛选查询树 |
| `sort_field` | `String`              | 否   | 排序字段    |
| `sort_order` | `String`              | 否   | 排序方向    |
| `page`       | `Integer`             | 否   | 当前页码    |
| `size`       | `Integer`             | 否   | 每页条数    |


请求 JSON 示例：

```json
{
  "query_tree": {
    "logic": "AND",
    "conditions": [
      {
        "field": "province",
        "operator": "eq",
        "value": "广东省"
      }
    ]
  },
  "sort_field": "competitiveness_score",
  "sort_order": "desc",
  "page": 1,
  "size": 20
}
```

返回字段表：


| 字段           | 类型                 | 说明       |
| ------------ | ------------------ | -------- |
| `code`       | `Integer`          | 统一响应码    |
| `msg`        | `String`           | 统一响应消息   |
| `data.list`  | `List<SearchItem>` | 企业检索结果列表 |
| `data.total` | `Long`             | 命中企业总数   |
| `data.page`  | `Integer`          | 当前页码     |
| `data.size`  | `Integer`          | 每页条数     |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "org_id": "ent_001",
        "name_cn": "深圳某科技有限公司"
      }
    ],
    "total": 32,
    "page": 1,
    "size": 20
  }
}
```



##### 4. 企业搜索筛选字典

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/filters`
- 接口用途：企业搜索筛选字典。
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseResponseDTOs.FiltersResponse>`

入参字段表：


| 字段  | 类型  | 必填  | 说明          |
| --- | --- | --- | ----------- |
| 无   | -   | -   | 空对象占位，无业务字段 |


请求 JSON 示例：

```json
{}
```

返回字段表：


| 字段                        | 类型             | 说明      |
| ------------------------- | -------------- | ------- |
| `code`                    | `Integer`      | 统一响应码   |
| `msg`                     | `String`       | 统一响应消息  |
| `data.industries`         | `List<String>` | 行业分类列表  |
| `data.provinces`          | `List<String>` | 省份列表    |
| `data.cities`             | `List<String>` | 城市列表    |
| `data.listing_statuses`   | `List<String>` | 上市状态列表  |
| `data.operating_statuses` | `List<String>` | 经营状态列表  |
| `data.enterprise_scales`  | `List<String>` | 企业规模列表  |
| `data.risk_levels`        | `List<String>` | 风险等级列表  |
| `data.tags`               | `List<String>` | 标签编码列表  |
| `data.industry_chains`    | `List<String>` | 产业链名称列表 |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "industries": ["电子信息", "高端装备"],
    "provinces": ["广东省"],
    "cities": ["深圳市", "广州市"],
    "listing_statuses": ["已上市", "未上市"],
    "operating_statuses": ["在营", "注销"],
    "enterprise_scales": ["大型", "中型"],
    "risk_levels": ["低", "中", "高"],
    "tags": ["high_tech", "little_giant"],
    "industry_chains": ["集成电路", "人工智能"]
  }
}
```



##### 5. 注册区县三级联动字典

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/regions`
- 接口用途：注册区县三级联动字典。
- 请求对象：`EnterpriseRegionRequest`
- 返回对象：`R<EnterpriseResponseDTOs.RegionsResponse>`

入参字段表：


| 字段            | 类型       | 必填  | 说明               |
| ------------- | -------- | --- | ---------------- |
| `parent_code` | `String` | 否   | 父级地区编码；为空时查询省级列表 |


请求 JSON 示例：

```json
{
  "parent_code": "440000"
}
```

返回字段表：


| 字段                       | 类型                 | 说明     |
| ------------------------ | ------------------ | ------ |
| `code`                   | `Integer`          | 统一响应码  |
| `msg`                    | `String`           | 统一响应消息 |
| `data.items`             | `List<RegionItem>` | 地区列表   |
| `data.items[].code`      | `String`           | 地区编码   |
| `data.items[].name`      | `String`           | 地区名称   |
| `data.items[].level`     | `String`           | 行政层级   |
| `data.items[].fulltitle` | `String`           | 完整地区名称 |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "code": "440300",
        "name": "深圳市",
        "level": "2",
        "fulltitle": "广东省深圳市"
      }
    ]
  }
}
```



##### 6. 企业类型枚举

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/company-types`
- 接口用途：企业类型枚举。
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseResponseDTOs.OptionsResponse>`

入参字段表：


| 字段  | 类型  | 必填  | 说明          |
| --- | --- | --- | ----------- |
| 无   | -   | -   | 空对象占位，无业务字段 |


请求 JSON 示例：

```json
{}
```

返回字段表：


| 字段                  | 类型                   | 说明     |
| ------------------- | -------------------- | ------ |
| `code`              | `Integer`            | 统一响应码  |
| `msg`               | `String`             | 统一响应消息 |
| `data.items`        | `List<CodeNameItem>` | 企业类型列表 |
| `data.items[].code` | `String`             | 类型编码   |
| `data.items[].name` | `String`             | 类型名称   |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "code": "有限责任公司",
        "name": "有限责任公司"
      }
    ]
  }
}
```



##### 7. 企业规模枚举

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/enterprise-scales`
- 接口用途：企业规模枚举。
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseResponseDTOs.OptionsResponse>`

入参字段表：


| 字段  | 类型  | 必填  | 说明          |
| --- | --- | --- | ----------- |
| 无   | -   | -   | 空对象占位，无业务字段 |


请求 JSON 示例：

```json
{}
```

返回字段表：


| 字段                  | 类型                   | 说明     |
| ------------------- | -------------------- | ------ |
| `code`              | `Integer`            | 统一响应码  |
| `msg`               | `String`             | 统一响应消息 |
| `data.items`        | `List<CodeNameItem>` | 企业规模列表 |
| `data.items[].code` | `String`             | 规模编码   |
| `data.items[].name` | `String`             | 规模名称   |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "code": "大型",
        "name": "大型"
      }
    ]
  }
}
```



##### 8. 标签字典查询

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/tags`
- 接口用途：标签字典查询。
- 请求对象：`EnterpriseTagRequest`
- 返回对象：`R<EnterpriseResponseDTOs.TagDictionaryResponse>`

入参字段表：


| 字段         | 类型       | 必填  | 说明                                |
| ---------- | -------- | --- | --------------------------------- |
| `category` | `String` | 否   | 标签分类编码，例如 `qualification`、`honor` |


请求 JSON 示例：

```json
{
  "category": "qualification"
}
```

返回字段表：


| 字段                          | 类型              | 说明     |
| --------------------------- | --------------- | ------ |
| `code`                      | `Integer`       | 统一响应码  |
| `msg`                       | `String`        | 统一响应消息 |
| `data.items`                | `List<TagItem>` | 标签字典列表 |
| `data.items[].tag_code`     | `String`        | 标签编码   |
| `data.items[].tag_name`     | `String`        | 标签名称   |
| `data.items[].tag_category` | `String`        | 标签分类   |
| `data.items[].tag_level`    | `Integer`       | 标签层级   |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "tag_code": "high_tech",
        "tag_name": "高新技术企业",
        "tag_category": "qualification",
        "tag_level": 1
      }
    ]
  }
}
```



#### 3.2 对比类接口



##### 9. 企业对比篮对比

- 接口路径：`POST gateway地址/enterprise/topic/v1/compare-basket/compare`
- 接口用途：企业对比篮对比。
- 请求对象：`EnterpriseCompareRequest`
- 返回对象：`R<EnterpriseResponseDTOs.CompareResponse>`

入参字段表：


| 字段        | 类型             | 必填  | 说明          |
| --------- | -------------- | --- | ----------- |
| `org_ids` | `List<String>` | 是   | 参与对比的企业主键列表 |


请求 JSON 示例：

```json
{
  "org_ids": ["ent_001", "ent_002"]
}
```

返回字段表：


| 字段            | 类型                  | 说明        |
| ------------- | ------------------- | --------- |
| `code`        | `Integer`           | 统一响应码     |
| `msg`         | `String`            | 统一响应消息    |
| `data.items`  | `List<CompareItem>` | 对比企业列表    |
| `data.total`  | `Integer`           | 对比企业总数    |
| `data.fields` | `List<String>`      | 前端对比表字段清单 |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "org_id": "ent_001",
        "name_cn": "深圳某科技有限公司",
        "competitiveness_score": 87.5
      }
    ],
    "total": 2,
    "fields": ["name_cn", "industry_class_name", "competitiveness_score"]
  }
}
```



#### 3.3 画像类接口



##### 10. 企业全景画像

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/panorama`
- 接口用途：企业全景画像。
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.PanoramaResponse>`

入参字段表：


| 字段       | 类型       | 必填  | 说明     |
| -------- | -------- | --- | ------ |
| `org_id` | `String` | 是   | 企业唯一标识 |


请求 JSON 示例：

```json
{
  "org_id": "ent_001"
}
```

返回字段表：


| 字段                         | 类型                            | 说明       |
| -------------------------- | ----------------------------- | -------- |
| `code`                     | `Integer`                     | 统一响应码    |
| `msg`                      | `String`                      | 统一响应消息   |
| `data.org_id`              | `String`                      | 企业唯一标识   |
| `data.name_cn`             | `String`                      | 企业中文名称   |
| `data.social_credit_code`  | `String`                      | 统一社会信用代码 |
| `data.province`            | `String`                      | 省份       |
| `data.city`                | `String`                      | 城市       |
| `data.industry_class_name` | `String`                      | 行业分类名称   |
| `data.tags`                | `List<TagItem>`               | 企业标签明细   |
| `data.industry_chains`     | `List<IndustryChainItem>`     | 产业链归属列表  |
| `data.executives`          | `List<ExecutiveItem>`         | 高管列表     |
| `data.financials`          | `List<FinancialRecord>`       | 财务历史列表   |
| `data.financings`          | `List<FinancingItem>`         | 融资事件列表   |
| `data.innovation_carriers` | `List<InnovationCarrierItem>` | 创新载体列表   |
| `data.risk_flags`          | `RiskFlags`                   | 风险标记汇总   |
| `data.risk_level`          | `String`                      | 风险等级     |
| `data.statistics`          | `List<Statistics>`            | 统计指标列表   |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "org_id": "ent_001",
    "name_cn": "深圳某科技有限公司",
    "social_credit_code": "91440300XXXXXX",
    "province": "广东省",
    "city": "深圳市",
    "industry_class_name": "电子信息",
    "tags": [
      {
        "tag_code": "high_tech",
        "tag_value": "高新技术企业"
      }
    ],
    "executives": [
      {
        "name": "张三",
        "position": "董事长"
      }
    ],
    "risk_flags": {
      "abnormal_count": 0,
      "shixin_count": 0
    }
  }
}
```



##### 11. 企业详情卡片弹窗

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/card`
- 接口用途：企业详情卡片弹窗。
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.CardResponse>`

入参字段表：


| 字段       | 类型       | 必填  | 说明     |
| -------- | -------- | --- | ------ |
| `org_id` | `String` | 是   | 企业唯一标识 |


请求 JSON 示例：

```json
{
  "org_id": "ent_001"
}
```

返回字段表：


| 字段                     | 类型                        | 说明       |
| ---------------------- | ------------------------- | -------- |
| `code`                 | `Integer`                 | 统一响应码    |
| `msg`                  | `String`                  | 统一响应消息   |
| `data.header`          | `CardHeader`              | 头部信息     |
| `data.metrics`         | `CardMetrics`             | 核心指标信息   |
| `data.description`     | `String`                  | 企业简介     |
| `data.business_info`   | `CardBusinessInfo`        | 工商信息块    |
| `data.industry_chains` | `List<IndustryChainItem>` | 产业链归属列表  |
| `data.qualifications`  | `List<TagItem>`           | 资质荣誉标签列表 |
| `data.finance_latest`  | `CardFinanceLatest`       | 最新财务快照   |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "header": {
      "name_cn": "深圳某科技有限公司",
      "social_credit_code": "91440300XXXXXX"
    },
    "metrics": {
      "competitiveness_score": 87.5,
      "registered_capital": "5000 万元"
    },
    "business_info": {
      "lerep": "张三",
      "company_type": "有限责任公司"
    },
    "finance_latest": {
      "year": 2024,
      "net_profit": 1200.0
    }
  }
}
```



##### 12. 企业工商概况详情

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/basic`
- 接口用途：企业工商概况详情。
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.BasicResponse>`

入参字段表：


| 字段       | 类型       | 必填  | 说明     |
| -------- | -------- | --- | ------ |
| `org_id` | `String` | 是   | 企业唯一标识 |


请求 JSON 示例：

```json
{
  "org_id": "ent_001"
}
```

返回字段表：


| 字段                              | 类型           | 说明       |
| ------------------------------- | ------------ | -------- |
| `code`                          | `Integer`    | 统一响应码    |
| `msg`                           | `String`     | 统一响应消息   |
| `data.org_id`                   | `String`     | 企业唯一标识   |
| `data.name_cn`                  | `String`     | 企业中文名称   |
| `data.social_credit_code`       | `String`     | 统一社会信用代码 |
| `data.lerep`                    | `String`     | 法定代表人    |
| `data.province`                 | `String`     | 省份       |
| `data.city`                     | `String`     | 城市       |
| `data.address`                  | `String`     | 企业地址     |
| `data.registered_capital_value` | `BigDecimal` | 注册资本     |
| `data.registration_org`         | `String`     | 登记机关     |
| `data.company_type`             | `String`     | 企业类型     |
| `data.operating_status`         | `String`     | 经营状态     |
| `data.business_scope`           | `String`     | 经营范围     |
| `data.description`              | `String`     | 企业简介     |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "org_id": "ent_001",
    "name_cn": "深圳某科技有限公司",
    "lerep": "张三",
    "province": "广东省",
    "city": "深圳市",
    "registered_capital_value": 5000.0,
    "company_type": "有限责任公司",
    "operating_status": "在营"
  }
}
```



##### 13. 企业概况 KPI 汇总卡

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/overview`
- 接口用途：企业概况 KPI 汇总卡。
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.OverviewResponse>`

入参字段表：


| 字段       | 类型       | 必填  | 说明     |
| -------- | -------- | --- | ------ |
| `org_id` | `String` | 是   | 企业唯一标识 |


请求 JSON 示例：

```json
{
  "org_id": "ent_001"
}
```

返回字段表：


| 字段                           | 类型           | 说明      |
| ---------------------------- | ------------ | ------- |
| `code`                       | `Integer`    | 统一响应码   |
| `msg`                        | `String`     | 统一响应消息  |
| `data.org_id`                | `String`     | 企业唯一标识  |
| `data.name_cn`               | `String`     | 企业中文名称  |
| `data.enterprise_scale`      | `String`     | 企业规模    |
| `data.operating_status`      | `String`     | 经营状态    |
| `data.risk_level`            | `String`     | 风险等级    |
| `data.competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.chain_position_text`   | `String`     | 产业链位置描述 |
| `data.risk_flags`            | `RiskFlags`  | 风险标记    |
| `data.statistics`            | `Statistics` | 关键统计指标  |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "org_id": "ent_001",
    "name_cn": "深圳某科技有限公司",
    "enterprise_scale": "中型",
    "risk_level": "低",
    "competitiveness_score": 87.5,
    "statistics": {
      "patent_total": 35,
      "latest_revenue": 5600.0
    }
  }
}
```



##### 14. 企业资讯分页查询

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/news`
- 接口用途：企业资讯分页查询。
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.NewsResponse>`

入参字段表：


| 字段       | 类型        | 必填  | 说明     |
| -------- | --------- | --- | ------ |
| `org_id` | `String`  | 是   | 企业唯一标识 |
| `page`   | `Integer` | 否   | 当前页码   |
| `size`   | `Integer` | 否   | 每页条数   |


请求 JSON 示例：

```json
{
  "org_id": "ent_001",
  "page": 1,
  "size": 10
}
```

返回字段表：


| 字段                    | 类型               | 说明     |
| --------------------- | ---------------- | ------ |
| `code`                | `Integer`        | 统一响应码  |
| `msg`                 | `String`         | 统一响应消息 |
| `data.list`           | `List<NewsItem>` | 资讯列表   |
| `data.total`          | `Long`           | 资讯总数   |
| `data.page`           | `Integer`        | 当前页码   |
| `data.size`           | `Integer`        | 每页条数   |
| `data.list[].news_id` | `String`         | 资讯主键   |
| `data.list[].title`   | `String`         | 资讯标题   |
| `data.list[].summary` | `String`         | 资讯摘要   |
| `data.list[].source`  | `String`         | 资讯来源   |
| `data.list[].date`    | `String`         | 资讯日期   |
| `data.list[].url`     | `String`         | 原文链接   |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "news_id": "news_001",
        "title": "深圳某科技有限公司完成新一轮融资",
        "summary": "企业近期完成战略融资",
        "source": "科技日报",
        "date": "2026-07-01",
        "url": "https://example.com/news/001"
      }
    ],
    "total": 15,
    "page": 1,
    "size": 10
  }
}
```



##### 15. 企业风险汇总

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/summary`
- 接口用途：企业风险汇总。
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.RiskSummaryResponse>`

入参字段表：


| 字段       | 类型       | 必填  | 说明     |
| -------- | -------- | --- | ------ |
| `org_id` | `String` | 是   | 企业唯一标识 |


请求 JSON 示例：

```json
{
  "org_id": "ent_001"
}
```

返回字段表：


| 字段                           | 类型                     | 说明        |
| ---------------------------- | ---------------------- | --------- |
| `code`                       | `Integer`              | 统一响应码     |
| `msg`                        | `String`               | 统一响应消息    |
| `data.risk_level`            | `String`               | 企业风险等级    |
| `data.risk_flags`            | `RiskFlags`            | 风险标记对象    |
| `data.competitiveness_score` | `BigDecimal`           | 综合竞争力得分   |
| `data.total_count`           | `Integer`              | 风险总条数     |
| `data.type_counts`           | `Map<String, Integer>` | 各风险类型数量映射 |


返回 JSON 示例：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "risk_level": "低",
    "risk_flags": {
      "abnormal_count": 0,
      "shixin_count": 0,
      "zhixing_count": 0,
      "punishment_count": 1
    },
    "competitiveness_score": 87.5,
    "total_count": 1,
    "type_counts": {
      "punishment": 1
    }
  }
}
```



### 4. DTO 映射策略

本次请求对象和响应对象已按 Python 文档中的字段命名与返回骨架进行映射，重点规则如下：

- 请求对象保留 Java 驼峰命名，通过 `@JsonProperty` 对齐 Python `snake_case`
- 典型请求映射字段包括：
  - `org_id`
  - `org_ids`
  - `query_tree`
  - `sort_field`
  - `sort_order`
  - `parent_code`
- 响应对象第一版已完成 typed DTO 收敛，核心响应类型包括：
  - `SearchResponse`
  - `FiltersResponse`
  - `CompareResponse`
  - `PanoramaResponse`
  - `CardResponse`
  - `BasicResponse`
  - `OverviewResponse`
  - `NewsResponse`
  - `RiskSummaryResponse`
- 当前深层嵌套对象也已补入第一版专用结构，例如：
  - `SuggestItem`
  - `TagItem`
  - `IndustryChainItem`
  - `ExecutiveItem`
  - `InnovationCarrierItem`
  - `FinancialRecord`
  - `FinancingItem`
  - `SupplyChainRelationItem`



### 5. 注释规范补齐

本次已按当前执行要求补齐以下注释：

- 类注释
- 字段注释
- 方法注释
- 参数与返回值说明
- 新增响应 DTO 的逐字段中文注释

后续该模块新增代码可沿用同一标准。

## 与 DoD 对照


| DoD 条目                                                                | 状态   | 说明                                                              |
| --------------------------------------------------------------------- | ---- | --------------------------------------------------------------- |
| `gkxlumen-enterprise` OpenAPI 草案（`search / compare-basket / profile`） | ✅    | 已完成第一版 Java 门面接口骨架与对外 Feign 契约                                  |
| 只读 ADS + Feign 调 Python；禁止 Java 算法                                    | ✅    | 当前 Java 仅做门面转发与契约承载，未落任何算法逻辑                                    |
| 与 `ENT-ARCH-IMPL-DESIGN` 架构图一致                                        | ✅/⚠️ | 总体分层一致；但 Python 侧当前对接的是 `/api/gkx-search/**`，未切为 `/internal/**` |
| API 分层与权限点由侯佳伟确认签字                                                    | ✅    | 本次代码由侯佳伟执行确认，可作为会签事实依据                                          |




## 偏离说明


| 偏离项                                  | 说明                                                              | 原因                                                        |
| ------------------------------------ | --------------------------------------------------------------- | --------------------------------------------------------- |
| Python 调用路径当前使用 `/api/gkx-search/**` | 仍未切换到架构铁律建议的 `/internal/**`                                     | 当前以既有 Python 文档与已实现端点为准，优先完成 Java 门面契约落地                  |
| 响应对象仍为第一版 typed DTO                  | 已完成 `search / compare / profile / meta` 主要响应收敛，但更深层业务块仍保留渐进细化空间 | 当前优先确保契约骨架稳定与 Feign/Controller/Service 全链路统一，后续可继续细化更多子对象 |
| 未形成独立 commit / PR                    | 本次在本地工作区完成实现与验证                                                 | 当前阶段以本地交付与 handoff 为主                                     |




## 验收证据

- **代码路径**：`lumen-svc-platform/gkxlumen-topic-enterprise/`
- **对外契约**：`RemoteTopicEnterpriseService.java`
- **门面控制器**：`EnterpriseOpenApiController.java`
- **服务分层**：`EnterpriseOpenApiService.java` + `EnterpriseOpenApiServiceImpl.java`
- **下游 Python 适配**：`RemoteEnterprisePythonClient.java`
- **注释补齐**：上述核心类、方法、字段均已补齐中文注释
- **静态检查**：`ReadLints` 无新增报错
- **编译验证**：
  - 执行命令：`mvn -pl gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz -am -DskipTests compile`
  - 结果：`BUILD SUCCESS`
- **环境问题确认**：
  - 原问题：Maven 继承 `JAVA_HOME=jdk1.8.0_231`
  - 当前结果：已验证在 `Java 17` 环境下可以完成编译



## 架构合规自检


| 铁律                    | 合规   | 说明                                                                      |
| --------------------- | ---- | ----------------------------------------------------------------------- |
| D1: 算法只在 Python       | ✅    | Java 侧未实现算法逻辑                                                           |
| D2: 调用链不可越层           | ✅/⚠️ | 仍为前端/Java/Python 三层；但 Python 目前走 `/api/gkx-search/**` 而非 `/internal/**` |
| D3: 图谱使用 NebulaGraph  | ✅    | 本次未触碰图谱实现，未引入违例依赖                                                       |
| D4: 可观测性              | ⚠️   | 本次任务为契约与门面骨架，未单独补企业模块观测埋点                                               |
| D5: CI/CD             | ⚠️   | 已完成本地编译验证，未进入 PR / Pipeline 阶段                                          |
| D6: demo2 只读 merge 铁律 | ✅    | 本次修改位于正式 Java 仓，不涉及 demo2 merge                                         |
| D7: 共享聚合核心            | ✅    | 企业门面作为 Java 聚合层承接 Python 能力                                             |
| D8: 前端规范唯一来源          | ✅    | 本次不涉及前端页面                                                               |
| D9: 数据血缘铁律            | ⚠️   | 当前只完成后端契约骨架，未将指标元数据卡片机制落到前端或完整返回模型                                      |




## 成本回填信息（供编排侧落库）

> 说明：执行侧当前无法直接读取平台精确 token / cost 统计，以下信息供 `coordinator / PM` 根据平台账单或会话统计回填到 `task-registry.yaml`。


| 字段              | 当前值                     |
| --------------- | ----------------------- |
| `actual_tokens` | 待编排侧回填                  |
| `model_used`    | `gpt-5.4`               |
| `actual_cost`   | 待编排侧回填                  |
| `cost_warn`     | 建议按平台统计判定，当前预计为 `green` |




## 待处理事项


| 优先级 | 事项                                                        | 负责人建议                   | 状态  |
| --- | --------------------------------------------------------- | ----------------------- | --- |
| P0  | 由编排侧更新 `ENT-ARCH-API-CONTRACT` 状态、证据路径与成本字段               | coordinator / PM        | 待办  |
| P1  | 确认 Python 下游是否需要从 `/api/gkx-search/**` 收敛为 `/internal/**` | architect / integration | 待办  |
| P1  | 对 `search / compare / profile` 响应体继续收敛 typed DTO          | api-agent 后续任务          | 待办  |
| P1  | 启动 Java 门面与 Python 服务联调验证                                 | integration / api-agent | 待办  |
| P2  | 补企业模块级可观测性与错误处理细化                                         | api-agent / devops      | 待办  |


---

**Handoff 编写**：api-agent（2026-07-16）  
**执行边界说明**：本次仅完成执行侧交付、证据整理与 handoff；状态更新、成本落库、下一单派发由编排侧处理。  