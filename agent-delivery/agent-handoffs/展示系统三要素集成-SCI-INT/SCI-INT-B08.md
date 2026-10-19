# SCI-INT-B08 handoff：机构深度模型（7）

| 项 | 值 |
|---|---|
| task_id | SCI-INT-B08（spike） |
| 执行 | agent:algorithm-agent |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新 |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：总派单 B08 的 7 条 `M_ORG_DEEP_149_1` … `M_ORG_DEEP_155_1`。每条一卡，`layer=metric`，号段 `INT-B-ORG-700` … `INT-B-ORG-706`。
- **产出**：`产物/SCI-INT-B08.yaml`。模式取包内 `b01.pattern`，七条都是 IP-08。`algorithm_type` 保持 `third_party`。
- **久新行**：SRS-149 … SRS-155 都在，有久新行，不标 IP-10。
- **页面**：只用包内 `srs_refs_02` 与 `a_cards`。`a_cards` 为空。149–152、154、155 写「未挂页」。153 按包保留 `DS-07-POLICY-GUARD`。
- **主数据**：机构主键只引用 C03 `INT-C-ORG-240`，不另造第二张机构主数据卡。
- **实现位置**：包内落点是 `lumen-algo-py` 适配层与 `lumen-etl-es-py` 入站。没有指向 `demo-*`。D12 写在每张卡上：正式实现禁止 lumen 调用任何 `demo-*`。153 另记 C05 草案 space 名 `demo_gkx_chain` 不得作为正式 space。

### 1.1 久新依赖

本叶不新增久新行号。七条都是库叶 API，确认状态都是「待确认」。

| 久新行 | 角色 | 交付 | 确认 | 消费卡 |
|---|---|---|---|---|
| SRS-149 | 重点技术领域布局 | API | 待确认 | INT-B-ORG-700 |
| SRS-150 | 发展历程 | API | 待确认 | INT-B-ORG-701 |
| SRS-151 | 深圳优势 | API | 待确认 | INT-B-ORG-702 |
| SRS-152 | 深圳痛难点 | API | 待确认 | INT-B-ORG-703 |
| SRS-153 | 合作关系链 | API | 待确认 | INT-B-ORG-704 |
| SRS-154 | 引入推荐 | API | 待确认 | INT-B-ORG-705 |
| SRS-155 | 扶持推荐 | API | 待确认 | INT-B-ORG-706 |

### 1.2 153 与 A09

A09 卡 `INT-A-X-0817` 把 `M_ORG_DEEP_153_1` / SRS-153 标成 IP-10。材料包 `b01.pattern` 是 IP-08，且有久新行。本叶保持 IP-08，不照抄那个错误。

包内 `srs_refs_02` 把 seq 153 写成「政策扶持力度分析」，页面 `DS-07-POLICY-GUARD`，与库叶名称「科研合作关系链条模型」不一致。页面按包保留，不改挂，也不因此改模式。

### 1.3 同步 / 异步

请求路径计：七条 IP-08 的久新 API 都还是「待确认」。按 IP-03 默认，SLA 未确认前先走异步 Job，适配层写快照。页面读快照不另记一条同步。

| 方式 | 条数 | 卡 |
|---|---|---|
| 同步 | 0 | — |
| 异步 | 7 | INT-B-ORG-700 … INT-B-ORG-706 |

## 2. 偏离说明

- 卡片数 = 指标数 = 7，差集空。未按页面再拆卡。
- 久新行上的 MODEL 与 `third_party` 的差异写在 `conflicts`，原值未改。
- 有久新行的七条保持包内 IP-08，不改标 IP-10。
- C 卡把入站写成离线 ETL，153 的 C 卡还带图模式。本叶不因此改模式编号。
- 机构没有 `org_uid`（C03，供应方 P0-1）。VID 前缀 `inst:` 与 `org:` 未统一，C05 建议 `inst:`，尚未拍板。本叶不代定。
- 新快照表升 `human:李伟`。机构主数据只引用已有卡 `INT-C-ORG-240`。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-B08.yaml`（7 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B08-check.py`
- 本 handoff
- 没有 commit，没有 push，没有改业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B08-check.py"`，退出码 0：

