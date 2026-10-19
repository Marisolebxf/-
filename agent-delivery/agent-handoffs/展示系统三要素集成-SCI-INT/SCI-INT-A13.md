# SCI-INT-A13 handoff：关注地区人才态势系统集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A13（spike） |
| 执行 | agent:product-agent（协作 architect-agent；coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新 |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：需规 `科技人才态势/关注地区人才态势.md`，excel_row 269–279（seq 266–276），共 11 个 SRS 叶。页面 DS-14-TALENT-REGION。
- **实现**：沿用已有 11 张卡的号段 INT-A-X-1200～1210，一叶一卡。自检先失败在占位文案「未实现（草案）」和 freshness 不在枚举。只改了这 11 张卡的占位字段，并补了三条结论，没有另起一套卡号。差集 0。
- **输入**：`产物/_prep/A13-pack.yaml` 与 P00 的 A13 叶、久新 row_id。未扫代码仓，未调 metric-get。材料包 2 个已挂指标均为 third_party / D1=草案 / D4=Mock。
- **页面文件**：材料包 `fe_files_hit` 只有 `lumen-ui-science-pc/src/router/menu.ts`，没有页面组件，也没有 demo 路径。lumen 与 demo 是否已有本页记 **未核实**。`fe_route` 保持 null。

### 1.1 页面指标挂叶

| metric_id | 材料包挂到的 SRS 行 | 卡片额外消费 |
|---|---|---|
| M_TALENT_BASE_98_1 | 273、274、278 | 269、271、272、275、276、277（同一 SQL-98 聚合的中国地图、镜头/筛选、深圳点击与镜头/筛选） |
| M_TALENT_DEEP_157_1 | 270 | — |

### 1.2 本叶必须给的结论

1. **中国地图（row 269，INT-A-X-1200）：人数来源是久新 SQL-98，底图未核实。** 材料包本行 metrics 为空。需规要各省、市的数量，同页 273 已挂 `M_TALENT_BASE_98_1`（IP-06，SRS-98），本卡额外消费，不另造指标，不新建主维。底图瓦片和行政区边界材料包没有，未核实（DN-A13-01）。密度要面积分母，材料没有，确认前只出人数（metric_missing）。
2. **深圳地图（row 274，INT-A-X-1205）：人数来源同样是 SQL-98，底图未核实，区/园区/载体升结构。** 材料包已把 SQL-98 挂在本行。需规还要行政区、科技产业园、创新载体逐级，材料包没有这级维表。`structure_escalation=true`，责任人 human:李伟（DN-A13-02）。落地前不下钻到园区，Java 不现场聚合。
3. **报告导出（row 279，INT-A-X-1210）：未核实，不新要久新行。** 材料包无指标、无久新行。地图数据导出复用已加载的 SQL-98 快照，前端落文件。智能报告的模型、模板、生成服务材料没有，未核实（DN-A13-03）。确认前 IP-10，不出报告，不向久新要假 API。

迁徙图（row 270）按叶名和已挂的 `M_TALENT_DEEP_157_1`（IP-08，SRS-157）集成。材料包里该行的需规正文复述了 269 的分布/热力/区域比较，与叶名不一致（CF-A13-2）。事件定义材料没有，未核实，确认前空态。

### 1.3 需要久新提供的能力

已有行 2 条，本叶不新增久新行：SRS-98（人才基础指标 SQL）、SRS-157（人才流动追踪）。底图、密度、代表性专家、学历/成长/合作网络、增速、智能报告不向久新虚构接口。

## 2. 偏离说明

