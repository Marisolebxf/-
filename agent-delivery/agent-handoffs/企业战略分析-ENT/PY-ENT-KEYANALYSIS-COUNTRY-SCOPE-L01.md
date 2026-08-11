# PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01 · handoff

> claimed_by: `agent:data-agent`  
> supervised_by: `human:徐滕强`  
> claim_type: `pull`  
> ponytail: `full`  
> 日期：2026-08-11

## 范围与实现

| DoD | 结果 |
|-----|------|
| `_build_common_filter` 支持 `country_codes` / `city_codes` + `region_id`/`region_ids` 三分 OR | ✅ |
| 国内 `admin_prefix`（去尾零）；国家/海外城 `terms` | ✅ |
| 禁止 alpha-3 / UN/LOCODE 写入 region_id | ✅（`classify_geo_token` 过滤） |
| 单测 | ✅ `tests/test_key_analysis_geo_filter.py` 7 passed |

共享：`gkx_common/geo_scope.py`

## 偏离

- 现网 ES 文档 `country_code`/`city_code` 可空（部分测试数据）；结构已对齐，查询侧可先上。  
- Java Request 透传两数组：collaborator api-agent，本单未改 Java。

## 验收证据

```text
.venv/bin/pytest tests/test_key_analysis_geo_filter.py -q  # 7 passed
```

## 架构合规

1 算法只在 Python：✅（本单为 search DSL，非模型推理）  
2 调用链：✅ 未越层  
其余 N/A

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~35000 |
| model_used | cursor-grok-4.5 |
| actual_cost | ~1.2 |
| cost_warn | green |
