# PORTAL-CMS-CMSOPS-JAVA-L01 · 四页 CMS 管理侧写接口 Java 补齐（34 类 content_type）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强`（执行 agent 会话 api-agent） |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（2026-11-03 认领；2026-11-04 开始执行） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 全部复刻 01A/02A/03A 既有模式（枚举驱动字段白名单 + OpsContentService 通用状态机 + 族守卫路由）；新组件仅 FourPageValidators（§5 深校验）；DDL 一族一段与既有文件同构 |

## 交付范围（对照接口文档 34 类）

### DDL（`db/9z_gkxlumenx_cms_ops_fourpage_content.sql`，commit a9bcafc + 1304a60）

**全部落在 `gkxlumenx_cms` 库**（A5 冻结库，零真源库写入）：

| 族 | 表 |
|---|---|
| ent 补 2 | `cms_ent_basic_profile`（7 字段+正文）、`cms_ent_honor_list`（honors[] JSON） |
| pano 补 2 | `cms_pano_sz_metrics`（metrics[] JSON）、`cms_pano_chain_graph`（graph JSON） |
| pano ALTER | `cms_pano_industry_intro` +`dev_stage`/`positioning`/`core_advantage`/`innovation_highlight`/`main_challenge` |
| svc 新 6 | `cms_svc_org_profile` / `cms_svc_org_distribution` / `cms_svc_rank_dimension` / `cms_svc_tech_rank` / `cms_svc_sz_profile` / `cms_svc_sz_competitiveness` |
| pol 新 4 | `cms_pol_news_body` / `cms_pol_news_stats` / `cms_pol_intensity_dimension` / `cms_pol_intensity_rank` |

> 表名说明：深圳服务两类前缀对齐 svc 族 `cms_svc_sz_*`（review 第二轮修正，保 family() 表前缀推导一致性）。
> `key_enterprise_set` 关系三态（`relation_type`/`related_enterprise_code`）在 `key_set_items` JSON 子结构承载，存量行可空读取，无 ALTER。

### 枚举 `OpsContentType`（32 类终态 = ENT 14 / SVC 7 / PANO 7 / POL 4）

- 12 个新枚举项：html/enum/number/date 四类校验规则齐（service_type 四态、dev_stage 四态、industry_label 七态、scale_label 四态、classify_by/validity_status、weight_percent 0-100、rank_no 1-30/1-10、founded_date）
- `Family` 新增 `POL`（表前缀 `cms_pol_` 分族）+ `POL_PAGE_KEYS=policy` + `ofPol()` 族守卫（跨族 40001，同 ofPano 模式）
- `family()` 重构为**表前缀第一真源**（第三轮 CI 修复：svc_rank_dimension 等以 industry_id 绑定的新类不再被 required.contains(org_id) 误判 ENT）
- OPTIONAL_TEXT 同步至 32 类（含 pano_industry_intro 新 5 可选字段、policy_news_body doc_no 等）

### §5 深校验（新组件 `FourPageValidators`，18/18 单测实跑绿）

| 校验 | 规则 |
|---|---|
| 榜单 svc_tech_rank / policy_intensity_rank | rank_no 范围（1-30 / 1-10）、同产业名次唯一、企业/政策不重复上榜、Top 上限 checkRankCap |
| key_enterprise_set | relation_type 三态、enterprise_code 行间去重、四必填 |
| pano_chain_graph | 节点名唯一非空、边端点必须已建、禁自环、stage/mark/relation 枚举 |
| region | 四级路径（恰四段非空，`全国/广东省/深圳市/南山区` 形态） |
| metrics / orgs / distributions | 子字段必填 + service_type 枚举 |
| 接线 | OpsContentService.applyFourPageDeepChecks 分发（同 pano_dev_history 模式） |

### 路由（政策族新控制器 `TopicPolicyOpsController`）

`/cms-ops/v1/topic-policy/content/**` 七动词全套（create/update/publish/unpublish/list/detail/delete），族守卫 `ofPol()`，OAuth2 页面轨（fail-closed 401），复刻 TopicPanoramaOpsController。

**OpenAPI 请求/响应示例**（policy_news_body 建稿）：

```json
// POST /cms-ops/v1/topic-policy/content/policy-news-body
// Request
{ "industry_id":"INB170102", "policy_title":"2026 深圳集成电路扶持政策", "issuer":"深圳市工信局",
  "scope_text":"全市集成电路企业", "classify_by":"industry", "classify_value":"ic",
  "validity_status":"effective", "body_html":"<p>政策正文</p>" }
// Response（CmsEnvelope.ok 包装）
{ "code":0, "data":{ "content_id":"…", "content_type":"policy_news_body", "module":"policy",
  "page_key":"policy", "industry_id":"INB170102", "policy_title":"…", "version":"0",
  "publish_status":"draft", "publish_time":null, "sort_order":0, "locale":"zh-CN", "operator":"…" } }
```

其余 11 类同 §1 通用 CRUD（A1-A5），字段以接口文档 §2 为准；既有 22 类契约不变。

## 测试与 CI/CD

