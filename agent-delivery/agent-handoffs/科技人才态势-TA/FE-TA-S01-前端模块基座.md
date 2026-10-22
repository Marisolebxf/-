# FE-TA-S01 · 科技人才态势 — 前端模块基座（Mock 先行）

- **任务**：FE-TA-S01（Epic：E-FE-TALENT）
- **执行**：agent:frontend-agent（监管 human:孔东）
- **日期**：2026-10-20
- **状态**：实现完成，停本地工作区待人工验收（AGENTS.md 闸门：验收通过前不 commit/push）
- **ponytail**：full

## 1. 范围与实现（对照派单 DoD）

| 交付物 | 落点 | 说明 |
|---|---|---|
| 种子冻结 | `src/mock/modules/talentSeed.ts`（1632 行） | demo `talent-trend/data.js` 逐行移植，`@ts-nocheck` + 固定种子 20260821；import 指向 `.ts` 同伴（唯一允许差异，自检白名单） |
| 难度规则冻结 | `src/mock/modules/talentDifficultyLogic.ts` | demo `difficultyTabLogic.js` 移植 |
| 类型层 | `src/types/talent.ts` | 4 数据集 + 人才主档（论文/专利/项目关系、合作网络、关键词、荣誉等）全字段 TS 化，约 40 interface |
| Mock 注册 | `src/mock/modules/talent.ts` + `src/mock/register.ts` | 4 端点：`taGlobalDataset` / `taFocusRegionDataset` / `taProfileDataset` / `taRecommendDataset` |
| API 双轨 | `src/api/talent.ts` | 4 个 `defineApi`；real 路径为占位（BE-TA-CONTRACT-01 冻结后替换，已注明禁止猜路径） |
| 筛选配置 | `src/views/talent/fieldConfig.ts` | demo `constants/fieldConfig.js` 移植；产业级联直接复用仓内 `@/lib/industryCluster`（不重复移植） |
| 跨页跳转 | `src/stores/talentNav.ts` | demo `navigation.js` 单例语义 → Pinia + `route.query.talentId`；路由 name 映射收口 |
| 页壳 ×4 | `src/views/talent/{global,region,profile,recommend}/index.vue` | `tl-page--ta-root` + fullBleed；`PageTabFrame`（global 双 Tab / profile 7 Tab / recommend 4 Tab）；region 双视图 `v-show` 保活（不叠互斥 display） |
| 路由挂接 | `src/router/menu.ts` | 4 菜单项从 `DevelopingView` 换真实组件，`fullBleed: true` |
| 样式冻结 | `src/views/talent/styles/demo-talent{,-focus-region,-profile,-recommend}.css` | demo 4 个 CSS 逐块移植（共 ~3100 行）+ lumen 页根 `--figma-*` 变量适配追加 |
| 可观测 | `src/views/talent/useTalentTrack.ts` | `ta-talent-track` CustomEvent + `createTraceId`（对齐 TS/DR 模式），4 页壳 page-mounted 埋点 |
| 自检 | `src/views/talent/talent.test.mjs` | 种子与 demo 真源主体逐行一致性断言（锚点行比对）+ 接线完整性断言 |

## 2. Arco 替换（antd → Arco Design Vue）

- 页签框架：antd Tabs → 仓内 `PageTabFrame`（内部 `a-tabs`）
- 双视图切换：antd Segmented → `a-radio-group type="button"`
- 产业级联：复用 FE-TS-04A 移植的 `IndustrySelect.vue`（`a-cascader` 多选 + checkStrictly）
- 搜索/下拉：`a-auto-complete` / `a-select`（allow-search）
- CSS 内 21 处 `.ant-*` 选择器未改写（保留冻结），由后续 01A–04A 页面任务在组件 scoped 层按 `.arco-*` 等价替换——基座不改 demo CSS 冻结内容

## 3. 验收证据（三绿）

- `pnpm type-check`（vue-tsc --build）：exit 0
- `node src/views/talent/talent.test.mjs`：ok（冻结一致性 + 接线断言全过）
- `pnpm build`：✓ built in 18.77s

## 4. 架构合规自检（公约 §2）

- ✅ 调用链：Mock 先行，`defineApi` 双轨；real 路径占位待 BE-TA-CONTRACT-01
- ✅ D8 Design：样式 token 逐块冻结 demo；Arco 组件替换无原生控件
- ✅ D9 血缘：MockBadge 挂页面统计区（`USE_MOCK` 门控）；8 件套 ⓘ 待各页面任务接 metric-registry
- ✅ D12 隔离：零 import demo-* 代码路径；种子为文本复制非模块引用
- ✅ 可观测：`ta-talent-track` + traceId
- ✅ 首屏同步初值防白屏（M7 教训）
- ✅ 图表容器显式高度：基座无图表；规则已写入页注释供 01A–04A 遵循

## 5. 偏离说明

1. 种子放 `src/mock/modules/`（非原计划 `views/talent/`）：对齐 DR 模块 `dataResourcesSeed.ts` 仓内先例。
2. seed 为 `.ts` + `@ts-nocheck`（非 `.js`）：仓内 allowJs 虽开，但 DR 先例为 `.ts`，保持一致。
3. 自检为源码断言式（非运行时执行）：仓内 DR 先例模式；种子运行时确定性由 demo 侧 16 个 test.mjs 覆盖 + 固定种子保证。

## 6. 后续任务接口（给 01A–04A）

- 数据：`fetchTalentGlobalDataset` 等 4 API；类型 `@/types/talent`
- 跳转：`useTalentNavStore` + `TALENT_NAV_ROUTE_NAME`；目标页读 `route.query.talentId`
- 筛选：`@/views/talent/fieldConfig`（10 组 options + `talentFieldInScope`）
- 样式：4 个 CSS 已就位；`.ant-*` 21 处待组件层 Arco 等价替换
