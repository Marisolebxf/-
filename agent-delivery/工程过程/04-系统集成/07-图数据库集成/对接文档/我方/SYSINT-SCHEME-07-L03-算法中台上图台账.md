# SYSINT-SCHEME-07-L03 · 算法中台各要素上图台账

> **任务**：`SYSINT-SCHEME-07-L03`（WBS-07-00B）
> **监管人 / 认领人**：human:郭万迎
> **完成日期要求**：2026-11-09（WBS-07-00 出门日）
> **创建时间**：2026-10-27

## 一、目的与口径

### 1.1 本文件是什么

本文件是**算法中台侧七要素上图能力台账**。以七个要素为轴，逐要素盘点「有哪些真实写图流水线代码入口、写出了哪些实体和边、cfg_metric 定义存在但未上线的指标有多少」。

它回答的问题是：**「算法中台在 Nebula 图数据库里真实写出了什么、哪些只是定义没上线」**。

### 1.2 核心判定规则（来自 DoD）

| 判定 | 含义 | DoD 依据 |
|---|---|---|
| ✅ **真实已跑通** | 代码仓库有真实写图入口（`INSERT VERTEX / INSERT EDGE` nGQL），且有实体 TAG 和关系 EDGE 的硬编码或映射逻辑 | 「已实现必须指出代码入口」 |
| 🔶 **定义存在但未上线** | cfg_metric seed 文件有 metric_id 定义，但 `is_mock: true`，算法服务 readiness matrix D4 全 mock，无真实写图代码入口 | 「指标 seed 与 D4 mock 不算已实现」 |
| 🔴 **仅描述** | cfg_model_registry 有架构定义但无真实配置，或 cfg_metric seed 完全空白 | 「设计中单独标注，不写成已实现」 |

### 1.3 与 L04 的边界区分

| 维度 | L03 本文件（算法中台） | L04（燕大侧） |
|---|---|---|
| 写的是谁 | 算法中台写 Nebula 的流水线代码 | 燕大 Platform Schema 抽取链 |
| 图空间 | demo_gkx_chain / demo_gkx_ent 等 demo 空间 | gkx_local_1 / gkx_full_1 平台空间 |
| 判定基准 | **代码仓库有真实写图 nGQL** | **燕大快照 1.2 节现状判定** |
| 两个系统的关系 | 算法中台是展示系统**自研的** Nebula 图 | 燕大是**对接的外部**知识图谱 |

### 1.4 代码仓库盘点（repos/ 已 clone）

| 仓库 | 路径 | 内容 |
|---|---|---|
| lumen-algo-py | `repos/lumen-algo-py/` | **主仓**（完整 monorepo，含核心算法 + vendor 子仓 + gateway） |
| demo-algo-ent-analysis | `repos/demo-algo-ent-analysis/` | 企业/产业/政策算法（已迁入 lumen-algo-py vendor） |
| demo-algo-science | `repos/demo-algo-science/` | 产业链/科学算法（已迁入 lumen-algo-py vendor） |
| demo-svc-topic-py | `repos/demo-svc-topic-py/` | 主题平台（含 Nebula 查询入口，只读不写） |
| demo-svc-platform | `repos/demo-svc-platform/` | Java 服务平台（图查询 API 透传） |
| lumen-svc-platform | `repos/lumen-svc-platform/` | 线上 Java 服务平台 |

**关键澄清**：之前记忆记录「lumen-algo-py 未 clone 是空壳」——**已修正**：lumen-algo-py 是完整 monorepo，含 60+ Python 源码文件，不是空壳。

### 1.5 cfg_metric 种子文件全局统计

> 11 个种子文件，579 条 metric_id，580 条 `is_mock: true`（几乎 100% mock）。

