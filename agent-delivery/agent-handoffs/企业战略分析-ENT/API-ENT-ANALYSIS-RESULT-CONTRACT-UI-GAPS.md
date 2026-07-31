# 分析结果契约 vs demo 三页结果数据结构差异（给算法）

> **版本**：v1.1 · 2026-07-31  
> **对象**：算法 / Python Worker（结果 JSON 写入 MinIO，前端经 `#105 → #106` 消费）  
> **契约真源**：`[API-ENT-ANALYSIS-RESULT-CONTRACT.md](./API-ENT-ANALYSIS-RESULT-CONTRACT.md)` v1.0  
> **UI 结果真源（本版）**：`demo-ui-topic` **三页结果区**  
>
> - 企业评估：`EnterpriseEvaluationResultWorkspace.tsx` + `enterpriseEvaluationResultModel.ts` + `enterpriseEvaluationModel.ts#EnterpriseQuality`  
> - 风险洞察：`RiskInsightSupplyResult.tsx` / `RiskInsightPainResult.tsx` + `riskInsightDefinition.ts`  
> - 引育推荐：`EnterpriseRecommendation.tsx` + `enterpriseRecruitDefinition.ts`  
> **目的**：以 demo 已验收交互为准，对照契约标出 **A 改名/重组** 与 **B 缺内容**；缺内容附 demo 结构实例。  
> **请算法侧反馈**：每条 B 类缺口选 `补字段` / `前端降级砍交互` / `后续版本再补`。

---



## 0. 阅读说明


| 类型               | 含义                      | 算法动作                       |
| ---------------- | ----------------------- | -------------------------- |
| **A. 字段改名/结构重组** | demo 与契约表达同一语义，键名或块划分不同 | 保持契约；前端 Adapter            |
| **B. 契约缺内容**     | demo 结果交互依赖该数据，契约无对等字段  | **确认是否写入** `#106` **JSON** |


下文 **§0.1 总览树** → **§1–§3 B 类详表** → **§4 A 类汇总**。

---



## 0.1 demo 三页结果数据结构总览（vs 契约）



### 页面 A · 企业评估（technology / business / competitiveness）

**demo 结果运行时模型（前端拼装，非一份落盘 JSON）**：

```text
EvaluationResultRow[]          // 排名主表
  ├─ enterprise { id, name }
  ├─ score                     // 综合分
  └─ quality? EnterpriseQuality
       ├─ coverage             // 覆盖率 %
       ├─ confidence           // high|medium|low|blocked
       ├─ missingMetricIds[]
       └─ hasKeyMissing

RESULT_DIMENSIONS[mode]        // 雷达轴（技术力5 / 商业力6 / 竞争力3）
buildDimensionSeries()         // 每企业 values[]，客户端算
buildRawMetricRows()           // 诊断表原始指标列（客户端算）
setAverage / setLeader         // 竞争力雷达：客户端从 series 聚合
businessTab: diagnosis|trend|benchmark  // 趋势/对标目前空态提示
```

**契约** `#106`：

```text
{ taskId, analysisType, subType, status, reportStatus, meta, enterprises,
  summary{ maxScore, avgScore, ... },
  result{
    technology: radarAxes, radarSeries, ranking, diagnosisRows{innovationCount,rdInvestmentPct,confidence,gapText}, trendAvailable
    business:   operatingIndicators, ranking, tabs, diagnosisRows, revenueTrendAvailable, industryBenchmarkAvailable
    competitiveness: radarAxes, radarSeries, setAverage, setLeader, dimensionRows[]
  },
  weights, dataSource
}
```


