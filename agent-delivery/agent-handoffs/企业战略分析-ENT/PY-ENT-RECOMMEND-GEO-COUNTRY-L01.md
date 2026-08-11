# PY-ENT-RECOMMEND-GEO-COUNTRY-L01 · handoff

> claimed_by: `agent:data-agent`  
> supervised_by: `human:徐滕强`  
> claim_type: `pull`  
> ponytail: `full`  
> 日期：2026-08-11

## 范围与实现

| DoD | 结果 |
|-----|------|
| `geographicSources[]` 分流：6 位→region / alpha-3→country / 5 位→city | ✅ |
| 写入 `region_ids` / `country_codes` / `city_codes` 供算法消费 | ✅ `normalize_recommend_filters` 在 `_validate_params` |
| 跳过 `CN-*`、连字符旧码、非法 token | ✅ |
| 单测 | ✅ `tests/test_recommend_geo_sources.py` 3 passed |

本单**不写 ES**；适配层规范化后透传 lumen-algo。

## 验收证据

```text
.venv/bin/pytest tests/test_recommend_geo_sources.py -q  # 3 passed
```

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~20000 |
| model_used | cursor-grok-4.5 |
| actual_cost | ~0.8 |
| cost_warn | green |
