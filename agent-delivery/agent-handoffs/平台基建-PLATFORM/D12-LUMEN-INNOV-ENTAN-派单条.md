# D12-DEBT-INNOV-PY / ENTAN-PY · lumen-algo-py 实现三叶

> 决策：`DECIDE-D12-LUMEN-CALLCHAIN` · 基线 `architecture-baseline.md` §3.1  
> 监管人默认：`human:淮政玮`  
> 强度：ponytail **full**。禁止用 YAGNI 跳过调用链（前端→Java→`/internal`）、OTel、与 demo 隔离。

## 为什么进 `lumen-algo-py`、不新建仓

- 基线：INNOV 算法进程迁入 **`lumen-algo-py`（或独立 `lumen-innov-py`）**；ENTAN **只**迁入 `lumen-algo-py`。
- Topic 是检索/AI **门面**，禁止并进厨房；innov/entan 是 **算法进程**，优先并进已有厨房仓。
- 禁止 `lumen-svc-innov-py`（`svc`=Java）。禁止只改 GitLab 名冒充切流。
- 现网泄漏根因：demo 仓 CI `PLATFORM_K8S_PREFIXES: "demo-platform gkxlumen-platform"` 一次 `set image` 热更新 **两边** Deployment，且镜像名仍是 `gkx-innov-py` / `gkx-entan-py-*`。

## 三叶（串行，同仓 1–2）

| 顺序 | ID | Agent | 状态意图 | 依赖 |
|------|-----|--------|----------|------|
| 1 | `PY-LUMEN-INNOV-PORT-L01` | algorithm-agent | 对照复制 innov 树 + 独立镜像/CI（**不切 helm 镜像名**） | D12 已拍板 |
| 2 | `PY-LUMEN-ENTAN-PORT-L01` | algorithm-agent | 对照复制 entan 树 + 独立镜像/CI | L01 联调闸门 |
| 3 | `API-LUMEN-INNOV-ENTAN-CUTOVER-L01` | api-agent + devops | helm 切 `gkxlumen-*`；demo CI 只更新 `demo-platform`；删 demo 回落 | L01+L02 镜像已推 |

## `/goal` 摘要

### PY-LUMEN-INNOV-PORT-L01

对照 `demo-algo-science` 复制到 `${GKX_ROOT}/repos/lumen-algo-py/vendor/innov-py`（禁止 merge）。  
Dockerfile / CI 镜像 **`gkxlumen-innov-py`**。deploy 只更新 `gkxlumen-platform-innov-py`。  
`py:test` 仍只 compileall `lumen_algo_service` / `lumen_algo_worker` / `lumen_common`。  
本叶不改 `values-lumen.yaml` 镜像仓库名、不改 demo-algo-science CI。

### PY-LUMEN-ENTAN-PORT-L01

对照 `demo-algo-ent-analysis` → `vendor/entan-py`。镜像 **`gkxlumen-entan-py-api`** / **`gkxlumen-entan-py-worker`**。  
deploy：`gkxlumen-platform-entan-py` / `gkxlumen-platform-entan-py-worker`。  
既有偏离：demo 门面仍暴露 `/v1/**`（helm 注释网关 `/entan/**`）；本叶不扩、不改成前端直连新路径。lumen 前端仍只经网关调 Java。

### API-LUMEN-INNOV-ENTAN-CUTOVER-L01

- helm `innovPy` / `entanPy` / `entanPyWorker` 的 `image.repository` → `gkxlumen-*`。
- 删除 values「可回落 `demo-platform-innov-py`」。
- `INNOV_CHAIN_ALGO_BASE_URL` / Nacos `gkxlumen-innov` chain → `http://lumen-platform-algo-py:8000`（产业链禁止 innov-py）。
- 科技新闻仍 `http://gkxlumen-platform-innov-py:8000`（DNS 不变，换制品来源）。
- `demo-algo-science` / `demo-algo-ent-analysis`：`PLATFORM_K8S_PREFIXES: "demo-platform"`。

## 不在本三叶

- 迁库 / 换 `innov` schema
- 把 entan `/v1/**` 收口成仅 `/internal/*`（登记为 as-built，不伪闭合）
- 改 `demo-ui-*` 产品行为
