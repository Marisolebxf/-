# DEC-CHAIN-Q053 · 产业链编码归一（INB 升格为平台主键）

| 项 | 内容 |
|---|---|
| ID | `DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807` |
| 日期 | 2026-08-07 |
| 模块 | CHAIN / `CHAIN-INST-DATA-ANALYSIS-L01` |
| 决策人 | `human:李伟`（架构师，本会话确认） |
| 关联 | 客户决策清单 **Q053**；`gkx-platform-business-keys.md`；v5 DWD §3.2 |
| 状态 | **已冻结**（技术主键方案；不改对外展示文案口径） |

---

## 1. 决定摘要

| # | 结论 |
|---|---|
| D1 | **采用供应方 INB 编码作为平台业务主键**，不另造国标（C2711 等）主键体系 |
| D2 | **双字段分层**：`chain_id`/`node_id`/`industry_id` = 平台键；`chain_code`/`node_code` = ODS 贴源码；**Wave1～生产灌数默认二者同值（均为 INB 原文）** |
| D3 | **禁止**用供应方自增 `pk_id`、以及历史 Mock 国标码，作为生产跨表关联键或 Nebula VID 业务段 |
| D4 | 若甲方日后要求「国标展示/对接」，只新增 **对照表**，**不回写、不替换**已冻结的 `chain_id` |

---

## 2. 键值规则（可执行）

### 2.1 赋值（相对本轮 4 张 ODS）

| 平台字段 | 取值 | ODS 来源 |
|---|---|---|
| `industry_id`（L0） | `industry_code` 原文，如 `INB1303` | `dwd_industry_chain_info` 且 `level=0` |
| `chain_id`（L0） | 同 `industry_id`，如 `INB1303` | 同上 |
| `chain_id`（方案 B 的 L1 子链） | `industry_link_code` 原文，如 `INB130303` | `level=1` |
| `chain_code` | 与对应行 `chain_id` 同值（INB） | 贴源保留 |
| `node_id` | `industry_link_code` 原文，如 `INB13030301` | 全量节点行 |
| `node_code` | 与 `node_id` 同值 | 贴源保留 |
| `parent_node_id` | `parent_code` 原文（空=根） | 同上 |

### 2.2 Nebula VID

与 `gkx-platform-business-keys.md` / 域设计 v1 对齐：

```text
链根 vid  = chain:{chain_id}           例 chain:INB1303
节点 vid  = node:{chain_id}:{node_id}  例 node:INB1303:INB130301
```

方案 A（节点全挂 L0）时，`chain_id` 段一律用 L0 的 INB。

### 2.3 校验

1. `chain_id` / `node_id` / `industry_id` 必须匹配 `^INB[0-9]+$`（生产批次）；Mock 可用 `mock:INB*` 或 `source_system=mock` 隔离；  
2. tags / product_tags JSON 拆出的 INB 码 **原样**写入关系表，不得再映射成国标；  
3. ETL 拒绝：空码、非 INB 生产码、仅 `pk_id` 充当业务键。

---

## 3. 明确否定的方案

| 方案 | 为何否定 |
|---|---|
| 以国标产业码（C2711 等）作 `chain_id` | 本轮 4 表无国标真源；会造成无供应数据支撑的第二套主键 |
| 平台另生成 UUID/`chain:seq` 再映射 INB | 增加无必要翻译层，与 tags JSON、树形父子码断裂 |
| 混用 Mock 国标与生产 INB 做关联 | 双轨脏数据；禁止跨 `source_system` 混连 |

---

## 4. Mock / 历史数据

1. 既有 Mock 若使用国标 `chain_id`：迁移到 INB，或整批保留 `source_system=mock` 且 **不得**与生产 INB 行做外键/图谱边；  
2. 新 Mock 一律使用真实或约定的 `INB*` 形态，批次号 `mock_*`。

---

## 5. 国标对照（可选后续，不阻塞灌数）

仅当甲方书面要求国标展示或外部系统对接时，再建：

```text
industry_code_xwalk
  platform_id   -- = chain_id / industry_id（INB）
  code_system   -- 'GB' / 'OTHER'
  external_code -- 国标或外部码
  valid_from / valid_to
```

ADS/API 需要国标时读对照表，**DWD 主键仍为 INB**。

---

## 6. 落地清单

| # | 动作 | Owner |
|---|---|---|
| 1 | Q053 → 🟢，本 DEC 为决策依据 | 本会话 / 李伟 |
| 2 | 更新 `gkx-platform-business-keys.md` 中 `chain_id` 示例为 INB | architect |
| 3 | 更新 v5 §3.2、Step2「依赖 Q053」表述为已冻结 | architect |
| 4 | ETL 灌数可按 INB 启动（仍受资讯无效、Q054 等其他缺口约束） | data-agent（另派） |

---

## 7. 非目标

- 不决定门户上「产业名称」展示文案；  
- 不决定是否对甲方 UI 展示编码本身；  
- 不解决资讯/投融资无源问题（Q054 等仍独立）。
