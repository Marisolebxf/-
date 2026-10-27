# LUMEN-INTEL-FE-L0 · handoff

## 认领信息

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| repo / branch | `repos/lumen-ui-topic` · `dev`（commit `a53cf83`，走查通过后已推 origin/dev） |
| ponytail | `full` |

## 范围与实现（DoD 对照）

综合智能分析菜单/路由/权限接入（E8 三叶 9 路由），总纲 `API-SYNTH-INTEL-REPLICA-PLAN.md` §3。

| DoD | 交付 |
|---|---|
| 权限矩阵补 ELEMENTS/COLLAB 两码 + L2 挂载 | ✅ `src/perms/matrix.ts`：`MENU_INTEL_ELEMENTS` / `MENU_INTEL_COLLAB` 入 `PERM_CODES`，三码均挂 L2 层（对齐 demo perms/matrix.ts #76–78/157–159） |
| NavIconKey 扩展 + 综合智能分析分组 | ✅ `src/router/menu.ts`：`NavIconKey` 加 `'intelligence'`；navGroups 尾部新增分组（3 工作台菜单项 + 6 隐藏路由：3×`tasks/:taskId` + 3×`report`），组件走 `developingComponent` 占位，L1B/VIT/ELEM/COLLAB 落页后替换 |
| 侧栏图标 | ✅ `src/layouts/DefaultLayout.vue`：`navIconMap` 加 `intelligence: IconBulb`（对齐 demo Layout.tsx IconBulb #160）+ import |
| selfcheck | ✅ `src/router/menu.selfcheck.mjs` 追加 intel-shell 段（分组/9 路由/权限码/图标映射断言） |

路由清单（9 条，均 `requiresAuth` + 各叶权限码）：

- `/intelligence/vitality` · `/intelligence/vitality/tasks/:taskId` · `/intelligence/vitality/report`
- `/intelligence/elements` · `/intelligence/elements/tasks/:taskId` · `/intelligence/elements/report`
- `/intelligence/collaboration` · `/intelligence/collaboration/tasks/:taskId` · `/intelligence/collaboration/report`

## 顺带修复（非本单范围，根因修复）

`menu.selfcheck.mjs` policy 段两条存量断言在 `8ddd74b`（algorithm-agent 改 policy 页文案「禁止空跑」→「不可空跑提交」、删 `require-graph-vid` 守卫改「禁止把 CL-* 当产业」）后即失败，先于本单改动存在（stash 验证确认）。按现状对齐：

- `/禁止空跑/` → `/不可空跑提交/`
- `/require-graph-vid/` → `/禁止把 CL-\* 当产业/`

## 产物清单（lumen-ui-topic，commit `a53cf83` · origin/dev）

- `src/perms/matrix.ts`（+4 行）
- `src/router/menu.ts`（+82 行：类型 1 行 + 分组 81 行）
- `src/layouts/DefaultLayout.vue`（+2 行）
- `src/router/menu.selfcheck.mjs`（intel 段 +23 行；policy 存量修复 2 行）

## 验收证据

- `node src/router/menu.selfcheck.mjs` → `menu.selfcheck intel-shell ok` + svc/policy 段全绿（含存量断言修复）
- `pnpm type-check`（vue-tsc --build）→ exit 0
- `pnpm build` → ✓ built in 19.09s（exit 0）
- 侧栏渲染：L2 用户可见「综合智能分析」分组三菜单；门户嵌入模式 URL 反查（`portalUrlCoversNav`）对 `/intelligence/*` 天然生效，无需 portal 侧改动

## 架构合规自检（公约 §2）

| # | 铁律 | 结论 |
|---|------|------|
| D8 | Arco 栈 | ✅ IconBulb 走 `@arco-design/web-vue/es/icon`，未加依赖 |
| D12 | demo 隔离 | ✅ 纯路由/权限声明，无 demo 引用（selfcheck `doesNotMatch demo-svc-/demo-ui-` 沿用） |
| D9 | 指标血缘 | N/A 本单无统计数字（L1 起接 readinessSeed） |
| §4.2 | push 纪律 | ✅ 走查通过后人工授权推 origin/dev（a53cf83），CI 触发 K8s dev rollout |

## 开放项

- 门户真实菜单树需在用户中心配置 `/intelligence/*` 三菜单（部署侧配置，非代码）；未配置前嵌入模式用户无 intel 菜单 = 预期行为
- `LUMEN-INTEL-FE-L1` 可开工（依赖本单走查通过）

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~35k |
| model_used | glm-5.3 |
| actual_cost | ~$0.9 |
| cost_warn | false |
