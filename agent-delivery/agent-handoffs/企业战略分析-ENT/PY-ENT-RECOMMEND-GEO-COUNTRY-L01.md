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
| 三分 OR 实际生效 | ✅ AI 适配层只读 ES 解析完整企业 ID 集；算法层以 ID 集合和其他条件做 AND |
| 跳过 `CN-*`、连字符旧码、非法 token | ✅ |
| 单测 | ✅ adapter 6 passed；algorithm 49 passed |

Code review P1 修复后链路：

1. `demo-svc-topic-py` 用 `region_id prefix OR country_code terms OR city_code terms` 只读查询 ES；
2. 通过 `search_after` 分页取完整企业 ID，避免先截断 50 条造成组合筛选漏数；
3. `lumen-algo-py` 只消费 `geo_enterprise_codes`，不读写 ES，并与标签/产业等筛选条件做 AND；
4. 区位无命中显式传空集合，算法返回空候选，不回退旧省市文本匹配。

## 产物

- `demo-svc-topic-py`：`ec75143`
- `lumen-algo-py`：`663262e`

## 验收证据

```text
demo-svc-topic-py: tests/test_recommend_geo_sources.py  # 6 passed
lumen-algo-py: tests/test_analysis.py                   # 49 passed
git diff --check                                       # passed
```

## 架构合规自检

- ✅ 算法只在 Python；算法层不承担 ES 访问
- ✅ 前端 → Java REST → Python `/internal/*` 调用链未变
- ✅ 未引入 Neo4j；图谱约束不涉及
- ✅ 使用既有日志与服务观测链路
- ✅ 未改 CI/CD 配置
- ✅ 未向 lumen 合并 demo 代码；仅修复 lumen 算法消费契约
- ✅ Java 不写算法、不读 ES
- ✅ ES 只读标准索引；无 Mock 回退
- ✅ D8/D9/D10 本次无 UI 变更

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~20000 |
| model_used | cursor-grok-4.5 |
| actual_cost | ~0.8 |
| cost_warn | green |
