# 全模块 · 方案 B 双签派单说明（王惠 + 唐绍祖）

> **决策**：2026-07-29 项目负责人确认方案 B，并明确 **非企业模块同样适用**  
> **规约**：`产品定义评审规程.md` §1.4.2（v2.6.1）· `team-roster.yaml#metric_dual_signoff`  
> **血缘阶段**：Phase 1 — `data-lineage-policy.md` §2.2  
> **企业维度专项交接**（历史）：`企业战略分析-ENT/ENT-SEMANTIC-DUAL-SIGNOFF-方案B-派单说明.md`

---

## 1. 角色分工（全模块）

| 角色 | 真人 | 域 | 职责 |
|------|------|----|------|
| 口径主责 | **王惠** | metric-subcoord | 全模块 metric_id、业务口径、适用性、开放项、PDR-05/06·H-01 口径侧；默认可 `supervised_by` |
| 算法共签 | **唐绍祖** | metric-subcoord（算法侧） | 公式、权重、算法定义卡；可代签收口；王惠缺席时按 §1.4.1 临时代口径（须纪要） |
| 名义 Owner | 何老师（北明） | 全要素 | 日常以双签为准 |
| 表级血缘执行 | data-agent + architect | lineage-subcoord | 项目自研 DWD 契约；王惠会签「能否撑指标」 |

**闭合铁律**：任一门 1 = 王惠口径签（或缺席临时代+纪要）+ 唐绍祖算法签（或算法 N/A 有据）。

---

## 2. 适用范围

- `ENT-*` / `ENT-MOD-*`（企业）
- `E-E7-POLICY-*` / 政策及其他要素 METRIC-OPEN
- 凡 wireframe 第 6 列 metric_id、指标 8 件套、PDR-05/06、H-01

新建 METRIC-OPEN 默认字段：

```yaml
supervised_by: human:王惠
owner_semantic: human:王惠
cosigner_algorithm: human:唐绍祖
subcoord: metric-subcoord
ods_dependency_phase: phase1
```

已 done 历史任务 **不回溯改签**；有变更增量走双签。

---

## 3. coordinator 派单话术（摘录）

**→ 王惠**：你是全模块 metric-subcoord 口径主责（方案 B）。监管各模块 METRIC-OPEN；Phase 1 一律 `⏳ pending_ods`。算法权重请唐绍祖共签。

**→ 唐绍祖**：全模块算法共签方。公式/权重你可代签收口；口径以王惠为准。王惠缺席时按 §1.4.1 临时代口径并写纪要。
