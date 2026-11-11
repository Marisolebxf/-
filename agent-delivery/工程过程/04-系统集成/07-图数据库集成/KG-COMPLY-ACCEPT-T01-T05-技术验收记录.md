# T01 / T05 技术验收记录（KG-COMPLY-ACCEPT-T01-T05）

- 验收人：唐绍祖（技术验收）
- 验收日期：2026-11-11
- 被验收对象：`KG-COMPLY-LOAD-T01`、`KG-COMPLY-LOAD-T05`
- 验收方式：**独立连库只读复测**，不采信交付文档自述；复测未执行任何 DDL/DML
- 目标库：`demo_gkx_chain`（NebulaGraph）
- 关联裁定：[KG-COMPLY-VID-L01](./KG-COMPLY-VID-L01-VID前缀实测与裁定.md)、[T04 答复](./KG-COMPLY-LOAD-T04-答复韩梦蕊-M08与paper点.md)

---

## 一、结论

| 任务 | 结论 | 依据 |
|---|---|---|
| T01 入图环境与结构核验 | **技术验收通过** | 16 条建表全部落地，5 个新点类型 + 11 种新边齐全，属性最小集合规 |
| T05 空态层入图核验 | **技术验收通过** | 11 条 M 关系逐条复跑全部为 0，`policy` / `institution` 历史数据与本期无供数区分正确 |
| T02 产业链与机构合作组 | **可置 ready** | T01 已复验，前置闸解除；须带下方三条护栏 |

---

## 二、T01 验收明细

### 2.1 交付物

| 文件 | 内容 |
|---|---|
| `T01-缺口清单-交付版.md`（v3 终版） | 初核 / v2 补列 / v3 裁定回填 / 11-11 执行与复验记录 |
| `T01-缺口清单-实测.md` | 初核实测 |
| `T01-补列-实测.md` | VID 前缀与端点抽样 |
| `T01-建表执行-实测.md` | 16 条 CREATE 执行记录（16/16 成功） |
| `T01-复验-实测.md` | 复验实测（9 基线 Tag + 15 基线 Edge 全一致） |
| `t01_verify.py` / `t01_sample_cols.py` / `t01_execute_ddl.py` | 核对脚本三件，凭据走环境变量 |

授权链：唐绍祖 2026-11-10 确认内容 → 徐滕强 2026-11-11 授权执行 → 2026-11-11 00:53 执行 16 条 CREATE，00:55 复验。

### 2.2 本次独立复测结果

复测语句：`SHOW TAGS` / `SHOW EDGES` / `DESCRIBE TAG` / `DESCRIBE EDGE`，全部只读。

| 检查项 | 期望 | 实测 | 判定 |
|---|---|---|---|
| 点类型（Tag）总数 | 原有 + 新建 5 | 15 | — |
| 边类型（Edge）总数 | 原有 15 + 新建 11 = 26 | 26 | ✅ |
| 新建 5 点类型 | `research` `paper` `patent` `project` `person` | 全在 | ✅ |
| 新建 11 边 | `belong` `participate` `author_of` `publish` `policy_relate` `policy_apply_to` `research_coop` `talent_coop` `service_provide` `supply` `parent_sub` | 全在 | ✅ |
| 新点属性 | 至少 `name` + `props` | 5 个新点均为 `name, props` | ✅ |
| 新边属性 | 至少 `weight` + `props` | 抽查 `belong` / `participate` / `publish` / `supply` / `parent_sub` 均为 `weight, props` | ✅ |

**重点复核历史 P0 缺陷**：首版曾出现 `CREATE EDGE ... ();` 空属性结构，本次实测新建边均带 `weight` + `props`，**缺陷已修复，不得回退**。

### 2.3 遗留说明（不阻塞验收）

- 新建边本期边数均为 0 属正常：数据由 T02–T04 后续灌入，T01 只负责结构。
- 库内存在 6 对语义重叠的历史边（`apply_to` / `policy_apply_to`、`belong` / `belongs_to`、`participate` / `participates`、`supply` / `supplies`、`cooperate` / `research_coop`、`cite` / `tech_has_paper`）。成因是早期技术点层与七要素层混装，**归 T06 语义去重处理**，不影响 T01 结构验收结论。
- 本次不核对 DDL 授权聊天记录原件，授权链以交付文件记载为准。

---

## 三、T05 验收明细

### 3.1 本次独立复测结果

逐条只读计数（`MATCH ()-[e:<边型>]->() RETURN count(e)`，端点关系单独按 Tag 对计数）：

