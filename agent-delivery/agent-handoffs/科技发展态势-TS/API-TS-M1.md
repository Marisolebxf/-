# API · 科技发展态势（TS）· M1 科技全域态势（接口契约草案）

> **任务**：`BE-TS-CONTRACT-01`（M0 · Java 接口契约定义与数据需求评审）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；M0 会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。路径前缀 / DTO 命名 / 服务归属均以 **M0 三方评审结论**为准，评审后本文件转正式契约。
> **范围**：仅 M1（科技全域态势）。M2–M9 按批另出 `API-TS-M2.md` 等，不要求一次出全。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `agent-delivery/agent-handoffs/科技发展态势-TS/TS-模块开发规划与任务拆分.md` §4 M1 |
| 前端字段名 | `demo-ui-science/src/data.js`（`factorItems` L250、`globalFilterDefaults` L73、`objectLevelMapPointTypes` L303、`sharedMapRegions` L335、`trendSeries` L933、`timeline` L1423）、`src/mapObjectDetail.js` L39/L114/L133/L150/L164/L179、`src/App.jsx` L388/L395/L400/L411/L423/L460/L1537 |
| 调用链 / 服务边界 / 网关前缀 | `agent-delivery/architecture-baseline.md` §1 铁律 · §2 D3/D4/D5/D7/D12 · §3 服务清单 |
| 统一包络 / trace 头 | `lumen-svc-platform/gkxlumen-common/gkxlumen-common-core/.../util/R.java`；`gkxlumen-gateway/.../filter/GkxlumenRequestGlobalFilter.java` |
| 路径先例 | `gkxlumen-metrics/.../MetricCatalogController.java`（`/metrics/v1/catalog`） |
| 血缘 / 就绪度 | `agent-delivery/data-lineage-policy.md` v1.3 §2.3 |
| Mock 开关口径 | `repos/lumen-ui-science-pc` 仓规（`USE_MOCK` / `VITE_APP_USE_MOCK`，`USE_MOCK=false` 零 mock 直连网关） |

---

## 0. 一句话

M1 分两种活：**只读聚合**（§3.1–§3.6，Java 只读 ADS、不算指标）与**带写的展示事务面**（§3.7 收藏/标签、§3.8 导出任务中心，落 `app_user` 家族）。前端不猜路径，全部按本文件冻结后的 DTO 对接。

**复用清单（已存在、禁止重复造）**

| 复用对象 | 现成接口 | 契约用法 |
|---|---|---|
| 领域 / 产业集群字典 | `/topic/v1/meta/industry-clusters`（`API-CHAIN-INDUSTRY-CLUSTER.md`） | `field_scope` 取值与标签，**禁止另造字典** |
| 指标 8 件套 + 四维就绪度 | `/metrics/v1/catalog` | `metric_id` 冒烟与 ⓘ 弹卡数据源 |
| 鉴权 / 租户 / trace | 网关统一（`GkxlumenRequestGlobalFilter`） | 全接口透传，不在业务侧重写 |

---

## 1. 全局约定（M1 全部接口遵守）

### 1.1 调用链与路径

```text
lumen-ui-science-pc → gkxlumen-gateway(/display/** StripPrefix) → Java 展示聚合 → (只读 ADS | Feign /internal/* → Python)
```

| 项 | 约定 |
|---|---|
| 网关对外前缀 | `/display/v1/...`（架构基线 §2 D5「展示 BFF」） |
| 服务内路径 | 网关 StripPrefix 后服务内为 `/v1/situation/**`（**待 M0 确认**） |
| 建议落库服务 | `gkxlumen-display`（架构基线 §3 列为 **Wave4**，当前仓中**尚无该模块**）；若 M1 需抢展示 V1.0（**10-30**）窗口，可先落已存在的 `gkxlumen-innov`（`/innov/v1/*`）→ **归属由 human:徐腾强 在 M0 拍板** |
| 禁止 | Java 写 ADS；Java 直连 Python/nGQL/DB 算法面；前端直连 Python/DB；打 `demo-*` 运行时（D12） |
| 读写面 | 业务数据只读 `*_ads`；**两类带写面**（§3.7 收藏/标签、§3.8 导出任务中心）读写 `app_user` 家族（D4） |

### 1.2 响应包络与错误码

统一 `R<T>`：`{ "code": 0, "msg": "ok", "data": { ... } }`（`lumen-svc-platform` common-core `R.java`）。`code≠0` 时 `data` 为空，前端走空态，**不伪造数据**。

| code | 语义 | 前端动作 |
|---|---|---|
| 0 | 成功 | 正常渲染 |
| 400 | 参数非法（如 `factor_key` 不在字典、`region_scope` 越级） | 提示并阻断请求 |
| 401 / 403 | 未登录 / 无权限（导出与收藏按角色） | 跳 SSO / 置灰入口 |
| 404 | 对象 / 事件不存在 | 抽屉显示「对象不存在」，不补假 |
| 409 | 标签重名、收藏重复 | 就地提示，不覆盖 |
| 500 | 服务异常 | 通用异常态 |

### 1.3 公共入参（筛选上下文，M1 六类只读接口复用）

对应 demo `globalFilterDefaults`（`data.js` L73）：

