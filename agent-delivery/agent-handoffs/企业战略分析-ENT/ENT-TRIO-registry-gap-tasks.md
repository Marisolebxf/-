# ENT 三模块 · registry 缺口 task 清单（YAML 片段）

> **依据**：`产品定义评审规程.md` §4 v2.5.1（PACK → METRIC-OPEN ∥ UX/V1 → PDR → V1-FINAL → V2∥G2）
> **范围**：企业查询 SEARCH · 对比篮 COMPARE · 企业评估 EVAL
> **状态**：2026-07-21 **已写入** `task-registry.yaml` + `scrum-sprint.yaml` stretch；本文档保留片段与 patch 说明备查

---

## 缺口总览

| 模块 | 新增 leaf | 须改既有 leaf |
|------|-----------|---------------|
| SEARCH | PACK-L01、METRIC-OPEN-L01、UX-L01、V1-FINAL、PDR-G1-RECLOSE | PDR-G1、V1-HIFI、V2-DEMO |
| COMPARE | METRIC-OPEN-L01、UX-L01、V1-FINAL、PDR-G1-RECLOSE | PACK-L01、PDR-G1、V1-HIFI、V2-DEMO |
| EVAL | V1-HIFI-R1、V1-FINAL、G2-SIGNOFF、V2-LUMEN、DG-G3 | PDR-G1（补 depends_on） |

---

## §A — 新增 task（复制到 `task-registry.yaml`）

### A1 · 插入位置：`ENT-MOD-SEARCH-PDR-G1` **之前**

```yaml
  - id: ENT-MOD-SEARCH-PACK-L01
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-SEARCH-PDR-G1-RECLOSE
    title: 企业查询 — 核心产品包（USM、TRACE、IA、Wireframe）
    agent: product-agent
    repo: agent-delivery
    depends_on: []
    status: review
    priority: P0
    sprint_id: "2026-W30"
    cicd: skip_design_only
    supervised_by: human:淮政玮
    note: |
      2026-07-21 流程合规 backfill：四件套已分散在 E1-企业查询/ 与 demo-ui-topic/docs/ia；
      TRACE-ENT-SEARCH 仍为 draft v0.1。本 task 合并真源、升版 TRACE，不重复 2026-07-12 legacy 门1结论。
    product_gates:
      target_gate: ENT-MOD-SEARCH-PDR-G1-RECLOSE
      track: Track-MS
      package_mode: pre_pdr_definition
    definition_of_done:
      - "USM/TRACE/IA/Wireframe 四份文档路径统一、相互一致"
      - "TRACE-ENT-SEARCH.yaml 从 draft 升为可评审版本"
      - "REQ-ENT-001 + E-20~E-35 检索触点映射完整"
      - "wireframe 字段表第 6 列 metric_id 已列（语义卡由 METRIC-OPEN 闭合）"
    evidence:
      - agent-handoffs/产品整体定义/E1-企业查询/USM-E1-ENT-SEARCH-企业查询.md
      - agent-handoffs/产品整体定义/TRACE-ENT-SEARCH.yaml
      - agent-handoffs/产品整体定义/E1-企业查询/IA-E1-ENT-SEARCH-企业查询.md
      - agent-handoffs/产品整体定义/E1-企业查询/Wireframe-E1-ENT-SEARCH-企业查询.md
    estimated_tokens: 80_000
    effort_points: 2
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-SEARCH-METRIC-OPEN-L01
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-SEARCH-PDR-G1-RECLOSE
    title: 企业查询 — 指标语义与 ODS/DWD 缺口核对（METRIC-OPEN）
    agent: algorithm-agent
    repo: agent-delivery
    repos: [agent-delivery]
    depends_on: [ENT-MOD-SEARCH-PACK-L01]
    status: blocked
    blocked_by: ENT-MOD-SEARCH-PACK-L01 review/done
    priority: P0
    sprint_id: "2026-W30"
    cicd: skip_design_only
    supervised_by: human:唐绍祖
    collaborators:
      - agent:data-agent
    note: |
      检索模块 metric 以 cfg_metric-ENT-seed + Q033~Q037 为主；algorithm-agent 核对检索相关口径，
      data-agent 输出贴源矩阵与 data-gap-catalog（如有 🟡/❌）。
    product_gates:
      target_gate: ENT-MOD-SEARCH-PDR-G1-RECLOSE
      track: Track-MS
      package_mode: metric_open_check
    definition_of_done:
      - "METRIC-OPEN-ENT-SEARCH-核对记录.md"
      - "更新 cfg_metric-ENT-seed.yaml 检索相关 M_ENT_*"
      - "适用时 {模块}/data-gap-catalog.yaml；Q033~Q037 与 TRACE open_items 一致"
      - "唐绍祖 §1.4.1 会签"
    evidence:
      - agent-handoffs/产品整体定义/METRIC-OPEN-ENT-SEARCH-核对记录.md
    estimated_tokens: 120_000
    effort_points: 2
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-SEARCH-UX-L01
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-SEARCH-V1-HIFI
    title: 企业查询 — UX 交互规格对齐（检索/高筛/列表/导出）
    agent: ux-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-SEARCH-PACK-L01]
    status: blocked
    blocked_by: ENT-MOD-SEARCH-PACK-L01 review/done
    priority: P1
    sprint_id: "2026-W30"
    cicd: skip_design_only
    supervised_by: human:高颖
    note: "真源：demo-ui-topic/docs/ia/enterprise/ENT-search-design.md + Q033~Q037 修订项；产出 UX-SPEC 或升版 IA。"
    evidence:
      - repos/demo-ui-topic/docs/ia/enterprise/ENT-search-design.md
    estimated_tokens: 60_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green
```

