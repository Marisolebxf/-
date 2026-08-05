# 企业分析实现复用矩阵 — CHAIN

> **目标模块**：E2 / CHAIN 产业链分析重构  
> **用途**：判断企业分析已落实现中哪些能力可直接复用、哪些只能适配、哪些禁止进入新产业链实现。  
> **边界**：本文是实现复用审计，不是需求来源。产业链需求只来自 `agent-delivery/bid-reference/*.md` 与当前已确认人类决策。旧 `/industry/*`、`/industry-portal/*` 代码仅用于删除依赖审计，未参与本矩阵的产品语义生成。

## 1. 复用判断原则

1. 新代码必须位于独立产业链目录，不 import `pages/enterprise/*` 或旧 `pages/industry*`。
2. 允许直接复用已去业务化的共享组件和系统服务契约。
3. 带 `enterprise` 字段、路由、存储键、trace id、任务类型或文案的实现只能提炼后适配。
4. 复用企业分析的用户心智，不复制企业分析的字段、指标、模型、权限 persona 或页面 IA。
5. 旧产业链代码不得复制、拆改或作为新实现模板。

## 2. 可直接复用

| 现有能力 | 代码位置 | 新产业链用途 | 复用约束 |
| --- | --- | --- | --- |
| 上下文条 | `components/common/ContextBar.tsx` | 区域、产业领域、时间上下文 | `chain_id`、`node_id` 由新模块状态模型补充；不得把产业领域与产业链混为同一字段 |
| 检索骨架 | `components/search/SearchScaffold.tsx` | 产业链关键词/结构化检索、结果列表、分页、状态 | 使用全新 `chainCenterSearchConfig` 与全新数据适配器 |
| 轻量详情容器 | `components/search/ElementProfile.tsx` | 关联企业、技术、政策、科研机构、服务机构抽屉预览 | 只注入目标对象摘要和显式跨模块跳转，不复制企业画像 renderer |
| 图表容器 | `components/common/EChart.tsx` | 趋势、对比、分布、评分可视化 | 图表语义和 metric_id 全部由 CHAIN 定义 |
| 指标卡 | `components/common/MetricCard.tsx` | 总览、画像和结果指标 | 每个统计值必须绑定 `M_CHAIN_*` 或显式缺口 |
| 指标说明 | `components/common/MetricSpecCard.tsx` | 评审模式指标口径 | 读取 `cfg_metric-CHAIN-seed.yaml` 对应语义；不得使用旧页面硬编码说明 |
| 评审追溯 | `components/common/ReviewTrace.tsx`、`ReviewOnly.tsx` | requirement/metric/Mock/Pending 挂载 | mount_id 使用 `CHAIN-*`，业务模式必须 absent |
| Mock/Pending 标识 | `components/common/MockBadge.tsx`、`PendingBadge.tsx` | 显式暴露 V1 数据与口径缺口 | 不得用标识替代正常业务字段，也不得在业务模式泄露内部评审文案 |
| 权限容器 | `components/common/RoleLevelGate.tsx` | 继承全系统 L0～L3 分级并 fail closed | 产业链无专项权限例外；产品角色与实现权限 persona 分开，产业链特有字段密级与数据范围仍由规格定义 |
| 系统任务存储与浮层 | `system-tasks/systemTaskStore.ts`、`SystemTaskLayer.tsx` | 周期、评价、竞争力、深圳发展与报告任务 | 复用系统任务契约，使用 `CHAIN_*` task_type、独立快照和新路由；不得依赖企业任务模型 |
| 报告阅读器 | `components/report/SystemReportReader.tsx` | 产业链结果报告阅读 | 使用全新 CHAIN 报告文档、章节和指纹，不复用企业报告内容 |
| 对比篮基础设施 | `components/common/CompareBasket.tsx` | 后续多对象暂存候选 | V1 的多对象评价以任务配置快照为准；若接入必须使用独立 `elementKey=industry-chain` |

## 3. 适配后复用

| 现有结果 | 当前问题 | 适配目标 | V1 动作 |
| --- | --- | --- | --- |
| 企业“对象—配置—任务—结果—报告”旅程 | 旅程散落在多个企业页面与企业任务模型 | 抽象为 CHAIN 页面状态机与系统任务输入 | 在新目录重新实现，不 import 企业页面 |
| `pages/enterprise/analysisShared.tsx` | 目录、字段、搜索参数和对象摘要均为 enterprise | 新建 `industry-center/IndustryCenterShell.tsx` 与 `ChainObjectContext` | 只参考通用交互契约，不复制代码 |
| 当前 `PersonalAssetsPage.tsx` | 文案、存储键、分区和数据读取高度企业化 | 增加共享资产注册/投影机制，接入关注、收藏、最近分析和报告 | 不让 CHAIN 直接读企业 storage key；先以共享系统任务和 CHAIN 独立资产 store 接入 |
| 企业结果页报告按钮 | 绑定企业 task、fingerprint 和 report builder | 新建 CHAIN result snapshot、report fingerprint、report template | 报告只从结果页发起；同指纹任务复用 |
| 企业跨模块下钻 | 多数目标仍围绕企业详情 | 统一 `source_context`、`return_to` 与目标对象类型 | 抽屉预览后显式跳转，返回恢复 chain/node |
| 企业总览发现与分流 | 企业口径为区域/产业领域/产业链/链位环节两层筛选 | 新总览以产业领域导航、产业链检索、重点产业链、最近分析分流 | 复用信息节奏，不复制企业总览区块或字段 |

## 4. 禁止复用

| 禁止内容 | 原因 |
| --- | --- |
| `pages/enterprise/*` 页面组件的直接 import | 会把企业字段、路由、权限和状态耦合进新产业链模块 |
| 企业评估、引育、风险模型与权重 | 不属于产业链八项 Bid 能力，业务语义不等价 |
| 企业 `enterprise_code`、企业类型、资质、供应链风险字段 | 产业链主对象是 `chain_id`，节点对象是 `node_id` |
| 企业专属 localStorage key、task_type、trace id | 会造成资产串域、任务误恢复和审计错误 |
| 企业页面级 IA、Tab 和文案 | 用户确认复用的是心智闭环，不是页面结构 |
| 旧 `pages/industry/*`、`pages/industry-portal/*`、旧 service/mock/config | 用户明确要求完全重写；只能用于删除反向引用审计 |

## 5. 新实现目录边界

```text
src/app/pages/industry-center/
├─ components/        # CHAIN 域组件，不引用 enterprise 或旧 industry
├─ model/             # chain/domain/node、任务、结果、报告、资产契约
├─ data/              # 确定性 V1 Demo 数据与 adapter
├─ pages/             # /industry-center/* 页面
└─ index.ts
```

允许依赖方向：

```text
industry-center
  → components/common | components/search | components/report
  → system-tasks | system-surfaces | perms | lib
```

禁止依赖方向：

```text
industry-center
  ✕ pages/enterprise
  ✕ pages/industry
  ✕ pages/industry-portal
  ✕ services/industry
  ✕ mock/industry
```

## 5.1 维护管理壳层复用（2026-08-05 增补）

| 现有能力 | 代码 / 定义位置 | 新产业链用途 | 复用约束 |
| --- | --- | --- | --- |
| ENT-OPS 维护管理壳 | `ENT-OPS-维护管理` 五件套；Demo `EnterpriseMaintenancePage` 导航壳 | `/industry-center/maintenance` 15 项分组导航与门户工作流 | **只复用壳层与样式**；字段、内容类型、埋点前缀、对象键改为产业域；禁止 import `pages/enterprise/*` 业务页 |
| E7 政策维护复用先例 | `E7-政策分析` 维护管理章节 | 同构决策参考 | 不复制政策字段 |

产品定义权威：`E2-产业链分析/CHAIN-OPS-维护管理/`。

## 6. 复用结论

- **可直接复用的主要价值**：统一上下文、检索、指标/追溯、系统任务、报告阅读与 Arco 交互基础；维护管理 **ENT-OPS 导航壳与工作流形态**。
- **必须重新实现的主要价值**：产业链对象模型、四工作区、页面状态机、任务快照、结果文档、公开/登录边界与所有业务数据；维护管理的产业字段与三类门户内容类型。
- **不进入新实现的内容**：企业专属逻辑和全部旧产业链业务代码；企业维护字段硬套。
