# ENT-MOD-SEARCH-V2 · 阶段 2 / 4 / 5 前端派单包

> **父任务**：`ENT-MOD-SEARCH-V2-DEMO`（孔东 · in_progress）  
> **前置**：`ENT-MOD-SEARCH-V2-S0` / `S1` 均已 **done**（地基 + 接口层已在 `origin/dev`）  
> **兄弟任务**：`ENT-MOD-SEARCH-V2-COMPONENTS`（曹丽影 · claimed；承接阶段 2B + 阶段 3 高筛）  
> **仓**：`repos/lumen-ui-topic`（生产仓；默认 feature 分支 + PR → `dev`；直推 `dev` 须监管人书面确认）  
> **规划真源**：`sprints/lumen-ui-topic-开发任务拆分规划.md`（2026-07-14 增补 §阶段 2.0–2.9）  
> **派单日期**：2026-07-14  
> **监管人**：`human:孔东`  
> **状态**：registry 已登记；待各任务认领后执行

---

## 0. 本轮目标与样式铁律

本轮交付 **通用组件层 → 三业务页装配 → 集成验收**，使企业查询 / 企业详情 / 对比篮在 lumen 达到可演示准生产水位。

### 0.1 样式复刻铁律（全程生效，违反拒收）

| # | 要求 |
|---|---|
| 1 | **视觉以 `demo-ui-topic` 为真源**：布局结构、间距密度、字号层级、色块分区、卡片圆角、标签/Chip 形态、空态、抽屉/页头、结果工具栏控件排布，须与原型站对应页 **对照复刻**（允许 Arco 控件替换 shadcn，但观感不得「换皮成另一套后台」）。 |
| 2 | **对照路径**（只读）：查询 `SearchPage`+`SearchScaffold`；详情 `EnterpriseProfilePage`+`ElementProfile`；对比篮 `EnterpriseCompareBasketPage`。组件级对照见规划 §2.0 与本包 §3。 |
| 3 | **Design.md / Arco 主题**：全局 token（主色 `#165DFF`、页面底 `#D8E7FC`、控件高 32px、正文 14px）与 demo 冲突时：**企业检索工作区优先对齐 demo 已定稿视觉**；全局壳（顶栏/侧栏）已按 S0 对齐 demo Persona 区。 |
| 4 | **禁止**：另起一套「通用后台风格」；禁止引入 antd / React；禁止把 demo CSS Modules 原样拷贝却不改写为 Vue SFC + UnoCSS/Arco。 |
| 5 | **验收证据**：handoff 须附 **demo vs lumen 同屏对照说明**（关键区域截图或逐项勾选表：Hub / 结果卡 / 工具栏 / 画像头 / 对比篮卡 / 空态）。 |

### 0.2 为什么拆 S2A / COMPONENTS / S4 / S5

```
S0/S1 done
    ├─→ S2A（孔东线）：跨流 chrome + Hub/List + 企业域卡/面包屑
    ├─→ COMPONENTS（曹丽影）：Scaffold 瘦身装配 + ElementProfile + 阶段3 高筛
    └─→ S2A ∩ COMPONENTS 契约对齐后
            └─→ S4 三页装配 → S5 集成验收 → 解锁 DEMO 会签剩余项
```

---

## 1. Registry 任务一览

| task-id | 标题 | 工时 | 依赖 | 执行建议 |
|---|---|---|---|---|
| `ENT-MOD-SEARCH-V2-S2A` | 阶段 2A：跨流展示 + SearchHub/Result* + 企业域 chrome | 1.5–2 天 | `S1` done | 孔东 / `frontend-agent`（监管：孔东） |
| `ENT-MOD-SEARCH-V2-COMPONENTS` | 阶段 2B+3：Scaffold/Profile/瘦身 + 高级筛选 | 3–4 天 | 软依赖 `S0/S1` types+api（已满足） | **曹丽影**（已 claimed；本包刷新范围与样式铁律） |
| `ENT-MOD-SEARCH-V2-S4` | 阶段 4：企业查询 / 详情 / 对比篮页面装配 | 2–3 天 | `S2A` + `COMPONENTS` | 孔东 / `frontend-agent` |
| `ENT-MOD-SEARCH-V2-S5` | 阶段 5：全链路集成与验收 | 1 天 | `S4` | 孔东 / `frontend-agent` + Lead 签收 |

并行：

- **S2A 与 COMPONENTS 可并行**（契约见 §2）；S2A 优先交付 2.5/2.7，供 Profile/List 挂载。
- **S4 不得早于** COMPONENTS 的 SearchScaffold + FilterPanel 可用 stub/真实现至少一侧可装配。

---

## 2. 契约边界（防双写）

