# CHANGELOG · GDF-POLICY-WORKPACK

## v1.0.1 · 2026-09-01

- `human:淮政玮` 拍板 **OPEN-POLICY-MAP-01 = 方案 A 永远分 UK**。禁止 `gbl:` 改 `policy_id`。

## v1.0 · 2026-09-01

- 首包：Wave A 贴源两张 `gkx` 政策表 → `gkxlumenx_ods`。  
- Wave B 洗入 **一张** `policy_base_info`（`source_plane` + `policy_id`）。  
- 不含 ES / ADS / Nebula。  
- 作废 `dwd_zck_*`、旧 v1 37 列贴源、Demo `ods_sync` 当产线。  
- Mapping 已冻结可投递；尚未执行建表或灌数。CDC 预填不在本版本。  
- 通用解析器尚未识别 `policy_base_info` 字段矩阵，自动预填前须补规则或按 09 人工配置。
