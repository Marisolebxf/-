# 专题前端生产缺口 · 接口总文档（本轮增补）

- 时间：2026-09-02
- 作者：api-agent（监管：human:侯佳伟）
- 任务：`API-TOPIC-FE-JAVA-GAP-L01` + `API-TOPIC-FE-JAVA-GAP-SVC-L01`
- 仓库：`lumen-svc-platform` + `lumen-topic-py` + `lumen-algo-py`
- 格式对齐：`企业战略分析-ENT/API-ENT-full-catalog.md`（一份文档，按模块分章）
- 企业存量 141 端点仍以 `API-ENT-full-catalog.md` 为准；本文只记本轮新增 / 变更
- 范围：本次 **P0 新能力 + P2 已有路径补字段**。**P1 本次不做**（见文末 §9）
- 口径未定项（Q016 对标城、Q-SVCCHAIN-* 等）字典可空，不替甲方拍板

| 档 | 含义 | 本次 |
|---|---|---|
| **P0** | 没有接口则页面只能写死或刷新丢失 | 已实现，推 `origin/dev` |
| **P1** | 没有也能用，对齐 Demo / 多端时再补 | **本次不做** |
| **P2** | 路径已有，补字段后对应区域才能展示 | 已补别名 / 空槽；缺数据不造数 |

## 目录

| 章 | 模块 | 编号 |
|---|---|---|
| §4 | 企业分析 | #G1–G11 |
| §5 | 产业链分析 | #C1–C6 |
| §6 | 服务链分析 | #S1–S16 |
| §9 | 已实现 / 待确认 / 后续补（含改 Java 还是 Python） | — |

## 1. 路由拼接规则

```text
gateway地址 / {网关前缀} / {Controller @RequestMapping} / {方法映射}
```

| 段 | 当前值 |
|---|---|
| gateway地址 | 外网 `http://111.198.38.90:50199`（内网 NodePort `http://10.50.69.111:30899`） |
| 企业 | `/enterprise` |
| 产业链 | `/chain` |
| 服务链 | `/svc` |
| 任务中心 / 评估辅助 | `/topicAsync`（StripPrefix=1） |

