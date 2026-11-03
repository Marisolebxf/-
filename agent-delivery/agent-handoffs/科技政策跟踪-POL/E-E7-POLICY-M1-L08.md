# E-E7-POLICY-M1-L08 · 专题政策门面 · 检索结果智能排序

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 任务已是 in_progress。本叶不改 task-registry，不标 done，不 commit，不 push。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 校正已有 rank 草稿，复用 `forwardQuery`。不新造打分公式，不加依赖。未用 YAGNI 跳过调用链、D9、D12。 |

## 范围与实现

对照已签收 `POL-L2-DS10-QRY-API` §4.1、`POL-L2-DS10-QRY-METRIC` §6.1、`POL-L2-DS10-QRY-ARCH` §7.1。

- 专题门面 `GET /topic/v1/policy/rank` 写在 `/{id}` 兜底之前。查询参数原样交给 Python `GET /internal/policy/rank`。
- `factor` 只接受 `relevance`（相关性）、`timeliness`（时效性）、`importance`（重要性）。
- 发布时间、效力级别、浏览量仍走已有 `search` 的 `order`（`publish_time` / `level` / `views`）。送进 rank 时不打分，返回诚实空列表，`reason=use_search`。
- Java 不打分。响应去掉 `smartScore`。
- 模型未注册时 Python 返回空列表，`honesty.fabricated=false`，`honesty.empty=true`，`reason=no_registered_rank_model`。不编造排序公式，不写 `metric_id`。
- 注册表里即使出现 `purpose=search_rank` 的模型，本路径也没有打分处理器，仍返回空列表，`reason=rank_handler_absent`。
- 展示侧 `GET /display/v1/policy/panorama/rank` 只委托本入口：前端 → 网关 → `gkxlumen-display` → `gkxlumen-topic-policy` 的 `GET /topic/v1/policy/rank` → Python `/internal/policy/rank`。浏览器不改打专题 URL。本叶不改 display 代码。
- 不进 `gkxlumen-topic-async-service`。不改唐绍祖锁定的合规算法闭包。

## 偏离

- 工作区草稿用 `axis` / `by` / `sort`，并接受中文轴名。已按签收契约改成只读 `factor` 的三个英文取值。中文「重要性」返回 `factor_not_supported`，不当作已接通的排序轴。
- 排序模型未在注册表登记。本叶不补公式、不补 `smartScore`。无模型时是诚实空态，不是编出来的名次。
- 展示模块不在本叶可改文件内，`gkxlumen-display` 未改。委托关系写在本交接，浏览器仍不直打 `/topic/v1/policy/rank`。

## 产物清单

- `repos/lumen-svc-platform`：`PolicyFacadeController`、`PolicyFacadeService`、`RemotePolicyPythonClient` 的 rank 注释与查询名；`PolicyFacadeControllerTest`、`PolicyFacadeServiceImplTest` 的 rank 用例。`PolicyFacadeServiceImpl.rank` 仍走已有 `forwardQuery`，并去掉 `smartScore`。favorites、share、search、docs、metrics 未删。
- `repos/lumen-algo-py`：`vendor/entan-py/api/policy_routes.py` 的 `/internal/policy/rank`；`tests/test_policy_job.py` 的 rank 用例。
- 本交接。未提交、未推送。

## 验收证据

Python（`lumen-algo-py`）：

```
python -m pytest tests/test_policy_job.py -k "rank_without_model or rank_catalog_order or rank_registered_model" -q
```

结果：`3 passed, 17 deselected`。

Java（只跑改到的两个测试类，`gkxlumen-topic-policy`）：

```
mvn -pl gkxlumen-topic-policy-biz -am -Dtest=PolicyFacadeControllerTest,PolicyFacadeServiceImplTest -Dsurefire.failIfNoSpecifiedTests=false -Dmaven.build.cache.enabled=false test
```

结果：`PolicyFacadeControllerTest` 18 通过，`PolicyFacadeServiceImplTest` 34 通过，合计 `Tests run: 52, Failures: 0, Errors: 0, Skipped: 0`。BUILD SUCCESS。未跑全仓 mvn。

## 架构合规自检

1. 算法只在 Python。Java 不计算分数。 ✅
2. 调用链是门面 REST → Python `/internal/policy/rank`，展示不直连 Python。 ✅
3. 未改 Nebula，未改唐绍祖锁定的合规算法闭包。 ✅
4. 沿用既有 Feign 门面，未新开绕过可观测的通道。 ✅
5. D12：Feign `name=lumen-algo-py`，路径 `/internal/policy/**`，无 `demo-*`。 ✅
6. 同步排序，不进 `gkxlumen-topic-async-service`。 ✅
7. D9：199 不是指标。不造 `metric_id`，不写公式，响应无 `smartScore`。 ✅
8. 未加依赖，未写对象存储，未改 D4。 ✅

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 20000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.11 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 20000、api-agent 80/20、B 档 `$3/$15` 回填：`20000×0.80×3/1e6 + 20000×0.20×15/1e6 = 0.108`，记 `0.11`。

## 修改内容

- 门面 rank 查询参数与签收稿对齐为 `factor`。
- Python 无排序模型时返回空目录；目录顺序三列不在本入口打分。
- 测试从 `axis` 改为 `factor`，并覆盖 `order=publish_time` 原样上送、不打分。

## 测试结果

- Python rank 三例通过。
- Java 两个测试类 52 例通过。

## 遗留风险

- 注册表没有检索排序模型。接通前 rank 的成功读面是空列表，不是按相关性打出的名次。
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
- `gkxlumen-topic-policy/.../feign/RemotePolicyPythonClient.java`
- `gkxlumen-topic-policy/.../PolicyFacadeControllerTest.java`
- `gkxlumen-topic-policy/.../PolicyFacadeServiceImplTest.java`
- `lumen-algo-py/vendor/entan-py/api/policy_routes.py`
- `lumen-algo-py/tests/test_policy_job.py`
- 本文件
