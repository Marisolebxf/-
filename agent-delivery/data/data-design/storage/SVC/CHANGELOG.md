# SVC 存储 CHANGELOG

| 日期 | 变更 |
|---|---|
| 2026-08-14 | 建立 `storage/SVC` 骨架（S1 `ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01`）；对齐 ENT / CHAIN 同构 |
| 2026-08-14 | 起草 `01-data-flow.md`：三图 + Demo ODS 真源锁定（doc/md-extract 国内机构要素库）+ `demo_gkxlumenx_ods`；开放项 OPEN-SVC-FLOW-01～12（含 Q-SVC-010 阻断级、Q-SVC-009） |
| 2026-08-14 | `00-context.md`：不复制 `dwd_org_base_info`；机构主体权威 = ENT |
| 2026-08-14 | 更新 `storage/README.md` 登记 SVC 同构域；handoff 待 `human:侯佳伟` 签 `approved` 后放行 S2 |
| 2026-08-14 | **`01-data-flow.md` 会签 approved**（`human:侯佳伟`）；放行 S2；本地未 push |
| 2026-08-14 | **S2** `DATA-SVC-STORAGE-S2-L01`：`sources/inventory.md`（33 表）+ `etl/pipeline-demo-mock` 脚本入口 + `seeds` 矩阵；`run_svc_ods_reconcile.py` 核对 `demo_gkxlumenx_ods` 差集 0（含 industry*）；禁第二套主表；零写正式 ODS |
| 2026-08-14 | **S2 本地签收**（`human:侯佳伟` · 会签通过 · **不 commit/push**）→ **放行 S3**；六类/Q-SVC-010 另轨 |
| 2026-08-14 | **S3** `DATA-SVC-STORAGE-S3-L01`：灌 `stores/mysql|elasticsearch|nebula` 清单（draft）+ etl 指针；ADS 必含；圈定表标待核验；**不 push** |
| 2026-08-17 | **S3 本地签收**（`human:侯佳伟` 指示开 S4）→ **放行 S4**；仍不 commit/push |
| 2026-08-17 | **S4** `DATA-SVC-STORAGE-S4-L01`：`data-design/服务机构/README.md` + v1/L01 文首横幅 → 强制导航 `storage/SVC`；不删旧正文；**本地 only** |
| 2026-08-17 | **DDL-L01**（结构优先）：`stores/mysql` 字段级 draft + `etl/demo_gkxlumenx_dwd_svc_tables.sql`；排除 Q-SVC-010 / 灌数；ADS 单轨 `svc_*`；**本地 only** |
| 2026-08-17 | **决策 #7**：服务机构挂接到一张 G（`demo_gkx_chain`）；`demo_gkx_svc` 不作为第二张图目标 |
