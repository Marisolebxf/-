# handoff · SVC-ORG-COVERAGE-NARRATE-L01

- **任务**：服务机构产业领域分析 · T1 覆盖结论 narrate（prompt 包 + 装配接线 + FE 渲染）
- **角色**：agent:algorithm-agent（协作 frontend-agent）；监管人：human:徐滕强；认领类型 pull，锁定 2026-10-27 13:38+08:00
- **强度**：ponytail full（最短可用 diff + 一个自检；未引框架、未造第二套 LLM 边界）
- **状态**：实现完成，**改动停本地未 push**（lumen 仓人工验收闸门 2026-10-20）

## 1. 范围与实现（对照 DoD 四条）

| DoD | 交付 |
| --- | --- |
| ① prompt 包 + loader | `lumen-algo-py/lumen_common/prompts/svc/coverage.narrate.v1.txt`（05.7.1 §6 全文）；经既有 `load_prompt()` 单一 loader，业务零内联文案 |
| ② 装配接入 | 新增 `lumen_common/algorithms/svcan/narrate_coverage.py`；`leaf_org_coverage` 收尾一行挂 `narrate_coverage(payload)`。只写 `payload.narration`（三态）；矩阵 depth/breadth 数字零触碰；无 Key→skipped、外呼失败/越数字/禁句→fallback，**任务仍 success**。client 可注入（`client=` 参数）。L4 建议句同包同调：ok 态返回 `narration.suggestions`，失败保留规则稿 `conclusions.suggestions` |
| ③ FE 渲染 | `svcCoverageModel.ts`：新增 `parseSvcCoverageNarration`（只读消费三态，unknown 拒收）；`SvcOrgCoverageBoard.vue`：仅 `status==="ok"` 渲染 `narrationText` + 建议，否则回退规则稿；禁止补覆盖数字（模型输出经算法侧白名单校验，前端不产数）。ⓘ 已 as-built（DEPTH/BREADTH 四处 ServiceReviewMount + 🧪 mock 由评审层按 registry D4=mock 出），本单未动 |
| ④ handoff + cost | 本文 + registry `task-update-fields`（evidence + cost 四字段） |

**topic-py 未改**（派单写「仅当透传需要时动」）：`gkx_svc_service` `_passthrough_slots` 原样透传 payload，`narration` 键自然下行；snapshot 剥离逻辑不受影响。

## 2. 明确不做（留 SVC-ORG-COVERAGE-STAGE-L01）

G1 四节点真分步 worker、G2 产业过滤指纹、G3 路由正名（org_coverage→models/gap）、G4 RustFS 强制——本单 narrate 挂在现装配路径，与四节点分步解耦，后续迁 worker 时该调用随装配体整体迁移，无需返工。

## 3. 产物清单（本地未推）

| 仓 | 文件 | 动作 |
| --- | --- | --- |
| lumen-algo-py | `lumen_common/prompts/svc/coverage.narrate.v1.txt` | 新增 |
| lumen-algo-py | `lumen_common/algorithms/svcan/narrate_coverage.py` | 新增 |
| lumen-algo-py | `lumen_common/algorithms/svcan/assembly/leaves.py` | +2 行（import + 挂调用） |
| lumen-algo-py | `tests/test_svcan_narrate_coverage.py` | 新增自检 |
| lumen-ui-topic | `src/views/service/svcCoverageModel.ts` | narration 三态解析 + board 字段扩展 |
| lumen-ui-topic | `src/views/service/SvcOrgCoverageBoard.vue` | 合作建议块渲染分支 + 来源角标 |
| lumen-ui-topic | `src/views/service/serviceOrgAnalysis.css` | +叙述段样式 8 行 |

## 4. 验收证据

- **算法侧**：`python3 -m tests.test_svcan_narrate_coverage` → 6 场景 ALL PASS（ok / 越数字拒绝 / 外呼异常 / 无 Key skipped / 空覆盖前置短路 / 事实包白名单不带全量矩阵）；既有回归 `pytest tests/test_svcan_assembly.py tests/test_svcan_engine.py` → **34 passed**。
- **前端侧**：`serviceOrgAnalysis.selfcheck` ok；`pnpm type-check` 干净；`pnpm build` 成功（25.76s）。
- **契约**：narration 三态之外不出现第四态；`skipped` 时业务 UI 与旧版渲染完全一致（规则稿）。

## 5. 偏离说明

1. DoD ③「ⓘ 挂 BREADTH/DEPTH（mock 🧪）」经核实**已 as-built**（评审层既有挂点），本单未重复改动——如实记录，不算缺口。
2. prompt 中「采购建议」改「合作建议」（与页面可见名一致）；「跨界综合服务采购/深度合作」方向短语保持 05.7.1 §6 原文。
3. fallback 语义收紧：叙述被拒时建议句不单独消费（避免 LLM 建议配规则叙述混排），整组退规则稿——比 05.7.1 §5.3 更严格，方向一致。

## 6. 架构合规自检

| 铁律 | 自检 |
| --- | --- |
| 1 算法只在 Python | ✅ LLM 调用全在 lumen-algo-py |
| 2 调用链 | ✅ narration 随装配 payload 原链路下行，无越层、topic-py 零改动 |
| 4 可观测 | ✅ 复用 logger/trace（narrate fallback 打 warn） |
| 润色契约 | ✅ 数字规则锁死+白名单、三态、失败任务仍 success、Java 不碰 Key、prompt 版本化 |
| D9 | ✅ 未新增/篡改指标；ⓘ/🧪 沿用既有评审层 |
| D12 | ✅ 全部 lumen 仓，无 demo 引用 |

## 7. cost

- `actual_tokens`: 约 150k
- `model_used`: glm-5.3-Flash
- `actual_cost`: 约 $1.5
- `cost_warn`: false（< $10 阈值）

## 8. 待人工验收

改动停在两仓本地工作区。验收通过后 push `origin/dev` 并由 coordinator 按 feature 类型推进（integration → pending_test → …）。验收前可用「无 Key 环境」直接复验：FE 渲染与线上现行为完全一致（skipped 路径）。
