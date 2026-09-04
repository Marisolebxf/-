# CHANGELOG — GDF-ENT-WORKPACK

## v3.1.1 — 2026-09-04

- as-built 回写：六模块 + `former_names` **已改读/已写模块**；两库 ADD 已落地。去掉「改读另开 / 代码未写 / 未 ADD 禁 finance」。  
- GRAPH：`/internal/entan/graph*` 已接四 op 预览；`13` 不再写「仍 blocked」。space 未点名，零写入 `gkx_chain`。  
- **仍不跑**产线 ES sync。V3-L01 **不打回**。

## v3.1 — 2026-09-03

- 列契约对齐正式库（`DATA-ENT-DWD-ALIGN-DOC-L01` / Q-WP3-29）。  
- `10/` 工商 v3.1 CREATE：bid/news/invest 改回正式列名；`enterprise_base` 回写现网宽列；专利现网列与宽列并存。  
- `09` 目标列跟正式库；注明 `lumen-etl-es-py` 六模块已改读。  
- `13`：demo 与正式库 **同一套 ADD**；GDF 洗数目标仍是 `gkxlumenx_dwd`。  
- 第 4 类 KPI 宽列回写设计、**不洗**。  
- V3-L01 **不打回**；列契约以本 ALIGN 为准。请通知辜少彬：禁止再按 v3.0 设计列名洗。

## v3.0 — 2026-09-02

- 升为可对外投递；父级 `派单包/README.md` 同步去掉 `v3.0-draft` /「编写中」。  
- `13` §5 第 6 步改为：表 success → 按 `15` 异步触发，禁止等全库再 `sync-all`。  
- `15` §6.1 定为**当前可执行临时态**（飞书值班 + 本侧转发 + 轮询 `GET /internal/etl/status`）；§4 Java/callback 标目标未上线。  
- `12` §3.4 按现网 `etl/scripts.py` 列出字段级策略；并写明未灌字段。财务各年 nested 写年末存量。  
- `09` 头注写清本叶复核范围（只复核 §8 七项，其余继承 v1.2）。`08` 标明非施工真源。  
- `14`：图谱日批 = 表→op_id；菜单仍给人用；GDF/灌数禁止写图。  
- 新增 `15-GDF触发调度与回执.md`：GDF = 触发调度；长任务必须异步；点名 `OPEN-ENT-GDF-TRIGGER` / `CALLBACK` / `ETL-JOBID`。  
- 已落到 demo/正式 DWD：`enterprise_base.region_id`、正式库 `enterprise_code` 可空、`enterprise_patent_org_rel`、财务 `total_assets`/`total_liabilities`。  
- `lumen-etl-es-py` `finance.py` 写入 `total_assets` / `total_liabilities`（及已 SELECT 未写出的主营/固定资产）。  
- live `gkx`：48 张中 45 张可见；书面阻塞 `dwd_org_tag_info`、`dwd_forg_subsidiary_info`；`chain_dtl` 继续索取。  
- 正式库专利详情/资讯/招投标等仍缺设计列，GDF 按 `13` §3 只 ADD 不 DROP。  
- 索引长文 `settings.yaml` 口令已脱敏；派单包禁止抄口令。
- 评审续修（未推）：`00`/`12`/`14`/`README` 去掉「当前收 callback」口径；`15` §6.1 明确 GDF 不拿 `/internal`；`05` 标 `tag_info`/`forg_subsidiary` 书面阻塞；正式库财务缺 3 列未 ADD 前禁止触发 `finance`。

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
