# CMS-JX 接口规格书（原型冻结版 v1.5）

> **定位**：`CMS-JX-INT` epic 全部 CRUD 开发单的**需求规格唯一真源**。实现 agent 只读本规格书 + 所依赖设计单，**禁止自行解读原型**。
> **依据**：原型 https://kejizhuantifuwu.netlify.app（2026-10-15 抓取版：`base-data-page.js` / `kg-mgmt-page.js` / `expert-knowledge-page.js`）+ 久新 2026-10-15 确认的范围口径（三模块全做，原型为准）。
> **边界**：本规格覆盖基础数据管理、全要素图谱管理、专家知识管理三模块；可视化管理与门户内容管理**不在本期**（对应 7 张只读单已打顺延 note）。
> **冲突裁决**：路径语法与 overlay 表结构如与 `CMS-JX-OVERLAY-A5-L01` 冻结版冲突，以 A5 为准并回改本规格；其余内容以本规格为准。
> **维护**：改需求改本文件一处，19 张工单同时生效；修订须注明日期与原因。

---

## 0. 通用约定（全部工单适用）

### 0.1 访问与鉴权（继承老设计单 CMS-JX-INT-DESIGN-L01，不重复设计）

| 项 | 约定 |
|---|---|
| 前缀 | `/api/open/cms/v1/*`，仅集群内 ClusterIP Service `gkxlumen-cms`，网关不注册路由 |
| 鉴权 | 请求头 `X-CMS-Api-Key`（nacos 加密配置，401 `CMS_AUTH_FAILED`） |
| 操作人 | 请求头 `X-CMS-Operator`（操作人姓名/账号；缺省记 `unknown`）——审计四件套的数据来源 |
| 模块 | 全部接口落 `lumen-svc-platform` 的 `gkxlumen-cms` 模块 |
| 限流 | 每接口默认阈值 TBD（压测后回填）；超限 429 `CMS_RATE_LIMITED` |
| 可观测 | OTel 全埋点（`OTEL_SERVICE_NAME=gkxlumen-cms`），trace 头透传 |

### 0.2 响应信封与错误码（PigX `R<T>` 惯例）

```json
// 成功
{ "code": 0, "msg": "ok", "data": { ... } }
// 列表
{ "code": 0, "msg": "ok", "data": { "total": 123, "page": 1, "size": 20, "records": [ ... ] } }
// 失败
{ "code": 40001, "msg": "删除被引用：该企业被 3 条动态资讯关联", "data": null }
```

| 错误码 | HTTP | 语义 |
|---|---|---|
| 0 | 200 | 成功 |
| 40001 `CMS_BAD_PARAM` | 400 | 参数缺失/格式错（msg 指明字段） |
| 40101 `CMS_AUTH_FAILED` | 401 | API Key 无效 |
| 40401 `CMS_NOT_FOUND` | 404 | 业务 ID 不存在或已软删 |
| 40901 `CMS_DELETE_REFUSED` | 409 | 删除被引用（`data.reasons` 列出引用来源与数量） |
| 42901 `CMS_RATE_LIMITED` | 429 | 限流 |
| 50001 `CMS_QUERY_FAILED` | 5xx | 真源/overlay 查询失败 |

### 0.3 分页/搜索/排序（对齐原型列表交互）

| 参数 | 约定 |
|---|---|
| `page` / `size` | 从 1 起；`size` 默认 20、max 100（原型 8/页是前端展示值，非接口约束） |
| `keyword` | 名称/标题模糊搜索（原型全局搜索框的行为收敛到主名称字段；各节标注命中字段） |
| 筛选参数 | 各节按原型列表页实际有的筛选器列明；原型没有的不做 |
| `sort` | 可选，`field,asc|desc`；默认各节注明 |

原型通用行为：**列表默认不返回已软删记录**（对应原型"录入状态=有效"默认态）。

### 0.4 overlay 读写语义（核心，全工单一致）

| 语义 | 规则 |
|---|---|
| **编辑真源实体** | 只写 `cms_entity_overlay.field_overrides`（JSON 字段级 diff merge）；**真源表永远不动**。响应返回更新时间 |
| **读视角（join）** | 列表/详情 = 真源 LEFT JOIN overlay，逐字段 `COALESCE(overlay.field, 真源列)`；未覆盖字段真源更新**自动透传** |
| **虚拟实体** | 新增时 `source_id=NULL`，业务 ID 规则 `cms:{TYPE}-{uuid8}`（如 `cms:ENT-a1b2c3d4`），防撞真源 `org_id`/`policy_id` |
| **软删** | `DELETE` 语义 = `is_deleted=1` + 审计行；不物理删。真源实体软删后视角列表不再返回该行 |
| **删除引用检查** | 被动态资讯/专项/图谱关系/专家知识等 overlay 内容引用时返回 40901，`data.reasons: [{"type":"ent_news","count":3}]` |
| **审计** | 所有写操作（新增/编辑/软删/标记断裂/状态标记）写 `cms_op_audit`：`op / reason / operator(X-CMS-Operator) / snapshot(变更前 JSON 镜像) / op_time` |

### 0.5 真源表名说明（A5 定稿：读正式表，v1.3 纠偏）

CMS 读侧统一读**正式库 `gkxlumenx_dwd`** 的项目 DWD 契约表：`enterprise_base`（企业主数据）、`policy_base_info`（政策）、`industry_chain` / `industry_chain_node`（产业链）、`enterprise_industry_product`（产品名称）；服务机构圈定池 `svc_org_circle`（demo 期 `demo_gkxlumenx_dwd`）。**禁止**引用供应方 ODS 命名（`dwd_org_base_info` / `dwd_policy_base` / `dwd_industry_chain_info`）——那是入站层表名，**实际上线读正式表**（human:徐滕强 2026-10-15 纠偏拍板）。映射一律按列名书写（`org_id`/`name_cn`/`external_id`/...），实现不得自行二选一。overlay 三件套落**业务库 `gkxlumenx_cms`**（A5-1），禁入 DWD/ADS。

