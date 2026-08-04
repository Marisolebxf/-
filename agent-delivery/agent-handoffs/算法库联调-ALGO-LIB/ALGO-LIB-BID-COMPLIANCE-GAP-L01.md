# 算法库联调 · bid-reference 合规差距总表

- **文档 ID**：ALGO-LIB-BID-COMPLIANCE-GAP-L01
- **角色**：coordinator-agent（调度者）
- **真源**：`agent-delivery/bid-reference/科技专题服务算法库.md` + `scope-baseline.yaml#algo-*`
- **关联 UI 镜像**：`demo-ui-system-test/src/views/shared/bidBasicIndicators.ts`
- **审计时间**：2026-08-04
- **监管人**：human:唐绍祖（算法 · bid-reference 合规收口）

---

## 1. 结论摘要

| 层级 | 状态 | 说明 |
|------|------|------|
| **联调台 UI（导航 + 基础指标展示）** | 🟡 部分合规 | ALGO-LIB-UI-NAV-L01 已交付；七类基础指标中 4 类有菜单、3 类 `planned` |
| **产业链 REST（代码仓）** | 🟢 代码齐 | A1–A9 + M1–M13 Python/Java 均已 commit |
| **产业链 REST（线上 dev）** | 🔴 **未对齐** | `111.198.38.90:50100` 仅 `market-stats` 200，A2–A9 **404** → **部署漂移** |
| **企业/政策 REST** | 🟡 demo 直连 Python | 基础 + 大部分深度有 API；招标 3 子页无 REST（历程/招引/培育） |
| **产业服务/产业综合/技术链/人才/科研机构** | 🔴 全缺 | 招标叶子未实现，联调台为占位 |
| **网关路由** | 🟡 部分在 DB | `/entan/**`、`/policy/**` 未写入 `gkx-gateway-dev.yml`，依赖一次性脚本 |
| **数据灌数** | 🟡 | chain pipeline 有；Q053 产业链编码 🔴 阻塞 ODS→DWD |

**合规交付路径**：先 **P0 部署 + 网关 + 灌数闭环**（已 commit 能力上线），再 **P1 补 ent 深度缺口 + 产业服务/综合设计**，最后 **P2 技术链/人才/科研机构新库**（scope ±10% 内须 PM 确认排期）。

---

## 2. 七类基础指标（§4.1）对齐矩阵

| # | 招标维度 | MD 章节 | 联调台菜单 | UI 清单 | 后端 REST | 线上可用 | 差距类型 |
|---|----------|---------|------------|---------|-----------|----------|----------|
| 1 | 产业链 | §4.1.1 | ✅ `/chain/basic` | A1–A9 折叠 | ✅ 9 端点 | 🔴 A2–A9 404 | **DEPLOY** |
| 2 | 技术链 | §4.1.2 | ❌ 无一级库 | T1–T11 planned | ❌ 无 `/v1/tech/**` | ❌ | **SCOPE_NEW** |
| 3 | 企业 | §4.1.3 | ✅ `/entan/basic` | A1–A5 | ✅ entan-py | 🟡 依赖网关 | **GATEWAY** |
| 4 | 人才 | §4.1.4 | ❌ 无一级库 | A1–A4 planned | ❌ 无 REST 库 | ❌ | **SCOPE_NEW** |
| 5 | 科研机构 | §4.1.5 | ❌ 无一级库 | A1–A4 planned | ❌ | ❌ | **SCOPE_NEW** |
| 6 | 政策 | §4.1.6 | ✅ `/policy/basic` | A1–A5 | ✅ policy_routes | 🟡 依赖网关 | **GATEWAY** |
| 7 | 服务机构 | §4.1.7 | ✅ `/industry-service/basic` | A1–A6 占位 | ❌ | ❌ | **ALGO+API** |

**产业综合分析**（§1.1.1.1.10）：无独立基础指标子模型；联调台 `/industry-comp/basic` 展示七维上游依赖表 ✅（符合 as-built 说明）。

---

## 3. 深度分析模型（§4.3 七要素）对齐矩阵

### 3.1 产业链深度 M1–M13（§1.1.1.1.3）

| 招标模型 | UI 子页 | Python | Java 门面 | 线上 |
|----------|---------|--------|-----------|------|
| M1 全景 | `/chain/panorama` | ✅ | ✅ | 🟡 同 deploy |
| M2/M5/M11/M12 深圳 | `/chain/shenzhen` | ✅ | ✅ | 🟡 |
| M3 历程 + M4 热点 + M13 布局 | `/chain/hotspot` | ✅ | ✅ | 🟡 |
| M6/M7 周期 | `/chain/cycle` | ✅ | ✅ | 🟡 |
| M8 关键环节 | `/chain/keynodes` | ✅ | ✅ | 🟡 |
| M9 瓶颈 | `/chain/bottleneck` | ✅ | ✅ | 🟡 |
| M10 区域指数 | `/chain/region` | ✅ | ✅ | 🟡 |
| 竞争力（工程扩展） | 合并在深圳/区域 | ✅ competitiveness | ✅ | 🟡 |

**UI 缺口**：8 子页合并展示 13 模型（acceptable demo 弹性）；无单独「问题识别/机遇分析」页（M11/M12 部分在 shenzhen）。

### 3.2 企业深度（§1.1.1.1.5 等）

| 招标子能力 | UI | REST | 差距 |
|------------|-----|------|------|
| 竞争力 | `/entan/competitiveness` | score/ranking | ✅ |
| 发展历程 | `/entan/history` | ❌ | **ALGO** |
| 痛难点 | `/entan/pain-points` | diagnosis | ✅ |
| 供应链 | `/entan/supply-chain` | centrality/graph | ✅ |
| 技术力/商业力 | `/entan/tech` `/entan/biz` | tech-power/biz-power | ✅ |
| 招引推荐 | `/entan/attract` | ❌（能力在 innov async） | **ALGO+路由** |
| 培育推荐 | `/entan/cultivate` | ❌ | **ALGO+路由** |

