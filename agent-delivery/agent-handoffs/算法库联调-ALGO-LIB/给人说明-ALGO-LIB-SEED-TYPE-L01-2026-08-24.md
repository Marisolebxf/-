# 生产派单说明 · ALGO-LIB-SEED-TYPE-L01

> **给谁**：监管人 `human:唐绍祖` 新开 **1** 个 Cursor 会话，执行 Agent = `algorithm-agent`；`data-agent` 协作枚举/缩进校验（可同会话）。  
> **日期**：2026-08-24  
> **任务状态**：`ready` · `task_type: definition` · Epic `E-ALGO-LIB-DEMO` · P0  
> **短包**：[`ALGO-LIB-SEED-TYPE-L01-派单包.md`](./ALGO-LIB-SEED-TYPE-L01-派单包.md)  
> **闸门**：`ALGO-LIB-METRIC-DEPS-L01` 已 `done`（唐绍祖 §8 类型/公式抽检 + 淮政玮签收）。`METRIC-SEED-REGISTER-L01` 已 `done`（身份在 seed，`D1=draft`，`algorithm_type=UNKNOWN`）。

本叶才把**已签**的 `algorithm_type` 与 `formula` 写入 `metrics/registry/cfg_metric-*-seed.yaml`。不算改口径。

---

## 1. 这一叶做什么

按 **metric_id 精确相交**：A1 表2 ∩ 已有 seed 行。只改这两项（缺则补键）：

- `algorithm_type`（YAML 键；表2 `API` → seed `third_party`，policy 同义）
- `formula`（写唐已签的表2 公式；骨架可写，**不**把未定权重/阈值写成可投产数）

`MODEL` / `GRAPH` / `MIXED` 的 `steps` **留在表2 / 定义卡**，不塞进 8 件套缺项、不冒充齐备。

`D1`：9 项仍不齐 → **保持 `draft`**。禁止 `UNKNOWN` 仍派实现单。禁止本叶把 `D1` 标 `aligned`。矩阵 `lifecycle_stage` 仅允许已回填行从 `open`/`identified` 升到 `formula_signed`；**禁止**改 D2/D3/D4、禁止 `kit_complete`。

### 1.1 本批相交（机器数过：表2 共 101）

表2 里正式 `M_*` **11 条**，全是企业域，这是本叶 **唯一允许改 seed 的集合**：

| metric_id | 表2 type | 回填注意 |
|---|---|---|
| `M_ENT_KEY_TOTAL` | STAT | 双阈值骨架成立；专利数/技术交易额具体值不写死（内部 🟡） |
| `M_ENT_TYPE_COUNT` | STAT | 只写类型+公式 |
| `M_ENT_DOMAIN_COVERAGE_COUNT` | STAT | 只写类型+公式 |
| `M_ENT_NEW_COUNT_Y` | STAT | 只写类型+公式 |
| `M_ENT_COMPETITIVENESS_SCORE` | MODEL | 骨架公式；不编权重 |
| `M_ENT_PAINPOINT_COUNT` | MODEL | 同上 |
| `M_ENT_SUPPLY_CHAIN_RISK` | MODEL | 同上 |
| `M_ENT_TECH_POWER_SCORE` | MODEL | `weights_status=pending_business_definition`；不冒充可投产 |
| `M_ENT_BUSINESS_POWER_SCORE` | MODEL | 骨架；不编权重 |
| `M_ENT_ATTRACTION_INDEX` | MODEL | 骨架；不编权重 |
| `M_ENT_CULTIVATION_INDEX` | MODEL | 骨架；不编权重 |

表2 另 **90 条 `TEMP_ALGO_*`**：列出「未入 seed、本叶不回填」即可。**禁止**把它们写成新 `M_*` 塞进 seed。禁止用赋号卡 `algorithm_type_suggested` 给 OPEN 新号填类型。

REGISTER 新建的 INNOV/TECH/ORG/TALENT 等号多数不在算法库 97 叶：**保持 `UNKNOWN`**，等后续 OPEN 贴源叶，不在本叶猜类型。

产业链全景 `TEMP_ALGO_ALGO-CHAIN-DEEP-117_1` 维持表2 已签 MODEL，**不入 seed、不写生产级公式/权重**。

## 2. 这一叶不做什么

| 禁止 | 原因 |
|------|------|
| 改 `definition` / 源表 / 源系统 / 更新频率 | DoD：除会签明确改公式外不改存量口径 |
| 把赋号卡 `suggested_unsigned` 当已签 | REGISTER 已写明 |
| 把 A2 `missing` 改 `mapped` | 另叶；T0-X = `ALGO-LIB-T0X-L01` |
| 写 Python / Java / 前端 | 定义叶 |
| 改 A1 双表 / xlsx / ods-gaps、改 A2 差集文件 | A2 两叶仍占 `metrics/algo-results/` |
| 开 OPEN 贴源 / GDF Sheet2 | 右框；等 T0-X 会后按桶拆 |
| PyYAML 默认 dump 覆盖 seed | REGISTER：须 `metric-registry-lib.mjs` 子集语法 |

## 3. 必读（按序）

1. 本文件 + 短包 `/goal`  
2. `metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`（表2 真源）  
3. `metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-验收教程-唐绍祖.md` §8（已签抽检）  
4. `agent-handoffs/算法库联调-ALGO-LIB/METRIC-SEED-REGISTER-L01.md`（YAML 写法、未知类型挂法）  
5. `data-lineage-policy.md` §2.1（`API`→`third_party`；`D1=aligned` 才 9 项齐）  
6. `metrics/README.md` §2.2  
7. 查 seed **只走** MCP `metric-registry`（`metric-get` / `metric-query`），禁止整文件读 `cfg_metric-*-seed.yaml` 来「看 8 件套」；写入时按 REGISTER 同语法改对应行

## 4. 交付

| 产物 | 路径 |
|------|------|
| seed 增量 | `metrics/registry/cfg_metric-ENT-seed.yaml`（上表 11 行的 type/formula） |
| 回填清单（含 skip 90） | `metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-backfill.md`（**不要**写入 `algo-results/`） |
| 解析自检 | `scripts/lib/metric-registry-lib.mjs` 能读到回填行；`algorithm_type≠UNKNOWN`（这 11 条） |
| handoff | `agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-SEED-TYPE-L01.md`（含 `ponytail: off`） |

## 5. 淮政玮 2026-08-24 内部默认（本叶遵守，不升甲方 🟢）

- 重点企业双阈值：骨架成立，具体阈值待补。  
- 技术力权重/归一化：保持 pending，不写死。  
- 表2「社会发展指标」映射纠错、MIXED 切碎、输入名尾句号：**不在本叶改 A1 表**。
