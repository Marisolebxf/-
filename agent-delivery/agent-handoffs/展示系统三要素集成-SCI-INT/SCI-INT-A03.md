# SCI-INT-A03 handoff — 科学技术全景·维护（写回链路）三要素集成分析

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A03（analysis 叶） |
| 执行 | agent:product-agent |
| 监管人 | human:淮政玮（claim_type=coordinator_dispatch） |
| ponytail: | N/A（分析叶） |
| 范围 | SRS `科技发展态势/科学技术全景.md` excel_rows 37–50（14 叶）；页面 DS-02-MAINTAIN-GRAPH（37–43）/ DS-02-MAINTAIN-ENTITY（44–50） |
| 不在范围 | rows 20–36（展示侧，归并行叶 A02） |

## 1. 范围与实现

- 按 `产物/_card-template.yaml` 出 **22 张卡**（layer: page，int_id `INT-A-{TECH|X}-200..221`），14 个 SRS 叶每叶 ≥1 卡；多依赖叶拆卡同 excel_row（37/38/42/44/45 各 2 张，43 拆 4 张：版本回滚 / Nebula 投影 / 久新同步 / 审核权限）。
- 维度：TECH 13（维护技术图谱 rows 37–43）、X 9（维护实体关系 rows 44–50，人/机构/论文/专利挂接，非单一三要素维度按 NONE_3E 外的 X 记）；TAL 0、ORG 0。
- 写回卡 `dep_kind` 含 `write_back` 共 18 张；全部三要素卡 `call_chain` 四段齐（FE `/trend/tech-panorama/maintain（draft）` → Java `POST /topic/v1/tech/graph/changes（draft）` → Python `POST /internal/v1/sci/tech/graph/changes（draft）` → 主表 / Nebula gkx_chain / ADS）。
- 指标：唯一挂 metric 的是 row 44 推荐列表与 row 45 智能计算关联强度 → `M_TECH_GRAPH_105_1`（MCP：third_party / d1=draft / d4=mock）；其余为操作类 `n/a_ops`，gaps 注明「metric_ids 无」；row 50 批量回执计数记 1 条 `metric_missing`（建议豁免 ⓘ，DN-A03-09）。
- 顶层 `write_back_design_draft`（草案，全部待裁定）：
  - **主数据持有**：沿 C02 结论——当前无人持有技术点主数据，TRSGraph 技术 ID=名称；草案为我方自建技术主表 + technology_id，Python 单写者（DN-A03-01）。
  - **三层**：auto（久新 104/105 Job 产出）/ manual（add / update / tombstone）/ published；合并规则字段级 manual > auto，tombstone 抑制自动复活，自动新值碰人工覆盖字段 → 冲突队列。
  - **流程**：编辑 → 草稿变更集 → 审核（可选，SRS 无「审核」字样，DN-A03-02）→ 发布（= SRS-40「保存」：主表 → 版本 → Nebula 投影 → ADS 投影，失败 projection_pending + 补偿重放）→ 同步。
  - **版本 / 回滚**：乐观锁 base_version（冲突 409）；回滚 = 应用反向变更集；改名不换 ID，合并 / 拆分写 redirect。
  - **审计**：Java `@SysLog`（请求级，gkxlumen-common-log 已有）+ Python `graph_change_log`（对象级，带 trace_id）。
  - **久新同步**：A 分层覆盖（推荐，104/105 交 Python 由我方 Job 跑）/ B 我方回推久新（需久新持有运行实体库，JX-A03-04）/ C 全量覆盖（否决，人工维护每轮丢失）。
  - **需久新提供 4 项**：JX-A03-01 104 可锚外部 technology_id + 增量 + run_id/置信度；JX-A03-02 105 边带 source/run_id/关系类型且 Job 接受排除清单；JX-A03-03 任意（实体, 技术点）关联强度函数；JX-A03-04（仅选项 B）人工变更接收接口 + 回执 + 冲突码 + 订阅。全部「待确认」。

## 2. 现状核查（只读）

| 仓 | 现状 |
|---|---|
| demo-ui-science `tech-situation-maintain/` | 纯内存 Mock：撤销栈 20、版本上限 8、operator 写死「演示账号」、推荐 5 条写死、批量仅删除；**无后端契约可参照** |
| lumen-ui-science-pc | 仅 `/trend/tech-panorama`；`api/situation/panorama.ts` 只有 `POST /situation/v1/panorama/graph`；「维护技术图谱」按钮只埋点；**无维护页 / 路由** |
| lumen-svc-platform | 无 `/situation`、无 tech 图谱写接口；`@SysLog` / gkxlumen-flow 模块存在（flow 可用性 unknown） |
| lumen-algo-py | 无 technology_id、无 tech 写路由；可参照写法 `vendor/entan-py/entan/graph/incremental.py`（ADS graph_node/edge + Nebula INSERT/DELETE VERTEX 双写） |

