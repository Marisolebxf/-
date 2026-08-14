# PY-LUMEN-INNOV-PORT-L01 · lumen-algo-py 对照迁入 innov-py

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控授权，lock 24h） |
| 说明 | D12-DEBT-INNOV-PY 第 1 叶。本叶不改 helm 镜像名、不改 demo CI。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照复制进 `vendor/innov-py`，独立 Dockerfile/CI；`py:test` 仍只跑厨房三包。未新建 GitLab 仓。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 对照复制 + CI 改名，不依赖检索压缩。 |

## 问题清单

- 无。未新建 `lumen-innov-py`（总控拍板并进 `lumen-algo-py`）。

## 修改内容

对照 `demo-algo-science@122f0c1` 复制到 `vendor/innov-py`（禁止 merge）。

| 项 | 值 |
|----|-----|
| 镜像 | `gkxlumen-innov-py`（**不**覆盖 `gkx-innov-py`） |
| Dockerfile | `docker/Dockerfile.innov` |
| K8s（本叶不切） | 仍 `gkxlumen-platform-innov-py`；`deploy:innov` 仅 `set image` |
| OTel 默认 | `gkxlumen-innov-py` → `gkxlumen-platform-otel-collector:4318`（helm 仍会覆盖） |
| pytest | `--ignore=vendor` + `pytest.ini` `norecursedirs = vendor` |

未改 `repos/demo-algo-science`。未改 helm `image.repository`。

## 测试结果

- commit：`179fe8d`（含 `396d0d3` 复制 + pytest 忽略 vendor）
- Pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5029  
  `py:test` / `image:api` / `image:worker` / **`image:innov` success**；deploy 保持 manual（本叶不切运行时）
- 5028 因 vendor 测试被 pytest 收集而红，已用 `--ignore=vendor` 修复

## 遗留风险

- 现网 `gkxlumen-platform-innov-py` 仍跑 `gkx-innov-py`，直到 CUTOVER。
- `vendor/innov-py` 仍带 `/v1/chain/**`（对照源）；产业链正式路径仍是 `lumen_algo_service`。
- 切服务 ≠ 切库（MySQL `innov`）。

## CI/CD（必填）

- 分支：`dev`
- commit：`179fe8d`
- pipeline URL / ID：https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5029
- 部署 namespace / 镜像 tag：未 deploy；Harbor `gkxlumen-innov-py:179fe8d` + `:latest`
- K8s rollout：本叶 **未** 触发 `deploy:innov`
- dev 测试 URL：ClusterIP `gkxlumen-platform-innov-py:8000/healthz`（仍旧镜像）

## 可观测性（建议）

- OTEL_SERVICE_NAME：镜像默认 `gkxlumen-innov-py`；现网 helm 仍可能写 `gkx-innov-py` 直到 CUTOVER 改 `serviceName`

## 涉及文件

- `vendor/innov-py/**` · `vendor/README.md`
- `docker/Dockerfile.innov`
- `.gitlab-ci.yml`
- `pytest.ini`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 调用链前端→Java→`/internal` | ✅ 本叶不改 Java；科技新闻已是 `/internal/tech-news/*` |
| Nebula | ✅ 未改图库 |
| 可观测 | ✅ Dockerfile OTel env |
| CI | ✅ pipeline 5029 image:innov 绿 |
| D12 不 merge demo | ✅ 对照复制 |
| 不覆盖 demo Harbor tag | ✅ `gkxlumen-innov-py` |

## 下一步

`PY-LUMEN-ENTAN-PORT-L01`（同仓 vendor/entan-py）。
