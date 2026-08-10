# Handoff — E-TECH-NEWS-ENTITY-M3-L02

> **status**: done  
> **claimed_by**: agent:api-agent  
> **supervised_by**: human:孙英哲  
> **claim_type**: coordinator_dispatch  
> **completed_at**: 2026-07-28T20:25:00+08:00  
> **repo**: demo-algo-science / demo-svc-platform / lumen-svc-platform / agent-delivery  

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| 实体 ADS DDL 可执行（非仅草案） | `demo-algo-science/scripts/sql/ads_tech_news_entity.sql`；已并入 `scripts/schema_mysql.sql` |
| Wave0 落库 + 查询 | `persist.save_entity_extract` 写头表/实体行/事件行；`GET /internal/tech-news/entity-extractions*` |
| demo + lumen 查询 REST | `GET /v1/tech-news/entity-extractions` + `/{id}`（Feign / RestTemplate 透传） |
| java-integration as-built | `agent-delivery/designs/tech_news_ie/docs/java-integration.md` §1–§3.2 |
| 冒烟 | pytest entity_ext **14 passed**；`mvn -pl gkx-innov` / `gkxlumen-innov` compile 绿 |

---

## 2. 偏离

- 正式 MySQL 写入仍可由后续任务接；本期 Wave0 以 Python SQLite 镜像 ADS 列契约，Java 只读转发查询。
- 完整 Spring 网关在线冒烟待环境（与既有残留同类）。

---

## 3. 验收命令

```powershell
# algo
cd repos/demo-algo-science
$env:PYTHONPATH=(Get-Location).Path; $env:TECH_NEWS_IE_MODE='mock'
.\.venv\Scripts\python -m pytest tests/tech_news_ie/entity_ext -q
# 14 passed

# java
cd repos/demo-svc-platform; mvn -pl gkx-innov -am compile -DskipTests -q
cd repos/lumen-svc-platform; mvn -pl gkxlumen-innov -am compile -DskipTests -q
```

---

## 4. 架构合规自检

1. 算法只在 Python ✅  
2. 前端→Java→Python `/internal/*` ✅  
3. 未引入 Neo4j ✅  
4. Java 不写抽取算法，仅转发/契约 ✅  

---

## 5. 开放项

- L03：复核页列表/回看接 `entity-extractions`  
- 网关在线冒烟 / MySQL 实落库  

---

## 6. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 55k |
| actual_cost | ~$0.30 |
| cost_warn | green |


---

## 7. 验收关单

- **accepted_by**: human:孙英哲
- **accepted_at**: 2026-07-29T11:41:43+08:00
- **result**: PASS
- **recheck**: pytest entity_ext 15 passed；demo/lumen `mvn -pl … compile -DskipTests` exit 0
- **follow-up**: L03 已升 `ready`（未自动开工）
