# SYSINT-03-02A-L01 · 产业全景内容管理 前端运维页（lumen-ui-topic）

> **任务**：SYSINT-03-02A-L01（`task_type=feature`，E-PM-DELIVERY / SYSINT-03 子域）
> **执行**：`agent:frontend-agent` · **监管**：`human:孔东`（JAVA 叶头部标注「孔东线」）
> **仓库**：`repos/lumen-ui-topic`（origin/dev）
> **日期**：2026-10-24 初版 · 2026-10-27 图谱待确认入口 + 本 handoff 补录建档
> **后端叶**：`SYSINT-03-02A-JAVA-L01`（agent:api-agent，监管 human:徐滕强；pano 5 类写接口 + §3.1 published 读端点，51/51 单测绿）
> **需规真源**：`bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.5.6.1（7769–7809 行）
> **契约真源**：`平台基建-PLATFORM/产物/PORTAL-CMS-专题全景.md`（淮政玮 2026-10-24 确认，字段冻结）

---

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东`（线主）→ `agent:frontend-agent` 执行 |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | JAVA 叶 2026-10-24 落地后孔东线开前端叶；2026-10-24 随三模块 CMS 初版同笔落地；2026-10-27 按需规 7769–7809 对照分析补图谱待确认入口并建档。本阶段到此收口（用户拍板「先这样」），缺口见 §遗留。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 SYSINT-03-15 框架 5 件套 + `PanoramaSectionForm`（正文/历程行两组件收敛）；零新依赖。富文本保存前契约白名单过滤。未用 YAGNI 跳过 D8/D9/D10（运营页无统计数字）、可观测、调用链（mock 态无网络层）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂 Headroom。 |

## 需规对照（7769–7809 三块 6 项）

| 需规条目 | 落点 | 状态 |
|----|------|------|
| 1.1(1) 产业链结构绘制维护（7779–7781） | 无 content_type（契约级缺口） | ⏸ 挂待确认入口 |
| 1.1(2) 关键环节标注维护（7783–7785） | 无 content_type（契约级缺口） | ⏸ 同上 |
| 1.2(1) 产业概况摘要编辑（7791–7793） | `pano_industry_intro`（title+富文本） | ✅ 正文即满足（多语言见遗留 #3） |
| 1.2(2) 发展历程事件录入（7795–7797） | `pano_dev_history` events 五字段 | ✅ 事件半边（阶段/专家观点见遗留 #4） |
| 1.3(1) 本地产业数据维护（7803–7805） | 无 content_type（契约级缺口） | ❌ 遗留 #5 |
| 1.3(2) 特色/集群/竞争地位（7807–7809） | `pano_sz_feature` / `pano_cluster_effect` / `pano_competitive_position` | ✅ CMS 侧（门户装配见遗留 #1） |

**口径说明**（监管人 2026-10-27 更正）：需规 7793 只要求「编辑摘要内容」，未要求优势/亮点/挑战结构化拆分——`pano_industry_intro` 正文形态即满足，不拆字段。

## 修改内容

页面：`/industry-center/overview-cms`（菜单【管】-产业全景内容管理）→ `src/views/cms/panorama/PanoramaCmsWorkspace.vue`。

- **列表屏**：产业 × 6 列状态矩阵（产业链图谱 / 介绍 / 深圳特色 / 集群效应 / 竞争地位 / 发展历程，三态 tag 未维护/草稿/已发布）+ 关键字筛选；
- **编辑屏**：5 Tab 对应契约 pano 5 类（`PanoramaSectionForm`：正文富文本或历程 rows，草稿/发布/下架状态机，发布前必填校验，HTML 白名单过滤）；
- **图谱待确认入口**（`284e01c`）：列表「产业链图谱」列橙色「待确认」tag + 编辑页专用 Tab（a-result 说明需规原文与缺口原因）+ Modal 详情——不做假维护，防后人误判为遗漏。

**提交轨迹（origin/dev）**：

| commit | 日期 | 说明 |
|---|---|---|
| `2be3717` | 10-24 | 三模块 CMS 初版（pano 5 类 schema + Workspace + SectionForm + mock 种子，与 ent/svc 同笔） |
| `0495b96` | 10-24 | 表格与表单类型对齐修正 |
| `284e01c` | 10-27 | 图谱维护待确认入口（+73/−8） |