| 契约字段 | 类型 | demo 字段 | 说明 |
|---|---|---|---|
| `region_scope` | enum | `regionScope` | 地域层级 `global`/`gba`/`shenzhen`，见 §3.2 |
| `region_sample` | string | `regionSample` | 样本口径（如「全球重点科创城市样本」）；仅回显，不参与聚合 |
| `start_year` / `end_year` | string | `startYear` / `endYear` | 年份区间，M1 默认 `2020`–`2026` |
| `field_scope` | string | `fieldScope` | 领域（cluster）编码，如 `CL-FUT-05`；**复用产业集群契约**（`API-CHAIN-INDUSTRY-CLUSTER.md`），禁止另造字典 |
| `field_tag` | string | `fieldTag` | 主题标签，如「智能机器人」 |
| `factor_keys` | string[] | `selectedFieldValues` / 图层开关 | 要素多选，取值见 §2.1 |
| `keyword` | string | `searchTerm` | 关键词定位 |

| 公共返回字段 | 类型 | 说明 |
|---|---|---|
| `filter_echo` | object | 回显生效筛选项；前端据此校准（防「筛选与结果不一致」） |
| `metric_ids` | string[] | 本接口涉及指标的 `metric_id`，走 `/metrics/v1/catalog`（§4 D9） |
| `empty_reason` / `empty_message` | string | 缺数时必填，见 §5 |

### 1.4 分页与排序（列表类接口统一）

| 入参 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `page` / `size` | int | 1 / 20 | 页码从 1 起；`size` 上限 100 |
| `sort_key` | string | `-` | 按接口枚举；`importance` / `count` / `time` 等 |
| `sort_order` | string | `desc` | `asc` / `desc` |

返回：`{ "total": 1234, "page": 1, "size": 20, "records": [...] }`。

### 1.5 可观测

`X-Trace-Id` / `traceparent` 由网关 `GkxlumenRequestGlobalFilter` 透传与回传（见基线 §1 铁律）；前端按仓规注入 axios。M1 八类接口全部纳入 trace 覆盖。

---

## 2. 枚举字典（前端只读消费，禁止前端手写状态或字典）

### 2.1 科创要素 `factor_key`（11 类）
按 demo `data.js` L250 `factorItems` 逐字：`scholar`专家学者 · `meeting`会议 · `institution`组织机构 · `enterprise`企业 · `service`服务机构 · `topic`课题 · `project`项目 · `paper`论文 · `journal`期刊 · `patent`专利 · `result`成果。
`default_active` 照 demo（`service` / `project` / `journal` 默认关）。`factor_label` 与色值同源自后端字典，**前端不各写一份**。

### 2.2 对象落点类型 `object_type`（6 类 → 归属要素）
`data.js` L303 `objectLevelMapPointTypes`：`enterprise`企业→`enterprise` · `park`园区→`enterprise` · `institution`科研机构→`institution` · `lab`高校/实验室→`institution` · `scholar`学者/专家→`scholar` · `service`服务机构→`service`。

### 2.3 热力等级 `heat_level`（4 档）
`data.js` L295 `sharedMapLegend.heatLevels`：`low`低 · `medium`中 · `high`高 · `extreme`极高（对象点图例用 3 档「低/中/高」，见 §3.2）。

### 2.4 事件相关

| 字典 | 取值（逐字） | 真源 |
|---|---|---|
| `event_type` | `hotspot`科技热点 · `publicOpinion`科技舆情 | `App.jsx` L395 |
| `importance_level` | `high`高 · `medium`中 · `low`低（筛选含 `all`全部） | `App.jsx` L388 |
| `time_granularity` | `day`日 · `week`周 · `month`月 · `quarter`季 · `year`年 | `App.jsx` L400 |

⚠️ demo 现以正则从文案猜 `importance`（`App.jsx` L1537 `getTimelineEventImportance`）；**契约要求后端直接返回 `importance_level` 字段，前端不再猜**。事件类型同理（demo L513 正则兜底）。

### 2.5 实时监控口径 `metric_kind`（3 类）
`App.jsx` L460 `overviewStatMetricOptions`：`count`数量统计 · `share`分布比例 · `growth`增长趋势。

### 2.6 导出角色策略（D1 决策：照搬 demo）
`App.jsx` L423 `globalSituationExportRolePolicies`：

| `role` | `max_rows` | 字段白名单 |
|---|---|---|
| `executive` | 20 | 名称/类型/地域/时间/重要性/摘要（汇总型，无指标值） |
| `analyst` | 50 | 名称/类型/地域/时间/重要性/指标值/摘要 |
| `governance` | 50 | 同 `analyst` |
| `default` | 30 | 同 `executive` |

`role` 由后端按登录态下发，**前端不得自选提权**。
导出审计：demo 以 `EXPORT_AUDIT_STORAGE_KEY = 'tech-global-situation-export-audit'` 本地留痕（`App.jsx` L409）；契约要求**审计落服务端**（见 §3.8），前端不再自存。

### 2.7 导出列与行为白名单（逐字，`App.jsx` L408–L421）

