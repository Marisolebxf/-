# 统一用户行为表设计（收藏 / 订阅 / 标签 / 预警规则 / 推送记录）

- **日期**：2026-11-02
- **范围**：`lumen-ui-science-pc`（展示系统 PC 端 27 页）+ `lumen-svc-platform`
- **结论**：**已落库**。5 张表已在 `gkxlumenx`（upms 主库）建成，DDL 落盘 `lumen-svc-platform/db/9x_gkxlumenx_user_behavior.sql`
- **回链**：WBS `WBS-05-18-16`（05-展示系统集成/WBS.md §4.3）、registry `SITUATION-ENT-FOLLOW-SVR-L01`

---

## 一、背景：全站 15 个功能点，0 张表 0 个接口

对 27 个页面逐页盘点（排除 `src/mock`），存在收藏/订阅类功能的有 **10 个页面、15 个功能点**：

| 行为类型 | 页面 | 功能 | 对象 ID 形态 | 改造前存储 |
|---|---|---|---|---|
| 收藏 | `situation/overview` | 要素收藏（企业/园区/机构/实验室） | `object-huawei-bantian` | localStorage `ts-follow-items` |
| 标签 | `situation/overview` | 标签目录 + 对象打标签 | `byObjectId[objectId]` | localStorage `ts-m1-factor-collection-tags-v1` |
| 收藏 | `achievement/incubation-carrier` | 新闻星标 | news.id | 组件 ref |
| 收藏 | `achievement/soft-science` | 收藏专题 / 点赞 | 专题、comment id | 组件 ref |
| 订阅 | `situation/shenzhen-innovation` | 载体订阅 | carrier.id | ref（+ `isSubscribed:false` mock 字段） |
| 订阅 | `talent/profile` | 人才订阅 + 我的订阅 + 推送通知 | talent.id | ref（通知本地伪造 2 条） |
| 订阅 | `achievement/incubation-carrier` | 载体动态推送订阅 | `C01` | 组件 ref |
| 订阅 | `achievement/instrument-sharing` | 订单进展提醒 | `RO-20260801-001` | ref（初值来自 mock） |
| 订阅 | `achievement/soft-science` | 关注动态 / 成果推送开关 | 专题级 | 组件 ref |
| **订阅规则** | `situation/global-innovation` detail | 区域订阅（范围+载体+指标+阈值 0-100+提醒方式+频率+关键词） | `rule-region-*` / 区域名 | ref（种子硬编码） |
| 订阅规则 | `situation/global-innovation` city | 订阅城市 + monitorConfig | 城市名 | ref（初始空） |
| 订阅规则 | `situation/global-innovation` monitor | 订阅领域/载体/条件(field/op/val)+频率+通道 | 领域名 / carrier.id | ref，推送列表恒 `[]`（如实空态） |
| **预警规则** | `situation/bay-innovation` | 城市能力阈值 50-90 + 通知已读/未读 + 变更记录 | alert id + 城市名 | ref |
| 推送设置 | `situation/tech-development-plan` | 关注领域 + 频率 + 渠道 | 领域名 | reactive（保存仅 toast） |
| 只读字段 | `data-resources/application` | 「订阅数」列 | `ud-001` | mock（**非用户行为，不进表**） |

**其余 17 个页面无此类功能**：panorama / tracking / tech-index / innovation-evaluation / maintain / talent(global,region,recommend) / data-resources(overview,access,theme) / innovation-ecosystem / space-time-evolution / service 三页 / policy 三页（未实现）/ graph 四页（未实现）。

**改造前**：`src/api` 全目录搜 `subscri|follow` 仅 1 处命中（常量 `isSubscribed:false`），**没有任何收藏/订阅接口**。

---

## 二、为什么能统一（架构依据）

`ARCH-DISPLAY-01.md`：

- §10.9「用户订阅（页面/指标/要素）→ 写订阅关系（展示侧库）→ 定时触发 → 复用 `gkxlumen-topic-async-service`」；「订阅**只复用异步执行能力**；订阅关系与触发规则属展示侧」
- §10.9.1「收藏 / 标签 / 订阅属 **PC 侧用户行为**」；「A9 未定 → 订阅关系、收藏、标签、导出配置均无处落库」