分析任务 create/status/result/**删除** 三模块共用 `/topicAsync/topic/v1/analysis`。删除 ≠ cancel。

## 2. 调用链（总览）

```text
企业 P0 写库：前端 /enterprise/.../compare-basket/{recruit|cultivate}-candidates → Java MySQL
企业 P0 字典：前端 /enterprise/.../meta/policy-orientations → Java Feign → lumen-topic-py
任务软删：前端 DELETE /topicAsync/.../tasks/{taskId} → Java status=deleted
企业 P2：评估/结果/KPI → Java 透传 → lumen-topic-py（补别名）

产业链 P0/P2：前端 /chain/topic/v1/industry/** → Java Feign → lumen-algo-py /internal/v1/chain/**

服务链 P0 字典/读面：前端 /svc/** → Java Feign → lumen-topic-py /internal/gkx-svc/**
服务链 P0 对比篮：前端 /svc/.../compare-basket → Feign enterprise → MySQL svc_compare_basket_item（不写 ADS）
```

## 3. 端点总览（三模块）

见各章 §4.3 / §5.3 / §6.3。编号 **#G / #C / #S** 仅本缺口文档；存量编号仍以 `API-ENT-full-catalog.md` 为准。

---

## 4. 企业分析

### 4.0 前端导读

> 分析任务中心仍共用一套 create/status/result。本轮只多一个 **DELETE 软删**，不要和 **cancel** 混用。  
> 网关：对比篮 / 字典 / 重点分析 / 深圳现状 → **`/enterprise`**；任务中心 / 评估辅助 → **`/topicAsync`**。

#### 该调哪些接口

| 业务 | 本轮新增 / 变更 | 生命周期 | 不要串线 |
|---|---|---|---|
| 引入企业推荐 · 候选名单 | **#G1 #G2** DELETE 招引候选 | 列表/加入仍走 catalog #98–99 | 不是对比篮 `items` |
| 培育企业推荐 · 候选名单 | **#G3 #G4** DELETE 培育候选 | 列表/加入仍走 catalog #100–101 | 同上 |
| 培育条件「政策导向」 | **#G5** 字典 | 选中值随 `talent_recommend` 任务提交 | 不要前端写死四项 |
| 分析记录「删除」 | **#G6** DELETE 任务 | 取消仍走 catalog #107 | 运行中先 cancel 再软删 |
| 企业评估 · 指标体系 | **#G7** 指标树补别名（原 #114） | 任务仍走 #102–109 | |
| 企业评估 · 维度对比 | **#G8** compare 补中文维名（原 #116） | | 不是对比篮 `#14` |
| 评估 / 引育结果页 | **#G9** 结果包别名（原 #105） | | 风险图谱本轮未 enrich |
| 重点分析 / 深圳页头时点 | **#G10 #G11** `dataTime`（原 #122 / #132） | | 现为显式 `null` |

#### 调用方图例

| 标注 | 含义 |
|---|---|
| **前端** | 浏览器业务页 |
| **Python** | 仅内部；前端勿调 `/internal/**` |

#### 容易混淆

| 容易当成 | 实际 |
|---|---|
| DELETE 任务 = 取消 | **#G6 软删** ≠ **#107 cancel**。运行中删除会先 cancel |
| 政策导向 = 评估指标 | **#G5** 只服务培育条件栏 |
| 结果 `dataTime` 有值 | 算法/`updated_at` 没有则 **不写死日期**，KPI 页显式 `null` |

### 4.1 路由

```text
gateway地址 / {EnableOpenApi value} / {Controller @RequestMapping} / {方法映射}
```

| 段 | 来源 | 当前值 |
|---|---|---|
| gateway地址 | Swagger / 网关基址 | 外网 `http://111.198.38.90:50199` |
| 企业门面网关前缀 | Gateway enterprise | `/enterprise` |
| ANALYSIS-CORE / EVAL 网关前缀 | Gateway async | `/topicAsync`（StripPrefix=1） |
| Controller 前缀 | `@RequestMapping` | 对比篮 `/topic/v1/compare-basket`；字典 `/topic/v1/search/meta`；任务 `/topic/v1/analysis`；评估 `/topic/v1/evaluation` |

示例：`DELETE gateway地址/enterprise/topic/v1/compare-basket/recruit-candidates/{enterprise_code}?user_id=u-1`

### 4.2 调用链

```text
# P0 候选删除（Java 自建 MySQL）
前端 → /enterprise/topic/v1/compare-basket/{recruit|cultivate}-candidates/**
  → CompareBasketController → CompareBasketService
  → MySQL gkxlumenx_topic_enterprise（ent_recruit_candidate / ent_cultivate_candidate）

# P0 政策导向（Java 透传 Python）
前端 → /enterprise/topic/v1/search/meta/policy-orientations
  → EnterpriseMetaDictController → Feign → lumen-topic-py
  → POST /internal/gkx-search/meta/policy-orientations

# P0 任务软删（Java；运行中会先 Feign 算法 cancel）
前端 → /topicAsync/topic/v1/analysis/tasks/{taskId} DELETE
  → AnalysisTaskController.delete → status=deleted
  → list 默认排除 deleted

# P2 评估 / 结果 / KPI（路径已有，Python 补字段，Java Map 透传）
前端 → /topicAsync/topic/v1/evaluation/indicators|tasks/compare
  → RemoteTopicAsyncAiPythonClient → /internal/gkx-ai/evaluation/**
前端 → /topicAsync/topic/v1/analysis/tasks/{taskId}/result
  → MinIO / AI Python result_data（评估/引育 enrich 在 Python）
前端 → /enterprise/topic/v1/key-analysis/overview-kpi
前端 → /enterprise/topic/v1/sz-status/chain-kpi
  → Feign → /internal/gkx-search/**
```

### 4.3 端点总览

> 编号 **#G*** 仅本缺口目录。存量编号仍以 `API-ENT-full-catalog.md` 为准。

| # | 分组 | 网关路径（相对 `{GW}`） | Python 下游 | 请求对象 | 返回 data 类型 | 动作 |
|---|---|---|---|---|---|---|
| G1 | 对比篮·P0 | `DELETE /enterprise/topic/v1/compare-basket/recruit-candidates/{enterprise_code}` | — | `user_id` query | `Void` | 新增 |
| G2 | 对比篮·P0 | `DELETE /enterprise/topic/v1/compare-basket/recruit-candidates/batch` | — | `BatchRemoveRequest` | `Void` | 新增 |
| G3 | 对比篮·P0 | `DELETE /enterprise/topic/v1/compare-basket/cultivate-candidates/{enterprise_code}` | — | `user_id` query | `Void` | 新增 |
| G4 | 对比篮·P0 | `DELETE /enterprise/topic/v1/compare-basket/cultivate-candidates/batch` | — | `BatchRemoveRequest` | `Void` | 新增 |
| G5 | 元数据·P0 | `POST /enterprise/topic/v1/search/meta/policy-orientations` | `/internal/gkx-search/meta/policy-orientations` | `MetaChainsDTOs.Request` | `MetaChainsDTOs.Response` | 新增 |
| G6 | 分析编排·P0 | `DELETE /topicAsync/topic/v1/analysis/tasks/{taskId}` | 运行中先走算法 cancel | `user_id` query | `AnalysisTaskEntity` | 新增 |
| G7 | 评估辅助·P2 | `POST /topicAsync/topic/v1/evaluation/indicators` | `/internal/gkx-ai/evaluation/indicators` | `EvalIndicatorsRequest` | `Map` 透传 | 补字段 |
| G8 | 评估辅助·P2 | `POST /topicAsync/topic/v1/evaluation/tasks/compare` | `/internal/gkx-ai/evaluation/tasks/compare` | `EvalCompareRequest` | `Map` 透传 | 补字段 |
| G9 | 分析编排·P2 | `GET /topicAsync/topic/v1/analysis/tasks/{taskId}/result` | AI `.../tasks/result` | `user_id` query | 任务 + 结果包 | 补字段 |
| G10 | 重点分析·P2 | `POST /enterprise/topic/v1/key-analysis/overview-kpi` | `/internal/gkx-search/key-analysis/overview-kpi` | `KeyAnalysisCommonRequest` | KPI + `dataTime` | 补字段 |
| G11 | 深圳现状·P2 | `POST /enterprise/topic/v1/sz-status/chain-kpi` | `/internal/gkx-search/sz-status/chain-kpi` | `SzStatusChainKpiDTOs.Request` | KPI + `dataTime` | 补字段 |

### 4.4 端点明细

#### 4.P0 新能力

##### G1. 移除招引候选一家
- **调用方**：**前端**（引入企业推荐分析 · 候选名单；系统对比篮 · 招引候选）
- 接口路径：`DELETE gateway地址/enterprise/topic/v1/compare-basket/recruit-candidates/{enterprise_code}`
- 服务内路径：`DELETE /topic/v1/compare-basket/recruit-candidates/{enterprise_code}`
- Python 下游：无（Java MySQL）
- 请求对象：path + query
- 返回对象：`R<Void>`
- 落库：`ent_recruit_candidate`

入参字段表：

| 字段 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `enterprise_code` | path | `String` | 是 | 企业编码 |
| `user_id` | query | `String` | 是 | 名单归属用户 |

请求示例：

```http
DELETE /enterprise/topic/v1/compare-basket/recruit-candidates/ENT-001?user_id=u-1001
```

出参字段表：

| 字段 | 类型 | 说明 |
|---|---|---|
| `code` / `msg` / `ok` | 包络 | 成功通常 `0` |
| `data` | `null` | 无业务体 |

返回 JSON 示例：

```json
{ "code": 0, "msg": null, "data": null, "ok": true }
```

##### G2. 批量移除或清空招引候选
- **调用方**：**前端**
- 接口路径：`DELETE gateway地址/enterprise/topic/v1/compare-basket/recruit-candidates/batch`
- 服务内路径：`DELETE /topic/v1/compare-basket/recruit-candidates/batch`
- 请求对象：`EnterpriseCompareBasketDTOs.BatchRemoveRequest`（snake_case）
- 返回对象：`R<Void>`

入参字段表：

| 字段 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `user_id` | body | `String` | 是 | 名单归属 |
| `enterprise_codes` | body | `List<String>` | 与 `clear_all` 二选一 | 要移除的编码 |
| `clear_all` | body | `Boolean` | 与上二选一 | `true` 清空当前用户招引候选 |

请求 JSON 示例：

```json
{ "user_id": "u-1001", "enterprise_codes": ["ENT-001", "ENT-002"] }
```

清空：

```json
{ "user_id": "u-1001", "clear_all": true }
```

出参同 #G1。

##### G3. 移除培育候选一家
- **调用方**：**前端**（培育企业推荐分析 · 候选名单；对比篮 · 培育候选）
- 接口路径：`DELETE gateway地址/enterprise/topic/v1/compare-basket/cultivate-candidates/{enterprise_code}`
- 服务内路径：`DELETE /topic/v1/compare-basket/cultivate-candidates/{enterprise_code}`
- 落库：`ent_cultivate_candidate`
- 入参 / 出参同 #G1（path 段改为 `cultivate-candidates`）

##### G4. 批量移除或清空培育候选
- **调用方**：**前端**
- 接口路径：`DELETE gateway地址/enterprise/topic/v1/compare-basket/cultivate-candidates/batch`
- 请求对象：同 #G2 `BatchRemoveRequest`
- 落库：`ent_cultivate_candidate`

##### G5. 培育政策导向字典
- **调用方**：**前端**（培育企业推荐分析 · 条件栏第二维）
- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/policy-orientations`
- 服务内路径：`POST /topic/v1/search/meta/policy-orientations`
- AI / 检索 Python：`POST /internal/gkx-search/meta/policy-orientations`
- 请求对象：复用 `MetaChainsDTOs.Request`
- 返回对象：`MetaChainsDTOs.Response`（`items[{code,name}]`）
- 约定：`code == name`（中文）。Java 不在本仓再写一份四项。

入参字段表：

| 字段 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `keyword` | body | `String` | 否 | 按名称过滤 |
| `scope` | body | `String` | 否 | DTO 兼容字段，本接口忽略 |

请求示例：

```http
POST /enterprise/topic/v1/search/meta/policy-orientations
Content-Type: application/json

{}
```

出参字段表：

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.items[].code` | `String` | 与 `name` 相同 |
| `data.items[].name` | `String` | 科技创新 / 产业升级 / 绿色发展 / 市场拓展 |

返回 JSON 示例：

```json
{
  "code": 0,
  "ok": true,
  "data": {
    "items": [
      { "code": "科技创新", "name": "科技创新" },
      { "code": "产业升级", "name": "产业升级" },
      { "code": "绿色发展", "name": "绿色发展" },
      { "code": "市场拓展", "name": "市场拓展" }
    ]
  }
}
```

##### G6. 删除分析任务（软删，≠ cancel）
- **调用方**：**前端**（企业评估 / 风险洞察 / 引入·培育推荐 · 分析记录）
- 接口路径：`DELETE gateway地址/topicAsync/topic/v1/analysis/tasks/{taskId}`
- 服务内路径：`DELETE /topic/v1/analysis/tasks/{taskId}`
- Python 下游：仅当任务 `running` 时先走已有 cancel（Feign 算法）
- 请求对象：path + query
- 返回对象：`R<AnalysisTaskEntity>`
- 落库：`analysis_task.status = deleted`（不另开 DDL）
- 列表 #103：无 status 过滤时 **排除 deleted**；详情对已删返回「任务不存在」

入参字段表：

| 字段 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `taskId` | path | `String` | 是 | Java 任务 ID |
| `user_id` | query | `String` | 否 | 归属校验兼容 |

请求示例：

```http
DELETE /topicAsync/topic/v1/analysis/tasks/EVAL-20260902-001?user_id=u-1001
```

出参字段表：

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.taskId` | `String` | 原任务 ID |
| `data.status` | `String` | `deleted` |
| `data.updateTime` | 时间 | 删除时间 |

返回 JSON 示例：

```json
{
  "code": 0,
  "ok": true,
  "data": {
    "taskId": "EVAL-20260902-001",
    "status": "deleted"
  }
}
```

> 取消运行中任务仍用 `POST /topicAsync/topic/v1/analysis/tasks/{taskId}/cancel`（catalog #107）。

#### 4.P2 已有路径补字段

##### G7. 评估指标树（原 catalog #114）
- **调用方**：**前端**（企业评估 · 创建条件「指标体系」）
- 接口路径：`POST gateway地址/topicAsync/topic/v1/evaluation/indicators`
- AI Python：`POST /internal/gkx-ai/evaluation/indicators`
- 本轮变更：每个 indicator 增补 FE 别名，**不改** `key` / `name` / `metric_id` / `default_weight` / `data_status`

入参仍见 catalog #114（`subType` / `industry`）。

出参新增（挂在每个 `indicators[]` 上）：

| 字段 | 类型 | 来源 | 说明 |
|---|---|---|---|
| `label` | `String` | `name` | 勾选栏展示 |
| `weight` | `Number` | `default_weight` | 默认权重 |
| `available` | `Boolean` | `data_status=="available"` | 不可用置灰 |
| `metricId` | `String` | `metric_id` | ⓘ 挂 metric |

返回 JSON 片段：

```json
{
  "key": "patent_grant_count",
  "name": "专利授权量",
  "metric_id": "M_ENT_PATENT_GRANT_COUNT",
  "data_status": "available",
  "default_weight": 15,
  "label": "专利授权量",
  "weight": 15,
  "available": true,
  "metricId": "M_ENT_PATENT_GRANT_COUNT"
}
```

`data_status=pending/gap` 时 `available=false`，不要前端改绿。

##### G8. 双企维度对比（原 catalog #116）
- **调用方**：**前端**（企业评估 · 结果「维度对比 / 雷达」）
- 接口路径：`POST gateway地址/topicAsync/topic/v1/evaluation/tasks/compare`
- 本轮变更：`dimension_diff[]` 补中文名与双方分值别名

入参仍见 catalog #116（`taskId` / `enterpriseA` / `enterpriseB`）。任务须 `success`，两企须在结果中。

出参 `data.dimension_diff[]`：

| 字段 | 类型 | 说明 |
|---|---|---|
| `dimension` | `String` | `innovation` / `operation` / `growth` / `risk` |
| `name` / `label` | `String` | 创新能力 / 经营能力 / 成长能力 / 风险 |
| `value_a` / `score_a` | `Number` | 企业 A |
| `value_b` / `score_b` | `Number` | 企业 B |
| `diff` | `Number` | A − B |
| `advantage` | `String` | `a` / `b` / `tie` |

返回 JSON 片段：

```json
{
  "dimension": "innovation",
  "name": "创新能力",
  "label": "创新能力",
  "value_a": 90,
  "score_a": 90,
  "value_b": 60,
  "score_b": 60,
  "diff": 30,
  "advantage": "a"
}
```

##### G9. 分析任务结果包（原 catalog #105）
- **调用方**：**前端**（评估 / 引育结果页）
- 接口路径：`GET gateway地址/topicAsync/topic/v1/analysis/tasks/{taskId}/result`
- 本轮变更：Python 在 **已有字段** 上补别名；没有覆盖率 / 趋势序列 **不发明**
- 评估 enrich：`gkx_ai_service/views/evaluation.py::_enrich_eval_result`
- 引育 enrich：`gkx_ai_service/views/recommend.py::_enrich_recommend_result`
- 风险：本轮 **未** 加 enrich（图谱 `owner` / `centrality` / `evidence` 仍待算法出）

出参别名（出现在 `result` 或结果包根上，有源才写）：

| 字段 | 类型 | 来源 | 页面区域 |
|---|---|---|---|
| `ranking[]` | `List` | `scores` | 评估结果企业卡 |
| `ranking[].enterprise_code` | `String` | `org_id` | |
| `ranking[].coverage` | `Number` | 仅当已有 `coverage_rate` | 覆盖率；没有就不写 |
| `ranking[].missingMetricIds` | `List<String>` | `missing_metric_ids` 或 `[]` | 缺指标 |
| `radarSeries[]` | `List` | `radar` / `radar_series` | 雷达图 |
| `radarSeries[].values` | `List<Number\|null>` | `dimensions` 按 innovation/operation/growth/risk | |
| `policyDirections` | 任意 | `policy_directions` | 引育名单政策标签 |
| `riskCredit` | 任意 | `risk_credit` | 信用记录 |
| `dataTime` / `data_updated_at` | `String` | `updated_at` | 结果页头；没有则 **省略**（不要前端写死） |

##### G10. 重点分析 KPI 时点（原 catalog #122）
- **调用方**：**前端**（重点企业分析 · 页头「数据更新于」）
- 接口路径：`POST gateway地址/enterprise/topic/v1/key-analysis/overview-kpi`
- 本轮变更：显式返回 `dataTime` / `data_updated_at`，当前 **恒为 `null`**（ES 无可靠时点，禁止写死日期）

出参增量：

| 字段 | 类型 | 说明 |
|---|---|---|
| `dataTime` | `null` | 待有真实时点再填 |
| `data_updated_at` | `null` | 同上 |

原有 `matched_enterprise_count` / `covered_type_count` / `covered_region_count` 不变。

##### G11. 深圳现状 KPI 时点（原 catalog #132）
- **调用方**：**前端**（深圳企业现状分析 · 页头）
- 接口路径：`POST gateway地址/enterprise/topic/v1/sz-status/chain-kpi`
- 必填：`chain_code`
- 本轮变更：同 #G10，`dataTime` / `data_updated_at` 显式 `null`

---

## 5. 产业链分析

### 5.0 前端导读

> 产业目录 ≠ 企业 `meta/chains` 字典。顶部产业下拉走 **本模块 catalog / search**。  
> 网关前缀一律 **`/chain`**。分析任务生命周期走 **`/topicAsync`**（与企业共用）。

#### 该调哪些接口

| 业务 | 本轮 | 说明 |
|---|---|---|
| 区域指数 / 竞争力 · 评价对象城市 | **#C1** `evaluation_cities` | 粤/深/京/沪/杭，默认 `440300` |
| 深圳产业对比 · 标杆 | **#C1** `benchmark.items=[]` | Q016 未定，空清单；级联树用企业 `region-scopes` |
| 产业诊断年窗 / 因子；区域指数叶与权重；深圳对比维 | **#C1** `year_windows` / `diagnosis` / `regional` / `shenzhen` | 选中值随分析任务提交 |
| 产业查询高筛 | **#C1** `search_filters` | `layoutStatus` / `coveredStage` **searchable=false**，不要当全命中 |
| 顶部产业选择 / 查询推荐 | **#C2** catalog 已有字段 | aliases / domain / 父级 / availability |
| 产业查询结果卡 | **#C3** 补 `classification` | 产业=领域；链=父产业名 |
| 产业总览 KPI / 地图 | **#C4** | `kpis[].value` 可 `null`（Q056/QC07）；`regionPoints.lat/lng` |
| 产业全景时间轴 | **#C5** | 统一 `as_of` / `asOf`；`evolutionStates` |
| 8 类「查看结果」 | **#C6** 共用任务 result | 缺槽空，不另开结果 URL |

#### 调用方图例

| 标注 | 含义 |
|---|---|
| **前端** | 浏览器业务页 |
| **Python** | `lumen-algo-py` `/internal/v1/chain/**`；前端勿调 |

### 5.1 路由

```text
gateway地址 / chain / {Controller @RequestMapping} / {方法映射}
```

| 段 | 当前值 |
|---|---|
| 产业链网关前缀 | `/chain` |
| Controller | `/topic/v1/industry` |
| 任务中心 | `/topicAsync/topic/v1/analysis` |

示例：`GET gateway地址/chain/topic/v1/industry/meta`

### 5.2 调用链

```text
# P0 字典
前端 → /chain/topic/v1/industry/meta
  → IndustryFacadeController.meta
  → Feign lumen-algo-py GET /internal/v1/chain/meta
  → workspace_meta.chain_meta()

# P2 目录 / 搜索 / 总览 / 快照（路径已有）
前端 → /chain/topic/v1/industry/{catalog|search|overview/kpi|panorama/snapshot}
  → Feign /internal/v1/chain/{sync/objects|search|sync/kpi|sync/snapshot}

# P2 作业结果
前端 → /topicAsync/topic/v1/analysis/tasks/{taskId}/result
  → 算法 chain job（cycle / key_link / bottleneck / regional_* / shenzhen_*）
```

### 5.3 端点总览

| # | 分组 | 网关路径（相对 `{GW}`） | Python 下游 | 请求对象 | 返回 data 类型 | 动作 |
|---|---|---|---|---|---|---|
| C1 | 字典·P0 | `GET /chain/topic/v1/industry/meta` | `GET /internal/v1/chain/meta` | 无 | `Map` | 新增 |
| C2 | 目录·P2 | `GET /chain/topic/v1/industry/catalog` | `GET /internal/v1/chain/sync/objects` | `IndustrySyncQuery` | `Map` | 补字段（多数已有） |
| C3 | 查询·P2 | `GET\|POST /chain/topic/v1/industry/search` | `/internal/v1/chain/search` | `IndustrySearchRequest` | `Map` | 补 `classification` |
| C4 | 总览·P2 | `GET /chain/topic/v1/industry/overview/kpi` | `GET /internal/v1/chain/sync/kpi` | `IndustrySyncQuery` | `Map` | 确认空值 / 坐标 |
| C5 | 全景·P2 | `GET /chain/topic/v1/industry/panorama/snapshot` | `GET /internal/v1/chain/sync/snapshot` | `IndustrySyncQuery` | `Map` | 补 `as_of`/`asOf` |
| C6 | 结果·P2 | `GET /topicAsync/topic/v1/analysis/tasks/{taskId}/result` | chain jobs | `user_id` | 任务 + 结果包 | 不另开地址 |

`GET /overview` 与 `#C4` 同实现。

### 5.4 端点明细

##### C1. 工作区 / 高筛字典（CHAIN-N1–N4）
- **调用方**：**前端**
- 接口路径：`GET gateway地址/chain/topic/v1/industry/meta`
- 服务内路径：`GET /topic/v1/industry/meta`
- Python：`GET /internal/v1/chain/meta`（亦接受 POST，body 忽略）
- 请求：无
- 返回：`R<Map<String, Object>>`

出参字段表：

| 字段 | 类型 | 缺口 | 说明 |
|---|---|---|---|
| `evaluation_cities[]` | `{code,name}` | N1 | 440000 广东省 / 440300 深圳市 / 110000 北京市 / 310000 上海市 / 330100 杭州市 |
| `default_evaluation_city` | `String` | N1 | `440300` |
| `benchmark.pending_ref` | `String` | N2 | `Q016` |
| `benchmark.items` | `List` | N2 | **恒 `[]`**，不发明沪/京/苏州 |
| `benchmark.source_api` | `String` | N2 | `POST /enterprise/topic/v1/search/meta/region-scopes` |
| `year_windows[]` | `{value,label}` | N3 | 3=近3年 / 5=近5年 |
| `diagnosis.key_link_stages[]` | `{key,label}` | N3 | 研发/设计/制造/销售/服务 |
| `diagnosis.key_link_factors[]` | `{key,label,weight,metric_id}` | N3 | 附加值率 / 技术壁垒 / 市场集中度 |
| `diagnosis.bottleneck_dimensions[]` | 同上 | N3 | 技术/人才/市场/资本/政策 各 20 |
| `regional.index_metrics[]` | `{key,label,group,official,metric_id}` | N3 | 区域指数叶 |
| `regional.competitiveness_weights[]` | `{key,label,weight,metric_id}` | N3 | `industry_foundation` 40 / `academic_ecology` 35 / `innovation_ecology` 25（**不是** Demo 的 enterprise/academic/support） |
| `shenzhen.compare_dimensions[]` | `{key,label,weight,metric_id}` | N3 | 企业/专利/政策/人才 各 25 |
| `search_filters.industry_level` | `{code,name,searchable}` | N4 | 一级产业 |
| `search_filters.industry_attribute` | 同上 | N4 | 重点产业 / 未来产业 |
| `search_filters.layout_status` | 同上 | N4 | 重点布局，`searchable=false` |
| `search_filters.covered_stage` | 同上 | N4 | 全链条，`searchable=false` |
| `search_filters.unsupported_search_fields` | `List<String>` | N4 | 含 `layoutStatus` / `coveredStage` |

返回 JSON 示例（节选）：

```json
{
  "code": 0,
  "ok": true,
  "data": {
    "default_evaluation_city": "440300",
    "benchmark": {
      "pending_ref": "Q016",
      "items": [],
      "source_api": "POST /enterprise/topic/v1/search/meta/region-scopes"
    },
    "year_windows": [
      { "value": 3, "label": "近3年" },
      { "value": 5, "label": "近5年" }
    ]
  }
}
```

##### C2. 对象目录（CHAIN-F1，路径已有）
- 接口路径：`GET gateway地址/chain/topic/v1/industry/catalog`
- Python：`GET /internal/v1/chain/sync/objects`
- 用途：顶部产业选择、查询推荐

出参（选项上已有，本轮确认）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `aliases` | `List<String>` | 别名 |
| `domain` | `String` | 领域 |
| `parentIndustryId` / `parentIndustryName` | `String` | 父级产业 |
| `availability` / `disabled` | | 不可用置灰 |
| `defaultIndustryId` / `defaultChainId` | `String` | 默认选中 |

##### C3. 产业查询（CHAIN-F2）
- 接口路径：`GET|POST gateway地址/chain/topic/v1/industry/search`
- 本轮变更：公开记录补 `classification`

出参记录增量：

| 字段 | 类型 | 说明 |
|---|---|---|
| `classification` | `String` | 产业 = `domain`；链 = `parentIndustryName` 或 `domain` |
| `tags` / `keywords` | `List<String>` | 结果卡标签 |
| `updatedAt` | `String` | `YYYY-MM-DD` |
| `aliases` / `domain` / `availability` | | 已有 |

`layoutStatus` / `coveredStage` 条件 **忽略且不按全量命中**。

##### C4. 总览 KPI（CHAIN-F3）
- 接口路径：`GET gateway地址/chain/topic/v1/industry/overview/kpi`
- Query：`objectId` / `chainId` / `industryId` / `asOf`（均可选）

出参要点：

| 字段 | 说明 |
|---|---|
| `kpis[].value` | **允许 `null`**（Q056 市场规模、QC07 投融资）。不要用 0 冒充 |
| `regionPoints[].lat` / `lng` | 缺坐标则为 `null`，不要编点 |

##### C5. 全景发布快照（CHAIN-F4）
- 接口路径：`GET gateway地址/chain/topic/v1/industry/panorama/snapshot`
- Query：`chainId` / `industryId` / `asOf`

出参增量：

| 字段 | 类型 | 说明 |
|---|---|---|
| `as_of` / `asOf` | `String\|null` | 所选快照 `effective_at` 日期，或请求 `asOf` |
| `dataset.evolutionStates` | `List` | 时间轴演进；无则 `[]` |
| `snapshot` | `Object\|null` | 无已发布快照则为 `null`，`dataset.nodes/edges=[]` |

返回 JSON 片段：

```json
{
  "as_of": "2026-08-14",
  "asOf": "2026-08-14",
  "snapshot": { "snapshot_id": "snap:INB130301:mock", "effective_at": "2026-08-14 03:14:55" },
  "dataset": { "chainId": "INB130301", "nodes": [], "edges": [], "evolutionStates": [] },
  "created_task": false
}
```

##### C6. 8 类分析任务结果（CHAIN-F5）
- 接口路径：`GET gateway地址/topicAsync/topic/v1/analysis/tasks/{taskId}/result`
- 不要另开结果地址。缺代表企业 / 五环节健康则 **空**，Java/Python 门面不补假名单。

| 分析类型 | 结果区看什么 | 本轮 |
|---|---|---|
| 周期诊断 | 旅程、时序、阶段 | 算法 `cycle` 已有结构则透传 |
| 关键环节 / 瓶颈 | 代表企业、五环节健康 | **可空** |
| 区域指数 / 竞争力 | 指数、分维、排名 | 透传 |
| 深圳对比 / 发展 | 对比分、评估槽、发展路径 | 透传 |

---

## 6. 服务链分析

### 6.0 前端导读

> 顶部产业下拉 **复用产业链 catalog**，不要再开服务链产业目录。  
> 分析任务创建 / 列表 / 删除走 **`/topicAsync`**（与企业共用；删除 = ENT #G6）。  
> 业务读面网关前缀 **`/svc`**。

#### 该调哪些接口

| 业务 | 本轮 | 说明 |
|---|---|---|
| 服务机构查询 · 高筛字段库 | **#S1** `service_types` / `org_kinds` / `cities` / `industries` | 六类服务真源 Python `_CLASS_LABELS` |
| 短板 / 培育 · 环节 | **#S1** `links[]` | 11 环节；`service_types=[]` 未拍板 |
| 技术力 / 趋势 / 招引 / 培育权重与年窗 | **#S1** `analysis` | 综合分由结果下发，页面不按权重重算 |
| 加入对比篮 | **#S2–S5**（推荐 `/svc/.../compare-basket`） | 同源写库；`source` 含 `external` 拒绝 |
| 专题服务五 Tab | **#S6–S11** | 全库 KPI，**不是**按产业切片；`filtered=false` |
| 机构检索 / 画像 | **#S12 #S13** | `tech_score` 无则 null；覆盖/成立年只从 `ext` |
| 生态图谱 | **#S14** | `nodes`/`edges`；排名表不能当图 |
| 引入 / 培育名单 | **#S15** | 页面不重算总分 |
| 八类查看结果 | **#S16** | 缺 `heat/matrix/paths` 给 `[]` |

#### 调用方图例

| 标注 | 含义 |
|---|---|
| **前端** | 浏览器业务页 |
| **Python** | `/internal/gkx-svc/**`；前端勿调 |
| **内部 Feign** | svc 门面 → enterprise 写篮；前端只调 `/svc` 即可 |

#### 容易混淆

| 容易当成 | 实际 |
|---|---|
| 门户 KPI 已按当前产业过滤 | **pool 级**。切产业后数字不变，直到数据侧有切片事实 |
| 对比篮在 ADS | 写 **topic_enterprise** |
| 引入推荐外部候选可入篮 | **拒绝** |
| Java 可写死六类服务 | 只许透传 Python |

### 6.1 路由

```text
gateway地址 / svc / {Controller @RequestMapping} / {方法映射}
```

| 段 | 当前值 |
|---|---|
| 服务链网关前缀 | `/svc` |
| 查询 / 字典 / 图谱 / 名单 | `/topic/v1/service` |
| 门户 | `/topic/v1/service-portal` |
| 对比篮（推荐） | `/topic/v1/service/compare-basket` |
| 对比篮（企业仓直出，同源表） | `/enterprise/topic/v1/compare-basket/org-items` |
| 任务中心 | `/topicAsync/topic/v1/analysis` |

示例：`POST gateway地址/svc/topic/v1/service/meta`

### 6.2 调用链

```text
# P0 字典
前端 → /svc/topic/v1/service/meta
  → ServiceFacadeController.meta → Feign lumen-topic-py
  → POST /internal/gkx-svc/meta → repo.meta_catalog()
  Feign 失败：HTTP 200 + 空数组，不填金融服务

# P0 对比篮
前端 → /svc/topic/v1/service/compare-basket/**
  → SvcCompareBasketController → Feign enterprise OrgCompareBasket
  → MySQL gkxlumenx_topic_enterprise.svc_compare_basket_item

# P2 门户 / 检索 / 画像 / 图谱 / 名单
前端 → /svc/topic/v1/service-portal/** 或 /service/search|profile|eco-graph|rec-list
  → Feign → /internal/gkx-svc/**

# P2 任务结果
前端 → /topicAsync/.../tasks/{taskId}/result
  创建期 Python task.py GET lumen-algo /internal/v1/svcan/models/*
  缺槽补 heat/matrix/paths=[]
```

### 6.3 端点总览

| # | 分组 | 网关路径（相对 `{GW}`） | Python 下游 | 请求对象 | 返回 | 动作 |
|---|---|---|---|---|---|---|
| S1 | 字典·P0 | `POST /svc/topic/v1/service/meta` | `/internal/gkx-svc/meta` | `Map` 可空 | `Map` | 新增 |
| S2 | 对比篮·P0 | `GET /svc/topic/v1/service/compare-basket` | — | `user_id` | `BasketResponse` | 新增 |
| S3 | 对比篮·P0 | `POST /svc/topic/v1/service/compare-basket/items` | — | `AddItemsRequest` | `AddItemsResponse` | 新增 |
| S4 | 对比篮·P0 | `DELETE /svc/topic/v1/service/compare-basket/items/{org_id}` | — | `user_id` | `Void` | 新增 |
| S5 | 对比篮·P0 | `DELETE /svc/topic/v1/service/compare-basket/items/batch` | — | `BatchRemoveRequest` | `Void` | 新增 |
| S6 | 门户·P2 | `POST /svc/topic/v1/service-portal/overview` | `/portal/overview` | `Map` | `Map` | 补字段 |
| S7 | 门户·P2 | `POST /svc/topic/v1/service-portal/industry-distribution` | `/portal/industry-distribution` | `Map` | `Map` | 确认 |
| S8 | 门户·P2 | `POST /svc/topic/v1/service-portal/region-map` | `/portal/region-map` | `Map` | `Map` | 确认 |
| S9 | 门户·P2 | `POST /svc/topic/v1/service-portal/shenzhen` | `/portal/shenzhen` | `Map` | `Map` | trend 有条件 |
| S10 | 门户·P2 | `POST /svc/topic/v1/service-portal/key-orgs` | `/portal/key-orgs` | `Map` | `Map` | 确认 |
| S11 | 门户·P2 | `POST /svc/topic/v1/service-portal/ranking` | `/portal/ranking` | `Map` | `Map` | 与 #S15 同源 |
| S12 | 检索·P2 | `POST /svc/topic/v1/service/search/orgs` | `/search/orgs` | `Map` | `Map` | 补筛 / tech_score |
| S13 | 画像·P2 | `POST /svc/topic/v1/service/profile/get` | `/profile/get` | `Map` | `Map\|null` | ext 透出 |
| S14 | 图谱·P2 | `POST /svc/topic/v1/service/eco-graph` | `/eco/graph` | `Map` | `Map` | 已有点边 |
| S15 | 名单·P2 | `POST /svc/topic/v1/service/rec-list` | `/portal/ranking` | `Map` | `Map` | 行内分项空则 `{}` |
| S16 | 结果·P2 | `GET /topicAsync/topic/v1/analysis/tasks/{taskId}/result` | svcan models | `user_id` | 任务 + 结果 | 空槽 |

同源写篮（admin / 联调用）：`/enterprise/topic/v1/compare-basket/org-items` GET/POST/DELETE/`/batch`。

### 6.4 端点明细

##### S1. 检索 / 分析字典（SVC-N1–N3）
- **调用方**：**前端**
- 接口路径：`POST gateway地址/svc/topic/v1/service/meta`
- Python：`POST /internal/gkx-svc/meta`
- 请求：可 `{}`
- Feign 失败：HTTP 200，`empty=true`，各数组 `[]`，`analysis={}`，**无「金融服务」**

出参字段表：

| 字段 | 类型 | 缺口 | 说明 |
|---|---|---|---|
| `service_types[]` | `{code,name}` | N1 | FINANCE 金融服务 / IP 知识产权服务 / HR 人力资源服务 / MKT 市场营销服务 / CONSULT 咨询服务 / INNOV 科技创新服务 |
| `org_kinds[]` | `{code,name}` | N1 | UNI 高校 / INST 科研院所 / ENT 企业 |
| `cities[]` / `industries[]` | `{code,name}` | N1 | ADS `svc_org_card` DISTINCT；失败 `[]` |
| `links[]` | `{code,name,stage,service_types,description}` | N2 | 11 环节（上/中/下游）；`service_types` 恒 `[]` |
| `analysis.year_windows` | `List<int>` | N3 | `[3,5,8]`，默认 5 |
| `analysis.tech_dims[]` | `{key,label,weight}` | N3 | 专利/研发/专家/案例/标准 |
| `analysis.attract_indicators[]` | 同上 | N3 | 产业匹配/技术领先/潜力/合作意愿 |
| `analysis.cultivate_dims[]` | 同上 | N3 | 规模/创新/成效/市场缺口 |
| `analysis.org_types` | 同 `org_kinds` | N3 | |
| `analysis.score_source` | `String` | N3 | `task_result`（页面不重算） |
| `writes_ads` | `Boolean` | | `false` |
| `pending_client_confirm` | `Integer` | | `1` |
| `data_source` | `String` | | `demo_ads` 或 `unavailable:*` |

`links` 闭集：`up_rd` 上游·研发 / `up_std` 上游·标准 / `up_ip` 上游·知识产权 / `up_coop` 上游·科研合作 / `mid_pilot` 中游·中试 / `mid_test` 中游·检测 / `mid_inc` 中游·孵化 / `mid_xfer` 中游·技术转移 / `dn_fin` 下游·投融资 / `dn_hr` 下游·人才 / `dn_digital` 下游·数字化。

##### S2–S5. 服务机构对比篮（SVC-N4）
- 推荐路径前缀：`/svc/topic/v1/service/compare-basket`
- 落库：`gkxlumenx_topic_enterprise.svc_compare_basket_item`（**须先执行 DDL** `lumen-svc-platform/db/9x_gkxlumenx_topic_enterprise.sql`）
- 上限：加入最多 50；分发产业领域 1–50、技术力 2–5 由前端约束

**S2 GET** `?user_id=` → `items[]`，空篮合法。

**S3 POST /items**

| 字段 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `user_id` | body | `String` | 是 | 归属 |
| `org_ids` | body | `List<String>` | 是 | 机构 ID |
| `org_names` | body | `List<String>` | 否 | 展示名 |
| `source` | body | `String` | 否 | 含 `external`（忽略大小写）**拒绝** |

返回：`added` / `duplicated` / `basket_count`。

**S4 DELETE** `/items/{org_id}?user_id=`

**S5 DELETE** `/items/batch` body：`user_id` +（`org_ids` 或 `clear_all`）

##### S6. 门户概况（SVC-F1）
- 接口路径：`POST gateway地址/svc/topic/v1/service-portal/overview`
- 本轮：回显 `industry` / `chain`（来自请求）；`filtered=false`；`pool_level=true`；`scale_bands` 仅当 ADS 有 `M_SVC_SCALE_BAND`
- KPI 只出 ADS 有行的 metric，缺行不填 0

出参要点：

| 字段 | 说明 |
|---|---|
| `kpi.org_in_pool` / `sz_scale` | 有行才出现 |
| `new_org_series` / `invest_series` | 历年 |
| `scale_bands` | 无独立 dist 则为 `[]` |
| `industry` / `chain` | 回显，**不切片 KPI** |
| `filtered` | `false` |

##### S7–S10. 门户其余 Tab
- `#S7` 产业分布：`by_service_type` + `stages`（短板表有行才有）
- `#S8` 区域：`china` 省；无 country 不出国别假点
- `#S9` 深圳：`sz_total` / `districts`；**仅当** `M_SVC_SZ_SCALE` 有独立 series 才带 `trend`，禁止用全球趋势乘比例
- `#S10` 重点机构：最新技术力批次按 `org_id` 去重；无行 `items=[]`

##### S12. 机构检索（SVC-F2）
- 接口路径：`POST gateway地址/svc/topic/v1/service/search/orgs`

入参：

| 字段 | 必填 | 说明 |
|---|---|---|
| `keyword` / `q` | 否 | 名称 / org_id |
| `service_type` / `serviceType` | 否 | 六类 code |
| `city` / `province` / `area` / `district` | 否 | 已有列才入 SQL |
| `industry` | 否 | |
| `page` / `size` | 否 | 默认 1 / 20，size≤100 |

出参行：

| 字段 | 说明 |
|---|---|
| `tech_score` | `ext.tech_score` 或 `null`（FE「暂无」） |
| `recommended` | `ext.recommended` 或 `[]` |
| `org_type` | 名称启发式 高校/院所/企业（Q-SVCCHAIN-06） |

##### S13. 机构画像（SVC-F3）
- 接口路径：`POST gateway地址/svc/topic/v1/service/profile/get`
- body：`org_id` / `orgId` / `service_org_code`
- 无卡：`data=null`
- 有则：`tech_scores[]`；`coverage` / `found_year` / `recent_records` **仅当 ext 有**，否则不编造

##### S14. 生态图谱（SVC-F4）
- 接口路径：`POST gateway地址/svc/topic/v1/service/eco-graph`
- 已有 `nodes` / `edges` + 双密度。`filter=orgs|orgs_and_actors`
- 空图 `empty=true`。禁止用排名 JSON 冒充图

##### S15. 招引 / 培育名单（SVC-F5）
- 接口路径：`POST gateway地址/svc/topic/v1/service/rec-list`
- `kind=attract|cultivate` → `list_type=ATTRACT|CULTIVATE`
- 行内：`org_type` / `segment`（`growth_stage`）/ `suggestion_text` / `suggestion_tags=[]` / `dimension_scores={}`（无 ADS 分项列则空对象）
- **页面不按权重重算 `score`**

##### S16. 八类分析任务结果（SVC-F6）
- 接口路径：`GET gateway地址/topicAsync/topic/v1/analysis/tasks/{taskId}/result`
- 创建走已有任务中心；Python 适配 `GET /internal/v1/svcan/models/*`
- 缺 `heat` / `matrix` / `paths` 时补 **`[]`**，不发明热力或路径数

| 分析 | 结果区 | 缺则 |
|---|---|---|
| 产业领域 | 热力 / 广度深度 | `heat`/`matrix`=`[]` |
| 新增趋势 | 年序 / 代表机构 / 热度 | 空 |
| 技术力 | 综合分 / 五维 | 空 |
| 短板 | 环节机构数 / 问题类型 | 空 |
| 图谱 | 点边或指针 | 与 #S14 一致即可 |
| 深圳现状 | 分城 / 梯队 | 空 |
| 引入 / 培育 | 名单与建议 | 空 |
---

## 9. 缺口状态（已实现 / 待确认 / 后续补）

> 后续补列写清改 **Java** 还是 **Python**。P1 本次不做。

### 9.1 已实现（P0 + P2，代码已落地）

| 模块 | ID | 前端可调 | 改了哪 |
|---|---|---|---|
| 企业 | ENT-N1/N2 | `DELETE /enterprise/.../recruit-candidates/**`、`cultivate-candidates/**` | **Java** MySQL |
| 企业 | ENT-N3 | `POST /enterprise/.../meta/policy-orientations` | **Python** 出数 + **Java** 透传 |
| 企业 | ENT-N4 | `DELETE /topicAsync/.../analysis/tasks/{taskId}` | **Java** 软删 |
| 企业 | ENT-F1–F4 | 原 indicators / compare / result / KPI 路径补字段 | **Python**（Java 已透传） |
| 产业链 | CHAIN-N1–N4 | `GET /chain/.../industry/meta` | **Python** + **Java** GET |
| 产业链 | CHAIN-F2/F4 | search `classification`；snapshot `as_of` | **Python** |
| 产业链 | CHAIN-F1/F3/F5 | 目录/KPI 空值/任务 result | 原已有或只确认 |
| 服务链 | SVC-N1–N3 | `POST /svc/.../service/meta` | **Python** + **Java** 透传 |
| 服务链 | SVC-N4 | `/svc/.../compare-basket/**` | **Java**（写企业库） |
| 服务链 | SVC-F1–F6 | 门户/检索/画像/图谱/名单/结果空槽 | **Python** |

### 9.2 待确认（不替甲方拍板）

| 项 | 影响页面 | 现状 |
|---|---|---|
| Q016 对标城市 | 深圳企业现状、深圳产业对比、深圳服务链现状 | 字典空或只展示结果里的城 |
| Q014 评估指标可用性 | 企业评估勾选 | `available=false` 的 pending/gap |
| Q-SVCCHAIN-01~06 环节↔六类服务 | 短板 / 培育筛 | `links[].service_types=[]` |
| Q-SVCCHAIN-06 机构类型启发式 | 服务链概况 / 名单 | 按名称猜高校/院所/企业 |
| Q056 / QC07 | 产业总览市场规模、投融资 | KPI `value=null` |
| 门户是否按产业切片 | 服务链五 Tab | 现为全库 `filtered=false` |
| 数据时点 | 各页头「更新于」 | `dataTime=null` |
| 竞争力三维键名 | 区域竞争力权重 | 用 `industry_foundation` 等，不是 Demo 旧 key |

### 9.3 后续补 · P1（本次不做）

| ID | 要补 | 页面 · 区域 | 后续改哪 |
|---|---|---|---|
| ENT-O1 | 深圳企业对标城选项 | 深圳企业现状 · 对标多选 | 口径 → **Python** 字典或复用 `POST /enterprise/.../meta/region-scopes` + **Java** 透传 |
| ENT-O2 | 招引目标特征选项 | 引入推荐 · 条件栏 | **Python** 字典 + **Java** 透传 |
| CHAIN-O1 | 全景历史 / 双图 diff / 节点下钻 | 产业全景 | **Python** 扩 snapshot；**Java** 透传 |
| CHAIN-O2 | 跨端已查看结果 | 各分析 过程页→结果 | **Java** 用户态（不要 Python） |
| CHAIN-O3 | 区域指数个人模板上云 | 区域指数 · 指标模板 | **Java** MySQL |
| SVC-O1 | 深圳服务链对标城 | 深圳服务链现状 | 同 ENT-O1 |
| SVC-O2 | 检索联想 | 服务机构查询 · 搜索框 | **Python** suggest + **Java** 透传 |
| SVC-O3 | 报告 / 名单导出任务 | 结果导出 | **Java** ANALYSIS-CORE 扩 `analysisType` |
| SVC-O4 | 跨端已查看结果 | 过程页 → 结果 | **Java**（同 CHAIN-O2） |

### 9.4 后续补 · P2 仍空的槽（路径已有，等算法 / ADS / 口径）

| ID | 要补 | 页面 · 区域 | 后续改哪 |
|---|---|---|---|
| ENT-F3 续 | 覆盖率真值、商业力趋势/对标 | 评估结果卡 / 折线 | **Python 算法**；门面已会别名。禁止 Java/FE 造点 |
| ENT-F3 续 | 风险节点 `owner/centrality/evidence`、边 `strength` | 风险洞察图谱 | **Python 算法** 写 `result_data`；Java 透传 |
| ENT-F4 续 | 真实 `dataTime` | 页头 | **Python** 读 ES/ADS 时点 |
| CHAIN-N2 续 | 填 `benchmark.items` | 深圳产业对比标杆 | 口径后 **Python** |
| CHAIN-F5 续 | 代表企业、五环节健康 | 产业诊断结果 | **Python 算法** |
| SVC-F1 续 | 按产业出 KPI、规模四档、深圳 trend | 五 Tab | **ADS 有行** 后 **Python** 自动带；禁止拿全库冒充切片 |
| SVC-N2 续 | 环节对应服务类型 | 短板 / 培育 | 口径后 **Python** |
| SVC-F3 续 | coverage / 成立年 / 近三年 | 画像抽屉 | **ADS/ext** 有字段后 Python 已会透出 |
| SVC-F5 续 | 名单分项分 | 引入/培育名单 | **ADS 列 + Python**；不要 Java 重算 |
| SVC-F6 续 | 热力 / 年序 / 五维 / 短板问题 | 各分析结果区 | **Python 算法** svcan |

维护 CMS / 第二套服务链产业目录：**不做**。

### 9.5 运维

- 企业候选删除、任务软删 **无需新表**。
- 服务机构对比篮 **必须先跑** `svc_compare_basket_item` DDL（`lumen-svc-platform/db/9x_gkxlumenx_topic_enterprise.sql`），写 `gkxlumenx_topic_enterprise`，不写 ADS。
- 产业链 meta 复用存量 algo Feign，不是本轮新开 Java→算法直连。
- K8s 若只发 search-py：`gkx_svc` 路由已挂在 `gkx_search_service/main.py`。
