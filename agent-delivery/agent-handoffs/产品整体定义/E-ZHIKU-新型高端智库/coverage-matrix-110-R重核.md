# 110 项覆盖矩阵 R 批次重核（E-ZHIKU-PROTOTYPE-110 · R6 · 2026-08-05）

> **本文件为 R1-R5 重跑后的逐序号覆盖重核**，由 R6 批次产出。行级"原型落点"详情见业务仓 `demo-ui-gaoduanzhiku-view/docs/coverage-matrix-110.md`（S0-S6 历史 + §六 R 批次说明）；本文件登记每个序号的**归属叶子 / TRACE 文件 / 实现路由 / R 重核状态**，与五件套 TRACE 反向核对一致。
>
> 状态图例：✅ closed（闭环可演示）｜ ✅🧪 演示态（闭环可演示，但含算法/数据演示态诚实性标注，禁止对外决策展示）｜ ✅❓ 口径待定（功能闭环，业务口径挂客户决策清单 🟡）
>
> TRACE 文件均位于本目录对应叶子文件夹下；开放项 Q-ZHIKU-01~07 见 `agent-delivery/客户决策清单跟踪表.md` §2.ad。

## 汇总

| 批次 | 叶子 | 序号段 | USM AC 数 | handoff 自走查 | 状态 |
|---|---|---|:---:|:---:|:---:|
| R1 | ZHIKU-WRITING-报告智能写作 | 88-110 | 41 | 核心项抽核 + 用户打样确认达标 | integration |
| R2 | ZHIKU-BASIC-RESEARCH-基础研究智能决策 | 82-87 | 40 | 39/39 ✅ | integration |
| R3 | ZHIKU-TALENT-POOL-科技人才库 | 59-74、80-81 | 42 | 42/42 ✅ | integration |
| R3 | ZHIKU-TALENT-MAP-科技人才地图 | 75-79 | 27 | 27/27 ✅ | integration |
| R4 | ZHIKU-RESEARCH-NEED-研究需求分析 | 1-7 | 25 | 25/25 ✅ | integration |
| R4 | ZHIKU-TECH-SYSTEM-技术体系分析 | 8-28 | 35 | 35/35 ✅ | integration |
| R4 | ZHIKU-TECH-TREND-技术趋势分析 | 29-45 | 28 | 28/28 ✅ | integration |
| R5 | ZHIKU-STRATEGY-ROADMAP-领域技术线路 | 46-49 | 22 | 22/22 ✅ | integration |
| R5 | ZHIKU-STRATEGY-REPORT-战略咨询报告 | 50-54 | 26 | 26/26 ✅（1 条偏离登记：AC-RM-04-03 内联直出） | integration |
| R5 | ZHIKU-SMART-QUERY-智能问数 | 55-58 | 22 | 22/22 ✅ | integration |
| **合计** | 10 叶子 | **1-110 全闭合，无遗漏** | **308** | R2-R5 逐条 266 条 + R1 打样确认 | — |

## 逐序号登记

### 1-7 · ZHIKU-RESEARCH-NEED（TRACE-ZHIKU-RESEARCH-NEED.yaml · R4）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 1 | 搜索与筛选区（科技实体清单） | strategy/research-need | ✅ |
| 2 | 结果展示区（科技实体清单） | strategy/research-need | ✅ |
| 3 | 搜索结果定位（科技实体清单算法） | strategy/research-need | ✅🧪 Mock 匹配，算法待后端 |
| 4 | 颠覆性技术识别模块 | strategy/research-need | ✅ |
| 5 | 前沿技术清单模块 | strategy/research-need | ✅ |
| 6 | 技术趋势分析模块（宏观统计卡片） | strategy/research-need | ✅ |
| 7 | 媒体聚焦 | strategy/research-need | ✅（生成简报走 CT 契约；图谱联动 🧪 GAP-ZHIKU-RN-KG-LINK） |

### 8-28 · ZHIKU-TECH-SYSTEM（TRACE-ZHIKU-TECH-SYSTEM.yaml · R4）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 8 | 技术体系模块 | strategy/tech-system | ✅ |
| 9 | 在线编辑模块（技术体系树形编辑器） | strategy/tech-system | ✅ |
| 10 | 专家交互模块 | strategy/tech-system | ✅ |
| 11 | 论文分析总览模块 | strategy/tech-system | ✅ |
| 12 | 二维交叉分析 | strategy/tech-system | ✅ |
| 13 | 论文分析任务列表模块 | strategy/tech-system | ✅ |
| 14 | 任务操作模块（论文） | strategy/tech-system | ✅ |
| 15 | 专利分析总览模块 | strategy/tech-system | ✅ |
| 16 | 专利任务管理模块 | strategy/tech-system | ✅ |
| 17 | 专利案例库模块 | strategy/tech-system | ✅ |
| 18 | 专利深度分析模块 | strategy/tech-system | ✅（生成报告走 CT-TS-01） |
| 19 | 专利分析总览模块（算法层） | strategy/tech-system | ✅🧪 能力说明卡，Python 层后续 |
| 20 | 专利任务管理模块（算法层） | strategy/tech-system | ✅🧪 能力说明卡，Python 层后续 |
| 21 | 科研项目检索模块 | strategy/tech-system | ✅ |
| 22 | 科研项目统计分析模块 | strategy/tech-system | ✅ |
| 23 | 科研项目任务管理模块 | strategy/tech-system | ✅ |
| 24 | 社会网络可视化模块 | strategy/tech-system | ✅ |
| 25 | 社会网络结果分析模块 | strategy/tech-system | ✅ |
| 26 | 社会网络任务管理模块 | strategy/tech-system | ✅ |
| 27 | 社会网络数据上传模块 | strategy/tech-system | ✅ |
| 28 | 社会网络维护模块 | strategy/tech-system | ✅ |

### 29-45 · ZHIKU-TECH-TREND（TRACE-ZHIKU-TECH-TREND.yaml · R4）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 29 | 聚类任务模块 | strategy/tech-trend | ✅ |
| 30 | 聚类结果模块 | strategy/tech-trend | ✅🧪 聚类算法演示态（Q-ZHIKU-04） |
| 31 | 聚类筛选模块（初/中/终级） | strategy/tech-trend | ✅ |
| 32 | 聚类清单定制模块 | strategy/tech-trend | ✅ |
| 33 | 共性网络分析任务模块 | strategy/tech-trend | ✅ |
| 34 | 共性网络关系矩阵模块 | strategy/tech-trend | ✅ |
| 35 | 共性网络聚类规则模块 | strategy/tech-trend | ✅ |
| 36 | 共性网络语义网络模块 | strategy/tech-trend | ✅🧪 语义网络演示态（Q-ZHIKU-04） |
| 37 | 共性网络高产作者模块 | strategy/tech-trend | ✅（作者→人才库画像 CT-TT-01） |
| 38 | 技术热点模块 | strategy/tech-trend | ✅ |
| 39 | 交叉关联模块 | strategy/tech-trend | ✅ |
| 40 | 合作分析模块 | strategy/tech-trend | ✅ |
| 41 | 发展趋势模块 | strategy/tech-trend | ✅🧪 预测区间 `ZHIKU-TT-TREND-FORECAST` D1 missing（Q-ZHIKU-04） |
| 42 | 预警信息模块 | strategy/tech-trend | ✅（预警研判报告 CT-TT-02） |
| 43 | 动态跟踪模块 | strategy/tech-trend | ✅ |
| 44 | 预警推送模块 | strategy/tech-trend | ✅ |
| 45 | 趋势检测模块 | strategy/tech-trend | ✅🧪 检测算法演示态（Q-ZHIKU-04） |

### 46-49 · ZHIKU-STRATEGY-ROADMAP（TRACE-ZHIKU-STRATEGY-ROADMAP.yaml · R5）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 46 | 德尔菲问卷功能概述模块 | strategy/tech-roadmap | ✅ |
| 47 | 德尔菲问卷模块 | strategy/tech-roadmap | ✅ |
| 48 | 技术发展路线模块 | strategy/tech-roadmap | ✅（生成报告 CT-RM-01） |
| 49 | 开发精度模块 | strategy/tech-roadmap | ✅（研制精度环形进度，AC-RM-04-01） |

