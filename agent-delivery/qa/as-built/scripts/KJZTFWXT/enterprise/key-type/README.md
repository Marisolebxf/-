# 重点企业类型分析（KEYENT / view=type）测试脚本

- 入口：`catalog/KJZTFWXT.yaml` → `ent-key-type`
- 金样：`gold.yaml`（P0-01 … P0-05，禁止改 id）
- 全量：`scripts.yaml`（`includes` 金样）
- 覆盖矩阵：`coverage.md`（脚本 → 用例）
- 提示词：`../../../prompts/KJZTFWXT/enterprise/key-type/gold.md` · `full.md`
- 人读用例：`qa/test-cases/KJZTFWXT/KEYENT/FUNC-重点企业类型分析-用例.md`

只测 `view=type` / `workspace=type`。不要把「重点企业领域分析」写进本套脚本。
后续追加 P1 在 `scripts.yaml`，不要改已有 `id`。
