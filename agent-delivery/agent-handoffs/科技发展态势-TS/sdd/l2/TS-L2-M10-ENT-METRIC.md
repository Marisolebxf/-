# TS-L2-M10-ENT-METRIC · 维护管理 · 关键实体与关系 · 后台指标设计

- 任务：`TS-L2-M10-ENT-METRIC`
- 日期：2026-11-07
- 状态：四角色会签完成（ALGO 同意；API/DATA/ARCH 条件已回填），**待监管人签收**。不标 done
- 监管：`human:刘剑锋` · 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：全景序 41–47
- 上游：`sdd/l2/TS-L2-M10-ENT-ARCH.md`（done）· 会签输入：`会签/TS-L2-M10-ENT-SIGNOFF-ALGO.md`（8 行预期挂接表——本叶按其落笔，不照抄全 N/A）
- 查询：未见 metric MCP。`M_TECH_GRAPH_105_1` 身份转述 A03（2026-10-18 metric-get）与 calc-logic 文档；落笔前需确认公式签署状态（前置注记见会签）

本叶只写 M10-ENT 的指标挂接。SRS 序号 **41–47**（+跨叶 SRS-40 版本面）。不新注册，不改 D4，不写假公式。

## 1. 预期挂接表（ALGO 会签 §6 逐行落地）

| 叶 | A03 卡 | 挂接 | 说明 |
|---|---|---|---|
| 41 | INT-A-X-213 | **`M_TECH_GRAPH_105_1`**（ⓘ 必须；D4=mock 显示 MockBadge） | 需规 L378「算法自动计算并**展示**…关联强度」——展示数字，D9 适用。禁止「全 N/A」表述（ALGO-S1） |
| 42 | 215/216 | 无新号；回执 edges_created[].strength 若显示→同挂 105_1 | G2 现算不做（无 105 边对强度空；「无」vs 人工填=产品口径在册 JX-A03-03） |
| 43 | 217/202 | 写操作 N/A；**impact 计数并入 DN-A03-09 豁免** | A03 202 未标 metric_missing——缝隙由本叶收口（§2） |
| 44 | 218 | N/A（n/a_ops） | |
| 45 | 219 | N/A（表单字段；importance_level 非算法分） | |
| 46 | 220 | N/A；**strength_manual 不进 M_TECH_* 口径**（§3 保护条款） | |
| 47 | 221 | metric_missing：回执统计豁免待 DN-A03-09；validate dry_run 计数同入 | |
| 跨叶 SRS-40 | 209 | 版本 stats 若展示→并入 DN-A03-09 | |

## 2. DN-A03-09 豁免裁定建议（一次性写全）

本叶建议 DN-A03-09 裁定为「**操作回执类计数豁免 D9 ⓘ**」，范围一次写全（援引 LAYER probe 时延先例：不落指标事实表、无聚合口径、无更新频率）：

- 221 批量回执统计（succeeded/failed/skipped）
- 202 impact 预检计数（edge_count/entity_link_count/snapshot_refs）
- 209 版本 stats（+node/-node/+edge/-edge）
- 47 validate dry_run 预览 diff 计数

裁定待 **PM/数据 Lead** 确认后回填本表（A03 L1091 在册 owner——三分册会签 ALGO-N2 补全）；未裁前按「建议豁免」表述，不挂 ⓘ 不注册。

## 3. 口径保护条款（本叶写死，实现必须遵守）

1. **M_TECH_*_STRENGTH 系列 = auto 层（105/边权）口径**；`strength_manual` 是编辑层字段，**永不进指标公式**（A03 204/220/R-A03-08 三处警示的收口）。
2. 实现对齐：边属性双字段+source 标记（API 册 DTO 已落 strength_auto/strength_manual/source）；读面指标计算只取 auto；UI 显人工值时标注「人工」。
3. 序 46 表单可回显人工值；读面 Top5/边权排序仍按 auto。

## 4. 前置注记（落笔待办）

- `M_TECH_GRAPH_105_1`：calc-logic 实存（`metrics/calc-logic/TECH/M_TECH_GRAPH_105_1.md`，维护者唐绍祖，20261027 批，更新频率 pending）；A03 记 formula 未签（pending_cosign）、source_tables=pending_ods（2026-10-18 MCP）——**METRIC 签收前应确认公式签署状态有否更新**（无 MCP 本叶无法在线复核，稿头已声明）。
- A03 213/216 记 `M_TECH_ENTITY_TOP5` 与 DS 映射挂 105_1 不一致——沿 105_1 时同步销歧（报 data-agent 正式化）。
- 105 未交付期：叶 41 空态+PendingBadge（ARCH-C5），不灌 mock 充数。

## 5. 不做

- 不新注册任何 metric_id（G2 后续现算输出也归 105_1 口径，无需预留）
- 不改 D4/生命周期；不写假公式
- 不把 strength_manual/计数类塞进指标体系
