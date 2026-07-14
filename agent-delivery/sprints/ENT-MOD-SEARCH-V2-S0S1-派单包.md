# ENT-MOD-SEARCH-V2 · 阶段 0/1 前端派单包

> **父任务**：`ENT-MOD-SEARCH-V2-DEMO`（孔东 · in_progress）  
> **兄弟任务**：`ENT-MOD-SEARCH-V2-COMPONENTS`（曹丽影 · claimed；依赖本包 S0 的 types 契约）  
> **仓**：`repos/lumen-ui-topic`（生产仓，feature 分支 + PR → `dev`，禁止直推 main/dev）  
> **规划真源**：`sprints/lumen-ui-topic-开发任务拆分规划.md`（2026-07-14 修订）  
> **派单日期**：2026-07-14  
> **监管人**：`human:孔东`  
> **状态**：待认领执行（registry `status: ready`）

---

## 0. 为什么先做 S0/S1

`ENT-MOD-SEARCH-V2-DEMO` 页面装配与 `ENT-MOD-SEARCH-V2-COMPONENTS` 组件开发，共同依赖：

| 依赖项 | 解锁对象 |
|---|---|
| 全局 `USE_MOCK` + `defineApi` | 全部 `api/*.ts`、组件内 mock/真接口切换 |
| demo 对齐的用户/角色/评审 store | 顶栏、TraceInfoIcon、评审态菜单 |
| `types/enterprise|search|filter|perms` | COMPONENTS 与页面装配的契约 |
| 舍弃旧菜单 + 企业查询骨架路由 | 后续 4.x 页面挂载点 |
| `api/enterprise.ts` + mock + 对比篮 store | 阶段 2/4 联调 |

**本轮增量决策（开工必读）**：

1. 右上角**用户信息与角色信息模块**完全参照 `demo-ui-topic` 的样式与内容（`PersonaLevelSwitcher` + `CurrentUserProvider` 模型）。
2. `lumen-ui-topic` **现有菜单与角色可完全舍弃**，重建企业查询骨架；禁止继续扩展旧 `userRoles` / 八大专题 `navGroups`。

---

## 1. Registry 子任务一览

| task-id | 标题 | 工时 | 依赖 | 执行建议 |
|---|---|---|---|---|
| `ENT-MOD-SEARCH-V2-S0` | 阶段 0：Mock 工厂 + demo 用户/角色 + 类型 + 菜单重建 | 1.5–2 天 | `ENT-MOD-SEARCH-V1-HIFI` | 孔东 / frontend-agent（监管：孔东） |
| `ENT-MOD-SEARCH-V2-S1` | 阶段 1：企业 API + Mock 数据 + 对比篮 store | 1 天 | `ENT-MOD-SEARCH-V2-S0` | 同上；S0 done 后开工 |

并行说明：

- S0 内 **0.3 类型可优先合入**，提前解锁曹丽影 `ENT-MOD-SEARCH-V2-COMPONENTS`。
- S1 必须等 S0 的 `defineApi` + 领域类型落地后再派执行会话。

---

## 2. 架构铁律（派单必带）

1. 算法只在 Python；本任务不涉及算法。
2. 调用链：前端 → Java REST → Python `/internal/*`（本阶段 mock 开关在 api 层，不直连 Python/DB）。
3. 图谱：NebulaGraph；本阶段不接图谱。
4. 可观测性：沿用/补齐前端 observability（traceId）；不删已有埋点钩子。
5. CI/CD：feature 分支 PR → Pipeline 绿 → 合入 `dev`。
6. demo-ui-topic **只读参照**，禁止 merge 进 lumen。
7. 前端规范：Vue 3 + `@arco-design/web-vue` + Design.md token；**禁引 antd / React 组件**。
8. 数据血缘：指标卡预留 `metricId`；Mock 数据后续挂 🧪（阶段 2 通用组件落地）。
9. 交互：D10 交互规范；顶栏 Persona 切换须保留键盘可达与 Arco 语义。

---

## 3. 必读指针

