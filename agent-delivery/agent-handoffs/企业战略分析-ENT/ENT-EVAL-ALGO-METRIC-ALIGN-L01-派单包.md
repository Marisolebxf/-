# 派单包：ENT-EVAL-ALGO-METRIC-ALIGN-L01

- **派单方**：coordinator（human:徐滕强）
- **时间**：2026-07-20
- **执行人**：human:唐绍祖（`algorithm-agent`）
- **监管人**：human:唐绍祖
- **Sprint**：2026-W30
- **Epic**：E-ENT-SCRUM-PDR

## 1. 背景

`demo-ui-topic` 企业评估模块（技术力 / 商业力 / 综合竞争力）当前指标与默认权重在 `enterpriseEvaluationModel.ts` 中为 **UI 自洽 Mock**，与算法真源不一致：

| 侧 | 真源 / 参照 |
|---|---|
| 算法权重 | `demo-algo-ent-analysis/conf/settings.yaml` → `tech_power_weights` / `biz_power_weights`；A1 综合评分域权重见 `entan/realdata/a1_score.py` 与 entanHelp `score` Tab |
| 指标 8 件套 | `agent-delivery/metrics/cfg_metric-ENT-seed.yaml` |
| 算法说明与维度 | `demo-ui-system-test/src/views/entan/components/entanHelp.ts`（`tech` / `biz` / `score` Tab） |
| API 权重查询 | `/entan/v1/eval/weights?model=tech|biz`（`demo-ui-system-test` 已接） |

需在 **不改动 demo-ui-topic 其他模块** 前提下，将企业评估的 **指标清单 + 默认权重 + metric_id** 与上述算法定义对齐。

## 2. 范围（严格）

### 2.1 允许修改（demo-ui-topic）

仅 `src/app/pages/enterprise/` 下 **企业评估** 相关文件，例如：

- `enterpriseEvaluationModel.ts`（**主战场**：`EVALUATION_MODES` 三模式 indicators / 默认 weight）
- `enterpriseEvaluationResultModel.ts`（若雷达/结果维度需与算法五维/六维一致）
- `enterpriseEvaluationTrace.tsx`（仅 metric_id / 口径说明同步，不改页面结构）
- 其他 `enterpriseEvaluation*.ts(x)` **仅当**指标对齐必需且 diff 可证明无 UI 行为蔓延

### 2.2 禁止修改

- 企业 **检索 / 对比篮 / 画像 / 风险 / 引育 / 态势** 等页面与路由
- `src/app/pages/development/`、`src/app/mock/`（非 eval 专用）、全局布局/权限/导航
- `demo-ui-system-test`、`demo-algo-ent-analysis` **除非**需补 `/eval/weights` 文档或只读常量导出（优先只读参照，少改 algo 仓）

### 2.3 三种评估模式对齐期望

| 模式 | acceptanceUnit | 对齐参照 |
|---|---|---|
| 技术力 `technology` | E-23 | entan **tech** 五维：talent / innovation / transfer / cooperation / investment；权重 = `settings.yaml#tech_power_weights`（和为 1，UI 展示可 ×100 整数） |
| 商业力 `business` | E-24 | entan **biz** 六维：market / product / brand / cooperation / chain_coverage / chain_keynode；权重 = `settings.yaml#biz_power_weights` |
| 综合竞争力 `competitiveness` | E-30 | entan **score** A1：innov / operate / growth 三域；默认 **0.40 / 0.40 / 0.20**（与 entanHelp + a1_score 一致）；指标 metric_id 对齐 `cfg_metric-ENT-seed` |

**默认权重铁律**：模板初始权重以 **算法定义** 为准；用户自定义权重交互保留，但默认值必须与算法一致。

## 3. 架构铁律（7 条自检）

1. 算法只在 Python — 本任务 **不改 Java**；topic 侧仅同步指标/权重/catalog
2. 调用链 — 本期仍为 demo Mock 算分；若引用 entan API 仅只读 weights/metrics，不越层写 ADS
3. 图谱 NebulaGraph — N/A
4. 可观测性 — N/A（demo-ui-topic）
5. CI — push `demo-ui-topic` `origin/main` 后部署站可见
6. commit 标注 `[human:唐绍祖]` 或 `[agent:algorithm-agent]`
7. demo2 不 merge lumen — 仅 `demo-ui-topic`

## 4. Definition of Done

1. **对齐矩阵**（handoff §1）：三模式 × {indicator key, 中文名, metric_id, 默认权重, 算法源文件/字段, entanHelp Tab} 对照表
2. `EVALUATION_MODES` 更新后：`createDefaultEvaluationWeights()` 与算法默认一致；`metricId` 与 seed / entanHelp 一致
3. `enterpriseEvaluationResultModel.ts` 中 `RESULT_DIMENSIONS`（若有）与 tech/biz 维度命名一致或 handoff 说明保留 UI 聚合层映射
4. `npm run build`（或项目等效 type-check/build）通过
5. **范围证明**：`git diff --stat` 仅含 §2.1 允许路径（handoff 贴输出）
6. handoff：`agent-handoffs/企业战略分析-ENT/ENT-EVAL-ALGO-METRIC-ALIGN-L01.md` + 架构合规 7 条 + cost 四字段
7. 不修改 demo-ui-topic 其他模块（监管人 spot-check）

## 5. 参考路径

| 用途 | 路径 |
|---|---|
| Topic 评估模型 | `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationModel.ts` |
| 产品评估 IA | `agent-handoffs/产品整体定义/E-23_E-24_E-30-企业评估/IA-ENT-EVAL.md` |
| 算法权重 | `repos/demo-algo-ent-analysis/conf/settings.yaml` |
| 模型注册 | `repos/demo-algo-ent-analysis/conf/cfg_model_registry.yaml` |
| system-test 说明 | `repos/demo-ui-system-test/src/views/entan/components/entanHelp.ts` |
| 指标 seed | `agent-delivery/metrics/cfg_metric-ENT-seed.yaml` |

## 6. 派单话术（复制给执行人）

```text
/goal ENT-EVAL-ALGO-METRIC-ALIGN-L01

将 demo-ui-topic 企业评估三模式（技术力/商业力/综合竞争力）的指标与默认权重，
与 demo-algo-ent-analysis + demo-ui-system-test /entan 算法定义对齐；
默认权重以 settings.yaml / A1 域权重为准。
严格限制修改范围在 enterpriseEvaluation* 文件，禁止动检索/对比篮/画像等其他模块。

必读：本派单包 + enterpriseEvaluationModel.ts + entanHelp.ts + cfg_metric-ENT-seed.yaml
handoff：agent-handoffs/企业战略分析-ENT/ENT-EVAL-ALGO-METRIC-ALIGN-L01.md
```