### 0.6 端点动词约定（v1.2 定稿：全 POST + JSON Body，human:徐滕强 2026-10-15 拍板）

> **语法铁律**：全 epic 统一 `POST`；**禁止路径参数**——资源地址一律为不带动态段的固定路径，业务 `id`、筛选、分页、`reason` 等全部走 JSON body（下拉 suggest 简单关键词可用 query params）。与久新原评估「全 POST 复用专题现成封装」一致；老设计单 §5.2 十六只读接口登记表**同步改写**（见 §7.1 映射表，A5 落笔）。

| 操作 | 动词与路径 | body 要点 |
|---|---|---|
| 列表 | `POST /api/open/cms/v1/{resource}/list` | keyword/筛选/分页/排序 |
| 详情 | `POST /api/open/cms/v1/{resource}/detail` | `{ "id": "..." }` |
| 下拉 | `POST /api/open/cms/v1/{resource}/suggest` | `{ "keyword": "", "limit": 10 }`（读侧老单已建，不重复） |
| 新增 | `POST /api/open/cms/v1/{resource}/create` | 全量可填字段；虚拟实体 ID 服务端生成 |
| 编辑 | `POST /api/open/cms/v1/{resource}/update` | `{ "id": "...", ...被改字段 }`（字段级 diff merge 进 overlay） |
| 删除 | `POST /api/open/cms/v1/{resource}/delete` | `{ "id": "...", "reason": "必填" }`（软删+审计） |
| 专用动作 | `POST /api/open/cms/v1/{resource}/{action}` | 如 relations 的 `break`、webhook 等少数语义端点 |

---

## 1. 基础数据管理 · 企业

### 1.1 CMS-JX-ENT-CRUD-L01 · 企业实体写侧

原型面板：`base-data-page.js` → enterprise → ontology → `ent-base`。

**端点**：`POST /api/open/cms/v1/enterprise/create`、`POST /api/open/cms/v1/enterprise/update`（body 含 id）、`POST /api/open/cms/v1/enterprise/delete`（body 含 id+reason）。读侧升级：`CMS-JX-ENT-LIST-L01` 的列表/详情数据源改为 §0.4 join 视角。

**编辑弹窗字段**（新增=全部可填；编辑=真源只读字段回显+可覆盖字段提交）：

| 字段 | 原型标签 | 类型 | 必填 | 枚举/说明 | 落位 |
|---|---|---|---|---|---|
| id | 唯一 ID | string | 是 | 真源实体=org_id（只读回显）；虚拟=`cms:ENT-{uuid8}` 服务端生成 | overlay.source_id / key |
| name | 企业名称 | string | 是 | 真源 `name_cn`；覆盖写 `field_overrides.name` | 真源列 / overlay |
| regInfo | 工商注册信息 | textarea | 否 | 运营整理的工商摘录 | overlay.reg_info |
| founded | 成立时间 | date | 否 | 真源 `incorporation_date` 只读回显；虚拟实体填 `field_overrides.founded` | 真源列 / overlay |
| capital | 注册资本 | string | 否 | 真源 `registered_capital_value`+`capital_currency` 回显；覆盖写 overlay | 真源列 / overlay |
| type | 企业类型 | select | 否 | 高新技术企业/专精特新/上市公司/初创企业——**运营分类标签**，非工商 org_type | overlay.ent_type |
| industry | 所属行业 | select | 否 | 人工智能/生物医药/高端装备/新能源——运营标签；真源国标行业列只读回显（另列） | overlay.industry_tag |
| scale | 规模 | select | 否 | 大型/中型/小型；真源 `org_size` 优先，覆盖写 overlay | 真源列 / overlay.scale |
| isKey | 是否为重点企业 | select | 否 | 是/否 | overlay.is_key |
| flag | 重点企业标识 | select | 否 | 龙头/潜力/观察/风险关注 | overlay.key_flag |
| priority | 优先级 | select | 否 | P0/P1/P2/P3 | overlay.priority |
| reason | 标识原因 | textarea | 否 | — | overlay.flag_reason |

**列表列**（join 视角输出顺序）：id、name、founded、capital、type、scale、industry、isKey、flag、priority。
**列表筛选**：`keyword`（命中 name）、`is_key`、`key_flag`、`priority`、`page/size`；默认按 name 升序。
**只读回显附加字段**（详情接口额外返回，编辑弹窗不可改）：`external_id`（统一社会信用代码）、`province/city/area`、`org_type`（工商登记类型）、`industry_l1_name`~`l4_name`（国标行业）、`reg_status`。
**引用检查**：被 `ent_news.company` / `ent_sz.name` / 图谱关系（from/to）/ 专家知识（entity）引用时拒绝软删，40901。

### 1.2 CMS-JX-ENT-NEWS-L01 · 企业动态资讯

原型面板：`ent-news`。纯 overlay 内容表。

**端点**：`POST /api/open/cms/v1/enterprise/news/list | /detail | /create | /update | /delete`。

