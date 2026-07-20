# ENT-EVAL Demo v1.6 验证报告

> 状态：`delivery_stage: v1_hifi_round1`；当前四件套包 v1.6 已完成 Demo 落位、自动化、生产构建、真实指针与双模式验证 · 2026-07-20

## 本轮修订结果

- 原始需求只取当前 Bid；产品执行只取 `E-23_E-24_E-30-企业评估` 当前 IA / TRACE / USM / Wireframe；SRS 只保留 §6 / §7 约束。
- 数据覆盖与可信度预检已在四件套固化为产品解释：前端本地校验目标不超过 100ms；对象、模式或指标变化防抖 300–500ms 后由 Java 聚合后端执行正式预检；普通响应目标 1–3s、P95 不超过 5s，超过 300ms 显示稳定加载态，超过 5s 显示“仍在预检”及重试入口。
- 商业力配置沿用已落位的确定性行业模拟预览：未改动配置时切换行业会同时改变 4 个可用指标中的 3 项选中组合及其整数权重，未选中的可用指标权重为 0；已改动时必须在“应用行业配置 / 保留自定义配置 / 取消”三种结果中明确选择，不静默覆盖。
- 配置视图只在三模式页签上方渲染一个共享评估对象区；切换技术力、商业力或综合竞争力时保留同一对象集合，并按技术力 / 商业力至少 2 家、综合竞争力至少 1 家重新校验。
- 业务模式仅显示“行业模拟预览 / 非正式行业评价标准”等用户可理解说明；评审模式额外显示 Q014、K-O7、临时处理、关闭条件及 `product_interpretation`，内部治理字段不泄漏到业务模式。
- F07 在指标元数据缺失时显示结构化真实缺失态，不伪造正式指标元数据；内部评审模式支持 hover 预览、点击固定及 Enter 切换。
- 技术力仍为 Bid 五维雷达；综合竞争力仍为技术 / 市场 / 组织三维；未登记指标保持不可用、权重 0、不参与评分。
- 经本轮产品确认，技术模式将原“技术指标诊断”和通用“指标明细与综合差距”合并为单一“技术指标与差距诊断”：同表呈现技术力综合得分、原始技术指标、数据可信度、领先差距及优势短板，趋势与建议缺失态归入该模块；技术模式不再重复渲染通用企业明细表。该归并为 `product_interpretation`，不冒充 Bid 原文。
- 综合竞争力模式按 v1.6 将“优势与短板诊断”和“指标明细与综合差距”合并为单一“综合竞争力与差距诊断”：单企展示当前企业、综合得分、可信度、对象集均值/领先值与优势短板；双企展示双方综合得分、可信度、维度差值与结论；右侧综合竞争力排名仍为唯一排名表达。
- 当前 8 个 Demo 覆盖项统一采用保守数据治理事实：`provenance_type=simulated_fixture`、`mapping_status=pending_source`、`availability=partial`、`quality_status=unchecked`、`freshness_status=unknown`、`degradation_status=degraded`；未宣称真实来源、当前批次或质量通过。

## 验收单元与交付等级证据

| 验收单元 | 当前等级 | DEMO 登记 | 本轮证据 | 主要缺口 |
| --- | --- | --- | --- | --- |
| E-23 技术力评估 | `DEMO` | `agent-delivery/demo-fallback-registry.yaml#DEMO-005` | v1.6 验证待补 | Q014、正式算法、ADS |
| E-24 商业力评估 | `DEMO` | `agent-delivery/demo-fallback-registry.yaml#DEMO-006` | v1.6 验证待补 | Q014、K-O7、行业维度映射、正式算法、ADS |
| E-30 综合竞争力评估 | `DEMO` | `agent-delivery/demo-fallback-registry.yaml#DEMO-007` | `evidence/result-competitiveness-v16.png` 与 `evidence/dual-mode-dom-v16.json` | Q014、正式算法、ADS、正式报告服务 |

