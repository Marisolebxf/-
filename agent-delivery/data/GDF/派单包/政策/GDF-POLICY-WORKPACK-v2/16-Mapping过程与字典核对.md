# 16 — Mapping 过程与字典核对

> **日期**：2026-10-26  
> **读者**：GDF 产线、本侧数据  
> **性质**：核对记录。**不改** `09` 列规则，不重开 MAP-01，不把下面实值写成白名单。  
> **施工仍只认**：[09-政策域-ETL-Mapping明细-源表到DWD.md](09-政策域-ETL-Mapping明细-源表到DWD.md)  
> **对照**：要素库「国内政策要素库 / 国外政策要素库」值域列；国内库快照 `gkx.dwd_policy_base` 20,000 行（2026-10-23，见文末出处）

---

## 1. 过程逻辑

下面几条 `09` 已经写死，产线照做：

- 两张源表洗进同一张 `policy_base_info`。`dwd_policy_base` → `source_plane=domestic`，`dwd_global_policy_base` → `source_plane=global`。
- UK 永远是 `(source_plane, policy_id)`。`policy_id` 用 ODS `id` 原文。禁止哈希，禁止 `gbl:` 前缀。
- 取数不过滤。`is_deleted`、`is_history` 原样写入。空 `id` 丢弃。国际 `organ` 或 `publish_date` 为空则丢弃并计数。
- 国内 `status` 禁止改成 docstatus 20/30。国内 `rank` 禁止压成 smallint `level`。

产线配置时按下面执行，避免把注释里的举例当成过滤条件：

| 列 | `09` 的写法 | 配置时怎么做 |
|---|---|---|
| `rank` | 「国家级/省级/市级/区县级原文」 | **原样拷贝**。不要用这四个词做白名单。库内还有区级、园区级、双值、空数组（见 §2） |
| `status` | 「只认源文案 有效/失效」 | 值域就是这两个词，原样拷贝。快照里目前全是「有效」 |
| `type` → `policy_type` | 「展示类别原文」 | **原样拷贝**，含字面量 `'NULL'`。不要改成产业/人才/企业扶持。码化仍留给 ADS（QPOL-01） |
| `implementation_date` / `expire_date` | 直接映射 | 快照里这两列全是零日期 `0000-00-00`，不是 SQL NULL。禁止改写成 NULL，禁止因零日期丢行 |
| `policy_support` | 「JSON 原样」 | 快照里全表是小写字符串 `'null'`。目标列类型是 JSON：原样写入前先确认产线把该字符串落成 JSON null，禁止整行失败 |
| `doc_type` | 直接映射 | 源 `varchar(100)`，目标 `varchar(64)`。超长禁止静默截断；先计数再请本侧改列宽 |
| 国际 `category` → `policy_type` | 领域原文 | 要素库长度 5000，目标 `varchar(200)`。超长同样禁止静默截断 |

`status` 的「只认」和 `rank` / `type` 的「原文」不是同一条规则。`status` 的值域在要素库里是闭合的。`rank` 和 `type` 按原文落库，多出来的实值保留。

---

## 2. 字典是否齐

### 2.1 已闭合（与源注释一致）

| 字段 | 取值 | 落点 |
|---|---|---|
| `source_plane` | `domestic` \| `global` | Wave B 派生，见 `09` §1.2 |
| `is_deleted` | `0` 未删除 / `1` 已删除 | 直接映射 |
| `is_history` | `0` 当前 / `1` 历史 / `NULL` 当当前 | 直接映射。`NULL` 不改写成 `0` |
| `insert_remark` | `0` 新增 / `1` 修改 / `2` 补齐 | 只贴源，不进业务列（`04`） |

国内 `status` 的要素库值域是 **失效，有效**。`09` 已写上。快照 20,000 行全是「有效」，「失效」有定义、这批库里还没有。

### 2.2 国内 `rank`：注释里的四级不够