| 模块 | Owner | 消费方 |
|---|---|---|
| `Metric*` / `StatusTag` / `EntityIdentityHeader` / `MetricValueDisplay` / `EmptyState*` / `SectionPanel` / `WorkbenchPageHeader` | **S2A** | COMPONENTS、S4 |
| `CompareBasketDrawer` / `QueryConditionSummary` / `SearchExportWorkflow` / `QueryAssetPanel` / `useCandidateLists` | **COMPONENTS（2.6）** | Scaffold、S4 查询页 |
| `SearchScaffold` / `ElementProfile` / Filter* | **COMPONENTS** | S4 |
| `SearchHub` / `ResultList` / `ResultToolbar` | **S2A** | Scaffold 组合、总览下钻可复用 |
| `CompareItemCard` / `AnalysisTypePicker` / `ProfileBreadcrumb` | **S2A（2.8）** | S4.3 / S4.2 |
| `views/enterprise/*` + `config/enterpriseSearch.ts` | **S4** | S5 |

Props/emit 以 `types/search.ts` + `types/filter.ts`（S0）为准；新增 props 须先改类型再改组件。

---

## 3. 必读指针

| 优先级 | 路径 |
|---|---|
| P0 | `agent-delivery/sprints/lumen-ui-topic-开发任务拆分规划.md` §阶段 2.0–2.9、§阶段 4、§阶段 5 |
| P0 | 本派单包 |
| P0 | `repos/demo-ui-topic/src/app/components/search/**`（Scaffold/Hub/List/Toolbar/Profile） |
| P0 | `repos/demo-ui-topic/src/app/components/common/**`（Metric*/StatusTag/CompareBasket） |
| P0 | `repos/demo-ui-topic/src/app/pages/development/SearchPage.tsx` |
| P0 | `repos/demo-ui-topic/src/app/pages/development/EnterpriseProfilePage.tsx` |
| P0 | `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx` |
| P0 | `repos/lumen-ui-topic/src/api/enterprise.ts`、`stores/compareBasket.ts`、`types/*`（S0/S1 产物） |
| P1 | `agent-delivery/Design.md` §4/§5/§7/§14 |
| P1 | `agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md` §19 |
| P1 | `agent-handoffs/产品整体定义/UI-HIFI-ENT-SEARCH-会签单.md`、`FE-LUMEN-V2-ALIGN-ENT-SEARCH-会签单.md` |
| P1 | `repos/demo-ui-topic/docs/ia/enterprise/ENT-search-design.md` |

**禁读**：招标 PDF。**禁止扩范围**：企业总览巨页、评估模块真后端、政策要素检索（可留插槽）。

---

## 4. 架构铁律（派单必带）

1. 算法只在 Python；本任务不涉及。  
2. 调用链：组件 → `api/enterprise.ts` → Java；**禁止组件直引 `mock/enterprise`**。  
3. demo-ui-topic **只读参照**，禁止 merge。  
4. Vue 3 + `@arco-design/web-vue`；D8/D9/D10 合规；Mock 挂 🧪、指标挂 `metricId`+ⓘ。  
5. CI：feature → PR → `dev`（除非监管人明确要求直合）。  
6. **样式复刻**：见 §0.1。

---

## 5. 派单话术（复制到新会话）

### 5.1 `/goal` · ENT-MOD-SEARCH-V2-S2A（阶段 2A）

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + Vite + @arco-design/web-vue / TypeScript / Pinia；组件化复用、视觉严格复刻 demo 原型、只经 api 层调数据。

任务 ID：ENT-MOD-SEARCH-V2-S2A
父任务：ENT-MOD-SEARCH-V2-DEMO
前置：ENT-MOD-SEARCH-V2-S0 / S1 均为 done
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支策略：feature/ent-search-v2-s2a → PR 合入 dev（直推须孔东确认）
监管人：human:孔东
认领：确认 status=ready → 写入 claimed_by/supervised_by/lock_until 后再改代码

必读：
  - agent-delivery/sprints/lumen-ui-topic-开发任务拆分规划.md §2.2/2.3/2.5/2.7/2.8
  - agent-delivery/sprints/ENT-MOD-SEARCH-V2-S2S4S5-派单包.md §0.1 样式铁律 + §2 契约
  - repos/demo-ui-topic/src/app/components/search/{SearchHub,ResultList,ResultToolbar}.tsx
  - repos/demo-ui-topic/src/app/components/common/{MetricCard,MetricSpecCard,StatusTag}.tsx
  - repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx（对比卡/空态/页头）
  - Design.md §14；UX-UE 交互规范 §19
  - 禁扩：SearchScaffold 整壳、FilterPanel、业务 views（属 COMPONENTS / S4）

