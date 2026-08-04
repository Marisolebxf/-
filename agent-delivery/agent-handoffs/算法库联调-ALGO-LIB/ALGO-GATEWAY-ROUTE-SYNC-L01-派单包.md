# 派单包：ALGO-GATEWAY-ROUTE-SYNC-L01 — 算法库网关路由可复现同步

- **任务 ID**：ALGO-GATEWAY-ROUTE-SYNC-L01
- **派发角色**：coordinator-agent
- **承接角色**：api-agent
- **监管人**：human:唐绍祖
- **Epic**：算法库联调 · ALGO-LIB
- **effort / difficulty**：3 / M · est.tokens 100k
- **派发时间**：2026-08-04

---

## 1. 背景

`gkx-gateway-dev.yml` 当前仅含 `/innov/**`、`/topic/v1/industry/**`、`/chain/internal/**` 等。**缺少**：

- `/entan/**` → demo-algo-ent-analysis（企业分析 Python）
- `/policy/**` → 同上 FastAPI（policy_routes）

现网可能靠 **DB 一次性脚本**（`add_gateway_route.py`）注入，新集群/重建不可复现 → 企业/政策算法库联调不稳定。

另：chain internal 存在 **双轨**：

- 推荐：`/innov/v1/industry/internal/**` → gkx-innov → Python
- 兼容：`/chain/internal/**` → 直连 innov-py

---

## 2. 范围（必做）

### 2.1 更新 Helm/Nacos 路由 yaml

文件：`demo-svc-platform/helm/gkx-platform/configs/gkx-gateway-dev.yml`

新增（示例，以 PigX StripPrefix=1 惯例为准）：

```yaml
- id: gkx-entan
  uri: lb://demo-platform-entan-py   # 以 Nacos 实际服务名为准
  predicates:
    - Path=/entan/**
  filters:
    - StripPrefix=1

- id: gkx-policy
  uri: lb://demo-platform-entan-py   # policy 与 ent 同进程
  predicates:
    - Path=/policy/**
  filters:
    - StripPrefix=1
```

### 2.2 Nacos 同步

1. 审计现网 `sys_route_conf` 是否已有 ent/policy 路由
2. 与 yaml **双写一致**；缺失则补录
3. 记录 route id、uri、predicates 到 handoff

### 2.3 chain internal 统一说明

- 在 yaml 注释中标注 **推荐入口** = `/innov/v1/industry/internal/**`
- `/chain/internal/**` 保留兼容或标记 deprecated（architect 确认）
- 更新 `demo-ui-system-test/src/api/chain/index.ts` 头注释（若入口变更）

### 2.4 冒烟

| 路径 | 期望 |
|------|------|
| `GET /api/entan/v1/key-enterprises` | 200（非 404/502） |
| `GET /api/policy/v1/policy/indicators?kind=all` | 200 |
| `POST /api/innov/v1/industry/internal/run-chain-pipeline` | 200 或业务 code=1 可解释 |

---

## 3. DoD

- [ ] yaml 已 PR 合并 dev
- [ ] Nacos 与 yaml 一致（附 SQL/控制台截图）
- [ ] §2.4 冒烟通过
- [ ] handoff + 架构 D2 说明（demo ent/policy 直连 Python 为 demo 例外）

---

## 4. /goal 话术

```markdown
/goal api-agent
任务 ID：ALGO-GATEWAY-ROUTE-SYNC-L01
监管人：human:唐绍祖
仓库：demo-svc-platform（push origin/dev）
必读：ALGO-GATEWAY-ROUTE-SYNC-L01-派单包.md、ALGO-LIB-BID-COMPLIANCE-GAP-L01.md
目标：ent/policy/chain internal 网关路由 yaml+Nacos 可复现；完成冒烟。
DoD：见派单包 §3。
```
