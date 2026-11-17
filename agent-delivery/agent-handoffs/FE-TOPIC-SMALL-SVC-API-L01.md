# FE-TOPIC-SMALL-SVC-API-L01 — 专题小屏·产业服务链 A（API/契约层）

- **状态**：已交付（commit `6b58a68`，已推 `origin/dev`）
- **执行**：agent:frontend-agent；**监管**：human:孔东
- **交付时间**：2026-11-17 22:40 (+08:00)
- **ponytail**: full（契约逐字对齐 PC，不造新抽象；自检脚本 1 个）

## 范围与实现（对照 PC lumen-ui-topic）

| 文件 | 改动 |
|---|---|
| `src/api/enterprise/types/analysisTask.ts` | 补 `SVC_ANALYSIS_LEAVES` 八叶（org_coverage/org_trend/tech_power/shortboard/graph/shenzhen/attract/cultivate）、`SvcAnalysisType`（规范键 `svc:analysis:{leaf}` / 别名 `svcan.{leaf}.v0` / 裸键）、`svcAnalysisLeafOf` / `isSvcAnalysisType` / `svcAnalysisTypesMatch` —— 与 PC `analysisTask.ts` #47–153 同文 |
| `src/api/service/paths.ts` | 补 `meta` / `compareBasket` / `compareBasketItems` / `compareBasketItemsBatch` / `searchOrgs` / `ecoGraph` / `recList` 路径 |
| `src/api/service/index.ts` | 补 `svcMeta` / `svcCompareBasketGet` / `svcCompareBasketAddItems` / `svcCompareBasketRemoveItem` / `svcCompareBasketBatchRemove` / `svcSearchOrgs` / `svcEcoGraph` / `svcRecList` defineApi；再导出 `SVC_ECO_EDGE_TYPES` |
| `src/api/service/types.ts` | 补 `SvcSearchFilter` / `SvcSearchOrgs*` / `SvcEcoGraph*` / `SvcRecList*` / `SvcMeta*` / `SvcBasket*` 共 16 类型（对齐 PC #275–635） |
| `scripts/svc-api-contract.test.mjs` | 新增契约自检（8 叶/7 端点 key/8 函数/16 类型 + 诚实性注释锚点） |

## 验收证据

- `node scripts/svc-api-contract.test.mjs` ✅（8 叶 / 7 端点 / 8 函数 / 16 类型）
- `npm run type-check`：唯一报错 `chainBlockReportDocument.ts(735)` 为**并行 INTEL-D 会话工作区活产物**，已用 `git stash` 隔离本单改动复跑验证——**基线同样报错，非本单引入**。本单 5 文件不含类型错误。
- `node --test scripts/svc-api-contract.test.mjs` ✅ fail 0
- CI：commit `6b58a68` 已推 `origin/dev`，等 Pipeline 绿（K8s dev 自动 rollout）。

## 偏离说明

- 无功能偏离。PC `SvcPortalVizData` 等已在 mobile 存在的类型不重复移植。

## 架构合规自检

- ✅ 调用链（前端 → Java REST → Python /internal，不可越层）：仅定义 `/svc/topic/v1/**` Java 门面端点
- ✅ D8 Design：本单无 UI 改动，不涉及
- ✅ D9 数据血缘：类型注释保留诚实性约束（禁前端重算 score / 禁 fixture / relation_top 不当图谱）
- ✅ D10 交互规范：本单无 UI 改动，不涉及
- ✅ D12 demo/lumen 隔离：零 demo 依赖，未 merge demo 代码
- ✅ 可观测埋点：defineApi 走 `@/utils/http` 统一封装（含 trace 上报），与仓现行链路一致
- ✅ CI/CD：commit 推 `origin/dev` → Pipeline → K8s dev rollout

## 开放项

- B/C/D/E 单（`FE-TOPIC-SMALL-SVC-{CHAIN,ORG,REC,SEARCH}-L01`）依赖本单，已解锁。

## cost

- actual_tokens ≈ 60k；model_used: glm-5.3；actual_cost ≈ $0.9；cost_warn: green
