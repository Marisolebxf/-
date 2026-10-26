# LUMEN-ENT-EVAL-NARRATE-L01 · 企业评估 — narrate_eval 润色收尾（三模式事实包）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | registry：`LUMEN-ENT-EVAL-NARRATE-L01`（epic E-ENT-SCRUM-PDR，P0，claimed→in_progress 已按 MCP 流程提交推送） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。复用 `polan/insight_narrate` 流程骨架 + 既有 Common `llm_client`，未新增依赖、未加抽象层；仅落 `narrate_eval.py`（184 行）+ prompt loader（14 行）+ 版本化 prompt 文件 + 接线 15 行 + 单测。D9 诚实性（三态如实上报、越界退规则稿）与 §5.6 prompt 治理按约交付，未用 YAGNI 砍。唯一 ponytail 注释：数字白名单只做浮点相等（对齐金样，升级路径=字段级引用）。 |

## 问题清单

- 政策 `insight_narrate.py` 内联 `_SYSTEM` 为历史债——本单不跟抄，文案真源落 `lumen_common/prompts/ent/eval.narrate.v1.txt`（§5.6）。
- 事实包按 §5.2 收敛：不带企业原始明细、不带 `rd_investment_pct`（恒 None，送了诱导编数）、不带融资额/注册资本/诉讼。
- `competitiveness` 的 `dimension_rows` 每企业 3 行共用同一规则稿；润色按「企业×维度」逐卡校验，未命中行自然保留规则稿。
- 45/70 阈值写入事实包 `thresholds`，否则「低于 45 分线」这类合法短评会被白名单误杀（§5.4 示例要求）。

## 修改内容

- 新增 `lumen_common/tasks/narrate_eval.py`：一个收尾函数三种事实包（technology→`diagnosis_rows[].gap_text`、business→`diagnosis_rows[].diagnosis_text`、competitiveness→`dimension_rows[].gap_text`）；只改 text；narration 三态 `skipped|fallback|ok`；8s/0 重试/temperature=0.1；失败逐行退规则稿、任务仍 success；`confidence`/`data_quality` 不触碰；无新增 `degraded`。
- 新增 `lumen_common/prompts/__init__.py` + `lumen_common/prompts/ent/eval.narrate.v1.txt`：Common 统一 prompt 目录 + 单一 loader（`load_prompt`，lru_cache）；`PROMPT_PACK = "ent.eval.narrate.v1"` 对齐链域版本元数据习惯；改语义必须升版本 + 金标样例，禁 silent 改同名文件。
- 接线 `lumen_common/tasks/executor.py`：`_run_async` 内 `_compute_result` 之后、`finish_success` 之前调 `_narrate_eval_tail`（仅评估类 sub_type；异常兜底保任务终态）；`_narrate_client` 经 `extra_params` 注入（对齐政策 job）。
- 校验（§5.3 写死）：返回 `{"cards":[{"enterprise","text"}]}`；企业名必须在事实包内（多出/重复丢弃）；单条 ≤80 字；数字白名单浮点相等；禁因果句（因为/由于/导致/受…影响）。
- 客户端对齐 Common `llm_client`（`OpenAICompatibleClient`），Key 只在集群 Secret `gkx-zhipu-llm`，Java / `gkx_ai_service` 不感知、不透传。
- 编排仓文档 as-built：`05.3.1` §5 状态→「算法侧已实现」+ §5.7 as-built 锚点 + §7 快照同源现状 + 修订 v0.4；`05.3.2` ENT-NARRATE-01 关闭（算法侧）+ 修订行。

## 测试结果

