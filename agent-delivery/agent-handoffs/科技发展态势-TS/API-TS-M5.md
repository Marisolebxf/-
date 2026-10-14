# API · 科技发展态势（TS）· M5 湾区创新监测（接口契约草案）

> **任务**：`BE-TS-CONTRACT-02`（M2–M9 接口契约定义，按批冻结）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。本模块属**批 3**，批 3 开工前冻结。
> **范围**：仅 M5（湾区创新监测）。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `TS-模块开发规划与任务拆分.md` §4 M5（FE-TS-05a~05d） |
| 页面入口 / 数据集构建 | `demo-ui-science/src/App.jsx` L11700–L11770 `BayAreaInnovationMonitor` |
| 数据集构建器 | `demo-ui-science/src/bayAreaInnovationMonitor.js` L330–L371 `buildBayAreaInnovationMonitorDataset` |
| 能力项 / 时间轴 | `bayAreaInnovationMonitor.js` L8–L35 `bayAreaInnovationMonitorCapabilities` / L36–L155 `bayAreaInnovationMonitorTimeline` |
| 图例（成果类型） | `bayAreaInnovationMonitor.js` L156–L166 `bayAreaInnovationLegend` |
| 地图配置 | `bayAreaInnovationMonitor.js` L168–L179 `bayAreaInnovationMapConfig` |
| SWOT 四象限 | `bayAreaInnovationMonitor.js` L181–L186 `bayAreaSwotItems` |
| 11 城枚举 | `demo-ui-science/src/data.js` L220–L248（粤港澳大湾区城市清单） |

---

## 1. 模块约定（增量）

全局约定继承 `API-TS-M1.md` §1 / §4 / §5。

| 项 | 约定 |
|---|---|
| 服务内路径前缀 | `/v1/situation/bay-innovation/**`（网关对外 `/display/v1/situation/bay-innovation/**`） |
| 地域范围 | 固定粤港澳大湾区 11 城（§2.1）；地图中心 `[22.72, 113.72]` zoom 8.35（`bayAreaInnovationMapConfig`） |
| 读写面 | 全只读 ADS；无带写面 |

## 2. 枚举字典（前端只读消费）

### 2.1 湾区城市 `bay_city`（11 城，逐字）
`data.js` L220–L248：`shenzhen`深圳 · `guangzhou`广州 · `zhuhai`珠海 · `foshan`佛山 · `huizhou`惠州 · `dongguan`东莞 · `zhongshan`中山 · `jiangmen`江门 · `zhaoqing`肇庆 · `hongkong`香港 · `macau`澳门。

### 2.2 成果类型 `result_type`（5 类，逐字）
`bayAreaInnovationLegend.resultTypes`（L159–L165）：`paper`论文成果 · `patent`专利成果 · `project`协同项目 · `institution`创新载体 · `enterprise`创新企业。

### 2.3 SWOT 象限 `swot_key`（4 类，逐字）
`bayAreaSwotItems`（L181–L186）：`strength`优势 · `weakness`短板 · `opportunity`机会 · `threat`威胁。

### 2.4 能力项 `capability_key`（3+ 类）
`bayAreaInnovationMonitorCapabilities`（L8–L25）：`capability-index`创新能力指数 · `swot-analysis`SWOT 分析 · `indicator-data`指标数据（等，全量清单随字典接口下发）。

### 2.5 趋势方向 `direction`（2 类）
`rise`上行 · `fall`下行（`buildMetrics` L232–L236）。

## 3. 接口清单（4 类）

### 3.1 `POST /v1/situation/bay-innovation/achievements/search` — 湾区成果落点（11 城 67 点）

**用途**（规划 M5-BE ①）：11 城成果落点 + 城市/类型/领域/时间筛选（FE-TS-05a 成果地图）。

```json
{
  "cities": ["shenzhen", "guangzhou"],
  "result_types": ["patent", "project"],
  "field_scope": "CL-FUT-05",
  "start_year": "2020", "end_year": "2026",
  "keyword": "",
  "page": 1, "size": 100
}
```

