# 存储设计文件体系规范（草案）

> **状态**：草案（2026-08-12；**2026-08-13 增 CHAIN**；**2026-08-17 决策 #7 一张 G 签收**；**2026-08-18 范围 3 停机删除 `storage/SVC/`**；**2026-08-19 SVC S1 流图会签 approved**）  
> **范围**：企业维（ENT）+ 产业链维（CHAIN）+ 服务机构维（SVC，流图已会签、细表未建）存储与数据工程文档；**不含**功能设计 / Wireframe / USM  
> **流图会签 Owner**：架构师（ENT：`human:淮政玮`；CHAIN：`human:李伟`；SVC：`human:淮政玮` · **approved 2026-08-19**）  
> **现有** `data-design/企业|产业链|服务机构/*` **旧稿并行**；冲突时以本树 `storage/{ENT|CHAIN}` 为准；SVC 冲突以 **`storage/SVC/01-data-flow.md`** 为准（细表未建，旧稿勿当建表真源）。

---

## 1. 已拍板决策

| # | 议题 | 决定 |
|---|---|---|
| 1 | 目录根 | `agent-delivery/data/data-design/storage/`；企业维 = `storage/ENT/`；产业链维 = `storage/CHAIN/` |
| 2 | ADS | **必须**进入本树（契约面是存储设计的一部分） |
| 3 | MinIO | **平台级一份** + 企业维 **引用**（不复制平台正文） |
| 4 | 数据流图会签 | **架构师** |
| 5 | Demo / Mock 与正式 | **同一套 `stores/*` 结构**；落 `demo_*` 库 / MinIO `demo_**` 桶 / Nebula `demo_**`。**主路径**：ETL 调度**模拟 GDF**；**LLM 完整按三方在线约定表结构**写 Mock→**ODS**（**不以**现网三方 as-built 为准，屏蔽进度不一致）；少量覆盖样例、**先全链路闭环后性能**。禁止平行契约面；直写 ADS 仅为旁路 |
| 6 | 三方 ODS 真源 | **`doc/` xlsx = 权威唯一真源**；**日常优先读 `doc/md-extract/`**（自 Excel 抽取）；`gkx-mysql-raw` / Wave A 仅对账或施工镜像 |
| 7 | 一张 G | **从建库起就是一张 `G_科创`**（七要素本体、产业链为底图；展示/专题是窗口，不是第二张图）。**没有「二期并库」**。Demo 物理落点 = Nebula **`demo_gkx_chain`**（正式 **`gkx_chain`**）。企业/机构/政策/服务挂接投影进这张底图，跨域只保证 **DWD 主键对齐**（hang：`org_id` ↔ `node_id`）。现网 `entan` / `gkx_policy` 等是模块联调 as-built，**不是**目标态分域、也不是以后再并。禁止另起 `gkx_topic`「汇总二期」space。Tag/Edge 细表仍 draft。**签收** `human:淮政玮` · 2026-08-17 |

另约定（延续讨论）：

- 文件名 **禁止版本号**；版本写 frontmatter（`version` / `updated` / `status`）
- 关系库 **仅 MySQL**；文档与图中 **禁止 PostgreSQL / PG / `dwd.` PG schema**
- **功能设计不进本树**（重点/深圳功能设计等应归档到产品侧，本树不迁入）
- Demo 仓只放灌数/调度入口；表结构语义回链本树 `stores/*`；**ODS 字段口径**权威回链 `doc/` xlsx，**查阅优先** `doc/md-extract/`（决策 #6）
- 可选旁路：不跑工厂时 Python 直写 ADS（D7）——不替代 Demo 全链路主路径

---

## 2. 本体系回答什么

| 回答 | 不回答 |
|---|---|
| 企业维数据存在哪、结构、谁写谁读 | 页面交互、功能验收、产品 Wireframe |
| 第三方源边界、ETL、端到端数据流 | 全量供应库字段抄录（指向 `third-party-source`） |
| MySQL（ODS 视角/DWD/ADS/DIM）· ES · Nebula · MinIO（引用） | Java REST 字段别名细表（可外链 API 契约） |

对齐 `architecture-baseline.md`：调用链前端→Java→Python；Java **只读 ADS**；Python 写 ADS/Nebula/ES；图谱 = NebulaGraph；三方经数据工厂 `ODS → DWD → ADS`。

---

## 3. 目录架构（稳定路径 = 契约）

```text
data/data-design/storage/
├── README.md                          # 本规范 + 全平台入口
├── platform/
│   └── minio.md                       # ★ 平台级 MinIO（唯一正文）
├── ENT/                               # 企业维（已 S1–S4）
│   └── …                              # 见 ENT/README.md
├── CHAIN/                             # 产业链维（同构）
│   └── …                              # 见 CHAIN/README.md
├── SVC/                               # 服务机构维（S1 流图会签中 · 细表未建）
│   └── 00-context.md / 01-data-flow.md
```

**写作顺序（强制）**：`00-context` → **`01-data-flow`（架构师会签）** → `sources` → `etl` → `stores`。无会签流图不得扩写细表为「已批准」。  
域入口：[`ENT/README.md`](./ENT/README.md) · [`CHAIN/README.md`](./CHAIN/README.md) · [`SVC/README.md`](./SVC/README.md)（会签 pending）。

---

## 4. 真源优先级（模型必读）

```text
1. storage/README.md + storage/{ENT|CHAIN|SVC}/README.md
2. {域}/01-data-flow.md         （流图；架构师会签态）
3. {域}/stores/**               （落库 / 索引 / 图谱结构）
4. {域}/etl/** + sources/**     （工厂与入站边界）
5. storage/platform/minio.md    （对象存储；域内只引用）
6. data-design/企业|产业链|服务机构/*    （legacy 并行；冲突以 storage/{ENT|CHAIN} 为准；SVC 流图以 storage/SVC 为准）
```

指标 8 件套仍以 `metrics/*` + `data-lineage-policy.md` 为准；本树只提供 `source_tables` 可指到的物理存储。

---

## 5. 四存储职责矩阵（ENT / CHAIN 同构）

| 存储 | 角色 | 谁写 | 谁读 | 文档位置 |
|---|---|---|---|---|
| MySQL ODS（供应库视角） | 贴源 | 正式：三方入站；**Demo：按 `doc/` 约定写 `demo_*` ODS** | ETL（正式 GDF / Demo 模拟调度） | 各域 `sources/` + **`doc/md-extract/`（优先读）/ `doc/` xlsx（权威）** |
| MySQL DWD | 清洗标准明细/汇总 | GDF/ETL（Demo 同构调度） | ETL、算法（按需） | 各域 `stores/mysql/` |
| MySQL ADS | **契约面** | Python / 工厂写出（Demo 经模拟 GDF；可选直写旁路） | **Java 只读** | 各域 `stores/mysql/ads.md` |
| MySQL DIM | 码表/字典 | 数据任务 | 服务/ETL | 各域 `stores/mysql/dim.md` |
| Elasticsearch | 检索派生 | ETL/Python | 经 Java→Python 或约定门面 | 各域 `stores/elasticsearch/` |
| NebulaGraph | **一张 G** 主存（决策 #7） | Python（Demo 落 **`demo_gkx_chain`**） | Python（Java 禁直连 nGQL） | 各域 `stores/nebula/`；口径见 §5.2 |
| MinIO | 对象/报告资产 | 编排/Python（Demo 落 `demo_**` 桶） | 下载门面 | `platform/minio.md` + 各域 etl 引用 |

### 5.1 Demo / Mock 与正式（结构合一 · 实例隔离）

| 层 | 约定 |
|---|---|
| 结构真源 | **仅** 各域 `stores/**`（Demo 与正式共用）；改表只改此处 |
| ODS 字段口径 | **权威** = `third-party-source/doc/` xlsx；**优先读取** = `doc/md-extract/`（自 Excel 抽取）；**不以**现网 `gkx-mysql-raw` as-built 为建表真源 |
| Demo 主路径 | **LLM Mock → `demo_*` ODS → ETL 调度模拟 GDF →** 下游 DWD/ADS/ES/Nebula/`demo_**` MinIO；文档：`etl/pipeline-demo-mock.md` |
| 样本策略 | 少量覆盖数据特点与场景；**先全链路闭环，后性能**；索引见 `seeds/` |
| 读路径 | 同一：前端 → Java → ADS（+ Feign）；不因 Demo 另开读模型 |
| 可区分 | `demo_*` **实例/桶/space**、数据内容、指标 D4=`mock`/`live`；**不可**第二套表结构 |
| 可选旁路 | 不跑工厂时 Python 直写 ADS（`pipeline-mock-to-ads.md` / D7）；不替代全链路验收 |
| 禁止 | `storage/{域}-demo` 平行树；`demo_ads_*` 平行契约；前端/Java 造假；Mock 以现网三方 as-built 为准 |

与基线 D7 关系：契约面仍冻结于 ADS；Demo 用「约定 ODS + 模拟工厂」稳定输入，正式三方就绪后切换真实入站，**上层读模型零改**。

### 5.2 一张 G（Nebula · 建库口径）

SAD 真源：`agent-handoffs/产品整体定义/跨系统-知识图谱/`（**只建一张图**）。引擎表：`graph-engine.md` §3.1。瘦工作区开仓说明：`workspaces/README.md`。

```text
展示六模块 / 专题全景     = 窗口（只读同一张 G）
                │
                ▼
     一张 G  ·  demo_gkx_chain / gkx_chain
     底图 = 产业链环节；其余六要素挂在底图或彼此之间
```

| 项 | 口径 |
|---|---|
| 建库 | **一开始就是这一张**；灌数据 / 投影往 `demo_gkx_chain` 写底图 + 挂接 |
| 企业上链 | MySQL `enterprise_industry_chain` + `industry_chain_entity_rel`（`entity_id=org_id`）；Nebula 投影进 **同一张 G**，fail-soft |
| 现网多 space | `entan`、`gkx_policy` 等 = 模块联调 as-built；施工禁止按「先分库、二期 `gkx_topic` 再并」 |
| 禁止 | 新建 space 名 `chain`；发明 `chain_link`；把 ENT/SVC 模型复制成第二张七要素图 |

---

## 6. 单文件约定

Frontmatter 示例：

```yaml
---
doc_id: ENT-STORAGE-FLOW
element: ENT
role: data-flow          # context|data-flow|source|etl|store-mysql|store-es|store-nebula|store-minio-ref
status: draft            # draft | architect_review | approved
version: "2026-08-12"
updated: 2026-08-12
engine: null             # mysql|elasticsearch|nebula|minio|multi
signoff_owner: architect # 流图类必填
---
```

- 数据流：**Mermaid 必选**；每图附 `生产者|消费者|触发|失败语义|禁止事项`
- ETL 正文写作业意图与仓内脚本路径，**不粘贴大段 SQL**
- 表结构变更：改对应 `stores/*` + 记 `CHANGELOG.md`；**不改文件名**

---

## 7. 与旧稿映射（S4 已 stub）

| 旧路径（`data-design/企业/`） | 现行入口 |
|---|---|
| 目录首页 | [`企业/README.md`](../企业/README.md) → **`storage/ENT`** |
| `DWD…工商表-MySQL-v3.1.md` | 导航 [`ENT/stores/mysql/dwd-entity.md`](./ENT/stores/mysql/dwd-entity.md)；DDL 正文仍在旧文件 |
| `DWD…指标汇总表-MySQL-v3.1.md` | [`dwd-aggregate.md`](./ENT/stores/mysql/dwd-aggregate.md) |
| `DWD…模块-MySQL-v3.0.md` | [`dwd-risk.md`](./ENT/stores/mysql/dwd-risk.md)（+ 部分非风险见该 DDL） |
| `企业搜索-ES*.md` | [`ENT/stores/elasticsearch/*`](./ENT/stores/elasticsearch/) |
| PG 大稿 / 域设计 v1 / vs-demo / 详细设计 | stub → storage/ENT + `_archive/.../data-design-企业-legacy/` |
| 重点/深圳**功能设计** | **不迁入 storage**；文首已标明；仍留本目录 |

冲突时以 **`storage/ENT`** 为准。

### 服务机构（`data-design/服务机构/` · 历史对照）

`storage/SVC/` 于 2026-08-18 `DEMO-SVC-ABORT-L01` 范围 3 删除后，**2026-08-19** 按阶段 F 总控重建：流图 [`SVC/01-data-flow.md`](./SVC/01-data-flow.md) **approved**（`human:淮政玮`）。S2 已写 sources/etl/seeds **指针**（`DATA-SVC-STORAGE-S2-L02`）。**细表 / stores 未建**（S3）。仍禁止 F-SEED。本目录旧稿仅历史对照。

| 旧路径 | 说明 |
|---|---|
| 目录首页 | [`服务机构/README.md`](../服务机构/README.md)（历史对照） |
| `服务机构域数据库设计(v1).md` | 历史 DWD/ADS 稿；勿作建表真源 |
| `SVC-DATA-ANALYSIS-L01-数据分析报告.md` | **legacy 分析纪要**；开放项 → 客户决策清单 §2.ae |

---

## 8. 落地阶段

| 阶段 | 产出 | Owner |
|---|---|---|
| S0（本草案） | `storage/README.md` + 骨架 | 讨论确认 |
| S1 | `ENT/00-context` + **`01-data-flow` 会签** | 架构师 / 淮政玮（已 approved 2026-08-12） |
| S2 | `sources`（含在线约定文档入口）+ `etl`（**`pipeline-demo-mock` 主路径** + 工厂管道 + 可选 ADS 旁路）+ `seeds` 覆盖矩阵 | 数据 Lead / GDF / Demo |
| S3 | `stores/mysql|es|nebula` 从现网 as-built 灌入（Demo/正式共用结构；Demo 实例仍用 `demo_*`） | **done** · `DATA-ENT-STORAGE-S3-L01` |
| S4 | 旧路径 stub 指向本树 | **done** · `DATA-ENT-STORAGE-S4-L01` |
| SVC S1 | `SVC/00-context` + **`01-data-flow` 会签**（`ARCH-SVC-STORAGE-S1-L02`） | **approved** · `human:淮政玮` · 2026-08-19 |
| SVC S2 | `SVC/sources` + `etl/pipeline-demo-mock` + `seeds` 指针（`DATA-SVC-STORAGE-S2-L02`） | **draft 指针** · 2026-08-19；细表未建、未灌数 |
| SVC 停机 | 同构目录曾按范围 3 删除（`DEMO-SVC-ABORT-L01`） | 2026-08-18（历史） |

---

## 9. 变更

| 日期 | 说明 |
|---|---|
| 2026-08-12 | 初稿：锁定 storage/ENT、ADS 必含、MinIO 平台级+引用、流图架构师会签 |
| 2026-08-12 | 决策 #5：Demo/Mock 与正式**共用 stores**；增 §5.1 与目录 `pipeline-mock-to-ads` / `seeds/` |
| 2026-08-12 | **澄清 Demo 主路径**：LLM→约定在线 ODS→ETL 模拟 GDF；落 `demo_*` 库/桶/Nebula；少量覆盖、先闭环；增 `pipeline-demo-mock.md`；ADS 直写降为旁路 |
| 2026-08-12 | **决策 #6**：三方 ODS 权威 = `doc/` xlsx；**优先读** `doc/md-extract/` |
| 2026-08-12 | S3：`stores/*` as-built 灌入（draft）· `DATA-ENT-STORAGE-S3-L01` |
| 2026-08-12 | S4：旧 `data-design/企业` stub → `storage/ENT` · `DATA-ENT-STORAGE-S4-L01` |
| 2026-08-13 | 增 **CHAIN** 同构域 `storage/CHAIN/`（S1 `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01`）；ODS 真源同决策 #6；Demo ODS=`demo_gkxlumenx_ods` |
| 2026-08-17 | **决策 #7 签收**（`human:淮政玮`）：一张 G 从建库起即是；废止「二期 `gkx_topic` 并库」；Demo 落点 `demo_gkx_chain` |
| 2026-08-18 | **范围 3 停机**：删除 `storage/SVC/`（`DEMO-SVC-ABORT-L01`）；服务机构旧稿改历史对照 |
| 2026-08-19 | **SVC S2 指针**：`sources/inventory` + `etl/pipeline-demo-mock` + `seeds`（`DATA-SVC-STORAGE-S2-L02`）；仍禁止 F-SEED |
