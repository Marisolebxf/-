# POL-L2-DS12-EST-METRIC-SIGNOFF-ARCH · 政策效果推演 · 效果预估 · 指标分册架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-METRIC`（2026-11-05）
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-EST-ARCH`（2026-11-04 稿；2026-11-05 第 5.4、5.5 节已写成 `库.表`）。本页只核指标分册是否落在该架构内。不改分册，不改架构稿，不改任务状态
- 范围：SRS 序号 232–236 的指标挂接。只写本会签。强度 ponytail off

## 结论

同意会签

分册只认已有 `M_POLICY_SIMULATE`，只挂在 232、233、234。235、236 的 `metric_id` 留空。D4 保持 mock。不新注册指标。布局推荐键不进推演。五叶读表与架构稿相同。不调用 `polan.text.simulate.run`。未见 metric MCP、改读 `sdd/指标与501.md`，不构成不同意。

## 核对

| 项 | 分册 | 对架构判定 |
|---|---|---|
| 只认已有 `M_POLICY_SIMULATE`，且只挂 232–234 | 第 2 节挂接表只有这一条，类型 MODEL，挂在 232、233、234。三叶共用这一条，不另起三条推演指标 | 一致。与架构第 5.1–5.3 节、第 9 节「三种均用推演键」一致 |
| 235、236 留空 | 第 1、6 节：不新注册，不挂 `M_POLICY_SIMULATE`，不借用 `M_POLICY_DEEP_168_1`。多维评估行、参与意见行的 `metric_id` 留空 | 一致。与架构第 5.4、5.5 节「行上 `metric_id` 留空」一致 |
| D4 仍是 mock。不新建指标 | 第 4 节：D4 只转述 mock，不升 live。235、236 没有专属号，没有可改的 D4。第 6.2 节对已灌行的计数写明不是新指标。不改注册表 | 一致。与架构第 7、9 节「不新造 `metric_id`，不改 D4，D4 保持 mock」一致 |
| 布局推荐不挂进推演 | 第 1、7 节：`M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT` 不进入 232–236。不把推演页可接统计读面从 0 改掉 | 一致。与架构第 1.3、第 6 节「两键不合并、不进推演页任何区」一致 |
| 读表与架构稿一致 | 232–234 读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 的未出台仿真、新出台预测、区域空间行。235 读 `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。236 读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。无行则该区空。236 的请求不插入 | 一致。与架构第 2、5、9 节同一分组。分册用的是 2026-11-05 已改过的 `库.表` |
| 不调用 `simulate.run` | 第 3、5、8 节：不调用 `polan.text.simulate.run`，不读 `ads.policy_simulate`，不改 `simulate.py`，不改 `cfg_model_registry.yaml`。注册表把 `M_POLICY_DS_11_POLICY_EVAL_015` 与推演键并列表，不当成这三叶已经能由 `run()` 写出 | 一致。与架构第 1.4、第 6 节「展示不迁 `run()`、不读 `ads.policy_simulate`」一致 |
| 调用链与 501 | 五叶走已有 `POST /display/v1/policy/simulation/jobs`。链路是浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → 对应缺项表。不进异步，不加 `policy_simulate`。真推演种类仍是 501 空态。缺项读面不用 501 充当功能，也不把判定列改成可接统计 | 一致。与架构第 2 节并存口径一致 |
| 指标 MCP 回退 | 动态工具目录无 metric 命名空间。身份改读 `指标与501.md` §3 与说明书第 2 节。未填注册中文名、口径、公式、注册源表、源系统、更新频率、`version`、D1、D2、D3 | 不构成不同意。分册没有把未查到的字段写成已查到 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 232 | `POST /display/v1/policy/simulation/jobs` | `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 的未出台仿真行。`metric_id` 用已有 `M_POLICY_SIMULATE` | 无。不进 `PolicyAnalysisTypes`，不进 `JOB_SUB_TYPES`。请求种类：未出台仿真。同步读，不建任务 |
| 233 | 同上 | 同表的新出台预测行。`metric_id` 用已有 `M_POLICY_SIMULATE` | 无。请求种类：新出台预测。不调 `parse/jobs` |
| 234 | 同上 | 同表的区域空间行。`metric_id` 用已有 `M_POLICY_SIMULATE` | 无。请求种类：区域空间。服务端只回行 |
| 235 | 同上 | `gkxlumenx_gapfill.gapfill_policy_sim_result` 的多维评估行。`metric_id` 留空 | 无。请求种类：多维评估。同步读，不建任务 |
| 236 | 同上 | `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder` 的参与意见行。`metric_id` 留空 | 无。请求种类：利益攸关方。架构第 5.5 节「参与意见」指行内容，不另开种类。请求不插入 |

232–236 的结果跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` → `gkxlumenx_gapfill` 的对应 `gapfill_` 表。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`，不调用 `polan.text.simulate.run`。

`POL-L2-DS12-EST-GAPFILL-L01` 灌 232–234，行上 `metric_id` 用 `M_POLICY_SIMULATE`。`POL-L2-DS12-SIM-GAPFILL-L01` 灌 235、236，无号行的 `metric_id` 留空。分册不执行灌数。D4 保持 mock。

## 铁律

1. 算法只在 Python。本五叶没有新模型。不调用 `polan.text.simulate.run`。Java 不按弹性现算，不写 nGQL。
2. 调用链是浏览器 → `/display/v1/policy/simulation/jobs` → `gkxlumen-display` → `gkxlumen-element` 只读缺项表。展示不直连 Python，不直连库，不调用 `demo-*`。
3. 232–234 读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。235 读 `gkxlumenx_gapfill.gapfill_policy_sim_result`。236 读 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`。接口不直接返回写死的预测、得分或意见。
4. 五叶共用已有 `simulation/jobs`，一次一种类。不进 `PolicyAnalysisTypes`，不进异步管道。
5. `M_POLICY_SIMULATE` 只挂 232–234。235、236 留空。不新造 `metric_id`。D4 保持 mock。
6. `M_POLICY_DEEP_171_1`、`M_POLICY_LAYOUT_REC_COUNT` 不进 232–236。
7. 未见 metric MCP 时改读 `指标与501.md`。这不构成不同意。判定列仍是 501，分册不改那一列。

## 签收边界

本页不把任务标 done。签收仍由 human:淮政玮 做。同意会签不是签收。
