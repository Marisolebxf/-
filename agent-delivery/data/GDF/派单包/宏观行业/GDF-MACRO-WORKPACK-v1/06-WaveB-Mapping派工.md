# Wave B — Mapping / ETL 派工（MACRO v1.0）

> ②a（城市截面 ADS）**不进**本派工的字段配置，也不进 CDC 矩阵。事实表 Wave B 成功后的触发见 `12`。

> **DDL**：本包 `10/`  
> **Mapping**：`09-宏观行业域-ETL-Mapping明细-源表到DWD.md`  
> **区划反解 / 过滤**：`04`  
> **禁止**：Demo 映射当全文；写 ES / ADS / 图谱；用 `t_id` 建列；按名称 join 维度；取事实表时丢掉 `area_code_type`

## 1. 触发条件

1. Wave A 六张 P0 表贴源验收通过（行数对账含已删除行；取数无行过滤；`is_deleted` 与源一致进入 ODS，再写入 DWD）  
2. 可写 `gkxlumenx_dwd`  
3. 现网 / 目标结构已对照 `10`（缺列先 ALTER；**本叶未核现网**，见 `00` OPEN-MACRO-06）  
4. `sql/check_area_resolve.sql` 在 `gkxlumenx_ods` 上跑过，结果与 `04` §3.5 同结构

## 2. 数据流

```text
MACRO-B1-DIM（五张维度，全量，任意顺序）
gkxlumenx_ods.dwd_dim_index_cal / dwd_dim_index_dur / dwd_dim_source_code
              / dwd_dim_index_attribute / dwd_dim_admin_area
        → macro_index_cal / macro_index_dur / macro_source_code
          / macro_index_attribute / macro_admin_area

MACRO-B2-FACT（事实表；必须在 B1 的 macro_admin_area 之后）
gkxlumenx_ods.dwd_macro_index_data
        → macro_index_data（含 area_resolve / city_code / city_name / province_code 派生列）
```

顺序见 09 §4。B2 依赖 B1 里的区划维度，其余四张维度不挡 B2。

## 3. 作业状态

| 作业 | 状态 | 阻塞边界 |
|---|---|---|
| `MACRO-B1-DIM` | 可配置 | Wave A 六表验收；目标表已按 10 建好 |
| `MACRO-B2-FACT` | 可配置 | B1 的 `macro_admin_area` 成功 |
| ②a `MACRO-C-CITY-SECTION` | B2 成功后另排 | 见 `12`。不要配进本 Mapping 作业 |
| ②b 实效代理 | **不调度** | 仅附录 |
| 写 ES / Nebula | **不执行** | 不在本包 |

## 4. 交付物

- DDL 差集说明（六张 `macro_*`；缺表新建、缺列只 ADD）  
- 字段可追溯到 09 §3.1–3.6  
- 事实表抽样 ≥20 行；小维度表全量比对  
- drop / 冲突计数（空业务键、UK 冲突）  
- 事实表 `area_resolve` × `area_code_type` 分布（对照 `04` §3.5）  
- `check_area_resolve.sql` 三段输出  
- OPEN-MACRO-* 书面登记  
- 增量、删除与重跑策略回签；未回签不得宣称 CDC 闭环

## 5. 本侧后续

城市截面 ADS 见 `12`。落地实效改读 ADS 的口径见 `12` §5 附录，**不属于**本派工。正式 DAG 名由产线回写。