即：**这 15 个功能点本来就该共用一组表**，此前只是每个页面各自声明一份状态。

---

## 三、链路：用户身份怎么来（B 方案）

```
① 前端  Bearer(token) + 头 systemCode: display
        （src/utils/request.ts:129；token = 门户 Cookie portal_access_token，src/portal/auth.ts:14）
② 网关  只转发不解析（GkxlumenRequestGlobalFilter 无 token 校验逻辑）
③ 服务  Spring Security 资源服务器自动 introspect
          GkxlumenCustomOpaqueTokenIntrospector（sso.enabled=true → introspectViaSso）
            → SsoTokenChecker → POST {统一用户中心}/admin-api/system/oauth2/check-token
            → SsoCheckTokenVO{ userId, tenantId, userType, exp }
          → 组装 GkxlumenUser
④ 业务  SecurityUtils.getUser().getId() / .getTenantId()
⑤ 落库  按 user_id + tenant_id + 对象键 匹配
```

**关键事实（推翻既有假设）**：

| 项 | 结论 |
|---|---|
| 走哪条分支 | `SsoProperties.enabled` 默认 `true` → **统一用户中心分支**，不是 pigX 自签链路 |
| 能拿到什么 | `userId` ✅ `tenantId` ✅ `userType` ✅；`roleIds` ❌空、`deptId`/`nickname`/`email` ❌ null、`authorities` ❌ NO_AUTHORITIES |
| `username` 是什么 | ⚠️ `systemCode + ":" + clientId`（如 `display:xxx`）——**不是真实用户名**，故无法用 `RemoteUserService.info({username})` 反查本地 `sys_user` |
| 与 `sys_user.user_id` 的关系 | **不同源**。故收藏表不 join `sys_user`，直接存 SSO `userId` |
| 内部调用 | `@Inner`（默认 `value=true`）只认 `from=Y`；Feign 方法标 `@NoToken` 才由 `GkxlumenFeignInnerRequestInterceptor` 自动加头；`GkxlumenInnerHeaderRemoveFilter` 拒绝外部伪造 `from` 头。⚠️ `@Inner(value=false)` = 对外匿名放行，**不可用** |
| Feign 透传缺口 | `GkxlumenOAuthRequestInterceptor` **只透传 `Authorization`，不透传 `systemCode`** → 下游服务自己 introspect 会失败。故采用 **B 方案：display 取 userId 显式传参**，绕开该缺口 |

**性能提示**：SSO 校验**无缓存**，每个请求都打一次 check-token，收藏/订阅属高频操作，实装时应加 `token → userId` 本地缓存（TTL < token 有效期）。

---

## 四、表设计（5 张，落 `gkxlumenx`）

| # | 表名 | 字段数 | 承载 |
|---|---|---|---|
| 1 | `sys_user_relation` | 17 | 用户-对象关系统一表（收藏/订阅/关注/点赞） |
| 2 | `sys_user_tag` | 11 | 用户标签目录（用户私有） |
| 3 | `sys_user_relation_tag` | 8 | 关系-标签关联 |
| 4 | `sys_user_subscription_rule` | 22 | 订阅/预警规则（条件、阈值、频率、渠道） |
| 5 | `sys_user_notification` | 16 | 推送/通知记录（本期建表不实装，依赖 R8） |

### 关键设计决策

1. **用户键**：`user_id` = 统一用户中心 SSO `userId`（bigint），`tenant_id` = SSO 下发。**不 join `sys_user`**。
   > 既有表用户键类型混乱：`ent_search_history.user_id` 是 `varchar(64)`、`app_article_collect.user_id` 是 `bigint unsigned`、`policy_favorite.user_id` 是 `bigint`。SSO 返回的是 `Long`，故新表定死 **bigint**。
