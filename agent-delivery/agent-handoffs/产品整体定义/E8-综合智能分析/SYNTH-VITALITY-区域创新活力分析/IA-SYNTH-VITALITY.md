# IA-SYNTH-VITALITY｜区域创新活力分析 · 信息架构

> **版本**：v1.0-pack1 · 2026-08-10  
> **叶子**：`SYNTH-VITALITY`（E8 · 综合智能分析 / 区域创新活力分析）  
> **registry**：`SYNTH-MOD-VITALITY-PACK-L01`  
> **同步**：USM / TRACE / UX-SPEC / Wireframe  
> **历史参照（非权威）**：`../SYNTH-REGION-区域创新分析/` — 禁止复制其演示维权体系为算法对齐

## 1. 导航落位

```
专题服务系统
└── 综合智能分析
    ├── 区域创新活力分析   /intelligence/vitality          ← 本叶
    ├── 区域创新要素分析   /intelligence/elements          （兄弟叶 · CT-SYN-CTX）
    └── 区域创新协同分析   /intelligence/collaboration     （兄弟叶 · CT-SYN-CTX）
```

本叶只闭合系统方案 §8.1.1–8.1.3 与算法库 §10.5；不把 §8.2 / §8.3 能力写进本叶验收。顺链出口仅作上下文契约下钻。

## 2. Frame 清单

| Frame | 名称 | 路由 / 载体 | 主要区块 | 对应故事 |
| --- | --- | --- | --- | --- |
| `F-VIT-01` | 活力分析工作台 | `/intelligence/vitality` | 上下文条 · 默认秒开结果面 / 改条件配置面 · 指数总览 · 四维得分与权重 · 指标方法说明 · 指标明细 · 排名榜 · 趋势 · 优劣结论 · 「开始分析」 | US-VIT-01～05 |
| `F-VIT-02` | 可视化分析过程 | `/intelligence/vitality/tasks/:taskId` | 任务摘要卡 · 「可视化分析过程」五阶段 · 阶段 Alert · 右下操作 | US-VIT-04 |
| `F-VIT-03` | 指标与方法说明抽屉 | F-VIT-01 内 Drawer（`panel=method`） | 四维指标体系树 · 阈值/权重说明 · 合成公式占位（诚实态） · 输入来源 §10.1–10.4 | US-VIT-02 |

## 3. 产品角色（可回指源章节）

