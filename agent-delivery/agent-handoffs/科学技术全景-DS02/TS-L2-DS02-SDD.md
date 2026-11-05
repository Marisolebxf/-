# TS-L2-DS02-SDD · 科学技术全景系统详细设计

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
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

## 范围与实现

对照需规序号 17–47。展示只做 17–33。一次 `POST /display/v1/situation/panorama/graph`。34–40 不建实现单。41–47 归维护管理。实现只补读图、灌数、主路径测试。

## 偏离

无偏离。不重开 `FE-TS-02A` 与 `SYSINT-05-01A/B`。

## 产物清单

- `sdd/科学技术全景-系统详细设计说明书.md`
- `功能拆解.md`
- 展示 WBS-05-01d

## 验收证据

编排仓无业务 CI。签收核对结论：同意签收。调用链与功能架构第 2 节一致。

## 架构合规自检

1. 算法只在 Python。Java 不写 nGQL。✅
2. 调用链与功能架构相同，一次 graph，七个已有字段。✅
3. 图只读 `demo_gkx_chain`。✅
4. 可观测沿用现有服务，本叶不新加。✅
5. 定义稿无业务 CI。✅
6. D12：不调用 `demo-*`。✅
7. D18：分数表不进 ODS / DWD / 供应方库，不用 `gapfill_`。D4 保持 mock。接口不直接返回写死 mock。✅

## Cost 回填

- actual_tokens: 16000
- model_used: claude-sonnet-4.5
- actual_cost: 0.09
- cost_warn: green
- 会话模型为 Grok 4.7。注册表枚举无此项，按 sonnet 单价与 architect 80/20 计入。

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
