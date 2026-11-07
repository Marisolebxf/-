# 深圳政策现状分析 · LOOP 执行编排计划

- 状态：2026-11-08 02:44 轮：方案 A（读取侧收窄）已上线（`lumen-algo-py` `4df6ab5`，`CITY_SECTION_SQL` 加 `COALESCE(source_plane,'')='domestic' AND etl_batch_id IS NULL`；CI 4280 全绿，entan-api 已部署）。原样 force 重签：`POLICY-20261108-009`（产业，沿用 009 指纹）、`POLICY-20261108-010`（技术领域组合，沿用 011 指纹），两条 `success`、`reused=false`。三卡全绿：879 / 33.5585 / 名次 5 / 0.4653 / spearman 0.9467（`city_rows=10295` 与基线一致，城市回填未漂移截面）；档位 `4`（QPOL-02）；落地实效 `computable=true`、`score=72.7658`（gapfill 缺项行实算，`EFFECT-READ` 公式已接通，`honesty.source=dwd, degraded=false, fabricated=false`）；011 适配 9.245 / 43 / 锚点「智能网联汽车、人工智能」；第 4 章印分数 72.7658、第 5 章有供给结构与锚点适配。本轮起验收探测改读 `POLICY-20261108-009` 与 `POLICY-20261108-010`。DB 直查本轮受限（跳板机无 mysql 客户端），截面读数以算法 `diagnostics` 实读为证。有缺口按第 4 节派；同一缺口键连续两轮仍在则停止，交给人。
- 流程：`agent-delivery/产品实现规程.md` §6.5（用例 §6.4，SDD §4.1）。本模块经当次点名纳入，专题其他页不跟着进。
- 系统：科技专题服务系统。循环不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

## 1. 通过线

用例在 `agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/深圳政策现状分析-合规演示用例.md`。本计划不代替那份覆盖表，也不另编覆盖表。

产业结果 `POLICY-20261108-009`（集成电路，`industry_vid=chain:INB1303`，沿用 `POLICY-20261107-009` 指纹）。技术领域结果 `POLICY-20261108-010`（沿用 `POLICY-20261107-011` 指纹）。旧号 `POLICY-20261107-009/011` 与 `004` 不再当入口。验收不新签发任务，不带 `force=true`。

通过线（都要同时成立）：

| 项 | 预期 |
|---|---|
| 探测 | `GET` `POLICY-20261108-009` 与 `POLICY-20261108-010` 的结果，两条都带 `user_id=guest`。`POLICY-20261107-009/011` 与 `004` 不再当入口 |
| 支持力度 | 009 与 011 都是 879 / 33.5585 / 名次 5 / 层级均值 0.4653 |
| 扶持档位 | 两条结果都是 `value=4`，原因含 `QPOL-02`。空值、「无金额列」、写成 0 都不算通过 |
| 落地实效 | 两条结果都是 `computable=true`，`score=72.7658`（gapfill 缺项行实算；公式接通前的占位基线 50 已退役，不再核对 50） |
| 011 适配性 | `score=9.245`，`hit_count=43`，锚点「智能网联汽车、人工智能」 |
| 第 5 章 | 有供给结构 |
| 第 4 章 | 目标是印出落地实效实算分（当前 72.7658），不印「不可算」也不印 0 |
| 需规 114 指标体系 | 完成线是 demo 原型整块指标体系，不是「政策数量 / 资金规模 / 创新激励」三个勾选。默认入模 8 项，维内等权，一级权重 34/33/33，并有一键均分、恢复默认模型。页面还没有这块时，挂 `LUMEN-POLICY-SZ3D-FE-SRS-R20261107`，不建数据单、不建算法单 |
| 需规 116 仪表盘 | 同样挂 `LUMEN-POLICY-SZ3D-FE-SRS-R20261107`，不建数据单、不建算法单 |
| 落地实效不出现 Mock | 合规演示的配置区、结果和报告不出现 Mock。落地实效按 `gkxlumenx_gapfill` 里每条政策的缺项行实算，空值不写成 0。公式接通前，接口仍核对 `computable=true`、`score=50`。Mock 字样单独算缺口，不用这条分数代替 |
| 产业只交 VID | 因此出现「未提供链名」时，挂到同一张前端任务 `LUMEN-POLICY-SZ3D-FE-SRS-R20261107`，不建数据单、不建算法单 |
| 库 | `demo_gkxlumenx_dwd.policy_base_info` 中原生行 `city='深圳市' AND COALESCE(source_plane,'')='domestic' AND etl_batch_id IS NULL` 为 879，且 `rank` 有值。层级均值保持 0.4653。表里混灌的一张图 debug 批次（`etl_batch_id='debug_one_map_20261107_v1'`）与图2合成批（`etl_batch_id LIKE 'SYNTH-%'`）不算进截面，也不删。正式库只读 |

