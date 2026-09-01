# PLAN-S2-DATA-GAP-L01 · S2 三方源与指标数据缺口盘点

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:唐绍祖` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 经 `task-registry` MCP 认领（`task-claim`），状态 `claimed`；产出后推进 `done` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·盘点类，文档） |
| 说明 | 未压文档完整性；盘点级结论，字段级问答下沉 `DATA-SUPPLIER-Q-*` |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只新增编排仓 Markdown + 回填 project-plan.yaml，不缩代码 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改调用链/存储流图 |
| 会签态 | N/A |
| 说明 | 数据缺口盘点摘要，非 ARCH-IMPL |

## 范围与实现

- 产出「三方源符合度与缺口清单」定稿：`agent-delivery/data/third-party-source/三方源符合度与缺口清单.md`
- 内容合成自：全要素库差异摘要（2026-08-31 15:59）、供应方落库进度（07-31）、工作面 `SOURCE-TABLES.md`、指标字段缺口 sidecar（`source-gap-index.yaml`）、算法库差集（`TOPIC-ALGO-GAP-L01` Round 17 / `DS-ALGO-GAP-L01` Round 18）。
- 回填 `project-plan.yaml` N-S2-01：deliverables 的 `pending` 改为 `gap_catalog`（清单路径），节点 `status` `upcoming → done`。

## 修改内容 / 产物清单

- 新增：`agent-delivery/data/third-party-source/三方源符合度与缺口清单.md`
- 修改：`agent-delivery/project-plan.yaml`（N-S2-01 deliverables 回填 + 节点 status）
- 修改：`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/PLAN-S2-DATA-GAP-L01.md`（本 handoff）

未改：seed / 矩阵 / D3 枚举、`source-gap-index.yaml`、各域 `*-SUPPLIER-QUESTIONS.md`、进度导出脚本（属 `DATA-SUPPLIER-Q-*` 各叶，非本叶）。

## 测试结果

- 清单引用路径逐条核对存在（差异摘要 / 行数报告 / SUPPLIER-LOAD-PROGRESS / SOURCE-TABLES / source-gap-index / TOPIC-ALGO-GAP / DS-ALGO-GAP）。
- `project-plan.yaml` 语法未破坏（仅改 N-S2-01 两个字段值；无结构性变更）。

## 问题清单

- 三个子项中「多余算法列表」收集人仍 `TBD-02`（PM 还是各 Lead 未拍板），未闭合——已在清单 §3.2 记为 ⚠️ 未定，待 `human:郭万迎` 拍板后回填。
- 子项「展示指标梳理」归 `human:王惠`（LT-1-DRAFT，09-05），本叶只记录、不代做。

## 遗留风险

- 海洋 / 量子 / 外文论文 / 行业分析四域整批缺表，贴源无法覆盖（供应方核验中，不阻塞主路径 S3）。
- 高校 / 破产当事人业务行归零待供应方确认（软删 / 换批）。
- 算法库 missing ≈ 77 + 语义欠账 358，A1 需规/指标叶 ID 未交（`a1_tables_ready=false`），待注册时回填。

## CI/CD（必填）

- 分支：`dev`（编排仓）
- commit：待 PM 确认后提交（本 handoff 时尚未 commit）
- pipeline URL / ID：文档叶，无业务镜像
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId（dev 抽样）：N/A
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/data/third-party-source/三方源符合度与缺口清单.md`
- `agent-delivery/project-plan.yaml`
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/PLAN-S2-DATA-GAP-L01.md`

## 验收对照 DoD

| DoD（登记表原文） | 本波 |
|---|---|
| 三方源符合度与缺口清单可对外沟通风险/进度 | ✅ 清单 §0 总判定 + §4 风险与进度，可对外 |
| 子项：专题算法库缺口（唐绍祖 08-24）、多余算法列表交唐绍祖（收集人 TBD-02）、展示指标梳理（责任人 TBD-01 08-25）均有记录 | ✅ 清单 §3.1 / §3.2 / §3.3；TBD-02 记为未定、王惠子项记录待 09-05 |
| 清单路径回填 project-plan.yaml N-S2-01 | ✅ deliverables `pending → gap_catalog`，节点 `status done` |
| handoff 主责 human:唐绍祖；整体出门 2026-08-26 | ✅ 本 handoff；盘点已出门（快照 09-01） |

## 下一步

1. `human:淮政玮`（监管）收本 handoff；`human:郭万迎`（PM）确认 TBD-02 多余算法收集人。
2. 字段级缺口由 `DATA-SUPPLIER-Q-*` 域切片叶继续（企业 / 综合 / 产业链 / 服务机构 / 政策 / 机构·人才·技术）。
3. 王惠 LT-1-DRAFT 09-05 指标初稿出齐后回填「指标缺项」。
