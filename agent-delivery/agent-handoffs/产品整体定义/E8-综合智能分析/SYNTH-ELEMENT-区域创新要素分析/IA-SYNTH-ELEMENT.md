# IA-SYNTH-ELEMENT｜区域创新要素分析 · 信息架构

> **版本**：v1.0-pack1 · 2026-08-10  
> **叶子**：`SYNTH-ELEMENT`（E8 · 综合智能分析 / 区域创新要素分析）  
> **registry**：`SYNTH-MOD-ELEMENT-PACK-L01`  
> **同步**：USM / TRACE / UX-SPEC / Wireframe  
> **历史参照（非权威）**：`../SYNTH-REGION-区域创新分析/` — 禁止用旧「四类要素」覆盖算法库七要素

## 1. 导航落位

```
专题服务系统
└── 综合智能分析
    ├── 区域创新活力分析   /intelligence/vitality          （兄弟叶 · CT-SYN-CTX）
    ├── 区域创新要素分析   /intelligence/elements          ← 本叶
    └── 区域创新协同分析   /intelligence/collaboration     （兄弟叶 · CT-SYN-CTX）
```

本叶只闭合系统方案 §8.2.1–8.2.3 与算法库 §10.6–10.9；不把 §8.1 活力总榜或 §8.3 协同图谱主验收写入本叶。顺链入口/出口仅作上下文契约。

## 2. Frame 清单

| Frame | 名称 | 路由 / 载体 | 主要区块 | 对应故事 |
| --- | --- | --- | --- | --- |
| `F-ELEM-01` | 要素分析工作台 | `/intelligence/elements` | 上下文条 · 默认秒开结果面 / 改条件配置面 · 综合指数 · 类型/层次/领域三棱镜 · 七要素得分 · 指标方法说明 · 指标明细 · 贡献路径 · 排名/趋势/优劣 · 「开始分析」 | US-ELEM-01～05 |
| `F-ELEM-02` | 可视化分析过程 | `/intelligence/elements/tasks/:taskId` | 任务摘要卡 · 「可视化分析过程」五阶段 · 阶段 Alert · 右下操作 | US-ELEM-04 |
| `F-ELEM-03` | 指标与方法说明抽屉 | F-ELEM-01 内 Drawer（`panel=method`） | 七要素×类型/层次/领域指标体系 · 阈值/权重说明 · 综合合成公式占位（诚实态） · §10.6–10.9 映射 | US-ELEM-02 |

## 3. 产品角色（可回指源章节）

