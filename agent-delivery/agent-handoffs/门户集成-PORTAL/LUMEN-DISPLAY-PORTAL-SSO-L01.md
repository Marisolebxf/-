# LUMEN-DISPLAY-PORTAL-IFRAME-L01 · 独立打开走统一用户中心授权码登录

> **状态**：代码已推 `origin/dev`，待联调 · **监管**：human:孔东 · **执行**：agent:frontend-agent / agent:api-agent
> **强度**：ponytail full
> **说明**：本叶补独立打开（非 iframe）的授权码登录。iframe 嵌入认证仍以 `LUMEN-DISPLAY-PORTAL-IFRAME-L01.md` 为准。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东`（registry 原认领）；本叶代码由 agent 按该任务续做 |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 未改 registry 状态。任务当前仍为 `integration`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用已有 upms SSO 客户端与前端 token 存储，未新造登录体系。未跳过调用链与可观测头。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无（本叶不改架构图） |
| 图 diff | 无 |
| 会签态 | 无 |
| 说明 | 登录仍是前端 → 网关 `/admin/*` → upms → 统一用户中心。 |

## 问题清单

- 独立打开、`VITE_ENABLE_MOCK_AUTH=false`、且需要登录时，应跳统一用户中心，并用回调 `code` 换 token。
- 展示与专题的用户中心接口应共用 Java，按 `systemCode` 取 Nacos 客户端凭证。

## 修改内容

- Java（`lumen-svc-platform`，展示 `display` 与专题 `topic` 共用）：
  - `GET /admin/sso/authorize-url`：按 1.1 参数（`response_type=code`、Nacos `client_id`、前端 `redirect_uri`）拼 `{userCenterUrl}/sso/login`。文档中的 `POST /authorize` 由用户中心在登录页内调用，三方跳转前没有用户 Bearer，故不直调该 POST。
  - `POST /admin/sso/token`：1.2 `authorization_code`，Basic Auth 与 `get-permission-info` 相同。`access_token` 原样返回，后续仍走现有 1.3 `check-token`，不写入 pigX 令牌库。
  - 两接口 `@Inner(false)`，登录前匿名可调。
- 前端（`lumen-ui-science-pc`）：
  - `VITE_SSO_CALLBACK_URL=https://edu.itic-sci.com/tid/?callback=true`
  - 非 iframe 且 `VITE_ENABLE_MOCK_AUTH` 不是 `true`：未登录或登录失效时取登录地址并整页跳转；回调带 `code` 时换 token，写入现有 `localStorage` 键 `access_token`。
  - iframe 与 Mock 登录路径不变。
- `lumen-ui-topic` 已按同一套改本地工作区（回调 `https://edu.itic-sci.com/tts/svcz/?callback=true`），**本次未 commit / 未 push**。

## 测试结果

- `node src/utils/ssoCallback.selfcheck.mjs`（science-pc）：通过
- `pnpm exec vue-tsc --build`（science-pc）：通过
- Java：本机无 `mvn`，未编译
- 浏览器未走通真实统一用户中心跳转（当前环境 `VITE_ENABLE_MOCK_AUTH` 仍为 `true`，该开关为 true 时不进入这套跳转）

## 遗留风险

- 两个前端的 `VITE_ENABLE_MOCK_AUTH` 仍是 `true`，授权码跳转不会发生。启用须改为 `false`，且用户中心已登记对应 `redirect_uri`。
- 专题回调按公网前缀写成 `/tts/svcz/?callback=true`，须在 topic 客户端登记；专题前端代码还在本地。
- 网关若对 `/admin/**` 另有匿名白名单，需放行 `/admin/sso/authorize-url` 与 `/admin/sso/token`。仓内网关配置未见单独鉴权过滤器，放行靠 upms `@Inner(false)`。

## CI/CD（必填）

- 分支：`dev`
- commit：
  - `lumen-ui-science-pc` `4161753` feat(auth): 独立打开时走统一用户中心授权码登录
  - `lumen-svc-platform` `5bd0f87` feat(sso): 提供授权码登录地址与 code 换票（rebase 后；原本地 `e5daa4f`）
- pipeline URL / ID：push 后由 GitLab 触发，提交时未知
- 部署 namespace / 镜像 tag：未在本叶确认
- K8s rollout：未在本叶确认
- dev 测试 URL / 命令与结果：未做线上登录走查

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 upms / 网关既有服务名，本叶未改
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `repos/lumen-svc-platform`：`SsoCenterClient.java`、`SysSsoCenterController.java`
- `repos/lumen-ui-science-pc`：`.env.development`、`.env.production`、`env.d.ts`、`src/api/sso.ts`、`src/utils/ssoLogin.ts`、`src/utils/ssoCallback.mjs`、`src/router/guard.ts`、`src/main.ts`、`src/utils/request.ts`、`src/utils/authRedirect.ts`、`src/router/base.ts`
- 本地未推送：`repos/lumen-ui-topic` 同名 SSO 文件

## cost

- model_used：grok-4.7
- actual_tokens：未精确计量
- actual_cost：未精确计量
- cost_warn：green
