# 政策相关 ODS → DWD 字段映射分析报告（v2）

> 生成时间: 2026-06-02 ｜ 版本: v2（ODS 数据源切换为三方「要素库」）
> 分析范围: **政策** 数据域

---

## 1. 背景与版本变更

本报告分析三方采购数据源（ODS 层）能否满足本项目自建 **DWD 政策标准表** `dwd.policy_base_info`（37 字段）的字段填充需求。

| 项 | v1 | v2（本报告） |
|----|----|----|
| ODS 来源 | `ods.poc_tb_policy_info`（17 字段，拼音命名） | 三方「要素库」`dwd_zck_policy`（国内政策 20 字段）+ `dwd_zck_intl_policy`（国际政策 16 字段） |
| 字段命名 | 拼音 | 规范英文+中文注释 |
| 深度分析字段（摘要/要素/要点/扶持要素/谱系） | ❌ 需自建 NLP 管线从正文抽取 | ✅ **数据供应方已结构化提供**（要素库预处理输出） |
| 关键词质量 | 仅 9.4% 非空 | 必填字段，质量显著提升 |

> 命名澄清：要素库 `dwd_zck_policy`/`dwd_zck_intl_policy` 是数据供应方命名，其业务定位为**三方数据源 = 本系统 ODS（贴源层）**；右侧 `dwd.policy_base_info` 才是本项目自建 DWD 标准明细层。

**映射状态图例**：✅直接映射 ｜ 🔧需计算/算法 ｜ ⚠️待确认 ｜ ❌无来源 ｜ 🟦系统/预留

## 2. 政策相关 ODS 源表概况

| ODS 表 | 中文名 | 字段数 | 主键 | 数据特征 |
|--------|--------|--------|------|----------|
| `dwd_zck_policy` | 国内政策信息 | 20 | id | **主源**。含标题/文号/发布机构/日期/层级/地区/摘要/关键词/正文/谱系/主旨要素/要点/扶持要素/附件，深度字段均已结构化 |
| `dwd_zck_intl_policy` | 国际政策信息 | 16 | id | **补充源**（国外政策/资讯）。含标题原文+译文、正文原文+译文、媒体名称/类型、年份/日期、区域、语种、内容分类 |

**`dwd_zck_policy` 全部字段（国内政策主源）**：

| # | 字段名 | 类型 | 说明 |
|---|--------|------|------|
| 1 | id | varchar | 唯一 id |
| 2 | title | varchar(1000) | 政策标题 |
| 3 | issued_number | varchar | 政策文号 |
| 4 | publish_department_name | varchar | 发布机构 |
| 5 | create_time | date | 成文日期 |
| 6 | publish_time | date | 发文日期（发布日期） |
| 7 | status | varchar(10) | 时效状态（已发布/已撤销） |
| 8 | publish_year | varchar(4) | 发布年 |
| 9 | policy_level | varchar(32) | 政策层级（国家级/省级/市级/区县级） |
| 10 | region | varchar | 政策地区 |
| 11 | abstract | text | 摘要 |
| 12 | keywords | varchar(1000) | 关键词 |
| 13 | content | text | 正文内容 |
| 14 | url | varchar(1000) | 原文链接 |
| 15 | pedigree | text | 政策谱系/引用政策 |
| 16 | elements | text | 政策主旨要素 |
| 17 | keypoints | text | 政策要点 |
| 18 | allfactors | text | 政策扶持要素 |
| 19 | platform | varchar | 数据来源 |
| 20 | attachment | text | 附件 |

## 3. 映射覆盖率总览

| DWD 表 | 总字段 | ✅直接 | 🔧需计算 | ⚠️待确认 | ❌无来源 | 🟦系统/预留 | 覆盖率* |
|--------|--------|--------|---------|---------|---------|------------|--------|
| policy_base_info | 37 | 19 | 4 | 4 | 0 | 10 | 85.2% |

> *覆盖率 = (✅直接 + 🔧需计算) / (总字段 − 系统/预留) = 23 / 27 = 85.2%。
> 相比 v1（覆盖率 77.8%、直接映射率约 33%），v2 直接映射率提升至 **70.4%**，核心提升来自**深度分析字段（摘要/谱系/要素/要点/扶持要素/附件）由要素库直接提供**，无需自建 NLP 管线。

## 4. dwd.policy_base_info 逐字段映射详情

