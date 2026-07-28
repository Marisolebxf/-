# Handoff · E-TECH-NEWS-IE-M1-L04（质量加固 · 金标回归）

> **范围**：四要素抽取质量加固 — 文类门控 / impact 优先非空 / 事件去重 / 相对时间 / 金标 G01–G28 / 评测 CLI  
> **仓**：`demo-algo-science`（`origin/dev`）  
> **claimed_by**：`agent:algorithm-agent`（本会话执行；未新开 registry 认领条，承接 M1 后质量波次）  
> **supervised_by**：待监管人确认（建议沿用 M1 监管：`human:淮政玮` / 联调侧 `human:杨英杰`）  
> **日期**：2026-07-28  
> **状态**：`review`（算法产物已 push，待监管人验收关单）

---

## 1. 交付结论

在 M1-L01～L03 已通调用链之上，完成**抽取质量与可回归评测**加固，并推送：

| 项 | 结果 |
|----|------|
| Commit | `0ec4013` |
| 分支 | `dev` → 已 `git push origin/dev` |
| 金标 | `tests/tech_news_ie/gold/` · **G01–G28** |
| mock 金标 | **28/28** · KPI 全达门槛 |
| LLM 金标 | 初跑 26/27（G02 公司简称）；修复匹配后 G02 复测通过 |
| 网页烟测 | 10 URL；门控准确；Solidot 标题 +「上市」财经事项过滤已补 |

**未改**：Java Controller / 前端页面代码（本波次仅算法仓）。

---

## 2. 行为变更（联调必读）

### 2.1 文类门控（软拒绝 HTTP 200）

`POST /internal/tech-news/extract` 遇门控时：

- HTTP **200**
- `events: []`
- `error.code` ∈  
  `opinion_or_commentary` / `policy_or_legal_noise` / `consumer_retail_noise`
- `error.message` 形如 `document gated: …`

Java / 前端应把 `error` 当**业务拦截**展示，勿一律当 5xx。

### 2.2 Impact

- 提示词 + 规则兜底：**优先非空**（有价值从句则填）
- 禁止 matter≈impact；跨事件禁止复制同一 impact
- 页面噪声（「传递更多信息」等）不得作 impact
- 全文确无效果句时仍可为 `null`（金标 G02）

### 2.3 其它

- 相对时间：昨日/本月/上月/去年/今年/明年（锚定 `published_at` 或当天）
- 同公司 + 产品代号（如 RACCO）近重复合并
- 财经「上市」类 `completed_matter` 过滤（`finance_matter_dropped`）
- Solidot 标题从 `|` 右侧 / `.title` 节点恢复

### 2.4 LLM 配置（`.env.example`）

默认示例改为智谱 BigModel：`glm-4-flash`；`LLM_TIMEOUT_SEC` 建议 ≥ 60（长文 + impact 二轮更稳）。

---

## 3. 产物清单

| 产物 | 路径 |
|------|------|
| 门控 | `innov/tech_news_ie/gate.py` |
| Impact | `innov/tech_news_ie/impact_pass.py` / `candidates.py` / prompts |
| 时间 | `innov/tech_news_ie/_time_resolve.py` |
| 去重 | `innov/tech_news_ie/event_dedup.py` |
| 金标评测 | `innov/tech_news_ie/gold_eval.py` |
| 金标用例 | `tests/tech_news_ie/gold/cases/G*.json` |
| CLI | `scripts/tech-news-gold-eval.ps1` / `tech_news_web_smoke.py` / URL 抽取脚本 |
| API 门控 200 | `innov/tech_news_ie/api.py` |

---

## 4. 验证证据

```text
# mock 金标
.\scripts\tech-news-gold-eval.ps1 -Mode mock
→ passed=28/28 threshold_ok=True

# pytest
pytest tests/tech_news_ie/test_gold_regression.py tests/tech_news_ie/test_gate_dedup_time_v3.py -q
→ green

# 网页烟测（llm，抽样）
python scripts/tech_news_web_smoke.py --mode llm
→ 门控样例 PASS；技术样例可抽；Solidot 无效果句不强制 impact
```

本地报告示例：`%TEMP%\tech-news-ie\gold-report.json` / `web-smoke.json`。

---

## 5. 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ |
| 2 | 前端→Java→Python `/internal/*` | ✅ 未越层 |
| 3 | 图谱 Nebula | N/A |
| 4 | 可观测性 | ⚠️ 本波未改 instrument |
| 5 | CI/CD | ✅ push `origin/dev` |
| 6 | demo≠lumen merge | ✅ 仅 demo-algo |
| 7 | 共享聚合 | N/A |
| 8 | ADS/Mock | ✅ SQLite persist 仍可用 |
| 9 | Design.md 前端 | N/A（算法） |
| 10 | 数据血缘 | N/A 本波无新 KPI 卡；既有 M_TNIE_EVENT_COUNT 仍有效 |

---

## 6. 下游联调清单（下一步）

### Java（api-agent / 监管人）

1. Feign/RestTemplate **读超时**已提至 **120s**（本波次已改并本地 commit，待 push）：  
   - `demo-svc-platform` `d8f2456`  
   - `lumen-svc-platform` `59d9f6c`
2. 透传完整 `ExtractResponse.error`（含门控 code）— Service 已 Map 透传，**OK**
3. 确认网关 `/innov/v1/tech-news/**` 仍可达（L03 evidence：Helm `/innov/**` 覆盖）

### 前端（frontend-agent）— 盘点结论

| 项 | 现状（`origin/dev`） | 缺口 |
|----|----------------------|------|
| 页面 | `/service/tech-news-review` · `src/views/tech-news/index.vue` | — |
| 只调 Java | ✅ `/innov/v1/tech-news/**` | — |
| `error` 展示 | `a-alert type="error"` + `Message.error` | 门控应改为 **warning/info「文类已拦截」**，勿当系统失败 |
| impact null | 显示字面 `null` | 改为「暂无 / —」 |
| flags | Tag 展示 | 可强调 `gated_*` / `finance_matter_dropped` |

建议下一前端微修复任务：`E-TECH-NEWS-IE-M1-L05`（门控 UX + null 文案）。

### 口径（待甲方 / 监管拍板）

- 零售开售 vs 产品发布边界（当前：标题开售+元价 → 门控）
- impact「优先非空」是否写进产品验收（当前算法侧已按此训练）

---

## 7. 给监管人

请确认：

1. `0ec4013` 行为变更可接受  
2. 是否需要正式 registry 条 `E-TECH-NEWS-IE-M1-L04` 并关单  
3. 是否立即排期 Java 超时 + 前端门控展示
