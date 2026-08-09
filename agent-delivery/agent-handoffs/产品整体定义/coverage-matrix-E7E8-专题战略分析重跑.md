# 覆盖矩阵 — E7 产业服务链分析 + E8 综合智能分析（重跑收口版）

> 产出批次：TOPIC-STRAT-R4（2026-08-06）。真源：招标《科技信息展示系统和科技专题服务系统》§1.1.1.2.4.2.7（产业服务链分析，16 个三级项）、§1.1.1.2.4.2.8（综合智能分析，9 个三级项）、展示系统 §1.1.1.1.1.1.1.33（门户专题服务，含序号 97-104）。
> 与六份 TRACE 反向核对一致：TRACE-SVCCHAIN-ORG-ANALYSIS / -ECOSYSTEM / -RECOMMEND / -PORTAL、TRACE-SYNTH-REGION（R2B 修订随 ORG-ANALYSIS）。
> 状态口径：**closed** = 交互闭环落地且无未决业务/算法口径（mock 数据本身不降级）；**演示态 🧪** = 功能闭环但算法/判读口径挂 Q-*，UI 有诚实性标注；**口径待定 ❓** = 业务定义/数据源本身待甲方拍板（Q-* 高优）。
> 实现仓：`demo-ui-topic @ origin/dev`（R1 `9825411` / R2+R2B `284b681` / R2C `7b1a9bf`+`4c9d932` / R3 `905da04`）。

## 一、专题服务系统 §2.4.2.7 产业服务链分析（16 项）

| 招标项 | 内容 | 归属叶子 | TRACE | 实现路由 | 状态 | 关联 Q |
|---|---|---|---|---|---|---|
| 7.1.1 | 服务机构产业领域覆盖分析 | ORG-ANALYSIS | TRACE-SVCCHAIN-ORG-ANALYSIS | `/service/institution-judgment`（覆盖视图） | closed | — |
| 7.1.2 | 领域分析结果呈现（热力/矩阵） | ORG-ANALYSIS | 同上 | 同上（双图型切换） | 演示态 🧪 | Q-SVCCHAIN-02（深度得分 draft） |
| 7.2.1 | 新增趋势可视化呈现 | ORG-ANALYSIS | 同上 | `/service/institution-judgment?tab=trend` | closed | — |
| 7.2.2 | 市场热度判断 | ORG-ANALYSIS | 同上 | 同上（星级+依据行） | 演示态 🧪 | Q-SVCCHAIN-02（热度 D1 missing） |
| 7.3.1 | 技术力多维度评价模型 | ORG-ANALYSIS | 同上 | `/service/institution-judgment?tab=capability` | 演示态 🧪 | Q-SVCCHAIN-01 |
| 7.3.2 | 自定义对比分析（2~5 家） | ORG-ANALYSIS | 同上 | 同上（含对比篮分发承接） | closed | — |
| 7.4.1 | 服务链全链路可视化 | ECOSYSTEM | TRACE-SVCCHAIN-ECOSYSTEM | `/service/chain-analysis` | closed | — |
| 7.4.2 | 瓶颈堵点智能识别 | ECOSYSTEM | 同上 | 同上（短板高亮） | 演示态 🧪 | Q-SVCCHAIN-03 |
| 7.5.1 | 关系网络构建 | ECOSYSTEM | 同上 | 同上（图谱 Tab） | closed | — |
| 7.5.2 | 图谱探索与统计 | ECOSYSTEM | 同上 | 同上（过滤持久化+统计侧栏） | 演示态 🧪 | Q-SVCCHAIN-03（影响力评分） |
| 7.6.1 | 招引模型与指标 | RECOMMEND | TRACE-SVCCHAIN-RECOMMEND | `/service/institution-decision`（招引 Tab） | 演示态 🧪 | Q-SVCCHAIN-05 |
| 7.6.2 | 推荐名单生成 | RECOMMEND | 同上 | 同上（名单→导出） | 演示态 🧪 | Q-SVCCHAIN-05 |
| 7.7.1 | 培育模型与筛选 | RECOMMEND | 同上 | 同上（培育 Tab） | 演示态 🧪 | Q-SVCCHAIN-05 |
| 7.7.2 | 培育名单与建议 | RECOMMEND | 同上 | 同上（名单+建议标签+入篮） | 演示态 🧪 | Q-SVCCHAIN-05 |
| 7.8.1 | 深圳服务链统一评价框架 | ECOSYSTEM | TRACE-SVCCHAIN-ECOSYSTEM | `/service/chain-analysis`（深圳现状 Tab） | 口径待定 ❓ | Q-SVCCHAIN-04（框架/基准数据源） |
| 7.8.2 | 横向对比分析（柱状/仪表盘） | ECOSYSTEM | 同上 | 同上（对比指标选择持久化） | 演示态 🧪 | Q-SVCCHAIN-04 |

## 二、专题服务系统 §2.4.2.8 综合智能分析（9 项）

