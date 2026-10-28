# CHAIN-DIAG-NARRATE-L01 · 产业诊断分析（关键环节+瓶颈堵点）LLM 叙述落点改造

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 loader（`lumen_common/prompts.load_prompt`）与 `_fact_conflict`/`_empty_narrative`，未新增依赖、未新增框架；G3 只加 `art.llm_status` 一个状态位；确认未用 YAGNI 跳过 D9 诚实性（三态如实上报）与可观测（degrade_reasons 照旧上抛） |

## 范围与实现（对齐 registry DoD / 05.2.2 §5 / §8）

### 1. Prompt 文件化（CHAIN-DIAG-01，语义零变化）

| 项 | 前 | 后 |
|---|---|---|
| key_link | `N4C_SYSTEM` 内联于 `chain/key_link.py` | `lumen_common/prompts/chain/key_link.n4c.v2.txt`，经 `load_prompt()` 加载 |
| bottleneck | `ADVICE_SYSTEM` 内联于 `chain/bottleneck.py` | `lumen_common/prompts/chain/bottleneck.annotate.v2.txt`，经 `load_prompt()` 加载 |
| PROMPT_PACK | `key_link.n4c.prompts.v1` / `bottleneck.annotate.prompts.v1`（无实体文件） | `.v2`；`job_runtime.PROMPT_PACK_BY_GRAPH` 两行同步升 v2 |
| 旧版文件 | — | v1 无实体文件，无删除动作；升版删旧惯例自 v2 起生效 |
| 语义 | — | 硬规则逐条保留（key_nodes 只读 / 禁发明数字 / 禁「断链」「资金」/ 维名资本 / 禁「已完成实时全网检索」/ 只输出 JSON）；bottleneck 口头「不得发明数字」顺势写实为「每个数字必须能在 Context 中找到」（与 G2 校验同向，非语义收紧） |

### 2. 护栏收敛

| 缺口 | 处置 |
|---|---|
| **G2** bottleneck 无数字白名单 | `call_advice_llm` 校验链改 `_advice_ok(...) or kl._fact_conflict(data, context_pack)`，复用 key_link `_NUM` 整包正则；输出数字 ⊄ Context 即拒 → 重试耗尽 → degraded |
| **G3** 三态粒度 | 两叶 annotate 节点先查 `llm_configured()`：无 Key → `skipped` + `degrade_reasons=["no_key"]`；调用失败 → `degraded` + `["llm_unavailable"]`；成功 → `ok`。`honesty.llm` key_link 补齐（对齐 bottleneck 两态字段）；`art.llm_status` 贯穿。**失败永不改任务终态不变**——`_empty_narrative` 空块回填、任务仍 success。`degrade_reasons` 家族命名维持 05.2.1 §11 拍板冻结（不引 `narration.status` 新字段） |
| **G4** temperature 未写死 | 两叶 `httpx.post` payload 写死 `"temperature": 0.1`（对齐 05.3.1 §5.3 客户端契约） |
| **G6** 无 Key 空态 | 维持诚实空态（`overview=""` / `by_stage=[]` / `items=[]` / `causes=[]` / `suggestions=[]` + degraded 标志）；规则稿占位属 CHAIN-DIAG-07 产品定义，本单不碰 |
| **G5** | Java 侧 schema 校验，api 侧另单，不在本单 |

### 3. 调用参数与 05.3.1 §5.3 对齐

`temperature=0.1`、`timeout=20s`、`retry_max` 默认 0（limits 可调）——写死项只 temperature；`max_tokens` 不传（与全仓 chain 域现状一致，避免截断 by_stage 长数组）。

## 测试结果

- 新增 `tests/test_chain_diag_narrate.py`（7 例）：prompt 文件即 system 唯一真源断言（`N4C_SYSTEM == load_prompt(N4C_PROMPT)`）、v1 无实体文件、PROMPT_PACK_BY_GRAPH v2 同步、G2 白名单拒（`fact_conflict`）、G3 无 Key skipped / 调用失败 degraded（client 桩 = monkeypatch `httpx.post`，零外呼）、G4 两叶请求体 `temperature==0.1` 断言。
- 既有测试更新 3 处：`test_chain_key_link.py` / `test_chain_bottleneck.py` 版本断言 v1→v2 + 无 Key 语义 `no_key`/`skipped` + 注入桩测试补 env 前置（G3 门先查 `llm_configured()`）；`test_chain_job_runtime.py` `llm_unavailable`→`no_key`。
- **全仓回归：`pytest tests/` → 614 passed, 6 skipped, 0 failed**（两次全量确认）。

## 偏离说明

