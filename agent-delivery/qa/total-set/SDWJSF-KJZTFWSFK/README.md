# 科技专题服务算法库 · 功能点拆分（两套并存）

本目录同时放 **两套拆法**，不要混读、不要把 by-api 存成 `_v3.xlsx`。

| 套 | 原则 | 循环目录 | 合表 | 状态 |
|---|---|---|---|---|
| 需规口径 | `科技专题服务算法库-最细颗粒度功能点拆分原则-v1.md` | `fp-split-run/` | `…功能点拆分_v1.xlsx`（3347）· `_v2.xlsx`（3960） | **冻结**。禁止覆盖 |
| **by-api** | `科技专题服务算法库-功能点拆分原则-by-api.md` | `fp-split-by-api-run/` | `…功能点拆分-by-api_v1.xlsx`（尚未合表） | **准备中**。60 六级子任务，先金样 L31 |

by-api 真源 = 原 60 条六级需规 + `lumen-ui-algo-apiview` catalog。执行时一条六级一个子 agent，中间过程留在 `fp-split-by-api-run/{prompts,work,review}`。