| 差异点                    | 类型         | 说明                                                                                                                        |
| ---------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------- |
| `EnterpriseQuality` 整块 | **B**      | demo 排名筛、诊断表「数据可信度」、质量面板全靠它；契约仅 `confidence` 三档、无 coverage/blocked/missingMetricIds                                       |
| 诊断表「原始指标列」             | **B/部分 A** | demo 用 `buildRawMetricRows` 动态列；契约 tech 固定 `innovationCount`+`rdInvestmentPct`，business 用 `operatingIndicators` 中文 key 得分 |
| 领先差距文案                 | **A/前端可算** | demo 客户端用 leader.score 差值拼；契约有 `gapText`/`diagnosisText` 可直接用                                                             |
| 竞争力 setAverage/Leader  | **A**      | demo 客户端聚合；契约已下发                                                                                                          |
| 商业力展示形态                | **A**      | demo：原始指标卡片 + 排名条；契约：`operatingIndicators` 得分对象（非同一形态，需 Adapter）                                                          |
| 趋势/对标序列                | **B**      | demo Tab 存在但无序列体；契约仅 Available 开关                                                                                         |


---



### 页面 B · 风险洞察

**demo 供应链结果**：

```text
{ nodes: RiskGraphNode[], links: RiskGraphLink[] }   // 单一图 fixture，侧栏从图过滤

RiskGraphNode {
  id, name,
  owner: A|B|shared|center,     // ★ 契约无
  relationType | center,          // 契约 → type
  level,                          // 契约 → depth
  centrality,                     // ★ 契约仅 keyNodes.influenceScore
  keyNode,                        // 契约 → isKey
  riskType?, evidence?            // ★ 契约拆到 breakRisks + hasRisk
}
RiskGraphLink { source, target, relationType, strength }  // ★ strength 契约无；links→edges
```

**契约供应链**：`summary` + `graph{nodes,edges,...}` + **独立** `keyNodes[]` + `breakRisks[]`

**demo 痛难点结果**：

```text
PainIssueFixture {
  id, dimension(technology|market|finance|management),
  issue, severity(high|medium|low),
  evidence, cause, bestPractice, direction,
  affectedCount, dataStatus(available|insufficient)
}
// 卡片：从 issues 按 dimension 聚合
// Drawer 行（客户端合成）：{ id, name, status, hitCount }
```

**契约痛点**：`dimensionCards[]` + `issues{title,priority中文,dimension码 tech_rd…,typicalEnterprises[],…}`  
无 `dataStatus`；无受影响企业明细行。

---



### 页面 C · 引育推荐

**demo 一条推荐（招引/培育共用底座 + 分支字段）**：

```text
RecruitBase {
  id, name, industry, index,
  dimensions[{label,value,reviewRef}],
  evidence[{label,summary}],
  coreAdvantages[], keyMetrics[{label,value,unit,metricId}],
  enterpriseTags[], policyDirections[],   // ★ policy 契约无
  riskCredit {                            // ★ 远比契约 count 丰富
    state, recordCount, updatedAt,
    categories[], records[]
  }
}
Attraction +: regionSource, regionGroup, targetFeatures, targetFeatureEvidence, cooperationValue
Cultivation +: scale, developmentBottleneck, bottleneckEvidence, cultivationAdvice, neededSupport
```

**契约**：`rankings[]` + `details[enterpriseCode]{ dimensions[{code,evidenceStatus}], judgmentBasis, keyIndicators{两固定字段}, riskCredit{四计数}, …}`

---



## 1. 风险洞察 · `supply_chain`（B 类缺口）



### 1.1 节点归属 `owner`（双对象分析）


