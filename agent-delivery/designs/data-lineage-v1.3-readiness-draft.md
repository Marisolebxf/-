# D9 数据血缘规约 v1.3 增补草案 —— 指标四维就绪度模型（Readiness Model）

> **状态**：**已定稿（2026-08-01）**——项目负责人（淮政玮）放行**免会签**，规范正文已并入 `data-lineage-policy.md` §2.3（v1.3）；王惠 / 唐绍祖 / 架构师由淮政玮线下通知，异议走 v1.3.x 修订。**本文件转为决策记录存档，规范以 `data-lineage-policy.md` 为唯一真源。**
> ~~原状态：草案（DRAFT）——未生效；正式并入 `data-lineage-policy.md` 前需 王惠（口径主责）+ 唐绍祖（算法侧）+ 架构师 会签~~
> **任务**：D9-READINESS-MODEL-L01（监管人 human:淮政玮，2026-08-01 项目负责人批准建单）
> **背景决策**：2026-08-01 项目负责人在梳理评审模式角标时提出：现有单一 `mapping_status` 把「指标有没有定义」「结构算不算得出」「三方源喂不喂得饱」「当前接的是什么数据」四件事混在一个字段里，评审现场说不清责任方；决定拆为四个正交维度并配套 UI 图标字典。
> **关联**：`data-lineage-policy.md` §2/§5 · `评审模式-产品流程与状态定义.md` §5（位置字典/显隐边界，本草案不改写）· `Design.md` §7.4.1（视觉 token）· `产品定义评审规程.md` SIG-04/05

---

## 1. 四维模型定义

每个 `metric_id` 除 8 件套外，登记四个正交维度。**四维互不覆盖语义**：

```
D1 定义对齐   →  指标库里有没有这条（没有则 D2~D4 = n/a）
D2 结构支撑   →  项目自研存储设计（MySQL DWD / ES / 图）结构上算不算得出（与三方源无关）
D3 源映射     →  三方源→ETL→DWD→ES/图 全链字段级喂不喂得饱（甲方/供应方问题）
D4 接入状态   →  当前线上跑的是什么数据（运行时事实）
```

### 1.1 D1 `def_status` 指标定义对齐

| 值 | 含义 | 判定 |
|----|------|------|
| `aligned` | 已入指标库（cfg_metric 8 件套齐） | metric_id 在 seed/catalog 中且 definition/formula 非空 |
| `draft` | 已登记但口径未闭合 | 存在 `pending_ref`（Q-*）或 definition 含 pending_data_lead |
| `missing` | 指标库无此条 | UI 字段无 metric_id 或引用 GAP-* 治理占位 |

### 1.2 D2 `schema_status` 项目内结构支撑

只评估**架构师自研设计**：MySQL DWD 表结构、ES index mapping、图 schema（NebulaGraph tag/edge）。**与三方数据源无关。**

| 值 | 含义 |
|----|------|
| `ready` | 计算所需表/字段/索引/图结构全部已设计 |
| `partial` | 结构部分满足有缺陷（缺字段/缺维表/缺边类型等，须写明 gap） |
| `missing` | 结构未设计或未找到 |

按存储分述（一个指标可能 MySQL 齐而图未设计）：

```yaml
schema_status: partial
schema_detail:
  mysql_dwd: { status: ready, refs: [dwd.enterprise, dwd.enterprise_finance_history] }
  es:        { status: n/a }            # 该指标计算不经 ES
  graph:     { status: n/a }
  gap: "行业基准维表（DWS 聚合）未设计"
```

> 判定 owner：architect-agent 设计 / lineage-subcoord 核验。**未核验前必须标 `assessed: provisional`，不得伪造 ready。**

### 1.3 D3 `source_mapping_status` 三方源依赖与映射

覆盖全链：三方 ODS → GDF ETL → 项目 DWD → 灌 ES → 图谱导入，**字段级**判定。

| 值 | 含义 |
|----|------|
| `full` | 源字段完整、映射方案齐备，全链可灌 |
| `partial` | 有缺失字段/表（写明缺什么） |
| `none` | 三方源完全提供不了（如 M_ENT_MARKET_SHARE / Q019） |
| `pending_ods` | ODS 未稳定（8/20 前），暂无法判定（吸收原 ⏳ 语义） |

真源不变：GDF Mapping 报告、ODS-DWD 字段对照、`{模块}/data-gap-catalog.yaml`（`pending_ref`/`pending_hint` 仍是 ⚠️ 文案唯一来源）。

### 1.4 D4 `ingestion_status` 数据接入现状

| 值 | 含义 | UI |
|----|------|----|
| `mock` | 全 Mock 占位 | 🧪 MockBadge（现状不变，含批次+替换计划） |
| `ingesting` | 接入进行中 | 「接入中」角标 + **阶段清单**（不用百分比） |
| `live` | 真实数据全链接通 | 无角标（回归干净态） |

阶段清单（每阶段可验证、可追责，替代含糊的百分比）：

```yaml
ingestion_status: ingesting
ingestion_stages:
  ods_synced:   done          # 三方源已同步
  dwd_loaded:   done          # DWD 已灌数
  es_indexed:   in_progress   # ES 索引构建中
  graph_loaded: todo          # 图谱未导入
  verified:     todo          # QA 4 段链路核验（D9 §7.6）
as_of: "2026-08-01"
```

---

## 2. 与现有 `mapping_status` 的迁移映射

| 现值 | 迁移到 | 说明 |
|------|--------|------|
| `✅` | D3=full（+D1=aligned） | 保持 |
| `🔧` | D1=draft（若挂 Q）或 D3=partial（若缺源字段）；formula 待实现记 `formula_status` 不占四维 | **拆开**：🔧 原本混装「公式没写」和「源缺维度」 |
| `⚠️`/`🟡` | D1=draft + pending_ref | 口径待甲方 |
| `❌` | D3=none | 无源 |
| `⏳`（规约有、未落地） | D3=pending_ods | ⏳ OdsPendingBadge 不再单独实现 |

过渡期 `mapping_status` 字段**保留只读**，一个迭代周期后废弃；新增字段以 `metric-readiness-matrix-*.yaml` 为真源（§4）。

---

## 3. UI 图标字典（Arco Icon；D8 禁 emoji、不新发明颜色）

### 3.1 分层原则

- **入口层**（统计数字旁，最多 3 枚，间距 4px）：定义入口 → 数据健康 → 接入状态
- **卡内层**（ⓘ 弹卡）：8 件套 + 「就绪度」四行
- **标题旁**：仍只挂 `IconFile` 需求追溯（评审模式 §5 位置字典，不变）
- 全部包 `ReviewOnly`，业务态整组隐藏（不变）

### 3.2 入口层

| 维度/状态 | 图标 | 颜色 | 出现条件 |
|-----------|------|------|----------|
| D1 aligned / draft | `IconInfoCircle`（draft 加右上橙点） | 灰 `#86909C`，hover 蓝 `#165DFF` | 必有 |
| D1 missing | `IconQuestionCircle` | 红 `#F53F3F` | 替代 ⓘ；点开只显示治理引用 |
| D2 partial/missing | `IconStorage` | 橙 `#FF7D00` / 红 | 结构缺陷时出现（责任方=项目内） |
| D3 partial/none | `IconExclamationCircle`（沿用 ⚠️ PendingBadge） | 橙 / 红 | 源缺口时出现（责任方=甲方/供应）；文案仍读 gap catalog |
| D3 pending_ods | `IconClockCircle` | 蓝 `#165DFF` | ODS 未稳定 |
| D4 mock | `IconExperiment`（沿用 🧪） | 橙 | Mock 占位 |
| D4 ingesting | `IconSync` | 蓝 | Tooltip 展示阶段清单 |
| D4 live | 无 | — | 干净态 |

排列顺序：数字 → [ⓘ/？] → [IconStorage] → [⚠️/⏰] → [🧪/⟳]。

### 3.3 卡内层「就绪度」四行状态点

| 行状态 | 图标 | 颜色 |
|--------|------|------|
| 满足/就绪 | `IconCheckCircleFill` | 绿 `#00B42A` |
| 部分满足/有缺陷 | `IconExclamationCircleFill` | 橙 |
| 缺失/未设计/无源 | `IconCloseCircleFill` | 红 |
| 待定（pending_ods / 待核验） | `IconClockCircle` | 蓝 |
| 不适用（n/a） | `IconMinusCircle` | 灰 |

---

## 4. 真源与 Owner

| 维度 | 判定/维护 | 依据 |
|------|-----------|------|
| D1 | data-agent（口径拍板：数据 lead/甲方） | `cfg_metric-*-seed.yaml` |
| D2 | architect + data-agent；lineage-subcoord 核验 | DWD 表结构设计 / ES mapping / 图 schema 文档 |
| D3 | GDF / lineage-subcoord | Mapping 报告 / 字段对照 / `data-gap-catalog.yaml` |
| D4 | 数据工厂执行方；QA 核验 verified | 灌数记录 / 链路核验（Wave1 起 `/metrics/v1/catalog` 动态返回） |

机器真源：`agent-delivery/metrics/metric-readiness-matrix-{模块}.yaml`（本草案配套产出 ENT-EVAL 样例）。FE 只读消费，**禁止页面自填状态**。

---

## 5. 不改变的既有规则

1. 评审模式 §5 位置字典与显隐边界（IconFile↔标题 / 指标角标↔数字 / 关评审全隐藏）
2. ⚠️ 文案唯一真源 = `data-gap-catalog.yaml`（≥80 字走 Popover「数据缺口说明」）
3. `mapping_status='❌'` / D3=none 不伪造数值（业务态置灰/筹备中，不参与计分）
4. 模块复核状态（待核对/已通过）另轨表达，不用 ⚠️ 冒充
5. 业务口径决策只能甲方拍板（🟡 项登记客户决策清单）

## 6. 待会签事项（生效前必办）

- [ ] 王惠：D1/D3 枚举与判定规则口径侧确认
- [ ] 唐绍祖：D2「结构算得出」与 formula_status 关系、D4 阶段清单算法侧确认
- [ ] 架构师（徐滕强/李伟）：D2 判定权与 lineage-subcoord 核验流程确认
- [ ] 确认后：本草案并入 `data-lineage-policy.md`（bump v1.3），同步修订 `Design.md` §7.4.1「互斥」措辞为「并存排列顺序」
