# POL-L2-PC1-CLEAN-FDE-PY-L01 · 602 清洗 · Python 只读候选与五条判定收口

ponytail: full

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 已代认领。本会话未再调用 task-claim |
| 说明 | 开工时状态已是 `in_progress`，未改认领字段 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 沿用工作区已有两条只读路由收口，未推倒重写。未用 YAGNI 跳过调用链与可观测：路由挂在既有 FastAPI，trace 沿 `TraceHeaderMiddleware`。ARCH 写明本叶不新设计观测点。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POL-L2-PC1-CLEAN-ARCH-SEQ` |
| 图 diff | 未改图。代码按文末时序：候选与五条只 SELECT 演示贴源；准确性不在这次点击里现算 |
| 会签态 | 源文件状态行：「已按当日裁定重写。本稿不写会签结论，不把本单标 done」。不是 approved |
| 说明 | 对照 `POL-L2-PC1-CLEAN-ARCH.md` 文末时序，以及同目录 API 稿、DATA 稿。Java / 前端未改 |

## 修改内容

- `GET /internal/policy/clean-candidates`：国内、海外分源只读 `{ods}.dwd_policy_base`、`{ods}.dwd_global_policy_base` 当前行。国内搜索 `title`、`publish_code`、`ministry`；海外搜索 SQL 只有 `title`。表不存在或查询失败为 `read_failed` / 「读取失败」，`rows` 为 null，不返回 0。当前行为 0 才是「这一源还没有贴源数据」。
- `POST /internal/policy/clean-judge`：只 SELECT 勾选 id。去重合并、格式标准化、完整性校验在已有列上判定；噪声过滤、一致性校验无列，命中 null，走无加工事实。准确性校验被丢掉，不在本路由现算，也不读 `policy_accuracy_demo`。
- `scripts/mysql/policy_accuracy_demo.sql`：只含 `CREATE TABLE`，无 `INSERT`。应用启动不执行该文件，本单不灌数。
- 两条路由的 SQL 均为 SELECT。未对 ODS / DWD / ADS / 供应方库 / `script_state` 写入。

## 测试结果

- 命令（仓库根 `lumen-algo-py`）：`python -m pytest tests/test_policy_clean_routes.py -q`
- 结果：`2 passed, 1 warning in 1.11s`（Starlette 对 httpx 的弃用警告，与本单无关）
- 覆盖：海外搜索 SQL 不含 `publish_code`、`ministry`；读取失败不是 0、文案不是空源；准确性不在 judge 结果里；表不存在是读取失败；SQL 文件无 INSERT，且 `policy_routes.py` / `main.py` / `polan/common/db.py` 不引用 `policy_accuracy_demo`

## 遗留风险

- 准确性演示行留在点击之外，本单未写入，DDL 未在任何库执行。
- 公开执行响应上的「成功 / 部分 / 失败」由 element / display 汇总。本路由只回五条判定，不代算这三句，也不读准确性演示表。
- 测试使用假连接，未打真实演示贴源。
- 去重只比对本批勾选行。时序里写了对照贴源全表可能超时；本实现只 SELECT 勾选 id。
- 编排仓本 handoff 只落盘，未随 lumen-algo-py 提交。编排仓其他未提交文件未动。

## CI/CD（必填）

- 分支：`dev`
- commit：`3de0ab72a65e9fd29177e66ee5d7d68ac2862546`
- push：`origin/dev` 已成功（`0e7d125..3de0ab7`）
- pipeline URL / ID：本会话未查
- 部署 namespace / 镜像 tag：未查
- K8s rollout：未查
- dev 测试 URL / 命令与结果：本地 pytest 见上，未打线上

## 可观测性（建议）

- 路由挂在 `vendor/entan-py/api/main.py` 已有应用上，`TraceHeaderMiddleware` 回写 `traceparent` 与 `X-Trace-Id`
- 本叶按 ARCH 不新设计观测点
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `lumen-algo-py` `vendor/entan-py/api/policy_routes.py`
- `lumen-algo-py` `tests/test_policy_clean_routes.py`
- `lumen-algo-py` `scripts/mysql/policy_accuracy_demo.sql`
