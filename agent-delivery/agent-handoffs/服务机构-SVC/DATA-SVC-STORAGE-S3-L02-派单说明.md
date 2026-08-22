# DATA-SVC-STORAGE-S3-L02 · 派单说明（阶段 F · 细表 draft + Demo 空表 CREATE）

> **日期**：2026-08-19  
> **Task ID**：`DATA-SVC-STORAGE-S3-L02`  
> **总控**：[`DEMO-SVC-REOPEN-长任务总控.md`](./DEMO-SVC-REOPEN-长任务总控.md)（已授权 · 范围仅阶段 F）  
> **前置（联调闸门）**：`DATA-SVC-STORAGE-S2-L02` handoff + `integration`（不等看板 `done`）  
> **流图**：[`storage/SVC/01-data-flow.md`](../../data/data-design/storage/SVC/01-data-flow.md) **`signoff_status=approved`** · `human:淮政玮` · 2026-08-19  
> **淮总会签口径**：细表**不得**标 `approved`；**仍禁止 F-SEED / 50100 灌数**（须本单契约表落盘后，再经 S4 入口才开灌数叶）  
> **派单**：`agent:coordinator-agent` · `claim_type=coordinator_dispatch`  
> **监管 / 模块负责**：`human:侯佳伟`  
> **看板签收**：`human:淮政玮`  
> **执行**：`data-agent`  
> **task_type**：`definition` · 强度：**ponytail lite**  
> **锁**：24h  

旧叶 `DATA-SVC-STORAGE-S3-L01` = **废作**。禁止 `depends_on`、禁止复活、**禁止抄**旧 `gkx_svc` space / `service_org*` 全列主体五表 / `gkx_dwd.service_org` 38 列稿。

---

## 1. 这张单是什么 / 不是什么

**是**：把 SVC **项目侧** DWD/ADS/DIM/图 hang 细表清单写成 `storage/SVC/stores/*`（一律 `draft`）；写死 **OPEN-SVC-FLOW-06**（ODS 贴源 → SVC DWD 列映射）；在 **`demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` 写出空表 CREATE**（本单可只落 SQL；F-SEED 首刀执行，禁止两边都不建）。

**不是**：细表 `approved`、50100 灌数、F-SEED 叶、改 lumen 四仓、改 CHAIN、DROP/新建 ODS、平行 `svc_org_base`、`SELECT enterprise_*` 当主路径、平行 `gkx_service` space。

---

## 2. 必读（按序）

| 序 | 路径 | 用途 |
|---:|------|------|
| 1 | `storage/SVC/01-data-flow.md` | 已会签；§6 放行 S3 灌清单；§7 主路径；OPEN-06/12 |
| 2 | `storage/SVC/sources/inventory.md` | ODS 33 表；圈定主读 **`demo_gkxlumenx_ods.dwd_org_base_info`**（供方表名带 `dwd_`，角色是 ODS） |
| 3 | `storage/SVC/etl/pipeline-demo-mock.md` | 模拟 GDF 指针 |
| 4 | `DEMO-SVC-REOPEN-长任务总控.md` §1 | 抽取 = ODS→SVC DWD；禁 `enterprise_*`；禁全列复制 |
| 5 | `storage/ENT/stores/` · `storage/CHAIN/stores/` | 目录同构；**表名不要抄 ENT `enterprise_*`** |
| 6 | `metrics/registry/metric-readiness-matrix-SVC.yaml` | A1–A6 `M_SVC_*` |
| 7 | `docs/产业服务算法设计说明.md`（算法仓） | 十模型 ID；表名以本树为准，旧 `gkx_service` / `service_org` 仅对照 |

---

## 3. 命名铁律（防再混层）

| 写法 | 层 | 本单怎么用 |
|---|---|---|
| `demo_gkxlumenx_ods.dwd_org_base_info` | **ODS 贴源**（供方名 `dwd_`） | 抽取/圈定**源**；映射左列必须带库名 |
| `demo_gkxlumenx_dwd.enterprise_*` | ENT **项目 DWD** | **禁止** SVC 主路径 `SELECT` |
| `demo_gkxlumenx_dwd.svc_org_circle` 等 | SVC **项目 DWD** | 只 hang `org_id` + 圈定元数据 |
| `svc_org_base` / 全列拷贝 ODS 主表 | 平行主体 | **禁止** |

OPEN-06 = **从 ODS 抽列映射到 SVC DWD**，不是从 ENT DWD 再映射。

---

## 4. 交付（`storage/SVC/`）

### 4.1 映射（S2 债，本单关闭写作）

- `etl/ods-to-dwd-mapping.md`：左列=`demo_gkxlumenx_ods.dwd_org_base_info`（及投融资 ODS 表 hang）；右列=SVC DWD；图例：直接 hang / 派生进圈定表 / **n.a. 主体不复制** / 聚合进 ADS。

### 4.2 stores（一律 draft）

- `stores/README.md` + `stores/mysql/{README,dwd-svc,ads,dim}.md`
- `stores/nebula/graph-svc.md`：只 hang **`demo_gkx_chain`**（`org_id`↔`node_id`）；禁 `gkx_service`
- `stores/elasticsearch/README.md`：指针即可，**不挡 F**（OPEN-04 可保持开放）

**DWD 至少**：圈定池 `svc_org_circle`（UK `org_id`）；图 hang `svc_org_graph_hang`；投融资事件 hang（空表可建，Q-SVC-006 不伪闭合）。**不要** 38 列 `service_org` 主体。

**ADS 必须同时有**：

- 基础指标 A1–A6（`M_SVC_INDUSTRY_LAYOUT` / `ORG_CNT` / `INVEST_Y` / `NEW_CNT` / `SZ_SCALE` / `SZ_DISTRICT`）
- 十模型回写：短板 / 关系 / 六类技术力（可一张表按 `model_id` 区分）/ 招引 / 培育
- 短板运行时列 = **Q-SVCCHAIN-03**（0 / ≤1 / 均深&lt;55）；**Q061 只对照列** + `pending_client`

### 4.3 Demo 空表 CREATE（不可与 F-SEED 两头空）

- `stores/mysql/ddl-demo-empty.sql`：仅 `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`
- `CREATE TABLE IF NOT EXISTS`；禁 DROP ODS 33 表；禁新建 ODS 实例
- 本单**不灌数**。未连库执行则 handoff 写明「F-SEED 首刀跑本 SQL」

### 4.4 回填

- `SVC/README.md` 读序补 `stores/`；`CHANGELOG.md`；`storage/README.md` SVC 行改为 S3 draft（仍不得标建设完成）
- handoff：`agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S3-L02.md`

---

## 5. DoD

- [x] `etl/ods-to-dwd-mapping.md` 落盘；源表带 `demo_gkxlumenx_ods.` 库名
- [x] `stores/mysql/dwd-svc.md` + `ads.md` + `dim.md` + nebula hang `demo_gkx_chain` 落盘，**status=draft**
- [x] ADS 覆盖 A1–A6 **和** 十模型回写表；短板含 Q-SVCCHAIN-03 + Q061 对照
- [x] `ddl-demo-empty.sql` 覆盖本单列出的 Demo DWD/ADS 表
- [x] 无 `svc_org_base`；无 ODS 主表全列复制；无 `enterprise_*` 主路径；无 `gkx_service` 建表
- [x] **未** 50100 灌数、未建 F-SEED 叶、未改 lumen 四仓 / CHAIN
- [x] 细表未标 approved
- [x] handoff 含架构合规 + cost 四字段 + `ponytail: lite`

---

## 6. `/goal`（贴 data-agent 会话）

```
任务：DATA-SVC-STORAGE-S3-L02
监管：human:侯佳伟
认领：coordinator_dispatch · 24h
总控：agent-handoffs/服务机构-SVC/DEMO-SVC-REOPEN-长任务总控.md
厚包：agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-S3-L02-派单说明.md
强度：ponytail lite
上下文：headroom 推荐；禁止 compress 代替精读已会签 01-data-flow 与 OPEN-06

做：storage/SVC stores 细表 draft + ODS→SVC DWD 映射（源=demo_gkxlumenx_ods.dwd_org_base_info）+ demo DWD/ADS 空表 CREATE。
不做：approved、F-SEED、50100 灌数、lumen 四仓、CHAIN、svc_org_base、抄旧 S3-L01。

禁止 force。commit [agent:data-agent]。
```
