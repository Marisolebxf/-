# TS-L2-DS09-KEY-API · 重点领域规划 · 后台接口设计

> **任务**：`TS-L2-DS09-KEY-API`（definition，不写业务代码）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 api-agent（沿 KEY 组授权链）
> **状态**：**v2**——architect / api / algorithm 三家会签已审**同意**，必改项（caliber_note 行源 / 文案归属收口 / 排序保证 / delta 补漏 / 图层勘误 / empty_reason 落位）已修订，见文末「会签修订记录 v2」；待 data 会签（与 KEY-DATA DDL 联动项，§9）
> **硬依赖**：`sdd/l2/TS-L2-DS09-KEY-ARCH.md` 已落盘（本文与其冲突时，改本文不改 ARCH 稿）
> **文风基准**：与同菜单兄弟分册 `sdd/l2/TS-L2-DS09-OV-API.md` 保持一致（章节、信封、错误码、总则口径逐条沿袭）

**输入真源**

| 用途 | 真源 |
|---|---|
| 架构硬依赖 | `sdd/l2/TS-L2-DS09-KEY-ARCH.md`（§0 逐叶判定、§4 逐叶架构、§5 差异收口、§6 D18 三要素、§7 U8 建议） |
| 契约草案（批 4 未冻结） | `agent-handoffs/科技发展态势-TS/API-TS-M9.md` §3.7 `key-areas` + §1 模块约定 + §2 枚举字典 + §4 表 #5 + §5 U8 |
| 全局约定 | `API-TS-M1.md` §1 信封/错误码/公共入参、§4 D9 血缘、§5 空态四态（经 OV-API §0 转引，口径一致） |
| 指标赋号与差集 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-09-科技发展规划-核对记录.md` §3.3 KEY-DOMAIN（四条 `TEMP_DS09_KEYD_*`→`M_INNOV_KEYD_*`、④ 不适用三叶）+ §赋号表 + §4 KEYD-B01..B03 |
| FE 现状 | `repos/lumen-ui-science-pc/src/mock/modules/techDevelopmentPlan.ts` L347–L505（demo 冻结种子 9 数组，行数实测）+ `src/types/techDevelopmentPlan.ts`（dataset Tab2 9 字段）+ `KeyAreaTab.vue`（页面冻结，孔东锁至 2026-11-12） |
| DATA 分册 | `sdd/l2/TS-L2-DS09-KEY-DATA.md`（v1 成稿时未落盘、v2 已并行落盘：`rendered_note` / `dim_order` / 各表 `sort_no` 等列名已随会签对齐其 DDL；仍以 DATA DDL 为终准） |

**范围**：DS-09 重点领域规划页签（FE-TS-09b，需规序 **185–190** 共 6 叶：185–188 + 190 五读面叶 + 189 一交互壳叶）的后台接口定稿——本二级**仅 1 个读端点**（契约 §3.7 `key-areas`，响应按种子扩为平铺 9 块）、DTO、U8 两裁定落册、契约改约 delta、FE 接线差异。**不含** 09a 综合（OV 分册已 v2）/ 09c 研究分析（RES 分册另册）。

---

## 0. 总则

| 项 | 定稿 |
|---|---|
| 落仓 | `lumen-svc-platform/gkxlumen-display`，**复用 OV 组既有 `PlanningController`**（`@RequestMapping("/v1/situation/planning")`）与 `PlanningQueryService`，仅新增 `keyAreas()` 只读方法——**U1 裁定**（OV-ARCH §7 建议、KEY-ARCH §7.4 落定）：三页签统一 `planning` 前缀单 Controller，不按 09a/09b/09c 拆服务路由；**本页零新 Controller、零新路由** |
| 网关路径 | 按 api 规约铁律 9 拼接：`gateway地址 / display / v1/situation/planning / key-areas`，即网关对外 `/display/v1/situation/planning/key-areas`；服务内（Feign/直连）路径不带 `/display` |
| 响应信封 | 统一 `R<T>`：`{ "code": 0, "msg": "ok", "data": {…} }`（`gkxlumen-common-core` `R.java`，M1 §1.2）。`code≠0` 时 `data=null`，前端走空态不伪造（与 OV-API §0 逐字同口径） |
| 错误码 | 本端点**无 Query、无路径参数** → 不设 `400`（无枚举/必填校验面）；`401/403`（网关登录态，读端点免登但网关侧保留）/ `500`（服务异常）；**无 `501`**（本页零 501，catalog 501 通道只给 COMPREHENSIVE seq 184，ARCH §1）；无路径 id 类参数，不用 `404/409` |
| 空态 | 任一块无行 = `200` + 该块空数组 + `data.empty_reasons` 按块携带原因（M1 §5 枚举，多块落位见 §2.0）；按块独立判定，禁以 0 冒充缺失、禁补演示行。V1 灌数后为满态（9 表 61 行），空块仅出现在灌数失败/正式态清库时 |
| 读写面 | **1 读 0 写**——6 叶全部无写面（190「方案模拟」为 FE Modal 交互，非端点非 501） |
| metric_id | 本文所有 `metric_id` / `metric_ids` 值均为核对记录 §赋号表的**赋号草稿·未签·pending `human:唐绍祖`**（`M_INNOV_KEYD_*` 四条，公式未签）；仅替换契约 §3.7 样例中的 `Q0xx` 占位；**不发明任何新 `M_*`**。回填规则见 §6 |
| 文案铁律 | `caliber_note` / plans 三个 action 文案列等诚实标注与演示文案一律由 **D18 表行携带**（来源列在 §2 各字段表写明），**禁止 Java 硬编码文案**；服务端错误 `msg` 属错误信息非数据口径文案，允许代码常量（同 OV §0） |
| Mock 徽标 | 全部 D18 表读数的 D4 仍 mock → FE 🧪 MockBadge 保留至 D4 翻转（ARCH G-B5）；统计数旁 ⓘ draft 语义卡回指核对记录 §赋号表，禁点 `M_SYNTH_*` / `M_ENT_*` / `M_CHAIN_*` 伪 8 件套 |
| 列名口径 | v1 先于 KEY-DATA 分册完成 → §2 来源列按 **ARCH 稿表设计**写（ARCH 未定名处本文给建议列名并标注）；**一切列名以 DATA 分册 DDL 终准**（v2：DATA 已落盘，`rendered_note` / `dim_order` / 各表 `sort_no` 已随会签对齐，余者冲突仍改本文） |

---

## 1. 端点总表（本二级仅 1）

| # | 方法 | 服务内路径 | 网关路径（`/display` 前缀） | 需规叶（seq，六叶共用一端点） | D18 表（9 张，`gkxlumenx_ads`） | 读/写 |
|---|---|---|---|---|---|---|
| 1 | GET | `/v1/situation/planning/key-areas` | `/display/v1/situation/planning/key-areas` | 185 空间布局 · 186 竞争力评估 · 187 土地效益 · 188 载体分布 · 189 筛选联动（壳） · 190 优化建议 | `ts_plan_key_area`(3) / `_carrier`(22) / `_carrier_type`(6) / `_district_baseline`(6) / `_competitiveness`(5) / `_dimension`(5) / `_benchmark`(5) / `_land`(6) / `_plan`(3) | 读 |

- **Query：无**。189 筛选联动为交互壳（公共筛选承载，§5），V1 全量 61 行一次下发、FE 本地过滤，无分页/无服务端过滤参数（ARCH §4.5）。
- **U1 裁定写明**：不新建 `KeyAreaController`、不拆 `key-areas` 子路由——复用 OV 组 `PlanningController` 单 Controller 只加一个 GET 方法；与 OV §1 端点 1–9 同前缀共存，网关路由零新增配置项（仅既有 `/display/v1/situation/planning/**` 通配内新增方法映射）。
- 表/DDL 定稿归 KEY-DATA 分册（库名 `gkxlumenx_ads`、`ts_plan_key_area` 前缀族、不进 ODS/DWD、不带 `gapfill_`——D18 铁律，ARCH §6）。

---

## 2. 响应 DTO 定稿（按 ARCH §5 改约：平铺 9 块）

### 2.0 骨架与块-表-叶总览

响应 `data` 平铺 **9 块 + 3 顶层元字段**；cluster 内**不再嵌套** competitiveness / carriers / plans（契约示例嵌套结构弃用，§4 delta-1）。

| 块（逐字对齐 ARCH §5） | 表 | 行数（实测） | 消费叶 |
|---|---|---|---|
| `clusters` | `ts_plan_key_area` | 3 | 185 / 189 |
| `carriers` | `ts_plan_key_area_carrier` | 22（7 行 `cluster_id` NULL） | 185 / 188 / 189 |
| `carrier_types` | `ts_plan_key_area_carrier_type` | 6（含 `all` 图例行） | 188 / 189 |
| `district_baselines` | `ts_plan_key_area_district_baseline` | 6 | 188 |
| `competitiveness_metrics` | `ts_plan_key_area_competitiveness` | 5 | 186 |
| `dimension_scores` | `ts_plan_key_area_dimension` | 5 | 186 |
| `benchmark_rows` | `ts_plan_key_area_benchmark` | 5 | 186 |
| `land_use` | `ts_plan_key_area_land` | 6 | 187 |
| `plans` | `ts_plan_key_area_plan` | 3 | 190 |
| 顶层 `carrier_total` / `caliber_note` / `metric_ids` | —（汇总/表行携带） | — | 全叶 |

```json
{
  "code": 0,
  "data": {
    "clusters": [
      { "cluster_id": "ai", "cluster_name": "人工智能集群", "industry_category": "新一代信息技术",
        "technology_field": "人工智能", "default_map_layer": "产业热度",
        "carrier_ids": ["L003", "C002", "P001", "P002", "I001", "A001"],
        "metric_id": "M_INNOV_KEYD_SPATIAL" }
    ],
    "carriers": [
      { "carrier_id": "L001", "name": "鹏城实验室", "carrier_type": "lab", "district": "南山区",
        "lng": 113.932, "lat": 22.535, "level": "国家级",
        "cluster_id": null, "land_benefit": null }
    ],
    "carrier_types": [
      { "type_key": "all", "type_name": "全部载体", "carrier_count": 2856, "color": "#2563eb", "sort_no": 1 }
    ],
    "district_baselines": [
      { "district": "南山区", "total_carriers": 276, "leading_type": "重点实验室" }
    ],
    "competitiveness_metrics": [
      { "metric_key": "composite", "label": "综合指数", "value": 78.5, "change_pct": "12.3%",
        "metric_id": "M_INNOV_KEYD_COMPETITIVENESS" },
      { "metric_key": "potential", "label": "发展潜力", "value": 82, "change_pct": "10.1%",
        "metric_id": "M_INNOV_KEYD_POTENTIAL" }
    ],
    "dimension_scores": [
      { "dim_key": "innovation_resources", "dim_label": "创新资源", "score": 92,
        "metric_id": "M_INNOV_KEYD_COMPETITIVENESS" }
    ],
    "benchmark_rows": [
      { "region": "南山区", "score": 78.5, "rank_no": 1, "metric_id": "M_INNOV_KEYD_COMPETITIVENESS" }
    ],
    "land_use": [
      { "district": "南山区", "land_type": "研发用地", "area_sqm": 125000, "efficiency": 92,
        "status": "good", "metric_id": "M_INNOV_KEYD_LAND" }
    ],
    "plans": [
      { "plan_id": "a", "plan_name": "方案A", "title": "提升创新策源能力", "priority": "高",
        "expected_effect": "+18.6%", "resource_gap": "-23.2%",
        "actions": ["增强基础研究投入", "引育高端科研人才", "建设重大科研平台"],
        "primary_action": "查看建议", "secondary_action": "方案对比", "detail_action": "资源详情",
        "metric_id": null }
    ],
    "carrier_total": 22,
    "caliber_note": "…（186 竞争力口径说明，表行携带，见 2.10）",
    "metric_ids": ["M_INNOV_KEYD_SPATIAL", "M_INNOV_KEYD_COMPETITIVENESS", "M_INNOV_KEYD_POTENTIAL", "M_INNOV_KEYD_LAND"]
  }
}
```

> 示例值全部取自 demo 冻结种子（`techDevelopmentPlan.ts` L347–L505）逐字；各块仅示 1–2 行，全量以种子行数为准。四条 `M_INNOV_KEYD_*` 均**赋号草稿·未签**。

**排序保证**（v2 补）：`clusters` / `carriers` / `competitiveness_metrics` / `dimension_scores` / `land_use` / `plans` 各块 Service 按表 `sort_no`（`dimension` 表为 `dim_order`）**ASC** 稳定排序后返回，**FE 数组展示序即以此为据**（v1 仅 `carrier_types` 有 `sort_no`，DATA DDL 现已逐表设列——carrier 为 lab→center→park→incubator→accelerator 分组序）；`district_baselines` 同按表 `sort_no` ASC（DATA DDL 已设列，按总量降序种子序）；`benchmark_rows` 按自有语义列 `rank_no` ASC。仅 `carrier_types` 将 `sort_no` 作为 DTO 字段下发（§2.3），其余各表的排序列为**服务端排序保证、不进 DTO**。

**`empty_reason` 落位**（v2 补，对齐 OV 组诚实空态先例的多块扩展）：九块全满时 `data` **不含**空态字段；任一块为空时 `data` 增 **`empty_reasons`** 对象——键=块名（如 `"plans"`）、值=M1 §5 枚举（本端点无 Query，故恒 `no_source`，无 `filter_empty` 面）、**仅含空块**（满块不入表、不伪造原因）。FE 拼装层按块消费：空块走该块空态，不拖垮其余块；禁以 0 行/演示行冒充。

### 2.1 `clusters[]`（185 集群行 / 189 集群导航）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `cluster_id` | string | 集群键，**沿用 demo 键** `ai` / `bio` / `energy`（契约示例 `CL-FUT-05` 弃用，§4 delta-7） | `ts_plan_key_area.cluster_id` |
| `cluster_name` | string | 集群名（人工智能集群 / 生物医药集群 / 新能源集群） | 同表 `cluster_name` |
| `industry_category` | string | 产业大门类（新一代信息技术 / 生命健康 / 先进制造）——189 公共筛选联动源 | 同表 `industry_category` |
| `technology_field` | string | 科技领域细分（领军主题承载列之一，ARCH §4.5） | 同表 `technology_field` |
| `default_map_layer` | string | 默认图层，中文字面量（产业热度 / 科技载体 / 土地效益——demo `MapLayerKey` **四值类型中种子使用的三值**逐字；图层全集 4 值见 §5.1 勘误） | 同表 `default_map_layer` |
| `carrier_ids` | string[] | 挂集群载体引用（JSON 列；3 集群合计 15，指向 `carriers[].carrier_id`） | 同表 `carrier_ids`（JSON） |
| `metric_id` | string | `M_INNOV_KEYD_SPATIAL`（STAT 草稿·未签；读数为集聚归属演示，非网络密度） | 同表 `metric_id` |

### 2.2 `carriers[]`（185 地图落点 / 188 详情 / 189 联动）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `carrier_id` | string | 载体键，**沿用 demo 键** `L001`–`A003`（契约示例 `C-01` 弃用） | `ts_plan_key_area_carrier.carrier_id`（ARCH §4.1 简记 `id`；建议 DDL 与 DTO 同名，DATA 终准） |
| `name` | string | 载体名 | 同表 `name` |
| `carrier_type` | enum | 五类逐字：`lab` / `center` / `park` / `incubator` / `accelerator`（demo `CarrierLocationType`；`all` 是图例行不落载体行） | 同表 `carrier_type` |
| `district` | string | 所属区（南山区 等 6 区） | 同表 `district` |
| `lng` / `lat` | number | 经纬度（TiandituMap 落点；GIS 渲染 FE 既有承载，后端只供点位） | 同表 `lng` / `lat` |
| `level` | string | 能级字面量（国家级 / 省级 / 市级 / 区级，demo 逐字；展示值非校验枚举）——189 领军主题承载列之二 | 同表 `level` |
| `cluster_id` | string? | 所属集群，**可空**：实测 22 载体仅 15 行挂集群，`L001`/`L004`/`P003`/`P005`/`I003`/`I004`/`A002` 共 7 行置 **NULL**（诚实空，不强行归簇，ARCH §3） | 同表 `cluster_id`（NULL 可） |
| `land_benefit` | object? \| null | `{plot_ratio, output_per_mu}`（U8-2，§3.2）；**V1 恒 `null`**（诚实空，禁编造） | 同表 `land_benefit`（JSON 列，V1 全 NULL） |

**不设 `metric_id` 字段**：188 为 other_system（GIS 点位 + ADS 详情，非载体价值排名），无统计核，禁显伪 8 件套（表列置 NULL 仅作 DDL 一致性，DTO 不映射）。

### 2.3 `carrier_types[]`（188 类型图例/计数）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `type_key` | string | 六键逐字：`all` / `lab` / `center` / `park` / `incubator` / `accelerator` | `ts_plan_key_area_carrier_type.type_key` |
| `type_name` | string | 中文名（全部载体 / 重点实验室 / 工程中心 / 科技园区 / 孵化器 / 加速器） | 同表 `type_name` |
| `carrier_count` | int | **全市口径 demo 计数**（2856 / 128 / 256 / 68 / 420 / 186，🧪）——≠ `carrier_total`（§4 delta-4） | 同表 `carrier_count` |
| `color` | string | 图例色值（demo 逐字） | 同表 `color` |
| `sort_no` | int | 排序（`all`=1 首；**九块中唯一作为 DTO 字段下发的排序列**，其余各块的 `sort_no` / `dim_order` 仅作服务端排序保证，§2.0） | 同表 `sort_no` |

**不设 `metric_id` 字段**（同 2.2 口径）。

### 2.4 `district_baselines[]`（188 区县基线）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `district` | string | 区名（南山区 / 福田区 / 龙岗区 / 宝安区 / 龙华区 / 坪山区） | `ts_plan_key_area_district_baseline.district` |
| `total_carriers` | int | 区载体总数（276 / 242 / 208 / 174 / 140 / 106，demo 逐字，🧪） | 同表 `total_carriers` |
| `leading_type` | string | 主导载体类型中文名（重点实验室 / 工程中心 / 科技园区 / 孵化器） | 同表 `leading_type` |

**不设 `metric_id` 字段**（同 2.2 口径）。

### 2.5 `competitiveness_metrics[]`（186 指标卡，五键沿 demo 原键）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `metric_key` | enum | 五键逐字：`composite` / `innovation` / `industry` / `openness` / `potential`（与五维画像并存不合并，ARCH §7.1 配套） | `ts_plan_key_area_competitiveness.metric_key` |
| `label` | string | 指标卡名（综合指数 / 创新能力 / 产业基础 / 开放协同 / 发展潜力） | 同表 `label` |
| `value` | number | 指标值（78.5 / 88 / 85 / 62 / 82，demo 逐字） | 同表 `value` |
| `change_pct` | string | 环比字符串逐字（`12.3%` 等，含 %；数值化待 M0，同 OV delta 口径） | 同表 `change_pct` |
| `metric_id` | string | `potential` 行挂 `M_INNOV_KEYD_POTENTIAL`，其余四行挂 `M_INNOV_KEYD_COMPETITIVENESS`（均 MIXED 草稿·未签） | 同表 `metric_id` |

### 2.6 `dimension_scores[]`（186 五维画像，U8-1 落册 §3.1）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `dim_key` | enum | 五维英文键（U8-1 新定，§3.1）：`innovation_resources` / `research_output` / `industry_competitiveness` / `talent_support` / `open_collaboration` | `ts_plan_key_area_dimension.dim_key`（新列，一次定名免 ALTER） |
| `dim_label` | string | 五维中文名（demo `keyAreaDimensionScores` 权威）：创新资源 / 科研产出 / 产业竞争力 / 人才支撑 / 开放协同 | 同表 `dim_label` |
| `score` | number | 维度得分（92 / 88 / 85 / 78 / 72，demo `percent` 逐字） | 同表 `score` |
| `metric_id` | string | `M_INNOV_KEYD_COMPETITIVENESS`（MIXED 草稿·未签；权重未签 Q-MO-DS09-04 → ⚠️「待甲方确认」） | 同表 `metric_id` |

注：本表另携两列（**非行级 DTO 字段**，DATA DDL §2.6 已落列）：`dim_order`（维序 1..5，块内排序保证，§2.0）与 `rendered_note`（页级口径整句、5 行同值——顶层 `caliber_note` 的物理行源，§2.10）。

### 2.7 `benchmark_rows[]`（186 对标）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `region` | string | 对标区域（南山区 / 深圳湾合作区 / 广州天河区 / 香港科技园 / 珠海横琴新区） | `ts_plan_key_area_benchmark.region` |
| `score` | number | 对标分（78.5 / 74.2 / 71.3 / 69.1 / 66.8） | 同表 `score` |
| `rank_no` | int | 名次 1–5 | 同表 `rank_no` |
| `metric_id` | string | `M_INNOV_KEYD_COMPETITIVENESS`（草稿·未签） | 同表 `metric_id` |

### 2.8 `land_use[]`（187 区级用地）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `district` | string | 区名（南山区×2 / 福田区 / 龙岗区 / 宝安区 / 龙华区） | `ts_plan_key_area_land.district` |
| `land_type` | string | 用地类型（研发用地 / 产业用地） | 同表 `land_type` |
| `area_sqm` | number | 面积 ㎡（125000 / 98000 / …） | 同表 `area_sqm` |
| `efficiency` | number | 利用效率分（92 / 85 / 78 / 65 / 58 / 62） | 同表 `efficiency` |
| `status` | enum | 三档逐字：`good` / `medium` / `poor`（demo 逐字） | 同表 `status` |
| `metric_id` | string | `M_INNOV_KEYD_LAND`（STAT 草稿·未签；亩均/容积率正式值待正式态真源替换） | 同表 `metric_id` |

注：ARCH §4.3 在本表预留 `land_benefit` JSON 列（V1 NULL）——**表预留列，V1 无 DTO 字段**（187 读数由本块区级行承载；预留正式态回填），以 DATA DDL 终准。

### 2.9 `plans[]`（190 三方案，页级建议壳）

| 字段 | 类型 | 说明 | 来源表列（以 DATA DDL 终准） |
|---|---|---|---|
| `plan_id` | string | 方案键 `a` / `b` / `c`（demo 键） | `ts_plan_key_area_plan.plan_id` |
| `plan_name` | string | 方案A / 方案B / 方案C（契约 `name` 更名 `plan_name`，§4 delta-8） | 同表 `plan_name` |
| `title` | string | 方案主题（提升创新策源能力 等，demo 逐字） | 同表 `title` |
| `priority` | string | 优先级字面量（高 / 高 / 中，demo 逐字） | 同表 `priority` |
| `expected_effect` | string | 预期效果逐字（`+18.6%` / `+22.9%` / `+15.2%`）——「效果预测」即此表行值，无模拟端点 | 同表 `expected_effect` |
| `resource_gap` | string | 资源缺口逐字（`-23.2%` / `-19.8%` / `-16.7%`） | 同表 `resource_gap` |
| `actions` | string[] | 三条行动文案（JSON 列，demo 逐字；**demo 种子非生成物**，ARCH §1） | 同表 `actions`（JSON） |
| `primary_action` / `secondary_action` / `detail_action` | string | 三个按钮文案列（查看建议 / 方案对比 / 资源详情，demo 逐字；表行携带禁硬编码） | 同表 `primary_action` / `secondary_action` / `detail_action` |
| `metric_id` | string? | **恒 `null`**——n/a_ops 建议壳，演示读数不挂 ID（ARCH §4.6） | 同表 `metric_id`（NULL） |

### 2.10 顶层元字段

| 字段 | 类型 | 说明 | 来源 |
|---|---|---|---|
| `carrier_total` | int | **语义冻结**：= `carriers` 块行数 = 22（全量落点载体，含未挂集群 7 行）；≠ `carrier_types[].carrier_count`（`all`=2856 全市口径）；≠ 挂集群载体数（15）——§4 delta-4 | Service 由 carriers 行计数现算 |
| `caliber_note` | string | 186 竞争力口径整句——**表行携带，禁 Java 硬编码**；V1 灌入 KEY-DATA §2.6 占位整句（「竞争力五维与权重口径待定（Q-MO-DS09-04 / KEYD-B02·B03；赋号草稿未签，指标为演示读数）」逐字），M0 定稿后由 DATA 侧翻换（文案定稿归 DATA 种子，§9.5） | **`ts_plan_key_area_dimension.rendered_note`**（v2 会签更正：表名+列名双改，原 `competitiveness.caliber_def` 弃；五维行 5 行同值，Java 取任一行；以 DATA DDL 终准） |
| `metric_ids` | string[] | 四条 KEYD 草稿去重汇总（顺序：SPATIAL → COMPETITIVENESS → POTENTIAL → LAND） | Service 按各表 `metric_id` 列去重汇总（无核块零贡献，§6） |
| `empty_reasons` | object? | **条件字段**（v2 补落位）：仅当存在空块时返回，键=块名、值=M1 §5 枚举（本端点恒 `no_source`）、仅含空块；九块全满时省略——落位语义见 §2.0 | Service 按块行数现算 |

**错误码**：`401/403/500`；空态按块独立 `200` + 空数组 + `empty_reasons` 落位（§2.0；M1 §5 枚举，本端点恒 `no_source`）。

---

## 3. U8 两裁定落册（按 ARCH §7 建议落为 DTO 定稿值；最终 M0 + 数据侧拍板，会签点 §9-1）

### 3.1 U8-1 · 竞争力五维英文键 + 中文标签映射表

契约示例五维「技术/产业/空间/人才/政策」与 demo 两数组均不符（草案虚构），**弃用**；以 demo `keyAreaDimensionScores`（L424–L430）五个中文名为权威维度名，英文键新定：

| `dim_key`（DTO/表列） | `dim_label`（中文标签） | demo 得分（种子逐字） |
|---|---|---|
| `innovation_resources` | 创新资源 | 92 |
| `research_output` | 科研产出 | 88 |
| `industry_competitiveness` | 产业竞争力 | 85 |
| `talent_support` | 人才支撑 | 78 |
| `open_collaboration` | 开放协同 | 72 |

- **理由沿 ARCH §7.1**：FE-TS-09A 已冻结，demo 中文文案即页面既显内容（定名零页面改动）；英文键为 `dim_key` 新列一次定名避免后续 ALTER；五维语义与核对记录「区域对象竞争力」（KEYD-B03：vs 区域创新活力）对齐，不引「空间维」以免与 185 SPATIAL 混淆。
- **配套**：`competitiveness_metrics` 指标卡五键（composite/innovation/industry/openness/potential）沿 demo 原键不动，与五维画像**并存不合并**；仅 `potential` 行挂 `M_INNOV_KEYD_POTENTIAL`。

### 3.2 U8-2 · `land_benefit` 字段定名与 V1 诚实空

- **定名**：沿用契约示例 `plot_ratio`（容积率）/ `output_per_mu`（亩均产出）——标准园区用地效益口径（「亩均论英雄」通用指标），demo 无既有字段可沿，新定名即以契约为准。
- **诚实语义**：`carriers[].land_benefit` **V1 全 `null`**——demo 冻结种子无逐载体土地数据（土地只有区级 `landUseData` 6 行），**禁编造容积率/亩产数值**（契约示例 `2.8` / `1200` 为草案虚构，禁灌）；187 叶读数由 `land_use` 区级行（district/land_type/area_sqm/efficiency/status）承载。正式态接入 GIS 用地图层后回填真值（回填动作归 KEY-DATA/实现单，DTO 形状不变）。

---

## 4. 契约 §3.7 改约 delta 单列（供批 4 冻结并入 `BE-TS-CONTRACT-02`）

| # | 变更 | 性质 |
|---|---|---|
| 1 | **结构改约（嵌套→平铺）**：`clusters[]` 内不再嵌 `competitiveness` / `carriers` / `plans`；响应改平铺 **9 块** `clusters` / `carriers` / `carrier_types` / `district_baselines` / `competitiveness_metrics` / `dimension_scores` / `benchmark_rows` / `land_use` / `plans` + 顶层 `carrier_total` / `caliber_note` / `metric_ids`；后六块为契约 §3.7 未覆盖的新增块（ARCH §5 实测收口） | 定稿（ARCH 已裁） |
| 2 | **载体归属语义**：22 载体平铺全量下发，`cluster_id` 可空——实测仅 15 行挂集群，`L001`/`L004`/`P003`/`P005`/`I003`/`I004`/`A002` 共 7 行置 NULL（诚实空，不强行归簇）；`clusters[].carrier_ids` 改为引用数组（3 集群合计 15） | 定稿（种子实测） |
| 3 | **plans 页级**：三方案不属集群（demo `keyAreaScenarioPlans` 为页级数组），独立 `plans` 块 3 行；「方案模拟」为 FE Modal 交互，**无模拟端点、无 501** | 定稿（ARCH 已裁） |
| 4 | **`carrier_total` 语义冻结**：= `carriers` 块行数（22，全量落点含未挂集群 7 行）；≠ `carrier_types[].carrier_count`（`all`=2856 为全市口径 demo 计数）；≠ 挂集群载体数（15） | 定稿（本文落册） |
| 5 | **五维 key 改约**：契约示例 `dimension`「技术/产业/空间/人才/政策」弃用 → U8-1 五键五标签（§3.1：`dim_key` 英文键 + `dim_label` 中文名，形状由 `{dimension,score}` 改 `{dim_key,dim_label,score}`） | 定稿（ARCH 建议本文落册） |
| 6 | **`land_benefit`**：字段名沿用（`plot_ratio`/`output_per_mu`），**V1 恒 `null`**（契约示例值 2.8/1200 为虚构，禁灌）；187 读数由 `land_use` 区级行承载 | 定稿（ARCH 已裁） |
| 7 | **标识值域改约**：契约示例 `cluster_id=CL-FUT-05`、`carrier_id=C-01`、`plan_id=PLAN-A` 弃用 → 沿 demo 冻结键 `ai`/`bio`/`energy`、`L001`–`A003`、`a`/`b`/`c` | 定稿（种子实测） |
| 8 | **plans 字段扩展**：`name`→`plan_name`；增 `title` / `priority` / `expected_effect` / `resource_gap` / `actions[]` / `primary_action` / `secondary_action` / `detail_action`（三个 action 文案列表行携带） | 定稿（本文落册） |
| 9 | **metric_id 占位替换**：`Q0xx` → 四条 `M_INNOV_KEYD_SPATIAL` / `M_INNOV_KEYD_COMPETITIVENESS` / `M_INNOV_KEYD_POTENTIAL` / `M_INNOV_KEYD_LAND`（均**未签**，回填规则 §6） | 定稿（对齐核对记录） |
| 10 | **枚举字典注记**：新增字典性枚举 `carrier_type` 五类（lab/center/park/incubator/accelerator）与 `land status` 三档（good/medium/poor）；本端点无 Query，枚举不做入参校验，是否并入契约 §2 字典待批 4 拍板 | **建议，待会签** |
| 11 | **表清单调整（契约 §4 表 #5）**：建议 2 张（competitiveness/land_benefit 塞 JSON 列）→ 专用 **9 张**（沿 OV「专用表」先例，JSON 大列拆行表可维护可排序，仅 `carrier_ids`/`actions`/`land_benefit` 保 JSON）；两张建议名 `ts_plan_key_area`/`ts_plan_key_area_carrier` 原样沿用；DDL 归 KEY-DATA 分册 | 定稿（ARCH 已裁） |
| 12 | **plans 字段弃用（v2 补漏）**：契约嵌套示例 `plans[].summary` **弃用**——demo 无此数据，方案主题由 `title` 承载（delta-8 扩展字段的同族补漏） | 定稿（会签补漏） |

---

## 5. 189 交互壳（无端点）与 188 载体详情随响应下发

### 5.1 seq 189 · 产业与领域筛选联动 — 交互壳，后端零改动

- **判定**：核对记录 §3.3 ④ 差集 **n/a_ops**（大门类/细分 + 地图联动壳；xlsx 98/99 技术规模/发展状态随壳展示，不另开 missing）；禁 mapped 综合 189 / 技术链 133/137。B.1 备注同口径（同 OV 179 交互叶性质）。
- **实现**：产业大门类（`clusters[].industry_category`）/ 科技领域细分（`clusters[].technology_field`）/ 载体类型（`carrier_types[]`）公共筛选 + 集群导航（`clusters` 行）+ 图层单选（**4 值**：产业热度 / 科技载体 / 土地效益 / **资源缺口**，FE 本地常量，KeyAreaTab model L985——v1 误写 3 值，v2 勘误；种子 `default_map_layer` 仅用其中三值，§2.1）**全为 FE 状态**；对 `key-areas` **一次取全（9 表 61 行）本地过滤联动**——无独立端点、无 Query、无分页、无服务端过滤（V1 量级无必要）；领军主题由集群 `technology_field` + 载体 `level` 既有列承载。
- **metric_id**：无（n/a_ops）。

### 5.2 seq 188 · 载体详情随响应下发

载体详情字段（`carrier_type` / `district` / `level` + 坐标）**随 `carriers` 块一次下发**，点击地图 marker 无二次请求、无详情端点；FE 堆叠/区县/列表三视图全由 `carriers` + `carrier_types` + `district_baselines` 三块派生，无派生表无派生端点（ARCH §4.4）。**非载体价值排名**（other_system；禁抢 DS-06-CARRIER missing、禁 mapped 116 / 综合 188），无 metric_id，计数旁不显伪 8 件套。

---

## 6. metric_id 回填规则（会签落册）

| 项 | 定稿 |
|---|---|
| 回填值（**逐字**） | `clusters` 行=`M_INNOV_KEYD_SPATIAL`；`competitiveness_metrics` 行 `potential`→`M_INNOV_KEYD_POTENTIAL`、其余→`M_INNOV_KEYD_COMPETITIVENESS`；`dimension_scores` / `benchmark_rows` 行=`M_INNOV_KEYD_COMPETITIVENESS`；`land_use` 行=`M_INNOV_KEYD_LAND`；顶层 `metric_ids`=四条去重（顺序 SPATIAL→COMPETITIVENESS→POTENTIAL→LAND） |
| 状态标注 | 四条均**赋号草稿·未签**（STAT×2：SPATIAL/LAND 差集 other_system；MIXED×2：COMPETITIVENESS/POTENTIAL 差集 mapped 186 仅语义、同叶不同页不改挂；公式 `pending human:唐绍祖`；Q-MO-DS09-04 权重未签）→ UI ⚠️「待甲方确认」+ ⓘ draft 语义卡回指核对记录 §赋号表 |
| 无统计核块 | 核对记录 §3.3 ④ 不适用三叶（188 other_system / 189 n_a_ops / 190 n_a_ops）对应块（`carriers` / `carrier_types` / `district_baselines` / `plans`）**行不设 `metric_id` 字段、对顶层 `metric_ids` 恒零贡献（`[]`）**；表列置 NULL 仅作 DDL 一致性 |
| 禁取段 | **禁取 `Q010`–`Q019` / `QPOL-*` 等占位段**；禁自造 `M_KEYDOMAIN_*` / `M_SPATIAL_*` 等新号 |
| 撞号禁令（随稿冻结） | 展示 185–190 与综合 05 185–190 整段撞号，禁按号 mapped；185 禁 mapped 191 / 复用 `M_ENT_AGGLOMERATION_INDEX`；186 禁改挂 `M_SYNTH_VIT_*` / GBA/CITY 186 号 / 企业 141 / `M_CHAIN_COMPETITIVENESS_INDEX` / `M_CHAIN_REGION_INDEX`；POTENTIAL 禁挂技术链 135 / `M_TECH_POTENTIAL_SCORE`；187 禁按号综合 187；188 禁 mapped 116；189 禁技术链 133/137；190 禁 `M_CHAIN_LAYOUT_*` / `M_POLICY_INDUSTRY_FIT`；禁 B 轨 / SYNTH / CHAIN / SVC / TECH 全族与湾区 DS-05、深圳 DS-06-CITY/CARRIER/DOMAIN、DS-07、DS-08 混挂（ARCH §7.3） |
| 回填时点与行源 | 时点=**批 4 冻结**，由 `BE-TS-CONTRACT-02` 落契约正文（同 OV §0 口径）；物理行源=各表 `metric_id` 列（灌数脚本写入）；签后回填不改差集判定、不升 🟢、不写任何 `cfg_metric-*-seed.yaml` |

---

## 7. FE 接线差异清单（页面零改动，只改 api 拼装层）

**现状**：OV 分册 §6 已预留「09b 块（`carrierTypes`/`industryClusters`/… 等）在 KEY/RES 分册端点冻结前 real 分支局部保留 mock 种子（显式 TODO 标注），二步接线」——**本节即该 TODO 的落定**。接线文件族不变：`repos/lumen-ui-science-pc/src/api/situation/techDevelopmentPlan.ts`（仅此文件族）。

**组装点**：`fetchTechDevelopmentPlanDataset` real 分支增挂 `GET /display/v1/situation/planning/key-areas`（R 信封解包取 `resp.data`；与 09a 端点一并 `Promise.all` 或 Tab2 切页懒加载，由接线实现单拍板——页面零改动约束不变）；`defineApi` id `tsTechDevelopmentPlanDataset` 保持，类型文件零改动，映射全在 api 层做。

**dataset Tab2 9 数据块 → key-areas 端点组装映射**（种子 L347–L505 ↔ §2 各块；类型零改动）：

| dataset 块（types 字段） | 来源块 | 名称/形状映射 | 缺口处置 |
|---|---|---|---|
| `carrierTypes` | `carrier_types` | `key←type_key`、`name←type_name`、`count←carrier_count`、`color` 同名；按 `sort_no` 排序 | — |
| `carrierLocations` | `carriers` | `id←carrier_id`、`type←carrier_type`、`district`/`lng`/`lat`/`level` 同名；`cluster_id`/`land_benefit` 页面暂不渲染（189 联动可透传、187 预留恒 null），实现单定去留 | — |
| `industryClusters` | `clusters` | `key←cluster_id`、`label←cluster_name`、`industryCategory←industry_category`、`technologyField←technology_field`、`mapLayer←default_map_layer`、`carrierIds←carrier_ids` | — |
| `districtCarrierBaselines` | `district_baselines` | `district` 同名、`total←total_carriers`、`leadingType←leading_type` | — |
| `landUseData` | `land_use` | `area←district`、`type←land_type`、`area_sqm`/`efficiency`/`status` 同名 | — |
| `keyAreaScenarioPlans` | `plans` | `id←plan_id`、`name←plan_name`、`title`/`priority`/`actions` 同名、`expectedEffect←expected_effect`、`resourceGap←resource_gap`、`primaryAction←primary_action`、`secondaryAction←secondary_action`、`detailAction←detail_action` | — |
| `keyAreaCompetitivenessMetrics` | `competitiveness_metrics` | `key←metric_key`、`label`/`value` 同名、`change←change_pct` | — |
| `keyAreaDimensionScores` | `dimension_scores` | `label←dim_label`、`percent←score`（`dim_key` api 层留存备用） | — |
| `keyAreaBenchmarkRows` | `benchmark_rows` | `region`/`score` 同名、`rank←rank_no` | — |

- Tab2 **九块全部有端点来源，无「保持 mock 种子」残留项**（区别于 OV 分册 09a 的四处会签点）；`carrier_total`/`caliber_note`/`metric_ids` 由页面 ⓘ draft 语义卡与 189 壳消费（或暂不消费，实现单定）。
- Mock 徽标：D18 读数 D4 仍 mock → 🧪 MockBadge 保留至 D4 翻转；`USE_MOCK=true` 分支种子演示不变。

---

## 8. 合规自检

| # | 检查项 | 结论 |
|---|---|---|
| 1 | 调用链 | 前端 → 网关（`/display/**`）→ `gkxlumen-display` Java REST（复用 `PlanningController`，零新 Controller）→ **只读 ADS**（9 张 `ts_plan_key_area_*`）；Python 仅灌数期一次性写表、无运行时依赖；无 `demo-*` 依赖（D12）；不涉对象存储（D14 N/A）；不涉 NebulaGraph |
| 2 | 读写面 / 501 | 1 读 0 写；本页**零 501**（catalog 501 通道只给 COMPREHENSIVE seq 184；190 方案模拟=FE Modal 非 501） |
| 3 | D18 无接口直返 mock | 唯一端点全量读表；`caliber_note`（行源 **`ts_plan_key_area_dimension.rendered_note`**，v2 更正）/ plans 三个 action 文案列等全部表行携带、来源列已写明，禁 Java 硬编码；禁灌项显式：`carrier.land_benefit` V1 全 NULL、种子外派生数值（集聚度/密度）不补算；空态诚实（按块空数组 + `empty_reasons` 落位，§2.0） |
| 4 | metric_id | 全部引用核对记录 §赋号表四条草稿并标「未签」；不发明新 `M_*`；188/189/190 无核块不设字段、零贡献；回填规则/禁取段/撞号禁令落册（§6） |
| 5 | 网关路径 | 符合 api 规约铁律 9（网关=网关地址/display/@RequestMapping/方法映射），无前缀插序错误形态 |
| 6 | 诚实标注 | `land_benefit` V1 恒 null（禁编造 2.8/1200）；7 载体 `cluster_id` NULL 不强行归簇；`carrier_count` 全市口径计数 🧪；四条 metric ⚠️「待甲方确认」+ ⓘ draft；KEYD-B01..B03 语义债沿袭不动 |
| 7 | 交付边界 | 未改 task-registry、未 git 提交、未写业务代码；仅落本分册一个文件 |

## 9. 会签待决点（需四方会签讨论）

1. **U8 两裁定最终拍板**（M0 + 数据侧）：U8-1 五维英文键（§3.1）与 U8-2 `land_benefit` 定名（§3.2）——本文已按 ARCH 建议落为 DTO 定稿值，拍板即冻结，否决则改本文 §2.6/§2.2 与 §4 delta-5/6。
2. **列名对齐**：`rendered_note` / `dim_order` / 各表 `sort_no` 已随 v2 会签对齐 KEY-DATA DDL；余者（`carrier_id`〔ARCH 简记 `id`〕、land 表预留 `land_benefit`）以 KEY-DATA 分册 DDL 终准，冲突改本文。
3. **`carrier_total` 语义冻结**（=22 全量落点，§2.10/§4 delta-4）确认。
4. **§4 delta-10 枚举字典**：`carrier_type` 五类 / `land status` 三档是否并入契约 §2 字典（本端点无入参校验，仅字典性质）。
5. **`caliber_note` 文案（v2 已收口，会签裁定归 DATA 种子定稿）**：文案由 **KEY-DATA 分册种子行定稿**（V1 占位整句见其 §2.6，M0 定稿后翻换），本分册只定「表行携带」机制——消除 v1「API 待 DATA 定 / DATA 待 API 定」互指循环。

---

## 会签修订记录 v2（2026-11-06）

architect / api / algorithm 三家会签**同意**，必改项已逐条修订（本文件 v1→v2，仍仅改本文件、不碰其他）：

| # | 会签项 | 修订内容（落点） |
|---|---|---|
| 1 | caliber_note 行源更正（三家一致） | §2.10 行源由 `ts_plan_key_area_competitiveness.caliber_def` 更正为 **`ts_plan_key_area_dimension.rendered_note`**（表名+列名双改，对齐 KEY-DATA DDL §2.6；五维行 5 行同值，Java 取任一行）；§2.6 增列注（`rendered_note`/`dim_order` 非行级 DTO 字段）；§8-3 随改 |
| 2 | 文案定稿归属收口 | 会签裁定**归 DATA 种子定稿**：§9.5 改为「caliber_note 文案由 KEY-DATA 分册种子行定稿（V1 占位整句、M0 定稿后翻换），本分册只定表行携带机制」，消除 API §9.5 与 DATA §2.6 的互指循环；§2.10 说明同步（含占位整句逐字引用） |
| 3 | 排序保证补齐 | §2.0 增「排序保证」：clusters / carriers / competitiveness_metrics / dimension_scores / land_use / plans 各块按表 `sort_no`（dimension 表 `dim_order`）**ASC** 返回，FE 数组序以此为据（v1 仅 carrier_types 有）；district_baselines 同 `sort_no`、benchmark_rows 按 `rank_no`；§2.3 改注为「九块中唯一 DTO 下发的排序列」，其余服务端保证不进 DTO |
| 4 | delta 补漏 | §4 增 **delta-12**：契约嵌套示例 `plans[].summary` 弃用——demo 无此数据、方案主题由 `title` 承载（delta-8 同族补漏） |
| 5 | 图层全集勘误 | §5.1 图层单选由 3 值勘误为 **4 值**（+「资源缺口」，KeyAreaTab model L985）；§2.1 `default_map_layer` 注明为四值类型中种子使用的三值 |
| 6 | empty_reason 落位 | §2.0 增「`empty_reason` 落位」（对齐 OV 诚实空态先例的多块扩展）：`data.empty_reasons` 对象、键=块名、仅空块出现、恒 `no_source`（本端点无 Query 无 `filter_empty` 面）、九块全满省略；§0 空态行 / §2.10 增条件字段行 / §8-3 随动 |
