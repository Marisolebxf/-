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

- `POST /internal/tech-news/entity-extract`（mock-first；**LLM 已于 2026-07-28 用智谱 glm-4-flash 实跑补齐**）
- 包：`innov/tech_news_ie/entity_ext/`

---

## 2. 偏离说明

- 初版 PDR 交付为 mock-first（Wave1 LLM 后置）；**2026-07-28 监管人补跑智谱**后，LLM 接线与 10 篇样例实跑证据已齐（见 §3）。
- `company_name` 仍为兼容字段，科研机构也会填入主体列表（与四要素一致），细分类在 `entities[].type`。

---

## 3. 验收证据

```text
cd repos/demo-algo-science
$env:PYTHONPATH=(Get-Location).Path
$env:TECH_NEWS_IE_MODE='mock'
.\.venv\Scripts\python -m pytest tests/tech_news_ie/entity_ext -q
# mock 回归（历史：2 passed；现 entity_ext 全套更多）
```

### 3.1 智谱 LLM 实跑（PDR 残留关闭 · 2026-07-28）

| 项 | 值 |
|----|-----|
| Endpoint | `https://open.bigmodel.cn/api/paas/v4/chat/completions` |
| Model | `glm-4-flash` |
| 样例 | `pdr_samples.json` 共 10 篇 |
| 结果 | **llm_ok=10 / fallback_mock=0** |
| 证据文件 | `innov/tech_news_ie/entity_ext/samples/pdr_llm_zhipu_20260728.json` |

```powershell
$env:TECH_NEWS_IE_MODE='llm'
$env:LLM_BASE_URL='https://open.bigmodel.cn/api/paas/v4'
$env:LLM_MODEL='glm-4-flash'
$env:LLM_API_KEY='<from env, never commit>'
$env:LLM_TIMEOUT_SEC='120'
# 跑 entity pipeline → 见上证据 JSON
```

> API Key 仅环境变量注入；**禁止写入仓库 / handoff 明文**。

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
- ~~Wave1：LLM 路径接线~~ → **已关闭**（智谱 glm-4-flash，10/10，见 §3.1）  
- ~~Wave2：Java 门面 / ADS~~ → 已由 ENTITY-M2 / M3 承接  

---

## 6. Cost（回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~估 80k（会话量级，未精确计量）+ 智谱补跑约 10 次 chat |
| model_used | cursor-grok-4.5 + zhipu glm-4-flash（补跑） |
| actual_cost | ~$0.5（估，不含智谱计费） |
| cost_warn | green |
