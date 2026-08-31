# 派单厚包 · 五域图谱三元组闭环（界面 + apiview）

```yaml
---
doc_id: COORD-GRAPH-TRIPLE-UI-DISPATCH
dispatcher: agent:coordinator-agent
supervised_by: human:淮政玮
date: 2026-08-31
amended: 2026-08-31
amendment: "P0：图谱相关操作从灌数完全剥离；图谱菜单 A/B/C/D；每关系 op_id+I/O"
claim_type: coordinator_dispatch
status: claimed
---
```

> 调度者只建单、写厚包、给 `/goal`。**不写业务代码。**  
> 五叶已代派 `claimed`（见 §6）。registry 初版 DoD 改不了行，**执行真源=本厚包**。

**P0 硬闸（五叶每一叶、handoff 缺此条必退回）**：把**所有图谱相关操作**从「灌数」逻辑中**完全剥离**。含：NER / RE / 建点 / 建边 / Nebula `ensure_schema` / `INSERT VERTEX|EDGE` / 图投影 / hang。灌数入口（`run-pipeline` / `run_all_*` / 基础指标页「灌数据」/ `reload|append|replace`）**零调用**上述路径。图只允许从各域「图谱」菜单（及对应 `/v1/*/graph/*`、apiview `op_id`）触发。

## 1. 为什么派

政策 106/107 设计已写入 `storage/POLICY/etl/pipeline-to-nebula.md` §10–§16，但 Demo **规则抄字段、关联主体缺稳定 ID、图谱页仍写 `gkx_policy`、apiview 未按三元组验收**。  
企业 / 产业链 / 服务 / 综合的 `pipeline-to-nebula` 更薄（或缺失），两端页面也未按需规边集核对。

用户要求：每域同一条闭环——**先查原始需求 → 写入该域 `pipeline-to-nebula` → 界面对应该图谱 → 算法测试对到 `lumen-ui-algo-apiview` → 支持的关系三元组不能有遗漏**。

## 2. 五叶

| ID | 页 | SRS | 存储管道 | system-test | apiview |
|---|---|---|---|---|---|
| `DEMO-POLICY-GRAPH-TRIPLE-UI-L01` | 政策图谱 | 05 seq **106/107** `政策/图谱.md` | `storage/POLICY/etl/pipeline-to-nebula.md`（已有 §10，本叶补齐对照并驱动页） | `/policy/graph` | `policy.graph` |
| `DEMO-ENT-GRAPH-TRIPLE-UI-L01` | 企业图谱 | 05 seq **108/109** `企业/图谱.md` | `storage/ENT/etl/pipeline-to-nebula.md`（现仅指针） | `/entan/graph` | `entan.graph` |
| `DEMO-CHAIN-GRAPH-TRIPLE-UI-L01` | 全景/专题全景 | 05 seq **102/103** `产业链/图谱.md` | `storage/CHAIN/etl/pipeline-to-nebula.md`（现仅指针） | `/chain/panorama` `/chain/topic-panorama` | `chain.panorama` `chain.topic-panorama` |
| `DEMO-SVC-GRAPH-TRIPLE-UI-L01` | 产业服务图谱 | 05 seq **112/113** `产业服务/图谱.md` | **现无文件，本叶新建** | `/industry-service/graph` | `svc.graph` |
| `DEMO-COMP-GRAPH-TRIPLE-UI-L01` | 综合·图谱API | 05 seq **116** `综合/图谱API.md` | **无 `storage/COMP`，本叶 draft 指针** | 现无 graph 菜单，须补 | 须增 `comp.graph` 并纳入 `GRAPH_IDS` |

标题笔误：`DEMO-ENT-GRAPH-TRIPLE-UI-L01` 看板标题里「517」应为 **108/109**（已记 note）。

## 3. 必须覆盖的三元组（需规最低集）

页 / apiview / pipeline **同一张表**。做不到的标「本波不上图/无 ID」，**禁止静默删行**。

| 域 | 边（或关系名） | 典型终点 |
|---|---|---|
| 政策 | `support` 扶持 · `apply_to` 适用 · `regulate` 监管 · `cite` 引用 | 产业 / 技术 / 企业 / 人才 / 科研机构 / 服务机构 / 政策 |
| 企业 | 合作 · 投资 · 归属 · 产业所属 · 技术应用 · 人才关系 · 政策适用 · 科研合作 · 服务提供 | 产业 / 技术 / 人才 / 政策 / 科研 / 服务 |
| 产业链 | 产业-技术 · 产业-企业 · 产业-人才 · 产业-科研机构 · 产业-服务机构 · 产业-政策 | 见名 |
| 服务 | 服务机构-产业 · 技术 · 企业 · 政府 · 人才 · 政策 · 科研机构 | 见名 |
| 综合 | **不另造边**；消费一张 G 已有跨域三元组；API：实体检索 / 关系查询 / 可视化 / 语义相似 / 网络指标 | 已上图的全部类型 |

现网政策 as-built：产业可同时 `support`+`apply_to`；tech/talent 本波不上图（`OPEN-POLICY-GRAPH-01`）；无稳定 ID 不上图。其它域同样：**对不齐不上图，禁止名称猜 VID**。

---

## 0. 口径修订（2026-08-31）— 加工离灌数、进图谱菜单

### 0.1 拍板 + 灌数剥离清单（五叶强制）

识别 / 关系 / 跨域挂接是分析算子，**不是**贴源灌数。现网政策 `run_all_policy` 的 B/`entity.py`、B+/`nebula_loader` 必须迁出；企业 / 产业链 / 服务 / 综合各自 `run_all_*`、`run-pipeline`、灌数按钮同样清干净。

| 层 | 灌数只做 | 灌数禁止（完全剥离） |
|---|---|---|
| 允许 | 三方/Mock → ODS → DWD；可选基础指标 ADS | — |
| 禁止 | — | 调 `entity.py` / `nebula_loader` / hang-to-graph；TRUNCATE 图谱 ADS 后重写；`CREATE TAG/EDGE`；任何 nGQL 写；页面文案「灌数会建图」 |

过关自检（handoff 必附）：

1. 灌数脚本 / `build_steps` / `run-pipeline` **grep 不到** graph/nebula/entity NER-RE 调用。  
2. 基础指标页灌数成功后，**不**自动增加 `policy_graph_*` / 各域图 ADS / Nebula 边（重灌后图空或保持旧图、由图谱菜单另建）。  
3. 图谱 A/B/C 才写 ADS 图面与 Nebula。

重灌后图空是预期。禁止灌数静默把图填满。

### 0.2 图谱菜单四块（建议一页四档，不要先拆 15 张 registry 单）

POLICY / ENT / CHAIN / SVC 各域「图谱」菜单必须有：

| 档 | 名称 | 含义 | 写什么 |
|---|---|---|---|
| A | **实体识别** | 只认本域自身实体 | 政策：政策点+属性 NER；企业：企业本体；链：chain/segment；服务：机构本体 |
| B | **关系边上图** | 本域实体 ↔ 本域其他实体 | 政策：`cite`；企业：投资/归属/合作（企业-企业）；链：上下游/环节边 |
| C | **关联主体上图** | 本域实体 ↔ **其他域**已有顶点 | 政策 `support/apply_to/regulate`；企业-产业/政策/服务…；须 FETCH 到 `chain:`/`ent:`/`inst:`/`pol:` |
| D | **浏览** | 只读子图 | 现网 GraphView / 全景；不写库 |

综合（116）**没有 A/B/C 写入**，只做 D + 查询 API（检索/关系/可视化/语义相似/网络指标）。跨域边由各域 C 档负责。

### 0.3 算法：每类关系一张入库接口（真源写进 pipeline-to-nebula）

禁止「一个 `graph.run()` 包打天下」当对外契约。每条需规关系（或一组同构边）必须有：

| 字段 | 要求 |
|---|---|
| `op_id` | 如 `POLICY_RE_SUPPORT` / `ENT_RE_INVEST` |
| 档 | A / B / C |
| HTTP | `POST /v1/{domain}/graph/{ner\|intra\|hang}` 或更细；内部 `/internal/...`；**Java 只转发** |
| 输入 | `scope=one\|batch`；`id` 或过滤；`mode=rule\|llm`；`dry_run`；关系白名单；禁止无 ID 猜 VID |
| 输出 | `written_nodes[]` / `written_edges[]`（src, rel, dst, weight, props）；`skipped[]`（原因码：`no_stable_id` / `not_in_wave` / `empty_field` / `vid_too_long`）；`source`；`model_version`；`calc_batch_id` |
| 幂等 | 同 `calc_batch_id`+主键可重跑覆盖；`dry_run` 不写 ADS/Nebula |

LLM 只出现在输入声明的 `mode=llm`；无 Key 回退规则并在输出标明。Java 禁止 NLP。

pipeline-to-nebula **必须先有**「关系 × 接口 × I/O」表，再写代码。apiview **每个 `op_id` 一条算法测试**（可一页多 endpoint）。

### 0.4 不拆 15 叶

五域仍各一叶。A/B/C/D 是页内档位 + API，不是新 task-id。同仓仍串行认领。

---

## 4. 叶内编排（三人三会话，同一监管人）

**一叶不够一个 frontend。** 必须 **data-agent → algorithm-agent → frontend-agent** 各开会话、各写所长；**监管人始终是该叶点名执行人**（§6 表），不另派第二监管。

| 步 | 谁开会话 | 只做什么 | 不做 | 本步完成物（下一步开工门） |
|---|---|---|---|---|
| 1 | **data-agent** | 读 SRS；写/补 `pipeline-to-nebula.md`：三元组全集、A/B/C 分档、每 `op_id` 入参/出参、入库 mermaid、灌数剥离清单 | 不改 Python/Vue；不灌数 | 编排仓文档 push；handoff 小节「数据设计」 |
| 2 | **algorithm-agent** | 灌数路径**完全摘掉**图操作；实现 A/B/C（综合仅查询）接口，I/O 与文档一致 | 不改图谱菜单页、不改 apiview catalog | 算法仓 push；grep 灌数无 graph/nebula；接口可 curl |
| 3 | **frontend-agent** | 灌数页去「建图」文案；图谱菜单 A/B/C/D；apiview 每 `op_id` 算法测试 | 不改口径、不发明新边 | UI 两仓 push；handoff 收口 |

闸门：**步 1 文档未齐，禁止步 2 写接口；步 2 灌数未剥离开、接口未齐，禁止步 3 接线。** 同叶同一时间只开一个 coding 会话（避免 Convoy）。

`supervised_by` **全程不变**。`claimed_by` 随当前步切换：

```
步1  claimed_by=agent:data-agent       supervised_by=human:{点名人}
步2  claimed_by=agent:algorithm-agent  supervised_by=human:{点名人}
步3  claimed_by=agent:frontend-agent   supervised_by=human:{点名人}
```

三人各一份短 handoff 段落，frontend 收口成 `agent-handoffs/.../{task-id}.md`。commit 标当前角色 `[agent:data-agent]` 等。

跨叶：政策 / 企业 / 链 / 服务 可并行（不同监管人）。徐滕强 ENT 与 COMP **串行**（先 ENT 三步走完再 COMP）。

## 5. 铁律（五叶共用）

- **P0 灌数剥离**：图谱相关操作从灌数**完全剥离**（见文首硬闸 + §0.1）。灌数路径仍调 NER/RE/Nebula/hang → 本叶未完成。  
- 调用链：前端 → Java 网关 → Python `/internal/*`；Java 不写算法、不直连 nGQL  
- 图谱：仅 NebulaGraph；Demo space **`demo_gkx_chain`**；禁止 Neo4j、禁止 `CREATE SPACE gkx_policy` / `gkx_service` / 综合第二张图  
- D8 Design / D9 ⓘ / D10 交互 / 可观测：不得用 ponytail 跳过  
- D12：lumen apiview 不打 `demo-*` 服务；`USE_MOCK=false` 禁止 fixture  
- demo 推 `origin/dev`；commit 标**当前步**角色（`[agent:data-agent]` / `algorithm-agent` / `frontend-agent`），禁止三人共用一个 agent 标签  
- 图：`图：必含 {域}-GRAPH-TRIPLE`（pipeline 内 mermaid）；handoff 填 `diagram_id`  
- 强度：ponytail **full**

## 6. 认领（2026-08-31 `human:淮政玮` 已点名代派）

`claim_type=coordinator_dispatch` · 锁 24h · 看板 `claimed_by` 现为点名人。**开第 1 个会话（data-agent）时**改 `claimed_by=agent:data-agent`，`supervised_by` **不准改**。步 2/3 同理只改 `claimed_by`。

| ID | 负责人 / 监管 |
|---|---|
| `DEMO-POLICY-GRAPH-TRIPLE-UI-L01` | `human:淮政玮` |
| `DEMO-ENT-GRAPH-TRIPLE-UI-L01` | `human:徐滕强` |
| `DEMO-CHAIN-GRAPH-TRIPLE-UI-L01` | `human:李伟` |
| `DEMO-SVC-GRAPH-TRIPLE-UI-L01` | `human:侯佳伟` |
| `DEMO-COMP-GRAPH-TRIPLE-UI-L01` | `human:徐滕强` |

徐滕强名下 ENT + COMP：同仓 **不要两叶同时开任一步会话**，先把 ENT 的 data→algo→frontend 走完再开 COMP。

---

## 7. `/goal`（每叶开 **三次** 会话，按步粘贴）

先看 §7.0 填空，再复制 §7.1 / §7.2 / §7.3。禁止只开 frontend 一条把设计+算法做完。

### 7.0 五叶填空

| 叶 | `{TASK}` | `{SUPER}` | `{SRS}` | `{PIPE}` | `{UI}` | `{APIVIEW}` | `{HARD}` | `{SCOPE}` |
|---|---|---|---|---|---|---|---|---|
| 政策 | `DEMO-POLICY-GRAPH-TRIPLE-UI-L01` | `human:淮政玮` | `政策/图谱.md` 106/107 | `storage/POLICY/etl/pipeline-to-nebula.md` | `/policy/graph` | `policy.graph` | `run_all_policy`/`run-pipeline`/灌数据 禁 entity.py、nebula_loader、nGQL 写 | A 政策本体；B `cite`；C support/apply_to/regulate；D 浏览 |
| 企业 | `DEMO-ENT-GRAPH-TRIPLE-UI-L01` | `human:徐滕强` | `企业/图谱.md` 108/109 | `storage/ENT/etl/pipeline-to-nebula.md` | `/entan/graph` | `entan.graph` | 企业灌数禁 entan.graph 建点边、nebula、hang-to-graph | A 企业本体；B 合作/投资/归属；C 跨域六类；D 浏览 |
| 产业链 | `DEMO-CHAIN-GRAPH-TRIPLE-UI-L01` | `human:李伟` | `产业链/图谱.md` 102/103 | `storage/CHAIN/etl/pipeline-to-nebula.md` | `/chain/panorama` `/chain/topic-panorama` | `chain.panorama` `chain.topic-panorama` | 链灌数禁 Nebula 投影、禁顺带 hang | A 产业/环节；B 链内边；C 产业-六主体；D 双全景 |
| 服务 | `DEMO-SVC-GRAPH-TRIPLE-UI-L01` | `human:侯佳伟` | `产业服务/图谱.md` 112/113 | **新建** `storage/SVC/etl/pipeline-to-nebula.md` | `/industry-service/graph` | `svc.graph` | 服务灌数禁 hang、禁写 Nebula | A 机构；B 服务-服务；C 跨域七类；D 浏览 |
| 综合 | `DEMO-COMP-GRAPH-TRIPLE-UI-L01` | `human:徐滕强` | `综合/图谱API.md` 116 | **新建 draft** `storage/COMP/etl/pipeline-to-nebula.md` | 补 `/industry-comp/graph` | 补 `comp.graph` | 综合灌数禁建图/投影；本叶不写 A/B/C | 仅 D + 116 五查询；写入在各域 |

### 7.1 步 1 · data-agent（先开）

```markdown
/goal data-agent
身份：你是经验丰富、遵循最佳实践的数据工程师，只写存储设计与口径，不写业务 Python/Vue。
强度：ponytail full（写文档完整性优先；禁止用 YAGNI 裁掉接口表/过程图）。
上下文：headroom 可选。SRS 与现网 pipeline 必须读原文，禁止 compress 代替精读。
任务：{TASK} · 步1/3
监管：{SUPER}（supervised_by 不准改；claimed_by 改为 agent:data-agent）
硬闸：文档必须写清「灌数路径零图谱操作」清单（现网哪个函数/按钮要摘掉），供步2对照删除。
图：必含 {域}-GRAPH-TRIPLE（每实体 + 每组关系入库 mermaid）
仓库：仅 gkx-orchestration 编排仓 {PIPE}（及 SVC/COMP README、storage/README 指针）
必读：bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/{SRS}；本厚包 §0 §3 §7.0；architecture-baseline D12
产出：{PIPE} 与 POLICY §10–§16 同构；三元组零遗漏；每 op_id 入参/出参（scope/mode/dry_run、written/skipped 原因码）；A/B/C/D 分档={SCOPE}
禁止：改 demo-algo-* / demo-ui-* / lumen-ui-* 代码；不灌数、不 APPLY DDL
DoD：文档 push origin/dev；handoff 小节「数据设计」+ diagram_id + ponytail + cost；通知 {SUPER} 开步2
```

### 7.2 步 2 · algorithm-agent（步1 文档齐后）

```markdown
/goal algorithm-agent
身份：你是经验丰富、遵循最佳实践的算法工程师，只在 Python 实现图加工接口并从灌数剥离，不改 UI。
强度：ponytail full。禁止用 YAGNI 跳过可观测、接口 I/O 与灌数剥离。
上下文：headroom 推荐。步1 文档与现网 run_all 必须读原文。
任务：{TASK} · 步2/3
监管：{SUPER}（claimed_by 改为 agent:algorithm-agent）
硬闸：{HARD}。图谱相关操作从灌数完全剥离。grep run_all/run-pipeline/灌数入口，不得残留 graph/nebula/entity NER-RE。
图：实现须与步1 mermaid / op_id 表一致，禁止私自加边
仓库：${GKX_ROOT}/repos/demo-algo-ent-analysis（及该域既有模块）；Java 只预留 /internal 转发、本步可不改 Java
必读：步1 更新后的 {PIPE}；本厚包 §0.1 §0.3
产出：A/B/C 写入接口（综合叶只做 116 查询、不写图）；每 op_id 可 curl；dry_run；mode=rule|llm；无 Key 回退规则
禁止：改图谱菜单 Vue、apiview catalog；名称猜 VID；灌数里偷偷建图
DoD：算法仓 push；handoff 附 grep 证据（灌数无图调用）+ 接口样例；通知 {SUPER} 开步3
```

### 7.3 步 3 · frontend-agent（步2 接口齐后）

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的前端工程师，只接线图谱菜单与 apiview，不改口径、不写算法。
强度：ponytail full。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
上下文：headroom 推荐。Design.md / 步1 文档必须读原文。
任务：{TASK} · 步3/3
监管：{SUPER}（claimed_by 改为 agent:frontend-agent）
硬闸：灌数页/按钮去掉「会建图」文案与顺带调用；图操作只出现在 {UI} 的 A/B/C 档。
图：页面图例/测试覆盖步1 三元组表，不得漏行
复刻：{UI} ↔ {APIVIEW}；范围=四档加工+浏览+按 op_id 算法测试，不是整站重做
仓库：${GKX_ROOT}/repos/demo-ui-system-test · ${GKX_ROOT}/repos/lumen-ui-algo-apiview
必读：步1 {PIPE}；Design.md；data-lineage-policy.md；fe-replica-visual-dod.md；本厚包 §0
产出：菜单 A/B/C/D（综合仅 D+查询）；apiview 每 op_id 可测；source 写 demo_gkx_chain；去掉 gkx_policy 等旧文案
禁止：发明新边；USE_MOCK=false 时 fixture；直连 demo-* / Python（D12）
DoD：两仓 push；收口 handoff（数据+算法+前端）五列对照 + 灌数剥离证据 + diagram_id + ponytail: full + cost
```

## 8. 收单

缺任一步会话产物 → `needs-revision`。**灌数路径仍调用任何图谱操作 → 直接退回**（先于其它项）。另：缺 op_id I/O 表、菜单无 A/B/C（综合除外）、apiview 未按 op_id、无 mermaid / `ponytail:` / cost → 退回。

---

## 9. 政策叶执行单（等 `human:淮政玮` 确认后再启子智能体）

> 状态：**执行中。** `human:淮政玮` 已确认全链路；coordinator 串行开 P-1→P-2→P-3，步间不回头问。  
> 父单：`DEMO-POLICY-GRAPH-TRIPLE-UI-L01` · `supervised_by=human:淮政玮`（全程不变） · 当前步 P-1 `claimed_by=agent:data-agent`

### 9.0 集合一览

| 序 | 子智能体 | 开工条件 | 完成后 |
|---|---|---|---|
| P-1 | **data-agent** | 你回复确认 | 编排仓 `pipeline-to-nebula.md` 含 op_id I/O + 剥离清单；`claimed_by=agent:data-agent` |
| P-2 | **algorithm-agent** | P-1 文档已 push，coordinator 核过 | 灌数零图调用；A/B/C 接口可测；`claimed_by=agent:algorithm-agent` |
| P-3 | **frontend-agent** | P-2 grep+接口齐 | `/policy/graph` 四档 + apiview 按 op_id；收口 handoff；`claimed_by=agent:frontend-agent` |

同一时刻只跑一个子智能体。ENT/CHAIN/SVC/COMP **不在本集合**。

### 9.1 P-1 `/goal`（确认后原样下发）

```markdown
/goal data-agent
身份：你是经验丰富、遵循最佳实践的数据工程师，只写存储设计与口径，不写业务 Python/Vue。
强度：ponytail full（写文档完整性优先；禁止用 YAGNI 裁掉接口表/过程图）。
上下文：headroom 可选。SRS 与现网 pipeline 必须读原文，禁止 compress 代替精读。
任务：DEMO-POLICY-GRAPH-TRIPLE-UI-L01 · 步1/3
监管：human:淮政玮（supervised_by 不准改；开工时 claimed_by=agent:data-agent）
硬闸：图谱相关操作从灌数完全剥离。文档必须列出现网要摘掉的调用：scripts/run_all_policy.py 的 graph.run / nebula_loader、run-pipeline 灌数路径、基础指标页「灌数据」顺带建图。
图：必含 POLICY-GRAPH-TRIPLE（每类实体 + 每组关系入库 mermaid）
仓库：仅 gkx-orchestration · agent-delivery/data/data-design/storage/POLICY/etl/pipeline-to-nebula.md
必读：bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/政策/图谱.md（106/107）；本厚包 §0 §3 §9；architecture-baseline D12
产出：在已有 §10–§16 上补「关系×op_id×I/O」表与灌数剥离清单。A=政策本体 NER；B=cite；C=support/apply_to/regulate（终点产业/技术/企业/人才/科研/服务，tech/talent 本波不上图须标）；入参 scope=one|batch、mode=rule|llm、dry_run；出参 written_nodes/edges、skipped 原因码。
禁止：改 demo-algo-* / demo-ui-* / lumen-ui-*；不灌数、不 APPLY DDL
DoD：origin/dev push；handoff 小节「数据设计」+ diagram_id + ponytail + cost；停，等监管开 P-2
```

### 9.2 P-2 `/goal`（P-1 齐后下发）

```markdown
/goal algorithm-agent
身份：你是经验丰富、遵循最佳实践的算法工程师，只在 Python 实现图加工接口并从灌数剥离，不改 UI。
强度：ponytail full。禁止用 YAGNI 跳过可观测、接口 I/O 与灌数剥离。
上下文：headroom 推荐。P-1 文档与 run_all_policy 必须读原文。
任务：DEMO-POLICY-GRAPH-TRIPLE-UI-L01 · 步2/3
监管：human:淮政玮（claimed_by=agent:algorithm-agent）
硬闸：run_all_policy / run-pipeline / 灌数据 禁止调用 entity.py、nebula_loader、任何 nGQL 写。只留 ODS→DWD（+可选基础指标）。
图：实现须与 P-1 mermaid / op_id 表一致，禁止私自加边
仓库：${GKX_ROOT}/repos/demo-algo-ent-analysis（polan/graph、scripts/run_all_policy.py、api/policy_routes.py）
必读：P-1 更新后的 pipeline-to-nebula.md；本厚包 §0.1 §0.3 §9.1
产出：A/B/C 独立入库接口（可 /v1/policy/graph/ner|intra|hang 或按 op_id）；dry_run；mode=rule|llm；无 Key 回退规则；对不齐不上图
禁止：改 GraphView / apiview catalog；名称猜 VID；灌数里偷偷建图
DoD：dev push；handoff 附 grep 证据（灌数无图调用）+ curl 样例；停，等监管开 P-3
```

### 9.3 P-3 `/goal`（P-2 齐后下发）

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的前端工程师，只接线图谱菜单与 apiview，不改口径、不写算法。
强度：ponytail full。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
上下文：headroom 推荐。Design.md / P-1 文档必须读原文。
任务：DEMO-POLICY-GRAPH-TRIPLE-UI-L01 · 步3/3
监管：human:淮政玮（claimed_by=agent:frontend-agent）
硬闸：灌数页去掉「会建图」文案与顺带调用；图操作只出现在 /policy/graph 的 A/B/C。
图：图例/测试覆盖 P-1 三元组表，不得漏行
复刻：/policy/graph ↔ policy.graph；范围=四档加工+浏览+按 op_id 算法测试
仓库：${GKX_ROOT}/repos/demo-ui-system-test · ${GKX_ROOT}/repos/lumen-ui-algo-apiview
必读：P-1 pipeline-to-nebula；Design.md；data-lineage-policy.md；fe-replica-visual-dod.md；本厚包 §0
产出：A/B/C/D；apiview 每 op_id 可测；source=demo_gkx_chain；去掉 gkx_policy 与假 ID
禁止：发明新边；USE_MOCK=false 时 fixture；直连 demo-* / Python（D12）
DoD：两仓 push；收口 handoff（数据+算法+前端）+ 灌数剥离证据 + diagram_id + ponytail: full + cost
```

### 9.4 确认后 coordinator 动作（你点头才做）

1. `task-claim` `claimed_by=agent:data-agent` `supervised_by=human:淮政玮`  
2. Launch 子智能体 P-1（上列 `/goal`）  
3. 收 P-1 后再切认领、Launch P-2，再 P-3  
4. 不并行开 ENT/CHAIN/SVC/COMP

