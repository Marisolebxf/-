# SCI-INT-A01 handoff · 科技全域态势 系统集成依赖分析

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A01（spike） |
| 执行 | agent:product-agent（coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（路径沿用旧写法「九新」） |
| ponytail | N/A（分析叶） |
| 日期 | 2026-10-18 |

## 1. 范围与实现

- 范围：SRS `科技发展态势/科技全域态势.md` excel_rows 4–19（P00-baseline leaf=A01，共 16 叶），页面映射 DS-01-MAP / LAYERS / FACTORS / EVENTS。
- 产出 39 张 page 层卡片（`产物/SCI-INT-A01.yaml`），全部采用 `_card-template.yaml` 的字段格式。如果一个叶依赖多种对端能力，就按能力拆卡，拆出的卡共用同一个 `srs.excel_row`。
- 按维度：TAL 3 张 / ORG 3 张 / TECH 4 张 / X 29 张（X 指跨要素或非三要素；其中 12 张的 dimension 含三要素，调用链四段已全部写满）。
- 指标字段来源：algorithm_type 和 d1_d4 全部来自 MCP `user-metric-registry`（metric-get / metric-query）。无指标卡的 `other_system / n/a_ops` 取自 DS-01 映射表的需求分类，不是注册表字段。

### 1.1 重点问题结论

| 问题 | 结论 | 卡 |
|---|---|---|
| 图层数据源配置（第 11 行） | **不是算法**，是取数/接入配置服务：Java 登记图层与数据源的绑定，lumen-etl-es-py 执行拉取，用户填报单独走写回。需新增配置表和填报表（structure_escalation）。「API 接口」类数据源具体对哪个系统未知，不推测为久新 | X-008 / X-009 |
| 要素搜索（第 7 行） | 现状是**前端在已加载样本内做匹配，没有后端检索**；lumen-etl-es-py 只有企业索引。需新建三要素检索索引（科研机构/专家学者/服务机构），链路为 Java 门面 → Python /internal → ES。DS 规定不得映射 seq116 | X-004 |
| 事件重要性分级（第 18 行） | **是算法（MODEL）**：SRS 写明「基于影响力、关注度等指标自动计算等级」，注册表 3 个指标都是 MODEL。05 库和久新都没有覆盖，属无主算法。存量 `vendor/innov-py/innov/event/importance/scorer.py` 会写入 `ads_innovation_event`，但没有挂进 lumen_algo_service；注册表的 algo_server_location 指向 demo-algo-science（D12 风险）；注册表口径限定政策事件，与 SRS 的科创事件范围冲突 | X-034 / X-035 / X-036 |

### 1.2 需久新提供的能力（全部待确认）

| 久新行 | 能力 | 交付形态（B01） | 消费卡 |
|---|---|---|---|
| SRS-96 | 技术基础指标 | SQL（IP-06） | TECH-015、TECH-023，派生 X-028/029/032 |
| SRS-98 | 人才基础指标 | SQL（IP-06） | TAL-016，派生 X-028/029/032 |
| SRS-99 | 科研机构基础指标 | SQL（IP-06） | ORG-017、ORG-022，派生 X-028/029/032 |
| SRS-162 | 人才学术力评估模型 | API（IP-08） | TAL-021 |

合计 4 项。P00 里没有 SRS-116（综合图谱 API）的久新行，JIUXIN 目录也没有任何 DS-01 引用，所以图谱关联（X-020）目前无交付方。

## 2. 偏离说明

- 卡片数为 39，超过叶数 16，原因是按对端能力拆卡（总派单 §2 允许）。
- `gaps` 增加了 `algo_owner_missing:` 前缀，用来区分两种情况：「有 metric_id 但 05 库和久新都不交付」与「统计数字没有任何 metric_id」（后者标 `metric_missing:`）。字段结构没有变。
- 页面派生卡（X-028/029/032）的 `jiuxin_row_id` 为 null，在 downstream 里注明复用哪些父卡。这是 IP-09 的约定，不向久新重复索取。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A01.yaml`（39 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A01-check.py`（自检脚本）
- 本 handoff
- 未 commit、未 push，也没有修改任何业务仓、seed 或矩阵。

## 4. 验收证据

运行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A01-check.py"`，输出如下：

```
scope_count=16 covered_rows=16 diff=[]
cards: 39 {'X': 29, 'TAL': 3, 'ORG': 3, 'TECH': 4}
jiuxin_rows: ['SRS-162', 'SRS-96', 'SRS-98', 'SRS-99']
metric_missing: 2
structure_escalation: 11
patterns: {'IP-01': 12, 'IP-04': 4, 'IP-05': 1, 'IP-06': 5, 'IP-08': 1, 'IP-09': 3, 'IP-10': 5, 'IP-11': 1, 'IP-13': 7}
OK
```

