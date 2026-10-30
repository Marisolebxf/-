# KG-7ELEM-BUILD · 派单条

薄条不能单独开工。先读总控和厚包。

| 顺序 | 粘贴任务 | 门 |
|------|----------|----|
| 1 | `KG-7ELEM-BUILD-REQ-L02` | 现在可以领 |
| 2 | `KG-7ELEM-BUILD-REQ-L03` | L02 handoff 已在，且 ≥ integration |
| 3a | `KG-7ELEM-BUILD-REQ-L04` | L03 handoff 已在，且 ≥ integration |
| 3b | `KG-7ELEM-BUILD-REQ-L05` | 与 L04 同一道门，产物路径不同，可并行 |
| 4 | `KG-7ELEM-BUILD-REQ-L01` | L02～L05 都 ≥ integration。已认领，不要再次 task-claim |

每叶 `/goal` 头用厚包的身份、强度、监管人、锁。范围只做厚包表格里该叶的「只写」列。
