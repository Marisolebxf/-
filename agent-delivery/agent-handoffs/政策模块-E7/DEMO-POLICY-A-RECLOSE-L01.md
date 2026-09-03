# DEMO-POLICY-A-RECLOSE-L01 · 政策专题 A 退出门

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-A-总派单.md`](./LUMEN-POLICY-A-总派单.md)

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；本叶只做 Demo 库可测退出门，不重做 S1–S4 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 核验叶，未改业务代码；未用 YAGNI 跳过退出门行数/挂接样本 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只跑现网 `kubectl exec` 计数，无需压缩大日志 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 本叶不改拓扑。确认 lumen 数仓 = demo 源 `demo_gkxlumenx_*`；产品链 Java/lumen-ui 虚线留给 C/D |
| 会签态 | `approved`（`01-data-flow.md` frontmatter） |

## 范围与实现

- 对照 bid / 总控：专题政策链 A 退出门 = Demo 库可测 + 至少 1 条可挂图产业样本。
- **未写**正式 `gkxlumenx_*`、**未写**三方 `gkx`、**未改** helm JDBC。
- MOCK 叶不需要：DWD 底表与 ADS 读面已有行，Job 不缺底数。

## 修改内容

- 无代码 diff。现网只读核验：`kubectl -n dev exec deploy/demo-platform-entan-py -- python -c '…polan.common.db.connect…'`

## 测试结果

### 库名（禁止正式前缀）

| 层 | 现网 |
|----|------|
| ODS | `demo_gkxlumenx_ods` |
| DWD | `demo_gkxlumenx_dwd` |
| ADS | `demo_gkxlumenx_ads` |

### 行数（2026-09-02 05:45 UTC+8 · 88.50 / ns `dev`）

| 表 | n |
|----|--:|
| ODS `dwd_policy_base` | 47051 |
| ODS `dwd_global_policy_base` | 27563 |
| DWD `policy_base_info` | 47051 |
| ADS `policy_focus` / `policy_intensity` | 47082 |
| ADS `policy_text_parse` | 47051 |
| ADS `policy_entity` | 162570 |
| ADS `policy_graph_node` | 48320 |
| ADS `policy_graph_edge` | 6916 |
| ADS `policy_effect` | 155 |
| ADS `policy_match` | 144 |
| ADS `policy_level_dist` | 6 |
| ADS `policy_type_dist` | 13 |
| ADS `policy_national_dist` | 31 |
| ADS `policy_sz_dist` | 10 |
| ADS `policy_metric_timeseries` | 93 |
| ADS `policy_simulate` | 36 |
| ADS `policy_timeseries` | 1 |

DWD 上其余 `policy_*` 分析结果表多为 0 行（Job 产出，本退出门不要求灌满）。

### 挂接样本（DoD #2）

| 项 | 值 |
|----|-----|
| `policy_id` | `21259543` |
| 标题 | 广东省科学技术厅关于开展“集成电路前沿技术与产业化”科技成果对接活动的通知 |
| ODS | `dwd_policy_base.id=21259543` 命中 |
| DWD `related_entities.industry` | `[{"name":"半导体与集成电路","industry_link_code":"INB170101"}]` |
| 图上 VID | `chain:INB170101`（码已在 `industry_link_code`；禁止用 ODS `INB1303`） |

`INB1303` 未出现在该条 `related_entities`。

### 复跑命令

在 88.50：

```text
kubectl -n dev exec deploy/demo-platform-entan-py -- python -c "from polan.common.db import connect; c=connect(); print(c.ods,c.dwd,c.ads)"
```

计数：`SELECT COUNT(*) AS n FROM demo_gkxlumenx_dwd.policy_base_info`  
样本：`SELECT policy_id, related_entities FROM demo_gkxlumenx_dwd.policy_base_info WHERE policy_id=21259543`

灌数批处理（本叶未重跑，路径与 demo 一致）：`polan` `run_sync` / `ods_to_dwd` / `run_all_policy`。禁止对正式 `gkxlumenx_*` 执行。

## 偏离说明

- 无。未新开工厂、未换仓。
- ADS 图节点列名非 `vid`（本叶不改 DDL）；挂接验收以 DWD `related_entities.industry.industry_link_code` 为准。

## 遗留风险

- DWD 分析结果表大量 0 行：B harness / Job 灌数后才会涨；不挡 A 退出门。
- QPOL-01～07 仍 🟡：诚实降级，不停工。
- 两套 INB 对照表另开，不挡本链已拍板的图上码挂接。

## CI/CD（必填）

- 分支：无业务 commit（核验叶）
- commit：无
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：`dev` / 现网 `demo-platform-entan-py`（只读）
- K8s rollout：未改
- dev 测试 URL / 命令与结果：上表 kubectl 计数 + 样本 JSON

## 可观测性（建议）

- 本叶无新 OTel。现网 polan 读库走已有 pod。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未在 Java 写算法 |
| 调用链 前端→Java→Python `/internal` | ✅ 本叶不改调用链 |
| 图谱 Nebula `demo_gkx_chain` | ✅ 未建 `gkx_policy`、未写 `gkx_chain` |
| 可观测 | ✅ 无新服务，不要求新埋点 |
| CI/CD | ✅ 无 push |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / Java 不直连 nGQL | ✅ |
| 数据策略 ADS 先行 | ✅ 只读 `demo_gkxlumenx_*` |
| D8 / D10 | N/A 无 UI |
| D9 8 件套 | N/A 本叶不改指标 |
| D12 lumen 不调 demo **服务** | ✅ 数仓共用 demo 源是总控 §0 #6 |

## 验收对照 DoD

1. ✅ 行数 + 复跑命令已写本 handoff  
2. ✅ `21259543` → `industry_link_code=INB170101`  
3. ✅ 未写正式数据面  
4. ✅ `ponytail: full` + cost 四字段（registry）

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 18000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.12 |
| cost_warn | green |
