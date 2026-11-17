# FE-TOPIC-SMALL-CHAIN-PARITY-P0-L01 · 专题小屏·产业分析差单P0：全景页query深链断裂修复

- **状态**：实现完成，待联调+签收
- **执行**：agent:frontend-agent · **监管**：human:孔东
- **仓**：`repos/lumen-ui-topic-mobile`（分支 dev，改动停在本地工作区，待孔东确认推送）
- **日期**：2026-11-17
- **来源**：2026-11-17 mobile↔PC 产业分析大模块对照分析（会话报告 §一.A / §三.P0）
- **ponytail: full**

---

## 1. 范围与实现

### 问题（bug 级）

产业查询页「进入全景图谱」与 Overview 页 `goPanoramaPage` 均携带 `object_type/object_id` query 跳转 `/industry-center/panorama`，但 mobile 全景页 `IndustryPanoramaView.vue` 未引入 `useRoute`，onMounted 只用 catalog 默认值初始化对象——query 被静默丢弃，用户点了某产业链入口却显示默认对象。PC 基线逻辑在 `repos/lumen-ui-topic/src/views/industry-center/IndustryPanoramaPage.vue` onMounted #365–380。

### 修复（最小 diff，单文件）

`src/views/industry/IndustryPanoramaView.vue` onMounted 目录加载后消费 query 四参数，语义逐条对齐 PC：

| query | 分支行为 |
|---|---|
| `object_type=industry_chain` + `object_id` | 定位链；父产业取 `chain.parentIndustryId`（isIndustryId 校验），无父产业回退 catalog 默认产业 |
| `object_type=industry` + `object_id` | 定位产业（isIndustryId 校验，失败回退默认）；`chain_id` 透传 |
| 仅 `industry_id`（无 object_type） | 按 PC else 分支：产业 + `chain_id` 或 catalog 默认链 |
| `as_of` / `asOf` | 写入 `draftAsOf`，loadSnapshot 落在匹配时间态 |

配套细节：

- `applyCommitted()` 仍在 query 消费后调用（committedKey 覆盖 query 条件），首屏不误显「开始分析」。
- **同参双拉防护**：query 重置对象后 `watch([draftIndustryId, draftChainId])` 已排队触发 `loadSnapshot`，onMounted 末尾通过 `changed` 判定跳过显式调用；仅改 asOf（不触发 watch）或完全无 query 时才显式拉——`changed` 判定同时覆盖这两种情况。
- 仅改 asOf、对象等于默认值的边界：`draftAsOf.value !== ''` 命中 changed → 显式拉，正确。

## 2. 偏离说明

- PC 用 `catalog.apiDefaultIndustryId / apiDefaultChainId / firstChainId`（useIndustryCatalog composable）；mobile 仓无该 composable（页面自持 `industries/chains` ref），用等价内联表达式 `resp.defaultIndustryId || industries[0]?.id` / `chains.find(parentIndustryId)`。语义一致，不为此引 composable（ponytail：避免单文件修复扩散依赖面）。
- 未做评审层挂载（IndustryReviewMount 为 PC 专属，mobile 取舍在 PARITY-P2-L01 ⑤ 统一裁定）。

## 3. 产物清单

| 产物 | 位置 |
|---|---|
| 代码 | `repos/lumen-ui-topic-mobile/src/views/industry/IndustryPanoramaView.vue`（未提交，待确认） |
| 差单 | task-registry：本 ID + P1/P2/P3 三张后续单 |
| 本 handoff | `agent-delivery/agent-handoffs/FE-TOPIC-SMALL-CHAIN-PARITY-P0-L01.md` |

## 4. 验收证据

- `pnpm type-check`（vue-tsc --build）✅ 绿
- `pnpm test` ✅ pass 72 / fail 0
- 入口链路静态核验：`IndustrySearchView.goPanorama` 与 `IndustryOverviewView.goPanoramaPage` 的 query 组合（object_type=industry/industry_chain + object_id）均被新分支覆盖；`watch` 双拉防护见 §1
- 待真机联测项：查询页/Overview 页跳转后落在所选对象（本地无移动端运行环境，建议 QA 段补）

## 5. 架构合规自检

- 调用链：仅前端路由内消费 query，无新增后端调用 ✅
- D8/D9：无统计数字变更，MetricMarker 体系未触碰 ✅
- I2-12：committedKey 闸门语义保持（query 条件视为已应用，不自动 create）✅
- C3 拆仓：未写进 lumen-ui-topic ✅
- fe-local-no-auto-commit：改动停本地工作区，未 commit/push ✅

## 6. 防漏扫描摘要（附录 D）

- D.1 页面差集：本单仅涉 `/industry-center/panorama` 一页；其余差距已按 P1/P2/P3 差单登记
- D.2 本地 KPI 接线：无 KPI 改动
- D.3 镜像 vs 矩阵：无指标变更
- D.4 错挂/正名：无
- D.5 契约防漏：`industryPanoramaSnapshot` 请求参数（industryId/chainId/objectId/asOf）不变，仅初始化来源变化

## 7. cost

- actual_tokens ≈ 45,000（含前序对照分析会话）
- model_used: glm-5.3（Cursor agent）
- actual_cost ≈ $0.9 · cost_warn: false
