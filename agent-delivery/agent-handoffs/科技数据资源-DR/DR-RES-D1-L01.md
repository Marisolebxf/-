# DR-RES-D1-L01 · 科技数据资源四页改走 request() 并按 origin 挂 MockBadge

| 字段 | 值 |
|---|---|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 状态 | 仍是 `in_progress`。本叶不改登记表，不标 `done` |
| 仓 | `lumen-ui-science-pc`，分支 `dev`（已 `git pull --no-rebase origin dev`） |
| ponytail | `full` |

ponytail: full

只做前端接线。四条 `real()` 走已有 `request()`，不新造路径，不新做血缘组件，不改评审层总开关。未用 YAGNI 跳过 D9 的 MockBadge。

## 四条路径

`request()` 在 `code===0` 时只返回 `data`。`real()` 把这个 `data` 当作数据集，不再把整包信封当数据集，也不再裸 `fetch`。

| 方法 | 路径 |
|---|---|
| GET | `/display/v1/data-ops/overview/dataset` |
| GET | `/display/v1/data-ops/access/dataset` |
| GET | `/display/v1/data-ops/theme/dataset` |
| GET | `/display/v1/data-ops/application/dataset` |

`USE_MOCK=false` 时 `defineApi` 不查 mock 注册表。四个页面只有 `USE_MOCK` 为真才调用 `create*Dataset`；为假时初值是空壳，成功后整份换成 `request()` 的 `data`。缺键不拿 fixture 补数。`entityStock`、`columnCatalog` 页面不读。

## MockBadge

角标用已有 `@/components/lineage/MockBadge.vue`。

- KPI 卡：`origin===mock` 才挂。总体 / 接入 / 应用的 KPI 用接口元素上的 `origin`。主题页四张卡的数来自主题库行，行上 `origin===mock` 才把这个标记抄到卡上。
- 总体视窗里已有的统计数字（接口状态、累计调用、应用主体汇总）和申请页实时 QPS / 成功率：`origin===mock` 挂；没有 `origin` 的种子态仍按 `USE_MOCK` 挂。
- `origin===snap` 或 `jiuxin` 不挂。`entityStock`、`columnCatalog` 根上是 `snap`，页面不渲染这两块，自检确认即使子行带 `mock` 也不挂。

## 测试

- `node src/views/data-resources/mockOrigin.test.mjs` 通过。
- `pnpm type-check`（`vue-tsc --build`）通过。未跑 `pnpm build`。
- 未在浏览器打开四页。角标依赖网关返回的 `origin`，本叶没有联调环境。

## CI/CD

- 分支：`dev`，与 `origin/dev` 同步后再改
- commit：无
- push：无。改动停在 `lumen-ui-science-pc` 本地工作区
- pipeline / K8s：无

## 涉及文件

`lumen-ui-science-pc`：

- `src/api/dataResources.ts`
- `src/types/dataResources.ts`（`DrKpiItem` 增加可选 `origin`）
- `src/views/data-resources/mockOrigin.ts`
- `src/views/data-resources/mockOrigin.test.mjs`
- `src/views/data-resources/components/DrKpiCard.vue`
- `src/views/data-resources/theme/index.vue`
- `src/views/data-resources/application/index.vue`
- `src/views/data-resources/overview/components/ApplicationStatusMonitor.vue`
- `src/views/data-resources/overview/components/CumulativeCallTrendAnalysis.vue`
- `src/views/data-resources/overview/components/ResourceAppSubjectList.vue`

编排仓只新增本 handoff，未提交。
