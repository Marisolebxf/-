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