| 优先级 | 路径 |
|---|---|
| P0 | `agent-delivery/sprints/lumen-ui-topic-开发任务拆分规划.md` §2.1–2.2、§阶段 0/1 |
| P0 | `repos/demo-ui-topic/src/app/perms/types.ts` |
| P0 | `repos/demo-ui-topic/src/app/perms/CurrentUserProvider.tsx` |
| P0 | `repos/demo-ui-topic/src/app/components/common/PersonaLevelSwitcher.tsx` |
| P0 | `repos/demo-ui-topic/src/app/components/search/types.ts`（及 filter DSL 类型） |
| P0 | `repos/lumen-ui-topic/src/layouts/DefaultLayout.vue`、`src/router/menu.ts`、`src/api/auth.ts`、`src/utils/request.ts` |
| P1 | `agent-delivery/Design.md`（§4/§5/§6/§13/§14） |
| P1 | `agent-delivery/architecture-baseline.md`（D8） |
| P1 | `agent-delivery/decisions/DECIDE-FE-V2-LUMEN-DIRECT-2026-07-12.md` |
| P1 | `agent-handoffs/产品整体定义/FE-LUMEN-V2-ALIGN-ENT-SEARCH-会签单.md` |

---

## 4. 派单话术（复制到新会话）

### 4.1 `/goal` · ENT-MOD-SEARCH-V2-S0（阶段 0）

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + Vite + @arco-design/web-vue / TypeScript / Pinia；组件化复用、只经网关调 Java、沿用 observability，不直连 Python/DB。本任务为 React demo → Vue lumen 的工程化重写地基，禁止把 React 组件原样拷贝进 lumen。

任务 ID：ENT-MOD-SEARCH-V2-S0
父任务：ENT-MOD-SEARCH-V2-DEMO
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支策略：从最新 dev 拉 feature/ent-search-v2-s0（或孔东指定分支）→ PR 合入 dev；禁止直推 main/dev
监管人：human:孔东
认领：先确认 status=ready 且 claimed_by 为空 → 写入 claimed_by/supervised_by/lock_until 后再改代码

必读：
  - agent-delivery/sprints/lumen-ui-topic-开发任务拆分规划.md（§2.1 Mock 工厂、§2.2 用户/角色对齐 demo、阶段 0 验收）
  - agent-delivery/sprints/ENT-MOD-SEARCH-V2-S0S1-派单包.md（本包）
  - repos/demo-ui-topic/src/app/perms/{types.ts,CurrentUserProvider.tsx}
  - repos/demo-ui-topic/src/app/components/common/PersonaLevelSwitcher.tsx
  - repos/demo-ui-topic/src/app/components/search/types.ts
  - agent-delivery/Design.md §14；architecture-baseline.md D8
  - 禁读：招标 PDF；禁止扩范围到阶段 2+ 页面实现

目标（阶段 0 四件套）：
  0.1 全局 USE_MOCK（VITE_APP_USE_MOCK）+ utils/http.ts defineApi；用 defineApi 重构 api/auth.ts（行为不变）
  0.2 完全参照 demo-ui-topic 右上角用户/角色：types/perms.ts + stores/review.ts + components/review/PersonaLevelSwitcher.vue + TraceInfoIcon.vue；舍弃 userRoles/selectedRoleKey
  0.3 领域类型 types/{enterprise,search,filter}.ts（优先合入，解锁 COMPONENTS）
  0.4 舍弃现有 navGroups 八大专题菜单；重建「企业分析」组（企业查询/详情占位/对比篮）；默认落地企业查询占位

硬约束：
  - 顶栏 Persona/Level/评审模式样式与内容对齐 demo（非旧 6 角色文案）
  - grep 验证：src 内无 userRoles、领导驾驶舱用户、旧专题侧栏配置残留
  - demo-ui-topic 只读；Vue + Arco Vue 重写
  - npm run build（及仓内已有 type-check/lint）通过

DoD：见 task-registry ENT-MOD-SEARCH-V2-S0
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-V2-S0.md
  必含：产物清单、旧菜单/角色清理证据（grep）、与 demo 顶栏对照说明、PR 链接、cost 回填
