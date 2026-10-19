# SCI-INT-B05 handoff：技术深度模型集成项（130–140）

| 项 | 值 |
|---|---|
| task_id | SCI-INT-B05（spike） |
| 执行 | agent:algorithm-agent |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新 |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：`M_TECH_DEEP_130_1` … `M_TECH_DEEP_140_1`，共 11 条。每条一卡，`layer=metric`，号段 `INT-B-TECH-400` … `INT-B-TECH-410`。
- **产出**：`产物/SCI-INT-B05.yaml`。字段按 `_card-template.yaml`，并写明久新行、输入、输出、同步或异步、使用页面。
- **模式**：全部取包内 `b01.pattern` = **IP-08**。11 条都有久新行（SRS-130 … SRS-140），**不标 IP-10**。`algorithm_type` 保持 `third_party`，未改成久新行上的 MODEL。
- **调用方式**：11 条都按页面消费计为**异步**。IP-08 默认 T+1 快照，页面只读 `ads_sci_result_snapshot`（引用 SE-B02-01，不另造）。适配层内部可发连接 2s / 读 10s 的同步外呼，超时转 IP-04，不单独算同步卡。134、137 的 A 卡已写明批量 refresh。
- **页面**：只用包内 `srs_refs_02` 与 `a_cards`。有挂页 3 条（130 → DS-02-TECHGRAPH；134、137 → DS-03-RESULT 与 DS-03-WORKFLOW）。其余 8 条写「未挂页」。
- **展示行**：134 / 135 / 137 的展示同交写在对应卡上。没有 A 卡页面的行写「未挂页」。归属以 b01 备注为准。
- **技术点**：C02 技术点主数据没有 `technology_id`。TAG technology 未建（C04）。本叶不新造技术点主表。
- **实现位置**：包内 Python 落点为 `lumen-algo-py`。D12：正式实现禁止调用 `demo-*`。

### 1.1 久新依赖

| 久新行 | 指标 | 交付 | 确认 | 消费卡 |
|---|---|---|---|---|
| SRS-130 | M_TECH_DEEP_130_1 | API | 待确认 | INT-B-TECH-400 |
| SRS-131 | M_TECH_DEEP_131_1 | API | 待确认 | INT-B-TECH-401 |
| SRS-132 | M_TECH_DEEP_132_1 | API | 待确认 | INT-B-TECH-402 |
| SRS-133 | M_TECH_DEEP_133_1 | API | 待确认 | INT-B-TECH-403 |
| SRS-134 | M_TECH_DEEP_134_1 | API | 待确认 | INT-B-TECH-404 |
| SRS-135 | M_TECH_DEEP_135_1 | API | 待确认 | INT-B-TECH-405 |
| SRS-136 | M_TECH_DEEP_136_1 | API | 待确认 | INT-B-TECH-406 |
| SRS-137 | M_TECH_DEEP_137_1 | API | 待确认 | INT-B-TECH-407 |
| SRS-138 | M_TECH_DEEP_138_1 | API | 待确认 | INT-B-TECH-408 |
| SRS-139 | M_TECH_DEEP_139_1 | API | 待确认 | INT-B-TECH-409 |
| SRS-140 | M_TECH_DEEP_140_1 | API | 待确认 | INT-B-TECH-410 |

本叶直接依赖上述 11 行，**新增 0 行**。另外只引用、不新要：

- 130 的实体 / 关系读面引用 SRS-104、SRS-105（C-151 / C-152 / C-300 / C-340）。
- 134 的展示同交：DS-03-RESULT-001/002、DS-09-COMPREHENSIVE-001/002/004。
- 135 的展示同交：DS-07-TECH-INNOV-003、DS-07-INDUSTRY-POTENTIAL-002。
- 137 的展示同交：DS-03-RESULT-004/005/006、DS-07-SCI-CREATE-003。

### 1.2 同步 / 异步

| 方式 | 条数 | 卡 |
|---|---|---|
| 异步 | 11 | INT-B-TECH-400 … 410 |
| 同步 | 0 | — |

### 1.3 展示挂页（134 / 135 / 137）

| 卡 | 展示行 | 页面 |
|---|---|---|
| INT-B-TECH-404 | DS-03-RESULT-001 | DS-03-RESULT（INT-A-TECH-300） |
| INT-B-TECH-404 | DS-03-RESULT-002 | 未挂页 |
| INT-B-TECH-404 | DS-09-COMPREHENSIVE-001 / 002 / 004 | 未挂页 |
| INT-B-TECH-404 | （模型工作流，非展示行） | DS-03-WORKFLOW（INT-A-TECH-326） |
| INT-B-TECH-405 | DS-07-TECH-INNOV-003 | 未挂页 |
| INT-B-TECH-405 | DS-07-INDUSTRY-POTENTIAL-002 | 未挂页 |
| INT-B-TECH-407 | DS-03-RESULT-004 | DS-03-RESULT（INT-A-TECH-309） |
| INT-B-TECH-407 | DS-03-RESULT-005 / 006 | 未挂页 |
| INT-B-TECH-407 | DS-07-SCI-CREATE-003 | 未挂页 |
| INT-B-TECH-407 | （模型工作流，非展示行） | DS-03-WORKFLOW（INT-A-TECH-327） |

