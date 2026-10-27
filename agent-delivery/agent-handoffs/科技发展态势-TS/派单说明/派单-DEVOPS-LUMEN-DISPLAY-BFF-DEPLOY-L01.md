# 派单说明 · DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01

- **任务号**：`DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01`
- **名称**：展示聚合 BFF（`gkxlumen-display`）部署层四件套 + 首次部署上线（D15 唯一对外面）
- **监管**：`human:李伟`　**执行**：`agent:devops-agent`
- **仓**：`lumen-svc-platform`
- **状态**：`ready_to_sign`（待 `human:淮政玮` 签收 → `done`）
- **归属叶**：第 5 项 `WBS-05-12`（公共底座 · 部署上线）
- **派单日期**：2026-10-27

---

## 1. 派单目标

把展示聚合 BFF `gkxlumen-display` 从「仓里有代码」变成「dev 集群跑起来、网关可达、健康可查」，为 M1–M9 全部接口提供统一落点（D15 三层调用链）。

## 2. 交付范围（四件套）

| # | 件 | 内容 |
|---|---|---|
| 1 | 镜像构建 | `gkxlumen-display` Dockerfile + CI 构建 |
| 2 | Helm 编排 | chart / values，dev 环境参数 |
| 3 | 网关路由 | `gkxlumen-gateway` 增加 `/display/**` → `gkxlumen-display`（StripPrefix 后服务内 `/v1/situation/**`） |
| 4 | 首次部署 | dev 集群发布 + 健康验证 |

## 3. 交付证据（已达成）

| 项 | 证据 |
|---|---|
| CI 构建 | pipeline **#2760**，commit sha `2bc11e8` |
| Helm 发布 | helm job **#15022** success |
| 发布对象 | release `gkxlumen-platform` **deployed** |
| 运行态 | `gkxlumen-display` Pod **1/1 Running** |
| 网关 | 路由 **24 → 25 条**（新增 `/display/**`） |
| 健康 | `/display/actuator/health` **UP** |
| 提交 | 2026-10-22 五条提交全推 `origin/dev` |

## 4. 技术约束

- **调用链铁律（D15）**：前端 → 网关 `/display/**` → `gkxlumen-display` → Feign 调用域服务（`gkxlumen-element` :7082 / `gkxlumen-graph` :7083 / `gkxlumen-datacatalog` :7084，**均 `@Inner` 不对外**）。
- **禁止 helm 回落 demo**；K8s 服务名以 helm 为准。
- `gkxlumen-metrics` 是指标唯一真源（D9，共享）；`gkxlumen-innov` 为 M1 过渡复用。
- lumen 环境**无 demo 依赖**（含 `VITE_*`）；后端数据源暂读 `demo_gkxlumenx_ads` 属 A5 已知豁免（见技术方案 §3.1），不是本单范围。

## 5. 上下游

| 方向 | 任务 |
|---|---|
| 上游 | `SYSINT-SCHEME-05-L01`（第 5 项技术方案，仍处理中） |
| 下游 | `BE-TS-IMPL-01`（接口落本服务）· `WBS-05-01a/b`～`05-08`（各菜单页）· `WBS-05-09`（菜单与权限） |

## 6. DoD（可验收）

1. `gkxlumen-display` 镜像可重复构建，CI pipeline 绿 ✅
2. Helm 发布成功，Pod 1/1 Running ✅
3. 网关 `/display/**` 路由生效（24 → 25 条） ✅
4. `/display/actuator/health` 返回 UP ✅
5. 五条提交 push `origin/dev`，registry evidence 回填 ✅
6. **签收**：`ready_to_sign` → `human:淮政玮` 签收 → `done` ⏳

## 7. 边界（不写成已上线）

- 本单只证明 **BFF 在 dev 集群跑起来、网关可达、健康可查**。
- 业务端点返回 **401** 属平台统一安全基线（需鉴权），**不是故障**。
- **不能据此写成「展示系统页面已上线」**；页面可用与否由各菜单叶（`WBS-05-01`～`05-08`）各自验收。

## 8. 未决与阻塞

无阻塞项。唯一悬置：`human:淮政玮` 签收（签收后转 `done`）。

## 9. 会签

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 执行 | `agent:devops-agent` | 已交付 | 2026-10-22 |
| 监管 | `human:李伟` | 已核 | 2026-10-22 |
| 签收 | `human:淮政玮` | **待签收** | — |
