# 算法库 bid-reference 合规 · 调度派单批（2026-08-04）

- **调度者**：coordinator-agent
- **监管人（本批统一）**：human:唐绍祖
- **Epic**：E-ALGO-LIB-DEMO
- **Sprint**：2026-W32
- **背景**：联调台 `#/chain/basic` 线上 A2–A9 404；根因为 gkx-innov/innov-py 部署漂移 + 网关/灌数/企业深度缺口。详见 `ALGO-LIB-BID-COMPLIANCE-GAP-L01.md`。

---

## 派单清单（按执行顺序）

| 序 | 任务 ID | 执行 Agent | 优先级 | 派单包 | 依赖 |
|----|---------|------------|--------|--------|------|
| 1 | CHAIN-DEPLOY-ROLLOUT-L01 | devops-agent（协 api-agent） | P0 | `CHAIN-DEPLOY-ROLLout-L01-派单包.md` | — |
| 2 | ALGO-GATEWAY-ROUTE-SYNC-L01 | api-agent | P0 | `ALGO-GATEWAY-ROUTE-SYNC-L01-派单包.md` | 可与 #1 并行 |
| 3 | CHAIN-PIPELINE-SMOKE-L01 | algorithm-agent | P0 | `CHAIN-PIPELINE-SMOKE-L01-派单包.md` | #1 |
| 4 | ENT-DEEP-GAP-L01 | algorithm-agent | P1 | `ENT-DEEP-GAP-L01-派单包.md` | 网关 (#2) 建议先通 |

**已有任务（唐绍祖监管/执行，勿重复建单）**

| 任务 ID | 状态 | 说明 |
|---------|------|------|
| SVC-ALGO-DESIGN-L01 | review | 产业服务 §9 设计 |
| COMP-ALGO-DESIGN-L01 | review | 产业综合 §10 设计 |

---

## 给唐绍祖的执行要点

1. **P0 先 rollout**：`demo-svc-platform@21e67ec`（gkx-innov）+ `demo-algo-science@cb132a6`（innov-py）；冒烟见 DEPLOY 派单包 §2.2。
2. **灌数闭环**：`POST /innov/v1/industry/internal/run-chain-pipeline` → A1–A9 有数据。
3. **网关**：确认 `/entan/**`、`/policy/**` 在 Nacos 与 yaml 一致（可转 api-agent 执行，唐绍祖收口验收）。
4. **P1 企业三缺口**：历程 / 招引 / 培育 REST（`ENT-DEEP-GAP-L01`）。
5. **数据阻塞**：Q053 产业链编码 🔴 — 登记客户决策清单，Mock 灌数须 handoff 注明。

---

## Registry 状态（2026-08-04 已建单）

| 任务 ID | 状态 | claimed_by | supervised_by |
|---------|------|------------|---------------|
| CHAIN-DEPLOY-ROLLOUT-L01 | **claimed** | human:唐绍祖 | human:唐绍祖 |
| ALGO-GATEWAY-ROUTE-SYNC-L01 | **claimed** | human:唐绍祖 | human:唐绍祖 |
| CHAIN-PIPELINE-SMOKE-L01 | backlog | — | （DEPLOY 完成后 ready） |
| ENT-DEEP-GAP-L01 | backlog | — | （GATEWAY 完成后 ready） |

> Registry 任务 ID 须全大写：`CHAIN-DEPLOY-ROLLOUT-L01`（派单包文件名保留 ROLLout 拼写）。

---

## 附件

- 总表：`ALGO-LIB-BID-COMPLIANCE-GAP-L01.md`
- 各 `*-派单包.md` 含 `/goal` 复制话术
