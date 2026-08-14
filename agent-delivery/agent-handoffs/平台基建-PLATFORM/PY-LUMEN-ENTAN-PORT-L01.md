# PY-LUMEN-ENTAN-PORT-L01 · lumen-algo-py 对照迁入 entan-py

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控） |
| 说明 | D12-DEBT-ENTAN-PY 第 1 叶。本叶不改 helm 镜像名、不改 demo CI。淮政玮 2026-08-14 签收 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对照复制 `vendor/entan-py`；独立 api/worker 镜像；pytest 已 ignore vendor。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 对照复制 + CI，不依赖检索。 |

## 问题清单

- 对照源仍暴露 `/v1/**`（helm 注释网关 `/entan/**`）。本叶不扩、不收口为仅 `/internal`（as-built）。lumen 前端仍只经网关调 Java。

## 修改内容

对照 `demo-algo-ent-analysis@1054146` → `vendor/entan-py`。

| 项 | 值 |
|----|-----|
| 镜像 | `gkxlumen-entan-py-api` / `gkxlumen-entan-py-worker` |
| Dockerfile | `docker/Dockerfile.entan-api` · `docker/Dockerfile.entan-worker` |
| deploy | `gkxlumen-platform-entan-py` / `-worker`（本叶 manual 未切） |

未改 `repos/demo-algo-ent-analysis`。未改 helm repository。

## 测试结果

- commit：`ef54caa`（对照迁入）→ 现网钉 `9a1889a4`（PIN-SHA）
- Pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5030  
  `py:test` + `image:entan-api` + `image:entan-worker` **success**
- **2026-08-14 20:16 复验（淮政玮点名跑本叶）**：`dev` ns Ready 1/1
  - api `{"status":"ok"}` ← `gkxlumen-entan-py-api:9a1889a4`
  - worker `{"status":"ok"}` ← `gkxlumen-entan-py-worker:9a1889a4`
  - demo 仍 `gkx-entan-py-api:latest`（D12 隔离，未覆盖）

## 遗留风险

- `/v1/**` 对前端直达是既有偏离，不在本叶伪闭合。
- CUTOVER / PIN-SHA 已切 lumen 制品；本叶不必再对照复制。

## CI/CD（必填）

- 分支：`dev`
- commit：`ef54caa`（本叶）/ 现网 `9a1889a4`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5030
- 镜像 tag：`gkxlumen-entan-py-api:9a1889a4` / `gkxlumen-entan-py-worker:9a1889a4`
- K8s rollout：`gkxlumen-platform-entan-py` / `-worker` Ready 1/1（ns=dev）
- healthz：api `:8000/healthz` ok；worker `:8001/healthz` ok

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-entan-py-api` / `gkxlumen-entan-py-worker`

## 涉及文件

- `vendor/entan-py/**`
- `docker/Dockerfile.entan-api` · `docker/Dockerfile.entan-worker`
- `.gitlab-ci.yml`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| Python 算法 | ✅ |
| D12 不 merge | ✅ 对照复制 |
| 不覆盖 demo tag | ✅ `gkxlumen-entan-py-*` |
| 不塞进 py:test compileall | ✅ `--ignore=vendor` |

## 下一步

`API-LUMEN-INNOV-ENTAN-CUTOVER-L01`
