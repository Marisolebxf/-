# IA-SVCCHAIN-ECOSYSTEM｜服务链生态 信息架构

> **版本**：v1.0-r2（与 USM/Wireframe/UX-SPEC/TRACE 同步）
> **原始需求**：展示 Bid §1.1.1.2.4.2.7.4 / 7.5 / 7.8（6 个三级项）
> **实现仓**：demo-ui-topic `src/app/pages/service-center/`（与 R1 叶子同域目录，替换旧 `pages/service/ServiceChainAnalysis.tsx`）  
> **本轮决策（Q068 · P7）**：产业上下文 = 15 个产业集群。任务 `CHAIN-INDUSTRY-CLUSTER-SUPP-L01`。

## 1. 模块目标与边界

**做**：一个"服务链生态分析页"，三个分析页签（全链路短板 / 图谱分析 / 深圳现状）共享同一产业领域上下文，外加环节详情面板与机构画像抽屉（复用 R1 组件）。

**不做**：机构集合覆盖/趋势/评估（7.1-7.3，R1 叶子）；招引/培育名单（7.6/7.7，RECOMMEND 叶子）；链路知识库/城市基准数据的维护；NebulaGraph 直连（demo 阶段确定性数据，正式实现前端只调 Java REST）。

## 2. 对象与稳定身份

| 对象 | 稳定 ID | 说明 |
| --- | --- | --- |
| 产业领域 | `field_id`（`field-XXX`） | 与 R1 叶子共用字典真源（CT-SVC-ORG-02） |
| 链路环节 | `stage_id`（`stage-XXX`） | 专家知识库演示态 6 环节；环节详情、瓶颈判定、URL 共用 |
| 服务机构 | `org_id`（`svc-org-XXX`） | 与 R1 共用真源；图谱节点、环节机构列表、抽屉均用此 ID |
| 关联主体 | `ext_id`（`ent-/uni-/cap-XXX`） | 图谱关联节点（企业/高校/资本），仅摘要不做画像 |
| 关系边 | `rel`（类型枚举 + 端点） | investment / cooperation / competition / talent_flow |
| 对比城市 | `city_id` | 深圳/全国平均/北京/上海/广州（固定五列） |

## 3. IA 结构

```text
/service/chain-analysis（服务链生态分析，路由不变）
├─ 上下文区（产业领域 Select + 指标条）
├─ Tab: chain 全链路短板分析（默认）
│   ├─ 链路图（6 环节卡，问题环节高亮）
│   ├─ 瓶颈堵点识别面板（🧪 ❓Q-SVCCHAIN-03）
│   └─ Drawer: 环节详情（服务类型 + 环节内机构列表，可开画像/入对比篮）
├─ Tab: graph 服务链图谱分析
│   ├─ 过滤器（关系类型 / 节点类型 / 聚焦机构）
│   ├─ 关系网络图（EChart graph）
│   ├─ 统计面板（密度ⓘ / 中心性TOP5ⓘ / 影响力❓）
│   └─ 侧栏：关联主体摘要（非机构节点）
├─ Tab: shenzhen 深圳服务链现状
│   ├─ 统一评价框架说明卡（⚠️Q-SVCCHAIN-04）
│   ├─ 对比指标多选
│   ├─ 分组柱状图（五城市）+ 梯队仪表盘（🧪⚠️）
│   └─ 优势/短板/梯队结论（🧪）
└─ Drawer: 机构画像（复用 R1 OrgProfileDrawer，org 参数驱动）
```

## 4. URL 契约

| 参数 | 语义 | 示例 |
| --- | --- | --- |
| `tab` | 激活页签 `chain/graph/shenzhen` | `?tab=graph` |
| `field` | 产业领域 | `?field=field-bio` |
| `segment` | 打开环节详情的环节 | `?segment=stage-pilot` |
| `org` | 打开画像抽屉的机构 | `?org=svc-org-003` |

其余状态（图谱过滤、聚焦、对比指标选择）走 localStorage（`topic-svc-eco`，见 UX-SPEC §6）。参数非法时清除该参数并 Message 提示，不白屏。

## 5. Frame 职责

| Frame | 名称 | 职责 | 对应故事 |
| --- | --- | --- | --- |
| `F-SVC-ECO-01` | 页面外壳 | 上下文区、页签、指标条 | US-01 |
| `F-SVC-ECO-02` | 链路短板视图 | 链路图、瓶颈识别面板 | US-01、US-02 |
| `F-SVC-ECO-03` | 图谱视图 | 网络图、过滤器、统计面板、主体摘要 | US-03、US-04 |
| `F-SVC-ECO-04` | 深圳现状视图 | 框架卡、指标选择、对比图、结论 | US-05、US-06 |
| `F-SVC-ECO-05` | 环节详情面板 | 服务类型清单、环节内机构列表 | US-01 |
| `F-SVC-05` | 机构画像抽屉 | **复用 R1 组件**（CT-SVC-ORG-02） | US-04 |

## 6. 数据与服务边界

- Wave 0 全 Mock：链路知识库（6 环节 × 服务类型映射）、关系网络（确定性节点/边集）、城市基准（5 城市 × 指标）置 `serviceEcosystemData.ts`，禁止运行时随机数。
- 目标态：前端 → Java REST `/topic/v1/service-chain/ecosystem/**`；图谱数据由 Python 图算法层写 ADS，Java 只读（架构铁律 1/2/7）；前端不写 nGQL。
- 瓶颈判定、影响力评分、链完整度、梯队合成为演示口径或诚实缺失，正式算法待 Q-SVCCHAIN-03/04 定义卡。

## 7. 复用契约（对齐 REUSE-MATRIX-CHAIN 原则）

| 复用 | 来源 | 约束 |
| --- | --- | --- |
| EChart 容器 | `components/common/EChart.tsx` | 图表语义与 metric_id 由本叶子定义 |
| 机构画像抽屉 | R1 `service-center/OrgProfileDrawer.tsx` | 同域直接复用（CT-SVC-ORG-02，同一 org_id 语义） |
| 评审层 | R1 `ServiceReviewMount` + `serviceReviewData/serviceReadinessSeed` 扩展 | mount_id 用 `SVC-ECO-*`，业务模式 absent |
| 对比篮 | `components/common/CompareBasket.tsx`（`elementKey='service_org'`） | 见 CT-SVC-ORG-03（R2B）；环节详情/图谱节点入篮 |
| 图谱布局参照 | E2 产业链全景图谱（`REUSE-MATRIX-CHAIN.md` 审计原则） | 复用"图 + 过滤 + 统计"心智与 EChart graph 容器；不复制 CHAIN 字段/数据模型（CT-SVC-ECO-01） |
| 禁止 | import `pages/enterprise/*`、旧 `pages/service/ServiceChainAnalysis.tsx` 代码复制 | 旧页仅作删除审计 |

## 8. 指标登记（8 件套见 TRACE，就绪度四维见 readinessSeed）

| metric_id | 中文名 | D1 | 呈现 |
| --- | --- | --- | --- |
| `M_SVC_CHAIN_SEGMENT_ORG_COUNT` | 环节服务机构数 | aligned | ⓘ + 🧪 |
| `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` | 环节平均服务深度 | draft（Q-SVCCHAIN-02 沿用） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_CHAIN_BOTTLENECK` | 瓶颈堵点判定 | **missing**（Q-SVCCHAIN-03） | 红问号（只显治理引用）+ 🧪 |
| `M_SVC_GRAPH_DENSITY` | 服务网络密度 | aligned（标准公式） | ⓘ + 🧪 |
| `M_SVC_GRAPH_CENTRALITY` | 节点度中心性 | aligned（标准公式） | ⓘ + 🧪 |
| `M_SVC_GRAPH_INFLUENCE` | 生态影响力评分 | **missing**（Q-SVCCHAIN-03） | 红问号 + 🧪 |
| `M_SVC_SZ_COMPARE_METRIC` | 城市对比指标值 | draft（Q-SVCCHAIN-04） | ⓘ(橙点) + ⚠️ + 🧪 |
| `M_SVC_SZ_CHAIN_COMPLETENESS` | 服务链完整度 | **missing**（Q-SVCCHAIN-04） | 红问号；不参与图表渲染 |
| `M_SVC_SZ_TIER` | 深圳梯队位置 | draft（Q-SVCCHAIN-04） | ⓘ(橙点) + ⚠️ + 🧪 |

## 9. 跨模块契约

| 契约 | 方向 | 说明 |
| --- | --- | --- |
| CT-SVC-ORG-02 | R1 叶子 → 本叶子 | `org_id`/`field_id` 字典共用真源；画像抽屉组件直接复用，不另造 ID 体系 |
| CT-SVC-ECO-01 | E2 产业链全景 → 本叶子 | 复用"图谱 + 过滤 + 统计"交互心智与 EChart graph 容器；禁止复制 CHAIN 数据模型/字段/storage key（REUSE-MATRIX 原则 3/4） |
| CT-SVC-ECO-02 | 本叶子 → RECOMMEND 叶子 | 瓶颈/空白环节判定（stage_id + 问题类型）为招引方向的输入语义参照，不共享 storage key |
| CT-SVC-ORG-03 | 本叶子 → 系统对比篮 | 环节详情机构行、图谱机构节点提供"加入对比篮"（`elementKey='service_org'`，R2B 契约） |
