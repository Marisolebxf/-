# SYSINT-03-01A-JAVA-L01 · Handoff · 企业发展内容管理 Java 运营写接口

> **🔍 走查指引（给 human:徐滕强）**：核心逻辑只在 `ops/OpsContentType.java`（185 行，12 类字段规则表）与
> `ops/OpsContentService.java`（sanitize 校验 / CRUD / 状态机 / 审计，401 行）；
> `OpsContentController`（105 行）纯路由。改动 diff 仅 5 处（CI `-pl` 加 cms / pom surefire / 启动类注解 /
> yml ignore-urls / 删 permitAll 链配置），`git diff` 5 分钟可过。单测 23 例即行为规格说明。
> 已知取舍见 §1 偏离表 7 条（重点 #3 std_updated_at 改名、#6 删 permitAll 链的理由）。
> **回归面已核实**：单体 boot 不依赖 cms（pom/源码零引用），资源服务器链只影响 gkxlumen-cms 独立部署；
> 机器轨久新回归只读 5 处 diff 即可确认（Api-Key 过滤器代码零改动）。

> **任务**：SYSINT-03-01A-JAVA-L01（`task_type=feature`，E-PM-DELIVERY）
> **执行**：`agent:api-agent` · **监管/签收**：`human:徐滕强`
> **仓库**：`${GKX_ROOT}/repos/lumen-svc-platform`（origin/dev）· 模块 `gkxlumen-cms`
> **日期**：2026-10-23 · **强度**：ponytail full
> **契约真源**：`agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-企业发展.md`（已确认，字段禁改——本实现零改契约字段）
> **前端联调叶**：SYSINT-03-01A-L01（孔东线，lumen-ui-topic）

---

## 1. 范围与实现

供智树运维页面（lumen-ui-topic）编辑/发布企业发展 12 类正文。已拍板决策全部落地：

| 决策 | 实现 |
|---|---|
| 1. 挂 gkxlumen-cms，新建 OpsController 与久新接口分开 | `ops/OpsContentController`，前缀 `/cms-ops/v1/enterprise/content/**`；`/api/open/**` 零改动 |
| 2. 双轨鉴权 | 启动类加 `@EnableGkxlumenResourceServer`（对齐 gkxlumen-topic-enterprise）；`/api/open/**` 进 `security.oauth2.client.ignore-urls` 白名单保 Api-Key 轨；其余路径 Bearer fail-closed（OpaqueTokenIntrospector） |
| 3. 正文落 gkxlumenx_cms overlay | 12 张独立表 `cms_ent_{content_type}`（DDL 见 §5）；A5 冻结文件 `9x_gkxlumenx_cms.sql` 一字未动；真源零写 |
| 4. 草稿 MVP | `draft`（新建/编辑）→ `published`（发布 version+1）→ 下架回 `draft`；无版本历史、无审核流 |
| 5. 全部写操作记 cms_op_audit | 复用 `OverlayDao.audit()`（A5-7 冻结列），op_type=`CREATE/UPDATE/PUBLISH/UNPUBLISH/DELETE`，operator 取 SecurityContext（SSO 简化 principal 的 username=`systemCode:clientId`，introspector v1 契约） |

**实现形态（契约字段直译 + 元数据驱动）**：`OpsContentType` 枚举是 12 类字段的唯一真源（表名/必填/HTML/枚举/数值/日期规则），`OpsContentService` 一个服务跑全部 CRUD+发布，**零重复 controller/service 12 份**；子结构（modules/media_refs/timeline/stages/key_set_items/focus_set_items/members）按仓内惯例存 JSON 列（不拆子表，MVP）。

### 关键设计取舍（偏离说明）

