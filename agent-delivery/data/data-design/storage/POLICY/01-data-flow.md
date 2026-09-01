# 政策维 · 端到端数据流

```yaml
---
doc_id: POLICY-STORAGE-FLOW
element: POLICY
role: data-flow
status: approved
version: "2026-09-02"
updated: 2026-09-02
engine: multi
signoff_owner: human:淮政玮
signoff_status: approved
signoff_by: human:淮政玮
signoff_at: 2026-08-21
task_id: LUMEN-POLICY-PY-JOB-L01
amendment_note: "PY-BOOT：Python 生产者改指 lumen-algo-py vendor/entan-py/polan（/internal/policy）；工厂 ODS→GDF→DWD→ADS→demo_gkx_chain 拓扑不改、不翻签。联调台仍走 demo-algo-ent-analysis 虚线。细表 stores 仍 draft。PY-HARNESS-L01：专题 Job 经 polan.harness 分片调用已有入口，不改工厂拓扑、不改算子 run()。PY-JOB-L01：补 /internal/policy/search 与 /internal/policy/jobs/execute（只调 harness.dispatch）；分析 Job 边仍不改 ODS→DWD→ADS 工厂拓扑。"
---
```

> **会签 Owner / 已签：`human:淮政玮`** · 2026-08-21 **approved**。不经 `human:李伟`。  
> **执行**：`human:淮政玮` · `DATA-POLICY-STORAGE-S1-L01`。  
> **细表**（S3 `stores/*`）仍 draft，不得因本流图标 approved。

## 1. 批处理主链（工厂 + 投影）

实线 = 本管线授权施工（A 设计 / B 编码后）。虚线 = 目标态或 as-built，本单禁止当目标写入。

```mermaid
flowchart LR
  ODS["三方 gkx<br/>dwd_policy_base<br/>dwd_global_policy_base"] --> GDF["GDF / 模拟 GDF"]
  GDF --> DWD["demo_gkxlumenx_dwd<br/>policy_base_info"]
  DWD --> ADS["demo_gkxlumenx_ads<br/>policy_* / policy_graph_*"]
  DWD -->|"实线 投影"| NEB["Nebula demo_gkx_chain"]
  PY["lumen-algo-py<br/>vendor/entan-py/polan"] -->|写| ADS
  PY -->|"实线 投影"| NEB
  PY -.->|"虚线 as-built 禁止目标"| OLD["Nebula gkx_policy"]
  JAVA["Java 聚合"] -->|只读| ADS
  JAVA -->|"Feign /internal/policy"| PY
  FE["demo-ui-system-test /policy"] -->|"联调台实线"| GW["gkx-gateway gkx-policy"]
  GW -.->|"虚线 联调台仍走 demo"| DEMOPY["demo-algo-ent-analysis polan"]
  FE2["lumen-ui-*"] -.->|"虚线 D12 产品链"| JAVA
  FE3["demo-ui-science policy-tracking"] -.->|"虚线 as-built fixture"| MOCK["policyData.js"]
  FE3 -.->|"虚线 目标态"| JAVA
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| 三方 / Mock ODS | DWD `policy_base_info` | 批：模拟 GDF / `run_all_policy` | 本批失败不晋升 ADS；保留上一成功 DWD | 默写正式 `gkx`/`gkxlumenx_*`；仍用 `dwd_zck_*`；PG 叙述 |
| `lumen-algo-py` polan | ADS `policy_*` | 流水线 append/replace | 半成品不发布；任务 failed | 前端造假填数；专题调 `/v1`；专题 Job 一次 load 全表 4 万+（须走 `polan.harness` 分片） |
| `lumen-algo-py` polan | `demo_gkx_chain` | 投影（算子冻结，本叶只迁代码） | fail-soft：ADS 镜像仍可读；`source` 不得标 nebula | `CREATE SPACE gkx_policy`；`DROP SPACE demo_gkx_chain`；写 `gkx_chain` |
| Java | 前端 | 在线 HTTP | 不写回库；不扫 ODS | 直连 nGQL；lumen 调 demo 服务当正式链；展示前端把 fixture 当 ADS |

## 2. 在线读路径（算法库现网）

```mermaid
flowchart TB
  FE["demo-ui-system-test"] --> GW["gkx-gateway"]
  GW -->|"/policy/**"| PY["gkx-entan-py polan"]
  PY -->|"优先"| NEB["demo_gkx_chain"]
  PY -->|"兜底"| ADS["demo_gkxlumenx_ads.policy_graph_*"]
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| polan `/v1/policy/graph` | 前端 | 用户打开政策图谱 | Nebula 不可用 → `source=mysql`/`ads` 诚实兜底 | ADS 全表扫却 `source=nebula` |
| Tempo-Demo | 排障 | 响应头 X-Trace-Id | 2026-08-21 抽样仅 MySQL ADS | 把 as-built 当已投影 |

