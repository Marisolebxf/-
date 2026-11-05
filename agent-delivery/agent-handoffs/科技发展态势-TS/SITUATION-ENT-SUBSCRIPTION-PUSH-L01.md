# SITUATION-ENT-SUBSCRIPTION-PUSH-L01 · 订阅推送实装（P0 单模块闭环）

> **触发**：统一用户行为表服务端化（SITUATION-ENT-FOLLOW-SVR-L01）后续清单第 6 项「通知实装」。
> **角色**：`agent:api-agent`（监管人 `human:李伟`）
> **状态**：`delivered`（2026-11-05 按用户指令 commit + push `origin/dev`，待人工签收）
> **上位**：[SITUATION-ENT-长任务总控](./SITUATION-ENT-长任务总控.md)
> **真源**：[USER-BEHAVIOR-UNIFIED-TABLE-20261102.md](./USER-BEHAVIOR-UNIFIED-TABLE-20261102.md)
> **日期**：2026-11-04

---

## 一、决策（human:李伟 2026-11-04 拍板，已写入 task-registry.yaml note）

| 项 | 结论 |
|---|---|
| 调度器落点 | **gkxlumen-display**（读规则 / 取数 / 推送三能力齐全，零重复；不用 topic-async-service） |
| 频率 | 三档 **hourly / daily / weekly** |
| 通知 | **双写**：站内 `sys_user_notification` + 门户 `MessageCenterClient.pushNotice` |
| 范围 | 先 **global-innovation 单模块闭环**（region / city / domain / carrier 4 适配器） |

## 二、交付内容

### upms（`gkxlumen-upms`）
- **新增** `SysUserNotification` entity（16 字段，`@TenantTable` + `@TableName("sys_user_notification")`）
- **新增** `SysUserNotificationMapper`（extends `GkxlumenBaseMapper`）
- **新增** `UserNotificationDTO`（通知入参）
- `SysUserBehaviorService` / `Impl` 新增三方法：
  - `listEnabledRules(scopeType)`：跨租户扫描启用中规则（`@Inner` 空租户上下文 → 多租户插件跳过过滤 → 扫全表）
  - `recordNotification(dto)`：写站内通知，返回主键
  - `markPushed(ruleId)`：回写 `last_push_time = now()`
- `SysUserBehaviorController` 新增 3 个 `@Inner` 端点（`/rule/enabled`、`/notification/record`、`/rule/mark-pushed`）
- `RemoteUserBehaviorService` 新增 3 个 `@NoToken` Feign 方法

### display（`gkxlumen-display`）
- `pom.xml` 加 `gkxlumen-common-job` 依赖；`GkxlumenDisplayApplication` 加 `@EnableGkxlumenXxlJob`
- **新增** `job/SubscriptionPushJob`（`@XxlJob("subscriptionPushJob")`）
- **新增** `subscription/` 命中判定引擎：
  - `SubscriptionAdapter`（接口，按 `scopeType` 分派）+ `SubscriptionAdapterRegistry` + `SubscriptionHit`
  - `AbstractSubscriptionAdapter`（统一「取数 → 无数据不推 → 阈值闸门 → 组装文案」）
  - `Region/City/Domain/CarrierSubscriptionAdapter` 4 个适配器
- **新增** `service/SubscriptionNotifyService`（双写：站内 Feign + 门户 MessageCenterClient）

## 三、频率闸门与幂等

- Job 本身按小时触发，引擎内按 `push_frequency` 三档闸门：`last_push_time < 本周期起点` 才推。
  - hourly → 整点；daily → 当天 00:00；weekly → 本周一 00:00
- 推送成功后 `markPushed` 回写 `last_push_time = now()`，天然幂等（同周期不重复推）。
- 历史 `instant` 值映射为 `hourly`；空值默认 `daily`。

## 四、诚实边界（P0 不伪装闭合，逐条写明）

1. **命中语义 = 「范围有最新数据即推送摘要」**：不做 0-100 评分模型换算。
   `threshold + thresholdOp` 只是对取到的**原始指标值直比**（above ≥ / below ≤）；
   规则未设阈值时，范围有数据即命中。评分模型的换算属后续波次，未实现、未伪造。
2. **未做端到端跑批验证**：本次只做到 `mvn compile EXIT=0`。未在真实环境验证
   （无真实订阅规则数据 + 未连久新门面跑批），推送链路（取数→命中→双写）是**编译级**闭环，
   非运行时闭环。
