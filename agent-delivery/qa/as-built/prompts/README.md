# As-built 过程提示词

人读名称与文件对应：

| 步骤 | 人读名 | 提示词 | 主要产物 |
|------|--------|--------|----------|
| 1 | **测试用例** | [`_case.md`](_case.md) | `qa/test-cases/.../FUNC-*-用例.md` + **功能点→场景用例**覆盖矩阵 |
| 2 | **测试脚本** | [`_script.md`](_script.md) | `as-built/scripts/.../*.yaml` + **脚本→场景用例**覆盖矩阵 |
| 2a | **重写波父控** | [`rewrite-wave-parent.md`](rewrite-wave-parent.md) | 新对话只读此文件。不在对话里再贴长提示词 |
| 2b | **重写波子 agent** | [`rewrite-wave-child.md`](rewrite-wave-child.md) | 父控整份下发，只替换【】 |
| 3 | **测试结果** | [`_result.md`](_result.md) | `as-built/runs/{run-id}/` 明细 + `SUMMARY.md` |
| 4 | **总集提交表** | [`_submit.md`](_submit.md) | 场景用例 **切点投影** 成「一功能点一行」；不处理未覆盖点 |

企业查询专属顺序仍可放在 `prompts/KJZTFWXT/enterprise/search/gold.md` / `full.md`，不得覆盖上述文件的禁止项。
