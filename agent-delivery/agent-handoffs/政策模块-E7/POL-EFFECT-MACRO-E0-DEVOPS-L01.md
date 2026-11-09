# POL-EFFECT-MACRO-E0-DEVOPS-L01 · 落地实效宏观代理：E0 发布门

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md) §3 · 前序：FE / JAVA / ALGO / MID handoff（同目录）
> 日期：2026-11-09 · 类型：chore · Epic：`E-POLICY-PDR`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 纯发布核验，未改任何业务仓代码。连通性直接在 Pod 里调用 `macro_effect_card()`（真实代码路径），未另写探测脚本。SSH 合计 5 次调用，无探活。 |

## 结论

**E0 过门。** 5 仓 Pipeline 均绿（lumen-algo-py 见下「注意」），K8s dev 已滚到目标 commit，`lumen` 与 `demo` 算法 Pod 均可达 `gkx` 并真算出结果。E1 金路径 #1 可期望 `computable=true`，不会落「宏观源不可达」空态。

## 1. Pipeline / rollout 证据（`origin/dev`）

| 仓 | commit | Pipeline | 状态 | 关键 job | K8s 现状 |
|----|--------|----------|------|----------|----------|
| lumen-ui-topic | `112afa6` | [#4364](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/pipelines/4364) | ✅ success | build / image / trivy / sonar / `deploy:k8s` 全绿 | `gkx-lumen-topic` 镜像 tag `112afa6e` Running |
| lumen-svc-platform | `925df28` | [#4360](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4360) | ✅ deploy 全绿 | `backend:build`、8 个 image、`sonar:scan`、`deploy:topic-policy/topic-svc/topic-chain/topic-async-service/topic-enterprise/innov/display/element/cms` 全 success；`helm:*` / `deploy:nacos` / `diag:*` 为 manual 未触发（按规约日常 push 不碰 Nacos） | `gkxlumen-platform-topic-policy` 等 pod Running（镜像按 digest 引用，未逐个核 digest；以 deploy job success 为准） |
| lumen-algo-py | `1847cd9`（含 macro effect） | [#4359](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/4359) | ✅ py:test / sonar / `deploy:api` / `deploy:worker` / `deploy:entan-api` / `smoke:synth-routes` 全 success；`deploy:entan-worker` / `deploy:innov` 为 manual 未触发 | `gkxlumen-platform-entan-py`、`lumen-platform-algo-py`、`lumen-platform-algo-py-worker` 镜像 tag 均 `1847cd9d` Running |
| demo-ui-system-test | `41d757a` | [#4362](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-ui-system-test/-/pipelines/4362) | ✅ success | `deploy:k8s` success | 未单独核 Pod（以 job 为准） |
| demo-algo-ent-analysis | `707edd0` | [#4363](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-algo-ent-analysis/-/pipelines/4363) | ✅ success | `py:smoke`、`deploy:entan-py-api`、`deploy:entan-py-worker` success | `demo-platform-entan-py` 镜像 `gkx-entan-py-api:707edd03` Running；worker `707edd03` Running |

**注意（lumen-algo-py）**：`origin/dev` 之后又有他人提交 `8f60c6e`（`fix(svcan)`，含 `1847cd9`），[Pipeline #4365](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/4365) 写本 handoff 时仍在跑（py:test running）。不属本管线范围；它会滚动 algo pod，请 E1 开跑前确认 #4365 已结束且 `lumen-platform-algo-py` 仍健康，否则 E1 可能撞在滚动窗口。

## 2. 关键：Pod → `gkx` 连通性

做法：`kubectl exec` 进 Pod，在 `/app` 下 `socket.create_connection(183.240.141.251:3318, 8s)`，再直接调用 `polan.eval.effect_macro.macro_effect_card()`（即线上落地实效真实读算路径，只读 `gkx`）。

| Pod（ns `zhipu-tts`） | 镜像 | TCP 183.240.141.251:3318 | `macro_effect_card()` |
|---|---|---|---|
| `gkxlumen-platform-entan-py-59846d749-4zdtt`（**lumen**） | `gkxlumen-entan-py-api:1847cd9d` | ✅ 0.06s | ✅ `computable=True`，深圳 `score=78.5836`，参与指标 8 项 |
| `demo-platform-entan-py-6578fbfd89-nv5bx`（demo） | `gkx-entan-py-api:707edd03` | ✅ 0.07s | ✅ 同上，结果一致 |

- `ext.city_scores`：深圳 78.5836 / 广州 41.101 / 北京 48.5023 / 上海 30.3062 —— 四城不同，满足金路径 #2「分数随城市截面变化，非常量」的数据前提。
- 指标数 8（非 9）：「地区生产总值」仅 2 城有 TB·DNLJ 有效值，`参与城 2 < 3` 被算法按规则剔除，并写入 `proxy_notes`。属口径内行为，不是故障；E1 断言 `indicator_count` 请按 ≥1 / 当前 8，**不要写死 9**。
- Pod 内**未设** `GKX_ODS_MYSQL_*` 环境变量（`env | grep -c` = 0）：走 `settings_policy.yaml` 内置默认 `183.240.141.251:3318 / gkx / gkx_reader_zp`，已实测可读。风险：若日后要改源地址，须走 Secret/env 注入而非依赖 yaml 默认；本次不阻塞。
- 本次核的是 `entan-py` 系 Pod（`vendor/entan-py` 的落点）。`lumen-platform-algo-py` 主 api Pod 未单独 exec（落地实效不经它）。
- 结论：**连通 ✅，金路径不会因网络落「宏观源不可达」。**

## 3. 其他观察（非阻塞）

- `gkxlumen-platform-entan-py-worker` 仍是 `8aa6f57f`（`deploy:entan-worker` 为 manual、未触发）；落地实效在 api 内现查现算，不依赖 worker，不影响 E1。
- `gkxlumen-platform-topic`（Java 老聚合服务）镜像 tag 为 `latest`，本次未动。
- lumen-svc-platform 历史 Pipeline #4354 的 `topic-chain` deploy 与 `sonar:scan` 曾 failed，已被 #4356/#4360 修复，当前绿。

## 4. SSH 使用记录

`user-ssh-executor` 共 5 次业务调用（连接 1 + 命令 4），无探活、无空转：首次 `sudo cp` 因 `$(id -u)` 在 sudo 内展开为 root 导致属主错误（读到 permission denied），改为 `nohup sudo chown` 后恢复，随后一次 `kubectl exec` 取得全部连通证据。收尾已删除跳板机 `/tmp/admin-kc.yaml`、`/tmp/sudocp.log`（已 `ls` 确认不存在）。未在对话/文件中保存凭证。

## 范围与实现（对照 DoD）

| DoD | 结果 |
|---|---|
| 点名相关 K8s/CI deploy 绿（algo-py / platform / topic FE 以实际变更仓为准） | ✅ 见 §1 |
| handoff 含 Pipeline/rollout 证据 | ✅ §1、§2 |
| 关键：algo Pod 可达 `gkx` | ✅ §2 |

## 架构合规自检（00-team-constitution §2）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 未改代码 |
| 2 调用链 | ✅ 未改 |
| 3 Nebula | ✅ 不涉及 |
| 4 可观测 | ✅ 不涉及（effect_macro 自带 span：`policy.effect_macro.load/score`） |
| 5 CI/CD | ✅ push → Pipeline 绿 → K8s dev rollout，均有证据 |
| 6 demo2 只读 merge | ✅ 无 merge |
| 12 D12 | ✅ 仅核验，未改 lumen→demo 依赖 |
| 13 D14 | ✅ 无存储操作 |
| 日常 push 不碰 Nacos | ✅ `deploy:nacos` / `helm:*` manual 未触发 |

## 下游放行建议（E1 `POL-EFFECT-MACRO-E1-QA-L01`）

- 可放行。金路径 #1 期望 `cards.effect.computable=true`、`ext.caliber=macro_outcome_proxy`、深圳当前 ≈ 78.58（会随库更新变，勿硬断言数值，断言 `0 ≤ score ≤ 100` 且非常量）。
- E1 开跑前确认 lumen-algo-py Pipeline #4365 已结束（见 §1 注意）。
- 真 0 分在 FE 已按「分数 0」展示（见 FE handoff），非空态。

## 问题清单 / 遗留风险

- `GKX_ODS_MYSQL_*` 未走 Secret，依赖 yaml 内置凭据默认（仓内既有做法，非本叶引入；建议后续 devops 另立单迁 Secret）。
- lumen-algo-py #4365 正在滚动（他人提交）。

## 成本（回填 registry）

| 字段 | 值 |
|---|---|
| actual_tokens | 约 90000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 0.5 |
| cost_warn | green |
