# CHAIN-REGIONAL-NARRATE-L01 · 区域产业评价（指数+竞争力）gap 叙述三态收敛 + prompt 落盘迁移

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |
| 设计真源 | `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.2.3-区域产业评价链路.md`（§5 落点表 R1/R2 + §8 REGIONAL-01~04） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 `load_prompt` loader、key_link 三件套（`llm_configured`/`chain_llm_env`/`_glm53_thinking`）与两叶既有三态骨架，未新增依赖、未新增框架；REGIONAL-02 按 as-built 保留结构性防护未重建白名单（见偏离说明）；确认未用 YAGNI 跳过 D9 诚实性（三态如实上报）与可观测（degrade_reasons 照旧上抛） |

## 范围与实现（对齐 registry DoD / 05.2.3 §5 / §8）

### 1. REGIONAL-01 · Prompt 文件化（语义零变化，两图共用）

| 项 | 前 | 后 |
|---|---|---|
| GAP_SYSTEM | 内联于 `chain/regional_common.py`（两图共享一份） | `lumen_common/prompts/chain/regional.gap.v1.txt`，经 `load_prompt()` 加载；两图共用一份（若后续叙述口径分化再拆两文件并升版，05.2.3 §5.3 预案） |
| PROMPT_PACK | `regional_index.gap.prompts.v1` / `regional_competitiveness.gap.prompts.v1`（有名无文件半迁移态） | `.v2` 顺延；`job_runtime.PROMPT_PACK_BY_GRAPH` 两行同步升 v2 |
| 旧版文件 | — | v1 本无实体文件，无删除动作；升版删旧自 v2 起生效 |
| 语义 | — | 硬规则逐条保留（不得改分数/排名/权重 / 不得发明数字或主体 / 只输出 advantages+weaknesses 两键 JSON），文案字面零变化 |

### 2. REGIONAL-03 · 三态收敛（对齐 key_link CHAIN-DIAG 先例）

两叶 `node_gap_explain` 先查 `llm_configured()`：

| 状态 | 触发 | 表现 |
|---|---|---|
| `skipped` | 无 Key | `degrade_reasons=["no_key"]`；**不进入 `call_gap_llm`，零外呼** |
| `degraded` | 有 Key 但调用失败（超时/HTTP 异常/坏 JSON/缺键） | `degrade_reasons=["llm_unavailable"]` |
| `ok` | 成功 | `degrade_reasons=[]` |

三态写 `arts["art.gap_llm_status"]`；两叶 `honesty.llm` 为本单新增字段（对齐 key_link/bottleneck honesty.llm 惯例）。**失败永不改任务终态不变**：退 `_rule_gap` 规则稿 + `stage_degraded` 上抛 SSE，complete 仍 `succeeded`；`degrade_reasons` 家族命名维持 05.2.1 §11 拍板冻结。`call_gap_llm` 内部的无 Key 前置短路移除（三态归调用方，docstring 已注明）。

### 3. REGIONAL-04 · 调用参数写死

`temperature=0.1` 写死于 `call_gap_llm` 请求体（ REGIONAL-04 原建议 0.2 起步，取 0.1 对齐全仓 chain/ent 域现行写死值——key_link/bottleneck/ent narrate 均为 0.1）；`timeout=20s`、`retry_max` 默认 0（limits 可调）不变；`max_tokens` 不传（与全仓 chain 域一致，避免截断两数组）。

### 4. REGIONAL-02 · 数字白名单：as-built 保留，不重建

05.2.3 §5.2 结论原文：「协议层两键白名单 + 组装期数值全部取自 score_bundle（LLM 返回值只进 advantage_gap 文本，**结构性不可能改数**）；结构性强于 05.2.2，**无需额外加锁**」。本单按 as-built 保留该防护并落测试断言，未复刻 key_link `_fact_conflict` 整包正则——若后续要求正则级白名单，升级路径为一行 `or kl._fact_conflict(data, pack)`。prompt 层「不得发明数字」口头规则保留（随文件迁移）。

## 测试结果

- 新增 `tests/test_chain_regional_narrate.py`（8 例）：prompt 文件即 system 唯一真源（`GAP_SYSTEM == load_prompt(GAP_PROMPT)` + 硬规则关键词断言）、v1 无实体文件、两叶 PROMPT_PACK v2 与 `PROMPT_PACK_BY_GRAPH` 同步、两图共用同一 `call_gap_llm`、G4 请求体 `temperature==0.1` + system 来自文件、REG-02 越权键丢弃（`composite_index`/`rank` 不在返回）、G3 无 Key skipped（含「不外呼」断言）/ 调用失败 degraded / 成功 ok（client 桩 = monkeypatch `httpx.post`，零外呼）。
- 既有测试适配 1 处：`test_chain_regional.py::test_llm_cannot_change_index_scores` 补两行 env 前置（G3 门先查 `llm_configured()`，有 Key 才走 `call_gap_llm` 桩）。
- **全仓回归：`pytest tests/` → 621 passed, 6 skipped, 0 failed**（改动前后两次全量确认）。

## 偏离说明

