# DEVOPS-LUMEN-ALGO-CI-SPEED-L01 · lumen-algo-py CI 路径增量加速

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最小 diff 落地 Phase A（rules:changes + 可选脚本）；未用 YAGNI 跳过共享扇出、api Dockerfile 交叉 COPY（chainan/polan）、长任务 E0（api+worker 命中仍自动）与 D12 entan-api 自动；BuildKit/缩 py:test 留后续 |

## 瓶颈表（对照 pipeline 4751）

证据：`https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/4751`  
Commit `ad518403`（entan `polan` + seed 脚本）；改造前仍固定跑满 5 路 image。

| Job / 阶段 | 大致分钟（4751） | 根因 |
|------------|------------------|------|
| `py:test` | ~4.0 | docker 内 pip + compileall + pytest（ignore vendor）；**每条 pipeline 必跑** |
| `image:*` ×5 | 各 ~0.06–0.08；合计 CPU ~0.4；并行墙钟 ~0.1 | runner 层缓存热时偏短；**无路径 skip**，未改 innov 也 package |
| `deploy:api/worker/entan-api` | 各 ~0.2–1.3+（rollout+healthz） | 镜像都打了就自动 set-image；未改制品也滚 |
| `sonar:scan` | ~0.3（软门禁） | 本单不改 |
| **合计** | 墙钟 ≈ py:test 4 + package/deploy ~1–3 ≈ **5–7min** | 单制品改动仍付 5×package + 多路 deploy |

**Top3**：① `py:test` 全量墙钟主导；② 无路径裁剪的 5 路 docker package；③ 未改制品仍 auto deploy（含 innov 空跑 package）。

近 8 条 dev pipeline：`py:test` 稳定 ~242–253s；`image` 合计 ~18–28s（缓存热）；deploy 成功合计 ~26–66s。

## 路径 → 制品映射

| 制品 | 自身路径 | 交叉 / 共享 |
|------|----------|-------------|
| **api** | `lumen_algo_service/**`、`docker/Dockerfile.api`、`k8s/api.yaml` | `vendor/innov-py/chainan/**`、`vendor/innov-py/conf/settings.yaml`、`vendor/entan-py/polan/**`（Dockerfile COPY） |
| **worker** | `lumen_algo_worker/**`、`docker/Dockerfile.worker`、`k8s/worker.yaml` | `vendor/entan-py/polan/**` |
| **innov** | `vendor/innov-py/**`、`docker/Dockerfile.innov` | `lumen_common/**`（Dockerfile COPY） |
| **entan-api** | `vendor/entan-py/**`、`docker/Dockerfile.entan-api` | 日常自动 |
| **entan-worker** | `vendor/entan-py/**`、`docker/Dockerfile.entan-worker` | 镜像路径命中；deploy 默认 manual |
| **共享扇出** | `lumen_common/**`、`requirements.txt`、`conf/**`、`.gitlab-ci.yml`、`scripts/ci-affected-paths.sh` | → 日常自动 **api+worker+entan-api**；innov/entan-worker **镜像**亦随共享重建，deploy 仍 manual / FULL |

## Phase 方案卡

### Phase A（本单已落地）

- 日常 `image:api|worker|entan-api` + 对应 `deploy:*`：`rules:changes`；未命中 **skip**（保持现网 digest）。
- `image:innov|entan-worker`：路径 / 共享 / FULL / tag|release；`deploy`：FULL 自动，否则路径命中 **manual**。
- 共享路径扇出日常三件套；逃生：`REBUILD_ALL=true`（日常全量）、`FULL_PIPELINE=true`（含 innov/entan-worker 自动）。
- `e2e:chain-gold` / `smoke:synth-routes`：同 changes + `needs:optional`。
- `py:test`：**保留全量**（缩 scope 有漏测风险）。
- 对照脚本：`scripts/ci-affected-paths.sh`（`--self-check` / `--images` / `--daily`）。
- `GIT_DEPTH`：20 → **50**。

### Phase B/C（未本单）

- py:test 按变更缩 compileall/pytest 范围（需风险评审）。
- Docker BuildKit + cache-from（现 `DOCKER_BUILDKIT=0`）。

## 安全边界

1. 跳过 package ⇒ 必须跳过 deploy（同 rules）；禁止把旧镜像标成新 commit。
2. 公共 / CI 变更扇出日常自动制品。
3. api+worker（及 entan-api）路径命中时 origin/dev **仍自动** deploy（长任务 E0 / D12）。
4. api Dockerfile 交叉依赖（chainan/polan）写入 changes，避免漏重建。

## 已改文件

- `repos/lumen-algo-py/.gitlab-ci.yml`
- `repos/lumen-algo-py/scripts/ci-affected-paths.sh`
- `gkx-orchestration/agent-delivery/cicd-pipeline.md`（lumen-algo-py 增量段）
- `gkx-orchestration/agent-delivery/agent-handoffs/平台基建-PLATFORM/DEVOPS-LUMEN-ALGO-CI-SPEED-L01.md`

## 自检

- `bash scripts/ci-affected-paths.sh --self-check` → OK（Git Bash）。
- 本地模拟 HEAD（`ad51840` polan）：`--images`=`api worker entan-api entan-worker`；`--daily`=`api worker entan-api`（innov 正确略过）。
- 模拟 `lumen_algo_service/main.py` only → `api`。
- YAML：`pyyaml.safe_load(.gitlab-ci.yml)` → OK。
- **本单 push 自身**含 `.gitlab-ci.yml` → 共享扇出（预期一次日常三件套 + innov/entan-worker 镜像因共享路径）；之后单制品 push 才见加速。

## 预期加速比

| 场景 | 改造前 | 改造后 | 加速 |
|------|--------|--------|------|
| 单制品（如仅 `lumen_algo_service`） | py:test 4 + 5×image + 3×auto deploy | py:test 4 + 1×image + 1×deploy；innov/entan skip | package/deploy CPU ~**3–5×**；墙钟在缓存热时 ~**1.2–1.5×**（py:test 仍主导） |
| 仅 `vendor/innov-py` | 5×image + 日常三路 deploy | innov image + deploy manual；日常 deploy **skip** | 避免无谓 rollout |
| 共享 / CI / `REBUILD_ALL` | 同改造前日常 | 同改造前日常 | ~1× |
| 本单首次 push（改 CI） | — | 共享扇出全量日常 | 预期，非加速证据 |

## 风险与回滚

| 风险 | 缓解 |
|------|------|
| `GIT_DEPTH` / changes 漏判 | 提到 50；漏了用 `REBUILD_ALL=true` |
| 交叉 COPY 路径漏列 | Dockerfile 已对照写入 chainan/polan；handoff 映射表 |
| CI 改动首次全扇出 | 预期；后续单模块才加速 |
| 高风险 CI | **建议监管人看一眼 pipeline job 图**；回滚：revert CI commit 或 Run pipeline `REBUILD_ALL=true` |

回滚：对 `lumen-algo-py` revert 本单 CI commit，或新建 pipeline 设 `REBUILD_ALL=true` / `FULL_PIPELINE=true`。

## CI/CD

- 分支：`origin/dev`
- 仓：`lumen-algo-py` commit `2fa8234`
- 本单落地 pipeline：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/4754 （CI 文件变更 → 共享扇出，日常三件套全跑为预期）
- 对照基线流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/4751
- Nacos：未触碰；未设 `FORCE_NACOS_REPUBLISH`；未改业务算法逻辑

## 待监管人确认

1. Phase A 路径规则 + 交叉 COPY 扇出（polan→api/worker）是否接受。
2. 本单 push 后首次 pipeline（CI 文件扇出）是否需盯一眼：应见日常三件套自动；innov/entan-worker 镜像因共享可能重建但 deploy 仍 manual（非 FULL）。
3. `py:test` 保持全量是否接受（Phase B 再议缩 scope）。
4. 真正「单制品加速」证据：后续只改 `lumen_algo_service/**` 的业务 commit 验证 job 图。
