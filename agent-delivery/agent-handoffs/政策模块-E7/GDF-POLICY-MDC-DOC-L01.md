# GDF-POLICY-MDC-DOC-L01 · 政策包 v2.0.3：MDC / Graph / MRC / 灌数闸门说明

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-26 用户指定以淮政玮 + data-agent 领取并执行。锁 4 小时。依赖 `GDF-POLICY-WORKPACK-V2-L01` 已 `done`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |
| 说明 | 定义叶默认 off。未用 YAGNI 砍掉 `17`–`20` 或 `15` 的作业禁令。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无。未改 `POLICY-STORAGE-FLOW` |
| 图 diff | 无。本叶只核对说明，不新增写库边 |
| 会签态 | 不适用（未改图） |
| 说明 | C1 仍按 `12`。106 / 107 脚本未进包，不写 nGQL |

## 问题清单

- 登记备注写「正文已在工作区，认领后核对即可会签」。核对发现技术方案 §5 的 WBS-06-03D「可对端」写成「三章」，与包内 `17`–`20` 和 WBS「四章」不一致。已改成四章，并写明不代替 WBS-06-03。
- `16` 仍引用 `metrics/repro/out/` 的核对快照路径。那是 v2.0.1 的字典对照，不是把 repro 脚本拷进派单包。本叶不改 `16`，也不复制 repro。

## 修改内容

- 核对现行包 `GDF-POLICY-WORKPACK-v2` 包头 v2.0.3（commit `00d6e42c` 落盘 `17` / `18` / `19` / `20`、`15` 文末、CHANGELOG、README）。
- 技术方案 WBS-06-03D 可对端由「三章」改为「`17`–`20` 四章」，并写明不代替 WBS-06-03。
- 未改 `09`。`09` 最后提交仍是 `944ef4a3`，v2.0.3 提交的文件列表里没有它。
- 未生成 `scripts/mdc/`。包内 `scripts/` 仍只有 C1 / C2 两份。
- 未建 `mt_policy_` 表，未灌数。扶持空表仍指向 `GDF-POLICY-MT-SUPPORT-L01`。

## 测试结果

定义叶，无跑数、无 CDC、无业务仓 diff。对照 DoD：

| DoD | 结果 |
|-----|------|
| v2.0.3 含 `17` / `18` / `19` / `20` | 四份文件在包内。CHANGELOG v2.0.3 与 README 包头一致 |
| `15` 写明脚本未配前不建 MDC 作业 | `15` §5：`scripts/mdc/` 还没有，不要建节点，不要拷 `metrics/repro/` |
| 不改 `09` | `git log -1` 指向 `944ef4a3`，晚于该提交的 v2.0.3 未触及此文件 |
| 不生成 `scripts/mdc` | 目录不存在。`scripts/` 仅 `policy_c1_industry.py`、`policy_c2_clauses.py` |
| 不建 `mt_policy_`、不灌数 | `17` §3 与 `20` 写明本版不建表、不加工、不向 ODS 写 mock |
| 技术方案与 WBS-06-03D 指向本任务，不代替 06-03 | WBS 行与技术方案 §5 均写 `GDF-POLICY-MDC-DOC-L01`。06-03 仍是 Wave A/B 跑通叶 |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本叶不写脚本。后续 STAT / 106 / 107 另叶 |
| 调用链 | ✅ 说明叶。GDF 在脚本进包前不建 MDC 节点。不配 HTTP |
| 图谱 | ✅ 不写 nGQL，不改存储流图。C1 不代替 106 / 107 |
| 可观测 | 定义叶，无运行时埋点 |
| CI | `cicd: skip`（设计类文档） |
| D12 | ✅ 不把 demo 库写成产线目标 |
| D9 | ✅ 口径未闭合的指标只列表，不建作业、不灌假数 |
| D8 / D10 | 本叶无页面 |
| D14 | ✅ 不写对象存储 |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000（本会话估算，不是控制台账单） |
| model_used | grok-4.7 |
| actual_cost | 0.45 |
| cost_warn | green |

## 会签

2026-10-26 核对通过。本叶只说明范围和禁令，不是执行结果，也不是可对端。不代替 WBS-06-03 的跑通。

## 遗留风险

- MDC 第一批脚本归 `GDF-POLICY-MDC-STAT-L01`。脚本未进包前，GDF 不要建作业。
- 106 / 107 归 `GDF-POLICY-GRAPH-EXT-L01`。未配前不建作业。
- 灌数归 `GDF-POLICY-MOCK-GATE-L01`。负责人未确认批次上限、词表、提示词之前不写 mock。
- `mt_policy_` 归 `GDF-POLICY-MT-SUPPORT-L01`。未另行点头不建表。

## CI/CD（必填）

- 分支：`dev`
- commit：见本次提交
- pipeline URL / ID：编排仓无业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：文档核对，无运行时

## 涉及文件

- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/15-GDF触发调度与回执.md`（只读核对）
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/17-指标离线加工-POLICY-MDC.md`（只读核对）
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/18-实体关系抽取-POLICY-Graph.md`（只读核对）
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/19-实时指标-POLICY-MRC.md`（只读核对）
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/20-灌数闸门.md`（只读核对）
- `agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/技术方案.md`（可对端三章改为四章）
- `agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/WBS.md`（只读，已指向本任务）
