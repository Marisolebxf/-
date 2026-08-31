# DATA-POLICY-STORAGE-EDGE-SEMANTIC-L01 · stores/nebula.md 补四类边语义

## 任务认领

| 字段 | 值 |
|---|---|
| task_id | `DATA-POLICY-STORAGE-EDGE-SEMANTIC-L01` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| repo / branch | `gkx-orchestration` / `origin/dev` |
| depends_on | `DATA-POLICY-STORAGE-NEBULA-ETL-L01`（≥ ready_to_sign） |

## Ponytail

- ponytail: `full`
- 语义表直接落在既有 `stores/nebula.md`，未新建 `edges.md` 之类的第二份文档；不重复 ETL 文档已写的投影流程，只用一句指针互链。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | **无**。只补边语义文字，拓扑与边类型集合未变，不翻签。 |
| 会签态 | `approved`（`human:淮政玮` · 2026-08-21）维持 |

## 缘起

用户 2026-08-31 指出 `stores/nebula.md` 只有四类边的 nGQL，没有说明每类边代表什么业务关系，读者无法判断 `support` 与 `apply_to` 的边界。

## 修改内容

`storage/POLICY/stores/nebula.md` 新增「四类边语义」节，位于 DDL 块之前：

- 语义表：中文含义 / 起点→终点 / 源字段 / 权重 / props，逐行回源 `polan/graph/entity.py` RE 段（L109–156）。
- 四条要点：`support` vs `apply_to` 的资源流向与效力范围之分、产业同时拿两条边、`regulate` 与 `support` 不重叠、`cite` 批内校验不造悬挂边、边权之和即 `relation_degree` 计算基础。
- 说明 Nebula 实际落地少于 ADS 镜像（挂接需解析既有顶点，`talent` / `tech` 本波不上图），指向 ETL 文档 §8 的跳过明细。
- DDL 块加 ⚠️：per-edge 列 `factor_type` / `src_table` / `relation` 是设计意图，as-built 统一为 `(weight double, props string)`，转 `OPEN-POLICY-GRAPH-03`。

**未改** DDL 块本身、未改代码、未 APPLY、未灌数。

## 验收证据

逐条回源，未凭字面推测：

| 结论 | 代码位置 |
|---|---|
| 方向一律 policy 起点 | `entity.py` `add_edge(pkey, ...)` 全部以 `pkey` 为 src |
| industry 同时得 support+apply_to | L118–119 连续两次 `add_edge` |
| support 权重 0.8 / 0.5–0.9 / 0.7 | L118（industry）· L126（enterprise，`rng.uniform`）· L134（talent） |
| apply_to 权重 0.6 / 0.5 | L119（industry）· L147（service） |
| regulate 0.6 且 org_type=implement | L139–140 |
| cite 1.0 + `relation:上位` + 批内校验 | L150–156，`if up in pid_set` |
| 边权和 = relation_degree | `polan/eval/focus.py` 模块头 |
| 落地差异与跳过数 | B 叶 handoff `POLICY-NEBULA-PROJECT-CHAIN-L01.md` |

无 CI（定义叶）。相对链接已按目录层级核对。

## 遗留风险

- `OPEN-POLICY-GRAPH-03`（DDL per-edge 列是否跟改 as-built）仍待淮政玮裁决，本叶只标注不改。
- `support` 对 enterprise 用 `rng.uniform(0.5,0.9)` 随机权重，属 Mock 阶段产物；接真数据后权重口径需重定，届时本表要跟改。

## CI/CD

- 分支：`gkx-orchestration` `origin/dev`
- commit：待提交（`[agent:data-agent]`）
- pipeline / K8s：N/A（编排仓文档叶）

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/stores/nebula.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 零代码改动 |
| 调用链 / D12 | ✅ 未涉及 |
| 图谱 Nebula 一张 G | ✅ 仅描述 `demo_gkx_chain` 内边语义 |
| 无闸门不写正式库 | ✅ 本叶不灌数、不 APPLY |
| D9 血缘 | ✅ 每类边可追到 DWD 源字段 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 21000 |
| model_used | claude-opus-4.6 |
| actual_cost | 0.28 |
| cost_warn | green |
