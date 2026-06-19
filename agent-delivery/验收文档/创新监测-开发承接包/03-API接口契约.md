# 03 · API 接口契约（Java 仓）

> **读者**：Java 后端、前端
> **约定**：
> - Base URL：`/api/innov/v1`；鉴权沿用平台统一网关（Header `Authorization`）；
> - 响应包络：`{ "code": 0, "msg": "ok", "data": ... }`；分页统一 `pageNum/pageSize`，返回 `{total, list}`；
> - 时间格式 `yyyy-MM-dd HH:mm:ss`；枚举值与 01 文档字典表一致；
> - 每个接口标注数据来源 ADS 表。Java 不做计算，只做查询、聚合（SQL 级）、缓存与用户态逻辑。

---

## 1. M1 科创事件

### 1.1 GET /events  事件列表/地图点位
来源：`ads_innovation_event`

| 参数 | 类型 | 说明 |
|---|---|---|
| startTime / endTime | string | 时间范围（需规：日/周/月/季/年由前端换算） |
| eventTypes | string | 逗号分隔，见 dim_event_type |
| importanceLevels | string | 1,2,3 |
| cityCode / adminCode | string | 区域筛选 |
| bbox | string | 地图视野 `minLng,minLat,maxLng,maxLat`（点位模式必传） |
| keyword | string | 标题/摘要检索（走 ES，见 05 文档） |
| sortBy | string | importance_score(默认) / event_time |
| mode | string | `list` / `geo`（geo 模式仅返回轻量点位字段） |

geo 模式响应（GeoJSON FeatureCollection，前端直接喂地图）：
```json
{ "type": "FeatureCollection", "features": [
  { "type": "Feature", "geometry": {"type":"Point","coordinates":[114.05,22.54]},
    "properties": {"eventId":"e1","eventType":"financing","importanceLevel":1,
                   "importanceScore":87.5,"title":"…","eventTime":"2026-06-01 10:00:00"} } ] }
```

### 1.2 GET /events/heatmap  热力图聚合
来源：`ads_innovation_event` 按 geohash/admin 聚合。参数同 1.1（无 bbox 时按 adminLevel 聚合）；返回 `[{lng,lat,weight}]` 或 `[{adminCode,count}]`。

### 1.3 GET /events/{eventId}  事件详情
返回全字段 + `importanceDetail`（分级可解释明细）+ `sourceRefs`（原文出处）。

### 1.4 GET /events/{eventId}/relations  关联分析
来源：`ads_event_relation`。返回 `[{relType:"event|org|person", relId, relName, relDesc, score}]`。

### 1.5 GET /events/stats  时间分布对比
参数：`granularity=day|week|month|quarter|year`，`compare=ranges`（多时间段对比）。返回各时间桶计数，供时间轴/对比图。

### 1.6 POST /events/{eventId}/export ｜ POST /events/{eventId}/share
用户态：生成导出文件/分享链接，记录 `app_user.export_record`。

## 2. M2 创新点落图与赋分

### 2.1 GET /graph/domains  领域树
来源：`dim_tech_domain`。返回树结构（懒加载 `parentId` 参数）。

### 2.2 GET /graph/subgraph  领域子图（落图展示）
参数：`domainId`（必填）、`depth`（默认2）、`nodeTypes`、`limit`（默认200，按影响分截断）。
来源：`dwm_graph_node/edge` + `ads_node_influence`。
```json
{ "nodes": [{"nodeId":"n1","nodeType":"org","name":"…","influenceScore":92.1,"rank":3}],
  "edges": [{"src":"n1","dst":"n2","edgeType":"coop","weight":0.8}] }
```

### 2.3 GET /graph/nodes/{nodeId}/influence  节点影响分详情
来源：`ads_node_influence`。返回当前分、排名、`scoreDetail` 分项、近 12 期历史。

