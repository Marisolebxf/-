# TS-L2-DS09-OV-DATA · 综合发展规划 · 后台数据架构设计

> **任务**：`TS-L2-DS09-OV-DATA`（definition，不建表、不灌数、不跑脚本）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 data-agent（监管人 `human:王梓真`）
> **状态**：草案 v2（architect / api / algorithm 三家会签意见已并入，待 data 复核签收；修订清单见 §9）
> **硬依赖**：`sdd/l2/TS-L2-DS09-OV-ARCH.md`（8 张表清单与 D18 三要素见其 §0/§6；本分册 DDL 不与其冲突，差异均为事实澄清，见 §0）
> **范围**：DS-09 综合发展规划页签（需规序 178–184）8 张 `ts_plan_*` 表的库/DDL 冻结 + 行源实测清单 + 灌数方案规格 + 订阅面确认

**行源真源（实测对象）**

| 用途 | 真源 |
|---|---|
| demo 冻结种子（主） | `lumen-ui-science-pc/src/mock/modules/techDevelopmentPlan.ts`（下称 **mock**） |
| 类型对照 | `lumen-ui-science-pc/src/types/techDevelopmentPlan.ts` |
| 时间轴 / 地图点位种子 | `demo-ui-science/src/techDevelopmentPlan.js`（下称 **demo.js**；lumen mock 未复刻这两块，契约 §3.3 同款真源） |
| 接口形状 | `agent-handoffs/科技发展态势-TS/API-TS-M9.md` §2/§3（草案） |
| 订阅面 | `lumen-svc-platform` `gkxlumen-display` subscription 包 + `db/9x_gkxlumenx_user_behavior.sql` |

---

## 0. 对 ARCH 稿的事实澄清（不改 D18 判定，仅纠口径）

1. **序列粒度**：ARCH §4.1 称 `heat_series` 年度序列；种子实为**季度标签 × 三区间**（`technologyTrendSeriesByRange`：`3m` 3 点 / `6m` 4 点 / `12m` 9 点 × 8 技术）。表按「技术 × 区间 × 期」存，契约示例的 `year` 字段由 API 拼装层从 `period_label` 映射（OV-API 分册定）。
2. **空间分布无坐标**：ARCH/契约 §3.2 的 `spatial_distribution` 示例含 `lng/lat`；种子 `technologyTrendSpaceRegions`（mock L168–174）只有 **5 区 factor、无坐标**，且页面空间柱图是 FE 派生（`heat × factor`，model `buildTrendBarOption`）。本分册裁定：hot_tech 表 `spatial_distribution` 存 factor 数组逐字，**不预计算派生值、不造坐标**；坐标类点位语义由 `ts_plan_tracking_point`（regionCoordinates 7 城坐标）承载。
3. **订阅分派列名**：ARCH §4.6 写 `rule_type=planning_resource`；既有体系（`SubscriptionAdapter`/`SubscriptionAdapterRegistry`/`sys_user_subscription_rule`）实际分派列是 **`scope_type`**（varchar(32) 自由枚举，无 `rule_type` 列）。本分册按 `scope_type='planning_resource'` 新枚举值落位，**零 DDL**（§5）。
4. **reference_stats 无种子**：契约 §3.4 引「demo L361–L362」；该位置实为 `buildPlanRows`，demo.js 与 mock 均无 72/1240/215.4 三个数。本分册取**契约草案示例值逐字**灌 1 行 meta，`source='contract_draft_sample'`，「示例抽样」字样保留（契约边界原文），正式态换真源。**S-3 已裁定（architect，v2）**：灌入——需规 181 要求对比展示，整块空态反缺位。
5. **tracking 两表种子不在 mock**：lumen FE 09a 动态跟踪块用趋势折线 + 空间柱图（无时间轴/地图），时间轴与点位行源取 demo.js（契约同款真源）：`techDevelopmentPlanTimeline` 7 事件、`planRecords` 7 记录 × `regionCoordinates` 7 城坐标 × `layerKeys` 5 层（`buildMapRegions` L367–L381 逐字语义）。**`ts_plan_record` 仍取消**（ARCH §5 收口不变），仅点位投影入 `ts_plan_tracking_point`，记录正文（risk/evidence/recommendation）不建表不灌。

---

## 1. 库与表总表

**库**：展示 ADS MySQL · **`gkxlumenx_ads`**（demo 环境对应 `demo_gkxlumenx_ads`）。理由：

1. ARCH §6 建议落展示 ADS（D18：ADS 是应用唯一读面，Java 只读）；
2. `gkxlumenx_ads` 为既有展示 ADS 库，display/element 模块已有跨库只读先例（`gkxlumen-element` 连 `demo_gkxlumenx_ads`、cms 视图 join `gkxlumenx_ads.svc_org_card`），同库即复用只读账号与连接治理；
3. **D18 声明：8 张表不进 ODS / DWD / 供应方 `gkx` 库**（供应方库只读不可写，且本组为展示种子非入站再加工）；**不带 `gapfill_` 前缀**（非 D16 缺项表，是 D18 读表正身）；
4. `ts_plan_` 前缀在库内唯一，不与既有 `ads_*` / `svc_*` 族冲突。

字符集 `utf8mb4` / `utf8mb4_general_ci`（对齐 `db/9x_*.sql` 既有惯例）。引擎 InnoDB。**建表 DDL 的执行归 Java 实现单**（`lumen-svc-platform` SQL 变更），本分册只冻结列定义。

