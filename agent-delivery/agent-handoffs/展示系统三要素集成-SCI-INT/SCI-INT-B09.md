# SCI-INT-B09 handoff：机构基础 / 图谱 / 派生 / 统计（15）

ponytail: N/A（spike 分析，无代码）

| 项 | 值 |
|---|---|
| task_id | SCI-INT-B09（spike） |
| 执行 | agent:algorithm-agent |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新；图谱两条对端含 TRSGraph |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：总派单 §4 B09 的 15 条 `M_ORG_*`（含 `M_ORG_TECH_SCORE`）。每条一卡，`layer=metric`，号段 `INT-B-ORG-800` … `INT-B-ORG-814`。
- **产出**：`产物/SCI-INT-B09.yaml`。模式取包内 `b01.pattern`，`algorithm_type` 保持包内值（14 条 `third_party`，`M_ORG_PERF_QUERY` 为 `STAT`）。
- **拆分**：基础 1 条 IP-06，图谱库叶 2 条 IP-07，页面派生 10 条 IP-09，技术力 1 条 IP-08，绩效查询 1 条 IP-01。有久新行的不标 IP-10。绩效查询无久新行，仍保持 IP-01。
- **页面**：只用包内 `srs_refs_02` 与 `a_cards`。基础挂 `DS-01-FACTORS`，实体识别挂 `DS-04-REALTIME`，其余 13 条写「未挂页」。
- **主数据**：机构只引用 C03 `INT-C-ORG-240`（`dim_research_org`）。没有 `org_uid`。不另造第二张主表。别名引用 `INT-C-ORG-241`，文献桥引用 `INT-C-ORG-242`。
- **深度模型**：149–155 归 B08。本叶 IP-09 只写母指标，不重写 `M_ORG_DEEP_*` 卡。SRS-150 本叶不挂。
- **实现位置**：包内落点是 GDF、`lumen-etl-es-py`、`lumen-algo-py`，没有指向 `demo-*`。D12 写在每张卡上：正式实现禁止 lumen 调用任何 `demo-*`。

### 1.1 久新依赖

本叶不新增久新行号。库叶消费 3 行；6 条 IP-09 读 B08 父快照，不单独再要；4 条 IP-09 读本叶 SRS-99。`TOPIC-RORG-012` 是无专叶项。绩效查询无久新行。

| 久新行 | 角色 | 交付 | 确认 | 消费卡 |
|---|---|---|---|---|
| SRS-99 | 机构基础库叶；关注度、覆盖、新增、现状的母指标 | SQL | 待确认 | INT-B-ORG-800、803、807、808、811 |
| SRS-114 | 机构实体识别库叶 | Python | 待确认 | INT-B-ORG-801 |
| SRS-115 | 机构关系抽取库叶 | Python | 待确认 | INT-B-ORG-802 |
| SRS-149 | 布局母指标，卡在 B08 | API | 待确认 | INT-B-ORG-812（只读，不重写） |
| SRS-151 | 深圳优势母指标，卡在 B08 | API | 待确认 | INT-B-ORG-809 |
| SRS-152 | 痛难点母指标，卡在 B08 | API | 待确认 | INT-B-ORG-810 |
| SRS-153 | 合作链母指标，卡在 B08 | API | 待确认 | INT-B-ORG-805 |
| SRS-154 | 招引母指标，卡在 B08 | API | 待确认 | INT-B-ORG-804 |
| SRS-155 | 扶持母指标，卡在 B08 | API | 待确认 | INT-B-ORG-806 |
| TOPIC-RORG-012 | 技术力，05 无专叶 | API | 待确认 | INT-B-ORG-813 |

无久新行（IP-01，不是 IP-10）：INT-B-ORG-814 `M_ORG_PERF_QUERY`。

### 1.2 派生母指标

