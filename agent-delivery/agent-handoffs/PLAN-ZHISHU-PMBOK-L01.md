# PLAN-ZHISHU-PMBOK-L01 · 智树工作计划（九域 + 三线 L1）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:郭万迎` |
| supervised_by | `human:郭万迎` |
| claim_type | `pull` |
| 说明 | Cursor MCP 未挂载；经 `scripts/task-mcp-cli.mjs` 认领。依赖 LAYOUT / 总集叶当时均为 `review` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 未改调用链 |
| 会签态 | N/A |

## 问题清单

- S1 出门日仍为 08-25；`current_stage_id` 仍为 S1（未切 S2）
- S3/S4 新节点无 registry `task_ids`（按确认不建单）
- TBD-02 / TBD-04 / TBD-05 仍开放
- 总集【02】【04】日期与智树 L1 不一致处只对照、未改 01 夹
- 11-10 展示第三闸责任人待定，与郭万迎送智谱同日，核验包窗口紧

## 修改内容

- `02-智树工作计划/`：README 整合 + 九域 01–09；进度写三线共用指标闸口 + 算法库/专题/展示
- `project-plan.yaml` / `project-plan.md`：S2 出门条件与 N-S2-02 对齐 9.5/9.15；补 S3 五节点、S4 N-S4-02；TBD-01→王惠（仅指标梳理）；N-S3-01 Owner 唐绍祖；专题/展示开发闸口待定；关闭 TBD-03
- 卷 02 INDEX 本波链到进度页

未改：`system-wbs.yaml`、`scrum-sprint.yaml`、总集 01 夹正文、`PLAN-S5` 状态。

## 测试结果

- `project-plan.yaml` Python yaml 解析（见执行记录）
- 九域相对链接均指向 `../../../` 或卷页

## 遗留风险

见 [07-风险.md](../工程过程/02-策划与监控/02-智树工作计划/07-风险.md)

## CI/CD（必填）

- 分支：`dev`
- commit：待 PM 确认后提交
- pipeline / 部署 / K8s：N/A（文档叶）

## 可观测性

N/A

## 涉及文件

- `agent-delivery/工程过程/02-策划与监控/02-智树工作计划/`（README + 01～09）
- `agent-delivery/工程过程/02-策划与监控/INDEX.md`
- `agent-delivery/project-plan.yaml`
- `agent-delivery/project-plan.md`
- `agent-delivery/agent-handoffs/PLAN-ZHISHU-PMBOK-L01.md`

## 验收对照 DoD

| DoD | 证据 |
|---|---|
| 九域目录 | 01-范围 … 09-干系人；整合在 README |
| L1 里程碑表（日期/总集/Sx/Owner/出门条件） | `02-进度.md` §5；YAML S2–S4 节点 |
| 与 01 夹对照、不扩范围 | 进度对照列；`01-范围.md` 跟 scope-baseline |
| 细项 WBS 本叶不做 | README 写明 |
| 后续拆单 ID 草案 | 见下，**未建单** |

## 后续细项拆单 ID 草案（不建单）

| 草案 ID | 对应节点 |
|---|---|
| `PLAN-S3-ALGO-MODEL-L01` | N-S3-01 |
| `PLAN-S3-TOPIC-FEBE-L01` | N-S3-02 |
| `PLAN-S3-DISP-SITUATION-POLICY-L01` | N-S3-03 |
| `PLAN-S3-TOPIC-FIVE-ALGO-L01` | N-S3-04 |
| `PLAN-S3-DISP-ACHIEVE-TALENT-L01` | N-S3-05 |
| `PLAN-S4-DISP-RES-GRAPH-PANORAMA-L01` | N-S4-02 |

解锁仍须 PM confirm，禁止手改 ready。

## 下一步

1. PM 审 `project-plan` 与进度表；同意后 commit（`[human:郭万迎]`）
2. coordinator 收本 handoff
3. 需要派工时再按草案建单
