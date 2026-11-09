# 政策舆情评估 · LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-SENT-合规演示用例.md`
- 系统：科技信息展示系统。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

- 状态：用例覆盖表已齐。207、209–212 可演。208 设计无资源。本计划不建单、不探测。等人说「按 LOOP 跑」。

## 2026-11-09 第二轮（样本不满足，继续；第一轮令牌失效记录见 TREND 计划）

- 换新令牌（cbac64ed…，登录主体 userId=3101）后全量重测。
- 211 `GET /panorama/assessment-report`：id 2 五段正文与 generated_at 逐字一致 ✅（camelCase 键：scopeText/achievementText/socialImpact/problemText/suggestionText/reportBody）。
- 210 `GET /panorama/feedback`：旧 6 行仍在（含 GF-POL-SENT-210-01 评分 4.50）✅，但总量 6→406（问卷 134/在线评价 147/意见征集 125，并行灌数新增）→ 排序断言失效，归 DATA。
- 207 `GET /panorama/search?keyword=人工智能`：旧行 18323509/18363833 仍在且字段一致 ✅，但 total 73→129（SYN 合成行混排且按 publish_date 抢首条）→ DATA。
- 209 `POST /panorama/jobs {"sub_type":"policy_effect"}`：region_effect 31 行结构在，广东 440000 评分 15.0→28.26（口径说明文案同步刷新为「广东省效果评分28.26（v2 确定性口径…）」）→ DATA（ADS 被并行重算）。
- 212 `POST /panorama/jobs {"sub_type":"policy_match","params":{"subject_id":"E0001"}}`：华芯生物 8 行（期望 5），rank1 变「网络与通信产业发展财政支持规划」35 分、理由 `["国家级普适","未过期"]` → DATA。
- 208 设计无资源：不请求，维持。
- 分类与派单见 handoff。验收单留 `ready`，第三轮待 `POL-L2-DS10-EXPECT-REFRESH-L01` 完成后跑。

设计无资源的行不请求。不派数据单，不派算法单，不打探测。

人说「按 LOOP 跑」之后，再按 §6.5 建常驻验收单 `POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP`。不把这张单签 `done`。