| 卡 | 指标 | 母指标 | seq | 归属 |
|---|---|---|---|---|
| 803 | M_ORG_ATTENTION_TREND | M_ORG_BASE_99_1 | 99 | 本叶 |
| 804 | M_ORG_ATTRACT_SCORE | M_ORG_DEEP_154_1 | 154 | B08 |
| 805 | M_ORG_COLLAB_CHAIN | M_ORG_DEEP_153_1 | 153 | B08 |
| 806 | M_ORG_CULTIVATE_SCORE | M_ORG_DEEP_155_1 | 155 | B08 |
| 807 | M_ORG_INDUSTRY_COVER | M_ORG_BASE_99_1 | 99 | 本叶 |
| 808 | M_ORG_NEW_TREND | M_ORG_BASE_99_1 | 99 | 本叶 |
| 809 | M_ORG_SZ_ADVANTAGE | M_ORG_DEEP_151_1 | 151 | B08 |
| 810 | M_ORG_SZ_PAINPOINT | M_ORG_DEEP_152_1 | 152 | B08 |
| 811 | M_ORG_SZ_STATUS | M_ORG_BASE_99_1 | 99 | 本叶 |
| 812 | M_ORG_TECH_LAYOUT | M_ORG_DEEP_149_1 | 149 | B08 |

基础、两张图谱库叶、技术力、绩效查询的 `parent_metric` 为空。

### 1.3 同步 / 异步

请求路径计：IP-06、IP-09、IP-01 是同步读 ADS 或父快照；IP-07 抽取 Job 与 IP-08 页面读快照是异步。

| 方式 | 条数 | 卡 |
|---|---|---|
| 同步 | 12 | INT-B-ORG-800、803、804、805、806、807、808、809、810、811、812、814 |
| 异步 | 3 | INT-B-ORG-801、802、813 |

### 1.4 技术力如何挂接

`M_ORG_TECH_SCORE` 对上 `TOPIC-RORG-012`（`row_kind=无专叶项`），模式 IP-08，卡 `INT-B-ORG-813`。05 没有专叶，公式不展开，用户加权。适配层草案 `POST /internal/org/tech-score`，页面只读 `ads_sci_result_snapshot`（引用 SE-B02-01，不另造）。

conflicts 写明：禁止用 `M_SVC_ORG_TECH_SCORE` 顶替，本卡未改挂。`algorithm_type` 保持 `third_party`。`svcan /org/tech-score` 同名，口径未确认（C9）。久新行 `page_id=TOPIC-ORG-05` 不在 `a_cards`，使用页面写「未挂页」。

## 2. 偏离说明

- 卡片数 = 指标数 = 15，差集空。未按页面再拆卡。
- 久新行上的 STAT / GRAPH / MODEL 与 `third_party` 的差异写在 `conflicts`，原值未改。绩效查询保持 `STAT`。
- 无久新行的绩效查询保持包内 IP-01，不改标 IP-10。
- 深度模型 149–155 不在本叶重写。IP-09 只读父快照。
- C 卡把入站写成离线 ETL。本叶不因此改模式编号。
- Q084、Q085、Q086、Q087、Q089、Q090、Q091、Q092、Q104 只登记，不代甲方裁口径。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-B09.yaml`（15 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B09-check.py`
- 本 handoff
- 没有 commit，没有 push，没有改业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B09-check.py"`，脚本打印 OK：

```
cards=15 expect=15 gap=[]
int_ids=800-814 unique=15
sync=12 async=3
jiuxin_rows: ['SRS-99', 'SRS-114', 'SRS-115', 'SRS-154', 'SRS-153', 'SRS-155', 'SRS-151', 'SRS-152', 'SRS-149', 'TOPIC-RORG-012']
structure_escalation: ['SE-B09-01']
structure_escalation_refs: ['INT-C-ORG-240', 'INT-C-ORG-241', 'INT-C-ORG-242', 'SE-B02-01']
OK
```

脚本核对：包内 15 个 metric_id 全覆盖且顺序一致、差集为空、卡号 800–814、无占位符 TBD、模式与 `algorithm_type` 与久新行均等于包内 `b01`、有久新行的卡不是 IP-10、IP-09 都有母指标、页面集合等于包内 `srs_refs_02` 与 `a_cards`、技术力对上 `TOPIC-RORG-012` 且 conflicts 含 `M_SVC_ORG_TECH_SCORE`、绩效查询为 STAT / IP-01、未重写 B08 深度模型、未另造机构主表。

