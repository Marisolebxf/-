# DEVOPS-LUMEN-SVC-CI-SPEED-L01 · lumen-svc-platform CI 增量加速

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
| 说明 | 最小 diff 落地 Phase A；未用 YAGNI 跳过 digest/`git.commit.id` 校验与扇出安全边界；BuildKit/Maven cache 留 Phase C |

## 瓶颈表（对照 pipeline 4735）

证据：`https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4735`  
Commit `65556603` **仅改** `gkxlumen-display/**` 2 文件，却跑了全部日常 package+deploy。

| Job / 阶段 | 大致分钟（4735） | 根因 |
|------------|------------------|------|
| `backend:build` | ~2.5 | 全模块列表 `mvn clean verify -am`（本机 ~/.m2 热时偏短；冷启动更长） |
| `backend:image:*` ×9 日常 | 各 ~0.7–1.3；并行墙钟 ~1.3 | **每服务再** `mvn clean package -pl -am`；无路径 skip |
| `deploy:*` ×9 日常 | 各 ~0.7–2.4；并行墙钟 ~2.4 | 镜像都打了就全自动 set-image；未改服务也滚 |
| `sonar:scan` | ≥14（软门禁） | 另起全量 compile；本单不改 |
| **合计 CPU 分钟** | ~39（含 sonar 进行中） | 单服务改动仍付 9×package + 9×deploy |

**Top3**：① 无路径裁剪的 9 路二次 package；② 未改服务仍 auto deploy；③ build 全量 verify（共享未改时本可 `-pl` 裁剪）。

## 业界对照 → 本仓映射

| 实践 | 本仓落地 |
|------|----------|
| GitLab `rules:changes` + 逃生变量 | Phase A：日常 image/deploy 按服务目录；`REBUILD_ALL`/`FULL_PIPELINE` |
| `needs:optional` | `helm:deploy` 全部 image optional；`e2e:chain-gold` 两侧 deploy optional |
| dotenv / parent-child | Phase A 不用 dotenv 门控（rules 足够）；child pipeline 留 Phase C |
| Maven `-pl -am` + git diff reactor | `scripts/ci-affected-modules.sh --mvn-pl` |
| Maven Build Cache / Develocity | **Phase C**（现 `maven.build.cache.enabled=false`） |
| Docker BuildKit + cache-from | **Phase C**（shell executor、`DOCKER_BUILDKIT=0`） |
| Nx/Turborepo/Bazel affected | 语义对齐：路径→服务图 + 共享扇出；无引入新工具 |
| Google/Spotify monorepo CI | 变更集裁剪 + 强制全量旗标；本仓用 GitLab 原生 rules |

## Phase 方案卡

### Phase A（本单已落地）

- `backend:build`：脚本算 affected `-pl`；无 Java 变更则 skip verify。
- 日常 `backend:image:*` + 对应 `deploy:*`：`rules:changes`；未命中 **skip**（保持现网 digest）。
- 共享路径扇出：`pom.xml` / `gkxlumen-common/**` / `.gitlab-ci.yml` / 相关 scripts。
- `e2e:chain-gold` 仅 chain/async/共享变更时跑。
- 逃生：`REBUILD_ALL=true`（日常全量）、`FULL_PIPELINE=true`（含冷门）。

### Phase B（后续）

- api/biz 细粒度依赖扇出表；父 POM 属性变更策略文档化。
- 冷门服务也可按路径手动触发（保留 FULL 门）。

### Phase C（可选）

- 评估 Maven build cache / BuildKit；跨 job 传 class 须避开 artifact 413。

## 安全边界

1. 跳过 package ⇒ 必须跳过 deploy（同 rules）；禁止把旧镜像标成新 commit。
2. 实际 package 仍校验 jar 内 `git.commit.id == CI_COMMIT_SHA`。
3. 公共依赖变更必须扇出全部日常服务。
4. topic-chain / topic-async-service：路径命中时仍 origin/dev 自动 deploy（长任务规约不变）。

## 已改文件

- `repos/lumen-svc-platform/.gitlab-ci.yml`
- `repos/lumen-svc-platform/scripts/ci-affected-modules.sh`（含 `--self-check`）
- `gkx-orchestration/agent-delivery/cicd-pipeline.md`（lumen-svc-platform 增量段）

## 自检

- `bash scripts/ci-affected-modules.sh --self-check` → OK（Git Bash）。
- 本地模拟 4735：`CI_COMMIT_BEFORE_SHA`+仅 display 文件 → `--mvn-pl`=`gkxlumen-display`；`--services`=`display`。
- **本单 push 自身**含 `.gitlab-ci.yml` → 会触发共享扇出（预期一次全量日常）；之后单服务 push 才见加速。

## 预期加速比

| 场景 | 改造前（墙钟粗估） | 改造后（墙钟粗估） | 加速 |
|------|-------------------|-------------------|------|
| 单服务改动（如 4735 display-only） | build 2.5 + pkg~1.3 + deploy~2.4 ≈ **6–8min**（+9 路 CPU） | build~1 + 1×pkg~1 + 1×deploy~2 ≈ **3–4min**；CPU 约 **-80%** package/deploy | 墙钟 ~**2×**；CPU ~**5–8×** |
| 共享/CI 扇出或 `REBUILD_ALL` | 同改造前 | 同改造前 | ~1× |
| 仅 helm | 仍打满日常镜像 | image/deploy skip | 大 |

## 风险与回滚

| 风险 | 缓解 |
|------|------|
| `GIT_DEPTH` 过浅 → before SHA 缺失 | 提到 50；脚本遇缺失 **保守全量** |
| rules YAML 解析/嵌套 alias | 扁平 rules + `changes: *changes_shared_paths`；已 pyyaml 解析 |
| CI 改动首次全扇出 | 预期；后续单模块才加速 |
| 高风险 CI | **建议监管人看一眼 pipeline 再依赖**；回滚：`REBUILD_ALL=true` 或 revert CI commit |

回滚命令：对 `lumen-svc-platform` revert 本单 CI commit，或 Run pipeline 设 `REBUILD_ALL=true`。

## CI/CD

- 分支：`origin/dev`
- 仓：`lumen-svc-platform` commit `a606e62` + orchestration 文档
- pipeline（本单落地）：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4739 （CI 文件变更 → 共享扇出，日常常发全跑为预期）
- 对照慢流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4735 （display-only 却 9 路 package）
- Nacos：未触碰；未设 `FORCE_NACOS_REPUBLISH`

## 待监管人确认

1. Phase A 路径规则 + 扇出列表是否接受。
2. 本单 push 后首次 pipeline（CI 文件扇出）是否需盯一眼 job 图：应只见日常常发，冷门仍 FULL-only。
3. Phase B/C 是否排期（Maven cache / BuildKit）。