- 中国地图、镜头、筛选（269、271、272、275、276、277）材料包没有单独挂指标。人数与同页 SQL-98 是同一聚合，记 IP-09 或地图本卡 IP-06，不另向久新要一行。
- 无注册指标的统计写在 gaps，前缀 `metric_missing`。纯镜头不单独出数。
- 深圳排行上的增速、流动路径（278）不把 DEEP_157 再挂进这张 IP-06 卡。流动见 1201，本行记 metric_missing。
- 导出与智能报告拆开写：导出不新开查询；报告确认前不提供。

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| 集成卡片 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A13.yaml` |
| 自检脚本 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A13-check.py` |
| 本 handoff | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-A13.md` |

未改业务仓、seed、矩阵或 task-registry.yaml，未执行 git commit/push。

## 4. 验收证据

自检命令为 `python 产物/_work/A13-check.py`。脚本核对 P00 中 leaf=A13 的 269–279、差集、号段 1200–1299、全文无 TBD / skeleton / 「未实现（草案）」、IP 编号、材料包指标行的模式与久新行、三要素调用链无 `demo-`、中国/深圳底图结论为未核实、报告导出不新要久新行。实际输出：

```
scope_count=11 covered_rows=11 diff=[]
cards: 11 {'X': 11}
jiuxin_rows: ['SRS-157', 'SRS-98']
metric_missing: 6 ['INT-A-X-1200', 'INT-A-X-1202', 'INT-A-X-1204', 'INT-A-X-1206', 'INT-A-X-1209', 'INT-A-X-1210']
structure_escalation: 1 ['INT-A-X-1205']
patterns: {'IP-06': 4, 'IP-08': 1, 'IP-09': 5, 'IP-10': 1}
OK
```

**范围 11 / 已出卡 SRS 行数 11 / 差集 0**

### 4.1 统计

- **卡片**：11 张，号段 X 11（TAL/TECH/ORG 拆号 0；维度仍是 TAL）。
- **久新依赖**：2 条（SRS-98、SRS-157），新增 0 条。
- **metric_missing（6 张）**：密度（1200）、代表性专家（1202）、流动历史曲线（1204）、学历/成长/合作网络/简介（1206）、增速与流动路径（1209）、智能报告（1210）。
- **structure_escalation（1 张，升级 human:李伟）**：INT-A-X-1205，深圳区/园区/创新载体地理维，材料包没有这级表。
- **lumen 页面**：未核实。材料只点到菜单文件，没有页面组件。
- **demo 页面**：未核实。材料包无 demo 路径。
- **decision_needed**：DN-A13-01～05。

### 4.2 关键冲突

- **CF-A13-1**：材料包 row 269 没有指标，地图人数仍要展示。额外消费同页 SQL-98，不新造 metric_id。
- **CF-A13-2**：row 270 的需规正文复制了 269，叶名是迁徙图且已挂 DEEP_157。按叶名和指标集成。
- **CF-A13-3**：需规点名五个重点领域，材料包没有领域码。确认前不写死枚举（DN-A13-05）。

### 4.3 最大 3 个开放项

1. **底图与行政区边界**（DN-A13-01）：中国、深圳都未核实。确认前不接未点名的地图服务。
2. **深圳区/园区/载体维表**（DN-A13-02，INT-A-X-1205）：升结构。落地前不下钻。
3. **智能报告**（DN-A13-03）：模型、模板、是否大模型都未核实。确认前 IP-10，不向久新要假 API。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ SQL-98 进 ETL/ADS；API-157 走 Python 适配。Java 只读 ADS，不算密度、不差分迁徙、不生成报告 |
| 2 调用链：前端 → Java → Python /internal | ✅ 前端不直连久新。IP-06/09/10 在线不经 Python；IP-08 的在线链路经 Python 适配。路由材料未给，fe_route=null |
| 3 只用 NebulaGraph | ✅ 本叶不写图、不写 nGQL。合作网络无指标，记 metric_missing，不另造点边 |
| 4 可观测 | ⚠️ 页面文件未核实，本叶无实现。契约要求 Java Agent + Python 外呼 span；实现叶补齐 |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ 材料未给出 demo 路径，调用链不指向 demo |
| 7 共享聚合核心 | ✅ 人数读 SQL-98 落 ADS 的草案，Java 不现场扫三方库。门面路径标 draft，现网未核实 |
| 8 ADS 先行 + Mock | ✅ 无源走 IP-10。未核实字段不拿原型填数 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 材料包 2 个指标写入卡片并额外消费到同聚合叶。无注册统计记 metric_missing（6 张）。D1/D4 用材料包口径 |
| 11 D10 | N/A（不改 UI） |
| 12 D12 | ✅ 调用链无 demo-*（脚本断言）。未把 demo 服务写进正式链 |
| 禁读 registry YAML | ✅ 任务走 MCP。指标口径用材料包，未读 metrics/registry |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 160000（估算，无 Console 分项） |
| model_used | grok-4.7 |
| actual_cost | 0.86（USD，估算） |
| cost_warn | green |

预算表没有 Grok 单价。成本按 B 档（输入 $3/M、输出 $15/M）和约 80/20 的输入输出比估算：`160000×0.8×3/1e6 + 160000×0.2×15/1e6 = 0.86`。低于 $10 暂停线，不暂停。
