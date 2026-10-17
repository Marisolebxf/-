# API · 科技发展态势（TS）· M4 全球创新监测（接口契约草案）

> **任务**：`BE-TS-CONTRACT-02`（M2–M9 接口契约定义，按批冻结）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。本模块属**批 3**（M4/M5/M6），批 3 开工前冻结（`API-TS-M1.md` §9.2）。
> **范围**：仅 M4（全球创新监测）。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `TS-模块开发规划与任务拆分.md` §4 M4（FE-TS-04a~04e） |
| 五 Tab 结构 | `demo-ui-science/src/pages/global-innovation/index.jsx` L11–L46 |
| 成果类型/领域/城市枚举 | `demo-ui-science/src/pages/global-innovation/mockData.js` L2–L25 / L163 |
| 成果记录字段 | `mockData.js` L28–L60 `generateMockData` |
| 载体记录字段（含五年分） | `mockData.js` L63–L97 `generateCarriers` |
| 实时 KPI 四件 | `tabs/InnovationRealtime.jsx` L81–L129 |
| 预警 / 推送记录 | `mockData.js` L144–L161 `generateAlerts` / `generatePushRecords` |
| 城市能力五维 + 政策建议 | `mockData.js` L100–L142 `generateCityData`（radarData L129–L135） |
| 轮询口径（D2） | `TS-模块开发规划与任务拆分.md` §0 D2（轮询 + 定时刷新，首版 30s） |

---

## 1. 模块约定（增量）

全局约定继承 `API-TS-M1.md` §1 / §4 / §5。

| 项 | 约定 |
|---|---|
| 服务内路径前缀 | `/v1/situation/global-innovation/**`（网关对外 `/display/v1/situation/global-innovation/**`） |
| 实时性 | **轮询 + 定时刷新**（D2），首版 30s；`as_of` 增量提示，不做百分比进度 |
| 读写面 | 业务数据只读 ADS；**带写面** = §3.4 预警已读 / 推送已读 / 订阅配置（app_user 家族） |

## 2. 枚举字典（前端只读消费）

### 2.1 成果类型 `achievement_type`（5 类，逐字）
`mockData.js` L20–L25：`patent`专利 · `paper`论文 · `news`新闻 · `institution`科研机构 · `enterprise`创新企业。

### 2.2 领域 `domain`（8 类，逐字）
`mockData.js` L15–L18：`合成生物` · `光载信息` · `量子信息` · `新材料` · `人工智能` · `新能源` · `智能制造` · `生命健康`。

### 2.3 监测城市 `city`（10 城，逐字）
`mockData.js` L2–L13：`深圳` · `北京` · `上海` · `杭州` · `硅谷` · `纽约` · `伦敦` · `东京` · `新加坡` · `柏林`（各带 `country` 与 `location=[lng,lat]`）。

### 2.4 预警等级 `alert_level`（3 类，逐字）
`mockData.js` L147–L149：`urgent` · `important` · `normal`（与 M1 §2.8 `warning_level` 同义族，本模块用此三名）。

### 2.5 预警类型 `alert_type`（3 类，逐字）
`threshold`阈值 · `trend`趋势 · `relation`关系（`mockData.js` L147–L149）。

### 2.6 推送类型 `push_type`（3 类，逐字）
`update`动态更新 · `report`报告 · `ranking`排名更新（`mockData.js` L154–L160）。

### 2.7 实时 KPI `realtime_kpi`（4 件，逐字）
`InnovationRealtime.jsx` L81–L129：`realtime_patent`实时专利公开 · `realtime_paper`实时论文收录 · `realtime_investment`实时投资金额 · `realtime_org`实时新增机构。

### 2.8 城市能力五维 `city_dimension`（雷达，逐字）
`mockData.js` L129–L135：`创新投入` · `创新产出` · `创新环境` · `人才储备` · `政策支持`。

## 3. 接口清单（5 类）

### 3.1 `POST /v1/situation/global-innovation/achievements/search` — 创新成果列表 + 地图落点

**用途**（规划 M4-BE ①）：类型/领域/地理坐标 + 筛选（FE-TS-04a 综合展示）。

```json
{
  "achievement_types": ["patent", "paper"],
  "domains": ["人工智能"],
  "city": "深圳",
  "date_start": "2025-01-01", "date_end": "2026-10-14",
  "keyword": "",
  "page": 1, "size": 20, "sort_key": "date", "sort_order": "desc"
}
```

```json
{
  "code": 0,
  "data": {
    "total": 320, "page": 1, "size": 20,
    "records": [
      { "achievement_id": "inv-1", "name": "深圳人工智能创新企业成果1", "achievement_type": "enterprise",
        "type_label": "创新企业", "lng": 114.0579, "lat": 22.5431, "value": 180,
        "country": "中国", "city": "深圳", "domain": "人工智能", "date": "2026-05-25",
        "description": "…", "metric_id": null }
    ],
    "map_points": [ { "achievement_id": "inv-1", "lng": 114.0579, "lat": 22.5431, "achievement_type": "enterprise", "value": 180 } ],
    "filter_echo": { "achievement_types": ["patent", "paper"], "domains": ["人工智能"], "city": "深圳" },
    "metric_ids": []
  }
}
```

