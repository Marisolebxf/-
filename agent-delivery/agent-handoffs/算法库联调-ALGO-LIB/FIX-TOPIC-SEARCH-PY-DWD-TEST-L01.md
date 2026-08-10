# FIX-TOPIC-SEARCH-PY-DWD-TEST-L01 Handoff

> 状态：DWD 兼容测试已对齐 RiskRepository，待 QA / coordinator 验收  
> 执行：agent:data-agent  
> 监管：human:徐滕强  
> 仓：`demo-svc-topic-py`  
> 日期：2026-08-06

## 1. 范围与实现

修复 `tests/test_dwd_v3_compatibility.py` 全部失败用例（原 28 失败），继续断言 DWD MySQL v3 → 稳定 API 契约。

根因：

1. helper `_capture_risk_sql` 仍 `monkeypatch.setattr(enterprise_risk, "query", ...)`，但 `enterprise_risk.py` 已不再暴露模块级 `query`。
2. 测试调用已删除的 `enterprise_risk._query_risk_type_pg(...)`；实现已改为 `_query_risk_type` → `RiskRepository(session).list_by_type(...)`。
3. SQL/字段映射真源在 `gkx_common/repositories/risk.py` 的 `RISK_TYPE_CONFIG` / `RiskRepository`。

实现（仅改测试，未改 repository / 算法适配）：

1. `_capture_risk_sql` 改为对 `RiskRepository.list_by_type` 注入 `_CaptureSession`，在 `scalar`/`execute` 处用 MySQL dialect 编译语句并捕获 SQL。
2. 列别名断言去掉硬编码表别名 `t.`，改为语义片段（如 `case_id AS xhfgk_id`），兼容 ORM 表名限定列。
3. party join 断言改为：`ON <table>.case_id = <table>.case_id` + `is_history AS is_history` + `_party` 表参与。
4. `equity_freeze` 排序断言对齐当前实现：`date_field=None` → `ORDER BY risk_equity_freeze.id DESC`（Repository 注释：无事件日期时按主键 id 倒序，保持确定性排序）。

## 2. 偏离说明

| 项 | 原断言 | As-built | 理由 |
|---|---|---|---|
| SQL 捕获点 | `enterprise_risk.query` / `_query_risk_type_pg` | `RiskRepository.list_by_type` + 编译 SQL | view 已去模块级 query；契约真源在 Repository |
| 表别名 | `t.` / `p.` | ORM 表名（如 `risk_lawsuit` / `risk_lawsuit_party`） | SQLAlchemy 默认不用 `t`/`p`；语义等价 |
| equity_freeze 排序 | `ORDER BY t.case_id DESC` | `ORDER BY risk_equity_freeze.id DESC` | Repository 已定义无日期字段按主键 id；属确定性排序契约，非业务口径漂移 |

**未修改** `gkx_common/repositories/risk.py`：编译 SQL 核对后，列别名 / `NULL AS` / party join / 排序语义均与稳定 API 契约一致，无真实契约破坏。

**未碰** `gkx_ai_service` 算法适配改动（工作区另有未提交变更，与本任务无关）。

## 3. 产物清单

| 路径 | 说明 |
|---|---|
| `repos/demo-svc-topic-py/tests/test_dwd_v3_compatibility.py` | 唯一代码改动 |
| `agent-delivery/agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-TEST-L01.md` | 本 handoff |

## 4. 验收证据

```text
.venv/bin/pytest tests/test_dwd_v3_compatibility.py -v
============================== 31 passed in 1.07s ==============================
```

覆盖：

- 列别名映射 14 例
- 已删除字段 `NULL AS` 7 例
- party join 6 例
- equity_freeze 确定性排序 1 例
- mock 分支清除 / type_scale / distribution 源码契约 3 例

## 5. 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 未改算法 |
| 2 | 前端 → Java → Python `/internal/*` | ✅ 未改调用链 |
| 3 | NebulaGraph | ✅ N/A |
| 4 | 可观测性 | ✅ N/A |
| 5 | CI/CD | ✅ 测试对齐，待 push/CI（本任务未 commit/push） |
| 6 | demo2 只读 merge | ✅ N/A |
| 7 | 共享聚合核心 | ✅ N/A |
| 8 | 数据策略 ADS/DWD | ✅ 测试继续守护 DWD→稳定 API 映射 |
| 9 | 前端规范 | ✅ N/A |
| 10 | 数据血缘 | ✅ N/A |

## 6. Cost 回填

| 字段 | 值 |
|---|---|
| `actual_tokens` | ~45000 |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~$0.40 |
| `cost_warn` | false |

## 7. 开放项

1. 工作区另有 `gkx_ai_service/*` 等未提交变更，与本任务无关；提交本修复时请只 stage `tests/test_dwd_v3_compatibility.py`。
2. 本任务按指示**未 commit / 未 push**；监管人确认后由人提交，message 建议含 `[agent:data-agent]`。
3. task-registry MCP 在 Cursor 子 agent 会话中未挂载；已通过 `scripts/task-mcp-server.mjs` JSON-RPC 核验任务为 `in_progress` / `claimed_by=agent:data-agent` / `supervised_by=human:徐滕强`。handoff 后请 coordinator 推进 `pending_test`（bugfix AV-0）。
