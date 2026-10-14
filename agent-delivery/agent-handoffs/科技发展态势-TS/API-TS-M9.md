# API · 科技发展态势（TS）· M9 科技发展规划（接口契约草案）

> **任务**：`BE-TS-CONTRACT-02`（M2–M9 接口契约定义，按批冻结）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。本模块属**批 4**，模块最大（规划 FE ~5 工日），批 4 开工前冻结。
> **范围**：仅 M9（科技发展规划 · demo `TechDevelopmentPlan`）。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `TS-模块开发规划与任务拆分.md` §4 M9（FE-TS-09a~09c） |
| 能力项四分类 | `demo-ui-science/src/techDevelopmentPlan.js` L7–L28 `techDevelopmentPlanCapabilities` |
| 研判演进时间轴 | `techDevelopmentPlan.js` L30–L44 `techDevelopmentPlanTimeline` |
| 规划证据图层图例 | `techDevelopmentPlan.js` L197–L207 `techDevelopmentPlanLegend.resultTypes` |
| 地图配置 | `techDevelopmentPlan.js` L209–L220 `techDevelopmentPlanMapConfig` |
| 规划图谱 | `techDevelopmentPlan.js` L222–L239 `techDevelopmentPlanGraph` |
| 规划记录字段 | `techDevelopmentPlan.js` L46 起 `planRecords` |
| 汇总指标 | `techDevelopmentPlan.js` L290–L302 `buildMetrics` |
| 规划维度权重 | `techDevelopmentPlan.js` L304 起 `buildPlanDimensions` |
| 方向预警（六源 / 三级 / 报告产物） | `demo-ui-science/src/TechDevelopmentPlan.tsx` L383–L435 `directionMonitorSources` / `DirectionMonitorItem` / `directionWarningMeta` |
| 热点技术（8 项） | `TechDevelopmentPlan.tsx` L372–L381 `hotTechData` |
| 人才流动 | `TechDevelopmentPlan.tsx` L568–L603 / L747 / L1638–L1717 `talentFlowData` / `talentFlowTypeOptions` |
| 需求规格说明书 | `demo-ui-science/docs/科技发展规划_需求规格说明书.md` |

---

## 1. 模块约定（增量）

全局约定继承 `API-TS-M1.md` §1 / §4 / §5。

| 项 | 约定 |
|---|---|
| 服务内路径前缀 | `/v1/situation/planning/**`（网关对外 `/display/v1/situation/planning/**`） |
| 子功能 | 综合发展规划（09a）/ 重点领域规划（09b）/ 研究领域分析（09c），能力键 §2.1 |
| 读写面 | 业务数据只读 ADS；**带写面** = §3.6 资源推送订阅设置（app_user 家族） |
| 报告产物 | 方向预警 / 研究分析均产 **Word（.doc）报告**（demo `downloadHtmlAsWord` L1817）；服务端生成 + 短时签名 URL 下载（复用 M1 §3.8 导出任务中心机制，不另造下载通道） |

## 2. 枚举字典（前端只读消费）

### 2.1 能力项 `capability_key`（4 类，逐字）
`techDevelopmentPlanCapabilities`（L7–L28）：`comprehensive-plan`综合发展规划 · `key-area-plan`重点领域规划 · `research-analysis`研究领域分析 · `report-export`报告与导出。

### 2.2 证据图层类型 `result_type`（5 类，逐字）
`techDevelopmentPlanLegend.resultTypes`（L200–L206）：`hotspot`热点技术 · `space`空间布局 · `talent`人才流动 · `report`报告资源 · `warning`方向预警（各带色值，后端下发）。

### 2.3 预警来源 `warning_source`（6 源，逐字）
`directionMonitorSources`（L383–L390）：`paper`论文 · `patent`专利 · `project`项目 · `talent`人才 · `industry`产业 · `policy`政策。

### 2.4 预警等级 `warning_level`（3 级，逐字含标签/色值）
`directionWarningMeta`（L412–L416）：`high`高预警 `#f53f3f` · `medium`关注 `#ff7d00` · `watch`观察 `#165dff`。