### 3.3 政策深度

| 能力 | UI | REST | 差距 |
|------|-----|------|------|
| 焦点/力度/效果/短板/机遇/布局 | 6 子页 | `/v1/policy/analysis/{modelId}` | ✅ ADS 预计算 |
| 实时推理 | — | `/internal/analysis/policy/*` 未暴露 REST | 🟡 设计决策 |

### 3.4 未挂载算法库（招标 scope 内）

| 模块 | 招标 | 联调台 | 后端 |
|------|------|--------|------|
| 技术链深度 M1–M11 | §1.1.1.1.4 | ❌ | ❌ |
| 人才深度 | §1.1.1.1.6 | ❌ | ❌ |
| 科研机构深度 | §1.1.1.1.7 | ❌ | ❌ |
| 产业服务深度 | §1.1.1.1.9 | 占位 9 页 | ❌ |
| 产业综合深度 | §1.1.1.1.10 | 占位 4 页 | ❌ |

---

## 4. 部署 / 网关 / 数据（横切）

| ID | 问题 | 影响 | 责任 | 派单 |
|----|------|------|------|------|
| GAP-D01 | gkx-innov 未 rollout `21e67ec` | chain A2–A9 HTTP 404 | DevOps + api | **CHAIN-DEPLOY-ROLLOUT-L01** |
| GAP-D02 | innov-py 未 rollout `cb132a6` | Java 透传后 Python 404/502 | DevOps + algorithm | 同上 |
| GAP-D03 | `/entan/**` `/policy/**` 网关 yaml 缺失 | 新环境 ent/policy 全挂 | api-agent | **ALGO-GATEWAY-ROUTE-SYNC-L01** |
| GAP-D04 | chain internal 双轨（Java vs `/chain/internal` 直连） | 运维混淆、灌数路径不一致 | api-agent | 同上 §3 |
| GAP-D05 | Q053 产业链编码 INB vs 国标 | ODS→DWD 灌数 🔴 阻塞 | data + PM | 客户决策清单 Q053 |
| GAP-D06 | ent/policy demo 跳过 Java（D2 偏离） | 正式 lumen 需 Java 门面 | architect | 正式轨 backlog |

---

## 5. 派单队列（建议 registry 条目）

| 优先级 | 任务 ID | 角色 | effort | 说明 |
|--------|---------|------|--------|------|
| **P0** | CHAIN-DEPLOY-ROLLOUT-L01 | devops-agent + api-agent | 3 / M | K8s rollout + 冒烟 A1–A9 |
| **P0** | ALGO-GATEWAY-ROUTE-SYNC-L01 | api-agent | 3 / M | yaml + Nacos 同步 ent/policy/chain internal |
| **P0** | CHAIN-PIPELINE-SMOKE-L01 | algorithm-agent | 5 / M | 灌数 + ADS 表验证 + 联调台 A1–A9 截图 |
| **P1** | ENT-DEEP-GAP-L01 | algorithm-agent | 8 / L | 历程 + 招引/培育 REST（或迁 innov async） |
| **P1** | SVC-ALGO-DESIGN-L01 | algorithm-agent + ux | 5 / M | 已有派单包 · 产业服务 |
| **P1** | COMP-ALGO-DESIGN-L01 | algorithm-agent + ux | 5 / M | 已有派单包 · 产业综合 |
| **P2** | TECH-ALGO-LIB-SPIKE-L01 | algorithm-agent | 8 / L | 技术链基础+深度 spike |
| **P2** | TALENT-RES-ALGO-SPIKE-L01 | algorithm-agent | 8 / L | 人才+科研机构 spike |
| **P1** | ALGO-LIB-UI-NAV-L01 | frontend | — | **待签收** + 404 容错 patch 待 push |

---

## 6. 验收口径（合规交付 DoD 共用）

1. **部署一致**：dev 外网 `50100` / 内网 `30889` 上，chain A1–A9 全部 **HTTP 200 + `{code:0}`**（或空数据 `{code:0,data:[]}`，禁止 404）。
2. **灌数闭环**：`POST /innov/v1/industry/internal/run-chain-pipeline` 成功；`GET .../internal/status` pipelines 含 chain 且 `done`。
3. **UI 不伪绿**：`bidBasicIndicators.ts` 中 `status:'live'` 项须与线上一致；未部署前改为 `planned` 或 UI 显式降级横幅（已做 partial）。
4. **网关可复现**：`gkx-gateway-dev.yml` 与 Nacos `sys_route_conf` 一致；新集群 `kubectl apply` 即可用 ent/policy/chain。
5. **handoff**：每任务含 scope_ref（MD 章节）、架构自检、冒烟 URL、traceId 截图。

---

## 7. 范围守门说明

- 本表 **不新增 scope-baseline 叶子**；`SCOPE_NEW` 三项（技术链/人才/科研机构一级库）已在招标 MD 内，属 **baseline 未交付**，需 PM 排期而非 silent skip。
- 联调台 `planned` 占位 **符合** `implementation_flexibility`（禁止整页 404；当前为 Empty/占位 ✅）。
- 产业服务/综合从「灰显」改为可展开占位（ALGO-LIB-UI-NAV-L01）**不增加叶子计数**，深度实现仍待 SVC/COMP 设计任务。

---

**维护**：coordinator 在 CHAIN-DEPLOY 完成后更新 §2「线上可用」列；MCP task-registry 恢复后批量 `task-create` §5 条目。
