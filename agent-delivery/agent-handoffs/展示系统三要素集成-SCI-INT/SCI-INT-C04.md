# SCI-INT-C04 图谱数据集成 · handoff

- 作者：agent:data-agent（只读分析叶）
- ponytail: N/A（分析叶）
- 产物：`产物/SCI-INT-C04.yaml`；自检 `产物/_work/C04-check.py`
- 未连 Nebula / 任何库；现状全部取自仓内快照与代码（evidence 见 yaml `evidence_index` E01–E12）

## 1. 范围与实现

对照 TRSGraph 中三要素（TAL/TECH/ORG）需要的 tag/edge 和现状。覆盖四张图：技术点图谱、关键路径、人才关系链、科研合作链。需求来源是 SRS 科学技术全景 rows 21–50（含 A03 维护 rows 37–50），以及 重点科技人才画像 rows 280–307（A14）。

| 卡 | 类 | 名称 | VID | 现状 |
|---|---|---|---|---|
| INT-C-TECH-300 | TAG | technology | `tech:{technology_id}` | 缺失（只有旧 entan 有，且用名称作 VID） |
| INT-C-TAL-310 | TAG | talent | `talent:{scholar_id}` | 缺失（只有旧 entan 有，且用名称作 VID） |
| INT-C-ORG-320 | TAG | institution | `inst:{org_uid}` | 已有，需 ALTER 加属性；新库计数 0 |
| INT-C-X-330 | TAG | enterprise | `ent:{org_id}` | 已有，只 FETCH；新库计数 0 |
| INT-C-TECH-340 | EDGE | tech_relation（技术→技术） | — | 缺失 |
| INT-C-TECH-341 | EDGE | produces（实体→技术） | — | ENT 已设计、未建 |
| INT-C-TAL-350 | EDGE | talent_coop（人才↔人才） | — | ENT 已设计（ent→talent）、未建 |
| INT-C-TAL-351 | EDGE | work_at（人才→机构/企业） | — | 缺失 |
| INT-C-TAL-352 | EDGE | educated_at（人才→机构） | — | 缺失 |
| INT-C-ORG-360 | EDGE | research_coop（机构↔机构 / 企业→机构） | — | ENT 已设计（ent→inst）、未建 |

各图需要的 tag/edge：
- 关键路径：在 `tech_relation` 子图上算中心性，结果经 ADS 投影，再按 `technology.is_key_node` 回显，不另建边。
- 人才流动：用 `work_at` 的时间序列表示，不另建流动边。

- **space 方案**：沿用一张 G，三要素 Tag/Edge 只在已有的 `demo_gkx_chain` 里用 `IF NOT EXISTS` 追加；vid 用 FIXED_STRING(80)。禁止 entan / demo_entan / 新三要素 space。正式库 `gkx_chain` 尚未建，待李伟拍板（DN-C04-01）。
- **灌入链路**：先 ADS 再投影。
  - C01–C03 的主数据和关系表落 ADS 后，由 lumen-algo-py 新增的三要素投影 Job 作为唯一写者写入 Nebula。
  - 首次全量，之后按水位增量（weekly，待确认）；A03/A14 保存时按事件触发增量；删除走 tombstone。
  - 图算法 Job（IP-05）读 Nebula，结果投影回 ADS。
  - Java 只读 ADS，子图走 Feign → `/internal/graph/*`。
  - lumen-etl-es-py、Java、久新都不写 Nebula。
- **写回冲突**：共 5 条（WB-C04-01…05）。结论是 A03/A14 都不得直写 Nebula：
  - 写回落 ADS 人工层（字段级 override、tombstone、版本日志），再由唯一写者重投。
  - 人工与自动抽取冲突时的优先级、版本粒度、A14「实时更新」口径都待人定。

## 2. 偏离

- A03 产物 yaml 不存在，A14 也未开始，所以写回需求直接读 SRS，页面卡 int_id 写在 `page_cards_unknown` 里；A01/A02 已有的页面卡（INT-A-*）已挂接。
- B01 中「涉图指标」没有现成字段，按规则现算：`pattern=IP-05` 或 `jiuxin_row_id ∈ {SRS-104,105,110,111,114,115,130,131,153,157,160}`（图库叶、图链模型及其 IP-09 派生）。规则写在 yaml 的 `graph_metric_coverage.rule`。
- 机构 VID 取 `inst:`，没有沿用 C03 草案的 `org:`（CF-C04-01），需回 C03 修订。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-C04.yaml`：10 张卡，以及 space_plan、load_pipeline、write_back_conflicts、graph_metric_coverage、conflicts、decision_needed、risks、open_items
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/C04-check.py`
- 本文件

