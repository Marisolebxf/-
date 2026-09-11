# CROSS-VEC-POLICY-SEARCH-L01 · 政策语义抽槽按钮（search top-k → 对码）

> 总控 [`CROSS-VEC-长任务总控.md`](./CROSS-VEC-长任务总控.md) §0 #3 #6 #7 #16 #17 #18 #19、§6.5；派单 [`派单/CROSS-VEC-POLICY-SEARCH-L01-派单包.md`](./派单/CROSS-VEC-POLICY-SEARCH-L01-派单包.md)；流图 POLICY [`01-data-flow.md`](../../../data/data-design/storage/POLICY/01-data-flow.md) §2.4。前序 SWITCH `c41233e`（`index_version=20260911113702`，dim 768）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控 C 段；lock 24h；接单时已 claimed + in_progress |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 抽共享 `industry_enrich` + 按钮 HTTP；未做 JOB-A cursor/全量；未新 pip；定码复用仓内 `match_industry_anchors`。未用 YAGNI 跳过 honesty / 假 `chain:` 守卫 / handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓单叶，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` §3.1（按钮入口） |
| 图 diff | 加按钮边：`POST /internal/policy/industry/enrich` → `embed/search` top-k → `match_industry_anchors` → DWD `related_entities.industry`。重灌同步边仍停在 L0+L1，**不加** search / rebuild / LLM。跑批框仍指向 JOB-A |
| 会签态 | `v0.3-draft`（抄源文件 frontmatter，未自填绿） |

## 范围与实现

**做**：政策语义抽槽**按钮**（小 limit）。共享 enrich 模块给 JOB-A 复用。

1. **共享模块** `lumen-algo-py/lumen_common/algorithms/policy/industry_enrich.py`
   - `query_text`：与 L1 同字段（标题/摘要/关键词/要点 + policy_support 要素），禁止拼 theme/ext5
   - `apply_search_hits`：search 候选只用 `name`+`vid` → `match_industry_anchors`；**不**把 hit 名拼进 query（否则等于采 top-k）
   - `enrich_one`：已有码且 `force=false` 则 skip（不调 search）；`code≠0` / `degraded=true` **不写**；无码 `name_only_slot` 只留 `{name}`
   - 写槽守卫：丢掉 LLM 假 `chain:`、`score`、ODS `industry_code`；分数不是码
   - `enrich_policies`：按钮封装，`limit` 封顶 **20**；`cursor` / `mode=incremental|full` **拒绝**（JOB-A）
2. **按钮 API** `POST /internal/policy/industry/enrich`（`lumen_algo_service/views/policy_industry.py`）
   - 入参：`policy_id` / `policy_ids` 或当前筛选 + 小 `limit`
   - 成功 200；索引重建/degraded **503** 且不写假码；跑批字段 **400**
3. **重灌默认同步关**：`ods_to_dwd` / `ingest_pending` / `reload_from_ods` 仍只 L0+L1，零 search / 零 rebuild / 零本模块

**不做**：JOB-A 万级 cursor / incremental / full / 单飞；rebuild；改 Java / 前端；装模型；碰 `aip_kb_*`；把 score 写成 `industry_link_code`。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 本叶**未**对现网 DWD 实打 search 写槽 | 本机无 `.env`、无 `MILVUS_URI` / `EMBED_BASE_URL`；TEI 为 ClusterIP。单测用注入 `search_fn` 走同一套定码。现网 collection 仍是 SWITCH 的 `gkxlumen_industry_anchor` / `20260911113702` |
| 2 | HTTP 挂在 `lumen-platform-algo-py` 而非 entan-py | 与 `/internal/industry/embed/search` 同进程；本叶不改 Java Feign。政策重灌仍在 entan-py，**不**调用本接口 |

未违反硬闸：#17 不采 top1；#3 重灌不同步 search；#16 不 create/drop collection；#19 只 search、degraded 诚实失败。

## 产物清单

- `lumen-algo-py/lumen_common/algorithms/policy/industry_enrich.py`（JOB-A 复用真源）
- `lumen-algo-py/lumen_algo_service/views/policy_industry.py`
- `lumen-algo-py/lumen_algo_service/main.py`（挂路由）
- `lumen-algo-py/tests/test_policy_industry_enrich.py`
- 本 handoff

## 验收证据

### 1. API 路径

`POST /internal/policy/industry/enrich`

### 2. pytest

```text
cd ${GKX_ROOT}/repos/lumen-algo-py
python -m pytest tests/test_policy_industry_enrich.py tests/test_industry_vid_enrich.py -q
  → 21 passed

python -m pytest tests/test_industry_embed.py tests/test_chain_graph.py -k "rebuild or routes or guard" -q
  → 15 passed, 26 deselected
```

| 用例 | 断言 |
|------|------|
| `test_reload_ingest_files_do_not_call_search_or_rebuild` | incr/generate/run_all_policy **零** `industry_embed` / `embed/search` / `embed/rebuild` / 本模块 |
| `test_ods_to_dwd_does_not_invoke_embed_search` | 映射后 search 计数器仍 0 |
| `test_default_off_skips_search_when_already_coded` | 已有码默认不调 search |
| `test_apply_hits_does_not_take_top1_score_or_code` | top1 矿产勘探 0.99 **不**写码；命中文本中的集成电路 `chain:INB1303` |
| `test_no_match_keeps_name_only_drops_forged_chain` | 无码只留 `{name}`；假 `chain:FAKE` 丢 |
| `test_degraded_search_does_not_write` | `degraded` 不写库 |
| `test_http_enrich_route_and_small_limit` | 路由存在；按钮写对码 |
| `test_http_degraded_is_503_and_job_a_is_400` | degraded 503；cursor/full 400 |
| `test_button_limit_cap_is_small` | 50 条输入只处理 20 |

