# DATA-ENT-CMS-VS-APP-PARTITION-L01

> **文档性质**：coordinator → data-agent **数据分析派单包** + **分区结论（data-agent 已复核）**  
> **任务 ID**：`DATA-ENT-CMS-VS-APP-PARTITION-L01`（已登记 `task-registry.yaml`）  
> **模块范围**：E-31 企业总览 → **E-33 重点企业概览 / E-34 明星企业介绍 / E-35 深圳企业介绍**（demo-ui-topic 当前原型页）  
> **派单角色**：coordinator-agent  
> **执行角色**：data-agent（主）· 会签：product（口径）/ architect（低耦合边界）/ api（契约消费）  
> **监管人**：`supervised_by: human:淮政玮`  
> **性质**：设计/分析类（`cicd: skip`）  
> **状态**：`review` — data-agent 已复核 §3–§6、产出契约附录、回填决策清单；待 coordinator 验收 DoD  
> **日期**：2026-07-16  
> **作者标记**：`[agent:coordinator]` 初版 · `[agent:data-agent]` 复核升版  
> **cost**：`actual_tokens: 145000` · `model_used: cursor-grok-4.5` · `actual_cost: 0.85` · `cost_warn: green`

---

## 0. 派单话术（粘贴新开会话）

```markdown
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师，精通数仓分层(ODS/DWD/ADS)、
      数据契约与血缘；践行「标准表冻结 + Mock 先行 + 数据工厂解耦三方源」。
任务 ID：DATA-ENT-CMS-VS-APP-PARTITION-L01
性质：设计类（cicd: skip）
仓库/路径：
  - 编排：gkx-orchestration/agent-delivery/
  - UI 对照：repos/demo-ui-topic（只读，不改代码）
目标：
  在「科技专题内容运营中心由久新交付、须尽量低耦合」约束下，完成 E-33/E-34/E-35
  页面字段级「CMS 运营内容 vs 应用侧 ODS→DWD→ADS 计算」分区；冻结消费契约与禁耦合清单。
必读（P0）：
  - 本文件（派单结论初稿，须复核）
  - bid-reference/五、实施方案-智能服务集群-ZP-2025-11-18.docx
    → 科技专题内容运营中心（基础数据管理 / 专家知识管理 / 门户内容管理）
  - bid-reference/科技信息展示系统和科技专题服务系统.md
    → §1.1.1.2.4.5（尤其 5.1.2/5.1.3/5.1.6/5.1.7、5.2.2/5.2.3、5.6.3）
  - bid-reference/智慧服务门户系统-要素相关.md → 企业发展 E-33/E-34/E-35
  - agent-handoffs/产品整体定义/E-31-企业发展/**/USM-*.md、TRACE-*.yaml
  - architecture-baseline.md（前端→Java→ADS；算法只在 Python）
  - data-lineage-policy.md（统计指标 8 件套）
  - 客户决策清单跟踪表.md（Q041/Q047/Q048/Q049 及相关 🟡）
对照实现（只读）：
  - demo-ui-topic/src/app/pages/development/{KeyEnterprisesPanorama,StarEnterprises,ShenzhenEnterprises}.tsx
  - demo-ui-topic/src/app/mock/enterprise/portalAggregates.ts
  - demo-ui-topic/src/app/pages/development/developmentData.ts（E-32 若需对齐目录字典）
架构铁律（派单必带）：
  1. 算法只在 Python；Java 禁止 NLP/图谱算法/模型推理
  2. 调用链：前端 → Java REST →（必要时）Python /internal/*；不可越层
  3. 图谱：NebulaGraph；禁止 Neo4j
  4. 可观测性：Java Agent + Python instrument + 前端 observability.ts
  5. CI/CD：设计类可 skip；若动代码须 Pipeline 绿
  6. demo2/demo-ui-* 只读 merge 铁律：不 merge 进 lumen
  7. 共享聚合：Java 只读 ADS；不直连 nGQL、不写算法
  8. 数据策略：ADS 先行 + Mock；三方源由数据工厂映射
  9. Design.md / D10 交互规范：本任务不改 UI，仅标注 metric_id 与 MockBadge 义务
  10. 数据血缘：凡统计数字必须可挂 8 件套；Wave0 Mock 必有 🧪
久新低耦合硬约束（本任务特有）：
  - 禁止把久新 CMS 库表/内部 ID 写进 ADS DDL 或 Java Entity
  - 只消费「已发布内容只读契约」（enterprise_code / content_id / version / publish_status / sort_order）
  - ODS 工商/标签/专利等贴源真源不以 CMS 覆盖；CMS 只做运营层叠加与发布
  - 应用侧聚合、趋势、资质计数、论文专利领域抽取一律走 ODS→DWD→ADS（或算法写 ADS）
DoD：
  1. 复核本文件 §3–§6 分区表：逐条 ✅确认 / △修订 / ❌驳回，并写修订说明
  2. 产出「久新 CMS 只读契约字段表」与「ADS 指标/实体键表」（可附于本文件附录或同目录新文件）
  3. 每个「应用计算」项补齐：源 ODS 表（或缺口）、目标 DWD/ADS、metric_id 或 DEMO/Qxxx、更新频率
  4. 每个「CMS」项补齐：久新能力锚点（招标章节号）、发布态字段、失败降级（空态文案）
  5. 列出禁耦合清单（禁止事项 ≥8 条）与联调顺序（契约 Mock → ADS Mock → Java → UI 换源）
  6. 开放口径登记到 客户决策清单跟踪表（若新增）+ 回填 Q041/Q047/Q048/Q049 关联说明
  7. handoff：更新本文件 status + cost 四字段（actual_tokens/model_used/actual_cost/cost_warn）
不要问调度者实现细节；完成后通知 coordinator 验收本 DoD。
```

