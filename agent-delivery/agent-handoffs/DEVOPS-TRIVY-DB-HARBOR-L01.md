# DEVOPS-TRIVY-DB-HARBOR-L01 · Harbor 镜像 trivy-db，三仓 frontend scan 走内网库

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户 `/goal` 授权执行 job 24621 推荐方案；监管人与会话操作人一致 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用三仓已有 `trivy:frontend`，只改漏洞库地址与 Harbor 登录；未抽公共模板、未改 `allow_failure` / `--exit-code 0` |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶为 GitLab CI + Harbor OCI，未挂载 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 不改调用链 / 存储流图 |
| 会签态 | N/A |

## 问题清单

- 无阻塞。漏洞库需不定期从 ghcr 续镜像到 Harbor（当前层 digest `sha256:d35644f883794a61248ab3f45f797411cc2e7f2c1f2a51eef1cfcd0e393698df`，上游标注 created 2026-08-26）。
- `internet` 是 Harbor 代理缓存项目（`registry_id=2`），不能推自定义 OCI；DB 放在 `gkx`。

## 修改内容

- 在 88.84 断点续传拉完 `ghcr.io/aquasecurity/trivy-db:2` 的 `db.tar.gz`（sha256 与上游层一致），`oras push` 到 `harbor.htmisoft.net/gkx/aquasecurity/trivy-db:2`（manifest `sha256:b58c021f9b0a622224178427fd7f1f141b3bb84520594a528a30f22d3a482916`）。
- 三仓 `.gitlab-ci.yml`：`TRIVY_DB_REPOSITORY` 指向上述 Harbor 库；scan job `docker login` + 挂 `~/.docker`；`--skip-java-db-update` 避免再打 ghcr 的 java-db。
  - `lumen-ui-science-mobile` `b1f6685`
  - `lumen-ui-science-pc` `d8f415f`
  - `lumen-ui-topic` `3602a05`

pc / topic 原先已有 `trivy:frontend`（dev 会跑，但一直打 ghcr 失败）。本叶把 scan **跑通**，不是从零加 stage。

## 测试结果

| 仓 | pipeline | `trivy:frontend` | 证据 |
|----|----------|------------------|------|
| science-mobile | [5676](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-mobile/-/pipelines/5676) | [24657 success](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-mobile/-/jobs/24657) 21s | alpine 3.21.3，Total 35 (HIGH 33 / CRITICAL 2)，无 PROTOCOL_ERROR |
| science-pc | [5677](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-pc/-/pipelines/5677) | [24661 success](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-pc/-/jobs/24661) 18s | 日志 `DB Repository: harbor.htmisoft.net/gkx/aquasecurity/trivy-db:2` 后 `Downloading DB...` |
| topic | [5678](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5678) | [24665 success](https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/24665) 6s | cache 命中，scan success |

88.36 本地复测：Trivy 从 Harbor 拉库约 100 MiB/s、5s 内完成（对比 ghcr ~100 KiB/s 且中途 EOF）。

## 遗留风险

- 未做定时续镜像；DB 会过期。升级路径：cron/`oras copy` 到同一 tag，或再加一条 devops 叶。
- `allow_failure: true` 且 `--exit-code 0`：CVE 仍不挡发布（与改前一致）。
- science-pc `deploy:k8s` 仍是 manual，与本叶无关。

## CI/CD（必填）

- 分支：三仓 `origin/dev`
- commit：mobile `b1f6685` / pc `d8f415f` / topic `3602a05`
- pipeline：5676 / 5677 / 5678
- 部署 namespace / 镜像 tag：mobile、topic 本趟 `deploy:k8s` 已绿；pc deploy 仍为 manual
- K8s rollout：mobile + topic 成功；pc 未自动发
- dev 测试 URL：mobile http://10.50.69.111:30898 ；topic http://10.50.69.111:30892 ；pc 未在本叶强制 rollout

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A（CI scan）
- traceId：N/A
- Tempo / Loki：无

## 涉及文件

- `lumen-ui-science-mobile/.gitlab-ci.yml`
- `lumen-ui-science-pc/.gitlab-ci.yml`
- `lumen-ui-topic/.gitlab-ci.yml`
- Harbor `gkx/aquasecurity/trivy-db:2`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未改算法 |
| 调用链 前端→Java→Python | ✅ 未改 |
| 图谱 Nebula | ✅ 未改 |
| 可观测 | ✅ N/A（CI） |
| CI/CD push→Pipeline | ✅ 三仓 dev 已推，scan 绿 |
| demo2 不 merge lumen | ✅ 只改 lumen-ui-* |
| D12 lumen 不调 demo | ✅ 未改网关 |
| D8/D9/D10 | ✅ 未改 UI |
| ponytail | full |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000（会话估算，含排障等待） |
| model_used | grok-4.6 |
| actual_cost | 0.80 |
| cost_warn | green |
