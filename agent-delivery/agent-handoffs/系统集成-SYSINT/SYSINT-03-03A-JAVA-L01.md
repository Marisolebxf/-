# Handoff · SYSINT-03-03A-JAVA-L01 专题服务内容管理（Java 写侧 + shenzhen 展示合并）

> **任务**：`SYSINT-03-03A-JAVA-L01`（feature / P1 / M / 3分）· 执行 `agent:api-agent` · 监管/签收 `human:徐滕强`
> **模式**：企业发展写侧 SYSINT-03-01A-JAVA-L01 的直接复刻（12 类 → 1 类），模式文档 `/tmp/handoff-sysint-03-01a-enterprise-cms-pattern.md`
> **契约**：`agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题服务.md`（已确认 2026-10-24，字段禁改）
> **状态**：代码已推 `origin/dev`（commit `31990eb`，经用户 2026-10-24 拍板「本地与线上完全同步」放行）；**CI 流水线 [2847](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/2847) backend:build ✅ 绿**（2026-10-24 实测）

---

## 1. 范围与实现

### Part 1 · 后台写侧（gkxlumen-cms，页面轨 /cms-ops/**）

| 项 | 实现 |
|---|---|
| content_type | `svc_business_domain`（`OpsContentType.SVC_BUSINESS_DOMAIN`，契约 §2.1 直译） |
| 字段 | `org_id`（必填）/ `industry_id`（必填）/ `body_html`（必填 html） |
| 绑定 | org_id + industry_id 双键（svc 族新绑定键 `org_id`，列与 ent 族 `enterprise_code` 区分） |
| DDL | `db/9x_gkxlumenx_cms_ops_svc_content.sql`（单表 `cms_svc_business_domain`，信封列全带，`CREATE TABLE IF NOT EXISTS` 幂等） |
| 端点 | `TopicServiceOpsController` @ `/cms-ops/v1/topic-service/content/svc-business-domain`：POST 新建(draft) / PUT 编辑 / POST `{id}/publish`（version+1）/ POST `{id}/unpublish` / GET 列表（`industry_id`/`org_id`/`publish_status` 过滤+分页）/ GET `{id}` / DELETE 软删 |
| 通用服务 | 复用 `OpsContentService`（sanitize/发布状态机/软删/`OverlayDao.audit` 同事务）与 `HtmlWhitelist`，零重写 |

**通用服务最小泛化（3 处，模式文档没覆盖的新情况——svc 族表无 ent 绑定列）**：
1. `OpsContentType.writableFields()`：svc 族不继承 ent 的 `BINDING_FIELDS`（`enterprise_code`/`future_industry_code`），绑定键来自契约 required；
2. `OpsContentService.list()`：org 过滤列与产业过滤列按 `hasSvcOrgBinding()` 泛化（svc=`org_id`/`industry_id`，ent=`enterprise_code`/`future_industry_code`）；
3. `OpsContentService.envelope()`：输出绑定码按族选择；`loadBlockStatus()`（enterprise-summary 聚合）跳过 svc 表（无 `enterprise_code` 列，否则 SQL 报错）。

### Part 2 · 页面展示侧（gkxlumen-topic-svc，接口签名不变）

| 项 | 实现 |
|---|---|
| 落点 | `ServiceFacadeServiceImpl.portalShenzhen()`（`POST /topic/v1/service-portal/shenzhen`，网关 `/svc/topic/v1/service-portal/shenzhen`） |
| 逻辑 | Python 指标底数照旧查（unwrap 原样）→ 请求带 `org_id`+`industry_id` 时查 cms published `body_html` → 响应新增 `data.cms` 块 |
| 数据通道 | `CmsSvcContentDao`：本服务既有只读数据源（helm `SET SESSION TRANSACTION READ ONLY`），跨库限定名单查 `gkxlumenx_cms.cms_svc_business_domain`（同实例 10.50.11.76；模式文档 §4 授权「跨库同实例 join 或查 cms 服务」，取零新依赖 + 失败面最小路径） |
| 合并规则 | 指标数字永不被 cms 覆盖；有 published → `cms:{content_type, present:true, body_html}`；无 → `cms:{present:false}`（契约 §2.2 不造假介绍）；cms 挂 → `cms:{present:false, data_source:"cms:unavailable"}`（失败隔离，指标区照常，接口不 5xx） |
| 接口签名 | 请求/响应既有字段零变动，只增 `cms` 可选键；无 org 上下文的页级请求 `cms:{}` 空块 |

