# SCI-INT-B06 handoff：技术基础 / 图谱 / 路径派生（12）

| 项 | 值 |
|---|---|
| task_id | SCI-INT-B06（spike） |
| 执行 | agent:algorithm-agent |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新；图自建四条对端为 TRSGraph |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：总派单 §4 B06 的 12 条 `M_TECH_*`。每条一卡，`layer=metric`，号段 `INT-B-TECH-500` … `INT-B-TECH-511`。
- **产出**：`产物/SCI-INT-B06.yaml`。模式取包内 `b01.pattern`，`algorithm_type` 保持 `third_party`。
- **拆分**：基础 1 条 IP-06，图谱库叶 2 条 IP-07，页面派生 5 条 IP-09，图自建 4 条 IP-05。有久新行的不标 IP-10。
- **页面**：只用包内 `srs_refs_02` 与 `a_cards`。12 条都有挂页，没有「未挂页」。
- **主数据**：技术点实体只引用 C02 `INT-C-TECH-180`，不另造第二张技术点主表。桥接只引用 `INT-C-TECH-182`。
- **实现位置**：包内落点是 GDF、`lumen-etl-es-py`、`lumen-algo-py`，没有指向 `demo-*`。D12 写在每张卡上：正式实现禁止 lumen 调用任何 `demo-*`。

### 1.1 久新依赖

本叶不新增久新行号。库叶消费 3 行；5 条 IP-09 读父快照，不单独再要接口。4 条 IP-05 无久新行。

| 久新行 | 角色 | 交付 | 确认 | 消费卡 |
|---|---|---|---|---|
| SRS-96 | 技术基础库叶 | SQL | 待确认 | INT-B-TECH-500 |
| SRS-104 | 技术实体识别库叶，也是网图结构的母指标 | Python | 待确认 | INT-B-TECH-501、507 |
| SRS-105 | 技术关系抽取库叶；边权、关系网、Top5、弦线粗细的母指标 | Python | 待确认 | INT-B-TECH-502、503、505、506、511 |

无久新行（IP-05，不是 IP-10）：INT-B-TECH-504 影响力，508 中心度，509 关键节点，510 优先级。

### 1.2 派生母指标

| 卡 | 指标 | 母指标 | seq | 读取字段 |
|---|---|---|---|---|
| 503 | M_TECH_EDGE_STRENGTH | M_TECH_GRAPH_105_1 | 105 | 技术–技术边权 |
| 505 | M_TECH_ENTITY_REL | M_TECH_GRAPH_105_1 | 105 | 实体关联边、关联对象 |
| 506 | M_TECH_ENTITY_TOP5 | M_TECH_GRAPH_105_1 | 105 | 实体名称、实体类型、关联强度 |
| 507 | M_TECH_GRAPH_STRUCT | M_TECH_GRAPH_104_1 | 104 | 技术点实体集（边来自 105，主挂仍是 104） |
| 511 | M_TECH_REL_STRENGTH | M_TECH_GRAPH_105_1 | 105 | 技术–技术边权（弦线图线粗） |

基础、两张图谱库叶、四条 IP-05 的 `parent_metric` 为空。

### 1.3 同步 / 异步

请求路径计：IP-06 与 IP-09 是同步读 ADS 或父快照；IP-07 抽取 Job 与 IP-05 图批算是异步。页面读投影不另记一条。

| 方式 | 条数 | 卡 |
|---|---|---|
| 同步 | 6 | INT-B-TECH-500、503、505、506、507、511 |
| 异步 | 6 | INT-B-TECH-501、502、504、508、509、510 |

### 1.4 中心度三条建议

建议改由我方 Python 与 Nebula 计算。`M_TECH_PATH_CENTRALITY`、`M_TECH_PATH_KEYNODE`、`M_TECH_PATH_PRIORITY` 用同一条 `lumen-algo-py` 批 Job，在 TRSGraph（graphd `10.50.75.136:9669`）上算完，写入投影 `ads_tech_graph_node_metric`（SE-B06-01）。不向久新新要行，不改挂 seq 116，不用 `M_SVC_GRAPH_*`，不用 `M_CHAIN_KEY_NODE_COUNT`。

`algorithm_type` 保持 `third_party`，建议只写在 `conflicts`。负责人未定（DN-02，唐绍祖），本条不是定论。同族 `M_TECH_ENTITY_INFLUENCE` 建议并入同一 Job，注册值同样不改。

TAG technology 尚未建（C04 `INT-C-TECH-300`），且没有 `technology_id`（C02 `INT-C-TECH-180`）。这两件未落地之前 Job 不跑，页面空态。

## 2. 偏离说明

