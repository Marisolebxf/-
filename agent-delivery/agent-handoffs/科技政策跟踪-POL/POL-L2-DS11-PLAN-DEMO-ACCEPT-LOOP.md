# POL-L2-DS11-PLAN-DEMO-ACCEPT-LOOP · 演示样本验收 handoff

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-PLAN-合规演示用例.md`
- 系统：科技信息展示系统 · 政策分析评价 · 推荐方案（227–231）
- 监管人：`human:淮政玮`（口令「按 LOOP 跑」，2026-11-08 会话）
- 执行：`agent:qa-agent`（本会话代跑，验收单留 `ready`）
- 令牌：本机 `%USERPROFILE%\.gkx\display-loop-token`，不进 git、不打印。请求头 `Authorization: Bearer` + `systemCode: display`。

## 运行 2026-11-08

- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-PLAN-合规演示用例.md`
- 库：只读对照未直连库，沿用 2026-11-04 QA 连库核实记录（`gkxlumenx_gapfill.gapfill_policy_eval_scheme` 19 行：方案对照 2、参数模拟 5、路径与风险 6、互动意见 6；10.50.11.76:3306，账号 `gkxlumenx`）。不写口令。
- 样本满足：否
- 停止：继续（QUERY 缺口，挂在在办单 POL-L2-DS11-BE-L01）

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 227 方案对照 | POST jobs `{"kind":"方案对照"}` | 200 | 2 行：研发投入加力方案、人才引育优先方案，brief/dims/prosCons/suggestion 齐备，isMock=1 | ✅ 通过 |
| 228 参数模拟 | POST jobs `{"kind":"参数模拟","scheme_name":"研发投入加力方案","param_band":"资金规模基准档"}` | 200 | 唯一行，evalResult/trendText/archiveNote 三字段齐全且与表内原文一致 | ✅ 通过 |
| 229 路径与风险 | POST jobs `{"kind":"路径与风险","scheme_name":"研发投入加力方案"}` | 200 | 3 节点按 id 27/28/29 升序，metricId 全部 `M_POLICY_DS_11_POLICY_EVAL_015` | ✅ 通过 |
| 230 互动意见 | GET shells?kind=互动意见&scheme_name=研发投入加力方案 | 200 | `records: []` 空列表。库内该方案 3 条意见、共 6 行（QA 已核实） | ❌ 不通过 |
| 231 方案报告 | GET shells?kind=方案报告&scheme_name=研发投入加力方案 | 200 | `records: []` 空列表 | ❌ 不通过 |

探测即 227 请求（计划第 3 节），HTTP 200。230/231 重放为纯 GET 只读，库内互动意见保持 6 行（未插入）。

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `gapfill_policy_eval_scheme` 互动意见 shells 过滤 | QUERY | 空列表；库内 6 行（每方案 3 条，分类 评价/评论/建议 各 2） | 该方案 3 条（主体/分类/正文/时间齐备），请求不插入 | 修 shells 端点对 `gapfill_policy_eval_scheme` 的 kind 分支（旧列名/缺分支拣不中） | POL-L2-DS11-BE-L01（DoD 已含 230/231） |
| `gapfill_policy_eval_scheme` 方案报告 shells 过滤 | QUERY | 空列表 | 正文由当次读到的方案对照行+互动意见行拼出；无文件字节、不写对象存储 | 同上，shells 分支补齐后 231 由行拼装 | POL-L2-DS11-BE-L01 |

去重：无未完成的同缺口修复单；`POL-L2-DS11-BE-L01` DoD 明确含「方案五叶只读 gapfill_policy_eval_scheme、230/231」，整单挂靠，不新建。

### 结论

可演行 5 笔请求：3 笔通过、2 笔不通过（QUERY，同 shells 根因，挂 `POL-L2-DS11-BE-L01`）。样本未满足，验收单留 `ready`。下一轮待该单签收后重测 230/231。

## 运行 2026-11-08（第二轮 · 修复后复测）

- 修复单：`POL-L2-DS11-BE-L01`，commit `0a6b0d9` 已 push 并部署 dev（互动意见/方案报告分支随部署生效）。
- 样本满足：是

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 227 方案对比 | GET evaluation/shells `kind=方案对照` | 200 | 首轮已过（2 方案行），本轮未回归 | ✅ 通过 |
| 228 参数模拟 | POST jobs `kind=参数模拟` | 200 | 首轮已过，本轮未回归 | ✅ 通过 |
| 229 路径与风险 | POST jobs `kind=路径与风险` | 200 | 首轮已过，本轮未回归 | ✅ 通过 |
| 230 互动意见 | GET evaluation/shells `kind=互动意见&scheme_name=研发投入加力方案` | 200 | 3 条意见行：opinionSubject（王建国/李文韬/陈晓峰）、opinionClass（评价/建议/评论）、opinionText、opinionAt 齐备 | ✅ 通过 |
| 231 方案报告 | GET evaluation/shells `kind=方案报告&scheme_name=研发投入加力方案` | 200 | records 1 行（方案对照正文拼装）+ opinions 3 行，无文件字节、无对象存储写入 | ✅ 通过 |

### 结论

PLAN 五笔全部通过，样本满足。验收单转 `ready_to_sign`，监管人签收后 done。修复证据：commit `0a6b0d9`（lumen-svc-platform dev）。
