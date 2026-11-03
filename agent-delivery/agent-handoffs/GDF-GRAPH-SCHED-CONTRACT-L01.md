# GDF-GRAPH-SCHED-CONTRACT-L01 · GDF与知识图谱引擎调度接口契约与时序图

> 格式按 `templates/handoff-template.md`。定义任务，不写业务代码。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 2026-11-02 用户授权认领并执行。监管人用花名册与 `dispatch-rules.yaml` 中 architect-agent 的默认监管人，未改成其他人。锁 4 小时。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义任务。未用 YAGNI 跳过架构铁律。本文不缩交付范围。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-GDF-GRAPH-SCHED-SEQ` |
| 图 diff | 新图。参与方是 GDF 调度、燕大知识图谱引擎、引擎内部入图作业。边上能分开看到触发、已收下、轮询中、成功、失败。`SYSINT-SCHEME-06-SEQ` 只改了 GDF 到亿集 API 那条虚线的标签，节点未改，虚线仍表示未跑通。`SYSINT-SCHEME-07-SEQ` 节点未改。 |
| 会签态 | `draft`（写在图前的 yaml 里，不是已放行） |
| 说明 | 同一张图写入详细设计，以及两份集成方案的 §2.2 和 §2.3。不复用 `SYSINT-SCHEME-06-SEQ`、`SYSINT-SCHEME-07-SEQ`。 |

## 范围与实现

把 2026-11-02 锁定的四条基本方案写成详细设计，不改口径。

- GDF 与知识图谱引擎只通过任务调度转发通讯。
- 入图调度任务在引擎上完成。
- 引擎自己读增量，判断条件与 GDF 一致。
- GDF 发起只传任务类型枚举和时间戳。

详细设计路径：`agent-delivery/工程过程/04-系统集成/GDF-GRAPH-SCHED-CONTRACT-L01-调度转发接口设计.md`。

同一段契约摘要和同一张时序图写入：

- `agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/技术方案.md` 的 §2.2、§2.3
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/技术方案.md` 的 §2.2、§2.3

GDF 方案 §2.1 里「GDF 触发亿集 API」那句，以及贴源总图上对应虚线，改成指向这次调度转发，仍然写明没有跑通。§2.3 企业 ES / 图谱触发行仍是飞书值班。另加产业链入图走调度转发。

枚举：业务上只确定产业链第一批，即 `industry_chain_node` 当天 Wave B `success` 之后的环节点入图，引擎内部写 `gkx_chain` 的 Tag `segment`。字面值写的是「待燕大配置，不进本文」。没有把未上线 Java 路径里的 `segment_vertex` 当成引擎枚举。

时间戳：字段名、格式、时区写的是「还没有」。没有把方式 A 的 `since`、Java 的 `dwd_success_at`、入向量库的 `index_version` 写成已经能传的字段。

轮询用的号称为受理号，也就是锁定口径里的「任务号」。任务中心任务号和执行号分开写。二者与受理号的对应写的是「还没有」。方式 A 禁止。方式 B 与 Schedule 立即触发的形状对不上「只传枚举和时间戳」，因此没有配进 DAG。

未执行 nGQL，未改图空间，未把 definition id、schedule id 写入 git。未关闭 `SYSINT-SCHEME-06-L01`、`SYSINT-SCHEME-07-L01`。未把任务标成 done 或 ready_to_sign。

## 偏离说明

没有偏离锁定的四条。和《亿级科技知识图谱API文档》的差距写在设计第 8、9、14 节，用「还没有」或「待燕大配置」标出，没有编成已经能调的字段。

## 问题清单

- 只接收枚举和时间戳、并立刻返回受理号的转发入口，现有三条 HTTP 都对不上。
- 受理号是不是执行号，还没有。
- 现有 §2.9 查询按 §2.10 不更新终态，轮询不到成功或失败。
- 水位列名和 cron 在必读文档里没有，本文不补。
- 企业维仍是飞书值班，不在本接口里当成已经能调。

## 修改内容

- 新建详细设计。
- GDF 集成方案 §2.1 虚线指向调度转发；§2.2、§2.3 写入同一段摘要和同一张图；企业飞书行保留，另加产业链入图一行。贴源总图节点未改。
- 图数据库集成方案 §2.2、§2.3 写入同一段摘要和同一张图。在线查图时序的节点未改。文首说明这张新图不关闭 `SYSINT-SCHEME-07-L01`。

## 测试结果

