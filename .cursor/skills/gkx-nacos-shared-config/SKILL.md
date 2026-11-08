---
name: gkx-nacos-shared-config
description: >
  Change a Nacos shared config (application-{profile}.yml) for GKX lumen Java
  services and make it actually take effect, not just "发布". Covers: shared vs
  per-service decision, verifying spring.config.import, publishing, deciding
  whether a pod restart is required, image-cache traps, and log-based verification.
  Use when a Nacos config "已发布但不生效", when one setting (sso / datasource /
  redis / 白名单) must reach many lumen modules at once, or when a lumen resource
  server returns 401 访问令牌不存在 / sso check-token failed. Also the mandatory
  path for ANY lumen Nacos change (改 Nacos 配置, 改网关路由, 加配置项,
  FORCE_NACOS_REPUBLISH, helm configs/*.yml) — see rule nacos-config-change.mdc.
---

> **规约**（`.cursor/rules/nacos-config-change.mdc`，2026-11-07）：日常 push 不重发 Nacos；任何 lumen Nacos 改动都走本 skill §2「模板 + 单发」流程；密钥用 `@@NAME@@` + Secret。

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
| 仓库 `helm/gkxlumen-platform/configs/*.yml` | 无（模板，**线上真源**） | 必须与线上逐份一致。push 不会同步；按 §2 单个 dataId 发布。`FORCE_NACOS_REPUBLISH=true` 会整批覆盖 14 个 dataId，仅在确认一致且用户批准后用 |

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

## 2. 发布（模板 + 单发，缺一不算完成）

执行前须当次会话用户批准（线上变更）。

1. **先取线上原文对比模板**：发布前拉当前 dataId 内容，与仓库 `configs/<dataId>` 比对（忽略换行符）。不一致先查清是谁改的，不要直接覆盖。
2. **改模板并提交**：在 `lumen-svc-platform/helm/gkxlumen-platform/configs/<dataId>` 改，commit 带 `[agent:<role>]`。
   - 密钥写 `@@NAME@@`（大写/数字/下划线，不加引号），真实值放 Secret `zhipu-tts/gkxlumen-platform-nacos-config-secrets` 同名 key。新占位符先补 Secret（`kubectl patch`/`create`，不打印值）。
   - 已是 `${ENV:默认}` 的 Spring 占位符保持原样。
3. **单个 dataId 发布**：在 nacos pod 内 `POST /nacos/v1/auth/users/login` 拿 accessToken → 用 Secret 值替换 `@@NAME@@`（任一缺值则不发）→ `POST /nacos/v3/admin/cs/config`（`dataId`、`groupName=DEFAULT_GROUP`、`namespaceId=public`、`type=yaml`）。只发 `public` 一次即可（`""` 会归一到 `public`）。
4. **核对**：返回 `code=0`；历史版本新增一条；线上内容重新脱敏后 == 仓库文件。
5. 发布前后的含密钥临时文件用完即删，并 `ls` 确认。

禁止：
- 用 `FORCE_NACOS_REPUBLISH=true` 跑 `helm:chart` 代替单发（会整批覆盖 14 个 dataId；2026-11-07 事故即由此引发）。
- 只改控制台不改模板，或只改模板不发线上。
- 把真实密钥写进模板、commit、handoff 或聊天输出。

回滚：Nacos `U` 历史存的是**修改前**内容，同一时刻两条历史取 id 较小的一条即事故前版本；`GET /nacos/v3/admin/cs/history?nid=<id>&dataId=..&groupName=DEFAULT_GROUP&namespaceId=public` 取原文后按第 3 步整份发布。

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
- 模板里 `client-secret` 写 `@@SSO_TOPIC_CLIENT_SECRET@@` / `@@SSO_DISPLAY_CLIENT_SECRET@@`，真实值只在 Secret 与 Nacos

## 7. 沉淀 checklist

- [ ] 已获当次会话用户批准；没有用 `FORCE_NACOS_REPUBLISH=true` 代替单发
- [ ] 模板已同步提交，密钥为 `@@NAME@@` 且 Secret 已有同名 key
- [ ] 确认目标服务 import 了共享配置
- [ ] 值确实所有服务通用，且私有 dataId 没有同名 key 覆盖
- [ ] 发布后确认版本递增
- [ ] 先用 `/actuator/configprops` 验证绑定，**不要默认要重启**
- [ ] 验证看日志判据，不只盯 HTTP 码
- [ ] 若"配置对但无效"，按 jar **内容**（非版本号）确认类是否存在
- [ ] 确认 deployment 用 digest 而非 `:latest`
