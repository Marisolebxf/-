# Handoff · 科技新闻四要素抽取（本地沙箱）

> **范围**：`agent-delivery/designs/tech_news_ie/` 本地沙箱（未入 `task-registry`）  
> **领域**：科技新闻信息抽取（非金融）  
> **状态**：Phase 0–4 沙箱闭环完成 · 2026-07-27  
> **作者标记**：`[agent:algorithm-agent]`（沙箱，无正式认领）

---

## 1. 交付结论

已实现「科技新闻 → 四要素结构化结果 → 落库 → 复核页」端到端原型：

| 字段 | 口径（已按示例确认） |
|------|----------------------|
| 公司名称 | 成果主体机构（支持别名归一） |
| 完成时间 | 成果完成/交付/落地时间，非「今日宣布」 |
| 完成事项 | 技术/产品/工程事实 |
| 作用与影响 | 技术/应用效果；无据则为 null |

验证：

- `pytest`：**28 passed**
- `scripts/eval_report.py`：**9/9**（含 hard 4/4）

---

## 2. 产物清单

| 产物 | 路径 |
|------|------|
| 设计说明 | `agent-delivery/designs/tech-news-four-field-extraction-llm-schema.md` |
| 沙箱代码 | `agent-delivery/designs/tech_news_ie/` |
| Java 对接契约 | `tech_news_ie/docs/java-integration.md` |
| 正式迁移方案 | `tech_news_ie/docs/formal-migration-plan.md` |
| 复核页 | `GET http://127.0.0.1:8010/review` |
| 抽取 API | `POST /internal/tech-news/extract` |

---

## 3. 架构合规自检（沙箱视角）

| 铁律 | 状态 |
|------|------|
| 算法只在 Python | ✅ 沙箱为纯 Python |
| 调用链 前端→Java→Python | ⚠️ 沙箱复核页直连 Python（演示例外）；正式须经 Java |
| 图谱 Nebula | N/A（本任务无图谱） |
| 可观测性 | ⚠️ 仅有 logging；正式需补 OTel |
| demo 不 merge lumen | ✅ 未改 lumen 仓 |
| 前端 Design.md | ⚠️ 复核页为简易 HTML，非正式 Arco 页 |

---

## 4. 未做 / 开放项

1. **正式仓接入**：`demo-algo-science` / `lumen-svc-platform` / 前端仓尚未改代码  
2. **真实 LLM 验收**：默认 mock；需配置 `TECH_NEWS_IE_MODE=llm` 做抽检  
3. **模型蒸馏**：Phase 3 可选，暂缓  
4. **registry 任务**：无 task-id；升正式交付前需新建并认领  

---

## 5. 建议的下一步（需人确认）

按优先级：

1. **正式迁移 Phase A**：把 `tech_news_ie` 迁入 `demo-algo-science` 并挂到现有 FastAPI  
2. **正式迁移 Phase B**：Java 转发 + ADS DDL  
3. **正式迁移 Phase C**：按 Design.md 做正式复核 UI  

详见 `formal-migration-plan.md`。启动正式仓改动前，请提供：

- `task-id`
- `supervised_by`（花名册真名）
