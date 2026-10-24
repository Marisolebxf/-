# Handoff · SYSINT-03-02A-JAVA-L01 · 产业全景运营正文 · Java 运营写接口（5 个 pano_*）

> **状态**：代码冻结本地（lumen-svc-platform 主目录，**严禁自动 commit/push，停本地等 human:徐滕强 走查**）
> **日期**：2026-10-24 · **执行**：`agent:api-agent` · **监管**：`human:徐滕强`
> **契约真源**：`agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-专题全景.md`（human:淮政玮 2026-10-24 已确认，字段冻结禁改）
> **复刻样板**：SYSINT-03-01A-JAVA-L01（企业发展 12 类；模式文档 `/tmp/handoff-sysint-03-01a-enterprise-cms-pattern.md` §2 十步）
> **对接**：前端叶 SYSINT-03-02A-L01（孔东，产业介绍/发展历程接 CMS + 三块新渲染）；智树门户 Java（published 端点消费方）

---

## 1. 范围与实现（对照契约章节）

| 契约章节 | 要求 | 实现 | 产物 |
|---|---|---|---|
| §2.1 四块同构 | pano_industry_intro / pano_sz_feature / pano_cluster_effect / pano_competitive_position，字段=title(可选)+body_html(必填) | `OpsContentType` 4 个枚举（required={industry_id, body_html}，htmlFields={body_html}，OPTIONAL_TEXT={title}） | `OpsContentType.java` |
| §2.2 发展历程 | pano_dev_history：events[] 必填，每项 event_date(必填)+title(必填)+body_html(必填)+source_name(可选)+source_url(可选)，按 event_date 升序 | `PANO_DEV_HISTORY` 枚举 + `OpsContentService.validateAndSortPanoEvents()`：子字段必填校验、`events[].body_html` 过 HtmlWhitelist、按 event_date 升序排序后落 JSON 列 | `OpsContentService.java` |
| §0 公共信封 | content_id/content_type/page_key/industry_id/version/publish_status(+publish_time/sort_order/locale)；version/publish_status/publish_time 动作列禁 body 直写 | 复用 ent 族信封机制（envelope 输出 version→string、publish_status→小写、publish_time ISO-8601）；`writableFields()` 不含动作列（测试 `envelopeFieldsExcludedFromBodyActionColumns` 对 18 类断言） | 同上 |
| §0 绑定键 | industry_id（新族，非 ent enterprise_code、非 svc org_id） | 新增 `Family.PANO` 绑定族泛化：list 过滤列/envelope 输出/绑定继承按族 switch（ENT 双码/SVC org_id/PANO industry_id） | `OpsContentType.family()` + `OpsContentService` |
| §0 page_key 枚举 | panorama / overview | 新增 `PANO_PAGE_KEYS={panorama, overview}`；`pageKeys()` 按族取枚举集（pano 族用 pano 枚举，ent/svc 族原样）；DDL 默认 overview | `OpsContentType.java` |
| §3.1 读端点① | GET /api/published/topic-panorama/blocks?industry_id=必填&page_key=&content_type=&locale=（只出 PUBLISHED，空=200+blocks:[]） | `OpsContentService.publishedBlocks()` + `TopicPanoramaPublishedController.blocks()`；industry_id 缺失→40001；content_type 非 pano 族→40001（契约：无资讯类型）；空→200+`{blocks:[]}` | `TopicPanoramaPublishedController.java` |
| §3.1 读端点② | GET /blocks/{content_id}（未发布=404，不回退草稿） | `publishedBlock()`：pano 5 表逐一探测 `publish_status='PUBLISHED' AND is_deleted=0`；无命中→40401；非数字 content_id→404（不 500） | 同上 |
| 契约六动词 | list/create/update/publish/unpublish/delete | `TopicPanoramaOpsController`（/cms-ops/v1/topic-panorama/content/**，OAuth2 页面轨）复刻 `OpsContentController` 通用模式 | `TopicPanoramaOpsController.java` |
| 落库 | gkxlumenx_cms 5 张表，events 存 JSON 列，不动已冻结 DDL | `db/9x_gkxlumenx_cms_ops_pano_content.sql`：5 张 `cms_pano_*`，CREATE TABLE IF NOT EXISTS 幂等，索引 (industry_id, publish_status, is_deleted) | DDL 文件 |
| 审计 | 写操作与 cms_op_audit 同事务 | 复用 `OpsContentService.audit()`（op_type=CREATE/UPDATE/PUBLISH/UNPUBLISH/DELETE，entity_type=PANO_* 大写，operator=SecurityUtils） | 复用，零新代码 |

## 2. 偏离说明表

| # | 偏离 | 理由 | as-built |
|---|---|---|---|
| 1 | 写侧路径段用连字符（`/cms-ops/v1/topic-panorama/content/pano-industry-intro`）而 content_type 契约值是下划线 | 复刻 ent 族 `OpsContentController` 已有的 `{content_type}` 路径段风格（URL 惯例连字符），`panoOf()` 做了连字符↔下划线互转，信封 `content_type` 输出仍是契约下划线值 | 见 §4 curl；`TopicPanoramaOpsController.panoOf()` |
| 2 | 契约信封含 `publish_status=draft/archived` 三态，实现只有 DRAFT/PUBLISHED 两态 | 完全继承 ent/svc 族已评审的 MVP 状态机（draft↔published，无 archived），契约 §3.1 读侧只消费 published，三态语义不受影响 | DRAFT\|PUBLISHED；下架=published→draft |
| 3 | `publishedBlocks` 的 locale 过滤是 `=` 精确匹配而非语言族回退（zh→zh-CN） | 契约 §3.1 只说「locale 否，默认 zh-CN」，未定义回退规则；DDL 默认 zh-CN，运营不传 locale 时自然命中；ponytail：够用，加回退规则等甲方提出 | `AND locale=?`（仅显式传参才过滤） |
| 4 | published 详情端点按 pano 5 表逐一探测（最多 5 次点查） | content_id 是 cms 库自增主键，无跨表目录表；5 次索引点查在内容块量级（<<企业级）可忽略；ponytail：不为此建 content 目录表，量级上来再合并 | `publishedBlock()` 顺序探测 |
| 5 | Api-Key 机器轨扩展到 `/api/published/*`（原只挂 `/api/open/*`） | 契约 §3.1 调用方是「智树 Java」集群内服务间调用，浏览器不直连（§0.3）；不挂 Api-Key 则落到资源服务器链需 OAuth2，服务间无用户态；沿用同一 fail-closed Key（未配置=拒绝全部） | `CmsApiKeyFilterConfig.addUrlPatterns("/api/open/*","/api/published/*")` + `application.yml` ignore-urls 增 `/api/published/**` |
| 6 | events 子级多余键静默忽略（不报 40001） | 同 ent 族结构字段（modules/stages/members 等）「存 JSON 不深校验内部键」惯例；pano_dev_history 因契约显式给了子字段表才校验契约列的 3 必填 | `validateAndSortPanoEvents()` 只校验契约列 |
| 7 | 派单 §3.6 写「枚举总数=17」，实测断言为 18 | 派单撰写时未计入 SYSINT-03-03A 的 svc_business_domain（前叶已合入，改前基线=13）；12 ent+1 svc+5 pano=18 | `OpsContentMetaTest.eighteenContentTypesOneTableEach` |

## 3. 产物清单（lumen-svc-platform 主目录，未 commit）

| 文件 | 类型 | 说明 |
|---|---|---|
| `gkxlumen-cms/src/main/java/com/topcomm/gkxlumen/cms/ops/OpsContentType.java` | M | +5 枚举、Family 泛化、PANO_PAGE_KEYS/PANO_TYPES/pageKeys() |
| `gkxlumen-cms/src/main/java/com/topcomm/gkxlumen/cms/ops/OpsContentService.java` | M | list/envelope 族泛化、events 深校验+升序、publishedBlocks/publishedBlock |
| `gkxlumen-cms/src/main/java/com/topcomm/gkxlumen/cms/ops/TopicPanoramaOpsController.java` | 新增 | 写侧 7 端点（六动词+detail） |
| `gkxlumen-cms/src/main/java/com/topcomm/gkxlumen/cms/ops/TopicPanoramaPublishedController.java` | 新增 | §3.1 两个只读端点 |
| `gkxlumen-cms/src/main/java/com/topcomm/gkxlumen/cms/config/CmsApiKeyFilterConfig.java` | M | 挂 `/api/published/*` |
| `gkxlumen-cms/src/main/resources/application.yml` | M | ignore-urls 增 `/api/published/**` |
| `gkxlumen-cms/src/test/java/com/topcomm/gkxlumen/cms/ops/OpsContentMetaTest.java` | M | 13→18 断言、pano 契约断言（4 例新增） |
| `gkxlumen-cms/src/test/java/com/topcomm/gkxlumen/cms/ops/OpsContentServiceTest.java` | M | pano 行为测试（12 例新增） |
| `db/9x_gkxlumenx_cms_ops_pano_content.sql` | 新增 | 5 张表 DDL（幂等） |

**测试**：`mvn -pl gkxlumen-cms -am clean test` → **49/49 全绿**（Meta 16 + Service 33；pano 相关 16 例）。JDK 21。
**CI**：`.gitlab-ci.yml` backend:build 的 `-pl` 已含 `gkxlumen-cms`（未动 pom/CI）。

## 4. 接口设计文档（给前端叶 SYSINT-03-02A-L01 与智树门户联调）

### 4.1 写侧（页面轨，OAuth2 Bearer；运维前端用）

Base：`/cms-ops/v1/topic-panorama/content`（经网关携带 Bearer；operator 自动取当前用户）

| 动词 | 路径 | 说明 |
|---|---|---|
| POST | `/{content_type}` | 新建（draft）；content_type 路径段=连字符（如 `pano-industry-intro`、`pano-dev-history`） |
| PUT | `/{content_type}/{id}` | 编辑（draft/published 均可，version 不动） |
| POST | `/{content_type}/{id}/publish` | 发布（version+1，publish_time=now） |
| POST | `/{content_type}/{id}/unpublish` | 下架（published→draft） |
| GET | `/{content_type}?industry_id=&page_key=&publish_status=&page=&size=` | 列表（draft+published 都出） |
| GET | `/{content_type}/{id}` | 详情 |
| DELETE | `/{content_type}/{id}` | 软删 |

**四块同构请求体**（pano_industry_intro / pano_sz_feature / pano_cluster_effect / pano_competitive_position）：

```json
{
  "industry_id": "INB1701",
  "title": "产业介绍",
  "body_html": "<p>新一代信息技术产业……</p>",
  "page_key": "overview",
  "sort_order": 0,
  "locale": "zh-CN"
}
```
必填：`industry_id`、`body_html`；`title`/`page_key`/`sort_order`/`locale` 可选（page_key 默认 overview）；禁写：`version`/`publish_status`/`publish_time`（动作列，写了被白名单静默丢弃）。

**pano_dev_history 请求体**：

```json
{
  "industry_id": "INB1701",
  "events": [
    { "event_date": "2019-03-01", "title": "起步期", "body_html": "<p>首批重点企业落地</p>", "source_name": "深圳工信局", "source_url": "https://x.cn/a" },
    { "event_date": "2022-06-01", "title": "扩张期", "body_html": "<p>产业集群规模破千亿</p>" }
  ]
}
```
每项必填 `event_date`(yyyy-MM-dd)/`title`/`body_html`；可选 `source_name`/`source_url`；服务端自动按 event_date 升序归一落库（前端无需预排）。HTML 约束同 §0（段落/标题/列表/引用/加粗/链接/图片 URL；禁 script/iframe/事件属性/javascript:）。

**统一响应信封**（create/update/publish/unpublish/detail 返回）：

```json
{
  "code": 0, "msg": "ok",
  "data": {
    "content_id": "5", "content_type": "pano_industry_intro", "page_key": "overview",
    "industry_id": "INB1701", "version": "1", "publish_status": "draft",
    "publish_time": "2026-10-24T17:30:00", "sort_order": 0, "locale": "zh-CN",
    "title": "产业介绍", "body_html": "<p>……</p>"
  }
}
```
错误：40001（必填缺失/HTML 违禁/page_key 越界/events 子字段缺失）、40401（不存在/软删）、40901（发布/下架状态冲突）。

**curl 示例（写侧）**：

```bash
# 新建发展历程草稿
curl -X POST "$GW/cms-ops/v1/topic-panorama/content/pano-dev-history" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"industry_id":"INB1701","events":[{"event_date":"2019-03-01","title":"起步","body_html":"<p>落地</p>"}]}'

# 发布（version+1）
curl -X POST "$GW/cms-ops/v1/topic-panorama/content/pano-industry-intro/5/publish" -H "Authorization: Bearer $TOKEN"

# 列表（只看已发布）
curl "$GW/cms-ops/v1/topic-panorama/content/pano-industry-intro?industry_id=INB1701&publish_status=published" -H "Authorization: Bearer $TOKEN"
```

### 4.2 published 只读（机器轨，X-CMS-Api-Key；智树门户 Java 用，浏览器不直连）

| 动词 | 路径 | 行为 |
|---|---|---|
| GET | `/api/published/topic-panorama/blocks?industry_id=必填&page_key=&content_type=&locale=` | 只出 PUBLISHED；空=200+`{blocks:[]}` |
| GET | `/api/published/topic-panorama/blocks/{content_id}` | 未发布/软删/不存在=404，不回退草稿 |

**blocks 元素** = §4.1 信封（publish_status 恒为 `published`）。过滤参数：`page_key`∈{panorama,overview}、`content_type`∈pano 5 类（其他值 40001）、`locale` 精确匹配。

**curl 示例（读侧）**：

```bash
# 某产业全部已发布块（门户装配 overview 页）
curl "$CMS/api/published/topic-panorama/blocks?industry_id=INB1701" -H "X-CMS-Api-Key: $KEY"
# → {"code":0,"msg":"ok","data":{"blocks":[{content_id,content_type:pano_industry_intro,…},{content_type:pano_dev_history,events:[…]}]}}

# 只要产业介绍块
curl "$CMS/api/published/topic-panorama/blocks?industry_id=INB1701&content_type=pano_industry_intro" -H "X-CMS-Api-Key: $KEY"

# 空态（该产业未发布任何块）→ 200 {"blocks":[]}
# 详情未发布 → 404 {"code":40401,"msg":"CMS_NOT_FOUND: topic-panorama#5","data":null}
# 缺 industry_id → 400 {"code":40001,"msg":"industry_id 必填（契约 §3.1）"}
# 无/错 Key → 401 {"code":40101,"msg":"CMS_AUTH_FAILED"}
```

**DWD/ADS 展示侧既有接口（/ln、/ln/kpi、/ln/news、/panorama/snapshot）签名零改动**——前端叶渲染指标数字仍走原接口，CMS 块走本 handoff 端点。

## 5. DoD 逐条证据

| DoD（registry） | 证据 |
|---|---|
| gkxlumen-cms 新增 5 个 pano_* content_type 的 list/create/update/publish，正文落 gkxlumenx_cms，真源零写，操作写 cms_op_audit | `OpsContentType` 5 枚举+`TopicPanoramaOpsController` 7 端点；DDL 5 张 `cms_pano_*` 表（`USE gkxlumenx_cms`）；数据源=cmsJdbcTemplate（gkxlumenx_cms 库），无任何 DWD 写路径；`audit()` 与业务写同 @Transactional，测试 `panoPublishUsesSameStateMachineAndAudits` 断言恰好一行 PUBLISH 审计 |
| OpenAPI + 请求/响应示例入 handoff，供 SYSINT-03-02A-L01 前端叶联调 | 本文档 §4（swagger 注解已带 @Operation/@Parameter，/v3/api-docs 可出 OpenAPI） |
| 契约转正后字段不回改；转正前以草案字段为准开发，待确认项标记在 handoff | 契约 2026-10-24 已由 human:淮政玮 确认（非草案）；本叶零契约字段改动（偏离表 §2 全为实现层决策，不改字段语义）；无待确认项 |

## 6. 架构合规自检

| 铁律 | 结论 | 说明 |
|---|---|---|
| 调用链（前端→Java REST→Python /internal） | ✅ | 本叶纯 Java+MySQL（CMS 运营正文，无算法成分）；published 端点消费方=智树门户 Java（集群内），链路：浏览器→门户 Java→CMS Java `/api/published/**`（X-CMS-Api-Key），不越层 |
| D9 指标血缘 | ✅ | CMS 正文不含计算数字（契约 §0.2/§1.3：企业数/机构数/区域分布全走指标服务）；本叶零 metric 交互、零编造数字；pano 页指标缺口（深圳各区计数无 metric_id）已在契约 §1.3 记录，非本叶范围 |
| D12 demo 隔离 | ✅ | 只写 lumen-svc-platform 与 gkxlumenx_cms；零 demo-* 依赖、零 merge |
| 真源 DWD 零写入 | ✅ | 全部 SQL 打 cms_pano_*（gkxlumenx_cms）+ cms_op_audit；测试 `publishedBlocksEmptyYields200WithEmptyArray` 断言绝不查 cms_ent_/cms_svc_（更无 dwd） |
| 鉴权双轨隔离 | ✅ | 写侧 /cms-ops/** OAuth2（fail-closed）；读侧 /api/published/** Api-Key（fail-closed，未配置 Key=全拒）；互不复用路径 |
| 审计 | ✅ | 六动词全部落 cms_op_audit（op_type 大写动作、entity_type=PANO_*、snapshot_before 整行镜像、operator=SSO 用户） |
| 禁改配置铁律 | ✅ | 未动 .gitignore/pom/CI（`-pl` 已含 gkxlumen-cms）；application.yml 仅按任务要求加 ignore-urls 一行 |

## 7. cost 四字段

| 字段 | 值 |
|---|---|
| actual_tokens | ≈ 189,000（含输入缓存） |
| model_used | glm-5.3（Cursor agent） |
| actual_cost | ≈ $4.1 |
| cost_warn | false（< $10 阈值） |

`ponytail: full`

## 8. 走查指引（给 human:徐滕强）

核心只读两个文件（其余是复用样板）：
1. `OpsContentType.java`——pano 5 枚举 + `Family` 泛化（本叶唯一元数据改动面）
2. `OpsContentService.java`——`validateAndSortPanoEvents()`（events 深校验）+ `publishedBlocks()/publishedBlock()`（§3.1 两端点）+ list/envelope 三处族 switch

验证命令：
```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home
mvn -pl gkxlumen-cms -am clean test   # 期望 49/49 绿
```

DDL 执行（部署时）：`db/9x_gkxlumenx_cms_ops_pano_content.sql`（幂等可重跑；自检 `SHOW TABLES LIKE 'cms_pano_%';` 期望 5 张）。

## 9. 待办交接

- 走查通过后由监管人推送（commit 文案建议：`feat(cms): 专题全景 pano 族 5 类运营写接口 + §3.1 published 只读端点（SYSINT-03-02A-JAVA-L01） [agent:api-agent]`）→ push origin/dev → 盯 CI backend:build → 执行 DDL → deploy:cms → handoff §4.2 curl 复测（401 fail-closed / blocks 空态 / 404 详情 / 状态机 / 审计落库）
- 前端叶 SYSINT-03-02A-L01（孔东）按 §4.1 对接运维编辑页、门户侧按 §4.2 装配
- 本叶不做：前端渲染（02A-L01）、指标图谱数字（02B）、产业资讯（02C，读 `dwd_industry_chain_news_info` 不进 CMS）
