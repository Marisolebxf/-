# KG-ENT-GRAPH-LOAD-L01 · 企业维度入图：燕大派单包、GDF接口契约与gapfill

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-11-02 淮政玮指令认领并执行。依赖 `KG-7ELEM-BUILD-REQ-L03`、`KG-7ELEM-BUILD-REQ-L05` 均为 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义文档，不写业务代码。 |

## 范围与实现

企业维入图派单包 v0.1，目录 `agent-delivery/data/Graph/入图需求和派单/KG-ENT-WORKPACK-v0.1/`。DoD 里的旧路径 `data/GDF/派单包/入图/GDF-KG-ENT-WORKPACK-v0.1/` 不作废改登记表，以任务备注里的 Graph 路径为准。

包内写明：七要素 schema 一次建在新建空间 `gkx_chain`；第一批只灌企业点、`supply`、`parent_sub`；源表、VID、方向在 `01`。GDF 不直写 Nebula。触发请求和回执写在 `06`，并写明 Java 对外路径和 callback 现网没有，今天不配进 DAG。`07` 只写缺口方法和 `gapfill_` 表名，不建表、不灌数。

未执行 nGQL，未连接 `10.50.75.136:9669`，未改已签收的初始化脚本，未改已投出的企业贴源洗数包。

## 偏离

- 交付目录从 DoD 的 GDF 入图路径改为 `data/Graph/入图需求和派单/`，与 GDF 平级。任务备注已声明旧路径作废。
- 「密码和连接串不进包」：图库口令和读接口密钥不进包。MySQL 只读口令按淮政玮指令明文写在 `04`。库限 `gkxlumenx_dwd`、`gkxlumenx_ads`。
- DoD「不改图空间」按备注执行：不改 `demo_gkx_chain`。燕大目标是新建 `gkx_chain`。
- 派单说明第 4 条写明回签上传目录：`工程过程/04-系统集成/07-图数据库集成/对接文档/燕大/`。本包尚未正式发给燕大。淮政玮 2026-11-02 签收本派单任务。

## 产物清单

- `agent-delivery/data/Graph/入图需求和派单/KG-ENT-WORKPACK-v0.1/`（00–07，含 `03-schema-gkx_chain.ngql`）
- `agent-delivery/data/Graph/README.md`
- `agent-delivery/data/Graph/建图/README.md`
- 本 handoff

## 验收证据

- 对照已签收 `KG-7ELEM-LOAD-PATH-L02`：第一批只收企业点、`supply`、`parent_sub`。双向 `cooperate` 和 `participates` 不进第一批。
- 对照企业贴源包 `15` §6：对外 `/ent/v1/*` 与图谱 callback 未上线。`06` 把目标字段和现网飞书交接分开写。
- 未跑建图语句，未连 MySQL，未连 Nebula。
- CI：定义文档，无业务流水线。

## 架构合规自检

1. 算法只在 Python：入图规则要求燕大用 Python 脚本，Java 不算算法。✅
2. 调用链：GDF 只触发 Java REST，不直连 Python，不直连 graphd。✅
3. 图谱：Nebula，燕大写入新建空间 `gkx_chain`，展示仍读 `demo_gkx_chain`。本单未执行语句。✅
4. 可观测：本单不改运行时代码。目标回执保留 `task_id`，现网回执未上线，不写成已有 trace。✅
5. CI/CD：定义文档，无业务仓发布。✅
6. demo 隔离：不改 demo 写图空间，不把 demo 点边拷进 `gkx_chain`，不 merge demo 仓。✅
7. 共享聚合：不改展示读路径，Java 不写图语句。✅
8. D12：本单不新增 lumen 对 demo 服务的调用。✅
9. D14：不写对象存储。✅
10. D16：`gapfill_` 只写方法和表名，不建表、不灌数，不写 ODS / 供应方库。✅

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 90000 |
| model_used | grok-4.7 |
| actual_cost | 0.03 |
| cost_warn | green |

说明：本叶没有控制台分项。90000 按本轮读派单包和上图路径、补 `06`/`07` 估算。价表没有 grok-4.7，`actual_cost` 用文档档 A（输入 $0.25/M、输出 $1.25/M，输入占 95%）算出约 $0.03，只作登记，不是账单。`valid_model_enum` 尚无 grok-4.7。

## CI/CD（必填）

- 分支：`dev`
- commit：与本 handoff、派单包同一次提交
- pipeline URL / ID：无。定义文档无业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未连库，未执行 nGQL

## 涉及文件

- `agent-delivery/data/Graph/入图需求和派单/KG-ENT-WORKPACK-v0.1/00-背景与派单说明.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-ENT-WORKPACK-v0.1/02-技术方案.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-ENT-WORKPACK-v0.1/05-回签.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-ENT-WORKPACK-v0.1/06-GDF触发契约.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-ENT-WORKPACK-v0.1/07-gapfill清单.md`
- `agent-delivery/data/Graph/入图需求和派单/KG-ENT-WORKPACK-v0.1/README.md`
- `agent-delivery/agent-handoffs/KG-ENT-GRAPH-LOAD-L01.md`

## 遗留风险

- 触发契约的 HTTP 路径没有落号。现网仍是飞书交接。
- `enterprise_supply_chain` 在企业贴源包里曾标「本波不触发」。本包按已签收上图路径把它列入第一批，以本包为准，不改贴源包。
- 双向 `cooperate` 在 Nebula 里用两条有向边，规则未落地，第一批不写。
