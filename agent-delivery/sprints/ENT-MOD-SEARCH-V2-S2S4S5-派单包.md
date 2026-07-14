# ENT-MOD-SEARCH-V2 · 阶段 2 / 4 / 5 前端派单包

> **父任务**：`ENT-MOD-SEARCH-V2-DEMO`（孔东 · in_progress）  
> **前置**：`ENT-MOD-SEARCH-V2-S0` / `S1` 均已 **done**  
> **修订**：2026-07-14 晚 — **2B 并入 S2A**；`COMPONENTS` 仅阶段 3 高筛；**4.2 详情**改派 `ENT-MOD-PROFILE-V2-DEMO` → **曹丽影**  
> **修订**：2026-07-15 — 孔东确认：热门场景仅智能 Tab 且触发智能搜索；保存方案归 COMPONENTS；画像抽屉 footer 操作；推荐/结果卡对齐 demo；企业结果默认卡片无视图切换  
> **修订**：2026-07-15 晚 — 续修：企业无收藏；RegionSelect（选项可后台注入）；推荐对比篮已加入态；最近检索并入 Hub 按 Tab 过滤；导出确认弹窗+任务条对齐 demo；对比篮抽屉对齐 demo 并跳转 `/enterprise/enterprise-compare`（`max`=computed）  
> **仓**：`repos/lumen-ui-topic`  
> **规划真源**：`sprints/lumen-ui-topic-开发任务拆分规划.md`  
> **监管人**：`human:孔东`  

---

## 0. 本轮目标与样式铁律

交付 **通用组件层 → 查询/对比篮装配 + 详情（PROFILE）→ 集成验收**。

### 0.1 样式复刻铁律（全程生效，违反拒收）

| # | 要求 |
|---|---|
| 1 | **视觉以 `demo-ui-topic` 为真源**：布局、间距、字号、色块、卡片、Chip、空态、抽屉/页头、工具栏须对照复刻（Arco 可替换 shadcn，不得换皮成另一套后台）。 |
| 2 | **对照路径**：查询 `SearchPage`+`SearchScaffold`；详情 `EnterpriseProfilePage`+`ElementProfile`；对比篮 `EnterpriseCompareBasketPage`；高筛 `FilterPanel`。 |
| 3 | Design.md 与 demo 冲突时：**企业检索工作区优先对齐 demo**。 |
| 4 | 禁止 antd / React；禁止第二套 TraceInfoIcon。 |
| 5 | handoff 须附 **demo vs lumen 对照**（截图或勾选表）。 |

### 0.2 分工（2026-07-14 修订后）

```
S0/S1 done
    ├─→ S2A（孔东 / frontend-agent）：阶段2 全量组件（含原 2B Scaffold/Profile/2.6）
    ├─→ COMPONENTS（曹丽影）：仅阶段3 Filter*（目录 components/filter/）
    ├─→ PROFILE-V2-DEMO（曹丽影）：规划 4.2 企业详情整页（依赖 S2A）
    └─→ S4（孔东线）：4.1 查询 + 4.3 对比篮（详情不双写）
            └─→ S5：全链路（依赖 S4 + PROFILE）
```

---

## 1. Registry 任务一览

| task-id | 范围 | 状态 | Owner |
|---|---|---|---|
| `ENT-MOD-SEARCH-V2-S2A` | 阶段 2 全量（2.1–2.8，含原 2B） | `claimed` | 孔东 / frontend-agent |
| `ENT-MOD-SEARCH-V2-COMPONENTS` | **仅**阶段 3 高筛 | `claimed` | **曹丽影** |
| `ENT-MOD-PROFILE-V2-DEMO` | 规划 **4.2** 企业详情会签 | `claimed` | **曹丽影**（监管：孔东） |
| `ENT-MOD-SEARCH-V2-S4` | 4.1 查询 + 4.3 对比篮 | `blocked` | 孔东线 |
| `ENT-MOD-SEARCH-V2-S5` | 集成验收 | `blocked`（等 S4+PROFILE） | 孔东线 |

并行：S2A ∥ COMPONENTS（filter 目录隔离）；PROFILE 等 S2A 的 ElementProfile 合入后开工（可先读 demo 准备）。

---

## 2. 契约边界（防双写）