2. **`target_id` 用 varchar(128)**：对象 ID 形态混杂（`object-huawei-bantian`、城市名、`RO-20260801-001`、领域名）。
3. **唯一键不含 `del_flag`**：`(tenant_id,user_id,relation_type,source_page,target_type,target_id)`。取消行为走逻辑删除，再次触发时**复用原行置 `del_flag=0`** —— 避免「删了重建」插出重复行（`app_article_collect` 只有主键、靠代码查重，这里补唯一键）。
4. **`source_page` NOT NULL DEFAULT ''**：MySQL 唯一键对 NULL 不去重，空串才能保证去重生效。
5. **标签存 `tag_id` 不存字符串**：重命名标签只改 `sys_user_tag` 一行（现状 `factorTagStore.rename` 要遍历所有对象替换字符串）。
6. **规则独立成表而非 `rule_json`**：规则需被定时任务扫描（`idx_scan(status, monitor_frequency)`），JSON 列无法高效扫描。
7. **通知表建而不装**：订阅定时推送依赖 R8（XXL-Job 未部署）+ `gkxlumen-topic-async-service`。

---

## 五、功能点落位映射

| 页面 · 功能 | relation_type | target_type | target_id | 走规则表 |
|---|---|---|---|---|
| overview 要素收藏 | `follow` | `factor`/`enterprise`/`park`/`institution` | `object-huawei-bantian` | — |
| overview 对象标签 | — | （挂在 relation 上） | | — |
| incubation-carrier 新闻收藏 | `follow` | `news` | news.id | — |
| soft-science 收藏专题 | `follow` | `topic` | 专题 id | — |
| soft-science 点赞 | `like` | `comment` | comment id | — |
| soft-science 关注动态/推送开关 | `watch` | `topic` | 专题 id | — |
| shenzhen 载体订阅 | `subscribe` | `carrier` | carrier.id | — |
| incubation-carrier 载体订阅 | `subscribe` | `carrier` | `C01` | — |
| talent/profile 人才订阅 | `subscribe` | `talent` | talent.id | — |
| instrument-sharing 订单提醒 | `subscribe` | `order` | `RO-20260801-001` | — |
| global-innovation 区域订阅 | `subscribe` | `region` | 区域名 | ✅ 指标/阈值/频率/渠道/关键词 |
| global-innovation 城市订阅 | `subscribe` | `city` | 城市名 | ✅ |
| global-innovation 订阅管理 | `subscribe` | `domain`/`carrier` | 领域名 / carrier.id | ✅ 条件 field/op/value |
| bay-innovation 预警中心 | `subscribe` | `city` | 城市名 | ✅ 阈值 50-90 |
| tech-development-plan 推送设置 | `subscribe` | `field`/`resource` | 领域名 | ✅ 频率/渠道 |

**不进表**：`data-resources/application` 的「订阅数」（统计字段）、`space-time-evolution` 热点预警（分析结果，非用户订阅）。

---

## 六、归属决策记录（含被否决项）

| 候选 | 结论 | 依据 |
|---|---|---|
| ~~`gkxlumenx_dim`（维度库）~~ | ❌ **否决** | 库内全是共享主数据/字典（`admin_division`/`city`/`org_master`/`code_nic`…）；`code_region` 注释明写「**源 PG `dim.admin_division`**」= 由数据侧 ETL 同步，Java 写入会被下次同步覆盖 |
| ~~新建 `gkxlumenx_behavior` 库~~ | ❌ **本期不做** | 语义最干净，但需新增数据源配置 + 运维授权，且现有规范是按业务域分库（无横切行为库先例）；未来如需独立，表可直接迁移 |
| ~~`gkxlumenx_app`（app 库）~~ | ❌ **不采用** | `ARCH-DISPLAY-01.md:513` 写「写 `app_user`」是 **A9 未定**时的旧表述；现已确认 PC 用户 = 统一用户中心，非 `app_user` |
| **`gkxlumenx`（upms 主库）** | ✅ **采用** | 用户行为归用户域（upms 管用户）；不新增数据源即可落地；`human:李伟` 2026-11-02 拍板 |

