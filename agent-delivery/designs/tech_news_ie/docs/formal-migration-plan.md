# 正式仓迁移方案（Sandbox → Demo/Lumen）

> 前置：本地沙箱 Phase 0–4 已完成（见 `HANDOFF-sandbox.md`）。  
> 本文件是**迁移施工说明**，不是已执行记录。改正式仓前必须走 registry 认领。

---

## 0. 认领门禁（必做）

启动前向 coordinator/监管人确认：

| 项 | 示例 |
|----|------|
| task-id | 新建如 `E-TECH-NEWS-IE-M1-L01` |
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:{花名册真名}` |
| claim_type | `pull` |
| 目标仓 | `demo-algo-science`（先）→ `lumen-svc-platform` / 前端仓（后） |
| 分支 | worktree / feature，禁止直接推正式 `main`；demo-algo 与其它业务仓一律 `origin/dev` 直推 |

---

## Phase A — 迁入 `demo-algo-science`（建议先做）

### A1. 代码落位

```text
repos/demo-algo-science/
  innov/tech_news_ie/          # 从 sandbox src/tech_news_ie 拷贝/迁入
    ...
  api/main.py                  # 挂载路由或 include_router
```

建议：

1. 将沙箱包改名为 `innov.tech_news_ie` 或保持独立顶层包并加入 `PYTHONPATH`  
2. 在 `api/main.py` 增加：

```python
from innov.tech_news_ie.api import app as tech_news_app
# 或
app.mount("/tech-news", tech_news_app)
# 更好：把路由函数抽成 APIRouter，include_router(prefix="")
```

3. 复用仓内 `logging_config` / `otel_middleware`  
4. 依赖并入 `requirements.txt`（fastapi/pydantic/httpx/httpx2 已有可复用）

### A2. 配置

| 环境变量 | 含义 |
|----------|------|
| `TECH_NEWS_IE_MODE` | `mock` / `llm` |
| `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL` | LLM 模式 |
| `TECH_NEWS_IE_DB_PATH` | 临时 SQLite；正式改为 PG |

### A3. 验收

- 原 28 测例迁入 CI  
- `POST /internal/tech-news/extract` 在 innov-py 服务端口可用  
- 健康检查纳入现有 `/healthz` 或子路径

---

## Phase B — Java 转发 + ADS

### B1. Java（`lumen-svc-platform` 或 `demo-svc-platform`）

1. 新增 Client：调用 Python `POST /internal/tech-news/extract`  
2. 新增 Controller：对外 REST（鉴权后转发）  
3. 超时 ≥ 30s；透传 `X-Request-Id`  
4. **Java 不写抽取逻辑**

契约细节见 `java-integration.md`。

### B2. ADS DDL（建议）

以沙箱表为草案，迁到 PostgreSQL：

- `ads_tech_news_extraction`
- `ads_tech_news_event`

字段对齐沙箱 `persist.py`；正式由 Java 或 Python 二选一落库（推荐 Java 管业务落库、Python 只返回 JSON）。

### B3. 验收

- 经 Java 调用 Python 返回四字段  
- ADS 可查  
- 错误码 422/500 行为与契约一致

---

## Phase C — 正式前端复核页

1. 按 `Design.md` + Arco 重做复核页（替换沙箱 HTML）  
2. 仅调 Java API  
3. 展示：公司名称 / 完成时间 / 完成事项 / 作用与影响 + 证据展开 + flags  
4. Wave0 若用 Mock 数据，加 🧪 MockBadge；指标旁 ⓘ（若有 metric_id）

目标仓：`demo-ui-science`（原型）或 `lumen-ui-science-pc`（正式）——由 PM 指定。

---

## 风险

| 风险 | 缓解 |
|------|------|
| 沙箱复核页直连 Python | 正式禁止；只保留本地调试 |
| mock 启发式不可上生产 | 生产必须 `MODE=llm` + 抽检集 |
| 别名表不全 | 运营可维护 JSON/DB 别名 |
| 无 task 强行改正式仓 | 违反认领门禁，禁止 |

---

## 推荐执行顺序

```text
认领 task
  → A（algo 仓挂载）
  → B（Java + ADS）
  → C（正式 UI）
  → handoff + coordinator 验收
```
