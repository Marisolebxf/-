# DATA-POLICY-STORAGE-NEBULA-ETL-L01 · 补 etl/pipeline-to-nebula.md（as-built 回填）

## 任务认领

| 字段 | 值 |
|---|---|
| task_id | `DATA-POLICY-STORAGE-NEBULA-ETL-L01` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| repo / branch | `gkx-orchestration` / `origin/dev` |

## Ponytail

- ponytail: `full`
- 复用 ENT/CHAIN 同名文档的指针式结构与 POLICY 树既有 frontmatter 约定；未新建目录、未造模板、未引入工具。文档长度按 as-built 需要落，不铺不必要章节。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | **无**。本叶只把图中已 approved 的 `polan → demo_gkx_chain` 实线补上 ETL 侧文字说明，拓扑未动，不翻签。 |
| 会签态 | `approved`（`human:淮政玮` · 2026-08-21）维持 |

## 缺口来源

2026-08-31 存储设计完整度核查发现：B 叶 `POLICY-NEBULA-PROJECT-CHAIN-L01` 已 `done`、政策点边实际已投影进 `demo_gkx_chain`，但 ENT / CHAIN 都有的 `etl/pipeline-to-nebula.md` 在 POLICY 树缺位。施工已发生、文档未回填，as-built 与存储设计树脱节。

## 修改内容

- 新增 `storage/POLICY/etl/pipeline-to-nebula.md`（as-built，9 节）：入口与源、space/VID 强制约束、schema 增量 nGQL、挂接解析规则、写入幂等、fail-soft 与环境变量、首轮实投影基线、禁止清单。
- `storage/POLICY/README.md` 读序第 4 条挂入本文件并标 as-built。
- `storage/POLICY/CHANGELOG.md` 追加 2026-08-31 行。
- **未改**业务仓代码，**未** APPLY DDL，**未**灌数，**未**改 `stores/nebula.md`。

## 发现的不一致（不静默修）

`stores/nebula.md`（S3，`ready_to_sign`）把四类边写成：

```
support(weight double, factor_type string, src_table string)
apply_to(weight double, src_table string)
regulate(weight double, src_table string)
cite(relation string, weight double)
```

`polan/graph/nebula_loader.py` 实际建的是统一 `(weight double, props string)`（`EDGES` 常量 + `ensure_schema()`）。

处理：新文档 §4 以 as-built 为准并挂 ⚠️ 显式标注差异，转 `OPEN-POLICY-GRAPH-03` 升级 `human:淮政玮`。**不在本叶改 S3 已收单文档**——细表列语义变更属结构项，按长任务规约 §7.3 需升级，不由文档叶自行拍板。

## 验收证据

- 事实来源：B 叶 handoff `POLICY-NEBULA-PROJECT-CHAIN-L01.md`（commit `32124a0`、trace `1854b8f4688ca5206b10e22cfdb1ed3e`）+ 源码 `polan/graph/nebula_loader.py`、`polan/common/nebula.py` 逐条比对，未凭推测落笔。
- 文中每项约束均可回源：space 常量与 `conf()` 校验、`ensure_schema()` nGQL、`_vid()` 前缀与 80 长度、`_exists()` FETCH 证明、`chunk=100` 批量、`available()` 探活回退、`POLAN_NEBULA_*` 环境变量。
- 首轮基线数字（节点 47655 / 边 398 / 各类跳过数）直接引自 B 叶实投影记录。
- 无 CI（定义叶）。链接与相对路径已按 POLICY 树层级核对。

## 遗留风险

- `OPEN-POLICY-GRAPH-03`（边列定义对齐）未决，需淮政玮裁决 S3 是否跟改。
- 跳过量偏大（industry 850 / org 574）本质是 ADS 镜像缺稳定 ID，属 `OPEN-POLICY-GRAPH-01` 范畴，本叶只记录不改善。
- 政策 ETL 其余缺口仍在：`pipeline-ods-to-dwd` / `dwd-to-ads` / `dwd-to-es` / `mock-to-ads` / `etl/README.md` 未补。

## CI/CD

- 分支：`gkx-orchestration` `origin/dev`
- commit：待提交（`[agent:data-agent]`）
- pipeline / K8s：N/A（编排仓文档叶）

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-to-nebula.md`（新增）
- `agent-delivery/data/data-design/storage/POLICY/README.md`
- `agent-delivery/data/data-design/storage/POLICY/CHANGELOG.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本叶零代码改动；文档记录写图仍归 `polan` |
| 调用链 / D12 | ✅ 未改调用链；文档明确 Java 只读 ADS、禁直连 nGQL |
| 图谱 Nebula 一张 G | ✅ 仅 `demo_gkx_chain`；禁 Neo4j、禁 `gkx_policy` 目标态 |
| 无闸门不写正式库 | ✅ 文档重申 `gkx_chain` 零写入；本叶不灌数 |
| D9 血缘 | ✅ 源表 → space → 读路径链路可追溯 |
| 可观测 | ✅ 引用 B 叶 trace/span 作 as-built 证据 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 47000 |
| model_used | claude-opus-4.6 |
| actual_cost | 0.62 |
| cost_warn | green |