## 2.1 在线读路径（展示系统 · 目标态）

真源对照：[`windows/display-ds10-12.md`](./windows/display-ds10-12.md)。**不改** §1 工厂边。

```mermaid
flowchart TB
  SCI["lumen-ui-science-* / display/policy"] --> GW2["gkxlumen-platform-gateway"]
  GW2 --> JAVA2["Java 只读 ADS"]
  JAVA2 --> ADS2["demo_gkxlumenx_ads.policy_*"]
  JAVA2 -->|"图/推演 Feign"| PY2["lumen-algo-py /internal/policy"]
  DEMO["demo-ui-science policy-tracking"] -.->|"虚线 fixture"| FIX["policyData.js"]
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| ADS `policy_*` | 展示全景/评价/推演 KPI | 打开 DS-10/11/12 | 缺表诚实空 + D9 角标 | 第二套展示 DWD；直连 Nebula |
| Java 任务快照 | 未出台仿真 | 用户点运行 | I2-12 单飞；当天成功可复用 | 前端假装算完 |

## 3. 点/边挂接映射（拓扑已放行；细表 DDL 仍 draft）

CHAIN 现网 schema（`chainan.graph.nebula_schema`，禁止另起第二套本体）：

- Tag：`chain` / `segment` / `enterprise` / `institution`
- Edge：`belongs_to` / `participates` / `supplies` / `depends_on`

今日 `polan` as-built（独立 space 思路，**废作目标态**）：

- Tag：`policy` / `industry` / `tech` / `enterprise` / `talent` / `org` / `service`
- Edge：`support` / `apply_to` / `regulate` / `cite`

**B 叶已放行施工范围**（`human:淮政玮` · 2026-08-21）：仅 `demo_gkx_chain` 上 `CREATE TAG IF NOT EXISTS policy` 与 `CREATE EDGE IF NOT EXISTS` 四边 `support` / `apply_to` / `regulate` / `cite`。禁止 DROP SPACE、禁止写 `gkx_chain`、禁止新建 `gkx_policy`。

| polan 产出 | 一张 G 落点 | 本波 | 说明 |
|---|---|---|---|
| `policy` 节点 `pol:{policy_id}` | Tag `policy`（name/weight/props） | **施工** | B 叶 CREATE TAG IF NOT EXISTS |
| `industry` | hang `chain` 或 `segment`（`industry_link_code`） | **施工** | 对不齐则不上图 |
| `enterprise` | 已有 Tag `enterprise`（`org_id`） | **施工** | 与 ENT hang 同一 VID |
| `org` | 已有 Tag `institution` | **施工** | 不新建 `org` Tag |
| `service` | Tag `institution` + props.institution_type | **施工** | 不平行 SVC 本体 |
| `tech` / `talent` | 缺 Tag | **本波不上图** | OPEN-POLICY-GRAPH-01 |
| `support` / `apply_to` / `regulate` / `cite` | 同名新 Edge | **施工** | 不改 CHAIN 已有 EDGE_DDL 语义 |

**VID**：政策点 `pol:{policy_id}`；长度遵守 CHAIN `vid_length=80`。禁止截断导致碰撞。

## 4. 会签清单

- [x] 投影目标仅 `demo_gkx_chain`；`gkx_policy` 保持虚线  
- [x] 不 DROP 底图；不写 `gkx_chain`  
- [x] Tag/Edge 本波施工范围已写清（policy + 四边；tech/talent 不上图）  
- [x] 无 PostgreSQL / Neo4j  
- [x] ADS 仍为 Java 契约面；图失败 ADS 可兜底  

> 已由 `human:淮政玮` 于 2026-08-21 会签：`signoff_status=approved`。

## 5. 开放项

| ID | 项 | Owner | 关闭 |
|---|---|---|---|
| OPEN-POLICY-GRAPH-01 | `tech`/`talent` 是否上图、Tag 名 | `human:淮政玮` | 本波跳过；不挡 B |
| OPEN-POLICY-GRAPH-02 | 四类边是否日后折进 `participates` | `human:淮政玮` | 本波用同名新 Edge |
| OPEN-POLICY-GRAPH-03 | `policy` Tag 细列与 SAD 对齐 | 架构 | S3 stores/nebula |
| OPEN-POLICY-FLOW-01 | 正式调用链改 Java 门面 | api-agent | 展示+专题目标态 |
| OPEN-POLICY-DISP-01～09 | 展示窗口缺口（收藏/订阅/舆情/仿真快照等） | 见 `windows/display-ds10-12.md` | 不挡 B 投影 |
| OPEN-POLICY-DIM-01 | `dim.region` 省级/深圳区县维表缺失 | data-agent | 建维表，或把 seed 源表改为 as-built 做法 |
| OPEN-POLICY-DIM-02 | 专家策略库维表缺失 | `human:淮政玮` | 口径与来源均未定，随 QPOL-02 一并确认 |
| OPEN-POLICY-XDOM-01 | 跨域依赖 `dwd.industry_chain` 未登记 | data-agent | 与 CHAIN 域约定读法后登记为跨域引用 |

### 5.1 三项依赖缺口说明（2026-08-31 `DATA-POLICY-DEP-GAP-OPEN-L01` 登记）

来源：政策 17 指标定义与存储支撑核查。三项均为 **seed 声明了依赖、但存储树无对应对象**。

| ID | 受影响指标 | seed 声明 | 当前 as-built 做法 | 风险 |
|---|---|---|---|---|
| OPEN-POLICY-DIM-01 | `M_POLICY_NATIONAL_DIST` · `M_POLICY_SZ_DIST` | `dim: dim.region`（省级 / 深圳区县映射） | `basic/indicators.py` 直接用 `dwd.policy_base_info.region` 字符串聚合，无维表 | 省市区名称不规范时分组漂移；跨域口径无法与 CHAIN/ENT 对齐 |
| OPEN-POLICY-DIM-02 | `M_POLICY_LAYOUT_REC_COUNT` | 「专家策略库（待补维表）」 | 无。`eval/layout.py` 仅融合机遇 + 短板 | 布局建议缺专家策略输入，口径不完整 |
| OPEN-POLICY-XDOM-01 | `M_POLICY_INDUSTRY_COVERAGE` | `dwd.industry_chain`（跨域产业链维表） | 产业侧靠 `related_entities.industry` / `ext5` 文本，未接 CHAIN 维表 | 「产业链全节点数」分母无权威来源，覆盖度不可信 |

两条路二选一，**不得两边并存**：补齐对应对象，或把 seed 的 `source_tables` 改为 as-built 做法并在口径里写明降级。前者属结构项、后者属口径项，均需 `human:淮政玮` 定向。

## 6. 下游放行

| 阶段 | 结论 |
|---|---|
| 本叶 | 流图已签；细表仍 draft |
| B `POLICY-NEBULA-PROJECT-CHAIN-L01` | **放行 ready**：按 §3 施工范围投影 `demo_gkx_chain` |
