# POLICY · gapfill（D16 缺项库）

```yaml
---
doc_id: POLICY-STORES-GAPFILL
element: POLICY
role: store-mysql
status: draft
version: "2026-11-09"
updated: 2026-11-10
task_id: POL-IMPL-EFFECT-MOCK-VIA-UI-L01
---
```

> **库**：`gkxlumenx_gapfill`（DBA 预建；应用路径禁止 `CREATE DATABASE`）。  
> **边界**：只写 `gapfill_*`；禁止写入 ODS / 正式 DWD / ADS / 供应方库。  
> **D19**：新建表，以及任何会和 `policy_base_info.policy_id` 等值比较的列，用 `utf8mb4` / `utf8mb4_0900_ai_ci`，建表语句必须写明。下面已落地的 CREATE 多数仍是库默认的 `utf8mb4_unicode_ci`（可视化四张是 `utf8mb4_general_ci`）。这是 2026-11-10 的现网，复制这些语句前要改成 D19。未改之前禁止和主表 `policy_id` 做隐式等值。  
> **索引**：[`../README.md`](../README.md)。详设读侧：[05.6.2 §3.1](../../../../../agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.6.2-深圳政策现状分析.md)。  
> **按钮缺项空表**（`POL-MOCK-BTN-A01`）：下面「八张新表」与可执行脚本同文。210/211 现网已有，不在这里重建。

## `gapfill_policy_sz_effect`（深圳落地实效三维缺项）

一政策一行。深圳现状板在 DWD 空维时按 `policy_id` 只补内存字段（启动日 / 支持对象 / 反馈分），不改 `policy_base_info` 原列。

### CREATE（as-built）

真源：`lumen-algo-py/scripts/mysql/gapfill_policy_sz_effect.sql` 与 `polan/mockgen/effect_gapfill.py` 的 `CREATE_SQL`（同文；应用侧 `ensure_table` 只 `CREATE TABLE IF NOT EXISTS`）。

```sql
CREATE TABLE IF NOT EXISTS gkxlumenx_gapfill.gapfill_policy_sz_effect (
  policy_id VARCHAR(128) NOT NULL,
  implementation_date DATE NOT NULL,
  support_object VARCHAR(64) NOT NULL,
  feedback_score TINYINT NOT NULL,
  metric_id VARCHAR(64) NOT NULL,
  gap_item VARCHAR(128) NOT NULL,
  fill_method VARCHAR(16) NOT NULL,
  fill_model VARCHAR(64) NULL,
  gapfill_batch_id VARCHAR(128) NOT NULL,
  generated_at DATETIME NOT NULL,
  PRIMARY KEY (policy_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

| 列 | 约束 |
|---|---|
| `implementation_date` | 有效日；≠ 发布日、≠ 零日期；缺失不写成 `0000-00-00` |
| `support_object` | 非空（企业 / 科研机构 / 高等学校 / 新型研发机构） |
| `feedback_score` | 1–5；缺失不写成 0 |
| `metric_id` | 固定 `M_POLICY_IMPLEMENTATION_EFFECT` |
| `gap_item` | `落地执行启动,受益覆盖,实施反馈` |
| `fill_method` | 规则灌数 `rule`；LLM 路径可带 `fill_model` |

### 写入口（必须挂算法库页两过程）

| UI（`/#/policy/mock`） | 代码 | 行为 |
|---|---|---|
| 「Mock 10 条数据」 | `polan.mockgen.synth.run` | 当次合成政策（含历史版）UPSERT；末尾 `backfill_missing` 回补 DWD 仍缺行 |
| 「真实政策补外围：深圳 40 + 随机 10」 | `polan.mockgen.synth.run_real` | 挑中的全部政策都写（含 LLM 失败组）；全部已补时仍回补缺口 |

原则：**无表建表，有表 UPSERT**。响应字段 `effect_rows` = 当次写入 + 回补。批次号沿用 `…EFFECT-GAPFILL` / `…EFFECT-SYNTH`。

