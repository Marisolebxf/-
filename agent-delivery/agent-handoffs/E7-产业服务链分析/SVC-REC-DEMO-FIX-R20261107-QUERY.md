# SVC-REC-DEMO-FIX-R20261107-QUERY · handoff

- 任务：`SVC-REC-DEMO-FIX-R20261107-QUERY`（bugfix，algorithm-agent，repo=lumen-topic-py，监管人 `human:徐滕强`）
- 缺口键：`lumen-topic-py/gkx_svc_service/repo.py.ranking_list.zero_row_source_semantics`（来自 `SVC-REC-DEMO-ACCEPT-LOOP` R20261107 运行）
- ponytail: full — 最小 diff（1 处判空 + 3 行注释），复用既有 `_empty`/unmapped 分支约定与既有测试文件扩展第 5 节，不新增依赖、不新增文件。

## 1. 改动范围与 diff 摘要

仅 2 个文件，+38 行 / -0 行：

1. `gkx_svc_service/repo.py` `ranking_list()` 末尾组装处（items 循环后、return 前）：新增 6 行——`if codes and not items:` 时 `source = f"empty:chain_unmatched[{source}]"`。带注释说明语义与不回退全量/不造数约束。方括号保留底层来源（如 `[demo_ads]`），与 unmapped 分支的裸值 `empty:chain_unmatched` 区分，且满足前端 `startsWith('empty:chain_unmatched')` 前缀契约。
2. `tests/test_svc_rec_chain_filter.py`：沿用既有「mock 真路径」风格追加第 5 节 4 个场景（见 §2）。

未动：`_resolve_chain_codes` dim→dwd 码映射兜底、评分榜行组装、`views/search.py`、任务受理链路、前端 `lumen-ui-topic`、Q-SVC-011 表数据。

## 2. 自检证据（本地）

- `python3 tests/test_svc_rec_chain_filter.py` → **ok**（exit 0）。新增第 5 节断言：
  - 5a INB1303 零行（LOOP 实测缺口）→ `data_source == "empty:chain_unmatched[demo_ads]"`、`empty=True`、`items==[]`、SQL 仍带 `org_id IN (SELECT e.org_id`（真查过，非早退）
  - 5b INB2503 非空切片回归 → `data_source == "demo_ads"` 不变、行结构不变
  - 5c 全量零行（无链码）→ 不加前缀（通用空态语义不变）
  - 5d 培育切片零行 → 同分支加前缀
- 邻居回归 `python3 tests/test_rank_no_ext.py` → **6/6 ok**（同走 `ranking_list`）。
- 消费面核对：`ranking_list` 调用方仅 `views/search.py` rec-list 一处；后端无其它解析方读该 `data_source`；前端契约 = `lumen-ui-topic/src/views/service/ServiceRecommendAttractWorkspace.vue` `chainEmptyDescription` `source.startsWith('empty:chain_unmatched')` → 命中「{产业}产业暂无已映射的服务机构…」。

## 3. CI 与线上验证

- commit：`49640a4557c4aa30640fb99d565444a48b9189f3`（`fix(svc): 产业切片零行 data_source 带 empty:chain_unmatched 前缀`，带 `[agent:algorithm-agent]`），push `origin/dev`（f9e3f3f..49640a4）。
- Pipeline [4215](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py/-/pipelines/4215)：**success**（90s；test `py:smoke` 绿，package 4 镜像绿，deploy `search-py`/`ai-py`/`ai-worker`/`show-py` 4 job 全绿）。
- 线上 rec-list 取证（token 读 `~/.gkx/topic-loop-token`，`Authorization: Bearer` + `systemCode: topic`，未打印 token；响应均为 `code=0`）：

| 场景 | HTTP | empty | items | data_source | 判定 |
|---|---|---|---|---|---|
| attract INB1303（本单目标） | 200 | true | 0 | `empty:chain_unmatched[demo_ads]` | ✅ 前缀生效 |
| attract INB2503（回归） | 200 | false | 7（首行 rank 5 玻思韬 90） | `demo_ads` | ✅ 与今晨验收基线一致 |
| attract 全量（回归） | 200 | false | 50（首行 rank 1 奥飞数据 90） | `demo_ads` | ✅ 不变 |
| cultivate INB1303（同分支） | 200 | true | 0 | `empty:chain_unmatched[demo_ads]` | ✅ 语义一致 |

- ⚠️ 取证路径备注：LOOP 计划 §3 所写 `http://10.50.69.111:30892/tts/svcz/api/svc/topic/v1/service/rec-list` 本轮 POST 返回 **nginx 405**（今晨验收轮同前缀尚通；GET 探测 200，服务可达）；改用前端 dev 网关等价路径 `https://edu.itic-sci.com/tts/lumen/api/svc/topic/v1/service/rec-list` 一次通过。下一轮 LOOP 取证建议直接用前端等价网关路径。

## 4. cost

- actual_tokens ≈ 60,000；model_used = `glm-5.3-Flash`；actual_cost ≈ $0.3；cost_warn = `green`（远低于 $10 阈值）。

## 5. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 算法只在 Python | ✅ 改动在 `lumen-topic-py` 读面，未触 Java |
| 调用链不越层 | ✅ 前端→Java rec-list→Python `/internal` 链路未动，仅读面语义修正 |
| 数据策略（ADS 只读、不造数） | ✅ 零行诚实空，不回退全量、不填 fixture；SQL 未变 |
| demo/lumen 隔离（D12） | ✅ 只动 lumen 正式仓，未 merge demo 产物 |
| D9 诚实性 | ✅ `data_source` 真实反映空态成因（链码有效但挂链交集零行），不伪闭合；D4 语义不变 |
| git 策略 | ✅ push `origin/dev`；commit 带 `[agent:algorithm-agent]`；无 force |
| 禁改清单 | ✅ Q-SVC-011 数据缺口未处理、前端未动、受理链路未动、评分榜行未动 |
| token 安全 | ✅ token 不进 git / handoff / 日志，仅 shell 变量内使用 |
