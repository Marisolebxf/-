# POLICY-MOCK-INCR-L01 · 政策 Mock 增量入仓

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户授权建单+认领+执行、过程不打断 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 indana GLM C→B→A 与现有 ODS/DWD 映射，不新增依赖；未跳过 demo 只写 / 正式面闸门 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未把 Headroom 当本任务检索依赖 |

## 问题清单

- 政策 Mock 保存是否重算 ADS？否，只写 ODS。
- 【追加】是否继续内存造 600 条？否，改为 ODS−DWD 差集。
- 空库自举？startup 改为 `replace` 造 600 底数，避免 append 差集为 0 时跳过算法。

## 修改内容

- `polan/mockgen/incr.py`：ODS CRUD、LLM 填 1 条、差集入 DWD、`self_check`
- `polan/mockgen/generate.py`：`append` 转 `ingest_pending()`；`replace` 仍内存造 600
- `api/policy_routes.py`：`/v1/policy/mock/*`；status 增加 `pending_count` / `last_ingested`
- `api/main.py`：空 ADS 自举走重建底数
- `demo-ui-system-test`：侧栏「政策 Mock」页；基础指标【追加】徽章与条数 toast

## 测试结果

- `python -m polan.mockgen.incr` → `policy incr self_check OK`（SQLite：保存 1 条 pending → ingest 1 → pending 0；已入库只读）
- `py_compile` 通过：incr / generate / policy_routes / main / run_all_policy
- 热修：trace `bd82096aeb3cc29cf86da31651b0510c` → MySQL 1292 `expire_date=''`；`_ods_date` 空串改 NULL。self_check 断言 `expire_date is None`

## 遗留风险

- 联调台需 Python 服务与前端部署后才能点验 GLM 填表；无 Key 时回退离线模板 A
- 【重建】会清空未入仓 Mock 增量（确认框已写明）
- ADS 仍全量重算，不是指标增量计算

## CI/CD（必填）

- 分支：两业务仓与编排仓均为 `origin/dev`（本环境实际分支；非 constitution 表里的 demo main）
- commit：
  - `demo-algo-ent-analysis` `bf50d74` feat(policy): Mock 增量入 ODS，追加改读差集
  - `demo-ui-system-test` `b6cfcf9` feat(policy): 政策 Mock 页与追加可追加条数
  - `gkx-orchestration` `1e078df` docs(policy): POLICY-MOCK-INCR-L01 handoff
- pipeline URL / ID：push 后 GitLab CI（dev）
- 部署 namespace / 镜像 tag：demo 仓惯例
- K8s rollout：待 CI
- 本地：`python -m polan.mockgen.incr` → `policy incr self_check OK`
- 联调台：保存失败已按 trace 定位；热修 push 后待 CI 再点验（不写联调通过）
- 热修 commit：`demo-algo-ent-analysis` `d1d5a4e`（rebase 后以 origin/dev 为准）

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用现有 Python / 前端 request 拦截
- traceId（dev 抽样）：未在本任务新加
- Tempo / Loki：有 / 无 — 沿用联调台既有

## 涉及文件

- `demo-algo-ent-analysis/polan/mockgen/incr.py`（新增）
- `demo-algo-ent-analysis/polan/mockgen/generate.py`
- `demo-algo-ent-analysis/api/policy_routes.py`
- `demo-algo-ent-analysis/api/main.py`
- `demo-algo-ent-analysis/scripts/run_all_policy.py`
- `demo-ui-system-test/src/views/policy/pages/PolicyMockPage.vue`（新增）
- `demo-ui-system-test/src/views/policy/pages/BasicPage.vue`
- `demo-ui-system-test/src/views/policy/policyMenuConfig.ts`
- `demo-ui-system-test/src/router/index.ts`
- `demo-ui-system-test/src/api/policy/index.ts`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ LLM 填表与差集映射在 polan |
| 调用链 前端→（本 demo 直调 Python /policy） | ✅ 联调台既有范式，未越层改 lumen |
| 图谱 Nebula | ✅ 追加后仍走原 graph 步骤；未引入 Neo4j |
| 可观测 | ✅ 沿用 request 拦截 |
| demo 只写 demo_* | ✅ `assert_demo_mysql_targets` + `is_live("policy")` |
| D12 lumen 不调 demo | ✅ 未改 lumen |
| D9 指标 8 件套 | N/A 本页是 Mock 维护，不新增统计口径 |

## 验收对照 DoD

- [x] Mock 页在政策侧栏底部；保存只写 ODS
- [x] 追加不再内存造 600；读差集入 DWD 后重算 ADS
- [x] 追加旁可追加 N；完成后 toast 已追加 N
- [x] 重建仍内存造 600；确认框说明清增量
- [x] 正式面禁止写；self_check；本 handoff

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 90000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.54 |
| cost_warn | green |
| 口径 | algorithm 75/25 × $3/$15 /$M；source: session_estimate |
