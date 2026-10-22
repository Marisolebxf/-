# As-built 过程提示词

人读名称与文件对应：

| 步骤 | 人读名 | 提示词 | 主要产物 |
|------|--------|--------|----------|
| 1 | **测试用例** | [`_case.md`](_case.md) | `qa/test-cases/.../FUNC-*-用例.md` + **功能点→场景用例**覆盖矩阵 |
| 2 | **测试脚本** | [`_script.md`](_script.md) | `as-built/scripts/.../*.yaml` + **脚本→场景用例**覆盖矩阵 |
| 2a | **重写波父控** | [`rewrite-wave-parent.md`](rewrite-wave-parent.md) | 新对话只读此文件。不在对话里再贴长提示词 |
| 2b | **重写波子 agent** | [`rewrite-wave-child.md`](rewrite-wave-child.md) | 父控整份下发，只替换【】 |
| 2c | **404 重跑父控** | [`rewrite-wave-parent-404.md`](rewrite-wave-parent-404.md) | 只派旧 404 且已有 yaml 的 blocked。新对话只读此文件 |
| 2d | **404 重跑先跑** | [`rewrite-wave-child-404.md`](rewrite-wave-child-404.md) | 贴在 2b 之前。绿了停；页面打开仍红才改写 |
| 2e | **门户拆册 22 条父控** | [`rewrite-wave-parent-split.md`](rewrite-wave-parent-split.md) | 只派 05490–05511。新对话只读此文件。子提示词仍用 2b |
| 2f | **剩余 pending 32 条父控** | [`rewrite-wave-parent-pending.md`](rewrite-wave-parent-pending.md) | 只派当前 32 条 pending。已有 yaml 的 04296、05191 按用例覆盖。新对话只读此文件。子提示词仍用 2b |
| 2g | **覆盖表补齐父控** | [`coverage-fp-parent.md`](coverage-fp-parent.md) | 一册一路，并行 3。齐了父控自己合 B 线交付表。子提示词用 2h |
| 2h | **覆盖表子 agent** | [`coverage-fp-child.md`](coverage-fp-child.md) | 只改一个目录的 coverage-fp.md |
| 3 | **测试结果** | [`_result.md`](_result.md) | `as-built/runs/{run-id}/` 明细 + `SUMMARY.md` |
| 4 | **总集提交表** | [`_submit.md`](_submit.md) | 场景用例 **切点投影** 成「一功能点一行」；不处理未覆盖点 |

企业查询专属顺序仍可放在 `prompts/KJZTFWXT/enterprise/search/gold.md` / `full.md`，不得覆盖上述文件的禁止项。
