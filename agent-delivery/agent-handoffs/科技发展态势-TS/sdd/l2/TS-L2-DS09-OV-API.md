# TS-L2-DS09-OV-API · 综合发展规划 · 后台接口设计

> **任务**：`TS-L2-DS09-OV-API`（definition，不写业务代码）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 api-agent · **监管**：`human:王梓真`
> **状态**：**v2**——architect / api / algorithm 三家会签已审**同意**，必改项（talent stats 现算 / od_nodes / 列名更正 / M1 回填规则 / S-1 range / A3 产物表 / F5–F7 注记）已修订，见文末「会签修订记录 v2」；待 data 会签（od_nodes 加列、`sys_user_planning_push_record` DDL 等联动项，§9）
> **硬依赖**：`sdd/l2/TS-L2-DS09-OV-ARCH.md` 已落盘（本文与其冲突时，改本文不改 ARCH 稿）

**输入真源**

| 用途 | 真源 |
|---|---|
| 架构硬依赖 | `sdd/l2/TS-L2-DS09-OV-ARCH.md`（§0 逐叶判定、§4 逐叶架构、§5 差异收口、§6 D18 三要素） |
| 契约草案（批 4 未冻结） | `agent-handoffs/科技发展态势-TS/API-TS-M9.md` §1 约定、§2 枚举、§3.1–§3.6（OV 范围） |
| 全局约定 | `API-TS-M1.md` §1 信封/错误码/公共入参、§4 D9 血缘、§5 空态四态 |
| 订阅体系既有实现 | `SITUATION-ENT-SUBSCRIPTION-PUSH-L01.md`（SubscriptionPushJob / SubscriptionAdapter / SubscriptionNotifyService / app_user 家族） |
| FE 现状 | `repos/lumen-ui-science-pc/src/api/situation/techDevelopmentPlan.ts` + `src/types/techDevelopmentPlan.ts`（dataset 形状） |
| 指标赋号 | ARCH 稿 §0 表（5 个 `M_INNOV_PLAN_*` 均为赋号草稿·类型未签，公式 pending `human:唐绍祖`） |
| 数据侧 DDL 与实测 | `sdd/l2/TS-L2-DS09-OV-DATA.md`（**列名以 DATA DDL 为准**：§2.1 `caliber_def`、§2.2 序列表、§2.3 `metric_system`、§2.6 `local_adv`、§2.7 talent 实测裁定、§5 订阅面零 DDL） |

**范围**：DS-09 综合发展规划页签（FE-TS-09a，需规序 **178–184** 共 7 叶）的后台接口定稿——9 端点、DTO、错误码、501 机制、订阅面、FE 接线差异、批 4 冻结 delta。**不含** 09b 重点领域（§3.7）/ 09c 研究分析（§3.8），那两组归 KEY/RES 分册另行起草（ARCH §7）。

---

## 0. 总则

| 项 | 定稿 |
|---|---|
| 落仓 | `lumen-svc-platform/gkxlumen-display`，新增 `PlanningController`（`@RequestMapping("/v1/situation/planning")`）+ `PlanningQueryService`（只读）；沿 ARCH §7 U1 建议：三页签统一 `planning` 前缀单 Controller，不按 09a/09b/09c 拆服务路由 |
| 网关路径 | 按 api 规约铁律 9 拼接：`gateway地址 / display / v1/situation/planning / {方法映射}`，即网关对外 `/display/v1/situation/planning/**`，与 M1 §1.1 冻结前缀一致；服务内（Feign/直连）路径不带 `/display` |
| 响应信封 | 统一 `R<T>`：`{ "code": 0, "msg": "ok", "data": {…} }`（`gkxlumen-common-core` `R.java`，M1 §1.2）。`code≠0` 时 `data=null`，前端走空态不伪造。本文错误信封的文案字段即 `msg`（任务书表述的 message 不另造字段名） |
| 错误码 | `400`（枚举外值/缺必填/分页越限）· `401/403`（网关登录态，订阅写面必登）· `500`（服务异常）· `501`（**仅 §2.7 direction-warnings**，机制见 §3）。无路径 id 类端点，本分册不用 404/409 |
| 空态 | 无行 = `200` + 空数组 + `empty_reason`（`no_source` / `filter_empty`，M1 §5 四态）；**禁止**以 0 冒充缺失、禁止补演示行 |
| 读写面 | 8 读 1 写（唯一写面 = §5 PUT subscriptions，app_user 家族）；其余全部只读 ADS |
| metric_id | 本文所有 `metric_id` / `metric_ids` 值均为 ARCH 稿 §0 的**赋号草稿·未签**（`M_INNOV_PLAN_*`，公式 pending），仅替换契约样例中的 `Q0xx` 占位；**不发明任何新 `M_*`**。**回填规则（会签落册）**：回填值=五草稿号**逐字**——§3.2=`M_INNOV_PLAN_HEAT`+`M_INNOV_PLAN_GROWTH`、§3.4=`M_INNOV_PLAN_LOCAL_ADV`、§3.5=`M_INNOV_PLAN_TALENT_FLOW`、§3.1=`M_INNOV_PLAN_DIRECTION_ALERT`、§3.3 恒 `[]`；**禁取** `Q010`–`Q019` / `QPOL-*` 等占位段；回填时点=**批 4 冻结**，由 `BE-TS-CONTRACT-02` 落契约正文；物理行源=各表 `metric_id` 列 |
| 文案铁律 | `caliber_note` / `source` / 口径说明等诚实标注字段一律由 **D18 表行携带**（来源列在 §2 各字段表写明），**禁止 Java 硬编码文案**；服务端错误 `msg` 属错误信息非数据口径文案，允许代码常量 |
| Mock 徽标 | 全部 D18 表读数的 D4 仍 mock → FE 🧪 MockBadge 保留至 D4 翻转（ARCH G-B5）；统计数旁 ⓘ draft 语义卡回指核对记录 §赋号表，禁点 `M_CHAIN_*` / `M_SYNTH_*` 等伪 8 件套 |

---

## 1. 端点总表（9）

