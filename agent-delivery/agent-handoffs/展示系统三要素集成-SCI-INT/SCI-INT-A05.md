# SCI-INT-A05 handoff：全球创新监测·成果与实时数据系统集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A05（spike） |
| 执行 | agent:product-agent（coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（旧路径沿用「九新」写法） |
| ponytail | N/A（分析叶） |
| 日期 | 2026-10-18 |

## 1. 范围与实现

- **范围**：SRS `科技发展态势/全球创新监测.md` 的 excel_rows 59–75（seq 56–72），对应 P00-baseline 中 leaf=A05 的 17 个叶。页面映射：
  - rows 59–63 → DS-04-ACHIEVE-OVERVIEW
  - rows 64–69 → DS-04-ACHIEVE-DETAIL
  - rows 70–75 → DS-04-REALTIME
  - rows 76–91 属于 A06，本叶不涉及。
- **产出**：`产物/SCI-INT-A05.yaml`，共 25 张 page 层卡片，字段严格按 `_card-template.yaml`；int_id 号段 401–425。
  - 一叶多对端能力时拆卡：row 59（类型分类 / 价值分档）、row 63（成果列表刷新 / 资讯来源）、row 67（机构载体 / 企业载体）、row 72（图谱读面 / 落图 Job / 人才顶点 / 机构顶点）、row 73（机构+技术领域赋分 / 人才赋分口径缺）、row 75（页面水位 / 上游增量时效）。
- **卡片维度分布**：TAL 2、TECH 2、ORG 2、X 19。X 卡中 14 张带三要素维度，调用链四段全部写满；3 张纯 NONE_3E（地理范围筛选、订阅、对比），1 张 OTHER（企业载体）。
- **字段来源**：algorithm_type 与 d1_d4 全部来自 MCP `user-metric-registry`（metric-get / metric-query）。INNOV / SYNTH 域指标写 metric_domain_other（沿用 A01 写法）；三要素域指标（M_TALENT_GRAPH_110_1、M_ORG_GRAPH_114_1）写 metric_ids。无 metric 的卡按 DS-04-* 裁定填 other_system / n/a_ops，落图 Job 与人才赋分无注册类型，填 UNKNOWN。
- **引用而未重分析**：C01（人才主键候选 dwd_scholar.scholar_id，待确认）、C02（无技术主数据，`tech:{名称}` VID 不稳定）、A02（中心性/影响力无交付方，DN-02）、B01（IP 模式、DN-01…09、R4）。

### 1.1 派单关注点结论

| 问题 | 结论 | 卡 |
|---|---|---|
| 「实时」的真实时效 | **当前没有任何真实时能力。**<br>① 三方库源表 update_freq 在 C01/C02 中全部 unknown，供应方未书面给出（SUPPLIER-Q 的更新频率题未回）。<br>② MCP 中本页指标 update_freq 都是 pending，D3 pending_ods，D4 mock。<br>③ 久新 51 行没有 DS-04 行。<br>④ 我方链路是 GDF→ADS 批处理，默认 T+1。<br>⑤ lumen 的「实时同步 · 30s」是前端 setInterval 随机扰动（tooltip 自己注明「演示刷新非真源流」），详情页 45s tick 也是 mock。<br>**草案**：按 T+1 设计（成果列表可评估日内增量），页面显示「数据截至 yyyy-MM-dd HH:mm」，前端轮询只刷新元数据。是否必须分钟级/流式由甲方拍板（DN-A05-01），各源表频率由供应方书面给出（DN-A05-01b）。若甲方要分钟级，需要 CDC/推送方案，会触发结构升级。 | X-406 / X-424 / X-425 |
| 成果如何落图谱 | 由一个读面加三类顶点组成：<br>① 读面：Python `/internal/v1/innov/graph/*` 读 Nebula TRSGraph，Java 只做门面（IP-05）。注册表把 M_SYNTH_GRAPHAPI_116_1 记为 third_party，但久新 51 行没有 116，供应方题 SYNTH-P1-3 未回；如果供应方交 API，改走 IP-08。<br>② 落图 Job（创新点→技术顶点实体链接）：没有 metric_id、没有 05 叶、没有久新行，属于 algo_owner_missing。需要新建 innovation_point tag 和 LOCATED_IN edge（structure_escalation）。<br>③ 技术顶点依赖久新 SRS-104，人才顶点依赖 SRS-110，机构顶点依赖 SRS-114。这三行都已由 A02/B03/B09 提出，本叶**不新增**久新要求。<br>**前置条件**：技术 VID 需按 C02 OI-C02-16 迁移到 `tech:{technology_id}`，否则落点会随名称漂移。<br>现有 gkxlumen-innov 的 ads_innovation_point_map / dwm_graph_* 是 demo 库表，GraphController 直读 DWM（B01 R4），不可沿用。 | TECH-417 / TECH-418 / TAL-419 / ORG-420 |
| 实体影响赋分 | M_INNOV_DS_04_REALTIME_004（MODEL，0–100，覆盖机构和技术领域实体）：05 无叶、久新无行，注册表 algo_server_location 指向 demo-algo-science（D12 不可调）。lumen-algo-py 的 vendor/innov-py P6（PPR + 中心性）是演示版，基于 networkx 内存图，且未挂载到 lumen_algo_service。草案：lumen-algo-py 离线 Job 读 Nebula，写 ADS 快照（目标形态 IP-04，当前按 IP-10 空态加 ⚠️）。<br>与 A02 的 M_TECH_ENTITY_INFLUENCE 是同类缺口，建议与 DN-02 一起定案（DN-A05-03）。<br>SRS 要求对「图谱实体节点」赋分，但指标定义不含人才，因此单列 TAL-422（metric_missing）。 | X-421 / TAL-422 |
| 哪些交互需要后端 | 以下只靠前端：重点高亮的渲染、≤4 项对比的布局、图表类型切换。<br>以下需要服务：分类检索、地图落点与聚合、空间查询（圆形/矩形/多边形/行政区划，前端内存过滤在真实数据量下不可行）、详情、载体关联、订阅与定期推送（gkxlumen-innov 无订阅模块）、KPI 聚合、图谱读面、影响分和预测快照、数据水位。 | 各卡 dep_kind |

### 1.2 需要久新提供的能力（全部待确认）

| 久新行 | 名称 | 交付形态（B01 模式） | 消费卡 | 备注 |
|---|---|---|---|---|
| SRS-104 | 技术实体识别构建 | Python（IP-07） | TECH-418 | 已由 A02 提出；本叶只作技术顶点数据依赖，不是 DS 意义上的指标 mapped |
| SRS-110 | 人才实体识别构建 | Python（IP-07） | TAL-419 | 已由 B03 侧提出 |
| SRS-114 | 科研机构实体识别构建 | Python（IP-07） | ORG-420 | 已由 B09 侧提出 |

本叶涉及久新 3 行，**新增 0 行**。本页三个核心算法（创新价值、影响赋分、影响预测）和落图 Job 在久新清单与 05 库中都没有交付方。架构级初稿中「DS-04 依赖 99/149/153」的说法不适用于 rows 59–75（那几行属于载体/A06），已记为 conflict。

## 2. 偏离说明

- 卡片数为 25，SRS 叶数为 17。差异来自按对端能力拆卡（总派单 §2）。
- gaps 沿用 A01/A02 约定：`metric_missing:` 表示统计数字没有注册 metric_id；`algo_owner_missing:` 表示有 metric_id，但 05 库与久新都不交付。落图 Job 没有 metric_id，也按 algo_owner_missing 记录并加注说明。
- 自检脚本比 A02 版多放宽两处：① 三要素卡允许只用 metric_domain_other 挂指标（INNOV/SYNTH 按派单要求写这里）；② 非三要素 X 卡允许 dimension=[OTHER]（企业载体）。另外新增两项校验：freshness 枚举，以及 TAL/TECH/ORG 卡的 dimension 与号段类型一致。
- DS-04-ACHIEVE-DETAIL 把 seq 65 判为「详情订阅」n/a_ops，但 SRS 原文写「平台将定期推送」，lumen 也已实现区域规则订阅和推送记录。X-413 按需要后端服务（service/push/write_back）记录，冲突写入 conflicts 供评审确认（DN-A05-06）。
- DS-04-REALTIME 禁止本叶 mapped 104/105。TECH-418 挂 SRS-104 只作为技术顶点的数据依赖，没有改动任何映射。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A05.yaml`（25 张卡，含 realtime_verdict / summary / decision_needed / risks）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A05-check.py`（自检脚本）
- 本 handoff
- 没有 commit 或 push，没有改动任何业务仓、seed 或矩阵文件。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A05-check.py"`，输出如下：

```
scope_count=17 covered_rows=17 diff=[]
cards: 25 {'X': 19, 'ORG': 2, 'TECH': 2, 'TAL': 2}
jiuxin_rows: ['SRS-104', 'SRS-110', 'SRS-114']
metric_missing: 5
algo_owner_missing: 7
structure_escalation: 8
patterns: {'IP-01': 11, 'IP-04': 1, 'IP-05': 1, 'IP-07': 2, 'IP-09': 3, 'IP-10': 5, 'IP-13': 2}
OK
```

脚本校验了以下内容：

- P00 中 leaf=A05 的叶恰好是 rows 59–75，共 17 个，与 scope_count 一致；SRS 差集为空，没有超出范围的行。
- 每张卡的 path 与 P00 一致；page_ref 按行段对应正确；int_id 符合 `INT-A-*-4xx` 且不重复；类型分布与 summary 一致。
- integration_pattern 都在 IP-01 到 IP-13 之间；freshness 在枚举内；jiuxin_row_id 都在 P00 jiuxin_rows 中，且 counterpart=jiuxin。
- 带三要素维度的卡，调用链四段都不为空，并且有 metric_ids / metric_domain_other，或登记了 metric_missing，或属于 other_system / n/a_ops。

**结论：范围 17 叶，有卡片覆盖的 SRS 行 17 行，差集 0。**

### 4.1 统计

- **metric_missing 5 张**：
  - X-403：区域成果数 / 热力权重
  - X-406：新增成果数
  - X-415：KPI 环比/增量
  - TECH-418：图谱节点/关系统计
  - TAL-422：人才节点影响分
