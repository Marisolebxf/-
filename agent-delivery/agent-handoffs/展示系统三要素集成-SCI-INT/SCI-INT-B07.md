# SCI-INT-B07 handoff：技术 MODEL 3 + STAT 4 + 评估热度 9（16）

| 项 | 值 |
|---|---|
| task_id | SCI-INT-B07（spike） |
| 执行 | agent:algorithm-agent |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（8 条 IP-09）；MODEL 3 条与 STAT 4 条、综合分无久新行 |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：总派单 §4 B07 的 16 条 `M_TECH_*`。每条一卡，`layer=metric`，号段 `INT-B-TECH-600` … `INT-B-TECH-615`。
- **产出**：`产物/SCI-INT-B07.yaml`。模式取包内 `b01.pattern`，`algorithm_type` 保持包内 `b01` 值。
- **拆分**：MODEL 3 条 IP-04，STAT 4 条 IP-01，评估热度 8 条 IP-09，综合分 1 条 IP-10。有久新行或已有模式的不改标 IP-10。
- **页面**：只用包内 `srs_refs_02` 与 `a_cards`。无挂页的写「未挂页」。A09 的 `INT-A-X-0805/0807/0809` 记在三条 MODEL 的 `used_by`，页面仍是 `DS-07-TECH-INNOV`。
- **实现位置**：STAT 在 GDF，Java 只读 ADS。MODEL Job 与久新父任务在 `lumen-algo-py`。注册里的 `demo-algo-science` 不作为正式落点。

### 1.1 久新依赖

本叶不新增久新行号。8 条 IP-09 消费已有库叶，不单独再要接口。MODEL 3 条、STAT 4 条、综合分无久新行。

| 久新行 | 角色 | 交付 | 确认 | 消费卡 |
|---|---|---|---|---|
| SRS-134 | 前沿热点库叶。技术点热度与话题热度的母指标，对象不同 | API | 待确认 | INT-B-TECH-609、615 |
| SRS-135 | 产业化潜力库叶 | API | 待确认 | INT-B-TECH-612 |
| SRS-136 | 转化瓶颈库叶 | API | 待确认 | INT-B-TECH-608 |
| SRS-137 | 阶段分析库叶。阶段、成熟度、阶段判定分字段 | API | 待确认 | INT-B-TECH-610、611、613 |
| SRS-138 | 深圳技术发展问题库叶。潜力与阶段复用 135 / 137，不改挂 133 / 140 | API | 待确认 | INT-B-TECH-614 |

无久新行：INT-B-TECH-600、601、602（IP-04），603、604、605、606（IP-01），607（IP-10）。

### 1.2 MODEL 三条冲突结论

`M_TECH_DS_07_TECH_INNOV_002/004/006` 的注册 `algorithm_type` 保持 **MODEL**，不改注册值。

| 事实 | 结论 |
|---|---|
| 注册 | MODEL |
| A2 | DS-07-TECH-INNOV-002/004/006 差集判定 **missing**，05 无专叶 |
| 算法位置 | `extras.algo_server_location` 指向 `demo-algo-science`（D12，风险 R1） |
| 页面 | A09 卡 INT-A-X-0805 / 0807 / 0809 已标 IP-04 |
| 本叶 | 模式保持包内 IP-04，正式实现在 `lumen-algo-py` 重写，禁止 lumen 调用 `demo-algo-science` |
| Owner | DN-05 未定。同步或异步按 IP-03 判据待测，未测前按 IP-04 记异步 |

三条都写入 `conflicts` 与 `decision_needed`。兄弟行 DS-07-TECH-INNOV-003 属久新，不是 004。

### 1.3 同步 / 异步

请求路径计：IP-01、IP-09、IP-10 是同步读；三条 MODEL 按 IP-04 计异步 Job。

| 方式 | 条数 | 卡 |
|---|---|---|
| 同步 | 13 | INT-B-TECH-603 … 615 |
| 异步 | 3 | INT-B-TECH-600、601、602 |

STAT 四条不经 Python。IP-09 不另跑父 Job。IP-10 返回 null 与 reason，不跑评估 Job。

## 2. 偏离说明

- 卡片数 = 指标数 = 16，差集空。未按页面再拆卡。
- 评估热度 9 条的包头 `algorithm_type` 写成 `THIRD_PARTY`，`b01` 与 P00 为 `third_party`。卡上保持 `b01`，不改注册。久新行上的 MODEL 与 `third_party` 的差异只写在 `conflicts`。
- 综合分的页面卡 320 写成 IP-04，328 / 329 写成 IP-11。话题热度的页面卡 302 写成 IP-11。模式保持包内 `b01.pattern`。
- 只有综合分的包内模式是 IP-10。其余有久新行或已有模式的不改标 IP-10。
- C 卡把入站写成离线 ETL。STAT 仍按 IP-01，MODEL 仍按 IP-04。
- Q105、Q121、Q122、Q123、Q124、Q125、DN-03、DN-05、DN-06 只登记，不代甲方裁口径。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-B07.yaml`（16 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B07-check.py`
- 本 handoff
- 没有 commit，没有 push，没有改业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B07-check.py"`，退出码 0：

