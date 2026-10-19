# SCI-INT-A15 handoff：人才引进推荐评估集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A15（spike） |
| 执行 | agent:product-agent（coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：SRS `科技人才态势/人才引进推荐评估.md` excel_rows 308–332（seq 305–329），P00 leaf=A15 共 25 叶。页面映射一律 DS-16-TALENT-RECRUIT。
- **产出**：`产物/SCI-INT-A15.yaml`。在已落盘骨架上补全，未改 int_id 与行号。25 张 page 卡，号段 INT-A-X-1400–1424。已删除文件 `note` 与每张卡的 `skeleton`。
- **字段来源**：algorithm_type 与 d1/d4 用材料包里已写明的 MCP 口径（third_party / draft / mock）。无指标的叶 d1=missing。久新行只引用材料包 b01_mapping 里已有的 SRS-110、SRS-160、SRS-164，新增 0 行。
- **前端点查**：fe_files_hit 只有 `lumen-ui-science-pc/src/router/menu.ts`。菜单 `talent/talent-introduction-evaluation` 存在，`resolveNavComponent` 落到 `DevelopingView.vue`。lumen 无独立页面。demo 路径不在命中列表内，未点查。

### 1.1 派单关注点结论

| 问题 | 结论 | 卡 |
|---|---|---|
| DS-16 六条没有数据源的指标 | **不向久新要假 API。** C01 已核实无源。六条是 005 沟通障碍、006 文化融合、007 流动壁垒、010 引进阻力、013 成本模型、025 团队协同。模式 IP-10，`jiuxin_row_id` 空，owner 待定（DN-A15-01）。注册类型虽为 third_party，不能据此去要一行 API。禁止改挂 164/160/110。 | X-1404 / X-1405 / X-1406 / X-1409 / X-1412 / X-1424 |
| 成本模型的数据采集来源 | **开放项，当前无源。** row 319 没有 metric、没有久新行。薪酬、奖项、引才案例、薪酬趋势、激励政策都没有对端。013 属于上面六条。不向久新要采集 API，也不新建 ADS 成本表（新表须 human:李伟，现在没有口径）。DN-A15-COST 未关闭前，319–325 空态加警告，不出费用数字。 | X-1411–X-1417 |
| 人才主键 | **仍未定（C01 P0-1）。** 契约只用 `talent_key` 占位，不把 `scholar_id` 写成已定主键。主键落地前，画像与推荐不按已定键开查。 | 各人才卡，画像见 X-1418 |

## 2. 偏离说明

- 卡片数 25，SRS 叶数 25，一叶一卡，差集 0。骨架号段保持 X，维度改为 TAL。
- 有指标但无源的六条记 `owner_pending`，不算 metric_missing。没有注册指标、页面却要出数的叶才记 `metric_missing`。
- 308 缩放、328 报告拼装走 IP-09，只消费已有快照。无源章节保持空态。
- 本叶 `structure_escalation` 全部为 false。成本台账将来若要落新表，再升 human:李伟。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A15.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A15-check.py`
- 本 handoff
- 没有 commit 或 push，没有改动业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A15-check.py"`，输出：

```
scope_count=25 covered_rows=25 diff=[]
cards: 25 {'X': 25}
jiuxin_rows: ['SRS-110', 'SRS-160', 'SRS-164']
metric_missing: 11 ['INT-A-X-1401', 'INT-A-X-1408', 'INT-A-X-1410', 'INT-A-X-1411', 'INT-A-X-1413', 'INT-A-X-1414', 'INT-A-X-1415', 'INT-A-X-1416', 'INT-A-X-1417', 'INT-A-X-1422', 'INT-A-X-1423']
structure_escalation: 0 []
patterns: {'IP-07': 1, 'IP-08': 6, 'IP-09': 2, 'IP-10': 16}
OK
```

脚本核对了 P00 leaf=A15 恰好是 308–332、差集为空、卡号落在 1400–1499、全文无 TBD、无 skeleton、六条无源为 IP-10 且 owner 待定、成本结论为无源、主键引用 P0-1、lumen_page 为无、调用链不含 demo-*。

**结论：范围 25 叶，有卡片覆盖的 SRS 行 25 行，差集 0。**

### 4.1 统计

- **久新依赖（新增 0）**：SRS-164（310/311/327/329）、SRS-160（315/316）、SRS-110（326）。
- **metric_missing 11 张**：1401 贡献切面、1408 活跃度、1410 策略建议、1411 成本采集、1413 成本结构、1414 方案测算、1415 历史成本、1416 成本预警、1417 行业对比、1422 增量跟踪、1423 风险合规。
- **structure_escalation**：无。
- **lumen 页面**：无。

### 4.2 最大 3 个开放项

1. **六条无源指标的 owner（DN-A15-01）**：005/006/007/010/013/025。确认前 IP-10，不向久新追加 API。
2. **成本数据采集来源（DN-A15-COST）**：319 无表无行。未拍板前不出费用，不建新表。
3. **人才主键（C01 P0-1）**：仍未定。本页不选定 scholar_id。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 164/160 适配与 110 离线 Job 都在 Python；Java 只读 ADS。IP-10 叶不实现算法 |
| 2 调用链：前端 → Java → Python /internal | ✅ 有对端的卡按这个顺序写。前端不直连久新或 Nebula |
| 3 只用 NebulaGraph | ✅ 本叶在线不写 nGQL、不直连 graphd。110 的图侧沿用既有离线 Job |
| 4 可观测 | N/A（分析叶，无页面可埋点） |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 只读 | ✅ 未改 demo 仓。demo 页面未点查 |
| 7 共享聚合核心 | ✅ 110/160/164 复用已有久新行，不新开 |
| 8 ADS 先行 + Mock | ✅ 无源指标走 IP-10 空态，不用 mock 金额或假分填数 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 有注册指标的卡挂了 metric_id；没有的登记 metric_missing |
| 11 D10 | N/A |
| 12 D12 | ✅ 调用链不指向 demo-* 服务 |
| 禁读 registry YAML | ✅ 任务状态只走 MCP。指标口径用材料包已标注的 MCP 结果，未读 seed |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 120000（估算，与任务 estimated_tokens 同量级） |
| model_used | grok-4.7 |
| actual_cost | 1.5（USD，估算） |
| cost_warn | green |

未超过 $10，不暂停。
