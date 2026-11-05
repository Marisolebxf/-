# Handoff · LUMEN-CHAIN-SZ-NARRATE-L01

> 执行：agent:algorithm-agent · 监管人：human:徐滕强 · 仓：`lumen-algo-py`（origin/dev）
> 强度：ponytail full · 设计真源：`05.2.4-深圳产业对比与发展链路.md`（SZ-01 / SZ-02）
> 状态：**改动停本地未 push**（人工验收闸门 2026-10-20 裁定）；registry 单据 coordinator 建单后回填

## 1. 范围与实现

### SZ-01 · prompt 文件化迁移（业务 .py 零内联）

| 叶 | prompt 文件（新增） | pack（v1→v2 顺延） | 内联迁置 |
|---|---|---|---|
| shenzhen_comparison | `lumen_common/prompts/chain/shenzhen_comparison.narrative.v1.txt` | `shenzhen_comparison.narrative.prompts.v2` | `NARRATIVE_SYSTEM` → `load_prompt(NARRATIVE_PROMPT_FILE)` |
| shenzhen_development | `lumen_common/prompts/chain/shenzhen_development.path.v1.txt` | `shenzhen_development.path.prompts.v2` | `PATH_SYSTEM` → `load_prompt(PATH_PROMPT_FILE)` |

- **分文件（不合并）的理由**：两叶 pack id 独立（`shenzhen_comparison.narrative.*` / `shenzhen_development.path.*`），语义生命周期独立（对比归纳 vs 路径生成），与 chain 目录既有「逐能力一文件」治理惯例（cycle 两文件、key_link/bottleneck 各一文件）一致；合并文件需再造分节 loader，违背 ponytail 阶梯第 2 条。
- 文案**语义零变化**：内联版全部硬规则关键词逐句保留（测试断言钉死）；文件头注释注明出处与升版规则（对齐 `regional.gap.v1.txt` / `key_link.n4c.v2.txt` 头注释体例）。
- `job_runtime.PROMPT_PACK_BY_GRAPH` 同步深圳两行 v1→v2（**只新增深圳两行改动**；该文件中 key_link/bottleneck/regional 四行 v1→v2 为 CHAIN-DIAG/REGIONAL 其他单据的既有未提交改动，本单未触碰）。

### SZ-02 · 流程内 LLM 三态显式建模（两叶分别锁死）

**comparison · narrative**（`node_narrative`）：
- 无 Key → `skipped`（`degrade_reasons=["no_key"]`），不外呼；调用失败 → `degraded`（`["llm_unavailable"]`）；成功 → `ok`。
- 三态写回 `arts["art.llm_status"]`，组装端 `honesty.llm = {"narrative": <status>}`（对齐 key_link/bottleneck/regional 惯例）。
- 任何非 ok 态都退规则稿（bundle 内置模板），任务终态不变。

**development · path_generate**（`node_path_generate`）：
- 无 Key → `skipped`（不咨询 LLM，直接规则稿 `_rule_paths`）；有 Key 失败/空产出 → `degraded`（同样退规则稿）；成功 → `ok`。
- 淘汰旧词汇 `"failed"`（无消费方，grep 证据在 §5），对齐 REGIONAL-03 三态词汇表。
- `honesty.degrade_reasons` 按态细分：skipped→`["no_key"]`、degraded→`["llm_unavailable"]`（原实现恒 `["llm_unavailable"]`）。
- ① **「路径数 <2」硬失败保持不变**：`path_validate` / `validate_assemble` 的 `PATH_COUNT_LT_2 → NodeFailed` 一行未动；degraded 语义不得弱化判定硬失败（测试 `test_development_lt2_paths_still_hard_fails` 锁死：有 Key + LLM 只回 1 条 → `outcome=failed`）。

**共享 caller**（`shenzhen_common.call_json_llm`）：payload 补 `"temperature": 0.1` 写死（对齐 regional `call_gap_llm` REGIONAL-04 先例；原深圳 caller 未写 temperature，环境注入可抖动采样）。

### 防护不动（as-built 保留）

- `PATH_SYSTEM`「不得编造源外数字」语义（文件原文保留）+ `numbers_outside_source` 校验 + `SILENT_KEYS` + `FORBIDDEN_KPI_BLOCKS` + 禁自签 `result_snapshot_id` 全部未动。

## 2. 偏离说明

| 项 | 偏离 | 理由 |
|---|---|---|
| 既有测试前置 | `test_chain_shenzhen.py` 4 例 LLM 桩用例补「配 Key 前置」+ 1 例 reason 断言 `llm_unavailable`→`no_key` | SZ-02 新语义下「无 Key 不咨询 LLM」；测 LLM 产出的用例必须配 Key。桩注入手法（monkeypatch `call_json_llm`/`httpx.post`）零外呼不变 |
| `"failed"` 状态词淘汰 | development `llm_status` 词汇表 `ok/skipped/degraded` 三态 | 派单明确「无 Key → skipped、失败 → degraded、成功 → ok」；grep 全仓无 `llm_status == "failed"` 消费方 |

