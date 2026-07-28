# Handoff — E-TECH-NEWS-ENTITY-M2-L02

> **status**: review  
> **claimed_by**: agent:api-agent  
> **supervised_by**: human:孙英哲  
> **claim_type**: coordinator_dispatch  
> **completed_at**: 2026-07-28T19:20:00+08:00  
> **repos**: demo-svc-platform · lumen-svc-platform · gkx-orchestration（契约文档）

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| demo-svc + lumen-svc 暴露 entity-extract REST | `POST /v1/tech-news/entity-extract` → Python `/internal/tech-news/entity-extract` |
| ADS/落库说明更新 | `agent-delivery/designs/tech_news_ie/docs/java-integration.md` |
| 读超时 ≥120s | 沿用既有 Feign / RestTemplate tech-news 配置（120s） |
| handoff | 本文件 |

### 改动类

**demo-svc-platform**（Feign）：

- `TechNewsAlgoClient#entityExtract`
- `TechNewsExtractService#entityExtract`
- `TechNewsExtractController` `POST /entity-extract`

**lumen-svc-platform**（RestTemplate + `R.ok`）：

- 同上 Controller/Service 方法

上游不可达时 fallback 含 `events: []` 与 `entities: []`。

---

## 2. 偏离

- 未新建独立 ADS 实体表 DDL；Wave0 继续 Python SQLite `persist`；文档已标注后续 `ads_tech_news_entity` 草案位。
- 完整 Spring 网关在线冒烟待环境；本机 `gkx-innov` 已 `mvn compile` 通过。

---

## 3. 架构合规

1. 算法只在 Python ✅（Java 仅透传）  
2. 调用链 前端→Java→Python `/internal/*` ✅  
3. 不直连 nGQL ✅  
4. 超时沿用 120s ✅  

---

## 4. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 35k |
| actual_cost | ~$0.2 |
| cost_warn | green |
