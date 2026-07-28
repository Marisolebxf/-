# Handoff — E-TECH-NEWS-ENTITY-M2-L01

> **status**: done  
> **claimed_by**: agent:algorithm-agent  
> **supervised_by**: human:孙英哲  
> **claim_type**: coordinator_dispatch  
> **completed_at**: 2026-07-28T19:00:00+08:00
> **accepted_at**: 2026-07-28（监管人指示关单；pytest 6 passed 复验）  
> **repo**: demo-algo-science  

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| LLM 宽松字段形状单测 | `tests/tech_news_ie/entity_ext/test_entity_m2_l01.py::test_parse_llm_loose_shapes` |
| week + 非法 granularity 不崩；slash 日期归一 | `_as_completion_time` + `test_as_completion_time_slash_and_week`；LLM 后 `enrich_completion_time` |
| 实体金标 ≥10 | `entity_ext/samples/pdr_samples.json`（10 条）；覆盖 7 类实体 |
| llm 失败 notes 显式 | `test_llm_fallback_notes_not_silent`（含异常信息，非静默成功） |
| pytest 全绿 | `pytest tests/tech_news_ie/entity_ext` → **6 passed** |

代码：`innov/tech_news_ie/entity_ext/pipeline.py`（解析容错 + 时间 enrich）。

---

## 2. 偏离

- 金标当前以 **mock** 路径回归为主；LLM 端到端金标评测 CLI 可在后续加活（本单已有 web 实跑证据 `samples/llm_web_run_20260728.json`）。
- Q051/Q052 仍 🟡，schema 未升 v1.0。

---

## 3. 验收命令

```powershell
cd repos/demo-algo-science
$env:PYTHONPATH=(Get-Location).Path
$env:TECH_NEWS_IE_MODE='mock'
.\.venv\Scripts\python -m pytest tests/tech_news_ie/entity_ext -q
# 6 passed
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

- L02 Java 转发 entity-extract（backlog，依赖本单 done）  
- LLM 金标评测脚本（可选）  

---

## 6. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 40k |
| actual_cost | ~$0.25 |
| cost_warn | green |
