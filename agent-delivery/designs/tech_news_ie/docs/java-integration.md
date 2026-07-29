# Java → Python 对接契约（E-TECH-NEWS-IE-M1-L02 Phase B）

> 正式调用链：前端 → Java REST → Python `/internal/tech-news/*`。  
> Java 不写 NLP / LLM / 抽取逻辑。

## 1. Python 接口

| Method | Path | 说明 |
|--------|------|------|
| POST | `/internal/tech-news/extract?persist=true` | 四要素抽取；Header 可选 `X-Request-Id` |
| POST | `/internal/tech-news/entity-extract?persist=true` | 实体扩展抽取（7 类实体 + event_type）；M2-L02 |
| GET | `/internal/tech-news/extractions?limit&offset` | 四要素历史列表 |
| GET | `/internal/tech-news/extractions/{request_id}` | 四要素详情 |
| GET | `/internal/tech-news/entity-extractions?limit&offset` | 实体扩展历史列表（M3-L02） |
| GET | `/internal/tech-news/entity-extractions/{request_id}` | 实体扩展详情（entities/events + response） |

请求体字段：`request_id?` / `title?` / `content` / `published_at?` / `source?` / `options?`。

## 2. Java 门面（已落地）

### 2.1 demo-svc-platform（`gkx-innov`）

| 类 | 路径 |
|----|------|
| Feign | `com.topcomm.gkx.innov.technews.TechNewsAlgoClient` |
| Service | `TechNewsExtractService` |
| Controller | `TechNewsExtractController` → `/v1/tech-news/**` |

对外：

| Method | Path | 上游 |
|--------|------|------|
| POST | `/v1/tech-news/extract` | `/internal/tech-news/extract` |
| POST | `/v1/tech-news/entity-extract` | `/internal/tech-news/entity-extract` |
| GET | `/v1/tech-news/extractions` | 同左 |
| GET | `/v1/tech-news/entity-extractions` | `/internal/tech-news/entity-extractions`（M3-L02） |
| GET | `/v1/tech-news/entity-extractions/{id}` | 同左详情 |

配置：

```yaml
gkx.innov.tech-news.algo-base-url: ${INNOV_TECH_NEWS_ALGO_BASE_URL:${INNOV_CHAIN_ALGO_BASE_URL:http://127.0.0.1:8000}}
spring.cloud.openfeign.client.config.tech-news-algo.readTimeout: 120000
```

属性 `gkx.innov.tech-news.read-timeout-ms` 默认同为 **120000**（LLM + impact 二轮）。

网关：`/innov/v1/tech-news/**` → StripPrefix → `/v1/tech-news/**`（已覆盖 `entity-extract` / `entity-extractions`）。

### 2.2 lumen-svc-platform（`gkxlumen-innov`）

| 类 | 路径 |
|----|------|
| RestTemplate 透传 | `com.topcomm.gkxlumen.innov.technews.TechNewsExtractService` |
| Controller | `TechNewsExtractController` → `/v1/tech-news/**`（`R.ok` 包络） |

对外同 demo：含 `POST /entity-extract` 与 `GET /entity-extractions[/{id}]`。

配置见 `gkxlumen-innov/src/main/resources/application-tech-news.yml`（读超时默认 **120s**）。

## 3. ADS（as-built · E-TECH-NEWS-ENTITY-M3-L02）

### 3.1 四要素

| 表 | 说明 |
|----|------|
| `ads_tech_news_extraction` | 请求头 + 完整 JSON |
| `ads_tech_news_event` | 事件行（公司/时间/事项/影响） |

- 增量脚本：`scripts/sql/ads_tech_news_ie.sql`
- 已并入：`scripts/schema_mysql.sql`

### 3.2 实体扩展（非仅草案）

| 表 | 说明 |
|----|------|
| `ads_tech_news_entity_extract` | 实体扩展请求头 + 完整 JSON |
| `ads_tech_news_entity` | 实体行（type/name/evidence/confidence） |
| `ads_tech_news_entity_event` | 事件扩展行（含 `event_type` / `news_source` / `entity_refs`） |

- 增量脚本：`scripts/sql/ads_tech_news_entity.sql`
- 已并入：`scripts/schema_mysql.sql`
- Wave0 写入：Python `persist=true` → SQLite 同名逻辑表（`ExtractionStore.save_entity_extract`）
- **M4-L01**：`TECH_NEWS_IE_STORE=sqlite|mysql|dual`；`mysql`/`dual` 写入 `gkxlumenx_ads.ads_tech_news_entity*`（复用 `INNOV_MYSQL_*`）；`list/get entity-extractions` 在 `mysql` 模式读 ADS，`dual` 优先 MySQL 失败回退 SQLite
- 查询：Python `/internal/tech-news/entity-extractions*` → Java `/v1/tech-news/entity-extractions*`
- 表名映射：`scripts/sql/mysql/innov_table_map.yaml`（`ads_tech_news_entity*`）

## 4. 验收清单

- [x] Java Client/转发（超时 ≥ 30s，透传 `X-Request-Id`）
- [x] Controller 对外 REST（含 `entity-extract`，E-TECH-NEWS-ENTITY-M2-L02）
- [x] ADS DDL（四要素）+ 实体扩展正式 DDL（M3-L02）
- [x] MySQL ADS 写/读开关（E-TECH-NEWS-ENTITY-M4-L01）
- [x] 实体扩展查询 REST（demo + lumen，M3-L02）
- [x] 联调：Java 契约客户端 / Python mock（见 `agent-handoffs/evidence/E-TECH-NEWS-IE-M1-L03/02-smoke*`）；完整 Spring+网关在线待环境恢复
- [x] 网关路由：Helm `Path=/innov/**` 已覆盖 `/innov/v1/tech-news/**`（见 evidence `01-gateway-route.md`）
