# 政策舆情评估 · LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-SENT-合规演示用例.md`
- 系统：科技信息展示系统。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

- 状态：2026-11-09 第三轮（期望刷新后复测）。样本满足：是（停止：完成）。207/209/210/211/212 全部通过、208 设计无资源不请求（断言 10/10，见 handoff 第三轮表）。本轮子任务 `POL-L2-DS10-EXPECT-REFRESH-L01` 已签收（human:淮政玮 指令）。验收单 `POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP` = `ready`（常驻单按计划约定不签 done；样本已满足，待监管人明示）。handoff：`agent-handoffs/科技政策跟踪-POL/POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP.md`

- 换新令牌（cbac64ed…，登录主体 userId=3101）后全量重测。
- 211 `GET /panorama/assessment-report`：id 2 五段正文与 generated_at 逐字一致 ✅（camelCase 键：scopeText/achievementText/socialImpact/problemText/suggestionText/reportBody）。
- 210 `GET /panorama/feedback`：旧 6 行仍在（含 GF-POL-SENT-210-01 评分 4.50）✅，但总量 6→406（问卷 134/在线评价 147/意见征集 125，并行灌数新增）→ 排序断言失效，归 DATA。
- 207 `GET /panorama/search?keyword=人工智能`：旧行 18323509/18363833 仍在且字段一致 ✅，但 total 73→129（SYN 合成行混排且按 publish_date 抢首条）→ DATA。
- 209 `POST /panorama/jobs {"sub_type":"policy_effect"}`：region_effect 31 行结构在，广东 440000 评分 15.0→28.26（口径说明文案同步刷新为「广东省效果评分28.26（v2 确定性口径…）」）→ DATA（ADS 被并行重算）。
- 212 `POST /panorama/jobs {"sub_type":"policy_match","params":{"subject_id":"E0001"}}`：华芯生物 8 行（期望 5），rank1 变「网络与通信产业发展财政支持规划」35 分、理由 `["国家级普适","未过期"]` → DATA。
- 208 设计无资源：不请求，维持。
- 分类与派单见 handoff。验收单留 `ready`，第三轮待 `POL-L2-DS10-EXPECT-REFRESH-L01` 完成后跑。

## 2026-11-09 第三轮（期望刷新后复测，样本满足）

- 刷新单 `POL-L2-DS10-EXPECT-REFRESH-L01` 由本会话代跑（human:淮政玮「签收」指令 + self_claim 选项）：SENT 用例 207/209/210/212 期望按现行读面重冻结（波动语义锚定），208 维持。
- 复测断言 10/10 全过：207 total=85 且旧行 18323509 字段一致；209 广东 28.26 口径文案一致、31 省齐；210 三渠道 ≥2 且缺项演示 6 行原文一致；211 全字段逐字一致；212 8 行全 35 分、理由闭集、rank1 含「通知」。
- 样本满足。验收单 `ready`，常驻单不签 done；208 持续不请求。

设计无资源的行不请求。不派数据单，不派算法单，不打探测。

人说「按 LOOP 跑」之后，再按 §6.5 建常驻验收单 `POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP`。不把这张单签 `done`。