```
cards=7 expect=7 gap=[]
int_ids=700-706 unique=7
sync=0 async=7
jiuxin_rows: ['SRS-149', 'SRS-150', 'SRS-151', 'SRS-152', 'SRS-153', 'SRS-154', 'SRS-155']
structure_escalation: ['SE-B08-01']
structure_escalation_refs: ['INT-C-ORG-240']
pattern_153: IP-08
OK
```

脚本核对：包内 7 个 metric_id 全覆盖且顺序一致、差集为空、卡号 700–706、无占位符 TBD、模式与 `algorithm_type` 与久新行均等于包内 `b01`、有久新行的卡不是 IP-10、输入输出与包内 C 卡一致、页面集合等于包内 `srs_refs_02` 与 `a_cards`、153 保持 IP-08 并写明 A09 纠偏、机构主数据只引用 INT-C-ORG-240。

**结论：7 张卡，差集 0。自检 OK，差集 0。**

### 4.1 结构升级

| id | 负责人 | 新表 | 范围 |
|---|---|---|---|
| SE-B08-01 | human:李伟 | `ads_sci_org_deep_snapshot`（包内表名未定，暂用此名） | INT-B-ORG-700 … 706。七条深度模型的 API 结果快照 |
| INT-C-ORG-240（引用，不新开） | human:李伟 | C03 科研机构主数据 | 不另造第二张主表。当前无 org_uid |

### 4.2 最大 3 个开放项

1. **库叶 API 未确认**（OI-B08-01）：SRS-149 … SRS-155 的接口文档、鉴权、QPS、SLA 仍是「待确认」。
2. **机构主键与 VID**（OI-B08-02）：没有 `org_uid`（C03，供应方 P0-1）。VID 前缀 `inst:` 与 `org:` 未统一，C05 建议 `inst:`，尚未拍板。
3. **新快照表升李伟**（OI-B08-03）：`ads_sci_org_deep_snapshot`（SE-B08-01）。机构主数据只引用 INT-C-ORG-240。

类型冲突留在卡片 `conflicts`，不在本叶改 `algorithm_type`。153 的页面错名只登记，不代甲方改挂。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ IP-08 适配与异步 Job 在 lumen-algo-py；Java 不算模型 |
| 2 调用链：前端 → Java → Python /internal | ✅ Java 只调 `/internal/org/*` 或读 ADS 快照；153 子图只 Feign `/internal/graph/*`；不直连久新，不写 nGQL |
| 3 只用 NebulaGraph | ✅ 153 若读图只走 TRSGraph；VID 前缀未拍板，本叶不写死；未采用 Neo4j |
| 4 可观测 | N/A（spike 分析，无代码） |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 | ✅ 七条共一张快照；机构主键共引用 C03 一张主数据卡 |
| 8 ADS 先行 + Mock | ✅ D1=draft、D4=mock 只记现状；无快照即空态，禁止 Mock 兜底 |
| 9 D8 | N/A |
| 10 D9 | ✅ 每卡绑定包内 metric_id，未把状态改绿，未读 metrics/registry |
| 11 D10 | N/A |
| 12 D12 | ✅ 包内实现位置是 lumen-algo-py / lumen-etl-es-py，不是 demo-*。每张卡写明禁止 lumen 调用 demo-*。153 排除 demo_gkx_chain 作为正式 space |
| 业务口径不替甲方拍板 | ✅ org_uid、VID 前缀、久新「待确认」、153 页面错名只登记 |
| 只读 | ✅ 未连库，未 commit，未读 task-registry.yaml |

## 6. cost

价表无 grok 行。按 algorithm 默认比例 75/25，用旗舰档 Opus 4.7 单价（输入 $15/M、输出 $75/M）作上界。`source: estimate`。

`actual_cost = 160000×0.75×15/1e6 + 160000×0.25×75/1e6 = 4.80`

| 字段 | 值 |
|---|---|
| actual_tokens | 160000 |
| model_used | grok-4.7 |
| actual_cost | 4.80 |
| cost_warn | green |

未超过 $5，不标黄。未超过 $10，不暂停。
