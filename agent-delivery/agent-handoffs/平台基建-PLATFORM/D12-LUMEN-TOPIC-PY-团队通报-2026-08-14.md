# 【团队通报】D12 已落地：企业检索/AI 切到 `lumen-topic-py`

> **已被晚间总通报替代**（2026-08-14 晚）：登记债已全部闭合，请转发  
> [`D12-LUMEN-ISOLATION-团队通报-2026-08-14.md`](./D12-LUMEN-ISOLATION-团队通报-2026-08-14.md)。  
> 下文 §6「innov / entan 仍开」、§8 飞书短讯里的 QA 领取句 **作废**。本文只保留检索/AI 切仓细节。

> **发给**：全体开发 / DevOps / QA / 架构（人类同事）  
> **日期**：2026-08-14  
> **监管人**：淮政玮  
> **一句话**：正式环境的企业检索和专题 AI，已经从 demo Python 切到独立新仓 **`lumen-topic-py`**。请不要再改、再连 `demo-platform-search-py`。

---

## 0. 请大家先记住这 4 条

1. **`demo-*` 只做原型**；正式开发只在 **`lumen-*`**。这是架构铁律 **D12**。
2. **正式仓名是 `lumen-topic-py`**。禁止叫 `lumen-svc-topic-py`（`svc` 是 Java 层）。禁止只改 GitLab 项目名冒充切流。禁止把 topic-py 并进 `lumen-algo-py`。
3. **`demo-svc-topic-py` 保留**，继续服务 demo 前端。两边独立镜像、独立 K8s Service，互不覆盖。
4. lumen 前端调用链必须是：  
   `lumen-ui-*` → `gkxlumen-platform-gateway` → `gkxlumen-*` Java → **`lumen-topic-py` / `lumen-algo-py` / `lumen-etl-es-py`** 的 `/internal/*`。  
   **禁止** nginx / `VITE_*` 直连，以及 Java Feign、helm **回落**到任何 `demo-*` 服务。

---

## 1. 今天做完了什么

闭合整改债 **D12-DEBT-TOPIC-PY**：原先 `gkxlumen-topic-enterprise` 直连 demo 的 `http://demo-platform-search-py:8080`，async 还靠 Nacos 名 `gkx-ai-service` 找到 demo AI。现网已切到 lumen 自己的 Python 门面。

| 步骤 | 任务 | 仓 | 结果 |
|------|------|----|------|
| 1 建仓隔离 | `DEVOPS-LUMEN-TOPIC-PY-L01` | `lumen-topic-py` | **done** |
| 2 对照迁代码 | `PY-LUMEN-TOPIC-PY-PORT-L01` | `lumen-topic-py` | **pending_test**（等 QA） |
| 3 Java 切流 | `API-LUMEN-TOPIC-PY-CUTOVER-L01` | `lumen-svc-platform` | **pending_test**（等 QA） |

看板签收可以积压；**运行时已经切完**。

---

## 2. 现网对照（请收藏）

### 2.1 调用链（合法）

```
lumen-ui-topic / lumen-ui-*
    → gkxlumen-platform-gateway   （NodePort 30899）
        → gkxlumen-topic-enterprise     （检索门面）
        → gkxlumen-topic-async-service  （分析编排）
            → lumen-topic-py /internal/*
            → lumen-algo-py  /internal/*   （算法厨房，未改）
```

### 2.2 新旧 URL

| 用途 | 旧（禁止再写进 lumen） | 新（正式） |
|------|------------------------|------------|
| 企业检索 Python | `http://demo-platform-search-py:8080` | `http://gkxlumen-platform-search-py:8080` |
| 专题 AI Python | Nacos `gkx-ai-service` 或 demo AI | `http://gkxlumen-platform-ai-py:8081` |
| Java 回调 | （已是 lumen async） | `http://gkxlumen-platform-topic-async-service:7094` |
| 算法厨房 | `http://lumen-platform-algo-py:8000` | 不变 |

Helm / 环境变量：

- `GKXLUMEN_TOPIC_ENTERPRISE_PYTHON_BASE_URL=http://gkxlumen-platform-search-py:8080`
- `GKXLUMEN_TOPIC_ASYNC_PYTHON_AI_BASE_URL=http://gkxlumen-platform-ai-py:8081`

### 2.3 K8s / 镜像（与 demo 隔离）

