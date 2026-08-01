# ENT-MOD-ENT-READINESS-UI-L02 · Handoff

- **任务**：demo-ui-topic 就绪度镜像补全（28 缺口）+ 存量脱钩点收敛 + 防漏契约测试
- **执行**：agent:frontend-agent ／ 监管 human:淮政玮（claim_type: pull）
- **日期**：2026-08-01
- **仓库**：demo-ui-topic（push origin/dev）；上游依赖 ENT-READINESS-MATRIX-ENT-L02（矩阵已 75 条，status=review）
- **范围铁律**：只动企业维度相关文件（企业分析 + 企业总览各 tab 共享的 mock/组件/页面/测试），其它维度零变化

## 1. FE 镜像增量（readinessSeed.ts）

与矩阵 L02 增量一一对应，共 **+26 条**（32 → 58 条），三段：

| 段 | 条数 | D1 | D2 | D3 | D4 |
|---|---|---|---|---|---|
| L01 矩阵已有、L01 镜像遗漏补录 | 4（M_ENT_INDUSTRY_MATCH_SCORE / M_ENT_POLICY_MATCH_SCORE / M_ENT_GROWTH_POTENTIAL / M_ENT_STAR_ENTERPRISE_COUNT） | draft（Q015/Q037） | pending | 按矩阵（full/partial） | mock |
| ENT-OVERVIEW（矩阵 L02 补录段） | 11 | 按 seed（aligned/draft） | pending | **pending_ods**（无 gap catalog 依据，8/20 ODS 稳定后 GDF 统一评估） | mock |
| ENT-DEMO-UNREGISTERED（矩阵 L02 补录段） | 11 | **missing**（未入 cfg_metric-ENT-seed，待王惠正式化） | n/a | n/a | n/a（stages 全 n/a） |

- 类型扩展：`SchemaStatus` / `SourceMappingStatus` / `IngestionStatus` 增加 `'n/a'`；新增 `NA_STAGES` / `READINESS_UNREGISTERED` 常量承接 policy §2.3.1「D1 missing → D2~D4 = n/a」。
- **别名表 METRIC_ID_ALIASES：1 → 9 条**（镜像矩阵头部 demo_metric_id_aliases，禁止 FE 单方面增删）：

| demo 本地 ID | 矩阵正式 ID |
|---|---|
| M_ENT_DOMAIN_BREADTH | M_ENT_DOMAIN_COVERAGE_BREADTH（L01 存量） |
| M_ENT_SZ_TOTAL_COUNT | M_ENT_SZ_COUNT |
| M_ENT_NEW_COUNT | M_ENT_NEW_COUNT_Y（⚠️ demo「近 12 月」vs seed 按年，窗口差异已在矩阵 d1_note 登记） |
| M_ENT_RD_INVEST_AVG | M_ENT_AVG_RD_INVESTMENT |
| M_ENT_CLUSTER_INDEX | M_ENT_AGGLOMERATION_INDEX |
| M_ENT_DOMAIN_DEPTH | M_ENT_DOMAIN_COVERAGE_DEPTH |
| M_ENT_DOMAIN_DIVERSITY | M_ENT_DIVERSIFICATION_INDEX |
| M_ENT_TECH_SCORE | M_ENT_TECH_POWER_SCORE |
| M_ENT_BUSINESS_SCORE | M_ENT_BUSINESS_POWER_SCORE |

## 2. entGapCatalog.ts（gap 长文案镜像）

- **零新增**：矩阵 L02 新增 22 条均无 gap catalog 新依据（OVERVIEW 段 D3=pending_ods、未注册段 n/a），按「不编造 pendingRef/pendingHint」铁律不补条目。
- 收敛：本地私有 `GAP_ID_ALIASES` 删除，改统一复用 `readinessSeed.METRIC_ID_ALIASES`（别名单一真源，避免两份表漂移）。

## 3. 存量脱钩点收敛（3 处）

1. **EnterpriseKeyAnalysisPage.tsx**：删内联 `TYPE_METRIC_META` / `DOMAIN_COVERAGE_METRIC_META`，`MetricSpecCard` 改 `metricId="M_ENT_TYPE_COUNT"` / `"M_ENT_DOMAIN_COVERAGE_COUNT"` 走 metricSeed（seed 已有正式 8 件套条目，无需补登记；页面内联版为 fixture 措辞旧稿，正式语义以 seed=cfg_metric-ENT-seed 镜像为准）。
2. **EnterpriseKeyAnalysisV2Page.tsx**：同上（`TYPE_METRIC_META` / `DOMAIN_METRIC_META` 删除）。
3. **EnterpriseRiskInsightPage.tsx**：「数据与权限预检」区硬编码 Q017/Q018 的 PendingBadge 改 `getEntGap` 驱动（supply-chain → M_ENT_SUPPLIER_COUNT、pain-points → M_ENT_PAINPOINT_COUNT，与配置区说明语义一致），pendingRef/hint 全部来自 gap catalog 镜像。

## 4. 组件配套修正（就绪度语义）