### 50-54 · ZHIKU-STRATEGY-REPORT（TRACE-ZHIKU-STRATEGY-REPORT.yaml · R5）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 50 | 研究报告管理 | strategy/report-mgmt | ✅ |
| 51 | 洞察报告发布 | strategy/report-mgmt | ✅ |
| 52 | 热点分析 | strategy/report-mgmt | ✅🧪 热度指数 `ZHIKU-SP-HOTSPOT-INDEX` D1 missing（Q-ZHIKU-04）；页面归属待核实（Q-ZHIKU-02） |
| 53 | 战略咨询报告生成 | strategy/report-mgmt | ✅（生成报告 CT-SP-01） |
| 54 | 战略咨询案例展示 | strategy/case-show | ✅❓ 案例投资额/ROI/满意度口径待甲方（Q-ZHIKU-06） |

### 55-58 · ZHIKU-SMART-QUERY（TRACE-ZHIKU-SMART-QUERY.yaml · R5）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 55 | 多源数据接入 | strategy/smart-query | ✅❓ 智谱集成契约待三方联席（Q-ZHIKU-07） |
| 56 | 自然语言查询 | strategy/smart-query | ✅🧪 NL2SQL 演示态（Q-ZHIKU-04；集成契约 Q-ZHIKU-07） |
| 57 | 数据看板显示 | strategy/smart-query | ✅❓ 智树看板集成契约待三方联席（Q-ZHIKU-07） |
| 58 | 一键报告生成 | strategy/smart-query | ✅（生成报告 CT-SQ-01） |

### 59-74、80-81 · ZHIKU-TALENT-POOL（TRACE-ZHIKU-TALENT-POOL.yaml · R3）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 59 | 人才画像·基础信息 | talent/profile | ✅ |
| 60 | 人才画像·关联信息 | talent/profile | ✅🧪 影响力/成长指数演示态公式（Q-ZHIKU-04） |
| 61 | 人才画像·行为信息 | talent/profile | ✅ |
| 62 | 人才画像·心理信息 | talent/profile | ✅🧪 高敏感字段演示态，采集边界待合规（Q-ZHIKU-05，常驻 ⚠️ 声明） |
| 63 | 领域人才·节点分类管理 | talent/pool | ✅ |
| 64 | 领域人才·层级分类筛选 | talent/pool | ✅ |
| 65 | 领域人才·知识图谱与智能推荐 | talent/pool | ✅🧪 推荐为演示态 |
| 66 | 领域人才·数据可视化与导出 | talent/pool | ✅（空结果导出禁用） |
| 67 | TOP100·个性化筛选与条件设定 | talent/pool | ✅ |
| 68 | TOP100·人才池列表展示 | talent/pool | ✅ |
| 69 | TOP100·人才池详细画像 | talent/pool | ✅（跳转 talent/profile 携 ID，URL 可恢复） |
| 70 | TOP100·专属人才池管理 | talent/pool | ✅（生成报告 CT-TP-01；共享复制摘要） |
| 71 | 列表筛选·多维检索与筛选面板 | talent/pool | ✅（空词检索拦截） |
| 72 | 列表筛选·人才列表与卡片展示 | talent/pool | ✅ |
| 73 | 列表筛选·核心统计与可视化分析 | talent/pool | ✅ |
| 74 | 列表筛选·导出与个性化清单 | talent/pool | ✅ |
| 80 | 人才动态资讯 | talent/news | ✅（订阅规则真实推送 CT-TP-02） |
| 81 | 信息推送（千人千面） | talent/news | ✅🧪 个性化推荐为前端关键词过滤演示 |

### 75-79 · ZHIKU-TALENT-MAP（TRACE-ZHIKU-TALENT-MAP.yaml · R3）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 75 | 人才分布与动态趋势分析 | talent/map | ✅（地图↔列表双向联动，选中点持久化） |
| 76 | 人才指数 | talent/map | ✅🧪 `ZHIKU-TM-TALENT-INDEX` D1 missing（Q-ZHIKU-04）；权重零和显示"—" |
| 77 | 人才检索 | talent/map | ✅🧪 语义检索为同义词字典演示态 |
| 78 | 人才驾驶舱 | talent/map | ✅🧪 趋势预测演示态（Q-ZHIKU-04）；统计卡显隐定制 |
| 79 | 人才库订阅 | talent/map | ✅（订阅命中预览；生成报告 CT-TM-01） |

