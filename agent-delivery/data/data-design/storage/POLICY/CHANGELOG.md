# POLICY storage CHANGELOG

| 日期 | 任务 | 说明 |
|---|---|---|
| 2026-08-21 | `DATA-POLICY-STORAGE-S1-L01` | 开域 + `POLICY-STORAGE-FLOW` approved |
| 2026-08-21 | `DATA-POLICY-STORAGE-S2-L01` | sources / etl / seeds 指针 |
| 2026-08-21 | `DATA-POLICY-STORAGE-S3-L01` | stores draft；图谱 hang `demo_gkx_chain` |
| 2026-08-21 | `DATA-POLICY-STORAGE-S4-L01` | 旧稿 stub；文档闭环 ≠ 灌数 |
| 2026-08-21 | 展示窗口 | SRS 科技政策跟踪 + `demo-ui-science/policy-tracking`；`windows/display-ds10-12.md` |
| 2026-08-21 | ODS 表名纠正 | 三方 `gkx.dwd_policy_base` / `gkx.dwd_global_policy_base`；废止 `dwd_zck_*` |
| 2026-08-21 | ODS DDL 真源 | `sources/ods-ddl.md` + `etl/ods-to-dwd-mapping.md`；废止 v1 37 列当贴源 |
| 2026-08-21 | 模拟 ETL 澄清 | `etl/pipeline-demo-mock.md` 拆 E0→E1→T2→L3→L4；模拟 GDF = T2 |
| 2026-08-21 | T+1 增量 | 同文件补水位、`insert_remark`、DWD 合并、L3 快照重算、L4 点边增量 |
| 2026-08-31 | `DATA-POLICY-STORAGE-NEBULA-ETL-L01` | 补 `etl/pipeline-to-nebula.md`（as-built 回填 B 叶投影管线）；记录 `stores/nebula.md` 四类边列定义与 loader 实际 DDL 不一致，转 `OPEN-POLICY-GRAPH-03` |
| 2026-08-31 | `DATA-POLICY-STORAGE-EDGE-SEMANTIC-L01` | `stores/nebula.md` 补四类边语义表（含义/起终点/源字段/权重/props，回源 `polan/graph/entity.py` RE 段）+ DDL 块 as-built 差异标注 |
| 2026-08-31 | `DATA-POLICY-STORAGE-ETL-FILL-L01` | etl 层补齐：`README.md` 管道索引 + `pipeline-ods-to-dwd`（as-built）+ `pipeline-dwd-to-ads`（as-built，12 步写入图与顺序约束）+ `pipeline-dwd-to-es`（not-built）+ `pipeline-mock-to-ads`（not-built）；记录 `ads.md` 未登记 `policy_entity` / `policy_text_parse` / `policy_match` / `policy_simulate` 四表 |
