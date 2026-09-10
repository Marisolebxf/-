# 跨系统向量库 · 长任务总控（无人值守）

> **日期**：2026-09-10  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **特殊授权**：施工 **不等 SAD / ARCH-SIGN 正式双签**。v0.3-draft 即为开工真源；李伟 / 徐滕强 / 唐绍祖 **后补签不挡主链**。  
> **目标**：产业锚点向量面可测闭环：政策 L0 主题退出产业槽 →（会签纪要可后补）→ 出网 19530 + Python rebuild/search → 灌链末段挂钩 → Java Feign → 政策语义抽槽；夜班 Job A / Hang / Job B 按旁路排队。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md) v1.13  
> **设计真源**：[`INDEX.md`](./INDEX.md)（v0.3-draft）· [`派单/README.md`](./派单/README.md)  
> **对照**：知识图谱 [`跨系统-知识图谱/INDEX.md`](../跨系统-知识图谱/INDEX.md)（Hang ≠ G3；向量不替代建图）  
> **执行 agent 按本文件已拍板项继续**，禁止把「等会签 / 等用户」当默认阻塞。

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| 0 定义 | `gkx-orchestration` | `origin/dev` | `CROSS-VEC-SAD-L01` · `CROSS-VEC-ARCH-SIGN-L01` | 特殊授权：draft 即可施工；两叶可并行写纪要，**不挡** L0 |
| A 政策 L0 | `lumen-algo-py` | `origin/dev` | `CROSS-VEC-POLICY-L0-L01` | **可抢跑**：不等 ARCH-SIGN、不等 SAD 双签 |
| B 出网 + 索引 | `lumen-algo-py` | `origin/dev` | `CROSS-VEC-DEVOPS-NET-L01` ∥ `CROSS-VEC-PY-INDEX-L01` | 同仓仍串行；PY-INDEX **可先内存回退**；出网按 §0 冻结地址 |
| C 挂钩 / 门面 | `lumen-algo-py` · `lumen-svc-platform` | `origin/dev` | `CHAIN-HOOK` → `API-FEIGN` ∥ `POLICY-SEARCH` | 联调闸门解锁，不等签收 |
| D 夜班旁路 | 同上 | `origin/dev` | `JOB-A` → `API-JOB` → `HANG`；`JOB-B` 等 SEARCH | 不进主 DAG 金路径 |
| E | devops + qa | K8s `dev` | 本轮 **不派** 专题金路径；连通性 + pytest 即闭环 | 禁止逐叶 QA |

厚包：[`CROSS-VEC-总派单.md`](./CROSS-VEC-总派单.md) · 细叶：[`派单/`](./派单/)  
金路径：本文件 §4 · 缺陷包：[`templates/long-task-e-defect-pack.md`](../../templates/long-task-e-defect-pack.md)

---

## 0. 已拍板（落盘即生效 · 执行勿问）

| # | 议题 | 决定 |
|---|------|------|
| 1 | 轨道 | 跨系统平台能力（展示+专题共用产业锚点）。D12：lumen 只经网关调 `gkxlumen-*`；算法只在 Python `/internal/*`。禁止 lumen 调任何 `demo-*` 服务 |
| 2 | 建库切面 | **仅**产业链灌数：DWD 链表 + 上图 VID 稳定后 **一次** `embed/rebuild`。禁止映射逐行 embed |
| 3 | 消费切面 | 政策/企业 **重灌同步** = L0+L1，**不调** Milvus / LLM / rebuild。search / L2 只走按钮或 ETL Job |
| 4 | 物理引擎 | 现网 Milvus **2.4 standalone** = **`192.168.88.43:19530`**。不采购第二套向量云。<br>🟢 **2026-09-11 `human:淮政玮` 确认**（升级项 A 关闭）：地址口径就是 88.43，并提供 compose 真源（见 §5）。原设计稿 `192.168.88.48:19530` **作废**（该机无 Milvus 容器 / 无进程 / 19530 refused，`CROSS-VEC-DEVOPS-NET-L01` 从节点与 4 个 Pod 实测）。SAD 01 §2.1 / 02 §2 / 03 §0 的 88.48 待架构同步订正（文档项，不挡施工） |
| 5 | collection | **禁止**读写或 drop `amcpdp-*`。<br>**⚠️ as-built 更正（同上实测）**：前缀必须用下划线 **`gkxlumen_industry_`**（建议名 `gkxlumen_industry_anchor`）。Milvus 硬校验拒绝连字符，`gkxlumen-industry-anchor` 实测报 `code 1100 Invalid collection name`——原写法**物理建不出来**。SAD 03 §0 同步修订 🟡 待架构（升级项 C） |
| 6 | 定码 | 向量分数 **不得**写成 `industry_link_code` / `chain:INB*`。定码仍走图谱 VID + FETCH。无码只留 `{name}` |
| 7 | theme | 政策 `theme` **只进** DWD `ext5`，**退出** `related_entities.industry` |
| 8 | VID | 只用图上链码（例 `chain:INB170101`）。禁止把 ODS 短码或中文名当 VID、禁止伪造 `chain:INB1303` |
| 9 | 数仓 | 数据面 **`demo_gkxlumenx_*`**。禁止无闸门写正式 `gkxlumenx_*` |
| 10 | 图 | 一张 G = **`demo_gkx_chain`**。向量不替代建图；RAG 不是建图开工条件 |
| 11 | VEC-Q2（施工默认） | 文本 embedding ≠ `amcpdp` 多模态。本轮 PY-INDEX：**pytest 内存回退必绿**；连上 19530 再用仓内已装文本模型，`model_version`+`dim` 写入 collection 与 handoff。正式模型名书面会签后补，**不挡**内存实现。度量建议 COSINE（`ARCH-SIGN` 建议页，🟡） |
| 16 | **客户端前缀守卫（新增硬闸）** | 现网 Milvus `authorizationEnabled=false`，**没有账号级隔离**，任何能连 19530 的进程都是超级权限，且同实例住着 `aip_kb_1` / `aip_kb_2` / `spk_id_speaker_embeddings` 等在用库。因此 **PY-INDEX 必须在客户端校验** collection 名以 `MILVUS_COLLECTION_PREFIX`（`gkxlumen_industry_`）开头才允许 `create` / `drop` / `insert`，否则拒绝并报错。这是当前唯一防线，**不得**以「运维会开鉴权」为由省掉 |
| 12 | VEC-Q5 | Job A 增量默认可调度、全量须审批；Job B **默认关**（`enable_llm=true` 才跑） |
| 13 | 监管 | `supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`，`lock_hours=24` |
| 14 | 会签 | **特殊授权：不等正式双签**。SAD / ARCH-SIGN 仍交 handoff 纪要；缺失签字标 🟡 后补，主链继续 |
| 15 | 本轮不做 | 匹配推送、企业挂链 UI、链检索 UI、文档 RAG、改 `amcpdp-*`、G3 分析 Job、B 面发布作业、MATCH/ENT 建单 |

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：升 ready 后直接认领开工，不要等聊天确认。  
2. **已拍板不回问**：§0 十五项 + 调用链/废作。  
3. **会签 🟡**：诚实记「后补签」，**不停工**。  
4. **结构歧义**（新表/改主键/新 ES 索引/改 Milvus `amcpdp-*`）：该叶 `blocked` + 升级 **`human:李伟`**；同段其它叶继续。  
5. **缺数据 / 连不上 19530**：PY-INDEX 返回 degraded/非 0，禁止假 VID；DEVOPS 只交连通性探测。  
6. git：lumen / orchestration 推 `origin/dev`；禁止 force；commit `[agent:<role>]`。  
7. 每叶 handoff + `ponytail:`（定义叶 `N/A`）+ cost 四字段。`ready_to_sign→done` 可积压。  
8. **同仓 Convoy**：`lumen-algo-py` / `lumen-svc-platform` **同时只派一张** coding 单。定义叶（SAD / ARCH-SIGN，`agent-delivery`）可与 L0 **并行**。  
9. 本轮 **禁止逐叶 QA**；连通性与 pytest 写进各叶 handoff。段 E 专题金路径不在本管线。

锁：`lock_hours=24`。lease 过期则同一监管人续领，不改设计。

---

## 2. 依赖（联调闸门，见规约 §6）

```text
SAD-L01 ──┬── POLICY-L0（可抢跑；本总控授权：不等 SAD 双签 / 不等 ARCH-SIGN）
          └── ARCH-SIGN ──┬── DEVOPS-NET ──┐
                          └── PY-INDEX ────┴── CHAIN-HOOK
                                    │
                                    ├── API-FEIGN
                                    └── POLICY-SEARCH ── JOB-B（L2）/ MATCH / ENT（后，未建单）
```

夜班旁路（不进上图）：`JOB-A`（等 PY-INDEX + L0 + CHAIN-HOOK）→ `API-JOB` → `CROSS-KG-HANG-BATCH-L01`。

废作 / 不要派：把 RAG 写成建图前置；政策重灌里 search/rebuild/LLM；伪造 `chain:` 短码；改 `amcpdp-*`；MATCH/ENT UI。

---

## 3. 开工顺序