字段对齐 `generateMockData`（`mockData.js` L42–L59）。边界：`value` 为热度/规模演示值，真源口径**待 M0**（U2）；`metric_id=null` 时只显 ⓘ。

### 3.2 `GET /v1/situation/global-innovation/realtime` — 实时数据（轮询）

**用途**（规划 M4-BE ②）：4 KPI + 趋势 + 领域分布，支持轮询增量（FE-TS-04b）。

| Query | 说明 |
|---|---|
| `as_of` | 可选，上次响应时间；服务端返增量 `delta` |
| `domains` | 可选，领域过滤 |

```json
{
  "code": 0,
  "data": {
    "as_of": "2026-10-14T10:00:30+08:00",
    "kpis": [
      { "key": "realtime_patent",      "label": "实时专利公开", "value": 124580, "unit": "件",   "delta": 36,  "metric_id": "Q0xx" },
      { "key": "realtime_paper",       "label": "实时论文收录", "value": 48210,  "unit": "篇",   "delta": 12,  "metric_id": "Q0xx" },
      { "key": "realtime_investment",  "label": "实时投资金额", "value": 96.4,   "unit": "亿元", "delta": 0.8, "metric_id": "Q0xx" },
      { "key": "realtime_org",         "label": "实时新增机构", "value": 1280,   "unit": "家",   "delta": 3,   "metric_id": "Q0xx" }
    ],
    "trend": { "points": [ { "ts": "2026-10-14T09:30:00+08:00", "realtime_patent": 124500 } ] },
    "domain_distribution": [ { "domain": "人工智能", "value": 32 } ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：demo 的 30s 增量为**模拟**（`InnovationRealtime.jsx` L81–L129）；真源为流式/准实时汇聚，**增量 `delta` 口径待 M0**（U3）；无真源时按 M1 §5 返 `empty_reason=no_source` + 🧪。

### 3.3 载体排行 + 载体详情

**用途**（规划 M4-BE ③）：多维排名 + 五年分详情（FE-TS-04c）。

`POST /v1/situation/global-innovation/carriers/ranking`：入参 `domains[]` / `city` / `keyword` / `create_year_start` / `create_year_end` / `rank_dimension`（`score` 默认）/ 分页。

`GET /v1/situation/global-innovation/carriers/{carrier_id}`：

```json
{
  "code": 0,
  "data": {
    "carrier": { "carrier_id": "carrier-1", "name": "华为技术", "carrier_type": "enterprise", "city": "深圳", "country": "中国",
                 "lng": 114.0579, "lat": 22.5431, "domain": "人工智能", "create_year": 2003, "description": "…" },
    "score": 95, "rank": 1, "rank_change": 1,
    "score_history": [ { "year": 2020, "score": 76 }, { "year": 2021, "score": 81 }, { "year": 2022, "score": 86 }, { "year": 2023, "score": 90 }, { "year": 2024, "score": 93 } ],
    "stat": { "patents": 4300, "papers": 1600, "projects": 480 },
    "achievements": [ { "achievement_type": "patent", "name": "华为-人工智能成果", "year": 2020, "value": 78 } ],
    "metric_ids": ["Q0xx"]
  }
}
```

字段对齐 `generateCarriers`（`mockData.js` L76–L96）。边界：`score_history` 固定 5 年窗（2020–2024 演示口径，正式口径按筛选年份区间，U4）。

### 3.4 监测预警 + 推送记录（带写面）

**用途**（规划 M4-BE ④⑤）：预警卡 + 创新点发现 + 推送记录已读/未读（FE-TS-04d）。

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/v1/situation/global-innovation/alerts` | 预警列表（`alert_level` / `alert_type` / `is_read` / 分页） |
| `POST` | `/v1/situation/global-innovation/alerts/{alert_id}/read` | 标记已读（按登录用户隔离） |
| `GET` | `/v1/situation/global-innovation/push-records` | 推送记录（`push_type` / `is_read` / 分页） |
| `POST` | `/v1/situation/global-innovation/push-records/{record_id}/read` | 标记已读 |
| `GET` / `PUT` | `/v1/situation/global-innovation/monitor/subscriptions` | 监测订阅配置（关注点：领域/城市/载体/关键词），读写 app_user 家族 |

```json
{
  "code": 0,
  "data": {
    "total": 12, "page": 1, "size": 20,
    "records": [
      { "alert_id": "alert-1", "alert_level": "urgent", "alert_type": "threshold",
        "title": "量子信息领域突破性进展", "description": "…",
        "trigger_time": "2026-05-20 14:30", "is_read": false }
    ]
  }
}
```