## 2. 偏离说明

| # | 偏离 | 理由 + as-built |
|---|---|---|
| 1 | Part 2 走跨库直查而非契约 §3.1 的 `/api/published/**` 集群内接口 | 契约 §3.1 读接口是「智树门户对浏览器」的钦定链路（本单未实现，属展示合并叶后续范围）；/goal Part 2 钦定「查 gkxlumenx_cms 该双键的 published body_html」，模式文档 §4 两条通道均合法。取直查：topic-svc 已有只读源零新依赖，免跨服务 Feign 失败放大。as-built=`CmsSvcContentDao` 单表 SELECT，只读 |
| 2 | `body_html` 运营内容（人数/营收/排名）不做校验拦截 | /goal 明确「运营手写则按文本诚实展示」；HTML **安全**白名单（script/iframe/事件属性/脚本协议）仍强制（契约 §0），编辑口径靠运维规范 |
| 3 | 推送了 origin/dev（原单「停本地」约定的例外） | 用户 2026-10-24 明确指令「本地和线上完全同步，不弄丢别人的文件，本地变更也不丢失」，签收权人=监管人本人放行 |
| 4 | topic-svc-biz pom 补 surefire 3.2.5 钉版 | 存量 bug：默认 surefire 2.12.4 不认 JUnit5，该模块单测在 CI（clean verify）被静默跳过。修复后 85/85 真实执行（本单新增 4 例在其中）。照抄 cms 模块同款注释 |
| 5 | 中途产生 2 个过程 commit（WIP 全量 + 剥离格式化噪音） | `spring-javaformat:apply` 误伤 46 个无关文件，已在本仓内还原（`05cb14e`），最终 diff 只含本单 11 文件。过程 commit 保留可审计，无 squash 需求 |

## 3. 产物清单

| 文件 | 变更 |
|---|---|
| `db/9x_gkxlumenx_cms_ops_svc_content.sql` | 新增，幂等 DDL |
| `gkxlumen-cms/.../ops/OpsContentType.java` | +`SVC_BUSINESS_DOMAIN` 枚举 +`hasSvcOrgBinding()` +`SVC_ORG_BINDING` |
| `gkxlumen-cms/.../ops/OpsContentService.java` | list/envelope/loadBlockStatus 三处族泛化 |
| `gkxlumen-cms/.../ops/TopicServiceOpsController.java` | 新增，7 端点 |
| `gkxlumen-topic-svc/.../service/impl/CmsSvcContentDao.java` | 新增，published 只读单查 |
| `gkxlumen-topic-svc/.../service/impl/ServiceFacadeServiceImpl.java` | portalShenzhen 合并 + cmsIntroBlock |
| `gkxlumen-topic-svc/gkxlumen-topic-svc-biz/pom.xml` | surefire 3.2.5 |
| 测试 | `OpsContentMetaTest`（12→13 类契约断言 + svc 契约冻结断言）、`OpsContentServiceTest`（+5 例 svc 行为）、`ServiceFacadeServiceImplTest`（+4 例合并行为） |
| 手工验证明细 | 本文档 §5 curl 清单 |

## 4. 验收证据

| DoD 项 | 证据 |
|---|---|
| 单测绿 | 本地：cms `33/33`、topic-svc `85/85`（含新增 9 例）；CI：流水线 [2847](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/2847) **backend:build success**（2026-10-24，clean verify 真实执行两模块单测） |
| Reactor 实编两模块 | `clean verify -pl gkxlumen-cms,gkxlumen-topic-svc/gkxlumen-topic-svc-biz -am` 本地 BUILD SUCCESS；CI 同参数 |
| 无 token 401 fail-closed | 双轨配置未动（ignore-urls 不含 /cms-ops/**）；联调 curl §5.0 待 deploy:cms 后复测 |
| /api/open/** 回归 | 未触碰机器轨代码；同流水线 deploy:cms 后按 §5.0 复测 Api-Key 轨 |
| 审计一行 | `audit()` 与业务写同事务（复用未改）；单测 `svcPublishUsesSameStateMachineAndAudits` 断言 PUBLISH + entity_type=SVC_BUSINESS_DOMAIN |
| DDL 幂等 | `CREATE TABLE IF NOT EXISTS`；**未执行**（本机/跳板凭证均被 MySQL 来源 IP 白名单拒：10.253.202.239；需监管人在有权限环境跑 `db/9x_gkxlumenx_cms_ops_svc_content.sql`） |
| Part 2 合并两态（dev 实测 2026-10-24） | 网关 `http://10.50.69.111:30895`（deploy:topic-svc 已成功）：**态A** 带 org 上下文（表未建）→ `cms:{present:false, data_source:"cms:unavailable"}`，指标照常（`sz_total:14033`，HTTP 200，失败隔离 ✅）；**态B** 页级请求 → `cms:{}` 空块不出，9 区数据照常 ✅；**态C 有正文** 待 DDL+deploy:cms 后按 §5.3 补测 |

## 5. 接口设计文档（供前端叶 / 展示联调）

### 5.0 通用

- 写侧 Base：`gkxlumen-cms`，页面轨 OAuth2 Bearer（网关统一鉴权），无 token → 401 `{"code":40101,...}` fail-closed
- 响应包络：`CmsEnvelope.ok` → `{code:0, msg, data}`；错误码：40001 校验失败 / 40401 不存在或已软删 / 40901 发布冲突
- 禁写：`version`/`publish_status`/`publish_time` body 直写被忽略或 40001

### 5.1 写侧端点（/cms-ops/v1/topic-service/content/svc-business-domain）

```bash
# 新建（draft）
curl -X POST 'https://<gw>/cms-ops/v1/topic-service/content/svc-business-domain' \
  -H 'Authorization: Bearer <token>' -H 'Content-Type: application/json' \
  -d '{"org_id":"ORG-001","industry_id":"IND-01","body_html":"<p>重点机构业务服务领域介绍</p>","sort_order":1}'
# 200 data → {"content_id":"1","content_type":"svc_business_domain","page_key":"shenzhen",
#   "org_id":"ORG-001","industry_id":"IND-01","version":"0","publish_status":"draft",
#   "publish_time":null,"sort_order":1,"locale":"zh-CN","body_html":"<p>…</p>","updated_at":"…"}

# 编辑（draft/published 均可改；version 不动）
curl -X PUT '.../svc-business-domain/1' -H 'Authorization: Bearer <token>' \
  -d '{"body_html":"<p>修订后的介绍</p>"}'

# 发布（draft→published；version+1；publish_time=now）— 40901=非 DRAFT/并发抢占
curl -X POST '.../svc-business-domain/1/publish' -H 'Authorization: Bearer <token>'

# 下架（published→draft；version 保留；门户随即隐藏介绍区）
curl -X POST '.../svc-business-domain/1/unpublish' -H 'Authorization: Bearer <token>'

# 列表（draft+published 都出；三过滤可组合；page/size 分页，size≤200）
curl '.../svc-business-domain?industry_id=IND-01&org_id=ORG-001&publish_status=published&page=1&size=20' \
  -H 'Authorization: Bearer <token>'
# 200 data → {"total":1,"page":1,"size":20,"records":[ <同新建 data 形状> ]}

# 详情 / 软删
curl '.../svc-business-domain/1' -H 'Authorization: Bearer <token>'
curl -X DELETE '.../svc-business-domain/1' -H 'Authorization: Bearer <token>'
# → {"content_id":"1","deleted":true}
```

### 5.2 展示侧合并（签名不变，只增 `cms` 键）

```bash
curl -X POST 'https://<gw>/svc/topic/v1/service-portal/shenzhen' \
  -H 'Authorization: Bearer <token>' -H 'Content-Type: application/json' \
  -d '{"org_id":"ORG-001","industry_id":"IND-01"}'
# data 新增（其余字段与既有完全一致）：
#   有 published 正文: "cms": {"content_type":"svc_business_domain","present":true,"body_html":"<p>…</p>"}
#   无正文（§2.2 空态）: "cms": {"present":false}
#   cms 库故障（失败隔离）: "cms": {"present":false,"data_source":"cms:unavailable"}
#   页级请求（无 org 上下文）: "cms": {}
```

### 5.3 联调 curl 两态（DoD：有/无正文）

```bash
# 态 1 有正文：走 §5.1 建+发一条 → §5.2 请求应 present=true 且 body_html 等值
# 态 2 无正文：换一个未录入的 org_id → present=false 且不含 body_html，指标字段照常
# 态 3 隔离（可选）：cms pod 缩容 → present=false + data_source=cms:unavailable，HTTP 200，sz_total 等指标照常
```

## 6. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 调用链（前端→Java→Python /internal） | ✅ Part 2 是 Java 读侧合并（Python 底数照旧），未越层直调算法；Part 1 纯 CRUD 无算法 |
| 可观测 | ✅ 未新增绕过点；cms actuator 收敛配置未动；topic-svc 既有 tracing 配置未动 |
| demo 只读 merge（D12） | ✅ 全部在 lumen 仓，零 demo 引用 |
| 数据策略（D9） | ✅ 本单为运营正文（契约归类 `cms`），非统计指标，无 metric_id 义务；数字永走指标服务不被覆盖 |
| 禁改契约字段 | ✅ §2.1 三字段原样；page_key 枚举含 shenzhen |
| 对象存储（D14） | ✅ 不涉及 |
| 审计 | ✅ cms_op_audit 每写操作一行（CREATE/UPDATE/PUBLISH/UNPUBLISH/DELETE），operator=SecurityContext |

## 7. 待办（监管人徐滕强按序）

1. **执行 DDL**：`db/9x_gkxlumenx_cms_ops_svc_content.sql`（gkxlumenx_cms 库；幂等可重跑）。⚠️ agent 通道全被拒：本机/跳板凭证均被 MySQL 来源 IP 白名单拦（10.253.202.239 access denied），需在有权限的环境（K8s 集群内 / 运维机）执行
2. CI 流水线 [2847](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/2847)：**`deploy:cms` 是 manual 档待点击**（agent API 触发 403 无权限；`deploy:topic-svc` 已自动成功，Part 2 已上 dev）
3. curl 复测：DDL+deploy 后按 §5 清单——401 fail-closed / Api-Key 回归 / 状态机 / 审计落库 / §5.3 态C（有正文）
4. 走查核心文件（2 个）：`OpsContentType`（新枚举+族泛化）、`ServiceFacadeServiceImpl.portalShenzhen+cmsIntroBlock`
5. 走查通过后签收：registry `SYSINT-03-03A-JAVA-L01` `integration → done`（任务当前 integration 态，evidence/cost 已回填）

## 8. 成本回填（budget-estimate.md 口径）

- `actual_tokens`: ~320000（估，含救援+合并往返，retro 校准）
- `model_used`: glm-5.3（Cursor agent）
- `actual_cost`: <$3（远低于 $10 告警线）
- `cost_warn`: false
- `ponytail:` full——未新造轮子（服务/白名单/状态机/审计全复用），但按契约与 /goal 交付了 OpenAPI、审计、单测、幂等 DDL 全套，未以「更简」砍验收件
