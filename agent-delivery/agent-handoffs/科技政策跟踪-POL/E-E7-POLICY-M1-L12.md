# E-E7-POLICY-M1-L12 · 政策订阅实现

- 日期：2026-11-03
- 任务：`E-E7-POLICY-M1-L12`
- 监管：`human:淮政玮`
- claimed_by：`agent:api-agent`（总控已认领，本单不改状态）
- ponytail: full
- 仓库：`lumen-svc-platform`
- commit：`7a917b31d98f32295d0411f93dd2a85c4ebe927d`
- 推送：`origin/dev`（先被拒，`git pull --no-rebase` 一次后推到 `e443c41fabecd026c343e9ddd303e34014ba394b`）

外发通道仍未上线。本单不把外发说成已上线。系统通知、邮件、短信都没有可发送实现，推送记录是空列表，没有向 `gkxlumen-topic-async-service` 交执行记录。

## 门面

服务内路径（须带已鉴权用户的令牌；不采用请求体里的 `user_id`）：

| 动作 | 路径 |
|---|---|
| 读取 | `GET /topic/v1/policy/subscriptions` |
| 保存 | `POST /topic/v1/policy/subscriptions` |
| 修改 | `PUT /topic/v1/policy/subscriptions/{id}` |
| 取消 | `DELETE /topic/v1/policy/subscriptions/{id}` |

网关前缀按 `@EnableOpenApi("policy")` 为 `/policy` + 上表路径。浏览器不改打这些路径。

到点筛选只走门面已有 `search`（Python `/internal/policy/search`，读 `gkxlumenx_dwd.policy_base_info`）。条件对到：类别 `policy_type`，部门检索参数 `ministry`（检索对到 `publish_organization`），地区检索参数 `region`（检索对到 province/city），行业原样进 `industry_code`。Java 不解释产业码。没有命中不造政策、不删订阅。通道未接通时读取不调用检索。

## 表

`gkxlumenx_topic_policy.policy_subscription`

脚本：`db/9x_gkxlumenx_topic_policy.sql`。不进 ODS / DWD / ADS / `gkxlumenx_gapfill`，不用态势模块的 `sys_user_relation` / `sys_user_subscription_rule`。

一行存：鉴权用户；政策类别、行业领域、发布部门、省、市、地区原文（空着的维不限制）；频率 `day`/`week`/`month` 之一；通道 `system`/`email`/`sms`（可多选，空则不外发）；是否仍有效；入库水位 `ingest_watermark`；频率刻度 `last_outbound_at`。不存政策正文、推送文案、命中快照、收藏用的政策 id、匹配分。

2026-11-03 已在现网执行订阅表这一段 DDL。库 `gkxlumenx_topic_policy`，表 `policy_subscription`，行数 0。库地址沿用已有 `user-jdbc-url`。没有订阅时读取是空列表。

## 展示委托

浏览器资源（保存、修改、取消是同一资源的 POST / PUT / DELETE）：

`/display/v1/policy/panorama/subscriptions`

网关 StripPrefix=1 后，展示服务路径是 `/v1/policy/panorama/subscriptions`，类 `PolicyPanoramaSubscriptionController`，Feign `RemotePolicySubscriptionClient` 转到上面的门面路径。展示不落订阅、不跑定时、不发信、不写 element / ADS。未登录或下游失败只让这条资源为空，不改时序、地域、入库接口。

## 空列表与推送

该用户没有仍有效的订阅：HTTP 200，`subscriptions` 为空数组，`honesty.fabricated=false`。不用 501，不写死一条订阅。

通道未接通：`pushes` 为空数组，`honesty.outbound=unavailable:no_send_channel`。不制造推送历史。

## 测试

```
mvn -pl gkxlumen-topic-policy/gkxlumen-topic-policy-biz -am test "-Dtest=PolicyFacadeControllerTest" "-Dsurefire.failIfNoSpecifiedTests=false"
```

结果：`Tests run: 20, Failures: 0, Errors: 0, Skipped: 0`。覆盖空列表、保存后能读出、修改、取消后不再出现在有效列表、请求体 `user_id` 不被采信、通道未接通时不交执行记录、没有命中不删订阅、没有选定通道不检索。

`PolicyPanoramaSubscriptionControllerTest` 已提交。本机整模块编译被工作区里另一会话未提交的 `PolicyPanoramaService` 挡住（它调用了 `RemoteElementClient` 上还不存在的方法）。该文件不在本提交里。javac 报错列表里没有本单的展示类。

## 成本

| 字段 | 值 |
|---|---|
| model_used | grok-4.7 |
| actual_tokens | 未从会话计量；本单按指示不调 task-registry |
| actual_cost | 未计量 |
| cost_warn | false |

## 还没做到

- 外发通道仍未上线。没有调度器在日/周/月到点主动跑。通道接通之前，读取不会筛政策，也不会交异步执行记录。
- 2026-11-03 已建库 `gkxlumenx_topic_policy`，并 `GRANT ALL` 给 `gkxlumenx`@`%`。表 `policy_subscription` 已按脚本建成，`SELECT COUNT(*)` 为 0。没有插入订阅行。口令未写入本文。
- 展示委托的测试类未在本机跑绿，原因见上。浏览器页面仍是 localStorage，本单不改前端。
- 不把 `E-E7-POLICY-M1-L06` 改成展示联调单。未动 L13，未改任务状态。
