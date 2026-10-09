# CROSS-VEC-JOB-A-L01 · ETL Job A 政策产业槽向量补码跑批

> 总控 [`CROSS-VEC-长任务总控.md`](./CROSS-VEC-长任务总控.md) §0 #3 #6 #16 #17 #18 #19、§6.5；派单 [`派单/CROSS-VEC-JOB-A-L01-派单包.md`](./派单/CROSS-VEC-JOB-A-L01-派单包.md)；前序 [`CROSS-VEC-POLICY-SEARCH-L01.md`](./CROSS-VEC-POLICY-SEARCH-L01.md)（`7ca4bf6`）。02 §3.1 三种入口 / §3.2 Job A。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控 D 段；lock 24h；接单时已 claimed + in_progress |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 循环前序 `enrich_one`，未另写 VID / `match_industry_anchors` / search；未新 pip；未用 YAGNI 跳过 honesty / 单飞 / 重灌零 enrich / handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓单叶，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` §3.2 |
| 图 diff | 加 ETL 边：`POST /internal/industry/jobs/enrich` → 循环 `embed/search` → `enrich_one`/`match_industry_anchors` → DWD 槽。重灌同步边仍停在 L0+L1，**不加** search / 建库 / LLM。按钮边仍走 SEARCH。本叶不画灌链 rebuild。 |
| 会签态 | `v0.3-draft`（抄源文件 frontmatter，未自填绿） |

## 范围与实现

**做**：万级政策产业槽 **Job A 跑批**（增量默认、全量可开）。复用 SEARCH 抽出的共享模块，不重写定码。

> **验证闸（2026-09-11 `human:淮政玮`）**：本波只做可行性/跑通，**硬顶 100 条**。`limit` 缺省 **100**、封顶 **100**（超过 → HTTP 400）。`mode=full` 同样不得超过 100（单 job 累计 `processed` 到 100 即 `done`，不顺着 cursor 灌完库）。**这不是产线性能口径**；放开万级另叶。

1. **跑批 API** `POST /internal/industry/jobs/enrich`
   - 入参：`mode=incremental|full`（默认 incremental）、`force`、`cursor`、`limit`（默认 100、封顶 100）、可选 `job_id` 续跑
   - 出参：`job_id` + `job_kind=industry_embed_enrich` + `index_version` + 进度 `processed/skipped/coded/failed` + `status` + `next_cursor` + `degraded` + `limit_cap=100`
   - 增量：扫描无 `industry_link_code` 的行；全量：扫表，`force=false` 已有码走 `enrich_one` skip；本波两者都硬顶 100
   - 每请求最多 `limit` 条；同 job 累计亦 ≤100。不在一发 HTTP 里灌 4.7 万
2. **循环共享模块** `industry_enrich.py`：`enrich_one` · `apply_search_hits` · `query_text` · `name_only_slot` · `merge_industry` · `write_related`
3. **单飞**：键 = `job_kind + index_version`（`industry_embed_enrich:{index_version}`）。同键已有 `status=running` 的 **full** → 409 拒第二份；同 `job_id` 续跑放行
4. **`index_version` 只从 search 探测响应读**。探测或中途 `degraded` / `code≠0` → 停、不写假码（503）
5. **重灌同步继续零本入口**：`incr` / `generate` / `run_all_policy` grep 无 `jobs/enrich`

**不做**：建库；Job B LLM；Hang 写图；改 Java / 前端；进重灌同步 HTTP；采 top1 定码；与灌链并排的调度器（`CHAIN-CRON`）。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 本叶**未**对现网 DWD 实跑补码 | 本机无 `.env` 连 19530 / TEI（ClusterIP）。单测注入 `search_fn`。现网 collection 仍是 SWITCH `gkxlumen_industry_anchor` / `20260911113702` |
| 2 | 每请求只跑 `limit` 条，不在本进程起后台线程扫全表 | 可恢复靠 `job_id`+`cursor`；本波累计仍 ≤100。Java `API-JOB` 勿按万级估时 |
| 3 | 进程内 job 表（单副本） | ponytail：与 chain `acquire_worker` 同级天花板。多副本单飞要等 Java 侧 job 表 |
| 4 | 本波 `limit`/`full` 硬顶 100 | 监管人 2026-09-11 12:16 验证闸，**不是产线性能口径**；放开另叶 |

未违反硬闸：#17 不采 top1；#3 重灌不同步 search/enrich；#16 不 create/drop collection；#19 只 search、degraded 诚实停。

