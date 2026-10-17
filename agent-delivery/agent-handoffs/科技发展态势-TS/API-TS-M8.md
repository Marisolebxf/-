# API · 科技发展态势（TS）· M8 科技指数（接口契约草案）

> **任务**：`BE-TS-CONTRACT-02`（M2–M9 接口契约定义，按批冻结）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。本模块属**批 4**，批 4 开工前冻结。
> **范围**：仅 M8（科技指数 · demo `tech-index`/`tech-index-new`）。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `TS-模块开发规划与任务拆分.md` §4 M8（FE-TS-08a~08d） |
| 指标树（三级 + 权重 + 计算说明） | `demo-ui-science/src/pages/tech-index/mockData.js` L4–L141 `indicatorTreeData` |
| 科技指数 New 指标目录（8 件套 seed 镜像） | `demo-ui-science/src/pages/tech-index-new/metricCatalogMirror.js` L7–L25 |
| 赋权方法与公共算法口径 | `demo-ui-science/src/pages/tech-index-new/catalogConfig.js` L7–L13 |
| 需求规格说明书（可视化 / 专家 / 排行） | `demo-ui-science/docs/科技指数_需求规格说明书.md` L168–L342 |
| 未注册指标（D1 missing）处理 | `demo-ui-science/src/pages/tech-index-new/index.jsx` L54–L68 `UnregisteredIndicatorButton` |

---

## 1. 模块约定（增量）

全局约定继承 `API-TS-M1.md` §1 / §4 / §5。

| 项 | 约定 |
|---|---|
| 服务内路径前缀 | `/v1/situation/tech-index/**`（网关对外 `/display/v1/situation/tech-index/**`） |
| 指标目录复用 | 指标 8 件套（metric 8件套 + 四维就绪度）**统一走 `/metrics/v1/catalog`**（M1 §0 复用清单），M8 不另造指标目录接口；`metricCatalogMirror` 为前端只读 seed 镜像，头注释标真源路径 + 同步任务 ID |
| 赋权方法 | `catalogConfig.js` L7–L13：AHP 主观权重 × 熵权法客观权重等比合成；权重配置化、时间衰减；如有待确认 `pending_ref`，ReviewOnly 下显 ⚠️ 角标 |
| 读写面 | 全只读 ADS；无带写面（排行榜/专家评议均只读） |

## 2. 枚举字典（前端只读消费）

### 2.1 赋权方法 `weighting_method`（逐字）
`catalogConfig.js` L7–L13：AHP 主观权重 × 熵权法客观权重**等比合成**（等比合成四字逐字）。另有「时间衰减」规则，由后端配置项下发，前端不硬编码。

### 2.2 榜单类型 `ranking_type`（4 类，逐字）
`科技指数_需求规格说明书.md` L272–L342：综合 · 高校 · 企业 · 科研（科研机构）。

### 2.3 指数趋势维度 `trend_dimension`（4 类）
需求规格说明书 L168–L240 示例：创新指数 / 影响力趋势 / 活跃度 / 综合指数（正式维度名随字典下发，U2）。

### 2.4 专家活跃度 `expert_activity`（逐字）
需求规格说明书：H 指数 + 活跃度评分（正式口径随字典下发）。

### 2.5 指数构成权重（40/30/20/10）
需求规格说明书 / 原型：综合排名得分构成 = 40%（科研）/ 30%（产业）/ 20%（技术）/ 10%（政策），**按模块产品定义执行**；M8 指标树各节点权重由后端 `weight` 字段直接下发（`indicatorTreeData` L9/L18 等），前端不自行加总。

## 3. 接口清单（5 类）

### 3.1 `GET /v1/situation/tech-index/indicator-tree` — 指标树（三级 + 权重 + 赋权方法 + 版本历史）

**用途**（规划 M8-BE ①）：FE-TS-08a 指标树 Tab（三级缩进 + 权重说明 + 版本历史）。

| Query | 说明 |
|---|---|
| `version` | 可选，默认当前版本 |

