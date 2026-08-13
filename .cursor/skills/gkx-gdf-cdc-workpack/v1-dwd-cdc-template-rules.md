# v1 `DWD_CDC_TEMPLATE` 填写规则（分析稿）

> **对象**：`GDF-ENT-WORKPACK-v1/执行结果/2、明细数据_模板.xlsx`  
> **模板名**（索引 A1/B1）：`DWD_CDC_TEMPLATE`  
> **性质**：GDF 已填过的作业壳 + 样例，**不是**现行 `02`/`09` 表清单。生成 v2 只克隆布局与占位符，表名/字段以现行工作包为准。  
> **方法**：`officecli view outline` + 逐页格子核对。  
> **日期**：2026-08-13

---

## 1. 工作簿结构

officecli outline：18 个 Sheet。

| Sheet | 角色 |
|-------|------|
| `索引` | 作业目录，1 行 = 1 张目标 DWD |
| 其余 17 页 | **全部**是同一套「来源数据 / 数据结果」布局，不是两套模板 |

v1 索引 17 张目标表：

`enterprise_base` / `executive` / `extra` / `finance_history` / `industry_chain` / `news` / `bid` → 9 张 `risk_*` → `enterprise_risk_summary`。

**规则 1.1** 索引 `L`（数据映射）= Sheet 名 = 索引 `C`（表中文名）。  
**规则 1.2** 中文名是 **DWD 作业名**（「企业主数据输出」），不是源表中文名（源表中文写在映射页 `E4`，如「国内机构基本信息」）。

### 1.1 索引列（从第 3 行起）

| 列 | 表头 | v1 填法 |
|----|------|---------|
| A | 序号 | 1…n |
| B | 全局标识 | `#DWD_SCHEMA#.{dwd_table}` |
| C | 表中文名 | 与 Sheet 名相同 |
| D | 业务主题 | `ENT` |
| E | 表初始化方式 | `删表重建` |
| F | 自定义清数条件 | 空 |
| G | 插入模式 | `正常插入` |
| H | 分区配置 | 空 |
| I | 数据描述 | 空 |
| J | 作业频率 | **空**（outline 报 error cell，DRAFT 允许） |
| K | 运行区间 | **空** |
| L | 数据映射 | 同名 Sheet |

`#DWD_SCHEMA#` / `#ODS_SCHEMA#` 是 GDF 占位符，不要展开成真库名。

---

## 2. 映射页通用骨架（17 页相同）

左右分栏，`A2:J2` =「来源数据」，`K2:X2` =「数据结果」。`A1` =「返回」。

```
行3 左：别名 | 数据类型 | 数据源 | 表名 | 中文名
行3 右：关联条件 | 过滤条件 | 分组统计条件 | 排序条件 || 别名 | 数据类型 | 数据源 | 表名 | 是否去重 | 行数限制 | 中文名 | 扩展配置

行4 左：T1 | 数据表 | EDW_ODS | #ODS_SCHEMA#.{src} | 源表中文
行4 中：K=关联 SQL；L=过滤；M=分组（仅预聚合）
行4 右：O=MainOutput 或 IVn；P=输出表 或 临时视图；Q=EDW_DWD；R=#DWD_SCHEMA#.{dwd}；U=作业中文名

行5 左：序号 | 英文名称 | 中文名称 | 类型 | …（源字段表头）
行5 右：步骤 | 映射规则 | 描述 || 序号 | 英文名称 | 中文名称 | 类型 | …（目标字段表头）

行6+ ：L=表达式；O/P/Q=目标序号/英文字段/中文名
```

**规则 2.1** 源表声明在 **左栏 A–E**；JOIN/过滤/分组在 **K/L/M**；真正写出 DWD 的是 **右栏 O–X**。  
**规则 2.2** 映射表达式在 **L 列**（表头叫「映射规则」），不是 A 列。A–C 是源字段清单，可填可不填（「经营异常」行 6+ 左栏为空，只填了右栏）。  
**规则 2.3** 多源时：T1 字段清单结束后，再插一块「别名/数据类型…」表头 + `Tn` 行 + 该表字段清单（见「企业主数据输出」R43–T2）。JOIN 全文写在 **第一块的 K4**，不写在 Tn 行。  
**规则 2.4** `O4=MainOutput` 表示本块直接落目标表；`O4=IVn` 且 `P=临时视图` 表示中间结果，后面还要再接到 MainOutput。

---

## 3. 四种作业写法（按复杂度）

同一骨架，K/O/M 用法不同。

### 3.1 单源直出（最多）

例：经营异常、高管、资讯、多数 `risk_*`。

- 只有 T1；`K4=T1`；`O4=MainOutput`；`R4=#DWD_SCHEMA#.{dwd}`
- `M4` 空（不做分组）
- `L6+` = `T1.{col}`，`P` = 目标英文字段

这是「一行源字段 → 一行目标字段」的默认形态。

### 3.2 多源 JOIN 直出

| 页 | 驱动 | 关联 |
|----|------|------|
| 企业主数据输出 | T1 `dwd_org_base_info` | `T1 left join T2 on T1.org_id = T2.org_id`（T2=上市 `dwd_org_stock_base`） |
| 企业扩展表输出 | T1 机构 | T2 经营信息 + T3 上市，均 `org_id` |
| 企业招投标输出 | T1 `dwd_bid_base_out` | T2/T3/T4 均 `u_id`（不是 org_id） |
| 企业产业链关联输出 | **T2** 企业标签 | `T2 left join T1 on industry_code + industry_link_code and T1.is_deleted = 0` |

**规则 3.2.1** 默认 JOIN 键是 `org_id`；招投标用 `u_id`；产业链用行业/环节代码。  
**规则 3.2.2** K 里的驱动别名可以不是 T1（产业链 K 以 T2 开头）。  
**规则 3.2.3** 源没有的目标列写 `NULL` 或常量（如 `is_listed` 旁的 `org_size<=NULL`，链主 `is_chain_leader<=0`）。

### 3.3 IV 流水线（财务历史）

三步临时视图，最后 MainOutput：

1. **IV1** ← T1 年报；过滤 `T1.org_id is not null`；金额 `/ 10000.0`；年度 `CONCAT(ROUND(T1.yearTime, 0), '')`
2. **IV2** ← T2 上市财务；过滤 `T2.org_id is not null`；年度 `SUBSTRING(T2.occur_period, 1, 4)`；金额同样 `/10000`
3. **IV3** ← `IV2 left join IV1 on org_id + data_year`；`COALESCE(IV2.*, IV1.*)`，上市优先
4. **MainOutput** ← IV3 → `enterprise_finance_history`

**规则 3.3.1** 两路明细先各自洗成同构 IV，再按业务键合并，不要在一个 JOIN 里同时做单位换算。  
**规则 3.3.2** `data_source` 用字面量 `'annual'` / `'stock'`，合并后再 CASE。  
**规则 3.3.3** v1 把年报 `year` 写成了 `yearTime`。**校准 v1 必须复现**；v2 生产硬规则 H1：源字段保持 `year`。

### 3.4 预聚合 IV + 驱动表（企业风险汇总）

这是指标表写法，**不能**当成 3.1 从第 6 行清空。

每类风险一块（约 5 行一套）：

| 格 | 填法 |
|----|------|
| 左 A | T1…T9 源风险表 |
| K | 通常等于 Tn；破产主表用 `T9 LEFT JOIN T8 ON case_no`（主表可能没有 org_id） |
| M | `Tn.org_id`（分组） |
| O/P/U | `IVn` / `临时视图` / `{中文}预聚合` |
| L 第一行 | `Tn.org_id` → 目标 `org_id` |
| L 第二行 | `COUNT(DISTINCT Tn.{业务id})` → `{type}_count` |

然后：

- **T10** = `#DWD_SCHEMA#.enterprise_base`（已洗主数据当驱动，不是 ODS）
- **IV10** = T10 `LEFT JOIN IV1…IV9 ON org_id`，空计数 `COALESCE(..., 0)`，再加总 `total_risk_count`
- **MainOutput** `K=IV10`，`R=#DWD_SCHEMA#.enterprise_risk_summary`，把 IV10 宽列映到目标表

**规则 3.4.1** `M` 有值 = 预聚合；`M` 空 = 明细直出。  
**规则 3.4.2** 计数用 `COUNT(DISTINCT 业务主键)`，不要 `COUNT(*)` 替代（v1 各块都写了 DISTINCT）。  
**规则 3.4.3** v1 目标是 **宽表**（`abnormal_count`…）。**校准 v1 必须复现宽表**。现行 `10/` 已改成长表 `org_id + risk_type + total_count + …`；v2 生产 MainOutput 按长表，不能把宽表列写进 v2。

---

## 4. 表达式惯例（v1 实填）

