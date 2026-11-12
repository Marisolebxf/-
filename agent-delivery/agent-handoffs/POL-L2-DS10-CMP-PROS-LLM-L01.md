# Handoff · POL-L2-DS10-CMP-PROS-LLM-L01

- 任务：科创政策全景 · 政策详情对比 · LLM优缺点Job + 政策名称
- claimed_by：`agent:fullstack-agent`
- supervised_by：`human:淮政玮`
- claim_type：会话认领
- ponytail：full
- 日期：2026-11-12

## 范围与实现

按监管人锁定方案 A：214 详情对比点「开始对比」后，若优缺点皆空则起 `policy_detail_pros_cons` Job（display → async → Python LLM）写入 `gapfill_policy_detail_compare` 再回读；已有非空不覆盖。列头/图例/总结用政策名称，禁止「政策 #id」。

对照需规 214-6 / COVER-FDE 读面；本叶补「空则 LLM」加工链与展示名。

## 偏离

无。无密钥时诚实空态，不造假文（与 ARCH 一致）。

## 产物清单

| 仓 | 产物 |
|---|---|
| gkx-orchestration | A/B/C/E 简报；ARCH/API/DATA 回写；合规用例 214 行；本 handoff |
| lumen-algo-py | `polan/detail_pros_cons_job.py`；`polan/job.py` 白名单；单测 |
| lumen-svc-platform | display `JOB_SUB_TYPES`；async `PolicyAnalysisTypes`；单测 |
| lumen-ui-science-pc | `compareLive.ts` / `ComparisonModal.vue` / `FE-POL-CMP-LIVE.test.mjs` |

## 验收证据

- `node src/views/policy/panorama/FE-POL-CMP-LIVE.test.mjs` 全绿
- `pnpm type-check`（lumen-ui-science-pc）绿
- `PYTHONPATH=vendor/entan-py pytest tests/test_detail_pros_cons_job.py` 3 passed
- Java 单测已扩（待 CI）
- 前端仓：**待人工确认后推送**（fe-manual-confirm-push）

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ LLM 在 lumen-algo-py |
| 调用链 FE→Java→Python /internal | ✅ |
| Nebula | N/A |
| 可观测 | 沿用既有 Job 管道 |
| D12 demo 隔离 | ✅ 只改 lumen |
| D18 禁接口写死 mock | ✅ 写 gapfill 再读 |
| D4 mock | ✅ is_mock=1 / llm-synth |

## 遗留

- 线上 §6.5 冒烟待 Java/Python CI 发版 + 前端 push 后执行
- 合规样例已灌文案时 Job 跳过（符合「非空不覆盖」）
