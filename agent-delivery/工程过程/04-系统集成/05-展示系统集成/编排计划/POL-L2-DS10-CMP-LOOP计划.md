# 政策重点比对 · LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-CMP-合规演示用例.md`
- 系统：科技信息展示系统。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-08

- 状态：2026-11-10 第三轮。**样本满足（停止：完成）**。期望重冻结单 `POL-L2-DS10-CMP-DEMO-FIX-R20261110-DATA` 已由本会话代跑并签收（human:hzw「检查并签收」+ self_claim 先例）；第三轮真实复测 `cmp_round3.py` 26 PASS / 0 FAIL / 1 SKIP（213/214/215/216/217 全过，218 写型按规程跳过）。验收单 `POL-L2-DS10-CMP-DEMO-ACCEPT-LOOP` 已改 `done`（操作人 human:hzw）。用户报障 213 数据侧验证通过；界面待前端修复 `lumen-ui-science-pc a255d94` 部署生效。
- 对标双方（216/217/218）：固定 `北京市` ↔ `广东省`。见用例文首说明；循环不得改用其它省组合。

不派数据单，不派算法单，不打探测。

人说「按 LOOP 跑」之后，再按 §6.5 建常驻验收单 `POL-L2-DS10-CMP-DEMO-ACCEPT-LOOP`。不把这张单签 `done`。