| 项 | 值 |
|---|---|
| 全白名单 `globalSituationExportFieldWhitelist` | 名称 / 类型 / 地域 / 时间 / 重要性 / **指标值** / 摘要 |
| 受限白名单 `globalSituationLimitedFieldWhitelist` | 名称 / 类型 / 地域 / 时间 / 重要性 / 摘要（**无指标值**） |
| 导出列 `globalSituationExportColumns`（CSV 列冻结） | `name`名称 · `type`类型 · `region`地域 · `time`时间 · `importance`重要性 · `metric`指标值 · `summary`摘要 |
| 行为上限 `GLOBAL_SITUATION_EXPORT_ROW_LIMIT` | 50（`App.jsx` L408） |

### 2.8 预警等级 `warning_level`（`mapDisplay.js` L65–L75）

`urgent`紧急（阈值 100%） · `important`重要（80%） · `general`一般 · `normal`一般（60%）；排序权重 `['urgent','important','general','normal']`，demo 兼容别名 `alertLevel`。**仅对确有预警的对象/区域返回该字段**，无预警 → `null`，前端不渲染预警入口。

---

## 3. 八类接口

### 3.1 `GET /v1/situation/layers` — 要素图层与统计

**用途**（规划 §4 M1-BE ①）：11 类要素 key/label/count/数据源标注/默认开关。