| 角色 ID | 产品角色 | 源文件 · 章节 · 原文依据 | 数据边界 |
| --- | --- | --- | --- |
| `ROLE-SYN-GOV` | 政府科技战略决策用户 | `科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.8：「科技政策顶层设计、资源统筹配置与生态优化」；§8.2「识别关键驱动要素与配置瓶颈，精准优化要素供给与布局策略」；算法库 §1.1.1.1.1.1.1.10「为政府部门制定产业政策…」 | 授权范围内区域要素指标与对比结果 |
| `ROLE-SYN-RESEARCH` | 科研机构 / 研究分析用户 | 算法库 §1.1.1.1.1.1.1.10：「支持政府、**科研机构**及企业在战略规划、政策制定、资源配置等场景中的科学决策」；§10.7「为政府、科研机构及企业制定发展战略…」 | 公开口径指标；脱敏对比 |

> 不另造「业务分析师 / 园区专员」等岗位 persona。园区运营若需独立角色 → 待业务确认（开放项 `Q-SYNTH-E-ROLE`）。

## 4. 数据对象

| 对象 | 关键字段 | 说明 |
| --- | --- | --- |
| `RegionContext` | `region` / `compareScope` / `window` | 三叶共享；契约 `CT-SYN-CTX`（默认权威见 VITALITY 草案） |
| `ElementDefaults` | region=`深圳` · compare=`全国重点城市` · window=`最近3年` | **系统默认**；与跑批键一致则秒开 |
| `BatchSnapshot` | `batchKey` / `computedAt` / `resultRef` | 默认三元组对应的后台跑批结果；存在则秒开 |
| `ElementTask` | `taskId` / `frozenContext` / `status` / `nodes[]` | 改条件后「开始分析」创建的不可变任务 |
| `ElementType` | type∈{talent,enterprise,policy,service_org,research_org,capital,space} | 算法库七要素（权威） |
| `TypeScore` | type / score / weight / inputsRef | §10.6 类型维得分 |
| `LevelScore` | structure∈七大结构 / maturity / balance / thresholdHit | §10.7 层次结构评价 |
| `DomainScore` | industryDomain / techDomain / coverage / score | §10.8 领域覆盖与得分 |
| `IndicatorRow` | id / name / caliber / weight / rawValue / score / lens / type | 指标叶子；挂类型/层次/领域透镜 |
| `ContributionPath` | elementType / targetIndustryOrOutcome / contribution / pathDigest | §8.2.3 影响关联；算法未定诚实态 |
| `ElementResult` | compositeIndex / typeIndex / levelIndex / domainIndex / typeScores[] / levelScores[] / domainScores[] / weights[] / rankList[] / trend[] / strengths[] / weaknesses[] / contributions[] / methodDigest | §10.6–10.9 输出映射 |

## 5. 指标体系与算法语义（对齐算法库 §10.6–10.9）

| 模型（算法库） | 产品透镜 | 核心对象 | 产品展示要点 |
| --- | --- | --- | --- |
| §10.6 类型综合评价 | 类型 | 七要素配置与发展水平 | **人才 / 企业 / 政策 / 服务机构 / 科研机构 / 资金 / 空间** 得分 + **类型指数** |
| §10.7 层次综合评价 | 层次 | 七大结构成熟度 / 均衡度 / 达标 | 结构雷达或条形 + **层次指数** + 达标标记 |
| §10.8 领域综合评价 | 领域 | 产业领域 × 技术领域覆盖 | 覆盖矩阵 / 分维得分 + **领域指数** |
| §10.9 综合分析 | 综合 | 类型 + 层次 + 领域合成 | **区域创新要素指数** + 分项排序 + 优劣 + 趋势建议入口 |

系统方案映射（禁止伪闭合）：

| 系统方案 | 映射到本叶 |
| --- | --- |
| §8.2.1 创新要素数据汇聚 | 七要素全景汇聚区 + 过程阶段 `aggregate` |
| §8.2.2 要素评价模型构建 | 类型 / 层次 / 领域评价 + 方法说明（规模/质量/结构/活跃度挂入对应透镜） |
| §8.2.3 要素影响关联分析 | 贡献路径区；算法细则未定 → D1 missing + `Q-SYNTH-E-02` |

**要素对象清单权威 = 算法库七要素。** 旧 SYNTH-REGION「人才 / 资本 / 平台 / 项目」四类仅历史参照；系统方案举例「企业、科研机构、人才、资金」视为七要素的子集举例，不另起正式四类口径。

合成：类型指数 + 层次指数 + 领域指数 → **区域创新要素指数**（§10.9）。阈值 / 权重 / 综合合成公式未定 → D1 missing + `Q-SYNTH-02` / `Q-SYNTH-E-*`，禁止伪闭合。

## 6. 指标目录（D9）

| metric_id | 中文名 | D1 | 挂载点 |
| --- | --- | --- | --- |
| `M_SYNTH_ELEM_INDEX` | 区域创新要素指数（综合） | missing（`Q-SYNTH-02`） | F-ELEM-01 综合卡 / 排名 / 趋势 / 过程完成态 |
| `M_SYNTH_ELEM_TYPE_INDEX` | 区域创新要素类型指数 | missing（`Q-SYNTH-E-01`） | F-ELEM-01 类型透镜总览 |
| `M_SYNTH_ELEM_TYPE_SCORE` | 七要素类型维得分 | draft（`Q-SYNTH-E-01`） | F-ELEM-01 七要素卡 |
| `M_SYNTH_ELEM_LEVEL_INDEX` | 区域创新要素层次指数 | missing（`Q-SYNTH-E-01`） | F-ELEM-01 层次透镜 |
| `M_SYNTH_ELEM_LEVEL_SCORE` | 七大结构层次评价 | draft（`Q-SYNTH-E-01`） | F-ELEM-01 结构达标表 |
| `M_SYNTH_ELEM_DOMAIN_INDEX` | 区域创新要素领域指数 | missing（`Q-SYNTH-E-01`） | F-ELEM-01 领域透镜 |
| `M_SYNTH_ELEM_INDICATOR` | 要素分项指标值与得分 | draft（`Q-SYNTH-02`） | F-ELEM-01 指标明细 / F-ELEM-03 |
| `M_SYNTH_ELEM_WEIGHT` | 类型/层次/领域权重分布 | missing（`Q-SYNTH-E-01`） | F-ELEM-01 权重区 / F-ELEM-03 |
| `M_SYNTH_ELEM_CONTRIB` | 要素贡献度与影响路径 | missing（`Q-SYNTH-E-02`） | F-ELEM-01 贡献路径区 |
| `M_SYNTH_ELEM_RANK` | 对比范围要素综合排名 | missing（随综合指数） | F-ELEM-01 排名榜 |

就绪度：Pack1 阶段 D4 默认 mock（🧪）；跑批秒开结果在评审态标注「跑批预计算」；正式 ADS / 算法卡由 `SYNTH-MOD-ELEMENT-METRIC-OPEN-L01` 闭合。

## 7. 状态与 URL（`CT-SYN-CTX`）

| 状态 | 持久化 | URL | 说明 |
| --- | --- | --- | --- |
| 目标区域 | ✅ `topic-synth-workbench` | `region` | 默认 `深圳` |
| 对比范围 | ✅ | `compare` | 默认 `全国重点城市` |
| 时间窗 | ✅ | `window` | 默认 `最近3年`（取值 `3y`） |
| 结果模式 | — | `mode=result\|config` | 默认三元组且有跑批 → 直接 `result` |
| 分析任务 | — | `/tasks/:taskId` | 改条件提交后进入 F-ELEM-02 |
| 方法抽屉 | — | `panel=method` | F-ELEM-03 |
| 透镜 Tab | ✅（可选） | `lens=type\|level\|domain\|all` | 默认 `all` |

优先级：URL > localStorage > 系统默认。三叶必须读写同一 `CT-SYN-CTX` 键；**不得**为本叶另起互斥默认值。

## 8. 默认秒开 vs 改条件跑批

```
进入 F-ELEM-01
  ├─ context == 默认三元组 且 BatchSnapshot 存在
  │     → 秒开结果面（不创建 analysis task；不展示过程页）
  └─ context 任一字段 ≠ 默认 或 无对应跑批
        → 配置面：展示当前条件差集 + 「开始分析」
              → 创建 ElementTask → F-ELEM-02 五阶段（要素场景文案）
                    → 完成后停留过程页，用户点「查看分析结果」回 F-ELEM-01 结果面