| 项         | 内容                                                           |
| --------- | ------------------------------------------------------------ |
| **契约现状**  | 仅有汇总 `graph.commonNodeCount`；节点无 A/B/shared 归属               |
| **前端依赖**  | 单企业时隐藏 `owner==='B'`；共同节点计数按 `owner==='shared'` 过滤；双中心样例依赖归属 |
| **UI 影响** | 双企业供应链对比时无法区分「仅属 A / 仅属 B / 共有」；共同节点高亮与过滤失效                  |
| **建议**    | 节点增加 `owner: "A"                                             |


**Fixture 实例**（摘自 `demo-ui-topic/.../riskInsightDefinition.ts`，与 lumen fixtures 同构）：

```json
{
  "nodes": [
    {
      "id": "ENT-0001",
      "name": "深芯微集成电路股份有限公司",
      "owner": "center",
      "relationType": "center",
      "level": 0,
      "centrality": 96,
      "keyNode": true
    },
    {
      "id": "ENT-0002",
      "name": "鹏城智算半导体有限公司",
      "owner": "center",
      "relationType": "center",
      "level": 0,
      "centrality": 91,
      "keyNode": true
    },
    {
      "id": "SUP-01",
      "name": "湾区第三代半导体材料有限公司",
      "owner": "shared",
      "relationType": "supplier",
      "level": 1,
      "centrality": 82,
      "keyNode": true,
      "riskType": "单点依赖",
      "evidence": "两家中心企业的共同一级供应节点"
    },
    {
      "id": "CUS-01",
      "name": "南方智能终端制造有限公司",
      "owner": "A",
      "relationType": "customer",
      "level": 1,
      "centrality": 68,
      "keyNode": false
    },
    {
      "id": "PAR-01",
      "name": "粤港澳芯片研发中心",
      "owner": "B",
      "relationType": "partner",
      "level": 1,
      "centrality": 74,
      "keyNode": true,
      "riskType": "节点异常",
      "evidence": "近期合作频次连续两个周期下降"
    }
  ]
}
```

**示意（标注缺口）**：

供应链结果区 · owner / centrality / strength / riskType / id

---



### 1.2 图节点影响力 `centrality`（非仅关键节点）


| 项         | 内容                                                                       |
| --------- | ------------------------------------------------------------------------ |
| **契约现状**  | 影响力仅在 `keyNodes[].influenceScore`；`graph.nodes[]` 无分数字段                  |
| **前端依赖**  | 节点圆大小：`22 + centrality/8`；侧栏「节点影响度」进度条读节点 `centrality`                   |
| **UI 影响** | 非关键节点无法按影响力缩放；若侧栏改绑 `keyNodes` 后，图上仍缺节点级分数                               |
| **建议**    | `nodes[]` 增加 `influenceScore?: number`；或明确「仅关键节点有分、图大小改用 isKey 二值」由产品砍交互 |


**Fixture 字段片段**：

```json
{ "id": "SUP-01", "centrality": 82, "keyNode": true }
```

**示意**：风险洞察→供应链关系→供应链图谱。

---



### 1.3 边强度 `strength`


| 项         | 内容                                                |
| --------- | ------------------------------------------------- |
| **契约现状**  | `edges[]` 仅有 `source` / `target` / `relationType` |
| **前端依赖**  | 线宽：`1 + strength/40`                              |
| **UI 影响** | 强弱关系无法可视化，只能等宽线                                   |
| **建议**    | `edges[].strength?: number`（0–100）；或确认前端固定线宽      |


**Fixture 实例**：

```json
{
  "links": [
    { "source": "SUP-01", "target": "ENT-0001", "relationType": "supplier", "strength": 86 },
    { "source": "SUP-01", "target": "ENT-0002", "relationType": "supplier", "strength": 79 },
    { "source": "ENT-0001", "target": "CUS-01", "relationType": "customer", "strength": 71 }
  ]
}
```

---



### 1.4 风险类型文案 `riskType` + 节点级 `evidence`


| 项         | 内容                                                                                             |
| --------- | ---------------------------------------------------------------------------------------------- |
| **契约现状**  | 节点仅 `hasRisk: boolean`；断链明细在 `breakRisks[]`（`riskLevel` 高/中/低 + `impact` + `suggestion`）       |
| **前端依赖**  | Tag 文案：`单点依赖` / `节点异常` / `路径脆弱`；节点卡片展示 `evidence`                                              |
| **UI 影响** | 风险分类标签无法还原；点选图节点时缺少「风险依据」原文（需跳到侧栏且侧栏无同类枚举）                                                     |
| **建议**    | 二选一：① `breakRisks`/`nodes` 增加 `riskType` 枚举 + `evidence`；② 前端放弃三类标签，统一用 `riskLevel` + `impact` |


**Fixture 实例**：

```json
{
  "id": "SUP-02",
  "name": "新材料精密工艺有限公司",
  "owner": "A",
  "relationType": "supplier",
  "level": 2,
  "centrality": 61,
  "keyNode": false,
  "riskType": "路径脆弱",
  "evidence": "当前样例中与上游关键节点仅有一条连接路径"
}
```

**示意**：「riskType+evidence」与侧栏断链风险 Tag。

---



### 1.5 侧栏与图谱关联 `id`


| 项         | 内容                                                          |
| --------- | ----------------------------------------------------------- |
| **契约现状**  | `keyNodes[]` / `breakRisks[]` 只有 `name`，无节点 `id`            |
| **前端依赖**  | 点击侧栏行 ↔ 高亮图节点（按 `id`）                                       |
| **UI 影响** | 同名节点无法精确联动；只能按 name 模糊匹配                                    |
| **建议**    | `keyNodes[].id` / `breakRisks[].id` 与 `graph.nodes[].id` 对齐 |


**期望补丁形状（相对契约）**：

```json
{
  "keyNodes": [
    {
      "id": "SUP-01",
      "name": "湾区第三代半导体材料有限公司",
      "relationType": "supplier",
      "influenceScore": 82,
      "suggestion": "……",
      "isKey": true
    }
  ],
  "breakRisks": [
    {
      "id": "PAR-01",
      "name": "粤港澳芯片研发中心",
      "riskLevel": "中",
      "impact": "……",
      "suggestion": "……",
      "riskType": "节点异常",
      "evidence": "近期合作频次连续两个周期下降"
    }
  ]
}
```

---



## 2. 风险洞察 · `pain_points`（B 类缺口）



### 2.1 维度「数据不足」态 `dataStatus`


| 项         | 内容                                                                                           |
| --------- | -------------------------------------------------------------------------------------------- |
| **契约现状**  | `dimensionCards[]` 有 `issueCount` / `priority` / `affectedEnterpriseCount`，无「证据不足不判断」显式态     |
| **前端依赖**  | `dataStatus: "available"                                                                     |
| **UI 影响** | 无法区分「0 个问题」与「数据不够不下结论」                                                                       |
| **建议**    | `dimensionCards[].dataStatus` 或 `issues[]` 级 `dataStatus`；或约定 `issueCount=0 && priority 特殊值` |