---

## 1. 背景与问题

### 1.1 为什么拆

demo-ui-topic「企业总览」三 Tab（重点 / 明星 / 深圳）当前大量为可替换 Mock。上线路径上存在两类真源：

| 真源 | 责任方 | 典型内容 |
|------|--------|----------|
| **内容运营中心（CMS）** | **久新**（伙伴交付） | 运营名单、介绍文案、产品全景、团队、媒体、入选标准、专家知识、门户专题页 |
| **应用数据计算** | 本团队（data/algo → ADS → Java） | 企业主数据、资质标签、专利/论文聚合、数量对比、趋势、规模结构、领域覆盖统计 |

若不分区，会出现：重复建库、把统计写进 CMS、或把叙事文案塞进 ADS，导致与久新**强耦合**、口径难维护。

### 1.2 招标锚点（久新侧能力）

对照 `五、实施方案…docx` / `科技信息展示系统和科技专题服务系统.md` **§1.1.1.2.4.5 科技专题内容运营中心**（用户红框相关）：

| 招标章节 | 能力 | 与本三页关系 |
|----------|------|----------------|
| **5.1.2 产品链内容管理工具** | 产品实体、产业分类、产业动态/区域数据 | E-34 产品功能全景的**产品本体与说明** |
| **5.1.3 企业内容管理工具** | 企业主体维护、重点标识、动态与深圳专项 | 企业运营侧档案叠加；**不得取代 ODS 工商真源** |
| **5.1.6 政策内容管理工具** | 政策条目校正/增删 | 本三页弱相关（若生态/历程引用政策摘要则只读已发布） |
| **5.1.7 产业服务机构内容管理工具** | 服务机构本体与动态 | E-34 产业生态中「服务型合作方」叙述可挂接 |
| **5.2.2 产业链专家知识管理** | 结构与周期、瓶颈与深圳区域知识 | E-33 链结构说明/瓶颈文案；E-35 领域叙事补充 |
| **5.2.3 企业专家知识管理** | 发展历程、招引/培育推荐知识 | E-34 历程/口碑类专家叙述；招引培育**不进**本三页（范围外） |
| **5.6.3 企业发展内容管理（门户）** | 重点企业全景内容、**明星与深圳企业介绍维护** | **E-33/E-34/E-35 门户叙事与名单的主 CMS 出口** |

