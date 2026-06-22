# DevOps handoff：E-INNOV-M1-L02b

- 时间：2026-06-19
- 任务：gkx_lumen_backend → **lumen-svc-platform** 移植 GitLab CI + Helm
- 仓库：`gkx-lumen/lumen-svc-platform`
- 分支：`main`

## 产物

| 文件 | 说明 |
|------|------|
| `.gitlab-ci.yml` | backend:build / image(gateway,auth,upms) / helm:lint / helm:deploy(manual) |
| `helm/gkxlumen-platform/` | 从 demo gkx-platform 复制并适配 gkxlumen-* 镜像与 jarPath |
| `scripts/download-otel-agent.sh` | OTel JavaAgent 下载（CI package 前） |
| `gkxlumen-gateway|auth|upms-biz/Dockerfile` | harbor 基础镜像 + JAVA_TOOL_OPTIONS javaagent |

## 源码来源

- Java 代码：`E:/gkx_src/gkx_lumen_backend` → `${GKX_ROOT}/repos/lumen-svc-platform`
- CI/Helm 模板：`E:/gkx_src/gkx_service_demo`

## CI

- Pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/4110
- DoD：`backend:build` 绿；`helm:deploy` manual（符合 task-registry）

## 镜像（Harbor）

- `harbor.htmisoft.net/gkx/gkxlumen-gateway:{sha}`
- `harbor.htmisoft.net/gkx/gkxlumen-auth:{sha}`
- `harbor.htmisoft.net/gkx/gkxlumen-upms:{sha}`

## dev 部署

- `helm:deploy` → namespace `dev`，release `gkx`，chart `helm/gkxlumen-platform`
- 回滚：`helm rollback gkx {revision} -n dev`

## 架构合规

- OTel JavaAgent ✅
- Helm OTEL_* env（chart 模板 gkx.commonEnv）✅
- 禁用 latest 部署 tag（CI 用 SHA + ref slug）✅

## 偏离

- 新 GitLab 组 `gkx-lumen`（非 task 原文 SZCGKX）
- 首版 CI 仅打包 gateway/auth/upms 三服务（L03 innov 模块待 api-agent）
