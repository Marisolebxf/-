# API · 科技发展态势（TS）· M2 科学技术全景（接口契约草案）

> **任务**：`BE-TS-CONTRACT-02`（M2–M9 接口契约定义，按批冻结）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。路径前缀 / DTO 命名 / 服务归属沿用 `API-TS-M1.md` U1/U2 的 M0 结论；本模块属**批 2**，开工前必须冻结（`API-TS-M1.md` §9.2）。
> **范围**：仅 M2（科学技术全景 · 技术点图谱）。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `TS-模块开发规划与任务拆分.md` §4 M2（FE-TS-02a~02d） |
| 图谱过滤 / 切片 / 时间轴 | `demo-ui-science/src/pages/tech-knowledge-graph/graphFilter.js` L7–L141 |
| 实体 / 关系枚举与图谱种子 | `demo-ui-science/src/pages/tech-knowledge-graph/mockData.js` L4–L43 |
| 图谱渲染字段映射 | `demo-ui-science/src/pages/tech-knowledge-graph/AnalysisDisplay.jsx` L123–L174 / L260–L339 |
| 版本对比 / 历史版本 | `demo-ui-science/src/pages/tech-knowledge-graph/CentralityPanel.jsx` L243–L244 / L471–L489 |
| 编辑历史 / 模型部署态 | `demo-ui-science/src/pages/tech-knowledge-graph/decisionModel.js` L22–L42 |
| 调用链 / 图谱存储 | `agent-delivery/architecture-baseline.md` §2（图谱存储 Nebula；Java 不直连 nGQL，经 Java→Python 链路） |

---

## 1. 模块约定（增量）

全局约定（调用链 `/display/**` 前缀、`R<T>` 包络与错误码、公共筛选入参、分页排序、`X-Trace-Id` 可观测、D9 血缘与 Mock 先行、缺数降级四态）**继承 `API-TS-M1.md` §1 / §4 / §5**，本文件不重复。

| 项 | 约定 |
|---|---|
| 服务内路径前缀 | `/v1/situation/panorama/**`（网关对外 `/display/v1/situation/panorama/**`） |
| 图谱数据源 | 图谱真源 = **Nebula**；Java **不直连 nGQL**，图谱查询经 Feign `/internal/*` → Python KG 查询服务（基线 §2）；Java 侧只做聚合与契约适配 |
| 读写面 | 图谱数据只读；**带写面** = §3.4 图谱编辑（编辑历史 / 版本） |
| 前端组件 | `chart/GraphChart`（ECharts graph 封装，禁 G6 直连；规划 §1.4） |

## 2. 枚举字典（前端只读消费，禁止前端手写）

### 2.1 实体类型 `entity_type`（6 类，逐字）
`mockData.js` L4–L11 `entityTypes`：`institution`机构 · `technology`技术 · `paper`论文 · `patent`专利 · `project`项目 · `field`领域。
（demo 另有人才节点 `person`，分析展示默认排除——`graphFilter.js` L5/L25 `excludePerson` 默认 `true`；契约保留 `exclude_person` 入参，默认 `true`。）
各色值由后端字典下发（`color` / `icon` 同字段返回），前端不各写一份。

### 2.2 关系类型 `relation_type`（6 类，逐字）
`mockData.js` L34–L41 `relationTypes`：`cooperate`合作 · `belong`隶属 · `research`研究 · `cite`引用 · `participate`参与 · `belong_to`属于。

### 2.3 图谱切片 `slice_key`（5 类）
`graphFilter.js` L63–L126 `sliceKnowledgeGraph`：`overview`总览（默认） · `field`领域切片 · `institution`机构一度邻居 · `cooperation`合作切片（仅 `cooperate`/`participate` 边） · `timeline`年份切片。

### 2.4 编辑操作 `edit_operation`（6 类）
`add_node` / `update_node` / `remove_node` / `add_edge` / `update_edge` / `remove_edge`。
demo 撤销重做栈为纯前端演示；契约要求**编辑批次提交服务端**，服务端落编辑历史（§3.4）。

### 2.5 版本状态 `version_status`（3 类）
对齐 `decisionModel.js` L42 部署语义：`draft`草稿 · `deployed`已发布 · `archived`已归档。
版本号格式沿用 demo 历史版本口径 `v{yyyy}-{mm}`（`CentralityPanel.jsx` L243–L244：`v2025-01` / `v2026-03`），由后端生成。

## 3. 接口清单（4 类）

### 3.1 `GET /v1/situation/panorama/graph` — 技术点图谱数据

**用途**（规划 M2-BE ①）：节点/边/类型/层级 + 筛选 + 切片 + 时间轴统计。

