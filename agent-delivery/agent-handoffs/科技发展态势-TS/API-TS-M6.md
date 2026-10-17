# API · 科技发展态势（TS）· M6 深圳创新监测（接口契约草案）

> **任务**：`BE-TS-CONTRACT-02`（M2–M9 接口契约定义，按批冻结）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。本模块属**批 3**，批 3 开工前冻结。
> **范围**：仅 M6（深圳创新监测）。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `TS-模块开发规划与任务拆分.md` §4 M6（FE-TS-06a~06d） |
| 载体基础数据（60 条字段） | `demo-ui-science/src/shenzhenInnovationMonitor.js` L57–L179 `baseRecords` |
| 载体筛选逻辑 | `shenzhenInnovationMonitor.js` L246–L260 |
| 核心指标与趋势序列 | `shenzhenInnovationMonitor.js` L268–L307 `buildMetrics` / `buildTrendSeries` |
| 领域分布与城市对比 | `shenzhenInnovationMonitor.js` L335–L364 `buildFieldDistribution` / `buildCityComparison` |
| 数据集导出入口 | `shenzhenInnovationMonitor.js` L402–L443 `buildShenzhenInnovationMonitorDataset` |
| 运行监测时间轴 | `shenzhenInnovationMonitor.js` L41–L55 `shenzhenInnovationMonitorTimeline` |
| 页面 Tab / 能力枚举 | `demo-ui-science/src/App.jsx` L11809–L11825 |

---

## 1. 模块约定（增量）

全局约定继承 `API-TS-M1.md` §1 / §4 / §5。

| 项 | 约定 |
|---|---|
| 服务内路径前缀 | `/v1/situation/shenzhen-innovation/**`（网关对外 `/display/v1/situation/shenzhen-innovation/**`） |
| 地域锁定 | 城市分析 Tab **锁定深圳**（FE-TS-06d），对标 8 城为参照系 |
| 历史序列 | 指标体系历史序列固定 **2021–2025**（规划 M6）；运行监测时间轴 2020–2026（`shenzhenInnovationMonitorTimeline` L45） |
| 读写面 | 全只读 ADS；无带写面 |

## 2. 枚举字典（前端只读消费）

### 2.1 载体类型 `carrier_type`（5 类，逐字）
`baseRecords` 出现值（L62/L79/L96/L113/L130）：`载体` · `平台` · `企业` · `服务机构` · `项目`。

### 2.2 行政区 `district`（深圳区级，逐字）
`baseRecords` 与 timeline 出现值：`南山区` · `光明区` · `宝安区` · `福田区` · `龙岗区` · `坪山区` · `罗湖区`（其余区由后端字典全量下发，前端不硬编码——同 M1 §3.2 边界）。

### 2.3 趋势方向 `direction`（2 类）
`rise`上行 · `fall`下行（`baseRecords` L68/L169）。

### 2.4 领域 `field_key`（引用）
复用领域级联字典（`toSelectedFieldSet` / `fieldFilterOptions`，data.js）；demo 样本含 `intelligent-robotics` · `synthetic-biology` · `future-network-communications`。**禁止另造字典**（同 M1 §1.3 `field_scope`）。

### 2.5 页面能力 `capability`（6 类，逐字）
`App.jsx` L11809–L11825：`innovation-carriers`创新载体 · `core-indicators`核心指标 · `field-distribution`领域分布 · `operation-monitor`运行监测 · `carrier-ranking`载体排名 · `city-comparison`城市对比。

### 2.6 领域评价 `field_rating`（3 类）
规划 M6「优/潜/弱」：`advantage`优势 · `potential`潜力 · `weak`薄弱（逐字标签由后端字典下发，U3）。

## 3. 接口清单（5 类）

### 3.1 深圳载体检索 + 详情

**用途**（规划 M6-BE ①）：60 载体三级筛选 + 地图 + 排名 + 详情（FE-TS-06a）。

`POST /v1/situation/shenzhen-innovation/carriers/search`：

```json
{
  "field_values": ["intelligent-robotics"],
  "keyword": "",
  "start_year": "2020", "end_year": "2026",
  "districts": ["南山区"],
  "carrier_types": ["平台"],
  "sort_key": "score", "sort_order": "desc",
  "page": 1, "size": 20
}
```