### 2.5 热度趋势 `hot_trend`（3 类，逐字）
`hotTechData`（L372–L381）：`hot`热点 · `rising`上升 · `stable`平稳。

### 2.6 人才流动类型 `flow_type`（3 类，逐字）
`talentFlowTypeOptions`（L576/L747）：`学术→产业` · `产业→学术` · `预警流动`（`全部` 为筛选器特例，不作存储值）。

### 2.7 研究领域等级 `research_grade`（4 档）
规划 M9-BE ⑧「四档等级」；demo 需求规格说明书 §研究分析。等级逐字标签由后端字典下发（U3）。

### 2.8 概览时间窗 `overview_time_range`（3 类，逐字）
`overviewTimeRangeSourceNote`（L364–L368）：`3m`近3个月 · `6m`近6个月 · `12m`近12个月。

## 3. 接口清单（8 类）

### 3.1 `GET /v1/situation/planning/direction-warnings` — 方向预警（6 源分 + 预警卡 + 报告产物）

**用途**（规划 M9-BE ①）：FE-TS-09a 方向预警区。

| Query | 说明 |
|---|---|
| `field` | 技术领域过滤（`directionMonitorItems` 按 field 过滤，L1327–L1329） |
| `warning_level` | 可选 |

```json
{
  "code": 0,
  "data": {
    "source_averages": [
      { "source": "paper",    "label": "论文", "avg": 88.5 },
      { "source": "patent",   "label": "专利", "avg": 85.2 },
      { "source": "project",  "label": "项目", "avg": 83.0 },
      { "source": "talent",   "label": "人才", "avg": 81.6 },
      { "source": "industry", "label": "产业", "avg": 87.4 },
      { "source": "policy",   "label": "政策", "avg": 79.8 }
    ],
    "items": [
      { "warning_id": "embodied-ai", "name": "具身智能与工业协作机器人", "field": "具身智能",
        "warning_level": "high", "level_label": "高预警",
        "signal": "六源同步升温", "summary": "论文、专利与项目近12个月共振上升，产业落地加快，人才向企业集中，专项政策窗口已打开。",
        "updated_at": "2026-08-17 08:30",
        "sources": {
          "paper":    { "score": 92, "delta": "+18%", "note": "具身智能顶会论文连续三季放量" },
          "patent":   { "score": 88, "delta": "+21%", "note": "运动控制与力觉专利族扩容" },
          "project":  { "score": 86, "delta": "+16%", "note": "重点专项与联合攻关立项加快" },
          "talent":   { "score": 84, "delta": "+12%", "note": "高校向龙头企业净流入上升" },
          "industry": { "score": 90, "delta": "+19%", "note": "产线试点与场景订单同步增加" },
          "policy":   { "score": 81, "delta": "+9%",  "note": "机器人与智能制造专项连续出台" }
        },
        "metric_id": "Q0xx" }
    ],
    "report_meta": { "title": "潜在科技发展方向预警报告", "generated_at": "2026-10-14 08:00", "high_count": 1, "medium_count": 2, "watch_count": 3 },
    "metric_ids": ["Q0xx"]
  }
}
```

字段逐字对齐 `DirectionMonitorItem`（L401–L435）与 `directionMonitorReport`（L1339–L1378、L3462–L3477）。边界：
- 六源均分 `source_averages` 由服务端按当前可见 `items` 计算（对齐 demo L1331–L1337），前端不自算。
- 报告下载走 M1 §3.8 导出任务中心（`content_key=planning-direction-warning`），不单独造下载接口。
- `delta` 字符串百分比（demo 口径），数值化待 M0（同 M6 U2 族，U4）。

### 3.2 `GET /v1/situation/planning/hot-technologies` — 热点技术（8 项 + 热度序列 + 空间分布 + 口径）

**用途**（规划 M9-BE ②）：FE-TS-09a 热点技术区。

