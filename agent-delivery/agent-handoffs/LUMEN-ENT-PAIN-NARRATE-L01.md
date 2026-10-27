# LUMEN-ENT-PAIN-NARRATE-L01 · 企业痛难点四格润色（narrate_pain）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| ponytail | `full` |
| 设计契约 | `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.5-企业发展痛难点分析.md` §5（实现契约唯一真源）+ `DOC-ENT-PAIN-ANALYSIS-CHAIN-L01.md` §5.2 |

## 范围与实现

严格按 `/goal` 范围：只改 `issues[]` 四格 text（evidence/cause/best_practice/solution），逐格校验逐格替换；title/priority/dimension/typical_enterprises/dimension_cards 零触碰。Java 契约不变（narration 为新增可选字段，业务界面不展示）。

### 产物清单（lumen-algo-py，本地未提交）

| 文件 | 变更 |
|------|------|
| `lumen_common/tasks/narrate_pain.py` | **新增**：四格润色收尾函数（三态 / 逐格退 / 计数白名单 / 诚实句必留 / 政策词表 dormant）。`PROMPT_PACK="ent.pain.narrate.v1"`；客户端 30s/max_retries=0/temperature=0.1 复用 Common `OpenAICompatibleClient`；Key 纪律同评估族（只认 GKX/ENTAN/LLM 前缀，无 Key → skipped） |
| `lumen_common/prompts/ent/pain.narrate.v1.txt` | **新增**：四格论证链 prompt（40~85 字目标 / 100 硬上限 / 计数溯源 / 禁因果外推 / 诚实句整句保留 / 禁政策工具 / 禁空话营销腔）。与 `eval.narrate.v3` 同目录同 loader 同治理（升版删旧版） |
| `lumen_common/algorithms/science/pain_points.py` | **增产**（05.3.5 §5.2 目标态）：`signal_summary`（七类信号计数，口径按 hit lambda 经 `_signal_summary` 从 issues 计数派生）、`unavailable_fields`、`honesty_note`；诚实句整句抽为常量 `HONESTY_FIELDS`（单一真源，润色侧只读消费）。与润色解耦：skipped 时增产字段照常落快照 |
| `lumen_common/tasks/executor.py` | **接线**：`_narrate_pain_tail`（对齐 `_narrate_eval_tail` 模式），在 pain_points 结果组装后、finish_success 前调用；`sub_type != "pain_points"` 直接 return；异常全兜底（润色永不拖垮任务）；支持 `_narrate_client` 测试注入通道 |
| `tests/test_ent_pain_narrate.py` | **新增**：20 个测试（注入 client 桩） |
| `tests/test_ent_eval_narrate.py` | **仅一处守卫更新**：`test_prompt_dir_single_file` 断言目录 = eval.v3 + pain.v1 双文件（eval prompt 本体未动一字） |

### 契约落点对照（05.3.5 §5.3）

- **三态**：`skipped(no_key|empty)` / `fallback`（超时、坏 JSON、卡缺失/多出、单格违规）/ `ok`；失败退规则稿任务仍 success ✅
- **逐格退**：`narration.reason` 记 `title:field:verdict`（verdict ∈ `long{N}|cause|num:{x}|policy|honesty_missing`）；卡缺失 `missing:N`、多出/重复 `card{i}` ✅
- **诚实句整句必留（限 evidence 格）**：涉密 issue 的 evidence 润色稿必须子串包含诚实句整句（从 `HONESTY_FIELDS` 按 evidence 实配对），缺失 → `honesty_missing` 判拒；其余格无此要求 ✅
- **计数白名单**：事实包全量数值扁平化（同评估族 `_numbers_of` 整包正则）；阈值/计数随包携带可溯源 ✅
- **禁因果外推**：`cause` 格（及所有格）命中 `_CAUSE` 同款正则即拒 ✅
- **禁政策工具**：词表先空列表 → `policy` verdict dormant（漏放不误杀），ENT-PAIN-02 冻结后补词即可，不改结构 ✅
- **事实包**：只带 signal_summary 计数 + unavailable_fields + honesty_note + 卡级 drafts/count/typical，不带企业原始明细；pain_points 信封为扁平结构（issues 在顶层，与评估族嵌套不同形）✅
- **不动字段**：title/dimension/priority/typical_enterprises/dimension_cards/summary/report_status ✅

## 验收证据

- **全仓回归**：`pytest tests/ -q` → **607 passed, 6 skipped**（168.8s，与基线一致）
- **新增测试**：`tests/test_ent_pain_narrate.py` 20 用例全绿，覆盖：三态、逐格退四类 verdict（long/cause/num/honesty_missing）、诚实句只限 evidence 格、计数白名单（9999 拒 / 3·5 溯源过）、卡缺失/多出、政策词表 dormant 放行、事实包边界（无原始明细）、客户端 30s/0/0.1、prompt 治理金标、code fence 变体、executor 接线与崩溃兜底、compute 增产口径
- **文档一致性**：编排仓 `scripts/check-pain-asbuilt.py` 实跑通过（7 titles + 3 honesty lines 与 05.3.5 §3.1 一致）
- **端到端自检**：无 Key 环境 `narrate_pain` → skipped/no_key，规则稿零触碰

## 偏离说明

1. **信封形态**：初版按评估族嵌套 `result.issues` 误设，契约核对 §4 后修正为扁平顶层（`issues`/`signal_summary`/`summary` 同级）——这是与评估族金样的唯一结构性差异，已写进模块 docstring。
2. **signal_summary 派生方式**：§5.2 标注「由 compute 增产或派生」；实现取派生（从 issues 计数映射，未重扫 profiles）——hit 口径天然一致（计数=命中家数），避免双份判定逻辑。scope 过滤时未命中信号计 0（照实）。
3. **诚实句配对**：润色侧按「诚实句整句 ∈ issue.evidence」动态配对（不按 title 硬编码），算法侧常量为单一真源；若未来诚实句迁移出 evidence 格，校验自动失效（fail-safe：不误杀）。

## 架构合规自检

| 铁律 | 自检 |
|------|------|
| 算法只在 Python | ✅ LLM 润色在 lumen-algo-py，Java 零感知 |
| 调用链 | ✅ worker 内收尾，不经前端/Java |
| 可观测 | ✅ `_narrate_pain_tail` logger.info 三态 + reason；narration 落快照（同评估族检索指引） |
| D9 | ✅ 诚实句整句必留 + unavailable_fields 禁编数 + Mock 语义不受影响 |
| Java 契约 | ✅ 结果信封只增 `narration` 可选字段与三个增产字段，四格字段名不变，FE 零改动即同源 |
| prompt 治理 | ✅ 版本化文件 + 单一 loader，业务 .py 无内联文案真源 |

## 成本（budget-estimate.md 四字段）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~180k（含全仓回归日志读取） |
| model_used | glm-5.3-flash |
| actual_cost | ~$0.09 |
| cost_warn | false |

## 遗留 / 移交

- **ENT-PAIN-02**：政策工具词表冻结后补 `_POLICY_WORDS`（`narrate_pain.py` 顶部单点，含 ponytail 注释指路）
- **FE 报告接线**（05.3.5 §5.5）：报告 v2 痛难点块仍固定文案，需另立 FE 小单消费四格；本次结果页路径零 FE 改动即同源
- **线上首例验证**：待生产任务跑一轮观察 ok 率；诚实句整句保留若 ok 率过低，降级方案按 DOC handoff「遗留风险」需监管人拍板升 prompt 版本
- 完工停本地未 push（人工验收闸门，2026-10-20 用户裁定）
