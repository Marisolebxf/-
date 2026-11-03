# POL-L2-DS10-QRY-DISP-L01 · 科创政策全景 · 多维检索查询 · 展示委托排序收藏与导出

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮`（登记表）。本会话提交人为 `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。开工时已是 `in_progress` |
| 说明 | 不改 task-registry，不把任务标成 done |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只在 `gkxlumen-display` 增加一条 Feign 和六个资源。不新造收藏表，不调 Python，不连库。未改 `gkxlumen-topic-policy` |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POL-L2-DS10-QRY-ARCH` |
| 图 diff | 未改图。展示只委托专题门面已有入口 |
| 会签态 | 架构稿记 `draft`（源文件无 frontmatter） |
| 说明 | 浏览器入口仍是 `/display/v1/policy/panorama/**` |

## 修改内容

仓库 `lumen-svc-platform`，分支 `dev`，commit `70abaa792f78c5f094943668361469ef7f496b97`。

`PolicyPanoramaQueryController` 与已有全景控制器同前缀 `/v1/policy/panorama`。网关 StripPrefix=1 后，浏览器路径不变。`rank`、`favorites`、`share` 是字面路径，不进 `/{id}/detail`。

| 浏览器 | 内部委托 |
|---|---|
| `GET /display/v1/policy/panorama/rank` | `GET /topic/v1/policy/rank` |
| `GET /display/v1/policy/panorama/favorites` | `GET /topic/v1/policy/favorites` |
| `POST /display/v1/policy/panorama/favorites/history` | `POST /topic/v1/policy/favorites/history` |
| `POST /display/v1/policy/panorama/favorites/history/{id}/search` | `POST /topic/v1/policy/favorites/history/{id}/search` |
| `POST /display/v1/policy/panorama/favorites` | `POST /topic/v1/policy/favorites` |
| `GET /display/v1/policy/panorama/favorites/{policyId}` | `GET /topic/v1/policy/favorites/{policyId}` |
| `GET /display/v1/policy/panorama/share` | `GET /topic/v1/policy/share` |

下游无响应或调用失败时，列表为空，并带 `honesty.fabricated=false`。不造收藏行，不生成文件字节。

### 令牌

门面收藏、再次检索、打开收藏、导出都用 `SecurityUtils.getUser()` 取当前用户，不采用请求体里的 `user_id`。

展示侧与订阅客户端同一写法：`RemotePolicyQueryClient` 不标 `@NoToken`。`@NoToken` 会先写 `from: Y`，`GkxlumenOAuthRequestInterceptor` 见到该头就不再复制 `Authorization`。不标则把浏览器带来的登录令牌原样转到 `gkxlumen-topic-policy`。排序走同一条客户端，不另开一条丢掉令牌的客户端。

## 测试结果

`gkxlumen-display` 单测 `PolicyPanoramaQueryControllerTest`：4 通过。覆盖七个转发路径、确认方法和接口都没有 `@NoToken`、空列表原样返回、下游失败不造收藏。未跑整仓。

## 遗留风险

专题门面的 `rank`、`favorites`、`share` 仍标 `@Inner(false)`。资源服务器把这类路径放进 `publicUrls`，`GkxlumenBearerTokenExtractor` 对这些路径不读 `Authorization`。展示侧已经把令牌转过去，门面 `SecurityUtils.getUser()` 仍可能是空，收藏会走匿名空列表，指定了 `format=excel|pdf` 的导出也不会按登录用户写对象。

订阅入口已经不标 `@Inner(false)`，所以订阅能解析令牌。本单按约束没有改 `gkxlumen-topic-policy`。要让收藏和导出认到人，需要门面去掉这几处 `@Inner(false)`，展示侧这版不用再改。

排序不依赖用户。分享链接和当次目录在匿名时仍由门面返回，文件字节不在展示响应里。

## 架构合规自检

1. 浏览器 → display → topic-policy 已有入口。不直连 Python，不直连库。✅
2. 未写算法，未造假记录。✅
3. 未改 D4，未新造 `metric_id`。✅
4. 未调用 `demo-*`。✅

## CI/CD

- 分支：`dev`
- commit：`70abaa792f78c5f094943668361469ef7f496b97`
- 推送：`70c0b36..70abaa7` `origin/dev`
- 部署：本单未做 rollout

## 涉及文件

- `gkxlumen-display` `PolicyPanoramaQueryController`
- `gkxlumen-display` `RemotePolicyQueryClient`
- `gkxlumen-display` `PolicyPanoramaQueryControllerTest`