| # | 方法 | 服务内路径 | 网关路径（`/display` 前缀） | 需规叶（seq·叶名） | D18 表 / 存储 | 读/写 |
|---|---|---|---|---|---|---|
| 1 | GET | `/v1/situation/planning/hot-technologies` | `/display/v1/situation/planning/hot-technologies` | 178 · 全球热点技术捕捉 | `ts_plan_hot_tech` + `ts_plan_hot_tech_series` | 读 |
| 2 | GET | `/v1/situation/planning/metric-system` | `/display/v1/situation/planning/metric-system` | 179 · 多维度指标体系展示 | `ts_plan_metric_system` | 读（**ARCH 新增第 9 端点**，G-B2 方案 A） |
| 3 | GET | `/v1/situation/planning/tracking` | `/display/v1/situation/planning/tracking` | 180 · 技术与产业热点动态跟踪 | `ts_plan_tracking_event` + `ts_plan_tracking_point` | 读 |
| 4 | GET | `/v1/situation/planning/local-advantage` | `/display/v1/situation/planning/local-advantage` | 181 · 本地特色与优势分析 | `ts_plan_local_adv` | 读 |
| 5 | GET | `/v1/situation/planning/talent-flow` | `/display/v1/situation/planning/talent-flow` | 182 · 科技人才流动监控 | `ts_plan_talent_flow`（仅聚合计数行） | 读 |
| 6 | GET | `/v1/situation/planning/resource-push` | `/display/v1/situation/planning/resource-push` | 183 · 科创资源整合与推送 | `sys_user_planning_push_record`（**新表**，A3 裁定）× `sys_user_subscription_rule`（既有） | 读（按用户隔离） |
| 7 | GET | `/v1/situation/planning/resource-push/subscriptions` | `/display/v1/situation/planning/resource-push/subscriptions` | 183 · 同上 | `sys_user_subscription_rule`（既有） | 读 |
| 8 | PUT | `/v1/situation/planning/resource-push/subscriptions` | `/display/v1/situation/planning/resource-push/subscriptions` | 183 · 同上 | `sys_user_subscription_rule`（既有） | **写（本二级唯一写面）** |
| 9 | GET | `/v1/situation/planning/direction-warnings` | `/display/v1/situation/planning/direction-warnings` | 184 · 潜在科技发展方向预警 | `ts_plan_direction_warning`（V1 零行） | 读（**501 通道**，§3） |

> 契约 §3.1–§3.6 共 8 端点 + ARCH 稿 §4.2 新增 metric-system = 9。表/DDL 定稿归 OV-DATA 分册（库名建议 `gkxlumenx_ads`、`ts_plan_` 前缀，不进 ODS/DWD、不带 `gapfill_`——D18 铁律）。

---

## 2. 逐端点定稿

各节 JSON 示例与 API-TS-M9 对应节**逐字同构**；仅两处替换/标注：① `Q0xx` 占位换为 ARCH §0 赋号草稿（未签）；② ARCH §5 差异（表拆分、179 新端点、5 维度行）在「差异」行标注。

### 2.1 GET hot-technologies（seq 178，契约 §3.2）

**Query**（S-1 裁定，批 4 建议 §7-9）：

| Query | 类型 | 说明 |
|---|---|---|
| `range` | enum | 概览时间窗 `3m` / `6m` / `12m`（复用 §4 枚举），默认 `12m`；按 `range_key` 选取 `heat_series` 序列分区（3m 3 期 / 6m 4 期 / 12m 9 期，DATA §2.2）；出枚举 `400` |

8 技术行全量返回，量级固定不分页。

```json
{
  "code": 0,
  "data": {
    "items": [
      { "tech_id": "1", "name": "人工智能大模型", "category": "AI",
        "heat": 98, "growth": 45.2, "hot_trend": "hot",
        "patents": 12580, "papers": 3420,
        "description": "大语言模型技术持续突破，多模态融合成为新方向",
        "heat_series": [ { "year": "2026Q1", "heat": 91 }, { "year": "2026Q2", "heat": 98 } ],
        "spatial_distribution": [ { "name": "南山区", "factor": 1.08 } ],
        "metric_id": "M_INNOV_PLAN_HEAT" }
    ],
    "caliber_note": "热度 = 论文 40% / 专利 30% / 项目 20% / 资讯 10%（口径待 M0 定稿，U5）",
    "metric_ids": ["M_INNOV_PLAN_HEAT", "M_INNOV_PLAN_GROWTH"]
  }
}
```

| 字段 | 类型 | 说明 | 来源表列 |
|---|---|---|---|
| `items[].tech_id` | string | 行标识 | `ts_plan_hot_tech.tech_id` |
| `items[].name` / `category` | string | 技术名 / 分类 | 同表 `name` / `category` |
| `items[].heat` | int | 热度指数（MIXED 口径，`M_INNOV_PLAN_HEAT` 赋号草稿·未签） | 同表 `heat` |
| `items[].growth` | number | 增长速度 %（`M_INNOV_PLAN_GROWTH` 草稿·未签） | 同表 `growth` |
| `items[].hot_trend` | enum | §4 热度三趋势，逐字冻结 | 同表 `hot_trend` |
| `items[].patents` / `papers` | int | 专利 / 论文数 | 同表 `patents` / `papers` |
| `items[].description` | string | 技术描述 | 同表 `description` |
| `items[].heat_series[]` | `{year,heat}[]` | 热度序列：**`year` 字段语义冻结为「期标签」**（季度粒度逐字，如 `2025Q4`…`2026Q2`；由 API 拼装层从 `period_label` 映射，DATA §0.1/S-1），随 `range` 分区截取 | `ts_plan_hot_tech_series`（按 `tech_id`+`range_key` 关联，`period_label` / `heat_value` 列） |
| `items[].spatial_distribution[]` | `{name,factor}[]` | 空间分布因子（5 区，**无坐标**；柱图派生 `heat×factor` 由 FE 做，DATA §0.2）；坐标类点位语义由 `ts_plan_tracking_point` 承载（跨端点）或实现单落定（F3，§7-10） | `ts_plan_hot_tech.spatial_distribution`（JSON 列，种子逐字） |
| `items[].metric_id` | string | 行主指标=热度（草稿·未签） | 同表 `metric_id` 列 |
| `caliber_note` | string | 热度口径说明（含「待 M0 定稿，U5」文案）——**表行携带，禁 Java 硬编码** | `ts_plan_hot_tech.caliber_def`（JSON 列：三要素 `{scoreFormula,inclusionRules,defaultRule}` 种子逐字；Java 取任一行拼装，8 行同值，DATA §2.1） |
| `metric_ids` | string[] | 两指标草稿·未签 | 由 Service 按表 `metric_id` 列去重汇总 |

**错误码**：`400`（`range` 出枚举）；401/403/500；空态 `200 items=[]` + `empty_reason=no_source`（honestEmpty）。
**差异**（F3/S-1，均补进 §7 批 4 delta）：① `heat_series.year` 语义冻结为「期标签」（季度逐字，非年度）；② `spatial_distribution` 形状由契约示例 `{region,heat,lng,lat}` 更正为种子实际 `{name,factor}`（无坐标，坐标归 tracking_point）；③ 新增 `range` Query。

