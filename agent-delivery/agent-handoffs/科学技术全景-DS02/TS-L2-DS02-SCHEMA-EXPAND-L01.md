# TS-L2-DS02-SCHEMA-EXPAND-L01 · Nebula Tag/Edge 扩列（描述/实体属性/路径正文）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | Q072 拍板「另开 Tag/Edge 扩列」。不开工 `SYSINT-TECHGRAPH-02-L02`/`L03`。不改 `task-registry.yaml`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最小扩列 + 读投影 + 样本灌值；未用 YAGNI 跳过 DESCRIBE/灌数/读图联通核验。 |

## 修改内容

### DDL（`demo_gkx_chain`）

| 对象 | 新增列 |
|------|--------|
| TAG `tech_point` | `description string`, `development_status string` |
| TAG `tech_paper` / `tech_patent` / `tech_institution` / `tech_person` | `year int` |
| EDGE `tech_has_paper` / `tech_has_patent` / `tech_has_institution` | `relation_strength double`（对齐 chain `supplies.relation_strength`） |
| EDGE `tech_has_person` | 同上 `relation_strength`（保留原 `source_paper`/`source_topic`） |
| EDGE `tech_path_step` | `summary string`, `path_type string`, `time_label string` |

脚本：`scripts/nebula/expand_tech_graph_schema_q072.ngql` + `scripts/seed/expand_tech_graph_schema_q072.py`（`--check` / `--apply`）。

### 仓内契约

- `_TAGS` / `_EDGES`（`tech_graph.py`）与上表一致；写路径 `CREATE … IF NOT EXISTS` 带新列。
- `tech_graph_read.py` 投影：
  - 节点：`description`、`developmentStatus`
  - `listRecords`：`relationStrength`/`weight`、`year`、`updatedAt`（年四位）、非空 `name_zh`
  - `keyPathOptions`：`summary`、`pathType`/`typeKey`；阶段节点 `timeLabel`
- Java display：`normalizePoint` 不剥未知字段，**未改 Java**。

### 样本灌值（seed counts）

样本点 `tcn_000f21ac06aceb9cdd0575e82d0d85fc`：

| 项 | 数量 / 结果 |
|----|-------------|
| tech_point 描述/发展状态 | 1 |
| paper / patent / institution / person 顶点 year+name | 13 / 20 / 20 / 8 |
| tech_has_* `relation_strength` 边 | 61 |
| tech_path_step 正文/类型/时间（两案路径步） | 3 |

路径灌值注意：`WHERE e.path_id == …` 会 `IndexNotFound`；脚本改为从样本点扫边再按 `path_id` 过滤。

## 测试结果

- 单测：`tests/test_tech_graph_{read,edge,vertex}.py` → **26 passed**
- 现场：`python scripts/seed/expand_tech_graph_schema_q072.py --apply` 后 `--check`：
  - `DESCRIBE` 新列齐
  - 样本点 description/development_status 非空
  - 论文 name_zh + year + relation_strength 非空
  - `tep_8392b7f8…` / `tep_6cddc27a…` 有 summary / path_type / time_label
- `read_graph({technology_node_id: tcn_000f21ac…})`：节点带描述；`listRecords` 论文 13/13 有名+强度；路径 2 条带正文/类型/timeLabel

### 核验片段（无密钥）

```
DESCRIBE TAG tech_point → … description, development_status …
DESCRIBE EDGE tech_has_paper → relation_strength
DESCRIBE EDGE tech_path_step → path_id, step_order, summary, path_type, time_label

sample_point.description = 围绕神经性厌食症治疗路径的临床证据与干预手段演进。
sample_point.development_status = 临床转化期
path tep_8392b7f8… summary/path_type/time_label 非空
path tep_6cddc27a… summary/path_type/time_label 非空
```

## 遗留风险

1. 扩列后**线上 algo-py 镜像**需 CI rollout 才把新投影带到 K8s；图库侧列与样本已写入 `demo_gkx_chain`。
2. 前端 `entityRowsFromListRecords` 目前用 `relationCount` 作 score，未直接读 `relationStrength`——数据已在 `listRecords` 透出，FE 接线不在本单。
3. 全量历史边/点未回填，仅样本点邻域演示灌值；其余行新列为空属预期。
4. 未开工 L02/L03。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`
- commit：`a25e7ced96504221b3e021df0283e984e8ff047a`
- pipeline：push 触发；本机未等 CI 绿
- K8s rollout：待 CI
- 图库：本机 `--apply` 已写 `demo_gkx_chain`（口令未打印）

## 架构合规自检

1. 算法只在 Python：✅  
2. 调用链未越层：✅  
3. 只写 Nebula demo space：✅  
4. 未开工 L02/L03：✅  
5. 未改 task-registry.yaml：✅  
6. D4 mock 未伪绿：✅  
7. 未动其他会话脏文件（如 POL-L2-DS10-QRY）：✅  

## Cost 回填（建议）

- actual_tokens: ~45000
- model_used: composer-agent-router
- actual_cost: 0.20
- cost_warn: green

## 涉及文件

- `lumen_common/algorithms/tech_graph.py`
- `lumen_common/algorithms/tech_graph_read.py`
- `tests/test_tech_graph_read.py` / `tests/test_tech_graph_edge.py`
- `scripts/nebula/expand_tech_graph_schema_q072.ngql`
- `scripts/seed/expand_tech_graph_schema_q072.py`
- 本 handoff
