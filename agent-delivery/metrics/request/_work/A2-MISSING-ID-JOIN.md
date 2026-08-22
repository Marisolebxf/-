# A2 库 missing × 赋号草稿对照（2026-08-22）

> **口径**：功能要了、算法库未覆盖 = A2 列 11 `missing`。  
> **本表**：左连 `id-assign/*.yaml` 的正式草稿号。  
> **不改**：A2 `差集判定`、seed、catalog。有 `M_*` **不等于** mapped。  
> **A1** 双表未交，对照仍是 SRS 05 + B 轨。

## 计数

| 口径 | 条 |
|------|----|
| 专题 missing（主清单） | **7** |
| 展示 missing 主清单 | **70**（items 71，1 条专题重复已标 `topic_repeat_dropped`） |
| 已贴正式草稿号、库仍 missing | **48** |
| 尚无正式号 | **29** |

join：`{'a2_already_had_id': 5, 'no_id_this_loop': 29, 'id_assigned_still_missing': 43, 'topic_repeat_dropped': 1}`

## 已贴正式草稿号（库缺口保持）

| page_id | 主项 | 子项 | a2_metric_id | draft_metric_id | 建议类型 | join |
|---|---|---|---|---|---|---|
| CHAIN-TOPIC-PANORAMA | 产业链关联产品数 | — | M_CHAIN_PRODUCT_COUNT | M_CHAIN_PRODUCT_COUNT | — | a2_already_had_id |
| CHAIN-TOPIC-PANORAMA | 产业链关联专利数 | — | M_CHAIN_PATENT_COUNT | M_CHAIN_PATENT_COUNT | — | a2_already_had_id |
| E7-POLICY | 产业适配性 | 三维一级 | M_POLICY_INDUSTRY_FIT | M_POLICY_INDUSTRY_FIT | — | a2_already_had_id |
| SYNTH-ELEMENT | 要素贡献度与影响路径 | 贡献路径区 | M_SYNTH_ELEM_CONTRIB | M_SYNTH_ELEM_CONTRIB | — | a2_already_had_id |
| SYNTH-COLLAB | 协同—创新产出关联结果 | 效果评估 | M_SYNTH_COLLAB_OUTPUT_CORR | M_SYNTH_COLLAB_OUTPUT_CORR | — | a2_already_had_id |
| DS-01-FACTORS | 要素影响力 | 会议影响力 | — | M_INNOV_CONFERENCE_INFLUENCE | MODEL | id_assigned_still_missing |
| DS-01-FACTORS | 要素影响力 | 项目影响力 | — | M_INNOV_PROJECT_INFLUENCE | MODEL | id_assigned_still_missing |
| DS-01-FACTORS | 要素影响力 | 专利影响力 | — | M_INNOV_PATENT_INFLUENCE | MODEL | id_assigned_still_missing |
| DS-01-FACTORS | 要素影响力 | 期刊影响力 | — | M_INNOV_JOURNAL_INFLUENCE | MODEL | id_assigned_still_missing |
| DS-01-FACTORS | 要素聚类分析 | — | — | M_INNOV_FACTOR_CLUSTER | MODEL | id_assigned_still_missing |
| DS-01-FACTORS | 监测趋势预测 | — | — | M_INNOV_FACTOR_FORECAST | MODEL | id_assigned_still_missing |
| DS-01-FACTORS | 监测异常点识别 | — | — | M_INNOV_FACTOR_ANOMALY | MODEL | id_assigned_still_missing |
| DS-01-EVENTS | 事件关注度 | — | — | M_INNOV_EVENT_ATTENTION | MODEL | id_assigned_still_missing |
| DS-01-EVENTS | 事件影响力 | — | — | M_INNOV_EVENT_INFLUENCE | MODEL | id_assigned_still_missing |
| DS-01-EVENTS | 重要性等级 | 高/中/低自动分级 | — | M_INNOV_EVENT_IMPORTANCE | MODEL | id_assigned_still_missing |
| DS-02-ENTITY | [新增] 技术点影响力 | 实体优先级自动排序 | — | M_TECH_ENTITY_INFLUENCE | MODEL | id_assigned_still_missing |
| DS-02-PATH | 中心度 | — | — | M_TECH_PATH_CENTRALITY | GRAPH | id_assigned_still_missing |
| DS-02-PATH | 关键节点重要性 | 自动识别与标记 | — | M_TECH_PATH_KEYNODE | GRAPH | id_assigned_still_missing |
| DS-02-PATH | 节点优先级/重要度 | 识别核心节点 | — | M_TECH_PATH_PRIORITY | GRAPH | id_assigned_still_missing |
| DS-04-ACHIEVE-OVERVIEW | 创新价值 | 数值计算模型与按价值排序 | — | M_INNOV_ACHIEVE_VALUE | MODEL | id_assigned_still_missing |
| DS-04-MONITOR | 创新点发现 | — | — | M_INNOV_POINT_DISCOVERY | MODEL | id_assigned_still_missing |
| DS-04-MONITOR | 创新价值评估 | — | — | M_INNOV_POINT_VALUE | MODEL | id_assigned_still_missing |
| DS-04-REALTIME | 创新影响分数 | 实体节点影响赋分 | — | M_INNOV_IMPACT_SCORE | MODEL | id_assigned_still_missing |
| DS-04-REALTIME | 创新影响预测 | 创新贡献度 | — | M_INNOV_IMPACT_FORECAST | MODEL | id_assigned_still_missing |
| DS-04-CARRIER-RANK | 创新能力指数 | 数据模型计算与权重 | — | M_INNOV_CARRIER_INDEX_GLOBAL | MODEL | id_assigned_still_missing |
| DS-04-CARRIER-RANK | 多维度排名展示 | 总体/领域/地区 | — | M_INNOV_CARRIER_RANK_GLOBAL | MIXED | id_assigned_still_missing |
| DS-05-GBA-ANALYSIS | 优势因素分析 | 识别/表现/影响程度 | — | M_INNOV_GBA_SWOT_STRENGTH | MODEL | id_assigned_still_missing |
| DS-05-GBA-ANALYSIS | 短板因素分析 | 识别/表现/改进建议 | — | M_INNOV_GBA_SWOT_WEAKNESS | MODEL | id_assigned_still_missing |
| DS-05-GBA-ANALYSIS | 机会因素分析 | 识别/利用建议 | — | M_INNOV_GBA_SWOT_OPPORTUNITY | MODEL | id_assigned_still_missing |
| DS-05-GBA-ANALYSIS | 威胁因素分析 | 识别/应对策略 | — | M_INNOV_GBA_SWOT_THREAT | MODEL | id_assigned_still_missing |
| DS-05-GBA-ACHIEVE | 创新热点区域识别 | 自动识别/密度/主要类型 | — | M_INNOV_GBA_HOTSPOT | MODEL | id_assigned_still_missing |
| DS-06-CARRIER | 创新价值排名 | 高价值载体识别 | — | M_INNOV_CARRIER_VALUE_RANK_SZ | MODEL | id_assigned_still_missing |
| DS-07-POLICY-GUARD | 发展战略引导力评估 | 前瞻性/系统性/针对性 | — | M_INNOV_PG_GUIDE | MODEL | id_assigned_still_missing |
| DS-07-POLICY-GUARD | 政策与条件保障力综合评估 | 自定义权重综合得分 | — | M_INNOV_PG_COMPOSITE | MODEL | id_assigned_still_missing |
| DS-07-INDUSTRY-POTENTIAL | 科学影响力评估 | 论文被引次数/国际合作论文比例 | — | M_INNOV_POT_SCI_INFL | MODEL | id_assigned_still_missing |
| DS-07-INDUSTRY-POTENTIAL | 技术影响力评估 | 专利被引次数/标准必要专利数量 | — | M_INNOV_POT_TECH_INFL | MODEL | id_assigned_still_missing |
| DS-07-INDUSTRY-POTENTIAL | 产业发展潜力综合评估 | 自定义权重/综合得分/排名 | — | M_INNOV_POT_COMPOSITE | MODEL | id_assigned_still_missing |
| DS-07-TECH-INNOV | 专利质量评估 | 被引/权利要求/家族规模 | — | M_INNOV_TINN_PATENT_QUALITY | MODEL | id_assigned_still_missing |
| DS-07-TECH-INNOV | 技术创新力综合评估 | 自定义权重综合得分 | — | M_INNOV_TINN_COMPOSITE | MODEL | id_assigned_still_missing |
| DS-07-TECH-INNOV | 技术创新趋势预测 | 预测结果/置信区间 | — | M_INNOV_TINN_FORECAST | MODEL | id_assigned_still_missing |
| DS-07-SCI-CREATE | 科学创造力趋势预测 | 预测结果/置信区间 | — | M_INNOV_SCI_FORECAST | MODEL | id_assigned_still_missing |
| DS-09-COMPREHENSIVE | 本地特色与优势分析 | 优势领域/全球对比 | — | M_INNOV_PLAN_LOCAL_ADV | MODEL | id_assigned_still_missing |
| DS-09-COMPREHENSIVE | 科技人才流动监控 | 产业界/学术界流动趋势与预警 | — | M_INNOV_PLAN_TALENT_FLOW | MODEL | id_assigned_still_missing |
| DS-09-COMPREHENSIVE | 潜在科技发展方向预警 | 多源监测与预警 | — | M_INNOV_PLAN_DIRECTION_ALERT | MODEL | id_assigned_still_missing |
| DS-09-RESEARCH | 研究领域重叠度 | 两企业重叠度计算/可视化 | — | M_INNOV_RES_OVERLAP | MODEL | id_assigned_still_missing |
| DS-09-RESEARCH | 研究领域等级划分 | 等级标准/自定义阈值 | — | M_INNOV_RES_GRADE | MODEL | id_assigned_still_missing |
| DS-09-RESEARCH | 竞争情报等级 | — | — | M_INNOV_RES_CI_LEVEL | MODEL | id_assigned_still_missing |
| DS-09-RESEARCH | 多企业竞争情报比对 | 竞争矩阵/战略定位图 | — | M_INNOV_RES_CI_COMPARE | MIXED | id_assigned_still_missing |