### 2.2 GET metric-system（seq 179，ARCH §4.2 新增端点，G-B2 方案 A）

**Query**：无（7 分类全量）。

```json
{
  "code": 0,
  "data": {
    "categories": [
      { "category_key": "technology", "category_label": "技术库", "category_order": 1,
        "metrics": [ { "metric_label": "技术领域数", "metric_value": "128", "metric_unit": "个", "metric_change": "+12.3%" } ],
        "linked": ["…"] }
    ]
  }
}
```

| 字段 | 类型 | 说明 | 来源表列 |
|---|---|---|---|
| `categories[].category_key` | string | 分类英文 key（demo 种子冻结，7 类） | `ts_plan_metric_system.category_key` |
| `categories[].category_label` | string | 分类中文显示名 | 同表 `category_label`（DATA §2.3 已列，禁前端写死） |
| `categories[].category_order` | int | 分类顺序 1..7 | 同表 `category_order` |
| `categories[].linked` | string[] | 分类联动标签（DATA §2.3 `linked_json` 列已存，随分类下发；替代 FE 静态） | 同表 `linked_json`（JSON 列，冗余存于该类每行，Java 去重取一份） |
| `categories[].metrics[].metric_label` | string | 指标卡名 | 同表 `metric_label` |
| `categories[].metrics[].metric_value` | string | 指标值逐字字符串（不数值化，demo 口径，🧪） | 同表 `metric_value` |
| `categories[].metrics[].metric_unit` | string? | 单位（从 value 机械拆分，可空） | 同表 `metric_unit` |
| `categories[].metrics[].metric_change` | string | 环比字符串逐字（如 `+12.3%`，🧪）——F4 列名统一 | 同表 `metric_change` |

**metric_id**：无（N/A：大屏运营壳，无统计核，依据 ARCH §4.2；**不设 `metric_id`/`metric_ids` 字段**）。
**错误码**：401/403/500；空态 `200 categories=[]`。
**差异**：**契约 §3 无此端点**，本节即其 DTO 定稿，批 4 冻结时并入（建议编号 §3.2a，避免重排 §3.3–§3.8 引用，见 §7）。**全组列名以 DATA DDL（§2.3）为准**（F4：`note`→`metric_change`、`value`→`metric_value`、`unit`→`metric_unit`、`linked` 改由表 `linked_json` 列下发）。自定义布局持久化不做（FE 交互态，ARCH §4.2）。

### 2.3 GET tracking（seq 180，契约 §3.3）

**Query**：

| Query | 类型 | 说明 |
|---|---|---|
| `time_mode` | enum | `year` / `month`，默认 `year`（契约原文：切换参数由公共筛选承载） |
| `space_mode` | enum | `global` / `gba` / `shenzhen`，默认 `global`（语义对齐 M1 §1.3 `region_scope` 三级） |

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

| 字段 | 类型 | 说明 | 来源表列 |
|---|---|---|---|
| `timeline.title/current_year/range_label/years[]` | string/[] | 时间轴元信息 | `ts_plan_tracking_event`（`row_kind='timeline_meta'` 行：`title` / `current_year` / `range_label` / `years_json`，DATA §2.4） |
| `timeline.events[].date/region/text` | string | 演进事件（demo `techDevelopmentPlanTimeline` 冻结种子，7 条） | 同表（`row_kind='event'` 行：`event_date` / `region` / `event_text`） |
| `spatial.map_center/zoom` | number[]/number | 地图中心/缩放——**展示配置常量**（demo `techDevelopmentPlanMapConfig` 冻结），非统计数据，允许代码常量（会签认可；如否决改配置行携带） | —（展示配置） |
| `spatial.points[].result_type` | enum | §4 图层五类，逐字冻结 | `ts_plan_tracking_point.result_type` |
| `spatial.points[].name/lng/lat/score` | — | 点位名/坐标/分值（35 行=7 点×5 层，`WHERE result_type=?` 直拼，DATA §2.5） | 同表 `name` / `region` / `lng` / `lat` / `score` |
| `metric_ids` | string[] | 恒 `[]`：无独立统计核，消费 178 两指标（ARCH §0） | — |

**错误码**：`400`（`time_mode`/`space_mode` 出枚举，不静默改）；401/403/500；空态 `200` 空数组。
**差异**：契约 §4 #1 `ts_plan_record` 原拟由 §3.3/§3.4 聚合消费 → ARCH §5 改为本叶专用 `ts_plan_tracking_event` + `ts_plan_tracking_point` 两表，`ts_plan_record` 取消。空间分布无地理专核，COMP-B03 语义债保持（ARCH §4.3）。

### 2.4 GET local-advantage（seq 181，契约 §3.4）

**Query**：无。

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
    "metric_ids": ["M_INNOV_PLAN_LOCAL_ADV"]
  }
}
```

| 字段 | 类型 | 说明 | 来源表列 |
|---|---|---|---|
| `base_region` / `compare_to` | string | 本地=深圳 / 对照=全球 | `ts_plan_local_adv.base_region` / `compare_to` |
| `dimensions[].key/label` | string | 维度 key 与中文标签（契约三键 field/capability/output 逐字；`capability` 维行源=FE 补的 innovation 图，映射写进灌数转换，DATA S-2） | 同表 `dimension_key` / `dimension_label` |
| `dimensions[].local/global_avg` | number | 维度汇总分（若批 4 采纳 `items[]` 则为聚合值） | 同表 `local_score` / `global_score`（DATA §2.6：18 行=3 维×6 对比项） |
| `dimensions[].detail` | string | 说明（DATA DDL 无对应列，V1 置空，批 4 定去留） | —（无列） |
| `reference_stats.global.hotspots/carriers/capacity` | number | 全球对照统计（**契约草案示例值逐字**，`source='contract_draft_sample'`，DATA §0.4/S-3） | 同表 `reference_json`（`row_kind='reference'` 行，JSON 列） |
| `reference_stats.global.source` | string | 样本口径标注，**必返，表行携带**；「示例抽样」字样保持至正式态换真源（契约 §3.4 边界） | 同 `reference_json.source` |
| `metric_ids` | string[] | `M_INNOV_PLAN_LOCAL_ADV`（MODEL 草稿·未签，Q-MO-DS09-01 保持） | 同表 `metric_id` 列 |

**错误码**：401/403/500；空态 `200 dimensions=[]` + `empty_reason=no_source`。
**差异**：① DATA §2.6 实测落位为**契约三键 × 各 6 对比项 = 18 维度行 + 1 reference 行**（`capability` 维承接 FE 补的 innovation 图、`source='lumen_seed'` 标注，S-2；ARCH「5 维度行」表述据此收口为三键）；② FE 三块图表需**子项级序列**（`yAxis[]` 多行），契约 `dimensions` 为维度级标量 → 建议批 4 在 `dimensions[]` 增 `items[]{name,local,global_avg}` 子行——DATA 行型已按「维度 × 对比项」存储，本建议与其一致，见 §7-5，待会签。

### 2.5 GET talent-flow（seq 182，契约 §3.5）

**Query**：

| Query | 类型 | 说明 |
|---|---|---|
| `flow_type` | enum | §4 流动三类型（中文字面量逐字）；缺省全量 |
| `risk_level` | enum | 可选，`warning`（demo L1665：`riskLevel='warning' or warning=true`） |

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
    "od_nodes": [
      { "name": "深圳", "color": "#1677ff", "od_total": 18932, "trend_pct": 21.7 },
      { "name": "…", "color": "#…", "od_total": 12458, "trend_pct": 16.2 }
    ],
    "metric_ids": ["M_INNOV_PLAN_TALENT_FLOW"]
  }
}
```