| 字段 | 原型标签 | 类型 | 必填 | 枚举/说明 |
|---|---|---|---|---|
| title | 标题 | string | 是 | keyword 命中字段 |
| company | 关联企业 | string[]（多选） | 是 | 原型=可搜索多选下拉，选项源=企业实体（含虚拟）；存 org_id 数组，响应回显名称列表 |
| kind | 类型 | select | 否 | 新闻公告/财报摘要/法律诉讼/行政处罚/舆情事件 |
| content | 内容摘要 | textarea | 是 | 列表 2 行截断（前端行为，接口返回全文） |
| risk | 风险等级 | select | 否 | 低/中/高 |
| status | 时效状态 | select | 否 | 有效/已过期/已归档 |
| date | 动态发表日期 | date | 否 | — |
| sourceUrl | 来源地址 | url | 否 | — |

**列表列**：title、company、content、kind、risk、status、date。**筛选**：keyword(title)、kind、risk、status。

### 1.3 CMS-JX-ENT-SZ-L01 · 深圳本地企业专项

原型面板：`ent-sz`。纯 overlay 内容表。

**端点**：`POST /api/open/cms/v1/enterprise/sz/list | /detail | /create | /update | /delete`。

| 字段 | 原型标签 | 类型 | 必填 | 枚举 |
|---|---|---|---|---|
| name | 企业名称 | string（下拉回填） | 是 | 选项源=企业实体（含虚拟）下拉选择，存 org_id；响应回显名称 |
| district | 区域归属 | select | 否 | 南山/福田/宝安/龙岗/龙华/光明 |
| industry | 产业属性 | string | 是 | — |
| park | 所属园区 | string | 否 | — |
| szNote | 专项说明 | textarea | 否 | docx 字段（重点标识/专项说明），原型未显式列出，按 docx 补 |

**列表列**：name、district、industry、park。**筛选**：keyword(name)、district。**v1.5 唯一性约束**：同企业仅一条有效专项行（DB `uk_sz_active(domain, active_org)`，`active_org` 为软删感知生成列；重复录入返回 40001——human:徐滕强 2026-10-17 拍板保留，原型同名多行仅为展示数据）。

---

## 2. 基础数据管理 · 政策

### 2.1 CMS-JX-POL-CRUD-L01 · 政策条目写侧 + 删除操作审计

原型面板：`pol-review`（政策条目）+ `pol-audit`（删除操作审计，只读）。

**端点**：`POST /api/open/cms/v1/policy/create`、`POST /api/open/cms/v1/policy/update`（body 含 id）、`POST /api/open/cms/v1/policy/delete`（body 含 id+reason）、`POST /api/open/cms/v1/policy/audit-logs/list`（删除操作审计列表）。读侧升级：`CMS-JX-POL-LIST-L01` 列表/详情改 join 视角，且默认过滤 `status≠失效`（原型 `filterActive` 行为）+ 软删剔除。

**编辑弹窗字段**：

| 字段 | 原型标签 | 类型 | 必填 | 枚举/说明 | 落位 |
|---|---|---|---|---|---|
| title | 标题 | string | 是 | 真源 `title`；覆盖写 overlay | 真源列 / overlay.title |
| body | 正文 / 粘贴文本 | textarea | 是 | 真源 `content`；覆盖写 overlay | 真源列 / overlay.body |
| attachment | 来源附件 | string[]（URL/文件名） | 否 | **v1.5 降级定稿**：只记 URL/文件名字符串列表（与原型真实行为一致——原型亦仅存 file.name 无真实上传）；文件上传设施归久新侧，docx 四元组待其确认需要后另立项；真源 `attachment` 只读回显 | overlay.attachments |
| publisher | 发布单位 | string | 是 | 真源 `publish_organization` | 真源列 / overlay |
| pubDate | 发布日期 | date | 否 | 真源 `publish_date` | 真源列 / overlay |
| docNo | 文件编号 | string | 否 | 真源 `issued_number` | 真源列 / overlay |
| sourceUrl | 来源地址 | url | 否 | 真源 `url` | 真源列 / overlay |
| industryTag | 行业标签 | tagselect(多选) | 否 | 人工智能/绿色低碳/生物医药/低空经济——运营标签 | overlay.industry_tags（真源 ext5/keywords 仅作初始化建议，不作约束） |
| regionTag | 地域标签 | tagselect(多选) | 否 | 深圳/广东/全国 | overlay.region_tags（真源 `region` 只读回显） |
| reviewStatus | 审核状态 | select | 否 | 待审核/已校正/需复核 | overlay.review_status |

**只读回显附加字段**：`status`（时效状态：有效/失效文案，真源列，编辑弹窗不可改——失效治理走 `POL-EXPIRED`/`POL-WEBHOOK` 老单）、`level`、`source`。
**列表列**：title、publisher、pubDate、docNo、industryTag、regionTag、source、status、reviewStatus。**筛选**：keyword(title)、reviewStatus、industryTag、regionTag、status。
**删除操作审计接口**：`POST /api/open/cms/v1/policy/audit-logs/list`（body：keyword/page/size），只读；列：time（操作时间）、operator（操作人）、action（操作：删除/编辑/新增）、title（政策标题）、reason（原因）；数据源 `cms_op_audit`（不限于删除——原型面板名"删除操作审计"，实现返回全部写操作审计，前端自行过滤）。
**引用检查**：被专家知识（`cms_expert_knowledge.entity.entityId` 匹配，domain 五域枚举内）引用时拒绝软删（v1.5 修正实现枚举，此前检查空转）。

---

## 3. 基础数据管理 · 服务机构

### 3.1 CMS-JX-SVC-CRUD-L01 · 服务机构实体写侧

原型面板：`svc-base`。真源骨架=ODS 机构主表（列名同 §0.5）+ `svc_org_circle` 圈定池（**只读、不扩、不动 pending_client_confirm 态**）。