| 项 | lumen（新） | demo（保留，勿覆盖） |
|----|-------------|----------------------|
| 检索 Deployment/Service | `gkxlumen-platform-search-py` ClusterIP `:8080` | `demo-platform-search-py` NodePort **30805** |
| AI Deployment/Service | `gkxlumen-platform-ai-py` ClusterIP `:8081` | `demo-platform-ai-py` NodePort **30807** |
| Worker | `gkxlumen-platform-ai-worker` | `demo-platform-worker-py` |
| Harbor 镜像 | `gkxlumen-search-service` / `gkxlumen-ai-service` / `gkxlumen-ai-worker` | `gkx-search-service` / `gkx-ai-service` / `gkx-ai-worker` |
| OTel collector | `gkxlumen-platform-otel-collector:4318` | `demo-platform-otel-collector` |
| OTEL_SERVICE_NAME | `gkxlumen-search-service` 等 | `gkx-search-service` 等 |

lumen 侧 **没有** 再开 30805/30807，避免和 demo 抢 NodePort。集群内用 Service DNS。

### 2.4 Git

| 仓 | 地址 | 分支 | 本次 commit |
|----|------|------|-------------|
| 新 Python 仓 | https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py | `dev` | `5d20411` |
| Java 平台 | https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform | `dev` | `1ceb8e3` |
| 编排/基线 | https://gitlab.htmisoft.net/gkx-lumen/gkx-orchestration | `dev` | `02966f4` |
| 原型 Python | https://gitlab.htmisoft.net/gkx-lumen/demo-svc-topic-py | 未改 | — |

本地路径：`${GKX_ROOT}/repos/lumen-topic-py`（需 `git pull`）。

---

## 3. 怎么验证（2 分钟）

金路径（已实测，2026-08-14）：

```http
POST http://192.168.88.50:30899/enterprise/topic/v1/search/meta/filters
Content-Type: application/json

{}
```

期望：**HTTP 200**，body `code=0`，带 `listing_statuses` / `operating_statuses` 等字典。

CI：