| 字段 | 类型 | 说明 | 来源表列 |
|---|---|---|---|
| `stats.*` | int | 汇总四数——**Java 由表行现场聚合计算，无预聚合种子行**（DATA §2.7 实测裁定：`warning_count`=记录行 `risk_level='warning'` 计数**实测=2**；方向计数按 `flow_type` 聚合；`net_inflow` 聚合口径随实现单与 DATA 对齐）。**示例四数为契约草案演示值** | 现算：`record` / `institution_flow` 行（无 stats 专行专列） |
| `institution_flows[].*` | — | 机构净流入行（`direction` ∈ `in`/`out`） | 同表（`row_kind='institution_flow'`：`institution` / `net_inflow` / `flow_direction`） |
| `records[].flow_id/from/to/flow_type/person_count/risk_level/warning/field/updated_at` | — | 聚合行：from/to **机构级**、`person_count` 计数（恒 1）、`flow_type` 两存储值（「预警流动」=筛选特例不落行，DATA S-4）、`risk_level` | 同表（`row_kind='record'`：`flow_id` / `from_org` / `to_org` / `flow_type` / `person_count` / `risk_level` / `field` / `updated_at`） |
| `od_nodes[]` | `{name,color,od_total,trend_pct}[]` | **新增（F2）**：人才流向图六类节点（含色值）+ `od_total` OD 总量（深圳=18932 / 外地=12458）+ `trend_pct` 增幅——**G-B4 写死值在 DTO 层闭合**，FE/api 层删写死改读字段；示例数值为演示值 | `ts_plan_talent_flow.od_nodes`（**JSON 列，DATA 侧同步加列**，v2 联动项 §9） |
| `metric_ids` | string[] | `M_INNOV_PLAN_TALENT_FLOW`（MODEL 草稿·未签；⚠️ Q-MO-DS09-02 + U6 法务未决） | 同表 `metric_id` 列 |

**错误码**：`400`（`flow_type`/`risk_level` 出枚举）；401/403/500；空态 `200` 空数组。
**U6 合规（表结构级）**：`ts_plan_talent_flow` **不设姓名/证件/个人 ID 列**（种子 `name`/`avatar` 提取阶段即丢弃，DATA §4），只存机构级聚合计数行；DTO 无任何个人明细字段（ARCH §4.5）。行型（institution_flow / record）DDL 见 DATA §2.7；`stats` 无专行、Java 现算（上文）；`od_nodes` JSON 列 DATA 侧同步加。

### 2.6 GET resource-push（seq 183，契约 §3.6 清单）

**Query**（本分册定稿补充，对齐 M1 §1.4）：

| Query | 类型 | 说明 |
|---|---|---|
| `resource_type` | enum? | §4 新增四类，单选过滤 |
| `field` | string? | 领域过滤 |
| `is_read` | bool? | 已读过滤 |
| `page` / `size` | int | 默认 1 / 20，`size` 上限 100 |

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

| 字段 | 类型 | 说明 | 来源 |
|---|---|---|---|
| `records[].resource_id/resource_type/title/field/pushed_at` | — | 推送产物行（四类资源池命中后落库） | **`sys_user_planning_push_record`**（app_user 家族**新表**，A3 裁定：`sys_user_notification` 实测无 `resource_type`/`field` 列，过滤+分页不可维护；DDL 由 DATA 侧补，v2 联动项 §9） |
| `records[].is_read` | bool | 已读状态，按用户隔离 | 已读记录（复用 M4 §3.4 已读模式） |
| `subscriptions` | object | 当前用户订阅设置随清单回显（首屏免二次请求；契约样例即此形态），DTO 见 §5 | `sys_user_subscription_rule`（`scope_type='planning_resource'`） |

**错误码**：`400`（`resource_type` 出枚举 / `size`>100）；401/403/500；空态 `200 records=[]`（资源池无命中=诚实空态，ARCH §4.6）。
**差异**：契约 §3.6 未定 Query；本节补充项批 4 一并冻结（§7-6）。

### 2.7 GET direction-warnings（seq 184，契约 §3.1）

**Query**：

| Query | 类型 | 说明 |
|---|---|---|
| `field` | string? | 技术领域过滤（demo 按 field 过滤 L1327–L1329） |
| `warning_level` | enum? | §4 三级（`high`/`medium`/`watch`） |