- 单测经节点直注（`node_gap_explain(arts, ctx)`）而非 HTTP 层注入：护栏逻辑全在 `call_gap_llm` 与节点层，端到端行为由既有 `test_chain_regional.py`（17 例）回归兜住（CHAIN-DIAG 同款偏离，已验收先例）。
- temperature 取 0.1 而非 REGIONAL-04 文本建议的 0.2：跨域一致性优先，同款偏离走「实测校准」条款，后续如叙述发散单独升版调参。
- `regional_common.GAP_PROMPT_PACK`（`regional.gap.prompts.v2`）为 common 层记录常量，未接线 `versions`——两叶 `versions.prompt_pack_version` 继续用各自 `PROMPT_PACK`（v2），避免 Java 面出现第三个 pack 字符串。
- `honesty.llm` 为两叶新增字段：FE 不必感知（运维日志/降级提示可选消费）。

## FE 接线清单（REGIONAL-05，交 FE 小单；本单不做 FE）

仓 `lumen-ui-topic` → `/industry-center/regional`（`parseRegionalBoard`，`industryChainTask.ts`）。后端 payload 契约本单未变，以下为消费缺口：

| # | 缺口 | 后端字段 | 现状 |
|---|---|---|---|
| 1 | 热力图 x 轴 demo 别名 | `sections.heatmap_matrix.x_labels`（产业基础/学术生态/创新生态/综合） | FE `COMP_HEATMAP_DIMS` 硬编码「企业能力/学术生态/配套生态力/综合指数」，未读后端 x_labels——QC11 关联展示缺口 |
| 2 | `version_boundary` 块错位 | `honesty.version_boundary` | FE 读 `sections.version_boundary`，后端在 `honesty` → 恒空，跨版本禁混排提示未透出 |
| 3 | `heatmap_gis` 零消费 | `sections.heatmap_gis.{enabled,items,skipped_reason}` | FE 用 `evalMode/regionCount` 本地推导占位，数据链路未通（语义巧合一致） |
| 4 | `leaf_contributions` 零消费 | `sections.leaf_contributions.items[]` | 指数板无叶层渲染位——**需先过产品定义（QC05 关联面）** |
| 5 | `config_honesty` 零消费 | `sections.config_honesty`（`wysiwyg_is_not_result`/模板/权重回显） | 未上板——**需先过产品定义（QC05 关联面）** |

另：过程页五段文案（FE `REGIONAL_TASK_STAGES` vs 算法 `STAGE_LABELS`，语义对应非字面 1:1）是否收紧，并入 REGIONAL-05 一并评估。

## 架构合规自检

| 铁律 | 自检 |
|---|---|
| 算法只在 Python | ✅ 改动全在 `lumen-algo-py` |
| 调用链不可越层 | ✅ 未改 Java 对外契约、未动回调结构；`prompt_pack_version` 仅元数据字符串 v1→v2（Java 无 schema 校验、FE 不读，上游无感） |
| 可观测性 | ✅ 三态 `honesty.llm` + `degrade_reasons`（`no_key`/`llm_unavailable`）随 payload 持久化，stage 回调 `degraded` 上抛不变 |
| 数据血缘 D9 | ✅ 三态如实上报，无伪闭合；`honesty.*` 家族未破坏 |
| 不碰 RustFS 新路径 | ✅ 无对象存储写路径 |
| demo/lumen 隔离 D12 | ✅ 只在 lumen 仓作业 |

## CI/CD

- 分支：`dev`（本地，**完工停本地未 push**——人工验收闸门）
- commit：未提交（等验收；工作区另有其他单据未提交产物：E1 `pain_points.py`/`executor.py`/`pain.narrate.v1.txt` 等 + CHAIN-DIAG `key_link.py`/`bottleneck.py`，验收时请分开审。⚠️ `job_runtime.py` 现同时含两单行级改动——CHAIN-DIAG 的 key_link/bottleneck 两行升版 + 本单的 regional 两行升版，revert/拆分时注意）
- pipeline：未触发（无 push）

## 涉及文件

| 文件 | 变更 |
|---|---|
| `lumen_common/prompts/chain/regional.gap.v1.txt` | 新增（两图共用） |
| `lumen_common/algorithms/chain/regional_common.py` | GAP_SYSTEM 文件化 + `GAP_PROMPT`/`GAP_PROMPT_PACK` + temperature + 三态 docstring（移除内部无 Key 短路） |
| `lumen_common/algorithms/chain/regional_index.py` | PROMPT_PACK v2 + G3 三态分流 + `honesty.llm` |
| `lumen_common/algorithms/chain/regional_competitiveness.py` | 同上 |
| `lumen_common/algorithms/chain/job_runtime.py` | `PROMPT_PACK_BY_GRAPH` regional 两行 v1→v2（仅此两行属本单） |
| `tests/test_chain_regional_narrate.py` | 新增 8 例 |
| `tests/test_chain_regional.py` | 1 处 env 前置适配 |

## 遗留风险

- glm-5.3 思考模型 20s 超时对大 Context Pack 可能偏紧（ent 侧 ReadTimeout 先例）；本族 pack 仅 `{leader,strength,weakness,rows}` 极小，暂不调，现网 `llm_unavailable` 激增再升档。
- `no_key`/`llm_unavailable` 二分会使现网降级分布变化（原全记 `llm_unavailable`）：观测补记评估按 REGIONAL-03 条款随实现后进行，`honesty.*` 家族维持冻结不改。

## 成本

| 字段 | 值 |
|---|---|
| actual_tokens | ~95,000 |
| model_used | glm-5.3-Flash |
| actual_cost | ~0.5 |
| cost_warn | green |