130 另挂 DS-02-TECHGRAPH（INT-A-TECH-102）。131–133、136、138–140 未挂页。

## 2. 偏离说明

- 卡片数 = 指标数 = 11，差集空。未按页面再拆卡。
- `page_ref` 在多页时用列表，没有页面时写「未挂页」。
- 展示行归属跟 b01 备注，不跟 C 卡的交叉列表。C-156 把 DS-07-SCI-CREATE-003 放在 134，C-159 把 DS-07-INDUSTRY-POTENTIAL-002 放在 137。两处与 b01 备注对调，记入 `conflicts`，不在本叶改 C 卡。
- 久新行 `algorithm_type=MODEL` 与 b01 / P00 的 `third_party` 写入 `conflicts`，原值未改。
- C 卡把部分入站写成离线 ETL。本叶运行时仍按 IP-08。
- 快照表与适配层缓存只引用 SE-B02-01，不另造第二套。
- 新表只升一张领域维 `dim_tech_domain`（SE-B05-01）。不与 C02 技术点主数据各造一张。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-B05.yaml`（11 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B05-check.py`
- 本 handoff
- 没有 commit，没有 push，没有改业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B05-check.py"`：

```
cards=11 expect=11 gap=[]
int_ids=400-410 unique=11
sync=0 async=11
jiuxin_rows: ['SRS-130', 'SRS-131', 'SRS-132', 'SRS-133', 'SRS-134', 'SRS-135', 'SRS-136', 'SRS-137', 'SRS-138', 'SRS-139', 'SRS-140']
structure_escalation: ['SE-B05-01']
OK
```

脚本核对：包内 11 个 metric_id 与卡片全覆盖且顺序一致、差集为空、`INT-B-TECH` 数字在 400–499、无占位符 TBD、模式均为 IP-08、`algorithm_type` 均为 third_party、有久新行且不是 IP-10、执行方式均为异步。

**结论：11 张卡，差集 0。自检 OK，差集 0。**

### 4.1 结构升级

| id | 负责人 | 新表 | 范围 |
|---|---|---|---|
| SE-B05-01 | human:李伟 | `dim_tech_domain`（包内表名未定稿，暂用此名） | INT-B-TECH-403、404、410（INT-C-TECH-181） |
| SE-B02-01（引用） | human:李伟 | `ads_sci_result_snapshot`、`ads_sci_jiuxin_adapter_cache` | 11 张卡只引用，不另造 |

技术点：无 `technology_id`（C02）；TAG technology 未建（C04）。`tech_point.new_master_table=false`。

### 4.2 最大 3 个开放项

1. **久新 11 个 API 都未确认**（DN-B05-01）：SRS-130 … SRS-140 的接口文档、鉴权、QPS、SLA 仍是「待确认」。确认前页面只读快照，无快照则空态。
2. **8 条没有展示页，134/137 的部分展示行也未挂页**（DN-B05-02）：131–133、135、136、138–140 在 `srs_refs_02` 和 `a_cards` 中都没有页面。135 的两条展示行同样未挂页。
3. **领域维表与展示行归属**（DN-B05-03 / DN-B05-04）：`dim_tech_domain` 升 human:李伟。DS-07-SCI-CREATE-003 与 DS-07-INDUSTRY-POTENTIAL-002 在 C 卡和 b01 备注之间对调，本叶按 b01 备注落卡。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 适配与快照写入在 lumen-algo-py；Java 不算模型 |
| 2 调用链：前端 → Java → Python /internal | ✅ 每张卡按此顺序；前端与 Java 不直连久新 |
| 3 只用 NebulaGraph | ✅ 130/131 图谱读面写 TRSGraph / `/internal/graph/*`；Java 不写 nGQL；未采用 Neo4j。TAG technology 记为 C04 未建 |
| 4 可观测 | ⚠️ 本叶不改代码。实现时按 IP-08：Java Agent、Python 外呼 span、前端展示「数据截至」 |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 只读 | ✅ 未改 demo 仓 |
| 7 共享聚合核心 | ✅ 展示行与库叶共用一份快照，不另要接口 |
| 8 ADS 先行 + Mock | ✅ D4=mock 只作现状；运行态禁止 Mock 兜底，无快照即空态 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 每卡绑定已有 metric_id；d1=draft，d4=mock，来自任务包，未把状态改绿 |
| 11 D10 | N/A |
| 12 D12 | ✅ 包内实现位置是 lumen-algo-py，不是 demo-algo-science。风险已写入每张卡：正式实现禁止调用 demo-* |

## 6. cost

价表无 grok 行。按 algorithm 默认比例 75/25，用旗舰档 Opus 4.7 单价（输入 $15/M、输出 $75/M）作上界。`source: estimate`。

`actual_cost = 160000×0.75×15/1e6 + 160000×0.25×75/1e6 = 4.80`

| 字段 | 值 |
|---|---|
| actual_tokens | 160000 |
| model_used | grok-4.7 |
| actual_cost | 4.80 |
| cost_warn | green |

未超过 $10，不暂停。