**Fixture 实例**：

```json
{
  "id": "pain-management-01",
  "dimension": "management",
  "issue": "数据不足，暂不判断",
  "severity": "low",
  "evidence": "管理流程与组织效率相关样例数据未形成稳定时序",
  "cause": "当前证据不足以支持诊断",
  "bestPractice": "补充可追溯的流程时效与组织运行数据",
  "direction": "先完成数据补齐，不在当前任务中生成管理结论",
  "affectedCount": 0,
  "dataStatus": "insufficient"
}
```

**示意（标注缺口）**：

痛难点 · dataStatus 与受影响企业 Drawer

---



## 3. 企业评估 · `enterprise_eval`（B 类缺口）



### 3.1 数据覆盖与可信度块（整块缺失）


| 项         | 内容                                                                              |
| --------- | ------------------------------------------------------------------------------- |
| **契约现状**  | `diagnosisRows[].confidence` 仅为 `"high"                                         |
| **前端依赖**  | 配置/结果前「数据覆盖与可信度」面板：`coverage`%、`confidence`（含 **blocked**）、`missingMetricIds[]` |
| **UI 影响** | 质量预检卡片、按可信度筛排名、缺失 metric 评审展示无法用 `#106` 填充（目前靠本地 fixtures 造数）                   |
| **建议**    | 在结果或独立块增加 per-enterprise quality，例如：                                            |


