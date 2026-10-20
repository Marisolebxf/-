# IA-SVCCHAIN-ORG-ANALYSIS｜服务机构分析 信息架构

> **版本**：v1.0-r1-pilot（与 USM/Wireframe/UX-SPEC/TRACE 同步）
> **原始需求**：展示 Bid §1.1.1.2.4.2.7.1-7.3（6 个三级项）
> **实现仓**：demo-ui-topic `src/app/pages/service-center/`（新建隔离目录，复用契约见 §7）  
> **本轮决策（Q068 · P7）**：产业上下文 = 15 个产业集群。任务 `CHAIN-INDUSTRY-CLUSTER-SUPP-L01`。

## 1. 模块目标与边界

**做**：一个"服务机构分析工作台"，三个分析页签（领域覆盖 / 新增趋势 / 技术力评估）共享同一对象上下文（产业领域 + 机构集合），外加统一的机构画像抽屉。

**不做**：服务链路图与短板（7.4/7.5）、招引/培育名单（7.6/7.7）、深圳横向对比（7.8）——均属 R2 叶子；机构主数据维护；与企业库的实体互认跳转（无稳定映射，禁止伪跳转）。

## 2. 对象与稳定身份

| 对象 | 稳定 ID | 说明 |
| --- | --- | --- |
| 服务机构 | `org_id`（`svc-org-XXX`） | 全模块唯一；抽屉、URL、集合、评估均用此 ID |
| 产业领域 | `field_id`（`field-XXX`） | 字典对象；覆盖列、趋势曲线、筛选共用 |
| 服务链环节 | `segment`（上游/中游/下游细分枚举） | 机构属性 + 筛选维度 |
| 评估配置 | `eval_config`（本地对象） | 维度启停/权重/对比机构/图型；localStorage 持久化 |

## 3. IA 结构

```text
/service/institution-judgment（服务机构分析工作台，路由不变）
├─ 上下文区（产业领域 Select + 已选机构 Tag 集 + 选择机构入口 + 关键指标条）
├─ Tab: coverage 领域覆盖（默认）
│   ├─ 图型切换（热力图 | 矩阵图）
│   ├─ 覆盖可视化主区
│   └─ 核心结论区（🧪）
├─ Tab: trend 新增趋势
│   ├─ 领域对比选择（主领域 + ≤2 对比）+ 时间窗
│   ├─ 趋势折线主区
│   ├─ 市场热度研判面板（🧪 + ⚠️ Q-SVCCHAIN-02）
│   └─ 年度明细表（可下钻）
├─ Tab: capability 技术力评估
│   ├─ 模型配置区（维度启停/权重/自定义/归一）
│   ├─ 对比机构选择（2~5 家，来自已选集合）
│   ├─ 结果区（排名列表 | 雷达图）
│   └─ 结论区（🧪）
├─ Drawer: 机构画像（org 参数驱动，跨页签共用）
└─ 系统对比篮 picker（service_org Tab；篮内"新增"→在库机构搜索框）
```

## 4. URL 契约

| 参数 | 语义 | 示例 |
| --- | --- | --- |
| `tab` | 激活页签 `coverage/trend/capability` | `?tab=trend` |
| `field` | 主产业领域 | `?field=field-bio` |
| `org` | 打开画像抽屉的机构 | `?org=svc-org-003` |

URL 参数为分享/恢复契约；其余状态（机构集合、模型配置、图型、时间窗）走 localStorage（`topic-svc-*` 前缀，见 UX-SPEC §6）。参数非法时清除该参数并 Message 提示，不白屏。

## 5. Frame 职责

| Frame | 名称 | 职责 | 对应故事 |
| --- | --- | --- | --- |
| `F-SVC-01` | 工作台外壳 | 上下文区、页签、指标条、选择器 Modal、空态引导 | US-01 |
| `F-SVC-02` | 领域覆盖视图 | 热力/矩阵、图例、核心结论 | US-02 |
| `F-SVC-03` | 新增趋势视图 | 曲线、时间窗、热度研判、明细表 | US-04、US-05 |
| `F-SVC-04` | 技术力评估视图 | 模型配置、对比选择、排名/雷达、结论 | US-06 |
| `F-SVC-05` | 机构画像抽屉 | 基本信息、覆盖细分、技术力五维、新增记录 | US-03 |

## 6. 数据与服务边界

- Wave 0 全 Mock：确定性数据集（24 家机构 × 8 产业领域 × 8 年新增序列 × 技术力五维），置 `serviceCenterData.ts`，禁止运行时随机数（保证 AC 可复现）。
- 目标态：前端 → Java REST `/topic/v1/service-chain/orgs/**`；本模块不直连 Python、不写 nGQL（架构铁律 2/7）。
- 深度得分、热度评级、综合得分三类派生值为演示口径，正式算法待 Q-SVCCHAIN-01/02 定义卡；前端只消费不推断。

## 7. 复用契约（对齐 REUSE-MATRIX-CHAIN 原则）

| 复用 | 来源 | 约束 |
| --- | --- | --- |
| EChart 容器 | `components/common/EChart.tsx` | 图表语义与 metric_id 由本模块定义 |
| 评审层模式 | 参照 `industry-center` 的 ReviewMount 模式自建 `ServiceReviewMount` | mount_id 用 `SVC-ORG-*`，业务模式 absent |
| 就绪度镜像 | 自建 `serviceReadinessSeed.ts` | 真源 = TRACE 指标登记；禁止页面改写状态 |
| Arco 交互基础 | Tabs/Select/Drawer/Modal/Table/Message | 遵循 UX-UE 通用交互组件规范 |
| 禁止 | import `pages/enterprise/*`、旧 `pages/service/ServiceInstitutionJudgment.tsx` 的代码复制 | 旧页仅作删除审计 |

## 8. 指标登记（8 件套见 TRACE，就绪度四维见 readinessSeed）

| metric_id | 中文名 | D1 | 呈现 |
| --- | --- | --- | --- |
| `M_SVC_ORG_TOTAL` | 入库服务机构总数 | aligned | ⓘ + 🧪 |
| `M_SVC_ORG_SELECTED_COUNT` | 当前分析机构数 | aligned | ⓘ + 🧪 |
| `M_SVC_ORG_COVERAGE_BREADTH` | 服务广度（覆盖领域数） | aligned | ⓘ + 🧪 |
| `M_SVC_ORG_COVERAGE_DEPTH` | 服务深度得分 | draft（Q-SVCCHAIN-02） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_ORG_NEW_COUNT` | 年度新增服务机构数 | aligned | ⓘ + 🧪 |
| `M_SVC_ORG_MARKET_HEAT` | 市场热度评级 | **missing**（Q-SVCCHAIN-02） | 红问号（只显治理引用）+ 🧪 |
| `M_SVC_ORG_TECH_SCORE` | 技术力综合得分 | draft（Q-SVCCHAIN-01） | ⓘ(橙点) + ⚠️ + 🧪 |

## 9. 跨模块契约

| 契约 | 方向 | 说明 |
| --- | --- | --- |
| CT-SVC-ORG-01 | 本叶子 → R2 招引培育域 | 技术力评估结果（eval_config + 得分快照）为招引/培育模型的输入语义参照，不共享 storage key |
| CT-SVC-ORG-02 | 本叶子 → R2 链路生态域 | `org_id`/`field_id` 字典为两叶子共用真源，R2 不得另造机构 ID 体系 |
