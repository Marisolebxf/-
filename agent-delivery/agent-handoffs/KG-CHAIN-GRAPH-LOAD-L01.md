# KG-CHAIN-GRAPH-LOAD-L01 · 产业链维度入图：燕大派单包、GDF接口契约与gapfill

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-11-02 淮政玮指令签收。依赖 `KG-7ELEM-BUILD-REQ-L03`、`KG-7ELEM-BUILD-REQ-L05`、`KG-7ELEM-LOAD-PATH-L03` 均为 done。对齐企业维 `KG-ENT-GRAPH-LOAD-L01`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义文档，不写业务代码。`建图/产业链/脚本/chain_rules.py` 只是给燕大对照的规则样例，不接库。 |

## 范围与实现

产业链维入图派单包 v0.1，目录 `agent-delivery/data/Graph/入图需求和派单/KG-CHAIN-WORKPACK-v0.1/`。抽取说明在 `agent-delivery/data/Graph/建图/产业链/`。

公用的背景、两个空间、schema、MySQL 账号不另写，指向企业包 `00`、`03`、`04`。本包只写环节。第一批只写 Tag `segment`，源表 `gkxlumenx_dwd.industry_chain_node`，VID `segment:{node_id}`。不写 Tag `chain`。`depends_on` 的正式行是 `parent_child`，不改名，不进第一批。服务机构 `participates` 正式加工不产行。企业到环节的 `participates` 等企业点先在 `gkx_chain`。

派单说明第 4 条写明：填好的回签上传到 `工程过程/04-系统集成/07-图数据库集成/对接文档/燕大/`，文件名带完成日期。

GDF 不直写 Nebula。`06` 写明目标作业 `segment_vertex` 和现网回调没有，今天用飞书或工单。`07` 只写缺口方法和 `gapfill_` 表名，不建表、不灌数。不改已投递的产业链贴源包。

未执行 nGQL，未连接 `10.50.75.136:9669`，未改已签收的初始化脚本。

## 偏离

- 本版触发范围窄于 demo 能写的边：第一批只有环节点。`depends_on` 和两类 `participates` 写在需求和规则样例里，不进本版触发表。
- 贴源包 `12` 的 `POST /internal/v1/chain/graph/project` 是我方算法在洗数结束时写 `chain` 和 `segment`，给向量索引用。不是燕大作业，不算本批完成。
- 本包尚未正式发给燕大。淮政玮 2026-11-02 签收本派单任务。

## 产物清单

- `agent-delivery/data/Graph/入图需求和派单/KG-CHAIN-WORKPACK-v0.1/`
- `agent-delivery/data/Graph/建图/产业链/`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/WBS.md` 的 `WBS-07-00H`
- 本 handoff

## 验收证据

- 对照已签收 `KG-7ELEM-LOAD-PATH-L03`：第一批只收环节点。`depends_on` 不把 `parent_child` 改名。
- 对照企业包：空间、schema、库账号不复制。
- `chain_rules.py` 自检通过：`parent_child` 返回空，`reverse` 对调端点，`participates` 不写属性。
- 未跑建图语句，未连 Nebula。
- CI：定义文档，无业务流水线。

## 架构合规自检

1. 算法只在 Python：入图规则要求燕大用 Python 脚本，Java 不算算法。✅
2. 调用链：GDF 只触发，不直连 Python，不直连 graphd。✅
3. 图谱：Nebula，写入 `gkx_chain`，展示仍读 `demo_gkx_chain`。本单未执行语句。✅
4. 可观测：本单不改运行时代码。目标回执保留 `task_id`，现网回执未上线。✅
5. CI/CD：定义文档，无业务仓发布。✅
6. demo 隔离：不改 demo 写图空间，不把 demo 点边拷进 `gkx_chain`。✅
7. 共享聚合：不改展示读路径，Java 不写图语句。✅
8. D12：本单不新增 lumen 对 demo 服务的调用。✅
9. D14：不写对象存储。✅
10. D16：`gapfill_` 只写方法和表名，不建表、不灌数。✅

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 50000 |
| model_used | grok-4.7 |
| actual_cost | 0.02 |
| cost_warn | green |

说明：本叶没有控制台分项。50000 按本轮对照企业包和产业链上图路径、写派单包估算。价表没有 grok-4.7，`actual_cost` 用文档档估算，只作登记。

## CI/CD（必填）

- 分支：`dev`
- commit：与本 handoff、派单包同一次提交
- pipeline URL / ID：无。定义文档无业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未连 Nebula，未执行 nGQL

## 涉及文件

- `agent-delivery/data/Graph/入图需求和派单/KG-CHAIN-WORKPACK-v0.1/00-派单说明.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-CHAIN-WORKPACK-v0.1/01-产业链维需求.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-CHAIN-WORKPACK-v0.1/05-回签.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-CHAIN-WORKPACK-v0.1/06-GDF触发契约.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-CHAIN-WORKPACK-v0.1/07-gapfill清单.md`
- `agent-delivery/data/Graph/建图/产业链/`

## 遗留风险

- 触发契约的 HTTP 路径没有落号。现网仍是飞书交接。
- 企业点不在 `gkx_chain` 上之前，企业到环节的 `participates` 不能写。
