# Handoff — LUMEN-SVC-FE-ORG-BASKET-ENTRY-L01

- **任务**：服务机构产业领域分析对象集入口对齐 demo——分析页经系统对比篮 picker 组装分析对象
- **执行**：agent:frontend-agent · **监管**：human:淮政玮 · **类型**：bugfix（口径矛盾修复）
- **日期**：2026-10-20 · **强度**：ponytail full
- **背景**：排查「服务机构产业领域分析」菜单时发现，lumen 分析页对象集为直选 `SvcOrgPickerModal`（US-01 文本口径），而 demo 已评审原型（R2B，2026-08-05 用户口径）为**两层组装**：分析页 → 系统对比篮 picker（勾选回传）→ 篮内「新增」从在库机构列表选入篮。用户 2026-10-20 拍板对齐 demo。

## 一、范围与实现

| demo 原型（真源 `demo-ui-topic/.../ServiceOrgAnalysisPage.tsx`） | lumen as-built |
|---|---|
| 分析条件栏「打开对比篮」按钮（已选时文案「打开对比篮调整对象」） | ✅ `openCompareBasket()` → `appendCompareBasketPickerParams({objectType:'service_org', min:1, max:50})` |
| 空态门 Empty「尚未选择分析机构，请先在对比篮中组装分析对象」+「打开对比篮」主按钮 | ✅ `a-empty` 同文案 + 内嵌按钮 |
| capability 走 2~5 家 | ✅ 统一 `openCompareBasket` 按 workspace 分流（capability 2~5 不变） |
| 确认回传 `org_ids[]` + `source=compare-basket`，标签栏「来源：对比篮」 | ✅ 复用既有 `writeCompareBasketSelectionToParams` / `seedObjectSet` 篮分支 / `fromBasket` 角标，零改动 |
| 篮内「新增」= 在库机构列表（`CompareBasketAddModal`，只调 Java `search/orgs`） | ✅ `ServiceOrgCompareBasketPanel` 已有，本任务未动；z-index 已核（system-surface 120 < modal 140，浮层内弹窗正常压顶） |

### 变更清单（lumen-ui-topic，net -384 行）

- `src/views/service/ServiceOrgAnalysisWorkspace.vue`：直选入口/`SvcOrgPickerModal`/`confirmPicker`/`cancelPicker`/`openCapBasket` 删除；新增统一 `openCompareBasket`；空态门与按钮文案对齐 demo；capability `@open-basket` 直绑；头部注释更新
- `src/views/service/SvcOrgPickerModal.vue`：**删除**（直选 Modal 死代码，0 引用）
- `src/views/service/serviceOrgAnalysis.css`：`svc-org-picker-*` 14 个死样式块删除（106 行）
- `src/views/service/serviceOrgSearchModel.ts`：`pickerSearchBody` 删除（唯一消费者已删；`SERVICE_TYPE_ENTRIES` 仍被 `parseServiceOrgQuery` 使用，保留）
- `src/views/service/serviceOrgAnalysis.selfcheck.mjs`：断言改为「入口=对比篮 picker、直选器已删」防回退
- `.env.development`：**未纳入本任务提交**（工作区既有本地网关注入，属他人联调改动）

## 二、调用链合规自检（§2 铁律）

- D1 调用链 ✅：名单仍只调 Java `search/orgs`（经 `CompareBasketAddModal`）；分析 CREATE/GET/RESULT 不变；未越层
- D8/D9/D10 ✅：未动视觉 token / ⓘ 角标 / 交互规范；评审挂载点保留
- D12 ✅：只改 lumen-ui-topic，未引用任何 demo-* 服务
- 可观测 ✅：未动埋点面

## 三、验收证据

- 自检：`node src/views/service/serviceOrgAnalysis.selfcheck.mjs` → `coverage+profile ok`
- 类型门：`pnpm type-check` → 0 错
- 构建：`pnpm build` → ✓ built in 15.11s
- 提交：lumen-ui-topic `origin/dev`，commit `[agent:frontend-agent] LUMEN-SVC-FE-ORG-BASKET-ENTRY-L01 ...`

## 四、偏离与开放项

- **US-01 文本矛盾未回改**：`USM-SVCCHAIN-ORG-ANALYSIS` 中 US-01 仍写直选口径；R2B 篮口径已获用户裁定优先，USM 文本修订建议随下次定义任务收口（不在本 bugfix 范围）。
- demo `capability` 空态另走 `SvcOrgCapabilityBoard` 篮空门（`CAP_BLOCKER_TEXT.basket_empty`），与 demo 行为一致，未额外改动。
- 回归建议：QA 过一遍 field 空态 → 打开对比篮 → 篮内新增 → 勾选 1~50 家确定 → 开始分析全链路。