### A2 · 插入位置：`ENT-MOD-SEARCH-V1-HIFI` **之后**

```yaml
  - id: ENT-MOD-SEARCH-V1-FINAL
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-SEARCH-V2-DEMO
    title: 企业查询 — V1 联合修订冻结
    agent: product-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-SEARCH-PDR-G1-RECLOSE]
    status: blocked
    blocked_by: "ENT-MOD-SEARCH-PDR-G1-RECLOSE + ENT-MOD-SEARCH-V1-HIFI done"
    priority: P0
    sprint_id: "2026-W31"
    cicd: skip_design_only
    supervised_by: human:高颖
    note: "吸收 PDR 完整闭合与 V1 首轮反馈；冻结 HIFI-ENT-SEARCH-medium-v1.0 基线后再宣告 V2 准生产对齐完成。"
    evidence:
      - agent-handoffs/产品整体定义/UI-HIFI-ENT-SEARCH-联合修订冻结单.md
    estimated_tokens: 40_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-SEARCH-PDR-G1-RECLOSE
    epic: E-ENT-SCRUM-PDR
    title: "门1 PDR · 企业查询（v2.5 完整闭合）"
    agent: product-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-SEARCH-PACK-L01, ENT-MOD-SEARCH-METRIC-OPEN-L01, ENT-MOD-SEARCH-V1-HIFI]
    status: blocked
    blocked_by: "PACK + METRIC-OPEN + V1-HIFI-R1（§4 双轨汇合）"
    priority: P0
    sprint_id: "2026-W31"
    cicd: skip_design_only
    supervised_by: human:郭万迎
    note: |
      2026-07-12 ENT-MOD-SEARCH-PDR-G1 为 legacy 附条件通过；本 leaf 按 §4 重新完整闭合。
      不删除 legacy 纪要 PM-PDR-ENT-SEARCH-评审纪要.md。
    product_gates:
      pdr: agent-handoffs/企业战略分析-ENT/PM-PDR-ENT-SEARCH-评审纪要-v2-closure.md
      track: Track-MS
    evidence: agent-handoffs/企业战略分析-ENT/PM-PDR-ENT-SEARCH-评审纪要-v2-closure.md
    estimated_tokens: 50_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green
```

### A3 · 插入位置：`ENT-MOD-COMPARE-V1-HIFI` **之前**（在 COMPARE-PACK-L01 之后）

```yaml
  - id: ENT-MOD-COMPARE-METRIC-OPEN-L01
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-COMPARE-PDR-G1-RECLOSE
    title: 对比篮 — 指标语义与开放项适用性核对（METRIC-OPEN）
    agent: algorithm-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-COMPARE-PACK-L01]
    status: blocked
    blocked_by: ENT-MOD-COMPARE-PACK-L01 done
    priority: P0
    sprint_id: "2026-W30"
    cicd: skip_design_only
    supervised_by: human:唐绍祖
    collaborators:
      - agent:data-agent
    note: |
      派生容器模块：五件套 #4 预期大量 N/A（须书面依据）；#5 同步 Decision 088 / Q 项。
      跨模块 handoff（→ 评估/风险）边界写入核对记录。
    product_gates:
      target_gate: ENT-MOD-COMPARE-PDR-G1-RECLOSE
      track: Track-MS
      package_mode: metric_open_check
    evidence:
      - agent-handoffs/产品整体定义/METRIC-OPEN-ENT-COMPARE-核对记录.md
    estimated_tokens: 80_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-COMPARE-UX-L01
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-COMPARE-V1-HIFI
    title: 对比篮 — UX 交互规格（暂存/分发/跨模块携带）
    agent: ux-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-COMPARE-PACK-L01]
    status: blocked
    blocked_by: ENT-MOD-COMPARE-PACK-L01 done
    priority: P1
    sprint_id: "2026-W30"
    cicd: skip_design_only
    supervised_by: human:高颖
    evidence:
      - agent-handoffs/产品整体定义/ENT-COMPARE/Wireframe-ENT-COMPARE.md
    estimated_tokens: 50_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green
```

