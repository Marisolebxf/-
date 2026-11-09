# TS-L2-DS09-KEY-DATA · 重点领域规划 · 后台数据架构设计

> **任务**：`TS-L2-DS09-KEY-DATA`（definition，不建表、不灌数、不跑脚本）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 data-agent（沿 KEY-ARCH 授权链）
> **状态**：草案 v2（architect / api / algorithm 三家会签意见已并入，待 data 复核签收；修订清单见 §8）
> **硬依赖**：`sdd/l2/TS-L2-DS09-KEY-ARCH.md`（9 表清单与 D18 三要素见其 §0/§6；本分册 DDL 与其逐条对齐，事实澄清见 §0）
> **范围**：DS-09 重点领域规划页签（需规序 185–190，FE-TS-09b）9 张 `ts_plan_key_area_*` 表的库/DDL 冻结 + 行源实测清单 + 灌数方案规格

**行源真源（实测对象）**

| 用途 | 真源 |
|---|---|
| demo 冻结种子（主，9 数组全在） | `lumen-ui-science-pc/src/mock/modules/techDevelopmentPlan.ts`（下称 **mock**；KEY 组全部 9 数组均在 mock 内，**无需 demo.js 补源**——与 OV 组不同） |
| 硬依赖架构稿 | `sdd/l2/TS-L2-DS09-KEY-ARCH.md` §0（逐叶判定）/ §4（逐表列）/ §5（契约差异收口）/ §6（D18 总表）/ §7（U8 裁定建议 + 撞号禁令） |
| 契约草案（批 4 未冻结） | `agent-handoffs/科技发展态势-TS/API-TS-M9.md` §3.7 `key-areas`（示例嵌套结构/键名与 demo 不符处已由 ARCH §5 裁定弃用，见 §0.8） |
| 指标赋号与差集 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-09-科技发展规划-核对记录.md` §3.3 KEY-DOMAIN（四条 TEMP→`M_INNOV_KEYD_*` 赋号草稿·未签·pending `human:唐绍祖`）+ §赋号表 |
| 兄弟分册模板 | `sdd/l2/TS-L2-DS09-OV-DATA.md`（DDL 风格、灌数规格、验收断言写法保持一致） |

---

## 0. 对 ARCH 稿的事实核对与澄清（不改 D18 判定）

1. **行号与行数复核一致**：ARCH §3 引用的 9 数组行号（mock L347–L505）与行数经本分册逐数组实测核对无冲突——carrierTypes 6（L347–354）/ landUseData 6（L401–408）/ keyAreaScenarioPlans 3（L410–414）/ keyAreaCompetitivenessMetrics 5（L416–422）/ keyAreaDimensionScores 5（L424–430）/ keyAreaBenchmarkRows 5（L432–438）/ carrierLocations 22（L441–469）/ industryClusters 3（L471–496）/ districtCarrierBaselines 6（L498–505），合计 **61 行**。
2. **7 行未挂集群白名单（灌数校验用）**：3 集群 `carrierIds` 引用 ai 6（L003/C002/P001/P002/I001/A001）+ bio 4（L002/L005/P004/I002）+ energy 5（C001/C003/C004/P006/A003）= **15 行**；22−15=**7 行无归属**：`L001 / L004 / P003 / P005 / I003 / I004 / A002` → `cluster_id` 置 **NULL**（诚实空，不强行归簇；与 ARCH §5 收口第 1 行一致）。灌数脚本内置该 7 ID 白名单断言（§4）。
3. **`'all'` 是图例汇总行，非第 7 类实体**：`carrierTypes` 首行 `key='all'`（全部载体，count=2856）。保留为表行（FE 图例/类型筛选零改动，sort_no=1），列注释写明「全市口径 demo 计数 🧪，非实体类型」。
4. **三个计数口径互不调和（诚实声明，禁补算）**：22（地图点位 demo 逐行）/ 2856（类型图例全市口径）/ 1146（区基线 6 区合计 276+242+208+174+140+106）为 demo 各自冻结口径，**互不相等、不派生、不调和**；灌数与 Java 均不做任何对账/重算。
5. **行政区覆盖差（demo 事实，不补行）**：载体 22 行覆盖 6 区（南山 9/福田 4/光明 2/龙岗 3/坪山 1/宝安 3，**含光明区**）；区基线 6 区为南山/福田/龙岗/宝安/龙华/坪山（**含龙华、无光明**）；土地 6 行仅 5 区（南山×2/福田/龙岗/宝安/龙华，**无坪山/光明**）。三块覆盖差为种子冻结事实，**不补行、不调和**。
6. **`updated_at` 加列（对齐本组 ARCH）**：KEY-ARCH §6 要求「每表带 `metric_id` 列与 `updated_at`」；OV 组 8 表仅有 `created_at`。本分册 9 表统一加 `updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`（静态种子，值=灌数时间戳，不显式写值）。属两组 ARCH 口径差异，非笔误，随本组 ARCH 执行（会签点 K-5）。
7. **`land_benefit` 双预留（ARCH §4.3 + §5/§7.2）**：carrier 表（逐载体语义，契约 §3.7 示例所指）与 land 表（区级预留语义）各留一 JSON 可空列，**V1 双双全 NULL**——demo 冻结种子无任何逐载体/区级土地效益数值，**禁编造容积率/亩产**；187 叶读数由 `ts_plan_key_area_land` 区级行标量列（area_sqm/efficiency/status）承载，正式态接入 GIS 用地图层后回填真值（字段定名 U8-2：沿用契约 `plot_ratio`/`output_per_mu`）。
8. **契约 §3.7 示例无源项弃用清单（ARCH §5 已裁定，本分册按 demo 真源落列）**：① `cluster_id='CL-FUT-05'` 形态（demo 实为 ai/bio/energy）→ 沿 demo 键；② competitiveness/carriers/plans 嵌在 cluster 内 → 平铺 9 块；③ 五维「技术/产业/空间/人才/政策」（与 demo 两数组均不符，草案虚构）→ 弃用，以 demo 五中文名为准 + 新定英文键（U8-1）；④ carrier 内 `land_benefit` 示例值（plot_ratio 2.8 / output_per_mu 1200，demo 无源）→ 列保留 V1 全 NULL。契约示例字段名与本分册列名的映射归 KEY-API 分册改约（批 4 冻结时）。

---

## 1. 库与表总表

**库**：展示 ADS MySQL · **`gkxlumenx_ads`**（demo 环境对应 `demo_gkxlumenx_ads`）。理由：

1. KEY-ARCH §6 建议落展示 ADS（D18：ADS 是应用唯一读面，Java `gkxlumen-display` 只读，复用 OV 组 `PlanningController` 单 Controller 只加 `keyAreas()` 方法）；
2. `gkxlumenx_ads` 为既有展示 ADS 库，display/element 模块已有跨库只读先例，同库即复用只读账号与连接治理（沿 OV §1 理由 2）；
3. **D18 声明：9 张 `ts_plan_key_area_*` 表不进 ODS / DWD / 供应方 `gkx` 库**（供应方库只读不可写，且本组为展示种子非入站再加工）；**不带 `gapfill_` 前缀**（非 D16 缺项表，是 D18 读表正身）；
4. `ts_plan_key_area_` 前缀在库内唯一，不与 OV 组 `ts_plan_hot_tech` 等 8 表及既有 `ads_*` / `svc_*` 族冲突。

字符集 `utf8mb4` / `utf8mb4_general_ci`（对齐 `db/9x_*.sql` 既有惯例）。引擎 InnoDB。**建表 DDL 的执行归 Java 实现单**（`lumen-svc-platform` SQL 变更），本分册只冻结列定义。

**列名基准（沿 OV v2 item 7 同款声明）**：KEY 组全链（KEY-API / Java 实现 / FE 接线 / 灌数脚本）列名以本分册 DDL 为准——指标卡值列 = `value`、环比列 = `change_pct`（种子 change 逐字字符串，无 + 前缀）；五维得分列 = `score`（种子 percent）；对标列 = `rank_no`（种子 rank）；载体类型计数列 = `carrier_count`（种子 count，全市口径）；集群引用列 = `carrier_ids`（JSON）；方案效果列 = `expected_effect` / `resource_gap`（含符号字符串逐字，U4 不数值化）；载体层级列 = `level`（国家级/省级/市级/区级）；土地状态列 = `status`（good/medium/poor 英文枚举逐字，**不翻译**）；集群名列 = `cluster_name`（种子 label）。契约 §3.7 示例与本分册列名/结构差异（嵌套→平铺、cluster_id 形态、五维键、land_benefit）映射表落 KEY-API 分册。

| # | 表 | 行数（V1 实测种子） | 消费块（契约 §3.7 `key-areas` 平铺 9 块） | 服务叶（seq） | D18 灌数方 |
|---|---|---|---|---|---|
| 1 | `ts_plan_key_area` | 3 | clusters | 185 / 189 | Python 一次性脚本 |
| 2 | `ts_plan_key_area_carrier` | 22（7 行 cluster_id NULL） | carriers | 185 / 188 | 同上 |
| 3 | `ts_plan_key_area_carrier_type` | 6（含 all 图例行） | carrier_types | 188 | 同上 |
| 4 | `ts_plan_key_area_district_baseline` | 6 | district_baselines | 188 | 同上 |
| 5 | `ts_plan_key_area_competitiveness` | 5 | competitiveness_metrics | 186 | 同上 |
| 6 | `ts_plan_key_area_dimension` | 5 | dimension_scores | 186 | 同上 |
| 7 | `ts_plan_key_area_benchmark` | 5 | benchmark_rows | 186 | 同上 |
| 8 | `ts_plan_key_area_land` | 6 | land_use | 187 | 同上 |
| 9 | `ts_plan_key_area_plan` | 3 | plans | 190 | 同上 |

种子合计：3+22+6+6+5+5+5+6+3 = **61 行**（与 ARCH §6 一致）。189 无表无端点（交互壳，ARCH §4.5）；响应级 `carrier_total`（=22）与 `metric_ids` 数组由 Java 读表组装（carrier 计数 / metric_id 列去重），`caliber_note` 物理行源 = `ts_plan_key_area_dimension.rendered_note`（§2.6，禁 Java 拼文案；**文案由本分册种子行定稿，KEY-API 只定携带机制**——v2 item 1 会签裁定）。**种子表按 demo 冻结实测行数（61），非生成型 mock，不适用「≥1000 条/表」规（沿 OV 244 行先例）。**

---

## 2. 逐表 DDL 草案

> 约定（沿 OV §2）：`id bigint unsigned AUTO_INCREMENT` 主键；`source varchar(16) NOT NULL DEFAULT 'demo_seed'`（KEY 组 9 数组全部 demo 逐字，无 lumen_seed / contract_draft_sample 行）；`created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP`（灌数时间戳）+ `updated_at`（§0.6）为公共列，下文每表不重复注释。数值演示种子标 🧪（D4=mock，MockBadge 保留至翻转）。四条 metric 值均为**赋号草稿·未签**（核对记录 §赋号表，pending `human:唐绍祖`），列注释标明。

### 2.1 `ts_plan_key_area`（3 行，序 185/189）

```sql
CREATE TABLE ts_plan_key_area (
  id              bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  cluster_id      varchar(16) NOT NULL COMMENT '集群键，沿用 demo 键（ai 人工智能/bio 生物医药/energy 新能源；种子 industryClusters.key；契约示例 CL-FUT-05 形态系草案虚构已弃，§0.8）',
  cluster_name    varchar(32) NOT NULL COMMENT '集群名（人工智能集群/生物医药集群/新能源集群，种子 label 逐字）',
  industry_category varchar(32) NOT NULL COMMENT '产业大门类（新一代信息技术/生命健康/先进制造，种子 industryCategory 逐字；189 公共筛选项数据源之一）',
  technology_field varchar(32) NOT NULL COMMENT '科技领域细分（人工智能/合成生物/机器人，种子 technologyField 逐字；189 领军主题承载列，ARCH §4.5）',
  default_map_layer varchar(16) NOT NULL COMMENT '默认地图图层（产业热度/科技载体/土地效益，种子 mapLayer 逐字——3 集群默认值未用满图层全集，demo 事实；189 图层单选全集实为 4 值=科技载体/土地效益/资源缺口/产业热度，FE 本地常量 MAP_LAYER_OPTIONS，v2 item 3 勘误），本列承载集群默认值',
  carrier_ids     json NOT NULL COMMENT '集群载体引用数组（种子 carrierIds 逐字：ai 6 / bio 4 / energy 5；元素=ts_plan_key_area_carrier.carrier_id，无物理 FK，灌数校验存在性）',
  metric_id       varchar(32) NOT NULL COMMENT 'M_INNOV_KEYD_SPATIAL（赋号草稿·未签·STAT·TEMP_DS09_KEYD_SPATIAL，核对记录 §赋号表；185 空间密度/集聚度 GIS+ADS 图层读数，差集 other_system，禁 mapped 191 / M_ENT_AGGLOMERATION_INDEX）；表级指标，3 行同值冗余',
  sort_no         smallint NOT NULL COMMENT '集群顺序 1..3（种子数组序）',
  source          varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at      datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_cluster_id (cluster_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·产业集群（D18 读表，序185/189）';
```

### 2.2 `ts_plan_key_area_carrier`（22 行，序 185/188）

```sql
CREATE TABLE ts_plan_key_area_carrier (
  id          bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  carrier_id  varchar(16) NOT NULL COMMENT '载体键（L001..L005/C001..C004/P001..P006/I001..I004/A001..A003，种子 id 逐字；lab 5+center 4+park 6+incubator 4+accelerator 3=22）',
  name        varchar(64) NOT NULL COMMENT '载体名（鹏城实验室/深圳湾实验室/…，种子 name 逐字）',
  carrier_type varchar(16) NOT NULL COMMENT '类型键（lab/center/park/incubator/accelerator，种子 type；值域=ts_plan_key_area_carrier_type.type_key 除 all）',
  district    varchar(16) NOT NULL COMMENT '行政区（南山/福田/光明/龙岗/坪山/宝安 6 区，种子 district 逐字；覆盖差见 §0.5，不补行）',
  lng         decimal(8,5) NOT NULL COMMENT '经度（种子 lng，113.835..114.358）',
  lat         decimal(8,5) NOT NULL COMMENT '纬度（种子 lat，22.527..22.79）',
  level       varchar(8)  NOT NULL COMMENT '层级（国家级/省级/市级/区级，种子 level 逐字；188 详情 + 189 领军主题承载列）',
  cluster_id  varchar(16)          DEFAULT NULL COMMENT '所属集群键（逻辑引用 ts_plan_key_area.cluster_id，无物理 FK）；22 行中 7 行未挂集群置 NULL（L001/L004/P003/P005/I003/I004/A002，诚实空不强行归簇，§0.2），15 行挂 ai/bio/energy',
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
```

**187 读数路径说明（ARCH §4.3/§7.2 落实）**：本表 `land_benefit` 列 V1 全 NULL（demo 无源）；187 叶土地读数走 `ts_plan_key_area_land` 区级行（district/land_type/area_sqm/efficiency/status）承载，Java 不从本表拼土地效益。

### 2.3 `ts_plan_key_area_carrier_type`（6 行，序 188）

```sql
CREATE TABLE ts_plan_key_area_carrier_type (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  type_key      varchar(16) NOT NULL COMMENT '类型键（all/lab/center/park/incubator/accelerator，种子 key；all=图例汇总行「全部载体」非实体类型，§0.3）',
  type_name     varchar(32) NOT NULL COMMENT '类型名（全部载体/重点实验室/工程中心/科技园区/孵化器/加速器，种子 name 逐字）',
  carrier_count int unsigned NOT NULL COMMENT '全市口径载体计数 🧪（2856/128/256/68/420/186，种子 count 逐字；与 22 点位、区基线合计 1146 三口径互不调和，§0.4 禁对账禁派生）',
  color         varchar(9)  NOT NULL COMMENT '图例色（#2563eb 等，种子 color 逐字，演示态展示用）',
  sort_no       smallint    NOT NULL COMMENT '图例顺序 1..6（种子数组序，all=1）',
  metric_id     varchar(32)          DEFAULT NULL COMMENT 'NULL——188 other_system（GIS 载体点位+ADS 详情，无统计核；计数旁不显伪 8 件套，ARCH §4.4）',
  source        varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_type_key (type_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·载体类型图例与全市计数（other_system 无 metric_id，序188）';
```

### 2.4 `ts_plan_key_area_district_baseline`（6 行，序 188）

```sql
CREATE TABLE ts_plan_key_area_district_baseline (
  id             bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  district       varchar(16) NOT NULL COMMENT '行政区（南山/福田/龙岗/宝安/龙华/坪山，种子 district 逐字；含龙华无光明，覆盖差 §0.5 不补行）',
  total_carriers int unsigned NOT NULL COMMENT '区载体总量 🧪（276/242/208/174/140/106，种子 total 逐字；合计 1146 与 22/2856 互不调和，§0.4）',
  leading_type   varchar(16) NOT NULL COMMENT '区主导载体类型（重点实验室/工程中心/科技园区/孵化器，种子 leadingType 中文名逐字；与 carrier_type.type_name 同名域，映射归 API）',
  metric_id      varchar(32)          DEFAULT NULL COMMENT 'NULL——188 other_system，同 §2.3',
  sort_no        smallint    NOT NULL COMMENT '种子数组序 1..6（按总量降序）',
  source         varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at     datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_district (district)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·区县载体基线（other_system 无 metric_id，序188）';
```

### 2.5 `ts_plan_key_area_competitiveness`（5 行，序 186）

```sql
CREATE TABLE ts_plan_key_area_competitiveness (
  id          bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  metric_key  varchar(16) NOT NULL COMMENT '指标卡键，沿用 demo 键（composite/innovation/industry/openness/potential，种子 key；契约无此块，键名沿 demo，映射归 KEY-API）',
  label       varchar(16) NOT NULL COMMENT '指标卡名（综合指数/创新能力/产业基础/开放协同/发展潜力，种子 label 逐字）',
  value       decimal(5,1) NOT NULL COMMENT '指标值 🧪（78.5/88/85/62/82，种子 value；与五维画像并存不合并，ARCH §7.1 配套）',
  change_pct  varchar(16) NOT NULL COMMENT '环比字符串逐字（12.3%/8.6%/6.2%/5.4%/10.1%，种子 change，无 + 前缀；U4 不数值化，待 M0）🧪',
  metric_id   varchar(32) NOT NULL COMMENT '行级挂号（赋号草稿·未签）：potential 行=M_INNOV_KEYD_POTENTIAL（MIXED·TEMP_DS09_KEYD_POTENTIAL·Q-MO-DS09-04），其余 4 行（composite/innovation/industry/openness）=M_INNOV_KEYD_COMPETITIVENESS（MIXED·TEMP_DS09_KEYD_COMPETITIVENESS·Q-MO-DS09-04）；禁改挂 M_SYNTH_VIT_*/GBA/CITY 186 号/企业 141/M_CHAIN_*（ARCH §7.3）',
  sort_no     smallint    NOT NULL COMMENT '卡片顺序 1..5（种子数组序，composite 首位）',
  source      varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_metric_key (metric_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·竞争力指标卡（D18 读表，序186）';
```

### 2.6 `ts_plan_key_area_dimension`（5 行，序 186）

```sql
CREATE TABLE ts_plan_key_area_dimension (
  id            bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  dim_key       varchar(32) NOT NULL COMMENT '五维英文键（U8-1 建议新定，种子无）：innovation_resources/research_output/industry_competitiveness/talent_support/open_collaboration；契约示例「技术/产业/空间/人才/政策」系草案虚构已弃（ARCH §7.1）；M0+数据侧拍板后冻结，禁引「空间维」以免与 185 SPATIAL 混淆',
  dim_label     varchar(16) NOT NULL COMMENT '五维中文名（创新资源/科研产出/产业竞争力/人才支撑/开放协同，种子 keyAreaDimensionScores.label 逐字；FE-TS-09A 已冻结，demo 中文文案即页面既显内容）',
  score         smallint unsigned NOT NULL COMMENT '维度得分 🧪（92/88/85/78/72，种子 percent 逐字；权重未签 Q-MO-DS09-04，不展开公式）',
  metric_id     varchar(32) NOT NULL COMMENT 'M_INNOV_KEYD_COMPETITIVENESS（赋号草稿·未签·MIXED·Q-MO-DS09-04）；表级指标，5 行同值冗余',
  rendered_note varchar(255) NOT NULL COMMENT '页级口径整句（响应 caliber_note 物理行源，禁 Java 拼文案，沿 OV hot_tech.rendered_note 先例）：文案由本分册种子行定稿、KEY-API 只定携带机制（v2 item 1 会签裁定）；定稿句=「本页竞争力五维得分与指标值为演示数据，五维构成与评估权重口径待定稿后更新」——用户可读、零内部编号（v2 item 2：Q-MO-DS09-04 / KEYD-B02·B03 等内部编号只留本表 metric_id 列注释，不进响应文案，核对记录 §6 零泄漏纪律）；正式口径定稿后随本分册种子行版本翻换；5 行同值冗余',
  dim_order     smallint    NOT NULL COMMENT '维序 1..5（种子数组序）',
  source        varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_dim_key (dim_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·竞争力五维画像（D18 读表，序186；dim_key 为 U8-1 新定英文键）';
```

### 2.7 `ts_plan_key_area_benchmark`（5 行，序 186）

```sql
CREATE TABLE ts_plan_key_area_benchmark (
  id        bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  region    varchar(32) NOT NULL COMMENT '对标区域（南山区/深圳湾合作区/广州天河区/香港科技园/珠海横琴新区，种子 region 逐字；首行为本市基线行，其余为对标行——语义由 rank 隐含，不拆表）',
  score     decimal(4,1) NOT NULL COMMENT '对标分 🧪（78.5/74.2/71.3/69.1/66.8，种子 score 逐字）',
  rank_no   smallint unsigned NOT NULL COMMENT '名次 1..5（种子 rank 逐字；南山 78.5 与竞争力综合指数 78.5 同源同值，demo 口径不复算）',
  metric_id varchar(32) NOT NULL COMMENT 'M_INNOV_KEYD_COMPETITIVENESS（赋号草稿·未签·MIXED·Q-MO-DS09-04）；表级指标，5 行同值冗余',
  source    varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_rank_no (rank_no),
  KEY idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·竞争力区域对标（D18 读表，序186）';
```

### 2.8 `ts_plan_key_area_land`（6 行，序 187）

```sql
CREATE TABLE ts_plan_key_area_land (
  id           bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  district     varchar(16) NOT NULL COMMENT '行政区（南山×2/福田/龙岗/宝安/龙华，种子 area 逐字；无坪山/光明行，demo 覆盖差 §0.5 不补行）',
  land_type    varchar(16) NOT NULL COMMENT '土地用途（研发用地/产业用地，种子 type 逐字）',
  area_sqm     int unsigned NOT NULL COMMENT '用地面积 ㎡ 🧪（125000/98000/87000/156000/72000/113000，种子 area_sqm 逐字）',
  efficiency   smallint unsigned NOT NULL COMMENT '利用效率分 0-100 🧪（92/85/78/65/58/62，种子 efficiency 逐字；权重/公式未签不展开）',
  status       varchar(8)  NOT NULL COMMENT '效率状态（good/medium/poor，种子 status 英文枚举逐字不翻译；中文标签映射归 FE/API）',
  land_benefit json                 DEFAULT NULL COMMENT '区级土地效益预留 JSON（U8-2 定名 plot_ratio/output_per_mu）；V1 全 NULL——区级读数由本表标量列（area_sqm/efficiency/status）承载，本列正式态 GIS 图层接入后回填（§0.7 双预留）',
  metric_id    varchar(32) NOT NULL COMMENT 'M_INNOV_KEYD_LAND（赋号草稿·未签·STAT·TEMP_DS09_KEYD_LAND；GIS 用地/产出图层读数，差集 other_system，禁按号 mapped 综合 187、禁 missing）；表级指标，6 行同值冗余',
  sort_no      smallint    NOT NULL COMMENT '种子数组序 1..6',
  source       varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at   datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_district_type (district, land_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·土地用途与效益（区级，D18 读表，序187；亩均/容积率正式值待数据侧接入）';
```

### 2.9 `ts_plan_key_area_plan`（3 行，序 190）

```sql
CREATE TABLE ts_plan_key_area_plan (
  id              bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  plan_id         varchar(8)  NOT NULL COMMENT '方案键（a/b/c，种子 id；契约示例 PLAN-A 形态系草案虚构，沿 demo 键）',
  plan_name       varchar(16) NOT NULL COMMENT '方案名（方案A/方案B/方案C，种子 name 逐字；3 方案为产品定义，页级非集群级，ARCH §5 收口 1）',
  title           varchar(64) NOT NULL COMMENT '方案主题（提升创新策源能力/强化产业转化效率/优化空间协同布局，种子 title 逐字，非生成物）',
  priority        varchar(8)  NOT NULL COMMENT '优先级（高/高/中，种子 priority 中文逐字）',
  expected_effect varchar(16) NOT NULL COMMENT '预期效果字符串逐字（+18.6%/+22.9%/+15.2%，种子 expectedEffect 含 + 号；U4 不数值化）🧪；「方案模拟」Modal 效果预测值即本列 demo 逐字，无模拟端点无 501',
  resource_gap    varchar(16) NOT NULL COMMENT '资源缺口字符串逐字（-23.2%/-19.8%/-16.7%，种子 resourceGap 含 - 号）🧪',
  actions         json NOT NULL COMMENT '行动清单数组（["增强基础研究投入","引育高端科研人才","建设重大科研平台"] 等，种子 actions 逐字 3 项/方案）',
  primary_action  varchar(16) NOT NULL COMMENT '主操作文案（查看建议，种子 primaryAction 逐字）',
  secondary_action varchar(16) NOT NULL COMMENT '次操作文案（方案对比，种子 secondaryAction 逐字）',
  detail_action   varchar(16) NOT NULL COMMENT '详情操作文案（资源详情，种子 detailAction 逐字）',
  metric_id       varchar(32)          DEFAULT NULL COMMENT 'NULL——190 n/a_ops 建议壳（演示读数不挂 ID；禁 missing 模拟叶、禁借 501、禁改挂 186 附录建议/技术链 140/M_CHAIN_LAYOUT_*/M_POLICY_INDUSTRY_FIT）',
  sort_no         smallint    NOT NULL COMMENT '方案顺序 1..3（种子数组序）',
  source          varchar(16) NOT NULL DEFAULT 'demo_seed',
  created_at      datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_plan_id (plan_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='重点领域·资源配置优化方案（建议壳，n/a_ops 无 metric_id，序190）';
```

---

## 3. 行源映射与行数清单（mock 实测）

> 全部行数以 `lumen-ui-science-pc/src/mock/modules/techDevelopmentPlan.ts` **实测数出**，非估算；9 数组均在 mock 内（KEY 组零 demo.js 依赖）。

| 表 | 种子数组（mock 行号） | 展开规则 | 行数 |
|---|---|---|---|
| `ts_plan_key_area` | `industryClusters`（L471–496） | 1 集群 1 行 | **3** |
| `ts_plan_key_area_carrier` | `carrierLocations`（L441–469） | 1 载体 1 行（lab 5 + center 4 + park 6 + incubator 4 + accelerator 3）；7 行无集群引用 → cluster_id NULL（§0.2 白名单） | **22** |
| `ts_plan_key_area_carrier_type` | `carrierTypes`（L347–354） | 1 类型 1 行（含 all 图例汇总行） | **6** |
| `ts_plan_key_area_district_baseline` | `districtCarrierBaselines`（L498–505） | 1 区 1 行 | **6** |
| `ts_plan_key_area_competitiveness` | `keyAreaCompetitivenessMetrics`（L416–422） | 1 指标卡 1 行（composite 首位） | **5** |
| `ts_plan_key_area_dimension` | `keyAreaDimensionScores`（L424–430） | 1 维 1 行（dim_key 按 U8-1 映射表新定，种子仅有中文 label） | **5** |
| `ts_plan_key_area_benchmark` | `keyAreaBenchmarkRows`（L432–438） | 1 对标区 1 行 | **5** |
| `ts_plan_key_area_land` | `landUseData`（L401–408） | 1 区×用途 1 行（南山 2 行，余 4 区各 1） | **6** |
| `ts_plan_key_area_plan` | `keyAreaScenarioPlans`（L410–414） | 1 方案 1 行 | **3** |
| **合计** | | | **61** |

**dim_label → dim_key 映射表（U8-1 建议键，灌数内置）**：创新资源→`innovation_resources`、科研产出→`research_output`、产业竞争力→`industry_competitiveness`、人才支撑→`talent_support`、开放协同→`open_collaboration`（M0+数据侧拍板前为建议值，拍板不同则改映射不改表）。

**集群↔载体引用（15 行挂靠明细）**：ai=`L003/C002/P001/P002/I001/A001`（6）、bio=`L002/L005/P004/I002`（4）、energy=`C001/C003/C004/P006/A003`（5）；未挂 7 行=`L001/L004/P003/P005/I003/I004/A002`。

**配套说明（v2 item 3 勘误）**：189 图层单选全集实为 **4 值**：科技载体/土地效益/**资源缺口**/产业热度（FE 本地常量 `MAP_LAYER_OPTIONS`，`models/techDevelopmentPlanModel.ts` L985，行源 demo L2984–L2989；ARCH §4.5 写 3 值系勘误）。**「资源缺口」是图层选项、非载体类型**——`carrierTypes` 种子（L347–354）无对应行，`carrier_type` 表行数不变（6），行数合计 61 不变；仅 3 集群默认值落 `default_map_layer` 列（产业热度/科技载体/土地效益，未用满全集，demo 事实），**不建字典表**。189 公共筛选选项由 `industry_category`（大门类）/`technology_field`（细分）+ carrier_type 行承载，V1 全量 61 行一次下发 FE 本地过滤，无服务端筛选参数。

**种子存在但明确不灌的数组（防误灌清单）**：`hotTechData`/`technologyTrend*`/`multidimensionalIndicatorCategories`/`localAdvantage*`/`talent*`/`directionMonitor*`/`planningResourcePackages`/`technologyHeatTrendDefinition`（OV 组 09a，244 行另册）；`companies`/`overlapMatrix`/`overlapRuleProfiles`/`researchLevelCards`/`researchOverlapBenchmarks`/`regionalPlanningInsightRows`/`researchGraphNodes`（RES 组 09c，另册）。本分册只认 §3 清单 9 数组，多一行即错。

---

## 4. 灌数方案（Python 一次性脚本规格）

脚本实现属**后续 data-agent 执行单**（TS-L2-DS09-KEY 组实现阶段建单），本节只冻结规格：

1. **幂等**：按表 `TRUNCATE + INSERT`，单表单事务，可重跑；9 表全量 61 行，无排除表（对照 OV：本组无 direction_warning 式零行表）。
2. **输入 = 种子提取**（推荐脚本解析）：在 `lumen-ui-science-pc` 仓内用 node（vite-node/esbuild 加载 TS 模块）`import` mock 模块后 dump 9 数组 JSON（§3 清单为准，逐字零转录错漏）；**无需 demo.js**（KEY 组 9 数组全在 mock，与 OV 需 demo.js 补时间轴/点位不同）。手工转 JSON 备选，须与源文件 diff 校验后使用。
3. **转换规则**（脚本内显式实现）：
   - `industryClusters.carrierIds` → `carrier_ids` JSON 原组直存；同时对每 id 校验存在于 22 载体键集，缺一报错回滚；
   - `carrier.cluster_id` 由 3 集群 `carrierIds` 反查填充；未命中 7 行置 NULL，脚本内置 7 ID 白名单（`L001/L004/P003/P005/I003/I004/A002`）断言，反查结果 ≠ 白名单即报错回滚（防种子漂移）；
   - `land_benefit` 两表列一律不写（INSERT 显式 NULL，禁编造容积率/亩产）；
   - `keyAreaDimensionScores.label` + §3 dim_key 映射表 → 写入英文键；映射表在脚本内显式列出 5 条；
   - `metric_id` 列随行写入草稿号：cluster=SPATIAL、land=LAND、dimension/benchmark=COMPETITIVENESS、competitiveness 行级区分（potential 行=POTENTIAL，其余=COMPETITIVENESS）、carrier/carrier_type/district_baseline/plan=NULL；
   - `rendered_note` 整句逐字写入（定稿文案见 §2.6，**由本分册种子行定稿**、KEY-API 只定携带机制——v2 item 1；正式口径定稿后随本分册种子行版本翻换）；
   - 其余字段直存：`change_pct`/`expected_effect`/`resource_gap` 字符串逐字不数值化（U4）；`status` 英文枚举不翻译；`lng`/`lat` 数值直存。
4. **验收 = 逐表行数断言**：`SELECT COUNT(*)` 对 §3 清单 **3/22/6/6/5/5/5/6/3（合计 61）** + 抽样断言（carrier：L001 cluster_id IS NULL、A001 cluster_id='ai'；cluster：ai 行 carrier_ids 6 元素、default_map_layer='产业热度'；carrier_type：all 行 carrier_count=2856；district_baseline：南山 total_carriers=276；competitiveness：composite value=78.5 且 change_pct='12.3%'、potential 行 metric_id=M_INNOV_KEYD_POTENTIAL；dimension：创新资源 score=92 且 dim_key='innovation_resources'、5 行 rendered_note 同值；benchmark：rank_no=1 region=南山区 score=78.5；land：南山+研发用地 area_sqm=125000 efficiency=92 status='good'、6 行 land_benefit 全 NULL；plan：a 行 expected_effect='+18.6%' 且 actions 3 元素）；carrier 表另断言 `cluster_id IS NULL` 恰 7 行。任一失败即回滚整批。
5. **dry-run**：脚本带 `--dry-run`，只输出各表待写行数与 NULL 分布不落库。
6. **不做**：**不写第二套统计脚本**——密度/集聚度/效率派生/计数调和（22 vs 2856 vs 1146）一律不算（ARCH §3 唯一禁灌项 + §0.4）；不写 ODS/DWD/供应方库；不动 demo/lumen 两仓源码（只读事实源）；不写任何 `cfg_metric-*-seed.yaml`（四条草稿号只在核对记录 §赋号表，禁入 seed）。

---

## 5. 合规自检

| 项 | 自检 | 结论 |
|---|---|---|
| **D18 三要素** | 9 表逐表有「表名/行数/灌数方/读取接口」（§1 总表 = ARCH §6 对齐，61 行一致）；灌数=Python 一次性脚本；Java `gkxlumen-display` 单端点 `key-areas` 只读组装 9 块；接口不直返 mock/常量——文案由表行携带（plan actions/操作文案、rendered_note 口径整句、carrier_total=表计数） | ✅ |
| **D18 库边界** | 不进 ODS/DWD/供应方 `gkx` 库；不带 `gapfill_` 前缀；`gkxlumenx_ads` 展示 ADS、`ts_plan_key_area_` 前缀库内唯一 | ✅ |
| **无写面** | 6 叶零写面：5 叶 D18 读表 + 189 交互壳无表无端点；本页禁 501（catalog 501 只给 COMPREHENSIVE 184）；190 方案模拟=FE Modal 无模拟端点 | ✅ |
| **U8 落实** | U8-1：五维英文键入 `dim_key` 列（建议值，M0+数据侧拍板后冻结）；U8-2：`land_benefit` 沿契约 `plot_ratio`/`output_per_mu` 定名，V1 双表全 NULL | ✅（两键/定名待拍板，会签点 K-3） |
| **metric 物理列对齐** | 四条 KEYD 草稿号全落列：SPATIAL（cluster）/ COMPETITIVENESS + POTENTIAL（competitiveness 行级 + dimension/benchmark）/ LAND（land）；无核叶（carrier/carrier_type/district_baseline/plan）置 NULL；列注释均标「赋号草稿·未签」；不改差集、不写 seed、撞号禁令随 ARCH §7.3 冻结 | ✅ |
| **禁假数据** | `land_benefit` 双表 V1 全 NULL（demo 无源禁编造）；7 载体 cluster_id NULL（诚实空）；三计数口径（22/2856/1146）不调和不派生；行政区覆盖差不补行 | ✅ |
| **不写第二套统计脚本** | 唯一脚本只搬运种子（§4）；集聚度/密度等派生数值一律不算，正式态 GIS 图层接入后换真源 | ✅ |
| **字段沿用种子/契约命名** | 列名对齐 ARCH §4 逐叶列单（cluster_name←label、carrier_count←count、rank_no←rank、change_pct←change 等）；值逐字保留 demo 口径（含符号字符串/英文枚举/中文层级）；不擅自数值化（U4 待 M0） | ✅ |
| **范围** | 不改 task-registry、不 git 提交、不建表不灌数、不动 demo/lumen 源码；OV/RES 组数组列入防误灌清单 | ✅ |
| **v2 会签裁定落实** | 文案定稿归属收口（item 1）、rendered_note 零内部编号（item 2）、图层 4 值勘误且 carrier_type 行数不变（item 3）、修订记录（item 4）——逐条对应见 §8；行数合计复核 **61 不变** | ✅ |

---

## 6. 会签讨论点（单列，供四角色拍板）

| # | 点 | 建议与处置 |
|---|---|---|
| K-1 | `'all'` 图例汇总行保留在 `carrier_type` 表（count=2856 全市口径）vs 视为配置拆出 | **建议保留**（FE 图例/筛选零改动；列注释已标非实体类型；计数三口径不调和已声明 §0.4） |
| K-2 | `land_benefit` 双预留（carrier 逐载体语义 + land 区级预留语义，ARCH §4.3/§5 均留） | **建议保留双列**（语义不同、双双 V1 NULL 零成本；如会签要求减一，先减 land 表列——carrier 列是契约 §3.7 点名项） |
| K-3 | 五维英文键 `dim_key` 具体值（U8-1）与 `land_benefit` 字段定名（U8-2） | **建议按 ARCH §7.1/§7.2 值冻结**（innovation_resources 等 5 键 / plot_ratio+output_per_mu）；M0+数据侧拍板不同则改灌数映射，不改表 |
| K-4 | `dimension.rendered_note` 新列（响应 `caliber_note` 物理行源，沿 OV hot_tech.rendered_note 先例；ARCH §3 要求「文案由表行携带」但未指明载体） | **已裁定（v2）**：保留；文案由本分册种子行定稿、KEY-API 只定携带机制（消除与 API §9.5 互指）；定稿句为用户可读口径句、零内部编号（Q-MO-DS09-04 / KEYD-B02·B03 只留列注释） |
| K-5 | `updated_at` 公共列（本组 ARCH §6 要求；OV 组 8 表仅有 created_at） | **建议保留**（两组 ARCH 口径差异，随本组 ARCH 执行；静态种子零副作用） |

---

## 7. 会签与签收路径

本分册随 KEY-ARCH 稿四角色会签（意见落 `sdd/l2/会签/重点领域规划-会签.md`）→ 全部同意后由授权人签收 → 与 KEY-API（按 ARCH §5 改约 §3.7 响应为平铺 9 块）/ KEY-METRIC 并行成稿 → 拆 Java 实现（建 DDL + `PlanningQueryService.keyAreas()`）/ 灌数（本分册 §4 规格转执行单）/ FE 接线 / 主路径测试四行实现单。

---

## 8. 会签修订记录 v2（2026-11-06，architect / api / algorithm 三家意见并入）

| # | 会签来源 | 变更 | 落点 |
|---|---|---|---|
| 1 | 三家会签（裁定） | **文案定稿归属收口**：`caliber_note`（`dimension.rendered_note`）文案由**本分册种子行定稿**，KEY-API 只定携带机制——消除与 API §9.5 的互指；§1 总表、DDL 列注释、灌数转换规则同步改写 | §1 / §2.6 / §4 |
| 2 | architect 会签 | **rendered_note 占位句去内部编号**（违核对记录 §6「零泄漏 Q-*」纪律）：原含 `Q-MO-DS09-04 / KEYD-B02·B03` 字样的口径句换为用户可读定稿句「本页竞争力五维得分与指标值为演示数据，五维构成与评估权重口径待定稿后更新」；内部编号只留 `metric_id` 列注释，不进响应文案 | §2.6 |
| 3 | 会签勘误 | **189 图层全集实为 4 值**（科技载体/土地效益/资源缺口/产业热度；FE 本地常量 `MAP_LAYER_OPTIONS`，model L985 = demo L2984–L2989），ARCH §4.5 的 3 值表述勘误；「资源缺口」为图层选项**非载体类型**，`carrierTypes` 种子无对应行 → **carrier_type 表行数不变（6）**、3 集群默认图层未用满全集的事实注明；§2.1 列注释同步 | §2.1 / §3 |
| 4 | 会签必改 | 本记录小节；行数合计复核：9 表 3/22/6/6/5/5/5/6/3 = **61 不变**（图层勘误不影响任何表行数）；状态升 v2、K-4 标已裁定 | §6 / §8 |
