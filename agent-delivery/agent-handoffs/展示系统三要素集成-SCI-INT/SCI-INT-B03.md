# SCI-INT-B03 handoff：人才基础 / 图谱 / 页面派生（15）

| 项 | 值 |
|---|---|
| task_id | SCI-INT-B03（spike） |
| 执行 | agent:algorithm-agent |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新 |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：总派单 B03 的 15 条 `M_TALENT_*`。每条一卡，`layer=metric`，号段 `INT-B-TAL-200` … `INT-B-TAL-214`。
- **产出**：`产物/SCI-INT-B03.yaml`。模式取包内 `b01.pattern`，`algorithm_type` 保持 `third_party`。
- **拆分**：基础 1 条 IP-06，图谱 2 条 IP-07，页面派生 12 条 IP-09。派生卡写明母指标 `seq` 与口径字段。
- **页面**：只用包内 `srs_refs_02` 与 `a_cards`。有挂页 3 条（基础、实体识别、关系抽取）。其余 12 条写「未挂页」。
- **流动**：`M_TALENT_FLOW_TRACK` 若用边表，只引用 B02 已升级的 `dwd_talent_flow`（SE-B02-02），不另造第二张流动边表。
- **实现位置**：包内落点是 GDF、`lumen-etl-es-py`、`lumen-algo-py`，没有指向 `demo-*`。D12 风险写在每张卡上：正式实现禁止 lumen 调用任何 `demo-*`。

### 1.1 久新依赖

本叶不新增久新行号。库叶消费 3 行；12 条派生读父快照，不单独再要接口。

| 久新行 | 角色 | 交付 | 确认 | 消费卡 |
|---|---|---|---|---|
| SRS-98 | 基础库叶，也是机构分布 / 区域分布 / 供给的母指标 | SQL | 待确认 | INT-B-TAL-200、208、209、211 |
| SRS-110 | 实体识别库叶 | Python | 待确认 | INT-B-TAL-201 |
| SRS-111 | 关系抽取库叶 | Python | 待确认 | INT-B-TAL-202 |
| SRS-157 | 流动的母库叶，本卡不另要 | API（父） | 待确认 | INT-B-TAL-207 只读 |
| SRS-158 | 高校新培育的母库叶 | API（父） | 待确认 | INT-B-TAL-214 只读 |
| SRS-159 | 深圳现状的母库叶 | API（父） | 待确认 | INT-B-TAL-212 只读 |
| SRS-160 | 关系链的母库叶 | API（父） | 待确认 | INT-B-TAL-210 只读 |
| SRS-161 | 供需评价的母库叶 | API（父） | 待确认 | INT-B-TAL-213 只读 |
| SRS-162 | 学术力的母库叶 | API（父） | 待确认 | INT-B-TAL-203 只读 |
| SRS-163 | 产业力的母库叶 | API（父） | 待确认 | INT-B-TAL-206 只读 |
| SRS-164 | 引入推荐的母库叶 | API（父） | 待确认 | INT-B-TAL-204 只读 |
| SRS-165 | 培育推荐的母库叶 | API（父） | 待确认 | INT-B-TAL-205 只读 |

### 1.2 派生母指标

| 卡 | 指标 | 母指标 | seq | 读取字段 |
|---|---|---|---|---|
| 203 | M_TALENT_ACADEMIC_SCORE | M_TALENT_DEEP_162_1 | 162 | 成果数量、学术影响力、专业技能 |
| 204 | M_TALENT_ATTRACT_SCORE | M_TALENT_DEEP_164_1 | 164 | 综合推荐分、名单规模 |
| 205 | M_TALENT_CULTIVATE_SCORE | M_TALENT_DEEP_165_1 | 165 | 综合培育推荐分、建议名单规模、培育方向文本 |
| 206 | M_TALENT_INDUSTRY_SCORE | M_TALENT_DEEP_163_1 | 163 | 专利转化、项目、商业化、综合评分、排名 |
| 207 | M_TALENT_FLOW_TRACK | M_TALENT_DEEP_157_1 | 157 | 流入、流出、留存、自然年 |
| 208 | M_TALENT_ORG_DIST | M_TALENT_BASE_98_1 | 98 | 机构类型、所属机构、人才数量、占比 |
| 209 | M_TALENT_REGIONAL_DIST | M_TALENT_BASE_98_1 | 98 | 地理单元、人才计数 |
| 210 | M_TALENT_RELATION_NET | M_TALENT_DEEP_160_1 | 160 | 节点规模、边规模 |
| 211 | M_TALENT_SUPPLY_STRUCT | M_TALENT_BASE_98_1 | 98 | 学士 / 硕士 / 博士毕业数量、存量学历 |
| 212 | M_TALENT_SZ_STATUS | M_TALENT_DEEP_159_1 | 159 | 计数、优劣势、短板 |
| 213 | M_TALENT_SZ_SUPPLY_DEMAND | M_TALENT_DEEP_161_1 | 161 | 供需评价指数、缺口或盈余、趋势 |
| 214 | M_TALENT_UNIV_NEW | M_TALENT_DEEP_158_1 | 158 | 新增培养识别、培养趋势、学科或技术方向、校际对比 |

基础与两张图谱是库叶，`parent_metric` 为空。

### 1.3 同步 / 异步

请求路径计：IP-06 与 IP-09 是同步读 ADS 或父快照；IP-07 抽取 Job 是异步。生产侧 T+1 或 weekly 不把读请求改记成异步 Job。

