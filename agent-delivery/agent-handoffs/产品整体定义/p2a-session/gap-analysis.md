# 科技专题服务系统原始需求 vs 当前实现差距分析

## 版本

Draft v0.1

## 对照口径

源文档：

`/Users/ying/Documents/codex/科技发展态势/docs/科技专题服务系统-实施方案摘录.md`

当前实现：

`/Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic`

判定等级：

- 已覆盖：当前实现有明确路由、页面和主要业务内容。
- 部分覆盖：当前实现有局部入口或相近能力，但未形成源文档要求的完整闭环。
- 缺失：未发现对应主导航、路由或页面。
- 口径偏差：当前实现存在，但产品边界、命名、层级或职责与源文档不一致。
- 待确认：需要产品判断后才能归类。

优先级：

- P0：影响核心业务闭环或当前产品定位。
- P1：重要但可在产品确认后分期补齐。
- P2：后台、运营、系统支撑或后续增强。

## 六大能力域总览

| 能力域 | 源文档二级能力 | 当前实现证据 | 覆盖状态 | 优先级 | 责任角色 | 处理建议 |
| --- | --- | --- | --- | --- | --- | --- |
| 数据查询 | 数据智能呈现、数据智能分析 | `/development/search`、`/industry/search`、`/policy-portal/search`；文件：`src/app/pages/development/SearchPage.tsx`、`src/app/pages/industry/ChainSearchPage.tsx`、`src/app/pages/policy-portal/PolicySearchPage.tsx` | 部分覆盖 | P0 | product-agent | 确认是否需要统一“科技专题数据查询”总入口，还是采用分专题检索入口。 |
| 专题分析 | 技术链、产业链、企业、科研机构、人才、政策、产业服务链、综合智能分析 | `routes.tsx` 与 `Layout.tsx` 覆盖多个专题分析导航组 | 已覆盖 | P0 | product-agent | 进入专题分析细分表，判断各专题能力完整度。 |
| 项目管理 | 项目驾驶舱、项目跟踪管理、项目内容管理、项目资源管理 | 未发现主导航或路由；未发现 `project` 相关页面入口 | 缺失 | P1 | product-agent | 判断项目管理是否属于当前前台版本范围；若属于，应单独开产品定义。 |
| 信息发布 | 编辑工具、推送配置 | 当前页面存在导出、分享、报告生成等零散按钮；未发现编辑工具/推送配置主入口 | 部分覆盖 | P0/P1 | product-agent | 作为前台闭环关键差距确认：分析结果如何发布、推送、沉淀。 |
| 内容运营 | 基础数据管理、专家知识管理、全要素图谱管理、可视化管理、工单申请、门户内容管理 | 企业 IA 文档提到 E-36/E-37 归后台/内容管理侧；前台不进入菜单 | 口径偏差 | P2 | product-agent | 明确为后台支撑域，不要求前台完整覆盖；需定义前台消费哪些维护结果。 |
| 系统支撑 | 账户管理、消息管理、工单管理、任务管理、历史关注 | 有 `CurrentUserProvider`、`perms/matrix.ts` 等权限模拟；未发现消息/工单/任务/历史关注完整模块 | 部分覆盖 | P2 | product-agent | 保留为后台/平台支撑域；当前前台只需说明登录、权限和锁态口径。 |

## 专题分析域细分