- **SchemaGapBadge**：渲染守卫由「非 ready 即渲染」改为「仅 partial / missing 渲染」——`pending`（未评估）与 `n/a`（未登记）属"未知/不适用"而非"已知缺陷"，只在 ⓘ 卡就绪度区块表达，不在入口层挂缺陷角标（policy §2.3.3 语义）。
- **MetricSpecCard** 就绪度四行：新增 `n/a` 态（`IconMinusCircle` 灰 + 「不适用（指标未登记，正式注册后评估）」）；D1 missing 行文案改为「正式指标库未登记，待正式注册」并支持治理引用显示；D3 `pending_ods` 行追加 gap 说明。

## 5. openItemCatalog.ts

- 新增 **Q048**（明星企业候选名单、发布准入与基础量化指标口径）、**Q049**（深圳企业统计正式 metric_id / ADS 与规模分级口径）——标题镜像 `客户决策清单跟踪表.md` 第 134/135 行，未自编。

## 6. 防漏契约测试（tests/enterprise-eval-readiness.test.mjs）

- 覆盖断言扩展为 EVAL 13 + 扩展 19 + 补镜像 4 + OVERVIEW 11 + 未注册 11 = **58 条**，与矩阵真源逐条比对（含别名 9 条与矩阵头部一一比对）。
- 诚实性断言：D1 missing → D2~D4 全 n/a；OVERVIEW 段 D3 只能 pending_ods；已登记段 D2 一律 pending。
- **§8 防漏硬约束**：递归扫描 `src/app/pages/enterprise` + `src/app/pages/development` 全部 `metricId[=:]` 引用（实测 40 个去重 M_ENT_*），每个必须 `getMetricReadiness` 命中（含别名解析）；例外白名单 `READINESS_SCAN_WHITELIST` 当前为空，新增例外须注明原因。
- §5b 脱钩点收敛断言：两 KeyAnalysis 页禁止 `MetricSpecCard meta=`；RiskInsight 禁止硬编码 `pendingRef="Q017/Q018"`，必须 `getEntGap` 驱动。
- `tests/enterprise-risk-insight-definition.test.mjs` 同步更新（原断言锁定旧硬编码形式）。

## 7. 验证证据

```
node --experimental-strip-types tests/enterprise-eval-readiness.test.mjs        → passed
node --experimental-strip-types tests/enterprise-risk-insight-definition.test.mjs → passed
enterprise-key-analysis-definition / -clean-rebuild / -drawer-handoff /
enterprise-overview-e33-e35 / enterprise-region-control-consistency /
enterprise-risk-insight-report / review-marker-self-gating                       → passed
```

- lint（IDE 诊断）：0 错误。本机无 npm/pnpm，未做本地构建（环境约束，CI 兜底）。
- **存量失败（与本任务无关，未修）**：`*-pointer` 系列、`enterprise-review-mount-contract`（依赖编排仓缺失文件，任务单已知）；另实测 `enterprise-evaluation-definition` / `enterprise-evaluation-v12-contract` 亦为存量失败——已用 `git stash` 移除本任务全部改动后复跑，失败内容完全相同（断言 EnterpriseEvaluationPage 的 ReviewOnly 标题结构与 F02/F09/F10 挂载点清单，该文件本任务未触碰），建议另行建单排查。

## 8. 开放项

1. 11 个 d1=missing 指标待王惠正式化入 cfg_metric-ENT-seed（清单见矩阵 ENT-DEMO-UNREGISTERED 段与 MATRIX-L02 handoff §5）；正式化后 FE 镜像随矩阵刷新升级。
2. M_ENT_NEW_COUNT 别名的「近 12 月 vs 按年」窗口差异待王惠确认（矩阵 d1_note 已登记）。
3. Q048/Q049 闭合后，明星/深圳段指标（M_ENT_STAR_PATENT_COUNT / M_ENT_STAR_RD_RATIO / M_ENT_STATE_OWNED_COUNT 等）按甲方口径正式注册并复评四维。
4. Wave 1 就绪度改读 Java `/metrics/v1/catalog` 后，readinessSeed / entGapCatalog / openItemCatalog 三个 FE 镜像整体退役（UI 不变）。

## 9. 架构合规自检（公约 §2 十一条）

1. 算法只在 Python：✅ 不涉及
2. 调用链：✅ 纯前端 mock 层，未越层
3. 图谱 NebulaGraph：✅ 不涉及
4. 可观测性：✅ 未改动 observability 配置
5. CI/CD：✅ push origin/dev 触发既有流水线
6. demo2 只读 merge：✅ 仅 demo-ui-topic，未 merge 进 lumen
7. 共享聚合核心：✅ 不涉及
8. 数据策略：✅ Mock 数据 + 就绪度如实标注
9. D8 前端规范：✅ 全部 Arco Icon（IconMinusCircle 新增 n/a 态），禁 emoji 表状态
10. D9 数据血缘：✅ FE 只读消费矩阵镜像，未自编状态/文案；防漏测试保证每个 metricId 有就绪度
11. D10 交互规范：✅ 角标 ReviewOnly 自闸，评审模式关闭零泄漏（守卫在组件内部）

## 10. Cost

- actual_tokens: 420_000（估）
- model_used: claude-fable-5
- actual_cost: $2.4（估，< $10 无需复盘）
- cost_warn: green