**处理顺序**：Query 枚举校验（`400` 优先）→ 模型注册检测（未注册 → `501`，见 §3）→ 读 `ts_plan_direction_warning`。

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
        "metric_id": "M_INNOV_PLAN_DIRECTION_ALERT" }
    ],
    "report_meta": { "title": "潜在科技发展方向预警报告", "generated_at": "2026-10-14 08:00", "high_count": 1, "medium_count": 2, "watch_count": 3 },
    "metric_ids": ["M_INNOV_PLAN_DIRECTION_ALERT"]
  }
}
```

| 字段 | 类型 | 说明 | 来源表列 |
|---|---|---|---|
| `source_averages[]` | `{source,label,avg}[]` | **六源均分由服务端按当前可见 items 计算**（对齐 demo L1331–L1337），前端不自算；注册后无行 → 空集 `[]`（服务端语义） | 由 `items` 现算（无独立列） |
| `items[].warning_id/name/field/warning_level/level_label/signal/summary/updated_at` | — | 预警卡主体（逐字对齐 `DirectionMonitorItem` L401–L435） | `ts_plan_direction_warning` 对应列 |
| `items[].sources.<六源>.{score,delta,note}` | — | 六源信号；`delta` 字符串百分比（demo 口径，数值化待 M0，U4） | 同表 `sources`（六源 JSON 列） |
| `items[].metric_id` | string | `M_INNOV_PLAN_DIRECTION_ALERT`（501 pending·赋号草稿未签） | 同表 `metric_id` 列 |
| `report_meta` | object | 报告产物元信息（对齐 `directionMonitorReport`） | 同表聚合（等级计数现算） |

**错误码**：`400`（`warning_level` 出枚举）；`501`（模型未注册，§3）；401/403/500；注册后无行 = `200` + `items=[]` + `source_averages=[]` + `empty_reason=no_source`（复用 M1 §5 枚举，`empty_message` 文案区分「模型已注册，暂无预警产出」；不新增枚举值）。
**边界**：报告下载走 M1 §3.8 导出任务中心（`content_key=planning-direction-warning`），不单独造下载接口；501 期建导出任务同步拒绝（§3）。`ts_plan_direction_warning` **V1 零行、永不灌演示行**（ARCH §4.7；「空态不得用假规划正文填」）。

---

## 3. 501 机制（direction-warnings 专属）

### 3.1 触发与信封

`M_INNOV_PLAN_DIRECTION_ALERT` MODEL 未注册（公式 pending，reuse=0）→ Java 侧按**模型注册检测**短路返回 501，不查表。沿用「Job 未注册则 501」先例（POL PC-4 模式，ARCH §4.7）。

```text
HTTP/1.1 501 Not Implemented

{
  "code": 501,
  "msg": "预警模型未注册：M_INNOV_PLAN_DIRECTION_ALERT 尚未上线（赋号草稿·未签）",
  "data": null
}
```

- 信封沿用 `R.java`（`code`/`msg`/`data`），不另造字段；任务书表述的 message 即 `msg` 承载文案。
- `msg` 属服务端错误信息（非数据口径文案），允许代码常量；**前端只按 HTTP 状态码 501 判定，不解析 `msg` 文案**（文案可变）。
- 网关透传 501，不改写、不吞（网关侧需确认无 501→500 改写规则——落实现单核验项）。

### 3.2 前端空态语义（G-B6）

| 信号 | 前端动作 |
|---|---|
| HTTP 501 | 方向预警区**空态** + ⚠️「预警模型未注册」角标；**报告导出入口禁用**（`content_key=planning-direction-warning`）；不显伪指标卡 |
| 200 + 空集 | 正常空态（「暂无预警产出」），导出入口按 report_meta 判定 |
| 501 非覆盖证明 | 差集 missing 保持，不升 🟢（ARCH §7） |

后端防御：M1 §3.8 导出任务中心对本 `content_key` 挂**同一开关闸门**——未注册时 `POST /export/jobs` 对该 content_key 返回 501，与读端点语义一致（前端禁用是第一道，服务端拒绝是第二道）。

### 3.3 检测开关载体（二选一，本分册裁定）

**建议：配置项**（Spring `Environment` / Nacos 配置中心）：

```yaml
planning:
  direction-alert:
    registered: false   # boolean，诚实默认 false（未注册）
```

理由：

1. **开关语义是部署期事实**：模型是否注册上线由算法侧交付与部署动作决定，属运维事实，不是运营内容——没有运营后台改它的场景，字典表引入不必要的写面。
2. **环境差异化天然支持**：模型先在 dev 注册联调、prod 仍 501，配置项按环境注入即可；字典表跨环境同步反而复杂。
3. **与前端消费无关**：字典表适合前端下拉/图例类内容（如 `warning_level` 标签色值），该开关不进任何下拉，无字典消费方。
4. **避免双真源漂移**：模型注册的权威事实源在 metrics 注册表（seed）；开关翻转动作写进模型注册运维 SOP（登记 seed + 翻配置同一变更单），字典表会形成第二份可漂移的状态。
5. **与先例一致**：「Job 未注册则 501」同为部署事实驱动的服务端短路；Nacos 热更新即时生效，无需 DDL。

否决字典表方案：引入 DB 写面/运营面、环境同步复杂、无前端消费场景，且与注册表双真源。

**翻转后行为**：`registered=true` → 端点走读表分支（表可能仍零行 → 诚实空态，非 501）；模型注册方（Python）开始写入 `ts_plan_direction_warning`。

---

## 4. 枚举字典（前端只读消费）

> 以下 7 组从 API-TS-M9 §2 **逐字复制**，**逐字冻结，禁改**（含中文字面量与色值）。服务端校验以此为准，出枚举一律 400。§2.7 `research_grade`（四档）不属 OV（09c），不在本分册。

| 组 | 枚举值（逐字冻结，禁改） | 契约源 | 消费端点 |
|---|---|---|---|
| 预警来源 `warning_source`（六源） | `paper`论文 · `patent`专利 · `project`项目 · `talent`人才 · `industry`产业 · `policy`政策 | §2.3 | §2.7 |
| 预警等级 `warning_level`（三级，含标签/色值） | `high`高预警 `#f53f3f` · `medium`关注 `#ff7d00` · `watch`观察 `#165dff` | §2.4 | §2.7 |
| 热度趋势 `hot_trend`（三类） | `hot`热点 · `rising`上升 · `stable`平稳 | §2.5 | §2.1 |
| 人才流动类型 `flow_type`（三类，中文字面量） | `学术→产业` · `产业→学术` · `预警流动`（`全部` 为筛选器特例，不作存储值） | §2.6 | §2.5 |
| 概览时间窗 `overview_time_range`（三类） | `3m`近3个月 · `6m`近6个月 · `12m`近12个月 | §2.8 | FE 跟踪块三窗（来源缺口见 §6/§7-7） |
| 能力项 `capability_key`（四类） | `comprehensive-plan`综合发展规划 · `key-area-plan`重点领域规划 · `research-analysis`研究领域分析 · `report-export`报告与导出 | §2.1 | 页面能力卡（FE 静态消费） |
| 证据图层 `result_type`（五类，各带色值，后端下发） | `hotspot`热点技术 · `space`空间布局 · `talent`人才流动 · `report`报告资源 · `warning`方向预警 | §2.2 | §2.3 `spatial.points` |

**本分册新增（建议批 4 并入契约 §2，待会签）**：推送资源类型 `resource_type` 四类——`report`报告 · `project`项目 · `policy`政策 · `carrier`载体（与 ARCH §4.6 四资源池一致；消费端点 §2.6/§5）。**F5 继承差口注记**：需规 183 原文为「行业资讯」，契约/ARCH 四池为「载体」——差口如实注记（§7-11），是否补行业资讯类待 M0/产品拍板，本分册不擅自加值。

---

## 5. 订阅面（resource-push / subscriptions）

