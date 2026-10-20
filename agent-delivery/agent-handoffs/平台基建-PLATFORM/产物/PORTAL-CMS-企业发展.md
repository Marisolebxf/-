# 门户 CMS 字段与读接口契约 · 企业发展

> **任务**：`PORTAL-CMS-FIELD-API-L01`  
> **状态**：已确认。本文件只写企业发展。专题全景、政策扶持、专题服务各有单独文件。  
> **日期**：2026-10-20  
> **执行**：`agent:product-agent` · 监管 `human:淮政玮`  
> **指标查询**：metric-registry，2026-10-20。无 `metric_id` 的只记缺口，不新编口径。  
> **读法**：字段、空态、接口都在本文件里。2026-07-16 的 `CMS-read-contract-E31.md` 只是早期来源；与本文不一致时以本文为准（瓶颈/结构解读已改为智树大模型生成，不再使用旧类型 `key_chain_expert_note`）。本文不改代码。

招标锚点：`智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.1 企业发展（企业整体概况、重点企业全景图、明星企业介绍、深圳企业介绍）。

---

## 0. 本模块约定

1. 门户只嵌入 CMS **已发布**正文。草稿、审核中不下发。
2. 计算数字走指标服务，带 `metric_id`。CMS 正文里不写这些数字，Java 不把富文本解析成指标。
3. 调用链：浏览器 → 门户 Java REST → 读取任欢侧已发布内容。浏览器和 Python 不直连任欢。
4. 现有 `/cms/v1/*` 是任欢后台向智树要企业/政策等事实数据的集群内接口，不走公网网关。本文件的门户读接口是另一条，给浏览器经网关使用，路径不用 `/cms/v1`。
5. `content_id` 只作内容引用，不进 ADS 主键。企业绑定用 `enterprise_code`。产业绑定用已发布的 `future_industry_code`，CMS 不自造正式产业码。

公共信封（每个 CMS 块都有）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `content_id` | string | 是 | 任欢内容实例 ID |
| `content_type` | string | 是 | 见 §2 |
| `page_key` | enum | 是 | `overview` / `key-pano` / `star` / `shenzhen` |
| `future_industry_code` | string | 条件 | 按产业出的块必填 |
| `enterprise_code` | string | 条件 | 绑企业的块必填 |
| `version` | string | 是 | 内容版本 |
| `publish_status` | enum | 是 | `published` / `draft` / `archived`；门户只收 `published` |
| `publish_time` | datetime | 是 | ISO-8601 |
| `sort_order` | int | 是 | 同集合内升序 |
| `locale` | string | 否 | 默认 `zh-CN` |
| `updated_at` | datetime | 推荐 | 缓存 |

`html` 类型只允许：段落、标题、列表、引用、加粗、链接、图片 URL。不允许 `script`、内嵌框架、事件属性。图片和链接只传 URL，不传二进制。

---

## 1. 区块对照

图例：`metric` 计算数字；`cms` 运营正文；`mixed` 同一屏两边都有，分栏取数；`llm` 智树调用大模型生成的摘要，不进 CMS，也不算指标。

表里的 D1 `aligned` 表示口径已在指标库对齐；D4 `mock` 表示当前仍是模拟数，还没有正式接入。缺口行是指标库里没有可用 ID。决策项编号见 §7。

### 1.1 企业整体概况 `page_key=overview`

本页没有 CMS 字段。数量、分布、人数都走指标。

| 招标叶子 | 归类 | metric_id | 库内名称 | 说明 |
|---|---|---|---|---|
| 企业总体数量 | metric | `M_ENT_TOTAL_COUNT` | 企业总数 | D1 aligned。口径是选定未来产业内国内并国外按 `org_id` 去重；选产业时国外无上链表，暂不能并入。D4 mock |
| 企业总体数量 · 历年趋势 | metric | — | 缺口 | 库内有 `M_ENT_NEW_COUNT_Y`（历年新增企业数），不是总数趋势，不能顶替 |
| 企业分布情况 | metric | `M_ENT_REGIONAL_COUNT` | 区域企业数量 | D1 aligned。国内省/市/县三套分组，国外按国家。产业不是分组维，选产业是接口过滤。D4 mock |
| 科研人数 | metric | `M_ENT_RESEARCHER_COUNT` | 全球企业科研人数 | D1 aligned。国内 `development_employee` 与国外 `rd_staff` 最新年求和。禁止用从业人数或研发金额顶替。待决仍挂 Q-E32-01。D4 n/a |

同页另有已注册指标 `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`（覆盖未来产业数）。它不是上面三行招标叶子，页面若展示该数字，同样走指标服务。

### 1.2 重点企业全景图 `page_key=key-pano`

| 招标叶子 | 归类 | 取数 |
|---|---|---|
| 重点企业全景（名单、环节名、关系叙述） | mixed | 名单与叙述：CMS `key_enterprise_set`、`key_chain_structure`。企业法定名称、区域、资质：指标/主数据，不用 CMS 覆盖 |
| 链位上的企业数 | metric | `M_ENT_KEY_NODE_COUNT` 重点环节企业数。D1 aligned，D4 mock |
| 重点企业规模统计（外企、高企、小微、上市 × 国家/省/市） | metric | `M_ENT_KEYPANO_QUAL_DISTRIBUTION` 整链资质分布。D1 aligned，D4 mock。按资质标签 × 区域计数，格子不能加总。曾经用过的名字 `M_ENT_KEY_QUAL_SCALE` 不在指标库里，本页不用 |
| 重点企业领域统计 | metric | `M_ENT_KEYPANO_DOMAIN_SUMMARY` 领域摘要（D1 aligned，D4 mock）。论文/专利关键词证据没有单独已注册 `metric_id`，记缺口，不把证据数写进 CMS |
| 瓶颈/结构解读文案 | llm | 智树侧根据链上结构与统计结果调用大模型生成。不进任欢 CMS。摘要不代替上表计数；生成失败时只隐藏这段文案 |
| 重点企业「是谁」的判定阈值 | metric | `M_ENT_KEY_TOTAL` 的公式是专利总量 ≥ 50 的企业去重，N=50 仍是团队临时值（Q038）。门户名单若走 CMS 圈定，与该计数 join，CMS 不手填这个数 |

### 1.3 明星企业介绍 `page_key=star`

| 区块 | 归类 | 取数 |
|---|---|---|
| 当前产业已发布名单、排序、入选标签、入选理由 | cms | `star_roster_item` |
| 「共 N 家」 | metric | `M_ENT_STAR_ENTERPRISE_COUNT`。口径是对 CMS 已发布名单 `COUNT(DISTINCT enterprise_code)`，禁止算法 TopN、禁止用专利数或荣誉标签冒充。D1 aligned，D4 mock |
| 入选标准名称、版本、适用产业、已确认维度 | cms | `star_selection_standard`。不下发权重、阈值、排名公式 |
| 企业法定名称 | mixed | 主数据为准。CMS `display_name_alias` 只作别名，界面标明非法定名 |
| 资质荣誉标签 | metric | 企业标签主数据。CMS「重点标识」不代替标签 |
| 产品功能全景图（产品、模块、场景、案例、媒体 URL） | cms | `star_product_panorama`，字段见 §2.3。按产品、模块、场景、案例、媒体拆开存，不收成一整块 HTML |
| 技术优势 · 专利数 | metric | 缺口。`M_ENT_STAR_PATENT_COUNT`、`M_ENT_PATENT_VALID_COUNT` 均未入种子，D1 missing。页面留位，CMS 不填这个数 |
| 技术优势 · 研发投入占比 | metric | `M_ENT_RD_INVESTMENT_RATIO`。最近完整自然年研发投入/营收。未注册别名 `M_ENT_STAR_RD_RATIO` 不用。D1 aligned，D4 mock |
| 技术优势 · 核心技术/原理/成果简介 | cms | `star_tech_narrative.body_html`，类型 `html`。专利数和研发投入占比不写进这段 HTML |
| **团队实力多维展示** | **cms** | **`star_team_strength.body_html`，类型 `html`**。见 §3 |
| 团队实力条带上的「科学家/核心人才比例」 | cms | 表单录入，字段见 §2.14。比例数字由运营填写，不是指标。不写进上方 HTML |
| 产业生态图谱的正式边 | metric | 图谱边由智树图谱数据给出。合作摘要不参与画边。边的正式口径仍待确认（决策项 Q040） |
| 产业生态的合作摘要 | llm | 来自企业供应链分析的大模型摘要。不进 CMS，不设 `star_ecosystem_note`。生成失败时只隐藏这段摘要，不补虚假节点 |
| 发展历程、口碑摘要 | cms | `star_story` |

### 1.4 深圳企业介绍 `page_key=shenzhen`

| 招标叶子 | 归类 | 取数 |
|---|---|---|
| 深圳企业数量 | metric | `M_ENT_SZ_COUNT` 深圳企业数。`region_id` 以 `4403` 开头，选产业再过滤。D1 aligned，D4 mock |
| 深圳企业数量 · 历年趋势 | metric | 缺口。建议名 `M_ENT_SZ_INDUSTRY_TREND` 未入指标库 |
| 深圳企业领域分布 | metric | `M_ENT_SZ_CHAIN_POSITION` 链中角色（上/中/下游计数）。它不是「已识别领域个数」，个数类另记缺口（建议名 `M_ENT_SZ_DOMAIN_DIST` 未入指标库） |
| 深圳企业规模分析 | metric | 缺口。建议名 `M_ENT_SZ_SCALE_DIST` 未入指标库。禁止用资质标签冒充大/中/小/微 |
| 上市数、国企数 | metric | 缺口。未查到已注册的深圳上市数、国企数 ID |
| 深圳重点企业圈定与介绍文案 | mixed | 圈定与文案：CMS `sz_focus_set`、`sz_enterprise_intro`。名称与资质走主数据 |
| 本地定位、优势、专家分析 | cms | `sz_enterprise_intro` |

---

## 2. CMS 字段

每个块都带 §0 的公共信封。下面是各 `content_type` 自己的字段，不必再打开别的契约。企业整体概况没有 CMS 块。

相对早期草稿：新增 `star_team_strength`、`star_tech_narrative`、`star_scientist_ratio`。瓶颈/结构解读不在本节，由智树调用大模型生成。

### 2.1 `star_roster_item`（明星名单）

页面 `star`。绑定产业 + 企业。前台要同时满足：`publish_status=published`，且 `list_published`、`basic_intro_published` 都为 true。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `enterprise_code` | string | 是 | 对齐企业主数据 |
| `future_industry_code` | string | 是 | 所属产业 |
| `selection_tag` | text | 是 | 一句入选标签，给选择器用 |
| `selection_reason` | text | 是 | 入选理由正文 |
| `list_published` | bool | 是 | 名单条目已发布 |
| `basic_intro_published` | bool | 是 | 基础介绍已发布 |
| `standard_ref` | string | 否 | 指向 `star_selection_standard` 的 `content_id` |
| `display_alias` | text | 否 | 展示别名，界面标明不是法定名称 |

### 2.2 `star_selection_standard`（入选标准）

页面 `star`。绑定产业。不下发权重、内部阈值、排名公式、未脱敏原始证据。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `standard_name` | text | 是 | 标准名称 |
| `standard_version` | text | 是 | 版本 |
| `applicable_industry_codes` | string[] | 是 | 适用产业码 |
| `candidate_scope_text` | text | 否 | 候选范围说明，不是算法阈值 |
| `confirmed_dimensions` | string[] | 否 | 已确认维度名称 |
| `updated_at` | datetime | 是 | 标准更新时间 |

未定稿时门户写「入选标准待配置」，企业展示仍保留。

### 2.3 `star_product_panorama`（产品功能全景）

页面 `star`。绑定企业。一个企业可以有多条，按 `sort_order` 升序。门户按这些字段画产品卡、模块、场景、案例和媒体，不把整块收成一段 HTML。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `product_id` | string | 是 | CMS 侧产品 ID，只作内容键，不是企业主数据主键 |
| `product_name` | text | 是 | 产品名称 |
| `product_summary` | text | 是 | 产品摘要 |
| `impact_summary` | text | 否 | 公开影响摘要 |
| `modules` | object[] | 否 | 功能模块，子字段见下表 |
| `scenario_refs` | text[] | 否 | 使用场景，每条一段正文 |
| `case_refs` | text[] | 否 | 行业案例，每条一段正文 |
| `media_refs` | object[] | 否 | 视频、演示、封面，子字段见下表 |

`modules` 的每一项：

| 子字段 | 类型 | 说明 |
|---|---|---|
| `product_module_id` | string | 模块内容键 |
| `module_name` | text | 模块名称 |
| `module_summary` | text | 模块说明 |

`media_refs` 的每一项：

| 子字段 | 类型 | 说明 |
|---|---|---|
| `media_type` | string | 如视频、案例、操作演示 |
| `url` | string | 媒体地址，只传 URL |
| `cover_url` | string | 封面地址，可空 |
| `auth_status` | enum | `authorized` / `pending` / `unavailable`。不是 `authorized` 的媒体不下发 |

没有已发布产品时，门户写「核心产品待完善」，不渲染空产品卡。

### 2.4 `star_tech_narrative`（技术优势正文）

页面 `star`。绑定企业。门户把 `body_html` 嵌进技术优势区。类型遵守 §0 的 `html` 限制。专利数和研发投入占比不在本块，走 §1.3 的指标，不写进 HTML。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `body_html` | html | 是 | 核心技术、原理、成果简介 |

### 2.5 `star_team_strength`（团队实力多维展示）

页面 `star`。绑定企业。字段与授权规则见 §3。类型是 `html`，不是 §2.3 这种拆字段。

### 2.6 生态合作摘要（不设 CMS 字段）

合作摘要来自企业供应链分析的大模型结果，不是任欢维护的内容。不设 `star_ecosystem_note`，也不要合作方名称、关系说明这类表单。图谱边仍走智树图谱数据，不用这段摘要推断边。生成失败时隐藏摘要，不补节点。

### 2.7 `star_story`（发展历程与口碑）

页面 `star`。绑定企业。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `timeline` | object[] | 否 | 每项：`year` string，`title` text，`summary` text |
| `reputation` | text[] | 否 | 已发布的口碑摘要，每条一段 |

### 2.8 `key_chain_structure`（重点企业链位结构）

页面 `key-pano`。绑定产业。环节名和上下游叙述走这里。环节上的企业数走指标，不写进叙述。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `structure_version` | string | 是 | 结构发布版本 |
| `stages` | object[] | 是 | 见下表 |

`stages` 的每一项：

| 子字段 | 类型 | 说明 |
|---|---|---|
| `stage_code` | string | 环节码 |
| `stage_name` | text | 环节名 |
| `upstream_of` | string[] | 下游环节码 |
| `narrative` | text | 该环节的运营叙述 |

未发布时门户写「档案待维护」。统计和链位计数仍可展示。

### 2.9 `key_enterprise_set`（重点企业运营集）

页面 `key-pano`。绑定产业。圈定「展示哪些企业」和关系叙述。企业法定名称、区域、资质以主数据为准，本块不覆盖。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `key_set_items` | object[] | 是 | 见下表 |

`key_set_items` 的每一项：

| 子字段 | 类型 | 说明 |
|---|---|---|
| `enterprise_code` | string | 企业码 |
| `stage_code` | string | 所在环节，对应 §2.8 |
| `relation_text` | text | 关系叙述 |
| `sort_order` | int | 同环节内排序 |

### 2.10 `sz_enterprise_intro`（深圳企业介绍文案）

页面 `shenzhen`。绑定产业，可再绑 `enterprise_code`。未发布则隐藏定位、优势、专家分析，数量和分布仍可展示。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `positioning` | text | 是 | 本地定位 |
| `advantage_summary` | text | 否 | 优势摘要 |
| `expert_analysis` | text | 否 | 专家竞争力分析 |

### 2.11 `sz_focus_set`（深圳重点企业圈定）

页面 `shenzhen`。绑定产业。只圈定展示名单。企业事实走主数据。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `focus_set_items` | object[] | 是 | 每项：`enterprise_code` string，`sort_order` int |

### 2.12 `display_name_alias`（展示别名）

各页可共用。绑定企业。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `display_alias` | text | 是 | 展示用别名。界面标明不是法定名称，不覆盖工商名称 |

### 2.13 空态

| 场景 | 门户文案 | 行为 |
|---|---|---|
| 产业没有已发布明星名单 | 本产业明星企业待配置 | 不跨产业补位，不用算法补名单 |
| 入选标准未定稿 | 入选标准待配置 | 企业展示保留 |
| 没有已发布产品 | 核心产品待完善 | 不渲染空产品卡 |
| 没有可下发的团队 HTML | 核心团队资料待完善 | 不虚构履历 |
| 供应链分析摘要未生成 | 不展示合作摘要 | 不生成虚假节点；图谱边仍按图谱数据显示 |
| 媒体未授权或地址失效 | 资源暂时不可用，请重试 | 保持区块高度 |
| 重点企业档案未发布 | 档案待维护 | 统计仍可展示 |
| 深圳介绍未发布 | 不显示专家观点区 | 数量和分布仍可展示 |
| CMS 超时或 5xx | 内容服务暂不可用 | 只影响 CMS 区，指标区照常 |
| 科学家/核心人才比例未发布 | 不展示比例数字和成员表 | 上方团队 HTML 仍可单独展示 |

### 2.14 `star_scientist_ratio`（科学家/核心人才比例）

页面 `star`，位于团队 HTML 下方。绑定企业。CMS 后台做成表单，不要做成指标，也不要写进 `star_team_strength.body_html`。

一条记录对应一家企业。成员按行增删。只下发 `publish_status=published` 的记录；成员行再按各自行的发布状态过滤。

| 表单项 | 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| 科学家/核心人才比例 | `ratio_percent` | number | 是 | 0–100 的百分数。界面右侧显示为 `38%` 这种形式。运营手填 |
| 数据时间 | `data_time` | date | 是 | 界面上的「数据时间」，如 `2026-07-14` |
| 团队成果 | `team_achievement` | text | 否 | 界面底部那一句成果说明 |
| 成员 | `members` | object[] | 是 | 至少一行。子字段见下表 |

`members` 每一行：

| 表单项 | 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| 核心成员 | `member_name` | text | 是 | 如「核心成员 A」 |
| 职务/领域 | `title` | text | 是 | 如「首席科学家 / 技术负责人」 |
| 发布状态 | `publish_status` | enum | 是 | `published` 已发布 / `draft` 未发布。未发布的行不下发 |
| 照片授权 | `portrait_authorization_status` | enum | 是 | `authorized` 已授权 / `pending` 待授权 / `unavailable` 不可用 / `no_asset` 无素材 |
| 外链授权 | `external_link_authorization_status` | enum | 是 | 取值同上。`no_asset` 表示没有外链素材 |

`no_asset` 只表示这一格没有素材，不因此整段比例隐藏。比例数字随整条记录的发布状态下发。

---

## 3. 团队实力多维展示（本轮样例）

门户上这块是明星企业介绍里的嵌入区。任欢侧提供一个 HTML 字段，门户把返回的 `body_html` 嵌进该区。

| 项 | 值 |
|---|---|
| content_type | `star_team_strength` |
| 字段 | `body_html` |
| 类型 | `html` |
| 绑定 | `enterprise_code` + `future_industry_code` |
| 页面 | `page_key=star`，明星企业介绍 |

HTML 里放运营编写的团队展示：成员介绍、主张、专业领域、行业成就、主导项目、团队成果、已授权的人物图片 URL 和外链。切换成员若要做轮播，由这段 HTML 自己表达，门户不再用结构化成员列表拼卡片。

门户嵌入路径只读 `body_html`。照片和外链授权不靠解析 HTML。内容项上另有两枚枚举：`portrait_authorization_status`、`external_link_authorization_status`，取值 `authorized` / `pending` / `unavailable`。两枚都为 `authorized` 且 `publish_status=published` 时，整段 HTML 才下发。任一未授权，整段不下发，门户显示「核心团队资料待完善」。人物照片和外链能否公开展示仍待确认（决策项 Q041），本规则先按整段授权执行。

早期曾设计过按人拆开的 `star_team_member`，门户本轮不用它拼卡片。字段留在这里，避免和 HTML 块搞混：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `team_member_id` | string | 是 | 成员内容键 |
| `name` | text | 是 | 姓名 |
| `title` | text | 是 | 职务或领域 |
| `profile_summary` | text | 否 | 画像摘要 |
| `professional_domains` | string[] | 否 | 专业领域 |
| `industry_achievements` | string[] | 否 | 行业成就 |
| `leading_projects` | string[] | 否 | 主导项目 |
| `avatar_url` | string | 否 | 照片 URL |
| `portrait_authorization_status` | enum | 是 | `authorized` / `pending` / `unavailable` |
| `external_profile_url` | string | 否 | 外部主页 |
| `external_link_authorization_status` | enum | 是 | 同上 |

若以后改回门户自己画成员轮播，用上表，不再嵌 `body_html`。同一屏不要两套同时渲染。

「科学家/核心人才比例」留在 HTML 外面，用 §2.14 的表单录入。界面上的 38% 来自运营填写的 `ratio_percent`，不走指标。

---

## 4. 读接口

### 4.1 任欢侧：已发布块列表

智树 Java 调用。浏览器不调用。

`GET {cms_base}/api/published/enterprise-development/blocks`

| 查询参数 | 必填 | 说明 |
|---|---|---|
| `future_industry_code` | 是 | 当前产业 |
| `page_key` | 否 | 不传则返回该产业下企业发展全部已发布块 |
| `enterprise_code` | 否 | 传了则只返回该企业的块，外加不绑企业的产业级块（标准、链结构） |
| `content_type` | 否 | 例如只要 `star_team_strength` |
| `locale` | 否 | 默认 `zh-CN` |

响应 `200`：

```json
{
  "future_industry_code": "integrated-circuit",
  "page_key": "star",
  "enterprise_code": "ENT-0001",
  "blocks": [
    {
      "content_id": "cms-star-team-0001",
      "content_type": "star_team_strength",
      "page_key": "star",
      "enterprise_code": "ENT-0001",
      "future_industry_code": "integrated-circuit",
      "version": "3",
      "publish_status": "published",
      "publish_time": "2026-10-20T10:00:00+08:00",
      "sort_order": 1,
      "locale": "zh-CN",
      "portrait_authorization_status": "authorized",
      "external_link_authorization_status": "authorized",
      "body_html": "<p>……</p>"
    }
  ]
}
```

只返回 `publish_status=published` 的块。团队块还要满足 §3 的两枚授权。没有已发布内容时 `200` 且 `blocks: []`，不要回退草稿。

| HTTP | 含义 | 门户处理 |
|---|---|---|
| 200 + 空数组 | 无已发布内容 | 对应空态文案 |
| 404 | 产业或企业不存在 | 同空态 |
| 401 | 服务凭证无效 | CMS 区不可用，指标区照常 |
| 429 / 5xx / 超时 | 任欢侧不可用 | CMS 区骨架「内容服务暂不可用」 |

服务凭证名待联调，不复用门户用户登录态。本单不规定 URL 主机。

### 4.2 任欢侧：单块

`GET {cms_base}/api/published/enterprise-development/blocks/{content_id}`

路径参数 `content_id`。未发布返回 404。字段与列表元素相同。

### 4.3 智树门户对浏览器（形状冻结，本单不实现）

`GET /portal/v1/enterprise-development/pages/{page_key}`

查询参数：`future_industry_code` 必填；`star` 与需要企业的块再传 `enterprise_code`。

响应分成三栏：

- `cms`：§4.1 的 `blocks`，原样嵌 HTML，不改写。
- `metrics`：只列本页要用的 `metric_id` 与指标服务返回值。值不来自任欢。
- `llm`：`key-pano` 的瓶颈/结构解读，以及 `star` 上企业供应链分析给出的生态合作摘要。都由智树内部调用大模型生成，不来自任欢，也不进 `metrics`。生成接口本单不展开。

`page_key=overview` 时 `cms.blocks` 为空数组，只有 `metrics`。

这条路径走门户网关，不注册到 `/cms/v1`。

---

## 5. 给任欢的对接摘要（仅企业发展）

请在内容管理里为企业发展维护 §2 的字段。明星企业介绍里有两段 HTML 富文本，门户直接嵌入：团队实力多维展示（`star_team_strength.body_html`），以及技术优势中的核心技术/原理/成果简介（`star_tech_narrative.body_html`）。专利数和研发投入占比不要写进后一段。科学家/核心人才比例按 §2.14 做表单：比例百分数、数据时间、团队成果，以及成员行（核心成员、职务/领域、发布状态、照片授权、外链授权）。

请提供 §4.1、§4.2 两个只读接口，只出已发布内容。团队块在照片和外链授权未通过时不要输出 HTML。

专利数、研发投入占比、各类企业计数不在这些接口里。那些数字由智树指标服务出，门户另栏展示。科学家/核心人才比例不是指标，按 §2.14 做表单。重点企业全景图上的瓶颈/结构解读、明星企业介绍里的生态合作摘要，都不是 CMS 字段：前者由智树调用大模型生成，后者用企业供应链分析里已有的大模型摘要。

---

## 6. 待确认（确认本模块时请看这四条）

1. 团队展示以整段 HTML 嵌入为准，结构化 `star_team_member` 不参与门户拼卡片。若仍要门户自己画成员轮播，本条需要改回结构化字段。
2. 科学家/核心人才比例按 §2.14 表单录入。界面上的 38% 是 `ratio_percent`，成员表是 `members`。
3. 产品全景、历程本轮仍是结构化或纯文本。团队块和技术优势正文是 HTML。生态合作摘要不进 CMS。
4. 指标缺口（历年总数趋势、专利数、深圳趋势、深圳规模、上市/国企数、领域证据数）只登记，不在本单新编 `metric_id`。人才比例不在这份缺口里。

---

## 7. 文中决策项

这些编号是尚未拍板的事项。本文只引用，不代替拍板。

| 编号 | 在本文中的意思 |
|---|---|
| Q-E32-01 | 科研人数怎么加工，仍待确认 |
| Q038 | 「重点企业」专利总量阈值暂按 50，未最终确认 |
| Q040 | 产业生态图谱正式边的口径仍待确认。合作摘要已明确取企业供应链分析的大模型结果，不进 CMS |
| Q041 | 团队人物照片和外部主页能否公开展示，未最终确认 |
| Q048 | 明星名单准入，以及专利数、研发占比的正式口径，未最终确认。人才比例已改为 CMS 手填，不再挂在本项 |
