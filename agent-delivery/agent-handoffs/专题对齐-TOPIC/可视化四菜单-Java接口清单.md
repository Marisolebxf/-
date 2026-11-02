# 可视化四页 · Java 接口说明

> **任务**：`SYSINT-03-VIZ-API-L01`。监管 `human:徐滕强`。实现仓 `lumen-svc-platform`，门面 `gkxlumen-topic`。  
> **前端**：`SYSINT-03-VIZ-FE-L01`（`human:孔东`）。页面在 `lumen-ui-topic`。Mock 打开时用 `src/views/viz/vizMock.ts`、`src/views/policy/policyNewsDisplayModel.ts` 演示；关掉 Mock 后，新接口里没有的块留空。  
> **本文**：给 Java 实现用的接口说明。新接口按页面收成 4 条。旧接口只复用，不改路径、不改已有字段。

调用链：浏览器 → 网关 → Java → 只读 ADS。要计算或生成文字时，Java 再调 Python `/internal/*`。浏览器不直连 Python。

## 0. 共同约定

网关包一层。前端只使用 `data`。

```json
{ "code": 0, "msg": "ok", "data": {} }
```

`code = 0` 为成功。下面的 JSON 都是 `data`。

新接口按块给空态，一块没有数据时其他块照常返回：

```json
{ "empty": true, "reason": "没有已注册口径" }
```

- 集合用空数组。数值没有就用 `null`，不用 `0` 填。
- `reason` 写一句人能读的原因。
- 没有坐标的点不要放进地图数组。
- 演示数据里的数字只说明字段类型，不能当作返回样例。
- 统计数若已有 `metric_id`，放在对应块上。没有就不填。
- 字段名：企业、服务、政策沿用 `snake_case`。产业查询参数沿用 `industryId`、`chainId`、`objectId`。

计算类（预测、SWOT 文字、同行归一化、政策事件抽取、词频、聚类、影响深度）由 Python 算。Python 返回空，Java 就把该块标空，不在 Java 里写死数。

筛选能在前端完成的，不另做参数、不另做接口：散点的行业和地区、需求的行业和规模、服务类型、词云的行业和区域、政策关键词里对重大事件的过滤。

---

## 1. 总表

已有 7 个，不改。新接口 4 个，每个页面一个。

| 编号 | 方法 | 路径 | 页面 |
|---|---|---|---|
| R-1 | POST | `/enterprise/topic/v1/search/query` | 企业搜索和列表 |
| R-2 | POST | `/enterprise/topic/v1/profile/finance/trend` | 新接口未接上时的营收、利润 |
| R-3 | POST | `/enterprise/topic/v1/profile/competitiveness` | 新接口未接上时的规模、链位、竞争力分 |
| R-4 | GET | `/chain/topic/v1/industry/overview` | 产业指标卡 |
| R-5 | GET | `/chain/topic/v1/industry/panorama/snapshot` | 产业链节点和边 |
| R-6 | POST | `/svc/topic/v1/service-portal/region-map` | 新接口未接上时的机构分布 |
| R-7 | GET | `/policy/topic/v1/policy/search` | 政策时间轴正文 |
| R-7b | GET | `/policy/topic/v1/policy/indicators?kind=all` | 影响范围柱，读 `national` |
| V-I | GET | `/chain/topic/v1/industry/viz` | 产业全景：规模、热力、结构、饼图、预测 |
| V-E | POST | `/enterprise/topic/v1/profile/viz` | 企业发展：卡片、散点、时间轴、财务、SWOT、同行 |
| V-S | POST | `/svc/topic/v1/service-portal/viz` | 产业服务：机构、需求、匹配、效能、案例 |
| V-P | GET | `/policy/topic/v1/policy/viz` | 政策：重大事件、词云、聚类、影响深度 |

导出 CSV、热力着色、时间轴展开收起、饼图切换、聚类图布局，都由前端用这 4 个包里的字段完成。

---

