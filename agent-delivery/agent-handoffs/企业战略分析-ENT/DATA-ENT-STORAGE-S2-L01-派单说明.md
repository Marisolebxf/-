# DATA-ENT-STORAGE-S2-L01 · 派单说明

> **日期**：2026-08-12  
> **阶段**：企业维存储 **S2**（sources / etl / seeds 清单落地）  
> **前置**：`ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01` = **done**（流图已 approved）  
> **Task ID**：`DATA-ENT-STORAGE-S2-L01`（registry · **ready**）  
> **执行 Agent**：`data-agent`  
> **建议监管**：`human:徐滕强`（数据/架构；以名册为准）· 知会 Demo 工程 / GDF  
> **强度**：ponytail **lite**（文档与指针清单；不灌 as-built、不写业务服务代码）

---

## 1. 目标

在流图会签通过后，把 **入站边界、ETL/Demo 管道指针、少量覆盖样例矩阵** 写实，关闭或推进开放项，使 S3（`stores/*` as-built）与 Demo 全链路工程可并行开工。

**Demo 主路径（已批准，不得改拓扑）**：

```text
LLM Mock → demo_* ODS（结构=三方在线约定文档，非现网 as-built）
        → ETL 调度模拟 GDF
        → demo_* DWD → ADS / ES / Nebula(demo_**) / MinIO(demo_**)
```

---

## 2. 必读（按序）

| 序 | 路径 |
|---:|---|
| 1 | `data-design/storage/README.md`（§5.1 Demo/Mock） |
| 2 | `data-design/storage/ENT/01-data-flow.md`（§1–3 + **§7**） |
| 3 | `data-design/storage/ENT/etl/pipeline-demo-mock.md`（**approved** 口径） |
| 4 | `data-design/storage/ENT/sources/README.md` |
| 5 | `architecture-baseline.md`（D3/D7） |
| 6 | handoff：`ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01.md`（开放项 OPEN-01~07） |

---

## 3. 交付清单（DoD）

### A. sources（关 OPEN-ENT-FLOW-05）

- [ ] `sources/inventory.md`：企业维依赖的 ODS **表级**清单（约定表名 + 一句话用途 + 落入 DWD/其它）
- [ ] 每行或文首给出 **三方在线约定文档**入口（URL 或仓内镜像路径）
- [ ] 注明：Demo 建表/Mock **不以**现网三方 as-built 为准；现网差异可写备注列

### B. Demo Mock 入口（关 OPEN-ENT-FLOW-06）

- [ ] 在 `etl/pipeline-demo-mock.md` §4 填实：
  - `demo_*` **库 / MinIO 桶 / Nebula space** 命名表
  - **LLM Mock** 脚本仓与入口命令/路径
- [ ] 不改 §1 拍板口径；不另造加工拓扑

### C. ETL 工厂管道指针（推进/关闭 OPEN-ENT-FLOW-01）

在下列文件写清「作业意图 + 调度/DAG 名或脚本路径」（禁止大段 SQL）：

| 文件 | 要点 |
|---|---|
| `etl/pipeline-ods-to-dwd.md` | 正式 GDF + Demo 模拟调度复用关系 |
| `etl/pipeline-dwd-to-ads.md` | ADS 写出；Java 只读 |
| `etl/pipeline-dwd-to-es.md` | 指向 `lumen-etl-es-py` 等真实入口 |
| `etl/pipeline-to-nebula.md` | Python 写图；禁 Java nGQL |
| `etl/pipeline-to-minio.md` | 本域前缀 + 任务表对照（**OPEN-ENT-FLOW-03**） |

能关 OPEN-01 则关；缺现网参数则保留开放项并写「阻塞原因」。

### D. seeds（关 OPEN-ENT-FLOW-07）

- [ ] `seeds/README.md` 覆盖矩阵：至少覆盖检索 / 详情 / 风险 / 汇总 / 报告对象等关键场景 × 代表性数据特点
- [ ] 每行有脚本或生成入口；强调**少量**、先闭环后性能

### E. handoff

路径：`agent-delivery/agent-handoffs/企业战略分析-ENT/DATA-ENT-STORAGE-S2-L01.md`

含：开放项关闭表、命名表摘要、下游 S3 是否可开工、`ponytail: lite`、cost 四字段。

---

## 4. 明确不做

- 不改 `data-design/企业/*` legacy  
- **不灌** `stores/*` as-built（**S3**）  
- 不写 Java / 前端 / 算法业务代码  
- 不把「直写 ADS」写成全链路主路径  
- 不以现网三方库结构覆盖在线约定文档  

---

## 5. 开放项对照

| ID | 本单目标 |
|---|---|
| OPEN-ENT-FLOW-05 | **关闭**（在线约定文档入口 + inventory） |
| OPEN-ENT-FLOW-06 | **关闭**（demo_* 命名 + LLM 入口） |
| OPEN-ENT-FLOW-07 | **关闭**（seeds 矩阵） |
| OPEN-ENT-FLOW-01 | **关闭或推进**（调度/DAG 指针） |
| OPEN-ENT-FLOW-03 | **关闭或推进**（MinIO 本域前缀） |
| OPEN-ENT-FLOW-02 / 04 | 可知会；不强制本单关闭（平台 / SLA） |

---

## 6. 会话提示词（可贴）

```text
/goal DATA-ENT-STORAGE-S2-L01
角色：data-agent
监管：human:徐滕强（或名册数据 Lead）
前置：ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01=done
强度：ponytail lite
必读：storage/README.md §5.1 → ENT/01-data-flow.md §7 → etl/pipeline-demo-mock.md → sources/README.md
交付：
  1) sources/inventory.md + 三方在线约定文档入口（关 OPEN-05）
  2) pipeline-demo-mock：demo_* 命名表 + LLM Mock 入口（关 OPEN-06）
  3) etl 各 pipeline：调度/脚本指针；pipeline-to-minio 本域前缀（推进 OPEN-01/03）
  4) seeds/README.md 覆盖矩阵（关 OPEN-07）
  5) handoff DATA-ENT-STORAGE-S2-L01.md
禁止：改旧 data-design/企业/*；灌 stores as-built（S3）；写业务代码；以现网三方 as-built 当 Demo ODS 真源；用直写 ADS 冒充全链路
Demo 主路径不可改：LLM→约定 ODS→ETL 模拟 GDF→demo_* 下游
```

---

## 7. 认领

```text
task-claim id=DATA-ENT-STORAGE-S2-L01
claimed_by=agent:data-agent
supervised_by=human:徐滕强
```

确认监管人后由执行方 claim → `in_progress`。
