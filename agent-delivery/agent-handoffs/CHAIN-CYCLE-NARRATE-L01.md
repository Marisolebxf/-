# CHAIN-CYCLE-NARRATE-L01 · Handoff

| 项 | 内容 |
| --- | --- |
| 任务 | 产业周期 — Prompt v2 + 双落点治理（OPEN-CY-1/2） |
| 角色 | algorithm-agent（监管人 human:徐滕强） |
| 强度 | ponytail: full |
| 仓 / 提交 | `lumen-algo-py` @ `88d361d`（push `origin/dev`，派单明示授权完工即推） |
| 设计门 | `DOC-CHAIN-CYCLE-ANALYSIS-CHAIN-L01`（05.2.1 §7–§8） |

## 范围与实现

- **OPEN-CY-1 Prompt 文件化**：`lumen_common/prompts/chain/cycle.diagnose.v2.txt` / `cycle.forecast.v2.txt` 落盘（照 05.2.1 §8 草案全文），经统一 `load_prompt()` loader 加载；`cycle.py` 删除内联 `DIAGNOSE_SYSTEM/FORECAST_SYSTEM`（不再作唯一真源）；版本 `cycle.prompts.v1→v2`（`PROMPT_PACKS`/`PROMPT_PACK`/`job_runtime.PROMPT_PACK_BY_GRAPH` 同步）。
- **OPEN-CY-2 文案护栏**（全部在 `call_diagnose_llm` / `call_forecast_llm` 内，节点层零改动）：
  - L1：`confirmed_phase` 必须 ∈ 相位枚举（改判由既有 `node_diagnose_stage` 相等校验拦截）；`rationale` ≤120 字 + 因果禁句 + **数字白名单**（`math.isclose` abs 1e-6；白名单池剔除 `prohibitions` 与 `retrieval_excerpts.id` 标识符，防「ID 数字拼数」）；编造 `evidence_ids` 丢弃（只保留事实包 excerpt id）。
  - L2：drivers ≤40 字逐条白名单过滤；拐点 `direction` 枚举 + `axis_year` 落 hist+forecast 年份窗口 + label/description 白名单；decision_brief 两键 ≤80 字白名单，不过则键留空（节点层按键回退 `RULE_BRIEF` 规则稿）；**全过滤返回 None** → 节点层按 degraded 走规则稿，不伪 ok。
  - 失败降级不变：无 Key=skipped、调用/校验败=degraded，任务终态仍 success。
- **loader 协作边界**：统一 loader（`lumen_common/prompts/__init__.py`，20 行）原属企业单 `LUMEN-ENT-EVAL-NARRATE-L01` 未提交产物；因其是本单 DoD 硬依赖且为 §5.6 公共基础件，本单先行入库（内容原样），`ent/eval.narrate.v1.txt` 仍归企业单提交，零冲突。

## 偏离说明

1. 「可注入 _narrate_client（或等价）」采用**等价**：沿用现网测试模式 monkeypatch `recipe.call_diagnose_llm / call_forecast_llm / _call_json_llm`（与既有 `test_llm_cannot_change_phase` 同法），不引入企业版的 OpenAICompatibleClient 注入——链域 LLM 管道（`chain_llm_env`）本就是独立约定，不另造第二套注入面。
2. prompt 文件在 v2 草案基础上补第 3/5 条因果禁句明示（对齐 05.3.2 风险域硬约束），其余一字未改。

## 产物清单

| 产物 | 位置 |
| --- | --- |
| Prompt v2 两文件 | `lumen_common/prompts/chain/cycle.{diagnose,forecast}.v2.txt` |
| 统一 loader | `lumen_common/prompts/__init__.py` |
| `cycle.py` 改造 | 内联删除 + import loader + 护栏函数（`_text_ok/_pack_numbers/_year_window/_clean_text`） |
| 版本元数据 | `job_runtime.py` `PROMPT_PACK_BY_GRAPH["cycle.graph.v1"]="cycle.prompts.v2"` |

## 验收证据

- `python3 -m pytest tests/test_chain_cycle.py -q` → **14 passed**（10 既有回归 + 4 新增：`test_prompt_files_are_single_source` / `test_diagnose_llm_text_guard`（白名单外数字/因果句/编造证据三例）/ `test_forecast_llm_text_guard`（越窗拐点/白名单外驱动/超限键回退））。
- 链域全量回归：`pytest tests/ -k chain` → **189 passed, 1 skipped**（既有 skip）。
- `py_compile` 三文件通过；不改 Java 契约、不碰 RustFS（LLM 对上层屏蔽，契约面仅 `honesty.llm`/`degraded`/`prompt_pack_version` 既有字段）。

## 架构合规自检

| 铁律 | 自检 |
| --- | --- |
| 调用链 / Java 契约不变 | ✅ 零 Java 改动；complete `prompt_pack_version` 值升 v2（既有字段） |
| LLM 只在算法侧、Key 边界 | ✅ 未动 `chain_llm_env`；Key 仍仅集群 Secret `gkx-zhipu-llm` |
| 诚实性（D9） | ✅ degraded/skipped 三态不变；全过滤不伪 ok；数字白名单防编造 |
| 不替甲方拍板 | ✅ QC03 临时口径语气条款保留在 prompt v2 |

## cost（四字段）

| 字段 | 值 |
| --- | --- |
| actual_tokens | ~85,000（会话估算：真源/样板通读 + 实现 + 测试） |
| model_used | glm-5.3-Flash |
| actual_cost | ~$0.26（估算） |
| cost_warn | false（远低于 $10 阈值） |

## 后续

- 企业单（`LUMEN-ENT-EVAL-NARRATE-L01`）提交时 `ent/` 文件直接落已入库 loader 之下，无需再动 `__init__.py`。
- OPEN-CY-1 剩余：key_link/bottleneck/panorama/regional/shenzhen 7 图 prompt 迁移（另单）。
