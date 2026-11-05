# POL-L2-DS12-EST-API-SIGNOFF-ARCH · 政策效果推演 · 效果预估 · 后台接口 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-API`（2026-11-05）
- 监管：`human:淮政玮`
- 强度：ponytail off
- 对照：`POL-L2-DS12-EST-ARCH`（2026-11-04 落盘。2026-11-05 只改第 5.4、5.5 节的库.表写法，读法未改）。`POL-L2-DS12-SIM-API` 只核种类是否撞车、是否另起第二套资源。本页不重新设计，不改接口分册，不改架构分册，不改 SIM 分册
- 范围：SRS 序号 232–236。推演整页仍只有一条 `POST /display/v1/policy/simulation/jobs`

## 结论

同意会签

232–234 同步读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`。235 同步读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_result` 的多维评估行。236 同步读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_stakeholder`：请求种类是利益攸关方，行内容是参与意见。五叶一次一种类，同步读不建任务。空态是空，HTTP 成功，不用 501 充当功能。与 237–242 共用这一条 `simulation/jobs`，不新建作业入口，不建第二个分发器。请求种类与 `POL-L2-DS12-SIM-API` 不撞车。

同意会签不是签收。

## 核对

| 项 | 接口稿 | 判定 |
|---|---|---|
| 232–236 都有落点。对外只有一条 `POST /display/v1/policy/simulation/jobs`。一次请求只带一种类 | 签收口径与第 1 节：五叶都是这一条。第 3–7 节各写另一次提交，233 不带未出台仿真和区域空间，235 不带未出台仿真和利益攸关方。偏离第 3 条与第 2 节写明不能把整条 `jobs` 改成只读预估表，也不为 232–236 再开第二条 dispatcher。控制器若尚未存在，只补契约里已有的这一条，补上后仍按种类分发 | 一致。对齐架构第 2 节：推演页一条资源，一次只带一种类 |
| 五叶同步读，不建任务 | 第 1 节五行都写「同步」「不建任务」。第 2 节：display 不建任务，不转发 `gkxlumen-topic-async-service`，不调 Python，不占并发锁，不发 SSE。切条件、切参数不自动起任务。五叶不进 `POST /internal/policy/jobs/execute`，不加 `policy_simulate`，不写入 `PolicyAnalysisTypes` 或 `JOB_SUB_TYPES` | 一致。对齐架构第 2 节失败语义：POST 不创建持久任务记录，不进异步服务 |
| 232–234 读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`。库名与表名分开写 | 第 1、3–5 节写法是 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`，按未出台仿真、新出台预测、区域空间拣行。第 2 节另写「库只允许 `gkxlumenx_gapfill`」。不进 ODS、DWD、ADS，不写供应方库。没有把库名和表名粘成一个标识 | 一致。对齐架构第 5.1–5.3 节与第 9 节：库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_forecast`，三种类，不拆成三张 |
| 235 读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_result` 的多维评估行 | 第 1、2、6 节：种类为多维评估。element 只拣多维评估行。同表上的重点、影响范围、路径环节、解读段落这次不返回。字段名归 `POL-L2-DS12-SIM-DATA`。本分册不写 DDL，不改行内容 | 一致。对齐架构第 5.4 节：表 `gkxlumenx_gapfill.gapfill_policy_sim_result`，种类为多维评估 |
| 236 读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_stakeholder`。请求种类是利益攸关方，行内容是参与意见 | 第 1、7 节：公开种类为利益攸关方。element 只读参与意见行。第 1 节写明「参与意见」是行内容，不是第二种请求种类。架构第 5.5 节写「种类为参与意见」，与第 2、3、4 节的请求种类「利益攸关方」并存；公开 kind 取后者。请求不插入、不更新、不删除 | 一致。架构稿就是这样分开的：请求走利益攸关方，行是参与意见 |
| 空态是空，不是 501 | 第 1、3–8 节：五叶无行则该区空，HTTP 成功，不返回 501。接口函数不返回写死的预测、得分、曲线或意见。架构第 2 节「真推演」未注册时的 501 不挂这五叶。清单、`指标与501.md`、说明书里仍写的 501 不覆盖本分册，本分册不改那些文件 | 一致。对齐架构第 2、8 节：无行则该区空；「未注册则 501」只约束真模型调用 |
| 禁止 `/topic/v1/policy`、第二个 dispatcher、`demo-*`、Java NLP、nGQL | 第 2、9 节：浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`、`/policy/topic/v1/policy`、`/topicAsync/**`、`/v1/policy/**`、`/v1/policy/simulate`。不把 `E-E7-POLICY-M1-L06` 写成展示路径。不设第二个 dispatcher。不调用 `demo-*`。display 不做 NLP，不写 nGQL，不直连库，不直连 Python。234 不把第 7 项读图写成空间模拟 | 一致。对齐架构第 1.4、第 2、第 7 节 |
| 与 `POL-L2-DS12-SIM-API` 种类不撞车，不另起第二套资源 | 本分册请求种类只有：未出台仿真、新出台预测、区域空间、多维评估、利益攸关方。SIM 分册请求种类只有：文本解析、重点可视化、影响范围、路径预测、解读报告。240 两边都不占种类、都不走 `simulation/jobs`。两组中文名不相交。235 与 SIM 的重点、影响范围、路径环节、解读段落同表不同种类。236 的请求种类是利益攸关方，SIM 分册不定义这个请求，不读 `gapfill_policy_sim_stakeholder`。两边都写明共用已有这一条 `jobs`，不新建作业入口，不建第二个分发器 | 一致。没有撞车，没有第二套资源 |
| 233 的候选列表不另开本叶资源 | 第 4 节：候选政策列表复用已有全景检索。那次检索不代替这次 `jobs`。本分册不新定义检索资源，不改它的委托 | 一致。对齐架构第 5.2 节。五叶的公开资源仍只有 `simulation/jobs` |
| 灌数归属与可实现 | 232–234 的字段与灌数归 `POL-L2-DS12-EST-DATA`、`POL-L2-DS12-EST-GAPFILL-L01`。235、236 的字段与灌数归 `POL-L2-DS12-SIM-DATA`、`POL-L2-DS12-SIM-GAPFILL-L01`。查询不灌数。mock 先落表，再被查询读出。不调用 `polan.text.simulate`，不读 `ads.policy_simulate` | 一致。对齐架构第 0、8、9 节与 D18：接口读表，不直接返回写死的 mock |
| 不新造 `metric_id`，不改 D4，不进异步白名单 | 232–234 行上用已有 `M_POLICY_SIMULATE`。235、236 行上 `metric_id` 留空，不借用 `M_POLICY_SIMULATE`，不借用 `M_POLICY_DEEP_168_1`。布局推荐键不进这五叶。D4 保持 mock。不加 `policy_simulate` | 一致。对齐架构第 5、6、9 节 |

## 路径、表、sub_type

| 序号 | 公开路径 | 表 | sub_type |
|---|---|---|---|
| 232 | `POST /display/v1/policy/simulation/jobs` | 库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_forecast` 的未出台仿真行 | 无。请求种类：未出台仿真。同步读，不建任务 |
| 233 | 同上 | 同库同表的新出台预测行 | 无。请求种类：新出台预测。同步读，不建任务 |
| 234 | 同上 | 同库同表的区域空间行 | 无。请求种类：区域空间。同步读，不建任务 |
| 235 | 同上 | 库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_result` 的多维评估行 | 无。请求种类：多维评估。同步读，不建任务 |
| 236 | 同上 | 库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_stakeholder` 的参与意见行 | 无。请求种类：利益攸关方。行内容：参与意见。不另开 kind。同步读，不建任务 |

232–236 的内部跳是：浏览器 → 网关 → `gkxlumen-display` → `gkxlumen-element` 只读。不进入 `gkxlumen-topic-async-service`，不进入 Python `/internal/*`。

`POL-L2-DS12-SIM-API` 在同一条 `simulation/jobs` 上的请求种类仍是文本解析、重点可视化、影响范围、路径预测、解读报告。240 不占种类。本页不改那六叶。

## 铁律

1. 算法只在 Python。本五叶的请求不生成预测，不按弹性现算，不拼空间分布，不插入意见。Java 不做 NLP，不写 nGQL。`gkxlumen-display` 不直连库，不直连 Python。
2. 调用链是浏览器 → `POST /display/v1/policy/simulation/jobs` → Java → `gkxlumen-element` 只读。不新建作业入口。不建第二个分发器。不改打 `/topic/v1/policy`。不调用 `demo-*`。
3. 232–234 只读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_forecast`，按种类分开。库名与表名分开写。
4. 235 只读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_result` 的多维评估行。236 只读库 `gkxlumenx_gapfill`、表 `gapfill_policy_sim_stakeholder` 的参与意见行。请求种类是利益攸关方。
5. 五叶同步读，不建任务。不加 `policy_simulate`。
6. 空态是空。232–236 不用 501 充当功能。真推演未注册种类的 501 不挂到这五叶。
7. 请求种类与 `POL-L2-DS12-SIM-API` 的文本解析、重点可视化、影响范围、路径预测、解读报告不相交。两边共用这一条 `simulation/jobs`，没有第二套资源。

## 签收边界

本页不把任务标 done，不改任务状态。签收仍由 human:淮政玮 做。同意会签不是签收。
