# Handoff — E-TECH-NEWS-ENTITY-PDR-L01

> **status**: review  
> **claimed_by**: agent:algorithm-agent  
> **supervised_by**: human:孙英哲  
> **claim_type**: coordinator_dispatch  
> **completed_at**: 2026-07-27T19:05:00+08:00（本地）  
> **repo**: demo-algo-science（沙箱）+ gkx-orchestration/agent-delivery（设计）

---

## 1. 范围与实现

对照 task DoD / 招标科创事件 + NER：

| DoD | 产物 |
|-----|------|
| 预研报告 | `agent-delivery/designs/tech-news-entity-extraction/PDR.md` |
| 扩展 Schema（7 实体 + 事件结构，兼容四要素） | `.../schema-v0.1.json` |
| Prompt 原型可跑（mock） | `.../prompt-entity-v0.1.txt` + `innov/tech_news_ie/prompts/entity_extract_v0.1.txt` |
| ≥5 篇样例覆盖实体组合 | `innov/tech_news_ie/entity_ext/samples/pdr_samples.json` + pytest 2 passed |
| 招标差异与演进 | PDR §5 |
| 业务口径登记客户决策清单 | Q051 / Q052 🟡 |
| handoff 架构自检 | 本文件 §4 |

运行时：

- `POST /internal/tech-news/entity-extract`（mock-first；llm 模式暂回落 mock 并 note）
- 包：`innov/tech_news_ie/entity_ext/`

---

## 2. 偏离说明

- LLM 实体抽取尚未接线（PDR 明确 Wave1）；当前强制 mock 启发式，保证可测。  
- `company_name` 仍为兼容字段，科研机构也会填入主体列表（与四要素一致），细分类在 `entities[].type`。

---

## 3. 验收证据

```text
cd repos/demo-algo-science
$env:PYTHONPATH=(Get-Location).Path
$env:TECH_NEWS_IE_MODE='mock'
.\.venv\Scripts\python -m pytest tests/tech_news_ie/entity_ext -q
# ..  2 passed
```

---

## 4. 架构合规自检

1. 算法只在 Python ✅  
2. 调用链预留 `/internal/*`，未越层 ✅  
3. 未引入 Neo4j ✅  
4. 可观测性：沿用现有 FastAPI/otel（新路由挂同一 app）✅  
5. CI：本地 pytest；cicd: skip（definition）✅  
6. 未 merge lumen ✅  
7. 共享聚合：不适用（预研）✅  
8. 数据策略：Schema 先行 + mock ✅  
9. Design.md 前端：本期无 UI ✅  
10. 数据血缘：无新统计指标上屏；口径决策进 Q051/Q052 ✅  
11. D10 交互：不适用 ✅  

---

## 5. 开放项

- 甲方确认 Q051 / Q052 后冻结 schema v1.0  
- Wave1：LLM 路径接线 + 更大样例集  
- Wave2：Java 门面 / ADS（另开 task）

---

## 6. Cost（回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~估 80k（会话量级，未精确计量） |
| model_used | cursor-grok-4.5 |
| actual_cost | ~$0.5（估） |
| cost_warn | green |
