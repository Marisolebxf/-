# Handoff — KG-COMPLY-LOAD-T08

## 任务认领

任务为 T08 图算法作业路径搜索批，执行人为 `agent:algorithm-agent`，监管人为 `human:宋飞扬`。开工登记已通过任务 MCP 提交 GitLab。按 SDD §5 的并行说明，在技术点层执行离线只读作业。

## 范围与实现

复用 11 月 7 日基线的 10 对技术点，在验收空间读取 19,430 点、541,428 边并保存有序快照。Python 使用 NetworkX 运行 BFS、倒数置信度代价的 Dijkstra 和每对 5 条无权简单备选路径。

读取字段为 `e.relation_confidence_score`。空值率为 0，10 对均可达，6 对取得严格代价改进。10 对当前加权与无权跳数一致。脚本、结果和 12 项回归均已完成。

## 产物清单

- `scripts/kg-comply-paths.py`
- `scripts/kg-comply-paths-selfcheck.py`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/燕大/T08/README.md`
- 同目录 `result.json`、`snapshot-metadata.json`、`verification.json`、`export.log`

最终执行源码提交为 [1e477587](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/gkx-orchestration/-/commit/1e477587c3fc2e893ab3eba35b9874f362ef2c58)。开发机目录为 `/home/zhangzhong_e43d4db3/qiliantupu/t08-runs/t08-20261111-ueacfwc4`，图快照保留在该目录。

## 验收证据

12 项离线回归在本机与智谱开发机均通过。实际读取的节点与边数量对齐历史规模，权重为空、非法权重、缺端点、自环和重复端点对均为 0。

独立快照复核检查了全部 10 对路径端点、边有效性、BFS 最短跳数、Dijkstra 最小代价和 50 条简单备选路径，结果为通过。证据在 `verification.json`。

## 偏离与待确认

本次明确采用 `cost = 1 / confidence`。旧材料没有发布转换公式，旧 JSON 未保存加权路径序列或总代价，因此公式一致性待唐绍祖确认。本批的第 2、7、9 对 Dijkstra 跳数与旧 JSON 不同，BFS 跳数全部一致。原 Markdown 声称 4 对加权跳数不同，其 JSON 实际是 3 对。

脚本自动质量检查通过，算法口径及任务签收交负责人确认。

ponytail 工具在本会话未提供，本次采用 12 项回归、真实图复跑和独立路径复核完成验证，执行过程如上。

## CI 与开发机验证

代码已在智谱开发机使用 Python 3.10、NetworkX 3.4.2 和 nebula3-python 3.8.3 实跑。源码提交和实际运行版本见结果 JSON。本批交付为离线脚本及证据，CI 状态按 GitLab 实际运行记录核查。

## 架构合规自检

- ✅ 算法实现为 Python 与 NetworkX。
- ✅ 数据来自指定的 `demo_gkx_chain` 技术点层。
- ✅ 图库语句为 USE 和 MATCH，任务执行形态为只读。
- ✅ 权重字段按本引擎约定读取，全部导出边已检查空值和非法值。
- ✅ 连接凭据来自进程环境，交付代码和证据只包含变量名。
- ✅ 空态、缺端点和非法权重分支有明确结果并通过回归。
- ✅ 快照摘要、固定 VID 点对、源码提交和结果摘要可复核。

## Cost 回填

model_used 为 Codex GPT-6。当前运行环境未提供模型会话的实际 token 和计费金额，actual_tokens 与 actual_cost 待平台账单回填；cost_warn 为 yellow，原因是计量缺失。
