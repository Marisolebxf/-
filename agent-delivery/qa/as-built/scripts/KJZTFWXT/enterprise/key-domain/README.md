# 重点企业领域分析 KEYDOM · Playwright 脚本工程（2026-10-14）

- 蓝本：`qa/test-cases/.../KEYDOM-重点企业领域分析/FUNC-重点企业领域分析-用例.md` v2.0（00511~00530，20 条）
- 金样 `gold.yaml`（P0-01~05 = 00511/00512/00515/00516/00518）；全量 `scripts.yaml`（includes + 15 = 20）
- 覆盖：`coverage.md`；环境：`fixtures/testdata.yaml`；实勘：`fixtures/scout/`
- 执行顺序：`agent-delivery/qa/as-built/prompts/KJZTFWXT/enterprise/key-domain/full.md`

## 关键实勘口径

- 路由 `view=domain`（可并存 `workspace=domain`）；侧栏二级，无页内类型/领域 Tab。
- 空态：待选择分析对象 / 尚未选择企业 / 前往对比篮选择企业。
- 结果四大区块：领域布局概览 / 企业领域覆盖 / 跨领域布局 / 重点领域分布。
- 概览四卡：已覆盖领域 / 涉及企业 / 跨领域企业 / 识别依据（评审态 ⓘ 口径名另见 fixtures）。
- 对象路径：页内对比篮确定回填；或系统 dock 发起分析 → 六类型 → 重点企业领域分布分析。
- 评审：persona 菜单 `aria-label=内部评审模式`。
