# POL-L2-DS10-SENT-MOCK-ADS · 效果与匹配写入已有 ADS

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。总控已认领并置 in_progress。本会话不改 task-registry，不标 done |
| 说明 | 只跑已有 `polan.eval.effect.run` 与 `polan.text.match.run`。不改这两个函数，不改 `job.py` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 新增一个可重复执行的入口，只调用这两份已有 `run()`。未新建 ADS 表，未改公式，未改 D4 |

## 范围与实现

落点以 `sdd/l2/POL-L2-DS10-SENT-DATA.md` 第 4 节、第 7 节为准。物理库是 `ads.md` 已登记、且这两份 `run()` 已经在写的 `demo_gkxlumenx_ads`。

入口 `scripts/run_policy_sent_mock_ads.py` 把平面锁在 demo，然后依次调用：

1. `polan.eval.effect.run`：删除 `policy_effect` 里 `scope_type='region_effect'` 的行再写入；删除 `policy_metric_timeseries` 里 `metric_id='M_POLICY_IMPLEMENTATION_EFFECT'` 的行再写入。社会维、环境维仍是 `run()` 里的受控代理，`ext` 带 `is_mock` 与 `pending=QPOL-02`。
2. `polan.text.match.run`：清空 `policy_match` 再写入。`metric_id` 仍是 `M_POLICY_MATCH`。同一主体内 `rank_no` 从 1 到至多 8。

没有新建表，没有加列，没有改公式，没有把查询接口改成返回写死 JSON。查询请求不调用这个入口。未写 `gkxlumenx_ods`、`gkxlumenx_dwd`、`gkxlumenx_ads`、`gkxlumenx_gapfill`。

## 偏离

没有。写出的区域数是现有 `run()` 按当前 `demo_gkxlumenx_dwd.policy_base_info` 的省份归并后的结果：广东省 `440000`、山东省 `370000`。本单没有改这个归并。

`match.run` 会清空整张 `policy_match` 再写。这是该函数现有写法。本单没有改它。下面的 111 行是这次跑完之后表上的行数。

## 产物清单

- `repos/lumen-algo-py/scripts/run_policy_sent_mock_ads.py`
- 本 handoff

未改 `polan/eval/effect.py`。未改 `polan/text/match.py`。未改 `job.py`。未改 Java。

## 验收证据

三张已有表都写入了。行数是跑完之后的 SELECT。

| 表 | SELECT | 行数 |
|---|---|---|
| `demo_gkxlumenx_ads.policy_effect` | `scope_type='region_effect'` | 2。广东省 `440000`、山东省 `370000`。`metric_id` 都是 `M_POLICY_EFFECT_SCORE` |
| 同上 | `ext` 含 `"is_mock": true` 且含 `QPOL-02` | 2 |
| `demo_gkxlumenx_ads.policy_metric_timeseries` | `metric_id='M_POLICY_IMPLEMENTATION_EFFECT'` 且 `dim_key='落地实效性'` | 2。区域代码同上。`ext` 含 `is_mock` 与 `QPOL-02` 的也是 2 |
| `demo_gkxlumenx_ads.policy_match` | `COUNT(*)` | 111 |
| 同上 | `metric_id='M_POLICY_MATCH'` | 111 |
| 同上 | `COUNT(DISTINCT subject_id)` | 18 |
| 同上 | `rank_no` 不在 1 到 8 | 0 |

命令（在 `repos/lumen-algo-py`，2026-11-03）：

- `python scripts/run_policy_sent_mock_ads.py` → 退出码 0。日志 `效果评估=2 区域`、`匹配推送：主体=18 匹配记录=111`。输出 `{"connected":true,"written":true,"db":"demo_gkxlumenx_ads","rows":{"policy_effect_region_effect":2,"policy_effect_mock_qpol02":2,"timeseries_implementation_effect":2,"timeseries_mock_qpol02":2,"policy_match":111,"policy_match_metric":111,"policy_match_subjects":18,"policy_match_rank_out_of_1_8":0}}`
- 独立 SELECT 再次核对：效果 2、效果标记 2、落地实效 2、匹配 111 / 指标 111 / 主体 18

## 架构合规自检

- ✅ 调用链：只跑已有 Python `run()` 写 demo ADS。未改 Java，未把接口改成写死 JSON
- ✅ 未新建表，未加列，未改公式
- ✅ 图谱：未写 nGQL
- ✅ 写入库是 `demo_gkxlumenx_ads`。未写正式 `gkxlumenx_ads`、ODS、DWD、gapfill、供应方库
- ✅ `policy_effect.metric_id` 仍是 `M_POLICY_EFFECT_SCORE`。时序只写 `M_POLICY_IMPLEMENTATION_EFFECT`。匹配行 `metric_id` 仍是 `M_POLICY_MATCH`，没有另写一套产业适配分
- ✅ 社会维、环境维仍在 `ext.dims`，行上 `is_mock` 与 `QPOL-02` 仍由原 `run()` 写入
- ✅ 未改 D4，未新造 `metric_id`
- ✅ 未改架构稿、说明书、WBS、`ads.md`、task-registry
- ✅ 未把本单标成 done

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 12000 |
| model_used | grok-4.7 |
| actual_cost | 0.05 |
| cost_warn | green |

## CI/CD

- 分支：`lumen-algo-py` 的 `dev`
- commit：`51efa4cb75742d51ce55b7c6292578791e1a08b6`
- pipeline：本单不跟发布
- 部署：无
- 库：`demo_gkxlumenx_ads` 已写入。效果 2 行，落地实效 2 行，匹配 111 行

## 涉及文件

- `scripts/run_policy_sent_mock_ads.py`

## 未做的事

- 未改 task-registry，未把任务标成 done
- 未改 `effect.py`、`match.py`、`job.py`、Java、查询接口
- 未新建 ADS 表，未改公式，未改 D4
- 未写正式 ODS、DWD、ADS、gapfill、供应方库