## 产物清单

- `lumen-algo-py/lumen_common/algorithms/policy/industry_job.py`
- `lumen-algo-py/lumen_algo_service/views/industry_jobs.py`
- `lumen-algo-py/lumen_algo_service/main.py`（挂路由）
- `lumen-algo-py/lumen_common/algorithms/policy/industry_enrich.py`（导出 `write_related`）
- `lumen-algo-py/tests/test_industry_job_enrich.py`
- 本 handoff

## 验收证据

### 1. API

`POST /internal/industry/jobs/enrich`

请求：

```json
{"mode":"incremental","force":false,"cursor":"","limit":100}
```

成功 200：

```json
{
  "code": 0,
  "data": {
    "job_id": "…",
    "job_kind": "industry_embed_enrich",
    "mode": "incremental",
    "status": "running|done",
    "index_version": "20260911113702",
    "processed": 0, "skipped": 0, "coded": 0, "failed": 0,
    "cursor": "", "next_cursor": "",
    "degraded": false
  }
}
```

- 探测/中途 degraded → **503** + `status=failed`，不写
- 第二份 full 单飞 → **409** + `status=rejected`
- 坏 `mode` / `limit>100` → **400**
- `limit` 缺省 100；`full` 本波也在 100 条处 `done`

### 2. pytest

```text
cd ${GKX_ROOT}/repos/lumen-algo-py
python -m pytest tests/test_industry_job_enrich.py tests/test_policy_industry_enrich.py tests/test_industry_vid_enrich.py -q
  → 33 passed

python -m pytest tests/test_industry_embed.py tests/test_chain_graph.py -k "rebuild or routes or guard or only_one" -q
  → 15 passed（灌链 rebuild 调用点仍只有 industry.py + graph_project.py）
```

| 用例 | 断言 |
|------|------|
| `test_incremental_skips_already_coded` | 增量不扫已有码；只对无码行 search/写 |
| `test_full_force_false_counts_coded_as_skipped` | 全量 `force=false` 已有码 skip，不调 search |
| `test_degraded_probe_does_not_write` | 探测 degraded 不写、processed=0 |
| `test_mid_batch_degraded_stops_and_does_not_write` | 中途 degraded 停、failed=1、不写 |
| `test_single_flight_rejects_second_full` | 同键 running 拒第二份 full；同 job_id 续跑 |
| `test_job_does_not_take_top1_score` | top1 矿产勘探不写码，写集成电路 `chain:INB1303` |
| `test_reload_files_have_no_jobs_enrich` | 重灌三文件零 `jobs/enrich` |
| `test_http_route_and_statuses` | 200 / 409 / 503 |
| `test_limit_over_cap_is_400` | `limit>100` → 400 |
| `test_wave_cap_full_and_default_stop_at_100` | 缺省/`full` 150 行只处理 100，续跑不加 |

样例 job 日志：无现网跑批。上表单测即进度字段的诚实替代（`processed/skipped/coded/failed` + `status`）。

### 3. 重灌 grep（exit 1 = 零命中）

```text
rg -n "jobs/enrich|/internal/industry/jobs|industry_job|run_enrich_job" \
  vendor/entan-py/polan/mockgen/incr.py \
  vendor/entan-py/polan/mockgen/generate.py \
  vendor/entan-py/scripts/run_all_policy.py
# 无输出，exit 1
```

### 4. 是否实跑现网

**没有。** 未连 19530 / TEI，未 UPDATE 现网 `demo_gkxlumenx_dwd.policy_base_info`。

## 对 CROSS-VEC-API-JOB-L01 的 Java 门面契约

| 项 | as-built |
|---|---|
| Python 路径 | `POST /internal/industry/jobs/enrich` |
| 建议 Java | `/topic/v1/industry/jobs/enrich`（与 FEIGN 同 `RemoteChainPythonClient` / `/chain/**`） |
| 请求 | `mode` `force` `cursor` `limit` `job_id?`（snake_case；Java 驼峰自行映射） |
| 进度字段 | `processed` / `skipped` / `coded` / `failed`（禁止假百分比） |
| 另回 | `job_id` `job_kind=industry_embed_enrich` `status` `index_version` `next_cursor` `degraded` `limit_cap=100` |
| **501** | Python **503** / `degraded=true` / `code≠0`（探测失败、重建窗口）→ 与 FEIGN 同一套 honesty，**禁止 200 假码** |
| **不要 501** | Python **409** = 第二份全量单飞（冲突，不是未就绪）；**400** = 坏 mode 或 `limit>100` |
| 续跑 | `status=running` 时带 `job_id` + `next_cursor` 再 POST；`processed` 到 100 即 `done`（本波验证闸） |
| 本波闸 | Java 默认 `limit=100`；勿按 4.7 万估时。放开万级另叶 |
| 分 job_kind | ETL 补槽 ≠ I2-12「开始分析」 |
| 本叶不实现 | Job B `extract-llm`；Java 不 embed、不直连 Milvus |

