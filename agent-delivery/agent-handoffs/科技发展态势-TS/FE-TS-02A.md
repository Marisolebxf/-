# FE-TS-02A · 科学技术全景（M2）整页复刻 — 前端交付（待联调）

> 仓库：`repos/lumen-ui-science-pc`；路由 `/situation/science-technology-panorama`（menu.ts 既有路由）。
> 状态：mock 数据环境人工点测通过，**进入联调**（BE-TS-CONTRACT-01 契约冻结后切 `USE_MOCK=false`）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复刻优先复用 M1 底座（WorkbenchLayout/InsightDetailDrawer/TiandituMap/defineApi 双轨零改动）；纯逻辑抽 `src/lib/graph/` 17 文件供 selfcheck 覆盖；未用 YAGNI 跳过 D9/可观测（X-Trace-Id 经 request 拦截器全量注入）。 |

## 范围与实现（对照 DoD）

| DoD 项 | 实现 |
|---|---|
| 图谱画布（底座 GraphChart 接入，类型图例/关系类型筛选/展开深度/关键词定位视口聚焦） | `KnowledgeGraphCanvas.vue`（G6 5.x 受控组件：roam/缩放/旋转/复位/折叠子节点/邻接高亮）+ `GraphEmbedSection.vue`（视图切换/数据输入工具条/维护入口）+ `GraphFactorPanel.vue`（左栏实体类型开关）+ `PanoramaFilterBar.vue`（领域单选/时间/关键词/关系类型/更多筛选） |
| 关键实体列表 + 节点/实体详情 | `GraphListSection.vue`（8 列表 + 三态排序 + 分页）+ `GraphAnalysisPanel.vue` 关键实体 Tab（Top5/完整抽屉/关系快照/类型分布 donut）+ M1 `InsightDetailDrawer` 复用 |
| 路径叠加 + 播放 + 对比模式 | `KeyPathPlaybackMode.vue`（回放模式：激活/播放/单步/速度）+ `PathComparisonPanel.vue`（候选 2-5 条勾选、并行/叠加双模式、共享/独占节点、强度对比）|
| 图谱编辑（导入 JSON/手动增删/撤销重做/版本） | `GraphManualInputDialog.vue`（手动添加）+ `graphImport.ts`/`import.ts`（JSON/XLSX 导入，xlsx 动态 import）+ `manualInput.ts` + Ctrl+Z/Y 撤销重做（会话级，demo 同语义） |
| Mock 种子冻结自 demo | `mock/modules/panorama.ts`（种子冻结 demo App.jsx L2083-3094 / graphKeyPathMockData.js）；`api/situation/panorama.ts` defineApi 双轨 |
| pnpm build 绿 | ✅ type-check 0 error / build 32.8s 绿 / selfcheck 40+ 断言 PASS |

### 类型契约（联调对接清单）

- `types/panorama.ts`：GraphNode/GraphRelation/GraphKeyPathOption/GraphListRecord 等（字段名与 demo 冻结种子一致）
- `api/situation/panorama.ts`：`POST /situation/v1/panorama/graph`，入参 `PanoramaGraphParams { selectedFieldValues, timeRange, currentYear }`，出参 `PanoramaGraphResult`（7 字段）
- 契约冻结（BE-TS-CONTRACT-01）后仅改 api 层 real 路径/方法，页面零改动

## 验收证据

- `pnpm type-check`（vue-tsc --build，含 noUncheckedIndexedAccess）：0 error
- `node src/lib/graph/selfcheck.mjs`：PASS（viewState/keywordFilter/visualState/pathPlayback/pathComparison/entityRanking/listData/interactionState/filterContext 全断言绿；临时产物自清理）
- `pnpm build`：绿（32.8s；KnowledgeGraphCanvas 独立 chunk 1.4MB gzip 413KB——G6 体积，无进一步拆分必要）
- 人工点测（监管人 human:孔东，2026-10-14~15）：图谱画布/列表/回放/对比/编辑/筛选全交互通过（含本轮 UI 修正）

## 本轮收尾修复（进入联调前）