> USM-ENT-SHENZHEN 已显式引用：`1.1.1.2.4.5.6.3.3 明星企业与深圳企业介绍维护`。

### 1.3 低耦合原则（本派单冻结）

1. **身份键统一**：业务主键用本系统稳定码（建议 `enterprise_code` / `org_id` / `credit_code` 三选一并映射），久新侧 `content_id` 仅作内容引用，不进 ADS 主键。  
2. **发布态消费**：前台只读 `publish_status=published`；草稿/内部标准阈值不下发门户。  
3. **真源分治**：工商、标签、专利、论文、财报 → ODS/贴源；叙事、排序、媒体、入选理由 → CMS。  
4. **接口形态**：Java Facade 聚合「ADS 指标包 + CMS 内容包」；前端不直连久新。  
5. **失败隔离**：CMS 超时/空发布 → 业务空态；ADS 失败 → 统计区骨架/重试；互不拖垮。  
6. **禁止**：共享库账号、共享表、反向写久新库、用 CMS 字段覆盖 ODS 冲突而不留审计。

---

## 2. 页面范围与 DEMO 现状

| 页面 | 路由（权威） | DEMO 数据入口 | 现状 |
|------|----------------|---------------|------|
| E-33 重点企业概览 | `?tab=key-enterprises` | `portalAggregates` + `ENTERPRISE_LIST` | 全 Mock；Q047 未闭合 |
| E-34 明星企业介绍 | `?tab=star-enterprises` | `STAR_ENTERPRISE_*` + `ENTERPRISE_LIST` | 已按 CMS 发布态建模（Mock）；指标 DEMO/Q048 |
| E-35 深圳企业介绍 | `?tab=shenzhen` | `SHENZHEN_*` + `ENTERPRISE_LIST` | 统计 Mock；本地介绍 CMS 待接（Q049） |

截图场景（明星企业）：未来产业=集成电路、企业=深芯微…、入训理由、遴选标准、产品功能全景 — 与 USM-E34「运营名单 + CMS 内容 + 数据侧指标」一致。

---

## 3. 分区总则（判定规则）

| 判定 | 归类 | 说明 |
|------|------|------|
| 需人工撰写/审核/发布，版本化叙事 | **CMS（久新）** | 理由、标准正文、产品介绍、团队画像、媒体、专家观点 |
| 可从贴源库聚合/算法产出，可复算 | **应用计算（ADS）** | 数量、趋势、资质计数、专利数、研发占比（有口径）、领域关键词抽取 |
| 运营圈定「是谁」，事实属性「是什么」 | **混合** | 名单/排序/是否明星→CMS；该企业标签/专利→ADS；页面 join |
| 官方产业目录编码 | **待甲方（🟡）+ 应用字典** | 不由久新私自定义「正式八大」；CMS 只引用已发布目录码 |

---

## 4. 字段级分区表（data-agent 已复核）

图例：**CMS** = 久新只读发布；**APP** = ODS→DWD→ADS（+算法）；**HYBRID** = join；**PENDING** = 口径未定。  
复核列：✅确认 / △修订 / ❌驳回。招标简写 `5.x` ↔ 实施方案 `1.1.1.1.4.2.5.x`（见 `CMS-read-contract-E31.md` §0.1）。

### 4.1 E-34 明星企业介绍（截图主页面 · 最清晰）

