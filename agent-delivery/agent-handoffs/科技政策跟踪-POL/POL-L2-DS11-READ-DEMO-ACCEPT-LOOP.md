# POL-L2-DS11-READ-DEMO-ACCEPT-LOOP · 演示样本验收 handoff

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-READ-合规演示用例.md`
- 系统：科技信息展示系统 · 政策分析评价 · 结果解读（223–226）
- 监管人：`human:淮政玮`（口令「按 LOOP 跑」，2026-11-08 会话）
- 执行：`agent:qa-agent`（本会话代跑，验收单留 `ready`）
- 令牌：本机 `%USERPROFILE%\.gkx\display-loop-token`，监管人当面提供，不进 git、不打印正文。请求头 `Authorization: Bearer` + `systemCode: display`。

## 运行 2026-11-08

- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-READ-合规演示用例.md`
- 库：只读对照未直连库，沿用 2026-11-04 QA 连库核实记录（`gkxlumenx_gapfill`，10.50.11.76:3306，账号 `gkxlumenx`）。不写口令。
- 样本满足：否
- 停止：继续（QUERY 缺口，挂在在办单 POL-L2-DS11-BE-L01）

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 223 热点问题分析看板 | GET evaluation/counts（无参数） | 200 | 31 省行：scopeCode/scopeName/shortboardCnt（"381"–"515" 正整数）+metricId，无机遇字段。未重放会改表的 focus jobs（遵守用例） | ✅ 通过 |
| 224 互动解读 + 225 多媒体 | GET evaluation/shells（无参数） | 200 | `records: []` 空列表。BUG-01：解读 4 条 + 多媒体 3 条应返回，库内有行（2026-11-04 已核实 7 行） | ❌ 不通过（BUG-01） |
| 226 智能摘要 | POST jobs `{"sub_type":"policy_text_parse"}` | 200 | 返回**新建分析任务载荷**（id=2198、taskId=POLICY-20261108-006、reused:false、resultAssetId=res-POLICY-20261108-006，01:27:39 跑完），1.9MB，正文无 `summary` 字段 | ❌ 不通过（行为缺口） |

探测即 counts 请求，HTTP 200。

### 副作用记录（诚实账）

226 用例口径是「只读取已有摘要，请求内不调用 parse.run」。按用例请求重放后，线上**新建了一个分析任务并执行**（`POLICY-20261108-006`，约 01:27:39–01:27:40，生成结果资产 `res-POLICY-20261108-006`）。本轮是按用例「填好的请求」原样重放，未额外签发、未人工补打；此行为本身正是缺口证据。`ads.policy_text_parse` 表行数是否变化未连库核对（本轮未连库）。

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `ads.policy_text_parse` shells/解读多媒体过滤（BUG-01） | QUERY | shells 空列表；旧列名拣不中，库内有行 | 解读 4 条 + 多媒体 3 条（标题+结论+建议） | 修 shells 列名映射（同 VIZ GAP-01 同根因） | POL-L2-DS11-BE-L01 |
| `jobs sub_type=policy_text_parse` 行为 | QUERY | 新建任务并执行（reused:false），返回任务载荷 | 只返回已有 `ads.policy_text_parse.summary`，跑前后行数不变，请求不调 parse.run | 改 jobs 的 text_parse 分支为纯读（该单 DoD 原文已有「226 只查 summary，请求不调 parse.run」） | POL-L2-DS11-BE-L01 |

去重：无未完成的同缺口修复单；`POL-L2-DS11-BE-L01` DoD 明确含 BUG-01 修复点与 226 只读口径，整单挂靠，不新建。

### 结论

可演行 3 组请求：223 通过、224/225 与 226 不通过（均 QUERY，挂 `POL-L2-DS11-BE-L01`）。样本未满足，验收单留 `ready`。下一轮待该单签收后重测 224/225/226。

## 运行 2026-11-08（第二轮 · 修复后复测）

- 修复单：`POL-L2-DS11-BE-L01`，commit `0a6b0d9`（SHELL_SQL 列名对齐真表 + 226 改 element 同步只读）已 push 并部署 dev。
- 样本满足：是

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 223 热点问题分析看板 | GET evaluation/counts（无参数） | 200 | 31 省行 shortboardCnt 正整数（首轮已过，本轮未回归） | ✅ 通过 |
| 224 互动解读 + 225 多媒体 | GET evaluation/shells（无参数） | 200 | 7 行（解读 4 + 多媒体 3），列 subjectName/conclusionText/suggestionText/title/captionText 与用例一致，2026-11-03 灌数批次 | ✅ 通过 |
| 226 智能摘要 | POST jobs `{"sub_type":"policy_text_parse"}` | 200 | 同步只读返回 `records`：含 policyId/title/summary/autoTags/structuredElements 的 ADS 摘要行（12MB，5.1s）。无任务创建，无 taskId，请求未触发 parse.run | ✅ 通过 |

### 副作用记录（诚实账）

226 本轮返回为纯读响应（无任务载荷）。响应体为 ADS 已有摘要行原样透出，未签发新任务、未改表。首轮误建的 `POLICY-20261108-006` 为历史残留任务，不影响本轮判定。

### 结论

READ 三组请求全部通过，样本满足。验收单转 `ready_to_sign`，监管人签收后 done。修复证据：commit `0a6b0d9`（lumen-svc-platform dev），CI 部署 dev rollout 后线上验证。
