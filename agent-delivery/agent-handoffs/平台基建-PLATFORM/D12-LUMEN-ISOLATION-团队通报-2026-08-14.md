# 【团队通报】D12 闭合：demo 与 lumen 运行时已拆开

> **发给**：全体开发 / DevOps / QA / 架构（人类同事）  
> **日期**：2026-08-14（晚）  
> **监管人**：淮政玮  
> **一句话**：登记过的 **D12 整改债已全部闭合**。正式流量只走 `lumen-*` / `gkxlumen-*`；`demo-*` 只服务原型。上午那份「检索切流」通报里「innov / entan 仍开」**作废**。

上午专题：[D12-LUMEN-TOPIC-PY-团队通报-2026-08-14.md](./D12-LUMEN-TOPIC-PY-团队通报-2026-08-14.md)（只讲检索/AI 切仓；§6 已过时）。

---

## 0. 请大家先记住这 5 条

1. **`demo-*` 只做原型**；正式开发只在 **`lumen-*`**。这是架构铁律 **D12**。
2. lumen 调用链必须是：  
   `lumen-ui-*` → `gkxlumen-platform-gateway`（30899）→ `gkxlumen-*` Java → **`lumen-topic-py` / `lumen-algo-py` / `lumen-etl-es-py`** 的 `/internal/*`。
3. **禁止** nginx / `VITE_*` 直连 Python，禁止 Java Feign、helm **回落**到任何 `demo-*` 服务。
4. 对照 demo **可以读代码后重写**；**禁止 `git merge` demo → lumen**。仓名禁止 `lumen-svc-topic-py`（`svc` 是 Java 层）。
5. **切服务 ≠ 共用库**：lumen 读写 `gkxlumenx_*`；demo 读写 `demo_gkxlumenx_*`。不要再让 demo Java/Python 扫正式 ADS。

---

## 1. 今天闭合了哪些债

基线真源：`architecture-baseline.md` §3.1（v2.2.3–v2.2.9）。

| 债 | 原来怎样 | 现在怎样 |
|----|----------|----------|
| **D12-DEBT-TOPIC-PY** | 企业检索/AI 打 `demo-platform-search-py` | 独立仓 **`lumen-topic-py`**；`gkxlumen-platform-search-py:8080` / `ai-py:8081` |
| **D12-DEBT-INNOV-PY** | 创新监测镜像由 `demo-algo-science` CI 热更新 lumen | 代码在 `lumen-algo-py` `vendor/innov-py`；镜像 **`gkxlumen-innov-py`**；demo CI 只更新 `demo-platform` |
| **D12-DEBT-ENTAN-PY** | 企业图谱由 `demo-algo-ent-analysis` CI 热更新 lumen | `vendor/entan-py`；镜像 **`gkxlumen-entan-py-api` / `gkxlumen-entan-py-worker`** |
| **D12-DEBT-ETL-ES-PY** | 正式 DWD→ES 挂在 `demo-platform-etl-es-py`（30806） | 正式 **`gkxlumen-platform-etl-es-py`** ClusterIP；demo 副本已卸 |
| **D12-DEBT-REGISTRY** | 登记表落后 | `lumen-algo-py` + `lumen-etl-es-py` + `lumen-topic-py` 已登记 |
| 数据面 | demo Java 能扫到正式 `gkxlumenx_ads` | demo `gkx-innov` DataPlane 改写到 `demo_*`；lumen innov SQL 落正式 2B 名 |
| 对外 /v1 | lumen Python 可能被直打 | lumen helm `INNOV_EXPOSE_PUBLIC_API=0` / `ENTAN_EXPOSE_PUBLIC_API=0`，只留 `/healthz` `/internal/*` |

demo 仓 **全部保留**（`demo-svc-topic-py` / `demo-algo-science` / `demo-algo-ent-analysis` / `demo-svc-platform`），只服务原型。

---

## 2. 现网对照（请收藏）

### 2.1 合法调用链

```
lumen-ui-*
    → gkxlumen-platform-gateway     NodePort 30899
        → gkxlumen-* Java
            → lumen-topic-py     /internal/gkx-search/**  /internal/gkx-ai/**
            → lumen-algo-py      /internal/*     （厨房 + vendor/innov-py + vendor/entan-py）
            → lumen-etl-es-py    in-cluster      （DWD→ES，无前端入口）
```

demo 前端继续打 **demo 网关 / `demo-platform-*`**，与上面这条链并存、互不覆盖。

### 2.2 Python 下游（lumen 只准写右边）