## 3. 偏离说明

- 无偏离 SRS 范围。接口路径、表名、模块落点均为 **draft**（门面落点 `/situation/v1` vs 详设 11 `/topic/v1/{element}/graph/**` 冲突，见 OI-A03-06 / R-A03-06）。
- DS 映射裁定 row 44 → `M_TECH_GRAPH_105_1`；指标 kit 中 `M_TECH_ENTITY_TOP5` 自述「维护侧候选列表复用 TOP5」，两处不一致，已在卡 213 gaps 记录，未擅自改映射。
- 卡 207（前端撤销 / 重做）为纯 FE 状态，`structure_escalation: false`；213/214/216 读面类亦 false；其余 18 张升级 human:李伟。

## 4. 产物清单

| 产物 | 路径 |
|---|---|
| 卡片 + 写回设计草案 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A03.yaml` |
| 自检脚本 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A03-check.py` |
| 本 handoff | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-A03.md` |

未 commit / push；未改任何业务仓、seed、矩阵。

## 5. 验收证据

范围 14 / 已出卡 SRS 行数 14 / 差集 0。实跑 `python 产物/_work/A03-check.py`（exit 0）：

```
scope_count=14 covered_rows=14 diff=[]
cards: 22 {'TECH': 13, 'X': 9}
cards_per_row: {37: 2, 38: 2, 39: 1, 40: 1, 41: 1, 42: 2, 43: 4, 44: 2, 45: 2, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1}
write_back_cards: 18
jiuxin_rows: ['SRS-104', 'SRS-105'] jiuxin_cards: 6
required_from_jiuxin: 4
metric_missing: 1
structure_escalation: 18
decision_needed: 9 risks: 8
patterns: {'IP-01': 1, 'IP-05': 10, 'IP-07': 5, 'IP-09': 2, 'IP-10': 1, 'IP-11': 2, 'IP-13': 1}
OK
```

脚本断言：rows 与 P00 leaf=A03 一致且 path 逐条匹配；int_id 号段 200–299；IP 仅 01–13；jiuxin_row_id ∈ P00 jiuxin_rows 且 counterpart=jiuxin；三要素卡 call_chain 四段非空；统计卡 metric_ids 或 metric_missing/「metric_ids 无」；metric 卡 algorithm_type 与 d1_d4 等于 MCP 返回值；int_id 唯一；card_count 自洽；写回草案各块非空；DN 引用卡存在。

## 6. 开放项 / 决策（摘要）

- OI-A03-01 / DN-A03-01 技术点主数据持有方与 technology_id 规则 → **阻塞全部写回卡**
- OI-A03-02 / R-A03-01 Nebula VID `tech:{名称}` 改名即断边，上线前须切 technology_id（C04）
- OI-A03-03 / DN-A03-07 「一张 G」作用域：本页编辑是否直接影响专题 TOPIC-TECH-05
- 其余：DN-A03-02 审核与角色、DN-A03-03 人工 vs 104/105 优先级、DN-A03-04 实体属性生效范围、DN-A03-05 关系类型枚举（四套）、DN-A03-06 保留期、DN-A03-08 搜索范围、DN-A03-09 回执计数豁免 ⓘ
- 业务口径项需甲方拍板，PM 登记 `客户决策清单跟踪表.md`。

## 7. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 算法只在 Python | ✅ 关联强度 / 合并 / 投影均放 Python；Java 只鉴权、审计、转发 |
| 调用链 FE → Java → Python `/internal/*` | ✅ 全部卡四段链；前端不直连久新 |
| NebulaGraph TRSGraph，禁 Neo4j | ✅ 只写 gkx_chain（demo: demo_gkx_chain） |
| Java 不写 nGQL / 只读 ADS | ✅ 写回经 Python；「Java 写变更表」方案仅入 R-A03-04 / OI-A03-05 |
| 可观测 | ✅ 审计含 trace_id；FE trackInteraction 已有 |
| 共享聚合核心 | ✅ 复用 `/topic/v1/{element}/graph/**` 方向（落点待 DN-07） |
| D9 血缘 | ✅ 指标卡 metric_id + MCP 类型 / d1_d4；缺口记 metric_missing |
| D12 demo 隔离 | ✅ 链路无 demo-*；demo 仅作现状参照 |
| 业务口径不替甲方拍板 | ✅ 9 条 decision_needed，久新行全部待确认 |

## 8. Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 300000（估算） |
| model_used | claude-opus-5.5 |
| actual_cost | 7.5 |
| cost_warn | yellow（> $5，< $10，无需暂停） |
