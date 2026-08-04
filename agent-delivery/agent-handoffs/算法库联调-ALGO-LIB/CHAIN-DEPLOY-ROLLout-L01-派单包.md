# 派单包：CHAIN-DEPLOY-ROLLout-L01 — 产业链 A2–A9 线上部署与冒烟

- **任务 ID**：CHAIN-DEPLOY-ROLLout-L01
- **派发角色**：coordinator-agent
- **承接角色**：devops-agent（主）+ api-agent（辅）
- **监管人**：human:唐绍祖
- **Epic**：算法库联调 · ALGO-LIB
- **effort / difficulty**：3 / M · est.tokens 120k
- **派发时间**：2026-08-04
- **阻塞**：ALGO-LIB 基础指标 §4.1.1 合规交付；用户现场 404

---

## 1. 背景

前端 ALGO-LIB-UI-NAV-L01 已对接 9 个产业链基础指标 API。代码仓 **已 push**：

| 仓 | 分支 | Commit | 内容 |
|----|------|--------|------|
| demo-algo-science | dev | `cb132a6` | Python `/v1/chain/enterprise-stats` … `sz-dist` |
| demo-svc-platform | dev | `21e67ec` | Java `ChainController` 透传 A2–A9 |
| demo-svc-platform | dev | （本地未 push）| `ChainController` 静态路由重排（建议同批部署） |

**线上** `http://111.198.38.90:50100` 实测：`market-stats` 可用，**A2–A9 及 investment-stats 返回 HTTP 404** → gkx-innov / innov-py 镜像未 rollout。

---

## 2. 范围（必做）

### 2.1 K8s dev rollout

1. 触发 **demo-algo-science** CI → 更新 `demo-platform-innov-py`（或等价 innov-py Deployment）至含 `cb132a6` 的镜像。
2. 触发 **demo-svc-platform** CI → 更新 **gkx-innov** 至含 `21e67ec`（+ 路由重排 commit）的镜像。
3. 确认 Pod 就绪、无 CrashLoop；Feign 目标 innov-py 服务名/Nacos 注册正常。

### 2.2 冒烟清单（登录态，与联调台一致）

Base：`/api/innov/v1/industry`（经 UI nginx → gateway）

| # | 端点 | 期望 |
|---|------|------|
| 1 | `GET /list` | 200, code=0 |
| 2 | `GET /market-stats?chainId=CH001` | 200 |
| 3 | `GET /enterprise-stats?chainId=CH001` | **200（非 404）** |
| 4 | `GET /institution-stats?chainId=CH001` | 200 |
| 5 | `GET /investment-stats?chainId=CH001` | 200 |
| 6 | `GET /global-dist?chainId=CH001` | 200 |
| 7 | `GET /national-dist?chainId=CH001` | 200 |
| 8 | `GET /news-stats?chainId=CH001` | 200 |
| 9 | `GET /sz-elements?chainId=CH001` | 200 |
| 10 | `GET /sz-dist?chainId=CH001` | 200 |

空数据允许 `{code:0,data:[]}`；**禁止 HTTP 404**。

### 2.3 灌数（若 ADS 空）

1. `POST /api/innov/v1/industry/internal/run-chain-pipeline`（timeout ≥20s）
2. `GET /api/innov/v1/industry/internal/status` → chain pipelines `done`
3. 重跑 §2.2，至少 A1/A2/A4 有非空序列

### 2.4 文档

- handoff 附：镜像 tag、rollout 时间、10 条 curl 结果、联调台 `#/chain/basic` 截图

---

## 3. 不在范围

- 技术链/产业服务新 API 开发
- lumen 正式仓 merge
- Q053 产业链编码决策（见客户决策清单）

---

## 4. DoD

- [ ] gkx-innov + innov-py dev 镜像 ≥ 上述 commit
- [ ] §2.2 十条冒烟全 200
- [ ] handoff：`agent-handoffs/算法库联调-ALGO-LIB/CHAIN-DEPLOY-ROLLout-L01.md`
- [ ] 架构自检：D2 调用链不变（Java 透传 Python）
- [ ] cost 四字段回填 registry

---

## 5. /goal 话术

```markdown
/goal devops-agent
身份：GKX K8s dev 环境运维；熟悉 demo-svc-platform / demo-algo-science CI 与 gkx-innov、innov-py Deployment。
任务 ID：CHAIN-DEPLOY-ROLLout-L01
监管人：human:唐绍祖
必读：
  - agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/CHAIN-DEPLOY-ROLLout-L01-派单包.md
  - agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-BID-COMPLIANCE-GAP-L01.md §GAP-D01/D02
  - demo-svc-platform/helm/gkx-platform/configs/gkx-gateway-dev.yml
目标：rollout gkx-innov(21e67ec+) + innov-py(cb132a6+)；完成派单包 §2.2 冒烟；必要时触发 chain pipeline。
DoD：见派单包 §4；status→integration→pending_test；附 curl + 截图。
不要问我，按派单包执行。
```
