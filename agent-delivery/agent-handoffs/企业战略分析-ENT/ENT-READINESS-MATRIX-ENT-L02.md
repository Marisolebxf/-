# ENT-READINESS-MATRIX-ENT-L02 — 就绪度矩阵补录 demo 页面引用缺口（53 → 75 条 + 别名归一）

> 状态：🔍 review（2026-08-01）· agent:data-agent · 监管 human:淮政玮 · claim_type: pull
> 依赖：ENT-READINESS-MATRIX-ENT-L01（企业全域矩阵真源）
> 真源：`agent-delivery/metrics/metric-readiness-matrix-ENT.yaml`（唯一矩阵文件，未新建第二份）

## 1. 范围与 28 个缺口 ID 的处置结论

派单附录 28 个 metric_id（审计方法：demo-ui-topic `rg "metricId[=:]" src/app` 对照 `getMetricReadiness`）逐一复核后分四类处置：

| 处置 | 数量 | 明细 |
|------|------|------|
| **新建条目（seed 已登记，ENT-OVERVIEW 段）** | 10 | `M_ENT_TOTAL_COUNT`(aligned) / `M_ENT_INNOVATIVE_COUNT`(draft Q011) / `M_ENT_NEW_COUNT_Y`(aligned) / `M_ENT_AVG_RD_INVESTMENT`(aligned) / `M_ENT_TYPE_COUNT`(draft Q010) / `M_ENT_REGIONAL_COUNT`(draft Q012) / `M_ENT_AGGLOMERATION_INDEX`(draft Q012) / `M_ENT_DOMAIN_COVERAGE_COUNT`(aligned) / `M_ENT_DOMAIN_COVERAGE_DEPTH`(draft Q013) / `M_ENT_DIVERSIFICATION_INDEX`(draft Q013)。其中 5 条系 demo 同义 ID 的**正名条目**（见别名清单） |
| **新建条目（seed 未登记，ENT-DEMO-UNREGISTERED 段，d1 missing）** | 11 | `M_ENT_RESEARCHER_COUNT` / `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`（TRACE-E31 自定义指标）/ `M_ENT_KEY_TOTAL`(Q038) / `M_ENT_REGION_COVERAGE` / `M_ENT_REGION_HOT_COUNT` / `M_ENT_CHAIN_STAGE_COVERAGE` / `M_ENT_PATENT_VALID_COUNT` / `M_ENT_CITY_RANK`(Q016) / `M_ENT_STAR_PATENT_COUNT`(Q048) / `M_ENT_STAR_RD_RATIO`(Q048) / `M_ENT_STATE_OWNED_COUNT`(Q049)。一律 `d1_note: 未入 cfg_metric-ENT-seed，待王惠正式化`；d2~d4 = n/a（policy §2.3.1） |
| **别名归一（不新建条目）** | 3 → 存量条目 | `M_ENT_SZ_TOTAL_COUNT`→`M_ENT_SZ_COUNT`；`M_ENT_TECH_SCORE`→`M_ENT_TECH_POWER_SCORE`；`M_ENT_BUSINESS_SCORE`→`M_ENT_BUSINESS_POWER_SCORE` |
| **复核确认已在矩阵（零动作）** | 4 | `M_ENT_GROWTH_POTENTIAL` / `M_ENT_INDUSTRY_MATCH_SCORE`（RECRUIT 段）/ `M_ENT_POLICY_MATCH_SCORE`（RECRUIT 段）/ `M_ENT_STAR_ENTERPRISE_COUNT`（STAR 段）——审计缺口实为 **FE readinessSeed 镜像未同步**（32 条 < 矩阵 53 条），归 UI-L02 补镜像 |

**补充发现（UI-L02 防漏扫描回灌，2026-08-01 追加）**：`M_ENT_TYPE_RATIO`（类型占比，seed 已登记 aligned）在 demo 页面以三元表达式引用致原审计 28 条清单漏检，防漏契约测试扫描命中后按同段规则补录 ENT-OVERVIEW 段（D2 pending / D3 pending_ods / D4 mock）。矩阵最终 **75 条**（OVERVIEW 段 11 条新建）。

**「仅 mock 文件」4 个 ID 的核对结论**（派单第 4 点，未凭空登记）：
- `M_ENT_TECH_SCORE` / `M_ENT_BUSINESS_SCORE`：仅 `src/app/mock/enterprise/filterFieldSchema.ts` 筛选字段配置引用（`pendingRef: Q014` 与正名条目一致）→ **登记别名**，不建条目，不建议清理（查询筛选器语义成立）；
- `M_ENT_POLICY_MATCH_SCORE` / `M_ENT_STAR_ENTERPRISE_COUNT`：仅 `entGapCatalog.ts` 镜像引用，且**已在矩阵** → 零动作；FE 镜像由 UI-L02 视页面消费情况补齐。

## 2. 别名清单（矩阵头部 `demo_metric_id_aliases`，共 9 条）

