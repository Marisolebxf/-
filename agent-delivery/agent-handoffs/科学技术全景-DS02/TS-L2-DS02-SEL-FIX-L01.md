# TS-L2-DS02-SEL-FIX-L01 · 全景图选中技术点下发 technology_node_id，透传 truncated

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | task_type = bugfix，P0；registry 状态由 coordinator 推进，本叶不动 task-registry |

## Ponytail（coding 任务必填）

ponytail: full

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单一致。只改共用的选中编号读取点和下游 query 键，未新增类、依赖或接口。D8/D9/D10、可观测未涉及，未以 YAGNI 跳过 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 小 diff 修复，未用 |

## 范围与实现

**问题清单**

- `gkxlumen-display` 的 `SituationPanoramaService.query()` 把选中技术点以 `techPointId` 发给 Python `POST /internal/tech-graph/read`。
- `lumen-algo-py/lumen_common/algorithms/tech_graph_read.py` 的 `_node_id()`（第 88 行）只读 `technology_node_id` / `technologyNodeId`。所以选中后 Python 仍按「未选」处理，关系、实体、路径永远为空。
- Python `data.truncated` 是一个布尔标志对象（`nodes / relations / person / institution / paper / patent / paths`）。Java 只按自己的截断规则生成 `truncated`，Python 的标志被丢掉。

**修改内容**

1. 新增私有方法 `selectedId(request)`，读取 `techPointId / nodeId / selectedNodeId / selectedGraphNodeId / technology_node_id / technologyNodeId`。`assemble()`（原第 152 行）和 `query()`（原第 242 行）两处都用它，口径一致。
2. `query()` 下发键由 `techPointId` 改为 `technology_node_id`。
3. `assemble()` 先把 Python `data.truncated` 中为真的标志并入响应 `truncated` 对象，再叠加 Java 自己的截断标志（`nodes / relations / entities / paths`）。七个既有字段（`nodes, relations, keyPathOptions, timeline, listRecords, relationTypeOptions, factorItems`）未改名。
4. 单测：扩展 `SituationPanoramaControllerTest.selectedPointKeepsListsAndReadsThreeScoresOnly`。断言下游 query 含 `technology_node_id=p1`、不再含 `techPointId`；断言 Python `truncated.patent=true` 透传，`truncated.relations=false` 不出现。

## 偏离说明

- **`truncated` 是对象，不是单个 boolean。** 派单写「加 `truncated` (boolean)」。实际上 Python 返回的就是标志对象，Java 响应原本已有同名 `truncated` 对象（既有单测断言 `$.data.truncated.entities`）。改成单个 boolean 会破坏既有契约且丢失分项信息，所以保持对象形态，只把 Python 为真的分项并入。没有任何截断时仍不输出该字段（与原行为一致）。
- 字段名：Python `data.truncated`（`dict[str, bool]`），Java 响应 `data.truncated`（`Map<String, Boolean>`，仅含为真的键）。

## 产物清单

| 仓 | commit | 说明 |
|----|--------|------|
| lumen-svc-platform | `732a586bc28fa7aad40a2020ab94ea67a154ea47` | `fix(display): 选中技术点下发 technology_node_id，透传 truncated [agent:api-agent]` |

涉及文件：

- `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/SituationPanoramaService.java`
- `gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/controller/SituationPanoramaControllerTest.java`

## 验收证据

**测试结果**

- 命令（仓根，JDK 17 + Maven 3.9.9）：`mvn -q -o -pl gkxlumen-display -am test "-Dtest=SituationPanorama*" "-DfailIfNoTests=false" "-Dsurefire.failIfNoSpecifiedTests=false"`
- 结果：退出码 0。`SituationPanoramaControllerTest` 10/10 通过；同次运行的 display 模块其余测试类 0 失败。
- `spring-javaformat:apply` 已在本模块执行；格式化波及的 62 个无关文件已还原，只提交本叶两个文件。
- 派单方 pod 内实测：`technology_node_id=tcn_000f21ac06aceb9cdd0575e82d0d85fc` 返回 65 条关系、61 个实体、2 条路径。

## CI/CD（必填）

- 分支：`dev`
- commit：`732a586`
- pipeline：[#4200](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/4200)，`backend:build`、`backend:image:display`、`deploy:display` 均 success；整体状态 `manual`（helm/nacos 手动作业未触发，与此前 pipeline 一致）
- `e2e:chain-gold` bridge：failed，`downstream_pipeline_creation_failed`。前两条 pipeline #4198、#4197 同样失败，属既有问题，与本叶无关
- K8s rollout：`deploy:display` success
- dev 端到端（选中技术点后前端看到关系/实体/路径）：本叶未在 dev 页面复测，待 QA

## 遗留风险

- 前端若只读 `truncated.entities`，Python 的 `person / institution / paper / patent` 分项需要前端自行映射；本叶未改前端。
- e2e:chain-gold 下游 pipeline 创建失败需另行排查（非本叶）。

## 架构合规自检（D1–D18）

| 条 | 结论 |
|----|------|
| D1 算法只在 Python | ✅ Java 只改参数键和字段透传，无算法 |
| D2 调用链 前端→Java→Python `/internal/*` | ✅ 未变 |
| D3 NebulaGraph | ✅ Java 不接图；Python 侧读 Nebula，未改 |
| D4 可观测 | ✅ 未改动埋点，沿用既有 Java Agent |
| D5 CI/CD | ✅ push → pipeline #4200 → deploy:display success |
| D6 demo 只读不 merge | ✅ 未涉及 demo 仓 |
| D7 共享聚合核心 | ✅ Java 不写 nGQL、不做算法 |
| D8 前端规范 | N/A 未改前端 |
| D9 数据血缘 | N/A 未新增指标 |
| D10 交互规范 | N/A |
| D12 demo/lumen 隔离 | ✅ 下游仍为 `lumen-algo-py`，未调用任何 `demo-*` 服务 |
| D14 对象存储 | N/A |
| D16 缺项补齐 | N/A |
| D17 合规/合理 | N/A 未改算法 |
| D18 可实现 | ✅ 无写死 mock |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~180k（估） |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ~$3（估） |
| cost_warn | false |
