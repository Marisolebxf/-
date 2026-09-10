# 跨系统向量库 · 总派单（厚包）

> 配合 [`CROSS-VEC-长任务总控.md`](./CROSS-VEC-长任务总控.md)。细叶步骤仍以 [`派单/`](./派单/) 各包为准。  
> 调度者只编排、认领、派 `/goal`。**不写业务代码。**

## 0. /goal 公共头

```text
监管：human:淮政玮 · claim_type=coordinator_dispatch · lock_hours=24
总控：agent-delivery/agent-handoffs/产品整体定义/跨系统-向量库/CROSS-VEC-长任务总控.md
特殊授权：不等 SAD/ARCH-SIGN 正式双签；按 v0.3-draft + 总控 §0 施工。
铁律：算法只在 Python /internal/*；Java 禁 NLP / 禁直连 19530；禁止 amcpdp-*；禁止假 VID；
      D12 lumen 不调 demo-*；数仓 demo_gkxlumenx_*；图 demo_gkx_chain。
git：push origin/dev；禁止 force；commit [agent:<role>]。
handoff：agent-handoffs/产品整体定义/跨系统-向量库/{task-id}.md
         含 ponytail / cost 四字段 / 架构合规；定义叶 ponytail: N/A。
```

## 1. Wave 1（已授权并行）

### 1.1 CROSS-VEC-SAD-L01 · architect-agent

```text
/goal architect-agent
身份：资深系统架构师；只评审与维护基线，不写业务代码。
任务：CROSS-VEC-SAD-L01
目标：跨系统向量库 SAD 按 v0.3-draft 施工关门（含 ETL Job A/B 切面）。正式双签后补，不挡主链。
仓库：${GKX_ROOT}/gkx-orchestration（agent-delivery）
必读：跨系统-向量库 INDEX+01/02/03；跨系统-知识图谱 02§3.1；长任务总控 §0。
铁律：向量不替代建图；重灌不上图/不 search；Job A/B 为长任务；禁止 amcpdp-*。
冻结：建库=灌链末段 rebuild；夜班 Job A→Hang；G3 分析不是上图。
产出：INDEX 封面写「2026-09-10 淮政玮特殊授权按 draft 施工」；handoff CROSS-VEC-SAD-L01.md（cost）。
禁止：改 lumen-* 业务代码；当生产 OpenAPI；等待李伟/徐滕强签字才交卷。
```

### 1.2 CROSS-VEC-POLICY-L0-L01 · algorithm-agent

```text
/goal algorithm-agent
身份：资深 Python 算法工程师。算法只在 Python；Java 禁止 NLP。
强度：ponytail full。禁止用 YAGNI 跳过可观测与架构铁律。
任务：CROSS-VEC-POLICY-L0-L01
仓库：${GKX_ROOT}/repos/lumen-algo-py
必读：跨系统-向量库/02-概要设计.md §1.1 §3；派单/CROSS-VEC-POLICY-L0-L01-派单包.md；长任务总控。
目标：政策 ODS→DWD 重灌 L0 — theme 只进 ext5，退出 related_entities.industry；L1 字面对图名保留。
不做：Milvus、LLM、embed/rebuild、假 VID、改 Java/前端。
验收：pytest 证明纯 theme 无 chain:INB*；handoff 含 ponytail: full 与 cost。
分支：push origin/dev；commit [agent:algorithm-agent]。
监管：human:淮政玮；先 MCP task-claim 再改代码。
```

## 2. 后续叶（空槽再派，勿抢 lumen-algo-py）

| 下一空槽 | ID | Agent | /goal 指针 |
|----------|-----|-------|------------|
| 定义（可与 algo 并行） | ARCH-SIGN | architect | `派单/CROSS-VEC-ARCH-SIGN-L01-派单包.md`；总控 §0 #4–#6 #11–#12 |
| algo 空 | DEVOPS-NET | devops | `派单/CROSS-VEC-DEVOPS-NET-L01-派单包.md`；只开通 19530 |
| algo 空 | PY-INDEX | algorithm | `派单/CROSS-VEC-PY-INDEX-L01-派单包.md`；内存回退可先交 |
| algo 空 | CHAIN-HOOK | algorithm | 汇合 NET+INDEX |
| Java 空 | API-FEIGN | api | 未就绪 501 |
| algo 空 | POLICY-SEARCH | algorithm | 重灌默认关 |
| 旁路 | JOB-A / API-JOB / HANG / JOB-B | 见派单 README | 不进本轮 #1–#6 必绿 |

## 3. Convoy

- `lumen-algo-py`：L0 → NET → INDEX → HOOK → SEARCH → JOB-A → HANG → JOB-B（同时只一张）。  
- `lumen-svc-platform`：FEIGN → API-JOB。  
- `agent-delivery`：SAD 与 ARCH-SIGN 不要两名 architect **同时改同一 SAD 目录**；SAD 交卷后再派 SIGN，或同一会话串写。
