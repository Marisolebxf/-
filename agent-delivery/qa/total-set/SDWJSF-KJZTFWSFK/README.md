# 科技专题服务算法库 · 功能点拆分（两套轨道）

本目录 **需规口径** 与 **by-api** 并存；合表与交付角色见下表（v0.2 #1）。

| 套 | 原则 | 循环目录 | 合表 | 状态 |
|---|---|---|---|---|
| 需规口径 | `科技专题服务算法库-最细颗粒度功能点拆分原则-v1.md` | `fp-split-run/` | `…功能点拆分_v1.xlsx` / `_v2.xlsx`（3960） | **内部对照**；`QA-KJZTFWALGO-FUNCLIST-SPLIT-L01` 未签收 |
| **by-api** | `科技专题服务算法库-功能点拆分原则-by-api.md` **0.2.1** | `fp-split-by-api-run/` | `…功能点拆分-by-api_v1.xlsx`（待合表） | **对外唯一交付**；字段级；金样 L01→L13 |

by-api 真源 = 60 条六级需规 + `lumen-ui-algo-apiview` catalog。旧接口级试跑归档：`fp-split-by-api-run-v0-202609/`。

执行：**A 线** 总索引 [`qa/algo-lib-playbook-index.md`](../../../algo-lib-playbook-index.md) · [`fp-split-by-api-playbook.md`](fp-split-by-api-playbook.md) · 一条六级一个子 agent → `fp-split-by-api-run/{prompts,work,review}`。**B 线** 同总索引 + [`qa/algo-lib-api-case-playbook.md`](../../../algo-lib-api-case-playbook.md)（接口用例，可与 F3 并行）。
