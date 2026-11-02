# KG-7ELEM-LOAD-PATH-L06 · 七要素上图路径·科研机构、人才、技术

> 定义文档。必须边只认已签收 L03，schema 只认已签收 L05。未签收。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 本叶停在 integration。不标 done |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义/文档） |
| 说明 | 派单强度为 N/A。没有用缩写删掉三问里的任何一类 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶要求精读已签收必须边、demo 写图代码、燕大代码和久新材料，不用压缩代替阅读 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `KG-7ELEM-MUST-EDGES`（本叶不改图） |
| 图 diff | 无。不增删必须边，不改 L03 正文 |
| 会签态 | 只抄 L03 frontmatter：`draft` |
| 说明 | 本叶是上图路径说明，不是建图正文 |

## 问题清单

- 第 1 问 2 条：M06 专利→论文，M09 人才→专利。只是久新键对得上。我方第 1 问是 0 条。
- 第 2 问 9 条：M03，M05，M06 论文→论文，M06 专利→专利，M07，M09 人才→论文，M10 科研机构端，M13 人才端，M14 科研机构端。
- 第 3 问 0 条。无示例脚本。
- 待确认 6 条：M01、M20（同一张人才合作表），M02、M19（同一张机构合作年表），M04（隶属），M08（17426 行项目角色；资助论文署名不能当参与）。
- 燕大有写边代码、我方没有该必须边写图入口：7 条（M01、M04、M06、M07、M08、M09、M20）。M01 与 M20 是同一份合著脚本，未覆盖合作全量。
- 久新现库能对上字段、但我方没有写图代码：2 条（与第 1 问相同）。待确认的 6 条不计入。
- 探查日期 2026-10-30。只读探查连上。快照日是 2026-10-22。两套不一致处写在正文第 8 节。

## 修改内容

- 新增 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L06-科研人才技术.md`。
- 我方写图只对照 `demo-algo-ent-analysis`、`demo-algo-science` 的当前代码。两个仓都没有论文、专利、项目写图。`nebula_loader.py` 只写企业点；`research_coop`、`talent_coop` 出现在企业挂边里，起点是企业，对不上 M19、M20。`technology` 是技术点。
- 燕大只对照 `yanda/tech-kg-api`。已实现以 `relation_extractors_one_relation` 的写边脚本为准。边名目录里没有脚本的不算已实现。
- 久新 `ads_*` 不写成我方 ADS。`company` 不并进科研机构。未把相似度、人名分析表或示例写成已实现。
- 未改派单说明、已签收建图正文、初始化脚本、storage、未签收方案、业务仓。未执行 nGQL，未连图库，未写久新库。

## 测试结果

- 无业务代码改动，无单测。
- 久新只读探查在 2026-10-30 连上。使用 `SHOW`、`COUNT`、分组和最多 200 行的键抽样。`information_schema.tables` 无权限，改用 `SHOW TABLES`。
- 人才画像的出生年、电话、邮箱只在正文保留字段名，探查未选取这三列的值。
- 第 3 问没有脚本，因此没有脚本执行记录。

## 遗留风险

- 科研机构类型集合未定。只滤 `company` 会把医院、政府、资助方、未知类型留在机构端。M02、M04、M08、M19 因此停在待确认。
- M01 与 M20、M02 与 M19 各共用一张合作表。L03 禁止并进，本叶没有替它们选边。
- 现库有 23 张 `ads_patent_analysis_*` 和一张机构子领域合作年表，5.11.0 快照与我方清单都未列。其中机构共有专利边与年度表「专利覆盖不可用」不一致。未拿它们填必须边。
- 我方 Tag/Edge 仍是 L05 的「存储设计未写」。即便久新键对得上，也不能按已签收 schema 写入。
- 成本是粗估，见下。无 Console 的输入/输出分离计数。

## CI/CD（必填）

- 分支：`dev`（文档未提交）
- commit：无
- pipeline URL / ID：无。本叶不改业务仓
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无

## 可观测性（建议）

- OTEL_SERVICE_NAME：无。本叶不改服务
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L06-科研人才技术.md`
- `agent-delivery/agent-handoffs/KG-7ELEM-LOAD-PATH-L06.md`

## 架构合规

- 调用链、Nebula、Java 不做 NLP：本叶不写代码，不连图库，不把推理写成 Java。
- D12：不改 lumen 调用。我方入口按 demo 仓代码核对，没有把 demo 服务写成 lumen 依赖。
- D16：加工建议只点到我方 DWD/ADS 或 `gapfill_` 前缀，未建表、未灌数，未写 ODS 或供应方库。
- 成本粗估：`actual_tokens=280000`，`model_used=grok-4.7`。价表无该模型。按预算说明 B 档（输入 3 美元/百万、输出 15 美元/百万）和读多写少 90/10 套算，`actual_cost=1.18`，`cost_warn=green`。这是量级，不是 Console 账单。

ponytail: N/A（定义/文档）