| 角色 ID | 产品角色 | 源文件 · 章节 · 原文依据 | 数据边界 |
| --- | --- | --- | --- |
| `ROLE-SYN-GOV` | 政府科技战略决策用户 | `科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.8：「科技政策顶层设计、资源统筹配置与生态优化」；§8.1「支撑战略定位与政策优化」；算法库 §1.1.1.1.1.1.1.10「为政府部门制定产业政策…」 | 授权范围内区域指标与对比结果 |
| `ROLE-SYN-RESEARCH` | 科研机构 / 研究分析用户 | 算法库 §1.1.1.1.1.1.1.10：「支持政府、**科研机构**及企业在战略规划、政策制定、资源配置等场景中的科学决策」 | 公开口径指标；脱敏对比 |

> 不另造「业务分析师 / 园区专员」等岗位 persona。园区运营若需独立角色 → 待业务确认（开放项 `Q-SYNTH-V-ROLE`）。

## 4. 数据对象

| 对象 | 关键字段 | 说明 |
| --- | --- | --- |
| `RegionContext` | `region` / `compareScope` / `window` | 三叶共享；契约 `CT-SYN-CTX` |
| `VitalityDefaults` | region=`深圳` · compare=`全国重点城市` · window=`最近3年` | **系统默认**；与跑批键一致则秒开 |
| `BatchSnapshot` | `batchKey` / `computedAt` / `resultRef` | 默认三元组对应的后台跑批结果；存在则秒开 |
| `VitalityTask` | `taskId` / `frozenContext` / `status` / `nodes[]` | 改条件后「开始分析」创建的不可变任务 |
| `DimScore` | dim∈{tech,industry,talent,policy} / score / weight / inputsRef | 算法库四维；输入来自 §10.1–10.4 评价结果 |
| `IndicatorRow` | id / name / caliber / weight / rawValue / score / dim | 指标体系叶子；Bid 列举高企/专利/论文等映射到对应维 |
| `VitalityResult` | index / dimScores[] / weights[] / rankList[] / trend[] / strengths[] / weaknesses[] / methodDigest | 算法库 §10.5 输出映射 |

## 5. 指标体系与算法语义（对齐算法库 §10.5）

| 一级维度（算法库） | 输入来源（算法库） | 产品展示要点 |
| --- | --- | --- |
| 区域创新科技 | §10.1 科技创新成果评价 | 专利质量、技术转化等指标行 + 维得分 |
| 区域创新产业 | §10.2 产业创新成果评价 | 产品服务 / 企业 / 服务机构创新绩效 |
| 区域创新人才 | §10.3 产业创新人才评价 | 数量、学历/年龄结构、成果产出 |
| 区域创新政策 | §10.4 产业创新政策评价 | 政策数量、类型、效果 |

合成：阈值与权重设计 → 加权求和生成 **区域创新活力指数**（§10.5 阐述 1–5）。公式 / 正式权重合计规则未定 → D1 missing + `Q-SYNTH-01` / `Q-SYNTH-V-*`，禁止伪闭合。

系统方案 §8.1.1 列举的「高新技术企业数量、专利申请与授权量、高质量论文数量」作为 **指标叶子示例** 挂入对应维度，不得另起与算法库冲突的「主体/产出/投入/转化」四维演示体系冒充算法对齐。

## 6. 指标目录（D9）

| metric_id | 中文名 | D1 | 挂载点 |
| --- | --- | --- | --- |
| `M_SYNTH_VIT_INDEX` | 区域创新活力指数 | missing（`Q-SYNTH-01`） | F-VIT-01 指数卡 / 排名 / 趋势 / 过程完成态 |
| `M_SYNTH_VIT_DIM_SCORE` | 四维单维评分 | draft（`Q-SYNTH-V-01`） | F-VIT-01 四维卡 / 权重分布 |
| `M_SYNTH_VIT_INDICATOR` | 活力分项指标值与得分 | draft（`Q-SYNTH-01`） | F-VIT-01 指标明细 / F-VIT-03 |
| `M_SYNTH_VIT_WEIGHT` | 维度权重分布 | missing（`Q-SYNTH-V-01`） | F-VIT-01 权重区 / F-VIT-03 |
| `M_SYNTH_VIT_RANK` | 对比范围活力排名 | missing（随指数） | F-VIT-01 排名榜 |

就绪度：Pack1 阶段 D4 默认 mock（🧪）；跑批秒开结果在评审态标注「跑批预计算」；正式 ADS / 算法卡由 `SYNTH-MOD-VITALITY-METRIC-OPEN-L01` 闭合。

## 7. 状态与 URL（`CT-SYN-CTX`）

| 状态 | 持久化 | URL | 说明 |
| --- | --- | --- | --- |
| 目标区域 | ✅ `topic-synth-workbench` | `region` | 默认 `深圳` |
| 对比范围 | ✅ | `compare` | 默认 `全国重点城市` |
| 时间窗 | ✅ | `window` | 默认 `最近3年`（取值 `3y`） |
| 结果模式 | — | `mode=result\|config` | 默认三元组且有跑批 → 直接 `result` |
| 分析任务 | — | `/tasks/:taskId` | 改条件提交后进入 F-VIT-02 |
| 方法抽屉 | — | `panel=method` | F-VIT-03 |

优先级：URL > localStorage > 系统默认。三叶必须读写同一 `CT-SYN-CTX` 键，禁止各叶私有互斥状态机。

## 8. 默认秒开 vs 改条件跑批

```
进入 F-VIT-01
  ├─ context == 默认三元组 且 BatchSnapshot 存在
  │     → 秒开结果面（不创建 analysis task；不展示过程页）
  └─ context 任一字段 ≠ 默认 或 无对应跑批
        → 配置面：展示当前条件差集 + 「开始分析」
              → 创建 VitalityTask → F-VIT-02 五阶段
                    → 完成后停留过程页，用户点「查看分析结果」回 F-VIT-01 结果面
```

## 9. 跨叶 / 跨模块契约

| ID | 方向 | 契约 |
| --- | --- | --- |
| `CT-SYN-CTX` | 三叶共享 | 区域 / 对比范围 / 时间窗同一 store + URL 约定（本叶定义权威草案，ELEMENT/COLLAB 引用） |
| `CT-SYN-VIT-ELEM` | 出 → 要素叶 | 「下钻要素分析」携带同一上下文 |
| `CT-SYN-VIT-COLLAB` | 出 → 协同叶 | 「查看协同分析」携带同一上下文 |
| `CT-SYN-03` | 出 → 报告面 | 「生成分析报告」挂不可变结果快照 |
| `CT-SYN-JOBS` | 出 → SYS-ANALYSIS-JOBS | 任务类型 `region_innovation_vitality`；阶段文案由本叶登记 |

## 10. 本轮决策摘要（非源需求）

| 项 | 源需求 | 本轮决策 | 待确认 |
| --- | --- | --- | --- |
| 默认区域/对比/时间 | §8.1.3 可灵活选择；未规定默认值 | 深圳 / 全国重点城市 / 最近 3 年；默认秒开靠跑批 | 默认集合是否与甲方正式一致 → `Q-SYNTH-V-02` |
| 改条件交互 | §8.1.3「自动调用模型实时计算」 | 非默认走后台任务 + 可视化五阶段（对齐 SYS-ANALYSIS-JOBS） | — |
| 四维命名 | 系统方案举例指标；算法库明确四维 | **以算法库科技/产业/人才/政策为准** | 指标叶子正式清单 → `Q-SYNTH-01` |