**补充事实**：系统内**没有专门的用户行为库**，既有行为表散落且各自为政：
- `gkxlumenx_topic_enterprise`：`ent_search_history` / `chain_search_history`（注释「用户隔离」，是唯一有完整服务实现的）
- `gkxlumenx_app`：`app_article_collect`（App 端文章收藏）
- `gkxlumenx_dwd`：`policy_favorite` / `policy_search_record` —— ⚠️ **后端 0 引用、db DDL 也 0 命中 = 孤表**，不可误当作"政策收藏已实现"

---

## 七、DDL 落盘与执行记录

- **DDL 文件**：`lumen-svc-platform/db/9x_gkxlumenx_user_behavior.sql`（命名对齐 `9x_gkxlumenx_*.sql` 增量脚本规范）
- **执行目标**：远程 MySQL `10.50.11.76:3306` 库 `gkxlumenx`（凭据取自 `gkxlumen-element/src/main/resources/application-local.yml`：`gkxlumenx` / `GKX@Lumen2026`）
- **执行结果**：`EXIT=0`，stderr 无错误
- **验证证据**（`information_schema` 实查）：

| 表名 | 字段数 | Engine | Collation |
|---|---|---|---|
| `sys_user_relation` | 17 | InnoDB | utf8mb4_general_ci |
| `sys_user_tag` | 11 | InnoDB | utf8mb4_general_ci |
| `sys_user_relation_tag` | 8 | InnoDB | utf8mb4_general_ci |
| `sys_user_subscription_rule` | 22 | InnoDB | utf8mb4_general_ci |
| `sys_user_notification` | 16 | InnoDB | utf8mb4_general_ci |

`sys_user_relation` 索引实查：`PRIMARY(id)`、`uk_user_relation(tenant_id,user_id,relation_type,source_page,target_type,target_id)` 唯一、`idx_user_type(user_id,relation_type,status)`、`idx_target(target_type,target_id)` —— 与设计一致。

> 环境提示：本机 3306（root/root）**不是**项目库（只有 `demo_gkxlumenx_ads/dwd` 与 `healthcarex*`）；本机 `nacos` 库 `config_info` **为空**、8848 不可达，配置实际走各模块 `application-local.yml`。

---

## 八、后续实施清单（本期未完成）

| # | 事项 | 说明 |
|---|---|---|
| 1 | upms-biz：Entity / Mapper / Service / Controller | Controller 方法标 `@Inner`（只认内部调用），入参含 `userId` |
| 2 | upms-api：`RemoteUserRelationService`（Feign） | 方法标 `@NoToken`，由 `GkxlumenFeignInnerRequestInterceptor` 自动加 `from=Y` |
| 3 | display：端点取 `SecurityUtils.getUser()` → 转发 | 对外路径沿用 `ARCH-DISPLAY-01.md:513`：`/display/v1/trend/favorites`、`/tags`，另加 `/subscriptions`、`/rules` |
| 4 | 前端：`useFollow` 服务端化 | 乐观更新 + 失败降级 localStorage；其余 9 页按 §五 映射逐页接线 |
| 5 | `sys_user_tag` 默认标签种子 | 用户首次访问写入 `重点关注 / 待跟踪 / 高价值`（对齐 `factorTagStore.DEFAULT_TAGS`） |
| 6 | 通知实装 | 阻塞于 R8（XXL-Job 未部署）+ `gkxlumen-topic-async-service` |
| 7 | 接口纳入契约 | `BE-TS-CONTRACT-01`（该单尚未产出） |
| 8 | 架构文档回填 | `ARCH-DISPLAY-01.md:513`「写 `app_user`」应更新为「写 `gkxlumenx` 用户行为表族」（A9 已由事实澄清） |

---

## 九、待办与风险

| 项 | 状态 |
|---|---|
| DDL | ✅ 已执行并验证 |
| 后端 CRUD / Feign / display 端点 | ✅ 已实现，`mvn compile` EXIT=0 |
| 前端 API 层 + useFollow 服务端化 | ✅ 已实现，`vue-tsc --build` EXIT=0 |
| 运行时联调 | ❌ **未做**：Nacos（`:8848` 本机/远程均不可达）导致 upms 无法启动，无端到端验证 |
| git | ⚠️ 全部改动**停本地未 commit 未 push**，待 `human:李伟` 走查 |
| 风险 | SSO check-token 无缓存（高频放大）；`@Inner(value=false)` 是匿名放行，实装时勿误用 |