| # | 偏离/取舍 | 理由 | as-built |
|---|---|---|---|
| 1 | `publish_status` 库内存 `DRAFT/PUBLISHED`（大写），接口层输出契约小写 `draft/published` | 与仓内 audit op_type 大写惯例一致；接口出参严格契约 | `OpsContentService.envelope()` |
| 2 | `version` 库内 int 自增，接口输出字符串（契约 `version: string`） | 契约信封类型保真 | 同上 |
| 3 | 契约 §2.2 `updated_at`（标准更新时间）落列名 `std_updated_at` | 避开 A5 宽表族审计列 `updated_at` 冲突；接口仍输出 `std_updated_at`（前端按契约 §2.2 行名对齐时注意：**此列 JSON 键为 std_updated_at**） | DDL 2.2 |
| 4 | HTML 白名单实现为黑名单拦截（禁 script/iframe 族/事件属性/javascript: 协议），非解析器白名单 | 契约 §0 只明令禁三类；ponytail 不引入新依赖；将来要严格白名单换 OwASP Sanitizer（留有 `ponytail:` 注释） | `ops/HtmlWhitelist` |
| 5 | 新增契约六动词之外的可选 DELETE（软删） | 运维误建数据清理用；审计照记；可忽略不用 | `OpsContentController#delete` |
| 6 | 删除 `CmsSecurityPermitAllConfig`（原 anyRequest permitAll 链） | 该链 order=HIGHEST_PRECEDENCE 会压死资源服务器链，导致页面轨无 token 也放行——**正是本叶要修的 fail-closed 前提** | 双轨文档挪至启动类 javadoc |
| 7 | `surefire` 3.2.5 加在 gkxlumen-cms 模块 pom（不动根 pom） | Maven 3.8 默认 surefire 2.12.4 不认 JUnit5，单测会被静默跳过；仓内既有测试（async-service）实际也未被执行——本叶只修本模块 | gkxlumen-cms/pom.xml |

## 2. 双轨鉴权（DoD 1）

- **机器轨（不破坏久新）**：`/api/open/**` 加 ignore-urls 白名单 → 资源服务器链 permitAll → `CmsApiKeyFilterConfig`（servlet Filter order=1）`X-CMS-Api-Key` fail-closed 校验，行为与改前完全一致（过滤器先行于 DispatcherServlet，且未动它的任何代码）。
- **页面轨（新建）**：`/cms-ops/**` 不在白名单 → `authenticated()` + `OpaqueTokenIntrospector`（`sso.enabled=true` 走统一用户中心 1.3 check-token；按请求头 `systemCode` 路由 app）。无 token / 无效 token → **401 fail-closed**（`ResourceAuthExceptionEntryPoint`）。
- **部署要求（⚠️ 联调前确认）**：Nacos `application-dev.yml` 需含 `sso:` 块（userCenterUrl/tenantId/apps，gkxlumen-topic-enterprise 现网同款）——cms 模块此前无资源服务器，属新增依赖配置。**本地 application.yml 不含 sso 块（真源在 Nacos，凭证不进 git）**。
- **Redis 连接（同源继承）**：资源服务器的 Redis 授权服务 Bean（common-data 自动装配）需要 `spring.data.redis.*`——与 topic-enterprise 同源，经 Nacos 全局 `application-dev.yml` 继承，本服务 yml 无需单独配。若 cms Pod 起不来报 Redis 连接类错误，先查全局配置。
- **网关路由（已有，无需新增）**：`db/9x_gkxlumenx_sys_route_conf_cms.sql`（2026-10-23 human:徐滕强 批准的久新联调临时路由）`/cms/** → lb://gkxlumen-cms`，全局 StripPrefix=1。据此：页面轨外部路径 `/cms/cms-ops/v1/**` → 服务内 `/cms-ops/v1/**`（fail-closed）；机器轨外部 `/cms/api/open/**` → `/api/open/**`（白名单+Api-Key）。⚠️ 该路由注释声明"联调结束删除"；页面轨长期路由注册属 WBS-03-18 收口，届时另立正式路由。

## 3. 接口契约（12 类通用 + 6 动词）

12 个 `content_type`（=路由路径段=审计 entity_type 小写化）：
`star_roster_item` / `star_selection_standard` / `star_product_panorama` / `star_tech_narrative` / `star_team_strength` / `star_story` / `key_chain_structure` / `key_enterprise_set` / `sz_enterprise_intro` / `sz_focus_set` / `display_name_alias` / `star_scientist_ratio`

| 动词 | 路径 | 语义 |
|---|---|---|
| POST | `/cms-ops/v1/enterprise/content/{content_type}` | 新建（draft） |
| PUT | `/cms-ops/v1/enterprise/content/{content_type}/{id}` | 编辑（version 不动） |
| POST | `/cms-ops/v1/enterprise/content/{content_type}/{id}/publish` | 发布（version+1，publish_time=now；仅 DRAFT 可发） |
| POST | `/cms-ops/v1/enterprise/content/{content_type}/{id}/unpublish` | 下架（回 draft；仅 PUBLISHED 可下） |
| GET | `/cms-ops/v1/enterprise/content/{content_type}?page_key=&future_industry_code=&enterprise_code=&publish_status=&page=&size=` | 列表（draft+published 都出；分页 ≤200） |
| GET | `/cms-ops/v1/enterprise/content/{content_type}/{id}` | 详情 |
| DELETE | `/cms-ops/v1/enterprise/content/{content_type}/{id}` | 软删（可选，运维清理） |