要素库样例是 JSON 数组 `["国家级"]`，值域列为空。描述写的是「国家级/省级/市级/区县级」。

2026-10-23 快照把数组拆开后的原始取值（合计 20,000）：

| 取值 | 行数 |
|---|---|
| 省级 | 7,449 |
| 市级 | 6,149 |
| 市级+省级（双值） | 2,473 |
| 国家级 | 2,174 |
| 区级 | 1,254 |
| 空数组 | 357 |
| 园区级 | 144 |

词是「区级」，不是「区县级」。另有园区级、双值和空数组。`09` 仍按原文拷贝，本文件不增加归并规则（归并是指标侧的事，不在 Wave B）。

### 2.3 国内 `type`：文种表未写进 `09`

要素库值域列为空，样例只有「申报通知」。`09` 写原文，QPOL-01 的码化留给 ADS。QPOL-01 要的是产业/人才/企业扶持，和这列不是同一套码。这列是文种。

快照 20,000 行（含字面量 `'NULL'` 1,862 行，不是 SQL NULL）：

| 取值 | 行数 |
|---|---|
| 其他通知 | 5,782 |
| 政策文件-管理办法/实施方案 | 3,708 |
| 公示公告 | 2,995 |
| 字面量 `'NULL'` | 1,862 |
| 申报通知 | 1,819 |
| 政策文件-指导意见 | 1,697 |
| 政策文件-规划纲要 | 699 |
| 政策文件-其他文件 | 683 |
| 规范性文件-规范条例 | 606 |
| 政策文件-政策指南 | 93 |
| 规范性文件-部门规章 | 34 |
| 政策解读 | 17 |
| 规范性文件-法律法规 | 4 |
| 政策文件-评定标准 | 1 |

Wave B 原样拷贝上表全部取值。不要把字面量 `'NULL'` 改成 SQL NULL。

### 2.4 国际列：要素库没有闭合值域

国外政策要素库的「值域」列为空。下表只有样例，**没有**和国内同口径的全表 distinct。禁止把 DDL 注释或样例当成白名单。

| 源字段 | 目标字段 | 要素库样例 | 说明 |
|---|---|---|---|
| `category` | `policy_type` | `Decision` | 与国内 `type` 分列存放，禁止套国内文种 |
| `language` | `language` | `English` | 开放文本 |
| `geo_region` | `geo_region` | `EU` | 开放文本 |
| `security_class` | `security_class` | `Public` | 注释写「保密等级」，无值域 |
| `version_type` | `version_type` | `Buff cover` | DDL 注释写「草案/正式版等」，与样例不是同一套词。以原文为准 |
| `doc_type` | `doc_type` | （空） | 无值域。长度见 §1 |

`province` / `city` / `theme` 不是闭合枚举。快照里省、市有大量字面 `'NULL'`；`theme` 只有 2 行是标签数组，其余为空。这三列原样拷贝，不另造码表。

---

## 3. 出处

| 材料 | 路径 |
|---|---|
| 国内要素库 | `agent-delivery/data/third-party-source/doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国内政策要素库.csv` |
| 国外要素库 | `agent-delivery/data/third-party-source/doc/md-extract/_csv/版权人才、企业机构、政策数据汇总表__国外政策要素库.csv` |
| 贴源 DDL | `agent-delivery/data/data-design/storage/POLICY/sources/ods-ddl.md` |
| `rank` 分布 | `agent-delivery/metrics/repro/out/M_POLICY_LEVEL_DIST_out.json`（生成 2026-10-24，快照日 2026-10-23） |
| `type` 分布 | `agent-delivery/metrics/repro/out/M_POLICY_TYPE_DIST_out.json` |
| `status` 与零日期 | `agent-delivery/metrics/repro/out/M_POLICY_VALIDITY_RATE_out.json` |

国际表没有这份 20,000 行快照。§2.4 只核到要素库样例和值域列。
