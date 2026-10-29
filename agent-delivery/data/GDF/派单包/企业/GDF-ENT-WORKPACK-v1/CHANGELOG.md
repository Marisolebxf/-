# CHANGELOG — GDF-ENT-WORKPACK

## v1.3 — 2026-07-31

- **本次企业维正式纳入 Mapping**：新增 `09-企业维-ODS到DWD-Mapping说明-v3.md`（字段级施工真源）。
- `06` 由「Wave B 预告」改为 `06-WaveB-Mapping派工.md`（同包投递；P0 贴源后开工）。
- `00` / README：目标改为「贴源 + Mapping」；DoD 增加 Wave B 关单项。
- `08` 降为表级辅助；`GDF/Mapping/企业/` 增加 v3 指针报告。
- **禁止**按 Mapping v2 / 旧 ODS 表名施工。

## v1.2.1 — 2026-07-31

- 目标库连接改为外网：`111.198.38.90:34306`（原内网 `10.50.11.76:3306`）；同步 `03`/`07`。

## v1.2 — 2026-07-31

- **承诺表真源切换**：企业 Wave A 表清单改为依据 `third-party-source/doc/`（`md-extract`），不再按 live `SOURCE-TABLES` 全量推断。
- **清单重写**：共 **40** 张（P0=17 / P1=23）——国内机构 28 承诺表（含港澳台、招投标出库、风险子集）+ 国外机构 8 + 产业链企业关联 4；去掉重复计入的 `dwd_org_org_product_info` 双源。
- **关键表名纠正**：主表 `dwd_org_base_info`（非 `reg_info`）；`dwd_org_heis_info`；`dwd_bid_*_out` 四表。
- **继续排除**：量子 `company_*` / `dwd_company*`、海洋 `hycy_*`、`ods_*`、专利包、live 扩大司法全套。
- 同步：`00`/`01`/`05`/`06`/`07`/`08`/README；验收表按新 P0/P1。

## v1.1 — 2026-07-31

- 排除全部 `dwd_company*`（量子工商簇暂不贴源）。
- 彼时清单仍来自 live 推断（已被 v1.2 取代）。

## v1 — 2026-07-31

- 初版工作包；跟踪任务 `GDF-ENT-MIRROR-L01`。

### 供应方落库进度（情报，非工作包版本 bump）

- **2026-07-31**：国内机构已落库约 **711 万 / 2500 万（~28%）** — 见 `third-party-source/SUPPLIER-LOAD-PROGRESS.md`。  
  → 不阻塞 Wave A 烟测；全量到位前产线按增量/重跑设计。专利 4000 万另波，不并入本包表清单。

### 待启动会确认后更新

- [ ] `02` → `priority_status: confirmed`
- [ ] 源库承诺表名可达性核验结果写入本 CHANGELOG
- [ ] 对接人表填入 `07` §5
- [ ] 供应方确认：国内机构 711 万覆盖哪些表；金融 3892/1600 口径