**列名基准（v2，会签 item 7）**：全组（OV-API / Java 实现 / FE 接线 / 灌数脚本）列名以本分册 DDL 为准——metric_system 环比列 = `metric_change`（非 change）；序列期列 = `period_label`（非 year/period）、序列热度列 = `heat_value`（hot_tech 主表热度列为 `heat`）；热点口径 = `caliber_def`（三要素 JSON）+ `rendered_note`（整句，响应 `caliber_note` 的物理行源，禁止 Java 拼文案）。契约示例字段与本分册列名不一致处，映射表落 OV-API 分册。例外：§5 A3 订阅产物表 `sys_user_planning_push_record` 不落 ADS，落 `gkxlumenx`（upms 主库，随 `db/9x_gkxlumenx_user_behavior.sql` 用户行为家族）。

| # | 表 | 行数（V1 实测种子） | 消费接口（契约 §） | D18 灌数方 |
|---|---|---|---|---|
| 1 | `ts_plan_hot_tech` | 8 | §3.2 hot-technologies | Python 一次性脚本 |
| 2 | `ts_plan_hot_tech_series` | 128 | §3.2（heat_series） | 同上 |
| 3 | `ts_plan_metric_system` | 30 | 第 9 端点 metric-system（G-B2 方案 A） | 同上 |
| 4 | `ts_plan_tracking_event` | 8（1 meta + 7 事件） | §3.3 tracking | 同上 |
| 5 | `ts_plan_tracking_point` | 35（7 点 × 5 层） | §3.3 tracking（spatial.points） | 同上 |
| 6 | `ts_plan_local_adv` | 19（18 维度 + 1 reference） | §3.4 local-advantage | 同上 |
| 7 | `ts_plan_talent_flow` | 16（6 stats + 5 机构 + 5 聚合） | §3.5 talent-flow | 同上 |
| 8 | `ts_plan_direction_warning` | **0（V1 零行，禁灌假预警）** | §3.1（未注册 501） | 无（模型注册后由模型方 Python 写入） |
| — | 订阅面：app_user 家族 | **零 DDL 变更** | §3.6 resource-push + subscriptions | 既有体系（§5） |
| — | `sys_user_planning_push_record`（订阅产物表，**gkxlumenx** upms 主库） | **0（初始零行，真实推送产生）** | §3.6 resource-push | 无灌数——适配器命中推送时写入（§5 A3 裁定） |

种子合计：8+128+30+8+35+19+16 = **244 行**；另有订阅产物表 `sys_user_planning_push_record` 初始 0 行（非种子，真实推送产生，不计入合计）。

---

## 2. 逐表 DDL 草案

> 约定：`id bigint unsigned AUTO_INCREMENT` 主键、`created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP`（灌数时间戳）、`source varchar(16)`（行源标注：`demo_seed` 冻结自 demo / `lumen_seed` lumen 复刻补充 / `contract_draft_sample` 契约草案示例）为公共列，下文每表不重复注释。数值演示种子标 🧪（D4=mock，MockBadge 保留至翻转）。

### 2.1 `ts_plan_hot_tech`（8 行，序 178）

```sql
CREATE TABLE ts_plan_hot_tech (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  tech_id       varchar(16)  NOT NULL COMMENT '技术ID（种子 hotTechData.id，1..8）',
  name          varchar(64)  NOT NULL COMMENT '技术名（人工智能大模型…）',
  category      varchar(32)  NOT NULL COMMENT '类别（AI/量子科技/生物工程…）',
  heat          smallint unsigned NOT NULL COMMENT '热度指数 0-100 🧪（种子 heat）',
  growth        decimal(5,1) NOT NULL COMMENT '增长速度 % 🧪（种子 growth，如 45.2）',
  hot_trend     varchar(8)   NOT NULL COMMENT 'hot热点/rising上升/stable平稳（契约 §2.5；种子 trend）',
  patents       int unsigned NOT NULL COMMENT '专利数 🧪（种子 patents）',
  papers        int unsigned NOT NULL COMMENT '论文数 🧪（种子 papers）',
  description   varchar(255) NOT NULL COMMENT '技术描述（种子 description 逐字）',
  spatial_distribution json  NOT NULL COMMENT '空间分布因子数组 [{"name":"南山区","factor":1.08}×5]（种子 technologyTrendSpaceRegions 逐字，无坐标；派生=heat×factor 由 FE 做，见 §0.2）',
  caliber_def   json         NOT NULL COMMENT '热度口径三要素 {scoreFormula,inclusionRules,defaultRule}（种子 technologyHeatTrendDefinition 逐字；口径构成由表行携带，非 Java 硬编码）',
  rendered_note varchar(255) NOT NULL COMMENT 'U5 口径整句（v2 item 3，algorithm 会签③）：「热度 = 论文 40% / 专利 30% / 项目 20% / 资讯 10%（口径待 M0 定稿，U5）」逐字（行源=契约 §3.2 caliber_note 原文；M0 定稿后随 U5 翻换）——响应 caliber_note 取本列，禁止 Java 拼文案',
  metric_ids    json         NOT NULL COMMENT '赋号草稿·未签（v2 item 1，algorithm 会签②）：["M_INNOV_PLAN_HEAT","M_INNOV_PLAN_GROWTH"]；heat 列挂 HEAT、growth 列挂 GROWTH，字段级映射 OV-API 定。取一列 JSON 而非两列：对齐契约 §3.2 响应 metric_ids 数组形态',
  source        varchar(16)  NOT NULL DEFAULT 'demo_seed',
  created_at    datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_tech_id (tech_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·全球热点技术（D18 读表，序178）';
```

`caliber_def`、`spatial_distribution`、`rendered_note`、`metric_ids` 为演示/草稿内容，8 行同值冗余（Java 取任一行拼装响应，避免第 9 张配置表）。

### 2.2 `ts_plan_hot_tech_series`（128 行，序 178）

