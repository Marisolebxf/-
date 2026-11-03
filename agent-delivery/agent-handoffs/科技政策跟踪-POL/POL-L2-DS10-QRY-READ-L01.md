# POL-L2-DS10-QRY-READ-L01 · 多维检索正式表空时改读缺项表

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。任务已是 in_progress。本会话不改 task-registry，不把任务标成 done |
| 说明 | 用户授权提交并推送 origin/dev。本页不写联调结论 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改检索、正文、统计、分布的读路径。未改排序，未改 D4，未把类型或有效率写进正式库 |

## 范围与实现

真源是 `sdd/l2/POL-L2-DS10-QRY-ARCH.md` 第 2 节和第 7 节。范围是 197、198、200。199 的排序读路径不在本叶。

正式 ADS/DWD 有行时，统计仍走已有 metrics/indicators，目录和正文仍走 `policy_base_info`。正式表没有行时改读这两张缺项表，都在 `gkxlumenx_gapfill`：

| 正式表空 | 改读 | 接口 |
|---|---|---|
| `gkxlumenx_dwd.policy_base_info` 无行 | `gapfill_policy_qry_doc` | `GET /internal/policy/search`；`GET /internal/policy/docs/{id}` 与 `GET /internal/policy/{id}` |
| `gkxlumenx_ads` 的级别、类型、时序、全国、深圳分布无行 | `gapfill_policy_qry_stat` | `GET /v1/policy/metrics`、`GET /internal/policy/metrics`；`GET /v1/policy/indicators`、`GET /internal/policy/indicators` |

统计行用表上已有的 `metric_id`：总数、级别、全国、深圳、时序、类型、有效率。类型不写入 `ads.policy_type_dist`。有效率不写入正式库有效率列。

两处都没有行则列表空或统计空，HTTP 成功。不造 0，不在代码里写死目录。不读 demo 库，不写 ODS/DWD/ADS。不改 D4。不返回 `smartScore`。

`GET /internal/policy/rank` 与 `_load_rank_rows` 未改。

## 偏离

无。正式目录有行时，效力级别、状态、文号、产业这些缺项目录没有的列不另造筛选，命中为空。

## 产物清单

- `repos/lumen-algo-py/vendor/entan-py/api/policy_routes.py`
- `repos/lumen-algo-py/tests/test_policy_job.py`
- 本 handoff

未改 Java，未改 `gkxlumen-display`。

## 测试结果

`python -m pytest tests/test_policy_job.py -q -k "search or detail or indicator or metrics or qry_gapfill or rank"`

21 passed，14 deselected。正式表有行的用例仍走原读路径，没有被缺项行覆盖。

## 遗留风险

缺项统计没有产业列。正式目录为空且请求带了产业条件时，时序、全国、深圳仍读缺项表全量行。正式目录有行时仍按原逻辑切产业和地域。

## CI/CD

- 分支：`lumen-algo-py` `origin/dev`
- commit：`25c7a53` `feat(policy): 正式表空时读多维检索缺项表 [agent:algorithm-agent]`
- push：已推到 `origin/dev`（`bce9122..25c7a53`）
- 本 handoff 在 `gkx-orchestration` `origin/dev`

## 架构合规自检

- D12：只读 `lumen-algo-py` 正式连接上的 `gkxlumenx_dwd` / `gkxlumenx_ads` / `gkxlumenx_gapfill`，不读 demo 库
- D16：缺项只读 `gapfill_` 表，不写 ODS/DWD/ADS
- D4：未改
- 排序：未改 `_load_rank_rows`，未改 `GET /internal/policy/rank`