```json
{
  "code": 0,
  "data": {
    "total": 60, "page": 1, "size": 20,
    "records": [
      { "carrier_id": "sim-nanshan-robotics", "name": "西丽湖智能机器人创新载体群",
        "field_key": "intelligent-robotics", "carrier_type": "载体", "district": "南山区", "city": "深圳",
        "institution": "西丽湖国际科教城 / 鹏城实验室",
        "score": 96, "trend": "+17.8%", "direction": "rise", "year": "2026",
        "carriers": 42, "achievements": 318,
        "evidence": "创新载体库 / 国内项目 / 企业资讯",
        "summary": "…", "metric_id": "Q0xx" }
    ],
    "map_points": [ { "carrier_id": "sim-nanshan-robotics", "district": "南山区", "score": 96 } ],
    "ranking": [ { "carrier_id": "sim-nanshan-robotics", "rank": 1, "score": 96 } ],
    "filter_echo": { "districts": ["南山区"] },
    "metric_ids": ["Q0xx"]
  }
}
```

字段逐字对齐 `baseRecords`（L57–L179）。`GET /v1/situation/shenzhen-innovation/carriers/{carrier_id}` 返全字段 + `evidence` 来源链。边界：`trend` 为字符串百分比（demo 口径，如 `+17.8%`），**数值化口径待 M0**（U2）；`evidence` 为数据来源标注，必返。

### 3.2 `GET /v1/situation/shenzhen-innovation/indicator-systems` — 指标体系（10 系三级 + 构成 + 历史）

**用途**（规划 M6-BE ②）：10 系下钻至三级 + 构成 pill + 历史序列 2021–2025 + 多指标对比 + 区间对比（FE-TS-06b）。

| Query | 说明 |
|---|---|
| `system_keys` | 可选，多选（多指标对比）；默认全返 10 系 |
| `compare_ranges` | 可选，区间对比（如 `2021-2023,2023-2025`） |

