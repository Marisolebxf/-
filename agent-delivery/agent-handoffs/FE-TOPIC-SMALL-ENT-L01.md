# FE-TOPIC-SMALL-ENT-L01 · 专题小屏·企业维（查询/总览/画像裁剪）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:曹丽影` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 范围与实现

裁自 `lumen-ui-topic` 企业查询 + SPIKE 企业发展总览 + 画像 Drawer；目标仓 **`lumen-ui-topic-mobile`**。

| 路径 | 路由 | 状态 |
|------|------|------|
| 企业查询 | `/development/search` | 新增 `EnterpriseSearchView`：关键词 + 热词 + QuickFilter(≤4) + 列表 → 画像 |
| 企业发展 | `/enterprise-center/overview` | SPIKE 保留；画像抽至 `EnterpriseProfileDrawer` 复用 |
| 企业画像 | `ProfileDrawer` 全屏 | 查询/总览列表均可打开 10 Tab 画像 |

**砍掉（Design-mobile §10）**：高级 query_tree、对比篮、导出、G6 编辑、PermGate。

## Mock 开关

- `VITE_APP_USE_MOCK=true` 时走 `defineApi` + `registerApiMock`（`src/api/enterprise/mocks.ts`）
- `USE_MOCK=false` 时检索打 Java `/enterprise/topic/v1/search/*`，禁止 fixture 静默填数

## 架构合规

| 铁律 | 状态 |
|------|------|
| D12 不进 lumen-ui-topic / 不调 demo | ✅ |
| 前端 → Java Gateway | ✅（real 路径已接，Mock 演示） |
| Design-mobile C1/C2/C6 | ✅ Arco 壳 + Vant 页内；history 路由 |
| D9 ⓘ | ✅ 总览 StatCard 保留 metric_id |

## 产物

- `repos/lumen-ui-topic-mobile/src/views/enterprise/EnterpriseSearchView.vue`
- `repos/lumen-ui-topic-mobile/src/views/enterprise/EnterpriseProfileDrawer.vue`
- `repos/lumen-ui-topic-mobile/src/api/enterprise/*`
- `repos/lumen-ui-topic-mobile/src/utils/http.ts`

## 验收证据

- `pnpm build` 绿（2026-08-26 本地）
- 核心路径：侧栏「企业查询」→ 搜索/筛选 → 点企业 → 全屏画像 Tab 可切换；「企业发展」→ 列表/地图 → 画像

## 联调确认

联调通过（Mock 演示路径已自测；待孔东会签 UI 布局微调）。

## 遗留

- 总览 KPI 仍用 `previewSamples` 页内常量，未接 `entStats*` API（下一叶可接）
- 未 push / 未跑 CI（本地实现，待用户确认后提交）

## CI/CD

- 分支：dev（待 push）
- commit：待提交
- dev URL：本地 `pnpm dev`