| Query | 说明 |
|---|---|
| 公共入参 §1.3 | 支持 `region_scope` / `field_scope` / 年份区间 |

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "filter_echo": { "region_scope": "global", "start_year": "2020", "end_year": "2026", "field_scope": "CL-FUT-05" },
    "factors": [
      { "factor_key": "scholar",     "factor_label": "专家学者", "count": 248000,  "source_label": "人才基础指标模型",   "default_active": true,  "metric_id": "Q0xx" },
      { "factor_key": "service",     "factor_label": "服务机构", "count": 6200,   "source_label": "服务机构基础指标模型", "default_active": false, "metric_id": null },
      { "factor_key": "result",      "factor_label": "成果",     "count": 156000, "source_label": "科技成果与转化数据",   "default_active": true,  "metric_id": "Q0xx" }
    ],
    "heat_levels": [ { "key": "low", "label": "低" }, { "key": "medium", "label": "中" }, { "key": "high", "label": "高" }, { "key": "extreme", "label": "极高" } ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：`count=0` 的要素仍返回（前端置灰，不隐藏）；`metric_id=null` 时该数字只显 ⓘ 不显就绪度角标（§4）。

### 3.2 `GET /v1/situation/regions` — 地域树与对象落点

**用途**（规划 M1-BE ②）：全球/湾区/深圳三级 + 对象级点（随筛选参数返回）。

| Query | 说明 |
|---|---|
| `region_scope` | 必填：`global` / `gba` / `shenzhen` |
| `parent_key` | 可选，下钻（深圳 → 区） |
| `object_types` | 可选，`object_type` 多选，默认全部 |
| `bbox` | 可选，视口裁剪（`lng1,lat1,lng2,lat2`） |

```json
{
  "code": 0,
  "data": {
    "region_tree": [
      { "key": "global", "label": "全球", "level": 1, "children": [
          { "key": "gba", "label": "湾区", "level": 2, "children": [
              { "key": "shenzhen", "label": "深圳", "level": 3, "children": [
                  { "key": "futian", "label": "福田区" }, { "key": "guangming", "label": "光明区" }, { "key": "pingshan", "label": "坪山区" }
              ] }
          ] }
      ] }
    ],
    "regions": [
      {
        "object_id": "shenzhen",
        "name": "深圳",
        "heat_level": "high",
        "warning_level": "important",
        "trend_summary": "智能机器人、具身智能和硬件成果转化链路活跃",
        "factor_keys": ["patent", "paper", "enterprise", "result"],
        "lng": 114.0579, "lat": 22.5431,
        "summary_value": "综合 80.0",
        "viewport_zoom": 10
      }
    ],
    "object_points": [
      { "object_id": "PO-xxxx", "object_type": "park", "name": "南山先进材料联合实验室", "factor_key": "enterprise", "lng": 113.93, "lat": 22.53, "heat_level": "medium" }
    ],
    "heat_points": [ { "lng": 113.93, "lat": 22.53, "weight": 0.82 } ],
    "heat_legend": { "gradient": ["#165DFF", "#37A7FF", "#FFB65D", "#F53F3F"], "labels": ["低", "中", "高"] },
    "total": 20
  }
}
```

（`heat_points` / `heat_legend` 形状对齐前端 `TiandituMap` 的 `heatPoints` props 与 `mapDisplay.js` `getHeatGradientColors` / `getHeatColorForWeight`，L33–L52。）
边界：
- 越级 `region_scope`（如深圳对象挂在 `global`）→ **400**，不静默改层级。
- `bbox` 无命中 → `records=[]` + `empty_reason=sample_empty`（M1 为样本口径，不宣称全覆盖）。
- `warning_level` 只在有预警的对象上返回（无 → 省略或 `null`，见 §2.8）。
- 深圳区清单（demo 为 福田/光明/坪山）**由后端全量下发**，前端不硬编码区名。

### 3.3 `POST /v1/situation/factors/search` — 要素检索列表

**用途**（规划 M1-BE ③）：地域/时间/领域/要素/关键词过滤 + 排序分页。

```json
{
  "region_scope": "global",
  "start_year": "2020", "end_year": "2026",
  "field_scope": "CL-FUT-05", "field_tag": "智能机器人",
  "factor_keys": ["enterprise", "patent"],
  "keyword": "具身智能",
  "page": 1, "size": 20,
  "sort_key": "count", "sort_order": "desc"
}
```

```json
{
  "code": 0,
  "data": {
    "total": 1280,
    "page": 1, "size": 20,
    "records": [
      { "object_id": "PO-xxxx", "name": "鹏城智能计算研究院", "object_type": "institution", "factor_key": "institution",
        "region_label": "深圳", "time_label": "2026-05", "summary": "算力与基础模型", "score": 94.2, "metric_id": "Q0xx" }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：`factor_keys` 含未收录 key → **400**（不忽略）；`keyword` 空串按「不过滤」处理。

### 3.4 详情统一契约（四类抽屉：对象 L6 / 预警 / 事件 / 要素）

**用途**（规划 M1-BE ④）：四类详情共用一套 payload 形状，靠 `kind` 分派，前端 `InsightDetailDrawer` 一套渲染。

| 路由 | `kind` | 真源 |
|---|---|---|
| `GET /v1/situation/objects/{object_id}/l6` | `map-object` | `mapObjectDetail.js` L179 `buildMapObjectL6Sections`（五段） |
| `GET /v1/situation/warnings/{warning_id}` | `map-warning` | `mapObjectDetail.js` L482 `buildMapWarningDetail`（预警三卡） |
| `GET /v1/situation/events/{event_id}` | `timeline-event` | `mapObjectDetail.js` L527 `buildTimelineEventDetail`（载荷见 §3.5） |
| `GET /v1/situation/factors/{factor_key}` | `factor` | `mapObjectDetail.js` L639 `buildFactorDetail` |

```json
{
  "code": 0,
  "data": {
    "kind": "map-object",
    "title": "鹏城智能计算研究院",
    "tags": ["科创要素", "科研机构"],
    "summary": null,
    "metric_cards": [],
    "sections": [
      { "key": "basic",    "title": "基础信息查看功能",   "show_title": true, "body": "…",
        "rows": [ { "label": "对象名称", "value": "鹏城智能计算研究院" }, { "label": "图数据库ID", "value": "graph:xxxx" } ] },
      { "key": "metrics",  "title": "统计指标展示功能",   "show_title": true,
        "rows": [ { "label": "创新指数", "value": "94.2", "metric_id": "Q0xx" }, { "label": "专利数量", "value": "5,120" } ] },
      { "key": "analysis", "title": "分析数据展示功能",   "show_title": true, "body": "…",
        "rows": [ { "label": "服务协同", "value": "…" } ] },
      { "key": "trend",    "title": "监测数据趋势变化查看功能", "show_title": true, "body": "…",
        "rows": [ { "label": "趋势判断", "value": "…" }, { "label": "监测窗口", "value": "全球重点样本监测" } ],
        "trend_chart": { "years": ["2020","2021","2022","2023","2024","2025","2026"],
                         "series": [ { "label": "创新指数", "color": "#165DFF", "values": [72.0,74.8,76.6,78.4,81.2,79.8,82.0] } ] } },
      { "key": "map",      "title": "地图可视化展示功能", "show_title": true,
        "rows": [ { "label": "所属区域", "value": "深圳" }, { "label": "数据范围", "value": "全球重点样本" },
                  { "label": "地图图层", "value": "科研机构" }, { "label": "地图对象标识", "value": "PO-xxxx" } ] }
    ],
    "actions": ["关闭"],
    "metric_ids": ["Q0xx"]
  }
}
```

**各 kind 的 sections 固定顺序与关键字段**

| `kind` | sections（固定顺序） | 关键字段 |
|---|---|---|
| `map-object` | basic / metrics / analysis / trend / map（段标题真源 L39–L45） | metrics 行含 `metric_id`（挂 ⓘ，§4）；analysis 行来自 `relations`；trend 含 `trend_chart`；basic/map 属性行用 `PROPERTY_LABELS` 中文标签（L47–L63） |
| `map-warning` | 触发规则 / 处置建议 / 关联点位 | `metric_cards` 三卡：**变化幅度 / 预警阈值 / 触发时间**（L496–L500）；`tags`=[等级, 阈值预警, 区域]；`actions`=[关闭, 忽略, 查看关联对象] |
| `timeline-event` | 事件识别 / 相关主体 / 关联分析 / 证据核验 | 事件识别 5 行（事件标题/发布时间/来源·数据来源/地点·发生城市/事件类型）；相关主体为 `tags`；关联分析 3 行（关联事件/关联机构/关联人员）；证据核验（正文/原文链接 + `evidence_items`）；`actions`=[关闭, 导出文章, 分享事件] |
| `factor` | 描述 / 属性 / 关联关系 | `tags`=[科创要素, 要素类型]；属性行用中文属性标签（L366–L400） |

**三条硬约束**

1. **禁模拟内容**：demo 的关系行兜底（`mapObjectDetail.js` L328–L344）、事件关联主体兜底（L278–L300）、事件坐标抖动（`App.jsx` L1572）**均为演示兜底**；契约要求只返真实数据，空则空行 / 空 tags，**不得后端补假**。
2. 缺值统一 `"暂无数据"`（`mapObjectDetail.js` L37），**不省略 section**（前端五段结构固定）。
3. `graph_id` 仅作参考展示，**M1 不开放图查询**（M2 图谱才接）。

边界：路由对象不存在 → **404**；`metric_cards=[]` 时前端不渲染卡片区；`trend_chart` 缺失时前端不渲染趋势图（不补假曲线）。

### 3.5 `POST /v1/situation/events/search` + `GET /v1/situation/events/{event_id}` — 事件列表与详情

**用途**（规划 M1-BE ⑤）：时间粒度/重要性/类型筛选 + 分页排序 + 关联主体。

```json
{
  "region_scope": "shenzhen",
  "current_year": "2026", "time_granularity": "month",
  "event_types": ["hotspot", "publicOpinion"],
  "importance_level": "high",
  "field_scope": "CL-FUT-05",
  "keyword": "具身智能",
  "page": 1, "size": 20, "sort_key": "time", "sort_order": "desc"
}
```

```json
{
  "code": 0,
  "data": {
    "range_label": "2020-2026",
    "years": ["2020","2021","2022","2023","2024","2025","2026"],
    "total": 1280, "page": 1, "size": 20,
    "records": [
      { "event_id": "EV-xxxx", "date": "2026-05", "time_granularity": "month",
        "event_type": "hotspot", "event_type_label": "科技热点",
        "importance_level": "high", "importance_label": "高",
        "text": "智能机器人、光载信息、合成生物方向新增成果保持活跃",
        "related_objects": [ { "object_id": "PO-xxxx", "name": "鹏城智能计算研究院" } ],
        "lng": 114.06, "lat": 22.54,
        "source_label": "技术动态资讯", "metric_id": null }
    ],
    "metric_ids": []
  }
}
```

边界：`importance_level` 只支持单值（demo `App.jsx` L2347 为单选）→ 传数组 **400**；时间轴播放（`timeline.title` 时间演进动画）当前为**演示口径**（demo `App.jsx` L2359 已标「等级为演示口径，非真源实时」），真源事件流待 D3 三方库映射（§6）。
事件详情载荷见 §3.4（`kind=timeline-event`）：列表 `records[]` 只需带 `event_id` 供点开抽屉；列表字段与抽屉字段**同源不同形状**，前端不做二次拼装。

### 3.6 `GET /v1/situation/realtime/metrics` — 实时监控统计（轮询）

**用途**（规划 M1-BE ⑥）：要素卡统计 + 趋势序列（数量/占比/增长三口径），支持轮询。
**决策**（规划 D2）：**轮询 + 定时刷新**，首版前端常量 `30s`；页面不可见暂停、卸载清理。

| Query | 说明 |
|---|---|
| 公共入参 §1.3 | 必要 |
| `metric_kinds` | `count` / `share` / `growth`（默认三类全给） |
| `as_of` | 可选，上次响应时间；用于增量提示（**不做百分比进度**） |

```json
{
  "code": 0,
  "data": {
    "as_of": "2026-10-14T10:00:00+08:00",
    "cards": [
      { "factor_key": "patent", "factor_label": "专利",
        "count": { "value": 1820000, "unit": "件", "metric_id": "Q0xx" },
        "share":  { "value": 22.4, "unit": "%" },
        "growth": { "value": 8.6,  "unit": "%", "window": "同比" } }
    ],
    "trend": { "years": ["2020","2021","2022","2023","2024","2025","2026"],
               "series": [
                 { "name": "综合态势指数", "color": "#1d6fe9", "values": [63,68,72,79,83,86,88] },
                 { "name": "成果转化指数", "color": "#10a6b7", "values": [42,48,57,61,70,78,82] },
                 { "name": "政策效果指数", "color": "#f2a93b", "values": [51,56,60,66,71,76,79] } ] },
    "structure": [ { "key": "enterprise", "name": "企业", "value": 34 } ],
    "metric_ids": ["Q0xx"]
  }
}
```

（`trend` / `structure` 形状照 demo `data.js` L933 `trendSeries` / L955 `structureData`。）
边界：三口径任一缺失 → 该字段 `null` + 前端置灰；**禁止用 0 冒充缺失**。

### 3.7 收藏与标签（M1 带写面之一）

**用途**（规划 M1-BE ⑦ + D4）：服务端化 + 本地缓存；前端 `useFollow` 现有 localStorage 真源（key `sourcePage:type:objectId`）**降级为缓存**，服务端为准。

**收藏标识 `follow_key`**：`{source_module}:{type}:{object_id}`（对齐 demo `followItems.js`），由**后端生成并返回**，前端不得自造。语义保持 demo 口径：**同一对象在不同来源模块收藏 = 两条独立记录**（M1 不合并），避免前端误合成一条。

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/v1/situation/favorites` | 收藏列表（含标签）；可按 `source_module` 过滤 |
| `POST` | `/v1/situation/favorites` | 新增收藏 `{ "source_module": "global-situation", "type": "object", "object_type": "institution", "object_id": "PO-xxxx", "title": "…", "summary": "…", "tags": ["重点跟踪"] }` |
| `DELETE` | `/v1/situation/favorites/{follow_key}` | 取消收藏（**按 `follow_key`，不按 `object_id`**） |
| `PUT` | `/v1/situation/favorites/{follow_key}/tags` | 改挂标签 `{ "tags": ["重点跟踪"] }` |
| `GET` | `/v1/situation/tags` | 标签列表 |
| `POST` | `/v1/situation/tags` | 新建标签 `{ "name": "重点跟踪" }` → 重名 **409** |
| `PUT` | `/v1/situation/tags/{tag_id}` | 重命名 |
| `DELETE` | `/v1/situation/tags/{tag_id}` | 删除（**先解绑收藏**，不静默级联） |

```json
{
  "code": 0,
  "data": { "items": [
      { "follow_key": "global-situation:object:PO-xxxx", "source_module": "global-situation", "type": "object",
        "object_type": "institution", "object_id": "PO-xxxx", "title": "鹏城智能计算研究院",
        "summary": "算力与基础模型", "tags": ["重点跟踪"], "status": "active",
        "followed_at": "2026-10-14T10:00:00+08:00" }
  ] }
}
```

字段对齐 demo `followItems.js`：`source_module`→`sourceModule`、`followed_at`→`followedAt`、`type`/`object_type`/`object_id`/`title`/`summary`/`tags`/`status` 同名。`status` 取值枚举**待 M0 前端侧核验**（demo 语义未定，见 §6 U8）。
边界：收藏对象不存在 → **404**；`tags` 含未建标签 → **400**（前端先建后挂，禁止后端静默建）；写操作按登录用户隔离（`app_user` 家族）。

---

### 3.8 导出任务中心（M1 带写面之二；DoD 第 5 条 · 规划 §5 `BE-TS-S03`）

**用途**：把 demo 前端本地完成的导出（8 相位状态机）服务端化 + 审计留痕；角色策略与列白名单见 §2.6 / §2.7。

**相位映射**（demo `exportFlow.js` L36–L110 → 服务端状态）

| demo 相位（FE 已实现 `exportFlow.ts`） | 服务端语义 |
|---|---|
| `config`（选格式 / 内容项） | `GET /export/config` 下发 `format_options` / `content_items` |
| `generating`（`EXPORT_FLOW_PROGRESS_STEPS`） | `POST /export/jobs` 建任务 → `status=queued/running` |
| `success` | `status=success` + `file` 元数据 |
| `failure` | `status=failed` + `error_message`（对应 `FAIL_EXPORT`） |
| `cancelConfirm` | `POST /export/jobs/{job_id}/cancel` |
| `abandonConfirm` | 关闭未下载任务（不产文件） |
| `empty` | 建任务前即空 → 前端直接走 `empty`，不打接口 |
| `idle` | 无任务态 |

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/v1/situation/export/config` | 按角色下发 `format_options`、`content_items`（`{key,label}`）、`max_rows`、`field_whitelist`、`columns`（冻结 §2.7） |
| `POST` | `/v1/situation/export/jobs` | 建任务 `{ format, content_keys, filter:<§1.3> }` → `job_id` |
| `GET` | `/v1/situation/export/jobs/{job_id}` | 状态轮询：`status` + `stages[]`（事实状态）+ 成功时 `file` |
| `POST` | `/v1/situation/export/jobs/{job_id}/cancel` | 取消（仅 `queued` / `running` 可取消） |
| `GET` | `/v1/situation/export/jobs/{job_id}/download` | 下载（短时签名 URL 或 302；仅 `success` 且未过期） |

```json
{
  "code": 0,
  "data": {
    "role": "analyst", "max_rows": 50,
    "format_options": ["CSV"],
    "content_items": [ { "key": "factor", "label": "科创要素" }, { "key": "event", "label": "科创事件" } ],
    "field_whitelist": ["名称","类型","地域","时间","重要性","指标值","摘要"],
    "columns": ["name","type","region","time","importance","metric","summary"]
  }
}
```

```json
{
  "code": 0,
  "data": {
    "job_id": "EX-20261014-0001",
    "status": "running",
    "row_count_planned": 50,
    "filter_echo": { "region_scope": "global", "start_year": "2020", "end_year": "2026" },
    "stages": [
      { "key": "collect",  "label": "整理筛选条件",   "state": "done" },
      { "key": "validate", "label": "校验字段白名单", "state": "done" },
      { "key": "slice",    "label": "截取有限结果集", "state": "in_progress" },
      { "key": "generate", "label": "生成 CSV 文件",  "state": "todo" },
      { "key": "ready",    "label": "准备下载",       "state": "todo" }
    ],
    "created_at": "2026-10-14T10:00:00+08:00"
  }
}
```

边界与硬约束：

- **禁假进度**：demo `EXPORT_FLOW_PROGRESS_STEPS`（`exportFlow.js` L1–L8）的 10/30/55/75/90/100 是**演示动画**；契约只返五阶段事实状态（`done` / `in_progress` / `todo`），**不返百分比**（与 D4 `IngestingBadge` 同一诚实性口径）。
- **行数硬闸按角色**（executive 20 / analyst·governance 50 / default 30）：超限**直接 400**，不静默截断（前端先按 `max_rows` 提示）。
- **审计落服务端**（`{user, role, filter, columns, row_count, created_at}`），前端 `localStorage` 审计键（`EXPORT_AUDIT_STORAGE_KEY`）废弃。
- `job_id` 按登录用户隔离，跨用户访问 → **403**；`success` 但已过期 → **410**，前端提示重新导出。

---

## 4. D9 血缘与 Mock 先行

| 规则 | 要求 |
|---|---|
| `metric_id` | 每个统计数字必须能挂 `metric_id`（走 `/metrics/v1/catalog`），前端 ⓘ 弹卡含 8 件套 + 四维就绪度四行；镜像为空时 **不传 `metric_id`**，只留 ⓘ |
| 就绪度 | D1/D2/D3/D4 全部只读消费，前端禁「改绿」；D4 `mock` → 🧪 MockBadge |
| ADS 契约面 | 先冻 ADS 标准表，由 **Python 写 Mock 至 ADS**（D7）；**禁 Java/前端造数** |
| 前端 Mock 开关 | `USE_MOCK=true` 时按模块冻结 demo 种子（头注释标真源路径）；`USE_MOCK=false` 零 mock 直连网关；CI 构建显式 `USE_MOCK=false` |

⚠️ demo `data.js` 中 `factorItems.count`、`sharedMapRegions.detail`（`data.js` L346 起按 `rank` 线性推导）、`timeline.events` 文案、`App.jsx` L1572 事件坐标抖动**均为演示硬编码**，**禁止**直接当真源灌库；须由 Python 按 ADS 标准表写 Mock，并在 ⓘ/🧪 中如实标注。

---

## 5. 缺数降级与空态（统一语义，三层一致）

| 场景 | 后端 | 前端 |
|---|---|---|
| 该域无 ADS 数据（D3 `none`） | `records=[]` + `empty_reason=no_source` + 文案取自 `{模块}/data-gap-catalog.yaml` | 空态卡片；**禁止**填演示值参与展示/计分 |
| 筛选后无命中 | `empty_reason=filter_empty` | 「当前条件下无结果，请放宽条件」 |
| 样本口径未覆盖 | `empty_reason=sample_empty` | 明示「样本口径，非全域」 |
| 接口未就绪（过渡态） | 404 / 501 | 走只读镜像模块 + 🧪 MockBadge，不伪绿 |

三层同语义：前端禁生成 → 页面层本地空结果 → Java 侧硬闸不查 ADS。

---

## 6. 实现落点与未决项

| 仓 | 做什么 |
|---|---|
| 编排仓（本文件） | 契约真源 |
| `lumen-svc-platform` | 建议新增 `gkxlumen-display`（基线段 Wave4）或暂落 `gkxlumen-innov`；只读 `gkxlumenx_ads`；**带写面**（§3.7 收藏/标签、§3.8 导出任务 + 审计）读写 `app_user` 家族 |
| `lumen-ui-science-pc` | 按本文件对接；底座单 `FE-TS-S01`、整页单 `FE-TS-01A`（human:孔东） |
| Python（`lumen-algo-py` / `lumen-etl-es-py`） | 舆情/事件三方源 → ADS 映射（D3）；指标计算写 ADS；**本单不含算法任务** |

**未决项（不伪闭合）**

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | 服务归属：`gkxlumen-display`（Wave4，未建）还是先落 `gkxlumen-innov` | M0 拍板（human:徐腾强） |
| U2 | 服务内路径前缀 `/v1/situation/**` 与 DTO 命名（`snake_case` 沿用 `API-CHAIN-INDUSTRY-CLUSTER.md` 风格） | M0 拍板 |
| U3 | ADS 标准表**表名与字段定稿**（建议清单见 §9.1，待数据侧复核定名） | M0 + 数据侧（`系统-02` GDF）· 落 `BE-TS-S02` |
| U4 | 舆情/事件三方源映射（D3）与真源事件流上线时点 | `DATA-TS-S01`，随三方库 |
| U5 | 天地图 key 内网可达性（R1）；确认前 dev 用公网瓦片 | devops |
| U6 | M1 指标 `metric_id` 清单与登记（王惠 8 件套） | `ALL-TS-D9`，随各批评审 |
| U7 | 导出行数/字段白名单是否与客户口径（Q-* 待确认）一致（D1 暂照搬 demo） | 客户决策清单 |
| U8 | 收藏 `status` 取值枚举与 `source_module` 取值清单（demo `followItems.js` 语义未定） | M0 前端侧（human:孔东）核对 |

---

## 7. 自检（M0 前）

- [ ] 11 要素 `factor_key` 与 `data.js` L250 逐字一致（无自造 key）
- [ ] 三条筛选字典（事件类型/重要性/时间粒度）与 `App.jsx` L388/L395/L400 逐字一致
- [ ] 详情四 `kind`（`map-object` / `map-warning` / `timeline-event` / `factor`）齐备，五段 key/标题与 `mapObjectDetail.js` L39 一致；缺数不省略段
- [ ] 预警三卡与 `warning_level` 枚举（§2.8）与 `mapDisplay.js` L65–L75 / `mapObjectDetail.js` L496–L500 一致
- [ ] 导出：角色策略（20/50/50/30）、列白名单（§2.7）、8 相位映射（§3.8）与 `App.jsx` L408–L423 / `exportFlow.js` 一致
- [ ] 收藏 `follow_key` 组成与 `followItems.js` 对齐；跨页收藏语义已写明（不合并）
- [ ] ADS 标准表建议清单（§9.1）覆盖 11 要素/载体/指标/事件/舆情五域；M2–M9 清单（§9.2）齐备
- [ ] 全部接口落在 `/display/**` 网关前缀；前端不写第二份字典
- [ ] 调用链未越层（Java 不算算法、不写 ADS、不直连 nGQL）；无 `demo-*` 回落
- [ ] 缺数语义四态齐备；`metric_id` 空时不传参
- [ ] D3 `none` 指标不参与展示/计分
- [ ] 演示兜底内容（模拟关系行 / 关联主体 / 坐标抖动 / 假进度百分比）**均已在契约中显式禁止**

## 8. 会签记录（M0 待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |

> 会签通过后本文件冻结为正式契约，并在 `BE-TS-CONTRACT-01` handoff 内回填 M0 评审结论；U1–U8 逐项落结论，未决项不得以默认值静默通过。

---

## 9. 附录

### 9.1 ADS 标准表建议清单（DoD 第 4 条 · 规划 §5 `BE-TS-S02`）

| # | 域 | 建议表名（前缀待数据侧定名） | 关键字段 | 消费接口 | D3 就绪度 |
|---|---|---|---|---|---|
| 1 | 科创要素 | `ts_factor_stat`（要素 × 地域 × 年 计数） | `factor_key, region_scope, year, cnt, source_code` | §3.1 / §3.3 | 部分待映射 |
| 2 | 载体 / 对象 | `ts_object` | `object_id, object_type, name, lng, lat, region_key, factor_key, heat_level, warning_level` | §3.2 / §3.4 | 项目内结构 |
| 3 | 指标 | `ts_object_metric`（对象指标 × 年份序列） | `object_id, metric_key, metric_id, year, value, unit` | §3.4 metrics / trend | 对齐 `/metrics/v1/catalog` |
| 4 | 事件 | `ts_event` | `event_id, date, time_granularity, event_type, importance_level, title, text, lng, lat, source_name, original_url` | §3.5 | **D3 三方源映射待定（`DATA-TS-S01`）** |
| 5 | 舆情 | `ts_opinion`（舆情明细，供事件聚合） | `opinion_id, event_id, source, publish_at, influence, sentiment, url` | §3.5 聚合 | **D3 待定** |

**Mock 先行（D7）**：由 Python（`lumen-etl-es-py` / `lumen-algo-py`）按本清单写 Mock 至 ADS，Java 只读；**禁止 Java / 前端造数**。事件与舆情两域在 D3 未落前，接口按 §5 返 `empty_reason=no_source`，前端显 🧪 与「待接入」。

### 9.2 M2–M9 接口用途清单（DoD 第 3 条：按批冻结）

| 模块 | 接口用途（规划 §4 摘要） | 批量 / 冻结时点 |
|---|---|---|
| M2 科学技术全景 | 技术点图谱（节点/边/类型/层级）；关键路径与节点标记；关键实体检索与详情（关联强度/评分）；图谱编辑提交（增删改 + 历史 + 版本） | 批 2，**M2/M3 须在批 2 开工前冻结** |
| M3 技术发展跟踪 | 当前评估结果（综合/四方法/阶段/分项）；历史评估矩阵（四期 × 四方法）；参数模板（5 套）；评估方法知识（4 法 + 案例） | 批 2 |
| M4 全球创新监测 | 创新成果列表（类型/领域/坐标 + 筛选）；实时数据（4 KPI + 趋势 + 领域，轮询增量）；载体排行（多维 + 五年分）；监测预警 + 推送记录；城市能力（10 城五维 + 政策建议） | 批 3 |
| M5 湾区创新监测 | 湾区成果落点（11 城 67 点）；创新能力（四维 + 历史 + 构成）；SWOT 四象限 + 因素；指标数据（6 指标 + 11 城构成 + 口径） | 批 3 |
| M6 深圳创新监测 | 深圳载体（60 条 + 多筛选 + 排名）；指标体系（10 系三级 + 构成 + 历史序列）；领域分布（8 领域 × 4 指标 + 空间集聚）；城市对标（8 城四维 + 缺口 + 外推） | 批 3 |
| M7 科技创新评估 | 评估结果（综合 + 四维 + 建议）；历史报告（4 条 + 归档）；维度体系配置（四维 + 二级指标 + 权重） | 批 4 |
| M8 科技指数 | 指标树（三级 + 权重 + 赋权方法 + 版本）；区域指数（34 省五年）；专家数据（20 人 H 指数 + 活跃度）；指数趋势；成果排行 | 批 4 |
| M9 科技发展规划 | 方向预警（6 源 + 预警卡 + 报告产物）；热点技术（8 项 + 热度序列 + 空间分布）；动态跟踪（时空切换）；本地优势对比；人才流动；资源推送；重点领域（3 集群 + 22 载体）；研究分析（四档 + 图谱 + 重叠度 + 竞争情报） | 批 4 |

**冻结规则**：本文件只冻 M1。M2–M9 逐批出 `API-TS-M<k>.md`，路径 / DTO / 枚举风格延续本文件；批 2 开工前必须先冻 M2 / M3。
