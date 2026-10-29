# KG-CLOSELOOP · 七要素上图与图谱消费 · 长任务总控

> **日期**：2026-10-29  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：在燕大平台上把七要素上图跑成闭环；入图之后，用燕大查询/分析接口加上我方算法，支撑科技专题系统与展示系统的图谱展示和相关指标。  
> **模式**：长任务，本轮只写方案，不改业务仓代码，不开开发叶。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **过程夹**：[`07-图数据库集成`](../../工程过程/04-系统集成/07-图数据库集成/README.md)  
> **锁**：`lock_hours=24`，`claim_type=coordinator_dispatch`，`supervised_by=human:淮政玮`

本文件是 2026-10-29 会话启动令。授权人按第 07 项方案签收人口径写成淮政玮。调研叶认领不必再回聊天确认。

---

## 0. 两项目标（方案必须同时答完）

| # | 目标 | 完成看起来像什么 |
|---|---|---|
| 1 | 七要素上图在**燕大平台**上实施闭环 | 选定的第一刀要素：源数据 → 燕大抽取/写入 → 图上可查到点边。写明谁点运行、在哪个图空间、怎样验收。政策若图上还没有 TAG，不得假装已经闭环 |
| 2 | 入图后支撑**专题 + 展示**的图谱展示和相关指标 | 页面只走 `前端 → 网关 → Java → Python /internal/*`。Python 调燕大查询/分析接口；燕大给不出的指标才在 `lumen-algo-py` 自研。Java 不写 nGQL、不写算法。未就绪是 HTTP 501，不是假图 |

---

## 1. 为什么另开本管线

第 07 项已有技术方案 `SYSINT-SCHEME-07-L01`（处理中）。该文把范围收成**在线读图**：建图归第 6 项，且写明不在本仓写图算法，正式空间仍是我方 `demo_gkx_chain`。

2026-10-29 的目标与该文不一致：上图要在燕大平台闭环，消费要同时用燕大接口和我方算法，系统含专题与展示。本管线单写 [`实施方案`](../../工程过程/04-系统集成/07-图数据库集成/实施方案.md)（由 `KG-CLOSELOOP-SCHEME-L01` 落笔）。签收前**不改** `技术方案.md` 正文，不把 `SYSINT-07-01`～`03` 派出去编码。

已有材料只作输入，不重复做：

| 材料 | 任务 | 状态（2026-10-29 查询） | 本管线怎么用 |
|---|---|---|---|
| 技术方案（读图五段） | `SYSINT-SCHEME-07-L01` | in_progress | 调用链、501、禁止假图继续有效。上图与自研算法以本实施方案为准 |
| 对齐轴 / 中台上图台账 / 燕大对照 / GAP | `SYSINT-SCHEME-07-L02`～`L05` | ready_to_sign | 直接引用，禁止另起一套差集 |
| 需求清单 | `KG-YANDA-SCHEMA-REQ-L01` | ready_to_sign | 14 实体 / 17 关系 / 99 属性 / 31 计算 / 10 写入 |
| 早期 GAP v1.1 | `KG-YANDA-GAP-L01` | in_progress | **不沿用**。L05 已声明独立判定 |
| Schema 对比 | `KG-YANDA-SCHEMA-COMPARE-L01` | done | 只作背景 |
| 燕大七要素快照 | 对端 2026-10-26 | 已落盘 | 上图现状真源。空间 `gkx_local_1` / `gkx_full_1` |
| 三条读图开发叶 | `SYSINT-07-01-L01`～`07-03-L01` | ready | **方案签收前禁止派编码** |

---

## 2. 段与叶

全部仓：`gkx-orchestration`，分支 `origin/dev`。只写文档。`ponytail:` 写 `N/A`（定义轨）。