```

## 9. 跨叶 / 跨模块契约

| ID | 方向 | 契约 |
| --- | --- | --- |
| `CT-SYN-CTX` | 三叶共享 | 区域 / 对比范围 / 时间窗；**引用 VITALITY 草案 defaults，不另起** |
| `CT-SYN-VIT-ELEM` | 入 ← 活力叶 | 「下钻要素分析」携带同一上下文 |
| `CT-SYN-ELEM-COLLAB` | 出 → 协同叶 | 「查看协同分析」携带同一上下文 |
| `CT-SYN-ELEM-VIT` | 出 → 活力叶 | 「返回活力分析」携带同一上下文 |
| `CT-SYN-03` | 出 → 报告面 | 「生成分析报告」挂不可变结果快照 |
| `CT-SYN-JOBS` | 出 → SYS-ANALYSIS-JOBS | 任务类型 `region_innovation_elements`；阶段文案由本叶登记 |

## 10. 本轮决策摘要（非源需求）

| 项 | 源需求 | 本轮决策 | 待确认 |
| --- | --- | --- | --- |
| 默认区域/对比/时间 | Bid 未规定默认值 | 与 VITALITY 一致：深圳 / 全国重点城市 / 最近 3 年；默认秒开靠跑批 | 见 `Q-SYNTH-V-02`（共享） |
| 改条件交互 | §8.2 未写过程页；对齐 SYS-ANALYSIS-JOBS / 产业链过程壳 | 非默认走后台任务 + **要素场景**可视化五阶段 | — |
| 要素对象清单 | 系统方案举例子集；旧 DEMO 四类 | **以算法库七要素为准** | 资金/空间输入完整性 → `Q-SYNTH-E-04` |
| 权重/综合公式/贡献路径 | 算法库要求阈值权重；贡献路径系统方案有、算法细则未闭合 | D1 missing + Q；禁止伪闭合 | `Q-SYNTH-02` / `Q-SYNTH-E-01` / `Q-SYNTH-E-02` |
