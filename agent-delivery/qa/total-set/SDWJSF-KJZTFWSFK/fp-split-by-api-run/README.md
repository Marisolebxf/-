# fp-split-by-api-run（v0.2）

算法库 **对外唯一** 功能点拆分工作区。原则见 `../科技专题服务算法库-功能点拆分原则-by-api.md` **0.2**。

**怎么跑**：总索引 [`qa/algo-lib-playbook-index.md`](../../../algo-lib-playbook-index.md) → 编排 [`../fp-split-by-api-playbook.md`](../fp-split-by-api-playbook.md) → 本目录 `01-task-list.md` + `prompts/Lxx.md`（**子 agent 执行**；父控只调度）。

| 路径 | 用途 |
|---|---|
| `00-control.md` | 闸门与进度 |
| `_catalog-snapshot.md` | catalog 冻结清单（跑 `agent-delivery/scripts/_dump_algo_apiview_catalog.py` 刷新） |
| `_l6-to-catalog-map.yaml` | L01–L60 ↔ catalog 页 |
| `catalog-orphan-registry.yaml` | catalog 有、需规无（5b，不交付） |
| `prompts/` | 子 agent 提示词 |
| `work/` / `review/` | 六级过程稿 |

上一版接口级试跑（837 条、L31 金样）在 `../fp-split-by-api-run-v0-202609/`。