CI：frontend build 绿；PR → dev
```

### 4.2 `/goal` · ENT-MOD-SEARCH-V2-S1（阶段 1）

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + TypeScript + Pinia + axios 封装；api 层函数级 mock 开关、领域契约先行，不在组件内散落 fetch。

任务 ID：ENT-MOD-SEARCH-V2-S1
父任务：ENT-MOD-SEARCH-V2-DEMO
前置：ENT-MOD-SEARCH-V2-S0 必须 status=done（defineApi + 领域类型已合入）
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支策略：feature/ent-search-v2-s1 → PR 合入 dev
监管人：human:孔东

必读：
  - agent-delivery/sprints/lumen-ui-topic-开发任务拆分规划.md §阶段 1
  - agent-delivery/sprints/ENT-MOD-SEARCH-V2-S0S1-派单包.md
  - repos/lumen-ui-topic/src/utils/http.ts（S0 产物）
  - repos/lumen-ui-topic/src/types/{enterprise,search,filter}.ts（S0 产物）
  - repos/demo-ui-topic/src/app/mock/enterprise/**（mock 迁移真源）
  - Design.md §14；data-lineage-policy.md（字段挂 metricId / pending 标记）

目标（阶段 1 三件套）：
  1.1 src/api/enterprise.ts：searchEnterprises / getEnterpriseDetail / getEnterpriseProfile / exportEnterpriseList / getEnterpriseAggregates；全部 defineApi(real+mock)
  1.2 src/mock/enterprise/*：从 demo 迁移 ≥30 条企业 mock + filterFieldSchema + smartParser + portalAggregates
  1.3 src/stores/compareBasket.ts：elementKey 隔离、MAX_ITEMS=12、useStorage 持久化、超限 Arco Message

硬约束：
  - mock 纯函数导出，由 api/enterprise 引用；禁止组件直引 mock 文件作为数据源旁路
  - VITE_APP_USE_MOCK=true/false 两条路径签名一致
  - 不实现 SearchScaffold / 业务页面（属 COMPONENTS / DEMO 后续阶段）
  - npm run build 通过

DoD：见 task-registry ENT-MOD-SEARCH-V2-S1
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-V2-S1.md
  必含：API 清单、mock 条数与字段覆盖、对比篮验收步骤、PR 链接、cost 回填
CI：frontend build 绿；PR → dev
```

---

## 5. 验收清单（Coordinator / Lead 签收）

### S0

- [ ] `USE_MOCK` / `defineApi` 可用；登录 mock 回归通过  
- [ ] 顶栏与 demo PersonaLevelSwitcher 对照通过（Persona 列表 + Level + 评审开关）  
- [ ] 旧 `userRoles` / 八大专题侧栏已删除  
- [ ] 企业分析三路由占位可进  
- [ ] `types/{perms,enterprise,search,filter}.ts` 可供 COMPONENTS 引用  
- [ ] handoff + cost 回填 + PR 绿  

### S1

- [ ] `api/enterprise.ts` 五接口均 `defineApi`  
- [ ] mock ≥30 条 + 字段库/智能解析/聚合  
- [ ] 对比篮 store 隔离与超限提示  
- [ ] mock 开/关签名一致  
- [ ] handoff + cost 回填 + PR 绿  

---

## 6. 人机分工与认领提示

| 角色 | 动作 |
|---|---|
| **孔东（前端 Lead / 监管）** | 确认本派单包 → 用 `update-task-status` 认领 S0 → 开 frontend-agent 会话粘贴 §4.1 → 评审 PR → 签收 handoff |
| **frontend-agent** | 按 DoD 实现；不扩到阶段 2+；写 handoff |
| **曹丽影** | S0 类型合入后即可推进 COMPONENTS；勿依赖旧 menu/userRoles |
| **coordinator** | S0/S1 handoff 齐且 DoD 满足后改 `done`；再放行 DEMO 页面装配冲刺 |

**认领字段模板**（监管确认后写入 registry）：

```yaml
status: claimed
claimed_by: human:孔东   # 或 agent:frontend-agent
supervised_by: human:孔东
claim_type: pull
claimed_at: "2026-07-14T14:00:00+08:00"
lock_until: "2026-07-14T18:00:00+08:00"
```

---

## 7. 完成后对父任务的解锁

```
S0 done ──┬─→ COMPONENTS（曹丽影）可按 types 契约全速
          └─→ S1 ready → S1 done → DEMO 阶段 2/4 页面装配可启动
```

父任务 `ENT-MOD-SEARCH-V2-DEMO` 保持 `in_progress`；S0/S1 为子交付，不替代父任务会签 DoD。
