# CMS-read-contract-E31

> **任务**：`DATA-ENT-CMS-VS-APP-PARTITION-L01`  
> **性质**：久新「科技专题内容运营中心」→ 应用侧 **只读消费契约**（字段级）  
> **范围**：E-33 重点企业概览 / E-34 明星企业介绍 / E-35 深圳企业介绍  
> **状态**：data-agent 冻结草案（待久新接口联调确认字段名；语义不可漂移）  
> **日期**：2026-07-16  
> **作者**：`[agent:data-agent]` · 监管 `human:淮政玮`

---

## 0. 契约原则（不可协商）

1. 应用侧 **只消费已发布内容**；草稿/审核中不下发门户。  
2. **业务主键** = 本系统稳定码 `enterprise_code`（可映射 `credit_code` / `org_id`）；久新 `content_id` **仅内容引用，禁止进 ADS 主键 / Java Entity PK**。  
3. 禁止共享库账号、共享表、反向写久新；媒体只传 URL，不入 innov PG 二进制。  
4. Java Facade 聚合 CMS 包 + ADS 包；前端 / Python **不直连**久新。  
5. CMS 失败与 ADS 失败 **隔离降级**（见 §5）。

### 0.1 招标锚点对照

| 派单简写 | 实施方案 docx（智能服务集群） | 门户要素 / USM |
|----------|------------------------------|----------------|
| 5.1.2 产品链内容管理 | `1.1.1.1.4.2.5.1` ② | E-34 产品全景 |
| 5.1.3 企业内容管理 | `1.1.1.1.4.2.5.1` ③ | 运营档案叠加；**不得取代** ODS 工商 |
| 5.1.5 人才内容管理 | `1.1.1.1.4.2.5.1` ⑤ | E-34 团队画像 |
| 5.1.6 政策内容管理 | `1.1.1.1.4.2.5.1` ⑥ | 本三页弱引用 |
| 5.1.7 产业服务机构 | `1.1.1.1.4.2.5.1` ⑦ | E-34 生态服务型伙伴叙述 |
| 5.2.2 产业链专家知识 | `1.1.1.1.4.2.5.2` ② | E-33 链结构/瓶颈文案；E-35 区域知识 |
| 5.2.3 企业专家知识 | `1.1.1.1.4.2.5.2` ③ | E-34 历程/口碑；**招引/培育不进本三页** |
| 5.6.1 产业全景门户内容 | `1.1.1.1.4.2.5.6` ① | E-33/E-35 链全景结构展示 |
| 5.6.3 企业发展门户内容 | `1.1.1.1.4.2.5.6` ③ | **E-33/E-34/E-35 CMS 主出口** |
| 门户叶子 | `1.1.1.1.1.1.1.2~4` | 重点全景 / 明星介绍 / 深圳介绍 |

---

## 1. 公共信封（所有 CMS 资源）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `content_id` | string | ✅ | 久新内容实例 ID（仅引用） |
| `content_type` | enum | ✅ | 见 §2 |
| `enterprise_code` | string | 条件 | 企业绑定资源必填；与应用侧主数据对齐 |
| `future_industry_code` | string | 条件 | 产业绑定资源必填；须引用应用侧已发布目录码 |
| `version` | string | ✅ | 内容版本号（字符串，如 `3` / `2026.07.01`） |
| `publish_status` | enum | ✅ | `published` \| `draft` \| `archived`；门户只收 `published` |
| `publish_time` | datetime | ✅ | 发布时间（ISO-8601） |
| `sort_order` | int | ✅ | 同集合内升序；默认取最小 |
| `locale` | string | 可选 | 默认 `zh-CN` |
| `etag` / `updated_at` | string/datetime | 推荐 | 缓存与幂等 |

**幂等键**：`(content_type, content_id, version)`；列表资源另加 `(future_industry_code, enterprise_code, sort_order)` 业务唯一约束（由久新保证）。

**错误码（建议）**

| HTTP / code | 含义 | 应用侧处理 |
|-------------|------|------------|
| 200 + 空数组 | 无已发布内容 | 业务空态文案（§5） |
| 404 | 资源不存在 | 同空态；勿回退草稿 |
| 409 / stale | 版本冲突 | 重拉最新 published |
| 429 / 5xx / timeout | 不可用 | CMS 区骨架 + 重试；ADS 区不受影响 |

---

## 2. content_type 目录

| content_type | 页面 | 久新锚点 | 说明 |
|--------------|------|----------|------|
| `star_roster_item` | E-34 | 5.6.3 / 门户 31.3 | 产业内明星企业名单项 |
| `star_selection_standard` | E-34 | 5.6.3 + 专家知识 | 入选标准只读元数据（无权重） |
| `star_product_panorama` | E-34 | 5.1.2 + 5.6.3 | 产品全景及子内容 |
| `star_team_member` | E-34 | 5.1.5 + 5.6.3 | 团队成员画像 |
| `star_ecosystem_note` | E-34 | 5.6.3 / 5.1.7 | 合作伙伴**运营摘要文案**（正式边以 Q040 图谱/ADS 为准，CMS 不推断边） |
| `star_story` | E-34 | 5.2.3 / 5.6.3 | 发展历程时间线 + 口碑摘要 |
| `key_chain_structure` | E-33 | 5.6.1 / 5.2.2 | 链位结构（环节名/上下游叙事） |
| `key_enterprise_set` | E-33 | 5.6.3.2 | 重点企业运营集（名单+关系描述） |
| `key_chain_expert_note` | E-33 | 5.2.2 | 可选：瓶颈/结构专家解读文案 |
| `sz_enterprise_intro` | E-35 | 5.6.3.3 | 深圳企业定位/优势/专家分析 |
| `sz_focus_set` | E-35 | 5.6.3.3 | 深圳重点企业展示圈定（可选） |
| `display_name_alias` | 共用 | 5.1.3 | 可选展示别名（不得覆盖 ODS 法定名） |

---

## 3. 字段表（按 content_type）

### 3.1 `star_roster_item`（E-34 名单）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `enterprise_code` | string | ✅ | join ADS |
| `future_industry_code` | string | ✅ | 所属产业 |
| `selection_tag` | string | ✅ | 一句入选标签（选择器用） |
| `selection_reason` | string | ✅ | 入选理由正文 |
| `list_published` | bool | ✅ | 名单条目发布门闩（须 true） |
| `basic_intro_published` | bool | ✅ | 基础介绍发布门闩（须 true） |
| `standard_ref` | string | 可选 | 指向 `star_selection_standard.content_id` |
| `display_alias` | string | 可选 | 展示别名；UI 须标明非法定名 |

**前台准入**：`publish_status=published` ∧ `list_published` ∧ `basic_intro_published`。

### 3.2 `star_selection_standard`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `standard_name` | string | ✅ | |
| `standard_version` | string | ✅ | |
| `applicable_industry_codes` | string[] | ✅ | |
| `candidate_scope_text` | string | 可选 | 候选范围说明（非算法阈值） |
| `confirmed_dimensions` | string[] | 可选 | 已确认维度名称列表 |
| `updated_at` | datetime | ✅ | |

**禁止下发**：权重、内部阈值、排名公式、未脱敏原始证据。

### 3.3 `star_product_panorama`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `product_id` | string | ✅ | CMS 侧产品 ID（内容键，非 ADS PK） |
| `product_name` | string | ✅ | |
| `product_summary` | string | ✅ | |
| `impact_summary` | string | 可选 | |
| `modules[]` | object | 可选 | `{product_module_id, module_name, module_summary}` |
| `scenario_refs[]` | string | 可选 | |
| `case_refs[]` | string | 可选 | |
| `media_refs[]` | object | 可选 | `{media_type, url, cover_url, auth_status}` |

### 3.4 `star_team_member`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `team_member_id` | string | ✅ | |
| `name` | string | ✅ | |
| `title` | string | ✅ | 职务/领域 |
| `profile_summary` | string | 可选 | |
| `professional_domains[]` | string | 可选 | |
| `industry_achievements[]` | string | 可选 | |
| `leading_projects[]` | string | 可选 | |
| `avatar_url` | string | 可选 | |
| `portrait_authorization_status` | enum | ✅ | `authorized` \| `pending` \| `unavailable` |
| `external_profile_url` | string | 可选 | |
| `external_link_authorization_status` | enum | ✅ | 同上 |

**展示门闩**：照片/外链仅当 `publish_status=published` 且对应授权 = `authorized`。

### 3.5 `star_ecosystem_note` / `star_story`

| 类型 | 关键字段 |
|------|----------|
| ecosystem | `partner_name`, `relation_summary`, 可选 `related_enterprise_code` |
| story | `timeline[]{year,title,summary}`, `reputation[]` |

### 3.6 `key_chain_structure` / `key_enterprise_set`（E-33）

| 字段 | 说明 |
|------|------|
| `chain_code` / `future_industry_code` | 链/产业绑定 |
| `stages[]` | `{stage_code, stage_name, upstream_of[], narrative}` |
| `key_set_items[]` | `{enterprise_code, stage_code, relation_text, sort_order}` |
| `structure_version` | 结构发布版本 |

> 企业事实属性（名称、区域、资质）**不**从本契约覆盖 ODS；仅运营集与叙述。

### 3.7 `sz_enterprise_intro` / `sz_focus_set`（E-35）

| 字段 | 说明 |
|------|------|
| `positioning` | 本地定位文案 |
| `advantage_summary` | 优势摘要 |
| `expert_analysis` | 专家竞争力分析（可空） |
| `focus_set_items[]` | 可选圈定 `{enterprise_code, sort_order}` |

---

## 4. Java 聚合建议形状（CMS 段）

```json
{
  "cms": {
    "content_id": "cms-star-ent-0001-v3",
    "version": "3",
    "publish_status": "published",
    "publish_time": "2026-07-14T10:00:00+08:00",
    "selection_tag": "车规芯片与 EDA 代表",
    "selection_reason": "...",
    "standard": { "standard_name": "...", "standard_version": "V1.0" },
    "product_panorama": [],
    "team_members": [],
    "ecosystem": [],
    "timeline": [],
    "reputation": []
  }
}
```

完整 envelope 见派单包 §5；`facts` 段见 `ADS-facts-contract-E31.md`。

---

## 5. 失败降级与空态文案（CMS）

| 场景 | 空态 / 降级文案（门户） | 行为 |
|------|------------------------|------|
| 产业无明星名单 | 「本产业明星企业待配置」 | 不跨产业补位、不算法 TopN |
| 入选标准未定稿 | 「入选标准待配置」 | 保留企业展示 |
| 无产品 | 「核心产品待完善」 | 不渲染产品卡 |
| 无团队 | 「核心团队资料待完善」 | 不虚构履历 |
| 生态不足 | 「生态关系待完善」 | 不生成虚假节点 |
| 照片/外链未授权 | 隐藏入口 | 中性占位图（无姓名首字肖像） |
| 媒体不可用 | 「资源暂时不可用，请重试」 | 保持区块高度 |
| E-33 CMS 档案未发布 | 「档案待维护」 | 统计与链位仍可展示（ADS） |
| E-35 介绍未发布 | 隐藏专家观点区 | 仅 ADS 公开档案 |
| CMS 超时/5xx | 区块骨架 + 「内容服务暂不可用」 | **不拖垮** ADS 统计区 |

---

## 6. 契约 Mock 夹具（无久新环境）

| 夹具 | 路径 / 约定 |
|------|-------------|
| 字段形状真源 | `demo-ui-topic/.../portalAggregates.ts` → `STAR_ENTERPRISE_EXTRA` / `STAR_FUTURE_INDUSTRIES` |
| Mock 批次 | `batch=mock_cms_e31_20260716`；UI 必挂 🧪 MockBadge |
| 发布态过滤 | Mock 须含 `draft` 负例，断言前台不可见 |
| 联调顺序 | 见派单包 §12（契约 Mock → ADS Mock → Java → UI 换源） |

---

## 7. 开放项

| ID | 说明 | 状态 |
|----|------|------|
| Q041 | 团队字段/照片/外链授权与 CMS 发布口径 | 🟡 |
| Q048 | 名单发布准入与 `sort_order`（CMS 侧） | 🟡 |
| Q049 | 深圳 CMS 介绍接口 | 🟡 |
| Q050 | 久新发布 API 字段名/错误码与本契约对齐签字 | 🟡 新增 |
| Q040 | 生态图谱正式边数据（非 CMS 文案） | 🟡；CMS 仅叙述摘要 |