| 种子文件 | metric_id 数 | is_mock=true 数 | mock 比例 | 对应要素 |
|---|---:|---:|---:|---|
| cfg_metric-INNOV-seed.yaml | 143 | 144 | 100% | 创新（企业） |
| cfg_metric-CHAIN-seed.yaml | 100 | 101 | 100% | 产业链 |
| cfg_metric-ENT-seed.yaml | 96 | 97 | 100% | 企业实体 |
| cfg_metric-SVC-seed.yaml | 51 | 52 | 100% | 服务机构 |
| cfg_metric-SYNTH-seed.yaml | 46 | — | — | 综合 |
| cfg_metric-TECH-seed.yaml | 39 | 40 | 100% | 技术 |
| cfg_metric-POLICY-seed.yaml | 35 | 36 | 100% | 政策 |
| cfg_metric-TALENT-seed.yaml | 32 | 33 | 100% | 人才 |
| cfg_metric-ORG-seed.yaml | 22 | 23 | 100% | 科研机构 |
| cfg_metric-COMMON-seed.yaml | 1 | 2 | 100% | 公共 |
| cfg_metric-TNIE-seed.yaml | 1 | — | — | — |
| **合计** | **579** | **580** | **≈100%** | — |

---

## 二、要素 1 · 产业

### 2.1 三态判定

**✅ 真实已跑通**——有真实 Nebula 写图代码入口。

### 2.2 过程名与仓与入口

| 过程 | 仓 | 入口函数 | 写图方式 |
|---|---|---|---|
| 产业链图构建 | lumen-algo-py | `lumen_common/algorithms/chain/graph_project.py:204-369` `map_graph()` | 把 DWD 链路/节点/企业/机构行映射为 vertices/edges 列表 |
| 产业链 Nebula 写入 | lumen-algo-py | `lumen_common/algorithms/chain/graph_project.py:411-507` `NebulaSink` 类 | `ensure_schema()` 创建 space/tag/edge；`upsert()` 调用 `_insert_vertices()` / `_insert_edges()` 生成并执行 `INSERT VERTEX / INSERT EDGE` nGQL |
| 产业链增量写图 | lumen-algo-py | `vendor/innov-py/chainan/graph/build.py` | 增量 upsert |
| 产业域 Nebula loader | demo-algo-science | `chainan/graph/nebula_project.py:286-485` | 把 DWD 数据映射为 Nebula 节点/边，生成 `INSERT VERTEX / INSERT EDGE` |

### 2.3 写出的点边

| 实体 TAG | 来源表 | 对应 L02 对齐轴 |
|---|---|---|
| `chain`（产业链） | DWD chain 表 | 对应 IndustryChain |
| `segment`（产业环节/节点） | DWD node 表 | 对应 IndustryNode |
| `enterprise`（企业） | DWD 企业表 | 对应 enterprise |
| `institution`（机构） | DWD 机构表 | 对应 institution |

| 关系 EDGE | 起→终 | 对应 L02 对齐轴 | 备注 |
|---|---|---|---|
| `belongs_to` | segment → chain | 对应 HAS_NODE | — |
| `participates` | enterprise/institution/service_institution → segment | 对应 BELONGS_TO_NODE | — |
| `supplies` | enterprise → enterprise | — | 常量已定义，但 graph_project.py OPEN_ITEMS 注明「Demo DWD 无该结构，本单不造边」 |
| `depends_on` | segment → segment | 对应 CHILD_OF / DOWNSTREAM_OF | — |

### 2.4 证据路径

- 主代码：`e:\gkx-lumen\repos\lumen-algo-py\lumen_common\algorithms\chain\graph_project.py`
- NebulaSink 类：第 411-507 行，含 `INSERT VERTEX` / `INSERT EDGE` nGQL 生成逻辑
- 验证守卫：第 101-117 行 `demo_guard.py` 限制只能写 `demo_` 开头的 Nebula space

### 2.5 cfg_metric 种子文件

| 文件 | metric_id 数 | is_mock | 说明 |
|---|---:|---:|---|
| cfg_metric-CHAIN-seed.yaml | 100 | 全部 is_mock=true | 指标定义存在但算法服务 D4 全 mock |

---

## 三、要素 2 · 企业

### 3.1 三态判定

