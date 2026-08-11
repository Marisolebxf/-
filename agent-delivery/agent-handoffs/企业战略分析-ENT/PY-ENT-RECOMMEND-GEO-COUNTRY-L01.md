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
| 单测 | ✅ 本轮区位回归 26 passed（recommend 19 + key-analysis 7）；algorithm 49 passed（前序） |

Code review P1 修复后链路：

1. `demo-svc-topic-py` 用 `region_id prefix OR country_code terms OR city_code terms` 只读查询 ES；
2. 通过 `search_after` 分页取完整企业 ID，避免先截断 50 条造成组合筛选漏数；
3. `lumen-algo-py` 只消费 `geo_enterprise_codes`，不读写 ES，并与标签/产业等筛选条件做 AND；
4. 区位无命中显式传空集合，算法返回空候选，不回退旧省市文本匹配。

### 架构验收返修（2026-08-11）

1. `filter` 模式按算法实际支持字段校验“至少一个有效条件”；`geographicSources=[]` 或全非法地域码返回 400，不再退化为任意候选；
2. `ESClient.search` 将连接、超时和查询异常统一转换为 `ESUnavailable`，recommend 保持可控 503；
3. `search_after` 增加游标未推进保护，异常时失败关闭，禁止死循环或返回不完整候选；
4. 新增分页、空命中、重复游标、空地域、ES 异常及 503 回归测试；
5. GitLab `py:smoke` 增加 key-analysis/recommend 区位测试，后续提交由 CI 自动执行。
6. 二次复审补强：数组内必须至少有一个非空字符串，`[""]` / `[null]` / 全空白 / `[false]` / `[0]` 不再通过；
7. `geographicSources` 按冻结契约仅允许 `attraction`，`cultivation` 携带有效区位条件返回 400。

## 产物

- `demo-svc-topic-py`：`1e1ce0c`（本轮架构返修；已 push `origin/dev`）
- `lumen-algo-py`：`663262e`
- GitLab Pipeline：[`#4939`](https://gitlab.htmisoft.net/gkx-lumen/demo-svc-topic-py/-/pipelines/4939)

## 验收证据

```text
demo-svc-topic-py: tests/test_recommend_geo_sources.py  # 19 passed
demo-svc-topic-py: tests/test_key_analysis_geo_filter.py # 7 passed
lumen-algo-py: tests/test_analysis.py                   # 49 passed
git diff --check                                       # passed
GitLab #4939 py:smoke + 3 image jobs                   # passed
GitLab #4939 deploy:ai-py                              # manual，待人工触发
```

全量测试补充：`177 passed, 2 skipped, 1 failed`；唯一失败为既有
`test_smart_search_keyword_fields_use_wildcard_product_uses_phrase` 对旧四字段数量的断言，
与本轮 recommendation 区位返修无关，未越界修改。

## 架构合规自检

- ✅ 算法只在 Python；算法层不承担 ES 访问
- ✅ 前端 → Java REST → Python `/internal/*` 调用链未变
- ✅ 未引入 Neo4j；图谱约束不涉及
- ✅ 使用既有日志与服务观测链路
- ✅ CI `py:smoke` 增加区位回归测试；不改变 package/deploy 拓扑
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