### 5.1 与既有订阅体系对齐（真实现，不走 D18）

对齐 `SITUATION-ENT-SUBSCRIPTION-PUSH-L01`（SITUATION-ENT-SUBSCRIPTION-PUSH-L01 已交付，2026-11-05 push origin/dev）既有体系，**零重复造**：

| 既有组件 | 复用方式 |
|---|---|
| `sys_user_subscription_rule`（app_user 家族，既有表） | 新增 `scope_type='planning_resource'` 枚举值——**实际分派列是 `scope_type`，ARCH 的「rule_type」为术语笔误**（DATA §0.3 实测：`scope_type varchar(32)` 自由枚举，无 `rule_type` 列，**零 DDL**）；结构化订阅的存储映射（DATA §5 裁定）：`resource_types`+`fields` → `scope_value` JSON（或 `keywords`），`frequency` → `push_frequency`，DTO 结构化形状不变、不加列 |
| `SubscriptionPushJob`（XXL-Job `@XxlJob("subscriptionPushJob")`） | 直接复用调度，不新增调度面 |
| `SubscriptionAdapter` / `SubscriptionAdapterRegistry` / `AbstractSubscriptionAdapter` | 新增 `PlanningResourceSubscriptionAdapter` 挂入 Registry（`scopeType()='planning_resource'`）：命中报告/项目/政策/载体四类资源池（池=既有 ADS 只读源，表名 OV-DATA 对齐）。**F7 多资源命中语义**：同一规则一次 Job 运行命中多条资源 = **聚合一通知**（`SubscriptionNotifyService` 双写一次：站内 `sys_user_notification` + 门户 `MessageCenterClient.pushNotice`）+ **多产物行**（每命中资源一行 `sys_user_planning_push_record`，§2.6 清单按行过滤/分页）。产物落新表系 A3 裁定：`sys_user_notification` 实测无 `resource_type`/`field` 列，过滤+分页不可维护 |
| 幂等闸门 `last_push_time` | 沿用（`push_frequency` 三档闸门 + 回写幂等） |
| 订阅推送链路 | **不经 Python / 久新**（ARCH §4.6）；订阅设置读写按登录用户隔离 |

### 5.2 GET subscriptions

`GET /display/v1/situation/planning/resource-push/subscriptions` → `200`：

```json
{ "code": 0, "data": { "resource_types": ["report", "policy"], "fields": ["合成生物"], "frequency": "weekly" } }
```

未设置过 → `data` 返回默认值 `{ "resource_types": ["report","project","policy","carrier"], "fields": [], "frequency": "daily" }`（默认值**由表行/配置携带**，批 4 定稿；不默认空导致 FE 无兜底）。

### 5.3 PUT subscriptions

请求体（`200` 返回更新后同形对象；全量小对象提交，最后写胜，沿 M10 分册同口径）：

```json
{ "resource_types": ["report", "policy"], "fields": ["合成生物"], "frequency": "weekly" }
```

| 校验 | 失败码 |
|---|---|
| `resource_types` 每项 ∈ §4 四类枚举；`[]` = 清空订阅（允许） | `400` |
| `frequency` ∈ `realtime` / `daily` / `weekly`（**U7 待 M0**；契约原样） | `400` |
| `fields` 领域词建议复用 `/topic/v1/meta/industry-clusters` 字典（M1 §0 复用清单，禁另造）；是否强校验待批 4 | 待定 |
| 未登录 | `401` |

### 5.4 frequency 落地映射（U7 未决，如实标注）

既有引擎闸门为 `hourly` / `daily` / `weekly`（L01 三档；历史 `instant` 映射 `hourly`）。契约枚举 `realtime` / `daily` / `weekly` 中 **`realtime` 无现成通道**：若 U7 冻结保留 `realtime`，建议映射引擎 `hourly` 闸门（沿用 `instant→hourly` 先例，语义=小时级近实时）；真「实时」推送需新通道，不在本期。**此映射待 M0 拍板，本分册不擅自闭合。**

---

## 6. FE 接线差异清单（页面零改动，只改 api 拼装层）

**现状**（`repos/lumen-ui-science-pc/src/api/situation/techDevelopmentPlan.ts`）：real 分支单端点 `fetch('/situation/v1/planning/dataset')`，`response.json()` **未解 R 信封、无 /display 网关前缀**，整页一次取全 `TechDevelopmentPlanDataset`（30+ 字段）。文件头注释已预留拆端点演进。

**改造点**（接线单输入；仅此一个文件族）：

| # | 改造点 | 说明 |
|---|---|---|
| 1 | `fetchTechDevelopmentPlanDataset` real 分支重写 | 单 fetch → `Promise.all` 并发 8 个 GET（§1 端点 1–8）+ §2.7 单独 try/catch（501 → 预警块填空态，不拖垮整页；其余端点失败整页错误态，保持现行为） |
| 2 | R 信封解包 | 每响应取 `resp.data`（现状未解包，必改） |
| 3 | 网关前缀 | 路径统一 `/display/v1/situation/planning/*`；dev proxy 核对 `/display` → 网关转发 |
| 4 | `defineApi` id 不变 | `tsTechDevelopmentPlanDataset` 保持，页面引用稳定；新增导出 `updatePlanningSubscriptions`（PUT，设置面板调用，同文件） |

**dataset 09a 块 → 端点映射与名称映射**（类型零改动，映射在 api 层做）：