| UI 区块 / 字段 | 归类 | 久新锚点 | 应用侧锚点 | 低耦合要点 | 复核 |
|----------------|------|----------|------------|------------|------|
| 未来产业选择器选项 | **HYBRID** | 可维护展示名/简介 | **有效产业目录码**（字典/配置，非 CMS 发明） | CMS 不得私自增删「正式目录」；只消费已发布 `future_industry_code` | ✅ |
| 当前产业明星企业名单 + `sort_order` | **CMS** | 5.6.3 / 门户 31.3 | — | 固定运营名单，**禁止**算法 TopN 冒充 | ✅ |
| 「共 N 家明星企业」 | **APP** | — | 对 CMS 已发布名单契约 `COUNT`（`M_ENT_STAR_ROSTER_COUNT`） | **非 ODS 聚合**；避免双写 | △ 明确聚合对象=CMS 契约 |
| 入选标签 `selectionTag` | **CMS** | 5.6.3 | — | 一句话运营标签 | ✅ |
| 入选理由 `selectionReason` | **CMS** | 5.6.3 / 5.2.3 | — | 纯叙事 | ✅ |
| 遴选标准名称/版本/适用产业/更新时间/已确认维度（只读） | **CMS** | 5.6.3 + 专家知识 | — | **禁止**下发权重/阈值/排名算法细节 | ✅ |
| 企业名称、所属产业展示 | **HYBRID** | 名单绑定 `enterprise_code` | ODS `dwd_org_reg_info` → DWD | 名称以主数据为准；CMS 别名须标明 | ✅ |
| 资质荣誉标签 | **APP** | 重点标识仅运营叠加 | `dwd_org_tag_info` → DWD/ADS | CMS「重点标识」≠ 标签真源 | ✅ |
| 数据时间 | **APP**（统计）+ **CMS**（发布）并列 | `publish_time` | `calc_batch_id` | UI 勿混为一词 | △ 允许并列展示两套时间 |
| 产品功能全景 | **CMS** | **5.1.2** + 5.6.3 | — | 媒体 URL/授权态只走 CMS | ✅ |
| 技术优势：专利数、研发占比 | **APP** | — | ADS + Q048 metrics | 无口径则 🧪+🟡 | ✅ |
| 技术优势：科学家/人才占比 | **PENDING→APP 优先** | — | `M_ENT_STAR_SCIENTIST_RATIO`；口径未定 | TRACE 写「数据侧或 CMS 待确认」；**禁止 CMS 手填冒充实算**；闭合前 🧪+Q048 | △ 由纯 APP 改为 PENDING |
| 技术优势：核心技术条目、成果简介文案 | **CMS** | 5.6.3 | 关联 `patent_id[]` **APP** | 拆分：文案 CMS / 证据 ID APP（取消含糊「可 HYBRID」） | △ |
| 团队实力 | **CMS** | 5.1.5 + 5.6.3 | — | 授权失效隐藏外链（Q041） | ✅ |
| 产业生态：合作伙伴名称与关系摘要 | **HYBRID** | 5.6.3；可挂 5.1.7 | **正式边** Q040 图谱/ADS；CMS 仅运营摘要文案 | 正式态不以 CMS 推断边；DEMO 勿造假节点 | △ 与 Q040 对齐：图谱权威、CMS 叙述 |
| 发展历程、口碑摘要 | **CMS** | 5.2.3 / 5.6.3 | DEMO 可用官网公开事实并注明 | 上线以 CMS 已发布为准 | ✅ |
| 「进入企业画像」跳转 | **APP** | — | 统一档案路由 | 仅传 `enterprise_code` | ✅ |

### 4.2 E-33 重点企业概览

| UI 区块 / 字段 | 归类 | 久新锚点 | 应用侧锚点 | 低耦合要点 | 复核 |
|----------------|------|----------|------------|------------|------|
| 当前未来产业 + 当前产业链选择 | **HYBRID** | 5.6.1 结构展示 | ODS 挂链 / 自建 DWD | 展示结构可 CMS；挂链统计 APP | ✅ |
| 上中下游重点企业卡片名单 | **HYBRID** | 5.6.3 重点集 | APP 挂链 + Q038 候选 | **冻结 join**：CMS `key_enterprise_set` ∩ APP `enterprise_chain_link`；冲突以 CMS 发布态为准并审计 | △ 写明 join 键与冲突规则 |
| 链位导航结构 / 节点企业数 | **CMS** / **APP** | 5.6.1 / 5.2.2 | ODS + `COUNT` | 结构版本号走 CMS | ✅ |
| 整链资质规模统计 | **APP** | — | `M_ENT_KEY_QUAL_SCALE`（Q047） | **禁止**手填 CMS | ✅ |
| 领域统计 / 论文专利关键词证据 | **APP** | 解读文案可 CMS | Python → ADS（Q047） | 文案不替代证据表 | ✅ |
| 企业基础信息 | **APP** | 运营摘要可选 CMS | ODS 主数据 | 同 E-34 | ✅ |
| 合作/供应链描述性关系文案 | **CMS** | 5.6.3 | 可选图谱 APP | 描述≠风险诊断 | ✅ |

