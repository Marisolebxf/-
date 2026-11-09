# Wave A 验收检查表（回签）— 宏观行业 v1.0

> **任务**：`GDF-MACRO-WORKPACK-L01`（成包）· 跑通叶 `SYSINT-06-05-L01`  
> **清单真源**：`02-WaveA-贴源表清单.yaml`（6 张，均 P0 wash）  
> **tgt**：`gkxlumenx_ods` 同名表。贴源不连、不改、不验收 `demo_gkxlumenx_*`。  
> **行数**：取数无 `WHERE`。`src` / `tgt` 用 `COUNT(*)`，含已删除行。不要另加 `is_deleted = 0` 后再对账。  
> **阈值**：事实表、区划表（体量大）行数偏差 ≤1% 或绝对差 ≤100（取较宽者）；**三张小维度表（3 / 7 / 4 行）与属性表（867 行）要求行数精确相等**，否则绝对差 ≤100 的宽松阈值会掩盖整表缺失；每表抽样 ≥20 条（小维度表全量比对）且 `dwd_id` 命中 100%；DDL 同构（库名改为 `gkxlumenx_ods`）。  
> **预填行数不作验收线。** 2026-11-09 快照仅供参考，回签时现算；事实表与区划表 20,000 是样本上限，补数后会变。

**产线名称**：________________  
**调度周期 / DAG**：________________（未定前不得伪填）  
**GDF 负责人签字**：________ 日期：________  
**本侧验收签字**：________ 日期：________

列：`src/tgt`=全表行数；`ddl/sample`=Y/N；`batch`=最近成功批次；`done/sign`=回签。

## P0（关单必填，6）

| # | table_name | cn | 快照行数 | src | tgt | ddl | sample | batch | extract_mode | watermark | last_wm | done | sign | note |
|---:|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|
| 1 | dwd_macro_index_data | 数据表 | 20,000 | | | | | | 首次全量，之后增量 | updated_time | | | | 事实；样本上限；洗入 `macro_index_data` |
| 2 | dwd_dim_index_attribute | 指标属性表 | 867 | | | | | | 全量 | — | | | | 精确相等 |
| 3 | dwd_dim_admin_area | 区划表 | 20,000 | | | | | | 全量 | — | | | | 区划反解用；样本上限 |
| 4 | dwd_dim_index_cal | 计算维度表 | 3 | | | | | | 全量 | — | | | | 精确相等；HB/TB/JDZ |
| 5 | dwd_dim_index_dur | 时间维度表 | 7 | | | | | | 全量 | — | | | | 精确相等；7 个代码 |
| 6 | dwd_dim_source_code | 数据来源表 | 4 | | | | | | 全量 | — | | | | 精确相等；4 个来源 |

无 P1 / P2。供应方 `ods_*`、行业分析六表、金融表不贴，不计入完成数。

## 抽检 SQL

```sql
SELECT COUNT(*) FROM gkx.dwd_macro_index_data;      SELECT COUNT(*) FROM gkxlumenx_ods.dwd_macro_index_data;
SELECT COUNT(*) FROM gkx.dwd_dim_index_attribute;   SELECT COUNT(*) FROM gkxlumenx_ods.dwd_dim_index_attribute;
SELECT COUNT(*) FROM gkx.dwd_dim_admin_area;        SELECT COUNT(*) FROM gkxlumenx_ods.dwd_dim_admin_area;
SELECT COUNT(*) FROM gkx.dwd_dim_index_cal;         SELECT COUNT(*) FROM gkxlumenx_ods.dwd_dim_index_cal;
SELECT COUNT(*) FROM gkx.dwd_dim_index_dur;         SELECT COUNT(*) FROM gkxlumenx_ods.dwd_dim_index_dur;
SELECT COUNT(*) FROM gkx.dwd_dim_source_code;       SELECT COUNT(*) FROM gkxlumenx_ods.dwd_dim_source_code;
```

区划反解、键唯一、维度孤儿：跑 `sql/check_area_resolve.sql`（在 `gkxlumenx_ods` 上复核，结果对照 `04` §3.5）。

源库无表 → 记阻塞，禁止换旧名或造表关单。

## 关单

- [ ] 六张 P0 全部 `done=Y`，行数含已删除行；小维度表精确相等  
- [ ] 抽样 `dwd_id` 命中；事实表 `index_value` 精度（`decimal(38,8)`）未被截断  
- [ ] 目标库是 `gkxlumenx_ods`，不是 demo  
- [ ] `check_area_resolve.sql` 三段结果已附，四城预期类别一致（`04` §3.4 / §3.5）  
- [ ] 本表只验收贴源。Mapping 与 ②a 不在这张表关单
