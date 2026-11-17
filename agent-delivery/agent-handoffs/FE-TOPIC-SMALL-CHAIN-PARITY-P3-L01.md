# FE-TOPIC-SMALL-CHAIN-PARITY-P3-L01 · CMS/维护页小屏化（overview-cms + maintenance）

- **状态**：integration（待联调确认）
- **执行**：agent:frontend-agent
- **监管**：human:孔东
- **仓库**：lumen-ui-topic-mobile（dev，commit `7b18cf5`）
- **日期**：2026-11-17
- **ponytail**: full（日常 feature 全强度；本单为对照 PC 仓裁剪移植，删除侧无空间，新增文件均为 PC 已有对应物的最小移植）

## 1. 范围与实现（对照任务 DoD）

| DoD | 实现 |
|---|---|
| overview-cms / maintenance 从 NotAdaptedView 换真组件 | ✅ `IndustryOverviewCmsView.vue` + `IndustryMaintenanceView.vue`，ADAPTED_PAGES 注册 |
| CMS 审/发主链路可完成；运营类交互从简（R3 可用级） | ✅ 草稿保存/发布/下架三动作走真接口；富文本降级多行文本+白名单；select 降级原生下拉 |
| 路由注册 + 站内跳转核验；nav 口径不变 | ✅ 两 path 注册；`nav.ts` 未动（maintenance 侧栏可见、overview-cms 在门户 CMS 组，原样） |
| 工程自检三绿 + handoff 裁剪声明 | ✅ type-check / test 78/78 / build；裁剪声明见 §3 |

## 2. 交付清单

**新文件（lumen-ui-topic-mobile）**：
- `src/views/industry/IndustryOverviewCmsView.vue` — 产业全景内容管理小屏版
  - 列表屏：产业字典（`industryClusters` L0 展平；mock 回退 3 产业演示字典）× 七块状态总览（未维护/草稿/已发布），关键词+状态筛选（宽口径「任一维度命中」，与 PC C-2 同口径）
  - 编辑屏：七块 Tab（介绍/特色/集群/竞争/历程/本地数据/图谱），保存草稿/发布/下架
  - 图谱块：环节节点行编辑（名称/分段/标注/说明）+ 上下游关系行编辑（起点/关系/终点），校验口径与 PC `panoramaChainGraphModel` 一致（空名/重名/自环/未建端点）
- `src/views/industry/IndustryMaintenanceView.vue` — 维护管理壳小屏版
  - 15 项 Tab 与 PC `config/industryMaintenance.ts` 逐字一致（防漏测试锁定）
  - 三组折叠（内容运营/图谱运营/分析配置），当前组自动展开；tab query 路由同步
  - 写侧不接后端（与 PC 同口径：空态 + 禁用按钮 + 警示条「禁止把资讯冒充介绍或历程」）
- `src/api/cms/cmsOps.ts` — CMS Ops API 裁剪移植（panorama 前缀 + list/create/update/publish/unpublish/delete + listAll 翻页聚合）
- `src/api/cms/cmsPanoModel.ts` — 七块 schema + `toApiBody`/`fromEnvelope`（panorama 子集；`ROW_BAG`：dev_history→events、sz_metrics→metrics；chain_graph→graph.nodes/edges）
- `src/api/cms/cmsPanoStore.ts` — 双态 store（USE_MOCK=localStorage 种子 / 真实态 Java CRUD + 静默 reload）
- `src/api/cms/cmsPanoMockSeeds.ts` — mock 种子（PC `cmsMockSeeds.ts` pano_* 子集）
- `src/api/cms/htmlWhitelist.mjs` + `htmlWhitelist.d.mts` — HTML 白名单净化（PC 逐字移植）
- `src/api/cms/types.ts` — CmsRecord/CmsColumn 类型（panorama 子集）
- `scripts/chain-p3.test.mjs` — 6 项防漏自检（见 §5）

**修改**：
- `src/router/index.ts` — ADAPTED_PAGES 注册两 path

## 3. 小屏裁剪声明（对齐规划 R3「可用级」）

1. **富文本 → 多行文本**：PC `CmsRichText` 编辑器降级为 `van-field textarea`；保存仍经 `sanitizeCmsFields` 白名单净化（p/h/list/strong/a/img/br），正文 HTML 契约不变。
2. **select → 原生下拉**：`a-select` 降级 `<select>`（OS 原生滚轮最贴合移动习惯；pano 域选项均 ≤4 个，弹层 picker 反而重）。
3. **图谱块无 G6 实时预览**：维护态只做行编辑 + 「已建环节」清单提示；预览走门户全景页（graph 块发布后在 `/industry-center/panorama` 可见）。
4. **媒资上传不进本单**：pano 域七块无 file 字段，无需移植 `uploadPolicyMultimedia`。
5. **a-table → 卡片网格**：七块状态以 2 列 grid tag 呈现，点任一块进编辑屏（对齐 PC「图谱 tag 可点」交互）。

## 4. 架构合规自检

| 铁律 | 状态 |
|---|---|
| D8 Design token（--sci-* 变量、Vant 控件、Arco Empty 图标） | ✅ 与仓内既有页面同口径 |
| D9 血缘 | ✅ 本页为 CMS 运营面，无统计数字；不涉及 metric ⓘ 角标义务 |
| D12 demo/lumen 隔离 | ✅ 只对照 PC `lumen-ui-topic` 真源移植，未读 demo-* 代码 |
| D10 交互规范 | ✅ 表单校验 toast 反馈、禁用态诚实（维护页按钮 disabled）、空态 `EmptyState` |
| 调用链 | ✅ 前端 → Java REST（`/cms/cms-ops/v1/topic-panorama/**`），无越层 |
| 观测埋点 | ✅ 走仓内统一 `request`（X-Trace-Id/traceparent 自动注入） |
| 可逆性 | ✅ 单 commit `7b18cf5` 可 revert |

## 5. 验收证据

- `pnpm type-check` ✅（exit 0）
- `pnpm test` ✅ **78/78**（原 72 + 新增 `chain-p3.test.mjs` 6 项：路由注册/schema 逐字/ROW_BAG/写链路/净化与校验/15 Tab 逐字）
- `pnpm build` ✅（11.4s，产物 dist/）
- push：`2a9c60f..7b18cf5 dev -> dev`（GitLab CI 自动部署链触发）

## 6. 防漏扫描摘要（对照移动仓 P 系列 handoff 惯例）

- D.1 页面差集：本轮目标 2 页全部落位，产业分析大模块 11 页（overview/search/panorama/diagnosis/regional/shenzhen/results/reports/overview-cms/overview-viz/maintenance）已全部适配完毕，无 NotAdaptedView 残留（产业域内）。
- D.5 契约防漏：`industry_id` 写入 `toApiBody`；`contentTypePath` 连字符转换；`isServerContentId` 数字判定——三处契约点与 PC 逐字一致（测试锁定）。

## 7. 偏离说明

无。裁剪均在 R3「可用级」授权范围内且已声明（§3）。