```sql
CREATE TABLE ts_plan_hot_tech_series (
  id           bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  tech_id      varchar(16) NOT NULL COMMENT '逻辑引用 ts_plan_hot_tech.tech_id（无物理 FK）',
  range_key    varchar(4)  NOT NULL COMMENT '3m/6m/12m（契约 §2.8；种子 technologyTrendSeriesByRange 键）',
  period_label varchar(8)  NOT NULL COMMENT '期标签，季度粒度逐字（2025Q4…2026Q2）🧪；契约 heat_series.year 由 API 拼装层映射（§0.1）',
  period_order smallint    NOT NULL COMMENT 'x 轴序（区间内 1..N）',
  heat_value   smallint unsigned NOT NULL COMMENT '热度值 🧪（种子 series[techId][i]）',
  source       varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at   datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_tech_range_order (tech_id, range_key, period_order),
  KEY idx_range (range_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·热点技术热度序列（技术×区间×期，序178）';
```

行数展开：`3m` 8×3=24、`6m` 8×4=32、`12m` 8×9=72，合计 **128**。

### 2.3 `ts_plan_metric_system`（30 行，序 179，n/a_ops 运营壳）

```sql
CREATE TABLE ts_plan_metric_system (
  id             bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  category_key   varchar(32) NOT NULL COMMENT '分类键（种子 key：technology/industry/institution/project/achievement/statistics/talent，7 类）',
  category_label varchar(32) NOT NULL COMMENT '分类名（技术发展/产业数据库/机构库/课题库/成果库/统计库/人才库）',
  metric_label   varchar(32) NOT NULL COMMENT '指标卡名（热度指数/增长速度/文献数量…）',
  metric_value   varchar(32) NOT NULL COMMENT '指标值逐字字符串（12,580 / 186.7亿 / 18.3万），不数值化（demo 口径，数值化待 M0 同 U4 族）🧪',
  metric_unit    varchar(16)          DEFAULT NULL COMMENT '单位（从 value 机械拆分，可空；ARCH value/unit 拆分落位）',
  metric_change  varchar(16) NOT NULL COMMENT '环比字符串逐字（+12.3%）🧪',
  linked_json    json        NOT NULL COMMENT '分类联动标签数组（种子 linked 逐字，冗余存于该类每行）',
  category_order smallint    NOT NULL COMMENT '分类顺序 1..7（种子数组序）',
  sort_order     smallint    NOT NULL COMMENT '分类内卡片顺序 1..6',
  source         varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at     datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_cat_metric (category_key, metric_label),
  KEY idx_category (category_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·多维度指标体系卡片（运营壳，无 metric_id，序179）';
```

### 2.4 `ts_plan_tracking_event`（8 行 = 1 meta + 7 事件，序 180）

```sql
CREATE TABLE ts_plan_tracking_event (
  id          bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  row_kind    varchar(8)  NOT NULL COMMENT 'timeline_meta（1 行）/ event（7 行）',
  title       varchar(64)          DEFAULT NULL COMMENT 'meta 行：科技发展规划研判演进（demo.js L30 逐字）',
  current_year char(4)             DEFAULT NULL COMMENT 'meta 行：2026（种子 currentYear）',
  range_label varchar(16)          DEFAULT NULL COMMENT 'meta 行：2020-2026（种子 rangeLabel）',
  years_json  json                 DEFAULT NULL COMMENT 'meta 行：["2020".."2026"] 7 值（种子 years 逐字）',
  event_date  varchar(7)           DEFAULT NULL COMMENT 'event 行：2020-05…2026-04（种子 events[].date 逐字）',
  event_year  char(4)              DEFAULT NULL COMMENT 'event 行：年份（date 前 4 位，时间轴挂载用）',
  region      varchar(32)          DEFAULT NULL COMMENT 'event 行：全球/深圳/粤港澳大湾区/上海/北京/杭州/深圳（逐字）',
  event_text  varchar(255)         DEFAULT NULL COMMENT 'event 行：事件正文（逐字）',
  event_order smallint             DEFAULT NULL COMMENT 'event 行：时间序 1..7',
  source      varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_kind_order (row_kind, event_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·动态跟踪研判演进时间轴（序180；行源=demo.js，§0.5）';
```

### 2.5 `ts_plan_tracking_point`（35 行 = 7 点 × 5 层，序 180）

```sql
CREATE TABLE ts_plan_tracking_point (
  id          bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  result_type varchar(16) NOT NULL COMMENT 'hotspot/space/talent/report/warning（契约 §2.2 = demo.js techDevelopmentPlanLegend.resultTypes 5 类逐字）',
  source_id   varchar(32) NOT NULL COMMENT '来源规划记录 ID（demo.js planRecords.id，tdp-*；记录本体不建表，§0.5）',
  name        varchar(64) NOT NULL COMMENT '点名（demo buildMapRegions.name = region 名逐字）',
  region      varchar(32) NOT NULL COMMENT '区域名（深圳/粤港澳大湾区/北京/上海/杭州/苏州/广州）',
  lng         decimal(8,5) NOT NULL COMMENT '经度（demo regionCoordinates.position[1]；demo position=[lat,lng]，入库拆列）',
  lat         decimal(8,5) NOT NULL COMMENT '纬度（position[0]）',
  score       smallint unsigned NOT NULL COMMENT '规划优先级分 🧪（planRecords.score；level 高/中/低由 score≥88/≥82 派生，不落列）',
  source      varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_src_type (source_id, result_type),
  KEY idx_result_type (result_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·动态跟踪空间点位（点×图层展开，序180）';
```

展开依据：demo `buildMapRegions` 对每个记录点挂**全部 5 个 layerKeys**，契约 §3.3 point 单 `result_type` → 每点按 5 层各 1 行（7×5=35），Java 读表 `WHERE result_type=?` 直拼。`carrierLocations`（22 载体）属 09b KEY 组（契约 §3.7），**不入本表**。

### 2.6 `ts_plan_local_adv`（19 行 = 18 维度 + 1 reference，序 181）