| dataset 块 | 来源端点 | 名称/形状映射 | 缺口处置 |
|---|---|---|---|
| `directionMonitorItems` | §2.7 | `id←warning_id`、`level←warning_level`、`updatedAt←updated_at`，余同名；501 → 空数组 | — |
| `directionMonitorSources` / `directionWarningMeta` | §2.7 响应（`source_averages[].source/label`、`level_label`） | 501 态下字典无来源 → **短期沿用 mock 种子冻结字典**（demo 逐字，风险低）；批 4 建议增字典字段（§7-4） | 会签点 |
| `hotTechData` | §2.1 | `id←tech_id`、`trend←hot_trend`，余同名 | — |
| `multidimensionalIndicatorCategories` | §2.2 | `key←category_key`、`label←category_label`、`metrics[].label←metric_label`、`value←metric_value`、`change←metric_change`、`linked←linked`（改由端点下发，删 FE 静态） | — |
| 本地优势 3 块（`localAdvantageChart/Innovation/Output`） | §2.4 | 需子项序列（`yAxis[]` 多行），现契约为维度级标量 → 批 4 建议 `dimensions[].items[]`（§7-5）；**未冻结前该 3 块保持 mock 种子** | 会签点 |
| `talentFlowData` | §2.5 records | `flowType` 英文码↔中文枚举映射（`academia-to-industry↔学术→产业` 等；**F6 注记**：种子中文五类标签→契约四类枚举〔三存储值+「全部」筛选特例〕映射在本层落实，不新增枚举值）；`warning←warning`；**`name`/`avatar` 无聚合来源（U6 禁个人明细）→ 置空降级，个人卡改以 `from→to` 机构对为主标题** | **会签点（需 FE 孔东确认降级形态）** |
| `talentInstitutionFlowRows` | §2.5 institution_flows | `netInflow←net_inflow`、`trend←direction`（in→up/down→down） | — |
| `talentDirectionNodes` | §2.5 `od_nodes` 直读 | `name` 同名、`itemStyle.color←color`；OD 总量写死 18932/12458 与增幅由 `od_total`/`trend_pct` 替代（F2，G-B4 在 DTO 层闭合） | — |
| `planningResourcePackages` | §2.6 records | `id←resource_id`、`type←resource_type`、`updatedAt←pushed_at`；`reason`/`match`/`evidenceSource` 无契约来源 → 批 4 建议 `records[].reason`（§7-6）；未冻结前隐藏该列或保持种子 | 会签点 |
| `defaultPushSettings` | §5.2 GET | `fields←fields`、`frequency←frequency`；`email`/`sms` 无后端通道（双写=站内+门户）→ 保持 FE 静态禁用态 | — |
| 跟踪块（`technologyTrendSeriesByRange` / `technologyHeatTrendDefinition` / `technologyTrendColors` / `technologyTrendSpaceRegions`） | §2.3 仅覆盖 timeline+spatial | 序列块与热度口径定义块**无端点来源**（§2.1 `heat_series` 是按技术年度序列，非按时间窗全局序列）→ 保持 FE 冻结种子；批 4 处置建议（§7-7） | 会签点 |
| 09b/09c 块（`carrierTypes`/`industryClusters`/`companies`/`overlap*`/`research*` 等） | **不在本分册** | KEY/RES 分册端点冻结前 real 分支局部保留 mock 种子（显式 TODO 标注），二步接线 | KEY/RES 分册 |

---

## 7. 批 4 冻结变更清单（相对 API-TS-M9 的 delta，供 BE-TS-CONTRACT-02 并入）

| # | 变更 | 性质 |
|---|---|---|
| 1 | **新增第 9 端点** `GET /v1/situation/planning/metric-system`（G-B2 方案 A），DTO 定稿见本分册 §2.2；建议契约编号 **§3.2a**（避免重排 §3.3–§3.8 引用失效） | 定稿（ARCH 已裁） |
| 2 | **G-B1 网关路径定稿**：网关 `/display/v1/situation/planning/**`、服务内 `/v1/situation/planning/**`；FE 旧 real 路径 `/situation/v1/planning/dataset` **废弃**；后端**不提供**聚合 dataset 端点 | 定稿（ARCH 已裁） |
| 3 | **表清单调整**（契约 §4，已对齐 DATA DDL §2）：#1 `ts_plan_record` **取消**（OV 范围内无消费方）；新增 `ts_plan_metric_system`、`ts_plan_tracking_event`/`ts_plan_tracking_point`（179/180/181 各专用表，ARCH §5）；`ts_plan_hot_tech_series` 独立成表（技术×区间×期，128 行）；`ts_plan_talent_flow` 行型=institution_flow/record 两段（**stats 无专行、Java 现算**，DATA §2.7）+ **`od_nodes` JSON 列（F2，DATA 侧同步加列）**；订阅产物新表 **`sys_user_planning_push_record`**（A3，DDL DATA 侧补）；`ts_plan_direction_warning` 建表 **V1 零行**。OV 范围 `ts_plan_*` 表共 8 张；契约 §4 #5/#6（key_area/research）不属 OV，KEY/RES 分册另定；**全组列名以 DATA DDL 为准**（`caliber_def` / `period_label` / `heat_value` / `metric_change` 等，F3/F4） | 定稿（ARCH 已裁 + 会签更正） |
| 4 | §3.1 建议增补字典字段（六源 `source_dict`、三级 `level_dict` 含色值），解 501 空态下 FE 字典无来源；未同意则 FE 沿用冻结种子字典 | **建议，待会签** |
| 5 | §3.4 建议增补 `dimensions[].items[]{name,local,global_avg}` 子项序列（表按维度×子项行存储），解 FE 三块图表 `yAxis[]` 多行需求 | **建议，待会签** |
| 6 | §3.6 建议增补：records `reason`（推荐理由，**表行携带**）字段 + `resource_type` 四类枚举并入 §2 + 清单 Query（§2.6 定稿补充） | **建议，待会签** |
| 7 | §3.3 跟踪块趋势序列（`overview_time_range` 三窗）与热度口径定义块来源缺口处置：(a) §3.3 增 `trend_series` 字段，或 (b) FE 保持 demo 冻结种子；本分册倾向 (b)（量级小、非统计核），待会签 | **建议，待会签** |
| 8 | 契约样例 `Q0xx` 占位替换为赋号草稿 `M_INNOV_PLAN_HEAT` / `M_INNOV_PLAN_GROWTH` / `M_INNOV_PLAN_LOCAL_ADV` / `M_INNOV_PLAN_TALENT_FLOW` / `M_INNOV_PLAN_DIRECTION_ALERT`（均**未签**，签后回填；§1.2 差集判定不动） | 定稿（对齐核对记录） |
| 9 | **S-1**：§3.2 增 Query `range`（`3m`/`6m`/`12m`，默认 `12m`，对应序列表 `range_key` 分区）；`heat_series.year` 语义冻结为「期标签」（季度逐字），契约示例同步改季度标签 | api 会签裁定（S-1） |
| 10 | **F3 形状更正**：§3.2 `spatial_distribution` 由契约示例 `{region,heat,lng,lat}` 更正为种子实际 `{name,factor}`（无坐标、不预计算派生值，DATA §0.2）；坐标类点位语义由 `ts_plan_tracking_point` 承载（跨端点）或实现单落定 | 定稿（会签更正） |
| 11 | **F5/F6 注记**（不改值）：① 需规 183 原文「行业资讯」vs 契约四池「载体」继承差口，是否补类待 M0/产品；② talent `flow_type` 种子中文五类标签→契约四类枚举（三存储值+「全部」筛选特例）映射由 api 拼装层落实 | 注记（F5/F6） |

---

## 8. 合规自检

