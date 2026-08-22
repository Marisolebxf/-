# 派单包 · JIUXIN-TECH-ORG-TALENT-L01

> **状态**：`ready`（MCP 已建） · **认领类型**：`pull`（监管人 `human:郭万迎` 开工）或 `coordinator_dispatch`  
> **Agent**：`product-agent` · **supervised_by**：`human:郭万迎` · **辅助**：`human:李伟`（抽清单，不替九新拍板）  
> **仓**：`gkx-orchestration`（只写编排资产，不碰业务仓）  
> **Epic**：`E-ALGO-LIB-DEMO` · **不挡** 8/25 A1  
> **点名**：2026-08-22 `human:淮政玮`  
> **对人说明**：[`给人说明-指标与算法工作类型与流程梳理.md`](./给人说明-指标与算法工作类型与流程梳理.md) §2 / 责任矩阵 / WBS-0.5

## 1. 目标

列出 **专题系统** 与 **展示系统** 中，依赖 **技术链 / 科研机构 / 人才** 的能力，按 `algorithm.type` 分成 **STAT / COMPUTE / MODEL / GRAPH**，并与北京九新确认每条交什么：

| 交付形态 | 默认对应（沟通起点，非最终） |
|----------|------------------------------|
| **SQL** | `STAT`：计数、占比、排名、简单聚合；九新交可执行 SQL 或等价 ODS 字段+粒度说明 |
| **Python 脚本** | `COMPUTE`（有公式无模型）；`GRAPH`（中心性/路径/子图，**Nebula**，禁止 Neo4j） |
| **API** | `MODEL`；A2 已标 `third_party` / 实现类 / Job；需规写了 Restful/SDK 的深度分析叶 |

禁止：前端直连九新；调用链仍 **前端 → Java REST → Python `/internal/*`**。九新 API 由 Java/Python 封装。  
禁止：替九新编公式、改 `cfg_metric-*-seed.yaml`、复活废作 `TOPIC/DS-METRIC-INVENTORY/CLASSIFY-L01`。

## 2. 谁做什么

| 人 | 做什么 |
|----|--------|
| **郭万迎** | 对北京九新谈交付形态；收纪要；清单「九新确认」列只能他（或纪要）改 |
| **李伟** | 从 A2 yaml / SRS 05 抽全量表（专题三维 + 展示依赖行）；标清「不进本包」的企业/投融资 third_party |
| **唐绍祖** | **不**本叶主责。A1 `algorithm.type` 齐了之后回填「暂标」列；本叶不挡 A1 |

## 3. 必读（只读）

1. `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md`（轴 A type、轴 B 功能 Owner 仍待指定）
2. `metrics/request/专题系统/TOPIC-ALGO-GAP-L01.yaml` + summary（机器真源）
3. `metrics/request/展示系统/DS-ALGO-GAP-L01.yaml` + summary
4. `bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/` 下 **技术链 14 / 科研机构 10 / 人才 13**
5. `metrics/request/A2-GAP-schema.md`（差集判定枚举）

A1 `ALGO-LIB-METRIC-DEPS-L01` 仍 `ready` 未认领：`algorithm.type` 本叶用 **SRS 层暂标**（见 §5），A1 交卷后回填，不把本叶做成 A1。

## 4. 禁止塞进九新包

| 行 | 原因 |
|----|------|
| `ENT-SEARCH-009` 市场份额（Q019） | 企业展示采购项，不是技术/机构/人才 |
| `DS-CHAIN-OV-009/010` 投融资（QC07） | 产业链门户待采购，不是九新技术包 |
| 专题查询 / 运营（`n/a_ops`） | 本维未点名功能 Owner，不进九新清单 |
| A2 `missing`（专题 7 + 展示 70） | 那是「库没覆盖」，不是「九新交什么」 |
| 燕大知识图谱专包 | 本叶只对 **北京九新**；图谱层向九新只谈技术/机构/人才实体与关系，不把燕大合同并进本纪要 |

## 5. `algorithm.type` 暂标规则（A1 前）

| SRS 层 | 暂标 type | 向九新默认要 |
|--------|-----------|--------------|
| 基础指标 | `STAT` | **SQL** |
| 图谱 | `GRAPH` | **Python**（+ 图数据约定；禁止 Neo4j） |
| 深度分析 | `MODEL` | **API** |
| A2 `third_party` / 「实现类 / Job」 | 跟所挂库叶；无专叶则 `MODEL` | **API** |
| 加权/标准化且无模型（A1 后可能改 `COMPUTE`） | 先按 `MODEL` 谈 API；九新若只给脚本再改 **Python** | 纪要写清 |

`COMPUTE` 在三维库叶标题里几乎不出现；不要为了填满四列而把 STAT 改成 COMPUTE。

---

## 6. 算法库叶子（对人主清单 · 必须逐条问九新）

共 **37 叶**。`交付默认` = 沟通起点。

### 6.1 技术链（14）

| seq | 层 | 库叶 | type 暂标 | 交付默认 | 专题消费（A2） | 展示消费（A2 third_party 等） |
|-----|----|------|-----------|----------|----------------|-------------------------------|
| 96 | 基础指标 | 技术基础指标模型构建 | STAT | SQL | TECH-003 论文量/专利量 | 态势计数读面，非本包 Job |
| 104 | 图谱 | 技术实体识别构建 | GRAPH | Python | TECH-002 节点下钻 | — |
| 105 | 图谱 | 技术实体关系抽取 | GRAPH | Python | TECH-001 技术网络边 | DS-03 弦线 mapped，非 third_party |
| 130 | 深度 | 全景技术链模型 | MODEL | API | TECH-001 | — |
| 131 | 深度 | 深圳技术链模型 | MODEL | API | TECH-011 | — |
| 132 | 深度 | 技术发展历程模型 | MODEL | API | TECH-015 产品走 CMS，库叶仍须问九新有无 API | 禁止把历程 CMS 当 Job |
| 133 | 深度 | 深圳细分领域分布模型 | MODEL | API | TECH-012 复用 | — |
| 134 | 深度 | 技术前沿热点领域识别模型 | MODEL | API | TECH-004/005 | DS-03-RESULT-001/002；DS-07-SCI-CREATE-003；DS-09-COMPREHENSIVE-001/002/004 |
| 135 | 深度 | 技术产业化潜力识别模型 | MODEL | API | TECH-006/007 | DS-07-TECH-INNOV-003 |
| 136 | 深度 | 技术转化瓶颈堵点原因识别模型 | MODEL | API | TECH-013/014 | — |
| 137 | 深度 | 技术阶段分析模型 | MODEL | API | TECH-008/009；TECH-012 | DS-03-RESULT-004/005/006；DS-07-INDUSTRY-POTENTIAL-002 |
| 138 | 深度 | 深圳技术发展问题识别模型 | MODEL | API | TECH-012 | — |
| 139 | 深度 | 深圳技术发展机遇识别模型 | MODEL | API | TECH-012 | — |
| 140 | 深度 | 深圳技术发展重点布局领域推荐模型 | MODEL | API | TECH-012 | — |

### 6.2 科研机构（10）

| seq | 层 | 库叶 | type 暂标 | 交付默认 | 专题消费 |
|-----|----|------|-----------|----------|----------|
| 99 | 基础指标 | 科研机构基础指标模型构建 | STAT | SQL | RORG-002/005/006/008 |
| 114 | 图谱 | 科研机构实体识别构建 | GRAPH | Python | 机构节点（与选取壳 RORG-001 分开） |
| 115 | 图谱 | 科研机构实体关系抽取 | GRAPH | Python | 随合作链 |
| 149 | 深度 | 科研机构重点技术领域布局模型 | MODEL | API | RORG-003/008 |
| 150 | 深度 | 科研机构发展历程模型 | MODEL | API | RORG-017 产品走 CMS，库叶仍问 |
| 151 | 深度 | 深圳科研机构优势分析模型 | MODEL | API | RORG-015 |
| 152 | 深度 | 深圳科研机构痛难点识别模型 | MODEL | API | RORG-016 |
| 153 | 深度 | 科研合作关系链条模型 | MODEL | API | RORG-010 |
| 154 | 深度 | 科研机构引入推荐模型 | MODEL | API | RORG-013 |
| 155 | 深度 | 科研机构扶持推荐模型 | MODEL | API | RORG-014 |
| — | 实现类 | **技术力评价与对比**（05 无专叶） | MODEL | API | **RORG-012 `third_party`** · 必须单列问九新 |