```sql
CREATE TABLE ts_plan_local_adv (
  id              bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  row_kind        varchar(12) NOT NULL COMMENT 'dimension（18 行）/ reference（1 行）',
  dimension_key   varchar(16)          DEFAULT NULL COMMENT 'dimension 行：field/capability/output（契约 §3.4 三键逐字；映射 field←localAdvantageChart、capability←localAdvantageInnovation、output←localAdvantageOutput，见会签点 S-2）',
  dimension_label varchar(16)          DEFAULT NULL COMMENT '领域/能力/产出',
  indicator_name  varchar(64)          DEFAULT NULL COMMENT '对比项（合成生物学…/顶尖人才密度…/高被引论文…，yAxis 逐字）',
  local_score     smallint unsigned    DEFAULT NULL COMMENT '深圳分 🧪（种子 local[]）',
  global_score    smallint unsigned    DEFAULT NULL COMMENT '全球平均 🧪（种子 globalAvg[]）',
  indicator_order smallint             DEFAULT NULL COMMENT '维度内顺序 1..6',
  base_region     varchar(16) NOT NULL DEFAULT '深圳' COMMENT '对比基准（图例「深圳」）',
  compare_to      varchar(16) NOT NULL DEFAULT '全球' COMMENT '对比对象（图例「全球平均」→契约 compare_to=全球）',
  metric_id       varchar(32) NOT NULL COMMENT 'M_INNOV_PLAN_LOCAL_ADV（赋号草稿·未签，MODEL，Q-MO-DS09-01；v2 item 1，algorithm 会签②）；表级指标，各行同值冗余',
  reference_json  json                 DEFAULT NULL COMMENT 'reference 行：{hotspots:72,carriers:1240,capacity:215.4,source:"全球公开数据库（示例抽样）"}（契约 §3.4 草案示例值逐字；「示例抽样」保留至正式态换真源）',
  source          varchar(16) NOT NULL COMMENT 'field 行=demo_seed；capability/output 行=lumen_seed（FE 补两维正式化，B.1/G-B4）；reference 行=contract_draft_sample（§0.4）',
  created_at      datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_dim_order (row_kind, dimension_key, indicator_order),
  KEY idx_dimension (dimension_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·本地特色与优势对比（三维度 vs 全球 + 参照统计，序181）';
```

FE 补充两维度（`localAdvantageInnovation`/`localAdvantageOutput`）以 `source='lumen_seed'` 标注（**硬要求落实**）。

### 2.7 `ts_plan_talent_flow`（16 行，序 182；U6 表结构级无个人明细）

```sql
CREATE TABLE ts_plan_talent_flow (
  id           bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  row_kind     varchar(16) NOT NULL COMMENT 'stats（6 行）/ institution_flow（5 行）/ record（5 行）',
  -- stats 汇总行（种子 talentDirectionNodes 6 节点）
  stat_key     varchar(32)          DEFAULT NULL COMMENT 'od_shenzhen/od_external/node_academia/node_industry/node_gov/node_other',
  label        varchar(64)          DEFAULT NULL COMMENT '节点/口径名逐字（学术界/产业界/政府/科研院所/其他；深圳/外地）',
  color        varchar(9)           DEFAULT NULL COMMENT '节点演示色（#1677ff 等，种子 itemStyle.color 逐字，演示态展示用）',
  region       varchar(16)          DEFAULT NULL COMMENT 'OD 行：深圳/外地',
  person_count int unsigned         DEFAULT NULL COMMENT 'OD 行总量 🧪：深圳=18932、外地=12458（G-B4：FE 写死值改由表行提供）；record 行恒 1',
  trend_pct    decimal(5,1)         DEFAULT NULL COMMENT 'OD 行增幅 % 🧪（21.7/16.2，种子 ↑x%）',
  od_nodes     json                 DEFAULT NULL COMMENT 'FE 人才流向图六节点逐字 JSON（v2 item 2）：[{name,itemStyle:{color}}×6]（学术界/产业界/政府/科研院所/其他/外地|12,458人|↑16.2%/深圳|18,932人|↑21.7%，OD 总量 18932/12458 内嵌标签）；行源=种子 talentDirectionNodes 逐字不拆；供 API 分册新增 od_nodes 字段消费；冗余存于 6 条 stats 行（同 caliber_def 模式）',
  -- institution_flow 机构净流入行（种子 talentInstitutionFlowRows 5 行）
  institution  varchar(128)         DEFAULT NULL COMMENT '机构名（华为技术有限公司…中山大学（深圳））',
  net_inflow   int                  DEFAULT NULL COMMENT '净流入（带符号整数：+1248/+987/+756/-328/-276；种子 netInflow 字符串去千分位）🧪',
  flow_direction varchar(4)         DEFAULT NULL COMMENT 'in/out（种子 trend up→in / down→out）',
  -- record 聚合行（种子 talentFlowData 5 行，机构级聚合；name/avatar 丢弃不入库）
  flow_id      varchar(16)          DEFAULT NULL COMMENT 'tf-{种子 id}（tf-1..tf-5）',
  from_org     varchar(128)         DEFAULT NULL COMMENT '流出机构（清华大学/腾讯科技/MIT…）——机构级，非个人',
  to_org       varchar(128)         DEFAULT NULL COMMENT '流入机构（华为技术/中科院/字节跳动…）',
  from_type    varchar(16)          DEFAULT NULL COMMENT 'university/enterprise/research（机构类型枚举，非个人属性）',
  to_type      varchar(16)          DEFAULT NULL COMMENT '同上',
  field        varchar(64)          DEFAULT NULL COMMENT '领域（具身智能/AI安全/多模态模型/知识图谱/机器人控制）',
  flow_type    varchar(16)          DEFAULT NULL COMMENT '学术→产业 / 产业→学术（契约 §2.6 逐字；种子 academia-to-industry/industry-to-academia 映射；「预警流动」= 筛选特例 risk_level=warning，不作存储值——契约 §3.5 边界原文）',
  risk_level   varchar(8)           DEFAULT NULL COMMENT 'NULL / warning（种子 riskLevel；契约 §3.5 risk_level Query）',
  updated_at   varchar(16)          DEFAULT NULL COMMENT '种子 date 逐字（2026-03-20…；字符串口径同 U4，数值化待 M0）',
  metric_id    varchar(32)          DEFAULT NULL COMMENT 'M_INNOV_PLAN_TALENT_FLOW（赋号草稿·未签，MODEL，Q-MO-DS09-02 + U6 法务未决；v2 item 1，algorithm 会签②）；表级指标，行值冗余',
  source       varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at   datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_row_kind (row_kind),
  KEY idx_flow_type (flow_type),
  KEY idx_org (from_org, to_org)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·科技人才流动（仅机构级聚合计数，U6：无姓名/头像/证件/个人ID/scholar_id 任何个人明细列，序182）';
```

