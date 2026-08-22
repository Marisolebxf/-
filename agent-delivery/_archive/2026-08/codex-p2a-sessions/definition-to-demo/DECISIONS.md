# DECISIONS.md

## Decision 001

Question:

覆盖机制的适用范围。

User choice:

面向未来模块复用；E1 企业查询仅作为已完成人工核对的参考样本。

Rationale:

目标是让后续如 E-31 企业发展在定义清晰后可自动驱动 Demo 落地，避免每个模块重复人肉核对。

Impact on plan:

从“E1 补充清单”改为“跨会话 Skill + 模块级实施覆盖契约”；E-31 成为首个实际使用对象。

Status:

Confirmed

## Decision 002

Question:

Skill 的适用范围和输入方式。

User choice:

不绑定任何具体需求编号；后续其他模块也必须可用。

Rationale:

目标是形成可复用的工作流能力，而不是为 E-31 定制一次性自动化。

Impact on plan:

Skill 使用通用输入 `{module-id}` 或 `{definition-package-path}`，并自动发现相关任务、文档和目标 Demo 仓库。

Status:

Confirmed

## Decision 003

Question:

实施覆盖契约的生命周期与自动化边界。

User choice:

采用推荐默认值：定义冻结时生成初版，后续变更增量更新；机器可判定项未通过则阻断；默认自动实施，仅在定义 P0 矛盾或缺失、范围变化、文件集冲突或需人判断的语义/视觉取舍时暂停。

Rationale:

减少人工反复核对，同时保留人对业务与视觉判断的决策权。

Impact on plan:

创建通用 `$gkx-definition-to-demo` Skill；它支持任意模块 ID 或定义包路径，不绑定 E-31 或 E1。

Status:

Confirmed
