# TS-L2-DS09-OV-API · Handoff（薄）

- **任务**：`TS-L2-DS09-OV-API`（definition）· **执行**：agent:zcode 会话代跑 api-agent（子智能体起草）· **监管**：human:王梓真 · **日期**：2026-11-06
- **主产物**：`agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-DS09-OV-API.md`（511 行，9 端点定稿 + 501 信封 + 枚举逐字 + 订阅面 + FE 接线差异 + 批 4 delta）

## 范围与实现
9 端点（契约 §3.1–§3.6 + metric-system）路径/DTO/枚举/错误码定稿；501 信封 + 开关建议 `planning.direction-alert.registered`；caliber_note 等口径文案表行携带；订阅面 rule_type=planning_resource（注意：DATA 分册实测既有代码族用 scope_type 字段名，会签统一）；FE 接线清单（仅 techDevelopmentPlan.ts 拼装层，页面零改动）。

## 偏离
- 服务内路径定为无前缀插序（契约 §1 原文为 /v1/situation/planning/**，分册按网关 /display/v1/situation/planning/** 对外、服务内直挂）——批 4 冻结时确认。
- 4 项批 4 契约增补建议 + map_center/zoom 展示常量豁免——见分册，待会签裁定。

## 架构合规自检
前端→Java→只读 ADS ✅；无个人明细（U6）✅；501 语义 ✅；D18 无接口直返 mock ✅；不重做 FE-TS-09A ✅。

## Cost
actual_tokens ≈ 504782（子智能体）+ 会话调度 ≈ 560000；model_used = GLM-5.3-Highspeed；actual_cost ≈ $0.8；cost_warn = green。