| demo 本地 ID | 矩阵正名 ID | 备注 |
|---|---|---|
| M_ENT_DOMAIN_BREADTH | M_ENT_DOMAIN_COVERAGE_BREADTH | L01 已有 |
| M_ENT_SZ_TOTAL_COUNT | M_ENT_SZ_COUNT | |
| M_ENT_NEW_COUNT | M_ENT_NEW_COUNT_Y | ⚠️ demo KPI「近 12 月」窗口 vs seed 按年口径，窗口差异待王惠确认（已写入条目 d1_note） |
| M_ENT_RD_INVEST_AVG | M_ENT_AVG_RD_INVESTMENT | |
| M_ENT_CLUSTER_INDEX | M_ENT_AGGLOMERATION_INDEX | Q012 |
| M_ENT_DOMAIN_DEPTH | M_ENT_DOMAIN_COVERAGE_DEPTH | Q013 |
| M_ENT_DOMAIN_DIVERSITY | M_ENT_DIVERSIFICATION_INDEX | Q013 |
| M_ENT_TECH_SCORE | M_ENT_TECH_POWER_SCORE | 仅 filterFieldSchema 引用，Q014 |
| M_ENT_BUSINESS_SCORE | M_ENT_BUSINESS_POWER_SCORE | 仅 filterFieldSchema 引用，Q014 |

未做别名（诚实性）：`M_ENT_CHAIN_STAGE_COVERAGE` ≈ `M_ENT_CHAIN_COMPLETENESS`、`M_ENT_STAR_RD_RATIO` ≈ `M_ENT_RD_INVESTMENT_RATIO`、`M_ENT_PATENT_VALID_COUNT` ≈ `M_ENT_PATENT_TOTAL` 三组语义相近但口径未经确认，**不预先合并**，各自登记并在 d1_note 标注候选关系。

## 3. 诚实性说明（派单铁律逐条对照）

- **D1**：seed 已登记 10 条按 seed 推导（`definition_status/pending_ref` → draft+ref；无 pending → aligned）；未登记 11 条一律 `missing` + 待王惠正式化注记 ✅
- **D2**：新建 22 条（含补充发现 TYPE_RATIO）中 seed 已登记 11 条一律 `pending`（未逐条对照 DWD/ES/图 设计，未伪标 ready）；missing 11 条 = n/a ✅
- **D3**：28+1 个 ID 经全量检索确认**均无 6 份 data-gap-catalog 依据**（命中仅在 Wireframe/TRACE/IA/ADS-facts/UX 文档）→ seed 已登记 11 条一律 `pending_ods` 并注明「seed 旧 mapping_status 仅桌面推断，未经 GDF 字段级核对，8/20 后统一评估」，**未按 seed 的 ✅ 伪推 full**；missing 11 条 = n/a ✅
- **D4**：新建有效条目一律 `mock`（阶段清单全 todo）；missing = n/a ✅
- Excel 未作真源、未新建第二份矩阵文件（metrics/README §1 唯一性铁律）✅

## 4. 验收证据

- YAML 机器解析通过（node + yaml 包，TYPE_RATIO 补录后复验）：total 75；D1 aligned 15 / draft 44 / missing 16；D2 pending 46 / n/a 16；D3 pending_ods 11 / n/a 16；D4 mock 59 / n/a 16；别名 9；无重复 metric_id；与头部汇总段一致
- 每条 draft 均挂 `d1_pending_ref`（存量例外 `M_ENT_STAR_BASIC_INFO` / `M_ENT_STAR_HONOR_LIST` 为 L01 已有、d1_note 已说明口径无歧义仅待注册，本次未动）
- 头部 `updated: 2026-08-01`、生成任务注释追加 `ENT-READINESS-MATRIX-ENT-L02`

## 5. 开放项（接力）

| # | 事项 | 责任 |
|---|------|------|
| 1 | UI-L02：FE readinessSeed / METRIC_ID_ALIASES 增量镜像本次 22 条（含 TYPE_RATIO）+ 8 条新别名；entGapCatalog 不新增（本次无 gap catalog 新依据）——已完成，见 ENT-MOD-ENT-READINESS-UI-L02.md | frontend-agent（ENT-MOD-ENT-READINESS-UI-L02） |
| 2 | 未注册 11 条待王惠正式化入 seed 后升 D1（含 NEW_COUNT 窗口、CHAIN_STAGE_COVERAGE 是否并入 CHAIN_COMPLETENESS、STAR_RD_RATIO 是否对齐 RD_INVESTMENT_RATIO 三个口径点） | 王惠 → data-agent 正式化 |
| 3 | OVERVIEW 段 11 条 D2 待架构/data-agent 首评、D3 待 8/20 后 GDF 复判 | architect / GDF |
| 4 | 观察项（未入本次范围）：`M_ENT_SEARCH_RESULT_COUNT` / `M_ENT_SZ_SCALE_DIST` 存在于 demo metricSeed、页面未以 metricId 引用、矩阵无条目，待后续页面消费时再评估 | coordinator 留意 |

## 6. 架构合规自检（§2 十条）

1 算法只在 Python：不涉及 ✅ 2 调用链：纯文档/YAML ✅ 3 图谱：不涉及 ✅ 4 可观测：不涉及 ✅ 5 CI/CD：cicd: skip_design_only ✅ 6 demo2 只读 merge：不涉及 ✅ 7 共享聚合核心：不涉及 ✅ 8 数据策略：Mock 先行、D4 诚实标 mock ✅ 9 D8 前端规范：不涉及（FE 契约由 UI-L02 落）✅ 10 D9 血缘：本任务即其治理（8 件套/四维只读真源维护）✅
