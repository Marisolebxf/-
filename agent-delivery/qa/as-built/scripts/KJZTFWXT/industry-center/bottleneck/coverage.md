# 产业瓶颈堵点识别 脚本→用例 覆盖表（2026-10-14 BATCH32 回炉 · chain-bottleneck）

蓝本 = `qa/test-cases/KJZTFWXT/industry-center-产业链分析/BOTTLENECK-产业瓶颈堵点识别/FUNC-产业瓶颈堵点识别-用例.md` v2.0（00601~00625）。
env-gate = `fixtures/scout/env-gate.json`（overall=**partial**：g1/g2/g4 pass，g5 fail）。

| 统计 | 值 |
|------|-----|
| A 档金样 | 5（P0-01~P0-05），**零 allow_skip** |
| B 档（含 includes） | 25 |
| allow_skip | 10（P0-10 / P0-11 / P0-12 / P0-13 / P0-14 / P0-15 / P0-16 / P0-17 / P0-18 / P0-19）→ **10/25 = 40% >25%**（父波逐条补 GAP 暂超阈；结果态/清空控件通后应转实跑降占比） |
| 本轮未自动化 | 0（见下表；00625 已补 P0-19 划出） |

金样锁定（回炉后）：P0-01=00601 · P0-02=00603 · P0-03=00606 · P0-04=00609 · P0-05=00602  
（原用例册金样 00614 因无已完成任务降 B 档 skip，不进 A。）

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 档(A/B) | 页面区块/状态 | P | 可见动作 | skip ticket |
|---------|----------|---------|---------------|---|----------|-------------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00601 | A | 入口·路由与双 Tab | P0 | goto bottleneck | — |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00603 | A | 配置·三级默认 | P0 | 默认态核对 | — |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00606 | A | 配置·五维权重只读 | P0 | 5 spin=20 + disabled | — |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00609 | A | 异步·开始分析 | P0 | enabled + 显式触发；切对象不自动起 | — |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00602 | A | 配置·整体构成 | P0 | 三级/五维/版本/按钮 | — |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00604 | B | 配置·三级联动 | P0 | 切生物产业看联动 | — |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00605 | B | 配置·五维名称 | P0 | 读五维名 | — |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00607 | B | 配置·禁断链 | P0 | 配置区检索断链 | — |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00608 | B | 配置·版本四项 | P0 | 读只读版本 | — |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00610 | B | 过程·能力词 | P0 | 开始分析后读阶段文案 | ENV-CHAIN-BOTTLENECK-PROCESS-UI |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00614 | B | 结果·成因与建议 | P0 | 诊断记录→查看结果 | ENV-CHAIN-BOTTLENECK-NO-DONE-TASK |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00622 | B | 版本·任务快照绑定 | P0 | 开始分析后读绑定 | ENV-CHAIN-BOTTLENECK-PROCESS-UI |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00611 | B | 结果·顶栏与卡脖子 KPI | P0 | 诊断记录→查看结果 | ENV-CHAIN-BOTTLENECK-NO-RESULT（yaml ticket 已补；g5 未过不可去 skip） |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00612 | B | 结果·健康图谱与三档 | P0 | 诊断记录→查看结果 | ENV-CHAIN-BOTTLENECK-NO-RESULT（yaml ticket 已补；g5 未过不可去 skip） |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00613 | B | 结果·角标分层与详情分列 | P0 | 诊断记录→查看结果→点选节点 | ENV-CHAIN-BOTTLENECK-NO-RESULT |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00615 | B | 结果·健康度排序升降序 | P0 | 诊断记录→查看结果→升/降序切换 | ENV-CHAIN-BOTTLENECK-NO-RESULT |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00616 | B | 结果·图例两行与禁词禁并格 | P0 | 诊断记录→查看结果→浏览图例/检索禁词 | ENV-CHAIN-BOTTLENECK-NO-RESULT |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00621 | B | 备选·历史任务恢复复用 | P1 | 诊断记录→已完成行查看结果（恢复） | ENV-CHAIN-BOTTLENECK-NO-DONE-TASK |
| P0-19 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00625 | B | 异常·清空对象空态门禁 | P1 | 清空细分→空态保持+开始分析门禁 | ENV-CHAIN-BOTTLENECK-CLEAR-CTRL |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00617 | B | 备选·维度查看 | P1 | 点查看开/关 | — |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00618 | B | 备选·重置参数 | P1 | 脏配置→重置 | — |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00619 | B | 备选·双 Tab 草稿 | P1 | Tab 往返 | — |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00620 | B | 备选·诊断记录列表 | P1 | 切诊断记录 | — |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00623 | B | 备选·兄弟隔离 | P1 | 侧栏 cycle/key_link | — |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00624 | B | 备选·评审零泄漏 | P1 | 开/关内部评审 | — |