```json
{
  "dataQuality": [
    {
      "enterpriseCode": "91440300MA5DJWNF8W",
      "enterpriseName": "深芯微集成电路股份有限公司",
      "coverage": 86,
      "confidence": "medium",
      "hasKeyMissing": true,
      "missingMetricIds": ["M_ENT_PATENT_GRANT_COUNT", "M_ENT_RD_INVESTMENT_RATIO"]
    },
    {
      "enterpriseCode": "MOCK-BLOCKED-001",
      "enterpriseName": "样例·数据不足企业",
      "coverage": 42,
      "confidence": "blocked",
      "hasKeyMissing": true,
      "missingMetricIds": ["M_ENT_PATENT_GRANT_COUNT"]
    }
  ]
}
```

**当前 Fixture 类型**（`evaluationDemo.ts` → `EnterpriseQuality`）：

```ts
{
  enterpriseId: string
  coverage: number          // 0–100
  confidence: 'high' | 'medium' | 'low' | 'blocked'
  missingMetricIds: string[]
  hasKeyMissing: boolean
  provenance: 'simulated'
}
```

**示意（标注缺口）**：

综合竞争力评估 · 数据覆盖与可信度

> 说明：`#115` 预检 API 可部分覆盖「任务创建前」质量；**结果 JSON 内仍缺**与排名行绑定的 per-enterprise quality，demo/lumen 结果区筛选依赖该结构。

---



### 3.2 趋势 / 营收 / 对标「有开关无序列」（商业力评估-商业诊断与评估）


| 项         | 内容                                                                                                               |
| --------- | ---------------------------------------------------------------------------------------------------------------- |
| **契约现状**  | `trendAvailable` / `revenueTrendAvailable` / `industryBenchmarkAvailable` + hint 文案；**无**实际时序点或对标明细表             |
| **前端依赖**  | 打开 Tab 后画折线 / 对标表                                                                                                |
| **UI 影响** | 当 `*Available=true` 时仍无数据可绑；目前恒为 false + hint                                                                    |
| **建议**    | Available=true 时附带：`trendSeries[]` / `revenueTrend[]` / `industryBenchmarkRows[]`（字段可另开契约小节）；若本期不做，请书面确认永远 false |


---



## 4. 引育推荐 · `talent_recommend`（B 类缺口）

> lumen 引育结果页尚未全量用 `#106`；下列对照 **demo** `enterpriseRecruitDefinition.ts` 与契约 §3。



### 4.1 风险与信用明细（仅有计数）


| 项           | 内容                                         |
| ----------- | ------------------------------------------ |
| **契约现状**    | `riskCredit`：四类 **count**（司法/失信/异常/处罚）     |
| **Demo 依赖** | 三态 `state`、分类摘要、`records[]` 事件明细（时间、状态、来源） |
| **UI 影响**   | 「企业风险与信用」详情抽屉只能显示数字，无法展示事件列表与「待核验/未检出」语义   |
| **建议**      | 扩展 `riskCredit`，或确认前端只展示四计数                |


**Demo fixture 实例（缩略）**：

```json
{
  "riskCredit": {
    "state": "attention_required",
    "recordCount": 2,
    "updatedAt": "2026-07-21 16:30",
    "categories": [
      {
        "category": "司法涉诉",
        "recordCount": 1,
        "latestEventAt": "2026-05-18",
        "summary": "公开信息样例显示存在合同纠纷相关案件，建议在对接前复核处置进展。"
      },
      {
        "category": "行政处罚",
        "recordCount": 1,
        "latestEventAt": "2025-11-06",
        "summary": "公开信息样例显示存在一项历史行政处罚记录，建议核验整改情况。"
      }
    ],
    "records": [
      {
        "id": "RISK-DEMO-001",
        "category": "司法涉诉",
        "eventSummary": "公开信息样例显示存在合同纠纷相关案件，建议在对接前复核处置进展。",
        "occurredAt": "2026-05-18",
        "currentStatus": "审理中（样例）",
        "sourceName": "公开信息样例",
        "updatedAt": "2026-07-21 16:30"
      }
    ]
  }
}
```

