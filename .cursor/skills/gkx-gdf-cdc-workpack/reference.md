# CDC 模板与工作包约定

## 工作包目录

```
agent-delivery/data/GDF/派单包/{域}/GDF-{CODE}-WORKPACK-vN/
```

| 域 | CODE 例 | 现行包（随仓库更新，以 README 为准） |
|----|---------|--------------------------------------|
| 企业 | ENT | `企业/GDF-ENT-WORKPACK-v2` |
| 人才 | TAL / 未建则停止 | 尚无则不要发明表清单 |
| 专题 | TPC / 未建则停止 | 尚无则不要发明表清单 |

`02` 的 `groups[].tables[]` 至少含 `name` / `cn` / `priority`。可选 `mapping: wash | mirror_only`。

Mapping 真源文件名以该包 README 为准。企业 v2.1：**只认** `09-企业域-ETL-Mapping明细-源表到DWD.md`。`09-…v4.md` 是导读。

## 两张 CDC 的角色

| 文件 | 模板名 | 内容 |
|------|--------|------|
| `1、贴源_*.xlsx` | `SRC_DB_CDC_TEMPLATE` | Wave A：源 `gkx` → ODS 同名镜像 |
| `2、明细数据_*.xlsx` | `DWD_CDC_TEMPLATE` | Wave B：ODS → 项目 DWD |

本技能产出带 `预填-DRAFT`。GDF 跑通回传的才叫 `执行结果/`。

## Wave A 索引列（1-based，与 GDF 壳一致）

A 序号 · B 全局标识 `#ODS_SCHEMA#.{table}` · C 中文名 · D 目标数据源 `EDW_ODS` · E 来源表名 `#SRC_SCHEMA#.{table}` · F 来源数据源 `GKX_DB` · G 来源系统 `SRC_ENT`（它域按 `01` 词典改） · H `全量` · I 抽取过滤（默认 `is_deleted = 0`） · J `删表重建` · O 扩展值 Sheet 名（仅当有转换页）

## Wave B 索引列

A 序号 · B `#DWD_SCHEMA#.{dwd_table}` · C 表中文名 · D 业务主题（企业 `ENT`，它域用工作包代码） · E `删表重建` · G `正常插入` · L 数据映射 = 同名 Sheet

Wave B 业务页**全部**是「来源数据 | 数据结果」布局（没有第二种扁 Mapping 页）。索引 C/L 用 **目标表中文名**（如「企业主数据输出」）。左右栏按同一行号拉链填写，见 `v1-dwd-cdc-template-rules.md` §8。

v2 生产：`enterprise_risk_summary` MainOutput 对齐 `10/` 长表（`org_id` / `risk_type` / `total_count` …）。v1 校准复现宽表 `abnormal_count`…。

## Hard rules

来自 v1 回件审查 + 企业 Mapping 明细 v1.2。它域若明细有明文，以明细为准。

| ID | 规则 |
|----|------|
| H1 | 不把 `year` 改名为 `yearTime`，不改成 DOUBLE |
| H2 | `registered_capital_value` → `registered_capital` 必须 `/ 10000.0`（源元、目标万元） |
| H3 | 年报金额「单位待三方确认」→ 不自动 `/10000`，写入 warnings |
| H4 | 上市财务 `stock_finance_info` 明细若写 ÷10000 则除 |
| H5 | `is_listed`：明细若写「含上市 → 1」，用 `LIKE '%上市%'`，不要只等 `已上市` |
| H6 | `org_id` 复用源值，禁止自造 |
| H7 | 默认 `is_deleted = 0`；无列则报告，不留空过滤 |
| H8 | 明细 §2.4「暂不映射」或 `mapping: mirror_only` 不进 Wave B |
| H9 | 缺表登记，不删除清单行 |
| H10 | 技术字段可镜像，不得映射成业务主口径（除非明细明文） |

## 解析 Mapping 明细

- §2.1 直接 / §2.2 关联 / §2.3 指标 / §2.5 国外 → Wave B 目标表清单（目标列可含 `a + b`，拆开）
- §2.4 暂不映射 → `mirror_only`
- §3 逐表 `| 源字段 | 目标字段 | 映射类型 | 转换逻辑 |` → 字段行。目标为 `—` 或类型「不映射」则跳过；「自增」跳过

## 模板壳从哪来

企业第一次生成：可克隆

`派单包/企业/GDF-ENT-WORKPACK-v1/执行结果/1、贴源_模板.xlsx`

`…/2、明细数据_模板.xlsx`

只复制样式与模板名，索引与 Mapping 行必须按现行 `02`/`09` 整表重写。

填写格子的完整规则（四种作业写法 + v1 校准索引/拉链）见 [v1-dwd-cdc-template-rules.md](v1-dwd-cdc-template-rules.md)。

**给 GDF 对齐用的对外说明**：编排仓 `agent-delivery/data/GDF/CDC模板填写规则与预填算法.md`。协作 / Cursor / 认领：`agent-delivery/data/GDF/GDF协作指南.md`。v1 校准产出在工作包 `校准生成/`，不要写进 `执行结果/`。
