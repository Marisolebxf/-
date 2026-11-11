# T03 人才与机构入图交付

执行人：宋飞扬；执行任务：`KG-COMPLY-LOAD-T03`。图空间固定为 `demo_gkx_chain`，新边批号固定为 `comply-2026-11-11-t03`。

## 实际交付结果

2026-11-11 18:54:26（北京时间）完成真实图库独立验收，`verification.json.status=passed`。

| 项 | 应有／应入 | 图中实测 | 本次处理 |
|---|---:|---:|---|
| person | 100,000 | 100,000 | 逐 VID 核对，全为已有点，新增 0 |
| research | 83,745 | 83,745 | 逐 VID 核对，全为已有点，新增 0；机构类型全量一致 |
| M01 | 2,525,789 | 2,525,789 | 均带本批号；rank 非 0、非规范方向均为 0 |
| M04 | 72,099 | 72,099 | 均带本批号；rank 非 0 为 0 |
| M03 / M20 | 0 / 0 | 0 / 0 | 留空原因见下 |
| M22 存量企业合作 | 94,824 | 94,824 | 按 enterprise→enterprise 单独核对 |

本批新建关系共 **2,597,888 条**。M01、M04 的各 20 条小批验证边已计入该总数，全量执行时精确核对后跳过。`full-result.json` 中的 `new_verified` 因此分别为 2,525,769 和 72,079；不能把前置验证边再加进最终图库总数。

全部 5,565 个全量批次验证完成，无缺端点、并发抢先建入或遗留失败批次。独立验收重新核对了全量机构类型，并对人才、M01、M04 各取跨文件首尾的固定 20 个样本；所有新边属性此前已在写入阶段逐键完整回读。

## 执行依据与边界

以《KG-COMPLY-LOAD-T03-裁定-人才与机构四条关系》§3、§4、§7 为准。§7 对应 GitLab 提交 `832923ec12a206651850a10f23a12e0735a22cb3`，已将 M02 移交 T02／陈芸飞。本交付的执行器明确拒绝 M02，不访问机构合作年表。

| 项 | 源表 | 本期映射与应入图数量 |
|---|---|---|
| person | ads_talent_profile | 全量 100,000；VID `person:<talent_id>` |
| research | ads_institution_profile | 全量 83,745，含 15,392 个 company；VID `inst:<institution_id>` |
| M01 | ads_talent_collaborator | 5,051,578 行，取 `talent_id < collaborator_talent_id` 一侧，2,525,789 条 `person → person cooperate` |
| M04 | ads_talent_experience | 84,589 条工作经历，排除 company 的 420 行，同人同机构合并，72,099 条 `person → research belong` |
| M03 | ads_talent_institution_cooperation | 202,795 行均为人才—企业，端点类型不符，记 0 |
| M20 | 与 M01 同源 | `talent_coop` 记 0，避免同证据双灌 |
| M02 / M19 | 移交 T02 | M02 由 T02 执行；M19 同源重复留空，本批不写 |

M04 的 72,503 是排除 company **之前**的唯一对数，涉及 company 的唯一对数为 404，故正确分母为 `72,503 - 404 = 72,099`。这也与 `84,589 - 420 = 84,169` 条有效工作经历分组的结果一致。裁定明确「最终数以执行器对账单为准」，本交付保留原规则，修正对账分母。

## 映射与保护

M01 和 M04 均使用 rank=0，每对只写一条物理边。M01 保留合著论文数、共同专利数、合作起止年及 collaboration_score，`match_method=coauthor`；下游查询和算法须按无向关系消费 M01，不能只从物理起点向外遍历。M04 合并全部有效工作段，保留 `stint_count`、经历 ID、岗位列表、首个起始年、最后一个非空终止年，以及源 `is_current` 的值分布。M04 在职投影按裁定取 `ANY(end_year IS NULL OR end_year >= 2026)`，不按源 `is_current` 筛选。