- Python：[pipeline 5026](https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5026) 全绿（smoke + 三镜像 + 三 deploy）
- Java：[pipeline 5027](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5027)  
  `helm:deploy` [#21542](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21542)、`deploy:topic-enterprise` [#21544](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21544)、`deploy:topic-async-service` [#21545](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21545) **success**

---

## 4. 分角色：你需要做什么 / 不要做什么

### 前端（`lumen-ui-topic` / `lumen-ui-*`）

- **继续只打网关** `gkxlumen-platform-gateway`（30899）。不要加 `VITE_*` 直连 Python，不要打 30805。
- 企业检索、画像、分析任务走现有 `/enterprise/**`、`/topicAsync/**` 即可，契约路径未改。
- 对照 demo 页面可以读 `demo-ui-topic` 代码，**禁止 git merge demo → lumen**。

### Java（`lumen-svc-platform`）

- 新代码禁止再写 `demo-platform-search-py` / `demo-platform-ai-py` / Nacos `gkx-ai-service`。
- 检索直连：`http://gkxlumen-platform-search-py:8080`  
  AI 直连：`http://gkxlumen-platform-ai-py:8081`（不要靠空 URL 走服务发现）。
- HTTP 契约仍是 `/internal/gkx-search/**`、`/internal/gkx-ai/**`（包名仍 `gkx_*`，K8s 名已换成 `gkxlumen-*`）。
- 若本地/Nacos 被人手改过 DataId，以 git 为准：  
  `helm/gkxlumen-platform/configs/gkxlumen-topic-enterprise-biz-dev.yml`  
  `helm/gkxlumen-platform/configs/gkxlumen-topic-async-service-biz-dev.yml`  
  Pod env 也可压过旧 Nacos。

### Python / 算法

- **专题检索/AI 门面**：只在 **`lumen-topic-py`** 改。  
- **算法厨房**：仍只在 **`lumen-algo-py`**。topic-py 调厨房 `http://lumen-platform-algo-py:8000`。  
- **demo-svc-topic-py**：只修 demo 原型；改它不会进 lumen 流量。  
- 禁止 `git merge` demo → lumen；对照复制后改名已经做过一次，后续按 lumen 仓迭代。
- 本仓 CI 默认 **deploy 是 manual**；镜像名必须是 `gkxlumen-*`，不要推 `gkx-search-service` 以免覆盖 demo。

### DevOps

- 新仓 GitLab 项目 id **275**，默认分支 **`dev`**。组级变量 `HARBOR_*` / `KUBECONFIG_B64` 已能跑通本次 pipeline。
- 热更新：在 `lumen-topic-py` 的 pipeline 上手动点 `deploy:search-py` / `deploy:ai-py` / `deploy:ai-worker`。
- 不要把 lumen 的 search-py 配回 demo helm。

### QA

- 两叶停在 **`pending_test`**：`PY-LUMEN-TOPIC-PY-PORT-L01`、`API-LUMEN-TOPIC-PY-CUTOVER-L01`。  
- 闸门：`pending_test → testing` 需要 **qa-agent 认领** 或监管人 **黄敬洲**。  
- 建议回归：企业检索（上节 filters）、联想/复合检索一条、分析任务创建一条（打 AI）。  
- 失败请开缺陷包，不要直接改业务仓。

---

## 5. 刻意没做 / 请勿误判

| 项 | 说明 |
|----|------|
| 未改 `demo-svc-topic-py` | demo 前端 30805/30807 应仍可用 |
| 未切 DWD 库 | bootstrap 仍读 `demo_gkxlumenx_dwd`（切服务 ≠ 切库） |
| 未并进 `lumen-algo-py` | 产业链算法仓保持厨房职责 |
| 未关另外两笔 D12 债 | 见下一节 |
| 本地 pytest 有 1 条旧失败 | `test_query_tree_dsl.py::test_meta_query_tree_schema_matches_field_strategy`（`name_en` extra），对照源 demo 即有，CI smoke 不含该用例 |

---

## 6. 还没闭合的 D12 债（不要以为「全部隔离完了」）

| 债 | 现状 | 和本次关系 |
|----|------|------------|
| **D12-DEBT-TOPIC-PY** | **已闭合** | 本次三叶 |
| **D12-DEBT-REGISTRY** | **已闭合** | `lumen-topic-py` 已登记 |
| **D12-DEBT-INNOV-PY** | 仍开 | 创新监测 `gkx-innov-py` 仍由 `demo-algo-science` CI 热更新 |
| **D12-DEBT-ENTAN-PY** | 仍开 | 企业图谱 worker 仍由 `demo-algo-ent-analysis` CI 热更新 |

产业链 Java 已钉 `lumen-algo-py`，迁 innov / entan 时按那个样板，不要再回落 `demo-platform-*`。

---

## 7. 文档入口（需要细节时再点）

| 文档 | 路径 |
|------|------|
| 本通报 | `agent-delivery/agent-handoffs/平台基建-PLATFORM/D12-LUMEN-TOPIC-PY-团队通报-2026-08-14.md` |
| 架构铁律 D12 | `agent-delivery/architecture-baseline.md` §2 D12、§3.1 |
| 决策记录 | `agent-delivery/agent-handoffs/DECIDE-D12-LUMEN-CALLCHAIN.md` |
| 长任务总控 | `agent-delivery/agent-handoffs/平台基建-PLATFORM/D12-LUMEN-TOPIC-PY-长任务总控.md` |
| 建仓 handoff | `…/DEVOPS-LUMEN-TOPIC-PY-L01.md` |
| 迁代码 handoff | `…/PY-LUMEN-TOPIC-PY-PORT-L01.md` |
| 切流 handoff | `…/API-LUMEN-TOPIC-PY-CUTOVER-L01.md` |
| 新仓部署说明 | `${GKX_ROOT}/repos/lumen-topic-py/docs/DEPLOY-K8S.md` |

---

## 8. 飞书可直接粘贴的短讯

```
【D12 切流完成 2026-08-14】
企业检索/AI 已从 demo-platform-search-py 切到新仓 lumen-topic-py。
检索：http://gkxlumen-platform-search-py:8080
AI：http://gkxlumen-platform-ai-py:8081
验证：POST http://192.168.88.50:30899/enterprise/topic/v1/search/meta/filters → 200
请 lumen 侧不要再写 demo-platform-* / gkx-ai-service。
demo-svc-topic-py 保留给 demo 前端。
仓名禁止 lumen-svc-topic-py；禁止 merge demo→lumen。
QA：PY-PORT / CUTOVER 停在 pending_test，请黄敬洲领取。
innov-py / entan-py 两笔 D12 债仍开，与本次无关。
详情：orchestration 仓 agent-handoffs/平台基建-PLATFORM/D12-LUMEN-TOPIC-PY-团队通报-2026-08-14.md
```
