# DECIDE-D12-LUMEN-CALLCHAIN · D12 demo 原型 / lumen 正式隔离

> Task ID：`DECIDE-D12-LUMEN-CALLCHAIN`  
> 决策来源：项目负责人 2026-08-14 确认（会话指令：demo 开头仅原型；lumen 开头才是正式开发；lumen 前端调用链禁止调用 demo 项目服务）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 名词与流程见 [`task-claiming-guide.md`](../task-claiming-guide.md) |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |
| 说明 | architect 不以缩代码为目标；本任务只落盘决策，不改 Helm/Java 运行时。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未把本任务挂到 Headroom 压缩流。 |

## 问题清单

- 如何把「demo 只是原型、lumen 才是正式开发、lumen 前端调用链禁止打 demo 服务」写成可执行铁律，并同步公约 / 仓登记 / 角色 mdc。
- 现网 innov-py / entan-py 仍是 demo 仓制品：本任务只登记整改债，不改运行时。

## 修改内容

登记 **D12**（`architecture-baseline.md` v2.2）：

1. `demo-*` 仓只做原型；正式开发与交付只在 `lumen-*`。
2. lumen 前端调用链（`lumen-ui-*` → `gkxlumen-platform-gateway` → `gkxlumen-*` → lumen Python `/internal/*`）禁止直连或回落到任何 `demo-*` 服务。
3. 对照 demo 允许读代码后重写；禁止 git merge demo→lumen（延续原铁律 6）。

同步：公约铁律 12、`repo-registry.yaml`、`paths.yaml`（补 `lumen-algo-py`）、`项目工程化交付模式.md`、`产品实现规程.md` I2-01、`frontend.mdc` / `api.mdc` / `algorithm.mdc` / `architect.mdc`。

## D12 整改债（本任务不改代码）

| ID | 缺口 | 现状 | 目标 |
|----|------|------|------|
| **D12-DEBT-TOPIC-PY** | 企业检索/AI 仍打 demo | `python-base-url=http://demo-platform-search-py:8080` | 新建 `lumen-topic-py`（禁止 `lumen-svc-topic-py` / 只改名 / 并进 lumen-algo-py）。三叶：DEVOPS → PY-PORT → API-CUTOVER |
| D12-DEBT-INNOV-PY | 创新监测算法仍是 demo 制品 | helm `innovPy`=`gkx-innov-py`（`demo-algo-science` CI） | 迁入 `lumen-algo-py`（或独立 `lumen-innov-py`）；待拆 |
| D12-DEBT-ENTAN-PY | 企业图谱 worker 仍是 demo 制品 | helm `entanPy` 由 `demo-algo-ent-analysis` CI 热更新 | 迁入 `lumen-algo-py`；待拆 |
| D12-DEBT-REGISTRY | 登记表 | `lumen-algo-py` 已登记；`lumen-topic-py` 待建 | 随 TOPIC-PY 三叶闭合 |

派单条：`agent-handoffs/平台基建-PLATFORM/D12-LUMEN-TOPIC-PY-派单条.md`

产业链 `gkxlumen-topic-chain` 已钉 `lumen-algo-py`，可作为迁出样板。后续需 coordinator 拆 DEVOPS/API/ALG 实现任务（不在本决策范围内）。

## 测试结果

- 文档对照：D12 出现在 baseline §2 / §3.1 / §4 / §5.3 / §8。
- 现状扫描（本决策前，未改运行时）：lumen-ui-science-pc / topic / admin 的 nginx `/api` 已指向 `gkxlumen-platform-gateway`（前端 HTTP 合规）；innov-py / entan-py 仍为 D12 债。
- 无 K8s / CI 变更（`cicd: skip`，定义任务）。

## 遗留风险

- 在 D12-DEBT-INNOV-PY / ENTAN-PY 关闭前，lumen 创新监测 / 企业图谱页面仍会**间接**吃到 demo 算法制品。新 PR 不得再扩大该回落。
- `repo-registry.yaml` `innov_py.lumen.name` 暂仍写 `demo-algo-science` + `interim: true`，避免 agent 误以为 innov 已迁完。

## CI/CD（必填）

- 分支：`gkx-orchestration` 当前工作区（文档-only，未要求本会话 push）
- commit：待监管人确认后提交
- pipeline URL / ID：N/A（编排仓文档，无业务 CI）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A（决策落盘）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- Tempo / Loki：无（未改运行时）

## 涉及文件

- `agent-delivery/architecture-baseline.md`
- `agent-delivery/repo-registry.yaml`
- `agent-delivery/paths.yaml`
- `agent-delivery/项目工程化交付模式.md`
- `agent-delivery/产品实现规程.md`
- `.cursor/rules/00-team-constitution.mdc`
- `.cursor/rules/frontend.mdc`
- `.cursor/rules/api.mdc`
- `.cursor/rules/algorithm.mdc`
- `.cursor/rules/architect.mdc`
- `agent-delivery/agent-handoffs/DECIDE-D12-LUMEN-CALLCHAIN.md`

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 算法只在 Python | ✅ 未改 Java 算法边界 |
| 2 调用链不越层 | ✅ D12 强化 lumen 链只走 lumen 网关 |
| 3 NebulaGraph | ✅ 未改图谱引擎 |
| 4 可观测 | N/A 文档 |
| 5 CI/CD | N/A 定义任务 |
| 6 demo 不 merge lumen | ✅ 重申；并补运行时隔离 |
| 7 方案 A | ✅ 拓扑仍为共享聚合核心 |
| 8 ADS | ✅ 未改数据契约 |
| 9 D8 | N/A |
| 10 D9 | N/A |
| 11 D10 | N/A |
| 12 D12 | ✅ 本任务产物 |

## 范围与偏离

- 范围：架构决策落盘 + 整改债清单。
- 偏离：未改 `lumen-svc-platform` helm（按 DoD「不在本任务改 helm 代码」）。
- bid-reference：无功能点增减（±10% 不适用）。
