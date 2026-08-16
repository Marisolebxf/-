# CHAIN 存储 CHANGELOG

| 日期 | 变更 |
|---|---|
| 2026-08-13 | 建立 `storage/CHAIN` 骨架（S1 `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01`）；对齐 ENT 同构 |
| 2026-08-13 | 起草 `01-data-flow.md`：三图 + Demo ODS 真源锁定（doc/md-extract）+ `demo_gkxlumenx_ods`；开放项 OPEN-CHAIN-FLOW-01～09 |
| 2026-08-13 | **`01-data-flow.md` 会签 approved**（`human:李伟`）；放行 S2 建表；handoff `ARCH-CHAIN-STORAGE-FLOW-SIGNOFF-L01.md` |
| 2026-08-13 | 精简 S1 占位：删除空管道 stub 与 stores 空子 README；etl/stores 改索引式，细文件留给 S2/S3 |
| 2026-08-13 | S2：`run_chain_ods.py` + `demo_gkxlumenx_ods_chain_tables.sql`；`llm_ods` 按表头解析主键；inventory/etl 指针/seeds 矩阵；经 `111.198.38.90:34306` apply 四表入 `demo_gkxlumenx_ods` |
| 2026-08-13 | S2 副产品：`sources/md-extract-vs-live-ods-diff.md`；**2026-08-13 live DESCRIBE** `@183.240.141.251:3318/gkx` 四表（证据 `_chain_four_tables_live_2026-08-13.json`） |
| 2026-08-13 | S3：`stores/mysql`（dwd-chain/ads/dim）+ `elasticsearch` + `nebula` 清单灌入（draft）；`DATA-CHAIN-STORAGE-S3-L01` |
| 2026-08-13 | **ADS v1**：`产业链-ADS表设计-业务需求驱动(v1).md`（按 DWD v5 重做 8 表；废止旧十一 `chain_*` 当真源）；更新 `stores/mysql/ads.md` |
| 2026-08-13 | **S3 收口**：`stores/mysql/ads.md` 真源切换为 **ADS v2**（`产业链-ADS表设计-原型与Handoff驱动(v2).md`，10 物理表）；v1 降为对照；DWD 仍锁 v5；handoff `DATA-CHAIN-STORAGE-S3-L01.md` |
| 2026-08-13 | **S3 会签**：`human:李伟`「S3 确认，放行 S4」→ registry `ready_to_sign` |
| 2026-08-13 | **S4**：`data-design/产业链/README.md` + 主要旧稿文首横幅 → 强制导航 `storage/CHAIN`；handoff `DATA-CHAIN-STORAGE-S4-L01.md` |
| 2026-08-13 | **S4 补漏**：其余 legacy（映射 Step1/2、INST、DEC、灌数对照、国内机构库）+ handoff `DATA-CHAIN-db-design.md` 全部加 S4 横幅 |
| 2026-08-16 | **行业分析切片**：`DATA-CHAIN-INDANA-STORAGE-L01` 收录六表 `dwd_industry_analysis_*` → 项目 DWD `industry_analysis_*`（去前缀）；主图未翻签 |
| 2026-08-16 | **企业上链**：`etl/pipeline-ent-hang.md`；Demo 两表 `enterprise_industry_chain` + `industry_chain_entity_rel`（`entity_id=org_id`）；SEED-08 as-built / SEED-10；不翻签流图 |
| 2026-08-16 | **Demo 模拟过程**：`DEMO-CHAIN-SIM-PROCESS-L01` 落 `etl/pipeline-demo-sim-process.md` + `etl/ods-to-dwd-mapping.md`；缺口五表诚实空；**未翻签** `01-data-flow`；未改 `gdf_sim.py` |
