# ENT-MOD-SEARCH-V2-S0 · 企业查询 V2 阶段0 地基

> 格式参考 `templates/handoff-template.md`；内容按本次实测与代码实写。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| claimed_at | `2026-07-14T14:50:00+08:00` |
| lock_until | `2026-07-14T18:50:00+08:00` |
| worktree_branch | `feature/ent-search-v2-s0` |
| 说明 | 在现有工作区切 feature 分支执行；保留用户既有未提交改动（dashboard 删除、APP_TITLE 等），未纳入本任务提交范围 |

## 范围与实现（对照派单包）

| 子项 | 状态 | 说明 |
|------|------|------|
| 0.1 USE_MOCK + defineApi + auth 重构 | ✅ | `VITE_APP_USE_MOCK` 优先，缺省回退 `ENABLE_MOCK_AUTH`；明确 `false` 不回退 |
| 0.2 demo 对齐用户/角色/评审 | ✅ | Pinia `stores/review.ts` + `PersonaLevelSwitcher.vue` + `TraceInfoIcon.vue`；顶栏已替换旧 6 角色 |
| 0.3 领域类型 | ✅ | `types/{perms,enterprise,search,filter}.ts` 可供 COMPONENTS 引用 |
| 0.4 菜单重建 | ✅ | 舍弃八大专题；仅「企业分析」：企业查询 / 对比篮（侧栏）+ 企业详情路由（隐藏） |

## 产物清单

### 新增

- `src/utils/http.ts` — `defineApi`
- `src/types/perms.ts`
- `src/types/enterprise.ts`
- `src/types/search.ts`
- `src/types/filter.ts`
- `src/stores/review.ts`
- `src/components/review/PersonaLevelSwitcher.vue`
- `src/components/review/TraceInfoIcon.vue`
- `src/components/review/persona-switcher.css`

### 修改

- `src/config/app.ts` — `USE_MOCK`
- `src/api/auth.ts` — `defineApi` 重构（行为不变）
- `env.d.ts` / `.env.development` / `.env.production` — `VITE_APP_USE_MOCK`
- `src/router/menu.ts` — 企业分析骨架
- `src/router/routes.ts` — 默认落地 `enterprise-search`
- `src/layouts/DefaultLayout.vue` — 接入 Persona 切换器，移除旧角色 UI

## 旧菜单/角色清理证据（grep）

在 `src/` 内执行：

```text
rg -n "userRoles|领导驾驶舱|selectedRoleKey|科技发展态势|科技政策跟踪|科技人才态势|科技数据资源|科技知识图谱|科技成果展示|科技服务全景" src
```

结果：**无匹配**。

## 与 demo 顶栏对照说明

| 项 | demo-ui-topic | lumen-ui-topic（本任务） |
|----|---------------|--------------------------|
| 数据模型 | `CurrentUser` L0–L4 × Persona | 同构 `types/perms.ts` + `stores/review.ts` |
| 持久化 | `ent_mock_user` / `ent_review_mode` | 同 key |
| UI | `PersonaLevelSwitcher` Persona 主选 + Level 演示调节 + 内部评审开关 | Vue + Arco Vue 重写，文案/结构 1:1 |
| 评审关闭 | 仅当前 Persona；TraceInfoIcon 不渲染 | 同行为 |
| 旧 6 角色 | 无 | 已删除 `userRoles` / `selectedRoleKey` |

## 测试结果

| 检查 | 结果 |
|------|------|
| `npm run type-check` | ✅ 通过 |
| `npm run build-only` | ✅ 通过（1248 modules） |
| `npm run lint`（全仓） | ⚠️ 既有错误：`postcss.config.cjs`、`UnifiedLeafletMap.vue`（非本任务） |
| `eslint`（本任务触及文件） | ✅ 通过 |
| 残留 grep | ✅ 无旧角色/旧专题菜单 |

## CI/CD

- 分支：`feature/ent-search-v2-s0`
- commit：尚未提交（待监管人确认后 commit + push + 开 PR → `dev`）
- pipeline / PR / K8s：待 push 后补填
- 说明：本仓策略为 feature + PR 合入 `dev`；未直推 `dev`/`main`

## 成本回填

| 字段 | 值 |
|------|-----|
| estimated_tokens | 80_000 |
| actual_tokens | 180_000（量级估算：上下文读取 + 实现 + 验证） |
| model_used | claude-sonnet-4.5（会话实际为 Cursor Grok；按 registry 合法枚举就近回填） |
| actual_cost | 0.97（公式：180k × 0.8 × $3 + 180k × 0.2 × $15 / 1M） |
| cost_warn | green |

## 架构合规自检（公约 §2）

1. 算法只在 Python — ✅ N/A
2. 调用链前端→Java — ✅ mock 仅在 api 层
3. NebulaGraph — ✅ N/A
4. 可观测性 — ✅ 未删除既有钩子；埋点扩展留给后续阶段
5. CI/CD feature→PR — ✅ 分支已建；待 push
6. demo 不 merge lumen — ✅ 只读参照
7. 共享聚合 — ✅ N/A
8. ADS/Mock — ✅ Mock 开关地基就绪
9. Design.md / Arco Vue — ✅
10. D9 血缘 — ✅ 类型预留 metricId；UI 角标阶段 2
11. D10 交互 — ✅ Persona 键盘 Escape / focus-visible / aria

## 遗留风险 / 开放项

1. **未 commit / 未开 PR**：需孔东确认后提交（勿把 dashboard 删除、README、package-lock、index.html 等无关改动混入）
2. 全仓 lint 仍有历史债，不阻塞本阶段 DoD（build + 本任务文件 eslint 绿）
3. S1（enterprise API + mock + compareBasket）依赖本任务合入后解锁

## 涉及文件（本任务）

见「产物清单」。
