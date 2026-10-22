# CHANGELOG — GDF-ENT-WORKPACK-v4

## v4.0.2（2026-10-22，round2 问询 31 题拍板合入）

> 任务单：`GDF-ENT-WORKPACK-V4R2-L01`。round2 问询（`01-回填表-第2轮.md`，31 题）逐题拍板（human:徐滕强）后合入；回填物见 `交付客户-round2/round3/`。

### 09-企业域-ETL-Mapping明细

| 章节 | 变更 | 问询# |
|---|---|---|
| §1.8 | 新增「源端物理删除兜底」：源库不物理删 + 季度全量比对 | #4/#31 |
| §3.2 | `enterprise_executive.gender` 声明不洗（源无数据） | #14 |
| §3.3 | 三源优先级：不设优先级，`(org_id,data_year,data_source)` 共存 | #19 |
| §3.5 | news 8 缺口字段处置：data_source 直接映射；industry_category/region 关联 base；其余 5 列 NULL | #5(6-13) |
| §3.6 | `end_date` ← LEAD 窗口推导 | #15 |
| §3.8 | `event_date` 声明不洗（源无真实投资日期） | #16 |
| §3.1.2/§3.1.3 | **经营范围改列**：源 `main_activities`（注释「公司经营范围」）改落 `business_scope`，目标 `main_activities` 留空 | #22 |
| §3.9 | tag 重新拍板：`tag_value` 备用不写；JOIN 键 `org_tag=tag_dict.tag_name`；`tag_dict` 我方维护已灌 7 行种子 | #26/27/28 |
| §3.14.1 | `data_source` ← `table_data_source` 直接映射 | #17 |
| §3.12 | `bid_type` 保持空复核确认 | #18 |
| §3.15.2/3 | forg_extra 合并规则：主档建行、product 只补 NULL | #20 |
| §3.20 | `yftrje`→`rd_investment`、`yfrysl`→`rd_staff_count` 全部期共存放开洗 | #25 |
| §3.21 | 母子未命中行改整行丢弃（原写 NULL 撞 NOT NULL）；`sub_org_id` 允许 NULL 说明 | #21 |
| §4.2 | `enterprise_region_summary` SQL 重写（JOIN `gkxlumenx_dim.code_region`；`total_revenue` 口径） | #1 |
| §4.3 | `enterprise_industry_summary` SQL 重写（`stat_year`=跑批年；3 统计列来源） | #2 |
| §4.4 | 新增 `enterprise_patent_history` 7 指标聚合 SQL | #3 |

### 10-DWD-MySQL-DDL

| 文件 | 变更 | 问询# |
|---|---|---|
| 工商表 v3.1 | `enterprise_tag` 唯一键改 `uk_ent_tag(org_id,tag_code)`（正式库已执行；NULL 不判重导致原键失效） | #26 附带 |
| 指标汇总表 v3.1 §7.1 | 补 `enterprise_risk_summary` as-built CREATE TABLE（现网逐列核对） | #30 |
| 工商表 v3.1 | `enterprise_patent_org_rel` DDL（round2 已补，本轮复核在位） | #29 |

### 数据库变更（正式库 gkxlumenx_dwd，2026-10-22 已执行）

1. `enterprise_tag` 唯一键改为 `(org_id, tag_code)`。
2. `tag_dict` 灌入 demo 库 7 行种子（外资/瞪羚/高新/上市/专精特新/科技型中小企业/独角兽）。

### 结论口径

- 本期要实现维持 **36 张**（#1/#2/#3 全部拍板「洗」，无减）。
- 回填物：`交付客户-round2/round3/`（回填表 markdown + answers-round2.json + 本包副本）。

## v4.0.1（2026-10-21，GDF round1 响应合并）

（内容见此前记录，略）
