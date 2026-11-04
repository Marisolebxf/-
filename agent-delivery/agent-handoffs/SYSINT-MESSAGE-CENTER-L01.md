# SYSINT-MESSAGE-CENTER-L01 · 门户消息中心对接（消息推送开放接口）

> WBS-05-30 · 仓库 `repos/lumen-svc-platform`（`gkxlumen-display`）· 状态 **integration**（2026-11-04）
> 说明：本任务交付**集成底座**（客户端 + 配置 + 报文 DTO）；把 25 个推送/预警功能点逐个接线到 `pushNotice/pushTodo` 为后续子任务，不在本任务范围。

## 任务认领

| 字段 | 值 |
|------|-----|
| 执行 | `agent:api-agent` |
| supervised_by | `human:李伟` |
| 完成日期 | 2026-11-04（集成底座） |

## 背景与目标

展示系统（`systemCode=TECH_INFO_DISPLAY`）需要向门户统一消息中心推送通知/待办，覆盖系统内所有消息订阅与推送场景（订阅规则命中、预警触发等）。本任务先把消息中心开放接口对接集成进展示系统后端，交付可复用的推送客户端，供各功能点调用。

## 工作成果

### 后端（`gkxlumen-display`）

| 文件 | 说明 |
|---|---|
| `config/MessageCenterProperties.java` | 配置属性（`gkxlumen.message-center`）：base-url / system-code / system-name / system-secret / 超时 / 重试 |
| `config/MessageCenterConfiguration.java` | 装配带超时的 `messageCenterRestTemplate` Bean |
| `client/MessageCenterClient.java` | 推送核心：`pushNotice` / `pushTodo` / `newMessageId`；X-System-Code/X-System-Secret 认证头 + 503/225001 退避重试 + 统一响应解析 |
| `client/message/NoticeMessage.java` | 通知报文 DTO（topic `portal_notice_msg`） |
| `client/message/TodoMessage.java` | 待办报文 DTO（topic `portal_todo_msg`） |
| `client/message/MessageCenterResponse.java` | 统一响应体（code/message/data/traceId） |
| `application-local.yml` | 新增 `gkxlumen.message-center` 块（测试 base-url + 凭证） |

实现要点：
- 客户端用 **RestTemplate**（非 Feign），因消息中心是外部 HTTP 接口，需自定义认证头 + 退避重试，Feign 服务发现不适用；对齐 `upms` 的 `SsoCenterClient` 外部 API 模式。
- `newMessageId()` 生成 `<系统编码>-<32位小写UUID>`；分区键：通知取 `data.businessId`（兜底 messageId），待办取 `data.ticketNo`。
- 可重试错误：HTTP 503 或 `code=225001`（队列投递失败），默认重试 3 次、退避 500ms；其余 4xx/5xx 不重试直接失败。
- 配置 `enabled=false` 时静默跳过（返回 ok）。

## 工作过程

1. 读取消息中心对接文档（飞书 wiki + 7 张内嵌表格），取得完整契约（topic 白名单、报文 Schema、错误码）。
2. 探查展示系统后端结构，确认落点为 `gkxlumen-display`（`systemCode=TECH_INFO_DISPLAY` 对应展示系统 BFF），复用 `RemoteDeepShiClient` / `SsoCenterClient` 既有外部 API 模式。
3. 落地客户端 + 配置 + DTO，`mvn compile` 通过（本机 `JAVA_HOME` 指向 JDK8，需切 JDK17 编译）。

## 决策记录

| 决策 | 结论 | 依据 |
|---|---|---|
| 集成落点 | `gkxlumen-display`（展示系统后端 BFF） | `systemCode=TECH_INFO_DISPLAY` 对应展示系统；BFF 是展示系统后端入口 |
| 客户端选型 | **RestTemplate**，非 Feign | 消息中心是外部 HTTP 接口，需 `X-System-Code`/`X-System-Secret` 自定义认证头 + 退避重试，Feign 服务发现不适用；对齐 `SsoCenterClient` 模式 |
| 报文 DTO | 类型化 `NoticeMessage`/`TodoMessage` + 响应 `data` 用 `Map` | 请求侧字段固定走强类型；响应 `data` 字段（topic/key/partition/offset）按需取用，Map 避免字段名耦合 |
| 重试策略 | 仅 503 / `code=225001` 重试，默认 3 次退避 500ms | 文档明示 225001「可安全重试」，messageId 去重保证幂等；其余错误重试无意义 |
| 凭证管理 | 本地 yml 落凭证；**生产放 Nacos，不入 git** | 仓内铁律「口令不进 git」 |
| 任务范围 | 本任务只交付集成底座，25 功能点接线为后续子任务 | 触发逻辑分布在 upms / topic-policy 等，需逐点确认触发点，不宜本任务一把梭 |

## 验收证据

- `mvn -pl gkxlumen-display -am compile -DskipTests -o` 通过（JDK17）。

## CI/CD

- 分支 `dev`；改动停在本地工作区，**未 commit / 未 push**（人工验收闸门）。

## 遗留 / 后续

1. **25 个推送/预警功能点接线**：需逐个确认触发点（订阅规则匹配、定时任务、预警阈值），把触发逻辑接到 `pushNotice`/`pushTodo`。涉及服务：upms（`sys_user_subscription_rule`）、topic-policy 等。
2. **生产配置**：`base-url`（生产门户网关域名）与 `system-secret` 落到 Nacos（`application-dev.yml` / `gkxlumen-display-dev.yml`）。
3. **待办 ticketNo 生成**：格式 `TK_<系统代码>_<yyyyMMdd><4位流水>`，当前由调用方传入，未内置流水号生成器（业务侧确认流水来源后补）。
4. **接收人 `receiverId` 口径**：需与统一用户中心对齐（文档要求接收人用户 ID），接线前确认展示系统的 userId 与门户 userId 映射。
