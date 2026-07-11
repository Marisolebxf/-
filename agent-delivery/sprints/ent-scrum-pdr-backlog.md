# 企业维度 Scrum 重组 · PDR 三门 backlog

> **日期**：2026-07-12  
> **维护**：PM（郭万迎）+ coordinator + 高颖（体验 Owner）  
> **规程真源**：`产品定义评审规程.md`  
> **IA 真源**：`p2a-session/五模块IA追溯标注清单.md` §2 · `企业完整深化规格.md`  
> **机器队列**：`task-registry.yaml` → Epic `E-ENT-SCRUM-PDR`

---

## 1. 为什么要重组

| 问题 | 对策 |
|------|------|
| 旧 Epic `E-ENT-PROTOTYPE` 按「企业总览/全景/洞察/决策」四菜单拆 task | **已 superseded**；与新任务链 IA 冲突 |
| 门 1 PDR 已通过的能力未在 registry 体现 | 新增 `ENT-MOD-*-PDR-G1` + 下游 V1/V2/ARCH |
| 待 PDR 模块无占位 task | 新增 `blocked_by: 待门1 PDR` 的 backlog leaf |
| 人类看板不可见 | Planning 后写 `sprint_id` + 跑 Bitable sync |

---

## 2. 企业二级菜单 × PDR 状态（2026-07-12）

| 模块 ID | 二级菜单 / 横向能力 | 门1 PDR | 当前可并行 | 监管人建议 |
|---------|---------------------|---------|------------|------------|
| **SEARCH** | 企业查询（搜索/高筛） | ✅ 已过 | V1 高保真 · V2 demo · 后台架构 | 高颖 / 孔东 / 徐滕强 |
| **COMPARE** | 对比篮 | ✅ 已过 | V1 · V2 · 后台架构 | 高颖 / 孔东 |
| **PROFILE** | 企业详情（画像） | ✅ 已过 | V1 · V2 · 后台架构 | 高颖 / 孔东 |
| OVERVIEW | 企业总览 | ⏳ 待评审 | 仅产品五件套起草 | 高颖 + 郭万迎 |
| KEYENT | 重点企业分析 | ⏳ 待评审 | — | 高颖 |
| EVAL | 企业评估 | ⏳ 待评审 | — | 高颖 + 何老师 |
| RISK | 风险洞察 | ⏳ 待评审 | — | 高颖 |
| RECRUIT | 引育推荐 | ⏳ 待评审 | — | 高颖 |
| EXPORT | 分析导出 | ⏳ 待评审 | — | 郭万迎 |
| OPS | 维护管理 | ⏳ 待评审 | — | 高颖 + 徐滕强 |

**横向能力说明**：企业画像 = PROFILE；对比篮 = COMPARE；搜索 = SEARCH（含 `/development/search` 高级检索与场景化入口）。

---

## 3. 门 1 已通过模块 · 下游链（Track-MS）

```text
门1 PDR ✅（2026-07-12 团队确认）
    ├─► V1 高保真会签（高颖主持 · 许丹丹/望淋莉 + ui-agent）
    ├─► V2 lumen 准生产会签（孔东团队 · lumen-ui-science-topic dev）
    ├─► 门2 体验+语义会签（须 V2 ✅）
    ├─► 门3 DG 拍板（淮政玮）
    └─► ready → API 接线/联调硬化（同仓迭代，无复刻）

并行（不阻塞 V1/V2）：
    └─► ENT-ARCH-IMPL-DESIGN（徐滕强/李伟 · 功能实现架构设计）
        └─► ENT-ARCH-API-CONTRACT（侯佳伟 · OpenAPI 草案）
        └─► ENT-DATA-IMPL-PATH（辜少彬 · 贴源/ES/Mapping 确认）
```

> **铁律**（规程 §11）：未过 **V2** 不得门 2；未过 **门3** 不得标工程 leaf `ready`。V2 在 `lumen-ui-science-topic` dev 实现，**无复刻步骤**（见 `decisions/DECIDE-FE-V2-LUMEN-DIRECT-2026-07-12.md`）。

---

## 4. Sprint 2026-W28 承诺（覆盖 ISO 周 W27–W28）

| 优先级 | Task ID | 标题 | 负责人 |
|--------|---------|------|--------|
| P0 | ENT-MOD-SEARCH-V1-HIFI | 企业查询 V1 高保真 | 高颖 + ui-agent |
| P0 | ENT-MOD-COMPARE-V1-HIFI | 对比篮 V1 高保真 | 高颖 + ui-agent |
| P0 | ENT-MOD-PROFILE-V1-HIFI | 企业详情 V1 高保真 | 高颖 + ui-agent |
| P0 | ENT-ARCH-IMPL-DESIGN | 企业功能实现架构设计 | 徐滕强 |
| P1 | ENT-PDR-MINUTES-TRIO | 补录三门 PDR 纪要（三模块） | 郭万迎 + coordinator |
| Stretch | ENT-MOD-*-V2-DEMO | V1 完成后进 V2 lumen 准生产 | 孔东团队 · lumen dev |

**待 PDR 模块**：不进 W29 committed；仅在高颖完成 USM+TRACE 后排门 1 会议。

---

## 5. Legacy 任务处置

| 旧 Task | 处置 |
|---------|------|
| `ENT-UE-IA-L01`~`L08` | `blocked` — 四菜单 IA 已废弃 |
| `FE-ENT-SEARCH-STATE-CLOSURE` | `blocked` — 待 SEARCH 模块 V2 后重做 |
| `FE-ENT-OVERVIEW-DRILLDOWN-ACTIONS` | `blocked` — 企业总览门1 未过 |
| `ENT-REQ-CONFIRM-01` | 保留历史；新流程以 PDR 三门为准 |
| `PM/UE-ENT-OVERVIEW-*` | 保留 `done` 作历史决策参考 |

---

## 6. 站会三问（企业专班）

1. **门1 三模块**：V1 进度？V2 何时开？ARCH 契约有无阻塞？
2. **待 PDR 模块**：哪几个 USM/TRACE 能在 Sprint N+1 上门 1？
3. **飞书看板**：committed task 是否已 sync？认领是否填 `supervised_by` 真名？

---

## 7. 相关文档

| 文档 | 用途 |
|------|------|
| `产品定义评审规程.md` | 三门 + V1/V2 标准 |
| `team-members.md` | 孔东/曹丽影/徐滕强/辜少彬分工 |
| `feishu-bitable-bidirectional-ops.md` | 看板 sync |
| `task-claiming-guide.md` | 认领字段 |
