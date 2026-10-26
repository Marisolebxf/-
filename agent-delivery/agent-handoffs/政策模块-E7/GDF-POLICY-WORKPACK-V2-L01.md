# GDF-POLICY-WORKPACK-V2-L01 · 政策维 GDF 派单包 v2

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-26 用户确认认领并执行。锁 4 小时。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |
| 说明 | 派单禁止 ponytail 强度行。未用 YAGNI 砍掉 05 / 12 / 13 / 15。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 无。未改 `01-data-flow.md`。C1 仍只写 `policy_industry_rel`，C2 仍只合并 ADS 条款，与图上 2026-10-23 注一致。 |
| 会签态 | `approved`（`signoff_status: approved`，`human:淮政玮`，2026-08-21） |
| 说明 | 未发现新写库边。 |

## 问题清单

- 任务 DoD 写「继承 v1.0.3、不改 09」。同日用户已把取数改成不过滤 `is_deleted` / `is_history`，并要求贯穿到 DWD。v2 继承的是这份 v1.0.4，没有把历史行过滤加回去。UK 未改。
- 派单说明 §0.2 四项当时按默认执行。随后用户要求：GDF 不认识内部 HTTP，加工逻辑要能配进 GDF。现行 `12` / `15` 已改成两份可复制脚本加流程图，不再把飞书值班或 Java 任务接口当当前投递。
- `policy_industry_rel` 只有 `policy_id`，没有 `source_plane`。两平面 id 撞车时 C1 会混写。本叶不改表，写在 `12` / `13`，发现撞车先停。
- `13` 未连库，不是现网 as-built。空表核对在 `SYSINT-06-03-DDL-L01`，本叶不代替。
- 通用 `parse_workpack.py` 仍读不出政策字段行。本叶不出 CDC 预填。

## 修改内容

- 新建 `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/`。Wave A/B 从当日 v1.0.4 复制。09 只改版本指针，不改字段矩阵。
- 新写 `05`、`13`、`15`。`12` 写 C1 / C2 流程图和脚本路径。`scripts/` 两份 Python 供 GDF 复制到自己的节点。
- `派单包/README.md`：现行政策包改为 v2，v1 标历史。v1 README 只加替代指针。
- 工程过程 WBS / 技术方案：目录已落盘。06-03 仍是跑通叶，施工文件改指 v2 的 A/B，不执行 Wave C。

## 测试结果

- 定义叶，无跑数、无 CDC xlsx、无 lumen 业务仓 diff。
- 对照 DoD：目录含 00/01/02/03/04/05/06/09/10/11/12/13/15/CHANGELOG/README。
- 09 两张源表仍无行过滤，`is_history` 直接映射，UK 仍是 `(source_plane, policy_id)`。
- `15` 写明：两张平面 B 都 success 之后，在 GDF Python 节点上各跑一次脚本。不配置内部 HTTP。C 失败不回滚 B。
- 两份脚本 `--self-check` 均通过（不连库）。未在 GDF 节点上执行。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ C1/C2 是包内 Python。Java 不写对码或切条 |
| 在线调用链 | 本叶是 GDF 批处理，不是页面请求。用户 2026-10-26 改口径：GDF 配置这两份脚本，不配 `/internal/*`。在线 Java 门面未写成已接通 |
| 图谱 | ✅ 不写 Nebula，不改 `POLICY-STORAGE-FLOW` |
| 可观测 | 定义叶，无运行时埋点 |
| CI | `cicd: skip` |
| D12 | ✅ 目标库 `gkxlumenx_*`。不把 `demo_gkxlumenx_*` 当产线 |
| D9 / D8 / D10 | 本叶不出指标、不出页面 |
| D14 | ✅ 不写对象存储 |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 220000（本会话估算，不是控制台账单） |
| model_used | grok-4.7 |
| actual_cost | 1.2 |
| cost_warn | green |

## 签收

2026-10-26 用户要求完成并签收。原 DoD 写「调用链 GDF→Java→`/internal/*`、GDF 只触发」。同日用户改为：GDF 要能把加工逻辑配进自己的平台，交付两份 Python 和流程图。签收按后一口径。未在 GDF 上跑通，不把产线写成已接通。

## 遗留风险

- 脚本要由 GDF 配上库、向量和模型环境后才算接到产线。本叶没有执行结果。
- 应用在线若另有 Java 入口，不是 GDF 这两份作业，本叶也不把它写成已接通。
- ADS `policy_text_parse` 没有在本包给出冻结 DDL。缺表时不猜列。
- 并行会话已认领 `SYSINT-06-03-DDL-L01`。空表若按旧的 v1 `10/` 建，须带上 `is_history`；现行列快照在 v2 `10/`。

## CI/CD（必填）

- 分支：`dev`
- commit：签收提交含 v2 包、v1 的取数贯穿与同文脚本、派单包 README、本 handoff、WBS、技术方案。设计类无业务 CI。
- pipeline URL / ID：设计类，`cicd: skip`
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无

## 涉及文件

- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/`
- `agent-delivery/data/GDF/派单包/README.md`
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v1/README.md`（仅替代指针）
- `agent-delivery/agent-handoffs/政策模块-E7/GDF-POLICY-WORKPACK-V2-DISPATCH.md`
- `agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/WBS.md`
- `agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/技术方案.md`