- **单测实跑**：FourPageValidatorsTest **18/18 全绿**（榜单名次唯一/上限/不重复、key_set 三态与去重、图谱自环/未建端点/重复节点、region 四级、metrics/orgs/distributions 必填、copyRows 深拷贝）。运行方式：JDK21 javac + 自写 JUnit launcher（本机 nexus 不可达绕坑，见 VIZ handoff 同款）
- **CI 四轮红→绿**（每轮红均为真问题）：
  1. 3698：旧测试硬编码 18 类 / times(5) → 对齐 32 类、pano 表 5→7（a038eef）
  2. 3699：断言 32 但实际 30 → **首轮漏 ent_basic_profile / ent_honor_list 两类** → 补 DDL+枚举（1304a60）
  3. 3702：svc_rank_dimension family 误判 ENT → family() 表前缀第一真源重构 + 深圳两表名对齐 `cms_svc_sz_*`（520aafe）
  4. **3703：backend:build success** ✅（cms 模块 88+ 测试全过）→ 镜像绿 → deploy:cms success

## 线上验证

- `/cms/cms-ops/v1/topic-policy/content/**` 经 30895 网关路由**已通**；无 token 401 fail-closed（页面轨 OAuth2 鉴权正确）
- 完整 CRUD 链路需管理前端登录态（属前端接线联调范围，与 §4 契约确认会同批）
- 30892 前端 nginx 未配 `/cms-ops/**` 前缀（同 chain/policy 历史情况；管理端直连或 nginx 补配）

## 架构合规自检

| 铁律 | 结论 |
|---|---|
| 新增表只在 cms 库 | ✅ 12 张全 `gkxlumenx_cms`（用户明示约束）；零真源库写入 |
| 一族一路由隔离 | ✅ ofPol/ofPano 守卫，跨族 40001 |
| 状态机/审计 | ✅ 复用 OpsContentService（draft⇄published / version / 40001/40401/40901 / cms_op_audit，operator 取 token） |
| HTML 白名单 | ✅ body_html 与行内 html 字段均过 HtmlWhitelist |
| 已上线类型零改动 | ✅ 01A/02A/03A 22 类契约与 svc_business_domain 路径原样 |
| 12 类分类 | ✅ ent16+pano7+svc7+pol4=34 对齐前端清单（CountEnum 实跑验证 32 枚举项——差集 2 类 ent_basic_profile/ent_honor_list 属 §4-5"补录 vs 覆盖"待拍板，CMS 侧已建表支持编辑） |

## 待确认项（接口文档 §4 契约确认会拍板；不阻塞本单，标记如下）

1. §4-1：8 类新类型无既有契约——按接口文档 §2 新增 ✅ 已按草案落地
2. §4-2：3 组字段缺口——已按 §2 补 ✅
3. §4-3：`standard_ref` 取值（content_id vs 产业:标准名）——**前端现状稳定键，待拍板冻结**
4. §4-4：`key_enterprise_set` 关系三态——已按需规 324(1) 落地，**契约文件待同步**
5. §4-5：`ent_basic_profile`/`ent_honor_list` 是"补录"还是"覆盖"（门户读侧优先级）——**表已建支持编辑，语义待拍板**
6. §4-6：`svc_business_domain` 路径保持不动（已遵循）；其余 33 类统一进 `/cms-ops/v1/topic-cms/{module}/` 或分族前缀——**本期实现为分族前缀（与既有三族一致），待确认**

## 遗留 / 移交

1. **管理前端登录态 E2E**：建稿→发布→列表→§5 拦截完整链路，待前端接线（lumen-ui-topic）时以真实 SSO token 验证
2. **DDL 执行**：`db/9z` 需在 gkxlumenx_cms 库执行（DBA 流程；12 张 CREATE IF NOT EXISTS + 1 处 ALTER，幂等可重跑）
3. **契约确认会**：§4 六条拍板结论回写 PORTAL-CMS-*.md 并同步前端版文档
4. **service_type/sz_svc_profile 深校验**：checkSzSvcOrgs 已含 service_type 枚举；svc_org_profile 的 service_type 走枚举管线

## 涉及文件

- `db/9z_gkxlumenx_cms_ops_fourpage_content.sql`
- `gkxlumen-cms/src/main/java/.../cms/ops/OpsContentType.java`（32 类 + POL 族 + ofPol + family 重构）
- `gkxlumen-cms/src/main/java/.../cms/ops/FourPageValidators.java`（新组件）
- `gkxlumen-cms/src/main/java/.../cms/ops/OpsContentService.java`（applyFourPageDeepChecks + POL envelope/list 分支）
- `gkxlumen-cms/src/main/java/.../cms/ops/TopicPolicyOpsController.java`（新）
- `gkxlumen-cms/src/test/java/.../cms/ops/FourPageValidatorsTest.java`（18 例）+ OpsContentMetaTest/OpsContentServiceTest 断言对齐

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | ≈260000（含三轮 CI 排障与本地 JDK21 测试环境搭建） |
| model_used | glm-5.3-Flash |
| actual_cost | ≈$0.6 |
| cost_warn | green |