**U6 表结构级落实**：全表**无任何个人明细列**（无 name/avatar/证件/手机/scholar_id/person_id）；record 行只存 from/to 机构、领域、flow_type、person_count（=1）、risk_level。契约 §3.5 `stats` 四数（net_inflow/warning_count/academic_to_industry/industry_to_academic）为**契约草案示例值，无种子、不灌**，由 Java 读表即时计算（warning_count=记录行 risk_level=warning 计数=2；方向计数按 flow_type 聚合）。

### 2.8 `ts_plan_direction_warning`（0 行，序 184；建表不灌）

```sql
CREATE TABLE ts_plan_direction_warning (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  warning_id    varchar(32) NOT NULL COMMENT '预警项 ID（契约 §3.1 warning_id，对齐种子 directionMonitorItems.id 形态）',
  name          varchar(64)  NOT NULL COMMENT '预警方向名',
  field         varchar(32)  NOT NULL COMMENT '技术领域（Query field 过滤）',
  warning_level varchar(8)   NOT NULL COMMENT 'high/medium/watch（契约 §2.4 逐字）',
  signal        varchar(64)  NOT NULL COMMENT '信号摘要（如「六源同步升温」）',
  summary       varchar(500) NOT NULL COMMENT '预警正文',
  sources       json         NOT NULL COMMENT '六源分 JSON {paper/patent/project/talent/industry/policy: {score,delta,note}}（契约 §3.1/§2.3 六源逐字；delta 字符串口径 U4）',
  updated_at    varchar(16)  NOT NULL COMMENT 'demo 字符串口径（2026-08-17 08:30 形态，U4）',
  metric_id     varchar(32)       DEFAULT NULL COMMENT 'M_INNOV_PLAN_DIRECTION_ALERT（模型注册后回填）',
  generated_by  varchar(64)       DEFAULT NULL COMMENT '模型写入方标注（未来 Python 模型写入时带出，禁人工行）',
  source        varchar(16)       DEFAULT NULL COMMENT '模型注册后由写入方填，非种子',
  created_at    datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_warning_id (warning_id),
  KEY idx_level (warning_level),
  KEY idx_field (field)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·潜在科技发展方向预警（V1 零行；模型未注册走 501，禁灌假预警，序184）';
```

**V1 零行**：灌数脚本不含本表任何 INSERT/TRUNCATE；种子 `directionMonitorItems`（5 条）**不迁移**（那是假预警）。六源均分 `source_averages` 为服务端语义，前端不自算；未注册期接口 501 空态信封（ARCH §4.7）。

---

## 3. 行源映射与行数清单（mock 实测）

> 全部行数以 `lumen-ui-science-pc/src/mock/modules/techDevelopmentPlan.ts`（标注 L 行号为该文件）与 `demo-ui-science/src/techDevelopmentPlan.js`（标注 demo L）**实测数出**，非估算。

| 表 | 种子数组（源位置） | 展开规则 | 行数 |
|---|---|---|---|
| `ts_plan_hot_tech` | `hotTechData`（mock L153–162） | 1 技术 1 行 | **8** |
| `ts_plan_hot_tech_series` | `technologyTrendSeriesByRange`（mock L176–216） | 8 技术 ×（3m 3 期 + 6m 4 期 + 12m 9 期）= 24+32+72 | **128** |
| `ts_plan_metric_system` | `multidimensionalIndicatorCategories`（mock L226–306） | 7 分类：technology 6 卡 + industry/institution/project/achievement/statistics/talent 各 4 卡 = 30 卡 | **30** |
| `ts_plan_tracking_event` | `techDevelopmentPlanTimeline`（demo L30–44） | events 7 条（2020-05…2026-04，逐年 1 条）+ meta 1 行 | **8** |
| `ts_plan_tracking_point` | `planRecords`（demo L46–173，7 条）× `regionCoordinates`（demo L175–183，7 城）× `layerKeys` 5 层 | 7 点 × 5 result_type | **35** |
| `ts_plan_local_adv` | `localAdvantageChart`（mock L549–553）6 项 + `localAdvantageInnovation`（L556–560）6 项 + `localAdvantageOutput`（L563–567）6 项 | 三维度各 6 对比项 + reference 1 行（契约示例值 72/1240/215.4 逐字，**S-3 已裁定灌入**，§0.4） | **19** |
| `ts_plan_talent_flow` | `talentDirectionNodes`（mock L326–333）6 节点（stats 行；同组原样写入 stats 行 `od_nodes` JSON，v2 item 2，**不增行**）+ `talentInstitutionFlowRows`（L318–324）5 行（机构净流入）+ `talentFlowData`（L310–316）5 行（record，机构级聚合、person_count=1、姓名/头像丢弃） | 6+5+5 | **16** |
| `ts_plan_direction_warning` | —（种子 `directionMonitorItems` 5 条**禁灌**） | 建表零行 | **0** |
| `sys_user_planning_push_record` | —（订阅产物，非种子；真实推送产生，A3 裁定） | 初始零行 | **0** |
| **合计** | | | **244**（订阅产物表 0 行不计入） |