---

## 十、实施记录（2026-11-02 后端 + 前端落地）

### 10.1 新增文件（17 个）

**upms-api（Entity / DTO / VO / Feign）**

| 文件 | 说明 |
|---|---|
| `entity/SysUserRelation.java` | 关系表实体（17 字段，不含 `snapshot_json`，避免 json↔String 类型处理器问题） |
| `entity/SysUserTag.java` | 标签目录（用户私有） |
| `entity/SysUserRelationTag.java` | 关系-标签关联 |
| `entity/SysUserSubscriptionRule.java` | 订阅/预警规则（22 字段） |
| `dto/UserRelationDTO.java` | 关系保存/切换入参（含 `tagIds`） |
| `dto/UserTagDTO.java` | 标签入参 |
| `dto/UserRuleDTO.java` | 规则入参 |
| `vo/UserRelationVO.java` | 关系返回体（含 `tagIds/tagNames`，前端一次取回） |
| `feign/RemoteUserBehaviorService.java` | 11 个方法，**全部 `@NoToken`** |

**upms-biz（Mapper / Service / Controller）**

| 文件 | 说明 |
|---|---|
| `mapper/SysUserRelationMapper.java` | 含 `selectAny`（查含已删行）、`restore`（复用原行） |
| `mapper/SysUserTagMapper.java` | 同上（同名标签复用） |
| `mapper/SysUserRelationTagMapper.java` | 含 `physicalDeleteByRelation/ByTag`（**物理删除**） |
| `mapper/SysUserSubscriptionRuleMapper.java` | 基础 Mapper |
| `service/SysUserBehaviorService.java` | 接口（11 个方法） |
| `service/impl/SysUserBehaviorServiceImpl.java` | 实现（核心逻辑 + 事务） |
| `controller/SysUserBehaviorController.java` | `/user/behavior/**`，11 个端点**全部 `@Inner`** |

**display**

| 文件 | 说明 |
|---|---|
| `controller/UserBehaviorController.java` | `/v1/user-behavior/**`，取 `SecurityUtils.getUser()` 覆盖 userId/tenantId 后转发 |
| `pom.xml`（改） | 新增 `gkxlumen-upms-api` 依赖 |

**前端**

| 文件 | 说明 |
|---|---|
| `src/api/userBehavior.ts`（新） | 11 个 API 封装，**全部 `optional: true`**（401 不触发登出） |
| `src/components/export/useFollow.ts`（改） | 真源改服务端；对外签名不变；模块级单例共享状态 |

### 10.2 实现中确定的三个关键细节

1. **`@TableLogic` 与"复用原行"冲突的解法**
   唯一键不含 `del_flag`，取消后再收藏必须复用原行；但 MP 的 `@TableLogic` 会让 `select` 自动追加 `del_flag='0'`，**查不到已删行**。
   解法：Mapper 加两条原生 SQL —— `selectAny`（裸查、绕过逻辑删除过滤）+ `restore`（`UPDATE ... SET del_flag='0'`）。

2. **关联表用物理删除**
   `sys_user_relation_tag` 唯一键 `(relation_id, tag_id)` 不含 `del_flag`，若走逻辑删除则重新绑定同一标签会撞唯一键；关联数据无审计价值，改 `@Delete` 物理删除（`physicalDeleteByRelation/ByTag`）。

3. **租户隔离必须显式传参**
   `GkxlumenTenantHandler.ignoreTable`：`TenantContextHolder.getTenantId() == null` 时 **跳过租户过滤**（查全部）。
   `@Inner` 调用不带 token → 租户上下文为空 → 框架不会自动过滤。
   因此 Service 每个方法都 `requireUser(tenantId, userId)` 强校验 + 查询条件显式 `.eq(tenantId)`，否则会跨租户串数据。

### 10.3 验证结果

