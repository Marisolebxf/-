# LUMEN-ENT-EVAL-REPORT-WIRE-L01 · 企业评估报告 — 关键发现接 gapText/diagnosisText（ENT-NARRATE-05 路径 A）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 用户直接派单；status 流转 claimed → in_progress（2026-10-26 18:51，registry 已推远端） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度行一致。最小 diff：报告构造器 +1 个入参组（`diagnosisByCode`/`diagnosisKey`）+ 1 段追稿循环；调用方 +1 处按模式解析；未新增依赖、未新建组件、未做 LLM/prompt（文案真源仍在算法侧）；复用既有 `diagnosisByCode` 映射与规则两句，未用 YAGNI 跳过 D9 追溯与诚实空态 |

## 问题清单

- 派单原文「对齐竞争力 dimensionRows.gapText」：竞争力报告「关键发现」短板行（weakLines）本就消费 `dimensionRows[].gapText`，本次零改动，仅回归自检保护（用例 4）。
- 编排仓 `task-registry.yaml` 本地工作区存在**其他会话**的 evidence 回填（PORTAL-ENT-DEV-SRS-API-L01），按多会话保护铁律未触碰、未提交；本任务状态流转已由 registry MCP 直写远端（远端 `status: in_progress` 已核验）。

## 修改内容

**仓：`lumen-ui-topic`（改动停本地，待人工验收）**

1. `src/components/enterprise/evaluation/evalReportDocument.ts`
   - `EvalReportResultInput`：行级增加 `enterpriseCode?`（缺省回退企业名，兼容旧调用）；输入级增加 `diagnosisByCode?: Record<string, EvalDiagnosisByCode>`（复用 `evalResultMap.ts` 既有类型）与 `diagnosisKey?: 'gapText' | 'diagnosisText'`。
   - `buildEvalReportDocument` ③「关键发现」块：在 FE 规则两句之后、weakLines 之前，按 `rows` 逐企业追加 `${企业名}：${诊断稿}`；稿缺位（skipped / 无该企业键 / 该键无文案）自然不追加 → 规则两句保持，不伪造文案。
2. `src/components/enterprise/evaluation/EvalResultWorkspace.vue`
   - 组装 `result` 时传 `enterpriseCode: row.key`；按模式传入 `diagnosisByCode` + `diagnosisKey`（technology=`gapText` / business=`diagnosisText`；competitiveness 不传，走既有 weakLines 消费）。
3. `scripts/eval-report-findings.test.mts`（新增）
   - 沿用仓内 `node --test` + `scripts/alias-loader.mjs` 惯例，直接 import 真源 `evalReportDocument.ts`（非内联复制逻辑）。

**仓：`gkx-orchestration`（观测补记，改动停本地待随验收提交）**

- `05.3.1-企业技术力评估对比分析.md`：§4 `diagnosis_rows` 行接线提示改「已按 FE 路径 A 接线」；§5.0 报告行 **❌→✅**；§5.5 覆盖表 technology/business 报告列 ❌→✅；§7「同源前提」改「同源成立」；修订记录 v0.5。
- `05.3.2-企业分析LLM落点表.md`：落点表 P1/P2 报告行改「✅ 接线已完成」；§1.1 报告行 ⚠️→✅；§1.2 覆盖位置表补注；**ENT-NARRATE-05 开放项关闭（✅ 已闭合）**；汇总行收敛；v0.9 算法侧「仍待 FE 同批」追记更新；frontmatter 版本 v1.0-draft；修订记录 v1.0。

## 测试结果

- `node --no-warnings --experimental-loader ./scripts/alias-loader.mjs --test scripts/eval-report-findings.test.mts` → **5/5 pass**：
  1. 技术力：`gapText` 进关键发现（规则两句 + 1 诊断稿行），skipped 企业（键无文案）不伪造；
  2. 商业力：`diagnosisText` 进关键发现；
  3. skipped（诊断稿空）：仅 FE 规则两句（领先者/分差）；
  4. 竞争力回归：weakLines（`dimensionRows.gapText`）不破坏（规则两句 + weakLines 1 行）；
  5. 诚实空态保持：`result=null` 只出 `empty-state` 块。
- `pnpm type-check`（vue-tsc --build）✅ 0 错误
- `npx eslint`（3 个触碰文件）✅ 0 问题；`pnpm build` ✅ built in 20.4s
- 相邻既有自检无回归：`schema-field-whitelist` + `analysis-task-gate` → 17/17 pass
- `USE_MOCK=false` 合规：本次零 fixture 填充——报告只消费 `mapEvalResultPayload` 映射后的真实任务快照；mock 模式不产生 `diagnosisByCode` 时自然走规则句（与现状一致）

## 遗留风险

- 报告「关键发现」的诊断稿行当前**逐企业平铺**（50 家上限时 bullet 数 = 2 + N + weakLines）；文档密度可接受（05.3.2 §1.2 事实包口径 <8K token），如走查嫌长可再评估折叠，不在本单范围。
- `EvalModeResultBody.vue` 结果页尾列的 FE 兜底句（「距领先对象 X 分…」）保持不动（05.3.1 §4 明确「不删」）；润色 skipped 时结果页与报告均为规则稿，**同源退化为同规则**，语义一致。

## CI/CD（必填）

- 分支：`dev`（lumen-ui-topic）
- commit：**未 commit**——按 lumen-ui-topic AGENTS.md 人工验收闸门（2026-10-20 用户裁定），改动停本地工作区，待监管人 human:徐滕强 走查通过后再推
- pipeline URL / ID：N/A（未推送；验收后 push 触发 `frontend:build` → deploy:k8s → 30892）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：本地全量验证见「测试结果」；验收路径 `企业评估 → 任一模式跑任务 → 查看报告 → 关键发现块`

## 可观测性（建议）

- 本任务为纯 FE 文档组装，无新增埋点点位；报告生成链路 OTEL 埋点已在既有任务流（enterpriseEvalStream）覆盖。

## 涉及文件

- `repos/lumen-ui-topic`：
  - `src/components/enterprise/evaluation/evalReportDocument.ts`（改）
  - `src/components/enterprise/evaluation/EvalResultWorkspace.vue`（改）
  - `scripts/eval-report-findings.test.mts`（新增）
- `gkx-orchestration`：
  - `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.1-企业技术力评估对比分析.md`（改）
  - `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.2-企业分析LLM落点表.md`（改）

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| 调用链（前端只经 Java 读快照） | ✅ 报告只消费 `resultPayload` 快照映射，不新增后端调用 |
| 算法只在 Python / 不做 LLM、不写 prompt | ✅ 纯 FE 消费；文案真源在算法侧 `narrate_eval` |
| D9 指标追溯 | ✅ 未动 KPI ⓘ / metric_id；诚实空态与 skipped 退规则句均保持，不伪闭合 |
| D12 demo↔lumen 隔离 | ✅ 只改 `lumen-ui-topic`，未读未引 demo 仓 |
| git 策略 | ✅ 停本地等人工验收；未 force push；registry 变更经 MCP 直写远端 |