**端点**：`POST /api/open/cms/v1/service-org/create`、`POST /api/open/cms/v1/service-org/update`、`POST /api/open/cms/v1/service-org/delete`（delete body 含 id+reason）。读侧升级：`CMS-JX-SVC-LIST-L01` 改 join 视角，行集=圈定池 ∪ overlay 虚拟机构。

| 字段 | 原型标签 | 类型 | 必填 | 枚举/说明 | 落位 |
|---|---|---|---|---|---|
| id | 唯一 ID | string | 是 | 真源=org_id 只读；虚拟=`cms:SVC-{uuid8}` | overlay.source_id / key |
| name | 机构名称 | string | 是 | 真源 `name_cn` | 真源列 / overlay |
| founded | 成立时间 | date | 否 | 真源 `incorporation_date` 只读回显 | 真源列 / overlay |
| contact | 联系人 | string | 否 | 运营维护（真源 `phone_num` 只读回显另列） | overlay.contact |
| flag | 重点机构标识 | select | 否 | 是/否 | overlay.flag |
| priority | 优先级 | select | 否 | P0/P1/P2/— | overlay.priority |
| type | 机构类型 | select | 否 | 孵化器/加速器/咨询公司/检测机构/路演平台 | overlay.org_type |
| scope | 服务范围 | textarea | 否 | — | overlay.scope |
| cert | 资质信息 | string | 否 | — | overlay.cert |
| ability | 服务能力描述 | textarea | 否 | — | overlay.ability |
| domain | 服务领域 | string | 否 | — | overlay.domain |

**列表列**：id、name、type、scope、cert、domain、flag、priority。**筛选**：keyword(name)、type、flag、priority。
**只读回显附加字段**：province/city/area、org_size、phone_num。
**引用检查**：被 `svc_news.org` / `svc_sz.name` / 图谱关系 / 专家知识引用时拒绝。

### 3.2 CMS-JX-SVC-NEWS-L01 · 服务机构动态资讯

原型面板：`svc-news`。纯 overlay。端点：`POST /api/open/cms/v1/service-org/news/list | /detail | /create | /update | /delete`。

| 字段 | 原型标签 | 类型 | 必填 | 枚举 |
|---|---|---|---|---|
| title | 标题 | string | 是 | keyword 命中 |
| kind | 类型 | select | 否 | 服务案例/客户反馈/培训活动/路演对接会 |
| org | 所属机构 | string[]（多选） | 是 | 选项源=服务机构实体（含虚拟），存 org_id |
| content | 内容摘要 | textarea | 否 | — |
| date | 动态发表日期 | date | 否 | — |
| sourceUrl | 来源地址 | url | 否 | — |

**列表列**：title、kind、org、content、date。**筛选**：keyword(title)、kind。

### 3.3 CMS-JX-SVC-SZ-L01 · 深圳服务机构专项

原型面板：`svc-sz`。纯 overlay。端点：`POST /api/open/cms/v1/service-org/sz/list | /detail | /create | /update | /delete`。

| 字段 | 原型标签 | 类型 | 必填 | 枚举 |
|---|---|---|---|---|
| name | 机构名称 | string（下拉回填） | 是 | 选项源=服务机构实体（含虚拟），存 org_id |
| type | 所属类型 | select | 否 | 孵化器/加速器/咨询公司/检测机构 |
| domain | 服务领域 | string | 是 | — |
| cert | 资质信息 | string | 否 | — |
| district | 区域归属 | select | 否 | 南山/福田/宝安/龙岗/龙华 |
| cases | 典型案例 | textarea | 否 | docx 补充字段 |
| evaluation | 服务评价 | string | 否 | docx 补充字段 |
| szNote | 专项说明 | textarea | 否 | docx 补充字段 |

**列表列**：name、type、domain、cert、district。**筛选**：keyword(name)、type、district。

---

## 4. 基础数据管理 · 产品链

### 4.1 CMS-JX-PROD-CRUD-L01 · 产品实体写侧

原型面板：`prod-entity`。真源仅产品名称（`enterprise_industry_product`，挂 org_id）；型号/技术参数为运营补充。

**端点**：`POST /api/open/cms/v1/product/create | /update | /delete`（update/delete body 含 id；delete 另含 reason）。读侧：`CMS-JX-ENT-PRODUCT-L01`（真源产品名，按企业查）+ 本单 overlay 视角；产品列表接口=真源产品名 UNION overlay（含虚拟产品），输出合并视角。

| 字段 | 原型标签 | 类型 | 必填 | 说明 | 落位 |
|---|---|---|---|---|---|
| id | 唯一 ID | string | 是 | 真源产品=真源行主键只读；虚拟=`cms:PROD-{uuid8}` | overlay.source_id / key |
| name | 产品名称 | string | 是 | 真源产品名列；覆盖写 overlay | 真源列 / overlay |
| orgId | 归属企业 | string | 虚拟必填 | 选项源=企业实体下拉（真源产品自带；虚拟产品必选） | overlay.org_id |
| models | 多型号信息 | string | 否 | 逗号分隔（原型占位文案） | overlay.models |
| params | 技术参数 | textarea | 否 | — | overlay.params |
| chain | 产业链环节 | select | 否 | 选项源=标准环节（`/api/open/cms/v1/industry/chain-links`）∪ 自定义环节（§4.2）；存环节编码 | overlay.chain_code |

**列表列**：id、name、models、params、chain。**筛选**：keyword(name)、chain。

### 4.2 CMS-JX-IND-CUSTOM-L01 · 自定义产业分类 + 自定义产业链环节

原型面板：`prod-dict`（树形）+ `prod-chain`。