| Query | 类型 | 默认 | 真源 |
|---|---|---|---|
| `keyword` | string | - | `graphFilter.js` L9（支持场景化关键词预设，见 U3） |
| `entity_type` | enum | `all` | §2.1 |
| `relation_type` | enum | `all` | §2.2 |
| `field` / `region` / `author` | string | `all` | `graphFilter.js` L12–L14 |
| `year_start` / `year_end` | int | 2020 / 2026 | `graphFilter.js` L15–L16 |
| `exclude_person` | bool | `true` | `graphFilter.js` L17 |
| `slice_key` / `slice_value` | enum / string | `overview` / - | §2.3 |
| `depth` | int | 1 | 图谱展开深度（FE-TS-02a「深度」筛选） |

```json
{
  "code": 0,
  "data": {
    "filter_echo": { "entity_type": "all", "relation_type": "all", "year_start": 2020, "year_end": 2026, "slice_key": "overview" },
    "nodes": [
      { "node_id": "N-xxxx", "name": "鹏城实验室", "entity_type": "institution", "type_label": "机构",
        "value": 86, "field": "人工智能", "region": "广东", "author": null, "year": 2023, "institution": "鹏城实验室" }
    ],
    "edges": [
      { "edge_id": "E-xxxx", "source": "N-xxxx", "target": "N-yyyy", "relation_type": "cooperate", "relation_label": "合作", "weight": 0.72, "year": 2024 }
    ],
    "timeline": [ { "year": 2024, "entities": 128, "relations": 342 } ],
    "kpis": { "matched_entities": 128, "matched_relations": 342, "covered_fields": 6 },
    "metric_ids": []
  }
}
```

形状对齐：节点/边字段对齐 `AnalysisDisplay.jsx` L123–L174（`id/name/type/value` + `source/target/type/weight`）；`timeline` 对齐 `buildTimelineSeries`（`graphFilter.js` L128–L141，`{year, entities, relations}`）；`kpis` 对齐 `AnalysisDisplay.jsx` L260–L339（匹配实体 / 匹配关系 / 覆盖领域）。
边界：
- 切片口径必须服务端执行（`institution` 一度邻居、`cooperation` 仅合作边、`timeline` 按年），**前端不自行裁边**。
- `exclude_person=true` 时结果不含 `person` 节点；显式 `false` 才返回。
- 结果集上限：节点 >2000 时返 `400` 提示缩窄筛选（防一次拉全图），**待 M0 确认上限值**。

### 3.2 `GET /v1/situation/panorama/critical-paths` — 关键路径清单与节点标记

**用途**（规划 M2-BE ②）：关键路径清单 + 路径节点标记（FE-TS-02c 路径叠加/播放/对比）。

| Query | 说明 |
|---|---|
| 公共筛选 | 同 §3.1 |
| `path_rank` | 可选：`strength`关联强度 / `recency`新近度，默认 `strength` |

