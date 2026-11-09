# TS-L2-DS09-RES-DATA · 研究领域分析 · 后台数据架构设计

> **任务**：`TS-L2-DS09-RES-DATA`（definition，不写业务代码、不建表、不灌数）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 data-agent（子智能体链路故障，主会话按授权链代写；监管人 `human:王梓真`）
> **状态**：草案，待四角色会签 · **硬依赖**：`sdd/l2/TS-L2-DS09-RES-ARCH.md`（11 表 68 行设计在其 §0/§6）
> **约定沿袭**：OV/KEY 两组分册——`gkxlumenx_ads`、utf8mb4、`updated_at` 公共列、metric 列注释标未签、灌数 TRUNCATE+INSERT 幂等 + 逐表行数断言

---

## 1. 库与表总表（11 表 68 行，全部 D18 读面）

**D18 声明**：全部落展示 ADS MySQL `gkxlumenx_ads` 库、`ts_plan_research_` 前缀；**不进 ODS / DWD / 供应方库、不带 `gapfill_` 前缀**；Python 一次性灌数（demo 冻结种子），Java 只读。每表公共列：`metric_id VARCHAR(64) NULL`（列注释：赋号草稿·未签·pending 唐绍祖；无核叶恒 NULL）、`updated_at DATETIME`。

| # | 表 | 行数（实测） | 消费块（RES-API §2） |
|---|---|---|---|
| 1 | `ts_plan_research_field` | 5 | fields |
| 2 | `ts_plan_research_company` | 7（目标 1 + 六企 6） | companies |
| 3 | `ts_plan_research_overlap` | **6**（15 对中 9 对无真值**不灌行**） | overlap_matrix |
| 4 | `ts_plan_research_overlap_rule` | 3 | overlap_rules |
| 5 | `ts_plan_research_time_factor` | 3 | time_scopes |
| 6 | `ts_plan_research_grade` | 4 | level_cards |
| 7 | `ts_plan_research_overlap_benchmark` | 3 | overlap_benchmarks |
| 8 | `ts_plan_research_graph_node` | 14 | graph.nodes |
| 9 | `ts_plan_research_graph_edge` | 13 | graph.edges |
| 10 | `ts_plan_research_insight` | 4 | intelligence_rows |
| 11 | `ts_plan_research_report_template` | 6+2（报告 3+建议 3 模板 + page_caliber/graph_limit 2 系统行） | report_export / strategy_advice / caliber_note / U9 阈值 |

> 注：ARCH 稿计 68 行 = 11 数组 68；本分册将 page_caliber / graph_limit 两个系统模板行补入 report_template（6+2=8），**种子合计 70 行**（差异 2 行为 RES-API §2/§3 的口径与阈值行源，属本分册对 ARCH 的增量，已在 §6 差异表登记）。

## 2. 逐表 DDL 草案

```sql
-- 1. 领域字典（ResearchTab L53 常量表行化）
CREATE TABLE ts_plan_research_field (
  field_key    VARCHAR(32)  NOT NULL COMMENT '领域键（ai/quantum/synbio/ic/newenergy）',
  field_label  VARCHAR(64)  NOT NULL COMMENT '领域名（人工智能/量子科技/合成生物学/集成电路/新能源）',
  sort_no      INT          NOT NULL DEFAULT 0,
  metric_id    VARCHAR(64)  NULL COMMENT '无统计核，恒 NULL',
  updated_at   DATETIME     NOT NULL,
  PRIMARY KEY (field_key)
);

-- 2. 比对企业（目标主体 + 六企）
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
);

-- 3. 重叠度真值对（G-B4：哈希算法废弃，只有真值行）
CREATE TABLE ts_plan_research_overlap (
  pair_id        BIGINT      NOT NULL AUTO_INCREMENT,
  company_a      VARCHAR(128) NOT NULL COMMENT '对端 A（约定 target 或字典序在前）',
  company_b      VARCHAR(128) NOT NULL,
  overlap_score  DECIMAL(5,2) NOT NULL COMMENT '真值 45–72；15 对中 9 对无种子 → 不灌行、不造数（诚实空）',
  level          VARCHAR(8)  NOT NULL COMMENT 'high | medium',
  related_fields JSON        NULL COMMENT '相关领域数组',
  metric_id      VARCHAR(64) NOT NULL DEFAULT 'M_INNOV_RES_OVERLAP' COMMENT '赋号草稿·未签',
  updated_at     DATETIME    NOT NULL,
  PRIMARY KEY (pair_id),
  UNIQUE KEY uk_pair (company_a, company_b)
) COMMENT='G-B4：FE 名称哈希兜底已废弃；本表只有种子真值对';

-- 4. 重叠规则三档（复算参数面，逐字）
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
);

-- 5. 时间系数（筛选下拉 + 复算系数双职责）
CREATE TABLE ts_plan_research_time_factor (
  scope_key   VARCHAR(8)   NOT NULL COMMENT '1y | 3y | 5y',
  scope_label VARCHAR(16)  NOT NULL COMMENT '近1年/近3年/近5年',
  factor      DECIMAL(4,2) NOT NULL COMMENT '0.82 / 1.00 / 1.12',
  sort_no     INT NOT NULL DEFAULT 0,
  metric_id   VARCHAR(64) NULL,
  updated_at  DATETIME NOT NULL,
  PRIMARY KEY (scope_key)
);

-- 6. 四档等级（U3：标签逐字 + 阈值建议值）
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
);

-- 7. 对标基准（gauge 兜底 + 196 合作机会拼接源）
CREATE TABLE ts_plan_research_overlap_benchmark (
  bench_id   BIGINT NOT NULL AUTO_INCREMENT,
  name       VARCHAR(128) NOT NULL COMMENT '华为技术有限公司82 / 腾讯科技（深圳）67 / 大疆创新科技 48',
  score      DECIMAL(5,2) NOT NULL,
  sort_no    INT NOT NULL DEFAULT 0,
  metric_id  VARCHAR(64) NOT NULL DEFAULT 'M_INNOV_RES_OVERLAP' COMMENT '采 METRIC 分册建议：基准值属重叠度口径（会签可裁）',
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (bench_id)
);

-- 8/9. 知识图谱演示骨架（V1；U9 超 100 节点/300 边走 M2）
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
);
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
);

-- 10. 情报行（195 列表 + 196 派生源）
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
);

-- 11. 报告模板（文案表行携带；Java/Python 不硬编码）
CREATE TABLE ts_plan_research_report_template (
  section_key   VARCHAR(32) NOT NULL COMMENT 'overlap_section/advantage_section/suggestion_section/tech_route/resource_config/cooperation + 系统行 page_caliber/graph_limit',
  section_label VARCHAR(64) NOT NULL,
  template_text TEXT NOT NULL COMMENT '含 {target}/{compare}/{field} 占位符；demo buildResearchIntelligenceReport L460-490 逐字',
  is_system     TINYINT(1) NOT NULL DEFAULT 0 COMMENT '1=系统行（page_caliber 整页口径 / graph_limit U9 阈值 100/300）',
  sort_no       INT NOT NULL DEFAULT 0,
  metric_id     VARCHAR(64) NULL,
  updated_at    DATETIME NOT NULL,
  PRIMARY KEY (section_key)
);
```

