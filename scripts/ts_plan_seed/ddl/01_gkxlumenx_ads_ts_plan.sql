-- =====================================================================
-- TS-L2-DS09-SEED-L01 · 科技发展规划（DS-09）28 张 ts_plan_* 表 DDL
-- 目标库：gkxlumenx_ads（utf8mb4 / utf8mb4_general_ci，InnoDB）
-- 冻结真源（列定义逐字）：
--   OV  8 表：sdd/l2/TS-L2-DS09-OV-DATA.md  §2.1–§2.8（244 行种子）
--   KEY 9 表：sdd/l2/TS-L2-DS09-KEY-DATA.md §2.1–§2.9（61 行种子）
--   RES 11 表：sdd/l2/TS-L2-DS09-RES-DATA.md §2（70 行种子；引擎/字符集沿 OV/KEY 约定补齐）
-- D18：不进 ODS/DWD/供应方 gkx 库；不带 gapfill_ 前缀；Java 只读 ADS。
-- ts_plan_direction_warning（§OV 2.8）建表不灌：V1 零行，禁灌假预警。
-- =====================================================================

-- ---------------------------------------------------------------------
-- OV 组（综合发展规划，序 178–184）8 表 244 行
-- ---------------------------------------------------------------------

-- OV §2.1 全球热点技术（8 行，序 178）
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
  spatial_distribution json  NOT NULL COMMENT '空间分布因子数组 [{"name":"南山区","factor":1.08}×5]（种子 technologyTrendSpaceRegions 逐字，无坐标；派生=heat×factor 由 FE 做）',
  caliber_def   json         NOT NULL COMMENT '热度口径三要素 {scoreFormula,inclusionRules,defaultRule}（种子 technologyHeatTrendDefinition 逐字；口径构成由表行携带，非 Java 硬编码）',
  rendered_note varchar(255) NOT NULL COMMENT 'U5 口径整句：「热度 = 论文 40% / 专利 30% / 项目 20% / 资讯 10%（口径待 M0 定稿，U5）」逐字（行源=契约 §3.2 caliber_note 原文；M0 定稿后随 U5 翻换）——响应 caliber_note 取本列，禁止 Java 拼文案',
  metric_ids    json         NOT NULL COMMENT '赋号草稿·未签：["M_INNOV_PLAN_HEAT","M_INNOV_PLAN_GROWTH"]；heat 列挂 HEAT、growth 列挂 GROWTH，字段级映射 OV-API 定。取一列 JSON 对齐契约 §3.2 响应 metric_ids 数组形态',
  source        varchar(16)  NOT NULL DEFAULT 'demo_seed',
  created_at    datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_tech_id (tech_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·全球热点技术（D18 读表，序178）';

-- OV §2.2 热点技术热度序列（128 行 = 8 技术 × (3m 3 期 + 6m 4 期 + 12m 9 期)，序 178）
CREATE TABLE ts_plan_hot_tech_series (
  id           bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  tech_id      varchar(16) NOT NULL COMMENT '逻辑引用 ts_plan_hot_tech.tech_id（无物理 FK）',
  range_key    varchar(4)  NOT NULL COMMENT '3m/6m/12m（契约 §2.8；种子 technologyTrendSeriesByRange 键）',
  period_label varchar(8)  NOT NULL COMMENT '期标签，季度粒度逐字（2025Q4…2026Q2）🧪；契约 heat_series.year 由 API 拼装层映射',
  period_order smallint    NOT NULL COMMENT 'x 轴序（区间内 1..N）',
  heat_value   smallint unsigned NOT NULL COMMENT '热度值 🧪（种子 series[techId][i]）',
  source       varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at   datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_tech_range_order (tech_id, range_key, period_order),
  KEY idx_range (range_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·热点技术热度序列（技术×区间×期，序178）';

-- OV §2.3 多维度指标体系卡片（30 行，序 179，n/a_ops 运营壳）
CREATE TABLE ts_plan_metric_system (
  id             bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  category_key   varchar(32) NOT NULL COMMENT '分类键（种子 key：technology/industry/institution/project/achievement/statistics/talent，7 类）',
  category_label varchar(32) NOT NULL COMMENT '分类名（技术发展/产业数据库/机构库/课题库/成果库/统计库/人才库）',
  metric_label   varchar(32) NOT NULL COMMENT '指标卡名（热度指数/增长速度/文献数量…）',
  metric_value   varchar(32) NOT NULL COMMENT '指标值逐字字符串（12,580 / 186.7亿 / 18.3万），不数值化（demo 口径，数值化待 M0 同 U4 族）🧪',
  metric_unit    varchar(16)          DEFAULT NULL COMMENT '单位（从 value 机械拆分，可空）',
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

-- OV §2.4 动态跟踪时间轴（8 行 = 1 meta + 7 事件，序 180；行源=demo.js）
CREATE TABLE ts_plan_tracking_event (
  id          bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  row_kind    varchar(16) NOT NULL COMMENT 'timeline_meta（1 行）/ event（7 行）；分册草案 varchar(8) 装不下自身取值 timeline_meta(13)，勘误放宽为 16',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·动态跟踪研判演进时间轴（序180；行源=demo.js）';

-- OV §2.5 动态跟踪空间点位（35 行 = 7 点 × 5 层，序 180）
CREATE TABLE ts_plan_tracking_point (
  id          bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  result_type varchar(16) NOT NULL COMMENT 'hotspot/space/talent/report/warning（契约 §2.2 = demo.js techDevelopmentPlanLegend.resultTypes 5 类逐字）',
  source_id   varchar(32) NOT NULL COMMENT '来源规划记录 ID（demo.js planRecords.id，tdp-*；记录本体不建表）',
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

-- OV §2.6 本地特色与优势对比（19 行 = 18 维度 + 1 reference，序 181）
CREATE TABLE ts_plan_local_adv (
  id              bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  row_kind        varchar(12) NOT NULL COMMENT 'dimension（18 行）/ reference（1 行）',
  dimension_key   varchar(16)          DEFAULT NULL COMMENT 'dimension 行：field/capability/output（契约 §3.4 三键逐字；映射 field←localAdvantageChart、capability←localAdvantageInnovation、output←localAdvantageOutput）',
  dimension_label varchar(16)          DEFAULT NULL COMMENT '领域/能力/产出',
  indicator_name  varchar(64)          DEFAULT NULL COMMENT '对比项（合成生物学…/顶尖人才密度…/高被引论文…，yAxis 逐字）',
  local_score     smallint unsigned    DEFAULT NULL COMMENT '深圳分 🧪（种子 local[]）',
  global_score    smallint unsigned    DEFAULT NULL COMMENT '全球平均 🧪（种子 globalAvg[]）',
  indicator_order smallint             DEFAULT NULL COMMENT '维度内顺序 1..6',
  base_region     varchar(16) NOT NULL DEFAULT '深圳' COMMENT '对比基准（图例「深圳」）',
  compare_to      varchar(16) NOT NULL DEFAULT '全球' COMMENT '对比对象（图例「全球平均」→契约 compare_to=全球）',
  metric_id       varchar(32) NOT NULL COMMENT 'M_INNOV_PLAN_LOCAL_ADV（赋号草稿·未签，MODEL，Q-MO-DS09-01）；表级指标，各行同值冗余',
  reference_json  json                 DEFAULT NULL COMMENT 'reference 行：{hotspots:72,carriers:1240,capacity:215.4,source:"全球公开数据库（示例抽样）"}（契约 §3.4 草案示例值逐字；「示例抽样」保留至正式态换真源）',
  source          varchar(32) NOT NULL COMMENT 'field 行=demo_seed；capability/output 行=lumen_seed（FE 补两维正式化）；reference 行=contract_draft_sample（21 字符，分册草案 varchar(16) 装不下，勘误放宽为 32）',
  created_at      datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_dim_order (row_kind, dimension_key, indicator_order),
  KEY idx_dimension (dimension_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·本地特色与优势对比（三维度 vs 全球 + 参照统计，序181）';

-- OV §2.7 科技人才流动（16 行 = 6 stats + 5 机构 + 5 record，序 182；U6 无个人明细）
CREATE TABLE ts_plan_talent_flow (
  id           bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  row_kind     varchar(16) NOT NULL COMMENT 'stats（6 行）/ institution_flow（5 行）/ record（5 行）',
  stat_key     varchar(32)          DEFAULT NULL COMMENT 'od_shenzhen/od_external/node_academia/node_industry/node_gov/node_other',
  label        varchar(64)          DEFAULT NULL COMMENT '节点/口径名逐字（学术界/产业界/政府/科研院所/其他；深圳/外地）',
  color        varchar(9)           DEFAULT NULL COMMENT '节点演示色（#1677ff 等，种子 itemStyle.color 逐字，演示态展示用）',
  region       varchar(16)          DEFAULT NULL COMMENT 'OD 行：深圳/外地',
  person_count int unsigned         DEFAULT NULL COMMENT 'OD 行总量 🧪：深圳=18932、外地=12458（G-B4：FE 写死值改由表行提供）；record 行恒 1',
  trend_pct    decimal(5,1)         DEFAULT NULL COMMENT 'OD 行增幅 % 🧪（21.7/16.2，种子 ↑x%）',
  od_nodes     json                 DEFAULT NULL COMMENT 'FE 人才流向图六节点逐字 JSON：[{name,itemStyle:{color}}×6]（OD 总量内嵌标签）；行源=种子 talentDirectionNodes 逐字不拆；冗余存于 6 条 stats 行',
  institution  varchar(128)         DEFAULT NULL COMMENT '机构名（华为技术有限公司…中山大学（深圳））',
  net_inflow   int                  DEFAULT NULL COMMENT '净流入（带符号整数：+1248/+987/+756/-328/-276；种子 netInflow 字符串去千分位）🧪',
  flow_direction varchar(4)         DEFAULT NULL COMMENT 'in/out（种子 trend up→in / down→out）',
  flow_id      varchar(16)          DEFAULT NULL COMMENT 'tf-{种子 id}（tf-1..tf-5）',
  from_org     varchar(128)         DEFAULT NULL COMMENT '流出机构（清华大学/腾讯科技/MIT…）——机构级，非个人',
  to_org       varchar(128)         DEFAULT NULL COMMENT '流入机构（华为技术/中科院/字节跳动…）',
  from_type    varchar(16)          DEFAULT NULL COMMENT 'university/enterprise/research（机构类型枚举，非个人属性）',
  to_type      varchar(16)          DEFAULT NULL COMMENT '同上',
  field        varchar(64)          DEFAULT NULL COMMENT '领域（具身智能/AI安全/多模态模型/知识图谱/机器人控制）',
  flow_type    varchar(16)          DEFAULT NULL COMMENT '学术→产业 / 产业→学术（契约 §2.6 逐字；种子 academia-to-industry/industry-to-academia 映射；「预警流动」= 筛选特例 risk_level=warning，不作存储值）',
  risk_level   varchar(8)           DEFAULT NULL COMMENT 'NULL / warning（种子 riskLevel；契约 §3.5 risk_level Query）',
  updated_at   varchar(16)          DEFAULT NULL COMMENT '种子 date 逐字（2026-03-20…；字符串口径同 U4，数值化待 M0）',
  metric_id    varchar(32)          DEFAULT NULL COMMENT 'M_INNOV_PLAN_TALENT_FLOW（赋号草稿·未签，MODEL，Q-MO-DS09-02 + U6 法务未决）；表级指标，行值冗余',
  source       varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at   datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_row_kind (row_kind),
  KEY idx_flow_type (flow_type),
  KEY idx_org (from_org, to_org)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='规划·科技人才流动（仅机构级聚合计数，U6：无姓名/头像/证件/个人ID/scholar_id 任何个人明细列，序182）';

-- OV §2.8 潜在科技发展方向预警（0 行，序 184；建表不灌，禁假预警）
CREATE TABLE ts_plan_direction_warning (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  warning_id    varchar(32) NOT NULL COMMENT '预警项 ID（契约 §3.1 warning_id，对齐种子 directionMonitorItems.id 形态）',
  name          varchar(64)  NOT NULL COMMENT '预警方向名',
  field         varchar(32)  NOT NULL COMMENT '技术领域（Query field 过滤）',
  warning_level varchar(8)   NOT NULL COMMENT 'high/medium/watch（契约 §2.4 逐字）',
  `signal`      varchar(64)  NOT NULL COMMENT '信号摘要（如「六源同步升温」）；signal 为 MySQL 保留字，列名必须反引号',
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

-- ---------------------------------------------------------------------
-- KEY 组（重点领域规划，序 185–190）9 表 61 行
-- ---------------------------------------------------------------------

-- KEY §2.1 产业集群（3 行，序 185/189）
CREATE TABLE ts_plan_key_area (
  id              bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  cluster_id      varchar(16) NOT NULL COMMENT '集群键，沿用 demo 键（ai 人工智能/bio 生物医药/energy 新能源；种子 industryClusters.key；契约示例 CL-FUT-05 形态系草案虚构已弃）',
  cluster_name    varchar(32) NOT NULL COMMENT '集群名（人工智能集群/生物医药集群/新能源集群，种子 label 逐字）',
  industry_category varchar(32) NOT NULL COMMENT '产业大门类（新一代信息技术/生命健康/先进制造，种子 industryCategory 逐字；189 公共筛选项数据源之一）',
  technology_field varchar(32) NOT NULL COMMENT '科技领域细分（人工智能/合成生物/机器人，种子 technologyField 逐字；189 领军主题承载列）',
  default_map_layer varchar(16) NOT NULL COMMENT '默认地图图层（产业热度/科技载体/土地效益，种子 mapLayer 逐字——3 集群默认值未用满图层全集，demo 事实；189 图层单选全集实为 4 值=科技载体/土地效益/资源缺口/产业热度，FE 本地常量 MAP_LAYER_OPTIONS），本列承载集群默认值',
  carrier_ids     json NOT NULL COMMENT '集群载体引用数组（种子 carrierIds 逐字：ai 6 / bio 4 / energy 5；元素=ts_plan_key_area_carrier.carrier_id，无物理 FK，灌数校验存在性）',
  metric_id       varchar(32) NOT NULL COMMENT 'M_INNOV_KEYD_SPATIAL（赋号草稿·未签·STAT·TEMP_DS09_KEYD_SPATIAL，核对记录 §赋号表；185 空间密度/集聚度 GIS+ADS 图层读数，差集 other_system）；表级指标，3 行同值冗余',
  sort_no         smallint NOT NULL COMMENT '集群顺序 1..3（种子数组序）',
  source          varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at      datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_cluster_id (cluster_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·产业集群（D18 读表，序185/189）';

-- KEY §2.2 科技载体点位与详情（22 行，序 185/188；land_benefit V1 全 NULL）
CREATE TABLE ts_plan_key_area_carrier (
  id          bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  carrier_id  varchar(16) NOT NULL COMMENT '载体键（L001..L005/C001..C004/P001..P006/I001..I004/A001..A003，种子 id 逐字；lab 5+center 4+park 6+incubator 4+accelerator 3=22）',
  name        varchar(64) NOT NULL COMMENT '载体名（鹏城实验室/深圳湾实验室/…，种子 name 逐字）',
  carrier_type varchar(16) NOT NULL COMMENT '类型键（lab/center/park/incubator/accelerator，种子 type；值域=ts_plan_key_area_carrier_type.type_key 除 all）',
  district    varchar(16) NOT NULL COMMENT '行政区（南山/福田/光明/龙岗/坪山/宝安 6 区，种子 district 逐字；覆盖差不补行）',
  lng         decimal(8,5) NOT NULL COMMENT '经度（种子 lng，113.835..114.358）',
  lat         decimal(8,5) NOT NULL COMMENT '纬度（种子 lat，22.527..22.79）',
  level       varchar(8)  NOT NULL COMMENT '层级（国家级/省级/市级/区级，种子 level 逐字；188 详情 + 189 领军主题承载列）',
  cluster_id  varchar(16)          DEFAULT NULL COMMENT '所属集群键（逻辑引用 ts_plan_key_area.cluster_id，无物理 FK）；22 行中 7 行未挂集群置 NULL（L001/L004/P003/P005/I003/I004/A002，诚实空不强行归簇），15 行挂 ai/bio/energy',
  land_benefit json                DEFAULT NULL COMMENT '土地效益 JSON {plot_ratio 容积率, output_per_mu 亩均产出}（U8-2 定名沿用契约）；V1 全 NULL——demo 种子无逐载体土地数据，禁编造数值；正式态 GIS 用地图层接入后回填',
  metric_id   varchar(32)          DEFAULT NULL COMMENT 'NULL——载体行本体属 188 other_system（GIS 落点+详情，非价值排名，无统计核）；185 叶 SPATIAL 读数挂 ts_plan_key_area 集群行，不在本表挂号',
  sort_no     smallint     NOT NULL COMMENT '种子数组序 1..22（lab→center→park→incubator→accelerator 分组序）',
  source      varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_carrier_id (carrier_id),
  KEY idx_cluster (cluster_id),
  KEY idx_type_district (carrier_type, district)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·科技载体点位与详情（GIS 落点，非价值排名，序185/188）';

-- KEY §2.3 载体类型图例与全市计数（6 行含 all 汇总行，序 188）
CREATE TABLE ts_plan_key_area_carrier_type (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  type_key      varchar(16) NOT NULL COMMENT '类型键（all/lab/center/park/incubator/accelerator，种子 key；all=图例汇总行「全部载体」非实体类型）',
  type_name     varchar(32) NOT NULL COMMENT '类型名（全部载体/重点实验室/工程中心/科技园区/孵化器/加速器，种子 name 逐字）',
  carrier_count int unsigned NOT NULL COMMENT '全市口径载体计数 🧪（2856/128/256/68/420/186，种子 count 逐字；与 22 点位、区基线合计 1146 三口径互不调和，禁对账禁派生）',
  color         varchar(9)  NOT NULL COMMENT '图例色（#2563eb 等，种子 color 逐字，演示态展示用）',
  sort_no       smallint    NOT NULL COMMENT '图例顺序 1..6（种子数组序，all=1）',
  metric_id     varchar(32)          DEFAULT NULL COMMENT 'NULL——188 other_system（GIS 载体点位+ADS 详情，无统计核；计数旁不显伪 8 件套）',
  source        varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_type_key (type_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·载体类型图例与全市计数（other_system 无 metric_id，序188）';

-- KEY §2.4 区县载体基线（6 行，序 188）
CREATE TABLE ts_plan_key_area_district_baseline (
  id             bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  district       varchar(16) NOT NULL COMMENT '行政区（南山/福田/龙岗/宝安/龙华/坪山，种子 district 逐字；含龙华无光明，覆盖差不补行）',
  total_carriers int unsigned NOT NULL COMMENT '区载体总量 🧪（276/242/208/174/140/106，种子 total 逐字；合计 1146 与 22/2856 互不调和）',
  leading_type   varchar(16) NOT NULL COMMENT '区主导载体类型（重点实验室/工程中心/科技园区/孵化器，种子 leadingType 中文名逐字；与 carrier_type.type_name 同名域，映射归 API）',
  metric_id      varchar(32)          DEFAULT NULL COMMENT 'NULL——188 other_system',
  sort_no        smallint    NOT NULL COMMENT '种子数组序 1..6（按总量降序）',
  source         varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at     datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_district (district)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·区县载体基线（other_system 无 metric_id，序188）';

-- KEY §2.5 竞争力指标卡（5 行，序 186）
CREATE TABLE ts_plan_key_area_competitiveness (
  id          bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  metric_key  varchar(16) NOT NULL COMMENT '指标卡键，沿用 demo 键（composite/innovation/industry/openness/potential，种子 key；契约无此块，键名沿 demo，映射归 KEY-API）',
  label       varchar(16) NOT NULL COMMENT '指标卡名（综合指数/创新能力/产业基础/开放协同/发展潜力，种子 label 逐字）',
  value       decimal(5,1) NOT NULL COMMENT '指标值 🧪（78.5/88/85/62/82，种子 value；与五维画像并存不合并）',
  change_pct  varchar(16) NOT NULL COMMENT '环比字符串逐字（12.3%/8.6%/6.2%/5.4%/10.1%，种子 change，无 + 前缀；U4 不数值化，待 M0）🧪',
  metric_id   varchar(32) NOT NULL COMMENT '行级挂号（赋号草稿·未签）：potential 行=M_INNOV_KEYD_POTENTIAL（MIXED·Q-MO-DS09-04），其余 4 行=M_INNOV_KEYD_COMPETITIVENESS（MIXED·Q-MO-DS09-04）；禁改挂 M_SYNTH_VIT_*/GBA/CITY 186 号/企业 141/M_CHAIN_*',
  sort_no     smallint    NOT NULL COMMENT '卡片顺序 1..5（种子数组序，composite 首位）',
  source      varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_metric_key (metric_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·竞争力指标卡（D18 读表，序186）';

-- KEY §2.6 竞争力五维画像（5 行，序 186；dim_key 为 U8-1 新定英文键）
CREATE TABLE ts_plan_key_area_dimension (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  dim_key       varchar(32) NOT NULL COMMENT '五维英文键（U8-1 建议新定，种子无）：innovation_resources/research_output/industry_competitiveness/talent_support/open_collaboration；契约示例「技术/产业/空间/人才/政策」系草案虚构已弃；M0+数据侧拍板后冻结',
  dim_label     varchar(16) NOT NULL COMMENT '五维中文名（创新资源/科研产出/产业竞争力/人才支撑/开放协同，种子 keyAreaDimensionScores.label 逐字；FE-TS-09A 已冻结，demo 中文文案即页面既显内容）',
  score         smallint unsigned NOT NULL COMMENT '维度得分 🧪（92/88/85/78/72，种子 percent 逐字；权重未签 Q-MO-DS09-04，不展开公式）',
  metric_id     varchar(32) NOT NULL COMMENT 'M_INNOV_KEYD_COMPETITIVENESS（赋号草稿·未签·MIXED·Q-MO-DS09-04）；表级指标，5 行同值冗余',
  rendered_note varchar(255) NOT NULL COMMENT '页级口径整句（响应 caliber_note 物理行源，禁 Java 拼文案，沿 OV hot_tech.rendered_note 先例）：文案由 KEY-DATA 分册种子行定稿、KEY-API 只定携带机制；定稿句=「本页竞争力五维得分与指标值为演示数据，五维构成与评估权重口径待定稿后更新」——用户可读、零内部编号；正式口径定稿后随种子行版本翻换；5 行同值冗余',
  dim_order     smallint    NOT NULL COMMENT '维序 1..5（种子数组序）',
  source        varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_dim_key (dim_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·竞争力五维画像（D18 读表，序186；dim_key 为 U8-1 新定英文键）';

-- KEY §2.7 竞争力区域对标（5 行，序 186）
CREATE TABLE ts_plan_key_area_benchmark (
  id        bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  region    varchar(32) NOT NULL COMMENT '对标区域（南山区/深圳湾合作区/广州天河区/香港科技园/珠海横琴新区，种子 region 逐字；首行为本市基线行，其余为对标行——语义由 rank 隐含，不拆表）',
  score     decimal(4,1) NOT NULL COMMENT '对标分 🧪（78.5/74.2/71.3/69.1/66.8，种子 score 逐字）',
  rank_no   smallint unsigned NOT NULL COMMENT '名次 1..5（种子 rank 逐字；南山 78.5 与竞争力综合指数 78.5 同源同值，demo 口径不复算）',
  metric_id varchar(32) NOT NULL COMMENT 'M_INNOV_KEYD_COMPETITIVENESS（赋号草稿·未签·MIXED·Q-MO-DS09-04）；表级指标，5 行同值冗余',
  source    varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_rank_no (rank_no),
  KEY idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·竞争力区域对标（D18 读表，序186）';

-- KEY §2.8 土地用途与效益（6 行，序 187；land_benefit V1 全 NULL）
CREATE TABLE ts_plan_key_area_land (
  id           bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  district     varchar(16) NOT NULL COMMENT '行政区（南山×2/福田/龙岗/宝安/龙华，种子 area 逐字；无坪山/光明行，demo 覆盖差不补行）',
  land_type    varchar(16) NOT NULL COMMENT '土地用途（研发用地/产业用地，种子 type 逐字）',
  area_sqm     int unsigned NOT NULL COMMENT '用地面积 ㎡ 🧪（125000/98000/87000/156000/72000/113000，种子 area_sqm 逐字）',
  efficiency   smallint unsigned NOT NULL COMMENT '利用效率分 0-100 🧪（92/85/78/65/58/62，种子 efficiency 逐字；权重/公式未签不展开）',
  status       varchar(8)  NOT NULL COMMENT '效率状态（good/medium/poor，种子 status 英文枚举逐字不翻译；中文标签映射归 FE/API）',
  land_benefit json                 DEFAULT NULL COMMENT '区级土地效益预留 JSON（U8-2 定名 plot_ratio/output_per_mu）；V1 全 NULL——区级读数由本表标量列（area_sqm/efficiency/status）承载，本列正式态 GIS 图层接入后回填',
  metric_id    varchar(32) NOT NULL COMMENT 'M_INNOV_KEYD_LAND（赋号草稿·未签·STAT·TEMP_DS09_KEYD_LAND；GIS 用地/产出图层读数，差集 other_system）；表级指标，6 行同值冗余',
  sort_no      smallint    NOT NULL COMMENT '种子数组序 1..6',
  source       varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at   datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_district_type (district, land_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·土地用途与效益（区级，D18 读表，序187；亩均/容积率正式值待数据侧接入）';

-- KEY §2.9 资源配置优化方案（3 行，序 190；建议壳 n/a_ops）
CREATE TABLE ts_plan_key_area_plan (
  id              bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  plan_id         varchar(8)  NOT NULL COMMENT '方案键（a/b/c，种子 id；契约示例 PLAN-A 形态系草案虚构，沿 demo 键）',
  plan_name       varchar(16) NOT NULL COMMENT '方案名（方案A/方案B/方案C，种子 name 逐字；3 方案为产品定义，页级非集群级）',
  title           varchar(64) NOT NULL COMMENT '方案主题（提升创新策源能力/强化产业转化效率/优化空间协同布局，种子 title 逐字，非生成物）',
  priority        varchar(8)  NOT NULL COMMENT '优先级（高/高/中，种子 priority 中文逐字）',
  expected_effect varchar(16) NOT NULL COMMENT '预期效果字符串逐字（+18.6%/+22.9%/+15.2%，种子 expectedEffect 含 + 号；U4 不数值化）🧪；「方案模拟」Modal 效果预测值即本列 demo 逐字，无模拟端点无 501',
  resource_gap    varchar(16) NOT NULL COMMENT '资源缺口字符串逐字（-23.2%/-19.8%/-16.7%，种子 resourceGap 含 - 号）🧪',
  actions         json NOT NULL COMMENT '行动清单数组（["增强基础研究投入","引育高端科研人才","建设重大科研平台"] 等，种子 actions 逐字 3 项/方案）',
  primary_action  varchar(16) NOT NULL COMMENT '主操作文案（查看建议，种子 primaryAction 逐字）',
  secondary_action varchar(16) NOT NULL COMMENT '次操作文案（方案对比，种子 secondaryAction 逐字）',
  detail_action   varchar(16) NOT NULL COMMENT '详情操作文案（资源详情，种子 detailAction 逐字）',
  metric_id       varchar(32)          DEFAULT NULL COMMENT 'NULL——190 n/a_ops 建议壳（演示读数不挂 ID；禁 missing 模拟叶、禁借 501、禁改挂 186 附录建议/技术链 140）',
  sort_no         smallint    NOT NULL COMMENT '方案顺序 1..3（种子数组序）',
  source          varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at      datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_plan_id (plan_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·资源配置优化方案（建议壳，n/a_ops 无 metric_id，序190）';

-- ---------------------------------------------------------------------
-- RES 组（研究领域分析）11 表 70 行（引擎/字符集沿 OV/KEY 约定）
-- ---------------------------------------------------------------------

-- RES §2-1 领域字典（5 行；ResearchTab L53 常量表行化）
CREATE TABLE ts_plan_research_field (
  field_key    VARCHAR(32)  NOT NULL COMMENT '领域键（ai/quantum/synbio/ic/newenergy）',
  field_label  VARCHAR(64)  NOT NULL COMMENT '领域名（人工智能/量子科技/合成生物学/集成电路/新能源）',
  sort_no      INT          NOT NULL DEFAULT 0,
  metric_id    VARCHAR(64)  NULL COMMENT '无统计核，恒 NULL',
  updated_at   DATETIME     NOT NULL,
  PRIMARY KEY (field_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·领域字典（ResearchTab 常量表行化，D18 读表）';

-- RES §2-2 比对企业（7 行 = 目标 1 + 六企 6）
CREATE TABLE ts_plan_research_company (
  company_id  VARCHAR(16)  NOT NULL COMMENT 'C-TARGET / C-01..C-06',
  name        VARCHAR(128) NOT NULL,
  role        VARCHAR(16)  NOT NULL COMMENT 'target | compare',
  color       VARCHAR(16)  NULL COMMENT 'compare 行颜色；target NULL',
  level_tag   VARCHAR(8)   NULL COMMENT 'S/S/A/A/A/B；挂 M_INNOV_RES_CI_LEVEL 草稿',
  sort_no     INT          NOT NULL DEFAULT 0,
  metric_id   VARCHAR(64)  NULL COMMENT 'compare 行=M_INNOV_RES_CI_LEVEL（未签草稿）；target NULL',
  updated_at  DATETIME     NOT NULL,
  PRIMARY KEY (company_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·比对企业（目标主体+六企，D18 读表）';

-- RES §2-3 重叠度真值对（6 行；15 对中 9 对无真值不灌，诚实空）
CREATE TABLE ts_plan_research_overlap (
  pair_id        BIGINT      NOT NULL AUTO_INCREMENT,
  company_a      VARCHAR(128) NOT NULL COMMENT '对端 A（约定 target 或字典序在前）',
  company_b      VARCHAR(128) NOT NULL,
  overlap_score  DECIMAL(5,2) NOT NULL COMMENT '真值 45–72；15 对中 9 对无种子 → 不灌行、不造数（诚实空）',
  level          VARCHAR(8)   NOT NULL COMMENT 'high | medium',
  related_fields JSON        NULL COMMENT '相关领域数组',
  metric_id      VARCHAR(64)  NOT NULL DEFAULT 'M_INNOV_RES_OVERLAP' COMMENT '赋号草稿·未签',
  updated_at     DATETIME     NOT NULL,
  PRIMARY KEY (pair_id),
  UNIQUE KEY uk_pair (company_a, company_b)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·重叠度真值对（G-B4：FE 名称哈希兜底已废弃；本表只有种子真值对）';

-- RES §2-4 重叠规则三档（3 行；复算参数面逐字）
CREATE TABLE ts_plan_research_overlap_rule (
  rule_key         VARCHAR(16) NOT NULL COMMENT 'strict | balanced | wide',
  label            VARCHAR(32) NOT NULL COMMENT '严格规则/均衡规则/宽松规则',
  prompt           VARCHAR(255) NOT NULL,
  threshold_high   DECIMAL(5,2) NOT NULL COMMENT '75 / 70 / 65',
  threshold_medium DECIMAL(5,2) NOT NULL COMMENT '60 / 55 / 50',
  threshold_low    DECIMAL(5,2) NOT NULL COMMENT '59 / 54 / 49',
  rule_source      VARCHAR(255) NOT NULL,
  scope_text       VARCHAR(64)  NOT NULL,
  sort_no          INT NOT NULL DEFAULT 0,
  metric_id        VARCHAR(64) NULL,
  updated_at       DATETIME NOT NULL,
  PRIMARY KEY (rule_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·重叠规则三档（复算参数面逐字，D18 读表）';

-- RES §2-5 时间系数（3 行；筛选下拉+复算系数双职责）
CREATE TABLE ts_plan_research_time_factor (
  scope_key   VARCHAR(8)   NOT NULL COMMENT '1y | 3y | 5y',
  scope_label VARCHAR(16)  NOT NULL COMMENT '近1年/近3年/近5年',
  factor      DECIMAL(4,2) NOT NULL COMMENT '0.82 / 1.00 / 1.12',
  sort_no     INT NOT NULL DEFAULT 0,
  metric_id   VARCHAR(64) NULL,
  updated_at  DATETIME NOT NULL,
  PRIMARY KEY (scope_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·时间系数（筛选下拉+复算系数双职责，D18 读表）';

-- RES §2-6 四档等级（4 行；U3 标签逐字+阈值建议值 is_draft=1）
CREATE TABLE ts_plan_research_grade (
  grade_key     VARCHAR(16) NOT NULL COMMENT 'lead | advantage | catching | potential',
  grade_label   VARCHAR(16) NOT NULL COMMENT '领先级/优势级/追赶级/潜力级',
  description   VARCHAR(255) NOT NULL,
  threshold_low DECIMAL(5,2) NOT NULL COMMENT 'U3 建议值 80/65/45/0；draft 列标 true 待 M0 终冻',
  is_draft      TINYINT(1)  NOT NULL DEFAULT 1 COMMENT '1=建议值未拍板',
  patent        INT NOT NULL,
  papers        INT NOT NULL,
  top_papers    INT NOT NULL,
  score         DECIMAL(5,2) NOT NULL COMMENT '92 / 76 / 58 / 34',
  sort_no       INT NOT NULL DEFAULT 0,
  metric_id     VARCHAR(64) NOT NULL DEFAULT 'M_INNOV_RES_GRADE' COMMENT '赋号草稿·未签',
  updated_at    DATETIME NOT NULL,
  PRIMARY KEY (grade_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·四档等级（U3 阈值建议值 is_draft=1，D18 读表）';

-- RES §2-7 对标基准（3 行；gauge 兜底+196 合作机会拼接源）
CREATE TABLE ts_plan_research_overlap_benchmark (
  bench_id   BIGINT NOT NULL AUTO_INCREMENT,
  name       VARCHAR(128) NOT NULL COMMENT '华为技术有限公司82 / 腾讯科技（深圳）67 / 大疆创新科技 48',
  score      DECIMAL(5,2) NOT NULL,
  sort_no    INT NOT NULL DEFAULT 0,
  metric_id  VARCHAR(64) NOT NULL DEFAULT 'M_INNOV_RES_OVERLAP' COMMENT '采 METRIC 分册建议：基准值属重叠度口径（会签可裁）',
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (bench_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·对标基准（gauge 兜底+196 合作机会拼接源，D18 读表）';

-- RES §2-8 知识图谱节点（14 行；V1 演示骨架；专家类留位不灌）
CREATE TABLE ts_plan_research_graph_node (
  node_id        VARCHAR(16) NOT NULL COMMENT 'N-01..N-14',
  node_name      VARCHAR(128) NOT NULL,
  category_key   VARCHAR(16) NOT NULL COMMENT 'enterprise|institution|tech_field|literature|patent（demo「专家」名实不符，正式定名取实义；专家类留位不灌）',
  category_label VARCHAR(32) NOT NULL,
  symbol_size    INT NOT NULL,
  x              INT NOT NULL COMMENT 'layout none 静态坐标',
  y              INT NOT NULL,
  sort_no        INT NOT NULL DEFAULT 0,
  metric_id      VARCHAR(64) NULL COMMENT 'mapped 116 无独立核，恒 NULL',
  updated_at     DATETIME NOT NULL,
  PRIMARY KEY (node_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·知识图谱节点（V1 演示骨架；U9 超 100 节点/300 边走 M2；专家类 0 行）';

-- RES §2-9 知识图谱边（13 行；星型：中心=深圳先进技术研究院）
CREATE TABLE ts_plan_research_graph_edge (
  edge_id  BIGINT NOT NULL AUTO_INCREMENT,
  source   VARCHAR(16) NOT NULL COMMENT '节点 id（星型：中心=深圳先进技术研究院）',
  target   VARCHAR(16) NOT NULL,
  relation VARCHAR(32) NOT NULL DEFAULT '关联',
  sort_no  INT NOT NULL DEFAULT 0,
  metric_id VARCHAR(64) NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (edge_id),
  KEY idx_source (source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·知识图谱星型边（model L740 builder 逻辑落表，Java 不硬编码）';

-- RES §2-10 情报行（4 行；195 列表+196 派生源）
CREATE TABLE ts_plan_research_insight (
  row_id           BIGINT NOT NULL AUTO_INCREMENT,
  field            VARCHAR(64) NOT NULL COMMENT 'AI大模型/具身智能/计算机视觉/边缘智能',
  competition      VARCHAR(64) NOT NULL COMMENT '领先布局/潜力追赶/优势稳固/潜力追赶',
  priority         VARCHAR(8)  NOT NULL COMMENT '高/中/中/中',
  evidence         VARCHAR(512) NOT NULL,
  regional_insight VARCHAR(512) NOT NULL,
  action           VARCHAR(512) NOT NULL,
  plan_id          VARCHAR(8)  NULL COMMENT '196 映射（a/b/c/b，灌数固化 resolveStrategyPlan 逻辑）',
  sort_no          INT NOT NULL DEFAULT 0,
  metric_id        VARCHAR(64) NULL COMMENT 'other_system 读面，恒 NULL',
  updated_at       DATETIME NOT NULL,
  PRIMARY KEY (row_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·情报行（195 列表+196 派生源，D18 读表）';

-- RES §2-11 报告模板（8 行 = 报告 3+建议 3+系统 2；文案表行携带）
CREATE TABLE ts_plan_research_report_template (
  section_key   VARCHAR(32) NOT NULL COMMENT 'overlap_section/advantage_section/suggestion_section/tech_route/resource_config/cooperation + 系统行 page_caliber/graph_limit',
  section_label VARCHAR(64) NOT NULL,
  template_text TEXT NOT NULL COMMENT '含 {target}/{compare}/{field} 占位符；demo buildResearchIntelligenceReport L460-490 逐字',
  is_system     TINYINT(1) NOT NULL DEFAULT 0 COMMENT '1=系统行（page_caliber 整页口径 / graph_limit U9 阈值 100/300）',
  sort_no       INT NOT NULL DEFAULT 0,
  metric_id     VARCHAR(64) NULL,
  updated_at    DATETIME NOT NULL,
  PRIMARY KEY (section_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='研究领域·报告模板（文案表行携带，Java/Python 不硬编码；Word 产物归 M1 任务中心渲染）';