| 波 | 任务 | 角色 | 状态门 | 产物 |
|----|------|------|--------|------|
| 1 | `KG-CLOSELOOP-R01` 燕大写侧能否跑通 | architect-agent | 无依赖，可直接认领 | handoff 同目录 `KG-CLOSELOOP-R01.md` |
| 1 | `KG-CLOSELOOP-R02` 我方数据能否喂给燕大 | data-agent | 无依赖 | `KG-CLOSELOOP-R02.md` |
| 1 | `KG-CLOSELOOP-R04` 燕大查询/分析契约 | algorithm-agent | 无依赖 | `KG-CLOSELOOP-R04.md` |
| 1 | `KG-CLOSELOOP-R05` 两系统消费清单 | product-agent | 无依赖 | `KG-CLOSELOOP-R05.md` |
| 2 | `KG-CLOSELOOP-R03` 图空间唯一落点 | architect-agent | R01、R02 有 handoff 且 ≥ ready_to_sign | `KG-CLOSELOOP-R03.md` |
| 2 | `KG-CLOSELOOP-R06` 自研算法边界 | algorithm-agent | R04 有 handoff 且 ≥ ready_to_sign | `KG-CLOSELOOP-R06.md` |
| 3 | `KG-CLOSELOOP-SCHEME-L01` 实施方案 | doc-agent | R03、R05、R06 有 handoff 且 ≥ ready_to_sign | `07-图数据库集成/实施方案.md` + `KG-CLOSELOOP-SCHEME-L01.md` |

厚包：[`KG-CLOSELOOP-调研段-总派单.md`](./KG-CLOSELOOP-调研段-总派单.md)

```text
R01 ─┐
R02 ─┼─ R03 ─┐
R04 ─┼─ R06 ─┼─ SCHEME-L01
R05 ─┘       ┘
```

同波文档叶可以并行：产物路径互斥。禁止两叶改同一个文件。禁止在本管线里改 `技术方案.md`、`task-registry.yaml`（注册表只走 MCP）。

---

## 3. 已拍板（执行中不许再问）

1. 调用链：浏览器和前端不直连燕大，不直连 Nebula。Java 不写 nGQL、不做图算法。算法与燕大 HTTP/nGQL 只出现在 Python `/internal/*`。
2. 图谱协议仍是 NebulaGraph / TRSGraph。禁止改提 Neo4j，禁止嵌亿集或燕大管理界面。
3. 凭据、API Key、连接口令不进 git。环境地址可以写，密钥不写。
4. 缺数：未就绪 = HTTP 501；查询执行了但无命中 = 空态；无权限 = 降级。三者不混用，禁止假图。
5. 指标只展示已有 `metric_id` 的结果。页面不新造口径。`cfg_metric` 且 D4=mock 不算已实现。
6. 第一刀要素优先选燕大快照里已经有独立 TAG、且不落 Organization 默认桶的对象。政策 TAG 未建，**不得**当第一刀。推荐顺序写在 R01，由方案叶拍板写死，默认识别为论文（Paper）优先于人才。
7. 本轮交付物是实施方案，不是代码。不 `task-create` 开发叶。`SYSINT-07-01`～`03` 维持不派。
8. L02～L05 的结论直接引用。发现事实冲突时，在本叶 handoff 里单列「与 L0x 不一致」，不回头改 L0x，除非授权人另说。
9. 结构歧义（新图空间、改 VID 规则、新写正式库）停在该叶，升级 `human:李伟`。其余叶继续。
10. `ready_to_sign → done` 只由 `human:淮政玮` 点。签收可以积压，不挡下一波调研叶。

---

## 4. 和燕大的工作边界（草案，方案叶收成定稿）

调研叶负责用证据核对，不准把草案改写成已经和白鑫凤签过字。

| 事项 | 燕大 | 智树 |
|---|---|---|
| 图平台运维、Schema 注册、抽取脚本、构建编排、人工审核、图空间 | 负责。测试环境 `http://10.50.183.56:8093` 已提供 | 不实现对方后台，不把管理界面嵌进展示/专题 |
| 七要素里已经有 TAG 的上图运行 | 在平台上执行抽取/构建，给出可复查的点边 | 把源数据准备到对方抽取链能读的表和字段；对不上的列写成缺口，不私自改对方脚本 |
| 政策 TAG、时序快照、Activity、关系中英文对照 | 缺口在对方图上。排期由对方回复 | 只登记缺口和因此做不了的页面/指标，不在我方 Nebula 上平行再造一套生产政策图冒充燕大闭环 |
| 查询、路径、PageRank / Louvain / Degree 等已有分析接口 | 提供可调用契约：路径、入参、限额、错误码 | Python 封装调用。样例 JSON 不等于已签契约 |
| 契约覆盖不了的专题/展示指标 | 不要求对方为每一条指标新做算法 | `lumen-algo-py` 实现，挂已有 metric_id。Java 只转发 |
| 展示页、专题页、网关、Java 门面 | 不改我方前端 | 我方实现。方案签收前不动 `SYSINT-07-*` 编码 |
| 统一用户、CMS 上的图谱 overlay | 无关 | overlay 继续不碰 Nebula，不纳入本闭环验收 |