### A4 · 插入位置：`ENT-MOD-COMPARE-V2-DEMO` **之前**

```yaml
  - id: ENT-MOD-COMPARE-V1-FINAL
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-COMPARE-V2-DEMO
    title: 对比篮 — V1 联合修订冻结
    agent: product-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-COMPARE-PDR-G1-RECLOSE]
    status: blocked
    priority: P0
    sprint_id: "2026-W31"
    cicd: skip_design_only
    supervised_by: human:高颖
    evidence:
      - agent-handoffs/产品整体定义/UI-HIFI-ENT-COMPARE-联合修订冻结单.md
    estimated_tokens: 40_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-COMPARE-PDR-G1-RECLOSE
    epic: E-ENT-SCRUM-PDR
    title: "门1 PDR · 对比篮（v2.5 完整闭合）"
    agent: product-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-COMPARE-PACK-L01, ENT-MOD-COMPARE-METRIC-OPEN-L01, ENT-MOD-COMPARE-V1-HIFI]
    status: blocked
    priority: P0
    sprint_id: "2026-W31"
    cicd: skip_design_only
    supervised_by: human:郭万迎
    note: "2026-07-12 legacy 通过；本 leaf 按 §4 完整闭合。保留 PM-PDR-ENT-COMPARE-评审纪要.md。"
    evidence: agent-handoffs/企业战略分析-ENT/PM-PDR-ENT-COMPARE-评审纪要-v2-closure.md
    estimated_tokens: 50_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green
```

### A5 · 插入位置：`ENT-MOD-EVAL-PDR-G1` **之前**

```yaml
  - id: ENT-MOD-EVAL-V1-HIFI-R1
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-EVAL-PDR-G1
    title: 企业评估 — UI Demo + V1 高保真首轮会签
    agent: ui-agent
    repo: ui_topic.demo
    depends_on: [ENT-MOD-EVAL-PACK-L01]
    status: ready
    priority: P0
    sprint_id: "2026-W30"
    cicd: skip_design_only
    supervised_by: human:高颖
    claimed_by: human:许丹丹、望淋莉
    note: |
      demo-ui-topic 已有 EnterpriseEvaluation* 页面；本 task 补 H-01~H-08 首轮会签单，
      与 METRIC-OPEN-L01 并行，不阻塞彼此；共同作为 PDR-G1 输入。
    product_gates:
      track: Track-MS
      v1_hifi_round1: agent-handoffs/产品整体定义/UI-HIFI-ENT-EVAL-会签单.md
      hifi_round1_version: HIFI-ENT-EVAL-medium-r1
    evidence:
      - agent-handoffs/产品整体定义/UI-HIFI-ENT-EVAL-会签单.md
      - repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseEvaluationPage.tsx
    estimated_tokens: 100_000
    effort_points: 2
    difficulty: M
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-EVAL-V1-FINAL
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-EVAL-V2-LUMEN
    title: 企业评估 — V1 联合修订冻结
    agent: product-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-EVAL-PDR-G1]
    status: blocked
    priority: P0
    sprint_id: "2026-W31"
    cicd: skip_design_only
    supervised_by: human:高颖
    evidence:
      - agent-handoffs/产品整体定义/UI-HIFI-ENT-EVAL-联合修订冻结单.md
    estimated_tokens: 40_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-EVAL-G2-SIGNOFF
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-EVAL-DG-G3
    title: 企业评估 — 门2 体验+语义会签
    agent: product-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-EVAL-V1-FINAL]
    status: blocked
    priority: P0
    sprint_id: "2026-W32"
    cicd: skip_design_only
    supervised_by: human:高颖
    note: "与 ENT-MOD-EVAL-V2-LUMEN 并行（§4 v2.4）"
    evidence: agent-handoffs/产品整体定义/PM-会签-ENT-EVAL-签字单.md
    estimated_tokens: 40_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-EVAL-V2-LUMEN
    epic: E-ENT-SCRUM-PDR
    parent: ENT-MOD-EVAL-DG-G3
    title: 企业评估 — V2 lumen 准生产实现会签
    agent: frontend-agent
    repo: ui_topic.lumen
    branch: dev
    depends_on: [ENT-MOD-EVAL-V1-FINAL]
    status: blocked
    priority: P0
    sprint_id: "2026-W32"
    cicd: default
    supervised_by: human:孔东
    note: "与 G2-SIGNOFF 并行；依赖 METRIC-OPEN catalog + V1 冻结基线"
    evidence: agent-handoffs/产品整体定义/FE-LUMEN-V2-ALIGN-ENT-EVAL-会签单.md
    estimated_tokens: 150_000
    effort_points: 3
    difficulty: M
    effort_source: planning_estimate
    cost_warn: green

  - id: ENT-MOD-EVAL-DG-G3
    epic: E-ENT-SCRUM-PDR
    title: "门3 DG · 企业评估拍板"
    agent: product-agent
    repo: agent-delivery
    depends_on: [ENT-MOD-EVAL-V1-FINAL, ENT-MOD-EVAL-G2-SIGNOFF, ENT-MOD-EVAL-V2-LUMEN]
    status: blocked
    priority: P0
    sprint_id: "2026-W33"
    cicd: skip_design_only
    supervised_by: human:淮政玮
    evidence: agent-handoffs/产品整体定义/DG-ENT-EVAL-拍板纪要.md
    estimated_tokens: 30_000
    effort_points: 1
    difficulty: S
    effort_source: planning_estimate
    cost_warn: green
```