## 2. 已有接口：页面实际读取的字段

### R-1 企业搜索

`POST /enterprise/topic/v1/search/query`

```json
{
  "user_id": "当前用户",
  "keyword": "半导体",
  "sort_field": "",
  "sort_order": "desc",
  "page": 1,
  "size": 10
}
```

| 字段 | 用途 |
|---|---|
| `list[].org_id` | 行主键，点行后作为 V-E 的 `org_id` |
| `list[].name_cn` | 企业名称 |
| `list[].province`、`list[].city` | 地区 |
| `list[].industry_class_name`，没有则 `industry_class` | 行业 |
| `total`、`page`、`size` | 分页 |

### R-2 财务趋势

`POST /enterprise/topic/v1/profile/finance/trend`，体为 `{ "org_id": "" }`。

读 `series[]` 的 `year`、营收（`main_business_revenue`，没有则 `operating_revenue`）、利润（`pure_profit`，没有则 `total_profit`）。研发投入在 V-E 的 `finance`，不往这条序列加字段。

### R-3 竞争力

`POST /enterprise/topic/v1/profile/competitiveness`，体同上。

读 `enterprise_scale`、`chain_position_text`、`competitiveness_score`。同行五维在 V-E 的 `peers`。

### R-4 产业总览

`GET /chain/topic/v1/industry/overview?industryId=&chainId=&objectId=`

读 `kpis[]`（`metric_id`、`metric_name_zh`、`metric_label`、`value`、`value_unit`）。区域热力改走 V-I 的 `heat`。本接口继续只供指标卡。

### R-5 产业链快照

`GET /chain/topic/v1/industry/panorama/snapshot`，参数与 R-4 相同。

读 `dataset.nodes[]`（`id`、`name`、`stage`、`status`）和 `dataset.edges[]`（`source`、`target`、`relation`）。占比和关键环节在 V-I 的 `structure`，`node_id` 对 `nodes[].id`。不要把占比写进 `name`。

### R-6 服务机构区域图

`POST /svc/topic/v1/service-portal/region-map`

```json
{ "industry": "", "chainId": "", "year": null }
```

读 `china[]` / `global[]` 的 `name`、`count`、`lat`、`lng`。不增加服务类型参数。V-S 接上后，分布、类型、疏密以 V-S 为准。V-S 的机构集合在同一 `industry`、`chainId` 下与本接口同一口径。

### R-7 政策检索与影响范围

`GET /policy/topic/v1/policy/search?keyword=&limit=50`

时间轴读 `items[]`：`policy_id`、`title`、`summary`（或 `abstract`）、`publish_time`（或 `publish_date` / `publishDate`）、`region_name`（或 `region`）。月 / 季 / 年的分桶在前端。

`GET /policy/topic/v1/policy/indicators?kind=all`

影响范围柱读 `national[]` 的 `province_name`、`policy_count`。`honesty.fabricated = true` 时整包不用。

---

## 3. 新接口

### 3.1 V-I 产业全景

`GET /chain/topic/v1/industry/viz`

| 参数 | 说明 |
|---|---|
| `industryId`、`chainId`、`objectId` | 与 R-4 相同 |
| `region` | 区域。缺省 `全国`。合法值来自本次返回的 `scale.regions` |
| `growthPct` | 假设年增速，百分数。页面滑块 0–20，缺省 8。只影响 `forecast` |
| `years` | 向后年数，只允许 3、4、5。缺省 5。只影响 `forecast` |

区域或滑块变化时重取这一条。`scale`、`heat`、`structure`、`mix` 只随产业和 `region` 变；`forecast` 再随 `growthPct`、`years` 变。

