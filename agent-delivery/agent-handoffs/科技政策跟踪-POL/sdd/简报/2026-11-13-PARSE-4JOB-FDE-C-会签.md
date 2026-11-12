# POL-L2-PC2-PARSE-4JOB-FDE · C 波 · 会签

- 总单：`POL-L2-PC2-PARSE-4JOB-FDE-L01`
- 日期：2026-11-13
- **监管人裁定**：卡1=A / 卡2=A / 卡3=A（按推荐执行）

## 锁定

| 卡 | 裁定 |
|---|---|
| 1 | `evaluation/jobs` × 四 `sub_type`：`policy_parse_semantic` / `policy_parse_clause` / `policy_parse_metric` / `policy_parse_entity` |
| 2 | 条款亦 async Job（worker 内复用 enrich） |
| 3 | 指标/实体写入 `ads.policy_text_parse.structured_elements`，不新表 |

## 会签结论

- 通过：与 237/242 同构；治理 `parse/clauses` 旁路保留；元信息并行 `panorama/detail`
- D 波：algo 四入口 + Java/async 白名单 + FE 一点并行起四 Job 并回填 KPI/四 Tab
