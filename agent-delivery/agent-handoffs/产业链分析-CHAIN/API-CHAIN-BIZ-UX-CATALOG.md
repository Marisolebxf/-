# 产业链 Java · 对比篮 / 查询辅助 / 区域模板 / 分析维度（本轮增补）

- 时间：2026-09-07
- 作者：api-agent（监管：human:侯佳伟）
- 任务：`LUMEN-CHAIN-JAVA-BIZ-UX-L01`
- 仓库：`lumen-svc-platform`（`gkxlumen-topic-chain` 门面 + `gkxlumen-topic-enterprise` 写库）
- 格式对齐：`企业战略分析-ENT/API-ENT-full-catalog.md`（一份文档，按模块分章；字段表 + HTTP/JSON 示例）
- 存量产业链读面仍以 `专题前端-TOPIC-FE/API-TOPIC-FE-GAP-CATALOG.md` §5 `#C1–C6` 为准；**本文只记本轮新增用户态写读**
- **字段结构真源**：`ChainUxDTOs` + `IndustryFacadeServiceImpl#analysisDims`
- 口径未定：对标城 **Q016** 保持 `benchmark.items=[]`，不发明清单

| 档 | 含义 | 本次 |
|---|---|---|
| **P0** | 没有接口则页面只能写死或刷新丢失 | 对比篮 / 示例·场景·最近检索 / 高筛方案 / 区域模板 |
| **P2** | 路径已有，切片给前端 | `#U18` 分析维度（切 `#C1` meta，不另造字典） |

## 目录

| 章 | 模块 | 编号 |
|---|---|---|
| §4 | 对比篮 | #U1–U4 |
| §5 | 查询辅助（示例 / 场景 / 最近检索） | #U5–U9 |
| §6 | 产业高筛「我的方案」 | #U10–U12 |
| §7 | 区域指数指标与模板 | #U13–U17 |
| §8 | 分析维度切片 | #U18 |

## 1. 路由拼接规则

```text
gateway地址 / chain / {Controller @RequestMapping} / {方法映射}
```

| 段 | 当前值 |
|---|---|
| gateway地址 | 外网 `http://111.198.38.90:50199`（内网 NodePort `http://10.50.69.111:30899`） |
| 网关前缀 | `/chain`（StripPrefix=1） |
| Controller | `/topic/v1/industry` |
| 内部写库（前端勿调） | topic-enterprise `/topic/v1/chain-ux/**` |

示例：`GET gateway地址/chain/topic/v1/industry/compare-basket?user_id=u-1`

`{GW}` 下文均指 gateway 基址。统一包络：`{ code, msg, ok, data }`，成功 `code=0`。

## 2. 调用链

```text
# 对比篮 / 查询辅助 / 高筛 / 区域模板（Java MySQL，不调 Python）
前端 → /chain/topic/v1/industry/{compare-basket|search-biz|filter-template|regional}/**
  → IndustryChainUxController
  → Feign TOPIC_ENTERPRISE_SERVICE /topic/v1/chain-ux/**
  → ChainUxInternalController → chain_* 表
  → MySQL gkxlumenx_topic_enterprise

# 分析维度（不写库）
前端 → /chain/topic/v1/industry/analysis-dims
  → IndustryFacadeController.analysisDims
  → 切既有 GET /industry/meta（Feign lumen-algo-py /internal/v1/chain/meta）
  → benchmark.items 保持 []，pending_ref=Q016
```

topic-chain 自己连的是只读 Demo ADS，**不能**把用户态写进 ADS。

## 3. 端点总览