目标（阶段 2A）：
  2.5 common：MetricCard / MetricSpecCard / MockBadge / StatusTag(+Chip) / PendingBadge / ElementLogo
      —— TraceInfoIcon 复用 S0 review 版，禁止第二套
  2.7 跨流：EntityIdentityHeader / MetricValueDisplay / EmptyStateWithActions /
      WorkbenchPageHeader / SectionPanel / JudgmentStrip
  2.2 SearchHub.vue（样式对齐 demo SearchHub）
  2.3 ResultList.vue + ResultToolbar.vue（头部用 EntityIdentityHeader；分数用 MetricValueDisplay；对比联动 compareBasket）
  2.8 enterprise：CompareItemCard / AnalysisTypePicker / ProfileBreadcrumb + config/enterpriseBreadcrumb.ts

硬约束：
  - 样式复刻 demo；handoff 附对照勾选（Hub/List/Toolbar/对比卡/空态）
  - 组件不直连 mock；行级对比走 stores/compareBasket
  - npm run type-check + build-only 通过

DoD：见 task-registry ENT-MOD-SEARCH-V2-S2A
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-V2-S2A.md
CI：frontend build 绿；PR → dev
```

### 5.2 `/goal` · ENT-MOD-SEARCH-V2-COMPONENTS（阶段 2B + 阶段 3 · 曹丽影）

```markdown
/goal frontend-agent（执行人：human:曹丽影 主导；可辅以 agent）
身份：资深前端；Vue 3 + Arco；config-driven 搜索壳；高级筛选 DSL；视觉复刻 demo SearchScaffold / FilterPanel / ElementProfile。

任务 ID：ENT-MOD-SEARCH-V2-COMPONENTS
父任务：ENT-MOD-SEARCH-V2-DEMO
前置：S0/S1 done（types + api/enterprise 已在 origin/dev）
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支：与孔东约定 feature 分支，避免与 S2A 同文件冲突（Scaffold vs Hub/List 目录边界见派单包 §2）
监管人：human:孔东

必读：
  - 规划文档 §2.1/2.4/2.6 + §阶段 3
  - ENT-MOD-SEARCH-V2-S2S4S5-派单包.md §0.1 样式铁律
  - demo-ui-topic SearchScaffold.tsx / ElementProfile.tsx / FilterPanel.tsx / ConditionBuilder.tsx
  - lumen api/enterprise.ts、types/search|filter.ts
  - S2A 若已合入：优先消费 EntityIdentityHeader / Metric*；未合入则 stub + TODO 对接

目标：
  2.1 SearchScaffold.vue —— 只做状态协调与装配；禁止再写 demo 级巨石单文件
  2.4 ElementProfile.vue —— mode=drawer|page 同源；头部对齐 demo
  2.6 瘦身：CompareBasketDrawer / QueryConditionSummary / SearchExportWorkflow(+useSearchExportTasks) /
      QueryAssetPanel / useCandidateLists / recordUtils
  3.x FilterEngine / FilterPanel / ConditionBuilder / FilterTemplateManager / 序列化

硬约束：
  - 样式复刻 demo（Scaffold 布局、高级筛字段库双形态、画像抽屉/整页）
  - 接口只经 api/enterprise.ts；挂 TraceInfoIcon（S0）
  - Hub/ResultList/Toolbar 由 S2A 交付则组合引用，勿双写
  - npm run build 通过

DoD：见 task-registry ENT-MOD-SEARCH-V2-COMPONENTS（已刷新）
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-V2-COMPONENTS.md
  必含：demo 对照截图/勾选、Scaffold 文件行数或模块清单（证明已瘦身）
```

### 5.3 `/goal` · ENT-MOD-SEARCH-V2-S4（阶段 4）

```markdown
/goal frontend-agent
身份：资深前端；页面装配者——薄 views + 厚 components；视觉与 demo 三页 1:1 可对照。

任务 ID：ENT-MOD-SEARCH-V2-S4
父任务：ENT-MOD-SEARCH-V2-DEMO
前置：ENT-MOD-SEARCH-V2-S2A 与 ENT-MOD-SEARCH-V2-COMPONENTS 均 done（或 Lead 书面允许 stub 合入）
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支：feature/ent-search-v2-s4 → PR → dev
监管人：human:孔东

必读：
  - 规划文档 §阶段 4
  - ENT-MOD-SEARCH-V2-S2S4S5-派单包.md
  - demo SearchPage / EnterpriseProfilePage / EnterpriseCompareBasketPage
  - demo enterpriseSearchConfig + enterpriseProfileTabs（迁为 config/enterpriseSearch.ts）