---

## §B — 既有 leaf 字段覆盖（patch）

### B1 · `ENT-MOD-SEARCH-PDR-G1`（legacy，保留 done）

```yaml
    status: done
    legacy_gate: true
    superseded_by: ENT-MOD-SEARCH-PDR-G1-RECLOSE
    note: "2026-07-12 legacy 附条件通过（TRIO）。§4 v2.5.1 完整闭合见 ENT-MOD-SEARCH-PDR-G1-RECLOSE。"
```

### B2 · `ENT-MOD-SEARCH-V1-HIFI`（等同 V1-HIFI-R1）

```yaml
    depends_on: [ENT-MOD-SEARCH-PACK-L01, ENT-MOD-SEARCH-UX-L01]
    alias: ENT-MOD-SEARCH-V1-HIFI-R1
    note: "…原有 note…；registry 别名 V1-HIFI-R1；不再依赖 legacy PDR-G1。"
```

### B3 · `ENT-MOD-SEARCH-V2-DEMO`

```yaml
    depends_on: [ENT-MOD-SEARCH-V1-FINAL]
    legacy_waiver: DECIDE-FE-V2-LUMEN-DIRECT-2026-07-12
    note: "…；工程已超前启动，须在 V1-FINAL 后补 FE-LUMEN 会签对齐声明。"
```

### B4 · `ENT-MOD-COMPARE-PACK-L01`

```yaml
    depends_on: []
    parent: ENT-MOD-COMPARE-PDR-G1-RECLOSE
    note: "…；修正依赖：PACK 先于 PDR（§4），不 depends_on legacy PDR-G1。"
```

### B5 · `ENT-MOD-COMPARE-PDR-G1`

```yaml
    legacy_gate: true
    superseded_by: ENT-MOD-COMPARE-PDR-G1-RECLOSE
```

### B6 · `ENT-MOD-COMPARE-V1-HIFI`

```yaml
    depends_on: [ENT-MOD-COMPARE-PACK-L01, ENT-MOD-COMPARE-UX-L01]
    alias: ENT-MOD-COMPARE-V1-HIFI-R1
```

### B7 · `ENT-MOD-COMPARE-V2-DEMO`

```yaml
    depends_on: [ENT-MOD-COMPARE-V1-FINAL]
```

### B8 · `ENT-MOD-EVAL-PDR-G1`

```yaml
    depends_on: [ENT-MOD-EVAL-PACK-L01, ENT-MOD-EVAL-METRIC-OPEN-L01, ENT-MOD-EVAL-V1-HIFI-R1]
    blocked_by: "METRIC-OPEN-L01 + V1-HIFI-R1（§4 双轨汇合）"
```

---

## §C · `scrum-sprint.yaml` stretch 建议追加

```yaml
      - ENT-MOD-SEARCH-PACK-L01
      - ENT-MOD-SEARCH-METRIC-OPEN-L01
      - ENT-MOD-COMPARE-METRIC-OPEN-L01
      - ENT-MOD-EVAL-V1-HIFI-R1
```

---

## §D · 推荐执行顺序（三模块）

```text
EVAL:  METRIC-OPEN-L01 ∥ V1-HIFI-R1 → PDR-G1 → V1-FINAL → (V2 ∥ G2) → DG-G3
SEARCH: PACK-L01 → METRIC-OPEN ∥ (UX → V1-HIFI) → PDR-RECLOSE → V1-FINAL → V2（补 waiver）
COMPARE: PACK-L01 done → METRIC-OPEN ∥ (UX → V1-HIFI) → PDR-RECLOSE → V1-FINAL → V2
```