## 尚无正式号（本批无 OPEN / 未赋号）

| page_id | 主项 | 子项 | a2_metric_id | draft_metric_id | 建议类型 | join |
|---|---|---|---|---|---|---|
| CHAIN-TOPIC-DIAGNOSIS | 环节健康度 | 瓶颈诊断 | — | — | — | no_id_this_loop |
| CHAIN-TOPIC-SHENZHEN | 全球成功案例匹配 | IC-36 | — | — | — | no_id_this_loop |
| DS-11-POLICY-EVAL | 智能摘要与结论推送 | 结果解读报告多维展示 | — | — | — | no_id_this_loop |
| DS-11-POLICY-EVAL | 实施路径与风险辅助 | 推荐方案报告交互展示 | — | — | — | no_id_this_loop |
| DS-16-TALENT-RECRUIT | 沟通障碍智能检测 | 学者引进难度预测 | — | — | — | no_id_this_loop |
| DS-16-TALENT-RECRUIT | 文化融合风险评估 | 学者引进难度预测 | — | — | — | no_id_this_loop |
| DS-16-TALENT-RECRUIT | 国际流动壁垒分析 | 学者引进难度预测 | — | — | — | no_id_this_loop |
| DS-16-TALENT-RECRUIT | 引进阻力量化评分 | 学者引进难度预测 | — | — | — | no_id_this_loop |
| DS-16-TALENT-RECRUIT | 高精度成本模型构建 | 引进成本预测 | — | — | — | no_id_this_loop |
| DS-16-TALENT-RECRUIT | 团队组合与协同分析 | 人才尽调报告与推荐 | — | — | — | no_id_this_loop |
| DS-25-SOFTSCI | 影响力评价与应用反馈 | 成果详情与案例展示 | — | — | — | no_id_this_loop |
| DS-26-ECO | 协同绩效与影响力智能评估 | 成绩单/影响力报告 | — | — | — | no_id_this_loop |
| DS-27-SPATIO | 热点区域自动识别与预警 | 全球研究主体地域时空分布展示 | — | — | — | no_id_this_loop |
| DS-27-SPATIO | 主题演化路径与创新前沿发现 | 专业主题科研活动时空分布分析 | — | — | — | no_id_this_loop |
| DS-29-INCUBATOR | 影响力评价 | 能级/势能/成长路径 | — | — | — | no_id_this_loop |
| DS-21-GRAPH-ANALYSIS | 自动模式识别 | 模式/异常/新兴路径 | — | — | — | no_id_this_loop |
| DS-21-GRAPH-ANALYSIS | 预测分析 | 论文/专利/热点技术趋势 | — | — | — | no_id_this_loop |
| DS-21-GRAPH-ANALYSIS | 分类与聚类 | 实体或事件按相似性分组 | — | — | — | no_id_this_loop |
| DS-21-GRAPH-ANALYSIS | 智能推荐 | 文献/专家/机构/项目/方案 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 多种路径搜索算法支持 | BFS/DFS/Dijkstra/Bellman-Ford/A* | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 最优路径发现与展示 | 最短路径/代价最低路径 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 度中心性计算与展示 | 度中心性值 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 紧密中心性计算与展示 | 紧密中心性值 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 中介中心性计算与展示 | 中介中心性值 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | PageRank算法计算与展示 | PageRank值 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 多种社群发现算法支持 | Louvain/LPA/Infomap/谱聚类/K-means/模块度 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 社群结构自动识别 | 学术团队/技术流派/合作集群 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 社群属性与特征分析 | 核心节点/连接强度/社群间关系 | — | — | — | no_id_this_loop |
| DS-23-GRAPH-ALGO | 社群动态演化追踪 | 形成/扩展/分裂/消亡 | — | — | — | no_id_this_loop |

## 机器文件

- `metrics/request/_work/A2-MISSING-ID-JOIN.yaml`
- `metrics/request/_work/A2-MISSING-ID-JOIN.csv`（Excel 可直接开）