- 单测经**节点函数直注**（`node_annotate(arts, ctx)`）而非 HTTP 层注入：护栏逻辑（G2/G3/G4）全在 `call_*_llm` 与节点层，节点直注覆盖等价且少一层 TestClient 样板；端到端行为由既有 `test_chain_key_link.py`/`test_chain_bottleneck.py` 回归兜住。
- prompt 文件头注释按 `eval.narrate.v3.txt` 惯例含升版指引；`PROMPT_PACKS` 元组（cycle 式）未引入——两叶各一 prompt，`PROMPT_PACK` 单值够用，不抄不必要结构。

## FE 接线清单（交 FE 小单，CHAIN-DIAG-06；本单不做 FE）

后端 payload 契约未变，以下为 FE 消费缺口（`lumen-ui-topic` → `industry-center/diagnosis`）：

| # | 缺口 | 后端字段 | 现状 |
|---|---|---|---|
| 1 | KPI 块错位 | `kpi.bottleneck_count` / `kpi.max_severity`（注意键名是 `max_severity`） | FE 读 `summary.*` → 堵点数靠前端重算、严重度恒「暂无」；改读 `kpi` 块 |
| 2 | 代表企业包装错位 | `sections.representative_enterprises.items[]` | FE 把对象当数组读 → 恒空态；改读 `.items` |
| 3 | 竞争格局 / 技术趋势零消费 | `sections.competition.{overview,by_stage}` / `sections.tech_trends.items` | FE 全仓无触点；**是否新增展示块属产品定义（QC02 关联面），先过 Wireframe** |
| 4 | 成因 / 建议零消费 | `sections.node_details[].causes/suggestions` | 详情侧栏只显健康度/档位；本单后字段已实时有数（有 Key 时） |

另：`honesty.llm` 本单为 key_link 新增字段，FE 可选消费（如「AI 叙述不可用」提示）；`no_key`/`llm_unavailable` 区分仅供运维日志，FE 不必感知。

## 架构合规自检

| 铁律 | 自检 |
|---|---|
| 算法只在 Python | ✅ 改动全在 `lumen-algo-py` |
| 调用链不可越层 | ✅ 未改 Java 对外契约、未动回调结构 |
| 可观测性 | ✅ `degrade_reasons`（`no_key`/`llm_unavailable`）随 payload 持久化，stage 回调 `degraded` 上抛不变 |
| 数据血缘 D9 | ✅ 三态如实上报，无伪闭合；`honesty.*` 家族未破坏 |
| 不碰 RustFS 新路径 | ✅ 无对象存储写路径 |
| demo/lumen 隔离 D12 | ✅ 只在 lumen 仓作业 |

## CI/CD

- 分支：`dev`（本地，**完工停本地未 push**——人工验收闸门，lumen-ui-* 仓级规约同款执行于本仓）
- commit：未提交（等验收；工作区另有其他会话未提交产物 `pain_points.py`/`executor.py`/`test_ent_eval_narrate.py`/`pain.narrate.v1.txt`，与本单无关，验收时请分开审）
- pipeline：未触发（无 push）

## 涉及文件

| 文件 | 变更 |
|---|---|
| `lumen_common/prompts/chain/key_link.n4c.v2.txt` | 新增 |
| `lumen_common/prompts/chain/bottleneck.annotate.v2.txt` | 新增 |
| `lumen_common/algorithms/chain/key_link.py` | prompt 文件化 + v2 + temperature + G3 |
| `lumen_common/algorithms/chain/bottleneck.py` | 同上 + G2 白名单 |
| `lumen_common/algorithms/chain/job_runtime.py` | PROMPT_PACK_BY_GRAPH 两行 v1→v2 |
| `tests/test_chain_diag_narrate.py` | 新增 7 例 |
| `tests/test_chain_key_link.py` / `tests/test_chain_bottleneck.py` / `tests/test_chain_job_runtime.py` | 版本与三态断言更新 |

## 遗留风险

- glm-5.3 思考模型下 20s 超时对大 Context Pack 可能偏紧（ent 侧 004/011/012 有 ReadTimeout 先例）；链域两叶 context_pack 较小，暂不调，现网若出现 `llm_unavailable` 激增再校准（`NARRATE_TIMEOUT_SEC` 同款升档路径）。
- G2 整包正则白名单与 ent 侧同款天花板：只做浮点包含判断，不证明语义正确（`_fact_conflict` 内已注 `ponytail:`）。

## 成本

| 字段 | 值 |
|---|---|
| actual_tokens | ~78,000 |
| model_used | glm-5.3-Flash |
| actual_cost | ~0.4 |
| cost_warn | green |