### 2.4 GET /graph/influence/rank  影响分排行
参数：`domainId, nodeType, period, pageNum/pageSize`。

### 2.5 GET /graph/points/{pointId}/mapping  创新点落图结果
来源：`ads_innovation_point_map`。返回该创新点映射的节点、关系类型、置信度。

## 3. M3 创新载体排行

### 3.1 GET /carriers/rank
来源：`ads_carrier_index`。参数：`dimension=total|domain|region`、`domainId`、`adminCode`、`period`、分页。返回 rank、indexScore、subScores。

### 3.2 GET /carriers/{carrierId}
详情：基本信息（`dim_carrier`）+ 指数趋势（多期 `ads_carrier_index`）+ 成果列表（`dwm_org_achievement_year` 经载体关系折算）。

### 3.3 GET /carriers/index-method
来源：`cfg_index_weight`（index_type=carrier，active 版本）。返回 `methodDesc` + 权重树——满足需规"用户可查看指数计算方法和权重设置"。

### 3.4 GET /carriers/compare
参数：`carrierIds`（2–5 个）。返回对比矩阵（成果/指数/趋势）。

## 4. M4 城市创新能力

### 4.1 GET /cities/rank  城市排名
来源：`ads_city_index`。参数：`scope=global|domestic`、`period`、分页。

### 4.2 GET /cities/{cityCode}  城市详情
指数 + 四子指数 + `indicatorValues` 指标明细 + 近 N 期趋势。

### 4.3 GET /cities/compare  对标分析
参数：`cityCodes`（2–5）。返回子指数雷达数据 + 指标级差值表。

### 4.4 GET /cities/{cityCode}/advice  政策建议
来源：`ads_report`（report_type=city_policy_advice，review_status=1）。返回 Markdown 正文。

### 4.5 GET /cities/index-method  同 3.3（index_type=city）

## 5. M5 创新影响预测

### 5.1 GET /forecast/domain/{domainId}  领域趋势
来源：`ads_impact_prediction`（target_type=domain）。返回历史序列 + 预测点 + `ciLower/ciUpper`（置信区间，前端画带状区域）。`forecastMode` 字段透传（trend|momentum，对应 G-25 降级）。

### 5.2 GET /forecast/contributions  贡献度排行
参数：`domainId, period, pageNum/pageSize`。来源同上（target_type=point），返回创新点、contribution、explainPath。

### 5.3 GET /forecast/bursts  突变/颠覆性技术
来源：`ads_topic_burst`。参数：`domainId, period`。

## 6. 订阅与推送（用户态，Java 自治）

| 接口 | 说明 |
|---|---|
| POST /subscriptions | 创建订阅 `{subType: domain/carrier/city/keyword, subTarget, frequency, channels}` |
| GET /subscriptions ｜ DELETE /subscriptions/{id} | 管理 |
| GET /push/history | 推送历史 |
| POST /monitor-models | 监测模型设置（指标、阈值、频率）→ Java 定时扫描 ads 增量触发 |

## 7. 通用

| 接口 | 说明 |
|---|---|
| GET /dict/event-types | `dim_event_type`（颜色/名称给前端图例） |
| GET /dict/regions | 区划树 `dim_admin_division` |
| GET /dict/cities | `dim_city` |
| GET /meta/data-status | 各 ADS 表最近更新时间、当前 model_version、降级开关状态（运维页用） |

## 8. 非功能约定

- 地图类接口 P95 ≤ 500ms：geo/heatmap 接口必须走缓存（Redis，key=参数哈希，TTL 10min）+ bbox 强制；
- 列表关键词检索走 ES 索引（Python 侧同步写入，见 05 文档），其余走 MySQL；
- 所有排行接口 period 缺省取最新快照期；
- 错误码：`40x` 参数/权限，`5001` 数据未就绪（ADS 快照缺失时返回，前端展示占位）。

---
**文档版本**：V1　**编制日期**：2026-06-11