**配套静态枚举（不落行，接口字典/Java 常量由 OV-API 分册定载体）**：`directionMonitorSources` 6 源、`directionWarningMeta` 3 级、`technologyTrendColors` 5 色、legend `resultTypes` 5 类。**写死值替换**：人才 OD 总量 18932（深圳，↑21.7%）/12458（外地，↑16.2%）由 `ts_plan_talent_flow` stats 行提供（G-B4），FE/api 拼装层删写死改读表。

**种子存在但明确不灌的数组**（防误灌清单）：`directionMonitorItems`（5，假预警）；`planningResourcePackages`（5，订阅资源池走既有 ADS 真源，不建演示资源行；推送产物落 `sys_user_planning_push_record`，其种子类型五类→四类映射见 §5 F6）；`carrierLocations`（22）/`industryClusters`（3）/`carrierTypes`（6）/`districtCarrierBaselines`（6）/`landUseData`（6）/`keyArea*`（3+5+5+5）/`companies`（6）/`overlapMatrix`（6）/`overlapRuleProfiles`（3）/`research*`（4+3+4+14）/`regionalPlanningInsightRows`（4）——属 09b/09c 的 KEY/RES 组分册，不在 OV 范围。

---

## 4. 灌数方案（Python 一次性脚本规格）

脚本实现属**后续 data-agent 执行单**（TS-L2-DS09 组实现阶段建单），本节只冻结规格：

1. **幂等**：按表 `TRUNCATE + INSERT`，单表单事务，可重跑；`ts_plan_direction_warning` **不在灌数范围**（脚本无该表任何语句，禁灌假预警）。
2. **输入 = 种子提取**，建议方式（二选一，执行单定）：
   - **脚本解析（推荐）**：在 `lumen-ui-science-pc` 仓内用 node（vite-node/esbuild 加载 TS 模块）`import` mock 模块后 dump JSON；时间轴/点位两块从 `demo-ui-science` 仓 `techDevelopmentPlan.js` 同法提取（timeline / planRecords / regionCoordinates 投影）。优点：逐字零转录错漏。
   - 手工转 JSON：导出为种子 JSON 入脚本目录，需与源文件 diff 校验后使用。
3. **转换规则**（脚本内显式实现）：`trend→hot_trend` 直存；`flowType`（academia-to-industry/industry-to-academia）→ `flow_type`（学术→产业/产业→学术）；`netInflow`（'+1,248'）→ `net_inflow`（1248）；OD 节点标签（'深圳\|18,932人\|↑21.7%'）→ 拆 region/person_count/trend_pct，同时 `talentDirectionNodes` 原组逐字写入 stats 行 `od_nodes` JSON（不拆）；`talentFlowData` 的 `name/avatar` **在提取阶段即丢弃**（不进任何中间文件）；`position=[lat,lng]` → 拆 `lat`/`lng` 两列；`rendered_note` 整句逐字写入（行源=契约 §3.2 caliber_note 原文，M0 定稿后随 U5 翻换）；`metric_ids`/`metric_id` 列随行写入（值=赋号草稿 M_INNOV_PLAN_*，见各表 DDL 注释）。
4. **验收**：逐表 `SELECT COUNT(*)` 对 §3 清单（8/128/30/8/35/19/16/0）+ 抽样断言（tech_id=1 heat=98、growth=45.2；12m 区间 tech 8 末期 heat=76；metric 30 卡含「热度指数=98」；talent od_shenzhen person_count=18932 且 `od_nodes` 六节点齐；point（tdp-global-robot, hotspot）score=94；hot_tech 各行 `rendered_note` 含「口径待 M0 定稿」）；失败即回滚整批。
5. **dry-run**：脚本带 `--dry-run`，只输出各表待写行数不落库。
6. **不做**：不做任何统计派生（无第二套统计脚本）；不写 ODS/DWD/供应方库；不动 demo/lumen 两仓源码（只读事实源）。

---

## 5. 订阅面确认（序 183，零 DDL）

读 `gkxlumen-display` subscription 包与用户行为表，结论：**app_user 订阅家族无 DDL 变更即可承载 `planning_resource`**；另按 **A3 会签裁定（v2）** 新增订阅产物表 `sys_user_planning_push_record`（见下 DDL）。

| 证据 | 文件 | 结论 |
|---|---|---|
| 适配器接口按 `scope_type` 字符串分派 | `display/subscription/SubscriptionAdapter.java`（`scopeType()` + `evaluate(rule)`） | 新增 `PlanningResourceSubscriptionAdapter` Bean 即挂入，无枚举白名单 |
| 注册表为 `Map<String, SubscriptionAdapter>` | `display/subscription/SubscriptionAdapterRegistry.java` | 无值域校验，新 scopeType 零改动注册 |
| 规则表 `scope_type varchar(32)` 自由枚举（现值 region/city/domain/carrier/order/keyword） | `gkxlumen-upms-api/.../entity/SysUserSubscriptionRule.java` + `db/9x_gkxlumenx_user_behavior.sql` L90 | `'planning_resource'`（17 字符）fits，**无需列变更**；ARCH 的「rule_type」为术语笔误，实际列名 `scope_type`（§0.3） |
| 订阅对象表 `target_type` 枚举已含 `resource` | `sys_user_relation` DDL L25 | 资源对象收藏/关注直接可用 |
| 推送记录 `biz_type` 自由（alert/push/update） | `sys_user_notification` DDL L120 | 资源推送记录走 `biz_type='push'`，已读 `read_flag` 复用 M4 §3.4 模式 |
| 规则读写接口透传 scopeType 查询参数 | `display/controller/UserBehaviorController.java`（`GET /v1/user-behavior/rules`） | 无值域拦截 |
| 推送调度已交付 | `display/job/SubscriptionPushJob.java`（XXL-Job）+ 4 适配器（region/city/domain/carrier） | 新适配器进既有扫描，不新增调度面 |