| # | 分组 | 网关路径（相对 `{GW}`） | Python 下游 | 请求对象 | 返回 data | 动作 |
|---|---|---|---|---|---|---|
| U1 | 对比篮 | `GET /chain/topic/v1/industry/compare-basket` | — | `user_id` query；`object_type` 可选 | `BasketResponse` | 新增 |
| U2 | 对比篮 | `POST /chain/topic/v1/industry/compare-basket/items` | — | `BasketAddRequest` | `BasketAddResponse` | 新增 |
| U3 | 对比篮 | `DELETE /chain/topic/v1/industry/compare-basket/items/{object_type}/{object_id}` | — | `user_id` query | `Void` | 新增 |
| U4 | 对比篮 | `DELETE /chain/topic/v1/industry/compare-basket/items/batch` | — | `BasketBatchRemoveRequest` | `Void` | 新增 |
| U5 | 查询辅助 | `POST /chain/topic/v1/industry/search-biz/examples/list` | — | `ExampleListRequest` | `List<ExampleItem>` | 新增 |
| U6 | 查询辅助 | `POST /chain/topic/v1/industry/search-biz/scenes/list` | — | 无 | `List<SceneItem>` | 新增 |
| U7 | 查询辅助 | `POST /chain/topic/v1/industry/search-biz/history/list` | — | `HistoryListRequest` | `List<HistoryItem>` | 新增 |
| U8 | 查询辅助 | `POST /chain/topic/v1/industry/search-biz/history/save` | — | `HistorySaveRequest` | `IdResponse` | 新增 |
| U9 | 查询辅助 | `POST /chain/topic/v1/industry/search-biz/history/clear` | — | `HistoryListRequest` | `Void` | 新增 |
| U10 | 高筛方案 | `POST /chain/topic/v1/industry/filter-template/list` | — | `UserIdRequest` | `List<FilterItem>` | 新增 |
| U11 | 高筛方案 | `POST /chain/topic/v1/industry/filter-template/save` | — | `FilterSaveRequest` | `IdResponse` | 新增 |
| U12 | 高筛方案 | `POST /chain/topic/v1/industry/filter-template/delete` | — | `IdUserRequest` | `Void` | 新增 |
| U13 | 区域指数 | `GET /chain/topic/v1/industry/regional/metrics` | — | `eval_mode` query | `List<RegionalMetricItem>` | 新增 |
| U14 | 区域指数 | `GET /chain/topic/v1/industry/regional/templates/official` | — | 无 | `List<RegionalTemplateItem>` | 新增 |
| U15 | 区域指数 | `POST /chain/topic/v1/industry/regional/templates/mine/list` | — | `UserIdRequest` | `List<RegionalTemplateItem>` | 新增 |
| U16 | 区域指数 | `POST /chain/topic/v1/industry/regional/templates/mine/save` | — | `RegionalTemplateSaveRequest` | `IdResponse` | 新增 |
| U17 | 区域指数 | `POST /chain/topic/v1/industry/regional/templates/mine/delete` | — | `IdUserRequest` | `Void` | 新增 |
| U18 | 分析维度 | `GET /chain/topic/v1/industry/analysis-dims` | `GET /internal/v1/chain/meta` 切片 | 无 | `Map` | 新增（兼容继续用 `#C1` meta） |

DTO：`com.topcomm.gkxlumen.topic.enterprise.api.dto.chainux.ChainUxDTOs`（snake_case）。

## 0. 前端导读

> 网关前缀一律 **`/chain`**。不要打企业 `/enterprise/.../filter-template`，也不要打 `biz_type=industry` 混企业表。  
> 对比篮对象是 **产业 / 产业链**，字段是 `object_type` + `object_ids`，**禁止** `enterprise_code`。  
> 分析任务生命周期仍走 `/topicAsync`（本叶不改）。

#### 该调哪些接口

| 业务 | 本轮 | 不要串线 |
|---|---|---|
| 产业查询 · 加入/移除对比篮 | **#U1–U4** | 不是企业篮 `#91–94`，也不是服务机构篮 `#S2–S5` |
| 智能检索 / 查产业 示例词 | **#U5** `kind=smart\|industry` | 不是企业 `search-biz/examples` |
| 热门场景 | **#U6** | 场景 JSON 是产业高筛，不是企业字段 |
| 最近检索 | **#U7–U9** | 按 `user_id` + `search_type` 隔离；替换 localStorage `gkx-industry-search-recents:v1` |
| 高级筛选「我的方案」 | **#U10–U12** | **独立表** `chain_filter_template`；不要再 `useFilterTemplates('industry')` 打企业接口 |
| 区域指数 · 可添加指标 | **#U13** | `eval_mode=index\|competitiveness` |
| 区域指数 · 官方 / 我的模板 | **#U14–U17** | 替换区域页 localStorage 模板 |
| 诊断/区域/深圳维度与权重 | **#U18** 或继续 **#C1** meta | `benchmark.items` 空；不要前端写死演示权重 |

#### 调用方图例

