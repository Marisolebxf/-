# SYSINT-SIT-02-L01 · 页面区块台账与自检摘要

> 任务 WBS-02-02｜范围 = SRS 9 页（M1–M9，196 叶），M10 维护管理排除（签字 2026-10-29）
> 交付形态：前端网关接线 + 诚实空态（不做后端控制器）
> 状态：改动停本地，未 commit/push，等人工验收

## 1. 页面 → 三要素供数台账

| # | 页面 | 前端 API 文件 | 网关路径（改后） | 后端控制器 | 供数状态 |
|---|---|---|---|---|---|
| M1 | 科技全域态势 | `api/situation/index.ts` | `/display/v1/situation/{map,overview,influence,cluster,compare}` | `SituationController` | 有数（timeline/events 空态） |
| M2 | 科学技术全景 | `api/situation/panorama.ts` | `/display/v1/situation/panorama/graph` | 无 | 空态（404→空图谱） |
| M3 | 技术发展跟踪 | `api/situation/tracking.ts` | `/display/v1/situation/tracking/{meta,dataset}` | 无 | 空态（meta null / 空数据集） |
| M4 | 全球创新监测 | `api/situation/globalInnovation.ts` | `/display/v1/situation/global-innovation/*` | `GlobalInnovationController` | 有数 |
| M5 | 湾区创新监测 | `api/situation/bayAreaInnovation.ts` | `/display/v1/situation/bay-innovation/*` | `BayInnovationController` | 有数 |
| M6 | 深圳创新监测 | `api/situation/shenzhenInnovation.ts` | `/display/v1/situation/shenzhen-innovation/*` | `ShenzhenInnovationController` | 有数（allSettled 分区降级） |
| M7 | 科技创新评估 | `api/situation/innovationEvaluation.ts` | `/display/v1/situation/innovation-evaluation/{meta,snapshot}` | 无 | 空态（空 meta/快照） |
| M8 | 科技指数 | `api/situation/techIndex.ts` | `/display/v1/situation/tech-index/dataset` | 无 | 空态（空 dataset） |
| M9 | 科技发展规划 | `api/situation/techDevelopmentPlan.ts` | `/display/v1/situation/planning/dataset` | 无 | 空态（空 dataset） |
| M10 | 维护管理（排除） | `api/situation/maintain.ts` | `/situation/v1/maintain/meta`（未改） | 无 | 非三要素页，不纳入本叶 |

## 2. 代码改动清单

- 新增 `src/api/situation/honestEmpty.ts`：`optionalPost` / `post` / `unwrap` / `optionalClient` / `NOT_IMPLEMENTED_STATUS`（第二处出现即封装）。
- `src/api/situation/index.ts`：复用公共件，删除本地重复实现（行为不变）。
- `src/api/situation/panorama.ts`：BASE → `/display/v1/situation/panorama`；`optionalPost` + 空图谱。
- `src/api/situation/tracking.ts`：路径 → `/display/v1/situation/tracking`；`optionalPost`；导出 `EMPTY_TRACKING_DATASET`；meta/dataset 404→null。
- `src/api/situation/innovationEvaluation.ts`：路径 → `/display/v1/situation/innovation-evaluation`；`optionalPost`；空 meta/快照。
- `src/api/situation/techIndex.ts` / `techDevelopmentPlan.ts`：路径 → `/display/...`；`optionalPost`；空 dataset。
- `src/views/situation/tracking/index.vue`：`loadMeta`/`loadDataset` 加 try/catch；`meta?.timeline?.years`；`dataset ?? EMPTY_TRACKING_DATASET`。
- `src/views/situation/tech-development-plan/tabs/OverviewTab.vue`：多维度指标空数组兜底。
- `src/views/situation/innovation-evaluation/models/evaluationModel.ts`：详情维度空数组兜底。

## 3. 自检扫描摘要（T11）

| 检查项 | 结果 | 说明 |
|---|---|---|
| `src/api` 内 `/situation/v1` 可执行命中 | 通过（白名单 2 处） | `talent.ts`（任务1 人才态势，非本叶）；`maintain.ts`（M10 已排除）。situation 其余文件仅注释提及 |
| 久新直连（`47.93.119.170` / `29030` / `test2` / `gkx_technology_analysis_dev`） | 零命中 | 前端无直连，符合 A3/D15 |
| `USE_MOCK=false` 零 fixture 填数 | 通过（终态为空态） | 5 个未接通页接口 404 后覆盖为空形状；首屏同步初值与静态字典仍引自 `@/mock`（既有架构，非接口数据），已登记 |
| 菜单相对路径 | 通过 | `src/router/menu.ts` 全部 `path: ${groupKey}/${itemKey}` |
| 企业 ≠ 科研机构 | 通过 | `FACTOR_LABELS` / `OBJECT_TYPE_LABELS` 中 `enterprise: '企业'`、`institution: '科研机构'` 分离正确 |

## 4. 工程验证

- `vue-tsc --build`：零错误（exit 0）。
- `vite build`：成功（✓ built，exit 0）。

> 备注：`pnpm` 因 corepack 签名问题不可用，改用本地 `node_modules/.bin/vue-tsc` 与 `vite` 直接执行；Node 版本 20.18.0 低于 Vite 建议的 20.19+，构建有版本提示但成功。