| 专题分析子域 | 源文档要求 | 当前路由证据 | 文件证据 | 覆盖状态 | 优先级 | 责任角色 | 处理建议 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 技术链分析 | 技术链全景图谱、新技术热点、产业化潜力、阶段研判、深圳技术发展、瓶颈识别 | `/techchain/panorama`、`/techchain/hotspot`、`/techchain/potential`、`/techchain/stage`、`/techchain/shenzhen`、`/techchain/bottleneck` | `src/app/pages/techchain/*` | 已覆盖 | P0 | product-agent | 当前路由与源文档二级能力匹配度高，后续只需确认数据口径和模型深度。 |
| 产业链分析 | 产业链全景、周期分析、区域指数、关键环节、瓶颈、深圳产业、竞争力评价 | `/industry/panorama`、`/industry/cycle`、`/industry/regional-evaluation`、`/industry/structure-analysis`、`/industry/problem-diagnosis`、`/industry/shenzhen-analysis` | `src/app/pages/industry/*` | 已覆盖 | P0 | product-agent | 覆盖较完整；需确认“产业总体概览/门户产业服务”与专题分析层边界。 |
| 企业分析 | 企业类型、领域分布、技术力、商业力、深圳现状、招引、培育、供应链、痛难点、竞争力 | `/enterprise-center/*`、`/enterprise/type-distribution`、`/enterprise/domain-distribution`、`/enterprise/capability`、`/enterprise/recommendation`、`/enterprise/supply-chain`、`/enterprise/pain-points`、`/enterprise/competitiveness` | `src/app/pages/enterprise/*`、`src/app/pages/development/*`、`docs/ia/enterprise/*` | 已覆盖/口径偏差 | P0 | product-agent | 企业域已有新 IA，需确认其“企业中心”是否替代源文档企业分析目录。 |
| 科研机构分析 | 涉及产业、技术领域、新增动态、深圳现状、合作关系、技术力、引入培育、优势、痛难点 | `/research/overview`、`/research/analysis`、`/research/capability`、`/research/cooperation`、`/research/recommendation`、`/research/support` | `src/app/pages/research-new/*` | 部分覆盖 | P1 | product-agent | 当前合并为 6 个页面，少于源文档 10 类能力；需确认合并口径是否可接受。 |
| 人才分析 | 区域分布、机构分布、供给、关系链、深圳现状、学术力、产业力、引入培育、高校新培育、供需 | `/talent/spatial-layout`、`/talent/comprehensive-evaluation`、`/talent/network`、`/talent/supply-demand`、`/talent/recommendation` | `src/app/pages/talent/*` | 部分覆盖 | P1 | product-agent | 当前聚合为 5 个页面，需确认是否覆盖源文档的人才细分分析。 |
| 政策分析 | 政策时序、区域政策对比、深圳政策现状 | `/policy/overview`、`/policy/analysis`、`/policy/recommendation` | `src/app/pages/policy/*`、`docs/ia/policy/POL-gap-analysis.md` | 已覆盖/部分覆盖 | P0 | product-agent | 分析层 3 页已建；既有 gap 文档指出仍有血缘、metric_id、技术栈等问题。 |
| 产业服务链分析 | 服务机构产业领域、新增趋势、技术力、短板、图谱、引入培育、深圳现状 | `/service/chain-analysis`、`/service/institution-judgment`、`/service/institution-decision` | `src/app/pages/service/*` | 部分覆盖 | P1 | product-agent | 当前 3 页高度聚合，需确认是否允许以“研判/决策”聚合源文档 8 类能力。 |
| 综合智能分析 | 区域创新活力、创新要素、创新协同 | `/intelligence/vitality`、`/intelligence/elements`、`/intelligence/collaboration` | `src/app/pages/intelligence/*` | 已覆盖 | P0 | product-agent | 路由与源文档三类能力一致，后续重点是指标口径与数据来源。 |

## 关键差距清单

| 差距 | 覆盖状态 | 优先级 | 责任角色 | 证据 | 建议 |
| --- | --- | --- | --- | --- | --- |
| 缺统一“科技专题数据查询”总入口 | 部分覆盖 | P0 | product-agent | 仅发现企业/产业/政策分散检索：`/development/search`、`/industry/search`、`/policy-portal/search` | 产品确认是否需要总入口；若需要，后续交给 UE 定义统一搜索/结果态。 |
| 项目管理四类能力未进入当前前台路由 | 缺失 | P1 | product-agent | `routes.tsx`、`Layout.tsx` 未发现项目驾驶舱/项目跟踪/项目内容/项目资源入口 | 判断是否属于当前版本；若属于，先产品定义项目对象、阶段和驾驶舱范围。 |
| 信息发布管理缺编辑工具和推送配置主入口 | 部分覆盖 | P0/P1 | product-agent | 当前只见各页导出/报告/分享类动作，未见独立编辑工具/推送配置路由 | 明确信息发布是否作为“分析成果输出闭环”补齐。 |
| 内容运营中心未作为前台模块实现 | 口径偏差 | P2 | product-agent | 企业 IA 文档明确 E-36/E-37 归后台/内容管理侧 | 明确后台支撑域边界，定义前台消费内容运营结果的展示规则。 |
| 系统支撑只覆盖权限模拟，未覆盖账户/消息/工单/任务/历史关注完整功能 | 部分覆盖 | P2 | product-agent | `src/app/perms/*`、`CurrentUserProvider.tsx`；未发现消息/工单/任务导航 | 归平台/后台能力；当前前台只保留权限与锁态口径。 |
| 科研机构、人才、产业服务链存在聚合实现，是否等价源文档细分能力待确认 | 待确认 | P1 | product-agent | `research-new/*`、`talent/*`、`service/*` 路由数少于源文档细分能力数 | 产品确认“聚合页覆盖”是否可接受，或需要补二级菜单/页面。 |

## 当前结论

`demo-ui-topic` 当前更像“科技专题服务系统前台专题分析工作台 + 部分门户展示”，而不是源文档描述的完整一体化系统。专题分析域覆盖较强；数据查询、信息发布、项目管理、内容运营、系统支撑存在不同程度缺口。

下一步不建议直接派 frontend-agent 修改。应先由 product-agent 确认：

1. 当前版本是否只做前台分析工作台。
2. 统一查询和信息发布是否纳入 P0 闭环。
3. 项目管理是否属于当前阶段。
4. 后台支撑域与前台消费边界。
5. 聚合页面是否能替代源文档细分能力。