| 标注 | 含义 |
|---|---|
| **前端** | 浏览器业务页 |
| **内部 Feign** | chain → enterprise 写库；前端只调 `/chain` |
| **Python** | 仅 `#U18` / `#C1`；前端勿调 `/internal/**` |

#### 容易混淆

| 容易当成 | 实际 |
|---|---|
| 和对企业一样传 `enterprise_codes` | 必须 `object_type` + `object_ids` |
| `object_type=enterprise` | **拒绝** |
| 高筛方案加 `biz_type=industry` 就能和企业共用表 | 本轮 **新表**，路径也在 `/chain` |
| `#U18` 会给出对标城清单 | **不会**。`pending_ref=Q016`，`items=[]` |
| 只发 topic-chain、不发 topic-enterprise | `/chain-ux/**` 404 |
| 只发镜像、不跑增量 SQL | 写库报错。只跑 `db/9x_gkxlumenx_topic_enterprise_chain_ux_l01.sql`，**禁止**跑带 DROP 的旧 `9x_gkxlumenx_topic_enterprise.sql` |

`user_id`：本叶 **按请求入参落库**（query 或 body）。空用户读接口返回空列表，写接口返回失败或空成功（见各条）。

---

## 4. 对比篮（#U1–U4）

> 表 `chain_compare_basket_item`。UK=`user_id + object_type + object_id`。上限 **50**。  
> `object_type` 仅 `industry` / `industry_chain`。  
> Controller：`IndustryChainUxController`。内部：`ChainCompareBasketServiceImpl`。

##### U1. 获取对比篮

- **调用方**：**前端**
- 接口路径：`GET gateway地址/chain/topic/v1/industry/compare-basket`
- 服务内路径：`GET /topic/v1/industry/compare-basket`
- Python 下游：—
- 接口用途：当前用户产业/链对比篮。空篮合法。
- 请求对象：query
- 返回对象：`R<ChainUxDTOs.BasketResponse>`

入参字段表：

| 字段 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `user_id` | query | `String` | 是 | 用户隔离；空则 `items=[]` |
| `object_type` | query | `String` | 否 | `industry` / `industry_chain`；不传返回两类 |

请求示例：

```http
GET /chain/topic/v1/industry/compare-basket?user_id=u-1001&object_type=industry
```

返回字段表（包络 + `data`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `code` | `Integer` | 成功通常 `0` |
| `msg` | `String` | 统一消息 |
| `ok` | `Boolean` | 是否成功 |
| `data.user_id` | `String` | 用户 ID |
| `data.basket_count` | `Integer` | 当前条数 |
| `data.basket_limit` | `Integer` | 固定 `50` |
| `data.items` | `List<BasketItemView>` | 按 `operated_at` 倒序 |
| `data.items[].object_type` | `String` | `industry` / `industry_chain` |
| `data.items[].object_id` | `String` | 产业或链 ID |
| `data.items[].object_name` | `String` | 加入时名称快照 |
| `data.items[].source` | `String` | 加入来源 |
| `data.items[].operated_at` | `LocalDateTime` | 最近操作时间 |

返回 JSON 示例：

```json
{
  "code": 0,
  "msg": null,
  "ok": true,
  "data": {
    "user_id": "u-1001",
    "basket_count": 1,
    "basket_limit": 50,
    "items": [
      {
        "object_type": "industry",
        "object_id": "INB1",
        "object_name": "人工智能",
        "source": "search",
        "operated_at": "2026-09-07T16:40:00"
      }
    ]
  }
}
```

##### U2. 加入产业或产业链

- 接口路径：`POST gateway地址/chain/topic/v1/industry/compare-basket/items`
- 服务内路径：`POST /topic/v1/industry/compare-basket/items`
- Python 下游：—
- 接口用途：批量加入；已在篮内计 `duplicated`；超过 50 返回错误。
- 请求对象：`ChainUxDTOs.BasketAddRequest`
- 返回对象：`R<ChainUxDTOs.BasketAddResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | `String` | 是 | 空用户 `added=0` |
| `object_type` | `String` | 是 | 仅 `industry` / `industry_chain` |
| `object_ids` | `List<String>` | 是 | **不是** `enterprise_codes` |
| `object_names` | `List<String>` | 否 | 与 ids 按下标对齐 |
| `source` | `String` | 否 | 加入来源 |

请求 JSON 示例：

```json
{
  "user_id": "u-1001",
  "object_type": "industry",
  "object_ids": ["INB1", "INB2"],
  "object_names": ["人工智能", "集成电路"],
  "source": "search"
}
```

返回字段表（`data`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `added` | `Integer` | 新加入 |
| `duplicated` | `Integer` | 已在篮内跳过 |
| `basket_count` | `Integer` | 当前总数 |

返回 JSON 示例：

```json
{
  "code": 0,
  "msg": null,
  "ok": true,
  "data": { "added": 1, "duplicated": 1, "basket_count": 2 }
}
```

失败：`object_type` 非法 → `object_type 只允许 industry 或 industry_chain`；超限 → `对比篮最多加入 50 个对象`。

##### U3. 移除一项

- 接口路径：`DELETE gateway地址/chain/topic/v1/industry/compare-basket/items/{object_type}/{object_id}`
- 服务内路径：同左剥 `chain`
- 返回对象：`R<Void>`

入参字段表：

| 字段 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `object_type` | path | `String` | 是 | `industry` / `industry_chain` |
| `object_id` | path | `String` | 是 | |
| `user_id` | query | `String` | 是 | 空用户视为无操作成功 |

请求示例：

```http
DELETE /chain/topic/v1/industry/compare-basket/items/industry/INB1?user_id=u-1001
```

##### U4. 批量移除或清空

- 接口路径：`DELETE gateway地址/chain/topic/v1/industry/compare-basket/items/batch`
- 请求对象：`ChainUxDTOs.BasketBatchRemoveRequest`
- 返回对象：`R<Void>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | `String` | 是 | |
| `clear_all` | `Boolean` | 否 | `true` 清空；可再带 `object_type` 只清一类 |
| `object_type` | `String` | 非清空时是 | 与 `object_ids` 一起删 |
| `object_ids` | `List<String>` | 非清空时是 | |

请求 JSON 示例（清空）：

```json
{ "user_id": "u-1001", "clear_all": true }
```

请求 JSON 示例（批量）：

```json
{ "user_id": "u-1001", "object_type": "industry", "object_ids": ["INB1"] }
```

---

## 5. 查询辅助（#U5–U9）

> 表：`chain_search_example` / `chain_search_scene` / `chain_search_history`。  
> `kind` / `search_type` 仅 `smart`（智能检索）/ `industry`（查产业）。  
> 最近检索默认保留 **20** 条，上限 50。同用户同类型同关键词覆盖时间。

##### U5. 查询示例

- 接口路径：`POST gateway地址/chain/topic/v1/industry/search-biz/examples/list`
- 请求对象：`ChainUxDTOs.ExampleListRequest`（可空）
- 返回对象：`R<List<ExampleItem>>`

入参：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `kind` | `String` | 否 | `smart` / `industry`；不传两类都返回 |

请求 JSON 示例：

```json
{ "kind": "smart" }
```

返回字段表：

| 字段 | 类型 | 说明 |
|---|---|---|
| `data[].id` | `Long` | 主键 |
| `data[].kind` | `String` | `smart` / `industry` |
| `data[].keyword` | `String` | 示例词 |
| `data[].sort_order` | `Integer` | 排序 |

返回 JSON 示例：

```json
{
  "code": 0,
  "ok": true,
  "data": [
    { "id": 1, "kind": "smart", "keyword": "人工智能", "sort_order": 1 },
    { "id": 2, "kind": "smart", "keyword": "集成电路", "sort_order": 2 }
  ]
}
```

Seed（幂等）：smart=人工智能/集成电路/生物医药；industry=人工智能/新能源汽车/高端装备。

##### U6. 热门场景

- 接口路径：`POST gateway地址/chain/topic/v1/industry/search-biz/scenes/list`
- 请求：无 body 亦可
- 返回对象：`R<List<SceneItem>>`

返回字段表：

| 字段 | 类型 | 说明 |
|---|---|---|
| `data[].id` | `Long` | |
| `data[].scene_name` | `String` | 场景名 |
| `data[].query_tree` | `Map` | 产业高筛 JSON |
| `data[].sort_order` | `Integer` | |

返回 JSON 示例：

```json
{
  "code": 0,
  "ok": true,
  "data": [
    {
      "id": 1,
      "scene_name": "重点产业",
      "query_tree": {
        "logic": "AND",
        "conditions": [{ "field": "industry_attribute", "op": "in", "value": ["key"] }]
      },
      "sort_order": 1
    },
    {
      "id": 2,
      "scene_name": "未来产业",
      "query_tree": {
        "logic": "AND",
        "conditions": [{ "field": "industry_attribute", "op": "in", "value": ["future"] }]
      },
      "sort_order": 2
    }
  ]
}
```

##### U7. 最近检索列表

- 接口路径：`POST gateway地址/chain/topic/v1/industry/search-biz/history/list`
- 请求对象：`HistoryListRequest`

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | `String` | 是 | 空则 `[]` |
| `search_type` | `String` | 否 | `smart` / `industry` |
| `limit` | `Integer` | 否 | 默认 20，最大 50 |

返回字段：`id` / `keyword` / `search_type` / `query_tree` / `search_time`。

##### U8. 写入最近检索

- 接口路径：`POST gateway地址/chain/topic/v1/industry/search-biz/history/save`
- 请求对象：`HistorySaveRequest`

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | `String` | 是 | |
| `keyword` | `String` | 是 | |
| `search_type` | `String` | 是 | `smart` / `industry` |
| `query_tree` | `Map` | 否 | 高筛条件快照 |

返回：`data.id`。

##### U9. 清空最近检索

- 接口路径：`POST gateway地址/chain/topic/v1/industry/search-biz/history/clear`
- body：`user_id` 必填；`search_type` 可选（只清一类）

---

## 6. 产业高筛「我的方案」（#U10–U12）

> 表 `chain_filter_template`。**不读不写** `ent_filter_template`。每用户最多 **50** 条。

##### U10. 列表

- 接口路径：`POST gateway地址/chain/topic/v1/industry/filter-template/list`
- 请求：`{ "user_id": "u-1001" }`
- 返回：`id` / `template_name` / `query_tree` / `description` / `is_default` / `sort_order` / `update_time`

##### U11. 保存（新增或更新）

- 接口路径：`POST gateway地址/chain/topic/v1/industry/filter-template/save`

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | `Long` | 否 | 有则更新且须属该用户 |
| `user_id` | `String` | 是 | |
| `template_name` | `String` | 是 | ≤100 |
| `query_tree` | `Map` | 是 | 不可空 |
| `description` | `String` | 否 | |
| `is_default` | `Integer` | 否 | `1` 默认 |
| `sort_order` | `Integer` | 否 | |

请求 JSON 示例：

```json
{
  "user_id": "u-1001",
  "template_name": "重点产业",
  "query_tree": {
    "logic": "AND",
    "conditions": [{ "field": "industry_attribute", "op": "in", "value": ["key"] }]
  }
}
```

返回：`data.id`。

##### U12. 删除

- 接口路径：`POST gateway地址/chain/topic/v1/industry/filter-template/delete`
- body：`{ "id": 1, "user_id": "u-1001" }`（非本人当不存在）

---

## 7. 区域指数指标与模板（#U13–U17）

> 表 `chain_regional_metric` / `chain_regional_template`。  
> 官方 seed：`TPL-CHAIN-REGIONAL-OFFICIAL`。  
> `metric_id` 只作挂载，本叶不改绿就绪度。

##### U13. 可添加指标总表

- 接口路径：`GET gateway地址/chain/topic/v1/industry/regional/metrics?eval_mode=index`
- query `eval_mode`：`index`（指数叶）/ `competitiveness`（竞争力一维）；不传返回全部

返回字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `key` | `String` | 如 `commercialization` |
| `label` | `String` | 中文名 |
| `group` | `String` | 商业力 / 技术力 / … |
| `official` | `Boolean` | 官方模板是否默认计入 |
| `metric_id` | `String` | 如 `M_CHAIN_REG_COMMERCIALIZATION` |
| `eval_mode` | `String` | `index` / `competitiveness` |

返回 JSON 示例（节选）：

```json
{
  "code": 0,
  "ok": true,
  "data": [
    {
      "key": "commercialization",
      "label": "企业商业化能力",
      "group": "商业力",
      "official": true,
      "metric_id": "M_CHAIN_REG_COMMERCIALIZATION",
      "eval_mode": "index"
    }
  ]
}
```

`index` seed：commercialization / revenue / financing / patent / tech_maturity / tech_barrier / research_org / papers / talent_structure / service_org / policy_coverage / ecosystem。  
`competitiveness` seed：industry_foundation / academic_ecology / innovation_ecology。