```json
{
  "code": 0,
  "data": {
    "paths": [
      { "path_id": "CP-01", "name": "具身智能关键器件路径", "node_ids": ["N-a","N-b","N-c"], "edge_ids": ["E-a","E-b"],
        "score": 91.5, "metric_id": "Q0xx", "description": "…" }
    ],
    "key_node_ids": ["N-a", "N-c"],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：路径叠加对比（02c）前端可叠加多条 `path_id`；`score` 带 `metric_id`（D9）。关键路径识别为算法产物（ALGO 参考：关键路径/节点识别），Java 只读不落公式。

### 3.3 关键实体检索与详情

**用途**（规划 M2-BE ③）：关键实体列表 + 节点/实体详情（关联强度/评分）（FE-TS-02b）。

`POST /v1/situation/panorama/entities/search`：入参同 §3.1 筛选 + §1.4 分页（M1）；`sort_key` ∈ `strength` / `score` / `year`。

`GET /v1/situation/panorama/entities/{entity_id}`：

```json
{
  "code": 0,
  "data": {
    "entity": { "node_id": "N-xxxx", "name": "鹏城实验室", "entity_type": "institution", "type_label": "机构",
                "field": "人工智能", "region": "广东", "year": 2023, "institution": "鹏城实验室", "summary": "…" },
    "metrics": [
      { "key": "relation_strength", "label": "关联强度", "value": 0.86, "metric_id": "Q0xx" },
      { "key": "composite_score",   "label": "综合评分", "value": 92.4, "metric_id": "Q0xx" }
    ],
    "neighbors": [ { "node_id": "N-yyyy", "name": "华为", "relation_type": "cooperate", "weight": 0.72 } ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：实体不存在 → **404**；`neighbors` 默认一度，可传 `depth=2`（上限 2，防爆量）。

### 3.4 图谱编辑（M2 带写面；FE-TS-02d）

**用途**：导入 JSON / 手动增删改 / 撤销重做 / 版本控制 + 维护管理入口。demo 编辑为纯前端态；契约要求**编辑批次服务端化**，可追溯、可发布、可回滚。

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/v1/situation/panorama/graph/edits` | 提交编辑批次 `{ "base_version": "v2026-03", "operations": [ { "op": "add_node", "node": {...} }, { "op": "remove_edge", "edge_id": "E-x" } ], "comment": "…" }` → 生成新 `draft` 版本 |
| `GET` | `/v1/situation/panorama/graph/edits` | 修改历史（分页；按版本/操作人过滤） |
| `GET` | `/v1/situation/panorama/graph/versions` | 版本清单（`version_id` / `version_status` / `created_by` / `created_at` / `change_summary`） |
| `POST` | `/v1/situation/panorama/graph/versions/{version_id}/publish` | 发布：`draft → deployed`，原 `deployed` 自动转 `archived`（对齐 `decisionModel.js` L42） |
| `POST` | `/v1/situation/panorama/graph/versions/{version_id}/restore` | 回滚：以该版本生成新 `draft` |
| `POST` | `/v1/situation/panorama/graph/imports` | 导入 JSON 生成 `draft`；**服务端校验**（字段齐、枚举合法、引用闭合），错误逐条返回不静默吞 |

```json
{
  "code": 0,
  "data": {
    "version_id": "v2026-10", "version_status": "draft",
    "applied": { "add_node": 3, "update_node": 1, "remove_edge": 2 },
    "edit_id": "EDIT-20261014-0007", "created_at": "2026-10-14T10:00:00+08:00"
  }
}
```

边界与硬约束：
- `base_version` 非当前 `deployed` → **409**（乐观锁，防并发覆盖）；冲突不自动合并。
- 编辑只写编辑历史/版本存储，**是否回写 Nebula 真源 = U4 未决**（图谱维护归属数据侧/算法侧，Java 不写 ADS 铁律同样适用于图库）。
- 版本对比（`CentralityPanel` 双版本 `v2025-01` vs `v2026-03` 对比）：`GET /graph/versions/diff?from=v2025-01&to=v2026-03` → 增删节点/边清单 + 中心性变化，**M2 首批可先只返增删清单，中心性变化为 U5**。

---

## 4. 数据需求与存储建议（DoD · Mock 先行 D7）

| # | 域 | 建议存储 | 关键字段 | 消费接口 | 备注 |
|---|---|---|---|---|---|
| 1 | 图谱节点 / 边 | **Nebula**（真源） | `node_id, entity_type, name, field, region, year, value` / `edge_id, source, target, relation_type, weight, year` | §3.1–§3.3 | Java 经 Python `/internal/*` 只读；不直连 nGQL |
| 2 | 编辑历史 | `ts_kg_edit_history`（app 侧） | `edit_id, version_id, op, payload, created_by, created_at` | §3.4 | 带写面 |
| 3 | 版本 | `ts_kg_version`（app 侧） | `version_id, version_status, base_version, change_summary, created_by, created_at, published_at` | §3.4 | 带写面 |
| 4 | 关键路径 / 实体评分 | ADS `ts_kg_critical_path` / `ts_kg_entity_score` | `path_id, node_ids, score, metric_id, calc_batch_id` | §3.2 / §3.3 | 算法产物带 `metric_id`（D9），Python 写 ADS |

**Mock 先行**：图谱 Mock 种子由 Python 按 demo `mockData.js` 结构写 ADS/图库（头注释标真源路径）；demo 种子随机数（`kgSeeded` L18–L31）为演示生成器，**禁止直接灌库当真源**。

## 5. 未决项（不伪闭合）

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | 图谱查询服务 `/internal/*` 路径与超时（大图切片） | M0 · human:徐腾强 + 算法侧 |
| U2 | 图谱结果集上限（§3.1 暂拟 2000 节点） | M0 拍板 |
| U3 | 场景化关键词预设（demo `keywordScenePresets`）是否服务端化 | M0 前端侧（human:孔东）核对 |
| U4 | 编辑批次是否回写 Nebula 真源、由谁写 | M0 + 数据侧（图谱维护归属） |
| U5 | 版本对比是否含中心性变化（首批可只返增删清单） | M0 + 算法侧 |
| U6 | 关键路径 / 实体评分 `metric_id` 清单登记 | `ALL-TS-D9`，随批 2 评审 |

## 6. 自检（冻结前）

- [ ] `entity_type` / `relation_type` 与 `mockData.js` L4–L41 逐字一致（无自造 key）
- [ ] 切片五 `slice_key` 语义与 `graphFilter.js` L63–L126 一致（服务端裁边，前端不裁）
- [ ] `timeline` 形状 = `{year, entities, relations}`（`graphFilter.js` L128–L141）
- [ ] 编辑批次乐观锁（`base_version` 409）与发布状态机（`draft→deployed→archived`）写明
- [ ] Java 不直连 nGQL；图谱查询走 `/internal/*` → Python
- [ ] 缺数 / 空态四态与 M1 §5 一致；`metric_id` 空时不传参

## 7. 会签记录（批 2 评审待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |
