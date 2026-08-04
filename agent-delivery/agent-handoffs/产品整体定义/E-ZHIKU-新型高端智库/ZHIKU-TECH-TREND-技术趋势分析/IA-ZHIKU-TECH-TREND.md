# IA-ZHIKU-TECH-TREND｜技术趋势分析 · 信息架构

> **版本**：v1.0-rework-r4（与 USM/Wireframe/UX-SPEC/TRACE 同步）
> **真源**：拆解表 §2.3（序号 29-45）；USM-ZHIKU-TECH-TREND.md

## 1. 模块目标与边界

- **目标**：从"主题归纳（聚类）→ 关系挖掘（共性网络）→ 四维研判（热点/关联/合作/趋势）→ 信号处置（预警/订阅/检测）"承载技术趋势监测全链路。
- **包含**：序号 29-45 全部 17 项。
- **不包含**：体系结构管理（ZHIKU-TECH-SYSTEM）、报告本体（ZHIKU-WRITING）、真实聚类/语义/预测算法（🧪 演示 + D1 缺失红问号）。

## 2. 对象与稳定标识

| 对象 | 标识 | 生命周期 | 持久化 |
| --- | --- | --- | --- |
| 聚类任务 ClusterTask | `clu-*` | 种子 + 新建/删除/重跑 | `zhiku-tt-cluster-tasks` |
| 筛选权重 FilterWeight | primary/secondary/final | 可调可重算 | `zhiku-tt-weights` |
| 主题清单 customList | index | 可编辑/恢复 | `zhiku-tt-custom-list` |
| 共性网络任务 CommonNetworkTask | `cn-*` | 种子 + 新建 | `zhiku-tt-cn-tasks` |
| 聚类规则 ClusterRule | `rule-*` | 种子 + 新建/启停 | `zhiku-tt-rules` |
| 预警 AlertItem | `al-*` | 种子；处理态演进 | `zhiku-tt-alerts` |
| 订阅规则 SubscriptionRule | `sub-*` | CRUD + 启停 | `zhiku-tt-subscriptions` |
| 检测任务 DetectionTask | `det-*` | 运行累积 | `zhiku-tt-detections` |
| UI 态（搜索/勾选/跟踪对象） | — | 会话间保留 | `zhiku-tt-ui` |

## 3. IA 结构（路由与 Frame）

```
/strategy/tech-trend（技术趋势分析 · 单路由多标签，?tab= 同步）
├─ tab=cluster  F-TT-01 聚类分析（任务/结果/三级筛选/清单定制）
├─ tab=network  F-TT-02 共性网络（任务/矩阵/规则/语义/作者）
├─ tab=hotspot  F-TT-03 热点与关联（热点/交叉/合作/趋势）
└─ tab=alert    F-TT-04 动态预警（预警/跟踪/订阅/检测）
```

| Frame | 职责 | 指标 |
| --- | --- | --- |
| F-TT-01 | 聚类任务与主题定制 | `ZHIKU-TT-CLUSTER-TOTAL` |
| F-TT-02 | 共性网络五视图 | — |
| F-TT-03 | 热点/关联/合作/趋势 | `ZHIKU-TT-HOTSPOT-TOTAL`、`ZHIKU-TT-TREND-FORECAST`（D1 missing） |
| F-TT-04 | 预警/跟踪/订阅/检测 | `ZHIKU-TT-ALERT-PENDING` |

## 4. 数据与服务边界

- 数据来自 `src/mock/clusterAnalysis.ts`、`commonNetwork.ts`、`techHotspot.ts`、`techAlert.ts` 领域 store（reducer 化 + localStorage `zhiku-tt-` 前缀）。
- 目标态：聚类/语义/预测算法全部走 Python `/internal/*`（架构铁律 1/2），Java 只聚合 ADS；前端只读消费。
- `ZHIKU-TT-TREND-FORECAST` 保持 D1 缺失红问号（GAP-ZHIKU-TT-TREND-FORECAST-非算法产出），上线前需算法定义卡或撤下预测区间。

## 5. 跨模块契约

| 契约 | 方向 | 说明 |
| --- | --- | --- |
| CT-TT-01 | TT → TALENT-POOL | 高产作者卡"学术档案"跳 `/talent/profile?talent=<按姓名匹配>`；未收录 Message 提示 |
| CT-TT-02 | TT → WRITING | 预警详情"生成预警研判报告"：`createTask` 预填（预警级别/影响评估），跳 `/writing/create?step=outline&task=` |
| CT-TT-03 | TT ← RN | RN 趋势卡"去技术趋势分析深挖"落点 `?tab=hotspot`（CT-RN-02 对偶） |