- `implementation-coverage.yaml` 顶层只定义 E-23、E-24、E-30 三个唯一验收单元合同；8 个覆盖项通过 YAML anchor 形成 18 条 item-to-unit 关联，均为标量 `acceptance_unit_id`，没有复合验收单元 ID。
- TECH 只归 E-23，BIZ 只归 E-24，COMP 只归 E-30；OBJ、QUALITY、RESULT、REPORT、HISTORY 分别覆盖 E-23 / E-24 / E-30。
- 每个验收单元的 `planned_tier` 与 `delivery_tier` 均为 `DEMO`；本轮不认领 `INTEG` 或 `FULL`。

## 自动化验证（已通过）

后续在 `repos/demo-ui-topic` 运行：

```bash
node --experimental-strip-types tests/enterprise-evaluation-definition.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-model.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-result-model.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-task-store.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-template-store.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-report.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-v12-contract.test.mjs
node --experimental-strip-types tests/enterprise-review-mount-contract.test.mjs
node --experimental-strip-types tests/review-marker-self-gating.test.mjs
npm run design:check
npm run build
```

- 上述 10 项企业评估契约、`design:check` 与生产构建均通过；构建仅保留既有 chunk-size 警告。
- 复合控件标签审计命令通过：

```bash
node /Users/ying/.codex/skills/gkx-ui-design-standards/scripts/check-composite-labels.mjs \
  src/app/pages/enterprise/EnterpriseEvaluationPage.tsx \
  src/app/pages/enterprise/EnterpriseEvaluationResultWorkspace.tsx \
  src/app/components/common/MetricSpecCard.tsx
```

结果：`Composite label audit passed (3 files).`

## 真实指针与双模式验证（已通过）

CDP 前置失败检查与正式验证命令：

```bash
node tests/enterprise-evaluation-v12-pointer.test.mjs
ENT_EVAL_CDP_PORT=9231 node tests/enterprise-evaluation-v12-pointer.test.mjs
```

- 隔离 Chrome 通过 CDP 真实坐标点击验证单企 / 双企切换，并生成 `result-competitiveness-v16.png` 与 `dual-mode-dom-v16.json`。
- v1.6 评审模式已验证的精确挂点集合：

| 路由 / 状态 | 精确集合 |
| --- | --- |
| configuration | `ENT-EVAL-F05-PAGE-TITLE, ENT-EVAL-F01-INDUSTRY-PREVIEW-NOTE, ENT-EVAL-F01-CONFIG-TITLE, ENT-EVAL-F01-QUALITY-TITLE` |
| metricDrawer | `ENT-EVAL-F05-PAGE-TITLE, ENT-EVAL-F01-INDUSTRY-PREVIEW-NOTE, ENT-EVAL-F01-CONFIG-TITLE, ENT-EVAL-F01-QUALITY-TITLE, ENT-EVAL-F07-METRIC-SPEC` |
| processing | `ENT-EVAL-F05-PAGE-TITLE, ENT-EVAL-F06-PROCESS-TITLE` |
| history | `ENT-EVAL-F05-PAGE-TITLE` |
| technologyResult | `ENT-EVAL-F05-PAGE-TITLE, ENT-EVAL-F02-RESULT-TITLE, ENT-EVAL-F02-TECH-RADAR-TITLE, ENT-EVAL-F02-TECH-RANKING-TITLE, ENT-EVAL-F02-TECH-DIAGNOSIS-TITLE, ENT-EVAL-F02-REPORT-TITLE` |
| businessResult | `ENT-EVAL-F05-PAGE-TITLE, ENT-EVAL-F02-RESULT-TITLE, ENT-EVAL-F02-BIZ-METRICS-TITLE, ENT-EVAL-F02-BIZ-RANKING-TITLE, ENT-EVAL-F02-BIZ-DIAGNOSIS-TITLE, ENT-EVAL-F02-REPORT-TITLE` |
| competitivenessResult | `ENT-EVAL-F05-PAGE-TITLE, ENT-EVAL-F02-RESULT-TITLE, ENT-EVAL-F02-COMP-RADAR-TITLE, ENT-EVAL-F02-COMP-RANKING-TITLE, ENT-EVAL-F02-COMP-DIAGNOSIS-TITLE, ENT-EVAL-F02-REPORT-TITLE` |
| reportModal | `ENT-EVAL-F05-PAGE-TITLE, ENT-EVAL-F02-RESULT-TITLE, ENT-EVAL-F02-COMP-RADAR-TITLE, ENT-EVAL-F02-COMP-RANKING-TITLE, ENT-EVAL-F02-COMP-DIAGNOSIS-TITLE, ENT-EVAL-F02-REPORT-TITLE, ENT-EVAL-F04-REPORT-TITLE` |

