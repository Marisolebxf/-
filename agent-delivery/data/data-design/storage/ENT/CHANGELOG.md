# ENT 存储 CHANGELOG

| 日期 | 变更 |
|---|---|
| 2026-08-12 | 建立 `storage/ENT` 骨架；规范见 `../README.md` |
| 2026-08-12 | 流图会签改由 **human:淮政玮** 认领执行（claimed）；派单说明已更新会话提示词 |
| 2026-08-12 | **`01-data-flow.md` 会签 approved**（淮政玮）；补全触发/失败语义与开放项；S2/S3 放行；handoff `ARCH-ENT-STORAGE-FLOW-SIGNOFF-L01.md` |
| 2026-08-12 | 规范决策 #5：Demo/Mock 与正式共用 `stores`；增 `etl/pipeline-mock-to-ads.md` + `seeds/` |
| 2026-08-12 | **澄清**：Demo 主路径 = LLM→三方**在线约定** ODS→ETL **模拟 GDF**；`demo_*` 库/桶/Nebula；少量覆盖先闭环；增 `pipeline-demo-mock.md` + 流图 §7；ADS 直写降为旁路 |
| 2026-08-12 | 淮政玮确认 Demo/Mock 口径全文写入 `pipeline-demo-mock.md`（approved）；handoff 补记 OPEN-05~07 |
| 2026-08-12 | 启动 S2 派单 `DATA-ENT-STORAGE-S2-L01`（ready · data-agent） |
| 2026-08-12 | S2 执行：inventory/etl/seeds 回填；淮政玮认领；handoff `DATA-ENT-STORAGE-S2-L01.md` |
| 2026-08-12 | **补强**：`doc/` xlsx = 三方 ODS **权威唯一真源**；**`md-extract/` 优先读取**（自 Excel 抽取）；Wave A / live 仅镜像或对账（决策 #6） |
| 2026-08-12 | **S3**：`DATA-ENT-STORAGE-S3-L01` 灌入 stores mysql/es/nebula（draft；真源外链 as-built） |
| 2026-08-12 | **S4**：旧 `data-design/企业` stub → storage/ENT（`DATA-ENT-STORAGE-S4-L01`） |
| 2026-08-12 | **OPEN-06 关闭**：`DEMO-ENT-LLM-ODS-L01` · `entan/llm_ods` + `scripts/run_llm_ods.py` |