```json
{
  "scale": {
    "empty": false,
    "reason": "",
    "region": "全国",
    "regions": ["全国"],
    "total_unit": "亿元",
    "metric_id": "",
    "series": [{ "year": "2016", "total": null, "growth": null }],
    "events": [{ "year": "2019", "title": "", "note": "" }]
  },
  "heat": {
    "empty": false,
    "reason": "",
    "points": [{
      "id": "",
      "name": "",
      "lat": null,
      "lng": null,
      "weight": null,
      "enterprise_count": null,
      "note": ""
    }]
  },
  "structure": {
    "empty": false,
    "reason": "",
    "nodes": [{ "node_id": "", "name": "", "share": null, "is_key": false }]
  },
  "mix": {
    "empty": false,
    "reason": "",
    "行业": [{ "name": "", "value": null }],
    "领域": [{ "name": "", "value": null }]
  },
  "forecast": {
    "empty": false,
    "reason": "",
    "growth_pct": 8,
    "years": 5,
    "total_unit": "亿元",
    "series": [{ "year": "2026", "total": null }]
  }
}
```

| 块 | 字段 |
|---|---|
| `scale.series` | 按年升序。`total` 为规模，单位 `total_unit`。`growth` 为年增长率，`8.1` 表示 8.1%。页面取最近 10 年，柱是规模，折线是增长率，同一条序列也画历史曲线 |
| `scale.events` | 标在曲线上的事件。`year` 能对上某一年。没有事件时数组为空，曲线仍在 |
| `scale.regions` | 区域下拉，至少含当前 `region` |
| `heat.points` | `weight` 是本批相对密度，前端按最大值铺颜色。`enterprise_count`、`note` 是点击详情。无经纬度的不返回。无 `weight` 的不参与热力 |
| `structure.nodes` | `node_id` 对 R-5 的节点 `id`。`share` 为百分数，`46` 表示 46%。`is_key` 为真时标「关键环节」。边仍用 R-5 |
| `mix` | 行业、领域两套一次给齐，前端切换不再请求。`value` 是扇区权重 |
| `forecast.series` | 长度等于 `years`，接在规模序列最后一年之后。走 Python。算不出则本块 `empty: true`，`series: []` |

`scale.series` 为空时只把 `scale` 标空。其余块同样。

### 3.2 V-E 企业发展

`POST /enterprise/topic/v1/profile/viz`

```json
{ "org_id": "R-1 选中行的 org_id" }
```

`org_id` 为空时，六块都 `empty: true`，`reason` 为「未选择企业」。选中另一家时重取这一条。散点上的行业、地区筛选用返回的点在前端做。

```json
{
  "card": {
    "empty": false,
    "reason": "",
    "org_id": "",
    "name": "",
    "region": "",
    "industry": "",
    "scale": "",
    "score": null
  },
  "scatter": {
    "empty": false,
    "reason": "",
    "industries": [],
    "regions": [],
    "points": [{
      "name": "",
      "industry": "",
      "region": "",
      "growth": null,
      "margin": null,
      "rd": null,
      "self": false
    }]
  },
  "timeline": {
    "empty": false,
    "reason": "",
    "years": [{
      "year": "2019",
      "items": [{ "title": "", "summary": "" }]
    }]
  },
  "finance": {
    "empty": false,
    "reason": "",
    "unit": "万元",
    "revenue_basis": "主营业务收入",
    "profit_basis": "净利润",
    "series": [{ "year": "2020", "revenue": null, "profit": null, "rd": null }]
  },
  "swot": {
    "empty": false,
    "reason": "",
    "items": [
      { "key": "strength", "title": "优势", "text": "" },
      { "key": "weakness", "title": "劣势", "text": "" },
      { "key": "opportunity", "title": "机会", "text": "" },
      { "key": "threat", "title": "威胁", "text": "" }
    ],
    "expert_comment": ""
  },
  "peers": {
    "empty": false,
    "reason": "",
    "indicators": [
      { "key": "growth", "name": "营收增速", "max": 100 },
      { "key": "margin", "name": "利润率", "max": 100 },
      { "key": "rd", "name": "研发强度", "max": 100 },
      { "key": "patent", "name": "专利", "max": 100 },
      { "key": "finance", "name": "融资", "max": 100 }
    ],
    "peers": [{ "name": "", "org_id": "", "self": true, "values": [null, null, null, null, null] }]
  }
}
```

