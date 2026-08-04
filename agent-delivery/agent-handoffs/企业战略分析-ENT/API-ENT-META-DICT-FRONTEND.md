# API-ENT-META-DICT — 企业字典透传契约（前端 / Java）

> 日期：2026-08-04  
> 作者：`[agent:data-agent]`  
> 网关前缀：`/enterprise`（**不要**写成 `/api/enterprise`；浏览器若经前端 nginx，才会带 `/api` 前缀，nginx 剥掉后再进网关）  
> Java 门面：`/topic/v1/search/meta/**` → Feign → Python `/internal/gkx-search/meta/**`  
> 状态：**含 `/meta/chains` 在内，下列字典 Java 门面均已存在**（`chains` 由 `API-ENT-META-CHAINS-JAVA-L01` 落地，catalog #138）

---

## 0. 前端怎么用（速查）

| 场景 | 调哪个 | Body 示例 | 取哪个字段 |
|---|---|---|---|
| 查企业 · 查询示例热词 chip | `POST /topic/v1/search/hot` | `{"size":10}` | `data[].keyword` |
| 查企业 · 热门/示例企业（可点详情） | `POST /topic/v1/recommend` | `{"count":5}` | `data.items[].org_id` / `name_cn` |
| 高筛 · 国民经济行业 | `POST /topic/v1/search/meta/industries` | `{"mode":"tree"}` 或 `{"parent_code":"0"}` | `data.items[].code/name` |
| 重点企业分析 / 深圳现状 · **产业链**下拉 | `POST /topic/v1/search/meta/chains` | `{}` 或 `{"keyword":"人工"}` | `data.items[].code/name` → 作 `chain_code` / `chain_codes` |
| 行政区划 | `POST /topic/v1/search/meta/regions` | `{"mode":"tree"}` | `data.items[]` |
| 运营地域（热门科创等） | `POST /topic/v1/search/meta/region-scopes` | `{}` | `data.items[]` |
| 工商企业类型 | `POST /topic/v1/search/meta/company-types` | `{}` | `data.items[]` |
| 企业规模四档 | `POST /topic/v1/search/meta/enterprise-scales` | `{}` | `data.items` + `is_above_scale` |
| 资质/标签（高企等） | `POST /topic/v1/search/meta/tags` | `{"category":"qualification"}` 可选 | `data.items[].tag_code` |
| 小型固定枚举 | `POST /topic/v1/search/meta/filters` | `{}` | 上市状态/经营状态等 |
| 高筛字段目录 | `POST /topic/v1/search/meta/query-tree-schema` | `{}` | `fields[].value_source` → 再调上表 |

> **勿混**：`meta/industries` = 国标行业（GB/T 4754）；`meta/chains` = 产业链（IC001/低空经济…）。重点企业分析 / 深圳现状要的是 **chains**。

---

## 1. 已就绪 Java 路径（昨天 DIM 独立字典，门面已通）

| Java（前端调） | Python | 说明 | Java 状态 |
|---|---|---|---|
| `/topic/v1/search/meta/filters` | `/internal/gkx-search/meta/filters` | 小型固定枚举 | ✅ 已透传 |
| `/topic/v1/search/meta/query-tree-schema` | `.../meta/query-tree-schema` | 高筛目录 + value_source_apis | ✅ |
| `/topic/v1/search/meta/regions` | `.../meta/regions` | 行政区划树 | ✅ |
| `/topic/v1/search/meta/industries` | `.../meta/industries` | 国标行业树（code_nic） | ✅ |
| `/topic/v1/search/meta/region-scopes` | `.../meta/region-scopes` | 运营地域 | ✅ |
| `/topic/v1/search/meta/company-types` | `.../meta/company-types` | 企业类型 | ✅ |
| `/topic/v1/search/meta/enterprise-scales` | `.../meta/enterprise-scales` | 规模四档 | ✅ |
| `/topic/v1/search/meta/tags` | `.../meta/tags` | 标签字典 | ✅ |
| `/topic/v1/search/hot` | `.../enterprises/hot` | 查询示例热词 | ✅ |
| `/topic/v1/recommend` | `.../enterprises/recommend` | 热门企业 | ✅ |
| `/topic/v1/search/meta/chains` | `.../meta/chains` | **产业链字典（新增）** | ✅ 已透传（`9fc2fe8`） |

联调网关示例：

```http
POST {gateway}/enterprise/topic/v1/search/meta/industries
Content-Type: application/json

{"mode":"tree"}
```

---

## 2. `/meta/chains`（Java 已透传）

### 2.1 契约

**Python**：`POST /internal/gkx-search/meta/chains`  
**服务内**：`POST /topic/v1/search/meta/chains`（`EnterpriseMetaDictController`）  
**网关**：`POST {gateway}/enterprise/topic/v1/search/meta/chains`

**Request**（均可选）：

```json
{ "keyword": "人工" }
```

**Response**：

```json
{
  "code": 0,
  "data": {
    "items": [
      { "code": "IC001", "name": "集成电路" },
      { "code": "AI001", "name": "人工智能" }
    ]
  }
}
```

| 字段 | 用途 |
|---|---|
| `code` | 深圳现状 `chain_code`；重点企业分析 `chain_codes[]`；高筛 `industry_chain_code` |
| `name` | 下拉展示；高筛 `industry_chain` |

数据源：`gkxlumenx_dwd.chain`；空/失败时回落固定清单（含低空/海洋/量子等）。

### 2.2 高筛挂接

`query-tree-schema` 已改：

- `industry_chain` → `value_source=meta_chains`，`value_field=name`
- `industry_chain_code` → `value_source=meta_chains`，`value_field=code`
- `value_source_apis.meta_chains` = `POST /internal/gkx-search/meta/chains`

---

## 3. 查企业热词 vs 热门企业（产品约定）

| 需求 | 接口 | 返回 | 交互 |
|---|---|---|---|
| 查询示例 / 热词 | `/topic/v1/search/hot` | `{keyword,count}` | 点选填入搜索框 |
| 热门企业 | `/topic/v1/recommend` | 企业卡片字段含 `org_id` | 点选进详情 |

**不要**把 `/hot` 改成返回企业（会破坏现有 `HotKeywordItem` 契约）。

---

## 4. 给前端的联调说明

产业链字典请走网关门面：

`POST {gateway}/enterprise/topic/v1/search/meta/chains` + `{}` 或 `{"keyword":"..."}`

（若前端经 nginx `/api/` 代理，浏览器侧会写成 `/api/enterprise/...`，进网关前会被剥掉 `/api`。）

正式环境禁止前端直连 Python。

其余字典（industries/regions/tags…）同样按 §0 表调 Java 门面。
