# SCI-INT-A04 handoff · 技术发展跟踪 系统集成依赖分析

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A04（spike） |
| 执行 | agent:product-agent（coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（路径沿用旧写法「九新」） |
| ponytail | N/A（分析叶） |
| 日期 | 2026-10-18 |

## 1. 范围与实现

- 范围：SRS `科技发展态势/技术发展跟踪.md` excel_rows 51–58（P00-baseline leaf=A04，共 8 叶），页面映射 DS-03-RESULT / DS-03-WORKFLOW。
- 产出 31 张 page 层卡片（`产物/SCI-INT-A04.yaml`），字段格式完全按 `_card-template.yaml`。一个叶依赖多种对端能力时按能力拆卡，拆出的卡共用同一个 `srs.excel_row`。
- 按维度：TECH 26 张 / X 5 张 / TAL 0 / ORG 0。本页只评估技术，没有人才、机构维度。X 卡都是纯前端、配置类或跨维度卡：305 区域、308 雷达、319 方法推荐、321 结果联动、324 参数导入导出。
- 指标字段来源：algorithm_type 和 d1_d4 全部来自 MCP `user-metric-registry`（metric-get / metric-query）。10 个 M_TECH_* 指标当前都是 d1=draft、d4=mock。
- 已复核现状：
  - lumen-ui-science-pc 路由是 `/trend/tech-development-tracking`，只调用 `GET /situation/v1/tracking/meta`、`/dataset` 两个接口。
  - lumen-svc-platform 没有任何 situation/tracking 实现。
  - lumen-algo-py 没有技术评估路由。`/internal/v1/chain/hotspot` 是产业链新闻热点，不是 seq134；`/v1/evaluation` 是企业评估。两者都不能复用。

### 1.1 重点问题结论

| 问题 | 结论 | 卡 |
|---|---|---|
| 热力图数据源 | 话题热度来自久新 API-134（DS-03-RESULT-001），成熟度来自 API-137（DS-03-RESULT-002）。我方 Python 适配器把结果落成快照，Java 只读 ADS（IP-08 + IP-11）。KPI 条的均值由快照派生（IP-09），不再向久新索取 | TECH-300/301/302/303 |
| 地域分布 | 区域发展水平、应用情况**没有 metric_id，也没有交付方**。现状由 trackingModel.ts 在前端伪造雷达值。需要新建按区域聚合的 ADS 表，数据来自专利/论文/项目的地址字段（C02 TECH-100/113/120）（metric_missing + structure_escalation） | X-305 / X-308 |
| 气泡图 | X 轴是投资额（M_TECH_INVEST_AMOUNT，STAT，IP-01，来源 C02 TECH-131/132/133），气泡大小是产出规模（M_TECH_OUTPUT_SCALE，STAT，IP-01）。**Y 轴默认用「潜力」**，但 M_TECH_POTENTIAL_SCORE 属于专题系统，不在 DS-03 范围内，已记为冲突。阶段颜色来自 LIFE_STAGE（DS-03-RESULT-004） | TECH-309/312/313/314 |
| 弦图 | 关系强度来自 DS-03-RESULT-006（M_TECH_REL_STRENGTH）。节点的技术关联来自 SRS-105 久新 Python 图谱模型（IP-07，并入 lumen-algo-py），结果写入 Nebula TRSGraph 技术边（C02 TECH-171）。Java 不写 nGQL，经 Python /internal 读取 | TECH-311/316/317 |
| 评估流程是不是异步 Job | SRS 要求「开始评估 → 运行 → 结果」，lumen 现在只是前端模拟进度，详设又写「本页不建 Job」，两者冲突。**草案选 (a)**：用户调整的权重在我方 Python 上，基于已落地的快照重算综合分。走 IP-04 异步 Job，遵守单飞、当天复用、Q-ANALYSIS-01；数据量小时可以降级为同步。需要新建评估运行表（structure_escalation） | TECH-320 |
| 方法推荐 | 规则配置（IP-13），不是算法，不需要久新参与 | X-319 |
| 参数保存 / 导入 / 导出 | 现状：模板只存在内存里，导出是 Message 桩。需要新建参数模板表（structure_escalation）。导入导出保持前端 JSON，由 Java 校验 schema | TECH-323 / X-324 |
| 结果跟踪历史 | 按 snapshot_id 回看历史快照（IP-11），不插值；某期没有快照就断线 | TECH-302/328–330 |
| 久新是否需要开放参数 | **按草案 (a) 不需要**。如果甲方要求「换参数后由久新重算」（方案 b），API-134/137 必须开放权重和阈值参数。已作为 decision_needed 写在 TECH-326/327 | TECH-326/327 |

### 1.2 DS-03-RESULT 与 jiuxin_row_id 对照

| 久新行 | 能力 | 交付形态 | 卡 |
|---|---|---|---|
| DS-03-RESULT-001 | 话题热度 M_TECH_TOPIC_HEAT | API（IP-08） | TECH-300 |
| DS-03-RESULT-002 | 成熟度 M_TECH_MATURITY_LEVEL | API（IP-08） | TECH-301 |
| DS-03-RESULT-004 | 生命周期阶段 M_TECH_LIFE_STAGE | API（IP-08） | TECH-309 |
| DS-03-RESULT-005 | 综合评分 M_TECH_COMPOSITE_SCORE | API；无源时按 IP-10 走空态加 ⚠️ | TECH-310 |
| DS-03-RESULT-006 | 关系强度 M_TECH_REL_STRENGTH | API（IP-08） | TECH-311 |
| SRS-134 | 技术热点深度分析 M_TECH_DEEP_134_1 | API（IP-08） | TECH-326 |
| SRS-137 | 技术成熟度深度分析 M_TECH_DEEP_137_1 | API（IP-08） | TECH-327 |
| SRS-105 | 技术关联图谱 M_TECH_GRAPH_105_1 | Python（IP-07） | TECH-316/317 |

需要久新提供的是 3 项库能力（SRS-134 API、SRS-137 API、SRS-105 Python），DS-03-RESULT-001/002/004/005/006 这 5 个展示行随这 3 项一起交付。另外有 2 项「是否开放参数」待确认（134/137）。所有久新行都是**待确认**（B01 DN-01、R2 SLA）。

## 2. 偏离说明

- 卡片数为 31，超过叶数 8，原因是按对端能力拆卡（总派单 §2 允许）。
- 架构级初稿漏掉了 SRS-105 图谱和 STAT/派生卡，本次已补齐。DS-03-RESULT.yaml 里「无 metric_id」的说法已经过时，本次以注册表为准。
- 页面派生卡（例如 TECH-303 KPI 条）的 counterpart 是 jiuxin，但 jiuxin_row_id 为 null，downstream 里注明复用父库叶快照。这是 IP-09 的约定，不向久新重复索取。
- 已登记的冲突（写在卡片 risks / decision_needed 中）：
  - 详设写「无 Job」，与 SRS / lumen 的运行阶段冲突。
  - COMPOSITE_SCORE 如果按用户权重重算，性质是 COMPUTE，但注册表标为 third_party（DN-03）。
  - 「潜力」被用于 KPI、Y 轴和权重维度，但不在 DS-03 范围内。
  - SRS 是五步流程，lumen 只有三阶段。
  - SRS 写「投资需求」，指标是「投资额」，口径不一致。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A04.yaml`（31 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A04-check.py`（自检脚本）
- 本 handoff
- 未 commit、未 push，也没有修改任何业务仓、seed 或矩阵。

## 4. 验收证据

在 `产物/` 目录下运行 `python _work\A04-check.py`，输出如下：

```
scope_count=8 covered_rows=8 diff=[]
cards: 31 {'TECH': 26, 'X': 5}
cards_per_row: {51: 5, 52: 4, 53: 7, 54: 3, 55: 2, 56: 2, 57: 5, 58: 3}
jiuxin_rows: ['DS-03-RESULT-001', 'DS-03-RESULT-002', 'DS-03-RESULT-004', 'DS-03-RESULT-005', 'DS-03-RESULT-006', 'SRS-105', 'SRS-134', 'SRS-137']
jiuxin_cards: 10
metric_missing: 3
structure_escalation: ['INT-A-X-305', 'INT-A-TECH-320', 'INT-A-TECH-323']
decision_needed: 21
patterns: {'IP-01': 4, 'IP-04': 1, 'IP-07': 1, 'IP-08': 4, 'IP-09': 5, 'IP-10': 5, 'IP-11': 5, 'IP-13': 6}
OK
```

脚本校验的内容：

- P00 中 leaf=A04 的叶共 8 个，等于 scope_count；SRS 行差集为空，且没有超出范围的行。
- 卡片 path 与 P00 一致；int_id 在 300–399 号段内且不重复；维度前缀与 dimension 一致。
- integration_pattern 在 IP-01 到 IP-13 之内。
- jiuxin_row_id 都在 P00 中，且 counterpart 为 jiuxin；DS-03-RESULT-001/002/004/005/006 全部都有卡对应。
- 三要素卡的调用链四段都不为空。
- 卡片的 algorithm_type 和 d1_d4 与 MCP 快照一致；没有 metric_id 的指标卡登记了 metric_missing。

结论：范围 8 叶，已出卡的 SRS 行 8 个，差集 0。

### 4.1 统计

- metric_missing 3 项：
  - TECH-303：KPI「待验证瓶颈」
  - X-305：区域发展水平 / 应用情况
  - X-308：区域雷达 5 轴
- structure_escalation 3 项（升级 human:李伟）：
  - X-305：区域聚合 ADS
  - TECH-320：评估运行表
  - TECH-323：参数模板表
- 久新快照表沿用 B01 已升级项（DN-07），不重复计数。

### 4.2 最大 3 个开放项

1. **「开始评估」的语义**（TECH-320）：有三种方案——(a) 我方基于快照用用户权重重算（草案）；(b) 久新带参数重跑，需要开放参数；(c) 只做展示，不重算。这决定了本页是否需要 Job，以及久新是否要开放参数，需要甲方或 PM 拍板。
2. **综合评分的权重和产出方**（DN-03 / TECH-310）：注册表标为 third_party，但用户可以调权重，性质接近 COMPUTE。权重口径要由甲方确认。
3. **久新 API-134/137 与 Python-105 的接口文档，以及 technology_id 主数据**：技术领域维表和桥接表都不存在（C02 TECH-180/181/182），热力图、气泡图、弦图三张图的 ID 无法对齐。

其他开放项：

- 「潜力」Y 轴超出范围
- 「投资需求」与「投资额」口径不一致
- 前端没有 ⓘ / MockBadge（D9 缺口）
- mock 被直接 import 进真实代码路径
- 前端伪造了明细趋势序列

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 重算、图谱、久新适配都在 lumen-algo-py；Java 只读 ADS |
| 2 调用链：前端 → Java → Python /internal | ✅ call_chain 都按这个顺序写；前端不直连久新；新路由用 /internal/v1/sci/*（B01 R7） |
| 3 只用 NebulaGraph | ✅ SRS-105 结果写入 TRSGraph；Java 不写 nGQL |
| 4 可观测 | ⚠️ 现状 tracking 视图没有接入 observability 埋点（仅记录，本叶不修复） |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ demo 仓只读对照 |
| 7 共享聚合核心 | ✅ 门面落在 gkxlumen-*（模块归属待 DN-07）；与专题系统共用 technology_id（记入风险，B01 C3） |
| 8 ADS 先行 + Mock | ✅ 无源时走 IP-10：空态加 ⚠️，USE_MOCK=false 时不伪造数值；同时指出现状 mock 被 import 进真实路径 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 统计卡都挂了 metric_id，或登记了 metric_missing；指出 tracking 视图没有 ⓘ / MockBadge |
| 11 D10 | N/A |
| 12 D12 | ✅ 方案不调用任何 demo-*；现状 lumen 的 tracking 链路也没有回落到 demo 服务 |
| 禁读 registry YAML | ✅ task 和 metric 都只通过 MCP 查询 |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 260000（估算） |
| model_used | claude-opus-5.5 |
| actual_cost | 6.5（USD，估算） |
| cost_warn | green |
