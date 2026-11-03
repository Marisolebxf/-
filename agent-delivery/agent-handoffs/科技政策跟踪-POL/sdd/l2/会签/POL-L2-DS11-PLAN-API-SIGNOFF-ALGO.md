# POL-L2-DS11-PLAN-API-SIGNOFF-ALGO · 政策分析评价 · 推荐方案报告交互展示 · 后台接口设计算法会签

- 角色：agent:algorithm-agent（监管 human:淮政玮）
- 日期：2026-11-03
- 对象：`sdd/l2/POL-L2-DS11-PLAN-API.md`（只读会签，不改分册）
- 监管：human:淮政玮
- 对照：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`（已签收架构，2026-11-03 四角色同意）；代码实读 `repos/lumen-algo-py/vendor/entan-py/polan/text/simulate.py`、`repos/lumen-algo-py/vendor/entan-py/conf/cfg_model_registry.yaml`（均只读）
- 范围：SRS 227–231 五叶的算法口径核对。格式沿同目录 VIZ 侧算法会签；会签环境未见 metric-registry MCP，本文不做指标注册查询，指标身份以分册对 `指标与501.md` 与架构稿的转述及代码实读为准

## 结论

同意会签

## 核对

| 项 | 分册写法 | 对算法判定 |
|---|---|---|
| 229 行上 metric_id 用已有 `M_POLICY_DS_11_POLICY_EVAL_015` | 第 2 节末段、第 5 节：路径与风险行用这个已有号，「现有函数不产出这条指标」，不新注册，不改 D4 | ✅ 属实。`simulate.py` 全文无 015，行上 `metric_id` 固定字面量 `M_POLICY_SIMULATE`；注册表里 015 仅是 `POLICY_SIMULATE` 项 `metric_ids` 的并列表，无 handler 产出。分册未虚构产出方，015 只能经灌数行落表，与代码事实相容 |
| 227/228/230 行上留空、231 不占种类 | 第 2 节末段「其余三种没有已挂指标，`metric_id` 留空，不新注册」；第 7 节 231 不单独占行种类，导出从当次读到的行生成 | ✅ 成立，与 METRIC/DATA 两册一致（DATA 定为写 NULL） |
| 228 与推演键切割 | 第 4 节：不调用 `polan.text.simulate.run`、不读 `ads.policy_simulate`、不在 Java 或 Python 里按弹性公式现算、请求内不重算；第 9 节明确不做同款 | ✅ 口径闭合。`run()` 写的是省级力度情景（前 12 省 × 3 情景弹性，产 baseline/simulated/delta/曲线），无方案、参数档语义，本就不能服务 228；分册把读表与现算两条路同时封死 |
| 五叶不进异步、不调 Python、不加 `policy_scheme`、不进 `POST /internal/policy/jobs/execute` | 第 1 节末段、第 2 节委托表、第 9 节：`PolicyAnalysisTypes` 现六键白名单不加 `policy_scheme`，不建任务、不转发 `gkxlumen-topic-async-service`、不调 Python、不占并发锁、不发 SSE | ✅ 显式且完整。display → element 只读缺项表，链路无 Python 参与点 |
| D18：接口不直接返回 mock、无行则空不 501 | 签收口径段与第 8 节空态对照表：五行全部「HTTP 成功、不返回 501」；「mock 若存在，只能先由灌数单落入表，再被查询读出。查询不灌数」 | ✅ D18 口径闭合，mock 唯一入口是 `POL-L2-DS11-PLAN-GAPFILL-L01` |
| 229 不读图、不被推演曲线或序号 241 顶替 | 第 5 节：不写 nGQL、不读政策子图、不进第 7 项读图、不返回 `polan.text.simulate` 曲线顶替；241 在推演页不顶替本叶 | ✅ GRAPH 只作纸面身份，读面不触发任何图查询 |
| 与已签收架构一致 | 五叶资源、按种类分发、只读 `gkxlumenx_gapfill.gapfill_policy_eval_scheme`、偏离三处只声明不回改 | ✅ 与 ARCH 第 2、8、9 节逐条对齐 |

### 算法侧补充

- 分册对 228 的处理与代码事实自洽：`ads.policy_simulate` 的行结构（`scenario_id`/`scope_code`/`curve` 等）与「方案 + 参数档 + 评估结果」粒度对不上，禁止复制是唯一正确解。
- 229 挂 015 但明写「现有函数不产出」，没有把注册表的 `POLICY_SIMULATE.metric_ids` 并列表当成 015 已有产出方，判定准确。

## 签收边界

- 本页只做算法角色会签。未改分册、未改代码、未碰 task-registry MCP、未 commit/push。
- 不把 `POL-L2-DS11-PLAN-API` 标 done 或 ready_to_sign；签收由 human:淮政玮 做。
