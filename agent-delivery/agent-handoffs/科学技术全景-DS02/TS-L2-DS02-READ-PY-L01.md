# TS-L2-DS02-READ-PY-L01 · 科学技术全景 · 读图

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:唐绍祖` |
| claim_type | 开工时已是 `in_progress`，本会话未改认领 |
| 说明 | 只实现 `POST /internal/tech-graph/read`。未把任务改为 `done` 或 `ready_to_sign` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 读图单独成模块，不改已有写入。未用 YAGNI 跳过调用链、空间拒绝、空图和截断标记 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ARCH-SEQ`、`TS-L2-DS02-SDD-SEQ` |
| 图 diff | 未改这两张图，语义不动。实现按说明书第 3 节：`gkxlumen-display` → `POST /internal/tech-graph/read` → `demo_gkx_chain` |
| 会签态 | 源文件无 frontmatter。功能架构与说明书已签收。本读图单仍待联调 |
| 说明 | 图在 `科学技术全景-DS02/sdd/l2/TS-L2-DS02-ARCH.md` 第 2 节与 `sdd/科学技术全景-系统详细设计说明书.md` 第 3 节 |

## 问题清单

- 领域筛选依赖挂产业表，不在这张图上。本接口不读那张表，也不按领域把结果滤空。
- 边上若还没有 `evidence_level`、`relation_type`、`path_id`、`step_order`，对应的关系或路径是空数组。这不是失败。
- 路径只取与选中点直接相连的 `tech_path_step`。单次最多 168 步（20 条路径、每条按代表路径 8 步计）。更长的路径不按 `path_id` 再补全。

## 修改内容

- 新增 `POST /internal/tech-graph/read`。只读 `demo_gkx_chain`。请求里的 `space` 不是这个就 422，不改去 `gkx_chain` 或 `entan`。环境空间不对同样拒绝。
- 未选技术点（没有 `technology_node_id` / `technologyNodeId`）：最多 200 个 `tech_point`，不查边。`name_zh` 为空就保持空。
- 选中一个点之后：该点的 `tech_rel` 最多 200。默认只要 `HIGH`、`MEDIUM`；`include_low_evidence` 或 `includeLowEvidence` 为真才带低证据。人、机构、论文、专利每类最多 20。`tech_path_step` 归成的路径最多 20。超出时 `truncated` 对应项为真。
- 空图：`nodes`、`relations`、`keyPathOptions`、`listRecords`、`relationTypeOptions`、`factorItems` 都是空数组，`emptyReason=GRAPH_EMPTY`。不返回演示种子，不写图，不发改写 nGQL。
- 七个字段给展示层装配：`nodes` 只放技术点；`relations` 只放选中点的 `tech_rel`；实体在 `listRecords`（`typeKey` 为 `person` / `institution` / `paper` / `patent`）；路径在 `keyPathOptions`。没有强度就不写 `weight`。
- 不调用 `M_TECH_GRAPH_STRUCT`、`M_TECH_EDGE_STRENGTH`、`M_TECH_ENTITY_TOP5`、`M_TECH_PAPER_PATENT_CNT`、`M_TECH_ENTITY_REL`、`M_TECH_PATH_KEYNODE`。请求里不算影响力、中心度、路径优先级。
- 未改 `POST /internal/tech-graph/vertex` 的写入行为，未改机构入图。

## 测试结果

- `python -m compileall -q lumen_algo_service lumen_common\algorithms\tech_graph_read.py`：退出码 0。
- `python -m pytest -q -p no:cacheprovider tests/test_tech_graph_read.py`：5 passed，1 条 Starlette 弃用警告，约 1.22s。
- 覆盖：`entan` / `gkx_chain` / `demo_entan` 拒绝且不开会话；路由 `POST /internal/tech-graph/read` 对 `space=entan` 返回 422；未选点 201 行截成 200 且语句里没有 `tech_rel` 和改写语句；空结果是空数组；选中后关系 200、论文 20、路径 20，默认语句只含 HIGH、MEDIUM。测试用假会话，不写真实图。

## 遗留风险

- 展示 Java（`SYSINT-05-01B-L01`）尚未改调本接口。页面仍可能是 `GRAPH_NOT_READY`。
- 三个数字仍由后续灌数单写 `ads_technology_panorama_score`，本接口不读这张表。
- 边上图若用了别的属性名，关系或路径会是空的，直到属性名与本读法一致。
- 本会话未等 CI，未核对 K8s rollout。

## CI/CD（必填）

- 分支：`lumen-algo-py` `dev`
- commit：`a03c52b0e8ca39429da2262fd0a56e7a93126964`
- pipeline URL / ID：已 push `origin/dev`。本会话未等 Pipeline，不编链接
- 部署 namespace / 镜像 tag：未核对
- K8s rollout：未核对
- dev 测试 URL / 命令与结果：见上面的 pytest。未打线上读图

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 `lumen-platform-algo-py` 进程内 `TraceHeaderMiddleware`，本接口不另建 tracer
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `lumen-algo-py` `lumen_common/algorithms/tech_graph_read.py`
- `lumen-algo-py` `lumen_algo_service/views/tech_graph_read.py`
- `lumen-algo-py` `lumen_algo_service/main.py`
- `lumen-algo-py` `tests/test_tech_graph_read.py`

## 范围与实现

`POST /internal/tech-graph/read` 只读 `demo_gkx_chain`。未选点最多 200 且不带边。选中后关系 200、每类实体 20、路径 20，超出有截断标记。空图是空数组。

## 偏离

无偏离。路径只取与选中点直接相连的 `tech_path_step`，不按路径编号补更长的链。

## 产物清单

- `lumen-algo-py` `a03c52b`
- `tests/test_tech_graph_read.py`

## 验收证据

`python -m pytest -q -p no:cacheprovider tests/test_tech_graph_read.py`：5 passed。

## 架构合规自检

1. 算法只在 Python，本接口只读不写。✅
2. 调用链供 `gkxlumen-display` 调用 `/internal/tech-graph/read`。✅
3. 空间只接受 `demo_gkx_chain`。✅
4. 可观测沿用现有中间件。✅
5. 已 push `origin/dev`。CI 未核。✅
6. 不写 `gkx_chain` 或 `entan`。✅
7. 不返回 fixture，不算三个数字。✅

## Cost 回填

- actual_tokens: 20000
- model_used: claude-sonnet-4.5
- actual_cost: 0.12
- cost_warn: green
- 会话模型为 Grok 4.7。注册表枚举无此项，按 sonnet 单价与 algorithm 75/25 计入。
