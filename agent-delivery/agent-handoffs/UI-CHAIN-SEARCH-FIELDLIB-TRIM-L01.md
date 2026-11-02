# UI-CHAIN-SEARCH-FIELDLIB-TRIM-L01 · 产业查询高筛字段库裁剪

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent`（本 Cursor 会话执行） |
| supervised_by | `human:孔东`（dispatch-rules 默认映射） |
| claim_type | `coordinator_dispatch` |
| 说明 | 用户 2026-11-02 16:54 确认建单开工 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 领域/分类走 `hideInLibrary` 标记（复用既有 fieldLibrary 结构，不另起过滤层）；`updatedAt`/`chainTags` 直接删除条目+孤儿变量；未新增依赖 |

## 问题清单（决策记录）

- 用户裁定 2026-11-02：
  - **去掉**：所属产业领域（=Q068 集群名，与「产业」四级树重复）、产业分类（重复）、目录更新时间（无此条件）
  - **移除**：产业链标签（需规 0 提及，与四级树「勾节点」语义重复；demo 夹具设计产物，非 SRS 约束）
  - **暂缓**：产业标签（需规仅算法 API 泛称、无需规约束；demo 库有数据，线上空疑因 lumen-platform-algo-py 部署版本旧于 10-29 灌数——待重新发布显形后另定去留）
- 需规对照：SRS 对产业链分析的要求是 8 类分析工具（产业链分析.md excel_rows 28–42），无高筛字段清单；「产业标签」85+ 处命中全为《05-深度挖掘算法》API 查询维度泛称。**移除不产生范围缺口（±10% 不受影响）**。

## 修改内容

- `src/types/filter.ts`：`FieldDef` 增 `hideInLibrary?: boolean`（通用能力：字段库隐藏、fieldLibrary 保留）
- `src/config/industrySearchConfig.ts`：
  - `domain`/`classification` 加 `hideInLibrary: true`（**保留**在 fieldLibrary——结果内筛选 `refineFieldKeys: ['objectType','domain','classification','tags']` 与条件摘要仍消费）
  - 删除 `updatedAt` 字段条目与 `updatedAt`/`chainTags` options 孤儿变量；删除 `chainTags` 字段条目
- `src/components/filter/FilterPanel.vue`：`filteredLibrary` 跳过 `hideInLibrary` 字段（drawer/page 两变体共用）
- `src/utils/industrySearchModel.ts`：`IndustrySearchField` 类型删 `chainTags`；取值器删 `chainTags`/`updatedAt` 分支；`SEARCH_FIELDS`（DSL 出站闸门）删 `chainTags`/`updatedAt` → **旧保存方案中这两类条件出站时静默丢弃**（安全兜底，不报错）

## 与同工作区并行会话的边界

⚠️ 本仓工作区在开工时已有另一会话**未提交**的「领域→分类 结果内筛选联动」改动（`industrySearchModel.ts` 的 `classificationOptionsFor`/`reconcileClassificationRefine`、`IndustrySearchPage.vue` 的 `refineConfig`、`types.ts`、`industrySearchRefine.selfcheck.mjs`）。本单：
- 未触碰其产物行；`domain`/`classification` 保留 fieldLibrary 正是为不破坏该联动的 refine 下拉
- 联动走 `industryRecordFieldValue(record,'classification')` 与 `SEARCH_FIELDS` 无交集冲突（classification 仍在集合中）
- 两单改动将在验收后由各自监管人协调提交顺序

## 测试结果

- `pnpm type-check`（vue-tsc --build）：**绿**
- 自检 `src/views/industry-center/industrySearchFieldLibTrim.selfcheck.mjs`（node 直跑，9 项断言）：**ALL CHECKS PASSED**
  - 字段库无「目录更新时间」「产业链标签」条目
  - 领域/分类走 hideInLibrary 且仍在 fieldLibrary；refineFieldKeys 未动
  - FilterPanel 跳过 hideInLibrary；model 类型/取值器/出站闸门三处 chainTags 清零
- 手工走查建议（监管人）：高级筛选页字段库不再出现四个字段；结果内筛选下拉（对象类型/所属产业领域/产业分类/产业标签）仍在；含旧 chainTags 条件的查询方案应用后该条件被忽略不报错

## 遗留风险

- 「产业标签」保留待定：依赖 `lumen-platform-algo-py` 重新发布后 catalog 返回真实 tags；若届时产品仍判冗余，按本单同款 `hideInLibrary` 一行即可隐藏
- 旧方案持久化里已存的 `chainTags`/`updatedAt` 条件将静默失效（预期行为，无迁移需要）

## CI/CD（必填）

- 分支：`dev`（**改动停本地工作区未 commit**——人工验收闸门 2026-10-20 裁定）
- commit：待 human:孔东 走查通过后提交（`[agent:frontend-agent]`）
- pipeline / K8s rollout / dev URL：待 push 后生成

## 涉及文件

- `src/types/filter.ts`
- `src/config/industrySearchConfig.ts`
- `src/components/filter/FilterPanel.vue`
- `src/utils/industrySearchModel.ts`
- `src/views/industry-center/industrySearchFieldLibTrim.selfcheck.mjs`（新增自检）