需规 114 对齐 demo 原型的指标体系构建。默认入模 8 项：支持力度为政策数量、资金规模、创新激励；产业适配性为政策-产业需求匹配、产业链覆盖广度、细分领域命中率；落地实效为落地执行率、受益覆盖广度。政策层级覆盖面、反馈满意度默认不入模。维内等权。一级权重为支持力度 34、产业适配性 33、落地实效 33。一键均分把一级权重写回 34/33/33。恢复默认模型把入模恢复为这 8 项，并把一级权重恢复为 34/33/33。循环不打开页面。页面还没有这块时，只挂前端任务。

落地实效维当前标着 Mock 缺口。合规演示不能出现 Mock。建表和按政策灌数不写在本计划正文里，任务是 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-GAPFILL`（已有政策）和 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-SYNTH`（图2政策分析算法库的合成与新增）。公式改读这张表是 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-READ`。配置区去掉 Mock 角标是 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-NOMOCK`。需规 116 的仪表盘仍挂 `LUMEN-POLICY-SZ3D-FE-SRS-R20261107`。

层级均值保持 0.4653，不追回 2026-10-25 的 0.4579。无城市名的行不补城市。

`LUMEN-POLICY-SZ3D-DATA-DEMO-L01` 不在本计划里签 `done`。

## 2. 验收单

沿用已有验收单，不另建。

