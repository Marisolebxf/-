# 企业分析结果 API 契约（camelCase · 前端直用）

> **版本**：v1.0 · 2026-07-30
> **作者**：[human:xtq] supervised_by human:徐滕强
> **来源**：ARCH-ANALYSIS-TASK-设计方案.md v3.4 §9/§10/§11 + §7.6 TS 类型定义
> **算法真源**：demo-algo-ent-analysis `async_task_manager.py`（enterprise_eval）+ demo-algo-science `innov/analysis/*`（risk_insight / talent_recommend）
> **命名风格**：本文档所有 JSON 字段均为 **camelCase**（Python Worker 从算法侧 snake_case 转换后写入 MinIO，前端直接消费）
> **用途**：前端 `src/topic/v1/analysis/results/*.ts` 类型定义的字段级权威

---

## 0. 数据流

```
算法 task_completed 回调（result 内嵌 payload，snake_case）
  → Python API 投递 RabbitMQ
  → Python Worker 消费：snake_case → camelCase 递归转换 → 写 MinIO
  → 转发 resultUrl 给 Java
  → Java 存指针（不解析 result JSON）
  → 前端 GET /tasks/{id}/result → 返回 resultUrl → 从 MinIO 拉 camelCase JSON
```

---

## 1. 企业评估（enterprise_eval）

### 1.1 统一外层（三个 subType 共用）

