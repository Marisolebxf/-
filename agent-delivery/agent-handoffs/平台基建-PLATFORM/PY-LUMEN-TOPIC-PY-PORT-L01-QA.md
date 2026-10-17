# PY-LUMEN-TOPIC-PY-PORT-L01-QA · lumen-topic-py 迁检索/AI/worker 切流验收

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控已授权；父会话已认领并推进 `testing`，本叶未再 claim） |
| 说明 | D12-DEBT-TOPIC-PY 第 2 叶 QA。测 **K8s 已发布** 隔离与冒烟，不改业务仓。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 写测 / 段 E 冒烟，未用 YAGNI 跳过 D12 隔离、可观测 trace、handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom；验收走网关 + SSH kubectl。 |

## 问题清单

- 无 P0 缺陷。未开缺陷包。
- **WARN（不挡切流）**：集群内 `gkxlumen-platform-ai-py:8081/healthz` 的 JSON `service` 仍为 `gkx-ai-service`（对照迁代码 logger/探针名未改）。K8s Deployment/Service/Harbor 镜像均为 `gkxlumen-ai-*`，Tempo 金路径未出现 demo 服务名。
- **WARN（不挡切流）**：可选分析任务创建被 Java 校验拒绝（`subType` 非法），未打到算法厨房。厨房失败本就不挡切流。
- `query`/`suggest` 对 `huawei`/`华为` 返回诚实空列表（HTTP 200 `code=0`），ES 探活 `es_available=true`。热门词 `/search/hot` 有数据。不判 FAIL。

## 修改内容

- 无代码变更，仅验收。

## 测试结果

测试时间：2026-08-14 14:51–14:55 +08。入口：网关 `http://192.168.88.50:30899`；前端 `http://192.168.88.50:30892`。禁止 localhost。

| # | 用例 | 证据 | 结果 |
|---|------|------|------|
| 1 | filters 主路径 `POST /enterprise/topic/v1/search/meta/filters` body `{}` | HTTP **200**，`code=0`，`ok=true`，含 `listing_statuses` / `operating_statuses`；耗时 **202ms**；`X-Trace-Id=338e664a81c06d9c0fd48d21f2df67a1` | **PASS** |
| 2 | 检索主路径 `POST /search/hot` body `{}` | HTTP **200**，`code=0`，`data` 为热词数组；耗时 **394ms**；`X-Trace-Id=cf4ff92c186140870b15c0be9ae9ae48` | **PASS** |
| 2b | `POST /search/suggest` `{"prefix":"huawei","size":5}` | HTTP **200**，`code=0`，`data=[]`（诚实空态）；`X-Trace-Id=406b83179050507b43fd89d596dd0aa9` | **PASS** |
| 2c | `POST /search/query` `{"keyword":"huawei","page":1,"size":5}` | HTTP **200**，`code=0`，`list=[]` `total=0`（诚实空态）；`X-Trace-Id=f669f6b0fb6068416d5fb4f0d5ecd67a` | **PASS** |
| 3 | 隔离：响应/错误不得含 `30805` / `demo-platform-search-py` / `demo-platform-ai-py` | 上列全部 body + Tempo 金路径 payload 均 0 命中 | **PASS** |
| 4 | demo 仍活 `GET http://192.168.88.50:30805/healthz` | HTTP **200**，`service=gkx-search-service`；demo Deployment 1/1 Running | **PASS** |
| 5 | K8s 三件套 Ready + 镜像 `gkxlumen-*` | 见下表 | **PASS** |
| 6 | 集群内 healthz | search `service=gkxlumen-search-service` `es_available=true`；AI `status=ok`（探针名见 WARN） | **PASS** |
| 7 | 分析任务（可选） | `POST /topicAsync/topic/v1/analysis/tasks/list` → 200 `code=0` 空页；create → 200 `code=1` 校验文案，未打厨房 | **WARN**（不挡） |
| 8 | CI 只核证据 | Python pipeline **5026** 全绿 | **PASS** |

### K8s（SSH `88.50`，ns=`dev`，约 44–46min 龄）