```json
{
  "code": 0,
  "data": {
    "items": [
      { "tech_id": "1", "name": "人工智能大模型", "category": "AI",
        "heat": 98, "growth": 45.2, "hot_trend": "hot",
        "patents": 12580, "papers": 3420,
        "description": "大语言模型技术持续突破，多模态融合成为新方向",
        "heat_series": [ { "year": "2024", "heat": 82 }, { "year": "2025", "heat": 91 }, { "year": "2026", "heat": 98 } ],
        "spatial_distribution": [ { "region": "深圳", "heat": 96, "lng": 114.0579, "lat": 22.5431 } ],
        "metric_id": "Q0xx" }
    ],
    "caliber_note": "热度 = 论文 40% / 专利 30% / 项目 20% / 资讯 10%（口径待 M0 定稿，U5）",
    "metric_ids": ["Q0xx"]
  }
}
```

字段逐字对齐 `hotTechData`（L372–L381，8 项：人工智能大模型 / 量子计算 / 合成生物学 / 固态电池 / 脑机接口 / 6G通信 / 人形机器人 / 可控核聚变）。边界：`caliber_note` 必填（D9 诚实性）；热度构成权重 40/30/20/10 为规划口径（ALGO 参考），**待 M0 定稿**（U5）。

### 3.3 `GET /v1/situation/planning/tracking` — 动态跟踪（时间/空间切换）

**用途**（规划 M9-BE ③）：FE-TS-09a 动态跟踪。

```json
{
  "code": 0,
  "data": {
    "timeline": { "title": "科技发展规划研判演进", "current_year": "2026", "range_label": "2020-2026",
                  "years": ["2020","2021","2022","2023","2024","2025","2026"],
                  "events": [ { "date": "2020-05", "region": "全球", "text": "综合发展规划接入全球热点技术、学术论文趋势和产业动态样本" } ] },
    "spatial": { "map_center": [31.5, 113.5], "zoom": 4.7,
                 "points": [ { "result_type": "hotspot", "name": "…", "lng": 114.06, "lat": 22.54, "score": 94 } ] },
    "metric_ids": []
  }
}
```

字段对齐 `techDevelopmentPlanTimeline`（L30–L44）与 `techDevelopmentPlanMapConfig`（L209–L220）。`time_mode=year|month` / `space_mode=global|gba|shenzhen` 切换参数由公共筛选承载。

### 3.4 `GET /v1/situation/planning/local-advantage` — 本地优势对比（领域/能力/产出 vs 全球）

**用途**（规划 M9-BE ④）：FE-TS-09a 本地优势区。

```json
{
  "code": 0,
  "data": {
    "base_region": "深圳",
    "compare_to": "全球",
    "dimensions": [
      { "key": "field",    "label": "领域", "local": 88, "global_avg": 76, "detail": "…" },
      { "key": "capability","label": "能力", "local": 91, "global_avg": 80, "detail": "…" },
      { "key": "output",   "label": "产出", "local": 93, "global_avg": 82, "detail": "…" }
    ],
    "reference_stats": { "global": { "hotspots": 72, "carriers": 1240, "capacity": 215.4, "source": "全球公开数据库（示例抽样）" } },
    "metric_ids": ["Q0xx"]
  }
}
```

`reference_stats` 对齐 demo L361–L362（全球对比样本）。边界：`source` 必返（样本口径诚实标注）；「示例抽样」字样在 Mock 态保留，正式态须换真源标注。

### 3.5 `GET /v1/situation/planning/talent-flow` — 人才流动（机构净流入 + 名单）

**用途**（规划 M9-BE ⑤）：FE-TS-09a 人才流动区。

| Query | 说明 |
|---|---|
| `flow_type` | §2.6（`学术→产业` / `产业→学术` / `预警流动`）；缺省全量 |
| `risk_level` | 可选：`warning`（demo L1665：`riskLevel='warning' or warning=true`） |

