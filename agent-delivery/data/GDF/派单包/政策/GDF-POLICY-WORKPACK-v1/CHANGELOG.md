# CHANGELOG · GDF-POLICY-WORKPACK

## v1.0.3 · 2026-10-23

- 生产规约：抽取产业、条款结构化必须提供 Python 脚本，逻辑与算法 demo 中台同一模块（`industry_enrich` / `industry_job`、`clause_job`）。禁止 CDC / SeaTunnel 另写。见 `12` 脚本规约。
- 目标库仍是 `gkxlumenx_dwd` / `gkxlumenx_ads`。本包不复制算法源码。

## v1.0.2 · 2026-10-23

- Wave B 成功后增加 Wave C：抽取产业、条款结构化（派单口语「条件结构化」）。说明见 `12`。  
- 抽取只写 `policy_industry_rel`（DWD 写完同步 ADS），不改 `policy_base_info`。  
- 条款只合并 ADS `policy_text_parse.structured_elements.clauses`，不 TRUNCATE、不写 ES。  
- 两作业不进 09 字段矩阵，也不进 CDC 预填。

## v1.0.1 · 2026-09-01

- `human:淮政玮` 拍板 **OPEN-POLICY-MAP-01 = 方案 A 永远分 UK**。禁止 `gbl:` 改 `policy_id`。

## v1.0 · 2026-09-01

- 首包：Wave A 贴源两张 `gkx` 政策表 → `gkxlumenx_ods`。  
- Wave B 洗入 **一张** `policy_base_info`（`source_plane` + `policy_id`）。  
- 不含 ES / ADS / Nebula。  
- 作废 `dwd_zck_*`、旧 v1 37 列贴源、Demo `ods_sync` 当产线。  
- Mapping 已冻结可投递；尚未执行建表或灌数。CDC 预填不在本版本。  
- 通用解析器尚未识别 `policy_base_info` 字段矩阵，自动预填前须补规则或按 09 人工配置。
