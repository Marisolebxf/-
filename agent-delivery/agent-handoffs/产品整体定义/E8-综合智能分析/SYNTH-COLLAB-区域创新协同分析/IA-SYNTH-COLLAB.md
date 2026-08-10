# IA-SYNTH-COLLAB｜区域创新协同分析 · 信息架构

> **版本**：v1.0-pack1 · 2026-08-10  
> **叶子**：`SYNTH-COLLAB`（E8 · 综合智能分析 / 区域创新协同分析）  
> **registry**：`SYNTH-MOD-COLLAB-PACK-L01`  
> **同步**：USM / TRACE / UX-SPEC / Wireframe  
> **历史参照（非权威）**：`../SYNTH-REGION-区域创新分析/`

## 1. 导航落位与边界

```text
专题服务系统
└── 综合智能分析
    ├── 区域创新活力分析   /intelligence/vitality
    ├── 区域创新要素分析   /intelligence/elements
    └── 区域创新协同分析   /intelligence/collaboration   ← 本叶
```

本叶只闭合系统方案 §8.3.1–8.3.3 与算法库 §10.10。区域、对比范围、时间窗复用三叶共享 `CT-SYN-CTX`；后台长耗时分析复用 `SYS-ANALYSIS-JOBS`，不自建第二套任务状态。

## 2. Frame 清单

| Frame | 名称 | 路由 / 载体 | 主要区块 | 对应故事 |
| --- | --- | --- | --- | --- |
| `F-COLLAB-01` | 协同分析工作台 | `/intelligence/collaboration` | 上下文条 · 默认秒开 / 改条件待分析 · 指标结果总览 · 主体关系图谱 · 集群/孤立诊断 · 趋势/横向对比 · 效果评估 · 「开始分析」 | US-COLLAB-01～06 |
| `F-COLLAB-02` | 可视化分析过程 | `/intelligence/collaboration/tasks/:taskId` | 任务摘要 · 协同场景五阶段 · 当前阶段说明 · 右下操作 | US-COLLAB-05 |
| `F-COLLAB-03` | 指标与计算方法抽屉 | F-COLLAB-01 内 Drawer（`panel=method`） | 完整度/中心度/密度定义 · 输入关系 · 计算流程 · 临时演示公式 · 正式待定项 | US-COLLAB-02 |
| `F-COLLAB-04` | 主体详情抽屉 | F-COLLAB-01 内 Drawer（`node=`） | 人才/科研机构基础信息 · 合作关系摘要 · 边界说明 | US-COLLAB-03 |

## 3. 产品角色（可回指源章节）

| 角色 ID | 产品角色 | 源文件 · 章节 · 原文依据 | 数据边界 |
| --- | --- | --- | --- |
| `ROLE-SYN-GOV` | 政府科技战略决策用户 | 系统方案 §1.1.1.2.4.2.8：「科技政策顶层设计、资源统筹配置与生态优化」；算法库 §10.10：「为区域创新政策制定、资源配置及战略布局提供科学依据」 | 授权范围内区域指标、图谱与对比结果 |
| `ROLE-SYN-PARK` | 产业园区创新生态用户 | 系统方案 §1.1.1.2.4.2 科技专题战略分析上级服务对象：「政府科技主管部门、产业园区、科研机构及重点企业」；「全面赋能政府科技主管部门、产业园区、投资机构与研究团队……生态化协同」 | 园区授权范围内主体关系与区域对比 |
| `ROLE-SYN-RESEARCH` | 科研机构 / 研究分析用户 | 算法库 §1.1.1.1.1.1.1.10：「支持政府、科研机构及企业在战略规划、政策制定、资源配置等场景中的科学决策」 | 公开口径指标、脱敏主体关系 |
| `ROLE-SYN-ENTERPRISE` | 企业创新规划用户 | 同上原文中的「企业」 | 本企业及公开合作网络；敏感关系按授权脱敏 |

> 以上均采用源需求服务对象，不从页面操作推导「园区运营专员」等岗位 persona。

## 4. 数据对象

| 对象 | 关键字段 | 说明 |
| --- | --- | --- |
| `RegionContext` | `region` / `compareScope` / `window` | 三叶共享 `CT-SYN-CTX` |
| `CollabDefaults` | region=`深圳` / compare=`全国重点城市` / window=`最近3年` | 系统默认；与跑批键一致时秒开 |
| `CollabBatchSnapshot` | `batchKey` / `computedAt` / `methodVersion` / `resultRef` | 默认三元组预计算结果 |
| `CollabTask` | `taskId` / `frozenContext` / `status` / `nodes[]` / `resultSnapshotId` | 非默认条件后台任务；服务端为状态真源 |
| `CollabNode` | `id` / `name` / `kind` / `industry` / `region` / `crossRef` | 企业、科研机构、人才等创新主体 |
| `CollabEdge` | `source` / `target` / `relationType` / `eventCount` / `weight` / `time` | 联合专利、合作项目、人才流动等合作关系 |
| `NetworkMetricResult` | `completeness` / `centralitySummary` / `density` / `methodVersion` | 算法库 §10.10 三指标结果 |
| `CollabResult` | `index` / `networkMetrics` / `compare` / `trend` / `clusters` / `isolatedNodes` / `strengths` / `weaknesses` / `strategySuggestions` / `outputRelation` | 不可变结果快照 |

## 5. 指标、方法与结果信息架构

### 5.1 用户必须看见的指标