- 卡片数 = 指标数 = 12，差集空。未按页面再拆卡。
- 久新行上的 STAT / GRAPH 与 `third_party` 的差异写在 `conflicts`，原值未改。
- 四条无久新行的指标保持包内 IP-05，不改标 IP-10。
- `M_TECH_PATH_PRIORITY` 的页面卡写成 IP-09，`M_TECH_GRAPH_STRUCT` 的页面卡写成 IP-08 / IP-05。模式保持包内 `b01.pattern`。
- 网图结构主挂 SRS-104。边输入来自 SRS-105，不因此改久新行号。
- C 卡把入站写成离线 ETL。本叶不因此改模式编号。
- Q126 只登记在弦线强度卡上，不代甲方裁口径。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-B06.yaml`（12 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B06-check.py`
- 本 handoff
- 没有 commit，没有 push，没有改业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B06-check.py"`，退出码 0：

```
cards=12 expect=12 gap=[]
int_ids=500-511 unique=12
sync=6 async=6
jiuxin_rows: ['SRS-96', 'SRS-104', 'SRS-105']
structure_escalation: ['SE-B06-01']
structure_escalation_refs: ['INT-C-TECH-180', 'INT-C-TECH-182', 'INT-C-TECH-300']
OK
```

脚本核对：包内 12 个 metric_id 全覆盖且顺序一致、差集为空、卡号 500–511、无占位符 TBD、模式与 `algorithm_type` 与久新行均等于包内 `b01`、有久新行的卡不是 IP-10、IP-09 都有母指标 seq 与字段、页面集合等于包内 `srs_refs_02` 与 `a_cards`、中心度三条的 conflicts 含自建建议且注册值仍为 `third_party`、未另造技术点主表。

**结论：12 张卡，差集 0。自检 OK，差集 0。**

### 4.1 结构升级

| id | 负责人 | 新表 | 范围 |
|---|---|---|---|
| SE-B06-01 | human:李伟 | `ads_tech_graph_node_metric`（包内表名未定，暂用此名） | INT-B-TECH-504、508、509、510。中心度 / 关键节点 / 优先级 / 影响力投影 |
| INT-C-TECH-180（引用，不新开） | human:李伟 | C02 技术点主数据 | 不另造第二张主表 |
| INT-C-TECH-182（引用，不新开） | human:李伟 | C02 桥接 | 不另造第二张桥 |
| INT-C-TECH-300（引用，不新开） | human:李伟 | C04 TAG technology | Tag 尚未建，本叶不新造 |

### 4.2 最大 3 个开放项

1. **库叶交付未确认**（OI-B06-01）：SRS-96 的 SQL、SRS-104/105 的 Python 仍是「待确认」。IP-09 不另要接口。
2. **中心度三条是否改由我方计算**（OI-B06-02）：建议是。负责人 DN-02 唐绍祖未定。`algorithm_type` 保持 `third_party`。
3. **新投影表升李伟**（OI-B06-03）：`ads_tech_graph_node_metric`（SE-B06-01）。技术点主数据只引用 INT-C-TECH-180。C02 无 technology_id，C04 TAG technology 尚未建，图未建则相关卡空态。

类型冲突留在卡片 `conflicts`，不在本叶改 `algorithm_type`。Q126 只登记，不代甲方裁口径。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ IP-07 抽取与 IP-05 批算在 lumen-algo-py；IP-06 的 SQL 落 GDF；IP-09 由 Java 读父快照，不算公式 |
| 2 调用链：前端 → Java → Python /internal | ✅ 在线读不直连久新；子图只 Feign `/internal/graph/*`；Java 不写 nGQL |
| 3 只用 NebulaGraph | ✅ 中心度建议写 TRSGraph（graphd 10.50.75.136:9669）；未采用 Neo4j；Tag 未建前不跑 Job |
| 4 可观测 | N/A（spike 分析，无代码） |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 | ✅ 派生与父库叶共一份快照；中心度三条共一条 Job、一张投影 |
| 8 ADS 先行 + Mock | ✅ D1=draft、D4=mock 只记现状；无快照即空态，禁止 Mock 兜底 |
| 9 D8 | N/A |
| 10 D9 | ✅ 每卡绑定包内 metric_id，未把状态改绿，未读 metrics/registry |
| 11 D10 | N/A |
| 12 D12 | ✅ 包内实现位置是 lumen-algo-py / lumen-etl-es-py / GDF，不是 demo-*。每张卡写明禁止 lumen 调用 demo-* |
| 业务口径不替甲方拍板 | ✅ Q126、DN-02 与久新「待确认」只登记；自建建议不改注册值 |
| 只读 | ✅ 未连库，未 commit，未读 task-registry.yaml |

## 6. cost

价表无 grok 行。按 algorithm 默认比例 75/25，用旗舰档 Opus 4.7 单价（输入 $15/M、输出 $75/M）作上界。`source: estimate`。

`actual_cost = 180000×0.75×15/1e6 + 180000×0.25×75/1e6 = 5.40`

| 字段 | 值 |
|---|---|
| actual_tokens | 180000 |
| model_used | grok-4.7 |
| actual_cost | 5.40 |
| cost_warn | yellow |

未超过 $10，不暂停。yellow 按预算规则知会 PM。