- **algo_owner_missing 7 张**，涉及 3 个指标加 1 个 Job：
  - M_INNOV_DS_04_ACHIEVE_OVERVIEW_001 创新价值：X-402 / X-404 / X-405 / X-410
  - M_INNOV_DS_04_REALTIME_004 影响分：X-421
  - M_INNOV_DS_04_REALTIME_005 预测：X-423
  - 落图 Job：TECH-418
- **structure_escalation 8 张**（升级给 human:李伟）：
  - X-401：成果统一表 / ES 索引
  - X-405：创新价值快照
  - ORG-411：成果-载体桥表
  - X-413：订阅规则表和推送记录表
  - X-415：KPI 聚合 ADS
  - TECH-418：Nebula innovation_point tag 与边，以及 ADS 落点投影
  - X-421：节点影响分正式表
  - X-423：影响预测正式表
- **新登记的 decision_needed**：DN-A05-01 / 01b（实时口径 / 供应方频率）、02（创新价值）、03（影响赋分）、04（预测）、05（分类体系）、06（订阅归属）、07（地理落点）、08（载体跳转）、09（投资金额来源）。引用了已有的 DN-01、DN-02，以及 C01 OI-C01-01/05、C02 OI-C02-01/02/16。
- **conflicts 摘要**：
  - 三组指标重复登记：DS_04_ACHIEVE_OVERVIEW_001 与 ACHIEVE_VALUE，REALTIME_004 与 IMPACT_SCORE，REALTIME_005 与 IMPACT_FORECAST。
  - 前端自造 4 个 `M_INNOV_*_RT` metricId，registry 中不存在。
  - 116 在 registry 记为 third_party，但久新没有对应行。
  - 载体跳转方式与 SRS 不一致。
  - 订阅范围与 DS 裁定不一致。

### 4.2 最大 3 个开放项

1. **「实时」口径与源头频率**（DN-A05-01 甲方 / DN-A05-01b 供应方）：SRS 两处写「实时」，源头频率 unknown，我方只能做到 T+1。lumen 现在的 30s 扰动是伪实时，评审前必须换成「数据截至」。
2. **三个 MODEL 算法加落图 Job 没有交付方**（DN-A05-02/03/04，owner human:唐绍祖）：创新价值、影响赋分、影响预测的注册位置都在 demo-algo-science（D12 不可调）；lumen-algo-py 的 vendor/innov-py 是演示版且未挂载。建议与 A02 的 DN-02 合并定案。
3. **数据隔离与图谱前置条件**：gkxlumen-innov 的 InnovSql 把 ads_*/dwd_* 映射到 `demo_gkxlumenx_*`，lumen Java 实际在读 demo 数据仓。落图依赖技术主数据和 VID 迁移（C02 OI-C02-01/16），以及机构主数据（C03 未产出）。

其他开放项：

- 资讯和企业动态的来源，以及 `/internal/tech-news/*` 在 lumen 中的落点，都是 unknown。
- 投资金额的数据源。
- 成果地理坐标的口径（全球精度）。
- 订阅是否与 A06 合并为同一服务。
- 前端 5 处直接 import `@/mock`（违反 IP-13）。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 创新价值、影响赋分、预测、落图都放在 lumen-algo-py 离线 Job；Java 只读 ADS 快照 |
| 2 调用链：前端 → Java → Python /internal | ✅ 所有服务卡都按这个顺序写；前端不直连久新、ES 或 Nebula |
| 3 只用 NebulaGraph | ✅ 图谱读面和落图都在 TRSGraph。vendor/innov-py 的「正式版 Neo4j」方案和 networkx 内存图只写在 risks 里，未采用；GraphController 直读 DWM（R4）不沿用 |
| 4 可观测 | ⚠️ 前端已有 createTraceId 和 `ts-global-innovation-track` 事件，但后端链路不存在，无法贯通；后续实现叶需要补 |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ demo-ui-science 和 demo-algo-science 只作读取对照 |
| 7 共享聚合核心 | ✅ 订阅服务是否与 A06 共用已登记（DN-A05-06）；104/110/114 顶点由专题和展示共用 |
| 8 ADS 先行 + Mock | ✅ 无交付方的指标走 IP-10，显示空态加 ⚠️，不伪造分值；已指出前端直接 import mock 违反 IP-13 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 统计卡都挂了 metric_id，或登记了 metric_missing / algo_owner_missing；已指出前端自造 `_RT` metricId 会导致 ⓘ 查不到 8 件套 |
| 11 D10 | N/A |
| 12 D12 | ⚠️ 发现两处风险，已写入 risks（R-A05-1/2）：① gkxlumen-innov 读 `demo_gkxlumenx_*` 库；② 三个 MODEL 指标的 algo_server_location 指向 demo-algo-science。本方案不调用任何 demo-* 服务 |
| 禁读 registry YAML | ✅ task 和 metric 都只通过 MCP 查询 |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 320000（估算） |
| model_used | claude-opus-5.5 |
| actual_cost | 8.0（USD，估算） |
| cost_warn | green |