```json
{
  "code": 0,
  "data": {
    "systems": [
      {
        "system_key": "innovation-input", "label": "创新投入系", "score": 86,
        "children": [
          { "indicator_key": "rd-expenditure", "label": "R&D 经费投入", "level": 2, "score": 88,
            "components": [ { "label": "构成项 A", "value": 62, "unit": "%" } ],
            "history": { "years": ["2021","2022","2023","2024","2025"], "values": [78, 81, 84, 86, 88] },
            "metric_id": "Q0xx" }
        ],
        "metric_id": "Q0xx"
      }
    ],
    "range_compare": [
      { "range": "2021-2023", "system_key": "innovation-input", "cagr": 6.8 },
      { "range": "2023-2025", "system_key": "innovation-input", "cagr": 4.9 }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：10 系清单与三级结构**由后端字典全量下发**（demo 未逐项展开，U4）；`cagr`（区间增速）为算法产物带 `metric_id`；构成 pill `components` 缺数返空数组。

### 3.3 `GET /v1/situation/shenzhen-innovation/field-distribution` — 领域分布（8 领域 × 4 指标 + 空间集聚）

**用途**（规划 M6-BE ③）：8 领域 × 4 指标 + 集聚地图 + 优/潜/弱（FE-TS-06c）。

```json
{
  "code": 0,
  "data": {
    "fields": [
      { "field_key": "intelligent-robotics", "field_label": "智能机器人",
        "metrics": { "achievement_count": 318, "carrier_count": 42, "avg_score": 86.2, "growth": 17.8 },
        "rating": "advantage", "rating_label": "优势",
        "clusters": [ { "district": "南山区", "lng": 113.93, "lat": 22.53, "weight": 0.86 } ],
        "metric_id": "Q0xx" }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：8 领域清单随字典下发；四指标固定 `achievement_count` / `carrier_count` / `avg_score` / `growth`（对齐 `buildFieldDistribution` L335–L364 的聚合口径，正式命名 M0 确认）；`rating` 判断（优/潜/弱）为算法产物（ALGO 参考：领域优潜弱判断），Java 只读。

### 3.4 `GET /v1/situation/shenzhen-innovation/city-benchmark` — 城市对标（8 城四维 + 缺口 + 外推）

**用途**（规划 M6-BE ④）：锁定深圳 + 雷达 + 轨迹 + 缺口 + 外推预测序列（FE-TS-06d）。

```json
{
  "code": 0,
  "data": {
    "base_city": "深圳",
    "benchmark_cities": ["北京", "上海", "杭州", "广州", "苏州", "成都", "合肥"],
    "dimensions": [
      { "key": "innovation_input", "label": "创新投入",
        "values": [ { "city": "深圳", "value": 94 }, { "city": "北京", "value": 96 } ] }
    ],
    "trajectory": { "years": ["2020","2021","2022","2023","2024","2025","2026"],
                    "series": [ { "city": "深圳", "values": [78, 81, 84, 87, 90, 92, 94] } ] },
    "comparison_series": [
      { "key": "shenzhen", "label": "深圳", "values": [] },
      { "key": "gba_avg", "label": "粤港澳大湾区均值", "values": [] },
      { "key": "national_avg", "label": "全国重点城市均值", "values": [] }
    ],
    "gaps": [
      { "dimension_key": "innovation_env", "label": "创新环境", "gap_value": 6.2, "benchmark_city": "北京", "source": "指标体系统计", "metric_id": "Q0xx" }
    ],
    "forecast": [
      { "dimension_key": "innovation_input", "method": "slope_extrapolation", "years": ["2026","2027","2028"], "values": [96, 98, 100], "metric_id": "Q0xx" }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：`comparison_series` 三系列对齐 `buildCityComparison`（L335–L364：深圳 / 粤港澳大湾区均值 / 全国重点城市均值）；缺口 `gaps` 须带 `source`（缺口来源）与 `metric_id`；外推 `forecast` 方法固定 `slope_extrapolation`（斜率外推，ALGO 参考），**须标注为预测值**，前端与实测序列视觉区分（虚线）。

### 3.5 运行监测时间轴（随载体检索同包）

`GET /v1/situation/shenzhen-innovation/operation-timeline`：返 `shenzhenInnovationMonitorTimeline`（L41–L55）结构 `{title, current_year, range_label, years[], events[{date, district, text}]}`；事件为数据侧维护内容，禁前端硬编码。

## 4. 数据需求与存储建议（Mock 先行 D7）

| # | 域 | 建议表名 | 关键字段 | 消费接口 | 备注 |
|---|---|---|---|---|---|
| 1 | 深圳载体 | `ts_sz_carrier` | `carrier_id, name, field_key, carrier_type, district, institution, score, trend, direction, year, carriers, achievements, evidence, summary, metric_id` | §3.1 | 60 条样本起步 |
| 2 | 指标体系 | `ts_sz_indicator_system` | `system_key, indicator_key, level, parent_key, label, weight, score, year, metric_id` | §3.2 | 10 系三级 |
| 3 | 领域分布 | `ts_sz_field_dist` | `field_key, year, achievement_count, carrier_count, avg_score, growth, rating, metric_id` | §3.3 | rating 算法产物 |
| 4 | 城市对标 | `ts_sz_city_benchmark` | `city, dimension_key, year, value, metric_id`；`ts_sz_city_forecast`（外推） | §3.4 | forecast 须标预测 |
| 5 | 运行事件 | `ts_sz_operation_event` | `event_id, date, district, text, source_code` | §3.5 | 数据侧维护 |

## 5. 未决项

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | 对标 8 城清单（除深圳外 7 城）定稿 | M0 产品侧 |
| U2 | 载体 `trend` 字符串百分比的数值化口径（同比/环比） | M0 + 数据侧 |
| U3 | `field_rating`（优/潜/弱）阈值与逐字标签 | M0 + 算法侧 |
| U4 | 10 指标体系清单与三级结构真源 | M0 + 数据侧（`ALL-TS-D9` 随批 3 评审） |
| U5 | 外推预测 `forecast` 的合规表述（页面需「预测」水印/标注） | M0 产品侧 |

## 6. 自检（冻结前）

- [ ] 载体字段与 `baseRecords`（L57–L179）逐字一致（含 `evidence` 来源链）
- [ ] `carrier_type` / `district` / `direction` 枚举与 demo 逐字一致；区清单后端全量下发
- [ ] `comparison_series` 三系列与 `buildCityComparison` 一致
- [ ] 外推 `forecast` 标注预测值；不冒充实测
- [ ] 缺数 / 空态与 M1 §5 一致

## 7. 会签记录（批 3 评审待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |
