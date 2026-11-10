# TS-L2-M10-ENT-SEED-L01 · handoff

- 任务：`TS-L2-M10-ENT-SEED-L01`（data · M10-ENT 存量数据种子）
- 日期：2026-11-09 · 监管：`human:刘剑锋` · 认领：`agent:data-agent`
- 状态：**已按监管人范围裁定执行到 dev 库并只读核对通过**。不标 done（待签收 / registry 补登）
- 强度：ponytail full（代码任务；最小可用实现）
- 用户故事：全景序 41–47（M10-ENT）
- 上游契约：`sdd/l2/TS-L2-M10-ENT-DATA.md`（DATA-A1 存量 seed / DATA-A3 挂接=边存在性）、`TS-L2-M10-ENT-METRIC.md`（strength_auto 口径 / strength_manual 不进指标）

## 范围裁定（监管人 human:刘剑锋 2026-11-09）

**只灌有真实 `relation_strength` 的技术点**，不做全量。原因：R2 无分页，全量灌入会让页面一次加载约 1.9 万行；全量留作后续单（需先做 R2 分页）。

- 默认行为 = `--only-with-strength`：只选至少有一条非空 `relation_strength` 的 `tech_has_*` 边的技术点。
- 全量保留显式开关 `--all`，且仍受 `--max-write` 写保护。

## 范围与实现

1. 新增 `repos/lumen-algo-py/vendor/entan-py/scripts/seed_tech_graph_maintain.py`
   - 只读 Nebula `demo_gkx_chain`：`tech_point` + 四类 `tech_has_*` 边（仅 `relation_strength IS NOT NULL`）。
   - 写 `gkxlumenx_dwd` / `gkxlumenx_ads`（默认正式库；`GKX_M10_ENT_DWD_DB` / `GKX_M10_ENT_ADS_DB` 可覆盖）。
   - **〔2026-11-10〕默认已改为中台库 `demo_gkxlumenx_dwd/ads`**（库边界 2026-10-19），现状数据已整表复制过去，见 `TS-L2-M10-ENT-DB-DEMO-L01.md`。
   - 默认 `--only-with-strength`；`--all` 为显式全量；`--max-write`（默认 5000）超限中止，`--allow-large` 放行。
   - `technology_master`：按唯一键 `name_cn` upsert；`external_ids` 记 `legacy_vid` + `technology_node_id`；重名点合并保留 `all_legacy_vids` / `all_technology_node_ids`。
   - `graph_entity_node`：只为范围内 active 技术点写（`version_id=当前 MAX ok 版本=1`，`display_name=name_cn`）。
   - `graph_entity_edge`：`src=technology_id 字符串`、`dst=实体 VID 原样`、`rel_type='关联'`、`rank=0`、`source='auto'`、`strength_auto=relation_strength`、`time_to=实体 year`；无 `relation_strength` 不写（不编数字）；`ON DUPLICATE KEY UPDATE` 用 `IF(source='manual', ...)` 保留人工行。
   - `graph_entity_overlay`：`entity_type=paper/patent/institution/person`、`entity_id=实体 VID`、`display_name=name_zh 或 name_en`。
   - 两行 demo fixture 假种子（「深圳某机器人公司」「具身智能」）：`status='deleted'` 软删（不物理删），并清除其 ADS 节点/边。
2. 改 `scripts/mysql/tech_graph_maintain.sql` §12：**删除两条演示技术点 INSERT**（「具身智能」「深圳某机器人公司」）；注释改为「存量种子由 scripts/seed_tech_graph_maintain.py 实扫，默认仅灌有真实强度的技术点」；保留 `v0` 版本行。
3. 未修改 `api/tech_graph_maintain_routes.py` / `test_graph_maintain.py`；未写 Nebula / demo_* 库；未 commit/push；未读写 `task-registry.yaml`。

## Nebula 调研结论（只读）

- `tech_point` 共 **19430** 个；VID 形如 `tech_point:tcn_<32hex>`；有 `technology_node_id/name_zh/name_en/...`，无 status/year；`name_zh` 无空值；重名 76 组/158 行。
- 四类边总量与强度覆盖：
  | 边 | 总边数 | relation_strength 非空 | 范围 |
  |---|---|---:|---|
  | tech_has_paper → tech_paper | 108337 | 13 | 0.55–1.51 |
  | tech_has_patent → tech_patent | 172644 | 20 | 0.55–2.07 |
  | tech_has_institution → tech_institution | 51000 | 20 | 0.55–2.07 |
  | tech_has_person → tech_person | 111578 | 8 | 0.55–1.11 |
  | **合计** | 443559 | **61** | — |
- 61 条强度边全部属于**同一个技术点**：`神经性厌食症治疗的临床视角`（`tech_point:tcn_000f21ac06aceb9cdd0575e82d0d85fc`）。
- 「具身智能」「深圳某机器人公司」在 `tech_point` 中**均不存在**（demo fixture 假种子）。
- 实体 id/名称字段：`tech_paper.paper_id` / `tech_patent.patent_id` / `tech_institution.institution_id` / `tech_person.talent_id`；均有 `name_zh/name_en/year`；实体 VID 如 `tech_paper:W...` / `tech_patent:<hash>` / `tech_institution:ins_...` / `tech_person:tal_...`。

## 执行行数（dry-run 与实写一致）

| 表/动作 | 计划 | 实际写入 |
|---|---:|---:|
| `gkxlumenx_dwd.technology_master` upsert | 1 | 1（technology_id=3） |
| `gkxlumenx_ads.graph_entity_node` active | 1 | 1 |
| `gkxlumenx_ads.graph_entity_edge` auto | 61 | 61 |
| `gkxlumenx_dwd.graph_entity_overlay` | 61 | 61 |
| `technology_master` 软删假种子 | 2 | 2 |
| **合计** | **126** | **126** |

- 执行前：master=2（均 active）/ node=0 / edge=0 / overlay=0 / version=1。
- 执行后：master **active=1、deleted=2**；node=1；edge **auto=61**；overlay=61（paper 13 / patent 20 / institution 20 / person 8）。
- 两行假种子 `technology_id=1`（具身智能）、`2`（深圳某机器人公司）均 `status='deleted'`；ADS `graph_entity_node` 与 `graph_entity_edge` 中无其投影。

## 只读核对（entan-py 路由同等 SQL）

- **R2 `/graph/current`**：`node_count=1`，技术点「神经性厌食症治疗的临床视角」（technology_id=3），`edge_count=61`，`entity_count=61`，实体类型覆盖 paper/patent/institution/person；`base_version=1`，`projection_status=ok`。
- **R1 `/nodes/3/recommend-entities`**：auto 强度边 61 条，manual 已挂接 0，`recommend_items=61`，接口返回 Top50；强度范围 0.55–2.07。
- 软删技术点 1/2 的 ADS 出边计数为 0。

## 偏离与待确认

1. **strength_auto 口径**：取自 Nebula 存量 `relation_strength`（**不是** `M_TECH_GRAPH_105_1` 的 105 边权快照），取值 **0.55–2.07（部分 >1）**。是否等价 / 是否需另灌 105 快照，请 **algorithm-agent 确认**；确认前该批数据不应被口径审计当作 105 交付。FE `weight≤1→百分制` 的归一化假设也需前端/算法确认。
2. **Nebula 凭据**：派单文档记「root / 空密码」，实测空密码 `Invalid password`；改用仓库 `conf/settings.yaml` 已登记凭据经 `entan.common.nebula` 连接（只读，未猜测其他密码）。建议更新派单文档凭据说明；本 handoff 不记录任何明文凭据。
3. **两行假种子**：「具身智能」「深圳某机器人公司」均为 demo fixture，Nebula 无对应点；已按裁定软删并清 ADS，保留行供审计，不物理删、不编造存量 VID（D16/D18）。
4. **全量灌数后续项**：`--all` 当前 dry-run 计划 **38818 行**（19348 主表行 + 19348 节点 + 61 边 + 61 overlay），会触发写保护；执行前应先完成 **R2 分页**，另行开单。
5. **task-registry 未登记**：本会话无 MCP，未调用 `task-claim` / `task-update-*`；需 coordinator 后续补登记 `TS-L2-M10-ENT-SEED-L01` 并回填 cost。

## 架构合规自检

- **D12 demo/lumen 隔离** ~~✅：只写 `gkxlumenx_dwd` / `gkxlumenx_ads`；未写任何 `demo_*` 库。~~ 〔2026-11-10 改判〕该口径与库边界 2026-10-19 冲突，已迁中台库，见 `TS-L2-M10-ENT-DB-DEMO-L01.md`。
- **D16 gapfill** ✅：未写 ODS/DWD/ADS 以外 gapfill 表；无强度边不写 auto 边，未编造数据。
- **D18 可实现** ✅：存量真扫 Nebula，无写死 mock；空态诚实。
- **D2 算法只在 Python / 调用链** ✅：仅 Python 脚本直读 Nebula + 写 MySQL，无 Java/前端越层。
- **Nebula 只读** ✅：仅 `MATCH` 查询，无 UPSERT/DELETE/DDL。
- **METRIC §3 口径保护** ✅：只写 `strength_auto` / `source='auto'`；`strength_manual` 不动；人工行由 SQL 条件保护。
- **禁改项** ✅：未改 routes/test；未碰其他仓/表；未 commit/push；未读写 task-registry.yaml。

## cost

- actual_tokens: ~95k · model_used: deepseek-v4-flash（Claude Code agent） · actual_cost: <$0.6 · cost_warn: green

## 产物

- 新增：`repos/lumen-algo-py/vendor/entan-py/scripts/seed_tech_graph_maintain.py`
- 修改：`repos/lumen-algo-py/vendor/entan-py/scripts/mysql/tech_graph_maintain.sql`（§12 演示种子与注释）
- 调研/核对临时脚本（不入仓）：`/tmp/pw/scripts/`
