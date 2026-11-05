# TS-L2-DS02-SDD · 科学技术全景系统详细设计

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | 未认领。定义单已建，状态 ready |
| supervised_by | `human:淮政玮` |
| claim_type | 未认领 |
| 说明 | 说明书已落盘。功能架构四角色已同意，签收未做，不推待签收 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义任务，不写业务代码 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-SDD-SEQ`、`TS-L2-DS02-SDD-DATA` |
| 图 diff | 说明书第 3、4 节。三个展示功能一次读取；分数表只供给三个数字 |
| 会签态 | 功能架构四角色同意。签收未做 |
| 说明 | 与 `TS-L2-DS02-ARCH` 同一条调用链 |

## 修改内容

- 新增 `sdd/科学技术全景-系统详细设计说明书.md`。按需规 17–47 拆。展示只做 17–33。34–40 不建单。41–47 归维护管理。
- 实现任务：已有 `FE-TS-02A`、`SYSINT-05-01A-L01`、`SYSINT-05-01B-L01`、入图三单不重开。新建 `TS-L2-DS02-READ-PY-L01`、`TS-L2-DS02-SCORE-L01`、`TS-L2-DS02-TEST-L01`，签收前仍为 backlog。

## 测试结果

- 未改业务仓。

## 架构合规

- 与功能架构同一条调用链。展示只做序号 17–33。34–40 不建实现单。41–47 归维护管理。
- 一次 `POST /display/v1/situation/panorama/graph`，七个已有字段。读失败不回退 fixture。空图 `GRAPH_EMPTY`。
- D18 分数表不进 ODS / DWD / 供应方库，不用 `gapfill_`。D4 保持 mock。

## 遗留风险

- 三个 `metric_id` 的注册口径仍是 IPC4 / 深圳卡位。mock 行不能说成那些函数的结果。
- 入图未完成时，三个功能是空图。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`
- pipeline URL / ID：编排仓无业务 CI
- K8s rollout：无

## 可观测性（建议）

- 沿用 `gkxlumen-display` 与 `lumen-platform-algo-py`。本叶不新加观测点。

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/科学技术全景-系统详细设计说明书.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/功能拆解.md`
- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/WBS.md`