| 模块 | Owner |
|---|---|
| SearchScaffold / ElementProfile / 2.6 瘦身 / Hub / List / 跨流 chrome / 企业域卡 | **S2A** |
| FilterEngine / FilterPanel / ConditionBuilder / FilterTemplate* | **COMPONENTS** |
| `EnterpriseDetail.vue` + 画像会签 | **PROFILE-V2-DEMO（曹丽影）** |
| `EnterpriseSearch.vue` / `EnterpriseCompare.vue` + 菜单查询/对比 | **S4** |

---

## 3. 必读指针

| 优先级 | 路径 |
|---|---|
| P0 | 规划文档 §阶段 2/3/4/5；本派单包 |
| P0 | demo `components/search/**`、`FilterPanel`、`EnterpriseProfilePage`、`EnterpriseCompareBasketPage` |
| P0 | lumen `api/enterprise.ts`、`stores/compareBasket.ts`、`types/*` |
| P1 | Design.md §14；UX-UE §19；FE-LUMEN-V2-ALIGN 会签单 |

---

## 4. 架构铁律

1. 组件 → `api/enterprise.ts`；禁止直连 mock。  
2. demo 只读。Vue 3 + Arco Vue。D8/D9/D10。  
3. **样式复刻** §0.1。  
4. feature → PR → `dev`（直推须监管确认）。

---

## 5. 派单话术

### 5.1 `/goal` · ENT-MOD-SEARCH-V2-S2A（阶段 2 全量）

```markdown
/goal frontend-agent
任务 ID：ENT-MOD-SEARCH-V2-S2A
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支：feature/ent-search-v2-s2a
监管人：human:孔东
状态：已 claimed（agent:frontend-agent）

必读：规划 §2.0–2.8；本派单包 §0.1；demo SearchScaffold/Hub/List/Profile/common

目标（含原 2B）：
  2.1 SearchScaffold（装配器+组合，禁止巨石）
  2.2 SearchHub / 2.3 ResultList+ResultToolbar
  2.4 ElementProfile drawer|page（抽屉操作在 footer）
  2.5 Metric*/StatusTag/MockBadge/PendingBadge/ElementLogo（TraceInfoIcon 用 S0）
  2.6 CompareBasketDrawer / QueryConditionSummary / SearchExportWorkflow /
      QueryAssetPanel（仅最近历史） / useCandidateLists / recordUtils
  2.7 EntityIdentityHeader / MetricValueDisplay / EmptyState / WorkbenchPageHeader / SectionPanel
  2.8 CompareItemCard / AnalysisTypePicker / ProfileBreadcrumb

交互铁律（2026-07-15）：
  - 热门场景仅智能搜索 Tab；点击 → 智能解析（非高级筛选）
  - 保存方案不在 Scaffold；归 COMPONENTS Filter*
  - 推荐列表 / 结果卡片视觉对照 demo
  - 企业结果默认卡片，allowResultViewSwitch=false
  - 企业 rowActions 无收藏；推荐「加入对比篮」须反映 basket.has
  - 最近检索并入 SearchHub，与热门同级，按当前 Tab 过滤
  - 结果内城市用 RegionSelect（选项可 API 注入）
  - 导出：SearchExportWorkflow.confirm（弹窗+任务条）；记录页 Toast 占位
  - 对比篮抽屉对齐 demo；CTA → /enterprise/enterprise-compare?compareIds=…

硬约束：样式复刻 demo；不实现 Filter*（COMPONENTS）与业务 views（S4 查询页仍待；对比篮页骨架已由 S2A 挂路由）
DoD：见 registry ENT-MOD-SEARCH-V2-S2A
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-V2-S2A.md
```

### 5.2 `/goal` · ENT-MOD-SEARCH-V2-COMPONENTS（仅高筛 · 曹丽影）

```markdown
/goal frontend-agent（执行：human:曹丽影）
任务 ID：ENT-MOD-SEARCH-V2-COMPONENTS
分支建议：feature/ent-search-v2-components
监管人：human:孔东

范围（仅阶段 3）：
  FilterEngine / FilterPanel / ConditionBuilder / GroupNode /
  FilterTemplateManager / toBackendDSL·fromBackendDSL
  **含查询方案保存/加载/删除**（从 Scaffold 划出）
样式：复刻 demo FilterPanel + ConditionBuilder
禁止：SearchScaffold / Hub / List / ElementProfile / 业务页（已归 S2A / S4 / PROFILE）
目录：src/components/filter/**，避免与 S2A 的 search/ 冲突
DoD：见 registry
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-V2-COMPONENTS.md
```