| 招标项 | 内容 | 归属叶子 | TRACE | 实现路由 | 状态 | 关联 Q |
|---|---|---|---|---|---|---|
| 8.1.1 | 活力指标体系构建 | SYNTH-REGION | TRACE-SYNTH-REGION | `/intelligence/vitality`（4 维×12 指标分层展开） | closed | — |
| 8.1.2 | 综合评价模型 | SYNTH-REGION | 同上 | 同上 | 演示态 🧪 | Q-SYNTH-01（指数 D1 missing） |
| 8.1.3 | 区域指数计算与可视化 | SYNTH-REGION | 同上 | 同上（指数卡/排名榜/趋势） | 演示态 🧪 | Q-SYNTH-01 |
| 8.2.1 | 创新要素数据汇聚 | SYNTH-REGION | 同上 | `/intelligence/elements`（四类要素+构成抽屉） | closed | — |
| 8.2.2 | 要素评价模型构建 | SYNTH-REGION | 同上 | 同上（四维雷达） | 演示态 🧪 | Q-SYNTH-02 |
| 8.2.3 | 要素影响关联分析 | SYNTH-REGION | 同上 | 同上（贡献度+影响路径联动） | 演示态 🧪 | Q-SYNTH-02 |
| 8.3.1 | 创新主体关系图谱 | SYNTH-REGION | 同上 | `/intelligence/collaboration`（ForceGraph 四类主体） | closed | — |
| 8.3.2 | 协同度计算模型 | SYNTH-REGION | 同上 | 同上（协同指数+三分项） | 演示态 🧪 | Q-SYNTH-03 |
| 8.3.3 | 协同效果评估 | SYNTH-REGION | 同上 | 同上（集群/孤立主体/产出相关性+报告） | 演示态 🧪 | Q-SYNTH-03 |

## 三、展示系统 §33 门户专题服务（33.1-33.5，含序号 97-104）

| 招标项 | 内容 | 归属叶子 | TRACE | 实现路由 | 状态 | 关联 Q |
|---|---|---|---|---|---|---|
| 33.1(97) | 全球服务机构数量分析（总量+历年趋势） | PORTAL | TRACE-SVCCHAIN-PORTAL | `/service-portal/overview` | 口径待定 ❓ | Q-SVCCHAIN-06（全球数据源） |
| 33.1(98) | 服务机构类型分析 | PORTAL | 同上 | 同上（类型环形） | 口径待定 ❓ | Q-SVCCHAIN-06（分档字典） |
| 33.1(99) | 服务机构规模分析 | PORTAL | 同上 | 同上（四档条形） | 口径待定 ❓ | Q-SVCCHAIN-06 |
| 33.2 | 服务机构产业分布（结合产业链全景图） | PORTAL | 同上 | `/service-portal/industry-distribution` | closed | —（CT-SVC-PT-01 字典复用） |
| 33.3 | 服务机构区域分布（全球/全国地图） | PORTAL | 同上 | `/service-portal/region-map` | 口径待定 ❓ | Q-SVCCHAIN-06（区域归属口径） |
| 33.4 | 服务机构技术能力（各产业 Top30） | PORTAL | 同上 | `/service-portal/capability-rank` | 演示态 🧪 | Q-SVCCHAIN-01（CT-SVC-PT-03 口径复用） |
| 33.5(100) | 深圳产业服务机构数量（历年趋势） | PORTAL | 同上 | `/service-portal/shenzhen` | 口径待定 ❓ | Q-SVCCHAIN-06 |
| 33.5(101) | 产业机构类型统计 | PORTAL | 同上 | 同上 | 口径待定 ❓ | Q-SVCCHAIN-06 |
| 33.5(102) | 产业机构产业领域分布（结合深圳产业链全景） | PORTAL | 同上 | 同上（领域×环节分布） | closed | —（环节字典同 CT-SVC-PT-01） |
| 33.5(103) | 产业机构区域分布（十区地图） | PORTAL | 同上 | 同上 | 口径待定 ❓ | Q-SVCCHAIN-06 |
| 33.5(104) | 重点产业服务机构（概况/规模/领域/业务分布四板块） | PORTAL | 同上 | 同上（KeyOrgDetailDrawer） | 演示态 🧪 | Q-SVCCHAIN-06（遴选参数） |

## 四、结论

- **36 行全闭合，无遗漏、无双重归属**（跨叶子共用能力——对比篮 CT-SVC-ORG-03、画像抽屉 CT-SVC-ORG-02、环节字典 CT-SVC-PT-01、技术力口径 CT-SVC-PT-03——在 TRACE 以契约登记，不重复计数）。
- 状态分布：closed 9 行、演示态 🧪 18 行、口径待定 ❓ 9 行。全部 🧪/❓ 行 UI 均有诚实性标注（红问号/⚠️/🧪），对应开放项 Q-SVCCHAIN-01~06、Q-SYNTH-01~03 已登记《客户决策清单跟踪表》§2（253-261 行，全部 🟡）。
- 算法定义卡族（Q-SVCCHAIN-01/02/03/05 + Q-SYNTH-01/02/03，责任人唐绍祖）与数据源口径族（Q-SVCCHAIN-04/06）为**上线闸门**：落地前 🧪/❓ 行禁止对外决策展示。
