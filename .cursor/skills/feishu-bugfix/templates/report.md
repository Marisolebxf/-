# 缺陷修复报告（渲染契约）

> 本文件不是手工填写模板，也不是运行时数据源。
> `.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report` 以固定渲染器生成实际 `report.md`；请勿复制本文件后手填事实。
> 实际报告固定包含：缺陷事实、根因与需规功能点覆盖（SRS 文件 + 序号/五级路径）、改动摘要与跨仓 Bundle 拓扑、验证矩阵（基础 fix / regression；按缺陷类型追加 boundary / integration / data / algorithm / security / performance / rollback）、风险、S/M/L、数据 policy、失败分类、提测信息（含 candidate / merge / deployed SHA 和 pipeline URL）、精确验收口令、飞书状态迁移、Gate、自动决策、回滚。
> 证据表必须显示 `reviewable`、`raw_retained` 和不可复核原因；`reviewable=false` 或 `raw_retained=false` 的证据不得支撑验证 PASS。DB 写证据还必须显示进入开发 gate、policy/scope hash 和写授权 ID；pipeline/rollout 字段明确标注为 Agent 查询记录。