| 意图 | v1 写法 | 生成时 |
|------|---------|--------|
| 直拷 | `T1.col` | 照做 |
| 缺源 | `NULL` | 照做，禁止编造 |
| 时间戳 | `current_timestamp` / `NOW()` | 照做 |
| 万元 | `/ 10000.0` | 明细写了「万元/÷10000」才除 |
| 上市 | `listing_status = '已上市' OR T2.stock_code is not null` | 现行 H5：含「上市」用 `LIKE '%上市%'`，不要只等精确「已上市」 |
| 年度 | 年报用了 `yearTime`；上市用 `SUBSTRING(occur_period,1,4)` | 年报用 `year`；上市 SUBSTRING 可留 |
| 日期 | `CAST(T1.publish_time AS DATE)` | 可留 |
| 金额单位分叉 | 招投标 `CASE amount_unit WHEN '万元' THEN *10000 WHEN '亿元' THEN *1e8` | 按明细 |
| 角色 | 招投标 CASE 中标/候选人/采购代理 | 按明细 |
| 合并优先 | `COALESCE(IV2, IV1)` | 财务：上市盖年报 |
| 预聚合 | `COUNT(DISTINCT id)` + `COALESCE(count,0)` | 指标表 |

技术列 `EDW_SRC_SYSTEM` / `EDW_SYS_DATE` / `EDW_DATA_DATE` 出现在主数据左栏末尾，**没有**映到右栏 P——不要当成业务字段输出。

---

## 5. 和生成器的差距（分析结论）

1. **没有「普通 Mapping 页」这第二种壳。** 17 张业务页都是数据结果布局。脚本若按「第 4 行 T1、从第 6 行当一张扁表」去清空，会拆掉：多源 T2 块、财务 IV 链、风险预聚合。
2. **GDF 认的是 L 列表达式 + 右栏 P 目标字段**；只改 A/B 当源字段不够。
3. **K 列是视图定义**：单表写 `T1`，多表写 JOIN 文本，IV 写 `IVn` 或 `IVa left join IVb`。
4. **索引中文名必须来自 DWD 作业名**，不能用 `02` 源表 cn。
5. v1 样例里有两处 **不要倒灌进 v2**：`yearTime`；`is_listed` 精确等于「已上市」。
6. v1 招投标 JOIN 了采购代理/标的物；现行 `09` §2.4 这两张 **暂不映射**，生成时不要因为 v1 有就加回来。

---

## 6. 生成时的套用顺序

1. 克隆本 xlsx 当壳（样式、合并单元格、表头、占位符）。
2. 按现行 `09` 重写 **索引**（行数随目标表变）。
3. 每张目标表选 3.1 / 3.2 / 3.3 / 3.4 之一，在对应 Sheet（或复制一页骨架）里填 T/K/L/M/O/R。
4. 指标表保留预聚合块；MainOutput 列对齐现行 `10/` DDL。
5. 抽检：Sheet 名 = 索引 L；`K2=数据结果`；风险汇总 `U` 含「预聚合」。v2 无 `yearTime`；v1 校准年报转换页必须有 `yearTime`。

---

## 7. v1 贴源索引校准规则（与执行结果逐格对齐）

从 v1 `02` 生成索引，不要抄执行结果行。再套这些 GDF 实填规则：

1. **序号 = yaml 中的 1-based 下标**（不是压成 1…n）。`dwd_org_org_product_info` 在 yaml 是第 4 条，索引行放到**最后**，`A` 仍写 `4`。
2. **`dwd_forg_college_org_info` 进「没找到的表」**，`J=清空数据`，序号仍为 yaml 下标 `33`。
3. **无过滤**：`dwd_org_base_info`、`dwd_org_org_product_info` 的 `I` 留空；其余 `is_deleted = 0`。
4. **转换页**（索引 `O` 指向同名 Sheet）：
   - 年报财务信息：`year` → `yearTime` DOUBLE（校准专用）
   - 国外机构基本信息：`created_time` / `updated_time` / `create_time` → DATETIME（记录号均为 `2`）
   - 产业动态资讯：`publish_date` 零日期 `CASE` 成 NULL

## 8. 左右栏拉链（数据结果页填写引擎）

左 `A–J` 与右 `K–X` 是两路事件，**共享行号**：

1. 行 1–2 壳：`返回` / `来源数据` | `数据结果`（合并单元格保留）。
2. 行 3 起：每一行左边一个事件、右边一个事件（可空）。
3. 左事件：源表头 `别名…` → `Tn 数据表` → 字段表头 → 源字段行。
4. 右事件：关联条件表头 → `MainOutput`/`IVn` 别名行 → 映射表头 → `L` 表达式 + `P` 目标字段。
5. 多源时 T2 块插在左栏队列尾；IV 块插在右栏队列里。不要从第 6 行当扁表清空。