## 问题清单 / 开放项

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | Java Feign 跑批门面 | `CROSS-VEC-API-JOB-L01` | 契约见上 |
| B | 现网万级实跑 / 放开 100 封顶 | 另叶（验证闸之后） | 本波硬顶 100，不是产线口径 |
| C | 多副本单飞 | API-JOB Java job 表 | 本叶进程内 |
| D | §0 #17 / #19 仍有效 | 后续叶 | 禁止采 top1；不得与灌链并排 |

## 修改内容

| 文件 | 行为 |
|------|------|
| `policy/industry_job.py` | Job A：探测 search → 扫描 → 循环 `enrich_one` → 进度 / 单飞 |
| `views/industry_jobs.py` | `POST /internal/industry/jobs/enrich` |
| `main.py` | include 路由 |
| `industry_enrich.py` | 导出 `write_related`（与按钮同一 UPDATE） |
| `test_industry_job_enrich.py` | 增量 skip / degraded / 单飞 / 重灌 grep |

## 测试结果

- Job A 11 例 + SEARCH 12 例 + L0 9 例 = **33 passed**
- embed/灌链 rebuild 守卫回归绿
- 未调 LLM、未建库、未碰 `aip_kb_*`

## 遗留风险

- 进程内 job 表，多副本各记各的；全量单飞以单副本为天花板
- 存量无码行要等 Java 续跑或夜班
- MemoryStore / TEI 不可用时 HTTP 503，不会用 hashgram 假码落库

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`（先 `git pull --ff-only`，前序 SEARCH `7ca4bf6`）
- commit：**`f07f87546e04c8807032331da7130cd48826fc33`** `fix(policy): cap industry enrich job at 100`（其上 `e5b0652` 首交）`[agent:algorithm-agent]`
- pipeline：push 触发 GitLab CI
- K8s rollout：本轮总控段 E 不派专题金路径；连通性 + pytest 闭环
- dev 测试：见上 pytest（未实打 19530）

## 可观测性（建议）

- 沿用 `current_trace_id()` 写入 job 包络
- 不写查询全文到日志

## 涉及文件

- `lumen-algo-py/lumen_common/algorithms/policy/industry_job.py`
- `lumen-algo-py/lumen_common/algorithms/policy/industry_enrich.py`
- `lumen-algo-py/lumen_algo_service/views/industry_jobs.py`
- `lumen-algo-py/lumen_algo_service/main.py`
- `lumen-algo-py/tests/test_industry_job_enrich.py`
- `lumen-algo-py/tests/test_policy_industry_enrich.py`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python `/internal/*` | ✅ 新口 `/internal/industry/jobs/enrich` |
| 调用链不可越层 | ✅ 未改 Java / 前端；只调已有 `embed/search` |
| 图谱仅 Nebula | ✅ 定码仍 `match_industry_anchors` |
| 可观测 | ✅ `current_trace_id` |
| CI/CD | ✅ push `origin/dev`，未 force；`[agent:algorithm-agent]` |
| D12 | ✅ 未调 `demo-*`；未碰 `amcpdp-*` / `aip_kb_*` |
| 数据策略 | ✅ 写槽走 polan demo 闸门 |
| Java 不写算法 | ✅ 本叶零 Java |
| D8 / D9 / D10 | N/A |
| §0 #3 重灌不同步 search | ✅ grep 零 `jobs/enrich` |
| §0 #16 不自建 collection | ✅ 只 search |
| §0 #17 禁止采 top1 | ✅ 单测锁死 |
| §0 #19 不建库；degraded 诚实 | ✅ 503 + 不写 |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 165000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.99 |
| cost_warn | green |

口径：algorithm 默认 75/25；B 档 `$3/$15` per 1M；`165000×0.75×3/1e6 + 165000×0.25×15/1e6 = 0.99`。含监管人 100 条验证闸增量。