**ODS 主源**: `dwd_zck_policy`（国内政策）｜ **补充源**: `dwd_zck_intl_policy`（国际政策）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增主键 |
| 2 | tenant_id | bigint | 🟦系统 | - | 多租户标识，系统配置 |
| 3 | policy_id | varchar(64) | ✅直接 | `dwd_zck_policy.id` | 政策唯一标识 |
| 4 | title | varchar(500) | ✅直接 | `dwd_zck_policy.title` | 政策标题（源 1000，需注意截断） |
| 5 | issued_number | varchar(200) | ✅直接 | `dwd_zck_policy.issued_number` | **v2 质量提升**（v1 仅 53.4% 非空） |
| 6 | publish_organization | varchar(300) | ✅直接 | `dwd_zck_policy.publish_department_name` | 发布机构 |
| 7 | publish_date | date | ✅直接 | `dwd_zck_policy.publish_time` | 发文日期 |
| 8 | implementation_date | date | ⚠️待确认 | `dwd_zck_policy.create_time`(成文日期，近似) | 无独立实施日期，可用成文日期近似或从正文提取 |
| 9 | expire_date | date | ⚠️待确认 | - | 无失效日期字段（`status` 有"已撤销"但无日期） |
| 10 | status | smallint | ✅直接 | `dwd_zck_policy.status`(已发布/已撤销) | **v2 直接枚举映射**（已发布→1有效，已撤销→2失效；v1 需计算推断） |
| 11 | publish_year | integer | ✅直接 | `dwd_zck_policy.publish_year` | 发布年份 |
| 12 | level | smallint | ✅直接 | `dwd_zck_policy.policy_level` | 枚举映射（国家级→1/省级→2/市级→3/区县级→4） |
| 13 | region | varchar(200) | ✅直接 | `dwd_zck_policy.region` | 政策地区 |
| 14 | abstract | text | ✅直接 | `dwd_zck_policy.abstract` | **v2 直接可得**（v1 需大模型摘要生成） |
| 15 | keywords | varchar(1000) | ✅直接 | `dwd_zck_policy.keywords` | **v2 直接可得且质量高**（v1 仅 9.4% 非空、需 NLP 重抽） |
| 16 | content | text | ✅直接 | `dwd_zck_policy.content` | 政策正文 |
| 17 | url | varchar(1000) | ✅直接 | `dwd_zck_policy.url` | 原文链接 |
| 18 | pedigree | text | ✅直接 | `dwd_zck_policy.pedigree` | **v2 直接可得**（政策谱系/引用政策，v1 需 NLP 提取） |
| 19 | elements | text | ✅直接 | `dwd_zck_policy.elements` | **v2 直接可得**（政策主旨要素，v1 需 NLP） |
| 20 | keypoints | text | ✅直接 | `dwd_zck_policy.keypoints` | **v2 直接可得**（政策要点，v1 需 NLP） |
| 21 | factors | text | ✅直接 | `dwd_zck_policy.allfactors` | **v2 直接可得**（政策扶持要素，v1 需 NLP） |
| 22 | source | varchar(200) | ✅直接 | `dwd_zck_policy.platform` | 数据来源 |
| 23 | gis_location | varchar(100) | 🔧需计算 | `dwd_zck_policy.region` → 地理编码 | 地区名→经纬度（地理编码 API） |
| 24 | attachment | text | ✅直接 | `dwd_zck_policy.attachment` | **v2 直接可得**（附件，v1 待确认） |
| 25 | sci_tech_attribute | smallint | 🔧需计算 | `dwd_zck_policy.keywords/elements/content` | 关键词+要素规则/轻量分类判断科创属性 |
| 26 | application_conditions | text | 🔧需计算 | `dwd_zck_policy.elements/allfactors/content` | 从已结构化的要素/扶持要素中提取申报条件 |
| 27 | execution_cycle | varchar(200) | ⚠️待确认 | `dwd_zck_policy.elements/content`(待提取) | 无独立字段，需从要素或正文提取 |
| 28 | execution_entity | varchar(300) | ⚠️待确认 | `dwd_zck_policy.publish_department_name`(近似) / 正文提取 | 可能=发布机构，或从正文提取执行主体 |
| 29 | related_entities | text | 🔧需计算 | `dwd_zck_policy.elements/keypoints` | 从已结构化要素中抽取关联产业/企业/人才/机构实体→JSON |
| 30 | create_time | timestamp | 🟦系统 | - | ETL 写入时间 |
| 31 | update_time | timestamp | 🟦系统 | - | ETL 更新时间 |
| 32 | is_deleted | smallint | 🟦系统 | - | 默认 0（逻辑删除标记） |
| 33 | ext1 | varchar(500) | 🟦预留 | - | 扩展字段 |
| 34 | ext2 | varchar(500) | 🟦预留 | - | 扩展字段 |
| 35 | ext3 | varchar(500) | 🟦预留 | - | 扩展字段 |
| 36 | ext4 | varchar(500) | 🟦预留 | - | 扩展字段 |
| 37 | ext5 | varchar(500) | 🟦预留 | - | 扩展字段 |