### 4.3 E-35 深圳企业介绍

| UI 区块 / 字段 | 归类 | 久新锚点 | 应用侧锚点 | 低耦合要点 | 复核 |
|----------------|------|----------|------------|------------|------|
| 未来产业目录（选项集合） | **APP 字典**（正式码待甲方） | 可展示名 | 同源目录服务（Q049） | 与 E-32/E-34 共用；CMS 不发明正式码 | △ 从 PENDING→明确 APP 字典供给 |
| 产业企业数量对比柱状图 | **APP** | — | `ads.ent_sz_industry_summary` | 仍 Mock；挂 Q049 | ✅ |
| 所选产业历年趋势 | **APP** | — | `ads.ent_sz_industry_trend` | CMS 禁止手填趋势 | ✅ |
| 领域分布 | **HYBRID** | 链全景结构 CMS（5.6.1） | 领域计数 APP | 「已识别 X」=项数≠覆盖率 | ✅ |
| 规模结构（大/中/小/微） | **APP** | — | `M_ENT_SZ_SCALE_DIST` | DEMO 存在「规上/大中小微」与「大中小微」两套枚举，闭合前统一到 Q049 | △ |
| 深圳重点企业列表 | **HYBRID** | 5.6.3 圈定+文案 | 档案+资质 APP | 列表圈定 CMS；事实 APP | ✅ |
| 本地定位/优势/专家分析 | **CMS** | 5.6.3 + 5.2.2 | — | 未发布则隐藏 | ✅ |
| KPI：上市数/国企数等 | **APP** | — | ADS | 系数放大须 🧪 | ✅ |

### 4.4 明确不进本三页（防范围漂移）

| 内容 | 原因 |
|------|------|
| 招引企业推荐清单/培育策略（5.2.3.2/3） | 属战略分析/推荐能力，非企业总览门户三 Tab |
| 技术力/商业力榜单维护（5.6.3.2） | 评估榜单另页；E-33 不做排名 |
| 政策条目全文管理 | 政策模块；本页最多引用摘要 |

---

## 5. 推荐数据流（低耦合）

```text
[三方 ODS / 贴源] --数据工厂--> [DWD] --算法/SQL--> [ADS 指标与实体事实]
                                              |
                                              v
[久新 CMS 已发布 API] --契约--> [Java Facade 聚合] --> [前端 E-33/34/35]
         ^                            |
         |                     只拼装，不改写真源
    运营/专家在久新后台维护
```

**Java 聚合伪契约（建议）**

```json
{
  "enterprise_code": "ENT-0001",
  "future_industry_code": "integrated-circuit",
  "data_batch_id": "2026-07-14",
  "facts": {
    "name": "...",
    "tags": ["上市", "专精特新"],
    "patent_count": 128,
    "rd_ratio": 18.6,
    "metric_refs": ["M_ENT_STAR_RD_RATIO"]
  },
  "cms": {
    "content_id": "cms-star-...",
    "version": "3",
    "publish_status": "published",
    "selection_reason": "...",
    "product_panorama": [],
    "team_members": []
  }
}
```

---

## 6. 禁耦合清单（data-agent 确认 · 12 条）

