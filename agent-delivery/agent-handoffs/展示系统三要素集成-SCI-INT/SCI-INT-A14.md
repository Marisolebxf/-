# SCI-INT-A14 handoff：重点科技人才画像集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A14（spike） |
| 执行 | agent:product-agent（coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：SRS `科技人才态势/重点科技人才画像.md` excel_rows 280–307（seq 277–304），P00 leaf=A14 共 28 叶。页面映射一律 DS-15-TALENT-PROFILE。
- **产出**：`产物/SCI-INT-A14.yaml`。在已落盘骨架上补全，未改 int_id 与行号。28 张 page 卡，号段 INT-A-X-1300–1327。已删除文件 `note` 与每张卡的 `skeleton`。
- **字段来源**：algorithm_type 与 d1/d4 用材料包里已写明的 MCP 口径（third_party / draft / mock）。无指标的叶 d1=missing。久新行只引用材料包 b01_mapping 里已有的 SRS-110、SRS-160、SRS-162，新增 0 行。
- **前端点查**：fe_files_hit 只有 `lumen-ui-science-pc/src/router/menu.ts`。菜单 `talent/key-talent-profile` 存在，`resolveNavComponent` 落到 `DevelopingView.vue`。lumen 无独立页面。demo 路径不在命中列表内，未点查。

### 1.1 派单关注点结论

| 问题 | 结论 | 卡 |
|---|---|---|
| 人才主键 | **人才主键未定（C01）。** 契约只用 `talent_key` 占位，不把 `scholar_id` 写成已定主键。 | 各卡 `C01-P0-1` |
| H 指数 / 活跃度 | **H 指数/活跃度在久新 DS-08-VIZ-001/004（A10），只引用。** 不把 `M_INNOV_EXPERT_*` 写入本叶 metric_ids，不在前端或 Java 重算。学术力读面只用已挂的 `M_TALENT_DEEP_162_1`。 | X-1311 / X-1313 |
| 基础信息写回 | **写回走 ADS 人工层再投影，不直接写 Nebula（A03/C04）。** Java 只受理；Python `/internal` 写人工层；审核通过后再投影。人工层是新表，升 human:李伟。导入与纠错复用这一层，不另建表。 | X-1302（升级），X-1304 / X-1305 复用 |
| 隐私与脱敏 | **decision_needed，不替甲方拍板。** 敏感字段、授权角色、脱敏规则、加密要求都未定。关闭前接口不返回敏感字段。 | X-1303，DN-A14-PRIVACY |
| 合作网络图谱 | **只引用 C04 的 talent（INT-C-TAL-310）与 talent_coop（INT-C-TAL-350）。** `_prep/C-index.yaml` 无这两个名字（`talent_coop` 零命中，`talent` 不是 Tag 名）。没有就 structure_escalation，不另造点边。在线 Java 只读 ADS 投影，不写 nGQL。 | X-1306 / 1308 / 1320 / 1322 / 1323 / 1324 / 1326 / 1327 |

## 2. 偏离说明

- 卡片数 28，SRS 叶数 28，一叶一卡，差集 0。骨架号段保持 X，维度改为 TAL。
- 没有注册指标、页面却要出数或排序的叶才记 `metric_missing`（5 张）。纯呈现、纯交互走 IP-10 或 IP-09，不记缺失。
- 有指标的叶按材料包 b01_mapping：160/162 为 IP-08，110 为 IP-07。第一张卡无指标，模式 IP-10。
- 图谱卡与写回新表 `structure_escalation: true`。纯缩放聚焦不升结构。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A14.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A14-check.py`
- 本 handoff
- 没有 commit 或 push，没有改动业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A14-check.py"`，输出：

```
scope_count=28 covered_rows=28 diff=[]
cards: 28 {'X': 28}
jiuxin_rows: ['SRS-110', 'SRS-160', 'SRS-162']
metric_missing: 5 ['INT-A-X-1307', 'INT-A-X-1312', 'INT-A-X-1316', 'INT-A-X-1318', 'INT-A-X-1319']
structure_escalation: 9 ['INT-A-X-1302', 'INT-A-X-1306', 'INT-A-X-1308', 'INT-A-X-1320', 'INT-A-X-1322', 'INT-A-X-1323', 'INT-A-X-1324', 'INT-A-X-1326', 'INT-A-X-1327']
patterns: {'IP-07': 2, 'IP-08': 8, 'IP-09': 8, 'IP-10': 10}
OK
```

脚本核对了 P00 leaf=A14 恰好是 280–307、差集为空、卡号落在 1300–1399、全文无 TBD、无 skeleton、主键引用 C01、隐私为 decision_needed、写回走 ADS 人工层、H 指数只引用 A10、调用链不含 demo-*。

**结论：范围 28 叶，有卡片覆盖的 SRS 行 28 行，差集 0。自检 OK，差集 0。**

### 4.1 统计

- **久新依赖（新增 0）**：SRS-160（286/288/300/302/303/306）、SRS-162（291/293）、SRS-110（304/307）。DS-08-VIZ-001/004 只引用 A10，不计入本叶新增。
- **metric_missing 5 张**：1307 语义检索、1312 相似人才与历史趋势、1316 成果列表、1318 新成果事件、1319 成果详情与原文链接。
- **structure_escalation 9 张**：1302 人工层新表；1306/1308/1320/1322/1323/1326 依赖 talent_coop；1324/1327 依赖 talent。升 human:李伟。
- **lumen 页面**：无。

### 4.2 最大 3 个开放项

1. **隐私与脱敏（DN-A14-PRIVACY）**：字段、角色、脱敏和加密都未拍板。不替甲方选定。
2. **人才主键（C01 P0-1）**：仍未定。本页不选定 scholar_id。
3. **图点边（DN-A14-GRAPH）**：C-index 没有 talent / talent_coop。结构由 human:李伟 落地前，合作网络与领域图空态，不另造。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 160/162 适配与 110 离线 Job 都在 Python；Java 只读 ADS。IP-10 叶不实现算法 |
| 2 调用链：前端 → Java → Python /internal | ✅ 有对端的卡按这个顺序写。前端不直连久新或 Nebula |
| 3 只用 NebulaGraph | ✅ 在线不写 nGQL、不直连 graphd。图名只引用 C04，Java 不写 Nebula |
| 4 可观测 | N/A（分析叶，无页面可埋点） |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 只读 | ✅ 未改 demo 仓。demo 页面未点查 |
| 7 共享聚合核心 | ✅ 110/160/162 复用已有久新行，不新开 |
| 8 ADS 先行 + Mock | ✅ 无源走 IP-10 空态。写回先落 ADS 人工层再投影 |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 有注册指标的卡挂了 metric_id；没有的登记 metric_missing。H 指数只引用不改挂 |
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
