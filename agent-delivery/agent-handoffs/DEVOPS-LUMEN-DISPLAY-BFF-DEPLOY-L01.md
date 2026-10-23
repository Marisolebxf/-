# DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01 · gkxlumen-display 展示聚合 BFF — 部署层四件套 + 首次部署上线（D15 唯一对外面）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent`（架构会话代行，授权来源 human:李伟 会话指令：先补齐部署层四件套 → 提交 → 执行首次部署） |
| supervised_by | `human:李伟` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 chart 微服务模板零新模板；仅 values/路由/种子/CI 清单四类声明式改动 + 一次临时清理 job；未加未请求的抽象 |

## 任务背景

D15 架构决策（展示系统 Python 门面独立 + 展示聚合 BFF）下，`gkxlumen-display` 代码骨架已于前序会话落地（编译三绿）。本单把该服务推到 dev 集群跑起来：补齐部署层四件套 → 人工验收通过后提交 → 执行首次部署并做端到端链路验证。三层调用链铁律：前端 → 网关(/display/**) → gkxlumen-display(:7099, /v1/**) → Feign {innov|topic|metrics} → Python。

## 修改内容（lumen-svc-platform，提交链 5 条全推 origin/dev）

| commit | 内容 |
|--------|------|
| `235fdda` | **部署层四件套**：① `values.yaml` display 段（enabled:false 默认，port 7099，waitForInfra，资源 100m/256Mi~500m/768Mi）；② `values-lumen.yaml` 启用 display + 头注释路由表补 `/display/**` 行；③ `configs/gkxlumen-gateway-dev.yml` 加 display 路由（无 StripPrefix，全局过滤器统一剥第一段）；④ `configs/gkxlumen-display-dev.yml` 最小 Nacos 种子（全注释 + 预留 aggregate/cache 配置位）；`.gitlab-ci.yml` 三处（`-pl` 清单、`backend:image:display`、`deploy:display`）；`DEPLOY-LUMEN.md` 服务清单补行 |
| `77f227a` | 修 `backend:image:topic-policy` 自依赖（`needs` 指向自己 → pipeline 创建即 failed 且 0 jobs，GitLab lint API 定位） |
| `3fa06d1` | `values-lumen.yaml` display 段**整表写全**——helm `--reuse-values` 下 chart values.yaml 默认值不参与合并，缺省 image.repository 为空 → Pod InvalidImageName（`harbor.test.com/zp-tts/:latest`） |
| `0271cd6` | 一次性 `ops:cleanup-display` job（删端口错建期的孤儿 Service/Deployment；K8s strategic merge 对 Service ports 数组按 port 追加同名 `http` 端口导致 patch 失败） |
| `2bc11e8` | `values-lumen.yaml` 显式 `nacosConfigInit.runOnUpgrade: false`——早期一次性 `--set` 已持久化进 release values，`--reuse-values` 每次带回 → post-upgrade hook Job（curlimages/curl 节点拉不到 docker.io）反复超时 → UPGRADE FAILED 死循环 |

## 部署过程（含三次故障定位与修复）

1. 首次 helm:chart：display Pod InvalidImageName → 定位 `--reuse-values` 合并语义（chart 默认值不参与）→ `3fa06d1` 整表补全
2. 二次 helm:chart：Service ports Duplicate `http` → strategic merge 按 port 追加 → `0271cd6` 清孤儿资源重建
3. 三次 helm:chart：hook 反复失败 → 定位 `--set` 持久化 + reuse 带回 → `2bc11e8` 显式压制 → **success**

Nacos 配置灌入因节点无法拉取 docker.io 的 curl 镜像、init hook 不可用，改走 **Nacos 3 console API 手动双 tenant 直灌**（空串 + 字面量 "public"，对齐 helm init job 行为）：`gkxlumen-display-dev.yml` 新建 + `gkxlumen-gateway-dev.yml` 原文追加 display 路由（json.load 抽 content 保证 RewritePath 行字节保真）。

## 验收证据（2026-10-22）

| 证据 | 值 |
|------|-----|
| Pipeline | [#2760](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/2760)（sha=2bc11e8），helm:lint #15006 success |
| helm:chart | job **#15022 success**，release `gkxlumen-platform` **STATUS: deployed** |
| 镜像 | `harbor.test.com/zp-tts/gkxlumen-display:latest`（backend:image:display success，trivy 过） |
| Pod | `gkxlumen-platform-display-*/`**`1/1 Running`**，ClusterIP `10.96.1.87:7099/TCP` |
| Nacos | 双 tenant 各 2 条：gateway-dev.yml（md5 `ca3a3d83`，双端一致，含 display 路由）+ display-dev.yml（id=33） |
| 网关热刷新 | `actuator/gateway/routes` 24 → **25 条**，`gkxlumen-display (Paths: [/display/**])` 在列，秒级生效未重启 |
| **端到端** | `http://10.50.69.111:30895/display/actuator/health` → `{"status":"UP"}`，discoveryClient 确认 display 已注册 Nacos（与 innov/topic/metrics 同注册表） |
| 路由匹配证明 | 垃圾路径 `/no-such-route-zzz/xxx` → 404；`/display/v1/aggregations/health` → 401（鉴权过滤器仅对匹配路由生效）→ 路由真匹配 |

> 业务端点 `/display/v1/**` 返回 401「访问令牌不存在」为平台统一安全基线（与 innov/metrics 一致），前端带业务 token 即通；免鉴权的 actuator 探活已证明 网关 → StripPrefix=1（全局过滤器）→ lb://gkxlumen-display 全链路。

## 架构合规自检（公约铁律逐条）

| 铁律 | 结果 |
|------|------|
| D15 三层调用链 | ✅ 网关唯一对外面 /display/** → display:7099 /v1/** → Feign 域服务；前端禁直连 innov/topic/metrics |
| 只读边界 | ✅ display 骨架只读聚合，不连业务库、不做算法 |
| 复用不新增 | ✅ 复用 microservices 通用模板，零新 Helm 模板；配置走既有 configs/ 灌入机制 |
| demo/lumen 隔离 | ✅ 资源前缀 gkxlumen-platform-*；未触碰 demo NodePort/Secret |
| CI/CD push→绿→K8s | ✅ pipeline 2760 lint 绿 + helm:chart success + rollout 完成 |
| 可观测 | ✅ OTEL_SERVICE_NAME=gkxlumen-display，走平台统一 collector |

## 遗留风险 / 后续

1. ~~`ops:cleanup-display` 临时 job~~ → 已替换为 `ops:cleanup-nacos-hook`（f0c99cf）执行孤儿 hook 清理（pipeline #2764 job #15081 success），临时 job 已随 ec1deea 移除，**CI 零遗留**
2. ~~孤儿 hook pod（ImagePullBackOff）~~ → 已删除，集群无残留
3. `configs/gkxlumen-gateway-dev.yml` 是**初始种子**性质：集群 Nacos 现存内容以手动灌入版为准（含 openapi + display 两条）；后续路由变更走 FORCE_NACOS_REPUBLISH 或 Nacos 控制台/API，注意种子与 Nacos 实际内容会漂移
4. CODEOWNERS 展示侧组名占位待 human:李伟 提供；需知会徐滕强 display 新模块与 show-py 部署边界
5. 后续接线：innov 启动类补 `@EnableGkxlumenFeignClients`、ShowPythonFeignConfig 热切换、M1–M9 业务聚合端点回填（W1 里程碑）、display 读缓存/分区降级参数在 Nacos 种子预留位启用

## 涉及文件（lumen-svc-platform）

- `helm/gkxlumen-platform/values.yaml` `values-lumen.yaml`
- `helm/gkxlumen-platform/configs/gkxlumen-gateway-dev.yml` `configs/gkxlumen-display-dev.yml`（新增）
- `helm/gkxlumen-platform/DEPLOY-LUMEN.md`
- `.gitlab-ci.yml`（-pl 清单 / image job / deploy job / ops:cleanup-display）
- `gkxlumen-display/`（骨架，前序会话 `235fdda` 一并入库）

---

*devops-agent · DEVOPS-LUMEN-DISPLAY-BFF-DEPLOY-L01 · 2026-10-22*