`research` 全量保留企业画像，但 M04 的机构端点按源画像类型排除 company，unknown 按裁定保留。每条新边均保留批号、源表和稳定源事实键，M04 另保留机构类型。

权重是执行器的显式映射：M01 用 `collaboration_score`，空值以 0 写 weight、原空值保留在 props；M04 未指定数值强度，weight=0。两个字段的数值不代表相同量纲。

图库已有 person/research 点由 T04 批次先建入。T03 按具体 Tag 和 VID 逐项核对并跳过，保留已有 name/props，不把这些点计作 T03 新增。独立验收进一步校验 research 的机构类型与源画像一致。存量 enterprise→enterprise cooperate 属 M22，独立计数，不混进 M01。

## 运行与恢复

执行代码：

- `scripts/kg-comply-t03.py`
- `scripts/kg_comply_t03_source.py`
- `scripts/kg_comply_t03_graph.py`
- `scripts/kg-comply-t03-verify.py`

源连接凭据通过 `GKX_SOURCE_USER` / `GKX_SOURCE_PASSWORD` 注入，图凭据通过 `GKX_GRAPH_USER` / `GKX_GRAPH_PASSWORD` 注入，不进入源码或证据。源库使用只读连接，源端 SQL 证据见 `source-audit.json`。`SET query_timeout=3600` 仅作用于当前源读取会话。

```bash
python3 scripts/kg-comply-t03.py snapshot --run-dir /absolute/run-dir
python3 scripts/kg-comply-t03.py apply --run-dir /absolute/run-dir --canary --batch-size 500
python3 scripts/kg-comply-t03.py apply --run-dir /absolute/run-dir --batch-size 500
python3 scripts/kg-comply-t03-verify.py --run-dir /absolute/run-dir
```

源快照按主键排序导出，M01 每页 50,000 行，使用最后一对主键续读，不使用 OFFSET。源表计数、版本及更新时间在导出前后核对；所有文件完成后才原子发布 manifest。源库不提供跨表事务快照，此处证明的是提取窗口内前后元数据一致。

写图采用 `INSERT ... IF NOT EXISTS`，已有数据跳过；不支持条件写入时停止，不降级为覆盖插入。SQLite journal 在写前保存原状态，写后逐键回读并核对全部新属性，验证成功才推进。故障恢复须保留同一快照、批号、目标、journal 和 batch-size，重跑原命令。源文件 hash 或配置改变会拒绝续跑；缺端点时停止，修复后可用原 journal 继续。

完成的 journal 重跑只读取已验进度，不能代替独立验收。最后一条 verify 命令重新查询真实图库，不修改图数据。

## 验证与产物

源模块 11 项、写图模块 17 项、独立验收模块 5 项回归，共 33 项，均已在智谱开发机通过。覆盖镜像去重、工作段聚合、企业过滤、源变更、条件插入、部分写入、崩溃恢复、并发点保留、缺端点修复、旧企业边保护，以及错误数量／属性／快照对验收的阻断。对应自检脚本在 scripts 目录，结果见 `selfcheck-results.json`。

真实写入结果以 `full-result.json`、独立验收以 `verification.json` 为准。`snapshot-metadata.json` 保存源版本、实际应入图条数、快照摘要及映射规则；`runtime-source.json` 绑定执行源码。完整原始快照与 SQLite 进度保留在智谱开发机的隔离执行目录，不提交 Git。

入图源码提交为 [576f1d68](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/gkx-orchestration/-/commit/576f1d6891522e60f3d9e686aec3c4101c1fac2d)，独立验收源码提交为 [93aab9c4](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/gkx-orchestration/-/commit/93aab9c46fe6eac0376edec97f870093e64a279d)。`runtime-source.json` 同时记录实际文件摘要和 LF 规范化摘要，对照 Git 源码时使用后者。

执行目录：`/home/zhangzhong_e43d4db3/qiliantupu/t03-runs/t03-20261111`。

技术实现与实际对账通过后提交待签收，任务签收由有权人员完成。
