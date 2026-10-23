# KG-YANDA-SCHEMA-COMPARE-L01 · 燕大知识图谱平台 Schema 对比调研

> 任务来源：七链图谱构建专题会（2026-10-21）待办，来自 `human:淮政玮`：「将燕大知识图谱平台导出的 schema，与当前项目业务需求中定义的图谱 schema 进行逐项核对匹配」。派单对象 `human:唐绍祖`。
> 报告真源：[`agent-delivery/designs/亿集知识图谱/燕大图谱平台schema对比调研报告.md`](../designs/亿集知识图谱/燕大图谱平台schema对比调研报告.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:coordinator-agent`（调研执行）|
| supervised_by | `human:唐绍祖` |
| claim_type | `coordinator_dispatch` |
| 说明 | 会议纪要待办项 @唐绍祖；本 handoff 由 AI 代理起草，结论措辞待监管人复核 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类调研，不改业务代码） |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 不改我方调用链；仅调研报告提出「子图 API 参数对齐」等后续建议，未实施 |
| 会签态 | N/A |
| 说明 | 纯调研任务，不触碰 Java/Python 调用链与存储流图 |

## 问题清单（任务原文）

1. 阅读七链图谱构建专题会纪要，了解会议沟通情况
2. 用 playwright 等工具深度解读 `http://10.50.183.56:8093/schema`，重点是 Schema 管理页（含「查看脚本」内嵌内容）
3. 检查 `repos/` 中科技专题服务系统、科技信息展示系统的图谱功能代码，逐项核对 schema 差异
4. 对照需规（`bid-reference/` 三份文档）总结对方 schema 与功能设计中可借鉴项
5. 分析我方哪个系统/模块/功能可参考对方

## 修改内容（产物清单）

| 产物 | 路径 |
|------|------|
| 调研报告（279 行，7 章 + 附录） | `agent-delivery/designs/亿集知识图谱/燕大图谱平台schema对比调研报告.md` |
| 证据：46 份抽取脚本（溯源/置信度/VID 算法） | `agent-handoffs/evidence/KG-YANDA-SCHEMA-COMPARE-L01/scripts_entity/`（17）· `scripts_relation/`（29） |
| 证据：API 快照（Schema 全量导出/构建任务/总览） | `agent-handoffs/evidence/KG-YANDA-SCHEMA-COMPARE-L01/api_snapshots/`（6 件） |
| 证据：平台页面截图（16 页 + nGQL 控制台 + 图算法 Tab） | `agent-handoffs/evidence/KG-YANDA-SCHEMA-COMPARE-L01/screenshots/`（19 张） |

## 核心结论（详见报告）

1. **Schema 匹配度约 60%**：燕大 17 实体/33 关系覆盖论文、专利、项目、机构、人才、产业链；缺**政策、服务机构、技术链**三类需规要素（前两类我方 polan/svcgraph 已有，可反向输出）。
2. **最可借鉴**：①「DDL+脚本+运行状态」三位一体 Schema 元数据管理；② 10 字段溯源规约 + 动态置信度 + 人工审核闭环（需规「可信度评估入库」正要求此能力）；③ md5 归一化 VID（修复我方 `ind:{中文产业名}` vid 隐患）。
3. **9 个推理服务**（需规 SRS-07 逐条对应）：校友/同事/两点合作成果 3 个已 ready 可直调，其余 6 个 scaffold 需跟进或我方兜底。
4. **分工建议**：底层构建/治理复用燕大；图算法指标（我方 6+ 种 vs 燕大 3 种）与可视化前端我方主导。

## 测试结果

- 燕大平台 API 全部实测通过（`graph-console/query` 执行 nGQL、`graph-search/subgraph` 子图、`kg-construction/*` 服务元数据、`schema-management/*` 全量导出）。
- 无代码改动，无需回归。

## 遗留风险

- 燕大 `graph-console/query` 当前允许写入（仅禁 DDL），我方接入须申请只读账号并锁定图空间 `gkx_local_1`。
- 燕大 9 推理接口 7 个仍为 scaffold，排期依赖其团队；需规交付前以我方算法库能力兜底。
- 其数据源配置存在大量测试空间（60+ 数据源含脏配置），接入时须确认生产空间规划。

## CI/CD（必填）

- 分支：`origin/dev` 直推（编排仓规约，`00-team-constitution.mdc` §4.2）
- commit：见本条提交（`docs(kg): 燕大图谱平台 schema 对比调研报告与证据`）
- pipeline URL / ID：无业务 CI（纯文档）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A

## 可观测性（建议）

- N/A（纯文档任务）

## 涉及文件

- `agent-delivery/designs/亿集知识图谱/燕大图谱平台schema对比调研报告.md`
- `agent-delivery/agent-handoffs/evidence/KG-YANDA-SCHEMA-COMPARE-L01/**`（72 文件）
- 本地工作原件：`local-workspace/docs/tasks/investiage/20261023_燕大图谱平台schema对比/`（不入库）
