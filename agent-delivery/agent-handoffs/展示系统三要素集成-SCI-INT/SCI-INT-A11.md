# SCI-INT-A11 handoff：科技发展规划系统集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A11（spike） |
| 执行 | agent:product-agent（coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（热点三条 API，待确认） |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：需规 `科技发展态势/科技发展规划.md`，excel_row 181–199（seq 178–196），共 19 个 SRS 叶。页面 DS-09-COMPREHENSIVE / DS-09-KEY-DOMAIN / DS-09-RESEARCH。
- **实现**：按 `产物/_card-template.yaml` 输出 19 张页面级卡片（号段 INT-A-X-1000～1018），一叶一卡，差集 0。本页跨要素，编号统一用 X。
- **输入**：`产物/_prep/A11-pack.yaml`、总派单 §2、B01 的 IP-01～IP-13、A12 已完成结论。只点查了材料包 `fe_files_hit`，未扫 demo 仓，未读 A11-digest.txt。
- **指标**：材料包已给出 MCP 口径，未再调 metric-get。INNOV / SYNTH 指标写入 `metric_domain_other`。

### 1.1 本叶必须给的结论

1. **人才流动（row 185，INT-A-X-1004）：IP-10，不归久新。** 注册为 MODEL（`M_INNOV_DS_09_COMPREHENSIVE_006` / `M_INNOV_PLAN_TALENT_FLOW`），但无 scholar_id、无流动边表。空态+⚠️。前端 `buildTalentOdLinks` 写死 18932 / 12458 人，不能当正式数。
2. **与 A12 不要并成一件。** A12 迁徙图主源是久新 API-157（`M_TALENT_DEEP_157_1`，INT-A-TAL-1103，SRS-157）。本页 excel 185 是另一条指标。
3. **资源推送（row 186，INT-A-X-1005）并入 gkxlumen-innov 订阅。** 与 A05 INT-A-X-413、A06 INT-A-X-515 同一服务，只加 `rule_type=planning_resource`。规则匹配不算算法，不经 Python，不经久新。
4. **竞争情报报告（row 198，INT-A-X-1017）与 A07 相同。** 目前前端模板拼装。是否大模型润色由甲方定（DN-A11-03，同 DN-A07-07）。
5. **久新只有三条热点 API，均待确认：** DS-09-COMPREHENSIVE-001 / 002 / 004。热度与增速注册为 MIXED，与久新 MODEL 冲突（CF-A11-1），不改型。
6. **前端现状：** 只调未实现的 `GET /situation/v1/planning/dataset`。重叠度用企业名称哈希（`getDeterministicOverlap`）。Java 与 Python 均无本页接口。

## 2. 偏离说明

