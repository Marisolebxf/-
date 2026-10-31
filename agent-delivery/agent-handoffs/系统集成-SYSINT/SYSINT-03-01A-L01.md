# SYSINT-03-01A-L01 · 企业发展内容管理 前端运维页（lumen-ui-topic）

> **任务**：SYSINT-03-01A-L01（`task_type=feature`，E-PM-DELIVERY / SYSINT-03 子域）
> **执行**：`agent:frontend-agent` · **监管**：`human:孔东`（JAVA 叶头部标注「孔东线」）
> **仓库**：`repos/lumen-ui-topic`（origin/dev）
> **日期**：2026-10-24 初版 · 2026-10-26 需规缺口升级 · **2026-10-27 补录本 handoff**（初版落地时未单独落档，本文件为追溯补录）
> **后端叶**：`SYSINT-03-01A-JAVA-L01`（agent:api-agent，监管 human:徐滕强；12 类写接口已就绪，27 单测绿）
> **框架叶**：`SYSINT-03-15-L01`（孔东，公共表单框架 5 件套 + 预览路由；commit `5e35bf7` 已落 origin/dev——该叶 handoff「未 push」记述已过时）

---

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东`（线主）→ `agent:frontend-agent` 执行 |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | JAVA 叶 2026-10-23 落地后孔东线开前端叶；2026-10-24 初版三模块同笔提交（02A/03A 前端一并带出，各自 handoff 另补）；2026-10-26 按需规 7841–7881 缺口分析升级为五屏结构。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 SYSINT-03-15 框架 5 件套（CmsContentFrame/CmsRichText/CmsRepeatRows/CmsScalarField/CmsIndustrySwitch）+ schema 驱动表单 + mock store 草稿-发布状态机，零新依赖。富文本保存前仍走契约白名单过滤（htmlWhitelist）。未用 YAGNI 跳过 D8/D9/D10（纯运营页无统计数字，不挂 ⓘ）、可观测、调用链（mock 态无网络层）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂 Headroom。 |

## 问题清单

- **数据层全部 mock**：读写走 `useCmsMockStore`（localStorage，种子 `cmsMockSeeds.ts`），JAVA 写接口（`/cms-ops/v1/enterprise/content/**`）**未接**。本叶不标联调通过。
- 企业主数据是 mock（`CMS_MOCK_ENTERPRISES` 6 家 + 注册地字典），JAVA 叶 §8.1 `enterprise-summary` 接口（dwd 真实 ∪ cms 虚拟 + blocks 状态摘要）才是列表真源，待接。
- 需规 7841–7881「企业发展内容管理」6 项 vs JAVA 契约 12 类：**企业基础档案、技术力/商业力 Top30 榜单不在 12 类契约内**（详见遗留风险 #1）。

## 修改内容

页面：`enterprise/development-cms`（菜单【管】-企业发展内容管理）→ `src/views/cms/enterprise/EnterpriseCmsWorkspace.vue`。

**信息架构（2026-10-26 升级后，五屏）**：

| 屏 | 内容 | 需规对应 |
|----|------|---------|
| 屏1 企业列表 | 产业/名称/明星/重点/注册地筛选 + 基础档案三态列 + 产业级入口 | — |
| 屏2 企业编辑（8 Tab） | 基础档案（新）/明星名单/产品/技术优势/团队与人才/成长轨迹/链位/深圳介绍 | 1.1.1 / 3.1 / 1.1.2 / 3.2 |
| 屏3 重点企业全景图 | 重点企业集（关系类型枚举+关系对象企业）+ 深圳重点圈定 + 链位结构 | 2.1 |
| 屏4 技术力/商业力榜单 | 双榜切换 + Top30 计数/满员禁增/名次查重/同榜去重 + 评估维度定义 | 2.2 |
| 屏5 入选标准 | star_selection_standard 列表 | 超需规补充 |

**Schema 层**（`cmsTypeSchema.ts`，schema 驱动表单的元数据唯一真源）：

- 契约 12 类直译 9 类（star_roster_item / star_selection_standard / star_product_panorama / star_tech_narrative / star_team_strength / star_scientist_ratio / star_story / key_chain_structure / key_enterprise_set / sz_enterprise_intro / sz_focus_set / display_name_alias 中 11 类有表单或行列映射）；
- 2026-10-26 新增 3 类超契约 schema：`ent_basic_profile`（基础档案+荣誉资质 rows）、`ent_rank_dimension`、`ent_competitive_rank`（Top30 榜单）——**JAVA 12 类枚举外，见遗留 #1**；
- `key_enterprise_set` 行增 `relation_type`（合作/供应链/竞争枚举）+ `related_enterprise_code` 两列——契约内子结构 JSON 列，行级字段超契约明细。

**提交轨迹（均在 origin/dev）**：

| commit | 日期 | 说明 |
|---|---|---|
| `2be3717` | 10-24 17:29 | 三模块 CMS 初版（企业发展 + 产业全景 + 产业服务 24 文件；02A/03A 前端一并带出） |
| `0495b96` | 10-24 21:48 | 表格与表单类型对齐修正 |
| `804996c` | 10-26 21:06 | 需规缺口升级：五屏 + 3 schema + 2 新组件（KeySetTab/RankTab）+ 9 helper + EnterpriseBlockDrawer saveHandler 钩子，8 文件 +1178/−40 |

需求对照分析、逐屏交互设计详见姊妹 handoff `专题前端-TOPIC-FE/LUMEN-TOPIC-FE-ENT-CMS-L01.md`（同日产出，编号体系不同但同一次升级的两个视角：该文件重需规对照，本文件重 SYSINT 线对接）。

## 测试结果

- `npx eslint src/views/cms/enterprise src/components/cms/cmsTypeSchema.ts src/components/cms/cmsMockSeeds.ts` ✅ 0 error
- `npm run type-check`：本叶文件 0 错误；既有错 `StarEnterprisesPanel.vue(217)`（Arco filter-function 类型，属 SYSINT-04-04 线，非本叶引入）
- mock 态交互走查：草稿→发布→下架状态机、榜单满员/名次冲突/重复上榜拦截、重点企业重复入库拦截、富文本白名单过滤均正常

## 遗留风险

1. **3 个新 content_type 超契约（P0，联调阻塞项）**：`ent_basic_profile` / `ent_rank_dimension` / `ent_competitive_rank` 不在 JAVA 12 类枚举内，真接 `/cms-ops/v1/enterprise/content/{content_type}` 会 40001「未知 content_type」。需走契约变更（PLATFORM 叶 `PORTAL-CMS-企业发展.md` 字段冻结禁改，变更需 human:淮政玮 线）或映射既有类。**需规 1.1.1 基础档案与 2.2 Top30 榜单本身是契约缺口**，建议登记 WBS。
2. **mock → 真接口接线未做**：`useCmsMockStore` 替换为 Java REST（写侧 `/cms-ops/v1/**` Bearer；网关临时路由 `/cms/cms-ops/v1/**`，2026-10-23 徐滕强批准、联调结束删除）；列表主数据接 §8.1 `enterprise-summary`（其 blocks 状态摘要设计与本页五屏列表天然对齐）。接线索：schema 的 `contentType` 即 REST 路径段，替换点集中。
3. **`key_enterprise_set` 行级新列**（relation_type/related_enterprise_code）：契约子结构 JSON 列内扩展，读侧无影响，但需在联调时与 JAVA 确认 sanitize 白名单放行。
4. `std_updated_at` 键名（JAVA 偏离表 #3）：入选标准表单已用该键，✅ 已对齐。
5. 空态文案（契约 §2.13）由前端渲染：各 Tab 已有 a-empty，✅。
6. `StarEnterprisesPanel.vue(217)` 既有类型错误（04-04 线）建议单独小单修复。
7. 孤儿组件 `EnterpriseCmsListTab.vue`（初版块式工作台，被五屏替代）去留待定，建议删除或明确留作参考。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`2be3717` → `0495b96` → `804996c`（均已推送；`804996c` 经 rebase 后哈希即此）
- pipeline URL / ID：前端仓随 dev CI 自动触发，未单独验收
- 部署 namespace / 镜像 tag：N/A（mock 态，联调接线后随 dev CI）
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：`npm run dev` → 菜单【管】企业发展内容管理（`enterprise/development-cms`）✅ 五屏可用（mock 数据）

## 可观测性（建议）

- N/A（mock 态无网络请求；接 Java 后复用仓内 `observability.ts` 封装，不新增 OTEL 服务名）

## 架构合规

| 铁律 | 结果 |
|------|------|
| 调用链 前端 → Java REST（接线上后）| 将符合（当前 mock，无直连 Python/nGQL） |
| D8 Arco + 仓内 token | 符合 |
| 运营编辑页不挂统计 ⓘ | 符合（无指标数字） |
| D12 不调用 demo 服务 | 符合 |

## 涉及文件（lumen-ui-topic，累计）

- `src/views/cms/enterprise/`：`EnterpriseCmsWorkspace.vue`（五屏主台）、`EnterpriseCmsKeySetTab.vue`、`EnterpriseCmsRankTab.vue`、`EnterpriseBlockDrawer.vue`（+saveHandler）、`EnterpriseSectionForm.vue`、`EnterpriseCmsStandardTab.vue`、`EnterpriseChainSlotsDrawer.vue`、`enterpriseCmsHelpers.ts`、`EnterpriseCmsListTab.vue`（孤儿待定）
- `src/components/cms/`：`cmsTypeSchema.ts`（schema 真源）、`cmsMockSeeds.ts`、`useCmsMockStore.ts`、`cmsEnterpriseStore.ts`、`types.ts` 等（框架叶 03-15 交付）

## 修订记录

| 版本 | 日期 | 作者 | 说明 |
|---|---|---|---|
| 1.0 | 2026-10-27 | frontend-agent | 补录建档：汇总 10-24 初版至 10-26 升级的完整轨迹；明确 mock 未接 Java 与 3 类超契约遗留 |