```
cards=16 expect=16 gap=[]
int_ids=600-615 unique=16
sync=13 async=3
jiuxin_rows: ['SRS-134', 'SRS-135', 'SRS-136', 'SRS-137', 'SRS-138']
structure_escalation: ['SE-B07-01', 'SE-B07-02']
OK
```

脚本核对：包内 16 个 metric_id 全覆盖且顺序一致、差集为空、卡号 600–615、无占位符 TBD、模式与 `algorithm_type` 与久新行均等于包内 `b01`、有久新行或已有非 IP-10 模式的卡不是 IP-10、三条 MODEL 的 conflicts 与 decision_needed 含注册 MODEL、A2 missing、demo-algo-science、D12、A09 卡号与 DN-05、STAT 四条为 IP-01 且不经 Python、新表升 human:李伟。

**结论：16 张卡，差集 0。自检 OK，差集 0。**

### 4.1 结构升级

| id | 负责人 | 新表 | 范围 |
|---|---|---|---|
| SE-B07-01 | human:李伟 | `ads_sci_async_task`（包内未给名，暂用此名） | INT-B-TECH-600、601、602。IP-04 任务元数据 |
| SE-B07-02 | human:李伟 | `ads_tech_query_term_tf`、`ads_tech_invest_amount`、`ads_tech_output_scale`、`ads_tech_paper_patent_cnt`（候选名） | INT-B-TECH-603、604、605、606。STAT 只读 ADS |
| SE-B02-01（引用，不新开） | human:李伟 | `ads_sci_result_snapshot` | MODEL 结果与 IP-09 父快照，不另造第二张 |
| SE-B05-01（引用，不新开） | human:李伟 | `dim_tech_domain` | 话题热度领域维，只引用 INT-C-TECH-181 |
| INT-C-TECH-182（引用，不新开） | human:李伟 | C02 桥接 | 投资额、技术规模、论文专利量，不另造第二张桥 |
| INT-C-TECH-180（引用，不新开） | human:李伟 | C02 技术点主数据 | 不另造第二张主表 |

### 4.2 最大 3 个开放项

1. **三条 MODEL 的 Owner 与落点**（OI-B07-01）：注册是 MODEL，A2 记 missing，算法位置指向 demo-algo-science。A09 已标 IP-04。DN-05 未定。不改注册值。
2. **STAT 预聚合表**（OI-B07-02）：四张 ADS 候选表升 SE-B07-02 / human:李伟。论文专利量自建还是复用 SRS-96 仍是 DN-06。
3. **综合分与久新确认**（OI-B07-03）：综合分保持 IP-10，权重 DN-03 未冻，不跑 Job。8 条 IP-09 的久新行均为待确认，不单独再要接口。任务表见 SE-B07-01。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ MODEL Job 在 lumen-algo-py；STAT 的 COUNT/SUM 在 GDF SQL；IP-09 由 Java 读父快照，不算公式；IP-10 不实现 |
| 2 调用链：前端 → Java → Python /internal | ✅ Java 只读 ADS 或快照，不直连久新；STAT 不经 Python；MODEL 的 worker 走 lumen-algo-py |
| 3 只用 NebulaGraph | ✅ 本叶不写 nGQL，不新开 space，未采用 Neo4j |
| 4 可观测 | N/A（spike 分析，无代码） |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 | ✅ 快照只引用 SE-B02-01；话题维只引用 SE-B05-01；深圳评估复用 135 与 137，不另写公式 |
| 8 ADS 先行 + Mock | ✅ D1=draft、D4=mock 只记现状；无快照或空表即空态，禁止 Mock 兜底 |
| 9 D8 | N/A |
| 10 D9 | ✅ 每卡绑定包内 metric_id，未把状态改绿，未改 seed |
| 11 D10 | N/A |
| 12 D12 | ✅ 三条 MODEL 写明禁止 lumen 调用 demo-algo-science，须在 lumen-algo-py 重写。其余卡禁止调用 demo-* |
| 业务口径不替甲方拍板 | ✅ DN-03/05/06 与 Q105/Q121/Q122/Q123/Q124/Q125 只登记；MODEL 注册值未改 |
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