其余零偏离：不改 Java 对外契约、不碰 RustFS 新路径、QC08/SZ_MOCK 等权分不动（SZ-04 另单）。

## 3. 产物清单（全部停本地，未 commit / 未 push）

```
lumen_common/prompts/chain/shenzhen_comparison.narrative.v1.txt   # 新增
lumen_common/prompts/chain/shenzhen_development.path.v1.txt       # 新增
lumen_common/algorithms/chain/shenzhen_comparison.py              # NARRATIVE_SYSTEM 迁置 + pack v2 + 三态
lumen_common/algorithms/chain/shenzhen_development.py             # PATH_SYSTEM 迁置 + pack v2 + 三态
lumen_common/algorithms/chain/shenzhen_common.py                  # call_json_llm temperature 0.1 写死（2 行）
lumen_common/algorithms/chain/job_runtime.py                      # 仅深圳两行 pack v1→v2
tests/test_chain_sz_narrate.py                                    # 新增 8 例
tests/test_chain_shenzhen.py                                      # 4 例补 Key 前置 + 1 例 reason 断言
```

## 4. 验收证据

- **全仓回归：630 passed, 6 skipped**（`python3 -m pytest tests/ -q`，2026-10-28，零失败）。
- 新增护栏 8 例（`tests/test_chain_sz_narrate.py`）：
  1. `test_both_systems_loaded_from_files` — 文件=唯一真源、关键词语义零变化、pack v2 顺延、无 v1 实体文件
  2. `test_prompt_pack_registry_synced` — registry 两行映射与 recipe 一致
  3. `test_comparison_no_key_skipped` — 无 Key skipped/no_key、终态仍 succeeded、桩抛错证明零外呼
  4. `test_comparison_llm_failure_degraded` — 失败 degraded/llm_unavailable、终态不变
  5. `test_comparison_llm_ok_and_prompt_is_single_source` — ok 态 + 发出 system 逐字等于文件 + temperature 0.1
  6. `test_development_no_key_skipped_rule_draft` — ② 无 Key 规则稿、succeeded
  7. `test_development_llm_failure_degraded` — ② 失败规则稿、succeeded
  8. `test_development_lt2_paths_still_hard_fails` — ① 有 Key + LLM 1 条 → PATH_COUNT_LT_2 failed（弱化即红）
- 深圳 21 例（12 既有 + 8 新增 + 1 既有 reason 调整）全绿。

## 5. FE 缺口清单（只登记，不实现）

1. `honesty.llm` 新增 `narrative` 键（comparison）：FE 若读 `honesty.degraded` 已兼容；如需展示 LLM 状态徽标按此键消费。
2. comparison `honesty.degrade_reasons` 出现 `no_key`（新枚举值）：FE 文案映射需覆盖 `no_key`（现只认 `llm_unavailable`）。
3. development `honesty.degrade_reasons` 无 Key 时为 `["no_key"]`：同上。
4. `versions.prompt_pack_version` 两叶由 v1 变 v2：FE 如按 pack 版本做缓存/对比需同步。
5. 两叶无新增展示字段、无结构变化：`paths` / `benchmark_judge` / 四维矩阵契约不变，FE 无强制改造。

## 6. 架构合规自检（公约 §2 逐条）

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ 本单全部改动在 lumen-algo-py，LLM 调用在 Python |
| 2 调用链 前端→Java→Python /internal | ✅ 未改调用链与 Java 契约 |
| 3 NebulaGraph | ✅ 不涉及图谱 |
| 4 可观测 | ✅ 沿用 worker stage/complete 回调，未减埋点；honesty 三态即观测面增强 |
| 5 CI/CD | ✅ 停本地，push 由人工验收后执行 |
| 6 demo2 只读 | ✅ 不涉及 |
| 7 共享聚合核心 | ✅ 未动聚合边界 |
| 8 数据策略 | ✅ 不涉及 |
| 9 D8 前端规范 | ✅ 不涉前端（FE 缺口已清单化 §5） |
| 10 D9 数据血缘 | ✅ honesty/metric_id/GAP 引用未减；`llm` 三态写回增强诚实性 |
| 11 D10 交互规范 | ✅ 不涉 |
| 12 demo/lumen 隔离 | ✅ 仅 lumen-algo-py |

## 7. 遗留与后续

- registry `LUMEN-CHAIN-SZ-NARRATE-L01`：截至完工 coordinator 尚未落单（task-get 反复 404），evidence/cost 回填与状态推进待建单后补。
- SZ-03（FE 行级锚点）、SZ-04（QC08 闭合后 SZ_MOCK 退役）另单。

## 8. cost 回填（handoff 时四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | 520000 |
| model_used | glm-5.3-Flash |
| actual_cost | 0.6 |
| cost_warn | green |

ponytail: full（阶梯执行：loader/三态/测试全部复用先例手法，零新依赖、零新抽象；prompt 分文件为治理惯例最小一致解）