**端点**：
- 自定义分类：`POST /api/open/cms/v1/industry/custom-class/list | /detail | /create | /update | /delete`；合并树视图 `POST /api/open/cms/v1/industry/tree-merged`
- 自定义环节：`POST /api/open/cms/v1/industry/custom-link/list | /detail | /create | /update | /delete`；合并环节下拉 `POST /api/open/cms/v1/industry/chain-links-merged`

**自定义分类字段**：

| 字段 | 原型标签 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| code | 编码 | string | 是 | 自定义编码，建议 `CUS-{seq}` 防撞标准编码 |
| name | 分类名称 | string | 是 | — |
| level | 层级 | select | 是 | 一级/二级/三级/四级/五级 |
| parent | 上级分类 | string | 否 | 树选择；一级为空；仅可选自定义分类（标准分类为只读锚点） |
| order | 排序 | number | 否 | docx 补充（分类排序） |

**自定义环节字段**：

| 字段 | 原型标签 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| code | 环节编码 | string | 是 | 建议 `CUS-CHAIN-{seq}`（原型占位 CHAIN-UPSTREAM 风格） |
| name | 环节名称 | string | 是 | — |
| definition | 环节定义 | textarea | 是 | — |
| order | 排序 | number | 否 | — |

**引用检查**：环节被产品实体 `chain` 引用时拒绝删除，40901。

### 4.3 CMS-JX-PROD-NEWS-L01 · 产业动态资讯

原型面板：`prod-news`。纯 overlay。端点：`POST /api/open/cms/v1/industry/news/list | /detail | /create | /update | /delete`。

| 字段 | 原型标签 | 类型 | 必填 | 枚举 |
|---|---|---|---|---|
| title | 标题 | string | 是 | keyword 命中 |
| kind | 类型 | select | 否 | 政策/报告/重大事件/市场动态 |
| content | 内容摘要 | textarea | 是 | — |
| date | 动态发表日期 | date | 否 | — |
| status | 状态 | select | 否 | 有效/归档 |
| sourceUrl | 来源地址 | url | 否 | — |

**列表列**：title、content、kind、date、status。**筛选**：keyword(title)、kind、status。

### 4.4 CMS-JX-PROD-SZ-L01 · 区域企业名录

原型面板：`prod-sz`。纯 overlay。端点：`POST /api/open/cms/v1/industry/region-roster/list | /detail | /create | /update | /delete`。

| 字段 | 原型标签 | 类型 | 必填 | 枚举 |
|---|---|---|---|---|
| name | 企业名称 | string | 是 | 支持下拉回填企业实体（存 org_id）**或手填**（名录语义允许非入库企业，手填时 org_id=NULL、name 冗余存 overlay） |
| industry | 产业归属 | string | 是 | — |
| district | 地理归属 | select | 否 | 南山/福田/宝安/龙岗/龙华/光明 |
| scale | 规模 | select | 否 | 大型/中型/小型/微型企业 |

**列表列**：name、industry、district、scale。**筛选**：keyword(name)、district、scale。

---

## 5. 全要素图谱管理（四类实体：industry / enterprise / policy / service）

> 通用于本章：`{entityType}` ∈ `industry|enterprise|policy|service`；实体下拉/批量初始化复用 `CMS-JX-BULK-L01` 与各 LIST 单；**全部写操作只落 overlay，禁止写 Nebula 正式图谱**（老设计单对正式图谱的只读边界继续生效）。
> **范围裁决（2026-10-15，human:徐滕强）**：原型 kg-mgmt 页签仅 industry/enterprise/policy/service 四类标（智树）；tech/research/talent 三类实体不在本期。**图谱绘制工具（graph-editor）不在本期**——侧栏菜单项未标（智树），属久新侧，不建工单、不提供保存类接口。

### 5.1 CMS-JX-KG-STAGE-L01 · 实体生命周期

原型模块：`kg-mgmt-page.js` entity-life（列表 + 阶段公共配置 + 状态标记弹窗 + 状态时间线）。

**端点**：
- 阶段定义：`POST /api/open/cms/v1/kg/{entityType}/stages/list | /create | /update | /delete`（阶段为该类型**全实体通用配置**——原型原话，不挂单实体；update/delete body 含 id）
- 状态标记：`POST /api/open/cms/v1/kg/{entityType}/status/mark`（新增或更新实体当前状态记录）
- 状态历史：`POST /api/open/cms/v1/kg/{entityType}/status/history`（body：entityId/page/size；时间倒序）
- 实体生命周期能量列表：`POST /api/open/cms/v1/kg/{entityType}/entities`（body：keyword/stage 多选/page/size；=实体列表 join 当前状态记录）

**阶段定义字段**：stageName（必填）、feature（典型特征/产业用"阶段定义描述"，必填）、metric（衡量指标，如"产值增速 > 25%"，原型 STAGE_DEFS 每阶段自带；2026-10-15 v1.1 补）、order。
**初始化导入**（首次部署 seed，来自原型 STAGE_DEFS，名称+feature+metric 三项齐备）：

| entityType | 默认阶段（名称 | 典型特征） |
|---|---|
| industry | 萌芽期\|市场规模小、标准未定；成长期\|资本涌入、企业扩张；成熟期\|格局稳定、利润收敛；转型/衰退期\|替代技术出现 |
| enterprise | 初创期\|产品打磨；成长期\|市场扩张；扩张期\|并购整合；成熟期\|稳定经营 |
| policy | 起草征求意见\|调研论证；发布实施\|正式生效；评估调整\|效果复盘；废止/延续\|时效到期 |
| service | 起步期\|服务能力建设；拓展期\|区域覆盖；品牌期\|口碑沉淀；平台期\|生态协同 |

**状态标记弹窗字段**：

