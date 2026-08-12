# 企业维 · 存储设计文件体系规范（草案）

> **状态**：草案（2026-08-12）  
> **范围**：企业维（ENT）存储与数据工程文档；**不含**功能设计 / Wireframe / USM  
> **流图会签 Owner**：架构师  
> **现有** `data-design/企业/*` **旧稿不动**；本树并行新建，冲突时以本树为准（待 stub 切换）

---

## 1. 已拍板决策

| # | 议题 | 决定 |
|---|---|---|
| 1 | 目录根 | `agent-delivery/data/data-design/storage/`；企业维 = `storage/ENT/` |
| 2 | ADS | **必须**进入本树（契约面是存储设计的一部分） |
| 3 | MinIO | **平台级一份** + 企业维 **引用**（不复制平台正文） |
| 4 | 数据流图会签 | **架构师** |
| 5 | Demo / Mock 与正式 | **同一套 `stores/*` 结构**；落 `demo_*` 库 / MinIO `demo_**` 桶 / Nebula `demo_**`。**主路径**：ETL 调度**模拟 GDF**；**LLM 完整按三方在线约定表结构**写 Mock→**ODS**（**不以**现网三方 as-built 为准，屏蔽进度不一致）；少量覆盖样例、**先全链路闭环后性能**。禁止平行契约面；直写 ADS 仅为旁路 |
| 6 | 三方 ODS 真源 | **`doc/` xlsx = 权威唯一真源**；**日常优先读 `doc/md-extract/`**（自 Excel 抽取）；`gkx-mysql-raw` / Wave A 仅对账或施工镜像 |

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
└── ENT/
    ├── README.md                      # ★ 企业维唯一入口（读序）
    ├── CHANGELOG.md
    ├── 00-context.md                  # 边界、铁律、与基线对齐
    ├── 01-data-flow.md                # ★ 主/子数据流（Mermaid）；架构师会签
    ├── sources/
    │   ├── README.md
    │   └── inventory.md               # 企业维依赖的 ODS 表级清单
    ├── etl/
    │   ├── README.md
    │   ├── pipeline-demo-mock.md      # ★ Demo：LLM→约定 ODS→ETL 模拟 GDF
    │   ├── pipeline-mock-to-ads.md    # 可选旁路：直写 ADS（D7）
    │   ├── pipeline-ods-to-dwd.md
    │   ├── pipeline-dwd-to-ads.md
    │   ├── pipeline-dwd-to-es.md
    │   ├── pipeline-to-nebula.md
    │   └── pipeline-to-minio.md       # 引用 platform/minio.md + 企业对象前缀
    ├── seeds/                         # 少量覆盖样例索引（非第二套 DDL、非性能全量）
    │   └── README.md
    └── stores/
        ├── mysql/
        │   ├── README.md
        │   ├── dwd-entity.md
        │   ├── dwd-risk.md
        │   ├── dwd-aggregate.md
        │   ├── ads.md                 # 必须
        │   └── dim.md
        ├── elasticsearch/
        │   ├── index-enterprise.md
        │   └── sync.md
        └── nebula/
            └── graph-enterprise.md
```

**写作顺序（强制）**：`00-context` → **`01-data-flow`（架构师会签）** → `sources` → `etl` → `stores`。无会签流图不得扩写细表为「已批准」。

---

## 4. 真源优先级（模型必读）

```text
1. storage/README.md + storage/ENT/README.md
2. ENT/01-data-flow.md          （流图；架构师会签态）
3. ENT/stores/**                （落库 / 索引 / 图谱结构）
4. ENT/etl/** + sources/**      （工厂与入站边界）
5. storage/platform/minio.md    （对象存储；ENT 只引用）
6. data-design/企业/*           （legacy 并行；冲突以 storage/ENT 为准）
```

指标 8 件套仍以 `metrics/*` + `data-lineage-policy.md` 为准；本树只提供 `source_tables` 可指到的物理存储。

---

## 5. 四存储职责矩阵（企业维）

| 存储 | 角色 | 谁写 | 谁读 | 文档位置 |
|---|---|---|---|---|
| MySQL ODS（供应库视角） | 贴源 | 正式：三方入站；**Demo：LLM 按 `doc/` 约定写 `demo_*` ODS** | ETL（正式 GDF / Demo 模拟调度） | `sources/` + **`doc/md-extract/`（优先读）/ `doc/` xlsx（权威）** |
| MySQL DWD | 清洗标准明细/汇总 | GDF/ETL（Demo 同构调度） | ETL、算法（按需） | `stores/mysql/dwd-*.md` |
| MySQL ADS | **契约面** | Python / 工厂写出（Demo 经模拟 GDF；可选直写旁路） | **Java 只读** | `stores/mysql/ads.md` |
| MySQL DIM | 码表/字典 | 数据任务 | 服务/ETL | `stores/mysql/dim.md` |
| Elasticsearch | 检索派生 | ETL/Python | 经 Java→Python 或约定门面 | `stores/elasticsearch/` |
| NebulaGraph | 图谱主存 | Python（Demo 落 `demo_**` space） | Python（Java 禁直连 nGQL） | `stores/nebula/` |
| MinIO | 对象/报告资产 | 编排/Python（Demo 落 `demo_**` 桶） | 下载门面 | `platform/minio.md` + ENT etl 引用 |

### 5.1 Demo / Mock 与正式（结构合一 · 实例隔离）

| 层 | 约定 |
|---|---|
| 结构真源 | **仅** `ENT/stores/**`（Demo 与正式共用）；改表只改此处 |
| ODS 字段口径 | **权威** = `third-party-source/doc/` xlsx；**优先读取** = `doc/md-extract/`（自 Excel 抽取）；**不以**现网 `gkx-mysql-raw` as-built 为建表真源 |
| Demo 主路径 | **LLM Mock → `demo_*` ODS → ETL 调度模拟 GDF →** 下游 DWD/ADS/ES/Nebula/`demo_**` MinIO；文档：`etl/pipeline-demo-mock.md` |
| 样本策略 | 少量覆盖数据特点与场景；**先全链路闭环，后性能**；索引见 `seeds/` |
| 读路径 | 同一：前端 → Java → ADS（+ Feign）；不因 Demo 另开读模型 |
| 可区分 | `demo_*` **实例/桶/space**、数据内容、指标 D4=`mock`/`live`；**不可**第二套表结构 |
| 可选旁路 | 不跑工厂时 Python 直写 ADS（`pipeline-mock-to-ads.md` / D7）；不替代全链路验收 |
| 禁止 | `storage/ENT-demo` 平行树；`demo_ads_*` 平行契约；前端/Java 造假；Mock 以现网三方 as-built 为准 |

与基线 D7 关系：契约面仍冻结于 ADS；Demo 用「约定 ODS + 模拟工厂」稳定输入，正式三方就绪后切换真实入站，**上层读模型零改**。

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

## 7. 与旧稿映射（迁移时用，旧文件暂不改）

| 旧路径（legacy） | 新路径 |
|---|---|
| `企业/DWD…工商表-MySQL-v3.1.md` | `ENT/stores/mysql/dwd-entity.md` |
| `企业/DWD…指标汇总表-MySQL-v3.1.md` | `ENT/stores/mysql/dwd-aggregate.md` |
| `企业/DWD…模块-MySQL-v3.0.md` | `dwd-risk` + 部分 etl/flow；API 映射外链 |
| `企业/企业搜索-ES*.md` | `ENT/stores/elasticsearch/*` |
| 重点/深圳**功能设计** | **不迁入**；归档产品侧 |
| PG 大稿 | 已在 `_archive`；禁止作现行真源 |

---

## 8. 落地阶段

| 阶段 | 产出 | Owner |
|---|---|---|
| S0（本草案） | `storage/README.md` + 骨架 | 讨论确认 |
| S1 | `ENT/00-context` + **`01-data-flow` 会签** | 架构师 / 淮政玮（已 approved 2026-08-12） |
| S2 | `sources`（含在线约定文档入口）+ `etl`（**`pipeline-demo-mock` 主路径** + 工厂管道 + 可选 ADS 旁路）+ `seeds` 覆盖矩阵 | 数据 Lead / GDF / Demo |
| S3 | `stores/mysql|es|nebula` 从现网 as-built 灌入（Demo/正式共用结构；Demo 实例仍用 `demo_*`） | data-agent |
| S4 | 旧路径 stub 指向本树 | coordinator |

---

## 9. 变更

| 日期 | 说明 |
|---|---|
| 2026-08-12 | 初稿：锁定 storage/ENT、ADS 必含、MinIO 平台级+引用、流图架构师会签 |
| 2026-08-12 | 决策 #5：Demo/Mock 与正式**共用 stores**；增 §5.1 与目录 `pipeline-mock-to-ads` / `seeds/` |
| 2026-08-12 | **澄清 Demo 主路径**：LLM→约定在线 ODS→ETL 模拟 GDF；落 `demo_*` 库/桶/Nebula；少量覆盖、先闭环；增 `pipeline-demo-mock.md`；ADS 直写降为旁路 |
| 2026-08-12 | **决策 #6**：三方 ODS 权威 = `doc/` xlsx；**优先读** `doc/md-extract/` |
| 2026-08-12 | S3：`stores/*` as-built 灌入（draft）· `DATA-ENT-STORAGE-S3-L01` |