| M 编号 | 边型 / 关系 | 交付报告 | 本次实测 | 判定 |
|---|---|---|---|---|
| M05 | `belong` | 0 | 0 | ✅ |
| M10 | `publish` | 0 | 0 | ✅ |
| M11 | `policy_relate` | 0 | 0 | ✅ |
| M12 / M13 / M14 | `policy_apply_to` | 0 | 0 | ✅ |
| M16 | `cite` | 0 | 0 | ✅ |
| M18 | `institution` → `segment`（`participates`） | 0 | 0 | ✅ |
| M21 | `service_provide` | 0 | 0 | ✅ |
| M23 | `supply` | 0 | 0 | ✅ |
| M24 | `parent_sub` | 0 | 0 | ✅ |

参考基线复算：

| 项 | 交付报告 | 本次实测 | 判定 |
|---|---|---|---|
| M17 存量 `enterprise` → `segment` | 178,731 | 178,731 | ✅ 与基线一致 |
| 历史混装 `institution` → `institution`（不属 M17/M18） | 34,769 | 未重算，采信报告 | — |

### 3.2 报告质量复核

- 11 条边逐条给出边型存在性 + 实测条数，无缺行；
- **区分了两层事实**：`policy` 点 20,000、`institution` 点 43,296 为历史数据，本期七要素合规层无新边，未将有点的表误写为空表；
- 未灌 mock、未从 `gkx_chain` 拷数，符合只读核数定位。

### 3.3 登记册历史状态回填口径

T05 登记册长期停留 `backlog`，成因是 2026-11-11 分工调整（兰天驰退出，T05 移交白鑫凤）时未补认领字段，**属记账遗留，非技术缺陷**。

- 补录方式：`claimed_by` 记为 `human:白鑫凤`，`claimed_at` 记为补录时刻，并在 `note` 明示「分工调整后补录，非原始认领时间」；
- **不得**倒填成她当初自行认领，**不得**因此影响其他任务的贡献归属；
- T05 为只读核数，不产生执行器经验，不进 T13 依赖，签收后无下游解锁影响。

---

## 四、T02 放行条件（三条护栏，缺一不得开工）

T01 已复验，`T01 → T02` 依赖闸解除，T02 可置 `ready` 由陈芸飞认领。但必须同步以下约束：

| 编号 | 护栏 | 原因 |
|---|---|---|
| G1 | **M15 / M17 只回读核对，严禁重灌** | `depends_on` 1,073 条、`participates` 178,731 条已由存量满足；重灌会边数翻倍，T07 对账直接失配。存量边不得回写 `props.batch`（改写既有数据，禁止） |
| G2 | **`research` 点与 T03 统一口径** | T02 为灌 M19 需补 `research` 端点，T03 要建全量 83,745 点。两侧必须同一源字段、同一 VID 前缀 `inst:<机构ID>`，已存在的点跳过并计数；否则会撞出重复点 |
| G3 | **新灌边打批次标记** | 新写入的 `research_coop` 边带 `props.batch=comply-<日期>-t02`，便于回滚与对账；存量边不加 |

T02 验收仍看对账单：存量已满足项回读计数 + 新灌 M19 数 vs 源表行数 + 端点缺失跳过计数 + `depends_on` 保持无环。

---

## 五、本次登记册变更

| 任务 | 变更前 | 变更后 | 说明 |
|---|---|---|---|
| `KG-COMPLY-LOAD-T01` | `ready_to_sign` | `done` | 技术验收通过，人工签收；签收前仅机械完整性检查通过，本次补业务验收结论 |
| `KG-COMPLY-LOAD-T05` | `backlog` | `done` | 技术验收通过；认领字段按分工调整后补录并注明 |
| `KG-COMPLY-LOAD-T02` | `backlog` | `ready` | 前置闸解除，待陈芸飞认领；`note` 写入 G1–G3 |

---

## 六、验收后仍需推进的事项

1. **T02 认领**：陈芸飞认领后按 G1–G3 执行，只新灌 M19。
2. **T03 / T04 开工**：前置同为 T01，现已解锁；`research` 点归属按 G2 与 T02 对齐。
3. **T06 语义去重**：处理上述 6 对历史重叠边，重点是 `apply_to` 与 `support` 的 100% 重合（实测 9,279 条同对），须判「停读一条」。
4. **T07 对账**：分母按应灌子集数，不按源表行数（`M08` 17,426 而非 2,255 万；`paper` 0 点）。
