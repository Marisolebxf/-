# D12-DEBT-TOPIC-PY · lumen-topic-py 实现三叶

> 决策：`DECIDE-D12-LUMEN-CALLCHAIN` · 基线 `architecture-baseline.md` §3.1  
> 监管人默认：`human:淮政玮`（建仓/切流）+ 算法监管按花名册  
> 强度：ponytail **full**。禁止用 YAGNI 跳过调用链（前端→Java→`/internal`）、OTel、与 demo 隔离。

## 为什么不是改名、不是 `lumen-svc-topic-py`

- 现网 lumen Java **已经**打 `http://demo-platform-search-py:8080`（`demo-svc-topic-py`）。只改 GitLab 名不切流量。
- `svc` = Java 层。本仓是 Python 检索/AI 门面，命名对齐 `lumen-algo-py` / `lumen-etl-es-py` → **`lumen-topic-py`**。
- 禁止并进 `lumen-algo-py`（产业链已禁整包搬 topic-py）。
- `demo-svc-topic-py` **保留**，服务 demo 前端。

## 三叶（串行）

| 顺序 | ID | Agent | 状态意图 | 依赖 |
|------|-----|--------|----------|------|
| 1 | `DEVOPS-LUMEN-TOPIC-PY-L01` | devops-agent | 建 GitLab 仓 + CI + K8s 资源名（**不切 Java 流量**） | D12 已拍板 |
| 2 | `PY-LUMEN-TOPIC-PY-PORT-L01` | algorithm-agent | 对照 `demo-svc-topic-py` 迁 search / ai / worker；独立演进 | L01 |
| 3 | `API-LUMEN-TOPIC-PY-CUTOVER-L01` | api-agent | `gkxlumen-topic-enterprise` / async Feign+helm 切到 lumen Service；删除 demo 回落 | L01+PORT |

## `/goal` 摘要

### DEVOPS-LUMEN-TOPIC-PY-L01

对照 `DEVOPS-LUMEN-UI-ADMIN-L01`。新建 `gkx-lumen/lumen-topic-py`，本地 `${GKX_ROOT}/repos/lumen-topic-py`。  
K8s 前缀 `gkxlumen-platform-`：`search-py` / `ai-py` / `ai-worker`。镜像名勿再沿用仅 demo 的 `demo-platform-*` Deployment。  
**本叶不改** `GKXLUMEN_TOPIC_ENTERPRISE_PYTHON_BASE_URL`（仍指向 demo，直到 CUTOVER）。不破坏 `demo-svc-topic-py`。

### PY-LUMEN-TOPIC-PY-PORT-L01

对照 demo 仓 `gkx_search_service` / `gkx_ai_service` / `gkx_ai_worker` 在 **lumen-topic-py** 落地。可复制后改名，禁止 git merge demo→lumen。算法厨房仍只调 `lumen-algo-py` `/internal`（已有 ARCH-ENT-PY-LUMEN-ALGO-ADAPT）。仅 `/internal/*`，不对前端暴露。

### API-LUMEN-TOPIC-PY-CUTOVER-L01

`python-base-url` / env `GKXLUMEN_TOPIC_ENTERPRISE_PYTHON_BASE_URL` 从 `http://demo-platform-search-py:8080` 改为 `http://gkxlumen-platform-search-py:8080`（以 DEVOPS 实际 Service 名为准）。async `python-ai-service-name` 同步。删除「可回落 demo」注释与默认值。lumen-ui-topic 走网关回归检索/画像一条主路径。

## 不在本三叶

- D12-DEBT-INNOV-PY / ENTAN-PY（另拆）
- 产业链（已在 `lumen-algo-py`）
