# 企业维度 · 方案 B 双签派单说明（王惠 + 唐绍祖）

> **更新**：2026-07-29 — 项目负责人确认 **非企业模块亦按方案 B**；全模块真源见 `产品整体定义/METRIC-DUAL-SIGNOFF-方案B-全模块派单说明.md` 与规程 §1.4.2 v2.6.1。
>

> **决策**：2026-07-29 项目负责人确认方案 B  
> **规约**：`产品定义评审规程.md` §1.4.2 · `team-roster.yaml#semantic_owner_delegation.enterprise_dual_signoff`  
> **血缘阶段**：Phase 1（ODS 未稳，~8/20）— `data-lineage-policy.md` §2.2

---

## 1. 角色分工

| 角色 | 真人 | 域 | 职责 |
|------|------|----|------|
| 口径主责 | **王惠** | metric-subcoord | metric_id、业务口径、适用性、开放项、PDR-05/06·H-01 口径侧；可 `supervised_by` |
| 算法共签 | **唐绍祖** | metric-subcoord（算法侧） | 公式、权重、算法定义卡；可代签收口；非企业模块仍按 §1.4.1 代何老师 |
| 名义 Owner | 何老师（北明） | 全要素 | 企业日常以双签为准 |
| 表级血缘执行 | data-agent + architect | lineage-subcoord | 项目自研 DWD 契约；王惠会签「能否撑指标」 |

**闭合铁律**：企业模块门 1 = 王惠口径签 + 唐绍祖算法签（或算法 N/A 有据）。缺一不可。

---

## 2. 在途 METRIC-OPEN 交接

| Task ID | 现状 | 建议动作 |
|---------|------|----------|
| `ENT-MOD-SEARCH-METRIC-OPEN-L01` | in_progress · supervised_by 唐绍祖 | 改主监管为 **王惠**；唐绍祖保留算法子项共签；开 30min 交接 |
| `ENT-MOD-RECRUIT-METRIC-OPEN-L01` | in_progress · supervised_by 唐绍祖 | 同上 |
| 已 done 的 COMPARE/EVAL/RISK METRIC-OPEN | done · 唐绍祖 | **不回溯改签**；新变更走双签 |
| KEYPANO / STAR / SHENZHEN / OPS METRIC-OPEN | 待启动 | 新建即按双签：`supervised_by: human:王惠` |

交接纪要须写：`owner_semantic: human:王惠` + `cosigner_algorithm: human:唐绍祖`。

---

## 3. 已写入 registry 的 leaf / 补齐说明

### 3.1 lineage（数据对齐 · Phase 1）

> **已入** task-registry.yaml：ENT-LINEAGE-DWD-CONTRACT-L01（status=backlog，supervised_by=王惠）

```yaml
- id: ENT-LINEAGE-DWD-CONTRACT-L01
  title: 企业维度 — 项目自研 DWD 契约样板（主表 + 指标支撑字段）
  agent: data-agent
  subcoord: lineage-subcoord
  status: backlog  # 已入 task-registry.yaml · 2026-07-29
  supervised_by: human:王惠          # 会签「能否撑指标」
  co_reviewers: [human:徐滕强]       # 架构审设计
  depends_on: []
  ods_dependency_phase: phase1
  definition_of_done:
    - 至少 1 张企业主表契约落盘于 data/data-design/企业/（模板：_templates/dwd-table-contract-template.md）
    - 每业务字段含 ods_mapping_expectation（confidence + expected_from）
    - 覆盖 SEARCH/EVAL/RISK/RECRUIT 已用到的核心字段清单表
    - 王惠会签记录写入 handoff（支撑哪些 metric_id）
    - 禁止按供应库 dwd_* 一一抄表
```

### 3.2 metric（指标定义 · 与 lineage 并行，source_tables 依赖契约）

在途任务字段建议统一补：

```yaml
owner_semantic: human:王惠
cosigner_algorithm: human:唐绍祖
subcoord: metric-subcoord
ods_dependency_phase: phase1
# mapping_status 产出约束：⏳ pending_ods（Phase 1）
```

新建未启动模块时复制 SEARCH 的 METRIC-OPEN DoD，并追加：

- 核对记录含双签栏位
- `source_tables[]` 仅指向项目自研 DWD
- UI 缺口文案进 `data-gap-catalog.yaml`（⏳/⚠️ 文案真源）

---

## 4. 本周最小闭环

1. ~~花名册登记王惠 + §1.4.2~~（本提交）
2. SEARCH / RECRUIT 交接会（王惠 + 唐绍祖，30–60min）
3. `ENT-LINEAGE-DWD-CONTRACT-L01` 入 registry 并派 data-agent
4. 用样板表挂 3～5 个核心 metric_id，验证双签流程

---

## 5. coordinator 派单话术（摘录）

**→ 王惠**

> 你是企业维度 metric-subcoord 口径主责（方案 B）。监管 METRIC-OPEN；Phase 1 一律 `⏳ pending_ods`。算法权重请唐绍祖共签。业务歧义只进客户决策清单。

**→ 唐绍祖**

> 企业维度算法共签方。公式/权重/算法定义卡你可代签收口；口径以王惠为准。非企业模块临时代行何老师（§1.4.1）不变。

**→ data-agent（lineage）**

> 按 `_templates/dwd-table-contract-template.md` 写项目自研 DWD 契约；王惠会签；不碰供应库一一映射。
