# SCI-INT-B02 handoff：人才深度模型集成项（156–165）

| 项 | 值 |
|---|---|
| task_id | SCI-INT-B02（spike） |
| 执行 | agent:algorithm-agent |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新 |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：`M_TALENT_DEEP_156_1` … `M_TALENT_DEEP_165_1`，共 10 条。每条一卡，`layer=metric`，号段 `INT-B-TAL-100` … `INT-B-TAL-109`。
- **产出**：`产物/SCI-INT-B02.yaml`。字段按 `_card-template.yaml`，并写明久新行、输入表/字段、输出、同步或异步、使用页面。
- **模式**：全部取包内 `b01.pattern` = **IP-08**（third_party × API，Python 适配层，Java 只调 Python）。`algorithm_type` 保持 `third_party`，未改成久新行上的 MODEL。
- **调用方式**：10 条都按页面消费计为**异步**。IP-08 默认 T+1 快照，页面只读 `ads_sci_result_snapshot`。适配层内部可发连接 2s / 读 10s 的同步外呼，超时转 IP-04，不单独算同步卡。
- **页面**：只用包内 `srs_refs_02` 与 `a_cards`。有挂页 4 条（157、160、162、164）。无挂页 6 条（156、158、159、161、163、165），卡上写「未挂页」。
- **实现位置**：包内 Python 落点为 `lumen-algo-py`，未见 `demo-algo-science`。正式实现只在 `lumen-algo-py`。D12 风险已写入每张卡。

### 1.1 久新依赖

| 久新行 | 指标 | 交付 | 确认 | 消费卡 |
|---|---|---|---|---|
| SRS-156 | M_TALENT_DEEP_156_1 | API | 待确认 | INT-B-TAL-100 |
| SRS-157 | M_TALENT_DEEP_157_1 | API | 待确认 | INT-B-TAL-101 |
| SRS-158 | M_TALENT_DEEP_158_1 | API | 待确认 | INT-B-TAL-102 |
| SRS-159 | M_TALENT_DEEP_159_1 | API | 待确认 | INT-B-TAL-103 |
| SRS-160 | M_TALENT_DEEP_160_1 | API | 待确认 | INT-B-TAL-104 |
| SRS-161 | M_TALENT_DEEP_161_1 | API | 待确认 | INT-B-TAL-105 |
| SRS-162 | M_TALENT_DEEP_162_1 | API | 待确认 | INT-B-TAL-106 |
| SRS-163 | M_TALENT_DEEP_163_1 | API | 待确认 | INT-B-TAL-107 |
| SRS-164 | M_TALENT_DEEP_164_1 | API | 待确认 | INT-B-TAL-108 |
| SRS-165 | M_TALENT_DEEP_165_1 | API | 待确认 | INT-B-TAL-109 |

本叶直接依赖上述 10 行，**新增 0 行**。另外只引用、不新要：

- 162 的展示同交 `DS-08-VIZ-001` / `DS-08-VIZ-004`（IP-08：与库叶同交，不单独再要）。
- 157 的图谱读面引用 `SRS-110` / `SRS-111` / `SRS-114`；160 引用 `SRS-111`。归属在 B03 / C04，本叶不新增久新要求。

### 1.2 同步 / 异步

| 方式 | 条数 | 卡 |
|---|---|---|
| 异步 | 10 | INT-B-TAL-100 … 109 |
| 同步 | 0 | — |

## 2. 偏离说明

- 卡片数 = 指标数 = 10，差集空。未按页面再拆卡。
- `page_ref` 在多页时用列表，单页缺失时写「未挂页」。模板示例是单个页面 id。
- 入站列名：包内只给出 `dwd_patent.inventors`、`dwd_zh_project.project_host` / `participants`。其余表写「包内未给列名」，没有补扫 DDL。
- 久新行 `algorithm_type=MODEL` 与注册值 `third_party` 的差异写入每张卡的 `conflicts`，原值未改。
- C 卡把入站写成离线 ETL。本叶运行时仍按 IP-08，不把模式改成 ETL。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-B02.yaml`（10 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B02-check.py`
- 本 handoff
- 没有 commit，没有 push，没有改业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B02-check.py"`：

```
cards=10 expect=10 gap=[]
int_ids=100-109 unique=10
sync=0 async=10
jiuxin_rows: ['SRS-156', 'SRS-157', 'SRS-158', 'SRS-159', 'SRS-160', 'SRS-161', 'SRS-162', 'SRS-163', 'SRS-164', 'SRS-165']
structure_escalation: ['SE-B02-01', 'SE-B02-02']
OK
```

脚本核对：包内 10 个 metric_id 与卡片全覆盖且顺序一致、差集为空、`INT-B-TAL` 数字在 100–199、无占位符 TBD、模式均为 IP-08、`algorithm_type` 均为 third_party、执行方式均为异步。

**结论：10 张卡，差集 0。**

### 4.1 结构升级

| id | 负责人 | 新表 | 范围 |
|---|---|---|---|
| SE-B02-01 | human:李伟 | `ads_sci_result_snapshot`、`ads_sci_jiuxin_adapter_cache` | 10 张卡都写快照并走适配层缓存 |
| SE-B02-02 | human:李伟 | `dwd_talent_flow`（包内表名未定，暂用此名） | INT-B-TAL-101、INT-B-TAL-108（对应 INT-C-TAL-071） |

### 4.2 最大 3 个开放项

1. **久新 10 个 API 都未确认**（DN-B02-01）：SRS-156 … SRS-165 的接口文档、鉴权、QPS、SLA 仍是「待确认」。在确认前页面只读快照，无快照则空态。
2. **6 条没有展示页**（DN-B02-02）：156、158、159、161、163、165 在 `srs_refs_02` 和 `a_cards` 中都没有页面。需要确认它们是否只服务专题 `SRS-TALENT`。
3. **类型冲突未改值**：10 行久新清单写 MODEL，注册与 P00 写 third_party。卡片保持 third_party，冲突在 `conflicts`。若评审要改类型，走口径变更，不在本叶改。

其他：流动边表是否单独立表（DN-B02-03 / SE-B02-02）；统计窗口与对象范围本包未展开；入站列名待 C 段补列。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 适配与快照写入在 lumen-algo-py；Java 不算模型 |
| 2 调用链：前端 → Java → Python /internal | ✅ 每张卡按此顺序；前端与 Java 不直连久新 |
| 3 只用 NebulaGraph | ✅ 157/160 的图谱读面写 TRSGraph / `/internal/graph/*`；Java 不写 nGQL；未采用 Neo4j |
| 4 可观测 | ⚠️ 本叶不改代码。实现时按 IP-08：Java Agent、Python 外呼 span、前端展示「数据截至」 |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 只读 | ✅ 未改 demo 仓 |
| 7 共享聚合核心 | ✅ 学术力同交 DS-08 与库叶共用一份快照，不另要接口 |
| 8 ADS 先行 + Mock | ✅ D4=mock 只作现状；运行态禁止 Mock 兜底，无快照即空态 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 每卡绑定已有 metric_id；d1=draft，d4=mock，来自任务包，未把状态改绿 |
| 11 D10 | N/A |
| 12 D12 | ✅ 包内实现位置是 lumen-algo-py，不是 demo-algo-science。风险已写入每张卡：正式实现禁止调用 demo-* |

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
