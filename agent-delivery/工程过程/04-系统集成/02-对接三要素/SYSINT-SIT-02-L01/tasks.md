# SYSINT-SIT-02-L01 · 实施任务清单

> 前置：`spec.md` 第 3 节范围裁定已签字（SRS 9 页、排除 M10）。
> 根：`repos/lumen-ui-science-pc`。改完停本地等人工验收，不 commit/push。

- [x] T0 范围确认：已签字 = SRS 9 页（M1–M9），M10 排除；仅前端接线+诚实空态（2026-10-29）
- [x] T1 抽取公共件 `src/api/situation/honestEmpty.ts`（`optionalPost` / `post` / `unwrap` / `optionalClient` / `NOT_IMPLEMENTED_STATUS`）
- [x] T2 改造 `src/api/situation/index.ts` 复用公共件，删除本地重复（行为不变）
- [x] T3 修 `src/api/situation/panorama.ts`：BASE → `/display/v1/situation/panorama`
- [x] T4 修 `src/api/situation/tracking.ts`：路径 + `optionalPost` + 空形状；改 `views/situation/tracking/index.vue` 容错（`meta?.timeline?.years`、`dataset ?? EMPTY_TRACKING_DATASET`、`loadMeta`/`loadDataset` try-catch）
- [x] T5 修 `src/api/situation/innovationEvaluation.ts`：路径 + `optionalPost` + 空 meta/快照；`evaluationModel.ts` 详情空数组兜底
- [x] T6 修 `src/api/situation/techIndex.ts` 与 `techDevelopmentPlan.ts`：路径 + `optionalPost` + 空 dataset；`OverviewTab.vue` 空分类兜底
- [x] T7（不适用）M10 维护管理已排除，`maintain.ts` 不动
- [x] T8 空态不白屏：静态扫描 5 页消费点，修复 3 处空数组解构崩溃点（tracking 空对象、OverviewTab 分类、evaluation 详情维度）
- [x] T9 `vue-tsc --build` 零错误
- [x] T10 `vite build` 成功
- [x] T11 自检扫描：`/situation/v1` 白名单 2 处（talent 任务1 / maintain M10）、无久新直连、`USE_MOCK=false` 终态空态、菜单相对路径、企业≠科研机构
- [x] T12 产出 `page-three-elements-ledger.md`（页面区块台账 + 扫描摘要），停本地待验收
