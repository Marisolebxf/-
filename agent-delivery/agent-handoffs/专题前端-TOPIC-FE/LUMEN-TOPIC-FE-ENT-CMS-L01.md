# LUMEN-TOPIC-FE-ENT-CMS-L01 · 企业发展内容管理补需规缺口（基础档案 / Top30 榜单 / 重点企业全景图）

> 格式参考 `templates/handoff-template.md`。需规真源：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.5.6.3（7841–7881 行）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `coordinator_dispatch` |
| 说明 | 用户令「按缺失项升级企业发展内容管理页面」，需规对照缺口分析见前置结论（本 handoff §问题清单）。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 CMS 组件体系（schema 驱动表单 / mock store / 草稿-发布状态机），零新依赖。未用 YAGNI 跳过 D8/D9/D10、可观测、调用链（纯 mock CMS，无网络层）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂 Headroom。 |

## 问题清单（需规对照缺口，升级依据）

需规把「企业发展内容管理」拆为 3 块 6 项，升级前对照：

| 需规条目 | 行号 | 升级前状态 |
|----|------|------|
| 1.1.1 企业基础档案维护（名称/成立时间/行业/规模） | 7851–7853 | ❌ 无任何维护入口，「基础信息」Tab 实为明星名单 |
| 1.1.2 企业成长轨迹维护（时间节点事件） | 7855–7857 | ✅ `star_story` 已覆盖 |
| 2.1 重点企业全景图（专家筛选/专属档案/合作·供应链·竞争关系） | 7859–7865 | ⚠️ 仅链位自由文本关系，无成员管理、无关系类型、无关系对象 |
| 2.2 技术力/商业力 Top30 榜单（维度定义+名单+依据+评述） | 7867–7869 | ❌ CMS 端完全没有 |
| 3.1 明星企业介绍（详介/核心成果/代表产品/荣誉资质） | 7871–7877 | ⚠️ 产品/技术/团队有，荣誉资质无 |
| 3.2 深圳企业介绍（档案+专家定位/优势/竞争力分析） | 7879–7881 | ✅ `sz_enterprise_intro` 覆盖；但 `sz_focus_set` 圈定名单无管理入口 |

另发现：`EnterpriseCmsChainTab.vue`（链位结构维护）与 `EnterpriseCmsListTab.vue` 为孤儿组件（无路由引用），链位环节码字典断链。

## 修改内容

仓：`lumen-ui-topic`。页面：`enterprise/development-cms`（`EnterpriseCmsWorkspace.vue`）。信息架构从「1 列表 + 7 Tab」升级为「1 列表屏 + 4 功能屏」，6 项需规全部落位：

| 屏 | 内容 | 对应需规 |
|----|------|---------|
| 屏1 企业列表 | 原筛选保留 + 新增「基础档案」三态状态列（未维护/草稿/已发布）+ 三个产业级入口按钮 | — |
| 屏2 企业编辑（8 Tab） | 新增「基础档案」Tab（`ent_basic_profile`：成立时间/所属行业/规模/地址 + 介绍正文 + 荣誉资质 rows）；「发展历程」更名「成长轨迹」；其余 7 Tab 保留 | 1.1.1 / 3.1（荣誉资质） |
| 屏3 重点企业全景图（新） | 三子 Tab：重点企业集（模态入库：企业+环节+关系类型枚举+关系对象企业+叙述，`key_enterprise_set` 增 `relation_type`/`related_enterprise_code` 列）；深圳重点圈定（`sz_focus_set` 勾选管理）；链位结构（接回孤儿组件 `EnterpriseCmsChainTab`） | 2.1 |
| 屏4 技术力/商业力榜单（新） | 双榜 radio 切换；Top30 计数 `N/30`、满员禁增、名次查重（提示占用企业）、同榜企业去重警示；评估维度定义子表（维度/说明/权重，随榜单类型联动） | 2.2 |

新增 schema：`ent_basic_profile`、`ent_rank_dimension`、`ent_competitive_rank`（`cmsTypeSchema.ts`）+ 对应 mock 种子；helpers 新增 9 个工具函数（榜单读取/名次查重/重点集与深圳圈定读取等）；`EnterpriseBlockDrawer` 增可选 `saveHandler` 钩子（自定义校验保存，不破坏既有调用方）；企业池 `CMS_MOCK_ENTERPRISES` 扩至 6 家 + 注册地字典。

`EnterpriseCmsListTab.vue` 仍为孤儿（未接回，旧版块式工作台与新版五屏重复，建议后续删除或留作参考）。

## 测试结果

- `npx eslint src/views/cms/enterprise src/components/cms/cmsTypeSchema.ts src/components/cms/cmsMockSeeds.ts` ✅ 0 error
- `npm run type-check`：本次改动文件 0 错误；仅剩**既有**错误 `StarEnterprisesPanel.vue(217)` Arco filter-function 类型不匹配（非本次引入，遗留）
- 交互走查（mock 态）：榜单满员/名次冲突/重复上榜/重点企业重复入库均有拦截提示；基础档案草稿-发布-下架状态机正常

## 遗留风险

- 数据层仍为 `useCmsMockStore`（localStorage mock），后端 CMS 契约未定；联调时按 contentType 替换为真实 API，schema 抽象已就位
- `key_enterprise_set` 新增两列后，旧 localStorage 数据（无 `relation_type`）会显示空——种子已更新，真实数据迁移时需补默认值
- `StarEnterprisesPanel.vue(217)` 既有类型错误待修（建议单独小单）
- `EnterpriseCmsListTab.vue` 孤儿组件去留待定

## CI/CD（必填）

- 分支：`dev`
- commit：`804996c`（`feat(ent-cms): 企业发展内容管理补需规缺口——基础档案/Top30榜单/重点企业全景图 [agent:frontend-agent]`，8 files / +1178 −40）
- pipeline URL / ID：GitLab push 后自动触发（前端仓无独立 pipeline 配置）
- 部署 namespace / 镜像 tag：N/A（mock CMS 页，无部署变更）
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：`npm run dev` → 菜单【管】企业发展内容管理（`enterprise/development-cms`）✅

## 可观测性（建议）

- N/A（纯前端 mock CMS，无网络请求）

## 涉及文件（lumen-ui-topic @ 804996c）

- `src/components/cms/cmsTypeSchema.ts`（+3 schema、关系列、企业池/注册地字典）
- `src/components/cms/cmsMockSeeds.ts`（+3 种子、关系列数据）
- `src/views/cms/enterprise/enterpriseCmsHelpers.ts`（+9 工具函数）
- `src/views/cms/enterprise/EnterpriseCmsWorkspace.vue`（重写五屏）
- `src/views/cms/enterprise/EnterpriseCmsKeySetTab.vue`（新建）
- `src/views/cms/enterprise/EnterpriseCmsRankTab.vue`（新建）
- `src/views/cms/enterprise/EnterpriseBlockDrawer.vue`（+saveHandler）
- `src/views/cms/enterprise/EnterpriseCmsStandardTab.vue`（清无用 import）