### 5.3 `/goal` · ENT-MOD-SEARCH-V2-S4（查询 + 对比篮）

```markdown
/goal frontend-agent
任务 ID：ENT-MOD-SEARCH-V2-S4
前置：S2A + COMPONENTS done
目标：4.1 EnterpriseSearch + config；4.3 EnterpriseCompare；4.4 菜单落地
禁止双写 4.2（详情归 ENT-MOD-PROFILE-V2-DEMO）
样式复刻 demo SearchPage / CompareBasketPage
Handoff：…/ENT-MOD-SEARCH-V2-S4.md
```

### 5.4 `/goal` · ENT-MOD-SEARCH-V2-S5（集成）

```markdown
/goal frontend-agent
任务 ID：ENT-MOD-SEARCH-V2-S5
前置：S4 + ENT-MOD-PROFILE-V2-DEMO 均 done
目标：查询↔详情↔对比篮全链路；Mock 双路径；评审模式；会签材料
Handoff：…/ENT-MOD-SEARCH-V2-S5.md
```

### 5.5 `/goal` · ENT-MOD-PROFILE-V2-DEMO（4.2 详情 · 曹丽影）

```markdown
/goal frontend-agent（执行：human:曹丽影）
任务 ID：ENT-MOD-PROFILE-V2-DEMO
承接：规划 4.2 企业详情页
前置：S1 done；S2A 的 ElementProfile / ProfileBreadcrumb 可用（或约定 stub 合入点）
分支：feature/ent-profile-v2
监管人：human:孔东

必读：
  - demo EnterpriseProfilePage.tsx + ElementProfile
  - 规划 §4.2；FE-LUMEN-V2-ALIGN-ENT-PROFILE 会签单
  - lumen api getEnterpriseDetail / getEnterpriseProfile

目标：
  views/enterprise/EnterpriseDetail.vue（ElementProfile mode=page）
  多来源面包屑；搜索态/对比篮上下文携带
  关系链条 Tab（ECharts）；会签材料

硬约束：样式复刻 demo；复用 S2A 画像壳，不另起第二套
DoD：见 registry ENT-MOD-PROFILE-V2-DEMO
Handoff：会签单 + 可选 agent-handoffs/企业战略分析-ENT/ENT-MOD-PROFILE-V2-DEMO.md
```

---

## 6. 验收清单

### S2A
- [ ] 2.1–2.8 齐全；Scaffold 非巨石  
- [ ] 热门场景仅智能 Tab 且触发智能搜索  
- [ ] 无「保存方案」于关键字/智能路径；最近检索在 Hub 且按 Tab 过滤  
- [ ] 企业无收藏；推荐对比篮按钮已加入态正确  
- [ ] RegionSelect 对齐 demo；选项可注入  
- [ ] 导出确认弹窗 + 任务条对齐 demo  
- [ ] 对比篮抽屉对齐 demo；跳转对比篮页；标题 n/max 非 undefined  
- [ ] 画像抽屉 footer 操作对齐 demo  
- [ ] 推荐列表 / 结果卡片对照 demo；无视图切换  
- [ ] demo 对照（Scaffold/Hub/List/画像头/篮/导出/空态）  
- [ ] handoff + cost + PR  

### COMPONENTS
- [ ] 仅 filter 目录；AND/OR + 模板（**含保存方案**）  
- [ ] demo 高筛对照  
- [ ] handoff + cost  

### PROFILE
- [ ] EnterpriseDetail 可进；上下文携带  
- [ ] demo 详情对照；会签材料  
- [ ] 复用 S2A ElementProfile  

### S4 / S5
- [ ] 查询+对比篮装配；不双写详情  
- [ ] S5 全链路含详情  

---

## 7. 人机分工

| 角色 | 动作 |
|---|---|
| **孔东** | S2A / S4 / S5；监管曹丽影 COMPONENTS + PROFILE |
| **曹丽影** | COMPONENTS（高筛）+ PROFILE-V2-DEMO（4.2 详情） |
| **frontend-agent** | 按 `/goal` 执行；写 handoff |

---

## 8. 解锁关系

```
S2A done ──┬─→ S4（+ COMPONENTS done）──┐
           ├─→ PROFILE（曹丽影）─────────┼─→ S5 → SEARCH DEMO 会签
COMPONENTS ─┘                           │
                                        └─→ PROFILE 会签（独立）
```