### 6.3 人才（13）

A2 专题人才 **0 条 third_party、15 条 mapped** —— **仍须全列**，不能因「已 mapped」跳过九新。

| seq | 层 | 库叶 | type 暂标 | 交付默认 | 专题消费 |
|-----|----|------|-----------|----------|----------|
| 98 | 基础指标 | 人才基础指标模型构建 | STAT | SQL | TAL-001/002/003 分布与供给 |
| 110 | 图谱 | 人才实体识别构建 | GRAPH | Python | TAL-014 |
| 111 | 图谱 | 人才实体关系抽取 | GRAPH | Python | TAL-015 |
| 156 | 深度 | 重点人才识别模型 | MODEL | API | TAL-012 |
| 157 | 深度 | 人才流动追踪模型 | MODEL | API | TAL-013；展示 DS-13/14 迁徙 mapped |
| 158 | 深度 | 高校学院新培育人才模型 | MODEL | API | TAL-010 |
| 159 | 深度 | 深圳重点人才优势和短板分析模型 | MODEL | API | TAL-005 |
| 160 | 深度 | 人才关系链模型 | MODEL | API | TAL-004；画像合作网 |
| 161 | 深度 | 人才供需分析评价模型 | MODEL | API | TAL-011 |
| 162 | 深度 | 人才学术力评估模型 | MODEL | API | TAL-006；**展示 DS-08-VIZ-001 H 指数、DS-08-VIZ-004 活跃度**（A2 `third_party`） |
| 163 | 深度 | 人才产业力评估模型 | MODEL | API | TAL-007 |
| 164 | 深度 | 招入人才推荐模型 | MODEL | API | TAL-008；展示 DS-16 推荐/画像 mapped |
| 165 | 深度 | 培育人才布局模型 | MODEL | API | TAL-009 |

---

## 7. 展示系统 · 必须问九新的 third_party（13 条态势 + 2 条实为人才）

A2 展示 `third_party` 共 16：其中 **13** 条科技发展态势（技术 Job 读面）、**2** 条其实挂人才学术力（seq 162）、**3** 条不要进本包（企业份额 1 + 投融资 2）。

| row_id | 页面 | 主项 | 挂库叶 seq | 交付默认 |
|--------|------|------|------------|----------|
| DS-03-RESULT-001 | 技术评估结果 | 话题热力图展示 | 134 | API |
| DS-03-RESULT-002 | 技术评估结果 | 技术话题热度 | 134 | API |
| DS-03-RESULT-004 | 技术评估结果 | 动态气泡图（阶段/成熟度） | 137 | API |
| DS-03-RESULT-005 | 技术评估结果 | 技术成熟度 | 137 | API |
| DS-03-RESULT-006 | 技术评估结果 | 技术发展阶段 | 137 | API |
| DS-07-INDUSTRY-POTENTIAL-002 | 产业发展潜力 | 技术产品成熟度评估 | 137 | API |
| DS-07-TECH-INNOV-003 | 技术创新力 | 技术市场潜力分析 | 135 | API |
| DS-07-SCI-CREATE-003 | 科学创造力 | 科学研究前沿性分析 | 134 | API |
| DS-09-COMPREHENSIVE-001 | 综合发展规划 | 全球热点技术捕捉 · 热度 | 134 | API |
| DS-09-COMPREHENSIVE-002 | 综合发展规划 | 全球热点技术捕捉 · 增速 | 134 | API |
| DS-09-COMPREHENSIVE-004 | 综合发展规划 | 技术与产业热点动态跟踪 | 134 | API |
| DS-08-VIZ-001 | 指数可视化 | 专家 H 指数排行 | **162** | API |
| DS-08-VIZ-004 | 指数可视化 | 专家活跃度 | **162** | API |

