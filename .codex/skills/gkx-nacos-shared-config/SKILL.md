---
name: gkx-nacos-shared-config
description: >
  Change a Nacos shared config (application-{profile}.yml) for GKX lumen Java
  services and make it actually take effect, not just "发布". Covers: shared vs
  per-service decision, verifying spring.config.import, publishing, deciding
  whether a pod restart is required, image-cache traps, and log-based verification.
  Use when a Nacos config "已发布但不生效", when one setting (sso / datasource /
  redis / 白名单) must reach many lumen modules at once, or when a lumen resource
  server returns 401 访问令牌不存在 / sso check-token failed.
---

# GKX Nacos 共享配置变更与生效

改 Nacos 配置不是终点。**"发布成功" ≠ "服务生效"**，本 skill 的价值在于把最后这段链路走通并留下证据。

## 何时用

- 一个配置要同时作用于多个 lumen Java 服务（`sso:`、`datasource`、`redis`、`security.oauth2.client.*`）
- 用户说「Nacos 已经改了/发布了，但接口还是老行为」
- 资源服务返回 `401 访问令牌不存在` + `data` 里带 `sso check-token failed`
- 需要判断「改完到底要不要重启 pod」

只管单个服务内部的业务开关、或改的是代码逻辑 → 不是本 skill。

## 0. 先分清配置落在哪一层

| 位置 | 作用范围 | 说明 |
|---|---|---|
| Nacos `application-{profile}.yml` | **所有** import 了它的 lumen Java 服务 | 共享层，改一处全覆盖 |
| Nacos `{spring.application.name}-{profile}.yml` | 单服务 | **私有层优先级高于共享层**，会覆盖同 key |
| 仓库 `helm/gkxlumen-platform/configs/*.yml` | 无（模板） | 默认**不会**自动同步到 Nacos；需 `FORCE_NACOS_REPUBLISH=true` 重跑 `helm:chart`，紧急时直接改 Nacos 控制台 |

> 判断依据：值是否"所有服务都一样"。一样的放共享，服务的端口/库名/业务开关放私有。

## 1. 确认目标服务真的加载了共享配置

每个服务 `src/main/resources/application.yml`（Spring Boot 3 无 bootstrap.yml）：

```yaml
spring:
  config:
    import:
      - optional:nacos:application-@profiles.active@.yml              # 共享
      - optional:nacos:${spring.application.name}-@profiles.active@.yml  # 私有
```

`@profiles.active@` 由 Maven 打包时替换成 `dev`。**没有第一行的服务，改共享配置对它无效**，必须写进它自己的私有 dataId 或先补 import。

## 2. 发布

- 控制台：`http://<nacos-host>:8848`，默认 `nacos/nacos`
- 只**追加**，不要覆盖原有 YAML 块；发布后确认历史版本号递增
- Nacos 3.x 的 v1 写接口已废弃，脚本化时用 `POST /nacos/v1/auth/login` 拿 accessToken 再调 v2/v3 admin API

## 3. 判断"要不要重启"（最容易踩的一步）

| Bean 形态 | 生效方式 |
|---|---|
| `@RefreshScope` | Nacos 推送后自动生效 |
| 普通 `@ConfigurationProperties` | 依赖 Spring Cloud `ConfigurationPropertiesRebinder` 重绑，**可能**自动生效但不可靠 |
| 启动期一次性装配的 Bean（`SecurityFilterChain`、`DataSource`、`RestTemplate` 拦截器、`@Bean` 里被构造参数快照掉的值） | **必须重启** |

结论：**先验证，不生效再重启**。不要一上来全量重启（服务多、重启慢、还会打断在跑的任务）。

> **实测修正（2026-10-22，zhipu-tts）**：给共享 `application-dev.yml` 追加 `sso:` 后，
> 7 个资源服务（topic-enterprise / topic-svc / topic-policy / topic-chain / topic-async-service
> / innov / metrics）在 **pod 已运行 44h、完全未重启** 的情况下全部自动绑上了新配置。
> 即普通 `@ConfigurationProperties` 在本仓是**可以热生效**的，"必须重启"属于过度操作。

**验证配置有没有绑上（不用重启、不用发业务请求）**

```bash
# 在 pod 内直接问 actuator：configprops 里出现该 @ConfigurationProperties 的 Bean 名即为已注册
sudo kubectl -n <ns> exec <pod> -- sh -c \
  'curl -s --max-time 5 http://localhost:<port>/actuator/configprops | grep -o "SsoProperties"'

# 业务实例按前缀命中才是真的绑定成功（比 Bean 名更强）
sudo kubectl -n <ns> exec <pod> -- sh -c \
  'curl -s --max-time 5 http://localhost:<port>/actuator/configprops' | grep -o '"prefix":"sso"[^}]*'
```

无输出 = Bean 未注册 → 优先怀疑 jar 里没这个类（见 §5），而不是"配置没发布"。

## 4. 验证顺序

1. 看服务日志里配置是否被读到/绑定（见 §6 案例的两条判据日志）
2. 直接打接口复现原请求（带同样的 header / token）
3. 仍失败 → `rollout restart` 再验一遍
4. 重启后仍失败 → **不是配置问题**，往代码层/镜像层查（§5）