边界：`alert_level` 三档与 demo 逐字一致；`is_read` 按用户隔离；预警触发为算法产物（创新点发现与预警），Java 只读结果 + 落已读状态。

### 3.5 `GET /v1/situation/global-innovation/cities/capability` — 城市能力（10 城五维 + 政策建议）

**用途**（规划 M4-BE ⑥，FE-TS-04e）。

| Query | 说明 |
|---|---|
| `cities` | 可选，多选（默认 10 城全返） |
| `year` | 年份，默认当前 |

```json
{
  "code": 0,
  "data": {
    "cities": [
      {
        "city": "深圳", "country": "中国", "rank": 1, "score": 94,
        "radar": [ { "dimension": "创新投入", "value": 96 }, { "dimension": "创新产出", "value": 91 }, { "dimension": "创新环境", "value": 93 }, { "dimension": "人才储备", "value": 89 }, { "dimension": "政策支持", "value": 92 } ],
        "dimensions": {
          "innovation_input": { "rd_expenditure": 98, "talent": 89, "investment": 99, "enterprise_investment": 94 },
          "innovation_output": { "patents": 7200, "papers": 2600, "new_products": 430 },
          "innovation_env": { "institutions": 180, "enterprises": 4600, "incubators": 88, "policy_support": 91 },
          "innovation_performance": { "gdp_contribution": 5.8, "employment_rate": 92.1 }
        },
        "policy_suggestions": ["深圳应加大高端人才引进力度", "…"],
        "metric_id": "Q0xx"
      }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

字段对齐 `generateCityData`（`mockData.js` L113–L141）：`dimensions` 四组明细 + `radar` 五维雷达 + `policy_suggestions`。边界：政策建议文本为**演示生成**（L136–L140 模板拼接），真源待算法/数据侧（U5）；无真源时返空数组 + 前端不渲染建议区。

## 4. 数据需求与存储建议（Mock 先行 D7）

| # | 域 | 建议表名 | 关键字段 | 消费接口 | D3 就绪度 |
|---|---|---|---|---|---|
| 1 | 创新成果 | `ts_gi_achievement` | `achievement_id, name, achievement_type, domain, country, city, lng, lat, value, date, description, source_code` | §3.1 | 部分待映射 |
| 2 | 实时汇聚 | `ts_gi_realtime_stat` | `kpi_key, ts, value, delta, domain, calc_batch_id` | §3.2 | **流式源待定（U3）** |
| 3 | 创新载体 | `ts_gi_carrier` | `carrier_id, name, carrier_type, city, country, lng, lat, domain, create_year, score, rank, rank_change, patents, papers, projects` | §3.3 | 项目内结构 |
| 4 | 载体五年分 | `ts_gi_carrier_score_year` | `carrier_id, year, score, metric_id` | §3.3 | 对齐 `/metrics/v1/catalog` |
| 5 | 预警 | `ts_gi_alert` | `alert_id, alert_level, alert_type, title, description, trigger_time, object_ref` | §3.4 | 算法产物 |
| 6 | 城市能力 | `ts_gi_city_capability` | `city, year, score, rank, radar JSON, dimensions JSON, metric_id` | §3.5 | 算法产物 |
| 7 | 已读/订阅 | app_user 家族 | `user_id, alert_id/record_id, read_at`；`subscription JSON` | §3.4 | 带写面 |

## 5. 未决项

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | 成果 `value`（热度/规模）真源口径与单位 | M0 + 数据侧 |
| U2 | 10 城清单是否固定 / 可扩（demo 硬编码 10 城） | M0 产品侧 |
| U3 | 实时数据真源（流式汇聚 or 定时快照）与增量 `delta` 口径 | M0 + 数据侧 |
| U4 | 载体五年分窗口（演示 2020–2024 固定 vs 随筛选区间） | M0 前端侧 |
| U5 | 政策建议文本来源（算法生成 or 人工维护） | M0 + 算法侧 |
| U6 | 预警/推送 `metric_id` 清单 | `ALL-TS-D9`，随批 3 评审 |

## 6. 自检（冻结前）

- [ ] `achievement_type` / `domain` / `city` 枚举与 `mockData.js` L2–L25 逐字一致
- [ ] 实时 KPI 四件与 `InnovationRealtime.jsx` L81–L129 逐字一致；轮询口径 D2（30s、不可见暂停）
- [ ] 预警/推送 `is_read` 按用户隔离；带写面落 app_user
- [ ] 城市能力 `radar` 五维与 `dimensions` 四组字段与 `mockData.js` L113–L141 一致
- [ ] 演示生成内容（政策建议模板拼接、模拟增量）已显式标注，未伪闭合
- [ ] 缺数 / 空态与 M1 §5 一致

## 7. 会签记录（批 3 评审待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |
