# ENT-MOD-SEARCH-V2-S1 · 企业查询 V2 阶段1 接口层

> 格式参考 `templates/handoff-template.md`；对照派单包 §4.2。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| claimed_at | `2026-07-14T18:11:00+08:00` |
| lock_until | `2026-07-14T22:11:00+08:00` |
| worktree_branch | `feature/ent-search-v2-s1` |
| 说明 | 基于 `origin/dev`（含 S0 `09bd376`）切 feature 分支；本阶段仅接口层 + Mock + 对比篮 store，不含 SearchScaffold / 页面 |

## 范围与实现（对照派单包 §4.2）

| 子项 | 状态 | 说明 |
|------|------|------|
| 1.1 `api/enterprise.ts` 五接口 `defineApi` | ✅ | search / detail / profile / export / aggregates；real + mock 签名一致 |
| 1.2 `mock/enterprise` 从 demo 迁移 | ✅ | 30 条企业；含 `filterFieldSchema` / `smartParser` / `portalAggregates` / `enterpriseProfile` |
| 1.3 `stores/compareBasket.ts` | ✅ | `elementKey` 隔离、`MAX_ITEMS=12`、`useStorage('ent.compareBasket.v1')`、超限 Arco `Message.warning` |

## 产物清单

### 新增

- `src/api/enterprise.ts` — 五接口 `defineApi`
- `src/mock/enterprise/enterpriseList.ts` — 30 条企业主数据
- `src/mock/enterprise/enterpriseProfile.ts` — 画像明细
- `src/mock/enterprise/filterFieldSchema.ts` — 字段库
- `src/mock/enterprise/smartParser.ts` — 智能解析
- `src/mock/enterprise/portalAggregates.ts` — 门户聚合
- `src/mock/enterprise/index.ts` — barrel + 五接口 mock 纯函数
- `src/stores/compareBasket.ts` — 对比篮 Pinia store

### 修改

- `src/types/enterprise.ts` — 扩展 `SearchParams` / `PageResult` / `ProfileTabData` / `EnterpriseAggregates`（`CompareItem` 等 S0 已有）

## DoD 对照证据

| DoD | 证据 |
|-----|------|
| 五接口均 `defineApi(real+mock)` | `src/api/enterprise.ts` |
| mock ≥30 条 | `enterpriseList.ts` 中 `id: 'ENT-` 计数 = **30** |
| 含 filterFieldSchema / smartParser / portalAggregates | 对应三文件已迁入 |
| compareBasket 隔离 / 12 / useStorage / Message | `stores/compareBasket.ts` |
| Mock 仅经 api 层 | `rg "mock/enterprise" src --glob "!mock/**"` → **仅** `api/enterprise.ts` |
| 未越界做页面/脚手架 | 无 SearchScaffold / ResultList 等新增 |
| `npm run type-check` | ✅ |
| `npm run build-only` | ✅（1248 modules） |

## 测试结果

| 检查 | 结果 |
|------|------|
| `npm run type-check` | ✅ 通过 |
| `npm run build-only` | ✅ 通过 |
| 组件直连 mock 绕过 | ✅ 无（仅 api 层引用） |

## CI/CD

- 分支：`feature/ent-search-v2-s1` → fast-forward 合入 `dev`
- commit：`9504b75` — `feat(ENT-MOD-SEARCH-V2-S1): enterprise API, mock data, and compare basket store [agent:frontend-agent]`
- 远程：已 push `origin/dev`（`09bd376..9504b75`）
- 说明：监管人孔东明确要求直合 `dev` 并推远程（与 S0 同流程）

## 成本回填

| 字段 | 值 |
|------|-----|
| estimated_tokens | 60_000 |
| actual_tokens | 95_000（量级估算：认领 + demo 迁移 + API/store + 验证 + handoff） |
| model_used | claude-sonnet-4.5（会话实际为 Cursor Grok；按 registry 合法枚举就近回填） |
| actual_cost | 0.51（公式：95k × 0.8 × $3 + 95k × 0.2 × $15 / 1M） |
| cost_warn | green |

## 架构合规自检（公约 §2）

1. 算法只在 Python — ✅ N/A（前端 mock 纯函数，无 NLP）
2. 调用链前端→Java — ✅ 组件只应调 `api/enterprise`；mock 不越层
3. NebulaGraph — ✅ N/A
4. 可观测性 — ✅ 未删除既有钩子
5. CI/CD feature→PR — ✅ 已 ff 合入并推送 `origin/dev`（`9504b75`）
6. demo 不 merge lumen — ✅ 只读参照 `demo-ui-topic`
7. 共享聚合 — ✅ N/A
8. ADS/Mock — ✅ Mock 数据 + `USE_MOCK` 开关（S0）
9. Design.md / Arco Vue — ✅ Message 用 `@arco-design/web-vue`
10. D9 血缘 — ✅ mock→Enterprise 映射带 `metricId`（如 `M_ENT_*`）
11. D10 交互 — ✅ N/A（本阶段无页面交互）

## 遗留风险 / 开放项

1. `getEnterpriseAggregates` 返回体含函数字段 `chainStageOf`（与 demo 对齐）；JSON 序列化场景需注意，真实 API 落地时可能改为纯数据
2. 阶段 2+（SearchScaffold / 页面）未开工，属后续任务（COMPONENTS / S2）
3. COMPONENTS（曹丽影）可消费已合入 `dev` 的 `api/enterprise` + types
4. 2026-07-14 监管人孔东确认代码审核通过 → registry `done`（`completed_at: 2026-07-14T21:21:00+08:00`）

## 涉及文件（本任务）

见「产物清单」。
