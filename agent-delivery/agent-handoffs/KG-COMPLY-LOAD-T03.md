# Handoff — KG-COMPLY-LOAD-T03

## 任务认领

监管人 `human:宋飞扬`，执行人 `agent:data-agent`。T03 认领与开工已通过任务 MCP 登记并推送 GitLab。2026-11-11 18:54:26（北京时间）完成本批写入及独立图库核验，提交待签收。

## 范围与实现

按唐绍祖新裁定与补充裁定 §7，T03 负责 person/research 主数据以及 M01、M04；M02 已在提交 `832923ec` 中移交 T02。代码明确拒绝以 T03 写入 M02。

指定图空间为 `demo_gkx_chain`，新边批号为 `comply-2026-11-11-t03`。开发机运行脚本，源数据只读连接外部 Doris `47.93.119.170:29030/gkx_technology_analysis_dev`，原始源表不在开发机。

实际结果：

- person 100,000、research 83,745 个点全部已有，逐 VID 核对后跳过，新增 0，保留已有属性。
- M01：源 5,051,578 行，取 ID 小侧一条，写入并独立实测 2,525,789 条 person→person cooperate；`match_method=coauthor`。
- M04：84,589 条工作经历排除 420 条 company 后，84,169 行合并成 72,099 条 person→research belong。保留岗位、经历段数和年份；按裁定生成在职投影。
- M03：202,795 行的 8,784 个机构全部为 company，端点不符，本期 0；M20 与 M01 同源重复，本期 0。
- enterprise→enterprise cooperate 存量仍为 94,824 条，独立计数，不混进 M01。

本批新边合计 2,597,888 条，含前置小批验证写入的 M01、M04 各 20 条。所有输入按固定键排序；M01 每页 50,000 行主键分页。图库采用条件插入、稳定 rank=0、SQLite 断点、每批精确回读；已完成的源文件与 journal 均可校验追溯。

## 偏离与数量修正

裁定和登记册的 M04 数量 72,503 为 company 排除前的唯一对数；实测 company 占 404 个唯一对，所以最终分母是 72,099。源 SQL、原始聚合结果、规则和解释均在交付目录。按裁定「最终数以执行器对账单为准」执行；T07 应使用本交付分母。

M02 执行归属以 §7 新变更为准，已从 T03 导出器、写入器和默认运行入口移除。M19 的同源重复处置归 T02 对账。共享机构 VID 保持 `inst:<institution_id>`，T02 可按该源字段与已存在的 research 点对接。

M01 的 weight 显式映射 collaboration_score，空值以 0 写入并保留原空值；M04 未定义数值强度，weight=0。M01 的查询与算法消费者需要按无向关系读取单条规范方向物理边。

## 产物清单

- `scripts/kg-comply-t03.py`
- `scripts/kg_comply_t03_source.py`
- `scripts/kg_comply_t03_graph.py`
- `scripts/kg-comply-t03-verify.py`
- 同目录 source、graph、verify 三个 selfcheck 脚本
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/对接文档/燕大/T03/README.md`
- 同目录 `full-result.json`、`verification.json`、`snapshot-metadata.json`、`source-audit.json`、`source-verification.sql`、`selfcheck-results.json`、`runtime-source.json`、小批结果及运行日志

入图源码 [576f1d68](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/gkx-orchestration/-/commit/576f1d6891522e60f3d9e686aec3c4101c1fac2d)，独立验收源码 [93aab9c4](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/gkx-orchestration/-/commit/93aab9c46fe6eac0376edec97f870093e64a279d)。运行文件摘要与 LF 规范化摘要均已对照 Git 源码确认。

开发机隔离执行目录为 `/home/zhangzhong_e43d4db3/qiliantupu/t03-runs/t03-20261111`。完整源快照及 SQLite 进度保留在该目录，不进入 Git 交付包。

## 验收证据

智谱开发机上 33 项回归全部通过（source 11、graph 17、verify 5）。真实小批验证通过后完成全量 5,565 批，全部逐键回读核对；缺端点、并发建入和遗留失败均为 0。

独立验证器重新查询真实图库：M01 与 M04 的总数、本批数、rank 和方向均正确；83,745 个 research 的机构类型与源画像全量一致；person 及两类边各固定 20 个跨文件样本的身份、字段、权重与批号一致。M04 样本覆盖在职／离职以及多段任职。

`verification.json.status=passed`；不以 completed journal 的旧计数代替真实图库验收。源文件 hash、行数、导出前后版本／计数／更新时间均一致。源库不提供跨表事务快照，此处证据为提取窗口前后元数据一致。

## 架构合规自检

- ✅ 源库仅只读查询，查询超时设置只作用于当前读取会话。
- ✅ 图库操作固定 `demo_gkx_chain`，无图结构 DDL。
- ✅ 原生 Nebula 条件插入保护已有点、边属性，不做覆盖降级。
- ✅ M01 单方向物理去重，M04 只工作经历并按唯一人才—机构对合并。
- ✅ 机构边排除 company、保留 unknown，机构点保留完整主数据规模。
- ✅ 固定批号与 rank、源快照摘要和 SQLite journal 支持审计与续跑。
- ✅ 每批全部新属性回读，独立验收按端点 Tag 与精确批次分组。
- ✅ 凭据只从进程环境或本机已配置凭据在内存使用，不进入源码或交付证据。

## Cost 回填

model_used：Codex GPT-6。当前会话没有提供真实计费的 actual_tokens、actual_cost，二者待平台账单回填，不填写推测值。cost_warn：yellow（计量缺失）。技术执行与独立验收证据已完整交付，任务签收由有权人员完成。