| # | 禁止事项 | 复核 |
|---|----------|------|
| 1 | 禁止 ADS/DWD DDL 引用久新内部表名或外键 | ✅ |
| 2 | 禁止前端直连久新；禁止 Python 算法直写 CMS | ✅ |
| 3 | 禁止用 CMS 手填数覆盖 ADS 统计（默认禁止；若破例须 `source=cms_override` 审计且本三页不允许） | ✅ |
| 4 | 禁止把入选标准内部权重/阈值暴露给门户 | ✅ |
| 5 | 禁止算法 TopN 静默写入「明星企业」发布名单 | ✅ |
| 6 | 禁止三套「八大未来产业」私有列表分叉（E-32/34/35 必须同源 APP 字典） | ✅ |
| 7 | 禁止 CMS 工商字段与 ODS 冲突时静默以 CMS 为准 | ✅ |
| 8 | 禁止在 demo 验收材料中把 Mock 叙事宣称为久新已发布或 ODS 已贯通 | ✅ |
| 9 | 禁止把产品视频等二进制写入 innov PG；媒体只走 CMS/对象存储 URL | ✅ |
| 10 | 禁止 Java 内解析 CMS 富文本为指标计算输入（计算只认结构化 ADS） | ✅ |
| 11 | 禁止将久新 `content_id` / 内部 ID 写入 ADS 主键或 Java Entity PK | ✅ 新增明确 |
| 12 | 禁止 CMS「重点标识」替代 `dwd_org_tag_info` 资质真源 | ✅ 新增明确 |

---

## 7. 与客户决策 / 开放项映射（已回填）

| 编号 | 与分区关系 | data-agent 动作 | 状态 |
|------|------------|-----------------|------|
| **Q041** | E-34 产品/团队/媒体 CMS | 契约 §3.3–3.5 对齐；授权门闩写入 CMS-read-contract | 🟡 已关联说明 |
| **Q047** | E-33 三项统计 | 纯 APP；metric 建议名 + ODS 候选入 ADS-facts §3.1 | 🟡 已关联说明 |
| **Q048** | E-34 名单 CMS + 量化 APP | 名单/标准→CMS；专利/RD/人才比→APP | 🟡 已关联说明 |
| **Q049** | E-35 统计 APP + 介绍 CMS | 目录 APP 同源；介绍 `sz_enterprise_intro`；规模枚举统一待闭合 | 🟡 已关联说明 |
| **Q050** | 久新发布 API ↔ 消费契约签字 | **新增** 客户决策清单 | 🟡 新增 |
| **Q038** | E-33/E-35 重点判定阈值 | APP 候选侧；与 CMS 重点集 join | 🟡 引用 |
| **Q040** | 生态图谱边 | APP/图库；CMS 仅关系摘要文案 | 🟡 引用 |

---

## 8. data-agent 交付物清单（DoD）

| # | 交付物 | 路径 | 状态 |
|---|--------|------|------|
| A | 本文件复核批注（§4 逐条） | 本文件 | ✅ |
| B | 久新 CMS 只读契约 | `CMS-read-contract-E31.md` | ✅ |
| C | ADS 指标/实体键契约 | `ADS-facts-contract-E31.md` | ✅ |
| D | 联调顺序与 Mock 夹具 | §12 + CMS-read §6 | ✅ |
| E | 客户决策清单回填 + Q050 | `客户决策清单跟踪表.md` | ✅ |
| F | cost 四字段 + registry | 本文件头 + `task-registry.yaml` | ✅ → review |

**工作量**：`effort_points: 5` · `difficulty: M` · `estimated_tokens: 180_000`。

---

## 9. coordinator 验收清单

- [x] §4 分区无「未标注」行；HYBRID 均有 join 键（E-33：`enterprise_code`+`stage_code`；E-34/35：`enterprise_code`+`future_industry_code`）  
- [x] 禁耦合清单 ≥8（现 12）且交付物未违反  
- [x] Q041/Q047/Q048/Q049 均有落点说明；新增 Q050  
- [x] 契约字段级可被 api-agent 开 OpenAPI（CMS-read + ADS-facts）  
- [x] 未要求久新改造内部库（只要求发布 API/导出契约）  
- [x] cost 已回填  
- [ ] **待 coordinator 勾选关闭** → `done`