## 5. 国际政策（`dwd_zck_intl_policy`）映射补充

国际政策表结构与国内政策差异较大（偏媒体资讯+双语），映射到 `dwd.policy_base_info` 时部分字段对应、部分需特殊处理：

| DWD字段 | ODS来源（国际政策） | 映射状态 | 说明 |
|---------|---------------------|----------|------|
| policy_id | `dwd_zck_intl_policy.id` | ✅直接 | 唯一 id |
| title | `translate_title`（标题译文）优先，`title`（原文）备 | ✅直接 | 中文展示用译文 |
| abstract | `abstract`（摘要原文） | 🔧需翻译 | 需译文，或保留原文 |
| content | `translate_content`（正文译文）优先 | ✅直接 | 中文展示用译文 |
| publish_date | `release_date` | ✅直接 | 发布日期 |
| publish_year | `release_year` | ✅直接 | 年份 |
| region | `media_area`（所属区域） | ✅直接 | 区域 |
| url | `url_link` | ✅直接 | 链接 |
| source | `source` / `media_product_name` | ✅直接 | 数据来源/媒体名称 |
| level | - | ❌无对应 | 国际政策无国内行政层级概念，建议固定为"境外/国际" |
| issued_number / publish_organization | - | ❌无对应 | 国际媒体资讯无文号/发布机构口径 |
| keywords / elements / keypoints / factors / pedigree | - | ❌无对应 | 国际政策表未提供结构化深度字段 |
| 其他（class/class_no/language/media_type） | `class`、`class_no`、`language`、`media_type` | 🟦扩展 | 可存入 ext1~ext5 或单独的国际政策扩展表 |

> 建议：国际政策与国内政策**语义口径差异较大**，可在 `dwd.policy_base_info` 中以 `level`='国际'/`source` 区分；或单独建国际政策扩展表承接双语、媒体类型等专有字段，避免污染国内政策主表。

## 6. v1 → v2 关键改善对照

| DWD 字段 | v1 状态 | v2 状态 | 改善原因 |
|----------|---------|---------|----------|
| abstract | 🔧 大模型摘要生成 | ✅ 直接 | 要素库已提供 `abstract` |
| keywords | ⚠️ 质量差(9.4%)、需 NLP | ✅ 直接(必填) | 要素库 `keywords` 必填、质量提升 |
| pedigree | 🔧 NLP 提取引用政策 | ✅ 直接 | 要素库已提供 `pedigree` |
| elements | 🔧 NLP 抽取主旨要素 | ✅ 直接 | 要素库已提供 `elements` |
| keypoints | 🔧 NLP 抽取要点 | ✅ 直接 | 要素库已提供 `keypoints` |
| factors | 🔧 NLP 抽取扶持要素 | ✅ 直接 | 要素库已提供 `allfactors` |
| attachment | ⚠️ 待确认 | ✅ 直接 | 要素库已提供 `attachment` |
| status | 🔧 需计算推断 | ✅ 直接枚举 | 要素库 `status`（已发布/已撤销） |
| issued_number | ⚠️ 53.4% 非空 | ✅ 直接(必填) | 要素库 `issued_number` 必填 |

## 7. 数据缺口与风险

### 7.1 待确认/无直接来源字段

| DWD 字段 | 问题 | 处理建议 |
|----------|------|----------|
| implementation_date | 无独立实施日期字段 | 用 `create_time`（成文日期）近似，或从正文/要素提取生效日期 |
| expire_date | 无失效日期字段 | `status`='已撤销'仅表状态无日期；需从正文/谱系推断或采购 |
| execution_cycle | 无独立执行周期字段 | 从 `elements`/`allfactors`/正文提取（如"2024-01-01 至 2026-12-31"） |
| execution_entity | 无独立执行主体字段 | 默认取发布机构，或从正文提取 |

### 7.2 需轻量加工的字段

| DWD 字段 | 加工类型 | 说明 |
|----------|---------|------|
| gis_location | 地理编码 | `region` → 经纬度，调地图 API |
| sci_tech_attribute | 规则/分类 | 基于 `keywords`+`elements` 判断科创属性 |
| application_conditions | 结构化抽取 | 从已结构化 `elements`/`allfactors` 二次提取申报条件 |
| related_entities | 实体抽取 | 从 `elements`/`keypoints` 提取关联实体→JSON |

> 注：v2 中这些加工字段的**输入已是结构化要素**（而非 v1 的原始正文），加工难度由"全文 NLP"降为"结构化字段二次解析"，复杂度显著下降。

### 7.3 风险提示

| 风险项 | 描述 | 缓解措施 |
|--------|------|----------|
| 深度字段格式 | `elements`/`keypoints`/`factors`/`pedigree` 为 text，需确认是否为 JSON 及其 schema | 与供方确认结构化格式，制定解析规范 |
| 国内/国际口径差异 | 国际政策为媒体资讯，无层级/文号/结构化要素 | 用 `level`/`source` 区分或单建扩展表 |
| 失效/实施日期缺失 | 影响政策时效计算 | 正文提取或采购补充 |
| 标题超长 | 源 `title` varchar(1000)，DWD varchar(500) | ETL 截断或扩容 DWD 字段 |

## 8. ETL 实施建议

```
Phase 1（直接映射加载，<1周）
└── policy_base_info 直接字段：id/title/文号/机构/日期/层级/地区/
    摘要/关键词/正文/链接/谱系/要素/要点/扶持要素/附件/来源  约 19 字段

Phase 2（轻量加工，1周）
├── status/level 枚举映射
├── gis_location 地理编码
├── sci_tech_attribute 科创属性规则判定
├── application_conditions / related_entities 结构化要素二次解析
└── implementation/expire/execution 从要素或正文提取

Phase 3（国际政策接入）
└── dwd_zck_intl_policy 双语/媒体字段映射或扩展表
```

**示例 ETL（国内政策主源加载）**：

```sql
INSERT INTO dwd.policy_base_info (
  tenant_id, policy_id, title, issued_number, publish_organization,
  publish_date, publish_year, status, level, region,
  abstract, keywords, content, url, pedigree, elements, keypoints, factors,
  source, attachment
)
SELECT
  1,
  p.id,
  LEFT(p.title, 500),
  p.issued_number,
  p.publish_department_name,
  p.publish_time,
  CAST(p.publish_year AS integer),
  CASE p.status WHEN '已发布' THEN 1 WHEN '已撤销' THEN 2 ELSE 1 END,
  CASE p.policy_level
       WHEN '国家级' THEN 1 WHEN '省级' THEN 2
       WHEN '市级' THEN 3 WHEN '区县级' THEN 4 ELSE 0 END,
  p.region,
  p.abstract,
  p.keywords,
  p.content,
  p.url,
  p.pedigree,
  p.elements,
  p.keypoints,
  p.allfactors,
  p.platform,
  p.attachment
FROM ods.dwd_zck_policy p;
```

## 9. 综合结论

| 评估维度 | v1 满足度 | v2 满足度 | 说明 |
|----------|-----------|-----------|------|
| 政策基础信息（标题/机构/日期/层级/地区） | 80% | 100% | 字段齐全、文号/关键词质量提升 |
| 政策正文/链接/来源 | 100% | 100% | 直接可得 |
| 政策深度分析（摘要/谱系/要素/要点/扶持要素） | 20%（需 NLP） | 95%（直接） | **最大改善点**：供方已结构化提供 |
| 政策附件 | 待确认 | 100% | 直接可得 |
| 政策时效（实施/失效日期） | 20% | 40% | 仍缺独立日期，需提取/采购 |
| 政策衍生字段（科创属性/申报条件/关联实体/GIS） | 20% | 70% | 输入已结构化，加工难度下降 |
| 国际政策 | 80% | 75% | 双语媒体资讯，部分口径无对应 |

**关键结论**：

1. **政策深度字段由"需自建 NLP"转为"直接映射"**：摘要、谱系、主旨要素、要点、扶持要素、附件均由要素库直接提供，这是 v2 相对 v1 最显著的改善，大幅降低政策数据治理成本。
2. **覆盖率提升**：`policy_base_info` 直接映射率由约 33% 提升至 **70.4%**，整体覆盖率 85.2%。
3. **剩余工作集中在轻量加工**：GIS 编码、科创属性判定、申报条件/关联实体解析，且输入已是结构化要素，难度较 v1 显著降低。
4. **主要缺口**：政策实施/失效日期无独立字段，影响时效计算，需从正文提取或补充采购。
5. **国际政策需独立处理**：与国内政策口径差异大，建议以 `level`/`source` 区分或单建扩展表。

---

*报告生成时间: 2026-06-02 ｜ ODS 数据源: db/要素库建表语句.sql（政策相关 2 张表）｜ DWD 目标: dwd.policy_base_info（37 字段）*