```json
{
  "code": 0,
  "data": {
    "current_version": "v2026-03",
    "weighting_method": "AHP 主观权重 × 熵权法客观权重等比合成",
    "weighting_notes": ["权重配置化", "时间衰减"],
    "nodes": [
      {
        "node_id": "1", "name": "科技创新能力", "level": 1, "weight": 0.40,
        "description": "衡量区域/机构科技创新综合能力的核心指标，反映科技创新的基础实力和核心竞争力",
        "calculation": "加权求和二级指标得分：科研投入×0.5 + 创新产出×0.5",
        "significance": "…",
        "children": [
          {
            "node_id": "1-1", "name": "科研投入", "level": 2, "weight": 0.50,
            "description": "衡量科技创新资源投入强度的指标",
            "children": [
              { "node_id": "1-1-1", "name": "R&D 经费投入", "level": 3, "weight": 0.60,
                "description": "年度研发投入经费总额占 GDP 比例",
                "calculation": "R&D 经费/GDP×100%", "significance": "…", "metric_id": "Q0xx" }
            ]
          }
        ]
      }
    ],
    "versions": [
      { "version": "v2026-03", "effective_from": "2026-03-01", "change_log": "…" }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

字段逐字对齐 `indicatorTreeData`（`mockData.js` L4–L141）。边界：
- 三级结构固定（`level=1/2/3`），前端按 `level` 缩进，不依赖 `children` 深度硬编码。
- `metric_id` 仅在三级叶节点挂接；非叶节点不挂 `metric_id`（它们由子节点合成）。
- `metric_id` 已在 `/metrics/v1/catalog` 登记则走 8 件套弹卡（D9 ⓘ）；未登记 → D1 missing 红问号（`UnregisteredIndicatorButton`，L54–L68）。

### 3.2 `GET /v1/situation/tech-index/region-index` — 区域指数（34 省 + 五年序列）

**用途**（规划 M8-BE ②）：FE-TS-08b 34 省地图 + 专家 H 指数 + 四维趋势。

```json
{
  "code": 0,
  "data": {
    "regions": [
      { "region_code": "44", "region_name": "广东", "index_value": 92.4, "year": "2026", "rank": 1, "metric_id": "Q0xx" }
    ],
    "trend_series": [
      { "dimension_key": "innovation", "label": "创新指数", "years": ["2020","2021","2022","2023","2024","2025","2026"], "values": [78, 81, 84, 87, 90, 92, 94] }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：34 省清单由后端字典全量下发；`index_value` 为算法产物带 `metric_id`；缺省指数返 `null`（不参与排名，不补 0）。

### 3.3 `GET /v1/situation/tech-index/experts` — 专家数据（20 人 + H 指数 + 活跃度）

**用途**（规划 M8-BE ③）：FE-TS-08d 专家评议（20 人只读）。

```json
{
  "code": 0,
  "data": {
    "total": 20, "page": 1, "size": 20,
    "records": [
      { "expert_id": "EX-001", "name": "张三", "institution": "清华大学",
        "field": "人工智能", "h_index": 48, "activity_score": 82.5,
        "paper_count": 120, "patent_count": 15, "metric_id": "Q0xx" }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

字段对齐需求规格说明书专家数据段。边界：专家名单为**评审定向输入**（20 人为展示样本量，非全量），数据源待对齐（U3）；`metric_id` 挂接每个统计数字（D9）。

### 3.4 `GET /v1/situation/tech-index/trends` — 指数趋势（四维时序）

**用途**（规划 M8-BE ②）：FE-TS-08b 四维趋势。

```json
{
  "code": 0,
  "data": {
    "dimensions": [
      { "dimension_key": "innovation",  "label": "创新指数",   "years": ["2020","2021","2022","2023","2024","2025","2026"], "values": [78,81,84,87,90,92,94], "metric_id": "Q0xx" },
      { "dimension_key": "influence",   "label": "影响力趋势", "years": ["2020","2021","2022","2023","2024","2025","2026"], "values": [72,74,78,80,83,85,87], "metric_id": "Q0xx" },
      { "dimension_key": "activity",    "label": "活跃度",     "years": ["2020","2021","2022","2023","2024","2025","2026"], "values": [70,73,76,79,82,84,86], "metric_id": "Q0xx" },
      { "dimension_key": "composite",   "label": "综合指数",   "years": ["2020","2021","2022","2023","2024","2025","2026"], "values": [75,78,81,84,87,89,91], "metric_id": "Q0xx" }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

### 3.5 `GET /v1/situation/tech-index/rankings` — 成果排行（综合/高校/企业/科研 + 详情）

**用途**（规划 M8-BE ②）：FE-TS-08c 排行榜。

| Query | 说明 |
|---|---|
| `ranking_type` | `composite` / `university` / `enterprise` / `research` |
| `region_scope` / `year` | 可选 |

```json
{
  "code": 0,
  "data": {
    "ranking_type": "composite",
    "total": 33, "page": 1, "size": 20,
    "records": [
      { "rank": 1, "name": "清华大学", "region": "北京",
        "score": 94.5, "composite_breakdown": { "research": 37.8, "industry": 28.4, "technology": 18.9, "policy": 9.4 },
        "history": [ { "year": "2024", "score": 93.2 }, { "year": "2025", "score": 94.5 } ],
        "metric_id": "Q0xx" }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：`composite_breakdown` 权重 40/30/20/10 按模块产品定义（L272–L342）；`history` 含历年得分；排行数量固定 33 条为演示口径，正式上限按分页 `size` 控制。

## 4. 数据需求与存储建议（Mock 先行 D7）

| # | 域 | 建议表名 | 关键字段 | 消费接口 | 备注 |
|---|---|---|---|---|---|
| 1 | 指标树 | `ts_ti_indicator_tree`（只读字典） | `node_id, name, level, weight, parent_id, description, calculation, significance, metric_id, version` | §3.1 | 版本化 |
| 2 | 区域指数 | `ts_ti_region_index` | `region_code, region_name, year, index_value, rank, metric_id` | §3.2 | 34 省 |
| 3 | 专家 | `ts_ti_expert` | `expert_id, name, institution, field, h_index, activity_score, paper_count, patent_count, metric_id` | §3.3 | 数据源待对齐 |
| 4 | 趋势 | `ts_ti_trend` | `dimension_key, year, value, metric_id` | §3.4 | 四维 |
| 5 | 排行 | `ts_ti_ranking` | `ranking_type, year, rank, object_id, name, region, score, composite_breakdown JSON, metric_id` | §3.5 | 四榜 |

## 5. 未决项

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | 指标树版本化：版本触发方式（人工 / 算法训练完成自动发布） | M0 拍板 |
| U2 | 指数趋势四维 key 命名与 `trend_dimension` 枚举定稿 | M0 产品侧 + `ALL-TS-D9` |
| U3 | 20 专家数据源（人事库 / 人才库 / 评审定向输入）与更新频率 | M0 + 数据侧 |
| U4 | 未注册 `metric_id`（D1 missing）的治理引用清单（`pending_ref` / `Q-TINDEX-02`） | 指标口径组（王惠） |
| U5 | 排行榜 `composite_breakdown` 四子项命名与权重（40/30/20/10 是否需可配置） | M0 产品侧 |

## 6. 自检（冻结前）

- [ ] 指标树字段与 `indicatorTreeData`（L4–L141）逐字一致
- [ ] 赋权方法与 `catalogConfig.js` L7–L13 逐字一致（AHP × 熵权法等比合成）
- [ ] 指标 8 件套走 `/metrics/v1/catalog`，M8 不另造指标目录接口
- [ ] 未注册 metric_id 按 D1 missing 处理（红问号，不显伪 8 件套）
- [ ] 排行榜 composite_breakdown 权重标注（40/30/20/10 或等比合成值），前端与后端一致
- [ ] 缺数 / 空态与 M1 §5 一致

## 7. 会签记录（批 4 评审待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |
