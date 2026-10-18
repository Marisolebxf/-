# SCI-INT-A02 handoff：科学技术全景系统集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A02（spike） |
| 执行 | agent:product-agent（coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（旧路径沿用「九新」写法） |
| ponytail | N/A（分析叶） |
| 日期 | 2026-10-18 |

## 1. 范围与实现

- **范围**：SRS `科技发展态势/科学技术全景.md` 的 excel_rows 20–36，对应 P00-baseline 中 leaf=A02 的 17 个叶。页面映射如下：
  - rows 20–24 → DS-02-TECHGRAPH
  - rows 25–30 → DS-02-ENTITY
  - rows 31–36 → DS-02-PATH
  - rows 37–50 属于 A03，本叶不涉及。
- **产出**：`产物/SCI-INT-A02.yaml`，共 22 张 page 层卡片，严格按 `_card-template.yaml` 字段格式。
  - 一个叶依赖多个对端能力时拆成多张卡，例如 row 21 拆成 4 张（130 API、104 实体、105 关系、技术主数据），row 25 和 row 30 各拆 2 张。拆出来的卡共用同一个 `srs.excel_row`。
  - int_id 号段为 101–122。
- **卡片维度分布**：TECH 13 张，X 9 张，TAL 0 张，ORG 0 张。
  - X 卡中有 2 张（X-109 Top5 实体、X-114 实体关系网络）同时带 TECH/TAL/ORG 维度，另有 X-112 实体详情同时带 TAL/ORG/TECH 维度。这些卡的调用链四段都写满了。
  - 其余 6 张 X 卡是纯前端交互，dimension 为 NONE_3E：导入、图交互、实体筛选、用户排序、路径比较、动态演示。
- **字段来源**：algorithm_type 和 d1_d4 全部来自 MCP `user-metric-registry`（metric-get / metric-query）。没有 metric 的卡，按 DS-02-* 映射裁定填 `n/a_ops` 或 `other_system`，d1_d4 填 n/a。

### 1.1 派单关注点结论

| 问题 | 结论 | 卡 |
|---|---|---|
| 图结构怎么生成（row 21） | 由三个对端能力加一份我方主数据组成：<br>① 久新 SRS-104（Python）识别技术实体，并入 lumen-algo-py 后写入 Nebula TRSGraph 顶点。<br>② 久新 SRS-105（Python）抽取关系和关联强度，写入 TRSGraph 边。<br>③ 久新 SRS-130（API）提供全景链结构，由 Python 适配器拉取，凭据只放在 Python 侧，并做熔断、缓存和快照。<br>④ 我方 Python `/internal/v1/sci/tech-graph/*` 读取 Nebula，输出子图和 ADS 投影；Java 只做门面，前端只负责布局和着色。<br>**前置缺口**：没有人持有技术主数据，TRSGraph 中的技术 VID 是 `tech:{名称}`，不稳定（OI-C02-01 P0 / OI-C02-16），需要新建主表、维表和桥表（structure_escalation）。 | TECH-102 / 103 / 104 / 105 |
| 关键路径算法归谁（rows 31–32） | **当前久新侧没有交付行**：05 库没有关键路径叶，130 不含关键节点识别，131 是深圳链，116 禁用。<br>草案建议由我方 Python 在 TRSGraph 上自建（IP-05），结果投影到 ADS。如果改为请久新补行，需要 DN-02 拍板（owner human:唐绍祖）。<br>lumen-algo-py 中现有的 chain `key_link.graph.v1` 是产业链 Job，并且写 demo_* 快照，**不能复用**（D12）。 | TECH-117 / 118 / 120 |
| 哪些交互需要后端 | 以下交互只靠前端：导入、缩放/拖拽、实体筛选、用户排序、路径比较、播放。<br>以下交互需要服务：搜索（需要全库索引）、技术点详情、实体详情、点击节点后按节点懒加载实体、关键路径和关键节点、路径详情。 | 各卡 dep_kind |

### 1.2 需要久新提供的能力（全部待确认）

| 久新行 | 名称 | 交付形态（B01 模式） | 消费卡 |
|---|---|---|---|
| SRS-96 | 技术基础指标模型 | SQL（IP-06） | TECH-110 |
| SRS-104 | 技术实体识别 | Python（IP-07） | TECH-103 |
| SRS-105 | 技术实体关系抽取 | Python（IP-07） | TECH-104、X-109、X-114 |
| SRS-130 | 全景技术链模型 | API（IP-08） | TECH-102 |

合计 4 项。以下 4 项目前没有交付方（algo_owner_missing 或无源），在 DN-02 定案前都没有 owner：影响力（TECH-115）、关键路径（TECH-117）、中心性/关键节点（TECH-118）、路径详情文案（TECH-119）。

## 2. 偏离说明

- 卡片数为 22，SRS 叶数为 17。差异来自按对端能力拆卡，拆卡规则见总派单 §2。
- 在 gaps 中沿用 A01 的约定：`algo_owner_missing:` 表示已有 metric_id，但 05 库和久新都没有交付方；`metric_missing:` 表示页面上的统计数字没有任何注册的 metric_id。卡片字段结构没有改动。
- TECH-111（节点点击）在 DS 映射中被判为 n/a_ops。我判定它需要服务，理由是：接入真实数据后，全图实体无法一次放进 graph 响应，必须按节点懒加载。依据已写入该卡 gaps，供评审确认。
- JIUXIN 清单对 105 的备注是「展示消费为 DS-03」，与 DS-02-TECHGRAPH TG-D03 判定本页 mapped 105 不一致。我只记录了这个差异，没有改动任何映射。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A02.yaml`（22 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A02-check.py`（自检脚本）
- 本 handoff
- 没有 commit 或 push，也没有改动任何业务仓、seed 或矩阵文件。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A02-check.py"`，输出如下：

```
scope_count=17 covered_rows=17 diff=[]
cards: 22 {'X': 9, 'TECH': 13}
jiuxin_rows: ['SRS-104', 'SRS-105', 'SRS-130', 'SRS-96']
metric_missing: 2
algo_owner_missing: 3
structure_escalation: 6
patterns: {'IP-01': 3, 'IP-05': 4, 'IP-06': 1, 'IP-07': 2, 'IP-08': 1, 'IP-09': 9, 'IP-10': 1, 'IP-13': 1}
OK
```

脚本校验了以下内容：

- P00 中 leaf=A02 的叶恰好是 rows 20–36，共 17 个，与 scope_count 一致；SRS 差集为空，没有超出范围的行。
- 每张卡的 path 与 P00 一致，page_ref 按行段对应正确，int_id 符合 `INT-A-*-1xx` 格式且不重复。
- integration_pattern 都在 IP-01 到 IP-13 之间；jiuxin_row_id 都在 P00 的 jiuxin_rows 中。
- 带三要素维度的卡，调用链四段都不为空，并且满足以下之一：有 metric_ids、登记了 metric_missing、或属于 other_system / n/a_ops。非三要素的卡都是 X 卡且 dimension 为 NONE_3E。

**结论：范围 17 叶，有卡片覆盖的 SRS 行 17 行，差集 0。**

### 4.1 统计

- **metric_missing 2 张**：X-112（实体详情中的「统计数据」）、TECH-117（路径「重要性」字段）。
- **algo_owner_missing 3 张**：TECH-115 影响力、TECH-118 中心性/关键节点、TECH-120 重要性等级。另有 TECH-117（关键路径）和 TECH-119（路径详情）没有 metric，但同样没有交付方。
- **structure_escalation 6 张**（升级给 human:李伟）：
  - TECH-105：技术主表、领域维表、桥表，以及稳定的 VID。
  - TECH-107：技术点 ES 索引或主表检索。
  - TECH-115：影响力结果表。
  - TECH-117：关键路径结果表。
  - TECH-118：节点中心性结果表，不复用 innov 的 ads_node_influence。
  - TECH-119：路径详情表。
- **新登记的 decision_needed**：DN-A02-01 到 05，分别是导入是否持久化、「发展状态」的口径、实体详情统计项、关键路径的定义、路径详情的来源。另外引用了已有的 DN-02、DN-06、Q-MO-DS02-01/02/03。

### 4.2 最大 3 个开放项

1. **关键路径、中心性、影响力都没有算法主**（DN-02，owner human:唐绍祖）。DS-02-PATH 和 ENTITY 判定为 missing，久新没有对应行，展示侧的路径 Job「501 未注册」。草案建议我方 Python 在 Nebula 上自建。同时，注册表里同一概念登记了两个 ID：M_TECH_PATH_* / M_TECH_ENTITY_INFLUENCE 标为 third_party，M_INNOV_DS_02_PATH_00x 标为 GRAPH，M_ENT_DS_02_ENTITY_004 标为 MODEL 且挂在 ENT 域。类型和域都需要 data-agent 合并。
2. **技术主数据和 VID 是整张图的前置条件**（OI-C02-01 P0 / OI-C02-16）。104/105 写入 TRSGraph 时用 `tech:{名称}` 作为 VID，不稳定；分类体系（OI-C02-02）未定，层级着色、搜索和详情都会被卡住。
3. **契约断层**：前端只调用一个 `POST /situation/v1/panorama/graph`，lumen-svc-platform 没有 /situation 实现，lumen-algo-py 没有 sci 路由，BE-TS-CONTRACT-01 未冻结。全景页没有 ⓘ / MockBadge，也没有 src/review 评审层，不满足 D9。

其他开放项：

- 104/105 是否覆盖人才、机构、论文、专利四类实体，以及边是否带时间（影响时间轴回放）。
- 96 与 M_TECH_PAPER_PATENT_CNT 口径重叠（DN-06）。
- M_TECH_GRAPH_104_1 的 srs_refs 没有包含本页 seq 18。
- 105 的展示消费方是 DS-02 还是 DS-03 不一致。
- 130 的结果由专题和展示共用，谁来写入（B01 C3）。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 实体识别、关系抽取、关键路径、中心性、影响力都放在 lumen-algo-py；Java 只读 ADS。「前端自算路径」只写在 risks 里，未采用 |
| 2 调用链：前端 → Java → Python /internal | ✅ 所有服务卡都按这个顺序写；前端不直连久新、ES 或 Nebula；久新凭据只放在 Python 侧 |
| 3 只用 NebulaGraph | ✅ 图都在 TRSGraph；Java 不写 nGQL；记录了 innov GraphController 直读 DWM 的问题（B01 R4），新方案不照搬 |
| 4 可观测 | ⚠️ 前端已有 trackInteraction / createTraceId，但没有后端链路可以贯通；各服务卡的 test_points 都要求 trace 贯通 |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ demo-ui-science 只作读取对照 |
| 7 共享聚合核心 | ✅ 130、104、105 的结果由专题和展示共用，写入方待 B01 C3 决定（已记入 conflicts） |
| 8 ADS 先行 + Mock | ✅ 没有来源的路径详情走 IP-10，显示空态加 ⚠️；USE_MOCK=false 时禁止用 fixture 填数 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 统计卡都挂了 metric_id，或登记了 metric_missing / algo_owner_missing；已指出全景页缺 ⓘ / MockBadge |
| 11 D10 | N/A（交互卡的 test_points 包含键盘可达） |
| 12 D12 | ⚠️ 发现风险并写入 TECH-117 的 risks：lumen-algo-py chain 的 panorama / key_link Job 写 demo_* 快照，禁止复用到技术点关键路径。本方案不调用任何 demo-* 服务 |
| 禁读 registry YAML | ✅ task 和 metric 都只通过 MCP 查询 |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 300000（估算） |
| model_used | claude-opus-5.5 |
| actual_cost | 7.5（USD，估算） |
| cost_warn | green |
