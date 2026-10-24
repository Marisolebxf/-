# LUMEN-POLICY-SZ3D-B-JOB-L01 · 深圳政策现状结果板

> 设计：`05.6.2-深圳政策现状分析.md` §3–§5，总控 §0，calc-logic `M_POLICY_SUPPORT_STRENGTH`。只改 Python。未改 Java / 前端，未领 C/D/E。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时状态已是 `in_progress`。本叶不把任务改成 done。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 新结果板与时序 / 区域同级，复用时序的层级标签、润色失败边界和 8 秒客户端。未加依赖，未改时序 `narrate_board` 的原路径。 |

## 修改内容

- `policy_shenzhen` / `policy_sz_3d` 不再走 `harness.dispatch`，`harness_mode=shenzhen_board`。焦点和 `policy_shard` 仍走 harness。`shards=0`，不进三档分片。
- 请求 `items` 达到 40000 仍 `FULL_SCAN_FORBIDDEN`。Python 不写 `result_snapshot_id`。
- 支持力度：有城市名且不少于 30 条的城市截面。因子只有条数和层级，内部权重 0.5/0.5，待 `QPOL-02`。档位 `value=null`，`reason=无金额列`。深圳分数、名次、条数、层级均值和与条数的秩相关写在 `cards.support`。无城市名的行不进分子也不进分母，记在 `diagnostics.city_null_rows`。不读 `dwd_bid_*`，不按 `industry_vid` 重算。在线数字来自当次行，不写死 33.5585 / 879。
- 在线 `level` 沿用 `policy_base_info` / 时序板：1 国家级、2 省级、3 市级、4 区县级，权重 1.0 / 0.75 / 0.5 / 0.25。中文层级名同样可算。调研快照里「4=国家级」不用于这个接口。
- 产业适配性：标题包含请求的链名。本地命中城市少于 3，或没有命中，则 `score=null`，不补数。技术锚点 `computable=false`，`reason=技术锚点在分类体系会签前不映射到链`。
- 落地实效 `computable=false`，`reason=实施日、支持对象、反馈全缺`。无执行率、覆盖、满意度，无三维综合分。
- 优化建议在同一次 execute 里收尾。规则先写 `strategies`（`id` / `title` / `dimension` / `priority` / `conclusion`）。模型只改 `conclusion`。无 Key、异常、坏 JSON、数字不在事实包、出现「深圳政策弱 / 招标 / 资金强度 / 新设补贴」时，该卡退回草稿，任务仍成功。`narration.status` 为 `ok` / `fallback` / `skipped`。润色失败不把 `honesty.degraded` 设为真。取数异常才 `degraded=true`。
- 建议卡只有三张：深圳进入排名才有供给结构；档位为 null 才有扶持档位不可算；适配性命中才有锚点适配。落地实效和综合分不出卡。

## 结果 JSON 样例

注入行，不是真库，也不是 calc-logic 的 879 / 33.5585。深圳 60 条省级，上海 40 条市级，北京 30 条国家级，杭州 5 条不入榜，1 条无城市名。链名「集成电路」。无 Key，所以 `narration=skipped`。

```json
{
  "harness_mode": "shenzhen_board",
  "sub_type": "policy_shenzhen",
  "shards": 0,
  "mode": "shenzhen_board",
  "cards": {
    "support": {
      "metric_id": "M_POLICY_SUPPORT_STRENGTH",
      "computable": true,
      "score": 75.0,
      "rank": 1,
      "policy_count": 60,
      "level_mean": 0.75,
      "tier": {"value": null, "reason": "无金额列"},
      "spearman_vs_count": 0.5,
      "notes": ["供给规模与层级合成", "条数主导", "非资金强度", "min-max 不是趋势"],
      "weights": {"count": 0.5, "level": 0.5, "pending_ref": "QPOL-02"}
    },
    "fit": {
      "metric_id": "M_POLICY_INDUSTRY_FIT",
      "computable": true,
      "score": 100.0,
      "hit_count": 10,
      "anchor_name": "集成电路"
    },
    "effect": {
      "metric_id": "M_POLICY_IMPLEMENTATION_EFFECT",
      "computable": false,
      "reason": "实施日、支持对象、反馈全缺"
    }
  },
  "strategies": [
    {
      "id": "sz-supply-structure",
      "title": "供给结构",
      "dimension": "支持力度",
      "priority": 1,
      "conclusion": "深圳名次第 1，分 75.0，60 条，层级均值 0.75，与条数秩相关 0.5。市级为主，不宜写成政策偏弱。"
    },
    {
      "id": "sz-tier-gap",
      "title": "扶持档位不可算",
      "dimension": "支持力度",
      "priority": 2,
      "conclusion": "政策表没有金额列，本结果不提出资金加码建议。"
    },
    {
      "id": "sz-industry-fit",
      "title": "锚点适配",
      "dimension": "产业适配性",
      "priority": 3,
      "conclusion": "锚点集成电路命中 10 条，适配分 100.0。"
    }
  ],
  "narration": {"status": "skipped", "model": "", "reason": "no_key"},
  "honesty": {"empty": false, "fabricated": false, "degraded": false, "source": "items"}
}
```

「市级为主，不宜写成政策偏弱」是详设要求留在供给结构草稿里的口径句，不是这次注入行的层级占比。

## 测试结果

在 `lumen-algo-py`：

```text
python -m pytest tests/test_policy_shenzhen_board.py tests/test_policy_narrate.py tests/test_policy_job.py -q --tb=line
```

28 passed，2 warnings（FastAPI 422 弃用告警，原有，与本叶无关）。覆盖：档位不是 0、无综合分、换产业不改支持力度、实效不可算、无 Key 时建议卡仍在且任务成功；时序 `narrate_board` 原测试仍过。

## CI/CD

- 分支：`lumen-algo-py` `origin/dev`
- commit：`7a6f6b24d10c8687b74ea8c8675368947286d591`
- 部署：本叶不点部署

## 遗留

- 未连真库。单测用注入行。在线截面要等有 DWD 的环境再看深圳名次。
- Java 透传、前端三张卡、发布和 QA 不在本叶。
- 任务状态保持 `in_progress`，未写「联调通过」，未改 done。
- registry 的 cost 四字段没有回写，避免把 `task-registry.yaml` 和本仓其他未提交文件一起提交。数字只记在下面。

## 涉及文件

- `repos/lumen-algo-py/vendor/entan-py/polan/shenzhen_board.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/job.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/insight_narrate.py`
- `repos/lumen-algo-py/tests/test_policy_shenzhen_board.py`

## 架构合规

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 前端 → Java → `/internal/*` | ✅ 本叶只改 Python 结果板 |
| 不自签 snapshot | ✅ |
| 图 | 派单写明不必。未改存储拓扑 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 90000 |
| model_used | grok-4.7 |
| actual_cost | 0.18 |
| cost_warn | green |
| 说明 | source: session_estimate。无 Console 的 in/out 分离值。粗估沿用上一叶时序润色 handoff 的混合单价（60000 token ≈ $0.12）。 |
