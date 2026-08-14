# API-LUMEN-INNOV-ENTAN-CUTOVER-L01 · helm 切 gkxlumen-*；demo CI 收窄

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控） |
| 说明 | 闭合 D12-DEBT-INNOV-PY / ENTAN-PY 运行时。前置：lumen-algo-py pipeline 5038 image 全绿。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改镜像名、删 demo 回落、收窄 demo CI 前缀；K8s Service DNS 不变。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 配置切流，不依赖检索。 |

## 问题清单

- 网关 `GET /innov/v1/dict/event-types` 本机 **424**（鉴权/依赖，与本次 Python 切流无关）。切流证据以 K8s healthz 为准。
- entan `/v1/**` 经网关 `/entan/**` 为既有 as-built，本叶不收口。

## 修改内容

| 项 | 旧 | 新 |
|----|----|----|
| helm `innovPy.image.repository` | `gkx-innov-py` | `gkxlumen-innov-py` |
| helm `entanPy` / Worker | `gkx-entan-py-*` | `gkxlumen-entan-py-api` / `gkxlumen-entan-py-worker` |
| `INNOV_CHAIN_ALGO_BASE_URL` | `gkxlumen-platform-innov-py:8000` | `lumen-platform-algo-py:8000` |
| 科技新闻 URL | `gkxlumen-platform-innov-py:8000` | **不变**（换制品） |
| demo CI `PLATFORM_K8S_PREFIXES` | `demo-platform gkxlumen-platform` | `demo-platform` |
| 回落注释 | 可回落 `demo-platform-innov-py` | **删除** |

## 测试结果

- Java helm commit：`474e98a` pipeline [5035](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5035) `helm:deploy` [#21627](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/jobs/21627) **success**
- Python：pipeline [5038](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5038) commit `8730ec9`
  - `deploy:innov` [#21647](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/jobs/21647) **success** healthz `{"status":"ok"}` 镜像 `gkxlumen-innov-py:8730ec91`
  - `deploy:entan-api` [#21648](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/jobs/21648) **success**
  - `deploy:entan-worker` [#21649](https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/jobs/21649) **success**
- demo CI：`demo-algo-science` `42f1392` · `demo-algo-ent-analysis` `db1bacd`（只更新 `demo-platform`）

## 遗留风险

- 切服务 ≠ 切库（`innov` / `gkxlumenx_*`）。
- entan `/v1/**` 对前端直达仍是 as-built。
- 网关 innov 字典 424 需鉴权，未当作本叶失败。

## CI/CD（必填）

- 分支：`lumen-svc-platform` / `lumen-algo-py` `dev`；demo 仓 `dev`
- commits：`474e98a` · `8730ec9` · `42f1392` · `db1bacd`
- K8s ns=`dev`；镜像 tag `8730ec91`
- rollout：**success**（上表 job）
- healthz：innov pod `{"status":"ok"}`

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-innov-py` / `gkxlumen-entan-py-api` / `gkxlumen-entan-py-worker`

## 涉及文件

- `helm/gkxlumen-platform/values.yaml` · `values-lumen.yaml` · `configs/gkxlumen-innov-dev.yml` · templates
- `demo-algo-science/.gitlab-ci.yml` · `demo-algo-ent-analysis/.gitlab-ci.yml`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 不打 demo 运行时 | ✅ lumen Deployment 不再由 demo CI 更新 |
| 不覆盖 demo Harbor tag | ✅ `gkxlumen-*` |
| 调用链科技新闻 Java→Python `/internal` | ✅ DNS 不变 |
| 产业链禁止 innov-py | ✅ `INNOV_CHAIN` → `lumen-platform-algo-py` |