```bash
# 批量重启（按 deploy 名，不要用通配符猜 pod 名）
sudo kubectl -n <ns> rollout restart deploy <svc1> <svc2> ...
sudo kubectl -n <ns> get pods | grep -E '<svc1>|<svc2>'
```

## 5. 镜像缓存陷阱（本项目已实测踩过）

Deployment 写 `image: repo:latest` + `imagePullPolicy: IfNotPresent` → 节点复用旧镜像，**Nacos 配置补好了，jar 里却没有消费该配置的类**，表现为"配置白加"。

```bash
# 确认运行镜像里有没有目标类
sudo kubectl -n <ns> exec <pod> -- sh -c 'jar tf /<app-dir>/<app>.jar | grep -i <ClassName>'
# 确认 deployment 与 pod 实际 digest
sudo kubectl -n <ns> get deploy <svc> -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
sudo kubectl -n <ns> get pod <pod> -o jsonpath='{.status.containerStatuses[0].imageID}{"\n"}'
```

⚠️ **版本号相同 ≠ 内容相同**：同名 `gkxlumen-common-security-5.12.0.jar` 存在新旧两版，
新版才有 `SsoProperties` / `SsoTokenChecker`。必须按 **jar 内容**校验，不能只看版本号：

```bash
# 嵌套 jar 不会被外层 `jar tf` 展开，需要先解出来
sudo kubectl -n <ns> exec <pod> -- sh -c \
 'cd /tmp && rm -rf q && mkdir q && cd q &&
  unzip -o -q /<app-dir>/<app>.jar "BOOT-INF/lib/gkxlumen-common-security-5.12.0.jar" &&
  unzip -l BOOT-INF/lib/gkxlumen-common-security-5.12.0.jar | grep -c SsoProperties'
# 0 = 旧包，需升级镜像；2（含 $App）= 新包
```

实例：`gkxlumen-platform-topic`（base）与 `gkxlumen-platform-cms` 就是这个坑——jar 名为 5.12.0 但没有 SSO 类，共享配置对它们完全无效。

修复：用 **digest** 固化，而不是 `:latest`

```bash
sudo kubectl -n <ns> set image deploy/<svc> <container>=<repo>@sha256:<digest>
sudo kubectl -n <ns> rollout status deploy/<svc>
```

## 6. 案例：`sso:` 只配在 upms → 其他资源服务全 401

**现象**

| 接口 | 结果 |
|---|---|
| `/admin/get-permission-info`（→ upms） | 200 |
| `/enterprise/topic/v1/filter-template/list`（→ topic-enterprise） | `401 {"msg":"访问令牌不存在","data":"sso check-token failed"}` |

**机制**（`gkxlumen-common-security`）

- `SsoProperties.enabled` 默认 `true` → 所有资源服务默认走 SSO 分支
- `GkxlumenCustomOpaqueTokenIntrospector.introspectViaSso()` 读请求头 `systemCode` → `SsoTokenChecker.check(token, systemCode)`
- `SsoTokenChecker.check()` 先 `props.findByCode(systemCode)`
  - 未命中 → `log.warn("sso introspect: unknown systemCode={}")` → 返回 null
  - 命中但用户中心返回非 0 → `log.warn("sso check-token non-zero: code={} msg={}")` → 返回 null
- 两条路径最终都抛 `InvalidBearerTokenException("sso check-token failed")`

**关键判据：HTTP 响应完全一样，只能看服务端日志区分**

| 日志 | 含义 | 处置 |
|---|---|---|
| `sso introspect: unknown systemCode=topic` | 该服务 `apps[]` 里没有 `topic` → **配置缺失** | 补 `sso.apps` |
| `sso check-token non-zero: code=401 msg=访问令牌已过期` | 配置正确，链路已通 → **token 本身无效** | 换合法 token，不是改配置 |
| 没有 `sso check-token >>>` 那行 | 根本没进 SSO 分支 | 查 jar 版本 / `sso.enabled` |

**修复**：把完整 `sso:` 块放到共享 `application-dev.yml`（upms 私有层已有的内容），避免逐服务重复配置。

```yaml
sso:
  enabled: true
  user-center-url: https://edu.itic-sci.com/uc
  tenant-id: "1"
  apps:
    - code: topic
      name: 科技专题系统
      client-id: <topic 的 clientId>
      client-secret: <topic 的 clientSecret>
    - code: display
      name: 科技展示系统
      client-id: <display 的 clientId>
      client-secret: <display 的 clientSecret>
```

注意：
- 请求头 `systemCode` 缺失时 `findByCode(null)` 同样返回 null，表现为 `unknown systemCode=null`
- 密钥不要写进仓库模板，只落 Nacos

## 7. 沉淀 checklist

- [ ] 确认目标服务 import 了共享配置
- [ ] 值确实所有服务通用，且私有 dataId 没有同名 key 覆盖
- [ ] 发布后确认版本递增
- [ ] 先用 `/actuator/configprops` 验证绑定，**不要默认要重启**
- [ ] 验证看日志判据，不只盯 HTTP 码
- [ ] 若"配置对但无效"，按 jar **内容**（非版本号）确认类是否存在
- [ ] 确认 deployment 用 digest 而非 `:latest`