| 字段 | 原型标签 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| entityId | {类型}实体 | select | 是 | 选项源=该类型实体列表（真源 ∪ 虚拟） |
| stage | 当前所处阶段 | select | 是 | 选项源=阶段定义 |
| since | 进入时间 | date | 是 | 默认今天 |
| event | 关键事件 | textarea | 是 | 便于回溯 |
| 类型专属字段 | 见下 | — | — | 按 entityType 追加 |

| entityType | 专属字段（均 textarea，非必填） |
|---|---|
| enterprise | financing 融资情况（如：融资轮次、金额、估值）、operation 经营状况（如：营收、利润、研发投入情况） |
| industry | stageInfo 阶段信息（如：市场规模、企业数量、产业增速）、linkedMetric 关联指标（如：产业增加值、企业增长率、市场渗透率） |
| policy | scope 影响范围（如：覆盖区域、产业、企业及人才类型）、effect 执行效果（如：落地率、企业响应度、产业拉动效果） |
| service | scale 服务规模（如：年度服务项目数、服务覆盖范围）、customers 客户数量（如：累计客户 860 家、年度新增 120 家） |

**实体列表列**：实体名称、当前所处阶段（badge）、进入时间、关键事件、类型专属列。**筛选**：keyword(实体名)、stage（多选）。
**状态历史记录字段**：变更前状态（`prevStage`，v1.5 实装：mark 时写入上一状态行 stage，首次标记为 null）、变更后状态（`stage`）、变更说明（=关键事件 `event`）、操作人（`createdBy`）、操作时间（`createdAt`）；另附类型专属字段整包 `extra` + 平铺键（v1.5：financing/operation 等按类型平铺输出）。

### 5.2 CMS-JX-KG-REL-L01 · 关系链生命周期

原型模块：relation-life（关系定义卡片 + 关系列表 + 新建/编辑弹窗 + 标记断裂 + 演变时间线）。

**端点**：`POST /api/open/cms/v1/kg/{entityType}/relations/list | /detail | /create | /update | /delete`、`POST /api/open/cms/v1/kg/{entityType}/relations/break`（标记断裂，body 含 id+reason）、`POST /api/open/cms/v1/kg/{entityType}/relations/history`（body 含 id）。

**关系字段**（弹窗）：

| 字段 | 原型标签 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| fromEntityId | 源实体 | select | 是 | 同类型实体下拉 |
| type | 关系类型 | string | 是 | 自由文本（占位：上游供给、合作、竞争） |
| toEntityId | 目标实体 | select | 是 | 同类型实体下拉 |
| status | 状态 | select | 否 | 新建/稳定/强化中/演进中（已断裂仅由 break 动作置入，不可手选） |
| since | 建立时间 | date | 否 | 默认今天 |

**标记断裂**：`{reason 必填}`，置 status=已断裂 + breakTime + 审计；**不做物理删**（列表仍可见，badge 灰化语义由前端处理）。
**关系历史**：变更前内容、变更后内容、变更原因、操作人、操作时间；时间倒序。**v1.5 实装口径**：history 返回结构化 `snapshotBefore`（变更前完整快照对象，不截断）+ `reason` + `operator` + `time` 独立字段（此前拼接截断 120 字不可结构化消费）。
**关系列表列**：源实体（名称回显）、关系类型、目标实体（名称回显）、状态、建立时间。**筛选**：keyword（源/目标实体名）、status。
**删除语义**：DELETE=软删（原型无删关系按钮，仅有标记断裂；DELETE 供误建清理，软删+审计）。

### 5.3 CMS-JX-KG-ATTR-L01 · 实体属性管理

原型模块：entity-attr（基础属性定义 + 动态属性更新两卡片）。**运营侧 schema 配置，不影响真源表结构**。
**原型明确移除、不做**：状态、停用、版本与变更、批量导入、保存属性（docx 第三节尾注）。

**端点**：
- 属性字段：`POST /api/open/cms/v1/kg/{entityType}/attrs/list | /create | /update | /delete`（update/delete body 含 id）
- ~~属性分类独立 CRUD~~ **v1.1 收敛（2026-10-15）**：原型四类实体（industry/enterprise/policy/service）的属性为**扁平列表**，按"基础/动态"双卡片分组（`group: base|dyn`），无独立分类管理界面（原型中分类输入仅出现在 tech 类型的参数表单，tech 不在本期）。故**取消 attr-categories 独立资源**，分类语义并入属性字段自身。

**属性字段字段**：

| 字段 | 原型标签 | 类型 | 必填 | 枚举 |
|---|---|---|---|---|
| name | 属性名 | string | 是 | — |
| group | 分组 | select | 否 | base 基础属性 / dyn 动态属性（原型双卡片；缺省 base） |
| dtype | 数据类型 | select | 否 | 文本/数值/整数/枚举/日期/百分比/多值 |
| constraint | 约束条件 | string | 否 | 占位：必填 ≤64 |
| value | 当前值 | string | 否 | — |

**seed 建议**：四类实体按原型 ATTR_DEFS 初始化（industry 4 条：产业名称/所属领域/年度产值(亿)/从业人数；enterprise 7 条：企业名称/统一社会信用代码/当前阶段/融资情况/经营状况/营收(亿)/研发投入占比；policy 14 条；service 14 条），首次部署导入。**v1.5 修正**：DDL seed 已补齐至原型全量（policy 补「当前版本/生效日期+7 条效果组」、service 补「联系方式/服务对象/客户评价/客户满意度+4 条质量组」，此前误删至 5+6 条）；分组映射：原型 basic/effect/service/quality 多组 → 本规格 base|dyn 双组（effect/quality 组归 dyn），对接文档需给久新映射说明。

---

## 6. 专家知识管理（5 类，12 section）

