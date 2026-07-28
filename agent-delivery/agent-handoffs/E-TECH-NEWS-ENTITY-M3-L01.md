# Handoff — E-TECH-NEWS-ENTITY-M3-L01

> **status**: review  
> **claimed_by**: agent:algorithm-agent  
> **supervised_by**: human:孙英哲  
> **claim_type**: coordinator_dispatch  
> **completed_at**: 2026-07-28T20:15:00+08:00  
> **repo**: demo-algo-science  

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| 四要素 impact ↔ 实体联合校验（冲突进 notes/flags） | `entity_ext/quality.py::validate_impact_entity_joint`；pipeline 末尾调用 |
| event_type 归一到 PDR 枚举（含 other）；非法不崩 | `normalize_event_type`；`_parse_llm_entity_payload` + mock 路径 |
| 回归 ≥3 联合 + ≥3 event_type | `tests/.../test_entity_m3_l01.py` |
| llm 失败禁止静默冒充 | 沿用 M2：`test_llm_fallback_notes_not_silent` |
| pytest 全绿 | `pytest tests/tech_news_ie/entity_ext` → **13 passed** |

代码：

- `innov/tech_news_ie/entity_ext/quality.py`（新）
- `innov/tech_news_ie/entity_ext/pipeline.py`（v0.3 + joint）

联合规则（软警告，不硬拒）：

- `impact_duplicates_matter`
- `impact_empty`
- `company_missing_from_entities`
- `entity_ref_unresolved`
- `event_type_entity_mismatch`（product_release / policy_publish）

---

## 2. 偏离

- Q051/Q052 仍 🟡；schema 保持 `entity-v0.1`，未升 v1.0。
- 联合校验为规则启发式，非再调 LLM。

---

## 3. 验收命令

```powershell
cd repos/demo-algo-science
$env:PYTHONPATH=(Get-Location).Path
$env:TECH_NEWS_IE_MODE='mock'
.\.venv\Scripts\python -m pytest tests/tech_news_ie/entity_ext -q
# 13 passed
```

---

## 4. 架构合规自检

1. 算法只在 Python ✅  
2. `/internal/*` 未越层 ✅  
3. 未引入 Neo4j ✅  
4. 仅 demo-algo-science ✅  
5. 调用链预留 ✅  

---

## 5. 开放项

- L02：实体 ADS DDL + Java 落库/查询（backlog，依赖本单 done）  
- Q051/Q052 甲方确认后冻结 schema v1.0  

---

## 6. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 45k |
| actual_cost | ~$0.25 |
| cost_warn | green |
