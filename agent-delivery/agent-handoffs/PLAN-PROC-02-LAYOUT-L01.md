# PLAN-PROC-02-LAYOUT-L01 · 工程过程 02 目录化（总集/智树计划夹）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:郭万迎` |
| supervised_by | `human:郭万迎` |
| claim_type | `coordinator_dispatch`（淮政玮建单后认领到 PM） |
| 说明 | 叶 1 仅目录与索引。执行：doc-agent 起草；措辞/链接 PM 终审 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |
| 说明 | 未压文档完整性 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓 Markdown 索引 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改调用链/存储流图 |
| 会签态 | N/A |
| 说明 | 过程索引，非 ARCH-IMPL |

## 问题清单

- 总集原始材料尚未收集（叶 2 阻塞原料，不阻塞本叶 DoD）
- 叶 2 / 叶 3 仍 backlog，未写计划正文

## 修改内容

- 建 `agent-delivery/工程过程/02-策划与监控/`：`INDEX.md` 承接原卷页索引，并增加「本卷两套计划」表
- 建 `01-总集大项目整体计划/README.md`、`02-智树工作计划/README.md`（用途 + 真源优先级 + 本波不做）
- 原 `02-策划与监控.md` 改为跳转 stub（选项 A）
- `工程过程/INDEX.md`：铁律增加 02 卷例外；卷表与 CMMI 行改指目录 INDEX
- `04-产品集成.md` 两处 02 链改指目录 INDEX

未改：`project-plan.md/.yaml`、`system-wbs.yaml`、`scrum-sprint.yaml`、`PLAN-S5` 状态。

## 测试结果

- 相对链接已按「夹内 INDEX 比原卷页深一层」改写（`../` → `../../` 指向 `agent-delivery/` 真源；卷页互指 `../00`～`../09`）
- 旧路径 `工程过程/02-策划与监控.md` 仍可打开并跳转

## 遗留风险

- Windows 上「同名 .md 文件」与「同名目录」可并存；其它 OS 同样可并存（扩展名不同）
- 仓内若还有未改的 `./02-策划与监控.md` 链，会落到 stub，行为正确

## CI/CD（必填）

- 分支：`dev`（编排主仓）
- commit：待 PM 确认后提交（本 handoff 时尚未 commit）
- pipeline URL / ID：文档叶，无业务镜像
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：打开 `agent-delivery/工程过程/INDEX.md` 点卷 02

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId（dev 抽样）：N/A
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/02-策划与监控.md`（stub）
- `agent-delivery/工程过程/02-策划与监控/INDEX.md`
- `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/README.md`
- `agent-delivery/工程过程/02-策划与监控/02-智树工作计划/README.md`
- `agent-delivery/工程过程/INDEX.md`
- `agent-delivery/工程过程/04-产品集成.md`
- `agent-delivery/agent-handoffs/PLAN-PROC-02-LAYOUT-L01.md`

## 验收对照 DoD

| DoD | 证据 |
|---|---|
| 已建目录 `02-策划与监控/`，INDEX 承接原索引 | `02-策划与监控/INDEX.md` |
| 子目录 01 / 02 各有 README | 两份 README |
| `工程过程/INDEX.md` 与相关卷页改指向新目录 | INDEX §1/§2；`04-产品集成.md` |
| 旧单文件链不断 | stub 保留 |
| 本叶不写总集/智树计划正文 | 子夹仅 README |
| handoff 写明 Owner=`human:郭万迎` | 本文件 |

## 下一步

1. PM 郭万迎审链接与措辞；同意后 commit（`[human:郭万迎]` 或 `[agent:doc-agent]` + 监管人）
2. coordinator 收本 handoff → `review` / 签收
3. 收集总集材料后开 `PLAN-ZONGJI-MASTER-L01`