| 资源 | Ready | 镜像 |
|------|-------|------|
| `gkxlumen-platform-search-py` | 1/1 Running | `harbor.htmisoft.net/gkx/gkxlumen-search-service:5d204114` |
| `gkxlumen-platform-ai-py` | 1/1 Running | `harbor.htmisoft.net/gkx/gkxlumen-ai-service:5d204114` |
| `gkxlumen-platform-ai-worker` | 1/1 Running | `harbor.htmisoft.net/gkx/gkxlumen-ai-worker:5d204114` |
| demo `demo-platform-search-py`（对照，勿覆盖） | 1/1 | `gkx-search-service:latest` NodePort **30805** |
| demo `demo-platform-ai-py` | 1/1 | `gkx-ai-service:latest` NodePort **30807** |

lumen Service 为 ClusterIP（search `:8080` / AI `:8081`），**未**占用 30805/30807。

集群内：`http://gkxlumen-platform-search-py:8080/healthz` 与 `:8081/healthz` 均可从 Java Pod DNS 打通。

### Tempo（金路径 filters）

- Grafana：`http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf）` → Explore → Tempo → TraceID `338e664a81c06d9c0fd48d21f2df67a1`
- API：`http://192.168.88.50:30201/api/traces/338e664a81c06d9c0fd48d21f2df67a1` → HTTP 200，约 20KB
- `service.name`：`gkxlumen-gateway` → `gkxlumen-topic-enterprise-biz` → **`gkxlumen-search-service`**
- payload 含 `gkxlumen-platform-search-py`×4；`demo-platform-search-py`×0、`30805`×0、`gkx-search-service`×0

## 遗留风险

- D12-DEBT-INNOV-PY / D12-DEBT-ENTAN-PY 仍开（本管线范围外）。
- DWD 仍 `demo_gkxlumenx_dwd`（切服务 ≠ 切库）。
- AI 探针 JSON 服务名仍 `gkx-ai-service`（见问题清单 WARN）。
- 本叶 pytest 1 fail（`test_query_tree_dsl.py` `name_en` extra）为开发 handoff 已声明对照源即有，CI smoke 不含，QA 未扩测。

## CI/CD（必填）

- 分支：`dev`
- commit：`5d20411`（`lumen-topic-py`）
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5026 （smoke + 三镜像 + 三 deploy，全绿；本 QA **不重跑**）
- 部署 namespace：`dev`
- K8s rollout：三 Deployment 1/1 Running，镜像 tag `5d204114`
- dev 测试 URL：`POST http://192.168.88.50:30899/enterprise/topic/v1/search/meta/filters` → 200 `code=0`

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-search-service` / `gkxlumen-ai-service`（K8s 注入）；AI 探针 JSON 名仍 `gkx-ai-service`
- traceId（dev 抽样）：`338e664a81c06d9c0fd48d21f2df67a1`（filters）
- Tempo / Loki：Tempo **有**（上节）；Loki 未强制（本叶 PASS，未做失败三联查）

## 涉及文件

- 无业务仓改动。
- 本 handoff：`agent-delivery/agent-handoffs/平台基建-PLATFORM/PY-LUMEN-TOPIC-PY-PORT-L01-QA.md`
- 开发 handoff：`…/PY-LUMEN-TOPIC-PY-PORT-L01.md`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 厨房仍 `lumen-algo-py`，本叶未并仓 |
| 2 调用链 `/internal` | ✅ 网关 → Java → lumen-topic-py |
| 3 Nebula | ✅ 未改 |
| 4 可观测 | ✅ Tempo 可见 `gkxlumen-search-service` |
| 5 CI/CD | ✅ 5026 证据 |
| 6 禁止 merge demo | ✅ demo 镜像仍独立 `gkx-*` |
| 7 Java 不写算法 | ✅ |
| 8 数据 | ✅ 未切库 |
| 9–11 D8/D9/D10 | N/A 切流冒烟 |
| 12 D12 | ✅ lumen 流量未打 demo NodePort/服务名 |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 0.45 |
| cost_warn | green |