## 3. 行源映射与行数清单（实测，mock L347–L545 及 ResearchTab/model 常量）

| 表 | 种子源 | 行数 |
|---|---|---|
| field | ResearchTab L53 五选项常量 | 5 |
| company | ResearchTab L38 目标主体 + mock companies L356 六企 | 7 |
| overlap | mock overlapMatrix L365（**9 对无真值不灌**） | 6 |
| overlap_rule | mock overlapRuleProfiles L374 | 3 |
| time_factor | mock timeScopeFactor L601 三键 | 3 |
| grade | mock researchLevelCards L516 | 4 |
| overlap_benchmark | mock researchOverlapBenchmarks L523 | 3 |
| graph_node | mock researchGraphNodes L530（**契约 6/6 已被实测推翻**） | 14 |
| graph_edge | model L740 星型 builder 逻辑落表（中心→13 节点） | 13 |
| insight | mock regionalPlanningInsightRows L509 | 4 |
| report_template | model L460–490 报告/建议模板 + 2 系统行 | 8 |

**种子合计 70 行**（ARCH 68 + 本分册 2 系统行，见 §1 注）。

## 4. report_template 与 M1 §3.8 任务中心的关系

模板行只存**展示元数据与文案槽位**；Word（.doc）文件产物由任务中心按模板行渲染生成，`job_id` 即 `report_ref`——**不重复存储文件本体**（文件存储归 M1 任务中心既有机制，本页不自建桶/目录，D14）。查询 = intelligence_rows + template 行 JOIN 渲染；下载 = 建导出任务。

## 5. 灌数方案（Python 一次性，实现归后续执行单）

- 提取：node 脚本或 Python 从 mock 模块 export 实位（L347–L545，**文件头部 L619 等注释行号陈旧，以 export 为准**）+ ResearchTab/model 常量段读取；星型边按 model builder 逻辑生成 13 行。
- 幂等：逐表 `TRUNCATE + INSERT`；可重跑。
- **禁灌清单**（断言必查）：① 15 对中 9 个无真值企业对（overlap 行数必须 =6）；② 专家类图谱节点（需规提及、种子无，诚实缺位）；③ 一切种子外派生数值（象限均值由 Java 现算，不落表）；④ land/级差类无本组字段。
- 验收断言（逐表行数）：5/7/6/3/3/4/3/14/13/4/8 = **70**；overlap 6 行值域 45–72；grade threshold_low 依次 80/65/45/0 且 is_draft=1；plan_id 序列 a/b/c/b。
- 不写第二套统计脚本（灌数脚本唯一，归 data-agent 执行单）。

## 6. 与 ARCH 稿差异（登记）

1. report_template 6→8 行（补 page_caliber / graph_limit 两系统行，作 RES-API caliber_note 与 U9 阈值的物理行源）——种子合计 68→70；
2. benchmark 表 metric_id 采纳 METRIC 分册建议挂 `M_INNOV_RES_OVERLAP` 草稿（基准值属重叠度口径；会签可裁）；
3. grade 表增 `is_draft` 列（U3 建议值未拍板的表行级标记，对应 API 响应 draft 语义）。

## 7. 合规自检

D18 ✅（三要素齐：表名/灌数方=Python 一次性/读取接口=research-analysis 块；不进 ODS/DWD/供应方库；无 gapfill_）；零 501 ✅（无模型注册面）；无个人明细 ✅（企业/机构级聚合，无人员行）；文案/阈值/模板全表行携带 ✅（Java 不硬编码）；graph 拓扑落表（Java 不硬编码星型逻辑）✅。