| 验证项 | 命令 | 结果 |
|---|---|---|
| 后端编译 | `mvn -o -pl gkxlumen-upms/gkxlumen-upms-api,gkxlumen-upms/gkxlumen-upms-biz,gkxlumen-display -am -DskipTests compile`（`JAVA_HOME=jdk-17`） | **EXIT=0**，5 个新 class 产物均已生成 |
| 前端类型 | `npm run type-check`（`vue-tsc --build`） | **EXIT=0** |
| 运行时联调 | — | **未做**：Nacos 不可达，upms 起不来 |

> 编译曾报「无效的目标发行版: 17」，原因是 maven 默认 JDK 非 17；显式 `set JAVA_HOME=C:\Program Files\Java\jdk-17` 后通过。

### 10.4 前端降级策略（必须有，否则线上会踢人）

- 请求统一 `optional: true` —— 未登录/服务异常时**不触发全局登出重定向**；
- 读失败 → 沿用 localStorage，页面照常展示；
- 写失败 → 保留乐观更新结果，仅 `console.warn`，不打断用户操作；
- 状态单例：`overview` / `FilterBar` / 详情抽屉共享同一 `sharedItems`，避免"收藏了别的组件看不到"。

### 10.5 尚未接线（下一步）

| 页面/功能 | relation_type | 状态 |
|---|---|---|
| `situation/overview` 要素收藏 | follow | ✅ 已接线（useFollow 内部切服务端，调用点零改动） |
| `situation/overview` 标签管理 | —（relation_tag） | ✅ **已接线**（A 方案，见 §十一） |
| 其余 8 页 13 个订阅点 | subscribe / watch / like | ⬜ 逐页按 §五 映射接线（API 层已就绪） |
| 通知中心 | — | ⬜ 阻塞 R8 |

---

## 十一、标签管理接线（A 方案，2026-11-02）

### 11.1 为什么必须新增 `tags-by-target`

| | 本地 `factorTagStore`（旧） | 服务端模型 |
|---|---|---|
| 挂载锚点 | `objectId` | `relation_id`（`sys_user_relation_tag`） |
| 标签标识 | 名字字符串 | `tag_id` |
| 重命名成本 | 遍历所有对象改一遍 | 改 `sys_user_tag` 一行 |
| 未收藏能否打标签 | 可以 | 原 `updateRelationTags` 直接返回 false |

`SituationFilterBar` 的勾选事件只带 `objectId`（relationId 前端拿不到），所以新增端点让**后端自己按对象定位关系**。

### 11.2 后端新增

`POST /user/behavior/relation/tags-by-target`（upms，`@Inner`）→ display `POST /v1/user-behavior/tags-by-target`

- 入参 `UserRelationDTO{relationType, targetType, targetId, tagIds, title, summary}`
- `SysUserRelationMapper.selectAnyByTarget` 按 `(tenantId,userId,relationType,targetType,targetId)` 取最新一条，**不含 sourcePage**（标签按对象打，不按来源页）
- 关系不存在 → 插一条 `follow`；已被取消（`del_flag=1`）→ `restore` 复用原行；有效 → 覆盖标签
- 返回 `UserRelationVO`（含 `tagIds/tagNames`）

### 11.3 前端改造

`factorTagStore.ts` 重写但**对外契约不变**（仍以标签名字符串返回），所以 `SituationFilterBar` 的 props 与 `index.vue` 模板不必改成 ID 视角：

- 内部维护 `catalogRows: {id,tagName}[]` + `tagIdsByTarget: Record<targetId, tagId[]>`
- `hydrateFactorTags()`：并拉 `fetchTags` + `fetchRelations`；目录为空且从未播种时补三条默认标签（`ts-m1-factor-tags-seeded` 标记防重复播种）
- 新建标签用**负占位 id** 乐观插入，落库后替换并回填到已引用它的对象 tags
- `toggleFactorObjectTag(objectId, tag, objectType?)` 推 `updateTagsByTarget`，失败回滚 + `console.warn`
- 重命名只发一次 `saveTag({id,tagName})`；因对象标签存 `tagId`，**显示名自动跟着变**（旧实现要遍历改所有对象）

`SituationFilterBar.vue`：`toggle-object-tag` 增加第三参 `objectType`；`index.vue` handler 透传，并在 `onMounted` 调 `hydrateFactorTags()`。

### 11.4 验证

| 项 | 结果 |
|---|---|
| 前端 `vue-tsc --build` | **EXIT=0** |
| 后端 upms-api + upms-biz `mvn compile` | **EXIT=0**（`SysUserBehaviorServiceImpl.class` 已生成） |
| display 编译 | **EXIT=0**（`JAVA_ERROR_COUNT=0`，`UserBehaviorController.class` 已产出）。⚠️ 踩坑记录：中途曾报「包 `admin.api.dto` 存在、类 `UserRelationDTO` 找不到」——根因是本地仓库 `gkxlumen-upms-api-5.12.0.jar` 还是 07:35 的旧版，**不是代码问题**；执行 `mvn install -pl gkxlumen-upms/gkxlumen-upms-api -am -DskipTests` 刷新 jar 后通过。期间并行会话的 `TrackingController.getFullYear()` 笔误（行号 549→583 漂移）由其自行修复 |

### 11.5 语义决策（已拍板）

**给未收藏对象打标签 = 自动补一条 follow**（用户 2026-11-02 选 A）。因此收藏面板里"打标签"可独立于"收藏"按钮生效，不会出现"必须先收藏才能打标签"的死角。

### 11.6 写失败可见化 + 误报纠正（2026-11-02 晚追加）

**① 写失败由静默 console.warn 改为用户可见**：

- `factorTagStore`：4 处写失败（新建/重命名/删除/对象标签同步）`Message.warning`，读降级（hydrate）**仍静默**——未登录匿名浏览是常态，弹窗等于骚扰；
- `useFollow`：`pushToggle` 失败提示「收藏状态同步失败，当前仅本地生效」。

**② 新增 `subscribeFactorTags` 订阅机制（比 toast 更重要的一步）**：
store 是「同步乐观 + 异步落库」，回滚发生在异步落点，但页面的 `factorTagCatalog`/`factorObjectTagsById` 快照 ref 不会自动刷新——只加 toast 会出现「toast 说已恢复、屏幕还是失败态」的**撒谎 UI**。故 store 在所有异步落点（占位 id 替换成功 / 写失败回滚 / 服务端回写 tagIds）统一 `notifyFactorTagsChanged()`；`index.vue` 在 `onMounted` 订阅 `refreshFactorTagState`、`onBeforeUnmount` 注销。

**③ 误报纠正**：上一轮判定 `index.vue:1042` 地区抽屉标签合并为死代码——**误报**。核实 `followViewItems` 的 map 含 `objectId: item.objectId`（= region.key），地区收藏项出现在面板、打标签按 region.key 存、抽屉按 region.key 取，链路是通的，**未做改动**。同时核实了 targetType 一致性：useFollow 存的 `targetType` 与 FilterBar 打标签传的 `objectType` 同为中文展示名串，`tags-by-target` 的 `selectAnyByTarget` 可命中同一条关系，不会分裂。

**④ 事件端点核对结论（无需改动）**：display `SituationController /events` 已由并行会话实装（注释记录 2026-10-30 补端点、10-31 修地域/领域过滤与旧占位类型），返回 `{scopedTimeline, events, scopeLabel, notes}` 与前端 `SituationEventsResult` 契约**匹配**（`notes` 为额外诊断字段，不破坏契约）；前端 `optionalPost` 空态兜底保留为合理防御。

**⑤ 环境两则**：Nacos `127.0.0.1:8848` 仍不可达（联调继续阻塞）；本轮 `vue-tsc` **无法执行**——node_modules 正被并行会话 pnpm 重装（顶层 vue/typescript/vite 链接未完成，`@volar/typescript` 未装，node.exe 进程 8→14 且含两个 ~1GB），**待安装完成后必须补跑 `npm run type-check`**（IDE read_lints 三文件 0 错误，参考性有限）。