## 本轮未自动化（砍脚本，环境债 / 依赖成功结果）

| 用例编号 | 原因 | ticket / 引用 |
|----------|------|----------------|
| 用例编号 | 原因 | ticket / 引用 |
|----------|------|----------------|
| ~~00612 | 健康图谱三档，依赖成功结果 | ENV-CHAIN-BOTTLENECK-NO-DONE-TASK~~ → **已补脚本 P0-14**（B 档 skip，归 ENV-CHAIN-BOTTLENECK-NO-RESULT，与旧票同根） |
| ~~00613 | 角标分层点选，同上 | ENV-CHAIN-BOTTLENECK-NO-DONE-TASK~~ → **已补脚本 P0-15**（B 档 skip，归 ENV-CHAIN-BOTTLENECK-NO-RESULT；用例册旧回填 P0-14 已让位给 00612） |
| ~~00615 | 健康度排序控件，同上 | ENV-CHAIN-BOTTLENECK-NO-DONE-TASK~~ → **已补脚本 P0-16**（B 档 skip，归 ENV-CHAIN-BOTTLENECK-NO-RESULT；用例册旧回填 P0-15 已让位给 00613） |
| ~~00616 | 结果图例禁词，同上 | ENV-CHAIN-BOTTLENECK-NO-DONE-TASK~~ → **已补脚本 P0-17**（B 档 skip，归 ENV-CHAIN-BOTTLENECK-NO-RESULT；用例册旧回填 P0-16 已让位给 00615） |
| ~~00621 | 恢复历史成功任务，查看结果 disabled | ENV-CHAIN-BOTTLENECK-NO-DONE-TASK~~ → **已补脚本 P0-18**（B 档 skip，归 ENV-CHAIN-BOTTLENECK-NO-DONE-TASK；用例册旧回填 P1-05 已让位给 00623） |
| ~~00625 | 清空对象 clear 控件不稳定 | ENV-CHAIN-BOTTLENECK-CLEAR-CTRL~~ → **已补脚本 P0-19**（B 档 skip，归 ENV-CHAIN-BOTTLENECK-CLEAR-CTRL；用例册旧回填 P1-09；细分无 clear-btn，探针 probe-p019*.json） |

## env-gate 摘要

| 闸门 | 结果 | 说明 |
|------|------|------|
| g1 登录+深链 | pass | `/industry-center/diagnosis?workspace=bottleneck` |
| g2 合法组合开始分析 enabled | pass | 新一代信息技术 / INB1701 / 半导体；截图 `env-gate-config.png` |
| g4 生物黑名单 | pass | 仅联动探测，不点成功路径 |
| g5 已完成可查看结果 | **fail** | 4 条失败行，查看结果全部 disabled → `env-gate-records.png` |

## as_built 偏差（D1～D4）

1. **D1** 分析对象 aria-label：集群 / 产业 + `industry-catalog-select`。
2. **D1** 「注册项只读启用」为 aria-label；数据状态「可用」。
3. **D4** 开始分析后过程 UI 常未现身 → B skip `ENV-CHAIN-BOTTLENECK-PROCESS-UI`。
4. **D4** 诊断记录仅失败、「查看结果」disabled → 结果态不进金样；代表条 P0-11 skip `ENV-CHAIN-BOTTLENECK-NO-DONE-TASK`。
5. **D4** 生物产业黑名单（INPUT_OBJECT_INVALID 风险）。
6. **D1** 金样由用例册 00614 调整为 00602（配置构成），与 env-gate 对齐。