`competitivenessResultBeforeReport` 与 `competitivenessResult` 应为同一 6 项集合。

- 业务模式九个状态均为零评审挂点；F07 payload、复合控件、单企 / 双企切换与报告 Modal 均通过。
- 历史截图和旧指纹只作参考，不作为 v1.6 验收证据。

## 证据与指纹

证据指纹只覆盖以下精确集合，不包含历史截图：

- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/industry-preview-business-v16.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/industry-preview-review-v16.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/metric-gap-review-v12.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/result-technology-v13.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/result-business-v12.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/result-competitiveness-v16.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/dual-mode-dom-v16.json`
- v1.6 三指纹已重算：definition `f1f629f9...`、implementation `c1f06e76...`、evidence `f922f900...`；`verified_status_valid: true`。

Implementation 指纹输入为 coverage 中 `implementation_files` 的去重并集，加 11 个相关测试；精确清单如下，不包含 coverage 文件自身：

```text
repos/demo-ui-topic/src/app/components/common/MetricSpecCard.tsx
repos/demo-ui-topic/src/app/components/common/MockBadge.tsx
repos/demo-ui-topic/src/app/components/common/PendingBadge.tsx
repos/demo-ui-topic/src/app/components/common/ReviewMetricBadges.tsx
repos/demo-ui-topic/src/app/components/common/ReviewTrace.tsx
repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx
repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseEvaluationPage.tsx
repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseEvaluationResultWorkspace.tsx
repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseOutputTaskModal.tsx
repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationModel.ts
repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationReport.ts
repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationResultModel.ts
repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationTasks.ts
repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationTrace.tsx
repos/demo-ui-topic/src/app/pages/personal/PersonalAssetsPage.tsx
repos/demo-ui-topic/tests/enterprise-evaluation-definition.test.mjs
repos/demo-ui-topic/tests/enterprise-evaluation-model.test.mjs
repos/demo-ui-topic/tests/enterprise-evaluation-report.test.mjs
repos/demo-ui-topic/tests/enterprise-evaluation-result-model.test.mjs
repos/demo-ui-topic/tests/enterprise-evaluation-task-store.test.mjs
repos/demo-ui-topic/tests/enterprise-evaluation-template-store.test.mjs
repos/demo-ui-topic/tests/enterprise-evaluation-v12-contract.test.mjs
repos/demo-ui-topic/tests/enterprise-evaluation-v12-pointer.test.mjs
repos/demo-ui-topic/tests/enterprise-review-mount-contract.test.mjs
repos/demo-ui-topic/tests/enterprise-compare-basket-definition.test.mjs
repos/demo-ui-topic/tests/review-marker-self-gating.test.mjs
```

## 边界

- 本文记录 `v1_hifi_round1` Demo 层 8 个覆盖项与 18 个评审挂点的 v1.6 有效验证证据；交付等级仍为 `DEMO`。
- Q014 默认指标与权重仍待甲方确认；K-O7 商业指标数据、行业维度映射、正式算法、ADS 数据、正式报告服务仍是后续依赖。
- Gate 1 / PDR、V1-FINAL、V2 lumen、INTEG、FULL 均未认领完成。
- 当前 Demo 与四件套准备提交并推送；部署完成后以线上资源指纹补充最终证明，registry 状态未修改。