---

## 10. 结论摘要（供站会 30 秒）

- **E-34**：叙事/名单/产品/团队/媒体/标准 → **久新 CMS**；资质/专利/研发占比/数据批次 → **应用 ADS**；「共 N 家」= APP 对 CMS 发布名单计数。  
- **E-33**：链结构与重点集 → **CMS**；挂链事实与资质/领域证据统计 → **APP**；名单 = CMS∩APP。  
- **E-35**：数量对比/趋势/规模/领域计数 → **APP**；定位/优势/专家文案与展示圈定 → **CMS**；目录字典 APP 同源供给。  
- **当前 DEMO**：均为可替换 Mock；**不得**宣称已接久新或 ODS 贯通。

---

## 11. 修订记录

| 版本 | 日期 | 作者 | 说明 |
|------|------|------|------|
| v0.1 | 2026-07-16 | coordinator-agent | 派单包 + 初版分区 |
| v1.0 | 2026-07-16 | data-agent | 复核 §3–§6（✅/△）；产出 CMS/ADS 契约；回填 Q041/047/048/049 + 新增 Q050；禁耦合扩至 12；转 review |

---

## 12. 联调顺序（冻结）

```text
① CMS 契约 Mock（按 CMS-read-contract-E31 字段形）
      ↓
② ADS Mock（按 ADS-facts-contract-E31；calc_batch_id=mock_*；MetricSpec 8 件套可展示）
      ↓
③ Java Facade 聚合（facts + cms；失败隔离；不直连 nGQL/不写算法）
      ↓
④ UI 换源（demo-ui-topic / lumen 去掉本地硬编码 portalAggregates；保留 🧪 直至去 mock_）
      ↓
⑤ 数据工厂：真实 ODS → DWD → ADS；久新发布 API 替换契约 Mock（Q050 签字后）
```

**验收门禁**：①② 可并行；③ 依赖 ①② 字段冻结；④ 不阻塞久新环境；⑤ 不得破坏 Java/前端契约面。

---

## 13. data-agent 修订说明汇总

| 编号 | 类型 | 说明 |
|------|------|------|
| R1 | △ | 「共 N 家」明确为对 **CMS 已发布名单** 的 APP COUNT，非 ODS |
| R2 | △ | 技术优势文案 vs 专利证据 ID 拆分为 CMS / APP，取消含糊 HYBRID |
| R3 | △ | E-33 重点集冻结 join：`key_enterprise_set` ∩ `enterprise_chain_link` |
| R4 | △ | E-35 目录供给明确为 APP 字典；规模枚举 DEMO 不一致记入 Q049 |
| R5 | △ | 统计批次时间与 CMS `publish_time` 允许并列、禁止混称 |
| R6 | ✅ | §3 判定规则、§5 数据流、§6 原 10 条禁耦合均确认；另增 content_id / 重点标识 2 条 |
| R7 | ❌ | 无整行驳回；招引/培育/榜单维护仍按 §4.4 排除 |
| R8 | △ | 科学家/人才占比改为 PENDING（Q048）；产业生态正式边以 Q040 图谱为准、CMS 仅摘要（对照 USM/TRACE 探索） |
| R9 | 注 | UI Mock 探索补充：`M_ENT_STATE_OWNED_COUNT` 页面已引用但 cfg/seed 未登记；E-35「重点企业数」勿复用 `M_ENT_TOTAL_COUNT`，建议 `M_ENT_SZ_KEY_COUNT`；ODS 候选表清单见 ADS-facts 附录 |

---

## 通知 coordinator

> **DATA-ENT-CMS-VS-APP-PARTITION-L01** 已提交 `review`。请按 §9 验收 DoD；证据路径见 §8。  
> 监管人：`human:淮政玮` · 执行：`agent:data-agent`。
