# 企业战略分析 异步任务结果 JSON 契约（task_completed Webhook result 字段）

> **文档目的**：定义算法侧 `task_completed` Webhook 中 `result` 字段的完整 JSON 结构，供前端提前编写展示代码。
> **关联任务**：ENT-ALGO-ENTAN-ASYNC-FRAME（企业评估）/ ENT-ALGO-SCIENCE-ASYNC-FRAME（风险洞察、引育推荐）
> **维护**：算法工程师 唐绍祖 ｜ **生成**：2026-07-29 ｜ **版本**：v2（已与代码逐字段核对）
> **代码真源**：
> - 企业评估：`repos/demo-algo-ent-analysis/entan/common/async_task_manager.py#_compute_result`（SELECT * FROM ads.tech_power / ads.biz_power）
> - 风险洞察 / 引育推荐：`repos/demo-algo-science/innov/analysis/{supply_chain,pain_points,attraction,cultivation}.py#compute`
> - 表结构：`repos/demo-algo-ent-analysis/scripts/mysql/schema_mysql.sql`（gkxlumenx_ads.tech_power / biz_power）

---

## 0. 数据链路（为什么前端要先拿到格式）

```
前端发起分析 → Java 编排 → Python svc create-and-start（写 MySQL pending，立即返回 task_id）
   → 算法 Worker 后台执行 5~6 节点 → 全部完成发 task_completed Webhook（result 字段 = 算法 compute() 返回值）
   → Python svc 把 result JSON 上传 MinIO + 回填 Java → 前端凭 MinIO 地址拉取 JSON 渲染
```

**关键**：`task_completed` Webhook 的 `result` 字段（即最终存入 MinIO 的 JSON）就是前端渲染的数据源。
`result` 是算法 `compute()` / `_compute_result()` 的**直接返回值，无额外包装**。本文档定义该值在 3 大类 / 6 小类下的完整结构。**全部字段 snake_case（D-30）**。

---

## 1. 3 大类 / 6 小类枚举

| analysis_type | sub_type | 中文名 | 产出仓 | 节点数 |
|---|---|---|---|---|
| enterprise_eval | technology | 技术力评估 | demo-algo-ent-analysis | 6 |
| enterprise_eval | business | 商业力评估 | demo-algo-ent-analysis | 6 |
| enterprise_eval | competitiveness | 综合竞争力评估 | demo-algo-ent-analysis | 6 |
| risk_insight | supply_chain | 供应链风险图谱 | demo-algo-science | 5 |
| risk_insight | pain_points | 发展痛难点诊断 | demo-algo-science | 5 |
| talent_recommend | attraction | 招引推荐 | demo-algo-science | 5 |
| talent_recommend | cultivation | 培育推荐 | demo-algo-science | 5 |

> ⚠️ 废弃历史 `mode` 字段，统一用 `sub_type`（D-30）。

---

## 2. task_completed Webhook 顶层结构

```json
{
  "event": "task_completed",
  "task_id": "EVAL-xxx",
  "analysis_type": "enterprise_eval",
  "sub_type": "technology",
  "status": "success",
  "progress": 100,
  "result": { /* 见 §3~§5 各 sub_type */ },
  "timestamp": "2026-07-29 19:00:00"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| event | string | ✅ | 固定 `task_completed` |
| task_id | string | ✅ | Java 生成的全局唯一 ID |
| analysis_type | string | ✅ | enterprise_eval / risk_insight / talent_recommend |
| sub_type | string | ✅ | 见 §1 枚举 |
| status | string | ✅ | success / failed / cancelled |
| progress | float | ✅ | 0~100，task_completed 时为 100 |
| result | object | ✅(success时) | 最终结果 = 算法 compute() 返回值，结构见 §3~§5 |
| error | string | failed时 | 错误信息 |
| timestamp | string | ✅ | YYYY-MM-DD HH:MM:SS |

---

## 3. 企业评估 enterprise_eval（sub_type: technology / business / competitiveness）

### 3.1 result 结构（三模式共用骨架，仅维度字段不同）

```json
{
  "sub_type": "technology",
  "enterprise_count": 5,
  "tech_power": [ { /* tech_power 表整行，见 3.2 */ } ],
  "biz_power": [ { /* biz_power 表整行，见 3.3 */ } ],
  "data_source": "entan",
  "radar_dimensions": ["创新", "经营", "成长", "风险", "可信度"]
}
```

**三模式差异**（仅最后一个维度字段不同，其余字段完全一致）：

| sub_type | 附加字段 | 值 |
|---|---|---|
| technology | `radar_dimensions` | ["创新", "经营", "成长", "风险", "可信度"]（五维雷达）|
| business | `biz_dimensions` | ["市场", "产品", "品牌", "技术合作", "产业链覆盖", "关键环节参与"]（六经营指标）|
| competitiveness | `radar_dimensions` | ["技术力", "商业力", "综合竞争力"]（三维雷达）|

> 说明：`tech_power` / `biz_power` 由 `SELECT * FROM gkxlumenx_ads.tech_power/biz_power WHERE org_id IN (...)` 取整行，三模式都会返回这两张表的全部行（不区分模式裁剪）。前端按 `sub_type` 决定用哪张表 + 哪个维度字段渲染。

### 3.2 tech_power 行结构（gkxlumenx_ads.tech_power 表，SELECT *）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 自增主键 |
| org_id | string | 企业 ID |
| enterprise_name | string | 企业名称 |
| industry_category | string | 行业分类 |
| headquarters_city | string | 总部城市 |
| talent_score | decimal | 人才分 |
| innovation_score | decimal | 创新分 |
| transfer_score | decimal | 转化分 |
| cooperation_score | decimal | 合作分 |
| investment_score | decimal | 投入分 |
| tech_power_index | decimal | 技术力综合指数 |
| rank_overall | int | 综合排名 |
| advantages | string(longtext) | 优势（JSON 文本）|
| weaknesses | string(longtext) | 短板（JSON 文本）|
| suggestions | string(longtext) | 建议（JSON 文本）|
| trend | string(longtext) | 趋势（JSON 文本）|
| model_version | string | 模型版本，如 ahp_weighted_v0.1-demo |
| create_time | string | 创建时间 |

### 3.3 biz_power 行结构（gkxlumenx_ads.biz_power 表，SELECT *）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 自增主键 |
| org_id | string | 企业 ID |
| enterprise_name | string | 企业名称 |
| industry_category | string | 行业分类 |
| headquarters_city | string | 总部城市 |
| market_score | decimal | 市场分 |
| product_score | decimal | 产品分 |
| brand_score | decimal | 品牌分 |
| cooperation_score | decimal | 合作分 |
| chain_coverage_score | decimal | 产业链覆盖分 |
| chain_keynode_score | decimal | 关键环节参与分 |
| biz_power_index | decimal | 商业力综合指数 |
| rank_overall | int | 综合排名 |
| advantages | string(longtext) | 优势（JSON 文本）|
| weaknesses | string(longtext) | 短板（JSON 文本）|
| suggestions | string(longtext) | 建议（JSON 文本）|
| trend | string(longtext) | 趋势（JSON 文本）|
| model_version | string | 模型版本 |
| create_time | string | 创建时间 |

> ⚠️ `advantages/weaknesses/suggestions/trend` 为 longtext，算法侧写入时为 JSON 字符串；前端需 JSON.parse 后使用（当前 demo 阶段可能为 null）。

---

## 4. 风险洞察 risk_insight

### 4.1 sub_type=supply_chain（供应链风险图谱）

```json
{
  "sub_type": "supply_chain",
  "summary": {
    "enterprises": ["企业(ORG001)", "企业(ORG002)"],
    "relation_scope": ["supplier", "customer", "partner"],
    "display_mode": "expand_by_node",
    "data_time": "2026-07-29"
  },
  "graph": {
    "max_depth": 3,
    "nodes": [
      {
        "id": "ORG001",
        "name": "企业(ORG001)",
        "type": "center",
        "depth": 0,
        "has_children": true,
        "is_key": true,
        "has_risk": false
      },
      {
        "id": "REL-1-0001-00",
        "name": "supplier节点-1-00",
        "type": "supplier",
        "depth": 1,
        "has_children": true,
        "is_key": false,
        "has_risk": true
      }
    ],
    "edges": [
      { "source": "ORG001", "target": "REL-1-0001-00", "relation_type": "supplier" }
    ],
    "level": 1,
    "node_count": 12,
    "common_node_count": 5
  },
  "key_nodes": [
    {
      "name": "supplier节点-1-00",
      "relation_type": "supplier",
      "influence_score": 0.872,
      "suggestion": "该supplier影响力突出，建议加强战略合作，建立长期协同机制。",
      "is_key": true
    }
  ],
  "break_risks": [
    {
      "name": "customer节点-2-01",
      "risk_level": "高",
      "impact": "下游订单流失，对企业运营影响重大",
      "suggestion": "立即启动备选customer寻源，建立应急库存与冗余供应体系。"
    }
  ],
  "report_status": "not_created"
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|---|---|---|
| summary.enterprises | string[] | 分析的企业名称列表（格式「企业(code)」）|
| summary.relation_scope | string[] | 关系类型范围：supplier(上游)/customer(下游)/partner(协同)；默认三者全选 |
| summary.display_mode | string | 展示模式，默认 `expand_by_node` |
| summary.data_time | string | 数据日期 YYYY-MM-DD |
| graph.max_depth | int | 最大展开层级（固定 3，D-20 方案 A 一次算满）|
| graph.nodes[].id | string | 节点 ID（中心企业=org_id；关系节点=REL-{depth}-{尾4位}-{序号}）|
| graph.nodes[].type | string | center / supplier / customer / partner |
| graph.nodes[].depth | int | 0=中心企业，1~3=逐级展开 |
| graph.nodes[].has_children | bool | 是否有下级（前端按需展开快照用）|
| graph.nodes[].is_key | bool | 是否关键节点 |
| graph.nodes[].has_risk | bool | 是否有断链风险 |
| graph.edges[].source / target | string | 父子节点 ID |
| graph.edges[].relation_type | string | supplier/customer/partner |
| graph.level | int | 默认展示层级（1）|
| graph.node_count | int | 节点总数 |
| graph.common_node_count | int | depth=1 公共节点数 |
| key_nodes[].influence_score | float | 影响力评分 0~1 |
| key_nodes[].suggestion | string | 影响力应对建议 |
| break_risks[].risk_level | string | 高/中/低 |
| break_risks[].impact | string | 风险影响文本 |
| break_risks[].suggestion | string | 风险应对建议 |
| report_status | string | 固定 `not_created`（预留）|

### 4.2 sub_type=pain_points（发展痛难点诊断）

```json
{
  "sub_type": "pain_points",
  "summary": {
    "enterprises": ["企业(ORG001)", "企业(ORG002)"],
    "diagnosis_method": "joint_common",
    "diagnosis_scope": ["tech_rd", "market_expand", "financing", "management"],
    "data_time": "2026-07-29"
  },
  "dimension_cards": [
    {
      "dimension": "tech_rd",
      "issue_count": 2,
      "priority": "高",
      "affected_enterprise_count": 3
    }
  ],
  "issues": [
    {
      "title": "研发投入强度偏低",
      "priority": "高",
      "dimension": "tech_rd",
      "affected_enterprise_count": 3,
      "typical_enterprises": ["企业(ORG001)", "企业(ORG002)"],
      "evidence": "样本企业平均研发投入占比 3.20%，低于行业基准，命中「研发投入强度偏低」",
      "cause": "研发投入占营收比低于行业均值，创新后劲不足",
      "best_practice": "头部企业研发投入占比普遍超过 8%，建议逐年提升至行业前列",
      "solution": "制定研发投入三年提升计划，设立专项研发预算，引入研发费用加计扣除政策红利"
    }
  ],
  "report_status": "not_created"
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|---|---|---|
| summary.diagnosis_method | string | 诊断方法，默认 `joint_common`（联合共性诊断）|
| summary.diagnosis_scope | string[] | 四维：tech_rd(技术研发)/market_expand(市场拓展)/financing(融资)/management(管理) |
| dimension_cards[].dimension | string | tech_rd / market_expand / financing / management |
| dimension_cards[].issue_count | int | 该维度命中问题数（1~3）|
| dimension_cards[].priority | string | 高/中/低 |
| dimension_cards[].affected_enterprise_count | int | 受影响企业数 |
| issues[].priority | string | 高/中/低（issues 按 高>中>低 排序）|
| issues[].typical_enterprises | string[] | 典型企业名称（最多 3 个，格式「企业(code)」）|
| issues[].evidence | string | 命中依据文本 |
| issues[].cause | string | 原因 |
| issues[].best_practice | string | 最佳实践 |
| issues[].solution | string | 解决建议 |
| report_status | string | 固定 `not_created`（预留）|

---

## 5. 引育推荐 talent_recommend

### 5.1 sub_type=attraction（招引推荐，对象：全国企业）

```json
{
  "task_id": "",
  "analysis_type": "talent_recommend",
  "sub_type": "attraction",
  "selection_mode": "filter",
  "generated_at": "2026-07-29T19:00:00+08:00",
  "candidate_count": 10,
  "report_status": "not_created",
  "weights": { "technology_match": 34, "growth": 33, "regional_fit": 33 },
  "rankings": [
    {
      "enterprise_code": "ORG001",
      "enterprise_name": "企业(ORG001)",
      "rank": 1,
      "industry_domain": "新一代信息技术",
      "geographic_source": "华南",
      "target_traits": ["专精特新", "高成长型"],
      "recommendation_score": 87.52
    }
  ],
  "details": {
    "ORG001": {
      "risk_focus_count": 2,
      "tags": ["专精特新", "高成长型"],
      "dimensions": [
        { "code": "technology_match", "evidence_status": "available" },
        { "code": "growth", "evidence_status": "partial" },
        { "code": "regional_fit", "evidence_status": "available" }
      ],
      "judgment_basis": {
        "technology_match_basis": "技术匹配度 0.82，有效专利 120 件，研发投入占比 8.50%",
        "growth_basis": "成长性 0.65，营收增长率 22.00%，最近年度营收 5.20 亿元",
        "regional_fit_basis": "区域适配性 0.78，地域来源 华南，行业领域 新一代信息技术"
      },
      "core_advantages": ["技术实力突出，有效专利 120 件"],
      "target_traits": ["专精特新", "高成长型"],
      "target_trait_basis": "基于企业指标与行业画像，命中 专精特新, 高成长型 特征",
      "key_indicators": {
        "valid_patent_count": 120,
        "latest_annual_revenue_yi_yuan": 5.20
      },
      "risk_credit": {
        "judicial_litigation_count": 1,
        "dishonest_enforcement_count": 0,
        "abnormal_operation_count": 1,
        "administrative_penalty_count": 0
      },
      "cooperation_value": "合作价值高，建议优先对接"
    }
  }
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|---|---|---|
| task_id | string | 算法返回空串，由调用方回填 |
| selection_mode | string | `filter`（Java/Python 侧筛选后传入候选企业）|
| generated_at | string | 生成时间 ISO8601 +08:00 |
| candidate_count | int | 候选企业数 |
| weights | object | 三维权重（合计 100，待 Q015 确认，当前临时默认）|
| rankings[].rank | int | 按 recommendation_score 降序排名（1 起）|
| rankings[].industry_domain | string | 行业领域（新一代信息技术/生物医药/新材料/新能源/高端装备）|
| rankings[].geographic_source | string | 地域来源（华南/华东/华北/西南/华中）|
| rankings[].target_traits | string[] | 目标特质标签（从专精特新/关键技术型/高成长型/链主企业/独角兽/瞪羚企业/高新技术企业/技术先进型 中随机 1~3 个）|
| rankings[].recommendation_score | float | 推荐指数 0~100 |
| details[code].risk_focus_count | int | 风险关注数（诉讼数+失信数）|
| details[code].tags | string[] | 同 rankings 的 target_traits |
| details[code].dimensions[].code | string | technology_match / growth / regional_fit |
| details[code].dimensions[].evidence_status | string | available(≥0.7) / partial(≥0.4) / unavailable |
| details[code].judgment_basis | object | 三维度判定依据文本（键：{dim}_basis）|
| details[code].core_advantages | string[] | 核心优势（维度≥0.7 命中；无则「综合能力均衡，具备合作潜力」）|
| details[code].target_trait_basis | string | 目标特征依据文本 |
| details[code].key_indicators | object | 关键指标：valid_patent_count(有效专利数) / latest_annual_revenue_yi_yuan(最近年度营收，亿元) |
| details[code].risk_credit | object | 风险信用：judicial_litigation_count(诉讼)/dishonest_enforcement_count(失信)/abnormal_operation_count(异常)/administrative_penalty_count(处罚) |
| details[code].cooperation_value | string | 合作价值评估文本（高/中等/待考察 三档）|

### 5.2 sub_type=cultivation（培育推荐，对象：深圳市内企业）

**顶层结构与 attraction 完全一致**（task_id/analysis_type/sub_type/selection_mode/generated_at/candidate_count/report_status/weights/rankings/details），差异如下：

| 差异点 | attraction | cultivation |
|---|---|---|
| sub_type | attraction | cultivation |
| 三维度 code | technology_match / growth / regional_fit | technology_barrier / market_growth / team_background |
| weights 键 | technology_match/growth/regional_fit | technology_barrier/market_growth/team_background |
| judgment_basis 键 | technology_match_basis / growth_basis / regional_fit_basis | technology_barrier_basis / market_growth_basis / team_background_basis |
| rankings 行字段 | industry_domain / geographic_source / target_traits / recommendation_score | industry_category / enterprise_scale / development_bottleneck / recommendation_score |

**cultivation rankings 行示例**：

```json
{
  "enterprise_code": "ORG002",
  "enterprise_name": "企业(ORG002)",
  "rank": 1,
  "industry_category": "电子信息",
  "enterprise_scale": "中型",
  "development_bottleneck": "核心技术产业化周期长",
  "recommendation_score": 82.10
}
```

**cultivation details[code] 字段**（与 attraction 的 details 字段有差异，注意替换）：

```json
{
  "ORG002": {
    "risk_focus_count": 2,
    "tags": ["技术壁垒型"],
    "dimensions": [
      { "code": "technology_barrier", "evidence_status": "available" },
      { "code": "market_growth", "evidence_status": "partial" },
      { "code": "team_background", "evidence_status": "available" }
    ],
    "judgment_basis": {
      "technology_barrier_basis": "技术壁垒 0.82，有效专利 120 件，研发投入占比 8.50%",
      "market_growth_basis": "市场增长 0.65，营收增长率 22.00%，最近年度营收 5.20 亿元",
      "team_background_basis": "团队背景 0.78，研发人员占比 25.00%"
    },
    "core_advantages": ["技术壁垒较高，有效专利 120 件"],
    "development_bottleneck": "核心技术产业化周期长",
    "cultivation_suggestion": "建议聚焦核心技术产业化...",
    "key_indicators": {
      "valid_patent_count": 120,
      "latest_annual_revenue_yi_yuan": 5.20
    },
    "risk_credit": {
      "judicial_litigation_count": 1,
      "dishonest_enforcement_count": 0,
      "abnormal_operation_count": 1,
      "administrative_penalty_count": 0
    },
    "required_support": "建议提供产业化中试资源支持"
  }
}
```

**cultivation details 字段说明**（与 attraction 不同的部分）：

| 字段 | 类型 | 说明 |
|---|---|---|
| tags | string[] | 培育标签（按维度≥0.7 命中：技术壁垒型/市场增长型/团队扎实型 等）|
| dimensions[].code | string | technology_barrier / market_growth / team_background |
| judgment_basis 键 | object | technology_barrier_basis / market_growth_basis / team_background_basis |
| development_bottleneck | string | 发展瓶颈（从 6 个预设瓶颈随机：核心技术产业化周期长/市场拓展资源不足/高端人才引进困难/融资渠道单一/供应链稳定性待提升/品牌影响力有限）|
| cultivation_suggestion | string | 培育建议文本 |
| required_support | string | 所需支持文本 |

> 注意：cultivation 的 details **没有** attraction 的 `target_traits` / `target_trait_basis` / `cooperation_value`；attraction **没有** cultivation 的 `development_bottleneck` / `cultivation_suggestion` / `required_support`。

---

## 6. 前端使用指引

1. **先按本文档写 mock 渲染**：前端可用 §3~§5 的 JSON 示例直接 mock，无需等算法实跑。
2. **MinIO 文件即本文档结构**：task_completed 后 Python svc 把 `result` 上传 MinIO，前端拉到的 JSON 与本文档结构一致（result 是算法 compute() 直接返回值，无额外包装）。
3. **枚举字段**（前端可直接 switch 渲染）：
   - `sub_type`：technology/business/competitiveness/supply_chain/pain_points/attraction/cultivation
   - `evidence_status`：available/partial/unavailable
   - `risk_level` / `priority`：高/中/低
   - 节点 `type`：center/supplier/customer/partner
   - 维度 `code`：attraction=technology_match/growth/regional_fit；cultivation=technology_barrier/market_growth/team_background；pain_points=tech_rd/market_expand/financing/management
4. **pending 字段**：`weights` 权重当前为临时默认值（pending Q015），甲方确认后更新；前端渲染时建议标注「权重待确认」。
5. `report_status` 固定 `not_created`，表示报告未生成（预留字段，前端可不渲染或置灰「报告生成中」）。
6. 企业评估的 `tech_power/biz_power` 行含 `advantages/weaknesses/suggestions/trend` longtext 字段，demo 阶段可能为 null，前端需做空值判断。

---

## 7. 算法侧待办

- [ ] 企业评估三模式当前 `SELECT *` 返回 tech_power + biz_power 全部行，未按模式裁剪；如前端需固定 schema，算法侧可在 assemble 节点做字段裁剪对齐（当前不阻塞前端，前端按 sub_type 取需要的字段即可）。
- [ ] 引育推荐 `weights` 待 Q015 甲方确认后更新 conf/settings.yaml 默认权重。
- [ ] MinIO 上传 + 回填 Java 的 callback 字段格式另见 `ENT-PY-ANALYSIS-完工.md`（callback 契约，非本文档范围）。

---

## 8. 修订记录

| 版本 | 日期 | 修订人 | 说明 |
|---|---|---|---|
| v1 | 2026-07-29 | 唐绍祖 | 初版，补齐 result 字段结构 |
| v2 | 2026-07-29 | 唐绍祖 | 与代码逐字段核对：修正 tech_power/biz_power 字段名（按 schema_mysql.sql 实际列）、修正 supply_chain.display_mode 默认值、修正 pain_points.summary.diagnosis_method/scope、修正 cultivation details 字段（补 development_bottleneck/cultivation_suggestion/required_support，去 target_traits/cooperation_value）|