```json
{
  "code": 0,
  "data": {
    "total": 67,
    "records": [
      { "achievement_id": "bay-001", "name": "深圳智能机器人专利群", "result_type": "patent",
        "city": "shenzhen", "city_label": "深圳", "institution": "…", "field_key": "intelligent-robotics",
        "year": "2026", "score": 94, "lng": 114.0579, "lat": 22.5431,
        "indicator": "专利授权 18400 件", "summary": "…", "metric_id": "Q0xx" }
    ],
    "map_points": [ { "achievement_id": "bay-001", "lng": 114.0579, "lat": 22.5431, "result_type": "patent", "city": "shenzhen" } ],
    "city_counts": [ { "city": "shenzhen", "city_label": "深圳", "count": 18 } ],
    "filter_echo": { "cities": ["shenzhen", "guangzhou"] },
    "metric_ids": ["Q0xx"]
  }
}
```

边界：记录字段对齐 `bayAreaInnovationMonitor.js` baseRecords（`filterRecords` L210–L226 的 `name/city/institution/fieldKey/year/summary` + `indicator`）；「67 点」为演示样本量，契约不限量，分页上限 100。

### 3.2 `GET /v1/situation/bay-innovation/capability` — 创新能力（四维 + 历史 + 构成）

**用途**（规划 M5-BE ②）：四维指数 + 2020–2025 历史 + 构成项 + 计算方法说明 + 城市雷达（FE-TS-05b）。

| Query | 说明 |
|---|---|
| `cities` | 可选，默认 11 城 |
| `start_year` / `end_year` | 默认 2020–2025 |

