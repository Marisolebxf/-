# ADS-facts-contract-E31

> **任务**：`DATA-ENT-CMS-VS-APP-PARTITION-L01`  
> **性质**：E-33/E-34/E-35 **应用侧事实与指标契约**（ODS→DWD→ADS；算法写 ADS）  
> **状态**：data-agent 冻结草案（Wave0 Mock 先行；正式口径随 Q047/Q048/Q049 升 🟢）  
> **日期**：2026-07-16  
> **作者**：`[agent:data-agent]` · 监管 `human:淮政玮`

---

## 0. 分层与命名提醒

| 层 | 本项目约定 | 说明 |
|----|------------|------|
| ODS | 要素库表名常以 `dwd_` 开头 | **贴源层**，非本项目自建 DWD |
| DWD | 本项目 `dwd.*` | 清洗后标准明细 |
| ADS | 本项目 `ads.*` / 聚合视图 | Java 只读；前端不直连 |

**身份键**：`enterprise_code`（业务）↔ 映射 `credit_code` / ODS `org_id`；**禁止** CMS `content_id` 作 ADS PK。

**批次**：`calc_batch_id` / `data_batch_id`；Wave0 前缀 `mock_`；UI 必挂 🧪 + MetricSpecCard ⓘ。

---

## 1. 实体键与字典

| 键 / 字典 | 归属 | 说明 |
|-----------|------|------|
| `enterprise_code` | APP | 稳定业务主键 |
| `credit_code` | ODS→DWD | 统一社会信用代码（映射） |
| `future_industry_code` | **APP 字典** | E-32/E-34/E-35 **同源**；CMS 只引用，不得私自增删正式目录 |
| `chain_code` / `stage_code` | APP（可对齐 CMS 结构版本） | 挂链统计用；结构叙事见 CMS |
| `tag_code` | APP 通用枚举 | 外企/国高企/小微/上市/专精特新/小巨人/链主龙头/独角兽/瞪羚 |

---

## 2. 推荐 ADS / DWD 目标表（逻辑名）

| 逻辑表 | 用途 | 页面 |
|--------|------|------|
| `dwd.enterprise_base` | 名称、区域、规模、性质 | 三页 |
| `dwd.enterprise_tag` | 资质荣誉多标签 | 三页 |
| `dwd.enterprise_chain_link` | 企业↔产业链环节 | E-33/E-35 |
| `ads.ent_key_qual_scale` | 整链资质 × 国/省/市 | E-33 |
| `ads.ent_key_domain_stat` | 链领域企业数 | E-33 |
| `ads.ent_key_domain_evidence` | 论文/专利关键词→链领域证据 | E-33 |
| `ads.ent_star_tech_metrics` | 明星企业技术量化指标 | E-34 |
| `ads.ent_sz_industry_summary` | 深圳 × 未来产业数量 | E-35 |
| `ads.ent_sz_industry_trend` | 深圳产业历年趋势 | E-35 |
| `ads.ent_sz_scale_struct` | 深圳规模结构 | E-35 |
| `ads.ent_sz_domain_dist` | 深圳领域/环节分布计数 | E-35 |
| `cfg_metric` / `cfg_metric_lineage` | 8 件套 + 血缘 | 凡统计数字 |

> 物理表名可在后续 DDL 任务微调；**契约面字段与 metric_id 冻结**。

---

## 3. 指标与血缘（按页面）

### 3.1 E-33 重点企业概览（Q047）

| UI 字段 / 指标 | metric_id（建议） | 公式 / 口径（临时默认） | 源 ODS（候选） | 目标 DWD/ADS | 更新频率 | 状态 |
|----------------|-------------------|-------------------------|----------------|--------------|----------|------|
| 整链资质规模：外企/国高企/小微/上市 × 市/省/国 | `M_ENT_KEY_QUAL_SCALE`（新建种子） | 对重点集 ∩ 挂链企业，按标签多选 **重复计数**；地域：市=深圳明细、省/国=聚合（闭合前省/国可 DEMO 放大） | `dwd_org_tag_info`, `dwd_org_reg_info`, `dwd_org_industry_chain_dtl` | `dwd.enterprise_tag` → `ads.ent_key_qual_scale` | 日批 | 🟡 Q047 / DEMO |
| 领域统计（上中下游企业数） | `M_ENT_KEY_DOMAIN_COUNT`（新建） | `COUNT(DISTINCT enterprise_code) GROUP BY stage` | `dwd_org_industry_chain_dtl` | `ads.ent_key_domain_stat` | 日批 | 🟡 Q047 / DEMO |
| 论文/专利关键词→链领域证据 | `M_ENT_KEY_DOMAIN_EVIDENCE`（新建） | 算法抽取关键词映射链领域；覆盖率分子分母待定 | 论文库 + 专利库（ODS 专利/论文域）+ 挂链表 | Python → `ads.ent_key_domain_evidence` | 周批 | 🟡 Q047；🔧 算法 |
| 企业基础信息（名称/区域） | （实体非 KPI） | 主数据展示 | `dwd_org_reg_info` | `dwd.enterprise_base` | 日批 | ✅ 有源 |
| 资质荣誉标签 | 复用通用标签服务 | 多标签展示；「高企」→「国高企」 | `dwd_org_tag_info` | `dwd.enterprise_tag` | 日批 | ✅ 有源；与 CMS 重点标识隔离 |
| 挂链企业集合 / 重点候选 | 关联 Q038 | APP 侧候选（如专利数阈值）；**正式重点集** = CMS `key_enterprise_set` ∩ APP 挂链 | 专利 `dwd_org_*` / 专利库 + 挂链 | `dwd.enterprise_chain_link` | 日批 | 🟡 Q038 |

**禁止**：将上述统计手填进 CMS 当正式指标。

### 3.2 E-34 明星企业介绍（Q048 / Q041）

| UI 字段 / 指标 | metric_id | 公式 / 口径（临时默认） | 源 ODS（候选） | 目标 DWD/ADS | 更新频率 | 状态 |
|----------------|-----------|-------------------------|----------------|--------------|----------|------|
| 「共 N 家明星企业」 | `M_ENT_STAR_ROSTER_COUNT`（新建） | `COUNT(*)` **对 CMS 已发布名单契约**（非 ODS TopN） | —（契约输入） | Java/ADS 轻量聚合表可选 `ads.ent_star_roster_count` | 近实时/随 CMS 拉取 | ✅ APP 聚合 CMS |
| 专利数 | `M_ENT_STAR_PATENT_COUNT`（demo metricSeed 已用） | 企业有效专利件数；范围待 Q048 | 专利 ODS（全球专利要素库） | `ads.ent_star_tech_metrics.patent_count` | 日批 | 🟡 Q048 / DEMO |
| 研发投入占比 | `M_ENT_STAR_RD_RATIO` / 可对齐 `M_ENT_RD_INVESTMENT_RATIO` | 研发投入/营收×100；无源则 DEMO | `dwd_org_annual_financial_info` / 上市财务 | `ads.ent_star_tech_metrics.rd_ratio` | 年/季 | 🟡 Q048；可能 ❌ 缺口 |
| 科学家/人才占比 | `M_ENT_STAR_SCIENTIST_RATIO`（新建） | **PENDING**：口径未定（职称？学历？）；APP 优先试算，禁止 CMS 手填冒充实算 | 人才/招聘相关 ODS 不足（`dwd_org_executive_info` 弱相关） | ADS 占位 | — | 🟡 Q048；❌→Mock 直至口径闭合 |
| 数据时间（统计） | — | 展示 `calc_batch_id` 业务日 | ETL | ADS 元数据 | 随批 | ✅ |
| 企业名称（法定） | — | ODS 主数据优先 | `dwd_org_reg_info` | `dwd.enterprise_base` | 日批 | ✅ |
| 资质荣誉 | — | 同通用枚举 | `dwd_org_tag_info` | `dwd.enterprise_tag` | 日批 | ✅ |
| 关联专利 ID 列表（证据） | — | 供技术优势「证据」跳转，非叙事 | 专利 ODS | DWD 关联表 | 日批 | ✅/🔧 |

**CMS 负责**（不进本表计算）：入选理由、标准正文、产品全景、团队、媒体、历程、口碑 — 见 `CMS-read-contract-E31.md`。

### 3.3 E-35 深圳企业介绍（Q049）

| UI 字段 / 指标 | metric_id | 公式 / 口径（临时默认） | 源 ODS（候选） | 目标 DWD/ADS | 更新频率 | 状态 |
|----------------|-----------|-------------------------|----------------|--------------|----------|------|
| 深圳企业总数 | `M_ENT_SZ_COUNT`（cfg 已有） | 注册地/总部 ∈ 深圳 | `dwd_org_reg_info` | ADS 汇总 | 日批 | 🟡 切片口径待确认 |
| 产业企业数量对比 | `M_ENT_SZ_INDUSTRY_COUNT`（新建） | 深圳 ∩ `future_industry_code` | 挂链/产业标签 + 主数据 | `ads.ent_sz_industry_summary` | 日批 | 🟡 Q049 / DEMO |
| 所选产业历年趋势 | `M_ENT_SZ_INDUSTRY_TREND`（新建） | 年快照计数；&lt;2 个连续可比点则隐藏 | 同上 + 历史快照 | `ads.ent_sz_industry_trend` | 年批/日批快照 | 🟡 Q049 |
| 领域分布计数 | `M_ENT_SZ_DOMAIN_DIST`（新建） | 当前产业下领域/环节 `COUNT`；「已识别 X 个」= 项数，**≠覆盖率** | `dwd_org_industry_chain_dtl` + 标签 | `ads.ent_sz_domain_dist` | 日批 | 🟡 Q049 |
| 规模结构 大/中/小/微 | `M_ENT_SZ_SCALE_DIST`（metricSeed 已用） | 分级口径待甲方；**禁止**用资质标签冒充规模 | `dwd_org_reg_info` / 经营信息 | `ads.ent_sz_scale_struct` | 日批 | 🟡 Q049 |
| KPI：上市数 | `M_ENT_SZ_LISTED_COUNT`（新建）或 `M_ENT_TYPE_COUNT`（type=上市） | 标签或上市表派生 | `dwd_org_stock_base`, `dwd_org_tag_info` | ADS | 日批 | 🟡 DEMO |
| KPI：国企数 | `M_ENT_SZ_SOE_COUNT` / UI 曾用 `M_ENT_STATE_OWNED_COUNT`（**须补种子**） | 登记类型/股权性质派生 | `dwd_org_reg_info`, `dwd_org_tag_info` | ADS | 日批 | 🟡 DEMO；cfg 未登记 |
| KPI：深圳重点企业数 | `M_ENT_SZ_KEY_COUNT`（新建；**禁止**复用 `M_ENT_TOTAL_COUNT`） | 深圳 ∩（CMS `sz_focus_set` 或 Q038 阈值） | 主数据 + 标签 + CMS 圈定 | ADS | 日批 | 🟡 Q038/Q049 |
| 深圳重点企业列表事实字段 | 关联 Q038 | 名称/区域/性质/资质 = APP；圈定名单可 CMS | 主数据+标签 | DWD | 日批 | HYBRID |

**目录**：`future_industry_code` 字典与 E-32/E-34 **必须同源**（APP 配置服务）；CMS 不得维护第二套正式八大。

---

## 4. Java `facts` 段建议形状

```json
{
  "enterprise_code": "ENT-0001",
  "future_industry_code": "integrated-circuit",
  "data_batch_id": "2026-07-14",
  "facts": {
    "name": "深芯微集成电路股份有限公司",
    "region": { "city": "深圳市", "district": "..." },
    "tags": ["上市", "专精特新"],
    "patent_count": 128,
    "rd_ratio": 18.6,
    "scientist_ratio": null,
    "metric_refs": [
      "M_ENT_STAR_PATENT_COUNT",
      "M_ENT_STAR_RD_RATIO"
    ]
  }
}
```

---

## 5. DEMO / Mock 义务

| 项 | 要求 |
|----|------|
| Wave0 | 全部统计可 Mock；`calc_batch_id` 前缀 `mock_` |
| UI | 每个数字 ⓘ MetricSpecCard + 🧪 MockBadge |
| 口径未定 | 挂 Q047/Q048/Q049；⚠️「待甲方确认」角标 |
| 禁止 | 验收材料宣称 ODS/久新已贯通 |

对照实现（只读）：`demo-ui-topic/src/app/mock/enterprise/portalAggregates.ts`、`metricSeed.ts`。

---

## 6. 与 cfg_metric 种子差距

| metric_id | cfg_metric-ENT-seed | demo metricSeed | 动作 |
|-----------|---------------------|-----------------|------|
| `M_ENT_SZ_COUNT` | ✅ | ✅ | 复用；补深圳切片说明 |
| `M_ENT_RD_INVESTMENT_RATIO` | ✅ | — | E-34 可对齐或保留 STAR 别名 |
| `M_ENT_STAR_*` | ❌ 未入种子 | 部分 ✅ | 后续 DATA 任务写入 cfg_metric 8 件套 |
| `M_ENT_KEY_*` / `M_ENT_SZ_INDUSTRY_*` | ❌ | 部分命名 | 同上，闭合 Q047/Q049 时登记 |

---

## 7. 联调顺序（应用侧）

1. **ADS Mock** 写入逻辑表（固定种子）→ MetricSpec 可展示  
2. Java 读 ADS Mock + CMS 契约 Mock 聚合  
3. UI 换源（去掉本地 `portalAggregates` 硬编码）  
4. 数据工厂映射真实 ODS → 去 `mock_` 批次  

详见派单包 §12。

---

## 8. ODS 候选表附录（UI/映射探索补充）

| 域 | ODS 表（贴源，`dwd_` 前缀属 ODS） |
|----|----------------------------------|
| 主数据 | `dwd_org_reg_info`, `dwd_company_base`, `dwd_org_org_product_info` |
| 标签/资质 | `dwd_org_tag_info`, `dwd_company_honor_tags`, `dwd_company_basic_tags`, `dwd_company_industry_tags` |
| 财务/研发 | `dwd_org_annual_financial_info`, `dwd_org_stock_finance_info`, `dwd_org_stock_base` |
| 挂链 | `dwd_org_industry_chain_dtl`, `dwd_industry_chain_info`, `dwd_org_industry_chain_pat_dtl` |
| 专利 | `dwd_patent*`, `dwd_org_rd_achiev_info` |
| 论文 | `dwd_zh_paper*`, `dwd_en_paper*` |
| 高管（团队弱相关，非 CMS 画像替代） | `dwd_org_executive_info` |

> `developmentData.ts` 属 **E-32**，与 E-33/34/35 无直接 import；产业目录以 `STAR_FUTURE_INDUSTRIES` / `SHENZHEN_FUTURE_INDUSTRIES` 及后续 APP 同源字典为准。