展示 **科技人才态势 DS-13～16**：A2 无 third_party。沟通时带上 **mapped 且对应 §6.3 库叶** 的行（分布/迁徙/学术力/关系链/招入推荐）；`n/a_ops` 壳、报告导出、指数 CMS **不问九新要模型**。DS-16 六条 `missing` 是我方库缺口，纪要可附录「库未覆盖、不向九新索要假 API」，不要写成九新已承诺。

展示 **机构** 专页：A2 未单列「科研机构」模块；机构能力主要通过专题 RORG + 库 10 叶问九新。若李伟在展示页发现机构 Job 读面，补进 yaml，禁止口头加项。

---

## 8. 产出（必须全部落盘）

目录：`agent-delivery/metrics/request/九新-技术机构人才/`

| 文件 | 内容 |
|------|------|
| `JIUXIN-TECH-ORG-TALENT-L01.xlsx` | 给人主表。列见下 |
| `JIUXIN-TECH-ORG-TALENT-L01.yaml` | 与 xlsx 同行 |
| `JIUXIN-TECH-ORG-TALENT-L01-minutes.md` | 与九新沟通纪要：谁、何时、每条确认/待确认 |
| `README.md` | 计数：SQL / Python / API / 待确认 |

xlsx 列（顺序固定）：

`系统`（专题/展示）· `维度`（技术链/科研机构/人才）· `page_id` · `row_id`（库叶用 `SRS-{seq}`）· `主项/库叶名` · `SRS seq` · `algorithm.type`（暂标/A1 回填）· `交付形态`（SQL / Python / API）· `九新确认`（确认 / 待确认 / 九新不提供）· `备注`

handoff：`agent-handoffs/算法库联调-ALGO-LIB/JIUXIN-TECH-ORG-TALENT-L01.md`

## 9. DoD

- [ ] 37 库叶 + RORG-012 无专叶项，每条都有 type 暂标 + 交付形态 + 九新确认状态
- [ ] 展示 13 条态势/人才 third_party 已入表；ENT 份额与投融资 **未** 混入
- [ ] 专题 TECH/ORG/TALENT 的 mapped 行能回溯到库叶（李伟辅助）
- [ ] 纪要存在；未确认不得写成「九新已交」
- [ ] 不改 seed、不写业务代码、不挡 A1
- [ ] handoff 含：SQL n / Python n / API n / 待确认 n

## 10. `/goal`（整段粘贴到新 Agent 会话）

```text
/goal
task: JIUXIN-TECH-ORG-TALENT-L01
agent: product-agent
supervised_by: human:郭万迎
辅助: human:李伟（抽清单）
claim_type: pull
强度：本叶为 definition/spike 文档+供应商沟通清单，禁止用 ponytail 砍表完整性；不写代码。
上下文：禁止 compress 代替精读 A2 yaml。

先读：
- agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/JIUXIN-TECH-ORG-TALENT-L01-派单包.md
- agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md
- metrics/request/专题系统/TOPIC-ALGO-GAP-L01.yaml
- metrics/request/展示系统/DS-ALGO-GAP-L01.yaml

动作：
1. MCP task-claim JIUXIN-TECH-ORG-TALENT-L01（supervised_by=human:郭万迎）后开工
2. 李伟辅助按派单包 §6–§7 抽全表；郭万迎对北京九新确认每条交 SQL / Python 脚本 / API
3. 落盘 metrics/request/九新-技术机构人才/ 四件套；写 handoff
4. 不改 seed、不复活废作四叶、不挡 ALGO-LIB-METRIC-DEPS-L01
```
