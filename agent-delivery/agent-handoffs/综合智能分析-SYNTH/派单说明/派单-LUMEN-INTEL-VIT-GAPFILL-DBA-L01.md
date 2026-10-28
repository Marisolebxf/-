# 派单说明 · LUMEN-INTEL-VIT-GAPFILL-DBA-L01（真人执行单）

> **派发给**：human:徐滕强（主执行）、human:淮政玮（知会 / 验收）
> **登记人**：human:唐绍祖 · 2026-10-29
> **优先级**：P1 —— 卡着「区域创新活力分析」第 4、5 单收尾，提测门禁 2026-11-05
> **建议完成时间**：2026-11-02 前（给我留灌数 + 实算 + 关单的时间）
> **预计耗时**：10 分钟（复制粘贴执行 + 半分钟核对）

---

## 一、一句话说明白要麻烦你们做什么

在 `192.168.88.43:3306` 这台 MySQL 上，**帮我建一个新库 `gkxlumenx_gapfill` 和三张空表，并把这张库的写权限授给我的应用账号 `gkxlumenx`**。建完我这边就能灌数，把区域创新活力分析的最后两个子任务（缺项表 + 灌数）彻底关掉。

## 二、为什么必须麻烦你们（我自己为什么不能建）

我的应用账号 `gkxlumenx`@`%` 在这台库上只有现有业务库的表级权限，**没有 `CREATE DATABASE`（建新库）和 `GRANT`（授权给别人）的权限**。已实测：

```sql
CREATE DATABASE gkxlumenx_gapfill;
-- ERROR 1044 (42000): Access denied for user 'gkxlumenx'@'%' to database 'gkxlumenx_gapfill'
```

所以建新库、建表、授权这三步，必须由有 root / DBA 权限的账号执行。

## 三、这三张表是干嘛的（30 秒背景）

区域创新活力分析要给深圳算「科技 / 产业 / 人才 / 政策」四个维度的活力分。其中有三个数据在现有数据库里**没有来源列**（缺口）：

| 缺口数据 | 对应表 |
|---|---|
| 新产品销售收入占比（产业维） | `gapfill_synth_new_product_sales_ratio` |
| 研发人员数量（人才维） | `gapfill_synth_rd_employee` |
| 政策实施效果指数（政策维） | `gapfill_synth_policy_effect` |

按数据血缘规约（`data-lineage-policy.md` §2.4 / `architecture-baseline.md` D16），这类补值**只能放进独立的 `gkxlumenx_gapfill` 库**，绝不许混进正式的 ODS/DWD/ADS 或供应方库。表建好后是**空表**，行数据由我这边的 Python 灌数脚本（`LUMEN-INTEL-VIT-GAPFILL-DATA-L01`）写入。

## 四、执行环境

| 项 | 值 |
|---|---|
| MySQL 实例 | `192.168.88.43:3306`（外网映射 `111.198.38.90:34306`） |
| 执行账号要求 | 有 `CREATE DATABASE` / `GRANT` 权限的账号（root / DBA） |
| 新库名 | `gkxlumenx_gapfill` |
| 被授权账号 | `gkxlumenx`@`%`（算法服务现有应用账号，**不需要新建**） |

## 五、要执行的 SQL（全文，可直接整段复制）

> 幂等脚本：全部 `IF NOT EXISTS`，重复执行无害。只建库建表授权，**不含任何 INSERT**。

```sql
-- ── 1. 建库 + 授权（需 DBA 权限） ──────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS `gkxlumenx_gapfill`
  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

GRANT ALL PRIVILEGES ON `gkxlumenx_gapfill`.* TO `gkxlumenx`@`%`;
FLUSH PRIVILEGES;

-- 如倾向最小权限，可用下面这行替代上面的 GRANT（对我的用途已足够）：
-- GRANT SELECT, INSERT, UPDATE, DELETE ON `gkxlumenx_gapfill`.* TO 'gkxlumenx'@'%';

-- ── 2. 表 1/3：新产品销售收入占比（活力·产业维缺项） ───────────────────────
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_synth_new_product_sales_ratio` (
  `id`                BIGINT       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `metric_id`         VARCHAR(64)  NOT NULL COMMENT '原指标 ID（M_SYNTH_VIT_INDICATOR）',
  `gap_item`          VARCHAR(64)  NOT NULL COMMENT '缺项键（ind-newprod）',
  `gap_item_name`     VARCHAR(128) NOT NULL DEFAULT '新产品销售收入占比' COMMENT '缺项中文名',
  `city`              VARCHAR(32)  NOT NULL COMMENT '城市编码（深圳市/广州市/…）',
  `year`              INT          NOT NULL COMMENT '统计年（基期 2024）',
  `value`             DOUBLE       NULL COMMENT '补值（占比 0-1；无行=null，禁止 0 占位）',
  `fill_method`       VARCHAR(64)  NOT NULL COMMENT '补值方法（如 同期同省均值/公开统计年鉴）',
  `fill_model`        VARCHAR(64)  NULL COMMENT '补值模型版本（无模型则 NULL）',
  `gapfill_batch_id`  VARCHAR(64)  NOT NULL COMMENT '灌数批次号（DATA 单写入）',
  `generated_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_city_year` (`city`, `year`),
  KEY `idx_batch` (`gapfill_batch_id`),
  KEY `idx_metric` (`metric_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = '活力缺项：新产品销售收入占比（只读；装包 confidence=gapfill）';

-- ── 3. 表 2/3：研发人员数量（活力·人才维缺项） ─────────────────────────────
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_synth_rd_employee` (
  `id`                BIGINT       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `metric_id`         VARCHAR(64)  NOT NULL COMMENT '原指标 ID（M_SYNTH_VIT_INDICATOR）',
  `gap_item`          VARCHAR(64)  NOT NULL COMMENT '缺项键（ind-talent-cnt）',
  `gap_item_name`     VARCHAR(128) NOT NULL DEFAULT '研发人员数量' COMMENT '缺项中文名',
  `city`              VARCHAR(32)  NOT NULL COMMENT '城市编码',
  `year`              INT          NOT NULL COMMENT '统计年',
  `value`             DOUBLE       NULL COMMENT '补值（全时当量人数；无行=null）',
  `fill_method`       VARCHAR(64)  NOT NULL COMMENT '补值方法',
  `fill_model`        VARCHAR(64)  NULL COMMENT '补值模型版本',
  `gapfill_batch_id`  VARCHAR(64)  NOT NULL COMMENT '灌数批次号',
  `generated_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_city_year` (`city`, `year`),
  KEY `idx_batch` (`gapfill_batch_id`),
  KEY `idx_metric` (`metric_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = '活力缺项：研发人员数量（只读；装包 confidence=gapfill）';

-- ── 4. 表 3/3：政策实施效果指数（活力·政策维缺项） ─────────────────────────
CREATE TABLE IF NOT EXISTS `gkxlumenx_gapfill`.`gapfill_synth_policy_effect` (
  `id`                BIGINT       NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `metric_id`         VARCHAR(64)  NOT NULL COMMENT '原指标 ID（M_SYNTH_VIT_INDICATOR）',
  `gap_item`          VARCHAR(64)  NOT NULL COMMENT '缺项键（ind-pol-effect）',
  `gap_item_name`     VARCHAR(128) NOT NULL DEFAULT '政策实施效果指数' COMMENT '缺项中文名',
  `city`              VARCHAR(32)  NOT NULL COMMENT '城市编码',
  `year`              INT          NOT NULL COMMENT '统计年',
  `value`             DOUBLE       NULL COMMENT '补值（效果指数 0-1；无行=null）',
  `fill_method`       VARCHAR(64)  NOT NULL COMMENT '补值方法',
  `fill_model`        VARCHAR(64)  NULL COMMENT '补值模型版本',
  `gapfill_batch_id`  VARCHAR(64)  NOT NULL COMMENT '灌数批次号',
  `generated_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_city_year` (`city`, `year`),
  KEY `idx_batch` (`gapfill_batch_id`),
  KEY `idx_metric` (`metric_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
  COMMENT = '活力缺项：政策实施效果指数（只读；装包 confidence=gapfill）';
```

## 六、执行完的核对（半分钟，两条 SQL）

```sql
-- 应返回恰好 3 行
SELECT table_name FROM information_schema.tables
 WHERE table_schema = 'gkxlumenx_gapfill' AND table_name LIKE 'gapfill_synth_%';

-- 应包含一行针对 gkxlumenx_gapfill 的授权
SHOW GRANTS FOR 'gkxlumenx'@'%';
```

## 七、回执方式

执行完成后，在本文末尾「执行回执」处追加一行（日期 / 执行人 / 核对结果），或在项目群里 @唐绍祖。我收到回执后立刻：灌数 → 实算验证 → 把五条活力指标的 D4 改 live → 关 `LUMEN-INTEL-VIT-GAPFILL-L01` 和 `LUMEN-INTEL-VIT-GAPFILL-DATA-L01` 两单。

## 八、边界承诺（不会发生的事）

- 不动现有任何 `gkxlumenx_*` 业务库；不写 ODS/DWD/ADS；不碰供应方库。
- 三张表建好后是空表，`COUNT(*)` 应为 0；不改任何指标的 D4 状态。
- 生产配置不读这个库，只有活力计算的 Python 装包只读它。

## 关联文档

| 内容 | 位置 |
|---|---|
| 任务登记（本单） | `agent-delivery/task-registry.yaml` → `LUMEN-INTEL-VIT-GAPFILL-DBA-L01` |
| DDL 脚本正本 | `repos/lumen-algo-py/vendor/entan-py/scripts/mysql/create_gapfill_synth.sql`（唐绍祖工作区） |
| 建表任务（读路径已完成） | 同目录 `派单-LUMEN-INTEL-VIT-GAPFILL-L01.md` |
| 灌数任务（等本单放行） | 同目录 `派单-LUMEN-INTEL-VIT-GAPFILL-DATA-L01.md` |
| 通俗背景解读 | `local-workspace/docs/tasks/construct/1028_淮哥大任务/06-通俗解读.md`（唐绍祖工作区） |

---

## 执行回执

| 日期 | 执行人 | 核对结果（3 表 / COUNT=0 / GRANTS） | 备注 |
|---|---|---|---|
| — | — | — | — |
