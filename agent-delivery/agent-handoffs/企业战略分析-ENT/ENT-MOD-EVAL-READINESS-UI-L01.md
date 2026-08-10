# ENT-MOD-EVAL-READINESS-UI-L01 —— demo-ui-topic 四维就绪度角标落地

> **任务**：ENT-MOD-EVAL-READINESS-UI-L01
> **执行**：agent:frontend-agent（监管 human:淮政玮）
> **日期**：2026-08-01
> **前置输入**：D9-READINESS-MODEL-L01（四维模型草案 + ENT-EVAL 矩阵，同会话产出）
> **状态**：✅ 交付（review 待验收）

---

## 1. 范围与实现

| 项 | 实现 |
|----|------|
| 就绪度数据源 | 新增 `src/app/mock/enterprise/readinessSeed.ts` —— `metric-readiness-matrix-ENT-EVAL.yaml` 的 FE 只读镜像（13 指标 × D1~D4）；Wave 1 改读 `/metrics/v1/catalog`，UI 不变 |
| 缺口文案接真源 | 新增 `src/app/mock/enterprise/entEvalGapCatalog.ts` —— `ENT-EVAL-data-gap-catalog.yaml` v1 的 FE 镜像（7 条，长文案均 >80 字走 Popover）；FE 不再自编 ⚠️ 文案 |
| MetricSpecCard | ① 卡内新增「就绪度」四行区块（定义/结构/源映射/接入，状态点按草案 §3.3 图标字典）② D1 missing（未登记指标）入口态由灰 ⓘ 改为红 `IconQuestionCircle`（草案 §3.2） |
| 新角标组件 | `SchemaGapBadge`（`IconStorage`，D2 partial 橙 / missing 红，责任方=项目内）；`IngestingBadge`（`IconSync` 蓝，Tooltip 为五阶段清单，不用百分比）；两者自带 ReviewOnly 自闸，无数据/无缺陷时自隐藏 |
| 页面挂接 | 评估页 F07「内部指标元数据」行：ⓘ → SchemaGapBadge → PendingBadge（文案取 gap catalog）→ IngestingBadge，排列顺序符合草案 §3.2 |
| metricSeed | 核对后未强制改写：demo 侧 13 条 EVAL 条目为 v1.2 定义评审后的精化版（如「缺失指标不计为零或短板」），与 cfg seed 差异属展示名/口径精化而非血缘冲突；血缘性差异（source_tables 占位）已在就绪度区块以矩阵数据补足。命名统一待 Q009（ENT vs E1）一并处理 |

## 2. 产物清单

- demo-ui-topic commit `247cb8b`（origin/dev）：8 文件 +618/−6
  - 新增：`readinessSeed.ts` / `entEvalGapCatalog.ts` / `SchemaGapBadge.tsx` / `IngestingBadge.tsx` / `tests/enterprise-eval-readiness.test.mjs`
  - 修改：`MetricSpecCard.tsx` / `EnterpriseEvaluationPage.tsx` / `components/common/index.ts`
- 本 handoff：`agent-delivery/agent-handoffs/ENT-MOD-EVAL-READINESS-UI-L01.md`

## 3. 验收证据

| 项 | 结果 |
|----|------|
| 新契约测试 `enterprise-eval-readiness.test.mjs` | ✅ 通过（13 指标精确覆盖、枚举合法、provisional 诚实性、镜像与编排仓真源弱一致、组件自闸、页面挂接） |
| 既有测试回归 | ✅ 与改动前基线完全一致：通过集不变；预存失败集不变（playwright/fetch 环境类 + 9 项经 stash 基线验证为预存，见 §5） |
| `review-marker-self-gating` | ✅ 通过（新组件同样 ReviewOnly 自闸） |
| `design:check` | ✅ 通过 |
| `vite build` | ✅ 成功（1m35s；chunk 体积告警为预存） |
| 业务态零变化 | ✅ 所有新增元素均在 ReviewOnly 内；v12-pointer 业务态防泄漏契约文件未放宽 |
| CI/CD | 按 pipeline_waiver v2：code_complete + git_push + handoff 达成 |

## 4. 偏离说明

1. **metricSeed 未做整文替换**（DoD 第 1 条按「血缘一致」达成而非「逐字一致」）：demo 侧定义为 v1.2 评审精化版，逐字覆盖会回退已评审语义；血缘信息差额由就绪度区块（矩阵镜像）补足。命名（Q009）与字段级回灌建议由 data-agent 在 cfg seed 侧统一收口。
2. 新角标未注册新的 review mount id：Wireframe-ENT-EVAL 的 18 个 mount 契约保持不动，避免与覆盖矩阵校验冲突；如评审需要定点索引可后续在 wireframe + coverage 同步登记。
3. demo-ui-topic 实际分支为 `dev`（非登记时假定的 main），已按仓库现状推 `origin/dev`。

## 5. 预存失败清单（与本任务无关，建议另立修复任务）

- playwright 缺依赖 / dev server fetch 失败：全部 `*-pointer` 测试（本机未装 playwright；`enterprise-evaluation-v12-pointer` 还含他人机器硬编码路径 `E:\Users\ying\...`）
- stash 基线复验为预存（改动前后失败一致）：`enterprise-evaluation-v12-contract`（model 演进后 gap 行断言过期）、`enterprise-evaluation-model`、`enterprise-evaluation-definition`（IA v1.10 基线断言）、`enterprise-review-mount-contract`（编排仓缺 `交付覆盖/ENT-RISK/implementation-coverage.yaml`）、`enterprise-evaluation-result-model`、`enterprise-evaluation-processing-navigation`、`enterprise-risk-insight-definition`、`enterprise-key-analysis-definition`

## 6. 架构合规自检（公约 §2 十一条）

1 算法只在 Python ✅（纯前端）· 2 调用链 ✅（无新请求，读本地 mock 镜像）· 3 图谱 ✅ N/A · 4 可观测 ✅（沿用 observability track；未新增埋点）· 5 CI/CD ✅（waiver v2）· 6 demo2 只读 merge ✅（未涉 lumen）· 7 共享聚合核心 ✅（Wave 1 消费点 /metrics/v1/catalog）· 8 数据策略 ✅（Mock 如实标注）· 9 D8 ✅（全 Arco Icon、主色 #165DFF、状态色按 token）· 10 D9 ✅（文案真源 catalog、矩阵只读消费、不伪闭合）· 11 D10 ✅（Tooltip/Popover 沿用既有交互契约，键盘可达属性保留）

## 7. Cost（registry 已回填）

| 字段 | 值 |
|------|-----|
| estimated_tokens | 200_000 |
| actual_tokens | 150_000 |
| model_used | claude-fable-5 |
| actual_cost | 0.90 |
| cost_warn | green |