```json
{
  "taskId": "EVAL-20260730-001",
  "analysisType": "enterprise_eval",
  "subType": "technology",
  "status": "success",
  "reportStatus": "not_created",
  "meta": {
    "taskName": "技术力评估",
    "enterpriseCount": 2,
    "templateName": "当前自定义配置",
    "createdAt": "2026-07-30T10:00:00",
    "generatedAt": "2026-07-30T10:00:30"
  },
  "enterprises": [
    { "enterpriseCode": "91440300MA5DJWNF8W", "enterpriseName": "深芯微集成电路股份有限公司" }
  ],
  "summary": { },
  "result": { },
  "weights": { },
  "dataSource": "entan"
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `taskId` | string | Java 全局唯一生成 |
| `analysisType` | string | 固定 `"enterprise_eval"` |
| `subType` | string | `"technology"` / `"business"` / `"competitiveness"` |
| `status` | string | 固定 `"success"`（失败/取消不返回结果） |
| `reportStatus` | string | `"not_created"` / `"running"` / `"success"`（Java 报告任务状态修正器回写） |
| `meta` | object | 任务元信息 |
| `enterprises` | array | 参评企业列表 |
| `summary` | object | KPI 汇总（按 subType 不同） |
| `result` | object | 详细结果（按 subType 不同） |
| `weights` | object | 权重快照（算法补充字段） |
| `dataSource` | string | 数据来源标识 |

### 1.2 technology（技术力）

**summary**：

| 字段 | 类型 | 说明 |
|---|---|---|
| `maxScore` | number | 最高分 |
| `enterpriseCount` | number | 企业数 |
| `avgScore` | number | 平均分 |
| `highRiskCount` | number | 高风险企业数（得分 < 40） |

**result**：

```json
{
  "radarAxes": ["技术创新", "技术人才", "技术投入", "技术合作", "技术转化"],
  "radarSeries": [
    {
      "enterpriseCode": "91440300MA5DJWNF8W",
      "enterpriseName": "深芯微集成电路股份有限公司",
      "values": {
        "技术创新": 85.5,
        "技术人才": 72.0,
        "技术投入": 68.5,
        "技术合作": 75.0,
        "技术转化": 60.0
      }
    }
  ],
  "ranking": [
    { "enterpriseName": "深芯微集成电路股份有限公司", "enterpriseCode": "91440300MA5DJWNF8W", "score": 85.5 }
  ],
  "diagnosisRows": [
    {
      "enterpriseName": "深芯微集成电路股份有限公司",
      "enterpriseCode": "91440300MA5DJWNF8W",
      "totalScore": 85.5,
      "innovationCount": 1,
      "rdInvestmentPct": 68.5,
      "confidence": "high",
      "gapText": "技术转化能力不足；建议加强产学研合作"
    }
  ],
  "trendAvailable": false,
  "trendHint": "当前无时序数据，暂不支持趋势分析"
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `radarAxes` | string[] | 五维雷达轴名 |
| `radarSeries` | array | 每企业的雷达数据（支持 A/B 对象选择） |
| `radarSeries[].values` | object | key=轴名，value=得分（0-100） |
| `ranking` | array | 按总分降序 |
| `diagnosisRows` | array | 诊断表（每企业一行） |
| `diagnosisRows[].totalScore` | number | 总分 |
| `diagnosisRows[].innovationCount` | number | 创新点数 |
| `diagnosisRows[].rdInvestmentPct` | number | 研发投入占比 |
| `diagnosisRows[].confidence` | string | `"high"` / `"medium"` / `"low"` |
| `diagnosisRows[].gapText` | string \| null | 差距与建议文案 |
| `trendAvailable` | boolean | 趋势数据是否可用 |
| `trendHint` | string | 趋势不可用时的提示文案 |

### 1.3 business（商业力）

**summary**：

| 字段 | 类型 | 说明 |
|---|---|---|
| `maxScore` | number | 最高分 |
| `enterpriseCount` | number | 企业数 |
| `avgScore` | number | 当前企业平均分 |
| `benchmarkAvgScore` | number \| null | 对标库平均分（对标库不可用时为 `null`） |
| `benchmarkAvailable` | boolean | 对标库是否可用 |
| `highConfidenceCount` | number | 高可信度企业数（得分 >= 70） |

**result**：

```json
{
  "operatingIndicators": [
    {
      "enterpriseCode": "91440300MA5DJWNF8W",
      "enterpriseName": "深芯微集成电路股份有限公司",
      "indicators": {
        "市场": 75.0,
        "产品": 80.0,
        "品牌": 65.0,
        "技术合作": 70.0,
        "产业链覆盖": 60.0,
        "关键环节参与": 55.0
      }
    }
  ],
  "ranking": [
    { "enterpriseName": "深芯微集成电路股份有限公司", "enterpriseCode": "91440300MA5DJWNF8W", "score": 75.0 }
  ],
  "tabs": ["operation_diagnosis", "revenue_trend", "industry_benchmark"],
  "diagnosisRows": [
    {
      "enterpriseName": "深芯微集成电路股份有限公司",
      "enterpriseCode": "91440300MA5DJWNF8W",
      "totalScore": 75.0,
      "confidence": "high",
      "diagnosisText": "市场拓展不足；建议加强品牌建设"
    }
  ],
  "revenueTrendAvailable": false,
  "revenueTrendHint": "当前无营收时序数据",
  "industryBenchmarkAvailable": false,
  "industryBenchmarkHint": "暂无对标库数据"
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `operatingIndicators` | array | 经营指标对比（非雷达） |
| `operatingIndicators[].indicators` | object | key=指标名（中文），value=得分 |
| `tabs` | string[] | Tab 标识符数组 |
| `diagnosisRows` | array | 经营诊断表 |
| `revenueTrendAvailable` | boolean | 营收趋势是否可用 |
| `industryBenchmarkAvailable` | boolean | 行业对标是否可用 |

> **注意**：`operatingIndicators[].indicators` 的 key 为中文（市场/产品/品牌/技术合作/产业链覆盖/关键环节参与），Python 转 camelCase 不会转换中文 key，前端直接按中文 key 读取。

### 1.4 competitiveness（综合竞争力）

**summary**：

| 字段 | 类型 | 说明 |
|---|---|---|
| `maxScore` | number | 最高分 |
| `enterpriseCount` | number | 企业数 |
| `avgScore` | number | 平均分 |
| `highConfidenceCount` | number | 高可信度企业数 |

**result**：

```json
{
  "radarAxes": ["创新能力", "经营能力", "成长能力"],
  "radarSeries": [
    {
      "enterpriseCode": "91440300MA5DJWNF8W",
      "enterpriseName": "深芯微集成电路股份有限公司",
      "values": {
        "创新能力": 85.5,
        "经营能力": 75.0,
        "成长能力": 65.0
      }
    }
  ],
  "setAverage": {
    "创新能力": 70.0,
    "经营能力": 68.0,
    "成长能力": 65.0
  },
  "setLeader": {
    "创新能力": 85.5,
    "经营能力": 75.0,
    "成长能力": 65.0
  },
  "ranking": [
    { "enterpriseName": "深芯微集成电路股份有限公司", "enterpriseCode": "91440300MA5DJWNF8W", "score": 75.17 }
  ],
  "dimensionRows": [
    {
      "enterpriseName": "深芯微集成电路股份有限公司",
      "enterpriseCode": "91440300MA5DJWNF8W",
      "totalScore": 75.17,
      "dimension": "创新能力",
      "score": 85.5,
      "setMean": 70.0,
      "setLeader": 85.5,
      "gapText": "技术转化能力不足"
    },
    {
      "enterpriseName": "深芯微集成电路股份有限公司",
      "enterpriseCode": "91440300MA5DJWNF8W",
      "totalScore": 75.17,
      "dimension": "经营能力",
      "score": 75.0,
      "setMean": 68.0,
      "setLeader": 75.0,
      "gapText": "技术转化能力不足"
    },
    {
      "enterpriseName": "深芯微集成电路股份有限公司",
      "enterpriseCode": "91440300MA5DJWNF8W",
      "totalScore": 75.17,
      "dimension": "成长能力",
      "score": 65.0,
      "setMean": 65.0,
      "setLeader": 65.0,
      "gapText": "技术转化能力不足"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `radarAxes` | string[] | 三维雷达轴名 |
| `radarSeries` | array | 每企业的雷达数据 |
| `setAverage` | object | 集合均值（key=维度名） |
| `setLeader` | object | 集合龙头（key=维度名） |
| `dimensionRows` | array | **扁平数组**，每维度一行（前端按 A/B 选择切换企业过滤） |
| `dimensionRows[].dimension` | string | 维度名 |
| `dimensionRows[].score` | number | 该维度得分 |
| `dimensionRows[].setMean` | number | 集合均值 |
| `dimensionRows[].setLeader` | number | 龙头值 |
| `dimensionRows[].gapText` | string \| null | 差距文案 |

---

## 2. 风险洞察（risk_insight）

### 2.1 supply_chain（供应链关系）

```json
{
  "subType": "supply_chain",
  "summary": {
    "enterprises": ["深芯微集成电路股份有限公司"],
    "relationScope": ["supplier", "customer", "partner"],
    "displayMode": "expand_by_node",
    "dataTime": "2026-07"
  },
  "graph": {
    "maxDepth": 3,
    "nodes": [
      {
        "id": "91440300MA5DJWNF8W",
        "name": "企业(91440300MA5DJWNF8W)",
        "type": "center",
        "depth": 0,
        "hasChildren": true,
        "isKey": true,
        "hasRisk": false
      },
      {
        "id": "REL-1-WNF8-00",
        "name": "supplier节点-1-00",
        "type": "supplier",
        "depth": 1,
        "hasChildren": true,
        "isKey": false,
        "hasRisk": false
      }
    ],
    "edges": [
      { "source": "91440300MA5DJWNF8W", "target": "REL-1-WNF8-00", "relationType": "supplier" }
    ],
    "level": 1,
    "nodeCount": 15,
    "commonNodeCount": 5
  },
  "keyNodes": [
    {
      "name": "supplier节点-1-00",
      "relationType": "supplier",
      "influenceScore": 85.0,
      "suggestion": "该supplier影响力突出，建议加强战略合作，建立长期协同机制。",
      "isKey": true
    }
  ],
  "breakRisks": [
    {
      "name": "customer节点-1-01",
      "riskLevel": "高",
      "impact": "下游订单流失，对企业运营影响重大",
      "suggestion": "立即启动备选customer寻源，建立应急库存与冗余供应体系。"
    }
  ],
  "reportStatus": "not_created"
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `summary.enterprises` | string[] | 分析对象企业名称列表 |
| `summary.relationScope` | string[] | 关系范围（`supplier`/`customer`/`partner`） |
| `graph.maxDepth` | number | 最大展开深度（固定 3） |
| `graph.nodes[]` | array | 图谱节点 |
| `graph.nodes[].type` | string | `center`/`supplier`/`customer`/`partner` |
| `graph.nodes[].depth` | number | 节点深度（0=中心企业，1-3=展开层级） |
| `graph.nodes[].hasChildren` | boolean | 是否有下级 |
| `graph.nodes[].isKey` | boolean | 是否关键节点 |
| `graph.nodes[].hasRisk` | boolean | 是否有断链风险 |
| `graph.edges[]` | array | 图谱边 |
| `graph.edges[].relationType` | string | 关系类型 |
| `graph.level` | number | 当前展示级数（默认 1） |
| `graph.nodeCount` | number | 节点总数 |
| `graph.commonNodeCount` | number | 公共节点数 |
| `keyNodes[]` | array | 关键节点列表 |
| `keyNodes[].influenceScore` | number | 影响力得分 |
| `breakRisks[]` | array | 断链风险列表 |
| `breakRisks[].riskLevel` | string | 风险等级（`高`/`中`/`低`） |

> **展开规则**：算法一次算满 3 级写入 MinIO，前端默认渲染 1 级，点击节点 `+` 从快照按需展开，不新建分析任务。

### 2.2 pain_points（发展痛难点）

```json
{
  "subType": "pain_points",
  "summary": {
    "enterprises": ["深芯微集成电路股份有限公司"],
    "diagnosisMethod": "joint_common",
    "diagnosisScope": ["tech_rd", "market_expand", "financing", "management"],
    "dataTime": "2026-07"
  },
  "dimensionCards": [
    {
      "dimension": "tech_rd",
      "issueCount": 2,
      "priority": "高",
      "affectedEnterpriseCount": 1
    },
    {
      "dimension": "market_expand",
      "issueCount": 1,
      "priority": "中",
      "affectedEnterpriseCount": 1
    }
  ],
  "issues": [
    {
      "title": "客户结构集中",
      "priority": "高",
      "dimension": "market_expand",
      "affectedEnterpriseCount": 1,
      "typicalEnterprises": ["深芯微集成电路股份有限公司"],
      "evidence": "前5大客户营收占比超过80%",
      "cause": "市场开拓策略偏向大客户",
      "bestPractice": "建立多元化客户体系，前5大客户占比控制在60%以内",
      "solution": "拓展中小客户群体，建立客户分级管理机制"
    }
  ],
  "reportStatus": "not_created"
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `summary.diagnosisMethod` | string | 诊断方式（`joint_common`） |
| `summary.diagnosisScope` | string[] | 诊断维度（`tech_rd`/`market_expand`/`financing`/`management`） |
| `dimensionCards[]` | array | 四维诊断卡片 |
| `dimensionCards[].dimension` | string | 维度代码 |
| `dimensionCards[].issueCount` | number | 问题数 |
| `dimensionCards[].priority` | string | 优先级（`高`/`中`/`低`） |
| `dimensionCards[].affectedEnterpriseCount` | number | 影响企业数 |
| `issues[]` | array | 共性问题列表（按优先级排序） |
| `issues[].dimension` | string | 所属维度 |
| `issues[].typicalEnterprises` | string[] | 典型企业名称列表 |
| `issues[].evidence` | string | 命中依据 |
| `issues[].cause` | string | 成因 |
| `issues[].bestPractice` | string | 行业最佳实践 |
| `issues[].solution` | string | 解决方向 |

---

## 3. 引育推荐（talent_recommend）

### 3.1 统一外层（attraction / cultivation 共用）

```json
{
  "taskId": "REC-20260730-001",
  "analysisType": "talent_recommend",
  "subType": "attraction",
  "selectionMode": "filter",
  "generatedAt": "2026-07-30T10:00:30",
  "candidateCount": 5,
  "reportStatus": "not_created",
  "weights": { "technologyMatch": 34, "growth": 33, "regionalFit": 33 },
  "rankings": [ ],
  "details": { }
}
```

### 3.2 attraction（招引推荐）

**rankings[]**：

```json
[
  {
    "rank": 1,
    "enterpriseCode": "MOCK001",
    "enterpriseName": "深圳创新科技有限公司",
    "industryDomain": "集成电路",
    "geographicSource": "深圳",
    "targetTraits": ["专精特新", "关键技术型"],
    "recommendationScore": 85.5
  }
]
```

**details**（key = enterpriseCode）：

```json
{
  "MOCK001": {
    "riskFocusCount": 0,
    "tags": ["专精特新", "关键技术型"],
    "dimensions": [
      { "code": "technology_match", "evidenceStatus": "available" },
      { "code": "growth", "evidenceStatus": "available" },
      { "code": "regional_fit", "evidenceStatus": "partial" }
    ],
    "judgmentBasis": {
      "technologyMatchBasis": "技术匹配度 0.85，有效专利 328 件，研发投入占比 12.00%",
      "growthBasis": "成长性 0.72，营收增长率 15.00%，最近年度营收 3.50 亿元",
      "regionalFitBasis": "区域适配性 0.65，地域来源 深圳，行业领域 集成电路"
    },
    "coreAdvantages": ["技术实力突出，有效专利 328 件"],
    "targetTraits": ["专精特新", "关键技术型"],
    "targetTraitBasis": "基于企业资质与技术领域匹配度",
    "keyIndicators": {
      "validPatentCount": 328,
      "latestAnnualRevenueYiYuan": 3.5
    },
    "riskCredit": {
      "judicialLitigationCount": 0,
      "dishonestEnforcementCount": 0,
      "abnormalOperationCount": 0,
      "administrativePenaltyCount": 0
    },
    "cooperationValue": "高"
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `rankings[].industryDomain` | string | 行业领域 |
| `rankings[].geographicSource` | string | 地域来源 |
| `rankings[].targetTraits` | string[] | 目标特征标签 |
| `rankings[].recommendationScore` | number | 招引推荐指数 |
| `details[].riskFocusCount` | number | 风险关注数（司法涉诉+失信被执行） |
| `details[].dimensions[].code` | string | `technology_match`/`growth`/`regional_fit` |
| `details[].dimensions[].evidenceStatus` | string | `available`/`partial`/`unavailable` |
| `details[].judgmentBasis` | object | 判定依据文本（三个维度） |
| `details[].coreAdvantages` | string[] | 核心优势列表 |
| `details[].targetTraitBasis` | string | 目标特征判定依据 |
| `details[].keyIndicators.validPatentCount` | number | 有效专利数 |
| `details[].keyIndicators.latestAnnualRevenueYiYuan` | number | 最近年度营收（亿元） |
| `details[].riskCredit` | object | 企业风险与信用汇总 |
| `details[].cooperationValue` | string | 合作价值（`高`/`中`/`一般`） |

### 3.3 cultivation（培育推荐）

**rankings[]**：

```json
[
  {
    "rank": 1,
    "enterpriseCode": "MOCK101",
    "enterpriseName": "深圳芯源微电子",
    "industryCategory": "集成电路",
    "enterpriseScale": "中型",
    "developmentBottleneck": "资金链紧张",
    "recommendationScore": 78.0
  }
]
```

**details**（key = enterpriseCode）：

```json
{
  "MOCK101": {
    "riskFocusCount": 0,
    "tags": ["集成电路", "中型"],
    "dimensions": [
      { "code": "technology_barrier", "evidenceStatus": "available" },
      { "code": "market_growth", "evidenceStatus": "available" },
      { "code": "team_background", "evidenceStatus": "partial" }
    ],
    "judgmentBasis": {
      "technologyBarrierBasis": "技术壁垒 0.80，有效专利 256 件，研发投入占比 10.00%",
      "marketGrowthBasis": "市场增长 0.65，营收增长率 12.00%，最近年度营收 5.20 亿元",
      "teamBackgroundBasis": "团队背景 0.55，研发人员占比 18.00%"
    },
    "coreAdvantages": ["行业壁垒高", "知识储备丰富"],
    "developmentBottleneck": "资金链紧张",
    "cultivationSuggestion": "建议在资金链紧张方面给予定向支持",
    "keyIndicators": {
      "validPatentCount": 256,
      "latestAnnualRevenueYiYuan": 5.2
    },
    "riskCredit": {
      "judicialLitigationCount": 0,
      "dishonestEnforcementCount": 0,
      "abnormalOperationCount": 0,
      "administrativePenaltyCount": 0
    },
    "requiredSupport": "资金+政策"
  }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `rankings[].industryCategory` | string | 产业类别 |
| `rankings[].enterpriseScale` | string | 企业规模 |
| `rankings[].developmentBottleneck` | string | 发展瓶颈摘要 |
| `details[].dimensions[].code` | string | `technology_barrier`/`market_growth`/`team_background` |
| `details[].cultivationSuggestion` | string | 培育建议 |
| `details[].requiredSupport` | string | 所需支持（`资金+政策`/`技术指导`等） |

---

## 4. TypeScript 类型定义（§7.6 权威）

前端 `src/topic/v1/analysis/results/` 下三个 `.ts` 文件，字段级权威以本文档为准。

> **唯一类型调整**：`BizEvalResult.summary.benchmarkAvgScore` 从 `number` 改为 `number | null`（对标库不可用时算法返回 `null` + `benchmarkAvailable: false`）。

---

## 5. 变更记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-07-30 | 初版：基于算法侧最新代码（ent-analysis 25ffba8 / science 733d8d1）+ ARCH v3.4 §7.6 TS 类型定义，全部字段转 camelCase |