3. **carrier 适配器取 top 200 载体榜**：超出榜单的载体匹配不到 → 诚实不推，不做兜底。
4. **domain / carrier 的 scopeValue 匹配用常见键名**（`name` / `name_zh` / `domain_id` /
   `carrier_id` / `location_id`），键名以久新实际返回为准；P0 未做字段级联调，若久新返回键名不同
   会导致匹配不到 → 同样诚实不推（不会误推）。
5. **幂等依赖 `last_push_time` 回写**：单实例假设下成立；未建独立的 `(rule_id, period_key)`
   去重表。若未来多实例并发，需补 period_key 去重（已在 DoD 记为幂等目标，P0 以回写实现）。

## 五、验证

`mvn -pl gkxlumen-upms/gkxlumen-upms-biz,gkxlumen-display -am compile -DskipTests`（JDK 17）：

```
gkxlumen-upms-api  .... SUCCESS
gkxlumen-upms-biz  .... SUCCESS
gkxlumen-common-job .... SUCCESS
gkxlumen-display   .... SUCCESS
BUILD SUCCESS
```

2026-11-05 复核：`mvn -pl gkxlumen-upms/gkxlumen-upms-biz,gkxlumen-display -am compile -DskipTests -o`（JDK 17）**BUILD OK**。

运行时证据（display local 启动日志）：

```
xxl-job register jobhandler success, name:subscriptionPushJob,
jobHandler=...SubscriptionPushJob#push
```

说明调度器 Bean 与 `@XxlJob("subscriptionPushJob")` 已被 XXL-Job 注册；但 `sys_user_subscription_rule` 当前 0 行，
**跑批链路未做端到端验证**（诚实边界第 2 条仍然成立）。

## 六、改动清单（2026-11-05 已 commit + push origin/dev）

| 仓库/模块 | 文件 | 动作 |
|---|---|---|
| gkxlumen-upms-api | `dto/UserNotificationDTO.java` | 新增 |
| gkxlumen-upms-api | `entity/SysUserNotification.java` | 新增 |
| gkxlumen-upms-api | `feign/RemoteUserBehaviorService.java` | 修改（+3 Feign 方法） |
| gkxlumen-upms-biz | `mapper/SysUserNotificationMapper.java` | 新增 |
| gkxlumen-upms-biz | `service/SysUserBehaviorService.java` | 修改（+3 方法签名） |
| gkxlumen-upms-biz | `service/impl/SysUserBehaviorServiceImpl.java` | 修改（+3 实现 + 注入 mapper） |
| gkxlumen-upms-biz | `controller/SysUserBehaviorController.java` | 修改（+3 端点） |
| gkxlumen-display | `pom.xml` | 修改（+gkxlumen-common-job） |
| gkxlumen-display | `GkxlumenDisplayApplication.java` | 修改（+@EnableGkxlumenXxlJob） |
| gkxlumen-display | `subscription/SubscriptionAdapter.java` | 新增 |
| gkxlumen-display | `subscription/SubscriptionHit.java` | 新增 |
| gkxlumen-display | `subscription/SubscriptionAdapterRegistry.java` | 新增 |
| gkxlumen-display | `subscription/adapter/AbstractSubscriptionAdapter.java` | 新增 |
| gkxlumen-display | `subscription/adapter/{Region,City,Domain,Carrier}SubscriptionAdapter.java` | 新增 |
| gkxlumen-display | `service/SubscriptionNotifyService.java` | 新增 |
| gkxlumen-display | `job/SubscriptionPushJob.java` | 新增 |

## 七、后续（供下一波次）

1. 评分模型换算（0-100 阈值）待数据侧口径，接上时改 `AbstractSubscriptionAdapter#passThreshold`。
2. 端到端联调：造真实订阅规则 + 连久新门面跑批，核对 4 适配器取数键名与 scopeValue 匹配。
3. 若多实例并发，补 `(rule_id, period_key)` 去重表。
4. 剩余范围类型（order / keyword）适配器待补。

## 八、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 90k（估） |
| model_used | auto |
| actual_cost | ≈ $0.6（估） |
| cost_warn | green |

ponytail: full（调度器落点 / 频率三档 / 双写 / 4 适配器全部按拍板落地；P0 命中语义与未做运行时验证均如实写进「诚实边界」，不把编译级闭环伪装成运行时闭环）