| 方式 | 条数 | 卡 |
|---|---|---|
| 同步 | 13 | INT-B-TAL-200，INT-B-TAL-203 … 214 |
| 异步 | 2 | INT-B-TAL-201、INT-B-TAL-202 |

## 2. 偏离说明

- 卡片数 = 指标数 = 15，差集空。未按页面再拆卡。
- 久新行上的 STAT / GRAPH / MODEL 与 `third_party` 的差异写在 `conflicts`，原值未改。
- 机构分布、区域分布、供给的备注写「派生走 IP-01」。模式保持包内 IP-09。
- 引入推荐的备注写 G3 Job。模式保持 IP-09，Job 留在父指标 `M_TALENT_DEEP_164_1`，本卡不另起。
- 基础指标备注称 srs_refs 15 条并含 TOPIC-TALENT-05。包内 `srs_refs_02` 只有 8 条。页面只按包内清单。
- 流动定义写可与 DS-14 同源但不改挂。包内无页面引用，写未挂页。
- 引入推荐定义写可与 DS-16 复用。包内无 `srs_refs_02`、无 `a_cards`，不补挂。
- C 卡把入站写成离线 ETL。本叶不因此改模式编号。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-B03.yaml`（15 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B03-check.py`
- 本 handoff
- 没有 commit，没有 push，没有改业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B03-check.py"`，退出码 0：

```
cards=15 expect=15 gap=[]
int_ids=200-214 unique=15
sync=13 async=2
jiuxin_rows: ['SRS-98', 'SRS-110', 'SRS-111', 'SRS-157', 'SRS-158', 'SRS-159', 'SRS-160', 'SRS-161', 'SRS-162', 'SRS-163', 'SRS-164', 'SRS-165']
structure_escalation: ['SE-B03-01', 'SE-B03-02']
structure_escalation_refs: ['SE-B02-02']
OK
```

脚本核对：包内 15 个 metric_id 全覆盖且顺序一致、差集为空、卡号在 200–299、无占位符 TBD、模式与 `algorithm_type` 与久新行均等于包内 `b01`、IP-09 都有母指标 seq 与字段且页面为未挂页、流动卡引用 SE-B02-02 且未另造流动边表。

**结论：15 张卡，差集 0。**

### 4.1 结构升级

| id | 负责人 | 新表 | 范围 |
|---|---|---|---|
| SE-B03-01 | human:李伟 | `dwd_talent_master`（包内表名未定，暂用此名，不替代 `dwd_scholar`） | INT-B-TAL-200。ADS 落表名未给，本叶不另起表名 |
| SE-B03-02 | human:李伟 | `dwd_person_id_map`（包内表名未定，暂用此名） | INT-B-TAL-201 |
| SE-B02-02（引用，不新开） | human:李伟 | `dwd_talent_flow` | INT-B-TAL-207 |

### 4.2 最大 3 个开放项

1. **库叶交付未确认**（OI-B03-01）：SRS-98 的 SQL、SRS-110/111 的 Python 仍是「待确认」。IP-09 不另要 SRS-157…165 的接口。
2. **12 条页面派生未挂页**（OI-B03-02）：`srs_refs_02` 与 `a_cards` 都空。需要确认是否只服务专题 `SRS-TALENT`。定义里提到的 DS-14、DS-16 本叶不补挂。
3. **两张新表升李伟**（OI-B03-03）：`dwd_talent_master`（SE-B03-01）、`dwd_person_id_map`（SE-B03-02）。流动只引用 SE-B02-02。

类型冲突留在卡片 `conflicts`，不在本叶改 `algorithm_type`。Q093、Q094、Q095、Q096、Q097、Q098、Q099、Q100、Q101、Q102 只登记，不代甲方裁口径。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ IP-07 抽取在 lumen-algo-py；IP-06 的 SQL 落 GDF；IP-09 由 Java 读父快照，不算公式 |
| 2 调用链：前端 → Java → Python /internal | ✅ 在线读不直连久新；子图只 Feign `/internal/graph/*` |
| 3 只用 NebulaGraph | ✅ 实体与关系写 TRSGraph（graphd 10.50.75.136:9669）；Java 不写 nGQL；未采用 Neo4j |
| 4 可观测 | N/A（spike 分析，无代码） |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 | ✅ 派生与父库叶共一份快照，不另要久新接口 |
| 8 ADS 先行 + Mock | ✅ D1=draft、D4=mock 只记现状；无快照即空态，禁止 Mock 兜底 |
| 9 D8 | N/A |
| 10 D9 | ✅ 每卡绑定包内 metric_id，未把状态改绿，未读 metrics/registry |
| 11 D10 | N/A |
| 12 D12 | ✅ 包内实现位置是 lumen-algo-py / lumen-etl-es-py / GDF，不是 demo-*。每张卡写明禁止 lumen 调用 demo-* |
| 业务口径不替甲方拍板 | ✅ Q 项与久新「待确认」只登记 |
| 只读 | ✅ 未连库，未 commit，未读 task-registry.yaml |

## 6. cost

价表无 grok 行。按 algorithm 默认比例 75/25，用旗舰档 Opus 4.7 单价（输入 $15/M、输出 $75/M）作上界。`source: estimate`。

`actual_cost = 220000×0.75×15/1e6 + 220000×0.25×75/1e6 = 6.60`

| 字段 | 值 |
|---|---|
| actual_tokens | 220000 |
| model_used | grok-4.7 |
| actual_cost | 6.60 |
| cost_warn | yellow |

未超过 $10，不暂停。yellow 按预算规则知会 PM。