### 读入口

| 调用方 | 行为 |
|---|---|
| `polan/shenzhen_board.py` | 城市截面读出后，只补尚未启动、无支持对象、无反馈的行 |
| 配置区「落地执行率 / 受益覆盖广度 / 反馈满意度」demo 常量 | **不**读本表、**不**进接口 |

### 禁止

- 旁路新建与两入口无关的灌数按钮当主写路径  
- 把缺项行写入 ODS / 正式 DWD / ADS / 供应方库  
- 空值充 0、发布日当实施日  

签收证据：`agent-handoffs/政策模块-E7/POL-IMPL-EFFECT-MOCK-VIA-UI-L01.md`。

## POL-MOCK-BTN-A01 八张新表（as-built，空表）

可执行语句：`demo-algo-ent-analysis/scripts/ensure_gapfill_policy_btn_tables.py`（`--check` 不连库，`--apply` 写前 `assert_demo_mysql_targets`）。只 `CREATE TABLE IF NOT EXISTS`，不 `DROP`、不 `DELETE`、不灌数。

2026-11-09 现网 `DESCRIBE` 列名与下列 CREATE 一致，八张表行数均为 0。唯一键与脚本同名。

每张表都有 `is_mock`、`fill_method`、`gapfill_batch_id`。`metric_id` 留空，不新造指标。闭集取值用中文，不用英文码。

### `gapfill_policy_semantic`（606）

一政策一面一行。业务键 `policy_id` + `facet_name`。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_policy_semantic` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id` varchar(64) NOT NULL COMMENT '演示库政策业务键',
  `facet_name` varchar(16) NOT NULL COMMENT '主旨、适用场景、约束、条款分类',
  `body_text` varchar(512) NOT NULL COMMENT '一句中文',
  `is_mock` tinyint NOT NULL,
  `metric_id` varchar(64) DEFAULT NULL COMMENT '留空，不新造 metric_id',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_policy_facet` (`policy_id`, `facet_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `gapfill_policy_xcmp`（610）

一对政策、一种关系一行。业务键 `policy_id_a` + `policy_id_b` + `relation_name`。写入时 `policy_id_a` 取字典序较小的键。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_policy_xcmp` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id_a` varchar(64) NOT NULL COMMENT '字典序较小的政策业务键',
  `policy_id_b` varchar(64) NOT NULL COMMENT '字典序较大的政策业务键',
  `relation_name` varchar(16) NOT NULL COMMENT '共性、差异、互补、冲突',
  `body_text` varchar(512) NOT NULL COMMENT '一句中文',
  `is_mock` tinyint NOT NULL,
  `metric_id` varchar(64) DEFAULT NULL COMMENT '留空，不新造 metric_id',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_pair_relation` (`policy_id_a`, `policy_id_b`, `relation_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `gapfill_policy_xcmp_viz`（611）

