# 段 C · 产业链 Java（lumen-svc-platform）总派单 · 长任务

> **日期**：2026-08-14  
> **监管**：`human:淮政玮`（无人值守，见 [ABCD 总控](./DEMO-CHAIN-ABCD-长任务总控.md)）  
> **执行**：`api-agent`  
> **仓**：`${GKX_ROOT}/repos/lumen-svc-platform` · push **`origin/dev`**  
> **强度**：ponytail **full**  
> **薄条**：[`DEMO-CHAIN-JAVA-C-派单条.md`](./DEMO-CHAIN-JAVA-C-派单条.md)

本段 **2 张长任务**。禁止再拆回 demo-svc-platform 13 GET 透传。

---

## 0. 模块落点（已拍板，勿问）

| 能力 | 落点 | 不要 |
|---|---|---|
| 产业查询 / 门户 / 发布快照 / 对象目录 | **新建** `gkxlumen-topic-chain`（api+biz），切法对齐 `gkxlumen-topic-enterprise` | 塞进企业模块；复制 `gkx-innov` ChainController |
| 生成分析 Job | **扩展** `gkxlumen-topic-async-service`（已有 `/topic/v1/analysis`） | 新建第三套任务微服务；把权威状态写进 Python `/gdf/tasks` |
| Feign Python | `lumen-algo-py` `/internal/v1/chain/**`（网关 `/lumen-algo`） | `demo-algo-science` `/v1/chain` |
| ADS | Java **只读** `demo_gkxlumenx_ads`（联调） | 扫 DWD；写 ADS；直连 nGQL |

`gkxlumen-topic` 现仅 health + `/internal/status` Feign，**不够**承载专题 REST，故新建 chain 模块。父 POM / boot / 网关路由一并挂上。

---

## 1. 铁律

- 算法只在 Python；Java 不做 NLP/图计算/LLM。  
- 前端只调本仓 REST。  
- 产业查询 **不**经 ES。Java 查询门面 Feign Python SEARCH，或只读 ADS 目录宽表——**以 B SEARCH 契约为准**，禁止自造 ES。  
- Snapshot：`task_id` / `input_snapshot_id` / `result_snapshot_id` **本段签发**；Python Complete 只交 `result_payload`。  
- `succeeded` → 前端 **wait_view**，禁止自动跳结果。  
- 互斥：同用户 + 同 `task_type`（`chain:{module}:{key}`）一条非终态。  
- 七键 Result 禁止写入 `industry_chain_graph_snapshot`。  
- 联调默认 Demo 库；禁止无闸门写正式 `gkxlumenx_*`。  
- 旧 `CHAIN-API-L01` 废作施工。

---

## 2. 长任务 A · `LUMEN-CHAIN-JAVA-FACADE-L01`

**依赖**：`DEMO-CHAIN-PY-SEARCH-L01` + `DEMO-CHAIN-PY-SYNC-L01`  
**一句话**：专题前端能经 Java 查产业、读门户 KPI、读全景发布快照、拉对象目录。

### 对外（对齐 Demo 路由，路径可微调但语义锁定）

| Demo 需要 | Java |
|---|---|
| 产业查询 | `/topic/v1/industry/search` → Feign Python SEARCH |
| 门户 KPI / 资讯列表头 | `/topic/v1/industry/overview/**` → ADS 只读 + 必要 Feign |
| 全景默认秒开 | `/topic/v1/industry/panorama/snapshot` → ADS `graph_snapshot` |
| 对象 Select | `/topic/v1/industry/catalog` |
| 指标 8 件套 | 走已有 `gkxlumen-metrics` catalog，不在 chain 模块手写就绪度 |

网关：`/topic/v1/industry/**` → chain 服务（不要再 Strip 到 innov `/v1/industry` 旧映射）。

### DoD

- 模块可启动；Nacos/dev 配置指向 Demo ADS + `algo-base-url`→lumen-algo-py。  
- search 三种 mode 与 Demo `IndustrySearchRecord` 字段能对上。  
- snapshot 与 Job Result **分 API**。  
- 无 ES 客户端。无 13 旧 GET。  
- 测：MockMvc 或契约测 + 一次联调 curl（B 未绿则测 Feign 契约，不造假数据）。  
- handoff `LUMEN-CHAIN-JAVA-FACADE-L01.md`。

---

## 3. 长任务 B · `LUMEN-CHAIN-JAVA-JOB-L01`

**依赖**：`DEMO-CHAIN-PY-JOB-RUNTIME-L01` + `DEMO-CHAIN-PY-JOB-KEY-LINK-L01`  
**一句话**：点「生成分析」走现有分析任务中心，厨房能托管 `chain:*`。

### 必须

- `analysisType` / `task_type` 注册：`chain:diagnosis:key_link` 先通，并预留七键 + `chain:panorama:graph` 白名单（其它键 B 后到时 **不必改前端路径**）。  
- Create → 冻 Input Snapshot → `POST` Python Execute → 收 Stage/Complete 回调 → 校验 schema → 签发 `result_snapshot_id`。  
- 过程事件给前端轮询/SSE（优先复用 async-service 已有 Get/List/SSE，差什么补什么，禁止另起一套 task 表）。  
- wait_view：succeeded 不自动当「已查看」。  
- 全景改条件：`chain:panorama:graph`；成功后调发布快照写入（ADS 写仍只允许 Python，Java 调 B PANORAMA Complete 后的发布语义以 B 为准：Python 写 snapshot，Java 不直接 UPDATE ADS 图）。  
- 报告任务只读 Result，禁止重跑分析（P1 可后做，本单至少 **挡住** 重跑入口）。

### DoD

- key_link 一条任务：Create→running→succeeded(wait)→GetResult。  
- Python 宕机 → failed，不假成功。  
- 不把企业 `enterprise_eval` 枚举写死导致 chain 被拒。  
- handoff `LUMEN-CHAIN-JAVA-JOB-L01.md`。

对照：`CONTRACT-Java-Python-Analysis-Job-v0.md` · Runtime · 企业 `AnalysisTaskController`（扩展而非分叉）。

---

## 4. `/goal`（两单通用头）

```text
/goal
你是经验丰富的 Java 平台工程师（api-agent）。
仓库：${GKX_ROOT}/repos/lumen-svc-platform · origin/dev
监管：human:淮政玮
强度：ponytail full。禁止用 YAGNI 跳过调用链、可观测、D9 门面。
上下文：headroom 推荐。Runtime/CONTRACT/Demo 页禁止 compress 代替精读。
必读：DEMO-CHAIN-JAVA-C-总派单.md · DEMO-CHAIN-ABCD-长任务总控.md
禁止：算法进 Java；Neo4j；扫 DWD；ES 产业查询；13 旧 GET；问用户选仓。
```

认领：`claimed_by=agent:api-agent` · `supervised_by=human:淮政玮` · `lock_hours=24`

---

## 5. 不做

CMS；OPS 写侧；lumen 前端；在 demo-svc-platform 加功能。
