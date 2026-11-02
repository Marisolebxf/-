# KG-7ELEM-LOAD-PATH-L04 · 政策上图路径

> 定义文档。只回答总控第 3 节三问。未改业务仓，未执行 nGQL，未连图库。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务调研叶。停在 integration。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。三问都保留，没有用 YAGNI 删类。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶要求读代码和已签收必须边，不用压缩代替阅读。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本叶不改图。 |
| 图 diff | 无。 |
| 会签态 | 无本叶图。引用的 L03 图 frontmatter 为 `draft`，不在本叶改签。 |
| 说明 | 未改 `KG-7ELEM-MUST-EDGES`，未改 POLICY 存储流图。 |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md |
| 范围边界 | KG-7ELEM-LOAD 总控 §3、总派单 L04 行 |

## 问题清单

- 问 1：2 条。待确认 0。
- 问 2：5 条。待确认 5（M11 表名；M12、M13、M14、M10 的稳定 ID 列或表名）。
- 问 3：4 条。待确认 0。
- 三问合计 11 条。待确认合计 5 条。
- 燕大有可执行写图或读图、我方没有：0 条。
- 燕大 Schema 种子另有 3 个关系名，无抽取脚本，不计入已实现，也不计入上一行。
- 向量或语义相似：未实现。M16 在 `mode=llm` 下抽出 `cite_pids` 已实现，那是大模型，不是向量。

## 修改内容

- 新增 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L04-政策.md`
- 新增示例 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L04/policy_relate_core_example.py`（未执行，不当成已实现）
- 我方入口写在 `repos/demo-algo-ent-analysis` 的 `api/policy_routes.py`、`polan/graph/ops.py`、`polan/graph/nebula_loader.py`。`lumen-algo-py` 服务代码没有政策写图。

## 测试结果

- 未执行示例脚本，未执行 nGQL，未连图库，未连 Doris。
- 入口路径在 `demo-algo-ent-analysis` 与 `yanda/tech-kg-api` 中按文件打开核对。

## 遗留风险

- `pedigree` 多数是引用原文，规则 `cite` 只能上 `上位政策:{pid}` 且 pid 在本批的行。
- `policy_relate`、`policy_apply_to`、`publish` 缺稳定 ID 列，表名或列名待确认。
- 未签收 L03 台账仍写政策无写图，与现行 demo 代码不一致。本叶以代码为准，未改那份台账。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`（文件在工作区，未 commit）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无。定义文档。

## 可观测性（建议）

- OTEL_SERVICE_NAME：无本叶发布
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L04-政策.md`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L04/policy_relate_core_example.py`
- `agent-delivery/agent-handoffs/KG-7ELEM-LOAD-PATH-L04.md`

## 架构合规自检

- D1 算法在 Python：本叶只记录 demo Python 写图。Java `PolicyGraphController` 只透传。✅
- D2 调用链：写图在 Python；Java 不直连 nGQL。✅
- D3 图谱协议：代码目标空间 `demo_gkx_chain`，本叶未执行、未改空间。✅
- D12：入口在 demo 算法仓，未把 demo 写成 lumen 放行，未把燕大写成生产。✅
- 未改已签收建图正文、初始化脚本、storage、SYSINT-SCHEME-07-L06、业务仓。✅
