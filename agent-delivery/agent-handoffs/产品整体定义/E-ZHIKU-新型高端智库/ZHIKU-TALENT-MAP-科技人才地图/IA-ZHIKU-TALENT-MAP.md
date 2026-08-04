# IA-ZHIKU-TALENT-MAP｜科技人才地图 信息架构

> **版本**：v1.0-rework-r3（与 USM/Wireframe/UX-SPEC/TRACE 同步）
> **真源**：需求拆解 §三 3.3 序号 75-79；USM-ZHIKU-TALENT-MAP.md

## 1. 模块目标与边界

- **目标**：分布研判 → 指数对比 → 精准检索 → 驾驶舱全景 → 资源订阅的空间人才研判闭环。
- **包含**：人才分布与动态趋势（75）、人才指数（76）、人才检索（77）、人才驾驶舱（78）、人才库订阅（79）。
- **不包含**：画像本体与库管理（59-74，归 POOL）；推送流本体（81，归 POOL，仅经契约追加条目）；报告写作本体（归 WRITING）。

## 2. 对象与稳定标识

| 对象 | 标识 | 生命周期 | 说明 |
| --- | --- | --- | --- |
| 分布点位 MapPoint | `pt-*` | 静态种子 | 类别/坐标/热度值 |
| 机构排名 InstitutionRank | rank 序 | 静态种子 | 与点位按名称对齐联动 |
| 流向线 FlowLine | from-to 组合 | 静态种子 | 人才流动趋势 |
| 指数维度 IndexDim | 维度名 | 静态种子 + 权重用户态 | 权重持久化 |
| 检索结果 SearchTalent | `sr-*` | 静态种子 | 映射 scholar 下钻 |
| 检索历史 | 关键词字符串 | 用户态持久化 | 最近 5 条 |
| 驾驶舱配置 | 卡片 key 集合 | 用户态持久化 | 显隐定制 |
| 订阅规则 SubscriptionRule | `rule-*` | 用户 CRUD 持久化 | 关键词+类别 |
| 订阅资源 SubscriptionResource | `sub-r-*` | 静态种子 | 四类资源样例 |

## 3. IA 结构

```
人才服务（左侧手风琴一级：talent）
└── 人才地图 /talent/map（URL: ?tab=map|index|search|cockpit|subscription）
    ├── 人才地图 Tab       F-TM-01（含"生成人才地图分析报告"出口 US-06）
    ├── 人才指数 Tab       F-TM-02
    ├── 人才检索 Tab       F-TM-03
    ├── 人才驾驶舱 Tab     F-TM-04
    └── 人才库订阅 Tab     F-TM-05
```

## 4. Frame 职责

| Frame | 区域 | 职责 | 序号 |
| --- | --- | --- | --- |
| F-TM-01 | 人才地图 | 点位地图 + 类别/热力筛选 + 机构排名/点位列表双向联动 + 流动趋势 + 报告出口 | 75 |
| F-TM-02 | 人才指数 | 五维权重滑杆 + 区域切换 + 柱状/雷达对比（D1 missing 诚实态） | 76 |
| F-TM-03 | 人才检索 | 语义🧪/关键词双模式 + 推荐专家 + 历史复搜 + 画像下钻（→POOL） | 77 |
| F-TM-04 | 人才驾驶舱 | 统计卡定制显隐 + 产业联动 + 趋势预测（演示态） | 78 |
| F-TM-05 | 人才库订阅 | 资源目录 + 规则 CRUD + 命中预览 + 推送联动（→POOL 推送流） | 79 |

## 5. 数据与服务边界

- 全部数据来自 `src/mock/talentMap.ts` 领域 store（Pinia），静态种子 + 用户态持久化（localStorage `zhiku-tm-` 前缀）。
- 目标态映射：前端 → Java REST → ADS 人才空间分布主题表；指数/语义检索/预测算法归 Python `/internal/*`（正式版，且指数需算法定义卡先行）。demo 不连任何后端。
- 跨叶子消费：`useWritingTaskStore.createTask`（US-06 报告出口）；`useTalentNewsStore.appendGeneratedPush`（US-05 订阅联动）；画像下钻路由 `/talent/profile?scholar=`（US-03）。

## 6. 指标登记

| metric_id | 挂载点 | 就绪度要点 |
| --- | --- | --- |
| `ZHIKU-TM-DIST-TOTAL` | F-TM-01 分布总数卡 | D1 draft / D4 mock |
| `ZHIKU-TM-INDEX-SCORE` | F-TM-02 综合得分卡 | **D1 missing 红问号**（算法定义卡未落地，GAP-ZHIKU-TM-INDEX，Q-ZHIKU-04） |
| `ZHIKU-TM-COCKPIT-ALERT` | F-TM-04 统计卡组 | **D1 missing 红问号**（预测非算法产出，GAP-ZHIKU-TM-COCKPIT） |
| `ZHIKU-TM-SUBSCRIPTION-TOTAL` | F-TM-05 订阅总数卡 | D1 draft / D4 mock（修复 S4 未登记错挂） |

## 7. 跨模块契约

| 契约 | 方向 | 载体 |
| --- | --- | --- |
| 人才地图分析报告 | TM → WRITING | `createTask({outline 预填分布统计})` + `/writing/create?step=outline&task=` |
| 订阅更新推送 | TM → POOL | `useTalentNewsStore.appendGeneratedPush(rule)` |
| 画像下钻 | TM → POOL | `/talent/profile?scholar=<id>` |
