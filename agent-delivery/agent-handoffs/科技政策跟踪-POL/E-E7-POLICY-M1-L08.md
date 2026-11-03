# E-E7-POLICY-M1-L08 · 专题政策门面 · 检索结果智能排序

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 任务已是 integration。本叶不改 task-registry，不标 done，不 commit，不 push。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | rank 改为只读缺项名次表，复用已有 `forwardQuery` 与 `connect()`。不新造打分公式，不加依赖。未用 YAGNI 跳过调用链、D9、D12。 |

## 范围与实现

对照已签收 `POL-L2-DS10-QRY-ARCH` 第 7.1 节。智能排序读缺项表，不再把「没有排序模型」写成接口里的空列表。

- 专题门面 `GET /topic/v1/policy/rank` 仍在 `/{id}` 之前。查询参数原样交给 Python `GET /internal/policy/rank`。
- Python 只读 `gkxlumenx_gapfill.gapfill_policy_qry_rank`。查询参数 `factor` 只接受 `relevance`、`timeliness`、`importance`。过滤列优先 `factor`、`rank_factor`，灌数表用的是 `rank_dim`。
- 名次列只认已有的 `rank_no` / `rank_order` / `position` / `seq`，用来保持灌数行序。没有这些列时按 `policy_id`。这不是打分公式。
- 表没有行：空列表，`honesty.fabricated=false`，`honesty.empty=true`，`reason=gapfill_empty`。连不上库、表不可读或没有维度列：同样空列表，`honesty.error=true`，`reason=gapfill_unavailable`。不返回 `smartScore`，不写公式，不写 `metric_id`。
- 发布时间、效力级别、浏览量仍走已有 `search`。这些值送进 rank 时不查名次表、不打分，`reason=use_search`。
- Java 不打分。若 Python 响应里仍有 `smartScore`，门面整棵去掉。
- 展示侧 `GET /display/v1/policy/panorama/rank` 只委托本入口。本叶不改 `gkxlumen-display`。不进 `gkxlumen-topic-async-service`。不改灌数脚本。

## 偏离

- 名次表由 `POL-L2-DS10-QRY-GAPFILL-L01` 建和灌。本叶只读，不建表、不灌行。
- 读列时若行上带有 `smartScore`、`smart_score`、`score`、`formula`、`weight`，Python 先丢掉再返回。Java 再剔一次。
- 中文「重要性」仍是 `factor_not_supported`，不当作已接通的排序轴。
- 其它查询参数（如 keyword）不参与打分，也不改名次表给出的行序。
- `gkxlumen-display` 未改。浏览器仍不直打 `/topic/v1/policy/rank`。

## 产物清单

- `repos/lumen-svc-platform`：`PolicyFacadeController`、`PolicyFacadeService`、`PolicyFacadeServiceImpl` 的 rank 注释改为读名次表。`rank` 仍走 `forwardQuery` 并去掉 `smartScore`。favorites、share、search、docs、metrics 未删、未改写。
- `repos/lumen-algo-py`：`vendor/entan-py/api/policy_routes.py` 的 `/internal/policy/rank` 改为只读 `gkxlumenx_gapfill.gapfill_policy_qry_rank`；`tests/test_policy_job.py` 的 rank 用例。
- 本交接。未提交、未推送。未改灌数脚本，未改 `gkxlumen-display`。

## 验收证据

Python（`lumen-algo-py`）：

```
python -m pytest tests/test_policy_job.py -k "rank_empty_table or rank_gapfill_down or rank_catalog_order or rank_returns_gapfill or load_rank_rows" -q
```

结果：`5 passed, 17 deselected`。

Java（只跑这两个测试类，`gkxlumen-topic-policy-biz`）：

```
mvn -pl gkxlumen-topic-policy/gkxlumen-topic-policy-biz -am -Dtest=PolicyFacadeControllerTest,PolicyFacadeServiceImplTest -Dsurefire.failIfNoSpecifiedTests=false -Dmaven.build.cache.enabled=false test
```

结果：`PolicyFacadeControllerTest` 18 通过，`PolicyFacadeServiceImplTest` 34 通过，合计 `Tests run: 52, Failures: 0, Errors: 0, Skipped: 0`。BUILD SUCCESS。未跑全仓 mvn。

## 架构合规自检

1. 算法只在 Python。Java 不计算分数。 ✅
2. 调用链是门面 REST → Python `/internal/policy/rank`，展示不直连 Python。 ✅
3. 未改 Nebula，未改唐绍祖锁定的合规算法闭包。 ✅
4. 沿用既有 Feign 门面，未新开绕过可观测的通道。 ✅
5. D12：Feign `name=lumen-algo-py`，路径 `/internal/policy/**`，无 `demo-*`。 ✅
6. 同步读名次表，不进 `gkxlumen-topic-async-service`。 ✅
7. D9：199 不是指标。不造 `metric_id`，不写公式，响应无 `smartScore`。D4 未改。 ✅
8. 只读 `gkxlumenx_gapfill`，不写 ODS / DWD / ADS，未加依赖。 ✅

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 20000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.11 |
| cost_warn | green |

## 修改内容

- Python rank 从「查模型注册表，没有模型就空列表」改为只读 `gkxlumenx_gapfill.gapfill_policy_qry_rank`，按 `factor` 返回已有名次行。
- 表空或库不可用仍是诚实空列表，不编造公式，不返回 `smartScore`。
- 发布时间、效力级别、浏览量进入 rank 时 `reason=use_search`，不打分。
- Java 继续转发并剔除 `smartScore`。

## 测试结果

- Python rank 五例通过。
- Java 两个测试类 52 例通过。

## 遗留风险

- 名次表由灌数单创建。表尚未建好或列名不是 `factor`（或 `rank_factor`）时，rank 的成功读面是空列表，`reason=gapfill_unavailable`。
- 展示侧委托尚未在 `gkxlumen-display` 落地。本叶只提供被委托的门面入口。
- 未推送，无新流水线，无 K8s 发布。

## CI/CD（必填）

- 分支：本地工作区，未提交
- commit：无
- pipeline URL / ID：未触发
- 部署 namespace / 镜像 tag：未发布
- K8s rollout：未发布
- dev 测试 URL / 命令与结果：见验收证据

## 涉及文件

- `gkxlumen-topic-policy/.../PolicyFacadeController.java`
- `gkxlumen-topic-policy/.../PolicyFacadeService.java`
- `gkxlumen-topic-policy/.../service/impl/PolicyFacadeServiceImpl.java`
- `lumen-algo-py/vendor/entan-py/api/policy_routes.py`
- `lumen-algo-py/tests/test_policy_job.py`
- 本文件