图种 × 政策对 × 对照项一行。业务键 `chart_kind` + `policy_id_a` + `policy_id_b` + `item_name`。只存对照数，不另算全景分布。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_policy_xcmp_viz` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `chart_kind` varchar(16) NOT NULL COMMENT '对比表、柱、雷达',
  `policy_id_a` varchar(64) NOT NULL,
  `policy_id_b` varchar(64) NOT NULL,
  `item_name` varchar(64) NOT NULL COMMENT '对照项中文名',
  `compare_value` decimal(18,4) NOT NULL COMMENT '对照数，不是新指标',
  `is_mock` tinyint NOT NULL,
  `metric_id` varchar(64) DEFAULT NULL COMMENT '留空，不新造 metric_id',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_chart_pair_item` (`chart_kind`, `policy_id_a`, `policy_id_b`, `item_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `gapfill_policy_xcmp_summary`（613）

一对政策、一种输出一行。业务键 `policy_id_a` + `policy_id_b` + `summary_kind`。612 的用户配置不进本表。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_policy_xcmp_summary` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id_a` varchar(64) NOT NULL,
  `policy_id_b` varchar(64) NOT NULL,
  `summary_kind` varchar(16) NOT NULL COMMENT '对比摘要、核心结论',
  `body_text` varchar(512) NOT NULL COMMENT '一句中文',
  `is_mock` tinyint NOT NULL,
  `metric_id` varchar(64) DEFAULT NULL COMMENT '留空，不新造 metric_id',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_pair_kind` (`policy_id_a`, `policy_id_b`, `summary_kind`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `gapfill_policy_report_analysis`（614）

一政策一面一行。业务键 `policy_id` + `aspect_name`。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_policy_report_analysis` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id` varchar(64) NOT NULL,
  `aspect_name` varchar(16) NOT NULL COMMENT '实施效果、经济社会、产业影响、趋势',
  `conclusion_text` varchar(512) NOT NULL COMMENT '一句结论',
  `is_mock` tinyint NOT NULL,
  `metric_id` varchar(64) DEFAULT NULL COMMENT '留空，不新造 metric_id',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_policy_aspect` (`policy_id`, `aspect_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `gapfill_policy_report_insight`（615）

一政策一种洞察一行。业务键 `policy_id` + `insight_kind`。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_policy_report_insight` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id` varchar(64) NOT NULL,
  `insight_kind` varchar(16) NOT NULL COMMENT '观点、建议、风险、机遇',
  `body_text` varchar(512) NOT NULL COMMENT '一句中文',
  `is_mock` tinyint NOT NULL,
  `metric_id` varchar(64) DEFAULT NULL COMMENT '留空，不新造 metric_id',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_policy_kind` (`policy_id`, `insight_kind`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `gapfill_policy_report_body`（616，618 只读）

一政策一模块一行。业务键 `policy_id` + `section_name`。正文在 `body_text`，不写 PDF / Word。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_policy_report_body` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id` varchar(64) NOT NULL,
  `section_name` varchar(64) NOT NULL COMMENT '模块名，中文',
  `body_text` text NOT NULL COMMENT '正文写在行里，不写文件',
  `is_mock` tinyint NOT NULL,
  `metric_id` varchar(64) DEFAULT NULL COMMENT '留空，不新造 metric_id',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_policy_section` (`policy_id`, `section_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `gapfill_policy_report_trace`（617）

一政策、一方向、一条结论一行。业务键 `policy_id` + `direction_name` + `conclusion_key`。不并入 `gapfill_policy_lineage_index`。

```sql
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_policy_report_trace` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id` varchar(64) NOT NULL,
  `direction_name` varchar(16) NOT NULL COMMENT '结论到原文、原文到结论',
  `conclusion_key` varchar(64) NOT NULL COMMENT '这条结论的中文短名',
  `conclusion_text` varchar(512) NOT NULL,
  `source_excerpt` varchar(512) NOT NULL COMMENT '原文摘句',
  `is_mock` tinyint NOT NULL,
  `metric_id` varchar(64) DEFAULT NULL COMMENT '留空，不新造 metric_id',
  `gap_item` varchar(128) NOT NULL,
  `fill_method` varchar(16) NOT NULL,
  `gapfill_batch_id` varchar(64) NOT NULL,
  `generated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_policy_direction_key` (`policy_id`, `direction_name`, `conclusion_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 210 / 211 现网已有（本单不重建）

`gapfill_policy_audience_feedback` 现网 591 行，`gapfill_policy_assessment_report` 现网 2 行。列与 `lumen-algo-py/scripts/mysql/gapfill_policy_audience.sql`、`gapfill_policy_assessment.sql` 的 CREATE 一致（不含其中的 `DELETE` / `INSERT`）。`--apply` 对这两张只执行 `CREATE TABLE IF NOT EXISTS`，行数未变。

两表都有 `is_mock`、`fill_method`、`gapfill_batch_id`。反馈表 `policy_id` 可空；评估报告无 `policy_id`，范围写在 `scope_text`。
