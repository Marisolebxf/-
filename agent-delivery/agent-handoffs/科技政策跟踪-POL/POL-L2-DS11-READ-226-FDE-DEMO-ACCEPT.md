# POL-L2-DS11-READ-226-FDE-DEMO-ACCEPT · 演示样本验收 handoff

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-READ-合规演示用例.md`
- 系统：科技信息展示系统 · 政策分析评价 · 结果解读 · **226-FDE**（新 `POST .../intelligent-summary`）
- 监管人：`human:淮政玮`
- 执行：本会话代跑（FDE 波次 E）
- 令牌：本机 `%USERPROFILE%\.gkx\display-loop-token`，不进 git、不打印正文。请求头 `Authorization: Bearer` + `systemCode: display`。

## 运行 2026-11-14

- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-READ-合规演示用例.md`（226 行已改为 intelligent-summary）
- 库：本轮未连库（探测未过）
- 样本满足：否
- 停止：token 失效

### 探测

| 步骤 | 请求 | HTTP | 结果 |
|---|---|---|---|
| 探测 | `GET https://edu.itic-sci.com/tid/api/display/v1/policy/evaluation/counts` | **401** | 未经授权。按 §6.5.3 熔断 |

未进入 226 `POST .../intelligent-summary` 样本对照。未建 DATA/QUERY/ALGO 子任务。

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| display-loop-token | ENV | 探测 401 | 探测 200 后对照 226 | 人重新登录展示系统，覆盖本机 token 文件后再开一轮 | — |

### 结论

验收单 `POL-L2-DS11-READ-226-FDE-DEMO-ACCEPT` → `blocked`。通知 `human:淮政玮`：请换新 `%USERPROFILE%\.gkx\display-loop-token` 后说「继续 E」或「按 LOOP 跑」。

## 运行 2026-11-14（续 · token 换新后）

- 用例：同上（226 = `POST .../intelligent-summary`）
- 库：未直连 MySQL；`ads.policy_text_parse` 行数用只读 `POST jobs {"sub_type":"policy_text_parse"}` 的 `records` 条数对照（跑前/后均为 3，无 taskId）
- 样本满足：是
- 停止：通过
- 政策样例：`policyId=18354678`（来自 shells 多媒体挂接）

### 探测

| 步骤 | 请求 | HTTP | 结果 |
|---|---|---|---|
| 探测 | GET .../evaluation/counts | 200 | 31 行，shortboardCnt 正整数 |

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 223 | GET counts | 200 | 31 省行，shortboardCnt 正整数；未重放 focus jobs | ✅ |
| 224+225 | GET shells | 200 | 7 行（解读 subject×4 + 多媒体 title×3） | ✅ |
| 226 | POST intelligent-summary `policyId=18354678` force=false | 200 | 首响 cached=false，含 conclusion / policySummary / keyHighlights(5) / recommendations(4)；二次 force=false → cached=true、文案不变 | ✅ |
| 226 重算 | 同上 force=true | 200 | cached=false，文案长度更新（结论 58→65，摘要 140→169）；随后 force=false 命中新缓存 | ✅ |
| 226 副作用 | jobs policy_text_parse 条数 | 200 | 智能摘要 force 前后 recordsN=3=3；无 taskId（未触发 parse.run / 未建任务） | ✅ |

### 缺口

无。

### 结论

可演行全部对上。无 DATA/QUERY/ALGO 子任务。LOOP 计划状态行已回写。验收单经 `human:淮政玮` 签收为 **done**。