**公共信封出参**（契约 §0）：`content_id` / `content_type` / `page_key` / `future_industry_code` / `enterprise_code` / `version`(string) / `publish_status`(小写) / `publish_time` / `sort_order` / `locale` / `updated_at` + 各类业务字段（snake 原名，JSON 列回对象/数组）。
**body 可写字段** = 契约业务字段 ∪ `page_key`/`sort_order`/`locale`；`version`/`publish_status`/`publish_time` 禁写（40001）。
**空态**（契约 §2.13）：列表无记录返回 `records: []`，文案由前端渲染——接口不做空态文案。
**§3 团队块下发规则**（两枚授权均 authorized 且 published 才出 body_html）与 **§2.14 成员行过滤**：属**读接口**（任欢侧 §4.1/§4.2 或门户 /portal/v1）的语义，本叶是运营写接口不做下发过滤；写侧已把 `portrait_authorization_status`/`external_link_authorization_status` 落为独立列（DDL 2.5）与 members 行字段（DDL 2.14），读侧可直接按列过滤。

### 请求/响应示例（前端联调依据）

**① 新建团队实力（draft）**

```http
POST /cms-ops/v1/enterprise/content/star_team_strength
Authorization: Bearer <token>
Content-Type: application/json

{
  "enterprise_code": "ENT-0001",
  "future_industry_code": "integrated-circuit",
  "page_key": "star",
  "sort_order": 1,
  "body_html": "<p>核心成员介绍…</p><img src=\"https://cdn.example.com/team.png\">",
  "portrait_authorization_status": "authorized",
  "external_link_authorization_status": "authorized"
}
```

```json
{ "code": 0, "msg": "ok", "data": {
  "content_id": "1", "content_type": "star_team_strength",
  "page_key": "star", "future_industry_code": "integrated-circuit", "enterprise_code": "ENT-0001",
  "version": "0", "publish_status": "draft", "sort_order": 1, "locale": "zh-CN",
  "updated_at": "2026-10-23T16:20:00",
  "body_html": "<p>核心成员介绍…</p><img src=\"https://cdn.example.com/team.png\">",
  "portrait_authorization_status": "authorized", "external_link_authorization_status": "authorized"
} }
```

**② 违禁 HTML 拒绝（40001）**

```json
{ "code": 40001, "msg": "字段 body_html 含 HTML 违禁内容（script/iframe/事件属性/脚本协议），契约 §0 白名单禁止", "data": null }
```

**③ 发布（version+1）**

```http
POST /cms-ops/v1/enterprise/content/star_team_strength/1/publish
```

```json
{ "code": 0, "msg": "ok", "data": { "content_id": "1", "version": "1", "publish_status": "published",
  "publish_time": "2026-10-23T16:25:00", "…": "…" } }
```

**④ 科学家比例（§2.14 表单）**

```http
POST /cms-ops/v1/enterprise/content/star_scientist_ratio
```

```json
{
  "enterprise_code": "ENT-0001",
  "ratio_percent": 38,
  "data_time": "2026-07-14",
  "team_achievement": "团队成果说明",
  "members": [
    { "member_name": "核心成员 A", "title": "首席科学家 / 技术负责人",
      "publish_status": "published", "portrait_authorization_status": "authorized",
      "external_link_authorization_status": "no_asset" }
  ]
}
```

`ratio_percent=138` → `40001 "ratio_percent 须在 0–100"`；`data_time: "07/14/2026"` → `40001 日期格式非法`。

**⑤ 列表（含分页）**

```http
GET /cms-ops/v1/enterprise/content/star_roster_item?future_industry_code=integrated-circuit&publish_status=published&page=1&size=20
```

```json
{ "code": 0, "msg": "ok", "data": { "total": 12, "page": 1, "size": 20, "records": [ { "content_id": "5",
  "content_type": "star_roster_item", "enterprise_code": "ENT-0001", "future_industry_code": "integrated-circuit",
  "selection_tag": "…", "selection_reason": "…", "list_published": true, "basic_intro_published": true,
  "standard_ref": "3", "display_alias": "…", "version": "2", "publish_status": "published",
  "publish_time": "2026-10-23T10:00:00", "sort_order": 1, "locale": "zh-CN",
  "updated_at": "2026-10-23T10:00:00" } ] } }
```

**⑥ 未带 token（fail-closed）**

```json
HTTP 401
{ "code": 401, "msg": "访问令牌不存在", "data": "…path…" }
```

**⑦ 未知 content_type / 状态机违规**

```json
{ "code": 40001, "msg": "未知 content_type: foo_bar", "data": null }
{ "code": 40001, "msg": "仅 DRAFT 可发布（当前 PUBLISHED）", "data": null }
```

**OpenAPI**：服务启动后 `http://gkxlumen-cms:7098/v3/api-docs`（tag=`cms-ops-enterprise-content`）；`/api/open/**` 既有 tag 不受影响。

## 4. DoD 自检（架构合规）

| DoD 项 | 证据 | 状态 |
|---|---|---|
| OpsController 全通；无 token 401 fail-closed | 资源服务器链 authenticated()（common-security），本机编译绿；401 形状见示例⑥；**K8s dev 部署后按 §7 curl 清单复测** | ✅ 代码级 / ⏳ 联调级 |
| /api/open/** Api-Key 轨回归不破坏久新 | 过滤器代码零改动；路径进 ignore-urls 后仍被过滤器 fail-closed 拦截（两层顺序：安全链先 permitAll、Filter 后拦截） | ✅ 代码级 / ⏳ 联调级 |
| 12 类 CRUD+发布/下架全通 | `OpsContentType` 12 枚举 = 契约 12 类（脚本断言枚举↔DDL↔契约三方一致）；状态机/sanitize/审计调用链行为测试（mock JdbcTemplate） | ✅ 单测 23/23 绿（元数据 11 + 服务行为 12） |
| cms_op_audit 每写操作一行 | 复用 `OverlayDao.audit()`（A5-7 列），`@Transactional` 与业务写同事务 | ✅ |
| OpenAPI + 示例入 handoff | §3 七组示例 + springdoc tag | ✅ |
| CI backend:build 绿且 Reactor 实编 gkxlumen-cms | `.gitlab-ci.yml` `-pl` 列表已加 `gkxlumen-cms`；本机 `mvn compile -pl gkxlumen-cms -am` 绿 | ✅ 推送后看流水线 |
| 新增表 DDL 入 db/（gkxlumenx_cms） | `db/9x_gkxlumenx_cms_ops_ent_content.sql`（12 表，幂等 CREATE IF NOT EXISTS） | ✅ |
| 架构铁律 | 调用链：lumen-ui-topic → 网关 → gkxlumen-cms → gkxlumenx_cms；Java 无算法/nGQL/ADS 写；demo2 只读未动；D12 合规（全部 gkxlumen-*） | ✅ |

## 5. 产物清单

| 文件 | 动作 | 说明 |
|---|---|---|
| `db/9x_gkxlumenx_cms_ops_ent_content.sql` | 新增 | 12 张表 DDL（契约 §2.1–2.14 直译；子结构 JSON；幂等） |
| `gkxlumen-cms/src/main/java/.../ops/OpsContentType.java` | 新增 | 12 类元数据与校验规则唯一真源 |
| `gkxlumen-cms/src/main/java/.../ops/HtmlWhitelist.java` | 新增 | 契约 §0 HTML 白名单校验 |
| `gkxlumen-cms/src/main/java/.../ops/OpsContentService.java` | 新增 | CRUD+publish/unpublish+软删+审计（12 类通用） |
| `gkxlumen-cms/src/main/java/.../ops/OpsContentController.java` | 新增 | `/cms-ops/v1/**` 七端点（springdoc 注解） |
| `gkxlumen-cms/src/main/java/.../GkxlumenCmsApplication.java` | 修改 | +`@EnableGkxlumenResourceServer`（双轨 javadoc） |
| `gkxlumen-cms/src/main/java/.../config/CmsSecurityPermitAllConfig.java` | **删除** | permitAll 链压死资源服务器链（偏离表 #6） |
| `gkxlumen-cms/src/main/resources/application.yml` | 修改 | +`security.oauth2.client.ignore-urls`（机器轨白名单+actuator+swagger） |
| `gkxlumen-cms/pom.xml` | 修改 | +surefire 3.2.5（偏离表 #7）；**common-security 依赖本已存在，未加** |
| `gkxlumen-cms/src/test/java/.../ops/OpsContentMetaTest.java` | 新增 | 契约元数据/白名单/状态机单测 11 例 |
| `gkxlumen-cms/src/test/java/.../ops/OpsContentServiceTest.java` | 新增 | 服务层行为测试 12 例（mock JdbcTemplate：sanitize 校验/状态机/审计链/动作列禁写） |
| `db/check_ops_ent_ddl.sh` | 新增 | DDL 烟测脚本（scratch 库用完即删；凭证走环境变量；验证语法/幂等/12 表/最小 INSERT/状态机 SQL） |
| `.gitlab-ci.yml` | 修改 | backend:build `-pl` +`gkxlumen-cms`（DoD 实编） |

## 6. 部署顺序（给 devops/监管人）

1. **先执行 DDL**：`db/9x_gkxlumenx_cms_ops_ent_content.sql`（10.50.11.76 / gkxlumenx_cms；幂等可重跑）
   - 可选预检：`db/check_ops_ent_ddl.sh`——在 scratch 库（`gkxlumenx_cms_ddlcheck`，用完自动删，不触碰真实库）验证 DDL 语法/幂等/12 表/最小 INSERT/状态机 SQL。用法：`MYSQL_HOST=… MYSQL_USER=… MYSQL_PWD=… bash db/check_ops_ent_ddl.sh`（凭证经环境变量，不落盘）
2. Nacos `application-dev.yml` 确认 `sso:` 块对 cms 生效（§2 部署要求）
3. 推送 origin/dev → CI `backend:build` 绿 → `deploy:cms`（单服务热更即可，不必 helm:deploy 全家桶）
4. 联调复测 §7 清单

### 验收后 commit message（已预置，copy 即用）

```
[agent:api-agent] feat(cms): 企业发展内容管理运营写接口（SYSINT-03-01A-JAVA-L01）

- ops/ 四件套：12 类 content_type CRUD+publish/unpublish（契约字段直译，OpsContentType 元数据驱动）
- 双轨鉴权：/api/open/** 保 Api-Key（ignore-urls 白名单）；/cms-ops/** 走 OAuth2 资源服务器（fail-closed）
- 删除 CmsSecurityPermitAllConfig：permitAll 链会压死资源服务器链
- 12 张 cms_ent_* 独立表 DDL（db/9x_gkxlumenx_cms_ops_ent_content.sql）+ 烟测脚本
- 写操作记 cms_op_audit（operator=SecurityContext）；HTML 白名单（§0）
- CI backend:build -pl 纳入 gkxlumen-cms；模块 surefire 3.2.5（JUnit5）
- 单测 23 例全绿；任务 SYSINT-03-01A-JAVA-L01（监管 human:徐滕强）
```

## 7. 联调 curl 清单（K8s dev，待跑）

```bash
# 网关路由：/cms/** → lb://gkxlumen-cms（StripPrefix=1，2026-10-23 徐滕强批准临时路由）
BASE=https://<网关地址>/cms
TOKEN=<统一用户中心 bearer>

# 401 fail-closed
curl -s -o /dev/null -w "%{http_code}\n" $BASE/cms-ops/v1/enterprise/content/star_team_strength   # 期望 401
# Api-Key 轨回归（久新不破坏）
curl -s -o /dev/null -w "%{http_code}\n" -H "X-CMS-Api-Key: $KEY" $BASE/api/open/cms/v1/enterprise/list -X POST -H 'Content-Type: application/json' -d '{"page":1,"size":1}'   # 期望 200（code=0）
# 全链路：建→发→下架→审计
# ① POST body 见示例① → content_id
# ② POST .../{id}/publish → version=1
# ③ POST .../{id}/unpublish → publish_status=draft
# ④ mysql: SELECT op_type,business_id,operator FROM cms_op_audit WHERE entity_type='STAR_TEAM_STRENGTH' ORDER BY id DESC LIMIT 3;  → CREATE/PUBLISH/UNPUBLISH 三行
```

## 8. 遗留与交接给前端叶（SYSINT-03-01A-L01）

- `std_updated_at` 键名（偏离表 #3）请前端按此对齐入选标准（§2.2）表单
- 列表 `records[]` 元素与详情同构（信封+业务字段），可直接复用同一渲染器
- 空态文案（契约 §2.13）由前端渲染：接口空集合即显示对应文案
- 网关页面轨路由：临时联调路由 `/cms/**` 已覆盖（§2）；长期正式路由与统一用户中心菜单角色名：**还没有**（属 WBS-03-18 收口范围）
- **契约校验全覆盖**：body 侧 `page_key` 枚举（§0）与 `sort_order` 整数校验已补（非法值 40001，不再落 DB 报 50001）；全量 Reactor verify 绿（cms [29/46]）

### 8.1 企业维度管理列表接口（前端设计文档 · 列表半边，用户拍板 2026-10-24 并入本叶）

**用途**：运维列表页主数据源。主体=企业（dwd 真实 ∪ cms 虚拟，软删剔除，同 v_cms_ent 口径）；`blocks` = 该企业在 12 类 content_type 下的内容块状态摘要（按 draft/published 计数），供列表渲染「已配置哪些块、发布没发布」及「点开企业→编辑字段」导航。

```http
GET /cms-ops/v1/enterprise/content/enterprise-summary?keyword=芯&page=1&size=20
```

```json
{ "code": 0, "msg": "ok", "data": {
  "total": 1, "page": 1, "size": 20,
  "records": [ {
    "enterprise_code": "ENT-0001",
    "name": "深芯微电子",
    "blocks": {
      "star_roster_item":       { "published": 1 },
      "star_team_strength":     { "published": 2 },
      "sz_enterprise_intro":    { "draft": 1 }
    }
  } ]
} }
```

说明：`blocks` 里**没出现的 content_type = 该企业未配置**（前端显示「未配置」引导新建）；keyword 空查全量；分页 ≤200。

### 8.2 bugbot 修复记录（两轮，全部修复）

| 轮次 | Findings | 修复 |
|---|---|---|
| 一轮（2026-10-24 12:03） | HIGH roster 表缺 page_key 列；MEDIUM 状态机竞态；LOW HTML 黑名单基础绕过 | DDL 补列（建表前零迁移）；publish/unpublish 改原子条件 UPDATE+影响行数检查（0 行抛 40901）；正则补 / 属性分隔+实体解码 |
| 二轮（2026-10-24 14:05 总审转介） | HTML5 无分号数字实体（`&#106avascript:`）+ scheme 夹 tab（`java&#9;script:`）绕过；契约 §2.2 `updated_at` 改名 `std_updated_at` 无映射（前端传参静默丢弃+审计列冒名输出）；烟测脚本 `WHERE id=5` 硬编码脆弱假绿 | 解码按 HTML5 十进制前缀解析（不吞字母）+ check 三遍检测（原文/解码/解码剥 tab·换行·CR）；`OpsContentType.COLUMN_ALIASES` 映射 + required 纳入 + sanitize/envelope 双向走映射，行审计时间不再冒名输出；脚本改 `MAX(id)` 动态引用 + bash 终态/审计断言 |

最终回归：`Tests 27/27 BUILD SUCCESS`。两轮修复均已推送（`aa5df80` pipeline 2830 绿、`e5c6d3b` pipeline 2841 backend:build success）。

### 8.3 WBS 待登记（用户拍板 2026-10-24）

| 事项 | 状态 |
|---|---|
| 前台查询合并单（Python/ADS 底数 + cms published 覆盖，接口签名不动，cms 挂=老数据兜底） | 待登记 WBS（SYSINT-03 维），归属 topic-enterprise 门面层，需架构师圈范围 |

**修订记录**

| 版本 | 日期 | 作者 | 说明 |
|---|---|---|---|
| 8.1 | 2026-10-24 | api-agent | 企业维度管理列表接口并入本叶（列表半边）；新增 `GET /enterprise-summary`；单测 23→25 |
| 8.2 | 2026-10-24 | api-agent | bugbot 一轮三修；单测 25→26 |
| 8.3 | 2026-10-24 | api-agent | bugbot 二轮三修（HTML5 解码/updated_at 映射/烟测脚本断言）；单测 26→27 |
| 8.4 | 2026-10-24 | api-agent | 主仓 reset 丢失恢复：§8.1–8.3 重建（内容同前） |

---

**ponytail**: full——契约字段直译无删减；12 类元数据驱动零重复代码；HTML 校验黑名单有注释升级路径；无多余抽象（单 controller/service/enum 三件套）。
**架构合规自检**：§2 铁律逐条 ✅（见 §4 末行）；D12：全部在 lumen 仓与 gkxlumenx_cms，零 demo 依赖。
**本 handoff 遵循**：`agent-delivery/templates/handoff-template.md` 章节（范围/偏离/产物/证据/合规）。