##### U14. 官方模板

- 接口路径：`GET gateway地址/chain/topic/v1/industry/regional/templates/official`

返回 JSON 示例：

```json
{
  "code": 0,
  "ok": true,
  "data": [
    {
      "template_id": "TPL-CHAIN-REGIONAL-OFFICIAL",
      "template_name": "区域产业指数官方模板",
      "template_type": "system",
      "keys": ["commercialization", "financing", "patent", "tech_maturity", "research_org", "policy_coverage"],
      "included": ["commercialization", "financing", "patent", "tech_maturity", "research_org", "policy_coverage"],
      "weights": {
        "commercialization": 16,
        "financing": 16,
        "patent": 16,
        "tech_maturity": 16,
        "research_org": 16,
        "policy_coverage": 20
      },
      "create_time": "2026-09-07T16:40:00"
    }
  ]
}
```

##### U15. 我的模板列表

- `POST .../regional/templates/mine/list` body `{ "user_id": "u-1001" }`
- `template_type=personal`

##### U16. 保存我的模板

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `user_id` | `String` | 是 | |
| `template_name` | `String` | 是 | |
| `keys` | `List<String>` | 是 | 指标 key |
| `included` | `List<String>` | 否 | 默认同 keys |
| `weights` | `Map` | 否 | key→权重 |

返回：`data.id` + `data.template_id`（个人模板新 ID）。

##### U17. 删除我的模板

- `POST .../regional/templates/mine/delete` body `{ "id": 2, "user_id": "u-1001" }`  
  （按行主键；非本人不可删官方 `system` 行）

---

## 8. 分析维度切片（#U18）

- **调用方**：**前端**（诊断 / 区域 / 深圳条件栏；禁止再硬编码演示权重）
- 接口路径：`GET gateway地址/chain/topic/v1/industry/analysis-dims`
- 服务内路径：`GET /topic/v1/industry/analysis-dims`
- Python：切 `GET /internal/v1/chain/meta`（与 GAP **#C1** 同源）
- 请求：无

从 meta **原样拷贝**（有才带）：`diagnosis` / `regional` / `shenzhen` / `year_windows` / `evaluation_cities` / `default_evaluation_city`。

强制：

| 字段 | 说明 |
|---|---|
| `benchmark.pending_ref` | 无则补 `Q016` |
| `benchmark.items` | 无则 `[]`，**不发明对标城** |

兼容：字典仍可只调 `#C1` `GET /chain/topic/v1/industry/meta`。`#U18` 是给「只要维度、不要整包 meta」的瘦接口。

返回 JSON 示例（节选）：

```json
{
  "code": 0,
  "ok": true,
  "data": {
    "year_windows": [],
    "evaluation_cities": [],
    "benchmark": { "pending_ref": "Q016", "items": [] }
  }
}
```

`diagnosis` / `regional` / `shenzhen` 结构以 `#C1` 字段表为准（本叶不改算法）。

---

## 9. 落库与部署

| 项 | 值 |
|---|---|
| 库 | `gkxlumenx_topic_enterprise`（与企业篮同库） |
| DDL | **只跑** `lumen-svc-platform/db/9x_gkxlumenx_topic_enterprise_chain_ux_l01.sql`（`CREATE TABLE IF NOT EXISTS` + 幂等 INSERT） |
| 禁止 | `db/9x_gkxlumenx_topic_enterprise.sql`（含 `DROP TABLE`） |
| 镜像 | topic-chain `f3bbc5d` + topic-enterprise `f3bbc5d`（pipeline [6049](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6049) 已发 dev） |
| 前端接线 | collaborator `frontend-agent` 另单；本叶未改 `lumen-ui-topic` |

## 10. 代码落点

| 层 | 路径 |
|---|---|
| 门面 | `gkxlumen-topic-chain-biz/.../IndustryChainUxController.java` |
| Feign | `.../feign/RemoteChainUxClient.java` |
| 分析维度 | `IndustryFacadeController#analysisDims` |
| 写库 | `gkxlumen-topic-enterprise-biz/.../ChainUxInternalController.java` |
| DTO | `...-api/.../dto/chainux/ChainUxDTOs.java` |
| 本 handoff | `LUMEN-CHAIN-JAVA-BIZ-UX-L01.md` |
