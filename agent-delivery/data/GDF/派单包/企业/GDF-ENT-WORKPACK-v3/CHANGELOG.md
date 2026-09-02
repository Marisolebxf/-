# CHANGELOG — GDF-ENT-WORKPACK

## v3.0 — 2026-09-02

- 升为可对外投递；新增 `13-现网DDL差集-GDF开工必读.md`。  
- `12` 从指针改为 **ES 更新逻辑**（17 模块、水位表、10 分钟时间片、Painless、全量顺序）；财务存量取最新一年。  
- 新增 `14-DWD到图谱.md`：**菜单 A/B/C + op_id** 更新 Nebula；GDF/灌数禁止写图；正式 lumen 链不编造。  
- 已落到 demo/正式 DWD：`enterprise_base.region_id`、正式库 `enterprise_code` 可空、`enterprise_patent_org_rel`、财务 `total_assets`/`total_liabilities`。  
- live `gkx`：48 张中 45 张可见；书面阻塞 `dwd_org_tag_info`、`dwd_forg_subsidiary_info`；`chain_dtl` 继续索取。  
- 正式库专利详情/资讯/招投标等仍缺设计列，GDF 按 `13` §3 只 ADD 不 DROP。

## v3.0-draft — 2026-09-02

- 从 v2.1 **整包继承**（未带 `预填作业/`，CDC 另派）。  
- **新增** `12-DWD到ES.md`：别名 `gkx_enterprise` 双索引；写库方 `lumen-etl-es-py`。  
- 财务金额目标统一万元，GDF 须留单位证据；无法判断时阻塞。  
- 国内 `enterprise_finance_history` 按源表补回年末时点存量 `total_assets` / `total_liabilities`；ES 取最新一年，不与收入同维。  
- `chain_dtl` 经 live 证实不存在：先用 `industry_tags` 洗可覆盖字段，同时继续向供应方索取。  
- 港澳台纳入国内 `enterprise_base`；恢复历史遗漏 `region_id`，`enterprise_code` 改可空，缺 `org_id` 不造。  
- 专利新增 `enterprise_patent_org_rel`，完整申请人/权利人按名称精确关联企业主档。  
- 按 v3 清单重出 `05-WaveA-验收检查表.md`。  
- `OPEN-ENT-FLOW-01/04` 保持独立任务，V3 仅点名未关。  
- 现行企业施工包改指本目录；v2.1 标为历史。

## v2.1 — 2026-08-13

见 [`../GDF-ENT-WORKPACK-v2/CHANGELOG.md`](../GDF-ENT-WORKPACK-v2/CHANGELOG.md)。
