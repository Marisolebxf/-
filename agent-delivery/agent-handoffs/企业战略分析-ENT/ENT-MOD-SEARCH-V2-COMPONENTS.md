# ENT-MOD-SEARCH-V2-COMPONENTS · 企业查询-搜索范式与高级筛选组件

> 格式参考 `templates/handoff-template.md`；内容按本次实测与代码实写。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:曹丽影` |
| claim_type | `pull` |
| claimed_at | `2026-07-14T20:27:12+08:00` |
| lock_until | `2026-07-15T00:27:12+08:00` |
| worktree_branch | `feat/ENT-MOD-SEARCH-V2-COMPONENTS` |
| worktree_path | `worktrees/lumen-ui-topic--ENT-MOD-SEARCH-V2-COMPONENTS`（基于 `origin/dev` / S0 `09bd376`） |
| 说明 | 组件层与 DEMO/S1 解耦；Vue 3 + `@arco-design/web-vue` 重写，只读 demo 配置驱动思想 |

## 范围与实现（对照 DoD）

| DoD | 状态 | 说明 |
|-----|------|------|
| 搜索组件 config-driven（注入 `ElementSearchConfig`） | ✅ | `SearchScaffold` + `enterpriseSearchConfig` |
| 高级筛选递归 AND/OR + FilterTemplate 存/载/删 | ✅ | `FilterEngine.evaluate` 递归；`FilterTemplateManager` localStorage |
| 接口统一经 `api/enterprise.ts` + Mock/真开关 | ✅ | `defineApi` stub（`searchEnterprises` / `exportEnterpriseList` / `getEnterpriseDetail`）；S1 可扩 mock 数据 |
| 评审模式 `TraceInfoIcon` 挂载 | ✅ | `MetricSpecCard` → `TraceInfoIcon`；ResultList / ConditionBuilder / ElementProfile |
| `npm run build` 通过 | ✅ | worktree 内 `pnpm run build` 绿（vue-tsc + vite，~6s） |

## 产物清单

### 新增 — filter

- `src/components/filter/FilterEngine.ts`
- `src/components/filter/ConditionBuilder.vue`
- `src/components/filter/FilterPanel.vue`
- `src/components/filter/GroupNode.vue`
- `src/components/filter/FilterTemplateManager.vue`
- `src/components/filter/index.ts`

### 新增 — search

- `src/components/search/SearchScaffold.vue`
- `src/components/search/SearchHub.vue`
- `src/components/search/ResultList.vue`
- `src/components/search/ResultToolbar.vue`
- `src/components/search/ElementProfile.vue`
- `src/components/search/queryEngine.ts`
- `src/components/search/searchStorage.ts`
- `src/components/search/configs/enterpriseSearchConfig.ts`
- `src/components/search/configs/enterpriseFieldLibrary.ts`
- `src/components/search/index.ts`

### 新增 — api / common

- `src/api/enterprise.ts`
- `src/components/common/MetricSpecCard.vue`
- `src/components/common/PendingBadge.vue`

## 测试结果

| 检查 | 结果 |
|------|------|
| `pnpm run build`（worktree） | ✅ 通过 |
| 页面级路由装配 demo | ⏳ 留给 DEMO / 后续接线（组件可 import） |
| 全量企业 mock 列表 | ⏳ 软依赖 S1 |

## CI/CD

- 分支：`feat/ENT-MOD-SEARCH-V2-COMPONENTS`
- commit：**尚未提交**（监管人确认后 commit + push + PR → `dev`）
- pipeline / PR / K8s：待 push 后补填
- 说明：lumen 仓走 feature + PR；禁止直推 `dev`/`main`

## 成本回填

| 字段 | 值 |
|------|-----|
| estimated_tokens | 150_000 |
| actual_tokens | 220_000（量级估算：认领/地基核对 + 组件实现 + build） |
| model_used | composer-2 / cursor-agent（会话混合；按量产档近似） |
| actual_cost | 1.19（公式：220k × 0.8 × $3 + 220k × 0.2 × $15 / 1M） |
| cost_warn | green |

## 架构合规自检（公约 §2）

1. 算法只在 Python — ✅ N/A
2. 调用链前端→Java — ✅ 组件经 `api/enterprise.ts`；mock 在 api 层
3. NebulaGraph — ✅ N/A
4. 可观测性 — ⚠️ 未新增埋点；脚手架未删既有钩子
5. CI/CD feature→PR — ✅ 待 push
6. demo 不 merge lumen — ✅ 只读参照
7. 共享聚合 — ✅ N/A
8. ADS/Mock — ✅ `defineApi` + USE_MOCK
9. Design.md / Arco Vue — ✅
10. D9 血缘 — ✅ metricId → TraceInfoIcon；完整 8 件套目录留给 S1/指标种子
11. D10 交互 — ⚠️ 基础 Arco 键盘可达；未做完整 §19 走查

## 遗留风险 / 开放项

1. **未 commit / 未开 PR**：需曹丽影确认后提交
2. 企业查询页尚未 import `SearchScaffold`（DEMO 装配）
3. S1 到位后替换 stub mock；签名已稳定
4. 嵌套分组从字段库添加条件 UX 可再打磨；`smartParser` 仅 props 预留
5. Result refine（区域等）与对比篮持久化未做（非本任务核心 DoD）

## 涉及文件

见「产物清单」。