**A3 会签裁定（v2）：新增订阅产物表 `sys_user_planning_push_record`**——属**订阅面真实现产物**（ARCH §4.6 真读+真写面；由 `PlanningResourceSubscriptionAdapter` 命中推送时写入），**非 D18 表**（不落 `ts_plan_`/ADS、不属 demo 种子）、**非 gapfill**。库 = `gkxlumenx`（upms 主库，对齐 `db/9x_gkxlumenx_user_behavior.sql` 用户行为家族）。**初始 0 行**（真实推送产生，无灌数）：

```sql
CREATE TABLE sys_user_planning_push_record (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  tenant_id     bigint unsigned NOT NULL DEFAULT 0 COMMENT '租户ID（统一用户中心下发，对齐 sys_user_relation）',
  user_id       bigint unsigned NOT NULL DEFAULT 0 COMMENT '用户ID（统一用户中心 SSO userId，非 sys_user.user_id，同 9x 惯例）',
  resource_type varchar(16)  NOT NULL COMMENT 'report/project/policy/carrier（四类资源池，ARCH §4.6；值域见 F6 映射）',
  resource_id   varchar(128) NOT NULL COMMENT '资源对象ID（字符串兼容混杂 ID 形态，对齐 sys_user_relation.target_id 惯例）',
  title         varchar(255) NOT NULL COMMENT '资源标题快照（列表直显，避免回表）',
  field         varchar(64)  DEFAULT NULL COMMENT '命中领域（订阅规则领域）',
  reason        varchar(255) DEFAULT NULL COMMENT '推送理由（适配器产出文案）',
  pushed_at     datetime     NOT NULL COMMENT '推送时间（契约 §3.6 pushed_at）',
  is_read       char(1)      NOT NULL DEFAULT '0' COMMENT '0未读 1已读（复用 M4 §3.4 已读模式，按用户隔离；映射契约 is_read 布尔）',
  create_time   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (id),
  KEY idx_user_read (tenant_id, user_id, is_read, pushed_at) COMMENT '过滤分页：按用户+已读+推送时间',
  KEY idx_user_type (user_id, resource_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·科创资源推送产物记录（订阅面真实现产物，A3 裁定；初始零行，非 D18 表非 gapfill）';
```

**F6 注记（v2）：种子资源类型中文五类 → 契约四类枚举映射**（行源 = mock `planningResourcePackages.type` 五类，含「核心人才」；同时约束适配器产出与 API 分册 `resource_type` 值域）：

| 种子 type（中文五类） | 种子 id | `resource_type` 四类枚举 | 说明 |
|---|---|---|---|
| 政策文件 | policy | `policy` | 1:1 |
| 科研项目 | project | `project` | 1:1 |
| 行业报告 | report | `report` | 1:1 |
| 企业载体 | carrier | `carrier` | 1:1 |
| 核心人才 | talent | **—（无对应，不映射）** | 不在四类资源池（ARCH §4.6）；人才推荐走既有人才能力，是否入池待 M0/产品定——未定前适配器**不得**产出 talent 型记录 |

**审批项（单列，不擅自改）**：契约 §3.6 `subscriptions` 为结构化对象 `{resource_types[], fields[], frequency}`；若会签要求其独立成列（如 `resource_types` JSON 列），才需对 `sys_user_subscription_rule` 加列——本分册裁定 V1 以 `scope_value`/`keywords`/`push_frequency` 既有列承载（领域多选入 `keywords` 逗号分隔或 `scope_value` JSON 字符串），**不加列**；如 OV-API 分册裁定必须结构化列，提审批单走三方评审（规约铁律 7）。

---

## 6. 合规自检

| 项 | 自检 | 结论 |
|---|---|---|
| **D18 三要素** | 8 张 ts_plan 表逐表有「表名/灌数方/读取接口」（§1 总表 = ARCH §6 对齐）；灌数=Python 一次性脚本；Java `gkxlumen-display` 9 端点只读 ADS；接口不直返 mock/常量（caliber_note=`rendered_note` 物理行源、OD 总量 18932/12458、指标卡值、时间轴、点位全部表行携带）；`sys_user_planning_push_record` 属订阅面写产物，不在 D18 清单（A3） | ✅ |
| **D18 库边界** | 不进 ODS/DWD/供应方 `gkx` 库；不带 `gapfill_` 前缀；`gkxlumenx_ads` 展示 ADS | ✅ |
| **U6 个人信息** | `ts_plan_talent_flow` 全表无姓名/头像/证件/个人 ID/scholar_id 列（§2.7 列清单）；种子 name/avatar 提取阶段丢弃；只机构级聚合 + person_count | ✅（法务最终边界仍待 U6 裁定，表结构已按最严口径） |
| **不写第二套统计脚本** | 唯一脚本只搬运种子（§4）；stats 类数字（warning_count、方向计数、六源均分）由 Java 读表即时计算，无离线统计作业 | ✅ |
| **字段沿用种子/契约命名** | 列名对齐契约 §3.x（tech_id/hot_trend/flow_type/warning_level…）；值逐字保留 demo 口径（含千分位/单位字符串/日期字符串）；不擅自数值化（U4 族待 M0） | ✅ |
| **禁假数据** | direction_warning V1 零行；reference_stats 以 contract_draft_sample 显式标注；空间分布不造坐标、不预计算派生值 | ✅ |
| **范围** | 不改 task-registry、不 git 提交、不建表不灌数、不动 demo/lumen 源码；KEY/RES 组数组列入防误灌清单 | ✅ |
| **v2 会签裁定落实** | metric_id 三表补列（草稿标注）、od_nodes 列、rendered_note 列、S-3 裁定灌入、A3 产物表、F6 映射、列名基准声明——逐条对应见 §9；行数合计复核 244+0 不变 | ✅ |