| metric_id | 中文名 | 算法语义 | D1 | 结果挂载点 |
| --- | --- | --- | --- | --- |
| `M_SYNTH_COLLAB_COMPLETENESS` | 协同网络完整度 | 网络连接全面性 / 覆盖水平 | draft（`Q-SYNTH-C-01`） | 指标总览、对比、趋势 |
| `M_SYNTH_COLLAB_CENTRALITY` | 协同网络中心度 | 关键节点辐射影响力 | draft（`Q-SYNTH-C-01`） | 指标总览、中心主体、图谱 |
| `M_SYNTH_COLLAB_DENSITY` | 协同网络密度 | 整体合作紧密度 | draft（`Q-SYNTH-C-01`） | 指标总览、对比、趋势 |
| `M_SYNTH_COLLAB_INDEX` | 区域创新协同指数 | 三指标综合加权并经历史数据校准 | missing（`Q-SYNTH-C-02`） | 指数卡、排名、趋势、集群 |
| `M_SYNTH_COLLAB_RELATION_INPUT` | 协同关系输入统计 | 联合专利 / 合作项目 / 人才流动等关系量 | draft（`Q-SYNTH-C-01`） | 输入构成、图谱边统计 |
| `M_SYNTH_COLLAB_OUTPUT_CORR` | 协同—创新产出关联结果 | 协同网络与联合发明专利等产出的关联性 | missing（`Q-SYNTH-C-03`） | 效果评估 |

### 5.2 计算方法呈现

F-COLLAB-03 固定展示：

1. 输入：创新主体基础数据、合作关系数据；关系候选包括联合专利、合作项目、人才流动。
2. 处理：数据真实性/一致性校验 → 构建区域协同网络。
3. 三指标：完整度（全面性）、中心度（辐射影响力）、密度（合作紧密度）。
4. 合成：三指标综合加权 + 历史数据校准 → 区域创新协同指数。
5. 输出：指数、三指标、横向对比、纵向趋势、优势不足、优化合作路径策略建议与结构化报告。

正式分母、聚合方式、权重与校准窗口未由源需求给定，必须以 D1 missing/draft + Q 展示。若 V1 使用可复现演示公式，须明确标「团队临时默认 / 🧪」，不得写成正式算法。

## 6. 默认秒开与后台任务

```text
进入 F-COLLAB-01
  ├─ context == 深圳 × 全国重点城市 × 最近3年 且默认跑批快照存在
  │    → 秒开结果；不创建任务，不进过程页
  └─ 任一条件变化或默认快照缺失
       → 待分析态 + 当前条件差异 + 「开始分析」
          → 创建/恢复 task_type=region_innovation_collaboration
             → F-COLLAB-02 协同五阶段
                → 成功后「查看分析结果」绑定任务快照
```

## 7. 状态与 URL

| 状态 | 持久化 | URL | 说明 |
| --- | --- | --- | --- |
| 目标区域 | ✅ `topic-synth-workbench` | `region` | 默认深圳 |
| 对比范围 | ✅ | `compare` | 默认全国重点城市 |
| 时间窗 | ✅ | `window` | 默认最近 3 年（`3y`） |
| 结果模式 | — | `mode=result\|config` | 默认快照存在时 `result` |
| 分析任务 | 服务端 | `/tasks/:taskId` | 跨页/刷新/登录恢复 |
| 方法抽屉 | — | `panel=method` | 指标与计算方法 |
| 图谱筛选 | ✅ | `industry` / `kinds` | 不改变已冻结任务结果；仅过滤展示 |
| 主体抽屉 | — | `node` | 企业/服务机构优先跨模块下钻 |

优先级：URL > localStorage > 系统默认。任务事实只读服务端，不以 localStorage 伪造。

## 8. 跨叶 / 跨模块契约

| ID | 方向 | 契约 |
| --- | --- | --- |
| `CT-SYN-CTX` | 三叶共享 | 深圳 / 全国重点城市 / 最近 3 年默认值及 URL/store 约定 |
| `CT-SYN-JOBS` | 出 → SYS-ANALYSIS-JOBS | `task_type=region_innovation_collaboration`；协同五阶段登记与恢复 |
| `CT-SYN-01` | 出 → 企业画像 | 企业节点携带真实企业编码 |
| `CT-SYN-02` | 出 → 机构画像 | 服务机构节点携带稳定机构 ID |
| `CT-SYN-03` | 出 → 报告面 | 报告绑定跑批或任务的不可变结果快照 |

## 9. 本轮决策摘要

| 项 | 源需求 | 本轮处理 | 状态 |
| --- | --- | --- | --- |
| 指标 | §10.10 明确完整度/中心度/密度/协同指数 | 全部进入结果与方法区 | 必达 |
| 公式 | 仅给出语义、综合加权、历史校准 | 正式参数保持缺口；演示公式单独标识 | `Q-SYNTH-C-01/02` |
| 策略建议 | §8.3.3 要求提出优化合作路径建议，未规定生成方式 | 结果中显性展示；生成规则保持开放 | `Q-SYNTH-C-04` |
| 默认条件 | 源需求支持按区域/时间查询，未给默认值 | 深圳 / 全国重点城市 / 最近 3 年 | 团队临时默认，复用 `Q-SYNTH-V-02` |
| 计算体验 | 源需求写实时分析 | 默认跑批秒开；改条件后台任务 | 本轮产品解释，接 `CT-SYN-JOBS` |