1. **类型门修复（89 → 0）**：此前会话以 `vue-tsc --noEmit` 验证为空跑（根 tsconfig 是 project-references，`files: []`）；真实类型门 `pnpm type-check`（`vue-tsc --build` + `noUncheckedIndexedAccess`）暴露 89 错。根因三块：
   - `GraphNode`/`GraphRelation`/`GraphKeyPathOption`/`GraphContextPathNode`/`GraphStatItem`/`GraphEntityRow`/`GraphKeyPathStageNode`/`GraphAnalysisContext`/`NormalizedGraphPath` 等 interface 缺索引签名，与 `lib/graph` 泛型约束（`[key: string]: unknown`）互喂时推断塌掉——统一补透传声明（图谱数据天然携带演示扩展字段）
   - mock 层 jitter 数组索引/`location` 元组/字典 fallback 的 noUncheckedIndexedAccess 机械修
   - 真问题：`fetchPanoramaGraph({})` 缺必填参、`graphTimeline` null 守卫、`pathPlaybackOptions` 首元素可能 undefined、XLSX sheet 索引、`GraphListSection` 模板引用未定义变量 `active`（demo renderSortHeader 局部变量移植丢失，按 demo 语义补条件表达式）、`KnowledgeGraphCanvas` 一处 React `graphRef.current` 残留
2. **selfcheck 环境修复**：仓切 pnpm 严格布局后 `esbuild` 不在顶层 node_modules，裸 import 失败——改从 vite 依赖闭包解析（npm/pnpm 通吃）；运行后自动清理 `.tmp-selfcheck.mjs`
3. `GraphAnalysisPanel` 未使用的 `graphListResultCount` prop 删除（ponytail 删除优先）

## 偏离说明

- 图谱编辑为会话级 Mock（demo 同语义），无后端持久化接口；真实编辑提交接口待契约
- `selfcheck.mjs`/`selfcheck-entry.ts` 为 ponytail 要求的最小自检，非框架测试
- G6 为本任务新增依赖（`@antv/g6@^5.1.1`，Architecture-baseline 图谱前端栈指定 G6/图可视化组件）；`xlsx@^0.18.5` 为导入功能动态依赖（动态 import，不进主包）

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python | ✅ api 层只写真实调用路径 |
| D12 不调 demo-* | ✅ USE_MOCK=false 零 mock 代码 |
| D8 Design token | ✅ demo 样式按选择器命中整块抽取（styles 内 demo-*.css）+ token 主题复用 M1 |
| D9 血缘 | ✅ StatCard ⓘ 挂位（metric_id 待 catalog 正式接入替换） |
| 可观测 | ✅ X-Trace-Id/traceparent 全请求注入（M1 拦截器） |
| 图谱栈 | ✅ G6（本页画布）+ ECharts graph（底座 GraphChart）双轨，按 D12 复刻 demo |
| 无计划外依赖 | ⚠️ 新增 @antv/g6 + xlsx（见偏离说明） |

## CI/CD（必填）

- 分支：`dev`（工作区未提交，零 git 操作——等联调回归后随 FE-TS-02A/04A 一起提交）
- dev 测试：`pnpm dev` → `/situation/science-technology-panorama`（USE_MOCK=true）

## 涉及文件

**新增**：`src/views/situation/panorama/`（index.vue + 10 组件 + models/chartBuilders.ts + styles/demo-panorama.css）、`src/lib/graph/`（17 文件）、`src/api/situation/panorama.ts`、`src/mock/modules/panorama.ts`、`src/types/panorama.ts`
**修改**：`src/mock/register.ts`（注册 panorama/globalInnovation）、`src/types/situation.ts`（M4 类型 + 本轮索引签名透传）、`src/config/echarts.ts`、`src/router/menu.ts`、`src/components/map/TiandituMap.vue`、`package.json`（+@antv/g6 +xlsx）

## 遗留风险

- `vue-tsc --noEmit` 在本仓是空跑（project-references 结构），**后续验证一律用 `pnpm type-check`**
- metric_id（TS-M2-*）为前端占位，D9 正式接入 `/metrics/v1/catalog` 后替换
- G6 chunk 1.4MB（gzip 413KB）：路由级懒加载已隔离，暂不拆分；若首屏指标超标再评估 CDN externals