> 通用：纯 overlay；关联实体下拉取对应实体列表（含虚拟）；**存储建议单一内容表 + section 字段 JSON**（`CMS-JX-OVERLAY-A5-L01` 定表结构，本节冻结字段语义与顺序）。原型 section 内的分栏 tabs（如 policy-effect 两栏）为 UI 分组，**不拆接口**。
> 端点统一：`POST /api/open/cms/v1/expert/{domain}/list | /detail | /create | /update | /delete`（update/delete body 含 id）、`POST /api/open/cms/v1/expert/{domain}/sections`（section 元数据：id/名称/字段定义有序数组——供久新前端动态渲染表单）。

**通用记录字段**（全部 section 一致）：

| 字段 | 原型标签 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| sectionId | 所属 section | string | 是 | 见各域枚举 |
| title | 标题 | string | 是 | keyword 命中 |
| entity | 关联实体 | string | 是 | 关联对象名称/ID（下拉回填或手填；存 `{entityType, entityId, name}`） |
| expert | 专家 | string | 否 | — |
| content | 结构化字段值 | JSON | 是 | 按 section 字段定义的有序键值对（字段清单见下，键=拼音蛇形命名） |
| view | 观点摘要 | string | 否 | 缺省取 content 首个非空值 |
| conclusion | 结论建议 | string | 否 | 缺省取 content 末字段 |
| evidence | 研判依据 | string | 否 | — |
| sourceType | 来源类型 | string | 否 | — |
| source | 来源 | string | 否 | — |
| advice | 行动建议 | string | 否 | — |

**列表**（各域同）：`POST /api/open/cms/v1/expert/{domain}/list`（body：keyword/sectionId/page/size）；列：title、entity、expert、sectionName、view、updatedAt。

### 6.1 CMS-JX-EK-INDUSTRY-L01 · 产业链（domain=industry）

| sectionId | section 名称 | content 字段（有序） |
|---|---|---|
| industry-cycle | 产业链结构与周期知识维护 | industryLifeStage 产业生命周期阶段、stageFeature 阶段特征判断、turningPointForecast 周期拐点预测、keyLinks 关键环节、techBarrier 技术壁垒评估、profitSpace 利润空间评估、strategicValue 战略价值评估、relatedReport 关联分析报告 |
| industry-bottleneck | 产业瓶颈与深圳区域知识维护 | chainLink 产业链环节、bottleneckType 瓶颈类型、blockIssue 堵点问题、impactScope 影响范围、difficulty 解决难度、potentialConsequence 潜在后果、szAdvantage 深圳产业优势、chainShortboard 产业链短板、breakRisk 断链风险、improveSuggestion 改进建议 |

关联实体：产业链（标准+自定义产业分类下拉）。

### 6.2 CMS-JX-EK-ENT-L01 · 企业（domain=enterprise）

| sectionId | section 名称 | content 字段（有序） |
|---|---|---|
| enterprise-history | 企业发展历程专家知识管理 | growthStage 企业发展关键阶段、expertOpinion 专家观点、relatedCase 关联案例、growthPath 成长路径分析、pathCompare 多路径比较 |
| enterprise-attract | 招引企业推荐专家知识管理 | attractStandard 招引标准、filterDims 筛选维度、recommendList 推荐企业清单、recommendReason 推荐理由、expectContribution 预期贡献、riskHint 风险提示 |
| enterprise-nurture | 培育企业推荐专家知识管理 | nurtureTargets 重点培育企业、entTags 企业标签、filterBasis 筛选依据、nurtureStrategy 个性化培育策略 |

关联实体：企业实体（含虚拟）。

### 6.3 CMS-JX-EK-POLICY-L01 · 政策（domain=policy）

| sectionId | section 名称 | content 字段（有序） |
|---|---|---|
| policy-timing | 政策时序与力度知识维护 | keyTimeNodes 关键时间节点、timingArrange 时序安排、timingImpact 时序潜在影响、strengthDims 政策力度评估维度、strengthOpinion 政策力度评估意见 |
| policy-effect | 政策效果与区域分析知识维护 | effectIndicators 政策效果评估指标、actualEffect 实际成效判断、caseEvidence 案例佐证、szInnovation 深圳政策创新点、implAdvantage 实施优势、coverageBlindSpot 政策覆盖盲区、execDifficulty 执行难点、optimizeSuggestion 优化建议 |
| policy-match | 政策匹配与应用建议知识维护 | matchObjectType 匹配对象类型、matchLogic 匹配逻辑、applyCondition 适用条件、actualMatchEffect 实际匹配效果、applicabilityBias 适用性偏差、execObstacle 执行障碍、improveSuggestion 改进建议 |

关联实体：政策（含虚拟）。

### 6.4 CMS-JX-EK-SVC-L01 · 服务机构（domain=service）

| sectionId | section 名称 | content 字段（有序） |
|---|---|---|
| service-gap | 服务链短板诊断知识维护 | serviceType 服务类型、weakLink 服务链薄弱环节、gapDesc 短板问题描述、impactScope 产业影响范围、priority 解决优先级、difficulty 实施难度 |
| service-support | 服务机构引扶建议知识维护 | intakeStandard 服务机构引入参考标准、recommendOrgs 推荐机构清单、recommendReason 推荐理由、expectContribution 预期服务贡献、riskHint 潜在风险、keySupportOrgs 重点扶持机构名单、supportStrategy 个性化扶持策略、resourcePlan 资源配置建议、capabilityPath 能力建设路径 |

关联实体：服务机构（含虚拟）。

### 6.5 CMS-JX-EK-REGION-L01 · 综合区域（domain=region）

| sectionId | section 名称 | content 字段（有序） |
|---|---|---|
| region-innovation | 区域创新能力评估知识维护 | region 评估区域、vitalityIndicators 创新活力评估指标、indicatorScore 指标评分或定性判断、elementDims 区域创新要素评估维度、elementDist 要素分布状况、configReasonableness 配置合理性、structuralShortboard 结构性短板 |
| region-collaboration | 区域协同机制与障碍知识维护 | collabSubjects 协同主体、collabMode 协同模式、mechanismSummary 协同机制总结与评价、obstacleType 协同障碍类型、obstacleDesc 协同障碍描述、improveSuggestion 改进建议或解决方案 |

关联实体：区域为自由结构化字段（如"深圳市南山区"），不挂区域维表。

---

## 7. 工单 ↔ 规格节对照表（note 绑定索引用）

| 工单 ID | 规格节 |
|---|---|
| CMS-JX-OVERLAY-A5-L01 | 全文（A5 在本规格基础上冻结表结构与路径语法） |
| CMS-JX-OVERLAY-DDL-L01 | §0.4 / §0.5 + 各节"落位"列 |
| CMS-JX-ENT-CRUD-L01 | §1.1 |
| CMS-JX-ENT-NEWS-L01 | §1.2 |
| CMS-JX-ENT-SZ-L01 | §1.3 |
| CMS-JX-POL-CRUD-L01 | §2.1 |
| CMS-JX-SVC-CRUD-L01 | §3.1 |
| CMS-JX-SVC-NEWS-L01 | §3.2 |
| CMS-JX-SVC-SZ-L01 | §3.3 |
| CMS-JX-PROD-CRUD-L01 | §4.1 |
| CMS-JX-IND-CUSTOM-L01 | §4.2 |
| CMS-JX-PROD-NEWS-L01 | §4.3 |
| CMS-JX-PROD-SZ-L01 | §4.4 |
| CMS-JX-KG-STAGE-L01 | §5.1 |
| CMS-JX-KG-REL-L01 | §5.2 |
| CMS-JX-KG-ATTR-L01 | §5.3 |
| CMS-JX-EK-INDUSTRY-L01 | §6.1 |
| CMS-JX-EK-ENT-L01 | §6.2 |
| CMS-JX-EK-POLICY-L01 | §6.3 |
| CMS-JX-EK-SVC-L01 | §6.4 |
| CMS-JX-EK-REGION-L01 | §6.5 |

> 读侧升级涉及的 4 张老只读单（ENT-LIST/POL-LIST/SVC-LIST/ENT-PRODUCT）：实现时按 §0.4 join 视角升级数据源，各自 handoff 引用本规格 §0.4 与对应写侧节。

---

## 修订记录

| 日期 | 版本 | 变更 | 作者 |
|---|---|---|---|
| 2026-10-17 | v1.5 | **原型符合性审计修订**（三方对照：原型 2026-10-17 线上版 ↔ 本规格 ↔ 实现，产出 4high+10med）：①**§2.1 attachment 降级定稿**：只记 URL/文件名字符串列表，与原型真实行为一致（原型提交逻辑亦仅存 file.name，无真实上传，human:徐滕强 2026-10-17 拍板）；文件上传设施归久新侧，docx「文件」四元组待其确认需要后另立项。②§1.3 增补「同企业唯一有效行」约束登记（DB `uk_sz_active`，重复录入 40001；原型同名多行仅为展示数据，human:徐滕强 拍板保留）。③§5.1 状态历史增补 `prevStage` 变更前状态字段（docx 要求；首次标记为 null）。④§5.3 属性 seed 修正为原型 ATTR_DEFS 全量（policy 14/service 14，此前 5+6）。⑤新增 policy/suggest 端点（此前 OpenAPI 已登记代码缺失）。⑥列表 size 上限统一 100（§0.3 原约定）。⑦关系 history 返回结构化 `snapshotBefore`+`reason`（不再拼接截断）。⑧政策删除引用检查 domain 枚举修正为 EK 五域。 | api-agent（human:徐滕强 拍板 3 项决策） |
| 2026-10-17 | v1.4 | 全 epic 对外前缀切换：`/cms/v1/*` → `/api/open/cms/v1/*`（久新未接入前全新切换，无兼容负担；gen-openapi.py 同步重生成 OpenAPI） | api-agent（human:徐滕强 拍板） |
| 2026-10-15 | v1.0 | 首版：19 工单全量规格（基于原型 2026-10-15 抓取版冻结） | coordinator（受 human:徐滕强 委托） |
| 2026-10-15 | v1.1 | 字段审计修订：①§5 头补范围裁决（graph-editor 不在本期，tech/research/talent 实体不在本期）；②§5.1 阶段定义补 metric 字段；③§5.3 取消 attr-categories 独立资源，改为 group(base/dyn) 字段并对齐原型双卡片结构 | coordinator（审计结论经 human:徐滕强 确认） |
| 2026-10-15 | v1.2 | 动词语法定稿：全 epic 统一 POST + JSON body，禁止路径参数（human:徐滕强 拍板，方案 U + 读侧同步改写）；§0.6 重写为 create/update/delete/list/detail 动作式路径，§1–§6 全部端点行同步替换；老设计单 §5.2 十六只读接口登记表由 A5 同步改写 | coordinator |
| 2026-10-15 | v1.3 | §0.5 真源表名纠偏（A5 八条裁决）：读项目 DWD 正式表 `enterprise_base`/`policy_base_info`/`industry_chain(_node)`（正式库 gkxlumenx_dwd），禁用 ODS 名 `dwd_org_base_info` 等；overlay 三件套落业务库 `gkxlumenx_cms` | coordinator（human:徐滕强 逐条拍板） |
