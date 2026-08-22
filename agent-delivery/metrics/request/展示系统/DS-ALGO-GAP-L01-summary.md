# DS-ALGO-GAP-L01 · 展示差集计数

> 任务：`DS-ALGO-GAP-L01` · 日期：2026-08-22 · **Round 18**（METRIC-OPEN-LOOP 指针返工）  
> 对照：SRS 05（97 叶）+ B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*`  
> A1 双表未交，`A1需规ID` / `A1指标叶ID` 一律空，交卷后回填。  
> yaml 为机器真源。根目录半成品 xlsx 未覆盖。

## 两套计数（必须分开）

| 口径 | 旧版（Round 18 前） | Round 18 后 | 说明 |
|------|---------------------|-------------|------|
| **缺 OPEN 叶 · DS-01…09**（catalog `metric_open_status=missing`） | **35 页** | **0** | 只改指针 + 分类。语义层已挂 9 份态势核对记录。 |
| **缺 OPEN 叶 · E-ZHIKU** | 有 path、无 status | **0**（补 `present` + `ZHIKU-METRIC-OPEN-L01`） | 演示态 🔴 未改 mapped。 |
| **缺 OPEN 叶 · DS-10/11/12** | 有 `METRIC-OPEN-E7-DS10-12` path、无 status | 补 `present` + `POLICY-METRIC-OPEN-L01` | 不重写核对记录。 |
| **缺 OPEN 叶 · DS-13～16** | **4 页** | **4（仍 missing）** | 本批未建展示人才 OPEN。**未改挂** `TOPIC-TALENT-METRIC-OPEN-L01` / `TEMP_TOPIC_TALENT_*`。 |
| **缺 OPEN 叶 · 其它未在 16 张 OPEN 内**（成果/图谱/服务全景/ENT-E33 等） | 保持 | 保持原状 | 不假装有 OPEN。 |
| **库 missing**（列 11，功能要了、算法库未覆盖） | **70**（items 71） | **70（未改）** | 禁止把库缺口改成 mapped。专题已记 7 条不重列。 |

缺 OPEN 叶 ≠ 库缺口。OPEN 存在不把 `missing` 改 `mapped`。

## 总览（列 11，库差集）

| 口径 | 条数 |
|------|------|
| 页面包 | **75**（+ FANIN 数据需求 1 行） |
| 清单行 | **930** |
| **missing 主交付（去专题重复）** | **70** |
| items 内 missing（含专题已列） | 71 |
| mapped | 204 |
| third_party | 16 |
| other_system | 336 |
| n/a_ops | 303 |
| 语义欠账（不进 missing） | 247 |

专题已 missing 的 `M_POLICY_INDUSTRY_FIT`（DS-10-POLICY-PANORAMA，缺口说明含 also_in E7-POLICY）不进主清单。专题 7 条 missing **不重列**。

## 按模块（清单行，含 items 内 missing）

| 模块 | 页 | mapped | missing | third_party | other_system | n/a_ops | 合计 |
|------|----|--------|---------|-------------|--------------|---------|------|
| 科技发展态势 | 35 | 52 | 43 | 13 | 89 | 71 | 268 |
| 科技政策跟踪 | 3 | 25 | 3 | 0 | 11 | 17 | 56 |
| 科技人才态势 | 4 | 33 | 6 | 0 | 26 | 27 | 92 |
| 科技成果展示 | 5 | 7 | 5 | 0 | 50 | 28 | 90 |
| 科技知识图谱 | 4 | 8 | 14 | 0 | 13 | 20 | 55 |
| 科技服务全景 | 5 | 0 | 0 | 0 | 34 | 11 | 45 |
| 科技数据资源 | 4 | 0 | 0 | 0 | 45 | 25 | 70 |
| 企业展示 | 13 | 64 | 0 | 1 | 60 | 76 | 201 |
| 新型高端智库 | 1 | 0 | 0 | 0 | 6 | 25 | 31 |
| 智慧服务门户 | 1 | 15 | 0 | 2 | 1 | 3 | 21 |
| 数据资源 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |

## missing 主清单（70，库未覆盖，Round 18 未改）

| page_id | metric_id | 主项 |
|---------|-----------|------|
| DS-01-FACTORS | （无正式 ID） | 要素影响力 |
| DS-01-FACTORS | （无正式 ID） | 要素影响力 |
| DS-01-FACTORS | （无正式 ID） | 要素影响力 |
| DS-01-FACTORS | （无正式 ID） | 要素影响力 |
| DS-01-FACTORS | （无正式 ID） | 要素聚类分析 |
| DS-01-FACTORS | （无正式 ID） | 监测趋势预测 |
| DS-01-FACTORS | （无正式 ID） | 监测异常点识别 |
| DS-01-EVENTS | （无正式 ID） | 事件关注度 |
| DS-01-EVENTS | （无正式 ID） | 事件影响力 |
| DS-01-EVENTS | （无正式 ID） | 重要性等级 |
| DS-02-ENTITY | （无正式 ID） | [新增] 技术点影响力 |
| DS-02-PATH | （无正式 ID） | 中心度 |
| DS-02-PATH | （无正式 ID） | 关键节点重要性 |
| DS-02-PATH | （无正式 ID） | 节点优先级/重要度 |
| DS-04-ACHIEVE-OVERVIEW | （无正式 ID） | 创新价值 |
| DS-04-MONITOR | （无正式 ID） | 创新点发现 |
| DS-04-MONITOR | （无正式 ID） | 创新价值评估 |
| DS-04-REALTIME | （无正式 ID） | 创新影响分数 |
| DS-04-REALTIME | （无正式 ID） | 创新影响预测 |
| DS-04-CARRIER-RANK | （无正式 ID） | 创新能力指数 |
| DS-04-CARRIER-RANK | （无正式 ID） | 多维度排名展示 |
| DS-05-GBA-ANALYSIS | （无正式 ID） | 优势因素分析 |
| DS-05-GBA-ANALYSIS | （无正式 ID） | 短板因素分析 |
| DS-05-GBA-ANALYSIS | （无正式 ID） | 机会因素分析 |
| DS-05-GBA-ANALYSIS | （无正式 ID） | 威胁因素分析 |
| DS-05-GBA-ACHIEVE | （无正式 ID） | 创新热点区域识别 |
| DS-06-CARRIER | （无正式 ID） | 创新价值排名 |
| DS-07-POLICY-GUARD | （无正式 ID） | 发展战略引导力评估 |
| DS-07-POLICY-GUARD | （无正式 ID） | 政策与条件保障力综合评估 |
| DS-07-INDUSTRY-POTENTIAL | （无正式 ID） | 科学影响力评估 |
| DS-07-INDUSTRY-POTENTIAL | （无正式 ID） | 技术影响力评估 |
| DS-07-INDUSTRY-POTENTIAL | （无正式 ID） | 产业发展潜力综合评估 |
| DS-07-TECH-INNOV | （无正式 ID） | 专利质量评估 |
| DS-07-TECH-INNOV | （无正式 ID） | 技术创新力综合评估 |
| DS-07-TECH-INNOV | （无正式 ID） | 技术创新趋势预测 |
| DS-07-SCI-CREATE | （无正式 ID） | 科学创造力趋势预测 |
| DS-09-COMPREHENSIVE | （无正式 ID） | 本地特色与优势分析 |
| DS-09-COMPREHENSIVE | （无正式 ID） | 科技人才流动监控 |
| DS-09-COMPREHENSIVE | （无正式 ID） | 潜在科技发展方向预警 |
| DS-09-RESEARCH | （无正式 ID） | 研究领域重叠度 |
| DS-09-RESEARCH | （无正式 ID） | 研究领域等级划分 |
| DS-09-RESEARCH | （无正式 ID） | 竞争情报等级 |
| DS-09-RESEARCH | （无正式 ID） | 多企业竞争情报比对 |
| DS-11-POLICY-EVAL | （无正式 ID） | 智能摘要与结论推送 |
| DS-11-POLICY-EVAL | （无正式 ID） | 实施路径与风险辅助 |
| DS-16-TALENT-RECRUIT | （无正式 ID） | 沟通障碍智能检测 |
| DS-16-TALENT-RECRUIT | （无正式 ID） | 文化融合风险评估 |
| DS-16-TALENT-RECRUIT | （无正式 ID） | 国际流动壁垒分析 |
| DS-16-TALENT-RECRUIT | （无正式 ID） | 引进阻力量化评分 |
| DS-16-TALENT-RECRUIT | （无正式 ID） | 高精度成本模型构建 |
| DS-16-TALENT-RECRUIT | （无正式 ID） | 团队组合与协同分析 |
| DS-25-SOFTSCI | （无正式 ID） | 影响力评价与应用反馈 |
| DS-26-ECO | （无正式 ID） | 协同绩效与影响力智能评估 |
| DS-27-SPATIO | （无正式 ID） | 热点区域自动识别与预警 |
| DS-27-SPATIO | （无正式 ID） | 主题演化路径与创新前沿发现 |
| DS-29-INCUBATOR | （无正式 ID） | 影响力评价 |
| DS-21-GRAPH-ANALYSIS | （无正式 ID） | 自动模式识别 |
| DS-21-GRAPH-ANALYSIS | （无正式 ID） | 预测分析 |
| DS-21-GRAPH-ANALYSIS | （无正式 ID） | 分类与聚类 |
| DS-21-GRAPH-ANALYSIS | （无正式 ID） | 智能推荐 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 多种路径搜索算法支持 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 最优路径发现与展示 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 度中心性计算与展示 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 紧密中心性计算与展示 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 中介中心性计算与展示 |
| DS-23-GRAPH-ALGO | （无正式 ID） | PageRank算法计算与展示 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 多种社群发现算法支持 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 社群结构自动识别 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 社群属性与特征分析 |
| DS-23-GRAPH-ALGO | （无正式 ID） | 社群动态演化追踪 |

未发明 M_* 写入 seed。B 轨已有 ID 未打 missing。

## OPEN 指针（Round 18 相对旧版）

旧版 catalog `metric_open_status: missing` → 本轮 `present`（DS-01…09 共 35 页）：

| task | 覆盖页 |
|------|--------|
| `DS-01-METRIC-OPEN-L01` | FACTORS / LAYERS / MAP / EVENTS（4） |
| `DS-02-METRIC-OPEN-L01` | TECHGRAPH / ENTITY / PATH / MAINTAIN-GRAPH / MAINTAIN-ENTITY（5） |
| `DS-03-METRIC-OPEN-L01` | WORKFLOW / RESULT（2） |
| `DS-04-METRIC-OPEN-L01` | ACHIEVE-OVERVIEW / DETAIL / MONITOR / REALTIME / CITY / CARRIER-RANK（6） |
| `DS-05-METRIC-OPEN-L01` | GBA-ANALYSIS / INDICATOR / ACHIEVE / CAPACITY（4） |
| `DS-06-METRIC-OPEN-L01` | CITY / CARRIER / INDICATOR / DOMAIN（4） |
| `DS-07-METRIC-OPEN-L01` | POLICY-GUARD / INDUSTRY-POTENTIAL / TECH-INNOV / SCI-CREATE（4） |
| `DS-08-METRIC-OPEN-L01` | RANK / VIZ / INDICATOR（3） |
| `DS-09-METRIC-OPEN-L01` | COMPREHENSIVE / RESEARCH / KEY-DOMAIN（3） |

本轮 **补** `metric_open_status: present`（原先已有 path、缺 status）：

- `E-ZHIKU` → `ZHIKU-METRIC-OPEN-L01`
- `DS-10-POLICY-PANORAMA` / `DS-11-POLICY-EVAL` / `DS-12-POLICY-SIM` → `POLICY-METRIC-OPEN-L01`

保持诚实 missing（本批未建展示人才 OPEN）：

- `DS-13-TALENT-GLOBAL` / `DS-14-TALENT-REGION` / `DS-15-TALENT-PROFILE` / `DS-16-TALENT-RECRUIT`

专题 catalog **未动**。未改挂 `TOPIC-TALENT`。

## skip（不进清单）

| page_id | 原因 |
|---------|------|
| EDU-ADDON | 教育核增 |
| POLICY-COMPARE-ADDON | 政策对比核增 |
| DS-ANTI-EPIDEMIC | 招标核减 |
| DS-DATAREQ | 一行 other_system 汇总，不算 skip 漏项 |
