# A1 交付 schema · 双表 DoD（2026-08-21 定稿）

> 决策：淮政玮确认按双表定义。企业域现有 `calc-logic/ENT` + `cfg_metric-ENT-seed.yaml` + `metric-readiness-matrix-ENT.yaml` 只作**样板与对照**，不代替本叶对算法库 SRS 叶子的逐条登记。  
> **8/25 目的**：从双表抽出 **三方 ODS 不满足** 清单给人（采购/入站）。  
> 本叶**不改** seed / 就绪度矩阵。ODS 满足度枚举沿用 D9 D3：`full | partial | none | pending_ods | n/a`。

## 交双表 + 缺口清单

```
metrics/algo-results/
├── ALGO-LIB-METRIC-DEPS-L01.md                 ← handoff
├── ALGO-LIB-METRIC-DEPS-L01-summary.md         ← 八维计数（须与 xlsx Sheet4 一致）
├── ALGO-LIB-METRIC-DEPS-L01-requirements.yaml  ← 表1 需规逐条对应
├── ALGO-LIB-METRIC-DEPS-L01-metrics.yaml       ← 表2 指标·算法·公式·数据依赖
├── ALGO-LIB-METRIC-DEPS-L01-ods-gaps.yaml      ← 表3 投影（机器）
├── ALGO-LIB-METRIC-DEPS-L01-ods-gaps.md        ← 不满足 + 待核验（给人 md）
└── ALGO-LIB-METRIC-DEPS-L01-ods-status.xlsx    ← 8/25 给人主表（全量/不满足/待核验/八维汇总）
```

给人 xlsx 栏目与 DoD：`agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md` **§9**。禁止只交 yaml 不交 xlsx。

旧名 `*-deps.yaml` **作废**，不要再交一张混表。

---

## 表1 · 需规逐条对应 `*-requirements.yaml`

粒度：**算法库 SRS 叶子一条一行**（八维 README 合计 97）。一条需规可对应 0～N 个指标。

```yaml
version: 1
task: ALGO-LIB-METRIC-DEPS-L01
updated: "YYYY-MM-DD"
srs_leaf_count_expected: 97
srs_leaf_count_actual: 97
requirements:
  - requirement_id: ALGO-ENT-BASE-97          # 稳定 ID：ALGO-{维缩写}-{层}-{seq}
    dimension: 企业
    layer: 基础指标                           # 基础指标 | 图谱 | 深度分析 | 综合分析 | 图谱API
    srs_path: agent-delivery/bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/企业/基础指标.md
    excel_row: 6
    seq: 97
    requirement_title: 企业基础指标模型构建
    requirement_excerpt: "五类：重点企业提取、类型分布、领域分布、重点资讯、新增企业数量"
    inventory_ref: null                       # L01 candidate_id，无则 null
    coverage_status: full | partial | missing | third_party
    metrics:
      - metric_id: M_ENT_KEY_TOTAL            # 已有 seed 用正式 ID；尚无则 TEMP_ALGO_{requirement_id}_{n}
        metric_name_zh: 重点企业总数
        algorithm_id: ALG-ENT-STAT-001
        formula_ref: M_ENT_KEY_TOTAL          # 指向表2 同 metric_id
    coverage_note: "五类中资讯类仅部分映射"
```

`coverage_status`：需规要求是否被**指标+算法**解释完整（不是 ODS 是否满足）。

| 值 | 含义 |
|----|------|
| `full` | 需规点名的能力均有指标对应 |
| `partial` | 只覆盖部分子能力 |
| `missing` | 算法库需规有、本分析落不出指标（A2 差集的输入） |
| `third_party` | 人才/科研机构/技术实现等，不伪展开公式，但仍须挂所需输入（见表2） |

---

## 表2 · 指标与重要数据依赖 `*-metrics.yaml`

粒度：**一项指标一条**。复合模型拆 `inputs[]`，每条输入单独评 ODS。

