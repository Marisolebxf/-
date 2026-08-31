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
| 2026-08-31 | `DATA-POLICY-STORAGE-S3-GAP-L01` | S3 缺口补齐：`ads.md` 口径由「九张指标表」更正为 as-built **15 张**分群登记并补 NER 1 + 文本 3 表；`dwd.md` 补 `policy_base_info` as-built 列清单（含 ext1/ext5 临时口径说明）；`stores/README.md` 索引同步 |
| 2026-08-31 | `DATA-POLICY-STORAGE-DEMO-FLOW-L01` | `etl/pipeline-demo-mock.md` 重写为 as-built 灌数全景：Mermaid 总图 + `run_all_policy` 15 步时序 + replace/append 分流；标明国际行同表、L4 读 ADS 图镜像、正式 GDF E0→T2 仍虚线；纠正旧稿「九张表 / 先 ODS 再映射」 |
| 2026-08-31 | `DATA-POLICY-STORAGE-DEMO-METRIC-L01` | 同文件补 §2.1：政策域 32 条按步覆盖（叶 19 / 模型身份 9 / 本管线不覆盖 4）；回源 metric-registry + `polan` 各模块文头 |
| 2026-08-31 | `DATA-POLICY-D13-DS-MENU-L01` | §2.1 升 35 条：D1–D3 注册为叶；4 条 DS-07/11 改「组合读面」纳入本管线；算法库菜单拆 parse/match/simulate + 引导力/保障力 |
| 2026-08-31 | `DATA-POLICY-D13-POLAN-WIRE-L01` | polan 写出：D1–D3 表加 `metric_id`；C7 写 `ds_guide`/`ds_guard`；API `analysis/guide|guard`；前端组合页读分 |
| 2026-08-31 | `DATA-POLICY-DEMO-ACCEPT-MATRIX-L01` | 算子级验收对照：35 条 × 两套 UI；apiview 补 parse/match/simulate/guide/guard |
| 2026-08-31 | 三方→ODS 同步 | `etl/pipeline-source-to-ods.md` + `scripts/run_policy_ods_sync.py`；中台基础指标页「数据同步」；默认 Demo，lumen 双确认 |
