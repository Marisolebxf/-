# POL-AUDIT-FE-REFACTOR-L01 · 政策跟踪审核整改①：3 项功能冗余 + 4 项设计不合理（重构）

> 来源：2026-11-05 科技政策跟踪模块需规符合性审核（原需规 1.1.1.1.4.2.1-4.2.3 全量对照 + 核增 4.2.4 PC-01~PC-17）。
> 审核结论：44 原生叶 + 17 核增叶全实现，0 叶级遗漏；查出冗余 R1-R3、设计问题 D1-D4、偏差 B1-B6。本单处理 R+D 七项；B 系列见 POL-AUDIT-FE-BIAS-L02（前端）与 POL-AUDIT-API-GAP-L03（接口登记）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 孔东监管限定（2026-11-04 裁定）：改动停在本地工作区，等孔东人工确认后才 commit/push |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 全部用既有模式（组件封装/组合式拆分/既有公共件复用），零新依赖；D4 仅注释标注不改行为；未用 YAGNI 跳过 D8/D9/D10（MockBadge 顺带修复上线态角标泄漏） |

## 问题清单

- R1：全景页高级/普通检索两分支结果渲染体 ~90 行 × 2 逐行重复（卡头+二次筛选条+结果体）
- R2：parse 页内联 `MockBadgeInline`（~30 行）与公共 `MockBadge.vue` 语义重复，且无 reviewMode 自闸（上线态泄漏「演示数据」角标，违反 D9 零泄漏）
- R3：CompareTab「标杆比对 / 对标报告生成与导出 / 对标结果可视化展示」三卡都只跳同一 `BenchmarkCompareModal`，重复入口
- D1：panorama/index.vue 1813 行巨石页（含订阅双轨映射 ~200 行）
- D2：全景页 header 统计卡「落地实效 92.5 / 覆盖地区 32」为全局快照值，常驻 header 与检索结果卡并列，跨 Tab 语义漂移
- D3：推演页 `dimsEvalDone` 父 `ref(true)` + 子 gates 双真值源，首帧可能闪变（父 true → 子首抛 false）
- D4：治理页 `kpiValue` 魔法数 `-28 / 下限 40` 无来源与清理时点标注

## 修改内容

### R1 — 抽取 `PolicySearchResultPanel.vue`（新文件）

- 新建 `src/views/policy/panorama/components/PolicySearchResultPanel.vue` + `styles/pp-search-result.css`（样式自含，复刻铁律 2）
- 两分支渲染体替换为该组件（props 下传 + 事件上抛，仅 title 文案不同）
- panorama/index.vue 净减 ~170 行

### R2 — 删内联件，公共 MockBadge 补样式自含

- parse/index.vue 删 `MockBadgeInline`（内联 defineComponent ~30 行），4 处使用点换公共 `MockBadge`
- `MockBadge.vue` 补 `margin-left: 6px`（修复原「裸样式」缺陷）；**顺带修复上线态角标泄漏**（公共件自带 reviewMode 自闸，内联件没有）

### R3 — CompareTab 三入口合并

- 三卡（标杆比对/报告生成导出/可视化展示）合并为一张「标杆比对（报告生成与可视化）」全流程卡；描述合并三能力文案

### D1 — 订阅双轨拆 `subscriptionStore.ts`（新文件）

- 新建 `src/views/policy/panorama/subscriptionStore.ts`：Storage 读写、契约映射（toSubscriptionBody/fromSubscriptionItem）、名称缓存、useSubscriptionFamily 组合式
- index.vue 删 ~200 行映射逻辑，接线消费；文案工具复用 `policySubscriptionSeed` 既有导出（formatFreqLabel/formatSubscriptionConditions），不重复实现

### D2 — 全景页统计卡跨 Tab 语义修正

- 前 4 卡（当前命中/本周新增/类型热点/收藏政策）保持随检索联动（语义正确）
- 「落地实效/覆盖地区」两张全局快照卡收窄为仅检索语义 Tab（search/trend）展示（`showSearchScopedStats`）；数值 live 接线留给 L02 B1

### D3 — dimsEvalDone 单一真值源

- simulation/index.vue 父组件初始值 `ref(true)` → `ref(false)`；真值源收敛到 EstimateWorkbench gates（watch immediate 首帧同步）；消除双源闪变

### D4 — 治理页魔法数标注

- `kpiValue`（-28/下限 40）、`totalCount = 3256` 补来源（demo L318 冻结演示逻辑）与清理时点（BE-POL-CONTRACT-01 契约冻结后，联动 L02 B1）

### 自检适配（语义等价迁移，非改断言强度）

- FE-POL-01B.test.mjs：勾选态断言指向 PolicySearchResultPanel（封装后两分支 :selected-ids 都在共享面板内）
- displayPanoramaQuery.compliance.test.mjs：DoD-3 订阅数据源断言指向 subscriptionStore.ts（D1 拆分后真源位置）

## 测试结果

- `pnpm type-check`：**政策模块 0 错误**（仓级剩余 8 错全在 knowledge-graph，为其他会话 FE-KG-03A 未提交产物，多会话保护规约不碰；该会话修复后 build 时已清零）
- 政策模块自检 15 个：13 绿；**FE-POL-04A / FE-POL-06A 2 个失败为存量失败**（stash 验证：与本次改动无关；06A 断言 `v-if="reviewStore.reviewMode"` 写死老组件写法、04A 断言 `review.reviewMode` 但页面已解构 `reviewMode`，两测试落后于页面重构；Interfaces 冻结，改他人测试须 coordinator，不在本单处理）
- `pnpm build`：**绿**（37.95s）
- 更新后的 FE-POL-01B / compliance 复跑：**全绿**

## 遗留风险

- R1 封装后两分支行为需人工回归一次（普通/高级检索、分组/列表视图、二次筛选、导出分享）
- ~~04A/06A 存量测试失败建议 coordinator 另派测试修正单~~ → **2026-11-05 12:18 用户裁定：去掉两条过时断言（04A 旧正则 `review\.reviewMode` 匹配 0 处 / 06A 链路卡有意常显），走查事项并入原 owner；已随 dev 565c094 修复，政策模块自检 15/15 全绿**
- L02（B1/B5/B6 前端侧）与 L03（B2/B3/B4 接口登记）待本单确认后推进

## CI/CD（必填）

- 分支：dev（**未 commit/push——孔东监管限定，等人工确认**）
- commit：待孔东确认后提交
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：本地 dev server 待孔东走查

## 涉及文件

**lumen-ui-science-pc（本地工作区，待确认）**

- `src/views/policy/panorama/components/PolicySearchResultPanel.vue`（新）
- `src/views/policy/panorama/styles/pp-search-result.css`（新）
- `src/views/policy/panorama/subscriptionStore.ts`（新）
- `src/views/policy/panorama/index.vue`（R1+D1+D2）
- `src/views/policy/panorama/components/CompareTab.vue`（R3）
- `src/views/policy/parse/index.vue`（R2）
- `src/views/policy/simulation/index.vue`（D3）
- `src/views/policy/governance/index.vue`（D4）
- `src/components/lineage/MockBadge.vue`（R2 样式自含）
- `src/views/policy/panorama/FE-POL-01B.test.mjs`（自检适配）
- `src/views/policy/panorama/search/displayPanoramaQuery.compliance.test.mjs`（自检适配）