```yaml
version: 1
task: ALGO-LIB-METRIC-DEPS-L01
updated: "YYYY-MM-DD"
metrics:
  - metric_id: M_ENT_TECH_POWER_SCORE
    metric_name_zh: 技术力得分
    requirement_refs: [ALGO-ENT-DEEP-xxx]
    owner: 我方 | 第三方
    definition: "企业技术力五维综合评分，0–100"

    algorithm:
      algorithm_id: ALG-ENT-MODEL-001
      type: STAT | COMPUTE | MODEL | GRAPH | API | MIXED | UNKNOWN
      description: "五维标准化后加权求和"
      formula: "SUM(normalize(x_i) * w_i)"
      steps: []                    # MODEL/GRAPH 必填步骤；STAT 可空
      parameters:
        weights_status: pending_business_definition | specified | n/a
      output_grain: "enterprise_id + period"
      version: draft-v1

    inputs:                        # 重要计算数据依赖，一条输入一行
      - input_name: 研发人员数
        required_grain: "enterprise_id + year"
        required_field: development_employee
        source_system: 三方企业库
        ods_table: ""              # 未核验留空
        ods_field: ""
        dwd_table: gkx.dwd_org_annual_financial_info
        dwd_field: development_employee
        join_key: org_id
        ods_mapping_status: full | partial | none | pending_ods | n/a
        evidence: "对照路径或「未核三方入站」"
        gap: ""
        impact: ""
        workaround: null

      - input_name: 高级研发人才数量
        required_grain: "enterprise_id + year"
        required_field: senior_rd_headcount
        source_system: 三方企业库
        ods_table: null
        ods_field: null
        dwd_table: null
        dwd_field: null
        join_key: org_id
        ods_mapping_status: none
        evidence: "calc-logic/ENT/M_ENT_TECH_POWER_SCORE.md 待建字段"
        gap: "缺学历/职称结构字段"
        impact: "技术人才子维度无法完整计算"
        workaround: null

    dependency_rollup:
      ods_mapping_status: partial
      reason: "研发人员数可得，高级研发人才缺失"
```

### ODS 汇总规则（指标级 `dependency_rollup`）

| 输入情况 | 指标汇总结论 |
|----------|----------------|
| 全部必需输入 `full` | `full` |
| 至少一项可用，且存在 `partial`/`none` | `partial` |
| 全部必需输入 `none` | `none` |
| 任一必需输入尚未核三方 ODS | `pending_ods`（禁止凭 DWD 反推已满足） |
| 纯派生（排名等） | `n/a`，且 `inputs` 指向上游 `metric_id` |

第三方算法：`formula` 可写「不展开」，`inputs` 与 `ods_mapping_status` **仍必填**。

---

## 表3 · 三方缺口清单（8/25 主交付）

从 `*-metrics.yaml` 的 `inputs[]` **投影**，禁止手填一套对不上的平行表。

| 分区 | 收录 | 不收录 |
|------|------|--------|
| `confirmed_unmet`（给人的「不满足」） | `ods_mapping_status` 为 `none` 或 `partial` | `full` / `n/a` / `pending_ods` |
| `pending_verify`（待核验，不得当成已确认缺口） | `pending_ods` | — |

```yaml
version: 1
task: ALGO-LIB-METRIC-DEPS-L01
deadline: "2026-08-25"
as_of: "YYYY-MM-DD"
confirmed_unmet:
  - gap_id: ODS-GAP-001
    ods_mapping_status: none | partial
    input_name: 高级研发人才数量
    metric_id: M_ENT_TECH_POWER_SCORE
    requirement_refs: [ALGO-ENT-DEEP-xxx]
    source_system: 三方企业库
    missing: "学历/职称结构或硕士以上专职研发人员字段"
    required_grain: "enterprise_id + year"
    impact: "技术人才子维度无法完整计算"
    evidence: "calc-logic/ENT/M_ENT_TECH_POWER_SCORE.md"
pending_verify: []
```

`*-ods-gaps.md` 给人读：先 `confirmed_unmet` 表，再 `pending_verify` 表；文首写截止日、两档条数，以及全量五档（full/partial/none/pending_ods/n/a）计数。

**8/25 给人主表**必须另交 `*-ods-status.xlsx`（四 sheet：全量满足度 / 不满足 / 待核验 / 八维汇总）。Sheet 1 行数 = 表2 全部 `inputs[]`；Sheet 2 只含 `none`/`partial`；Sheet 3 只含 `pending_ods`。未核入站不得标 `full`，也不得写入 Sheet 2。

---

## summary.md 必含计数

按八维列出：SRS 叶子数、`coverage_status` 四档、指标数、`algorithm.type` 分布、`dependency_rollup` 五档、**confirmed_unmet / pending_verify 条数**。