- 自定义布局、筛选联动、报告导出没有单独向久新再要。筛选读空间密度父快照（IP-09）。报告维持前端模板（IP-13）。
- 无注册指标的统计数字写在 gaps，前缀 `metric_missing`（6 张）。
- 空间密度与土地效益需要新 ADS，升结构。流动边不在本叶另建，沿用 A12 已升的 INT-C-TAL-071。
- demo 页是否存在记 `unknown`（本叶未扫 demo 仓）。

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| 集成卡片 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A11.yaml` |
| 自检脚本 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A11-check.py` |
| 本 handoff | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-A11.md` |

未改业务仓、seed、矩阵或 task-registry.yaml，未执行 git commit/push。

## 4. 验收证据

自检命令为 `python 产物/_work/A11-check.py`。脚本先 `yaml.safe_load`，再核对 P00 中 leaf=A11 的 181–199、差集、号段 1000–1099、id 连续、IP 编号、三要素四段调用链、调用链无 `demo-`、久新行在 P00 内、材料包指标与未挂指标都进 assignment、流动为 IP-10 且不并 API-157、推送不经 Python、报告为模板。实际输出：

```
scope_count=19 covered_rows=19 diff=[]
cards: 19 {'X': 19}
jiuxin_rows: ['DS-09-COMPREHENSIVE-001', 'DS-09-COMPREHENSIVE-002', 'DS-09-COMPREHENSIVE-004']
metric_missing: 6 ['INT-A-X-1001', 'INT-A-X-1002', 'INT-A-X-1010', 'INT-A-X-1011', 'INT-A-X-1012', 'INT-A-X-1018']
structure_escalation: 2 ['INT-A-X-1007', 'INT-A-X-1009']
patterns: {'IP-01': 2, 'IP-04': 4, 'IP-08': 2, 'IP-09': 3, 'IP-10': 6, 'IP-13': 2}
OK
```

**范围 19 / 已出卡 19 / 差集 0**

### 4.1 统计

- **卡片**：19 张，全部 X。
- **久新依赖**：3 条，均待确认，新增 0 条。001 热度、002 增速、004 动态跟踪。
- **metric_missing（6 张）**：七库指标盘（1001）、热点动态跟踪无注册指标（1002）、载体分布（1010）、筛选联动的规模/状态/领军主题（1011）、资源配置模拟（1012）、战略建议模拟评估（1018）。
- **structure_escalation（2 张，升级 human:李伟）**：
  - INT-A-X-1007：空间密度 ADS 候选 `ads_innov_spatial_density`。
  - INT-A-X-1009：土地效益 ADS 候选 `ads_innov_land_benefit`。
- **lumen 页面**：有。`/trend/tech-development-plan`，单 dataset 接口未实现。
- **demo 页面**：unknown。
- **decision_needed**：DN-A11-01～06；另引用 Q149 / Q150 / Q151 / Q152、DN-01、DN-07、DN-A05-06、DN-A07-07、DN-A12-02。

### 4.2 关键冲突

- **CF-A11-1**：热度/增速注册 MIXED，久新 001/002 标 MODEL。
- **CF-A11-2**：004 标 MODEL，本叶无注册 metric_id。
- **CF-A11-3**：本页流动监控与 A12 API-157 不是同一个指标。
- **CF-A11-4**：等级注册 MODEL，实现是重叠度阈值切分。
- **CF-A11-5**：全要素图谱注册 THIRD_PARTY，但不在三条热点 API 内。

### 4.3 最大 3 个开放项

1. **三条热点 API 是否交付，以及 MIXED 与 MODEL 以谁为准**（DN-A11-01 / CF-A11-1）。确认前不改注册类型。
2. **流动监控与迁徙图保持两件**（DN-A11-02 / CF-A11-3）。scholar_id 与流动边未就绪前 1004 不出数。
3. **竞争情报报告是否大模型润色**（DN-A11-03）。现状是前端模板，同 A07。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 区位商、方向预警、竞争力、重叠度走 lumen-algo-py。规则匹配留在 Java 订阅，不算算法。Java 不算区位商、不做名称哈希 |
| 2 调用链：前端 → Java → Python /internal | ✅ 前端不直连久新。IP-01/09/10/13 的在线链路不经 Python，已在卡片写明 |
| 3 只用 NebulaGraph | ✅ 图谱归属未定前空图。若自建，只写 TRSGraph，Java 不写 nGQL |
| 4 可观测 | ⚠️ 本页后端未实现。契约要求 Java Agent + Python 外呼 span；实现叶补齐 |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ 未扫 demo，调用链不指向 demo |
| 7 共享聚合核心 | ✅ Java 只读 ADS / 快照。门面归属引用 DN-07 |
| 8 ADS 先行 + Mock | ✅ 无源走 IP-10。USE_MOCK=false 禁止哈希和写死人数 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 已挂指标写入卡片。无注册统计记 metric_missing（6 张） |
| 11 D10 | N/A（不改 UI） |
| 12 D12 | ✅ 调用链无 demo-*（脚本断言）。正式开发禁止复用 demo 服务 |
| 禁读 registry YAML | ✅ 任务走 MCP。指标口径用材料包，未读 metrics/registry |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 200000（估算，无 Console 分项） |
| model_used | grok-4.7 |
| actual_cost | 1.08（USD，估算） |
| cost_warn | green |

预算表没有 Grok 单价。成本按 B 档（输入 $3/M、输出 $15/M）和约 80/20 的输入输出比估算：`200000×0.8×3/1e6 + 200000×0.2×15/1e6 = 1.08`。低于 $10 暂停线，不暂停。