**✅ 真实已跑通**——有真实 Nebula 写图代码入口（批量灌图 + 增量写图）。

### 3.2 过程名与仓与入口

| 过程 | 仓 | 入口函数 | 写图方式 |
|---|---|---|---|
| 企业批量灌图 | lumen-algo-py | `vendor/entan-py/entan/graph/nebula_loader.py:46-127` | `ensure_schema()` 创建 Nebula space/tag/edge；`_load_nodes()` / `_load_edges()` 批量构造 `INSERT VERTEX / INSERT EDGE`；`run()` 从 PG `graph_node/graph_edge` 读取写入 Nebula |
| 企业增量写图 | lumen-algo-py | `vendor/entan-py/entan/graph/incremental.py:221-295` | `_nebula_upsert()` 调用 nebula_loader 的 `_load_nodes/_load_edges` 做增量；`add_enterprise()` PG+Nebula 双写，幂等覆盖 |
| 企业图谱编辑 API | lumen-algo-py | `vendor/entan-py/api/main.py:621-640` | `POST /v1/graph/nodes` 调用 `inc.add_enterprise()`；`DELETE /v1/graph/nodes/{org_id}` 执行 `DELETE VERTEX WITH EDGE` |

### 3.3 写出的点边

> **关键架构**：nebula_loader.py 是一条**通用灌图流水线**，从 PG `ads.graph_node` / `ads.graph_edge` 表读取数据，按 `node_type` / `relation_type` 分流写入 Nebula 不同 TAG/EDGE。这条流水线**跨要素写 5 个领域**的 TAG——不只是企业一个。

| 实体 TAG | PG node_type 值 | 硬编码位置 | 对应 L02 对齐轴 | 覆盖要素 |
|---|---|---|---|---|
| `enterprise` | `enterprise` | nebula_loader.py:26 | enterprise | **企业** |
| `industry` | `industry` | nebula_loader.py:26 | 对应 IndustryNode（近似） | **产业** |
| `research` | `research` | nebula_loader.py:26 | 对应 institution（科研机构） | **科研机构** |
| `talent` | `talent` | nebula_loader.py:26 | 对应 person | **人才** |
| `service` | 兜底（else） | nebula_loader.py:80 | 对应 institution（服务机构） | **服务机构** |

| 关系 EDGE | PG relation_type 值 | 起→终 | 硬编码位置 | 覆盖要素 |
|---|---|---|---|---|
| `industry_belong` | — | industry → enterprise | nebula_loader.py:27 | 产业-企业 |
| `research_coop` | — | research ↔ research | nebula_loader.py:27 | 科研机构-科研机构 |
| `talent_coop` | — | talent ↔ talent | nebula_loader.py:27 | 人才-人才 |
| `service_provide` | — | service → enterprise | nebula_loader.py:27 | 服务-企业 |
| `cooperate` | — | enterprise ↔ enterprise | nebula_loader.py:27 | 企业-企业 |
| `supply` | — | enterprise → enterprise | nebula_loader.py:27 | 企业-企业 |
| `parent_sub` | — | enterprise → enterprise | nebula_loader.py:27 | 企业-企业 |

**分流逻辑**（nebula_loader.py:80）：
```python
tag = n["node_type"] if n["node_type"] in by_tag else "service"
```
PG `ads.graph_node.node_type` 列**无枚举约束**（varchar(30)），任何值都可以写入。不在 5 个硬编码 TAG 中的值会被兜底写入 `service`。

### 3.4 证据路径

- 批量写图：`e:\gkx-lumen\repos\lumen-algo-py\vendor\entan-py\entan\graph\nebula_loader.py`
- 增量写图：`e:\gkx-lumen\repos\lumen-algo-py\vendor\entan-py\entan\graph\incremental.py`
- API 入口：`e:\gkx-lumen\repos\lumen-algo-py\vendor\entan-py\api\main.py` 第 621-640 行
- 前置数据源：`scripts/mysql/schema_ent_score.sql` + `scripts/mysql/schema_cfg.sql` 建 PG graph_node/graph_edge 表

