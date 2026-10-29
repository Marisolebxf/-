# Handoff — E-TECH-NEWS-ENTITY-M4-L01

> **status**: done  
> **claimed_by**: agent:algorithm-agent  
> **supervised_by**: human:孙英哲  
> **claim_type**: coordinator_dispatch  
> **completed_at**: 2026-07-29T12:15:00+08:00  
> **repo**: demo-algo-science / agent-delivery  

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| `TECH_NEWS_IE_STORE=sqlite\|mysql\|dual` | `innov/tech_news_ie/config.py`；healthz 返回 `store` |
| entity-extract 可写 MySQL ADS 三表 | `persist_mysql.py` + `ExtractionStore.save_entity_extract` |
| list/get 在 mysql 模式读 ADS | `list_entity_extracts` / `get_entity_extract` |
| `.env.example` + as-built | `.env.example`；`java-integration.md` §3.2 |
| pytest | `entity_ext` **16 passed, 1 skipped**（MySQL live smoke 需 `TECH_NEWS_IE_MYSQL_SMOKE=1`） |

### 改动文件

- `innov/tech_news_ie/persist_mysql.py`（新）
- `innov/tech_news_ie/persist.py` / `config.py` / `api.py`
- `scripts/sql/mysql/innov_table_map.yaml`
- `tests/tech_news_ie/entity_ext/test_entity_m4_mysql_store.py`
- `.env.example`
- `agent-delivery/designs/tech_news_ie/docs/java-integration.md`

---

## 2. 偏离

- 本机无法连通 `10.50.11.76:3306`（超时），未做 live MySQL 写入验收；默认仍 `sqlite`，不破坏 CI。
- 正式库需已执行 `ads_tech_news_entity.sql`；运维侧执行 DDL + 配 `INNOV_MYSQL_*` 后设 `TECH_NEWS_IE_STORE=mysql|dual`。

---

## 3. 验收命令

```powershell
cd repos/demo-algo-science
$env:PYTHONPATH=(Get-Location).Path; $env:TECH_NEWS_IE_MODE='mock'
.\.venv\Scripts\python -m pytest tests/tech_news_ie/entity_ext -q
# 可选 live：TECH_NEWS_IE_MYSQL_SMOKE=1 + INNOV_MYSQL_* 
```

---

## 4. 架构合规

1. 算法/落库在 Python ✅  
2. Java 仍透传 ✅  
3. ADS 表在 `gkxlumenx_ads` ✅  

---

## 5. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 70k |
| actual_cost | ~$0.40 |
| cost_warn | green |


---

## 验收关单

- **accepted_by**: human:孙英哲
- **accepted_at**: 2026-07-29T12:15:17+08:00
- **result**: PASS