- 新增 `tests/test_ent_eval_narrate.py` **10 例全绿**：无 Key skipped、空行 skipped、客户端异常 fallback 且规则稿原样、ok 只换文案、白名单外数字/未知企业/重复卡 fallback、因果句+超长 fallback、事实包断面（无原始明细、阈值在包）、三模式字段接线、8s/0 重试/0.1 构造参数、prompt 文件即 system 唯一真源。
- 全仓回归 `pytest tests/`：**555 passed, 6 skipped**（约 170s），存量零破坏。
- executor 接线自检脚本：business 润色生效、`pain_points` 不触碰、narration 写回正确。
- 契约对照 05.3.1 §5 逐条：§5.1 边界（只改三字段）✅ / §5.2 事实包 ✅ / §5.3 校验+三态+8s ✅ / §5.6 prompt 统一 ✅；ADVICE/suggestions 未润色 ✅（ENT-NARRATE-02 暂缓）。

## 遗留风险

- **ENT-NARRATE-05 路径 A（FE）未落地**：报告 v2「关键发现」在 technology/business 模式暂仍显示 FE 规则两句（frontend-agent 同批交付）；竞争力报告润色稿落快照即自动同源。
- 模型真实质量（金标语义）未经真实 Key 线上验证；单测用注入桩。首次 dev 联调建议抽查 5 家企业对照 §5.4 允许/禁止示例。
- 50 家对象 token 估算 <8K（ENT-NARRATE-03）；若线上超预算需按该开放项做分批，禁止砍企业行。
- `narration` 随信封持久化到 RustFS JSON，业务界面不展示——FE 无需改动（本单）。

## CI/CD（必填）

- 分支：`dev`（lumen-algo-py）
- commit：`[agent:algorithm-agent] LUMEN-ENT-EVAL-NARRATE-L01 narrate_eval 三模式 + Common prompt 统一`（见下「涉及文件」；**待人工验收后由监管人放行推送**——lumen 正式仓人工验收闸门，未擅自 push）
- pipeline URL / ID：push 后自动触发（dev → K8s dev），以 CI 实跑为准
- 部署 namespace / 镜像 tag：gkx-lumen dev（`Dockerfile.api` 已 COPY `lumen_common/`，prompt 文件随镜像）
- K8s rollout：待 push 后 CI 触发
- dev 测试 URL / 命令与结果：`python3 -m pytest tests/test_ent_eval_narrate.py -q` → 10 passed

## 可观测性（建议）+ 观测补记指引

- 现状：润色收尾只打 logger.info/warning（`Task %s narrate_eval sub_type= status= reason=` / fallback 原因），OTel 无新增 span（narration 三态已随信封持久化，可事后归集）。
- **观测补记指引（实现后回写 05.3.1 §5.0/§7 与 05.3.2 ENT-NARRATE-01——已完成，见上文修改内容）**：
  1. `narration` 字段随结果信封进 RustFS 快照，事后统计三态分布：按 `result.narration.status` 聚合（`skipped/no_key` 占比应随 Secret 配置归零）；
  2. 日志检索：`narrate_eval sub_type=`（ok/fallback/skipped 计数）与 `ent eval narrate fallback:`（异常类型）；fallback reason 是逗号拼接的越界企业名/异常类名，可直接定位脏行；
  3. 不新增 `degraded`/不改 `confidence`（§5.3），取数失败与润色失败不会混淆——排查时先看 `narration.reason`，再看节点重试记录；
  4. 后续如需 Tempo span：在 `_narrate_eval_tail` 包一层 OTel span（属性 `narration.status`），本单未做（避免为统计重复埋点，信封已是事实源）。

## 涉及文件

- `lumen-algo-py`（本地，待验收后 push）：
  - `lumen_common/tasks/narrate_eval.py`（新增）
  - `lumen_common/prompts/__init__.py`、`lumen_common/prompts/ent/eval.narrate.v1.txt`（新增）
  - `lumen_common/tasks/executor.py`（接线 `_narrate_eval_tail`）
  - `tests/test_ent_eval_narrate.py`（新增，10 例）
- `gkx-orchestration`（已随本 handoff commit）：
  - `agent-delivery/agent-handoffs/LUMEN-ENT-EVAL-NARRATE-L01.md`（本文件）
  - `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.1-企业技术力评估对比分析.md`（as-built v0.4）
  - `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.2-企业分析LLM落点表.md`（ENT-NARRATE-01 关闭）