| 用途 | 禁止再写进 lumen | 正式（现网） |
|------|------------------|--------------|
| 企业检索 | `http://demo-platform-search-py:8080` | `http://gkxlumen-platform-search-py:8080` |
| 专题 AI | Nacos `gkx-ai-service` / demo AI | `http://gkxlumen-platform-ai-py:8081` |
| 创新监测 Python | `gkx-innov-py` / `demo-platform-innov-py` | `http://gkxlumen-platform-innov-py:8000`（科技新闻仍打这里；**换的是制品**） |
| 产业链厨房 | innov-py / `demo-algo-science` | `http://lumen-platform-algo-py:8000` |
| 企业图谱 API / Worker | `gkx-entan-py-*` / `demo-platform-entan-py` | `gkxlumen-platform-entan-py` / `entan-py-worker`（ClusterIP） |
| DWD→ES ETL | `demo-platform-etl-es-py`、外网 **30806** | `http://gkxlumen-platform-etl-es-py:8000` |

Helm 环境变量（检索/AI）：

- `GKXLUMEN_TOPIC_ENTERPRISE_PYTHON_BASE_URL=http://gkxlumen-platform-search-py:8080`
- `GKXLUMEN_TOPIC_ASYNC_PYTHON_AI_BASE_URL=http://gkxlumen-platform-ai-py:8081`
- `INNOV_CHAIN_ALGO_BASE_URL=http://lumen-platform-algo-py:8000`

### 2.3 镜像（禁止覆盖左边的 demo tag）

| lumen 镜像（Harbor） | 现网钉死 tag | demo 对照（勿覆盖） |
|----------------------|--------------|---------------------|
| `gkxlumen-search-service` / `ai-service` / `ai-worker` | `5d204114` | `gkx-search-service` 等 |
| `gkxlumen-innov-py` | `9a1889a4` | `gkx-innov-py` |
| `gkxlumen-entan-py-api` / `entan-py-worker` | `9a1889a4` | `gkx-entan-py-*` |
| `lumen-etl-es-py` | `2ac38573` | 已无正式副本 |

lumen 检索/AI **没有**再开 30805/30807；entan **没有**抢 demo 的 30800；ETL **没有**再占 30806。集群内用 Service DNS。

### 2.4 数据面

| 谁 | catalog / 库 |
|----|----------------|
| lumen Java `gkxlumen-innov` + lumen innov-py | `gkxlumenx_{ods,dwd,ads,dim}` + `gkxlumenx_cfg`（1B+2B **去前缀**表名，如 `innovation_event`） |
| lumen entan-py + 厨房 `lumen-algo-py` | `gkxlumenx_{dwd,ads,cfg}` |
| demo innov-py / demo entan-py / demo Java `gkx-innov` | `demo_gkxlumenx_{ods,dwd,ads,dim}` |
| `innov` 库 | **历史 M1 快照**，lumen 运行时不再指向 |

`INNOV_LEGACY_CATALOG=0`。cfg 字典目前仍可两边读同一份正式 cfg——不要在 demo 里改正式口径配置。

---

## 3. 怎么验证（各 1 分钟）

检索金路径（上午已 QA 签收）：

```http
POST http://192.168.88.50:30899/enterprise/topic/v1/search/meta/filters
Content-Type: application/json

{}
```

期望 HTTP **200**、`code=0`。Tempo 下游应是 **`gkxlumen-search-service`**，不得出现 `demo-platform-search-py` / **30805**。

其它（集群内）：

- `gkxlumen-platform-innov-py` / `entan-py*` / `etl-es-py` Ready，镜像是上表 `gkxlumen-*` / `lumen-etl-es-py`
- demo `demo-platform-search-py` 30805 仍应活着（证明没覆盖 demo 制品）
- 外网 `http://192.168.88.50:30806` **不再**当正式 ETL 入口

---

## 4. 分角色：你需要做什么 / 不要做什么

### 前端（`lumen-ui-*`）

- **只打网关 30899**。不要加 `VITE_*` 直连 Python，不要打 30805 / 30800 / 30806 / 30807。
- 企业检索、画像走现有 `/enterprise/**`、`/topicAsync/**`；创新监测走 `/innov/**`。契约路径未改。
- 对照可以读 `demo-ui-*`，**禁止 merge**。

### Java（`lumen-svc-platform`）

- 新代码禁止再写 `demo-platform-*`、`demo-algo-*`、`demo-svc-*`、Nacos `gkx-ai-service`、镜像 `gkx-innov-py` / `gkx-entan-py-*`。
- 检索/AI 直连 URL 见 §2.2；产业链 Job 只打 `lumen-platform-algo-py`。
- 科技新闻仍 Feign 到 `gkxlumen-platform-innov-py`（这是 lumen Deployment，不是 demo）。
- lumen 网关 **没有** `/entan`。不要给正式网关加直连 Python 的 `/entan/**`。

### Python / 算法

| 改哪里 | 仓 |
|--------|-----|
| 专题检索 / AI 门面 | **`lumen-topic-py`** |
| 产业链厨房、innov-py、entan-py | **`lumen-algo-py`**（vendor 目录，不要新建 `lumen-innov-py`） |
| DWD→ES | **`lumen-etl-es-py`** |
| demo 原型 | 对应 `demo-*` 仓；改它们 **不会** 进 lumen 流量 |

- 禁止 merge demo → lumen。镜像名必须 `gkxlumen-*`（ETL 除外，制品名 `lumen-etl-es-py`），不要推 `gkx-innov-py` / `gkx-search-service`。
- lumen innov/entan 运行时不要开 `/v1`。vendor 源码里可以留着，demo 网关 `/entan/**` 仍合法打 **demo** 那套。

### DevOps

- 热更新：
  - 检索/AI：`lumen-topic-py` pipeline 手动 `deploy:search-py` / `ai-py` / `ai-worker`
  - innov/entan：`lumen-algo-py` 的 `deploy:innov` / `deploy:entan-api` / `deploy:entan-worker`
  - ETL：`lumen-etl-es-py` 的 `deploy:etl-es-py`
- **只改 chart、不要滚 Java 镜像**：点 **`helm:chart`**，**不要**点 `helm:deploy`（`helm:deploy` 会把 `global.imageTag` 打成当次 SHA，并可能重发 Nacos）。
- demo 仓 CI 前缀已收窄为 **`demo-platform` only**，不要再加回 `gkxlumen-platform`。

### QA

- TOPIC-PY 两叶（PORT / CUTOVER）**已签收 done**。
- 新回归以 §3 为准：lumen 不打 demo DNS；demo 30805 仍活；正式库与 `demo_gkxlumenx_*` 不要串。
- 失败开缺陷包（必含 `X-Trace-Id`），不要直接改业务仓。

---

## 5. 刻意没做 / 请勿误判

| 项 | 说明 |
|----|------|
| demo 仓没删 | 原型还要继续用；只是不再喂 lumen |
| vendor 仍有 `/v1` 源码 | 运行时已关；不要当「lumen 又对前端暴露了」 |
| `innov` 库还在 | M1 快照，lumen 运行时不指向 |
| Nacos 可能仍被人改过 DataId | 以 git 中 helm configs 为准；Pod env 可压过 |
| 联调台 `X-GKX-PLANE-INNOV=live` | **不再**让 demo 创新 SQL 打回正式 ADS（已全拆） |

---

## 6. 文档入口

| 文档 | 路径 |
|------|------|
| **本通报** | `agent-delivery/agent-handoffs/平台基建-PLATFORM/D12-LUMEN-ISOLATION-团队通报-2026-08-14.md` |
| 上午检索切流（§6 已过时） | `…/D12-LUMEN-TOPIC-PY-团队通报-2026-08-14.md` |
| 架构铁律 D12 | `agent-delivery/architecture-baseline.md` §2 D12、§3.1 |
| 决策 | `agent-delivery/agent-handoffs/DECIDE-D12-LUMEN-CALLCHAIN.md` |
| innov/entan 总控 | `…/D12-LUMEN-INNOV-ENTAN-长任务总控.md` |
| topic-py 总控 | `…/D12-LUMEN-TOPIC-PY-长任务总控.md` |

---

## 7. 飞书可直接粘贴的短讯

```
【D12 全部闭合 2026-08-14 晚】
demo / lumen 运行时已拆开。登记债 TOPIC-PY / INNOV-PY / ENTAN-PY / ETL-ES-PY / REGISTRY 均已闭合。

正式链：lumen-ui-* → 网关 30899 → gkxlumen-* Java → lumen-topic-py / lumen-algo-py / lumen-etl-es-py
检索：gkxlumen-platform-search-py:8080
AI：gkxlumen-platform-ai-py:8081
创新监测 Python：gkxlumen-innov-py（K8s gkxlumen-platform-innov-py）
图谱：gkxlumen-entan-py-*
ETL：gkxlumen-platform-etl-es-py（30806 不再当正式入口）
库：lumen=gkxlumenx_* ；demo=demo_gkxlumenx_*

请 lumen 侧不要再写 demo-platform-* / gkx-ai-service / gkx-innov-py。
禁止 merge demo→lumen。只改 chart 请点 helm:chart，不要点 helm:deploy。
demo-* 仓保留给原型。
详情：orchestration 仓 agent-handoffs/平台基建-PLATFORM/D12-LUMEN-ISOLATION-团队通报-2026-08-14.md
```