## 4. 验收证据

`python 产物/_work/C04-check.py` 实际输出：

```
OK cards=10 gap=0 by_kind={'TAG': 4, 'EDGE': 6} by_status={'missing': 5, 'existing_alter': 1, 'existing': 1, 'planned_not_built': 3}
OK graph metrics (B01 rule) scope=23 covered=23 diff=0
OK structure_escalation=9 write_back_conflicts=5 conflicts=6 open_items=8
```

脚本断言的内容：
- int_id 落在 300–399 且不重复；scope = card = 10，gap 为 0。
- 图指标集合由 B01 现算，与 coverage 双向差集为 0；每张卡的 metric_ids 与 coverage 反推结果一致。
- source_cards ⊆ C01–C03 卡；page_cards ⊆ A01/A02 卡；久新行 ⊆ P00，且每张带久新行的卡的 gaps 里都有「待确认」。
- 结构变更的卡全部 `structure_escalation: true`；VID 规则不含名称。

自检第一次运行时发现 INT-C-TAL-352 漏标「待确认」，已补上。

**只读 nGQL（供人执行核实，本叶未执行）**：

```ngql
SHOW SPACES;
SHOW CREATE SPACE demo_gkx_chain;          -- 核 vid_type = FIXED_STRING(80)
USE demo_gkx_chain; SHOW TAGS; SHOW EDGES;
DESCRIBE TAG institution; DESCRIBE TAG enterprise; DESCRIBE EDGE participates;
SUBMIT JOB STATS;                           -- SHOW JOBS 完成后
SHOW STATS;
-- 旧 graphd 若仍可达，仅对照 as-built：
USE entan; SHOW TAGS; SHOW EDGES;
```

**最大 3 个开放项**：
1. OI-C04-01：新增 2 个 Tag、6 类 Edge，以及 institution 的 ALTER，结构审批 → human:李伟
2. OI-C04-02：写回优先级与版本归属，以及 ADS 人工层表结构 → 李伟 + 产品
3. OI-C04-03：人工执行上面的 nGQL，核实 live schema 和 institution 属性数（Q055「只能灌 4 个字段」）

**风险**：
- `graph_project.py` 的 `ensure_schema` 含 `CREATE SPACE IF NOT EXISTS`。
- Pod 未 rollout，仍指向旧 graphd。
- 新库 enterprise/institution 顶点为 0，三要素边端点目前会全部 skipped。
- vendor/entan-py 与 lumen-topic-py 仍连 entan（违反一张 G，且有 D12 风险）。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 投影与图算法 Job 都在 lumen-algo-py；Java 只读 ADS |
| 2 前端→Java→Python `/internal/*` | ✅ 每张卡的 call_chain 都按此写；子图走 Feign → `/internal/graph/*` |
| 3 图谱只用 NebulaGraph TRSGraph（10.50.75.136:9669） | ✅ 无 Neo4j；space 只用 demo_gkx_chain |
| 4 可观测 | N/A（分析叶，不写代码） |
| 5 CI/CD | N/A |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 Java 不写 nGQL、只读 ADS | ✅；与 B01 R4（GraphController 直读 dwm_graph_*）不一致的部分已在 B01 记录 |
| 8 ADS 先行 / Mock | ✅ 先 ADS 再投影；d4 如实记 mock |
| 9 D8 / 11 D10 | N/A |
| 10 D9 血缘 | ✅ metric_id 只来自 B01/P00（MCP 派生快照），没读 metrics/registry |
| 12 D12 | ✅ lumen 链路写者只有 lumen-algo-py；三要素 Job 禁止 import vendor/entan-py（已列入 CF-C04-06 / risks） |
| 业务口径不替甲方拍板 | ✅ 久新行全部标「待确认」；「实时」口径列为 DN-C04-04 |
| 只读 | ✅ 未连库，未 commit/push，未读 task-registry.yaml / metrics/registry/ |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ≈550,000（估算） |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ≈$8.0（估算） |
| cost_warn | yellow（>$5 且 <$10） |