**结论：15 张卡，差集 0。自检 OK，差集 0。**

### 4.1 结构升级

| id | 负责人 | 新表 | 范围 |
|---|---|---|---|
| SE-B09-01 | human:李伟 | `ads_org_perf_query`（包内表名未定，暂用此名） | INT-B-ORG-814。绩效查询聚合，不替代机构主数据 |
| INT-C-ORG-240（引用，不新开） | human:李伟 | `dim_research_org` | 不另造第二张主表。没有 org_uid |
| INT-C-ORG-241（引用，不新开） | human:李伟 | `map_org_alias` | 不另造第二张别名表 |
| INT-C-ORG-242（引用，不新开） | human:李伟 | `rel_doc_org` | 不另造第二张桥 |
| SE-B02-01（引用，不新开） | human:李伟 | `ads_sci_result_snapshot`、`ads_sci_jiuxin_adapter_cache` | 技术力与读 B08 父模型的派生共用，不另造 |

### 4.2 最大 3 个开放项

1. **库叶交付未确认**（OI-B09-01）：SRS-99 的 SQL、SRS-114/115 的 Python 仍是「待确认」。IP-09 不另要 149/151/152/153/154/155 接口。深度模型卡归 B08。
2. **技术力无专叶**（OI-B09-02）：对上 `TOPIC-RORG-012`。禁止用 `M_SVC_ORG_TECH_SCORE` 顶替。公式不展开。
3. **新投影表升李伟**（OI-B09-03）：`ads_org_perf_query`（SE-B09-01）。机构主数据只引用 INT-C-ORG-240，没有 `org_uid`。

类型冲突留在卡片 `conflicts`，不在本叶改 `algorithm_type`。决策项只登记，不代甲方裁口径。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ IP-07 抽取与 IP-08 适配在 lumen-algo-py；IP-06 / IP-01 的 SQL 落 GDF；IP-09 由 Java 读父快照，不算公式 |
| 2 调用链：前端 → Java → Python /internal | ✅ 在线读不直连久新；子图只 Feign `/internal/graph/*`；Java 不写 nGQL |
| 3 只用 NebulaGraph | ✅ 实体与关系写 TRSGraph（graphd 10.50.75.136:9669）；未采用 Neo4j；不新开 space |
| 4 可观测 | N/A（spike 分析，无代码） |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 | ✅ 派生与父库叶共一份快照；技术力与 B08 父模型共用 SE-B02-01 |
| 8 ADS 先行 + Mock | ✅ D1=draft、D4=mock 只记现状；无快照即空态，禁止 Mock 兜底 |
| 9 D8 | N/A |
| 10 D9 | ✅ 每卡绑定包内 metric_id，未把状态改绿，未读 metrics/registry |
| 11 D10 | N/A |
| 12 D12 | ✅ 包内实现位置是 lumen-algo-py / lumen-etl-es-py / GDF，不是 demo-*。每张卡写明禁止 lumen 调用 demo-* |
| 业务口径不替甲方拍板 | ✅ Q 项与久新「待确认」只登记；技术力替身只写 conflicts，不改挂 |
| 只读 | ✅ 未连库，未 commit，未读 task-registry.yaml |

## 6. cost

价表无 grok 行。按 algorithm 默认比例 75/25，用旗舰档 Opus 4.7 单价（输入 $15/M、输出 $75/M）作上界。`source: estimate`。

`actual_cost = 200000×0.75×15/1e6 + 200000×0.25×75/1e6 = 6.00`

| 字段 | 值 |
|---|---|
| actual_tokens | 200000 |
| model_used | grok-4.7 |
| actual_cost | 6.00 |
| cost_warn | yellow |

未超过 $10，不暂停。yellow 按预算规则知会 PM。