目标：
  4.1 views/enterprise/EnterpriseSearch.vue + config/enterpriseSearch.ts
      —— 装配 SearchScaffold；URL mode/q/preset/source；样式对齐 demo 查询页
  4.2 views/enterprise/EnterpriseDetail.vue
      —— ElementProfile mode=page；ProfileBreadcrumb；返回保留搜索态/对比篮
  4.3 views/enterprise/EnterpriseCompare.vue
      —— CompareItemCard + AnalysisTypePicker；空篮 EmptyStateWithActions；分发评估 Mock
  4.4 router/menu 落地：替换 DevelopingView 占位为三页真组件

硬约束：
  - 三页视觉复刻 demo；handoff 附三页对照
  - Mock 开关双路径；不直连 mock 目录
  - npm run type-check + build-only 通过

DoD：见 task-registry ENT-MOD-SEARCH-V2-S4
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-V2-S4.md
```

### 5.4 `/goal` · ENT-MOD-SEARCH-V2-S5（阶段 5）

```markdown
/goal frontend-agent
身份：资深前端 + 集成验收执行者；证据优先，不扩功能。

任务 ID：ENT-MOD-SEARCH-V2-S5
前置：ENT-MOD-SEARCH-V2-S4 done
仓库：${GKX_ROOT}/repos/lumen-ui-topic
监管人：human:孔东

目标（验收，非大功能开发）：
  5.1 查询→画像抽屉→整页详情→对比篮→回查询 全链路；搜索态保留
  5.2 VITE_APP_USE_MOCK=true/false 双路径冒烟
  5.3 reviewMode：Persona 切换、TraceInfoIcon/MetricSpecCard ⓘ 显隐正确
  5.4 npm run lint（任务触及文件）+ type-check + build 绿
  5.5 补齐 DEMO 会签材料：commit SHA、对照说明、已知问题；开/合 PR 按仓策略

硬约束：发现样式/交互偏离 demo → 记缺陷回 S2A/COMPONENTS/S4，本任务不顺手大改架构

DoD：见 task-registry ENT-MOD-SEARCH-V2-S5
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-V2-S5.md
  必含：验收勾选表、双路径结果、评审模式结果、demo 对照结论、cost 回填
```

---

## 6. 验收清单（Coordinator / Lead 签收）

### S2A

- [ ] 2.5 / 2.7 / 2.2 / 2.3 / 2.8 产物齐全  
- [ ] 无第二套 TraceInfoIcon  
- [ ] 样式对照 demo：Hub / 结果卡 / 工具栏 / 对比卡 / 空态  
- [ ] 对比按钮联动 `compareBasket`  
- [ ] handoff + cost + PR  

### COMPONENTS

- [ ] Scaffold 为装配器 + 2.6 子模块，非巨石  
- [ ] ElementProfile drawer/page 同源；样式对齐 demo  
- [ ] 高筛 AND/OR 嵌套 + 模板存取  
- [ ] 只经 `api/enterprise.ts`；TraceInfoIcon 正确  
- [ ] 样式对照：Scaffold 总布局 / Filter 双形态 / 画像头  
- [ ] handoff + cost + PR  

### S4

- [ ] 三页替换占位；菜单可点  
- [ ] URL 初始化搜索态；详情面包屑多来源  
- [ ] 对比篮空态与分发评估 Mock  
- [ ] 三页 demo 对照通过  
- [ ] handoff + cost + PR  

### S5

- [ ] 全链路 + 双路径 + 评审模式勾选通过  
- [ ] build/type-check 绿  
- [ ] DEMO 会签材料可提交评审  

---

## 7. 人机分工与认领提示

| 角色 | 动作 |
|---|---|
| **孔东** | 确认本派单包 → 认领/派 S2A → 协调曹丽影 COMPONENTS 边界 → S4/S5 签收 |
| **曹丽影** | 按 §5.2 推进 COMPONENTS；样式复刻；与 S2A 目录边界勿冲突 |
| **frontend-agent** | 按各 `/goal` DoD 实现；写 handoff；cost 回填 |
| **coordinator** | 依赖满足后改 `ready`/`done`；S5 done 后推动 DEMO 会签收口 |

**认领字段模板**：

```yaml
status: claimed
claimed_by: agent:frontend-agent   # 或 human:孔东 / human:曹丽影
supervised_by: human:孔东
claim_type: pull
claimed_at: "2026-07-14T22:00:00+08:00"
lock_until: "2026-07-15T02:00:00+08:00"
```

---

## 8. 完成后对父任务的解锁

```
S2A done ──┐
           ├─→ S4 ready → S4 done → S5 ready → S5 done
COMPONENTS done ─┘                              │
                                                 └─→ ENT-MOD-SEARCH-V2-DEMO 会签剩余 DoD
```

父任务 `ENT-MOD-SEARCH-V2-DEMO` 保持 `in_progress` 直至会签单签字；S2A/S4/S5/COMPONENTS 为子交付。
