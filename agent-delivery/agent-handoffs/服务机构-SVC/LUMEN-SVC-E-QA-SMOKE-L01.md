# LUMEN-SVC-E-QA-SMOKE-L01 · 产业服务链 E1 — 金路径冒烟

> 日期：2026-08-17  
> Task：`LUMEN-SVC-E-QA-SMOKE-L01`  
> 总控：[`DEMO-SVC-ABCD-长任务总控.md`](./DEMO-SVC-ABCD-长任务总控.md) §4  
> E0：[`LUMEN-SVC-E-DEVOPS-L01.md`](./LUMEN-SVC-E-DEVOPS-L01.md)  
> 本单 **不改业务代码**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权「不必再问」；lock 24h。QA 不改代码。本机无法打通已发布 NodePort → **blocked**（非 ready_to_sign）。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过「只认已发布」「期望未发生必红」「诚实不造绿」。无浏览器可达证据则不标 PASS。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本单为已发布冒烟；本机网络闸门优先于 compress。 |

## 结论（给 coordinator）

**BLOCKED（C2 · 本机网络不可达已发布前端）— 五条金路径均 NOT_RUN，禁止冒充绿。**

- 契约 URL：http://192.168.88.50:30892 （`gkx-lumen-topic` NodePort；非 localhost / 非 demo）
- 本机实测：`curl` connect-timeout 8s → **exit 28 / http_code=000**（`/` 与 `/service-portal/overview`）；网关 `http://192.168.88.50:30899` 同超时
- E0 旁证（**仅发布门，不等于 E1 金路径绿**）：见 `LUMEN-SVC-E-DEVOPS-L01` — CI deploy 绿（ui-topic [5115](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5115)、topic-svc/async `b9e638a8`、topic-py、algo-py）；devops 同记「本机无法 SSH/NodePort 直连」
- CI SVC 金路径：`e2e:svc-gold` **尚未落地**；仓内仅有 `e2e:chain-gold`（产业链故事，**不能**代替 SVC §4）
- 缺陷包：无产品 C1（无页面现象、无 `X-Trace-Id`）；本叶失败分类 = **C2**
- **不写「联调通过」**（金路径未在已发布环境点测）

## 五条金路径（总控 §4）

| # | 路由（已发布） | 期望 | 判定 | HTTP / 证据 | 失败分类 |
|---|---------------|------|------|-------------|---------|
| 1 | `/service-portal/overview` | 门户可开；经 Java `/svc`；不造假 KPI；可诚实空 | **NOT_RUN / 红闸** | `curl` 30892 connect **timeout**（http_code=000） | **C2** |
| 2 | `/service-center/search` | 记录或诚实空；不 5xx | **NOT_RUN / 红闸** | 同上；未发 search API | **C2** |
| 3 | `/service/institution-judgment` | 机构分析工作区壳经 Java | **NOT_RUN / 红闸** | 同上 | **C2** |
| 4 | `/service/chain-analysis`（短板） | `svc:analysis:shortboard` 经 async 到可解释终态 | **NOT_RUN / 红闸** | 同上；未 Create/轮询 | **C2** |
| 5 | `/service/institution-decision` | 招引/培育壳可开或诚实拦截 | **NOT_RUN / 红闸** | 同上 | **C2** |

路由对照 FE as-built：`LUMEN-SVC-FE-ENTRY-L01` / `LUMEN-SVC-FE-WORKSPACE-L01`。

### 网络探测记录（2026-08-17 · QA 主机）

```text
curl.exe --connect-timeout 8 --max-time 15 http://192.168.88.50:30892/
  → curl: (28) Connection timed out ; http_code=000

curl.exe ... http://192.168.88.50:30892/service-portal/overview
  → curl: (28) Connection timed out ; http_code=000

curl.exe ... http://192.168.88.50:30899/
  → curl: (28) Connection timed out ; http_code=000
```

### E0 CI 旁证（不可升格为 E1 PASS）

| 点名 | E0 | 链接 / tag |
|------|-----|-----------|
| lumen-ui-topic | deploy 绿 | pipeline 5115 |
| gkxlumen-topic-svc | deploy 绿 | `b9e638a8` job 22413 |
| gkxlumen-topic-async-service | deploy 绿 | `b9e638a8` job 22411 |
| lumen-topic-py | 绿 | job 22226 |
| lumen-algo-py | 绿 | pipeline 5102 |

## 问题清单

1. **C2**：QA / devops 本机均无法直连 `192.168.88.50:30892|30899` → E1 无法在本会话完成 wait_view。
2. **缺口**：`e2e:svc-gold` 未建；无法用 GitLab runner（能达 NodePort 的那一侧）代跑 SVC 金路径。
3. 无 C1 缺陷包（无现象、无 trace）。

## 修改内容

- 无业务仓代码变更。仅本 handoff + registry 状态。

## 测试结果

- 五条金路径：**0 PASS / 0 产品 FAIL / 5 NOT_RUN（网络闸）**
- Playwright / 浏览器：未跑（前置 URL 不可达）
- D12 / KPI 诚实性：未在运行时验证（源码/FE handoff 有声明，**不作本单绿证**）

## 遗留风险 / 解阻建议

1. 在能访问 `192.168.88.50` 的 runner / 跳板复测本五条，或落地 `e2e:svc-gold` 后由 CI 打已发布 30892。
2. 解阻后：本叶清 `blocked` → `testing` → 点测 → 全绿再 `ready_to_sign`；任一期望未发生按规约 §11.4 分类后出缺陷包。
3. 禁止用 E0 CI deploy 绿代替 E1 金路径绿。

## CI/CD（必填）

- 分支：orchestration `dev`（仅 handoff）
- commit：见本仓 push
- pipeline：未触发业务仓（QA 不改代码）
- 部署 namespace / 镜像：沿用 E0（topic-svc/async `b9e638a8`；ui-topic pipeline 5115）
- K8s rollout：E0 已 PASS（CI kubectl）；本单未再滚
- dev 测试 URL：http://192.168.88.50:30892 — **本机不可达**

## 可观测性

- 本会话无业务 `X-Trace-Id`（请求未发出）
- Tempo / Loki：未查（无 trace）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 只认已发布前端 | ✅ 仅尝试 30892；未用 localhost |
| QA 不改业务代码 | ✅ |
| 期望未发生必红 | ✅ 未测路径标 NOT_RUN/红闸，不造 PASS |
| D12 | 未运行时验证（E0/FE handoff 旁证，不升格） |
| 失败分类 | ✅ C2；非 C1 |

## cost 四字段（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | Cursor Grok 4.5 |
| actual_cost | 0.25 |
| cost_warn | false |

口径：`budget-estimate.md`；`source: estimate`。未超 $5。

## 涉及文件

- `agent-delivery/agent-handoffs/服务机构-SVC/LUMEN-SVC-E-QA-SMOKE-L01.md`（本文件）