脚本校验的内容：

- P00 中 leaf=A01 的叶共 16 个，等于 scope_count；SRS 行差集为空，且没有超出范围的行。
- 卡片 path 与 P00 一致；int_id 格式正确且不重复。
- integration_pattern 在 IP-01 到 IP-13 之内；jiuxin_row_id 都在 P00 jiuxin_rows 中。
- 含三要素维度的卡，调用链四段都不为空，并且要么有 metric_ids，要么登记了指标缺口。

结论：范围 16 叶，已出卡的 SRS 行 16 个，差集 0。

### 4.1 统计

- metric_missing 2 项：X-033 事件数量与时段分布、X-038 关联强度 score。
- algo_owner_missing 8 张卡：TECH-024、X-025、X-027、X-030、X-031、X-034、X-035、X-036。另有 X-026 的企业影响力 owner 未知，未计入。
- structure_escalation 11 项（升级 human:李伟）：
  - X-004 三要素 ES 索引
  - X-005 要素落点 ADS
  - X-007 图层分组表
  - X-008 数据源登记表
  - X-009 填报表
  - X-014 收藏/标签表
  - TECH-015、TAL-016、ORG-017 三要素基础指标 ADS
  - X-020 Nebula 三要素关系 schema
  - TAL-021 久新 162 结果快照表

### 4.2 最大 3 个开放项

1. **指标双轨**：DS-01 的 M_INNOV_*（自建 STAT/MODEL）与三要素库叶 96/98/99/162（久新 third_party）对应同一批页面数字，ⓘ 绑哪套未定。另外，lumen 前端 ⓘ 目前用的是自造 ID `TS-M1-factor-*`，不在注册表里。
2. **事件重要性分级无主**：这是算法，但没有交付方。存量 scorer 未挂载；注册表实现位置在 demo-algo-science（D12）；口径是政策事件，与 SRS 的科创事件冲突。
3. **契约断层**：前端调用 7 个 `POST /situation/v1/*` 端点，lumen-svc-platform 没有 /situation 实现。已有的 `GET /innov/v1/events/*` 路径和方法都对不上，并且 stats 不支持周/季粒度。BE-TS-CONTRACT-01 未冻结。

其他开放项：

- 「实时」口径与 T+1 链路不一致（X-006、X-036）
- 116 图谱无交付方，且现有 /v1/graph 读 dwm_graph_*（B01 R4）
- 用户填报范围待定
- 事件 NER 抽出的实体与 ORG/TAL 主数据如何对齐（X-038）
- 双 metric_id 待合并：M_INNOV_DS_FACTORS_* / M_INNOV_DS_01_EVENTS_* 与 OPEN 分配的 ID 并存
- M_TALENT_BASE_98_1 的 srs_refs 未包含 DS-01

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 所有 MODEL/GRAPH 卡都落在 lumen-algo-py，Java 只读 ADS |
| 2 调用链：前端 → Java → Python /internal | ✅ call_chain 都按这个顺序写；前端不直连久新、ES 或 Nebula |
| 3 只用 NebulaGraph | ✅ X-020 用 TRSGraph；Java 不写 nGQL |
| 4 可观测 | ⚠️ 现状缺口：前端 trackInteraction 只发 CustomEvent，没有接入 observability 后端（仅记录，本叶不修复） |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ demo-ui-science 只读对照 |
| 7 共享聚合核心 | ✅ 门面落在 gkxlumen-innov，三要素主数据 ID 与专题系统共用（记入风险） |
| 8 ADS 先行 + Mock | ✅ 无源的叶走 IP-10：空态加 ⚠️，USE_MOCK=false 时不伪造数值 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 统计卡都挂了 metric_id，或登记了 metric_missing/缺口；指出前端 ⓘ 用的是自造 ID |
| 11 D10 | N/A |
| 12 D12 | ⚠️ 发现风险，已写入 risks：M_INNOV_SCHOLAR_INFLUENCE、ORG_INFLUENCE、EVENT_IMPORTANCE、DS_01_EVENTS_003 的 algo_server_location 指向 `repos/demo-algo-science`。本方案不调用任何 demo-*，要求在 lumen-algo-py 重写或改用久新能力 |
| 禁读 registry YAML | ✅ task 和 metric 都只通过 MCP 查询 |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 230000（估算） |
| model_used | claude-opus-5.5 |
| actual_cost | 5.8（USD，估算） |
| cost_warn | green |