### 3.5 cfg_metric 种子文件

| 文件 | metric_id 数 | is_mock | 说明 |
|---|---:|---:|---|
| cfg_metric-ENT-seed.yaml | 96 | 全部 is_mock=true | 企业实体指标定义存在但算法服务全 mock |
| cfg_metric-INNOV-seed.yaml | 143 | 全部 is_mock=true | 企业创新指标定义存在但算法服务全 mock |

---

## 四、要素 3 · 技术（论文）

### 4.1 三态判定

**🔴 仅描述**——算法中台无真实技术/论文领域的 Nebula 写图代码入口。技术领域的上图完全由燕大侧 Platform Schema 抽取链负责（见 L04）。

### 4.2 代码入口扫描结果

| 扫描目标 | 结果 |
|---|---|
| lumen-algo-py/lumen_common/algorithms/science/ | 只有 attract/cultivation/pain_points/supply_chain 四个企业创新分析模块，**无论文/专利/项目实体写图** |
| lumen-algo-py/vendor/innov-py/chainan/ | 产业链算法，**无技术子域** |
| lumen-algo-py/vendor/entan-py/ | 企业分析，**无技术子域** |

### 4.3 边界说明

技术（论文）要素的上图 **完全由燕大侧负责**：燕大快照 1.2 节判定 ✅ 已实现；L04 已整理 Paper/Journal/Patent/PatentFamily/Report/Keyword/Project 七个实体 TAG + 9+2=11 条 EDGE。

算法中台在技术域只做**指标计算**（不做上图）：cfg_metric-TECH-seed.yaml 有 39 条指标定义（全 mock）。

### 4.4 cfg_metric 种子文件

| 文件 | metric_id 数 | is_mock | 说明 |
|---|---:|---:|---|
| cfg_metric-TECH-seed.yaml | 39 | 全部 is_mock=true | 技术指标定义存在但算法服务全 mock |

---

## 五、要素 4 · 人才

### 5.1 三态判定

**✅ 真实已跑通**——有真实 Nebula 写图代码入口（nebula_loader.py 通用灌图流水线）。

### 5.2 代码入口与写出的点边

**共享写图路径**：`vendor/entan-py/entan/graph/nebula_loader.py` + `incremental.py`（复用 nebula_loader）

nebula_loader.py TAGS 常量**硬编码包含 `talent`**（第 26 行），分流逻辑按 PG `graph_node.node_type` 值为 `talent` 的行写入 Nebula `talent` TAG。

| 实体 TAG | PG node_type | 来源 | 对应 L02 对齐轴 |
|---|---|---|---|
| `talent` | `talent` | PG ads.graph_node | 对应 person |

| 关系 EDGE | 起→终 | 硬编码位置 |
|---|---|---|
| `talent_coop` | talent ↔ talent | nebula_loader.py:27 |

### 5.3 边界说明

人才要素有**两条写图路径**：
- **算法中台**：nebula_loader.py 通用灌图（写 `talent` TAG + `talent_coop` EDGE）
- **燕大侧**：Person + ScholarOrganization 双 TAG + 6 条 EDGE（AFFILIATED_WITH / STUDIED_AT / COAUTHOR_WITH / …）

两侧 TAG/EDGE 命名不同（talent vs Person；talent_coop vs COAUTHOR_WITH），但都覆盖人才领域。

### 5.4 cfg_metric 种子文件

| 文件 | metric_id 数 | is_mock | 说明 |
|---|---:|---:|---|
| cfg_metric-TALENT-seed.yaml | 32 | 全部 is_mock=true | 人才指标定义存在但算法服务全 mock |

---

## 六、要素 5 · 科研机构

### 6.1 三态判定

**✅ 真实已跑通**——有真实 Nebula 写图代码入口（nebula_loader.py 通用灌图流水线）。

### 6.2 代码入口与写出的点边

**共享写图路径**：`vendor/entan-py/entan/graph/nebula_loader.py` + `incremental.py`（复用 nebula_loader）

nebula_loader.py TAGS 常量**硬编码包含 `research`**（第 26 行），分流逻辑按 PG `graph_node.node_type` 值为 `research` 的行写入 Nebula `research` TAG。

| 实体 TAG | PG node_type | 来源 | 对应 L02 对齐轴 |
|---|---|---|---|
| `research` | `research` | PG ads.graph_node | 对应 institution（科研机构） |

| 关系 EDGE | 起→终 | 硬编码位置 |
|---|---|---|
| `research_coop` | research ↔ research | nebula_loader.py:27 |

### 6.3 边界说明

科研机构有**三条隐含写图路径**：
1. **算法中台 nebula_loader.py**：写 `research` TAG + `research_coop` EDGE
2. **算法中台 graph_project.py**：产业链灌链中的 `institution` 端点（写 `institution` TAG）——注意：graph_project.py 的 institution 覆盖科研机构和服务机构，混装
3. **燕大侧**：Organization TAG + org_kind 枚举区分（`domestic_university` / `domestic_research_institute`）

两侧 naming 不同（研究机构的 research / institution vs 燕大的 Organization + org_kind），但都覆盖科研机构领域。

### 6.4 cfg_metric 种子文件

| 文件 | metric_id 数 | is_mock | 说明 |
|---|---:|---:|---|
| cfg_metric-ORG-seed.yaml | 22 | 全部 is_mock=true | 机构指标定义存在但算法服务全 mock |

---

## 七、要素 6 · 政策

### 7.1 三态判定

**🔶 定义存在但未上线**——cfg_metric-POLICY-seed.yaml 有 35 条指标定义（全 mock），但算法中台有部分政策分析代码（polan/ 子包），**无真实 Policy 实体 Nebula 写图代码**。

### 7.2 代码入口扫描结果

| 模块 | 有什么 | 缺什么 |
|---|---|---|
| lumen-algo-py/lumen_common/algorithms/policy/ | industry_enrich.py + industry_job.py 两个政策产业分析模块 | 无 Policy 实体 TAG 写图 |
| lumen-algo-py/vendor/entan-py/polan/ | 完整政策分析子包（job.py / ods_sync.py / 多个 eval 模块） | 无 Nebula 写 Policy TAG 的 nGQL |
| lumen-algo-py/vendor/entan-py/scripts/ | run_all_policy.py + run_policy_ods_sync.py + schema_policy_ads.sql | SQL 建 ADS 表，不写 Nebula |
| lumen-algo-py/vendor/innov-py | 无政策模块 | — |

### 7.3 cfg_metric 种子文件

| 文件 | metric_id 数 | is_mock | 说明 |
|---|---:|---:|---|
| cfg_metric-POLICY-seed.yaml | 35 | 全部 is_mock=true | 政策指标定义存在但算法服务全 mock |

### 7.4 边界说明

政策要素**两侧都缺写图**：
- 燕大侧：快照 1.2 节判定 ⚠ 未实现（蓝图+源表已备，无 Policy TAG）
- 算法中台侧：有政策分析代码和 ADS 表建表 SQL，**无 Policy TAG Nebula 写图**

---

## 八、要素 7 · 服务机构

### 8.1 三态判定

**✅ 真实已跑通**——有真实 Nebula 写图代码入口（vendor/entan-py/entan/svcgraph.py）。

### 8.2 过程名与仓与入口

| 过程 | 仓 | 入口函数 | 写图方式 |
|---|---|---|---|
| 服务机构 Nebula 写图 | lumen-algo-py | `vendor/entan-py/entan/svcgraph.py:139-202` `_upsert_nebula()` | 构造 `INSERT VERTEX IF NOT EXISTS institution(...)`，按字段 probe 结果动态写 name/institution_type/weight/props |
| 服务机构边写入 | lumen-algo-py | `vendor/entan-py/entan/svcgraph.py:221-357` | `upsert_participates()` 构造 `INSERT EDGE IF NOT EXISTS participates(...)`；`upsert_belongs_to()` 构造 `INSERT EDGE IF NOT EXISTS belongs_to(...)` |

### 8.3 写出的点边

| 实体 TAG | 来源 | 说明 |
|---|---|---|
| `institution`（服务机构） | 机构数据源 | 注意：算法中台写的 `institution` TAG 同时覆盖**企业**和**服务机构**（混装，与燕大侧 Organization 默认桶同困境） |

| 关系 EDGE | 起→终 | 硬编码位置 |
|---|---|---|
| `participates` | institution → 产业环节 | svcgraph.py:27 |
| `belongs_to` | institution → 产业 | svcgraph.py:27 |
| `supplies` | institution → enterprise | svcgraph.py:27（ALLOWED_EDGES 包含但 upsert 函数未见显式构造） |
| `depends_on` | institution → institution | svcgraph.py:27（ALLOWED_EDGES 包含但 upsert 函数未见显式构造） |

> **注意**：svcgraph.py 的 `ALLOWED_EDGES` 硬编码 4 条（第 27 行），但目前显式实现的 upsert 函数只有 `upsert_participates()` / `upsert_belongs_to()` 两条。`supplies` / `depends_on` 只在常量里声明，未见实际构造 `INSERT EDGE` 的函数。

### 8.4 证据路径

- 主代码：`e:\gkx-lumen\repos\lumen-algo-py\vendor\entan-py\entan\svcgraph.py`
- 第 139-202 行：`_upsert_nebula()` — Nebula vertex 写入
- 第 221-357 行：`upsert_participates()` / `upsert_belongs_to()` — Nebula edge 写入

### 8.5 cfg_metric 种子文件

| 文件 | metric_id 数 | is_mock | 说明 |
|---|---:|---:|---|
| cfg_metric-SVC-seed.yaml | 51 | 全部 is_mock=true | 服务机构指标定义存在但算法服务全 mock |

---

## 九、三态判定汇总

| # | 七要素 | ✅ 真实已跑通 | 🔶 定义存在但未上线 | 🔴 仅描述 | cfg_metric mock 数 |
|---|---|---|---|---|---:|
| 1 | 产业 | ✅ graph_project.py+NebulaSink + nebula_loader.py `industry` TAG | — | — | 100（CHAIN） |
| 2 | 企业 | ✅ nebula_loader.py 5 TAG 批量灌图 + incremental.py 增量双写 | — | — | 96（ENT）+ 143（INNOV） |
| 3 | 技术 | — | — | 🔴 燕大侧负责，算法中台无写图 | 39（TECH） |
| 4 | 人才 | ✅ nebula_loader.py `talent` TAG + `talent_coop` EDGE | — | — | 32（TALENT） |
| 5 | 科研机构 | ✅ nebula_loader.py `research` TAG + `research_coop` EDGE + graph_project.py `institution` 端点 | — | — | 22（ORG） |
| 6 | 政策 | — | 🔶 POLICY seed 35 条全 mock + polan/ 有分析代码无写图 | — | 35（POLICY） |
| 7 | 服务机构 | ✅ svcgraph.py `institution` TAG + `participates`/`belongs_to` + nebula_loader.py `service` TAG 兜底 | — | — | 51（SVC） |
| **合计** | — | **5 要素 ✅** | **1 要素 🔶** | **1 要素 🔴** | **≈580 条全 mock** |

### 两条核心写图路径

| 路径 | 仓 | 硬编码 TAG | 覆盖要素 |
|---|---|---|---|
| **产业链专用** | lumen-algo-py/lumen_common/algorithms/chain/graph_project.py | chain / segment / enterprise / institution（4 TAG） | 产业 |
| **通用灌图** | lumen-algo-py/vendor/entan-py/entan/graph/nebula_loader.py | enterprise / industry / research / talent / service（5 TAG） | 企业 / 产业 / 科研机构 / 人才 / 服务机构 |
| **服务机构专用增量** | lumen-algo-py/vendor/entan-py/entan/svcgraph.py | institution（1 TAG） | 服务机构（与 graph_project.py 共享 TAG 名） |

---

## 十、与 L04 燕大侧的分工对照

| 要素 | 算法中台侧（L03） | 燕大侧（L04） | 重叠度 | 备注 |
|---|---|---|---|---|
| 产业 | ✅ graph_project.py（chain/segment/enterprise/institution）+ nebula_loader.py `industry` TAG | ✅ 已实现（IndustryChain + IndustryNode） | 🔶 部分重叠 | 算法中台写 segment/chain 产业链环节；燕大写 IndustryChain/IndustryNode |
| 企业 | ✅ nebula_loader.py 5 TAG 批量灌图 + incremental.py 增量双写 | ✅ 已实现（Organization 默认桶） | 🔶 部分重叠 | 算法中台写 `enterprise` TAG；燕大写 Organization（混装企业/机构/海外） |
| 技术 | 🔴 仅描述（算法中台无写图） | ✅ 已实现（Paper/Journal/Patent/…） | 无 | **仅燕大侧写** |
| 人才 | ✅ nebula_loader.py `talent` TAG + `talent_coop` EDGE | ✅ 已实现（Person + ScholarOrganization） | 🔶 部分重叠 | 算法中台写 `talent` TAG + `talent_coop`；燕大写 Person + ScholarOrganization + 6 EDGE |
| 科研机构 | ✅ nebula_loader.py `research` TAG + graph_project.py `institution` 端点 | ✅ 已实现（Organization 两 org_kind 枚举） | 🔶 部分重叠 | 算法中台写 `research`/`institution`；燕大写 Organization + org_kind |
| 政策 | 🔶 POLICY seed 全 mock + polan 有分析代码无写图 | ⚠ 未实现（蓝图+源表已备） | 无 | **两侧都不写**——这是最终 GAP |
| 服务机构 | ✅ svcgraph.py `institution` TAG + nebula_loader.py `service` TAG 兜底 | ⚠ 无独立口径（Organization 默认桶混装） | 🔶 部分重叠 | 算法中台有两条路径；燕大侧混装 |

---

## 十一、L05 GAP 差集的衔接说明

L05 差集公式：**GAP = 需求清单 −（L03 已实现 ∪ L04 已实现）**

| L05 减数项 | 本文件对应章节 | L04 对应章节 |
|---|---|---|
| 算法中台真实写图的实体 TAG | 各要素 2.3/3.3/8.3 节 | — |
| 算法中台真实写图的关系 EDGE | 各要素 2.3/3.3/8.3 节 | — |
| 算法中台 cfg_metric 定义但未上线的指标 | 各要素 cfg_metric 小节 | — |
| 算法中台 + 燕大侧都不写的要素 | 第十章对照 + 第七章（政策） | L04 第七章 |

---

## 十二、输入材料索引

| 材料 | 路径 | 版本 |
|---|---|---|
| lumen-algo-py 主仓 | `e:\gkx-lumen\repos\lumen-algo-py\` | 已 clone（2026-10-27 确认完整） |
| demo-algo-ent-analysis | `e:\gkx-lumen\repos\demo-algo-ent-analysis\` | 已 clone |
| demo-algo-science | `e:\gkx-lumen\repos\demo-algo-science\` | 已 clone |
| cfg_metric 种子文件（11 个） | `agent-delivery/metrics/registry/cfg_metric-*-seed.yaml` | 2026-10-27 统计 |
| SYSINT-SCHEME-07-L02 对齐轴 | `agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/我方/SYSINT-SCHEME-07-L02-对齐轴.md` | v1.0 |
| 致燕大需求清单 v1.0 | `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/KG-YANDA-SCHEMA-REQ/科技信息展示系统-知识图谱实体、实体关系属性需求清单.md` | v1.0 |
| WBS-07 | `agent-delivery/工程过程/04-系统集成/07-图数据库集成/WBS.md` | 2026-10-26 |