### 3. 重灌 grep（exit 1 = 零命中）

```text
rg -n "industry_embed|embed/search|embed/rebuild|/internal/industry/embed|industry_enrich" \
  vendor/entan-py/polan/mockgen/incr.py \
  vendor/entan-py/polan/mockgen/generate.py \
  vendor/entan-py/scripts/run_all_policy.py
# 无输出，exit 1
```

### 4. 是否实打 search 写槽

**没有。** 未连 19530 / TEI，未 UPDATE 现网 `demo_gkxlumenx_dwd.policy_base_info`。前后槽只在单测注入路径验证（见上：无码 `{name:生物医药}`；有码 `集成电路/chain:INB1303`，非 top1 矿产勘探）。

## 问题清单 / 开放项

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | JOB-A 万级 cursor / incremental / full / 单飞 | `CROSS-VEC-JOB-A-L01` | ready 未派；复用本模块，勿重写定码 |
| B | Java Feign 按钮门面 | api-agent（未派） | 本叶不改 Java |
| C | 现网抽样实打 search 写槽 | 联调 / JOB-A | 本叶诚实未做 |
| D | §0 #17 / #19 仍有效 | JOB-A | 禁止采 top1；不得与灌链并排 |

## 对 JOB-A 的交接

**复用（不要重写）**：

- `lumen_common/algorithms/policy/industry_enrich.py`：`enrich_one` / `apply_search_hits` / `query_text` / `name_only_slot` / `merge_industry`
- 定码：`polan.graph.entity.match_industry_anchors`（已在仓内）
- search：`industry_embed.search`（只消费，**禁止** `rebuild` / 自建 collection）
- `index_version` 从 search 响应读

**不要做**：另写一套 VID 规则；采 `hits[0].vid` / `score`；把 `industry_code` 当链码；重灌里挂钩；与灌链并排跑。

**本叶留给你的**：cursor、incremental/full、未对码扫描、单飞键、夜班进度。按钮入口已拒这些字段。

## 修改内容

| 文件 | 行为 |
|------|------|
| `policy/industry_enrich.py` | 共享 worker：search → 对码 → 写槽 |
| `views/policy_industry.py` | `POST /internal/policy/industry/enrich` |
| `main.py` | include 路由 |
| `test_policy_industry_enrich.py` | 默认关 / 无码 `{name}` / 不采 top1 / degraded / 小 limit |

## 测试结果

- 本叶 12 例 + L0 9 例 = **21 passed**
- embed/rebuild 回归 **15 passed**
- 未调 LLM、未 rebuild、未碰 `aip_kb_*`

## 遗留风险

- 按钮 HTTP 尚未经 Java Feign；前端点不到属后叶
- 本机未实灌，存量无码行要等按钮或 JOB-A
- MemoryStore / TEI 不可用时 HTTP 503，不会用 hashgram 假码落库

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`（先 `git pull --ff-only`，前序 SWITCH `c41233e`）
- commit：**`7ca4bf6bef038a709e82a3c383d633895db695ed`** `feat(policy): add industry semantic enrich button API` `[agent:algorithm-agent]`
- pipeline：push 触发 GitLab CI
- K8s rollout：本轮总控段 E 不派专题金路径；连通性 + pytest 闭环
- dev 测试：见上 pytest（未实打 19530）

## 可观测性（建议）

- 沿用 `current_trace_id()` 写入 enrich 包络
- 不写查询全文到日志

## 涉及文件

- `lumen-algo-py/lumen_common/algorithms/policy/industry_enrich.py`
- `lumen-algo-py/lumen_algo_service/views/policy_industry.py`
- `lumen-algo-py/lumen_algo_service/main.py`
- `lumen-algo-py/tests/test_policy_industry_enrich.py`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python `/internal/*` | ✅ 新口 `/internal/policy/industry/enrich`；定码在 Python |
| 调用链不可越层 | ✅ 未改 Java / 前端；Python 只调已有 `embed/search` |
| 图谱仅 Nebula | ✅ VID 只信 search 命中后再经 `match_industry_anchors` 的图上码 |
| 可观测 | ✅ `current_trace_id` |
| CI/CD | ✅ push `origin/dev`，未 force；`[agent:algorithm-agent]` |
| D12 | ✅ 未调 `demo-*`；未碰 `amcpdp-*` / `aip_kb_*` |
| 数据策略 | ✅ 写槽走 polan demo 闸门；禁写正式 `gkxlumenx_*` |
| Java 不写算法 | ✅ 本叶零 Java |
| D8 / D9 / D10 | N/A（无 UI / 无指标卡） |
| §0 #3 重灌不同步 search | ✅ grep 零命中 |
| §0 #16 不自建 collection | ✅ 只 search |
| §0 #17 禁止采 top1 | ✅ 单测锁死 |
| §0 #19 不 rebuild；degraded 诚实 | ✅ 503 + 不写 |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 110000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.66 |
| cost_warn | green |

口径：algorithm 默认 75/25；B 档 `$3/$15` per 1M；`110000×0.75×3/1e6 + 110000×0.25×15/1e6 = 0.66`。