---

## 7. 会签讨论点（v2：S-3/A3/F6 已裁定，其余按建议收口）

> v2 状态：architect / api / algorithm 三家会签同意并回必改项（已并入，见 §9）；S-1/S-2/S-4/S-5/S-6 三家未提异议，按本分册建议收口，data 签收时终确认。

| # | 点 | 状态与处置 |
|---|---|---|
| S-1 | 序列粒度：种子季度 × 三区间（128 行）vs 契约示例按年（heat_series.year） | **收口**：季度逐字存储（`period_label`），`year` 由 API 拼装层映射；契约批 4 冻结时把 §3.2 heat_series 示例改季度或加 `period` 字段 |
| S-2 | 本地优势维度键：契约键 field/capability/output vs FE 种子图名 chart/innovation/output | **收口**：契约三键（capability←innovation 映射写进灌数转换），`source='lumen_seed'` 已标 |
| S-3 | reference_stats 无 demo 种子，灌契约草案示例值（72/1240/215.4） | **已裁定（architect，v2）**：灌入，`source='contract_draft_sample'`（需规 181 要求对比展示，整块空态反缺位）；「示例抽样」保留至正式态换真源 |
| S-4 | talent `flow_type` 只存两个方向值，「预警流动」作 risk_level 筛选（契约 §3.5 边界原文）vs ARCH §4.5「三枚举」表述 | **收口**：不存「预警流动」（存了会造出非流向语义的脏行）；ARCH 表述按 §0.3 同类事实澄清处理 |
| S-5 | tracking_point 35 行 = 7 点×5 层全挂（demo buildMapRegions 逐字）vs 只挂热点层 7 行 | **收口**：35 行全挂（demo 逐字）；KEY 组（22 载体）若需复用点位表另建其分册表 |
| S-6 | 订阅结构化字段是否给 `sys_user_subscription_rule` 加列（§5 审批项） | **收口（V1）**：不加列，用既有列承载；OV-API 分册如需结构化再走审批（A3 产物表不涉规则表） |

---

## 8. 会签与签收路径

本分册随 ARCH 稿四角色会签（意见落 `sdd/l2/会签/综合发展规划-会签.md`）→ 签收后与 OV-API / OV-METRIC 并行成稿 → 拆 Java 实现（含建 DDL）/ 灌数（本分册 §4 规格转执行单）/ 接线 / 主路径测试四行实现单。

---

## 9. 会签修订记录 v2（2026-11-06，architect / api / algorithm 三家意见并入）

| # | 会签来源 | 变更 | 落点 |
|---|---|---|---|
| 1 | algorithm ② | 三表补指标列（值=赋号草稿 M_INNOV_PLAN_*，列注释标「未签草稿」）：`ts_plan_hot_tech.metric_ids`（**取一列 JSON** 载 HEAT/GROWTH 两条——对齐契约 §3.2 响应 metric_ids 数组形态；heat 列挂 HEAT、growth 列挂 GROWTH，字段级映射 OV-API 定）、`ts_plan_local_adv.metric_id`（PLAN_LOCAL_ADV）、`ts_plan_talent_flow.metric_id`（PLAN_TALENT_FLOW） | §2.1 / §2.6 / §2.7 |
| 2 | 会签必改 | `ts_plan_talent_flow.od_nodes` JSON 列：FE 人才流向图六节点（节点名/色值/OD 总量 18932/12458 内嵌标签）逐字，行源=种子 `talentDirectionNodes`，冗余存 6 条 stats 行，供 API 分册 od_nodes 字段消费 | §2.7 / §3 / §4 |
| 3 | algorithm ③ | `ts_plan_hot_tech.rendered_note` 整句列（U5 文案物理行源）：值=「热度 = 论文 40% / 专利 30% / 项目 20% / 资讯 10%（口径待 M0 定稿，U5）」逐字，禁止 Java 拼文案；M0 定稿后随 U5 翻换 | §2.1 / §4 |
| 4 | architect（S-3 裁定） | `ts_plan_local_adv` reference 行灌契约示例值（hotspots 72 / carriers 1240 / capacity 215.4），`source='contract_draft_sample'`（需规 181 要求对比展示，整块空态反缺位）；「示例抽样」保留；行数不变（19） | §0.4 / §3 |
| 5 | A3 裁定 | 新增订阅产物表 DDL `sys_user_planning_push_record`（gkxlumenx upms 主库；列：id/tenant_id/user_id/resource_type/resource_id/title/field/reason/pushed_at/is_read + 过滤分页索引 idx_user_read / idx_user_type）；声明属订阅面真实现产物（**非 D18 表、非 gapfill**）；初始 0 行（真实推送产生）；§1 总表与 §3 行数清单相应更新 | §1 / §3 / §5 |
| 6 | F6 注记 | 种子资源类型中文五类（政策文件/科研项目/行业报告/核心人才/企业载体，含核心人才）→ 契约 `resource_type` 四类枚举（report/project/policy/carrier）灌数/产出映射表；核心人才不映射、待 M0/产品定 | §5 |
| 7 | 基准声明 | 全组列名以本分册 DDL 为准：metric_system 用 `metric_change`；序列用 `period_label`；热度序列列用 `heat_value`（hot_tech 主表为 `heat`）；caliber 用 `caliber_def` + `rendered_note` | §1 |
| 8 | — | 本记录小节；行数合计复核：**种子 244 行不变**（8/128/30/8/35/19/16/0）+ `sys_user_planning_push_record` 初始 0 行；`ts_plan_direction_warning` 仍 0、禁灌不变 | §9 |

