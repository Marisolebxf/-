# 门户企业发展四页签 · 读接口需求（需规 75–78 + 2026-10-26 产品确认）

| 项 | 内容 |
|----|------|
| **真源** | `bid-reference/srs/01-智慧服务门户系统/集群服务/科技专题服务.md` 序号 75–78 |
| **契约索引** | `agent-handoffs/企业战略分析-ENT/API-ENT-full-catalog.md`（#58–#76） |
| **前端任务** | `SYSINT-04-04-L01` 门户企业发展展示页 |
| **后端任务** | `PORTAL-ENT-DEV-SRS-API-L01`（监管 `human:徐腾强`） |
| **约束** | `industry_coverage_count` **不补**；`patent_valid` / `rd_ratio` **禁止**前端走 `#1` 检索拼装，须在明星/门户相关接口返回 |

---

## 0. 地图分布 `map_data` 与坐标

**结论：`map_data[]` 应提供 `lat` / `lng`（WGS84 或与地图底图一致的坐标系）；前端仅在字段缺失或为空时兜底。**

| 优先级 | 来源 |
|--------|------|
| 1 | `map_data[].lat`、`map_data[].lng`（后端按区划质心或业务聚合中心计算，**推荐主路径**） |
| 2 | `region_id` / `region_name` + 前端字典 `regionCenter()`（`portalFormat.ts` 的 `REGION_CENTER`，**仅兜底**） |

每行仍需：

- `region_id`、`region_name`
- `enterprise_count`
- （可选）`research_staff_count` — 列表若保留「科研人员数」；**不返回 `industry_coverage_count`**

接口与字典均无法落点时：地图不画点，列表仍可展示。

热力层与圆点共用同一套解析后的 `[lat, lng]`。

**接口仍需补：** 入参 **`chain_code`（或等价产业维度）**；`region_level` / 全球·全国·深圳等与现 `#65` 一致。契约需在 catalog / DTO 中显式增加 `map_data[].lat`、`map_data[].lng`（`BigDecimal` 或 `Double`，可空）。

---

## 1. 企业整体概况（需规 75）— #62–#65

| # | 现状问题 | 需求 |
|---|----------|------|
| **#62** | 实包常为零；科研口径前端「不动」 | 保持字段；**产业内** `enterprise_total` / `research_staff_total` 由后端按门户产业筛选语义聚合（与级联 `chain_code` 或文档约定一致）。**不新增** `industry_coverage` 展示依赖。 |
| **#63** | 产业对比 | `items[]`：`chain_code`、`chain_name`、`enterprise_count`；供排名与选中产业汇总。 |
| **#64** | 需按产业多年趋势 | 入参 **`chain_code`（可多次请求或支持多 code）**；`items[]`：`year`、`enterprise_count`（或 `cumulative_count`，与前端约定其一）。**不限制**前端最多选 2 个产业。 |
| **#65** | 无产业入参、`map_data` 常空 | 入参增加 **`chain_code`**（及现有 `region_level` 等）；`map_data[]`：`region_id`、`region_name`、**`lat`、`lng`**、`enterprise_count`、可选 `research_staff_count`；**不传** `industry_coverage_count`。 |

**Java：** `ENT-JAVA-OVERVIEW-STATS` 门面透传 + DTO 扩展。  
**Python/ADS：** 聚合灌数（`INB17xx` 等与 `#138 meta/chains` 一致）。

---

## 2. 重点企业全景图（需规 76）— #66–#70

| 能力 | 接口 | 需求 |
|------|------|------|
| 全景 | **#67** + **#68** | `#68` 产业列表；`#67` 按 `chain_code` 返回 `groups[]` + **`enterprises[]` 灌数**（基础信息字段与 catalog 一致即可）。 |
| **规模统计（需规 76②）** | **扩展 #69 或新只读端点** | 维度：**资质四类** — `foreign`（外企）、`high_tech`（高企）、`sme`（小微）、`listed`（上市） × **三级地域** `national` / `province` / `city`（市=深圳）。返回结构建议：`items[]: { qualification, levels: { national, province, city } }` 各 `enterprise_count`。**不再**用 **#70** 作为本模块主数据（#70 类型×规模可保留给其他场景）。 |
| **领域统计（需规 76③）** | **#67** 扩展 | `domain_evidence[]`：`domain`、`stage`（链位/环节）、`paper_keywords[]`、`patent_keywords[]`、`summary`、关联 `enterprise_count` 或企业 id 列表。关键词需可映射产业链节点。 |
| **#66 KPI** | 可选 | 页顶仅保留工具条「重点企业 N 家」类文案时，**#66** 仅需 `key_enterprise_total`；**不要求** `covered_chain_nodes` / `covered_districts` 页顶 KPI（前端将去掉明星页顶类似项；重点页无独立三 KPI 条）。 |

---

## 3. 明星企业介绍（需规 77）— #71–#72 + CMS

| 项 | 需求 |
|----|------|
| **#71** | 前端去掉页顶 KPI；**可不调用**或保留供评审层，无产品展示硬性依赖。 |
| **#72 名单** | 按产业/区域筛选；`items[]` 至少 catalog 字段 + 用于列表展示的 `industry_chain_names`。 |
| **明星详情包** | 不宜仅靠 `#72` 扁平字段；需 **门户读聚合**（Java 编排 CMS 已发布 + ADS）：`star_profile` 或等价 JSON，含四块：产品列表（**`products[]` 含后期 CMS 视频 URL 字段**）、技术（**`patent_count`、`rd_ratio`**，对齐 Q048 等，**禁止**前端调 `#1`）、团队、产业生态。 |
| **发展历程** | **单独 API**（CMS 维护），本阶段前端可空态；任务可跟 `SYSINT-03-01A-JAVA-L01` / `PORTAL-CMS-FIELD-API-L01`。 |
| **公开口碑** | 前端移除；接口不补。 |
| **入选标准** | 前端保留静态/配置文案；非本单阻塞。 |

---

## 4. 深圳企业介绍（需规 78）— #73–#76

| # | 需求 |
|---|------|
| **#73** | `enterprise_total`、`key_enterprise_total`；**不要求** `listed_*`、`state_owned_*`（前端去掉对应 KPI）。 |
| **#74** | 入参 **`chain_code`**，返回该产业深圳企业 **历年数量**（`year` + `count` / `cumulative_count`）。 |
| **#75** | 扩展为链式 **领域/环节** 分布（非仅 L0 产业名计数）：`items[]` 含 `chain_code`、`chain_name`、`domain_or_stage`、`enterprise_count` 等；与产业链全景语义一致。 |
| **#75 或专用** | **分产业规模**：`[{ chain_code, scales: [{ enterprise_scale, enterprise_count }] }]`（大/中/小/微）。 |
| **#76** | 按产业过滤；`industry_chain_names` 填全；卡片字段 `positioning`、`expert_view` 等按需规「重点企业情况」由 CMS/运营字段回写。**列表不分页**（前端一次展示当前 Tab 下全部或合理上限由接口 `page_size` 放大，产品确认去掉分页 UI）。 |

---

## 5. 与存量 Java 任务关系

| 任务 ID | 关系 |
|---------|------|
| `ENT-JAVA-OVERVIEW-STATS` | #62–#65 扩展与灌数，本需求 §1 |
| `ENT-JAVA-KEY-STAR-SZ` | #66–#76 扩展与灌数，本需求 §2–§4 |
| `PORTAL-CMS-FIELD-API-L01` | 明星 CMS 字段、发展历程读接口 |
| `SYSINT-03-01A-JAVA-L01` | 企业发展运营正文写/读 |

**本单 `PORTAL-ENT-DEV-SRS-API-L01`**：在联调态存量门面之上，按上表完成 **契约变更说明 + Java 透传 + 搜索/ADS 实现或灌数**，并与 `SYSINT-04-04-L01` 联调验收。

---

## 6. 验收要点（后端）

1. `USE_MOCK=false` 环境下，门户四 Tab 核心区块在至少 1 个 `chain_code`（如 `INB1701`）下有非空可读数据。  
2. #65 无 `industry_coverage_count`；#64 支持多产业趋势请求。  
3. 重点页规模图为 **资质×国省市**；领域块有 **domain_evidence** 与关键词。  
4. 明星技术指标准出在 **#72 聚合或专用详情接口**，非 `#1`。  
5. 深圳趋势可随产业切换；无上市/国有 KPI 字段依赖。

---

## 7. 前端范围（记入 `SYSINT-04-04-L01`，不重复开单）

- E-32：去掉「覆盖产业」KPI 与分布列表「覆盖未来产业数」列；趋势取消最多 2 产业限制；Mock 可补全字段，**`USE_MOCK=false` 禁止伪造**。  
- E-33：规模/领域模块换需规口径 UI；Mock 补 `domain_evidence`、资质矩阵。  
- E-34：去掉页顶 #71 KPI、去掉「公开口碑」；保留入选标准；发展历程等 CMS API 未就绪时空态。  
- E-35：去掉上市/国有 KPI、重点企业分页。