门户侧既有接线（本叶范围外但相关）：`IndustryOverviewPage.vue` 137–146 已留 `row?.intro ?? row?.cms?.intro`、`row?.history ?? row?.cms?.history` 消费口，等 Java overview 聚合返 cms 字段。

## 测试结果

- `npx eslint src/views/cms/panorama` ✅；`npm run type-check` ✅（`284e01c` 时点全绿，含全仓）
- mock 走查：5 Tab 草稿→发布→下架状态机、历程行必填校验、列表状态矩阵刷新正常；图谱入口三处（列 tag/Tab/Modal）可打开说明

## 遗留风险（缺口清单，按优先级）

**P1 门户装配（前端可先行）**
1. **三块文字门户零渲染**：`pano_sz_feature/cluster_effect/competitive_position` 全仓仅存在于 CMS 文件；门户「区域特色研判」仍 Q061 占位空态（`IndustryOverviewPage.vue` 668–674）。需 `industry.cms` 扩三字段渲染 + mock 补字段（Java 聚合侧配合走内部 published 端点，浏览器不直连——契约偏离 #5 四区模型）。
2. **发展历程渲染是 JSON dump**：门户时间线 `JSON.stringify(item)` 直出（`IndustryOverviewPage.vue` 573），应渲染结构化卡片（date/title/body_html/source）。

**P2 CMS 维护侧（契约内可做）**
3. **多语言版本管理**（需规 7793「支持多语言版本管理」）：契约信封 `locale` 可写但表单未暴露，无多语言版本列表/切换；Java 运营 list 端点无 locale 过滤参数，筛选方式需与 Java 确认。

**P3 契约级缺口（淮政玮线提案，前端无法单方解决）**
4. **历程「阶段定义+特征描述+专家观点」**（需规 7797 后半）：events 无 stage/expert 字段。⚠️ JAVA 偏离表 #6 只拷贝 5 个契约键、多余键静默剔除——前端私加键必被丢弃，契约变更先行。
5. **本地产业数据维护**（需规 7803–7805）：无 content_type；契约 §1.3 已记录「深圳各区计数无 metric_id」缺口悬空。
6. **图谱维护本体**：待确认入口已挂，数据源与 Java snapshot 关系未拍板。

**P4 联调接线（统一动作）**
7. mock store → Java REST：路径段连字符互转（`pano-industry-intro`↔`pano_industry_intro`）；rows 键 `bodyHtml`→契约 `body_html`；events 升序由 Java 排（前端免排）；产业字典 mock slug→`industry_id` 编码（`useIndustryCatalog`）；`publish_status` 小写。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`2be3717` → `0495b96` → `284e01c`（均已推送）
- pipeline URL / ID：随 dev CI 自动触发，未单独验收
- 部署 namespace / 镜像 tag：N/A（mock 态）
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：`npm run dev` → 菜单【管】产业全景内容管理（`/industry-center/overview-cms`）✅

## 可观测性（建议）

- N/A（mock 态无网络请求）

## 架构合规

| 铁律 | 结果 |
|------|------|
| 调用链（接线上后 前端→Java REST→内部 published） | 将符合（当前 mock） |
| D8 Arco + 仓内 token | 符合 |
| 运营页不挂统计 ⓘ / 不编数字 | 符合（图谱缺口不造假维护） |
| D12 不调用 demo 服务 | 符合 |

## 涉及文件（lumen-ui-topic）

- `src/views/cms/panorama/PanoramaCmsWorkspace.vue`（列表/编辑/图谱待确认入口）
- `src/views/cms/panorama/PanoramaSectionForm.vue`（正文与历程表单）
- `src/components/cms/cmsTypeSchema.ts`（pano 5 类 schema）
- `src/components/cms/cmsMockSeeds.ts`（pano 种子）
- 门户消费口：`src/views/industry-center/IndustryOverviewPage.vue`（cms.intro / cms.history 预留）

## 修订记录

| 版本 | 日期 | 作者 | 说明 |
|---|---|---|---|
| 1.0 | 2026-10-27 | frontend-agent | 补录建档：初版轨迹 + 需规对照 + 遗留缺口 P1–P4；本阶段按用户拍板收口 |