**示意（标注缺口）**：

引育 · 风险与信用明细

---



### 4.2 政策方向 `policyDirections`


| 项         | 内容                                               |
| --------- | ------------------------------------------------ |
| **契约现状**  | **无**                                            |
| **Demo**  | `policyDirections: string[]`，如 `["产业升级","科技创新"]` |
| **UI 影响** | 政策标签条无数据源                                        |
| **建议**    | `details[].policyDirections?: string[]` 或砍掉该展示   |


---



### 4.3 招引 `regionGroup` / 培育 `bottleneckEvidence`


| 项         | 内容                                                                                   |
| --------- | ------------------------------------------------------------------------------------ |
| **契约现状**  | 招引仅 `geographicSource`；培育有 `developmentBottleneck` / `cultivationSuggestion`，无独立瓶颈依据 |
| **Demo**  | `regionGroup`（长三角/京津冀…）；`bottleneckEvidence` 与瓶颈摘要分离                                 |
| **UI 影响** | 区域分组筛选/展示弱化；瓶颈「结论 vs 依据」无法分层                                                         |
| **建议**    | 可选补字段；或前端合并文案降级                                                                      |


**Demo 片段**：

```json
{
  "regionSource": "江苏省·苏州市",
  "regionGroup": "长三角",
  "developmentBottleneck": "行业场景验证不足，产品规模复制仍受算力与示范渠道约束。",
  "bottleneckEvidence": "现有订单集中于少量制造与政务客户，跨行业复用案例仍需补强。"
}
```

---



### 4.4 关键指标带 `metricId`（评审血缘）


| 项         | 内容                                                                  |
| --------- | ------------------------------------------------------------------- |
| **契约现状**  | `keyIndicators` 固定 `validPatentCount` / `latestAnnualRevenueYiYuan` |
| **Demo**  | `keyMetrics: { label, value, unit, metricId }[]`                    |
| **UI 影响** | MetricSpecCard / 血缘挂载不便扩展第三指标                                       |
| **建议**    | 数组化指标并带 `metricId`，或维持两固定字段并声明扩展冻结                                  |


---



## 5. A 类汇总（改名/重组，算法不用处理）

前端 Adapter 处理即可，**算法可维持现契约**：


| 模块    | Fixtures / Demo                                      | 契约                                                                |
| ----- | ---------------------------------------------------- | ----------------------------------------------------------------- |
| 供应链图  | `level` / `relationType` / `links` / `keyNode`       | `depth` / `type` / `edges` / `isKey`                              |
| 供应链侧栏 | 从图节点过滤                                               | 独立 `keyNodes[]` / `breakRisks[]`                                  |
| 痛点维度码 | `technology` / `market` / `finance` / `management`   | `tech_rd` / `market_expand` / `financing` / `management`          |
| 痛点字段  | `issue` / `severity` / `direction` / `affectedCount` | `title` / `priority`(中文) / `solution` / `affectedEnterpriseCount` |
| 评估排名  | fixtures 本地算分                                        | `result.ranking` / `radarSeries` / `operatingIndicators` 等        |
| 引育列表  | `index` / `targetFeatures` / …                       | `recommendationScore` / `targetTraits` / `details[code]`          |


---

## 6. 源文件索引


| 用途        | 路径                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------ |
| 契约        | `API-ENT-ANALYSIS-RESULT-CONTRACT.md`                                                                                    |
| demo 评估结果 | `demo-ui-topic/.../EnterpriseEvaluationResultWorkspace.tsx` · `enterpriseEvaluationResultModel.ts` · `EnterpriseQuality` |
| demo 风险结果 | `RiskInsightSupplyResult.tsx` · `RiskInsightPainResult.tsx` · `riskInsightDefinition.ts`                                 |
| demo 引育结果 | `EnterpriseRecommendation.tsx` · `enterpriseRecruitDefinition.ts`                                                        |
|           |                                                                                                                          |


---