```json
{
  "code": 0,
  "data": {
    "dimensions": [
      { "key": "innovation_input",  "label": "创新投入", "score": 86, "weight": 25, "metric_id": "Q0xx" },
      { "key": "innovation_output", "label": "创新产出", "score": 89, "weight": 25, "metric_id": "Q0xx" },
      { "key": "innovation_env",    "label": "创新环境", "score": 84, "weight": 25, "metric_id": "Q0xx" },
      { "key": "industry_collab",   "label": "产业协同", "score": 82, "weight": 25, "metric_id": "Q0xx" }
    ],
    "history": { "years": ["2020","2021","2022","2023","2024","2025"],
                 "series": [ { "key": "innovation_input", "label": "创新投入", "values": [70,74,78,81,84,86] } ] },
    "components": [ { "key": "rd_expenditure", "label": "研发投入", "value": 920, "unit": "亿元", "dimension_key": "innovation_input" } ],
    "method_note": "…（计算方法说明，真源待算法侧）",
    "city_radar": [ { "city": "shenzhen", "city_label": "深圳", "values": [92, 94, 90, 88] } ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：四维 key 命名与 M4 §2.8 五维**不强行复用**（湾区四维口径独立，U2）；构成项 `components` 示例取自 `bayAreaInnovationMonitorTimeline` 各年 `indicator`（如 L79「研发投入 920 亿元」）；`method_note` 无真源时返 `null` + 前端不渲染（不补假）。

### 3.3 `GET /v1/situation/bay-innovation/swot` — SWOT 四象限 + 因素

**用途**（规划 M5-BE ③）：SWOT 四象限全文 + 因素，默认短板维 + 诊断（FE-TS-05c）。

```json
{
  "code": 0,
  "data": {
    "items": [
      { "swot_key": "strength",   "label": "优势", "title": "资源与产业链密度高",          "detail": "深圳企业转化、广州临床资源、香港国际资金与规则接口形成互补。", "factors": [] },
      { "swot_key": "weakness",   "label": "短板", "title": "跨城数据与标准衔接不足",      "detail": "部分指标口径、技术合同和成果转化链路仍存在跨域协同成本。",   "factors": [] },
      { "swot_key": "opportunity","label": "机会", "title": "低空经济和具身智能进入场景窗口","detail": "应用场景和产业链基础共同支撑重点成果快速验证。",           "factors": [] },
      { "swot_key": "threat",     "label": "威胁", "title": "高端人才与关键环节竞争加剧",   "detail": "外部城市群和国际创新节点对资本、人才和核心技术持续分流。",     "factors": [] }
    ],
    "default_focus": "weakness",
    "diagnosis": null
  }
}
```

字段逐字对齐 `bayAreaSwotItems`（L181–L186）。边界：`factors`（因素归因，ALGO 参考）与 `diagnosis`（短板诊断）真源待算法侧；无真源时 `factors=[]` / `diagnosis=null`，不伪造（M1 §5）。

### 3.4 `GET /v1/situation/bay-innovation/indicators` — 指标数据（6 指标 + 11 城构成 + 口径）

**用途**（规划 M5-BE ④）：6 指标 + 11 城构成 + 口径说明（FE-TS-05d）。

```json
{
  "code": 0,
  "data": {
    "indicators": [
      { "key": "innovation_output_value", "label": "创新产值", "value": 3260, "unit": "亿元",
        "caliber": "…（口径说明，必填）",
        "city_breakdown": [ { "city": "shenzhen", "city_label": "深圳", "value": 1180 } ],
        "metric_id": "Q0xx" },
      { "key": "rd_investment",          "label": "研发投入", "value": 920,  "unit": "亿元", "caliber": "…", "city_breakdown": [], "metric_id": "Q0xx" },
      { "key": "tech_contract",          "label": "技术合同交易额", "value": 780, "unit": "亿元", "caliber": "…", "city_breakdown": [], "metric_id": "Q0xx" },
      { "key": "patent_grant",           "label": "专利授权", "value": 18400, "unit": "件", "caliber": "…", "city_breakdown": [], "metric_id": "Q0xx" },
      { "key": "paper_publish",          "label": "论文发表", "value": 12600, "unit": "篇", "caliber": "…", "city_breakdown": [], "metric_id": "Q0xx" },
      { "key": "cross_city_project",     "label": "跨境/跨城项目", "value": 128, "unit": "项", "caliber": "…", "city_breakdown": [], "metric_id": "Q0xx" }
    ],
    "caliber_note": "指标口径：创新产值、创新投入、技术合同交易额、专利及论文数量",
    "metric_ids": ["Q0xx"]
  }
}
```

口径真源：`buildBayAreaInnovationMonitorDetail`（L396）「指标口径」行。边界：6 指标清单为建议集（按 demo indicator 文案归纳），**最终清单与 metric_id 登记随批 3 评审**（U3）；`caliber` 必填（D9 诚实性，无口径不上线）。

## 4. 数据需求与存储建议（Mock 先行 D7）

| # | 域 | 建议表名 | 关键字段 | 消费接口 | 备注 |
|---|---|---|---|---|---|
| 1 | 湾区成果 | `ts_bay_achievement` | `achievement_id, name, result_type, city, institution, field_key, year, score, lng, lat, indicator, summary, metric_id` | §3.1 | 11 城 |
| 2 | 创新能力 | `ts_bay_capability` | `dimension_key, city, year, score, weight, metric_id, calc_batch_id` | §3.2 | 算法产物 |
| 3 | SWOT | `ts_bay_swot`（内容配置） | `swot_key, label, title, detail, factors JSON, updated_at` | §3.3 | 文案由数据/算法侧维护，禁前端硬编码 |
| 4 | 指标数据 | `ts_bay_indicator` | `indicator_key, city, year, value, unit, caliber, metric_id` | §3.4 | caliber 必填 |

## 5. 未决项

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | 香港/澳门数据可得性与展示口径 | M0 + 数据侧 |
| U2 | 湾区四维 key 与 M4 五维是否统一命名体系 | M0 拍板 |
| U3 | 6 指标最终清单与 `metric_id` 登记 | `ALL-TS-D9`，随批 3 评审 |
| U4 | SWOT 因素归因（factors）算法产物上线时点 | M0 + 算法侧 |

## 6. 自检（冻结前）

- [ ] 11 城枚举与 `data.js` L220–L248 逐字一致
- [ ] `result_type` 五类与 `bayAreaInnovationLegend` L159–L165 逐字一致
- [ ] SWOT 四象限文案与 `bayAreaSwotItems` L181–L186 逐字一致；`factors`/`diagnosis` 无真源返空不补假
- [ ] 指标 `caliber` 必填；无口径不上线
- [ ] 缺数 / 空态与 M1 §5 一致

## 7. 会签记录（批 3 评审待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |
