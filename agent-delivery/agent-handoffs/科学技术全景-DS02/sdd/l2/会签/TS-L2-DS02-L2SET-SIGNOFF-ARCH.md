# TS-L2-DS02-L2SET-SIGNOFF-ARCH · 科学技术全景 · 二级四单 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-07
- 对象：`TS-L2-DS02-{GRAPH,ENTITY,PATH}-{ARCH,API,METRIC,DATA}`（12 份 as-built）
- 监管：`human:淮政玮`
- 对照：说明书 `科学技术全景-系统详细设计说明书.md` 第 3、4、6 节；模块级 `TS-L2-DS02-ARCH.md` 第 2 节；公约 §2（调用链、Nebula、D12、D18）；需规 `科学技术全景.md` 序号 17–33
- 代码只读抽查：`lumen-algo-py` `tech_graph_read.py`、`tech_graph.py`；`lumen-svc-platform` `SituationPanoramaService.java`、`feign/Remote*Client.java`
- 任务单只读查询：经 MCP `task-get` 查 `TS-L2-DS02-SEL-FIX-L01`、`TS-L2-DS02-FE-ENTITY-FIX-L01`，经 `task-query` 查本模块任务状态。未写 task-registry
- 本页不改代码，不 commit。被审稿的文字修正见各节「第一轮 → 已改」

审的是记录是否如实、是否合规、偏离是否已登记且有归属。不重新设计。

## 总结论

| 二级 | 第一轮 | 已改 | 第二轮 |
|---|---|---|---|
| GRAPH（17–21） | 不同意 | 是 | 有条件同意 |
| ENTITY（22–27） | 不同意 | 是 | 有条件同意 |
| PATH（28–33） | 不同意 | 是 | 有条件同意 |

三节第一轮不同意的共同原因：偏离表的「归属」写的是 `SYSINT-05-01B-L01`、`SYSINT-05-01A-L01`、`TS-L2-DS02-READ-PY-L01`。三张单 `task-query` 查为 done。挂在已完成单上等于无人认领。实际已建修复单 `TS-L2-DS02-SEL-FIX-L01`（ready）、`TS-L2-DS02-FE-ENTITY-FIX-L01`（backlog），稿里一处都没写。

第二轮的共同条件（三节都适用，不满足则本页结论回到不同意）：

1. **C1 查询缺口建单。** `IndexNotFound` 当空（`07ffa9f`）与说明书第 6 节「读失败不用空壳冒充成功」相冲。抽查 `tech_graph_read.py`：选中点查点 `_one_point_ngql`、关系 `_rel_ngql`、路径 `_path_ngql` 都把 `id() == …` 与属性等值写在同一个 `OR`；搜索、领域收窄是纯属性 `WHERE`。写入侧 `tech_graph.py` 第 214、219 行注释自记「WHERE 在 `demo_gkx_chain` 上会 IndexNotFound」。所以 `SEL-FIX` 修完，选中点、搜索、领域筛选仍可能静默为空。须由 coordinator 建一张返修单（补 Tag 索引，或改成只按 VID 查；并把「Schema 未建 / 边类型不存在」与「IndexNotFound」分开，前者当空，后者不当空），并让 `SEL-FIX` 的联调验证排在它之后。
2. **C2 截断透传必做。** `SEL-FIX` 的 DoD 把透传 `truncated` 写成「可选同单」。说明书第 3 节「超过上限要标明截断」是设计要求，不是可选项。要么在该单改为必做，要么另建单。本页不改 registry，交 coordinator。

## 1. GRAPH（序号 17–21）

### 第一轮：不同意

| 文件 · 段落 | 问题 | 要改成 |
|---|---|---|
| `GRAPH-ARCH` 第 2 节 Mermaid 节点 `py` | 写成 `lumen-platform-algo-py`。那是 Feign 服务名，不是仓名。模块级会签第一轮正是要求图上锁死 `lumen-algo-py` | `lumen-algo-py（Feign 名 lumen-platform-algo-py）` |
| `GRAPH-ARCH` 第 6 节「选中点入参」「截断标记」处理列 | 只写「待修」，无归属 | 归 `TS-L2-DS02-SEL-FIX-L01`；截断注明 DoD 为「可选同单」 |
| `GRAPH-ARCH` 第 6 节「查询缺口」 | 说明书列写「—」，未点明与说明书第 6 节相冲；没列领域收窄、选中点同受影响；无归属 | 写明相冲、列全受影响查询、写「未建单」 |
| `GRAPH-ARCH` 第 6 节 | 漏登记：需规序号 20「模糊匹配和精确匹配」，as-built 只有 `CONTAINS` | 新增一行偏离 |
| `GRAPH-API` 第 5 节「不一致」段、第 6 节末句 | 归属写「`SYSINT-05-01B-L01` 或 `TS-L2-DS02-READ-PY-L01`」（均 done） | 改为 `SEL-FIX`，并补「只修字段名，选中点仍可能取空」 |

### 已改

上表五处已在被审稿中改文字（`GRAPH-ARCH` 第 2、6 节；`GRAPH-API` 第 5、6 节）。另随数据会签改了 `GRAPH-DATA` 第 5、7 节，随产品会签改了 `GRAPH-METRIC` 第 3 节。

### 第二轮：有条件同意（条件 C1、C2）

| 项 | as-built 稿 | 代码抽查 | 判定 |
|---|---|---|---|
| 调用链：页 → 网关 `/display/**` → `gkxlumen-display` → `lumen-algo-py` `POST /internal/tech-graph/read` → `demo_gkx_chain`；分数 display 只读 | 第 2 节图与跳表 | `RemoteTechGraphClient` name `lumen-platform-algo-py`、路径 `/internal/tech-graph/read`；`SituationPanoramaService` 下发 `space=demo_gkx_chain` | 一致 |
| 不经 `gkxlumen-graph`、不调 `demo-*`（D12） | 第 2 节末段 | 本链未用 `RemoteGraphClient`；无 `demo-*` 下游 | 一致 |
| Nebula、空间锁 | 第 2、8 节：只读 `demo_gkx_chain`，Python 422 / Java 502 | Python 只发 `MATCH` | 一致 |
| Java 不写 nGQL、请求内不算分（公约 §2.1） | 第 2 节 | Java 只装配、剥离 Python 自带分数后按编号 SELECT | 一致 |
| D18 | 分数表只读、无行为 null、不返回写死 mock | 同 | 一致 |
| 上限 200 / 200 / 20 / 20 | 第 5 节 | Python `_POINT_CAP`、`_REL_CAP` 等常量；Java `PATH_LIMIT=20` 等 | 一致 |
| 子学科收窄 | 第 2、6 节登记为偏离 | `RemoteDisciplineDictClient` → `gkxlumen-platform-search-py` `/internal/gkx-svc/dict/query` | 记录如实。`lumen-topic-py` 是 lumen 正式 Python（`architecture-baseline.md` 依赖规则 `java_downstream_may_call`），不违 D12。口径归产品，转登记 |

观察（不作为条件，不重开模块级已签决策）：

- D15 写「展示 BFF 不直连 Python / DB」，展示侧 Python 门面是 `gkx_show_service` `/internal/gkx-show/**`。as-built 里 display 直连 `lumen-algo-py`、JDBC 直读分数表、经专题侧 `/internal/gkx-svc/` 读子学科。前两项在模块级 `TS-L2-DS02-ARCH` 已签，第三项 display 已有同类先例（`RemoteFactorSearchPythonClient` 走 `/internal/gkx-search/`）。建议架构基线另开一行 D15 现状说明，不挡本二级。
- 子学科读的库是外部 `gkx_technology_analysis_dev` @ `47.93.119.170`（`jx_dict.py` 默认），正式链路依赖一个 `_dev` 库。归数据会签跟踪。

## 2. ENTITY（序号 22–27）

### 第一轮：不同意

| 文件 · 段落 | 问题 | 要改成 |
|---|---|---|
| `ENTITY-ARCH` 第 8 节表 #1、#2、#4、#5 归属列 | 全部指向 done 单；#2 实有 `FE-ENTITY-FIX-L01`、#1/#5 实有 `SEL-FIX-L01`，未写 | #1、#5 → `SEL-FIX`；#2 → `FE-ENTITY-FIX`；#4 写「原单已 done，返修未建单」 |
| `ENTITY-ARCH` 第 8 节 | 漏登记 `IndexNotFound` 当空与说明书第 6 节相冲（第 7 节只写了现象） | 新增 #6 |
| `ENTITY-API` 第 8 节 #1–#5 归属列 | 同上 | 同上 |

### 已改

上表三处已改（`ENTITY-ARCH` 第 8 节新增 #6 并改归属；`ENTITY-API` 第 8 节改归属）。

### 第二轮：有条件同意（条件 C1、C2；另加 C3）

- **C3**：`relationCount` 恒 1、`nodeIds` 只含当前点（`tech_graph_read.py` 第 379 行），与说明书第 2.2 节「条数是邻居个数」不符。原单 `READ-PY-L01` 已 done，须建返修单。

| 项 | as-built | 判定 |
|---|---|---|
| 时序图六跳 | 第 2 节 `sequenceDiagram`：页 → 网关 → display → `lumen-algo-py` → `demo_gkx_chain`；display → 分数表 | 一致 |
| 实体只来自图，分数不决定谁出现 | 第 3、4 节 | 一致 |
| 序号 26 为 501 | `entity-relations` 与 `entityRelations=true` 均 501，不调读图 | 一致 |
| 筛选、排序在前端，后端不收参数 | API 第 6 节 | 一致，不是 Java 写算法 |
| 每类 20、页面切 5、分数编号 400 | 第 6 节 | 一致 |

## 3. PATH（序号 28–33）

### 第一轮：不同意

| 文件 · 段落 | 问题 | 要改成 |
|---|---|---|
| `PATH-ARCH` 第 8 节 #1、#3 归口 | 指向 done 单 | `SEL-FIX` |
| `PATH-ARCH` 第 8 节 #2「需会签定」、#4「分档线需产品定」 | 两项是业务口径。公约 §3.8：任何角色都不能替甲方拍板。写成「会签定 / 产品定」越权 | 「口径项，四角色同意 as-built，转客户决策清单；改码未建单」 |
| `PATH-ARCH` 第 8 节 | 漏登记：`_path_ngql` 同样把 VID 与属性等值写在一个 `OR`，`IndexNotFound` 时路径整条当空 | 新增 #6 |
| `PATH-API` 第 9 节、`PATH-DATA` 第 6 节 | 不一致项无归属 | 补 `SEL-FIX` 与「口径项转登记」 |

### 已改

上表四处已改。

### 第二轮：有条件同意（条件 C1、C2）

| 项 | as-built | 判定 |
|---|---|---|
| 调用链图 | 第 2 节 `flowchart LR`：`lumen-algo-py` 写对；分数表只读 | 一致 |
| 路径步只来自图，不进分数表 | 第 3 节 | 一致 |
| 32 比较、33 播放页面内完成，不按 `currentYear` 换图 | 第 4 节第 5、6 步 | 一致 |
| 序号 28 写请求 501 | 第 1、5 节 | 一致 |
| 路径 20、步 168、编号 400 | 第 6 节 | 一致；`_PATH_FETCH` 带 `ponytail:` 注释，上限已标 |
| 关键节点不挂 `M_TECH_PATH_KEYNODE` | 第 1 节 | 与说明书第 5 节一致 |

路径「整条 vs 局部」、重要性分档线：同意 as-built，口径转登记（条目见产品会签）。

## 铁律逐条

| 铁律 | GRAPH | ENTITY | PATH |
|---|---|---|---|
| 算法只在 Python；Java 不写 nGQL、不算分 | ✅ | ✅ | ✅ |
| 调用链 前端 → Java → Python `/internal/*` | ✅ | ✅ | ✅ |
| Nebula `demo_gkx_chain`，不用 Neo4j，不改去 `gkx_chain` / `entan` | ✅ | ✅ | ✅ |
| D12 不调 `demo-*`，不经 `gkxlumen-graph` | ✅ | ✅ | ✅ |
| D18 只读新建 ADS 表，不返回写死 mock | ✅ | ✅ | ✅ |
| 读失败不用空壳冒充成功（说明书第 6 节） | ❌ as-built 违反，已登记，待 C1 建单 | ❌ 同左 | ❌ 同左 |
| 超限标明截断（说明书第 3 节） | ❌ 已登记，归 `SEL-FIX`，待 C2 | ❌ 同左 | ❌ 同左 |

## 签收边界

本页不把任务标 done，签收由 `human:淮政玮` 做。同意会签不是签收。C1、C2（ENTITY 另加 C3）须由 coordinator 建单或改单；本页不写 task-registry。