1. **Wave 1（本会话已派）**：`SAD-L01`（architect）∥ `POLICY-L0`（algorithm）。  
2. Wave 1 后：`ARCH-SIGN` 交书面纪要（可与 L0 收尾重叠；不挡 L0）。  
3. `lumen-algo-py` 空槽：`DEVOPS-NET` → `PY-INDEX`（若 L0 已交则先 NET 再 INDEX；INDEX 可先内存）。  
4. 汇合：`CHAIN-HOOK`。Java 空槽：`API-FEIGN`。algo 下一空槽：`POLICY-SEARCH`。  
5. 旁路：`JOB-A` → `API-JOB` → `HANG`；`JOB-B` 最后。  
6. 卡住只允许：真环境不通、正式库误写、要动 `amcpdp-*`、cost 硬闸。

---

## 4. 金路径（本轮验收 · 非专题 E1）

> **期望未发生必红**。空态只有写进本行才算过。

| # | 叶 | 期望（未发生=红） | 允许的空态 |
|---|-----|-------------------|------------|
| 1 | POLICY-L0 | 纯 `theme=监督管理` 且标题无链名 → 产业槽 **无** `chain:INB*`；theme 在 `ext5` | 标题含图上链名仍可 L1 对码 |
| 2 | PY-INDEX | 本地 pytest 内存 rebuild/search 绿；单测无 `amcpdp-` | 19530 不通 → degraded/非 0，禁止假 VID |
| 3 | DEVOPS-NET | helm/env 文档化可连 **`192.168.88.43:19530`**（as-built，§0 #4）；不得 drop `amcpdp-*` | 仅探测，不 insert 业务向量 |
| 4 | CHAIN-HOOK | 灌链末段仅一次 rebuild；点未稳定则跳过并保留上一 `index_version` | — |
| 5 | API-FEIGN | Java 只 Feign `/internal/industry/embed/*`；未就绪 **501** + honesty | 禁止 200 假 VID |
| 6 | POLICY-SEARCH | 独立入口才 search；reload/append 默认同步不调 search | LLM 假 `chain:` 必须丢 |

P1 不挡本轮闭环：Job A/B、Hang、MATCH/ENT。

---

## 5. as-built · Milvus 实例拓扑（`192.168.88.43`）

> 来源：2026-09-11 `human:淮政玮` 提供的 docker compose（确认升级项 A 时附）+ `CROSS-VEC-DEVOPS-NET-L01` 只读实测。**这是运维既有环境，本管线只消费，不改。**

| 项 | as-built |
|----|----------|
| Milvus | `harbor.htmisoft.net/internet/milvusdb/milvus:v2.4.0`，`milvus run standalone`，`19530:19530` |
| etcd | `quay.io/coreos/etcd:v3.5.0`，卷 `/docker/etcd` |
| MinIO | `minio:latest`，卷 `/docker/milvus-minio`，**数据端口 9900 / 控制台 9901**（非默认 9000）；bucket **`a-bucket`**；`STORAGE_TYPE=minio` |
| 鉴权 | compose **未设** `authorizationEnabled` → 走镜像内默认 **`false`**（与实测 `/milvus/configs/milvus.yaml:586` 一致） |
| 同实例在用 collection | `aip_kb_1` · `aip_kb_2` · `spk_id_speaker_embeddings`（**只读，禁动**） |
| `amcpdp-*` | **该实例上不存在**：连字符名被 Milvus `code 1100` 拒，物理不可能建出。设计稿的隔离对象不在 88.43（另有 88.49 / 88.54 / 88.249 也开 19530，88.54 疑似多媒体：`clip_image_collection` / `assets*`，未确认，不写入盘点） |

### 5.1 对升级项 B（开鉴权）的影响 —— 运维需知

`milvus` 容器**没有挂配置卷**（只有 etcd / minio 有 `volumes`）。因此要打开 `authorizationEnabled`：

- 不能直接编辑容器内 `/milvus/configs/milvus.yaml`（重建即丢），必须**新增配置文件挂载**或用**环境变量覆盖**该项，二者都要改 compose 并重启 `milvus` 容器；
- 重启会中断同实例在用系统（`aip_kb_*` / `spk_id_*`）→ 须运维窗口；
- 开鉴权后口令进 K8s Secret `lumen-algo-milvus`（`DEVOPS-NET` 已预留 `secretRef optional:true` 位），**不进 git**。

在 B 落地前，**唯一防线是 §0 #16 客户端前缀守卫**。

### 5.2 顺带记录（非本管线范围）

MinIO 用默认 `minioadmin/minioadmin`；Milvus 无鉴权且 19530 对网内开放。属运维既有配置，本管线不改、不扩权，仅在此登记供安全评审参考。