```json
{
  "code": 0,
  "data": {
    "stats": { "net_inflow": 128, "warning_count": 6, "academic_to_industry": 84, "industry_to_academic": 44 },
    "institution_flows": [
      { "institution": "华为", "net_inflow": 36, "direction": "in", "risk_level": null }
    ],
    "records": [
      { "flow_id": "tf-001", "from": "清华大学", "to": "华为", "flow_type": "学术→产业",
        "person_count": 12, "risk_level": "warning", "warning": true, "field": "人工智能", "updated_at": "2026-09-30" }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

字段对齐 `talentFlowData`（L568 起 `TalentFlow`）与筛选逻辑（L1638–L1717）。边界：`预警流动` 筛选 = `risk_level=warning`（demo L1665 语义）；`person_count` 涉及个人信息，**只聚合计数，不返个人明细**（合规，U6）。

### 3.6 资源推送（清单 + 订阅设置，带写面）

**用途**（规划 M9-BE ⑥）：FE-TS-09a 资源推送区。

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/v1/situation/planning/resource-push` | 推送资源清单（报告/项目/政策/载体，按订阅过滤） |
| `GET` / `PUT` | `/v1/situation/planning/resource-push/subscriptions` | 订阅设置（资源类型 / 领域 / 频率），读写 app_user 家族 |

```json
{
  "code": 0,
  "data": {
    "records": [
      { "resource_id": "res-001", "resource_type": "report", "title": "合成生物重点领域布局周报",
        "field": "合成生物", "pushed_at": "2026-10-13T08:00:00+08:00", "is_read": false }
    ],
    "subscriptions": { "resource_types": ["report", "policy"], "fields": ["合成生物"], "frequency": "weekly" }
  }
}
```

边界：`frequency` 枚举 `realtime` / `daily` / `weekly`（U7）；已读状态复用 M4 §3.4 已读模式（按用户隔离）。

### 3.7 `GET /v1/situation/planning/key-areas` — 重点领域（3 集群 + 22 载体 + 竞争力五维 + 土地 + 3 方案）

**用途**（规划 M9-BE ⑦）：FE-TS-09b 重点领域规划。

```json
{
  "code": 0,
  "data": {
    "clusters": [
      { "cluster_id": "CL-FUT-05", "cluster_name": "未来智能终端集群",
        "competitiveness": [ { "dimension": "技术", "score": 90 }, { "dimension": "产业", "score": 88 }, { "dimension": "空间", "score": 85 }, { "dimension": "人才", "score": 86 }, { "dimension": "政策", "score": 84 } ],
        "carriers": [ { "carrier_id": "C-01", "name": "…", "lng": 113.93, "lat": 22.53, "land_benefit": { "plot_ratio": 2.8, "output_per_mu": 1200 } } ],
        "plans": [ { "plan_id": "PLAN-A", "name": "方案 A", "summary": "…" } ],
        "metric_id": "Q0xx" }
    ],
    "carrier_total": 22,
    "metric_ids": ["Q0xx"]
  }
}
```

边界：3 集群 / 22 载体为 demo 口径，正式清单后端下发；竞争力五维 key 定稿 U8；`land_benefit`（土地效益：容积率 / 亩均产出）字段名待数据侧定名（U8）；`plans` 固定 3 方案为产品定义。

### 3.8 `GET /v1/situation/planning/research-analysis` — 研究分析（四档等级 + 图谱 + 重叠度 + 6 企竞争 + 情报 + 报告）

**用途**（规划 M9-BE ⑧）：FE-TS-09c 研究领域分析。

```json
{
  "code": 0,
  "data": {
    "fields": [
      { "field_key": "synthetic-biology", "field_label": "合成生物", "research_grade": "leading", "grade_label": "领先",
        "overlap_score": 0.68, "metric_id": "Q0xx" }
    ],
    "graph": { "nodes": [ { "id": "topic", "label": "规划主题", "type": "主题" } ],
               "edges": [ { "id": "e1", "source": "topic", "target": "tech", "label": "热点捕捉" } ] },
    "competing_enterprises": [
      { "enterprise_id": "ENT-001", "name": "华大基因", "field": "合成生物", "intelligence_level": "high", "score": 91, "metric_id": "Q0xx" }
    ],
    "intelligence_report": { "title": "合成生物竞争情报报告", "generated_at": "2026-10-14 08:00", "report_ref": "EXPORT-JOB-REF" },
    "metric_ids": ["Q0xx"]
  }
}
```

