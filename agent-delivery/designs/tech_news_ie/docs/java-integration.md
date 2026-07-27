# Java → Python 对接契约（E-TECH-NEWS-IE-M1-L02 Phase B）

> 正式调用链：前端 → Java REST → Python `/internal/tech-news/*`。  
> Java 不写 NLP / LLM / 抽取逻辑。

## 1. Python 接口

| Method | Path | 说明 |
|--------|------|------|
| POST | `/internal/tech-news/extract?persist=true` | 抽取；Header 可选 `X-Request-Id` |
| GET | `/internal/tech-news/extractions?limit&offset` | 历史列表 |
| GET | `/internal/tech-news/extractions/{request_id}` | 详情 |

请求体字段：`request_id?` / `title?` / `content` / `published_at?` / `source?` / `options?`。

## 2. Java 门面（已落地）

### 2.1 demo-svc-platform（`gkx-innov`）

| 类 | 路径 |
|----|------|
| Feign | `com.topcomm.gkx.innov.technews.TechNewsAlgoClient` |
| Service | `TechNewsExtractService` |
| Controller | `TechNewsExtractController` → `/v1/tech-news/**` |

配置：

```yaml
gkx.innov.tech-news.algo-base-url: ${INNOV_TECH_NEWS_ALGO_BASE_URL:${INNOV_CHAIN_ALGO_BASE_URL:http://127.0.0.1:8000}}
spring.cloud.openfeign.client.config.tech-news-algo.readTimeout: 30000
```

网关：`/innov/v1/tech-news/**` → StripPrefix → `/v1/tech-news/**`。

### 2.2 lumen-svc-platform（`gkxlumen-innov`）

| 类 | 路径 |
|----|------|
| RestTemplate 透传 | `com.topcomm.gkxlumen.innov.technews.TechNewsExtractService` |
| Controller | `TechNewsExtractController` → `/v1/tech-news/**`（`R.ok` 包络） |

配置见 `gkxlumen-innov/src/main/resources/application-tech-news.yml`（读超时默认 30s）。

## 3. ADS 草案（demo-algo-science）

| 表 | 说明 |
|----|------|
| `ads_tech_news_extraction` | 请求头 + 完整 JSON |
| `ads_tech_news_event` | 事件行（公司/时间/事项/影响） |

- 增量脚本：`scripts/sql/ads_tech_news_ie.sql`
- 已并入：`scripts/schema_mysql.sql`

Wave 0：可继续用 Python `persist=true`（SQLite）；ADS 表供正式 MySQL 迁移与 Java 只读查询承接。

## 4. 验收清单

- [x] Java Client/转发（超时 ≥ 30s，透传 `X-Request-Id`）
- [x] Controller 对外 REST
- [x] ADS DDL 草案
- [ ] 联调：Java → 运行中的 innov-py mock/llm
- [ ] 网关路由登记（若尚未有 `/innov/v1/tech-news/**`）
