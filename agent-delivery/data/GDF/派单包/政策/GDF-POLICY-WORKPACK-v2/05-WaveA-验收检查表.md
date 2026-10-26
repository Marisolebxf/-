# Wave A 验收检查表（回签）— 政策 v2.0

> **任务**：`GDF-POLICY-WORKPACK-V2-L01`  
> **清单真源**：`02-WaveA-贴源表清单.yaml`（2 张，均 P0 wash）  
> **tgt**：`gkxlumenx_ods` 同名表。贴源不连、不改、不验收 `demo_gkxlumenx_*`。  
> **行数**：取数无 `WHERE`。`src` / `tgt` 用 `COUNT(*)`，含已删除行和历史行。不要另加 `is_deleted = 0` 或 `is_history = 0` 后再对账。  
> **阈值**：行数偏差 ≤1% 或绝对差 ≤100（取较宽者）；每表抽样 ≥20 条且主键命中 100%；DDL 同构（库名改为 `gkxlumenx_ods`）。国内 `content` 抽检不得截断。  
> **预填行数不作验收线。** 回签时现算。

**产线名称**：________________  
**调度周期 / DAG**：________________（`OPEN-POLICY-FLOW-01` 未关前不得伪填）  
**GDF 负责人签字**：________ 日期：________  
**本侧验收签字**：________ 日期：________

列：`src/tgt`=全表行数；`ddl/sample`=Y/N；`batch`=最近成功批次；`done/sign`=回签。

## P0（关单必填，2）

| # | table_name | cn | src | tgt | ddl | sample | batch | extract_mode | watermark | last_wm | done | sign | note |
|---:|---|---|---:|---:|---|---|---|---|---|---|---|---|---|
| 1 | dwd_policy_base | 国内政策库 | | | | | | | updated_time | | | | `content` 须流式；洗入 `source_plane=domestic` |
| 2 | dwd_global_policy_base | 国外政策信息表 | | | | | | | updated_time | | | | 洗入同一张 `policy_base_info`，`source_plane=global` |

无 P1 / P2。`dwd_zck_*`、供应方 `ods_*` 不贴，不计入完成数。

## 抽检 SQL

```sql
SELECT COUNT(*) FROM gkx.dwd_policy_base;
SELECT COUNT(*) FROM gkxlumenx_ods.dwd_policy_base;
SELECT COUNT(*) FROM gkx.dwd_global_policy_base;
SELECT COUNT(*) FROM gkxlumenx_ods.dwd_global_policy_base;
```

源库无表 → 记阻塞，禁止换旧名或造表关单。

## 关单

- [ ] 两张 P0 全部 `done=Y`，行数含删除行和历史行  
- [ ] 抽样主键命中，国内正文未截断  
- [ ] 目标库是 `gkxlumenx_ods`，不是 demo  
- [ ] 本表只验收贴源。Mapping 与 Wave C 不在这张表关单
