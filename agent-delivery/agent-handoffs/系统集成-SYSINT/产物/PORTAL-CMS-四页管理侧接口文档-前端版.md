# 门户内容管理四页 · CMS 管理侧接口文档（前端版）

> **给谁**：Java 侧（CMS 写接口实现）+ 契约确认会
> **来源**：按 `lumen-ui-topic` @ `1ffebf5`（2026-11-03）四页前端**实际功能**整理；字段真源 = `src/components/cms/cmsTypeSchema.ts` + 各 workspace 组件
> **对照文档**：`agent-handoffs/专题对齐-TOPIC/门户内容管理-四页前端实现对照.md` v1.5（24/24 达成，D-1～D-8 全闭环）
> **既有契约**：`平台基建-PLATFORM/产物/PORTAL-CMS-*.md`（企业发展已确认；全景/政策/服务草案）；写侧动作语义沿用 `SYSINT-03-03A-接口文档-前端版.md` Part A（`svc_business_domain` 已在 dev 实现）
> **范围**：**管理侧（内容运营）写/查接口** + 前端已依赖的既有查询接口。门户展示侧读接口（`/published/*`）不在本文，见各契约 §4。
> **日期**：2026-11-03 · 整理 `agent:frontend-agent`

---

## 0. 通用约定

| 项 | 值 |
|---|---|
| 鉴权 | OAuth2 Bearer（网关统一鉴权；无 token 401 fail-closed） |
| 响应包络 | `{code:0, msg:"…", data:{…}}` |
| 错误码 | `40001` 字段校验失败（msg 含字段名）/ `40401` 不存在或已软删 / `40901` 发布冲突（并发或状态机不符） |
| 发布状态机 | `draft` ⇄ `published`；publish 时 `version+1`、`publish_time=now`；unpublish 回 draft，version 保留 |
| HTML 白名单 | 段落/标题/列表/引用/加粗/链接/**图片 URL**；禁 `script`/`iframe`/`on*` 事件属性/`javascript:` 协议（含实体编码），命中 `40001`；图片链接只收 http(s) URL，不收二进制 |
| 审计（建议） | 信封增 `operator`（服务端从 token 取，body 传入忽略），补齐 X-8 追溯缺口 |

**前端调用路径（2026-11-04 定稿）**：前端 axios（baseURL=`/api`）实际请求写

```
/api/cms/cms-ops/v1/topic-cms/{module}/{content_type}/...
```

拆解：`/api`（30892 nginx 剥掉）→ `/cms`（30895 网关 StripPrefix=1 剥掉，久新同轨路由）→ 服务内 `/cms-ops/v1/**`。**本文下文所有端点均写服务内路径 `/cms-ops/v1/**`，前端拼调用时在前面加 `/api/cms` 即可**；与其他模块（`/api/{enterprise|chain|svc|policy}/topic/v1/**`）不同，CMS 多一段 `/cms`（久新联调路由转正式，`FE-TOPIC-NGINX-CMS-PREFIX-L01` 2026-11-04 实证可达）。

---

## 1. 通用 CRUD 端点（全部 content_type 同一套动作）

路由前缀建议：`/cms-ops/v1/topic-cms/{module}/{content_type}`，`module ∈ enterprise | panorama | service | policy`。
已实现的 `svc_business_domain` 沿用既有路径 `/cms-ops/v1/topic-service/content/svc-business-domain`（语义相同，不必迁移）。

| # | 动作 | 端点 | 说明 |
|---|---|---|---|
| A1 | 新建草稿 | `POST /cms-ops/v1/topic-cms/{module}/{content_type}` | body = §2 该类型字段；`version=0`、`publish_status=draft` |
| A2 | 编辑 | `PUT …/{content_type}/{content_id}` | draft/published 均可改；`version` 不动；至少带一个可写字段 |
| A3 | 发布 / 下架 | `POST …/{content_id}/publish` / `…/unpublish` | 状态机不符 `40901`；发布时服务端复跑 §5 校验 |
| A4 | 列表 | `GET …/{content_type}?…` | draft+published 都出；筛选见下 |
| A5 | 详情 / 删除 | `GET/DELETE …/{content_type}/{content_id}` | 删除=软删，响应 `{"content_id":"…","deleted":true}` |

**A4 列表通用查询参数**：

| query | 必填 | 说明 |
|---|---|---|
| `industry_code` | 是 | 企业模块字段名 `future_industry_code`，其余模块 `industry_id` |
| `publish_status` | — | `draft` / `published`（不传=全部） |
| `enterprise_code` | — | 绑企业的类型过滤 |
| `org_id` | — | 绑机构的类型过滤 |
| `keyword` | — | 按类型 `titleFieldKeys` 模糊（各类型字段表「检索」列） |
| `page` / `size` | — | 默认 1 / 20，size ≤ 200 |

**响应信封**（A1/A2/A3/A5-detail 出参，各类型在其上扩展 §2 字段）：

```json
{ "content_id":"…", "content_type":"…", "module":"enterprise", "page_key":"star",
  "future_industry_code":"integrated-circuit", "enterprise_code":"ENT-0001", "org_id":null,
  "title":"…", "version":"3", "publish_status":"published", "publish_time":"2026-11-03T10:00:00+08:00",
  "sort_order":1, "locale":"zh-CN", "updated_at":"2026-11-03T10:00:00", "operator":"…" }
```

A4 出参：`data = {total, page, size, records:[<信封+类型字段>]}`，按 `sort_order` 升序。

**前端形态映射**：前端 mock 存 `fields{}`（标量）+ `rows[]`（行数组）；接口出参按 §2 结构化字段给，前端接线层做 `fields/rows ↔ 结构化` 互转，不影响接口形状。

---

## 2. 参数定义 · 按 content_type（34 类）

图例：**绑定** = 除产业外额外绑定维度；**检索** = A4 keyword 命中字段；**正文** = `body_html`（HTML 白名单）；「行编辑」类型的多行结构 = 前端 `CmsRepeatRows` 表格，增删改整行。

### 2.1 企业发展（16 类 · 菜单「企业发展内容管理」`EnterpriseCmsWorkspace.vue` 五屏）

绑定列统一 `future_industry_code`，下表只写差异绑定。

| content_type | 名称 | 绑定 | 结构化字段（▶=行编辑数组） | 检索 | 页面位置 |
|---|---|---|---|---|---|
| `ent_basic_profile` | 基础档案 | +企业 | `founded_date`(date,必) `industry_label`(enum: ic/ai/bio/new-energy/new-material/high-end-equipment/other,必) `scale_label`(enum: large/medium/small/micro,必) `staff_size`(text) `address_text`(text) + 正文 | 企业 | 屏2 编辑 Tab「基础档案」 |
| `ent_honor_list` | 资质荣誉 | +企业 | ▶`honors[]`: `honor_name`(必) `honor_level`(enum: national/province/city/other) `honor_year` `honor_remark` | 企业 | 屏2 Tab「资质荣誉」 |
| `star_roster_item` | 明星名单 | +企业 | `selection_tag`(必) `selection_reason`(必) `list_published`(bool,必) `basic_intro_published`(bool,必) `standard_ref`(string,见 §4-3) `display_alias`(text) | 标签/企业/理由 | 屏2 Tab「明星名单」 |
| `star_selection_standard` | 入选标准 | 产业 | `standard_name`(必) `standard_version`(必) `candidate_scope_text` `applicable_industry_codes`(string,逗号分隔,必) `confirmed_dimensions`(string) `std_updated_at`(date,必) | 标准名/版本 | 屏5「入选标准」 |
| `star_product_panorama` | 产品全景 | +企业 | `product_id`(必) `product_name`(必) `product_summary`(必) `impact_summary` ▶`modules[]`: `module_name`(必) `module_summary`；**多条/企业，`sort_order` 支持上移下移** | 产品名 | 屏2 Tab「产品」 |
| `star_tech_narrative` | 技术优势 | +企业 | 正文（核心技术/原理/成果简介） | 企业 | 屏2 Tab「技术优势」 |
| `star_team_strength` | 团队实力 | +企业 | 正文（团队多维展示 HTML） | 企业 | 屏2 Tab「团队与人才」 |
| `star_scientist_ratio` | 科学家比例 | +企业 | `ratio_percent`(number 0–100,必) `data_time`(date,必) `team_achievement` ▶`members[]`: `member_name`(必) `title`(必) `publish_status`(enum: published/draft,必) `portrait_authorization_status`(enum: authorized/pending/unavailable/no_asset,必) `external_link_authorization_status`(同前,必) | 企业 | 屏2 Tab「团队与人才」下半区 |
| `star_story` | 成长轨迹 | +企业 | `reputation`(text,每行一段) ▶`timeline[]`: `year`(必) `title`(必) `summary`(必) | 企业 | 屏2 Tab「成长轨迹」 |
| `key_chain_structure` | 链位结构 | 产业 | `structure_version`(必) ▶`stages[]`: `stage_code`(必,唯一) `stage_name`(必) `upstream_of`(string[],逗号拼接→数组) `narrative`(必)。**环节字典唯一真源（D-8）** | 版本 | 屏3「重点企业全景图」→Tab「链位结构」 |
| `key_enterprise_set` | 重点企业集 | 产业 | ▶`key_set_items[]`: `enterprise_code`(必) `stage_code`(必,须在 stages 字典) `relation_type`(enum: cooperation/supply_chain/competition,必) `related_enterprise_code`(org_id,可空) `relation_text`(必) `sort_order`(int,必)。**唯一写入口（D-6），企业编辑链位 Tab 只读** | — | 屏3→Tab「重点企业集」 |
| `ent_rank_dimension` | 榜单维度 | 产业 | `rank_type`(enum: tech/business,必) `dimension_name`(必) `dimension_meaning`(必) `weight_percent`(number %) | 维度名/榜单类型 | 屏4「榜单」下半区 |
| `ent_competitive_rank` | 技术力商业力榜单 | 产业 | `rank_type`(必) `enterprise_code`(org_id,必) `rank_no`(int 1–30,必) `rank_basis`(必) `expert_comment` | 企业/名次 | 屏4 榜单条目 |
| `sz_enterprise_intro` | 深圳介绍 | 产业(+企业可空) | `positioning`(必) `advantage_summary` `expert_analysis` | 定位 | 屏2 Tab「深圳介绍」 |
| `sz_focus_set` | 深圳重点圈定 | 产业 | ▶`focus_set_items[]`: `enterprise_code`(必) `sort_order`(int,必)。**上移/下移后整表重编号提交** | — | 屏3→Tab「深圳重点圈定」 |
| `display_name_alias` | 展示别名 | +企业 | `display_alias`(必,界面标明非法定名称) | 别名 | 屏2 Tab「明星名单」内 |

### 2.2 产业全景（7 类 · 菜单「产业全景内容管理」`PanoramaCmsWorkspace.vue` 列表 7 状态块 + 编辑 7 Tab）

绑定统一 `industry_id`；带 `title`(栏目标题) 字段的类型可改名。

| content_type | 名称 | 结构化字段 | 检索 | 页面位置 |
|---|---|---|---|---|
| `pano_industry_intro` | 产业介绍 | `title` `dev_stage`(enum: emerging/growing/mature/transforming) `positioning`(text) `core_advantage` `innovation_highlight` `main_challenge`（三摘要 textarea）+ 正文 | 标题 | 列表块「产业介绍」→Tab 1 |
| `pano_sz_feature` | 深圳特色 | `title` + 正文 | 标题 | 块「深圳特色」→Tab 2 |
| `pano_cluster_effect` | 集群效应 | `title` + 正文 | 标题 | 块「集群效应」→Tab 3 |
| `pano_competitive_position` | 竞争地位 | `title` + 正文 | 标题 | 块「竞争地位」→Tab 4 |
| `pano_dev_history` | 发展历程 | ▶`events[]`: `event_date`(date,必) `title`(必) `body_html`(html,必) `expert_opinion`(textarea) `source_name` `source_url` | — | 块「发展历程」→Tab 5 |
| `pano_sz_metrics` | 本地产业数据 | ▶`metrics[]`: `metric_name`(必) `metric_value`(必) `unit` `data_year` `remark` | — | 块「本地数据」→Tab 6 |
| `pano_chain_graph` | 产业链图谱 | ▶`nodes[]`: `node_name`(必,唯一) `stage`(enum: 上游/中游/下游,必) `mark`(enum: ''/key/bottleneck/active) `note`(textarea)；`edges[]`: `source`(节点名,必) `relation`(enum: upstream/downstream/peer/related,必) `target`(节点名,必) | — | 块「产业链图谱」→Tab 7（左编辑右 G6 预览） |

### 2.3 产业服务（7 类 · 菜单「产业服务内容管理」`ServiceCmsWorkspace.vue` 四屏）

绑定 `industry_id`，绑机构的类型另加 `org_id`。

| content_type | 名称 | 绑定 | 结构化字段 | 检索 | 页面位置 |
|---|---|---|---|---|---|
| `svc_business_domain` | 业务领域介绍 | +机构 | 正文（**已有接口**，DoD 校验见 §5） | 机构 | 屏2 机构编辑 Tab 1 |
| `svc_org_profile` | 全球服务机构概况 | +机构 | `founded_date`(date) `service_type`(enum: incubator/testing/consulting/other,必) + 正文（专家综合评估） | 机构 | 屏2 Tab 2「全球概况」 |
| `svc_org_distribution` | 产业区域分布 | +机构 | ▶`distributions[]`: `industry_name`(必) `region`(string,"/"分隔四级 label 路径如 `全国/广东省/深圳市/南山区`,必) `relation_desc`(必) | 机构 | 屏2 Tab 3「产业区域分布」 |
| `svc_rank_dimension` | 技术力维度 | 产业 | `dimension_name`(必) `dimension_meaning`(必) `weight_percent`(number %) | 维度名 | 屏3「技术力 Top30 榜单」下半区 |
| `svc_tech_rank` | 技术力 Top30 | 产业 | `rank_no`(int 1–30,必) `org_id`(必) `rank_basis`(必) `expert_comment` `service_case`(textarea) | 机构/名次 | 屏3 榜单条目 |
| `sz_svc_profile` | 深圳服务产业档案 | 产业 | `domain_label`(必) ▶`orgs[]`: `org_name`(必) `service_type`(enum 同上,必) `industry_coverage`(必) | 领域 | 屏4「深圳服务产业」档案表 |
| `sz_svc_competitiveness` | 服务产业竞争力 | 产业 | `domain_label`(必) `strength_summary`(必) `bottleneck_summary`(必) `potential_summary`(必) | 领域 | 屏4 竞争力表 |

### 2.4 政策新闻（4 类 · 菜单「政策新闻内容管理」`PolicyNewsCmsPage.vue` 三屏）

绑定统一 `industry_id`。

| content_type | 名称 | 结构化字段 | 检索 | 页面位置 |
|---|---|---|---|---|
| `policy_news_body` | 最新政策与时效 | `policy_title`(必) `issuer`(必) `doc_no` `scope_text`(必) `classify_by`(enum: industry/region/theme,必) `classify_value`(必) `validity_status`(enum: effective/upcoming/repealed,必) + 正文（政策原文） | 标题/文号/发布单位 | 屏1「政策本体」 |
| `policy_news_stats` | 概况与地理分布 | `summary_text`(必) `keywords`(必) `analysis_conclusion` ▶`regions[]`: `region`(同 2.3 四级路径,必) `association_note`(必) | 摘要/关键词 | 屏2「统计与区域」 |
| `policy_intensity_dimension` | 力度评估维度 | `dimension_name`(必) `dimension_meaning`(必) | 维度名 | 屏3「力度评估」维度块 |
| `policy_intensity_rank` | 政策力度榜单 | `rank_no`(int,必,Top10) `policy_name`(必) `rank_basis`(必) `expert_comment` `recommend_reason`(必) | 政策名/名次 | 屏3 榜单块 |

---

## 3. 前端已依赖的既有接口（不新做，联调确认可用）

| # | 接口 | 用途 | 调用点 |
|---|---|---|---|
| D1 | `POST /svc/ent/v1/search/suggest`（`entSearchSuggest`，入参 `{prefix, size?}`，出参 `[{org_id, name_cn}]`） | 全部 `ent-select` 企业字段（基础档案/榜单/深圳介绍/明星名单/别名/关系对象）+ KeySet 弹窗 + 深圳圈定联想添加 | `CmsScalarField.vue`、`EnterpriseCmsKeySetTab.vue` |
| D2 | `POST /svc/ent/v1/search/meta/region-scopes`（`entSearchMetaRegionScopes`，`{mode:"tree", include_members:true}`，出参树形 `items[]`） | `region` 类型字段四级级联（服务分布/政策地理），30min sessionStorage 缓存，失败回退本地树 | `CmsScalarField.vue` ← `useEntRegionScopesStore` |
| D3 | 产业选项接口（既有 `meta/chains` 或等价） | 产业下拉/切换（当前 mock 3 产业，接主数据后替换） | 四页筛选区 `CmsIndustrySwitch` |

环节字典（D-8）不单开接口：`stages` 选项由前端从 `key_chain_structure` A4 列表推导。

---

## 4. 与既有契约的差异（契约确认会须逐条拍板）

| # | 差异 | 现契约 | 前端现状（本文口径） |
|---|---|---|---|
| 1 | **7 类新类型无契约**：`pano_sz_metrics`、`pano_chain_graph`、`svc_org_profile`、`svc_org_distribution`、`svc_rank_dimension`、`svc_tech_rank`、`sz_svc_profile`、`sz_svc_competitiveness`（8 类） | 无对应 | 按 §2 新增（D-1/D-2 拍板产物） |
| 2 | **3 组字段缺口**：`pano_industry_intro` 的 `dev_stage/positioning/三摘要`；`pano_dev_history` 的 `expert_opinion`；`policy_intensity_rank` 的 `rank_no`（政策契约整个无 CMS 细型） | 草案无这些字段 | 按 §2 补 |
| 3 | `standard_ref` 取值 | 契约指向 `content_id` | 前端改「产业:标准名」稳定键（X-5 修复），旧 contentId 兼容回显；契约确认后二选一冻结 |
| 4 | `key_enterprise_set` 关系字段 | 契约 `key_set_items` 仅 `relation_text` | 需规 324(1) 要求合作/供应链/竞争三态，前端加 `relation_type` + `related_enterprise_code`，契约需同步 |
| 5 | `ent_basic_profile` / `ent_honor_list` 边界 | 契约口径：法定名称/资质走主数据与指标，CMS 不覆盖 | 前端作为 CMS 可编辑块（运营补录档案字段）。需拍板：CMS 值是「补录」还是「覆盖」，门户读侧优先级 |
| 6 | `svc_business_domain` 路径 | 已上线 `/cms-ops/v1/topic-service/content/svc-business-domain` | 保持不动；其余 33 类是否统一进新前缀由实现定 |

---

## 5. 服务端校验汇总（发布动作必跑；前端已做同款，服务端为最后防线）

| 校验 | 类型 |
|---|---|
| Top30 上限：同产业同榜单 `rank_no ≤ 30`，名次唯一，同企业/机构不重复上榜 | `ent_competitive_rank`、`svc_tech_rank` |
| 环节码必须在同产业 `key_chain_structure.stages` 字典内 | `key_enterprise_set.stage_code` |
| `stage_code` 字典内唯一 | `key_chain_structure` |
| 图谱：节点名唯一非空；边端点必须是已建节点；禁自环 | `pano_chain_graph` |
| 行编辑类型发布时必填行齐全（如荣誉/历程/分布/档案至少一行且必填列满） | 各 ▶ 行类型 |
| HTML 白名单（§0） | 全部含正文的类型 |
| DoD 正文模式：分数/名次/领导人/法定代表人字样不进正文（命中 40001） | `svc_business_domain` |
| `region` 值必须是合法四级路径（服务端可按 region-scopes 字典校验） | `svc_org_distribution`、`policy_news_stats` |

---

**ponytail**: off —— 接口需求文档，完整性优先。
