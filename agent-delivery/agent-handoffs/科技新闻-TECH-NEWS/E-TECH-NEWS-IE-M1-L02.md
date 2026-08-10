# Handoff · E-TECH-NEWS-IE-M1-L02

> **范围**：Phase B — Java 转发 tech-news 抽取 API + ADS 落库草案  
> **claimed_by**：`agent:api-agent`  
> **supervised_by**：`human:孙英哲`  
> **claim_type**：`pull`  
> **状态**：`done`（监管人验收关单 · 2026-07-27）  
> **日期**：2026-07-27

---

## 1. 交付结论

| 项 | 结果 |
|----|------|
| demo Java 门面 | `demo-svc-platform` → `origin/dev` merge `7234908` |
| lumen Java 门面 | `lumen-svc-platform` → `origin/dev` merge `e4fee82` |
| ADS DDL | `demo-algo-science` → `origin/dev` merge `0b8e6a0` |
| 契约文档 | `agent-delivery/designs/tech_news_ie/docs/java-integration.md` |

调用链：前端 → Java `/v1/tech-news/**` → Python `/internal/tech-news/*`；超时 30s；透传 `X-Request-Id`；Java 无抽取算法。

---

## 2. DoD 对照

| DoD | 状态 |
|-----|------|
| Java Client 调 Python extract（超时≥30s，X-Request-Id） | ✅ demo Feign + lumen RestTemplate |
| Java Controller 对外 REST；不写算法 | ✅ `/v1/tech-news/extract|extractions` |
| GET extractions 经 Java 转发 | ✅ 透传 Python；ADS 表供后续只读承接 |
| ADS DDL 草案 | ✅ `ads_tech_news_extraction` / `ads_tech_news_event` |
| handoff | ✅ 本文件 |

---

## 3. 产物清单

### 3.1 demo-svc-platform（`gkx-innov`）

- `com.topcomm.gkx.innov.technews.TechNewsAlgoClient`（Feign）
- `TechNewsExtractService` / `TechNewsExtractController`
- `application.yml`：`gkx.innov.tech-news.*` + Feign `readTimeout: 30000`
- 分支曾用：`feat/E-TECH-NEWS-IE-M1-L02` → 已合入 `dev`

### 3.2 lumen-svc-platform（`gkxlumen-innov`）

- `com.topcomm.gkxlumen.innov.technews.*`（RestTemplate，`R.ok` 包络）
- `resources/application-tech-news.yml`
- 分支曾用：`feat/E-TECH-NEWS-IE-M1-L02` → 已合入 `dev`

### 3.3 demo-algo-science

- `scripts/sql/ads_tech_news_ie.sql`
- `scripts/schema_mysql.sql`（已并入两表）
- 分支曾用：`feat/E-TECH-NEWS-IE-M1-L02-ads` → 已合入 `dev`

---

## 4. 验证说明

- 本机环境无 `mvn`/`mvnw`，未跑编译；合入以 git merge 无冲突为准。
- 联调建议：`TECH_NEWS_IE_MODE=mock` 起 innov-py，再调  
  `POST /innov/v1/tech-news/extract`（demo）或 lumen 对应网关路径。

---

## 5. 架构合规自检

| 铁律 | 状态 |
|------|------|
| 算法只在 Python | ✅ |
| 前端→Java→Python | ✅ |
| Java 不写 NLP | ✅ |
| 可观测性 | ⚠️ 沿用 Feign/RestTemplate + Java Agent；未单独加 span |
| CI/CD | ⚠️ 合入 dev 后依赖既有 Pipeline |
| ADS 先行 | ✅ DDL 草案已合入 |

---

## 6. 开放项（非本 task）

- Phase C：正式 Arco 复核 UI  
- 网关路由若尚未登记 `/innov/v1/tech-news/**` 需 devops 补一条  
- Java 写 ADS（当前仍可走 Python `persist=true` / SQLite）  
- 本机 Maven 编译绿

---

## 7. 验收关单

监管人 `human:孙英哲` 指示合并 MR 并关单；registry `status` → `done`。