- 定义文档，无业务单测，无 nGQL，无 graphd 连接。
- 核对五处摘要正文相同：详细设计 1 处，两份方案的 §2.2 与 §2.3 各 1 处，共 5 处。`diagram_id` 都是 `SYSINT-GDF-GRAPH-SCHED-SEQ`。
- 未把任务中心任务号和执行号都叫作任务号。

## 遗留风险

- 在燕大给出枚举对照、时间戳格式，以及能反映终态的查询之前，GDF 不能把这条转发配进 DAG。配早了会误用方式 A 或未上线的 Java 路径。
- §2.10 的查询限制不解除的话，GDF 即使拿到执行号也关不了单。
- 本任务停在联调/会签前。不写「会签通过」。

## 产物清单

- `agent-delivery/工程过程/04-系统集成/GDF-GRAPH-SCHED-CONTRACT-L01-调度转发接口设计.md`
- `agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/技术方案.md`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/技术方案.md`
- 本 handoff

## 验收证据

- 对照问 8、贴源包 `12` §5、产业链与企业入图包 `06`：链树 DWD `success` 之后才转发；收下不等于图已更新；失败不回滚 DWD；企业仍是飞书值班；Java `POST /chain/v1/graph/jobs/{job}/sync` 标成未上线并禁止配进 DAG。
- 对照 API 文档 §2.7、§2.9、§2.10、§2.11：方式 A 禁止；方式 B 返回执行号且不创建任务中心任务号；Schedule 立即触发无 Body 且不返回这两个号。
- CI：定义文档，无业务流水线。

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本文不写算法。入图仍在引擎侧，不把算法放进 Java，也不放进 GDF 节点 |
| 2 | 调用链：前端 → Java → Python `/internal/*` | ✅ 本接口不是在线读链。GDF 不调用 `POST /internal/v1/chain/graph/project`，不直连 Python 入图实现 |
| 3 | 图谱用 NebulaGraph，禁止 Neo4j | ✅ 正式空间名 `gkx_chain` 只作为引擎内部目标。本文不执行 nGQL，不直连 graphd |
| 4 | 可观测性 | ✅ 不改运行时代码，不新造追踪字段。图数据库方案 §2.3 原有 trace 句保留 |
| 5 | CI/CD | ✅ 定义文档。`cicd` 不要求本叶单独 rollout。无业务镜像 |
| 6 | demo 不 merge 进 lumen | ✅ 未改 demo 仓，未把 demo 空间 `demo_gkx_chain` 写成正式写入目标 |
| 7 | 共享聚合：前端只调 Java，Java 不写算法、不直连 nGQL | ✅ 未改前端和 Java。未上线的 Java 受理路径禁止配进 GDF DAG，没有另写一套当成已能调 |
| 8 | 数据走 ADS；Mock 先行 | ✅ 不改 ADS 表。入图读增量的水位列还没有，没有编造源列 |
| 9 | D8 前端规范 | ✅ 不涉及页面 |
| 10 | D9 指标 8 件套与四维就绪度 | ✅ 不涉及指标展示。未把入图完成说成指标已 live |
| 11 | D10 交互规范 | ✅ 不涉及交互 |
| 12 | D12：lumen 不调用 demo 服务 | ✅ 未增加 lumen 对 demo 的调用。正式空间与 demo 空间继续分开 |
| 13 | D14 对象存储 | ✅ 不写桶，不碰 RustFS |
| 14 | D16 缺项补齐 | ✅ 不建 `gapfill_` 表，不灌数 |
| 15 | D17 合规 / 合理 | ✅ 不改合规算法闭包，不新增 `-合理` 路由 |

## CI/CD（必填）

- 分支：`dev`
- commit：与本 handoff、详细设计、两份方案同一次提交。注册表认领另一次提交。哈希以推到 `origin/dev` 的结果为准
- pipeline URL / ID：无。编排仓定义文档无业务流水线
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未跑服务。核对限于文档互引和五处摘要一致

## 可观测性（建议）

- OTEL_SERVICE_NAME：无。本叶不改运行时
- traceId（dev 抽样）：无
- Tempo / Loki：无

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 90000 |
| model_used | grok-4.7 |
| actual_cost | 0.04 |
| cost_warn | green |

说明：本叶没有控制台分项。90000 按本轮通读 API §2.7–§2.11、问 8～13、两份触发契约和两份集成方案后写详细设计估算。价表没有 grok-4.7 的单价，`actual_cost` 只作登记，低于 10 美元，`cost_warn` 为 green。

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/GDF-GRAPH-SCHED-CONTRACT-L01-调度转发接口设计.md`
- `agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/技术方案.md`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/技术方案.md`
- `agent-delivery/agent-handoffs/GDF-GRAPH-SCHED-CONTRACT-L01.md`
