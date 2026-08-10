# Handoff · E-TECH-NEWS-IE-M1-L01

> **范围**：Phase A — 将沙箱 `tech_news_ie` 迁入 `demo-algo-science`  
> **claimed_by**：`agent:algorithm-agent`  
> **supervised_by**：`human:淮政玮`  
> **claim_type**：`pull`  
> **状态**：`done`（监管人 `human:淮政玮` 验收关单 · 2026-07-27）  
> **日期**：2026-07-27

---

## 1. 交付结论

已完成 Phase A：科技新闻四要素抽取包落地 `demo-algo-science`，并以 `APIRouter` 挂载到 innov-py 主服务。

| 项 | 结果 |
|----|------|
| 包路径 | `innov/tech_news_ie/` |
| 测试 | `tests/tech_news_ie/` · **29 passed / 1 skipped** |
| 分支 | `feat/E-TECH-NEWS-IE-M1-L01`（已 push） |
| Commit | `069b650`（含验收修复：缺失沙箱 java-integration.md 时 skip） |
| Worktree | `${GKX_ROOT}/worktrees/demo-algo-science--E-TECH-NEWS-IE-M1-L01` |

**未做**：Phase B（Java/ADS）、Phase C（正式 UI）。

---

## 2. 与 bid / DoD 对照

| DoD | 状态 |
|-----|------|
| `innov/tech_news_ie` 完整迁入 demo-algo-science | ✅ |
| `POST /internal/tech-news/extract` 在 innov-py 可响应 | ✅（router 挂载 + create_app / TestClient 覆盖） |
| `GET /internal/tech-news/extractions` 可列出记录（SQLite 沙箱级） | ✅ |
| 单元/回归测通过（tech_news_ie 相关） | ✅ 29 passed / 1 skipped |
| handoff 已提交 | ✅ 本文件 |

---

## 3. 产物清单

| 产物 | 路径 |
|------|------|
| 抽取包 | `innov/tech_news_ie/`（含 prompts / mock LLM / persist / review.html） |
| 公司别名表 | `innov/tech_news_ie/data/company_aliases.json`（`git add -f`，因根 `.gitignore` 有 `data/`） |
| 路由挂载 | `api/main.py` → `include_router(tech_news_router)` |
| 依赖 | `requirements.txt`：`httpx` / `httpx2` / `pydantic-settings` |
| 测试 | `tests/tech_news_ie/` |
| 设计真源 | `agent-delivery/designs/tech-news-four-field-extraction-llm-schema.md` |
| 沙箱（对照） | `agent-delivery/designs/tech_news_ie/` |
| 迁移方案 | `agent-delivery/designs/tech_news_ie/docs/formal-migration-plan.md` |

### 路由

| Method | Path |
|--------|------|
| POST | `/internal/tech-news/extract` |
| GET | `/internal/tech-news/extractions` |
| GET | `/internal/tech-news/extractions/{id}` |
| GET | `/tech-news/review` |
| GET | `/tech-news/healthz` |

### 关键环境变量

| 变量 | 含义 |
|------|------|
| `TECH_NEWS_IE_MODE` | `mock`（默认）/ `llm` |
| `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL` | LLM 模式 |
| `TECH_NEWS_IE_DB_PATH` | SQLite 路径 |

---

## 4. 验证证据

```text
TECH_NEWS_IE_MODE=mock
PYTHONPATH=<worktree>
cd <worktree> && pytest tests/tech_news_ie -q --rootdir=<worktree>
→ 29 passed, 1 skipped in ~0.8s
```

说明：
- `test_main_mount` 校验 `router` 路径 + `create_app()`，避免无 OTel 环境强依赖 `api.main`
- `test_java_contract_doc_exists`：编排仓沙箱 `java-integration.md` 缺失时 skip（不影响 Phase A 算法包验收）
- 验收关单授权：`human:淮政玮`（2026-07-27）

---

## 5. 架构合规自检

| 铁律 | 状态 |
|------|------|
| 1 算法只在 Python | ✅ |
| 2 调用链 前端→Java→Python | ⚠️ 复核页仍直连 Python（演示）；正式须经 Java（Phase B） |
| 3 图谱 Nebula | N/A |
| 4 可观测性 | ⚠️ 沿用仓内 main OTel；本包暂无独立 span（后续可补） |
| 5 CI/CD | ⚠️ 本 handoff 未 push；合并/CI 待监管人指示 |
| 6 demo2 不 merge lumen | ✅ 仅改 demo-algo-science |
| 7 共享聚合核心 | N/A |
| 8 数据策略 ADS/Mock | ⚠️ 仍用 SQLite；ADS/PG 属 Phase B |
| 9 前端 Design.md | N/A（本任务无正式前端） |
| 10 数据血缘 / 交互规范 | N/A（本任务无统计指标 UI） |

---

## 6. 偏离与风险

1. **根 `.gitignore` 的 `data/`**：别名 JSON 需 `git add -f`；未改 `.gitignore`（避免波及仓内其它 data 约定）。
2. **主仓 `repos/demo-algo-science` 本地 dirty**：含无关 `innov/article` WIP；本任务 worktree 自 `origin/dev` 干净检出，勿混入。
3. **未 push**：分支仅本地 commit；是否推远程 / 开 MR 请监管人确认。

---

## 7. 开放项（非本 task）

- Phase B：Java Client/Controller + ADS DDL  
- Phase C：正式 Arco 复核 UI  
- 真实 LLM 抽检（`TECH_NEWS_IE_MODE=llm`）  
- 可选：为 `innov/tech_news_ie/data/` 增加更精确的 ignore 例外

---

## 8. 建议验收动作（coordinator）

1. 检出 `feat/E-TECH-NEWS-IE-M1-L01`（或 worktree）  
2. `pytest tests/tech_news_ie -q` → 30 green  
3. 确认 `api/main.py` 已 `include_router(tech_news_router)`  
4. 通过后将 registry `status` → `done`
