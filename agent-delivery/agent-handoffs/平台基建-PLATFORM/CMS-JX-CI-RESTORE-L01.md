# CMS-JX-CI-RESTORE-L01 · 找回 CMS CI/部署三件套（merge 丢失修复）

> **任务**：`CMS-JX-CI-RESTORE-L01`（chore / P1 / CMS-JX-INT）
> **代码**：lumen-svc-platform `cb2d4e1`（origin/dev 已推）
> **监管**：human:徐滕强（2026-10-15 15:50 拍板走 devops-agent 自修）

## Ponytail

ponytail: `full`（纯找回 aebbf77 已评审内容 + 两处环境适配，无新设计）

## 问题与根因

- **现象**：pipeline 2586 无 `backend:image:cms` / `deploy:cms`；CMS 无镜像无部署
- **根因**：10-14 环境迁移 `0843d02 merge(legacy)` 解冲突时，`aebbf77`（api-agent 10-15 交付）携带的 CMS CI 三件套被主线版本覆盖丢失——`.gitlab-ci.yml` 两处 job 段、`gkxlumen-cms/Dockerfile`、`helm values.yaml microservices.cms` 全部消失
- **连带影响**：10-17 POL-CRUD 冒烟用的 Pod（ddbd569）实为丢失前构建；10-19 起 CMS 部署链路彻底断（这也是 gkxlumenx_cms 业务库一直没人建 DDL 的原因——helm 装不出就不会建）

## 修复内容（从 aebbf77 找回 + 新环境适配）

| 文件 | 恢复内容 | 适配点 |
|---|---|---|
| `.gitlab-ci.yml` | `backend:image:cms` job + `helm:deploy` needs 补 cms + `deploy:cms` set-image job | 无（模板引用不变） |
| `gkxlumen-cms/Dockerfile` | java:21-anolis 基础 + OTel agent + 7098 端口 | 基础镜像 `harbor.htmisoft.net` → **`harbor.test.com/zp-tts`**（对齐 topic/metrics 现行写法） |
| `helm/.../values.yaml` | `microservices.cms`（platformDb=gkxlumenx_cms / 7098 / ClusterIP / CMS_SOURCE_* env） | `CMS_SOURCE_MYSQL_HOST` 直接写 **10.50.11.76**（原 10.50.11.76 已废弃） |
| `helm/.../values-lumen.yaml` | `cms: { enabled: true }` | — |

## 验证（pipeline 2591）

1. `helm:lint` success（chart 语法绿）
2. `backend:image:cms` success → 镜像 `harbor.test.com/zp-tts/gkxlumen-cms:cb2d4e10` 入库
3. `helm:deploy`（手动触发）success → Deployment `gkxlumen-platform-cms` 首装 zhipu-tts
4. `deploy:cms`（手动触发，重试后）success → trace 显示 Pod `gkxlumen-platform-cms-f88c87f5f-hdnvt` **1/1 Running**（滚动替换旧 ReplicaSet）
5. 前置修复：`gkxlumenx_cms` 业务库在本机已按 `db/9x_gkxlumenx_cms.sql` 建库建表（POL-EXPIRED 单过程中完成），Pod 启动即可用

## 遗留（不阻塞本单）

- **CMS_API_KEY**：Pod 环境缺 nacos `gkxlumen-cms-dev.yml` dataId 的话，Api-Key 为空=拒绝全部（fail-closed，本地默认安全）。首次联调前需在 nacos 配置该 dataId（运维动作，口令不进 git）
- **业务库 DDL 漂移**：10-17 后若 `9x_gkxlumenx_cms.sql` 有他人在别处建过表，以 git 内 DDL 为准核对一次

## 架构合规

✅ 纯 CI/Helm 配置找回 / 口令未入 git（API_KEY 走 nacos）/ origin/dev 直推

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~45000 |
| model_used | glm-5.3 (Cursor) |
| actual_cost | ~$0.5 |
| cost_warn | green |
