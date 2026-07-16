# Frontend handoff：ENT-MOD-SEARCH-V2-S4

- 时间：2026-07-15
- 仓库：`repos/lumen-ui-topic`（worktree：`worktrees/lumen-ui-topic--ENT-MOD-SEARCH-V2-S4`）
- 分支：`feature/ent-search-v2-s4`
- Commit：`db73844` — `feat(ENT-MOD-SEARCH-V2-S4): wire enterprise search and compare pages [agent:frontend-agent]`
- 监管人：`human:孔东`
- 执行：`agent:frontend-agent`
- PR：未推送（待监管确认 push / 合入 `dev`）
- CI：本地 `npm run type-check` ✅ · `npm run build-only` ✅
- 复刻自：demo `SearchPage.tsx` / `EnterpriseCompareBasketPage.tsx`
- 覆盖：规划 4.1 / 4.3 / 4.4（**不含 4.2 详情**）

## 范围与实现

| # | 产物 | 说明 |
|---|---|---|
| 4.1 | `src/views/enterprise/EnterpriseSearch.vue` + `src/config/enterpriseSearch.ts` | 正式查询页；URL `mode/q/preset/source/region/task` 初始化 Scaffold；数据经 `api/enterprise.ts` |
| 4.3 | `src/views/enterprise/EnterpriseCompare.vue` | 薄封装 → `EnterpriseCompareBasketView`；空态 / 分析类型 / Mock 发起分析 |
| 4.4 | `src/router/menu.ts` | 侧栏「企业查询」「对比篮」挂真页；默认落地 = 查询页 |
| 详情 | `EnterpriseDetailStub.vue` | **占位**，注明 owner=`ENT-MOD-PROFILE-V2-DEMO`，禁止双写 |
| 高筛 | — | **本轮仍用 Scaffold 默认 Empty 占位**（监管确认）；未接 `components/filter/*` |

## 偏离说明

1. **高筛占位**：COMPONENTS 虽 `done`，监管明确本轮仍占位；后续 S5 / 联调再接 FilterPanel。
2. **详情 stub**：不实现 `EnterpriseDetail.vue` 真页，仅路由占位 + 回链查询/对比篮。
3. **config 路径**：registry 名 `config/enterpriseSearch.ts` 为 re-export；真源仍 `enterpriseSearchConfig.ts`（route 已改为 `/enterprise/enterprise-search`）。

## demo vs lumen 对照（勾选）

| 对照项 | demo | lumen S4 | 状态 |
|---|---|---|---|
| 查询页装配 SearchScaffold | SearchPage | EnterpriseSearch | ✅ |
| URL mode/q/preset/region | ✅ | ✅ | ✅ |
| 高级筛选面包屑 | ✅ | advanced 模式显示 | ✅ |
| 高筛面板本体 | FilterPanel | Empty 占位 | ⚠️ 监管允许 |
| 对比篮空态 CTA → 查询 | basket → search | → `enterprise-search` | ✅ |
| 分析类型选择 + 发起 Mock | ✅ | ✅ | ✅ |
| 详情整页 | ProfilePage | Stub（PROFILE） | ⚠️  intentional |

## 验收证据

- `vue-tsc --build` 通过
- `vite build` 通过（产出含 `EnterpriseSearch-*.js` / `EnterpriseCompare-*.js` / `EnterpriseDetailStub-*.js`）
- 菜单可进：`/enterprise/enterprise-search`、`/enterprise/enterprise-compare`
- 详情：`/enterprise/:code` → stub，文案标明 PROFILE owner

## 架构合规自检

1. 算法只在 Python — N/A（前端）✅
2. 调用链前端→Java — 经 `api/enterprise.ts`（Mock 双路）✅
3. 图谱 Nebula — N/A ✅
4. 可观测性 — 沿用仓内 request/observability；本薄页未新增独立埋点事件 ✅
5. CI/CD — 待 push 后 Pipeline；本地 type-check/build 绿 ✅
6. demo2 只读 — 未改 demo ✅
7. 共享聚合核心 — N/A ✅
8. 数据策略 ADS/Mock — Mock via api ✅
9. Design/Arco — Vue + Arco，复用 S2A 组件 ✅
10. 数据血缘 D9 — 指标展示在 Scaffold 内既有 TraceInfoIcon / MockBadge ✅
11. 交互 D10 — 对齐 demo 查询/对比篮交互；高筛占位已声明 ✅

## Cost 回填

| 字段 | 值 |
|---|---|
| `actual_tokens` | ~95_000（估） |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~0.45 |
| `cost_warn` | green |

## 开放项

1. push `feature/ent-search-v2-s4` → origin，开 PR 合 `dev`（需监管确认）
2. 接入 COMPONENTS Filter* 替换占位（建议 S5 或独立联调）
3. PROFILE 交付后替换 `EnterpriseDetailStub`
4. 飞书多维表 record `recvpmwLY2Z2b6` 状态同步（coordinator）