### 82-87 · ZHIKU-BASIC-RESEARCH（TRACE-ZHIKU-BASIC-RESEARCH.yaml · R2）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 82 | 问题识别与清单研发 | basic-research/issues | ✅（订阅/识别/发布刷新后保留；智能识别 🧪） |
| 83 | 问题发展趋势分析 | basic-research/issues | ✅🧪 潜力评估演示态打分；下钻 URL tab/issue 可分享恢复 |
| 84 | 国内外竞争格局报告 | basic-research/issues | ✅🧪 区域对比指数 D1 missing（Q-ZHIKU-04）；生成报告 CT（真实预填写作任务） |
| 85 | 深圳市基础研究部署清单 | basic-research/deploy | ✅🧪 清单为 Mock 静态集合；地图↔表格双向选中 |
| 86 | 基础研究组织实施分析 | basic-research/org | ✅🧪 需求预测/资源配置建议演示态 |
| 87 | 基础研究成果评估 | basic-research/eval | ✅🧪 四维得分 D1 missing（Q-ZHIKU-04）；对比/趋势切换持久化；生成报告 CT |

### 88-110 · ZHIKU-WRITING（TRACE-ZHIKU-WRITING.yaml · R1）

| # | 功能名称 | 路由 | 状态 |
|---|---|---|:---:|
| 88 | 挑选与预览战略报告模板 | writing/create | ✅ |
| 89 | 自定义模版大纲内容 | writing/create | ✅ |
| 90 | 自定义分析思路自动生成段落 | writing/create | ✅🧪 AI 生成为模拟 |
| 91 | 后台运行执行 AI 写作任务 | writing/create、writing/tasks | ✅🧪 写作进度为模拟 |
| 92 | 一键导出多格式报告文件 | writing/tasks | ✅（客户端文件生成下载） |
| 93 | 管理个人常用模板库 | writing/create | ✅ |
| 94 | 编辑个人模版内容 | writing/create | ✅ |
| 95 | 个人报告写作模版分享与保存 | writing/create | ✅ |
| 96 | 复制系统模版并编辑 | writing/create | ✅ |
| 97 | 删除个人模版 | writing/create | ✅ |
| 98 | 自然语言写作输入 | writing/create | ✅🧪 NL 意图解析为模拟 |
| 99 | 对话意图确认与追问引导 | writing/create | ✅🧪 NlIntentModal 意图确认 |
| 100 | 自动调取数据与图表生成 | writing/create（跨叶子共用 strategy/report-mgmt） | ✅🧪 |
| 101 | 图表样式切换 | strategy/smart-query（共用） | ✅ 页面归属待核实（Q-ZHIKU-02） |
| 102 | 历史创作内容保存 | writing/tasks | ✅（版本历史持久化） |
| 103 | 报告自动生成规范脚注 | writing/create | ✅ |
| 104 | 报告引用内容查看来源出处 | writing/create（共用 strategy/report-mgmt） | ✅（SourceDrawer 溯源） |
| 105 | 一键跳转原文/研报页面 | strategy/report-mgmt（共用） | ✅ 归属待核实（Q-ZHIKU-02） |
| 106 | 报告文本 AI 改写 | writing/create | ✅🧪 AI 改写为模拟 |
| 107 | 自动生成数据溯源附录 | writing/create（共用 strategy/report-mgmt） | ✅ |
| 108 | 用户上传材料 | writing/materials | ✅（上传/解析状态模拟，持久化） |
| 109 | 基于用户自定义素材写作 | writing/materials、writing/create | ✅（素材关联任务追踪） |
| 110 | 用户自定义素材溯源 | writing/materials | ✅ |

## 反向核对结论

- 1-110 在十份 TRACE 中逐条登记，**无遗漏、无双重归属**（跨叶子共用页面 100/104/105/107 在 TRACE 标注共用关系、计数归 WR）。
- 演示态/口径待定共 **30 行**（✅🧪 27 行 + ✅❓ 3 行），全部有 UI 诚实性标注 + 客户决策清单登记（Q-ZHIKU-02/04/05/06/07），不阻塞演示、禁止对外决策展示。
- 旧指标 id（ZHIKU-S1-\*~S5-\*）运行时零残留，rename 记录保留于 metricSeed/readinessSeed 注释与各 TRACE §renames。