| # | 检查项 | 结论 |
|---|---|---|
| 1 | 调用链 | 前端 → 网关（`/display/**`）→ `gkxlumen-display` Java REST → **只读 ADS**（8 张 `ts_plan_*` + 资源池）；Java 不写算法、不直连 nGQL；灌数走 Python 一次性脚本（data-agent 执行单）；无 `demo-*` 依赖（D12）；不涉对象存储（D14 N/A） |
| 2 | 读写面 | 唯一写面 = PUT subscriptions（app_user 家族，复用既有订阅体系）；其余 8 端点全只读 |
| 3 | U6 个人信息 | talent-flow DTO 无姓名/证件/个人 ID 字段，`person_count` 仅机构级聚合计数；表结构级无个人明细列；FE 个人卡字段降级为会签点（§6） |
| 4 | 501 语义 | 仅 direction-warnings；501=模型未注册通道态，**非覆盖证明**，差集 missing 保持；禁以假预警行/假规划正文填充；导出同闸 |
| 5 | D18 无接口直返 mock | 全部端点读表；`caliber_note`（列 `caliber_def`）/`source`/`od_nodes` OD 总量/默认订阅值等文案与写死替代字段全部表行携带、来源列已写明，禁 Java 硬编码；空态诚实（空数组+empty_reason）；唯一例外 `spatial.map_center/zoom` 展示配置常量（已标注待会签认可）；`ts_plan_direction_warning` V1 零行 |
| 6 | metric_id | 全部引用 ARCH §0 赋号草稿并标「未签」；不发明新 `M_*`；179/183 无 metric_id（N/A/n_a_ops 依据 ARCH §0）；UI 不显伪 8 件套 |
| 7 | 网关路径 | 符合 api 规约铁律 9（网关=网关地址/display/@RequestMapping/方法映射），无前缀插序错误形态 |
| 8 | 枚举 | 7 组逐字冻结（§4）；新增 `resource_type` 明确标为批 4 建议待会签，不冒充已冻结 |
| 9 | 交付边界 | 未改 task-registry、未 git 提交、未写业务代码；仅落本分册一个文件 |

## 9. 会签待决点（需四方会签讨论）

1. **FE 人才个人卡降级形态**：`TalentFlow.name/avatar` 在聚合口径下无来源，建议改以机构对为主标题（需 FE `human:孔东` 确认，页面零改动约束下的渲染形态）。
2. **批 4 建议与注记逐项拍板**：§7-4（§3.1 字典增补）/ §7-5（§3.4 `items[]`，与 DATA §2.6 行型一致）/ §7-6（§3.6 `reason`+枚举+Query）/ §7-7（§3.3 序列块处置 (a)/(b)，本分册倾向 (b)）/ §7-9（S-1 `range`）/ §7-11（F5 差口是否补类）。
3. **DATA 侧联动项（待 data 会签）**：`ts_plan_talent_flow.od_nodes` JSON 列加列（F2，含六节点/色值/OD 总量，与既有 stats 行型的收口）、`sys_user_planning_push_record` DDL（A3）、`net_inflow` 现算口径（DATA §2.7）。
4. **S-3（DATA 提出，api/architect 拍板）**：`reference_stats` 灌契约示例值（72/1240/215.4，`contract_draft_sample` 标注）vs V1 留空走诚实空态——本分册倾向维持示例值+标注（DATA 已按此灌 1 行）。
5. **`realtime` 频率映射**（U7）：映射 hourly 闸门的建议是否成立，M0 产品侧拍板。
6. **501 开关载体**：配置项方案（§3.3）确认；及网关 501 透传核验（实现单项）。
7. **`spatial.map_center/zoom` 展示配置常量**是否认可豁免表行携带（D18 边界裁定）。

---

## 会签修订记录 v2（2026-11-06）

architect / api / algorithm 三家会签**同意**，必改项已逐条修订（本文件 v1→v2，仍仅改本文件、不碰其他）：

| # | 会签项 | 修订内容（落点） |
|---|---|---|
| 1 | talent stats 矛盾（三家均指出） | §2.5 改为 **Java 由表行现场聚合计算**（DATA §2.7 实测裁定：无预聚合种子行，`warning_count` 实测=2；方向计数按 `flow_type` 聚合）；示例四数标注契约草案演示值 |
| 2 | od_nodes（api 会签 F2） | §2.5 响应增 `od_nodes[]{name,color,od_total,trend_pct}`，行源=`ts_plan_talent_flow.od_nodes` JSON 列（DATA 侧同步加列）；§6 `talentDirectionNodes` 改直读——G-B4 写死 18932/12458 在 DTO 层闭合 |
| 3 | §2.1 列引用更正（F3） | `caliber_note` 来源列→`caliber_def`；序列列 `year`/`heat`→`period_label`（期标签·季度逐字）/`heat_value`；`spatial_distribution` 更正为 `{name,factor}` 无坐标（坐标归 `ts_plan_tracking_point` 或实现单）；形状变更入 §7-10 |
| 4 | §2.2 列名统一（F4） | `note`→`metric_change`，全组以 DATA DDL §2.3 为准（`metric_value`/`metric_unit`/`category_order`，`linked` 随 `linked_json` 列下发） |
| 5 | M1 回填规则落册 | §0 总则 metric_id 行：五草稿号逐字映射（§3.2 双号 / §3.4 / §3.5 / §3.1 / §3.3 恒 `[]`），禁取 `Q010–Q019`/`QPOL-*`；时点=批 4 冻结由 BE-TS-CONTRACT-02 落契约正文；行源=各表 `metric_id` 列 |
| 6 | S-1 裁定 | §2.1 增 Query `range`（3m/6m/12m 默认 12m，对应 `range_key` 分区）；`year` 语义冻结为「期标签」；入 §7-9 |
| 7 | A3 裁定（协调会签拍板） | 推送产物落 **`sys_user_planning_push_record`** 新表（`sys_user_notification` 实测无 `resource_type`/`field` 列，过滤+分页不可维护）；§1 端点总表 / §2.6 / §5 更新；DDL 由 DATA 侧补 |
| 8 | F5/F6/F7 批 4 注记 | F5「行业资讯 vs 载体」继承差口（§4/§7-11）；F6 talent 种子中文五类→四类枚举映射（§6/§7-11）；F7 多资源命中=聚合一通知+多产物行（§5.1） |
| 9 | 随动一致性修正 | §5.1 `rule_type`→`scope_type`（DATA §0.3 笔误澄清，零 DDL）及订阅存储映射（DATA §5）；§2.3/§2.4 来源列名对齐 DATA DDL（`event_date`/`event_text`/`years_json`/`local_score`/`global_score`/`reference_json`）；§2.4 差异对齐 DATA §2.6 三键×6 对比项（S-2）；§9 待决点重排（A3 已裁定移出，新增 DATA 联动项与 S-3） |