还没钉死、必须在方案里写成「待拍板」的只有两件事：

1. 数怎么进燕大图：对方抽取我方 DWD，还是我方调用对方写入 API 推数。
2. 生产读哪张图：燕大 `gkx_local_1` / `gkx_full_1`，还是我方 `demo_gkx_chain`。两套同时当生产禁止。R03 给一个推荐，方案叶写入「待授权人确认」。

---

## 5. 启动时还没写进目标、但方案必须回答的事

1. **图空间冲突**。L01 锁 `demo_gkx_chain`；燕大快照是 `gkx_local_1` / `gkx_full_1`；旧政策叶曾写 `gkx_policy`（已禁止当目标态）。不先选唯一生产空间，上图和读图会各写各的。
2. **企业 / 科研机构 / 服务机构共用 Organization**。燕大没有「企业」「服务机构」专属 `org_kind`。查询不过滤就会串味。第一刀避开这只桶。
3. **「技术」有两个意思**。七要素的技术在燕大侧是论文/专利/项目。需求清单里的 `technology` 是技术点，两边都没有 TAG，数据在久新。方案里分开写，不许并成一行。
4. **删除和修改点**。10-21 纪要记写权限未开放。闭环定义成「可重建、可查询」，不要定义成「可在页面上改点」。
5. **九类查询样例不是契约**。专家关系、合作、任职、产业链 TOP-N、全景图都收过测试数据。R04 分成可调用 / 仅有样例 / 还没有契约。
6. **时序指标**。图版本快照仍是空白。趋势、对比、演化类指标在方案里标「现在做不了」，不排进第一刀。
7. **子图有多大**。单次返回上限、截断、限流还没有书面数。页面禁止一次拉全图。方案写默认截断，数字未确认就写「还没有」。
8. **VID**。不得从 VID 解析业务主键。我方准备的键与燕大 `vid=org_{org_id}` 一类规则要在 R02 对上。
9. **指标血缘**。图上算出来的数要能点开 ⓘ。对不上 metric_id 的展示需求进缺口，不临时编号。
10. **验收要带 trace**。第一刀的验收句子是：一次上图批次号 + 一次查询的 trace-id，能在图上指到同一批点。没有 trace 不算闭环。
11. **内网**。`10.50.183.56` 与 graphd `10.50.75.136:9669` 只在部署网络可达。方案写清哪一个环境跑第一刀，不假定笔记本能打通。
12. **三处不要各做一遍上图**。第 6 项 GDF 的 `{要素}-Graph`、我方 nebula loader、燕大抽取链。方案指定一条生产路径，另外两条写成停用或只作对照。
13. **CMS 图谱菜单**是运营覆盖，不读 Nebula。不要放进本闭环的演示脚本。
14. **关系中英文名还没对齐**。联调前没有对照表就会接错边。R04 列出缺这张表时哪些查询不能开工。
15. **刷新**。图谱批次更新和指标日更不是一回事。方案写第一刀的更新方式：手工触发一次，还是跟着抽取调度。不写没有依据的频率。

---

## 6. 历史任务怎么归堆（不重做）

### 6.1 第 07 项与燕大对接（现行）

见 §1 表。过程夹进度：设计约 58、开发 0（2026-10-28 快照）。开发分为 0 是事实，本总控不改这个数。

### 6.2 加工 / 上图（历史，只作输入）

| 任务 | 状态 | 和本目标的关系 |
|---|---|---|
| `E-PLATFORM-P0-L03` 图谱引擎 schema + `/internal/graph/*` | done | 我方读图骨架。不是燕大上图 |
| `E-PLATFORM-P0-TRSGRAPH-L01` 切 graphd，重灌 `demo_gkx_chain` | in_progress | 我方空间。R03 必须看见它，避免两套生产 |
| `DEMO-CHAIN-PY-GRAPH-L01` 产业链 DWD 投影 | pending_test | 我方投影样例 |
| `POLICY-NEBULA-PROJECT-CHAIN-L01` | done | 政策进 `demo_gkx_chain`。不是燕大 Policy TAG |
| `E-E7-POLICY-M1-L02` 灌 `gkx_policy` | done | 旧空间，禁止当目标态 |
| `DATA-POLICY-STORAGE-NEBULA-ETL-L01`、`DATA-POLICY-STORAGE-EDGE-SEMANTIC-L01` | done | 政策边语义文档 |
| `SCI-INT-C04` 三要素灌图 | ready_to_sign | 展示三要素集成，空间口径以 Z02 / L01 为准 |
| `SCI-REALDATA-P5` 创新要素图 | done | 落 ADS 表，不是图库闭环 |
| `DATA-ENT-GRAPH-OPS-L01` 企业图接正式 DWD | blocked | 我方写图，不替代燕大闭环 |
| `GDF-POLICY-MDC-DOC-L01` | integration | 政策 MDC/Graph/MRC 说明，R02 必读 |
| `CROSS-KG-HANG-BATCH-L01` 政策上图 FETCH | backlog | 未开工，不当依赖 |
| `CROSS-KG-SAD-L01` | in_progress | 未会签，禁止把接口形状抄进实施方案当契约 |
| `DEMO-ENT/CHAIN/SVC/POLICY-GRAPH-TRIPLE-UI` | 混合 | Demo 三元组。正式方案不回落到 demo 服务 |
| `DEMO-COMP-GRAPH-TRIPLE-UI-L01` | backlog | 同上 |

### 6.3 使用（页面或门面，多数还不是燕大读图）

| 任务 | 状态 | 备注 |
|---|---|---|
| `ENT-JAVA-GRAPH-DIST` | integration | Java 企业图谱门面 |
| `ENT-REALDATA-A4` 企业中心性 | done | 落 ADS，不是在线图算法 |
| `ENT-MOD-RISK-SUPPLY-GRAPH-SYNC-LUMEN`、`ENT-YIJI-INFER-PANEL-L01` | integration | 企业风险/推理图 |
| `LUMEN-SVC-JAVA-API-ECO-GRAPH-L01`、`LUMEN-SVC-FE-US-ECO-04` | blocked | 服务链生态图 |
| `DEMO-SVC-LAB-GRAPH-L01` | integration | hang `demo_gkx_chain` |
| `CHAIN-FE-L03` G6 | backlog | 页面关系图，R05 要标明是不是 Nebula |
| `FE-DISPLAY-KG-SERVICE-ALIGN-L01` | review | 展示·服务展示对齐 |
| `FE-TS-02A`、`FE-TS-10A` | integration | 科学技术全景/维护里的图 |
| `FE-TA-03A` | integration | 人才合作网络、领域图谱 |
| `FE-DR-01A`、`FE-DR-03A` | integration | 资源关联图谱 |
| `LUMEN-INTEL-FE-COLLAB` | integration | 综合分析协同图 |
| `CMS-JX-KG-STAGE/REL/ATTR-L01` | integration | **只做 overlay，不碰 Nebula** |
| `SYSINT-03-02B-L01` 产业全景指标与图谱数字 | claimed | 第 3 项交叉，R05 标明归不归本闭环 |

R05 不必把上表每一行都打开源码。每一行给四列结论即可：页面、图上展示什么、Nebula/燕大/页面关系图、归本闭环还是排除。没打开的写「还没有」。

---

## 7. 开工顺序

1. 认领并完成第一波 R01、R02、R04、R05。各交一份 handoff，状态到 `ready_to_sign`。不要写「会签通过」。
2. 两份前序 handoff 到了再认领 R03、R06。
3. 三份前序 handoff 到了再认领 `KG-CLOSELOOP-SCHEME-L01`。方案写到 `07-图数据库集成/实施方案.md`。
4. 方案叶自己停在 `ready_to_sign`。不标 `done`。不派开发叶。

卡住只允许：燕大测试环境从部署网络也不可达、要新建图空间或改 VID、要写正式库。单叶实际费用 > $10 暂停该叶。

---

## 8. 废作与禁止

不要派、不要当依赖、不要把结论抄进方案当契约：

- `KG-YANDA-GAP-L01` 的 v1.1 文本（用 L05）
- SAD v0.3 里的路径、点类型、边类型
- `gkx_policy` 作为目标图空间
- 任何 `demo-*` 服务作为 lumen 正式下游
- 在本轮新建 `SYSINT-07-*` 以外的开发叶，或派已经存在的 `SYSINT-07-01`～`03`
