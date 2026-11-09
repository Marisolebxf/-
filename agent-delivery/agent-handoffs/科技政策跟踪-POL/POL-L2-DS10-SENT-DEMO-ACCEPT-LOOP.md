# POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP · 演示样本验收 handoff

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成\05-展示系统集成/合规演示用例/POL-L2-DS10-SENT-合规演示用例.md`
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景 · 政策舆情评估（207–212）
- 监管人：`human:淮政玮`（口令「按 LOOP 跑」，2026-11-09 会话）
- 执行：`agent:qa-agent`（本会话代跑）
- 令牌：本机 `%USERPROFILE%\.gkx\display-loop-token`，不进 git、不打印。请求头 `Authorization: Bearer` + `systemCode: display`。

## 运行 2026-11-09（首轮）

- 样本满足：否
- 停止：令牌失效（按 §6.5 探测 401/令牌失效文案 → 验收单 `blocked`，不建子任务，不再开一轮）

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 207 | GET `/display/v1/policy/panorama/search?keyword=人工智能&q=人工智能` | 未发 | 探测 401，按规程停止 | ⛔ 未执行 |
| 208 | 设计无资源 | — | 不请求 | 不判 |
| 209 | POST `/display/v1/policy/panorama/jobs` `{"sub_type":"policy_effect"}` | 未发 | 同上 | ⛔ 未执行 |
| 210 | GET `/display/v1/policy/panorama/feedback` | 未发 | 同上 | ⛔ 未执行 |
| 211 | GET `/display/v1/policy/panorama/assessment-report` | 未发 | 同上 | ⛔ 未执行 |
| 212 | POST `/display/v1/policy/panorama/jobs` `{"sub_type":"policy_match","params":{"subject_id":"E0001"}}` | 未发 | 同上 | ⛔ 未执行 |

- 探测（`GET /ingest` 与 `GET /stats?kind=all`）返回 HTTP 401 `{"code":401,"msg":"访问令牌不存在","data":"sso check-token failed"}`；网关本体可达，排除 ENV。
- 令牌核对：本机文件当前值（5af83d33…）与会话旧令牌（1cce4c0b…）分别实测，均返回同一 401 文案，SSO 侧已判失效。

### 缺口

无 DATA/QUERY/ALGO 缺口。本轮属 §6.5「令牌失效」停止分支：通知 `human:淮政玮` 重新登录展示系统，覆盖 `%USERPROFILE%\.gkx\display-loop-token`，再说一次「按 LOOP 跑」后开第二轮。207、209–212 期望值已在断言脚本 `run_ds10_loop_tests.py`（本机 %TEMP%\gkx_loop\，不进 git）备好，换 token 后直接重跑。208 设计无资源，持续不请求。

### 结论

验收单 `POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP` = `blocked`（阻塞原因已登记 registry）。样本未满足。不签 done。

## 运行 2026-11-09 第二轮（令牌已换新）

- 令牌：`human:淮政玮` 09:17 换发（cbac64ed…），登录主体 userId=3101。探测 HTTP 200。
- 样本满足：否
- 停止：继续（FAIL 全归 DATA，根因同 TREND：用例期望冻结快照过期，挂 `POL-L2-DS10-EXPECT-REFRESH-L01`）

### 逐行结果（第二轮）

| 需规 | 请求 | HTTP | 实测 | 判定 |
|---|---|---|---|---|
| 207 | GET `/panorama/search?keyword=人工智能&q=人工智能` | 200 | 旧行 18323509/18363833 仍在且字段一致；但 total 73→129（SYN 合成行混排并按 publish_date 抢首条，首条已变） | ❌ DATA |
| 208 | 设计无资源 | — | 不请求 | 不判 |
| 209 | POST `/panorama/jobs` `{"sub_type":"policy_effect"}` | 200 | region_effect 31 行结构在；广东 440000 评分 15.0→28.26（口径说明文案同步刷新为「广东省效果评分28.26（v2 确定性口径…）」）→ ADS 被并行重算 | ❌ DATA |
| 210 | GET `/panorama/feedback` | 200 | 旧 6 行仍在（含 GF-POL-SENT-210-01 评分 4.50 原文一致）；但总量 6→406（问卷134/在线评价147/意见征集125）排序断言失效 | ❌ DATA |
| 211 | GET `/panorama/assessment-report` | 200 | id 2 五段正文与 generated_at（2026-11-03 14:30:00）逐字一致（camelCase 键：scopeText/achievementText/socialImpact/problemText/suggestionText/reportBody） | ✅ 通过 |
| 212 | POST `/panorama/jobs` `{"sub_type":"policy_match","params":{"subject_id":"E0001"}}` | 200 | 华芯生物 8 行（期望 5）；rank1 变「网络与通信产业发展财政支持规划（2026—2030）」35 分、理由 ["国家级普适","未过期"]、metric_id=M_POLICY_MATCH 在 | ❌ DATA |

### 缺口（第二轮）

无新增缺口键。七项 FAIL 与 TREND 同根因（期望冻结快照过期，并行灌数合法新增/重算，旧行未丢），整并挂刷新单 `POL-L2-DS10-EXPECT-REFRESH-L01`，不重复派单。

### 结论（第二轮）

样本未满足，验收单 `POL-L2-DS10-SENT-DEMO-ACCEPT-LOOP` = `ready`。第三轮待刷新单完成后重测；208 持续不请求。不签 done。

## 运行 2026-11-09 第三轮（期望刷新后复测，样本满足）

- 前置：同 TREND（EXPECT-REFRESH-L01 已签收，SENT 用例 207/209/210/212 期望重冻结，208 维持设计无资源）。
- 样本满足：是（停止：完成）

### 逐行结果（第三轮，断言 10/10）

| 需规 | 请求 | HTTP | 实测 | 判定 |
|---|---|---|---|---|
| 207 | GET `/panorama/search?keyword=人工智能&q=人工智能` | 200 | total=85（≥1）；旧行 18323509 在结果集且字段与 2026-11-07 记录一致（苏州市工业和信息化局，2021-11-24） | ✅ 通过 |
| 208 | 设计无资源 | — | 不请求 | 不判 |
| 209 | POST `/panorama/jobs` policy_effect | 200 | region_effect 31 省齐；广东 28.26，口径说明「广东省效果评分28.26（v2 确定性口径…）」格式一致；时序 metric_id=M_POLICY_IMPLEMENTATION_EFFECT 在 | ✅ 通过 |
| 210 | GET `/panorama/feedback` | 200 | 三渠道各 ≥2（总 448）；缺项演示 6 行仍在：广州原文一致（评分空）、深圳原文一致评分 4.50、policy_id=GF-POL-SENT-210-01 | ✅ 通过 |
| 211 | GET `/panorama/assessment-report` | 200 | id 2 六字段（scopeText/achievementText/socialImpact/problemText/suggestionText/reportBody）逐字一致，generatedAt=2026-11-03 14:30:00 | ✅ 通过 |
| 212 | POST `/panorama/jobs` policy_match E0001 | 200 | 华芯生物 8 行（≥5）全 35 分；理由闭集 ["国家级普适","未过期"]/["地区适用","未过期"]；rank1 含「通知」；metric_id=M_POLICY_MATCH | ✅ 通过 |

### 结论（第三轮）

样本满足，本轮无子任务（刷新单已签收）。验收单 `ready`（常驻单不签 done）；208 持续不请求。