| 块 | 字段 |
|---|---|
| `card` | 五列：名称、地区、行业、规模、竞争力分。前端用这五列导出 CSV。`score` 没有则为 `null` |
| `scatter` | `growth` 营收增速作横轴，`margin` 利润率作纵轴，`rd` 研发强度作气泡大小，都是百分数。三个数有任一为 `null` 的点不返回。`self: true` 是当前企业。`industries`、`regions` 是下拉 |
| `timeline.years` | 按年升序。没有已发布事件的年份不要。页面默认展开最后一年。只返回已发布的企业关键事件 |
| `finance.series` | 营收、利润、研发投入金额，单位 `unit`。某格没有则 `null`。三条都空的年份不要。与 R-2 分开 |
| `swot` | `key` 只这四个。没有文字的象限不放入 `items`。四条和 `expert_comment` 都空则本块 `empty: true`。文字走 Python，没有材料就空 |
| `peers` | `values` 与 `indicators` 对齐，0–100，由 Python 归一化。某一维没有口径，就从 `indicators` 和每家 `values` 里同时去掉，不用 0 占位。`self: true` 是当前企业。除它之外没有同行，或当前企业各维都空，则本块 `empty: true` |

R-3 的竞争力分不能拆进 `peers`。

### 3.3 V-S 产业服务

`POST /svc/topic/v1/service-portal/viz`

请求与 R-6 相同，不加服务类型：

```json
{ "industry": "", "chainId": "", "year": null }
```

产业或链条变化时重取。服务类型、需求的行业和规模，都由前端在返回结果里筛。

```json
{
  "orgs": {
    "empty": false,
    "reason": "",
    "types": ["技术服务", "检测认证", "孵化载体", "科技金融"],
    "band_rule": "临时：weight<8 为空白，weight>20 为饱和，其余为正常。口径登记后改由指标定义",
    "items": [{
      "id": "",
      "name": "",
      "type": "",
      "region": "",
      "lat": null,
      "lng": null,
      "weight": null,
      "band": ""
    }]
  },
  "demand": {
    "empty": false,
    "reason": "",
    "rows": [{ "industry": "", "scale": "", "region": "", "count": null }]
  },
  "match": {
    "empty": false,
    "reason": "",
    "cells": [{ "region": "", "type": "", "score": null }]
  },
  "effect": {
    "empty": false,
    "reason": "",
    "orgs": [{ "name": "", "satisfaction": null, "resolution": null, "response": null }]
  },
  "cases": {
    "empty": false,
    "reason": "",
    "items": [{
      "id": "",
      "title": "",
      "org": "",
      "type": "",
      "summary": "",
      "result": ""
    }]
  }
}
```

| 块 | 字段 |
|---|---|
| `orgs` | 机构集合与 R-6 同一产业、同一链条。`types` 是类型下拉。`weight` 是供给强度，前端按本批最大值铺颜色。`band` 为 `空白`、`正常`、`饱和` 之一，与 `band_rule` 一致。无坐标的仍可进表，不打点。无 `weight` 时 `band` 为空，该点不着色。口径未写明之前，不用机构条数充当 `weight` |
| `demand.rows` | `count` 是需求条数。`scale` 用已有规模档，例如 `中小`、`大型`。`count` 为 `null` 的行不返回。页面画柱 |
| `match.cells` | `score` 为 0–100，越大越密。横轴 `region`，纵轴 `type`。没有需求侧时本块 `empty: true`。`orgs.weight` 和机构数不能当作 `score` |
| `effect.orgs` | 满意度、解决率、响应速度，都是 0–100。任一为 `null` 的机构不返回。没有这三项口径时本块为空。技术力、竞争力分不能填进这三个字段 |
| `cases.items` | 卡片用 `title`、`org`、`type`、`summary`。抽屉用 `result`。一次带上详情 |

