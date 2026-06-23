# FE handoff · demo-ui-system-test 产业链分析 Demo

| 项 | 值 |
|---|---|
| 任务 | CHAIN-system-test-demo |
| 角色 | frontend-agent / coordinator |
| 仓库 | `demo-ui-system-test` |
| 分支 | `dev` |
| 日期 | 2026-06-23 |

## 范围与实现

仿照 **企业分析 Demo**（`/entan`）与 **政策分析 Demo**（`/policy`）范式，新增 **产业链分析 Demo**（`/chain`）：

| DoD | 状态 |
|---|---|
| 路由 `/chain` + 首页入口按钮 | ✅ |
| API 层 `src/api/chain/index.ts` | ✅ `/topic/v1/industry/**` + `/chain/internal/**` |
| 8 Tab 算法效果展示 | ✅ 基础指标 / 全景 / 周期 / 关键环节 / 瓶颈 / 区域 / 深圳 / 历程热点布局 |
| 灌数据 + 状态轮询 | ✅ 镜像 policy 交互 |
| AlgoHelp + D9 指标说明 | ✅ `chainHelp.ts` |
| `pnpm run build` | ✅ |

## 网关依赖（demo-svc-platform）

灌数据需网关路由 `gkx-chain-internal`：`/chain/internal/**` → `demo-platform-innov-py` `/internal/**`（已合入 `gkx-gateway-dev.yml`）。

## 架构合规

- ✅ 数据 API 走 Java 门面 `/topic/v1/industry/**`（前端不直连 Python 算法）
- ✅ 灌数据 internal 走 innov-py（与 policy/entan internal 范式一致）
- ✅ observability：request 拦截器 traceId 透传

## git

- 分支：`dev`
- 仓库：`demo-ui-system-test`

---

*handoff · CHAIN-system-test-demo*