| 项 | 值 |
|---|---|
| ID | `TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`algorithm-agent` |
| 状态 | 保持 `ready`，不签 `done` |
| 依赖 | `LUMEN-POLICY-SZ3D-DATA-DEMO-L01` 已有 handoff。不要求它先 `done` |
| 报告 | `agent-delivery/agent-handoffs/政策模块-E7/TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP.md` |

一轮写完退回 `ready`。不签 `done`。

note 不写「联调通过」「会签通过」「联调完成」「联调确认」「集成测试通过」。

## 3. 后端调用

token 只读本机文件 `%USERPROFILE%\.gkx\topic-loop-token`。请求头 `Authorization: Bearer`、`systemCode: topic`。与展示系统的 token 文件分开。不把口令或 token 正文写入本计划、handoff、注册表或 git。不打印。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `GET http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/POLICY-20261108-009/result?user_id=guest` | 产业结果。只验 token 和这条已签发结果 |
| 探测 | `GET http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/POLICY-20261108-010/result?user_id=guest` | 技术领域结果。只验 token 和这条已签发结果 |
| 库 | 只读 `demo_gkxlumenx_dwd.policy_base_info` | 核对原生行（加 `COALESCE(source_plane,'')='domestic' AND etl_batch_id IS NULL` 条件）`city='深圳市'` 为 879，以及深圳行的 `rank` 仍有值 |

任一探测返回 401、424，或正文为「访问令牌不存在」「用户凭证已过期」「token expired」：验收单改为 `blocked`，通知 `human:淮政玮`，不建子任务，不再开一轮。note 只写「token 失效，已通知 human:淮政玮」。

任一探测返回 404：同样停止并通知 `human:淮政玮`。原因写「接口映射不存在」或「演示任务结果不可读」。不建子任务，不改成补数。

两条都返回 200 之后，才进入第 1 节对照。库只 `SELECT`。不写 ODS、供应方库、`gapfill_`、新 ADS。正式库只读。

## 4. 缺口怎么派

只比较第 1 节。每轮最多两张新建子任务。不建 QUERY 单。

| 类 | 何时 | 执行人 | 计划 ID |
|---|---|---|---|
| DATA | 深圳 `city` 不足 879，或 `rank` 空；或扶持档位因缺列、空列而没有结果（含空值、「无金额列」、写成 0）。落地实效缺项不归这一行，归下面两张已建的 gapfill 单 | `data-agent` | `TOPIC-POL-SZ3D-DEMO-FIX-R{YYYYMMDD}-DATA` |
| 落地实效 gapfill | 合规演示出现 Mock，或政策没有落地实效缺项行 | `data-agent` 灌已有政策；图2合成入口由 `algorithm-agent` 灌当次写入的政策 | `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-GAPFILL`、`EFFECT-SYNTH`。公式接通挂 `EFFECT-READ`。去掉角标挂 `EFFECT-NOMOCK` |
| ALGO | 行数仍是 879 且 `rank` 在，支持力度的分数、名次或层级均值对不上；或 011 适配性的分数、命中数、锚点对不上；或源列已有非空值，结果字段里档位仍不可算，或落地实效不是 `computable=true`、`score=50`。gapfill 已有行但公式仍不读，归 `EFFECT-READ`，不另开 ALGO | `algorithm-agent` | `TOPIC-POL-SZ3D-DEMO-FIX-R{YYYYMMDD}-ALGO` |
| 挂前端 | 需规 114 的整块指标体系页面还没有；或需规 116 的仪表盘页面还没有；或产业只交 VID，结果出现「未提供链名」 | 不新建 | 挂到已有 `LUMEN-POLICY-SZ3D-FE-SRS-R20261107` |

下列情况不建数据单，也不建算法单：

- 需规 114 的整块指标体系（默认入模 8 项、维内等权、一级权重 34/33/33、一键均分、恢复默认模型）。页面还没有时，只挂 `LUMEN-POLICY-SZ3D-FE-SRS-R20261107`。不是三个勾选。
- 需规 116 的仪表盘。同样只挂这张前端任务。
- 落地实效的 Mock。不挂前端任务。已有政策归 `EFFECT-GAPFILL`，图2合成与新增归 `EFFECT-SYNTH`。
- 产业只交 VID 导致的「未提供链名」。同样只挂这张前端任务。
- `POLICY-20261107-009` 与 `POLICY-20261107-011` 的旧章节已由 `POLICY-20261108-009/010` 重签取代，不再参与验收。第 4 章目标是印出实算分，第 5 章仍要有供给结构。不为旧章节建 DATA 单，也不建 Python 算法单。

同一缺口键连续两轮仍在：停止建单，交给 `human:淮政玮`。

子任务 handoff 落盘后，才把验收单拨回 `ready`。下一轮仍读 009 与 011。只有数据或算法子任务明确要求重算时，才另签发任务；签发号写入该子任务 handoff，验收单改读新号。新号出现之前，009 与 011 的旧章节不算通过。验收轮自己不签发。

## 5. 一轮顺序

1. 验收单 `TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP` 保持 `ready`，不签 `done`。
2. 跑一轮时才认领，`supervised_by=human:淮政玮`。一轮写完退回 `ready`。
3. 读本机 `%USERPROFILE%\.gkx\topic-loop-token`，按第 3 节 GET `POLICY-20261108-009` 与 `POLICY-20261108-010`。不打开页面。不把 token 正文写入任何文件。
4. 401、424 或 404 则停，并按第 3 节通知 `human:淮政玮`。
5. 两条都是 200，才核对第 1 节，并 `SELECT` 深圳市行数与 `rank`。
6. 有缺口才按第 4 节处理。验收当轮不改库、不重算。指标体系、仪表盘、「未提供链名」只挂已有前端任务。落地实效出现 Mock，或政策没有缺项行，挂已建的 `EFFECT-GAPFILL` 与 `EFFECT-SYNTH`，不新建第三张灌数单。旧章节不建 DATA 单，不建 Python 算法单。
7. 报告只追加一节到 `agent-delivery/agent-handoffs/政策模块-E7/TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP.md`。验收单留在 `ready`。note 不用第 2 节禁止的那几句。