### 3.4 V-P 政策新闻

`GET /policy/topic/v1/policy/viz`

无查询参数。关键词、词云的行业和区域都在前端筛。普通政策时间轴仍用 R-7，影响范围柱仍用 R-7b。页面加载时取这一条。

```json
{
  "events": {
    "empty": false,
    "reason": "",
    "items": [{
      "time": "2024-03-18",
      "title": "",
      "region": "",
      "detail": "",
      "note": "",
      "major": true,
      "policy_id": ""
    }]
  },
  "terms": {
    "empty": false,
    "reason": "",
    "updated_at": "",
    "items": [{ "text": "", "weight": null, "industry": "", "region": "" }]
  },
  "clusters": {
    "empty": false,
    "reason": "",
    "items": [{
      "name": "",
      "items": [{ "title": "", "policy_id": "" }]
    }]
  },
  "depth": {
    "empty": false,
    "reason": "",
    "stages": [
      { "name": "市场", "value": null },
      { "name": "企业", "value": null },
      { "name": "人才", "value": null }
    ]
  }
}
```

| 块 | 字段 |
|---|---|
| `events.items` | `time` 为 `YYYY-MM-DD`，并进 R-7 的同一条时间轴。`detail` 是详细内容，`note` 是专家解读，点开后分两段。`major` 都是 `true`。`policy_id` 能对上原文时填写，打开仍走已有 `GET /policy/topic/v1/policy/docs/{id}`。对不上就空字符串。时间轴上不把这两段正文铺开 |
| `terms.items` | `weight` 是相对词频，越大字越大。字号由前端换算。`weight` 为 `null` 或 `text` 为空的不返回 |
| `clusters.items` | 一个元素是一个簇，`items` 是该簇条目。前端画中心点和周围点，点击后列出条目。坐标不返回。没有条目的簇不返回。`policy_id` 规则与事件相同 |
| `depth.stages` | 顺序固定为市场、企业、人才。`value` 是同一口径下的影响深度，页面画折线。某一层没有数就不要这一层。三层都没有则本块 `empty: true`。政策条数不能填进 `value` |

事件、词频、聚类、影响深度走 Python。某一块没有结果，只标这一块。

---

## 4. 页面对照

| 页面上的操作 | 接口 |
|---|---|
| 搜索、点一家企业 | R-1，随后 V-E |
| 卡片、导出、散点筛选、时间轴收起、三条财务线、SWOT、同行雷达 | V-E 一次返回，筛选和收起在前端 |
| 指标卡 | R-4 |
| 规模、增长率、历史曲线、事件标线、热力、环节占比、两套饼图 | V-I |
| 改区域或增速滑块 | 再次 GET V-I |
| 产业链的点和边 | R-5，占比用 V-I 的 `structure` |
| 机构地图、类型、空白饱和、需求柱、匹配热力、效能、案例 | V-S 一次返回，类型和需求筛选在前端 |
| 未接上 V-S 时的机构点 | R-6 |
| 时间轴正文、月季年、关键词 | R-7；重大事件并入 V-P，关键词也滤 V-P 的事件 |
| 词云筛选、聚类点击、影响深度 | V-P |
| 各省政策量 | R-7b |

---

## 5. 实现约束

1. 第 2 节旧接口的路径、请求和已有字段保持现状。门户四页、企业详情继续按原契约调用。
2. 新展示只增加 V-I、V-E、V-S、V-P 四条。研发投入、服务类型、预测、SWOT、同行、需求、匹配、效能、案例、政策事件和主题都在这四条的块里。
3. Java 只读 ADS，不写 ADS，不在门面里做预测、归一化或文本生成。
4. 某一块无行、无口径或 Python 无结果，只把该块标 `empty: true` 并给 `reason`，同一次响应里的其他块仍返回。
5. 联调每条新接口准备一份「各块皆空」和一份「有行」的 `data`。有行的数来自 ADS 或 Python，不抄前端 Mock。