边界：
- `graph` 结构对齐 `techDevelopmentPlanGraph`（L222–L239，6 节点 6 边演示骨架）；正式图谱数据量大时改走 M2 §3.1 图谱接口，**不在本接口内嵌全量图**（U9）。
- `intelligence_level`（竞争情报分级）为算法产物；报告产物走 M1 §3.8 导出任务中心（`report_ref` 引用 `job_id`）。
- 重叠度 `overlap_score` 口径（ALGO：重叠度分析）待算法侧登记 `metric_id`。

## 4. 数据需求与存储建议（Mock 先行 D7）

| # | 域 | 建议表名 | 关键字段 | 消费接口 | 备注 |
|---|---|---|---|---|---|
| 1 | 规划记录 | `ts_plan_record` | `id, name, field_key, region, type, capability_key, year, score, heat, growth, potential, layout, risk, evidence, recommendation, summary` | §3.3/§3.4 聚合 | 对齐 `planRecords` L46 起 |
| 2 | 方向预警 | `ts_plan_direction_warning` | `warning_id, name, field, warning_level, signal, summary, sources JSON, updated_at, metric_id` | §3.1 | 六源分 JSON |
| 3 | 热点技术 | `ts_plan_hot_tech` | `tech_id, name, category, heat, growth, hot_trend, patents, papers, description, metric_id`；热度序列 `ts_plan_hot_tech_series` | §3.2 | 口径 U5 |
| 4 | 人才流动 | `ts_plan_talent_flow` | `flow_id, from_org, to_org, flow_type, person_count, risk_level, field, updated_at` | §3.5 | 聚合计数，不存个人明细 |
| 5 | 重点领域 | `ts_plan_key_area` / `ts_plan_key_area_carrier` | `cluster_id, competitiveness JSON, land_benefit JSON` | §3.7 | 22 载体 |
| 6 | 研究分析 | `ts_plan_research_field` / `ts_plan_compete_intel` | `field_key, research_grade, overlap_score, intelligence_level, score, metric_id` | §3.8 | 算法产物 |
| 7 | 推送订阅 | app_user 家族 | `user_id, subscriptions JSON` | §3.6 | 带写面 |

## 5. 未决项

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | M9 子功能拆分粒度：是否按 09a/09b/09c 拆三个独立服务路由 | M0 拍板 |
| U2 | 规划图谱正式数据量与 M2 图谱接口复用边界 | M0 + 架构 |
| U3 | `research_grade` 四档逐字标签与阈值 | M0 + 算法侧 |
| U4 | 六源 `delta` 字符串数值化口径 | M0 + 数据侧 |
| U5 | 热点热度构成权重（40/30/20/10）定稿 | `ALL-TS-D9`，随批 4 评审 |
| U6 | 人才流动个人信息合规边界（只聚合计数是否足够） | M0 + 法务/合规 |
| U7 | 推送频率枚举（realtime/daily/weekly） | M0 产品侧 |
| U8 | 竞争力五维 key 与 `land_benefit` 字段定名 | M0 + 数据侧 |
| U9 | 研究分析图谱数据量超阈值时的降级方案（嵌套 vs 跳转 M2） | M0 拍板 |

## 6. 自检（冻结前）

- [ ] 能力项四类 / 图例五类 / 预警六源 / 预警三级 / 热度三趋势与 demo 逐字一致
- [ ] 方向预警 `sources` 六源结构与 `DirectionMonitorItem` 逐字一致；六源均分服务端计算
- [ ] 报告产物统一走 M1 §3.8 导出任务中心，不另造下载通道
- [ ] 人才流动只返聚合计数，不返个人明细
- [ ] 演示「示例抽样」标注保留至正式态替换真源；缺数 / 空态与 M1 §5 一致

## 7. 会签记录（批 4 评审待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |
