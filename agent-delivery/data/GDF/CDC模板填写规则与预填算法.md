# CDC 模板填写规则与预填算法

> **读者**：GDF 数据中台产线（导入 CDC 作业）+ 本侧 data / 架构  
> **日期**：2026-08-13  
> **协作 / Cursor / 任务认领**：同目录 [`GDF协作指南.md`](GDF协作指南.md)  
> **现行交付**：企业 `GDF-ENT-WORKPACK-v2` 预填草稿  
> **性质**：对齐说明。v1 `执行结果/` 只当壳和对照样例，不是现行表清单。

本侧产出带 `预填-DRAFT`。GDF 导入跑通回传的才叫 `执行结果/`。

---

## 1. 两张表分别干什么

| 文件 | GDF 模板名 | 含义 |
|------|------------|------|
| `1、贴源_*.xlsx` | `SRC_DB_CDC_TEMPLATE` | Wave A：源库 `gkx` → ODS **同名镜像** |
| `2、明细数据_*.xlsx` | `DWD_CDC_TEMPLATE` | Wave B：ODS → 项目 DWD |

`#ODS_SCHEMA#` / `#DWD_SCHEMA#` / `#SRC_SCHEMA#` 是 GDF 占位符，**不要展开成真库名**。

企业 v2.1 施工真源：

- 贴源清单：`02-WaveA-贴源表清单.yaml`
- Mapping：`09-企业域-ETL-Mapping明细-源表到DWD.md`（短版 `09` v4 不当字段矩阵）
- 建表：`10-DWD-MySQL-DDL/`

---

## 2. 贴源表（Wave A）填写规则

**只填「索引」**（缺表另进「没找到的表」）。v2 草稿**不再带转换页**，避免把 v1 的 `year → yearTime` 带进来。

从第 3 行起，一行一张源表：

| 列 | 填法（v2） |
|----|------------|
| A | 序号 1…n（按 `02` 清单顺序） |
| B | `#ODS_SCHEMA#.{表名}` |
| C | 中文名（`02` 的 cn） |
| D | `EDW_ODS` |
| E | `#SRC_SCHEMA#.{同名表}` |
| F | `GKX_DB` |
| G | `SRC_ENT` |
| H | `全量` |
| I | `is_deleted = 0` |
| J | `删表重建` |
| O | 空（v2 无转换页） |

缺表：进「没找到的表」，`J=清空数据`，**不从清单删行**。

---

## 3. 明细表（Wave B）填写规则

### 3.1 索引

一行 = 一张目标 DWD。

| 列 | 填法 |
|----|------|
| A | 序号 |
| B | `#DWD_SCHEMA#.{dwd_table}` |
| C | **DWD 作业中文名**（如「企业主数据输出」），不是源表中文名 |
| D | `ENT` |
| E | `删表重建` |
| G | `正常插入` |
| J / K | **空**（作业频率、运行区间 DRAFT 未填） |
| L | **同名 Sheet**（= C） |

### 3.2 业务页：只有一种壳

全部是「来源数据 \| 数据结果」，**没有第二种扁 Mapping 页**。

```
A1 = 返回
A2:J2 = 来源数据     K2:X2 = 数据结果   （合并单元格保留）

行3 左：别名 | 数据类型 | 数据源 | 表名 | 中文名
行3 右：关联条件 | 过滤条件 | 分组 | 排序 || 别名 | … | 中文名

行4 左：T1 | 数据表 | EDW_ODS | #ODS_SCHEMA#.{src} | 源表中文
行4 中：K = 视图定义（T1 / JOIN 文本 / IVn）
行4 右：O = MainOutput 或 IVn；P = 输出表 或 临时视图；R = #DWD_SCHEMA#.{dwd}

行5 左：源字段表头
行5 右：步骤 | 映射规则 | … | 目标字段表头

行6+：L = 表达式，P = 目标英文字段   ← GDF 执行认这两列
```

请确认这三点：

1. **GDF 跑批认的是 L 列表达式 + 右栏 P**，不是左栏 A/B 源字段清单（左栏可空）。
2. **K 列是视图定义**：单表写 `T1`，多表写 JOIN 全文，中间结果写 `IVn` 或 `IV2 left join IV1 …`。
3. 左右栏 **共享行号**（拉链）：左边在堆 T2 源表块时，右边可以同时在写映射或下一块 IV。不要从第 6 行当一张扁表清空。

### 3.3 四种作业（同一骨架，K/O/M 不同）

**① 单源直出**（高管、资讯、多数 `risk_*`）

`K=T1`，`O=MainOutput`，`L=T1.col` → `P=目标字段`。

**② 多源 JOIN 直出**（JOIN 写在**第一块 K4**，不写在 Tn 行）

| 页 | 驱动 | K |
|----|------|---|
| 企业主数据 | T1 机构 | `T1 left join T2 on org_id`（T2=上市） |
| 企业扩展 | T1 机构 | T2 经营 + T3 上市，均 `org_id` |
| 招投标 | T1 `dwd_bid_base_out` | T2 中标候选人，键 **`u_id`** |
| 产业链 | **T2 企业标签** | `T2 left join T1 on industry_code + industry_link_code and T1.is_deleted=0` |

v2 **不 JOIN** 采购代理 / 标的（`09` §2.4 暂不映射）。缺源的目标列写 `NULL`，不编造。

**③ 财务 IV 流水线**（`enterprise_finance_history`）

1. IV1 ← T1 年报，过滤 `org_id is not null`，年度用 **`year`（禁止 yearTime）**
2. IV2 ← T2 上市财务，年度 `SUBSTRING(occur_period,1,4)`
3. IV3 ← `IV2 left join IV1 on org_id + data_year`，`COALESCE(IV2, IV1)` 上市优先
4. MainOutput ← IV3

年报金额若明细写「单位待三方确认」→ **不自动 /10000**。

**④ 风险预聚合**（`enterprise_risk_summary`）

每类风险一块：`M=Tn.org_id`，`COUNT(DISTINCT 业务主键)`，`U` 含「预聚合」。

- **v1 回件是宽表**（`abnormal_count`… + 主数据驱动 LEFT JOIN）。
- **v2 草稿按现行 DDL 改成长表**：各 IV 预聚合后 `UNION ALL` 成 `org_id + risk_type + total_count + current_count + history_count + latest_date`。
- `current/history` 尚未按 `remove_date` 细拆，会在生成报告里标明。

### 3.4 硬规则

| 编号 | 规则 | v2 草稿现状 |
|------|------|-------------|
| H1 | 年报字段保持 `year`，不要改成 `yearTime` DOUBLE | 已按此填 |
| H2 | 注册资本源元 → 目标万元，必须 `/ 10000.0` | 已按此填 |
| H3 | 「单位待三方确认」不自动除 | 已按此填，进 warnings |
| H4 | 上市财务明细若写 ÷10000 则除 | 按明细 |
| H5 | `is_listed`：含「上市」用 `LIKE '%上市%'`，不要只等 `已上市` | 已按此填 |
| H6 | `org_id` 复用源值，禁止自造 | 已按此填 |
| H7 | 默认 `is_deleted = 0` | Wave A 已填 |
| H8 | `mirror_only` / 暂不映射：只贴源，不进明细索引 | 招投标代理/标的等已跳过 |
| H9 | 缺表登记，不删除清单行 | 已按此填 |
| H10 | 技术字段可镜像，不得映射成业务主口径（除非明细明文） | 已按此填 |

---

## 4. Python 预填算法

脚本：`gkx-orchestration/scripts/gdf-cdc/parse_workpack.py` → `fill.py`。填表用 **openpyxl**。

```
派单包 02 yaml + 09 Mapping 明细
        │
        ▼
 parse  → inventory.json（表清单 + 字段 + JOIN 源 + warnings）
        │
        ▼
 fill   克隆 GDF 空白壳（只借样式 / 合并格 / 模板名）
        清空已有格子（不拷 v1 回件内容）
        按 inventory 重写索引 + 业务页
        │
        ▼
 预填-DRAFT.xlsx  +  GENERATION-REPORT.md
```

### 4.1 解析

- Wave A 表：只认 `02-WaveA-贴源表清单.yaml`。
- Wave B 目标表 / 字段：只认 README 指定的 Mapping 明细。
- §2.4 暂不映射、`mapping: mirror_only` → 不进 Wave B。
- 表达式：直拷 `Tn.col`；逻辑里写了 ÷10000 才除；`occur_period` 抽年；`is_listed` 用 `LIKE`。

### 4.2 填表明细页：左右栏拉链

对每张目标表选 ①直出 / ②JOIN / ③财务 IV / ④预聚合，生成两路事件队列，**从第 3 行起同一行号写入**：

- **左队列**：源表头 → `Tn` 别名行 → 字段表头 →（可选）源字段；多源则再追加 T2 块。
- **右队列**：关联条件表头 → `MainOutput`/`IVn` 别名行 → 映射表头 → `L/P` 行；IV 块插在右队列里。

导入后某页对不齐时，优先看：

- K4 是否为整段 JOIN
- L 是否在「映射规则」列
- Sheet 名是否等于索引 L

### 4.3 v2 风险汇总算法（与 v1 回件不同）

```
每类风险 IVn：按 org_id 分组，COUNT(DISTINCT 业务id)
IV10 = UNION ALL (
  SELECT org_id, '{type}' AS risk_type, total_count,
         total_count AS current_count, 0 AS history_count, NULL AS latest_date
  FROM IVn
)
MainOutput ← IV10
  org_id, risk_type, total_count, current_count, history_count, latest_date
```

`risk_type` 取值：`abnormal` / `punishment` / `illegal` / `tax_punish` / `judicial_case` / `dishonest` / `executed` / `bankruptcy` / `bankruptcy_party`。

---

## 5. 建议会上确认

1. 明细页是否只认「数据结果」这一种壳（我们按 v1 回件 17 页全是这套来填）。
2. 风险汇总 v2 用长表 UNION、不再用宽表 JOIN 主数据，GDF 作业引擎能否直接跑。
3. 年报不要 `yearTime`；若 GDF 侧仍依赖转换页，请给新规则，本侧不会从 v1 回件倒灌。
4. 作业频率 / 运行区间草稿留空，是否由 GDF 导入后补调度。

---

## 6. 现行草稿位置

`agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v2/预填作业/`

- `1、贴源_预填-DRAFT.xlsx`（索引 47 表）
- `2、明细数据_预填-DRAFT.xlsx`（34 张目标表）
- `GENERATION-REPORT.md`

内部实现备忘（不对外）：`.cursor/skills/gkx-gdf-cdc-workpack/`
